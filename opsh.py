#!/usr/bin/env python3
"""
OpenSH - Open Natural Language Shell
Talk to your terminal in plain English.

Based on nlsh (https://github.com/junaid-mahmood/nlsh) by Junaid Mahmood

Support: https://ko-fi.com/ai_dev_2024
"""

__version__ = "0.1.1"

import signal
import os
import sys
import subprocess
import platform
import json
import webbrowser
from pathlib import Path
from datetime import datetime

# Session stats
session_start = datetime.now()
commands_run = 0

# Cross-platform readline support
if platform.system() == "Windows":
    try:
        import pyreadline3 as readline
    except ImportError:
        readline = None
else:
    import readline

def get_platform_info():
    """Get current platform details."""
    system = platform.system()
    if system == "Windows":
        return {
            "name": "Windows",
            "shell": "PowerShell",
            "home": Path.home(),
            "path_sep": "\\",
        }
    elif system == "Darwin":
        return {
            "name": "macOS",
            "shell": "zsh",
            "home": Path.home(),
            "path_sep": "/",
        }
    else:
        return {
            "name": "Linux",
            "shell": "bash",
            "home": Path.home(),
            "path_sep": "/",
        }

PLATFORM = get_platform_info()

def exit_handler(sig, frame):
    print()
    raise InterruptedError()

# Signal handling differs on Windows
if platform.system() != "Windows":
    signal.signal(signal.SIGINT, exit_handler)

script_dir = Path(__file__).parent.absolute()
env_path = script_dir / ".env"
config_path = script_dir / "config.json"

def load_config():
    """Load configuration from JSON file."""
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}

def save_config(config: dict):
    """Save configuration to JSON file."""
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

def load_env():
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value

def save_api_key(api_key: str):
    with open(env_path, "w") as f:
        f.write(f"GEMINI_API_KEY={api_key}\n")

def google_oauth_login():
    """
    Authenticate using Google OAuth via browser.
    Opens Google Cloud auth page, user signs in, grants permission.
    Returns credentials object on success, None on failure.
    """
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        import pickle
        
        creds_file = script_dir / ".google_creds.pickle"
        creds = None
        
        # Check for existing credentials
        if creds_file.exists():
            with open(creds_file, 'rb') as f:
                creds = pickle.load(f)
        
        # If credentials are valid, use them
        if creds and creds.valid:
            print("\033[32m✓ Using saved Google credentials\033[0m")
            return creds
        
        # Try to refresh expired credentials
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                with open(creds_file, 'wb') as f:
                    pickle.dump(creds, f)
                print("\033[32m✓ Refreshed Google credentials\033[0m")
                return creds
            except Exception:
                pass  # Will do full auth below
        
        # Need fresh OAuth - use Google AI Studio's OAuth
        print("\n\033[36m🌐 Opening Google Sign-in in your browser...\033[0m")
        print("\033[90m(If browser doesn't open, visit the URL shown)\033[0m\n")
        
        # Google AI's OAuth client ID (public, for AI Studio)
        # This allows users to authenticate with their Google account
        client_config = {
            "installed": {
                "client_id": "764086051850-6qr4p6gpi6hn506pt8ejuq83di341hur.apps.googleusercontent.com",
                "client_secret": "d-FL95Q19q7MQmFpd7hHD0Ty",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost", "urn:ietf:wg:oauth:2.0:oob"]
            }
        }
        
        # Scopes needed for Gemini API
        SCOPES = [
            'https://www.googleapis.com/auth/generative-language.retriever',
            'https://www.googleapis.com/auth/cloud-platform'
        ]
        
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        
        # This opens browser and waits for user to complete sign-in
        creds = flow.run_local_server(
            port=0,  # Random available port
            prompt='consent',
            success_message='✅ OpenSH authenticated! You can close this tab.'
        )
        
        # Save credentials for future use
        with open(creds_file, 'wb') as f:
            pickle.dump(creds, f)
        
        print("\033[32m✓ Successfully signed in with Google!\033[0m\n")
        return creds
        
    except ImportError as e:
        print(f"\033[31mOAuth libraries not available: {e}\033[0m")
        print("Install with: pip install google-auth-oauthlib")
        return None
    except Exception as e:
        print(f"\033[31mGoogle sign-in failed: {e}\033[0m")
        return None

