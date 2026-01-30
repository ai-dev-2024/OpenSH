# OpenSH - Open Natural Language Shell

Talk to your terminal in plain English. Works on **Windows**, **macOS**, and **Linux**.

> Powered by Google Gemini AI

## Install

### Windows (PowerShell)

```powershell
# Download and run the installer
irm https://raw.githubusercontent.com/YOUR_USERNAME/OpenSH/main/install.ps1 | iex
```

Or manually:
```powershell
git clone https://github.com/YOUR_USERNAME/OpenSH.git
cd OpenSH
.\install.ps1
```

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/OpenSH/main/install.sh | bash
```

## Uninstall

### Windows
```powershell
irm https://raw.githubusercontent.com/YOUR_USERNAME/OpenSH/main/uninstall.ps1 | iex
```

### macOS / Linux
```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/OpenSH/main/uninstall.sh | bash
```

## Usage

```bash
opsh
```

Type naturally:
- `list all python files` → `Get-ChildItem *.py` (Windows) / `find . -name "*.py"` (Unix)
- `git commit with message fixed bug` → `git commit -m "fixed bug"`
- `show disk usage` → `Get-PSDrive C` (Windows) / `df -h` (Unix)
- `find large files` → appropriate command for your OS

### Commands
| Command | Description |
|---------|-------------|
| `!api` | Change API key |
| `!help` | Show help |
| `!credits` | Show credits |
| `!cmd` | Run command directly (bypass AI) |
| `Ctrl+C` | Exit |

### Examples

```
Desktop > list all text files
→ Get-ChildItem -Filter *.txt [Enter]

file1.txt
file2.txt

Desktop > show me the contents of file1.txt
→ Get-Content file1.txt [Enter]

Hello, world!

Desktop > delete that file
→ Remove-Item file1.txt [Enter]
```

## Requirements

- Python 3.8+
- A free Google Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

## How It Works

1. You type a natural language request
2. OpenSH uses Gemini AI to translate it to a shell command
3. You review and confirm the command (press Enter)
4. The command runs

Direct shell commands (like `cd`, `ls`, `dir`, `git`) are passed through without AI translation.

---

## Credits

OpenSH is based on [nlsh](https://github.com/junaid-mahmood/nlsh) by **Junaid Mahmood**.

### Support

If you find OpenSH useful, consider buying me a coffee:

☕ **[ko-fi.com/ai_dev_2024](https://ko-fi.com/ai_dev_2024)**

---

## License

MIT License - see [LICENSE](LICENSE)
