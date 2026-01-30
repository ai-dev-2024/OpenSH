# Changelog

All notable changes to OpenSH will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Auto-execute mode (`-y` flag)
- Command aliases
- Customizable AI model selection

---

## [0.0.1] - 2026-01-30

### Added
- **Multi-platform support** - Works on Windows, macOS, and Linux
- **Cross-platform Python script** (`opsh.py`) with platform detection
- **Windows PowerShell installer** (`install.ps1`)
- **Unix bash installer** (`install.sh`)
- **AI-powered command translation** using Google Gemini API
- **Smart command detection** - 50+ shell commands bypass AI for direct execution
- **Command history context** - AI uses recent commands for better suggestions
- **Session statistics** - Shows commands run and session duration on exit
- **Built-in commands**:
  - `!api` - Change/update Gemini API key
  - `!version` - Show version and platform info
  - `!credits` - Show attribution and support links
  - `!help` - Show available commands
  - `!uninstall` - Remove OpenSH
  - `exit` / `quit` / `bye` - Exit with session summary
- **GitHub Actions CI** - Automated testing on Windows, macOS, Linux

### Credits
- Based on [nlsh](https://github.com/junaid-mahmood/nlsh) by Junaid Mahmood

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 0.0.1 | 2026-01-30 | Initial release with multi-platform support |

---

[Unreleased]: https://github.com/ai-dev-2024/OpenSH/compare/v0.0.1...HEAD
[0.0.1]: https://github.com/ai-dev-2024/OpenSH/releases/tag/v0.0.1