def setup_api_key():
    """Set up authentication via manual API key entry."""
    print(f"\n\033[36mGet your free key at: https://aistudio.google.com/apikey\033[0m")
    print("\033[90m(Takes ~30 seconds to create)\033[0m\n")
    api_key = input("\033[33mPaste your Gemini API key:\033[0m ").strip()
    if not api_key:
        print("No API key provided.")
        return None
    save_api_key(api_key)
    os.environ["GEMINI_API_KEY"] = api_key
    
    # Save config
    config = load_config()
    config["auth_method"] = "api_key"
    save_config(config)
    
    print("\033[32m✓ API key saved!\033[0m\n")
    return api_key

def setup_authentication():
    """Interactive authentication setup - API key based."""
    print("\n\033[1m🔐 OpenSH Setup\033[0m\n")
    print("OpenSH uses Google's Gemini AI to understand your requests.")
    print("You need a \033[1mfree\033[0m API key from Google AI Studio.\n")
    print("\033[36m→ Get your key at: https://aistudio.google.com/apikey\033[0m")
    print("\033[90m  (Takes ~30 seconds - just click 'Create API Key')\033[0m\n")
    
    # Open browser to make it even easier
    open_browser = input("\033[33mOpen Google AI Studio in browser? [Y/n]:\033[0m ").strip().lower()
    if open_browser != 'n':
        import webbrowser
        webbrowser.open("https://aistudio.google.com/apikey")
        print("\n\033[90mBrowser opened. Copy your API key and paste it below.\033[0m\n")
    
    api_key = setup_api_key()
    if api_key:
        return {"api_key": api_key}
    
    return None

def get_client():
    """Get the Gemini client with appropriate authentication."""
    from google import genai
    
    config = load_config()
    auth_method = config.get("auth_method", "")
    
    # Try OAuth credentials first
    if auth_method == "oauth":
        creds_file = script_dir / ".google_creds.pickle"
        if creds_file.exists():
            import pickle
            from google.auth.transport.requests import Request
            
            with open(creds_file, 'rb') as f:
                creds = pickle.load(f)
            
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open(creds_file, 'wb') as f:
                    pickle.dump(creds, f)
            
            if creds.valid:
                return genai.Client(credentials=creds)
    
    # Fall back to API key
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return genai.Client(api_key=api_key)
    
    return None

def show_help():
    print("\033[36m!auth\033[0m      - Change authentication method")
    print("\033[36m!version\033[0m   - Show version info")
    print("\033[36m!credits\033[0m   - Show credits")
    print("\033[36m!uninstall\033[0m - Remove OpenSH")
    print("\033[36m!help\033[0m      - Show this help")
    print("\033[36m!<cmd>\033[0m     - Run command directly (bypass AI)")
    print("\033[36mexit\033[0m       - Exit OpenSH")
    print("\033[36mCtrl+C\033[0m     - Exit OpenSH")
    print()

def show_version():
    config = load_config()
    auth_method = config.get("auth_method", "not configured")
    print(f"\n\033[1mOpenSH\033[0m v{__version__}")
    print(f"Platform: {PLATFORM['name']} ({PLATFORM['shell']})")
    print(f"Auth: {auth_method}")
    print(f"Python: {platform.python_version()}")
    print(f"GitHub: https://github.com/ai-dev-2024/OpenSH")
    print()

def show_credits():
    print("\n\033[36m─────────────────────────────────────────\033[0m")
    print(f"\033[1mOpenSH\033[0m v{__version__} - Open Natural Language Shell")
    print("Based on \033[36mnlsh\033[0m by Junaid Mahmood")
    print("https://github.com/junaid-mahmood/nlsh")
    print("\n☕ Support: \033[33mhttps://ko-fi.com/ai_dev_2024\033[0m")
    print("\033[36m─────────────────────────────────────────\033[0m\n")

