# 🚀 OpenSH

<div align="center">

![OpenSH Banner](https://capsule-render.vercel.app/api?type=waving&color=0:8b5cf6,100:ec4899&height=250&section=header&text=OpenSH&fontSize=80&animation=fadeIn&fontAlignY=35&desc=Your%20Terminal,%20Conversational.&descSize=25&descAlignY=55&fontColor=ffffff)

[![Website](https://img.shields.io/badge/🌐_Website-opensh.vercel.app-7c3aed?style=for-the-badge&logo=vercel&logoColor=white)](https://opensh.vercel.app)
[![Version](https://img.shields.io/github/v/release/ai-dev-2024/OpenSH?style=for-the-badge&color=ec4899)](https://github.com/ai-dev-2024/OpenSH/releases)
[![License](https://img.shields.io/github/license/ai-dev-2024/OpenSH?style=for-the-badge&color=22c55e)](LICENSE)

**[Installation](#-installation)** • **[Features](#-features)** • **[Configuration](#-configuration)**

---

<a href="https://ko-fi.com/ai_dev_2024">
  <img src="https://img.shields.io/badge/☕_Support_on_Ko--fi-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white" height="35" alt="Support on Ko-fi"/>
</a>

</div>

## 🔮 What is OpenSH?

**OpenSH** transforms your terminal into a natural language interface. Instead of memorizing complex flags and syntax for `find`, `grep`, `ffmpeg`, or `git`, just **say what you want**.

> "Find all large video files over 1GB in my downloads folder"  
> "Convert this video to mp4 and lower the bitrate"  
> "Git commit all changes with message 'update readme'"

OpenSH translates your intent into the correct command for your OS (Windows, macOS, or Linux), explains it, and executes it.

## ✨ Features

| Feature | Description |
| :--- | :--- |
| 🗣️ **Conversational** | Speaks your language. No more `tar -xvf`. |
| ⚡ **Auto-Run** | Generates, explains, and runs commands instanty. |
| 🧠 **Smart Context** | Sees your current files to give accurate suggestions. |
| 🔁 **Cross-Platform** | Native PowerShell for Windows, Bash/Zsh for Unix. |
| 🛡️ **Safety First** | User confirmation for destructive commands. |
| 🚀 **Zero Config** | Works out of the box with free API tiers. |

## 📦 Installation

### Windows (PowerShell)
Paste this into your terminal:
```powershell
irm https://raw.githubusercontent.com/ai-dev-2024/OpenSH/main/install.ps1 | iex
```

### macOS / Linux
One-line install:
```bash
curl -fsSL https://raw.githubusercontent.com/ai-dev-2024/OpenSH/main/install.sh | bash
```

## 🎮 Usage

OpenSH launches automatically with your terminal (if configured) or by typing `opsh`.

```text
C:\Users\You> find large node_modules folders
🔍 Thinking...
→ Get-ChildItem -Recurse -Directory -Filter "node_modules"
```

### Examples

**File Management**
- "Delete all temp files in this folder"
- "Organize these photos by date"

**Git Operations**
- "Undo the last commit but keep changes"
- "Push to main branch"

**System**
- "Kill the process using port 3000"
- "Show my IP address"

## ⚙️ Configuration

OpenSH uses a `config.json` file located in `~/.opsh/`. You can edit it to change your preferred model provider (Groq or Gemini) or API keys.

```json
{
  "provider": "groq",
  "api_key": "your_key_here"
}
```

## 🤝 Contributing

We welcome contributions! Please check out the issues or submit a PR.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
  <p>Made with ❤️ by the AI Dev Team</p>
</div>
