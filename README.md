# 🚀 OpenSH - Open Natural Language Shell

<div align="center">

![OpenSH Banner](https://img.shields.io/badge/OpenSH-Natural%20Language%20Shell-4285F4?style=for-the-badge&logo=google&logoColor=white)

[![Version](https://img.shields.io/badge/version-0.0.1-blue?style=flat-square)](CHANGELOG.md)
[![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat-square&logo=windows&logoColor=white)](https://github.com/ai-dev-2024/OpenSH)
[![macOS](https://img.shields.io/badge/macOS-000000?style=flat-square&logo=apple&logoColor=white)](https://github.com/ai-dev-2024/OpenSH)
[![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)](https://github.com/ai-dev-2024/OpenSH)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![CI](https://github.com/ai-dev-2024/OpenSH/actions/workflows/ci.yml/badge.svg)](https://github.com/ai-dev-2024/OpenSH/actions)

**Talk to your terminal in plain English.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Changelog](CHANGELOG.md) • [Support](#-support)

</div>

---

## ✨ Features

- 🌍 **Multi-Platform** - Works on Windows, macOS, and Linux
- 🤖 **AI-Powered** - Uses Google Gemini to understand natural language
- ⚡ **Smart Detection** - Recognizes shell commands and runs them directly
- 🔄 **Context-Aware** - Remembers your command history for better suggestions
- 💻 **Platform-Native** - Generates PowerShell on Windows, bash/zsh on Unix

## 📦 Installation

### Prerequisites

- **Python 3.8+** installed
- A **free Google Gemini API key** from [Google AI Studio](https://aistudio.google.com/apikey)

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
<summary><b>One-liner install (after GitHub release)</b></summary>

**Windows:**
```powershell
irm https://raw.githubusercontent.com/ai-dev-2024/OpenSH/main/install.ps1 | iex
```

**macOS/Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/ai-dev-2024/OpenSH/main/install.sh | bash
```

</details>

## 🚀 Usage

```bash
opsh
```

On first run, you'll be prompted to enter your **free Gemini API key**.

### Natural Language Examples

| You type | OpenSH generates |
|----------|------------------|
| `list all python files` | `Get-ChildItem *.py` (Win) / `find . -name "*.py"` (Unix) |
| `show disk space` | `Get-PSDrive C` (Win) / `df -h` (Unix) |
| `git commit with message fixed bug` | `git commit -m "fixed bug"` |
| `find large files over 100MB` | Appropriate command for your OS |

### Commands

| Command | Description |
|---------|-------------|
| `!api` | Change API key |
| `!help` | Show help |
| `!credits` | Show credits |
| `!<cmd>` | Run command directly |
| `Ctrl+C` | Exit |

## 🔧 How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  You type   │ ──► │   Gemini AI  │ ──► │   Command   │
│  naturally  │     │  translates  │     │   executes  │
└─────────────┘     └──────────────┘     └─────────────┘
```

1. Type a natural language request
2. OpenSH sends it to Gemini AI with platform context
3. Review the suggested command
4. Press Enter to execute (or type something else to cancel)

**Note:** Direct shell commands (like `cd`, `ls`, `dir`, `git`) bypass AI and run immediately.

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

If you find OpenSH useful, consider supporting the project:

<a href="https://ko-fi.com/ai_dev_2024">
  <img src="https://img.shields.io/badge/☕_Buy_me_a_coffee-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white" alt="Ko-fi"/>
</a>

---

## 📜 Credits

OpenSH is based on [**nlsh**](https://github.com/junaid-mahmood/nlsh) by Junaid Mahmood.

---

<div align="center">
<sub>Made with ❤️ for the command line</sub>
</div>