def show_goodbye():
    global commands_run, session_start
    duration = datetime.now() - session_start
    minutes = int(duration.total_seconds() // 60)
    seconds = int(duration.total_seconds() % 60)
    print(f"\n\033[36m─────────────────────────────────────────\033[0m")
    print(f"Session: {minutes}m {seconds}s | Commands: {commands_run}")
    print("\033[36mGoodbye! Thanks for using OpenSH ☕\033[0m")
    print("\033[36m─────────────────────────────────────────\033[0m\n")

# Initialize
load_env()

command_history = []
MAX_HISTORY = 10
MAX_CONTEXT_CHARS = 4000

def get_context_size() -> int:
    return sum(len(e["command"]) + len(e["output"]) for e in command_history)

def add_to_history(command: str, output: str = ""):
    global commands_run
    commands_run += 1
    command_history.append({
        "command": command,
        "output": output[:500] if output else ""
    })
    while len(command_history) > MAX_HISTORY:
        command_history.pop(0)
    while get_context_size() > MAX_CONTEXT_CHARS and len(command_history) > 1:
        command_history.pop(0)

def format_history() -> str:
    if not command_history:
        return "No previous commands."
    
    lines = []
    for i, entry in enumerate(command_history[-5:], 1):
        lines.append(f"{i}. $ {entry['command']}")
        if entry['output']:
            output_lines = entry['output'].strip().split('\n')[:2]
            for line in output_lines:
                lines.append(f"   {line}")
    return "\n".join(lines)

def get_command(client, user_input: str, cwd: str) -> str:
    history_context = format_history()
    
    # Platform-specific shell instructions
    if PLATFORM["name"] == "Windows":
        shell_instructions = """You are a shell command translator. Convert the user's request into a PowerShell command for Windows.
Use PowerShell cmdlets and syntax. Examples:
- List files: Get-ChildItem or dir
- Find files: Get-ChildItem -Recurse -Filter "*.py"
- Current directory: Get-Location or pwd
- Remove file: Remove-Item
- Copy file: Copy-Item
- Move file: Move-Item
- Create directory: New-Item -ItemType Directory
- View file: Get-Content or type
- Clear screen: Clear-Host or cls
- Process list: Get-Process
- Kill process: Stop-Process -Name "name"
- Network info: ipconfig, Test-NetConnection"""
    else:
        shell_instructions = f"""You are a shell command translator. Convert the user's request into a shell command for {PLATFORM['shell']} on {PLATFORM['name']}."""
    
    prompt = f"""{shell_instructions}
Current directory: {cwd}

Recent command history:
{history_context}

Rules:
- Output ONLY the command, nothing else
- No explanations, no markdown, no backticks
- If unclear, make a reasonable assumption
- Prefer simple, common commands
- Use the command history for context (e.g., "do that again", "delete the file I just created")

User request: {user_input}"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text.strip()

def is_natural_language(text: str) -> bool:
    if text.startswith("!"):
        return False
    
    # Exit commands
    if text.lower() in ["exit", "quit", "bye", "goodbye"]:
        return False
    
    # Common shell commands that should run directly
    if PLATFORM["name"] == "Windows":
        shell_commands = [
            "dir", "cls", "type", "copy", "move", "del", "md", "rd", 
            "pwd", "ls", "cat", "clear", "whoami", "date", "time",
            "ipconfig", "ping", "netstat", "nslookup", "tracert", "arp",
            "tasklist", "taskkill", "systeminfo", "hostname", "ver",
            "diskpart", "chkdsk", "format",
            "tree", "fc", "comp", "more", "sort", "find", "findstr",
            "attrib", "xcopy", "robocopy", "where", "set", "path",
        ]
        shell_starters = [
            "cd ", "cd\\", "cd/", "dir ", "echo ", "type ", 
            "copy ", "move ", "del ", "ren ", "rename ", "md ", "mkdir ",
            "rd ", "rmdir ", "attrib ", "xcopy ", "robocopy ",
            "Get-", "Set-", "New-", "Remove-", "Copy-", "Move-", "Out-",
            "Write-", "Read-", "Start-", "Stop-", "Invoke-", "Test-",
            "Select-", "Where-", "ForEach-", "Sort-", "Group-",
            "git ", "npm ", "node ", "npx ", "yarn ", "pnpm ",
            "python ", "python3 ", "py ", "pip ", "pip3 ",
            "cargo ", "rustc ", "go ", "java ", "javac ",
            "dotnet ", "nuget ",
            "curl ", "wget ", "ssh ", "scp ", "docker ", "kubectl ",
            "code ", "notepad ", "explorer ",
            "./", ".\\", "/", "\\", "~", "$", ">", ">>", "|", "&&", ";",
        ]
    else:
        shell_commands = [
            "ls", "pwd", "clear", "whoami", "date", "cal", "uptime",
            "top", "htop", "ps", "kill", "killall", "jobs", "bg", "fg",
            "cat", "head", "tail", "less", "more", "touch", "stat",
            "find", "grep", "awk", "sed", "wc", "sort", "uniq", "diff",
            "tar", "zip", "unzip", "gzip", "gunzip", "bzip2",
            "chmod", "chown", "chgrp", "id", "groups", "passwd",
            "df", "du", "free", "mount", "umount", 
            "ping", "curl", "wget", "ssh", "scp", "netstat", "ifconfig", "ip",
            "apt", "yum", "dnf", "pacman", "brew", "snap", "flatpak",
            "man", "which", "whereis", "history", "alias", "source", "export",
        ]
        shell_starters = [
            "cd ", "ls ", "ll ", 
            "cat ", "head ", "tail ", "touch ", "rm ", "cp ", "mv ",
            "mkdir ", "rmdir ", "chmod ", "chown ", "ln ",
            "echo ", "grep ", "sed ", "awk ", "cut ", "tr ", "xargs ",
            "git ", "npm ", "node ", "npx ", "yarn ", "pnpm ",
            "python ", "python3 ", "pip ", "pip3 ",
            "cargo ", "rustc ", "go ", "java ", "javac ",
            "make ", "cmake ", "gcc ", "g++ ", "clang ",
            "brew ", "apt ", "apt-get ", "yum ", "dnf ", "pacman ", "snap ",
            "sudo ", "su ", "ssh ", "scp ", "curl ", "wget ",
            "docker ", "kubectl ", "aws ", "gcloud ", "az ",
            "vi ", "vim ", "nano ", "emacs ", "code ",
            "open ", "xdg-open ",
            "export ", "source ", "alias ",
            "./", "/", "~", "$", ">", ">>", "|", "&&", ";",
        ]
    
    text_lower = text.lower()
    if text_lower in [c.lower() for c in shell_commands]:
        return False
    return not any(text.lower().startswith(s.lower()) for s in shell_starters)

def run_command(cmd: str) -> tuple:
    """Run a command and return (stdout, stderr)."""
    try:
        if PLATFORM["name"] == "Windows":
            result = subprocess.run(
                ["powershell", "-Command", cmd],
                capture_output=True, text=True, shell=False
            )
        else:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)

def main():
    # Check if first run (no auth configured)
    config = load_config()
    client = None
    
    if not config.get("auth_method"):
        # First run - show welcome and auth setup
        print("\n\033[1m🚀 Welcome to OpenSH!\033[0m")
        print("Talk to your terminal in plain English.\n")
        
        auth_result = setup_authentication()
        if not auth_result:
            print("\033[31mAuthentication required to use OpenSH.\033[0m")
            sys.exit(1)
    
    # Get client
    client = get_client()
    if not client:
        print("\033[33mNo valid authentication. Let's set it up:\033[0m")
        auth_result = setup_authentication()
        if auth_result:
            client = get_client()
    
    if not client:
        print("\033[31mCouldn't authenticate. Please try again.\033[0m")
        sys.exit(1)
    
    # Handle single command mode (-c flag)
    if args.command:
        query = ' '.join(args.command)
        cwd = os.getcwd()
        command = get_command(client, query, cwd)
        print(f"\033[33m→ {command}\033[0m")
        confirm = input("[Enter to run, or type to cancel] ").strip()
        if confirm == "":
            if command.startswith("cd "):
                path = os.path.expanduser(command[3:].strip())
                if PLATFORM["name"] == "Windows":
                    path = path.replace("/", "\\")
                try:
                    os.chdir(path)
                    print(f"Changed to: {path}")
                except Exception as e:
                    print(f"cd: {e}")
            else:
                stdout, stderr = run_command(command)
                print(stdout, end="")
                if stderr:
                    print(stderr, end="")
        return
    
    print("\033[1mOpenSH\033[0m ready! Type naturally or use !help\n")
    
    while True:
        try:
            cwd = os.getcwd()
            prompt = f"\033[32m{os.path.basename(cwd)}\033[0m > "
            user_input = input(prompt).strip()
            
            if not user_input:
                continue
            
            # Exit commands
            if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                show_goodbye()
                break
            
            # Handle cd command specially
            if user_input.startswith("cd "):
                path = os.path.expanduser(user_input[3:].strip())
                if PLATFORM["name"] == "Windows":
                    path = path.replace("/", "\\")
                try:
                    os.chdir(path)
                except Exception as e:
                    print(f"cd: {e}")
                continue
            elif user_input == "cd":
                os.chdir(Path.home())
                continue
            
            if user_input == "!auth":
                auth_result = setup_authentication()
                if auth_result:
                    client = get_client()
                    print("\033[32m✓ Authentication updated!\033[0m\n")
                continue
            
            if user_input == "!version":
                show_version()
                continue
            
            if user_input == "!uninstall":
                confirm = input("\033[33mRemove OpenSH? [y/N]\033[0m ")
                if confirm.lower() == "y":
                    import shutil
                    install_dir = Path.home() / ".opsh"
                    if PLATFORM["name"] == "Windows":
                        bin_path = Path.home() / ".opsh" / "opsh.cmd"
                    else:
                        bin_path = Path.home() / ".local" / "bin" / "opsh"
                    if install_dir.exists():
                        shutil.rmtree(install_dir)
                    if bin_path.exists():
                        os.remove(bin_path)
                    print("\033[32m✓ OpenSH uninstalled\033[0m")
                    sys.exit(0)
                continue
            
            if user_input == "!help":
                show_help()
                continue
            
            if user_input == "!credits":
                show_credits()
                continue
            
            if user_input.startswith("!"):
                cmd = user_input[1:]
                if not cmd:
                    continue
                stdout, stderr = run_command(cmd)
                print(stdout, end="")
                if stderr:
                    print(stderr, end="")
                add_to_history(cmd, stdout + stderr)
                continue
            
            if not is_natural_language(user_input):
                stdout, stderr = run_command(user_input)
                print(stdout, end="")
                if stderr:
                    print(stderr, end="")
                add_to_history(user_input, stdout + stderr)
                continue
            
            command = get_command(client, user_input, cwd)
            confirm = input(f"\033[33m→ {command}\033[0m [Enter] ")
            
            if confirm == "":
                if command.startswith("cd "):
                    path = os.path.expanduser(command[3:].strip())
                    if PLATFORM["name"] == "Windows":
                        path = path.replace("/", "\\")
                    try:
                        os.chdir(path)
                    except Exception as e:
                        print(f"cd: {e}")
                else:
                    stdout, stderr = run_command(command)
                    print(stdout, end="")
                    if stderr:
                        print(stderr, end="")
                    add_to_history(command, stdout + stderr)
            
        except (EOFError, KeyboardInterrupt):
            show_goodbye()
            break
        except InterruptedError:
            continue
        except Exception as e:
            err = str(e)
            if "429" in err or "quota" in err.lower():
                print("\033[31mRate limit hit - wait a moment and try again\033[0m")
            elif "API_KEY" in err or "api_key" in err or "authentication" in err.lower():
                print("\033[31mAuth error - run !auth to update your credentials\033[0m")
            elif "InterruptedError" not in err and "KeyboardInterrupt" not in err:
                print(f"\033[31mError: {err[:100]}\033[0m")

if __name__ == "__main__":
    main()
