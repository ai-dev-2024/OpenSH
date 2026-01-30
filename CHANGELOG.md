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

## [0.1.1] - 2026-01-30

### Added
- **Quick query mode** (`-c` flag) - Execute single commands from any terminal
- **`ask` function** in PowerShell - Quick natural language queries
- **Auto-launch message** - OpenSH ready notification on new terminals
- **Browser auto-open** - Opens Google AI Studio during setup

### Fixed
- Removed Google OAuth (was blocked by Google's unverified app policy)
- Simplified to API key only - more reliable

### Changed
- Setup now opens browser automatically for easier API key creation

---

## [0.1.0] - 2026-01-30

### Added
- Interactive authentication menu on first launch
- `!auth` command to change API key anytime
- JSON-based config storage for auth preferences

### Changed
- Version bump to 0.1.0 (significant new feature)
- Improved first-run experience with welcome message
- Renamed `!api` to `!auth` for clarity

---

## [0.0.2] - 2026-01-30

### Added
- **Authentication menu** - Choose between API key and Google OAuth (API key works now, OAuth coming soon)
- **google-auth-oauthlib** dependency for future OAuth support
- **Improved first-run experience** with cleaner setup flow

### Security
- Added `.auth_method`, `.google_creds.pickle`, and `client_secret.json` to `.gitignore`
- Credentials are never committed to the repository

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
| 0.1.1 | 2026-01-30 | Quick query mode, `ask` function, simplified auth |
| 0.1.0 | 2026-01-30 | Auth menu, config storage |
| 0.0.2 | 2026-01-30 | Authentication improvements |
| 0.0.1 | 2026-01-30 | Initial multi-platform release |

---

[Unreleased]: https://github.com/ai-dev-2024/OpenSH/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/ai-dev-2024/OpenSH/releases/tag/v0.1.1
[0.1.0]: https://github.com/ai-dev-2024/OpenSH/releases/tag/v0.1.0
[0.0.2]: https://github.com/ai-dev-2024/OpenSH/releases/tag/v0.0.2
[0.0.1]: https://github.com/ai-dev-2024/OpenSH/releases/tag/v0.0.1
