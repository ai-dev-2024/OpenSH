# 🚀 OpenSH - Natural Language Shell

<div align="center">

<!-- Banner -->
![OpenSH](https://img.shields.io/badge/🚀_OpenSH-Natural_Language_Shell-667eea?style=for-the-badge&labelColor=764ba2)

[![Version](https://img.shields.io/badge/version-0.2.0-blue?style=flat-square)](CHANGELOG.md)
[![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat-square&logo=windows&logoColor=white)](#-installation)
[![macOS](https://img.shields.io/badge/macOS-000000?style=flat-square&logo=apple&logoColor=white)](#-installation)
[![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)](#-installation)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![CI](https://github.com/ai-dev-2024/OpenSH/actions/workflows/ci.yml/badge.svg)](https://github.com/ai-dev-2024/OpenSH/actions)

### 💬 Talk to your terminal in plain English

**Stop memorizing commands. Just describe what you want.**

[![Website](https://img.shields.io/badge/🌐_Website-opsh.vercel.app-667eea?style=flat-square)](https://opsh-lemon.vercel.app)

[Features](#-features) • [Quick Start](#-quick-start) • [Examples](#-examples) • [Support](#-support)

---

<a href="https://ko-fi.com/ai_dev_2024">
  <img src="https://img.shields.io/badge/☕_Support_this_project-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white" alt="Ko-fi"/>
</a>

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 **Natural Language** | Type what you want in plain English - no command memorization needed |
| ⚡ **Auto-Execute** | Commands run automatically - see the translation, learn as you go |
| 🌍 **Cross-Platform** | Works on Windows, macOS, and Linux with platform-native commands |
| 🚀 **Auto-Start** | Opens automatically with every new terminal (configurable) |
| 📁 **Context-Aware** | Sees your files and folders to generate accurate commands |
| 🆓 **100% Free** | Uses Groq or Gemini free API tier - no paid subscription needed |

---

## 🎬 How It Works

```
You type:  "show all python files on desktop"
    ↓
OpenSH:    → Get-ChildItem "$env:USERPROFILE\Desktop" -Filter "*.py"
    ↓
Output:    (files listed...)
```

**You learn the real commands while getting work done!**

---

## 📦 Quick Start

### Prerequisites
- **Python 3.8+** installed
- Free API key from [Groq](https://console.groq.com) (recommended) or [Google AI Studio](https://aistudio.google.com/apikey)

### Windows (PowerShell)

```powershell
git clone https://github.com/ai-dev-2024/OpenSH.git
cd OpenSH
.\install.ps1
```

### macOS / Linux

```bash
git clone https://github.com/ai-dev-2024/OpenSH.git
cd OpenSH
bash install.sh
```

<details>
<summary><b>🚀 One-liner install</b></summary>

**Windows:**
```powershell
irm https://raw.githubusercontent.com/ai-dev-2024/OpenSH/main/install.ps1 | iex
```

**macOS/Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/ai-dev-2024/OpenSH/main/install.sh | bash
```

</details>

---

## 💡 Examples

### File Operations
| You say | OpenSH runs |
|---------|-------------|
| `show all python files` | `Get-ChildItem -Recurse -Filter "*.py"` |
| `find large files over 100MB` | `Get-ChildItem -Recurse \| Where-Object {$_.Length -gt 100MB}` |
| `delete all temp files` | `Remove-Item *.tmp` |
| `copy resume to desktop` | `Copy-Item resume.pdf $env:USERPROFILE\Desktop` |

### Navigation
| You say | OpenSH runs |
|---------|-------------|
| `go to the desktop` | `Set-Location "$env:USERPROFILE\Desktop"` |
| `what folder am I in` | `Get-Location` |
| `show what's in this folder` | `Get-ChildItem` |

### System
| You say | OpenSH runs |
|---------|-------------|
| `show running processes` | `Get-Process` |
| `how much disk space` | `Get-PSDrive C` |
| `what's my IP address` | `ipconfig` |

### Git
| You say | OpenSH runs |
|---------|-------------|
| `commit with message fixed bug` | `git commit -m "fixed bug"` |
| `push to main` | `git push origin main` |
| `show recent commits` | `git log -n 5 --oneline` |

---

## ⌨️ Commands

| Command | Description |
|---------|-------------|
| `!auth` | Change API provider/key |
| `!help` | Show help |
| `!credits` | Show credits |
| `!<cmd>` | Run command directly (bypass AI) |
| `exit` | Exit OpenSH |

---

## 🔧 Configuration

After installation, OpenSH **auto-starts** with every new terminal. To disable:

**Windows:** Remove the OpenSH section from your PowerShell profile:
```powershell
notepad $PROFILE
```

**Linux/macOS:** Remove from `~/.bashrc` or `~/.zshrc`

---

## 🗑️ Uninstall

### Windows
```powershell
.\uninstall.ps1
```

### macOS / Linux
```bash
bash uninstall.sh
```

---

## 💖 Support

If OpenSH saves you time, consider supporting the project:

<a href="https://ko-fi.com/ai_dev_2024">
  <img src="https://img.shields.io/badge/☕_Buy_me_a_coffee-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white" alt="Ko-fi"/>
</a>

**Other ways to support:**
- ⭐ Star this repository
- 🐛 Report bugs or suggest features
- 📢 Share with friends

---

## 📜 Credits

OpenSH is inspired by [**nlsh**](https://github.com/junaid-mahmood/nlsh) by Junaid Mahmood.

---

<div align="center">

**Made with ❤️ for people who hate memorizing commands**

[![GitHub stars](https://img.shields.io/github/stars/ai-dev-2024/OpenSH?style=social)](https://github.com/ai-dev-2024/OpenSH)

</div>
