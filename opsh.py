#!/usr/bin/env python3
"""
OpenSH - Open Natural Language Shell
Talk to your terminal in plain English.

Based on nlsh (https://github.com/junaid-mahmood/nlsh) by Junaid Mahmood

Support: https://ko-fi.com/ai_dev_2024
"""

__version__ = "1.0.0"

import signal
import os
import sys
import subprocess
import platform
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

def setup_api_key():
    print(f"\n\033[36mGet your free key at: https://aistudio.google.com/apikey\033[0m\n")
    api_key = input("\033[33mEnter your Gemini API key:\033[0m ").strip()
    if not api_key:
        print("No API key provided.")
        sys.exit(1)
    save_api_key(api_key)
    os.environ["GEMINI_API_KEY"] = api_key
    print("\033[32m✓ API key saved!\033[0m\n")

def show_help():
    print("\033[36m!api\033[0m       - Change API key")
    print("\033[36m!version\033[0m   - Show version info")
    print("\033[36m!credits\033[0m   - Show credits")
    print("\033[36m!uninstall\033[0m - Remove OpenSH")
    print("\033[36m!help\033[0m      - Show this help")
    print("\033[36m!<cmd>\033[0m     - Run command directly (bypass AI)")
    print("\033[36mexit\033[0m       - Exit OpenSH")
    print("\033[36mCtrl+C\033[0m     - Exit OpenSH")
    print()

def show_version():
    print(f"\n\033[1mOpenSH\033[0m v{__version__}")
    print(f"Platform: {PLATFORM['name']} ({PLATFORM['shell']})")
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

load_env()

first_run = not os.getenv("GEMINI_API_KEY")
if first_run:
    setup_api_key()
    print("\033[1mOpenSH\033[0m - talk to your terminal\n")
    show_help()

from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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

def get_command(user_input: str, cwd: str) -> str:
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
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text.strip()

def is_natural_language(text: str) -> bool:
    if text.startswith("!"):
        return False
    
    # Exit commands - always natural language to trigger exit
    if text.lower() in ["exit", "quit", "bye", "goodbye"]:
        return False
    
    # Common shell commands that should run directly
    if PLATFORM["name"] == "Windows":
        # Windows/PowerShell commands - comprehensive list
        shell_commands = [
            # Basic commands
            "dir", "cls", "type", "copy", "move", "del", "md", "rd", 
            "pwd", "ls", "cat", "clear", "whoami", "date", "time",
            # Network
            "ipconfig", "ping", "netstat", "nslookup", "tracert", "arp",
            # System
            "tasklist", "taskkill", "systeminfo", "hostname", "ver",
            # Disk
            "diskpart", "chkdsk", "format",
            # Other
            "tree", "fc", "comp", "more", "sort", "find", "findstr",
            "attrib", "xcopy", "robocopy", "where", "set", "path",
        ]
        shell_starters = [
            # Basic navigation
            "cd ", "cd\\", "cd/", "dir ", "echo ", "type ", 
            # File operations
            "copy ", "move ", "del ", "ren ", "rename ", "md ", "mkdir ",
            "rd ", "rmdir ", "attrib ", "xcopy ", "robocopy ",
            # PowerShell cmdlets
            "Get-", "Set-", "New-", "Remove-", "Copy-", "Move-", "Out-",
            "Write-", "Read-", "Start-", "Stop-", "Invoke-", "Test-",
            "Select-", "Where-", "ForEach-", "Sort-", "Group-",
            # Development tools
            "git ", "npm ", "node ", "npx ", "yarn ", "pnpm ",
            "python ", "python3 ", "py ", "pip ", "pip3 ",
            "cargo ", "rustc ", "go ", "java ", "javac ",
            "dotnet ", "nuget ",
            # Other tools
            "curl ", "wget ", "ssh ", "scp ", "docker ", "kubectl ",
            "code ", "notepad ", "explorer ",
            # Operators and paths
            "./", ".\\", "/", "\\", "~", "$", ">", ">>", "|", "&&", ";",
        ]
    else:
        # Unix commands - comprehensive list
        shell_commands = [
            # Basic
            "ls", "pwd", "clear", "whoami", "date", "cal", "uptime",
            # Process
            "top", "htop", "ps", "kill", "killall", "jobs", "bg", "fg",
            # Files
            "cat", "head", "tail", "less", "more", "touch", "stat",
            # Search
            "find", "grep", "awk", "sed", "wc", "sort", "uniq", "diff",
            # Compression
            "tar", "zip", "unzip", "gzip", "gunzip", "bzip2",
            # User/permissions
            "chmod", "chown", "chgrp", "id", "groups", "passwd",
            # System
            "df", "du", "free", "mount", "umount", 
            # Network
            "ping", "curl", "wget", "ssh", "scp", "netstat", "ifconfig", "ip",
            # Package managers
            "apt", "yum", "dnf", "pacman", "brew", "snap", "flatpak",
            # Other
            "man", "which", "whereis", "history", "alias", "source", "export",
        ]
        shell_starters = [
            # Navigation
            "cd ", "ls ", "ll ", 
            # File ops
            "cat ", "head ", "tail ", "touch ", "rm ", "cp ", "mv ",
            "mkdir ", "rmdir ", "chmod ", "chown ", "ln ",
            # Text processing
            "echo ", "grep ", "sed ", "awk ", "cut ", "tr ", "xargs ",
            # Development
            "git ", "npm ", "node ", "npx ", "yarn ", "pnpm ",
            "python ", "python3 ", "pip ", "pip3 ",
            "cargo ", "rustc ", "go ", "java ", "javac ",
            "make ", "cmake ", "gcc ", "g++ ", "clang ",
            # Package managers
            "brew ", "apt ", "apt-get ", "yum ", "dnf ", "pacman ", "snap ",
            # Other
            "sudo ", "su ", "ssh ", "scp ", "curl ", "wget ",
            "docker ", "kubectl ", "aws ", "gcloud ", "az ",
            "vi ", "vim ", "nano ", "emacs ", "code ",
            "open ", "xdg-open ",
            "export ", "source ", "alias ",
            # Operators and paths
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
            # Use PowerShell on Windows
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
    global client
    
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
            
            # Handle cd command specially (works in-process)
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
            
            if user_input == "!api":
                setup_api_key()
                client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
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
            
            command = get_command(user_input, cwd)
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
                print("\033[31mAPI key error - run !api to update your key\033[0m")
            elif "InterruptedError" not in err and "KeyboardInterrupt" not in err:
                print(f"\033[31mError: {err[:100]}\033[0m")

if __name__ == "__main__":
    main()
