# OpenSH - Windows PowerShell Installer
# Based on nlsh (https://github.com/junaid-mahmood/nlsh)
# Support: https://ko-fi.com/ai_dev_2024

$ErrorActionPreference = "Stop"

$INSTALL_DIR = "$env:USERPROFILE\.opsh"
$REPO_URL = "https://github.com/YOUR_USERNAME/OpenSH.git"  # TODO: Update with your repo

Write-Host "Installing OpenSH..." -ForegroundColor Cyan

# Check for Python
$pythonCmd = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $version = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0 -and $version -match "Python 3") {
            $pythonCmd = $cmd
            break
        }
    }
    catch {}
}

if (-not $pythonCmd) {
    Write-Host "Python 3 is required. Please install it from https://python.org" -ForegroundColor Red
    exit 1
}

Write-Host "Found $($pythonCmd): $((& $pythonCmd --version 2>&1))" -ForegroundColor Gray

# Clone or update repository
if (Test-Path $INSTALL_DIR) {
    Write-Host "Updating existing installation..." -ForegroundColor Yellow
    Push-Location $INSTALL_DIR
    try {
        git pull --quiet 2>&1 | Out-Null
    }
    catch {
        Write-Host "Warning: Could not update from git. Continuing with existing files." -ForegroundColor Yellow
    }
    Pop-Location
}
else {
    Write-Host "Downloading OpenSH..." -ForegroundColor Cyan
    
    # Try git clone first, fall back to copying local files if in development
    $scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
    if (Test-Path "$scriptPath\opsh.py") {
        # Local installation (development mode)
        Write-Host "Installing from local directory..." -ForegroundColor Gray
        New-Item -ItemType Directory -Path $INSTALL_DIR -Force | Out-Null
        Copy-Item "$scriptPath\opsh.py" "$INSTALL_DIR\" -Force
        Copy-Item "$scriptPath\requirements.txt" "$INSTALL_DIR\" -Force
        if (Test-Path "$scriptPath\.env") {
            Copy-Item "$scriptPath\.env" "$INSTALL_DIR\" -Force
        }
    }
    else {
        # Remote installation
        try {
            git clone --quiet $REPO_URL $INSTALL_DIR 2>&1 | Out-Null
        }
        catch {
            Write-Host "Failed to clone repository. Please check your internet connection." -ForegroundColor Red
            exit 1
        }
    }
}

Push-Location $INSTALL_DIR

# Create Python virtual environment
Write-Host "Setting up Python environment..." -ForegroundColor Cyan
& $pythonCmd -m venv venv

# Activate venv and install dependencies
$venvPython = "$INSTALL_DIR\venv\Scripts\python.exe"
$venvPip = "$INSTALL_DIR\venv\Scripts\pip.exe"

& $venvPip install --upgrade pip 2>&1 | Where-Object { $_ -notmatch "^\s*$" } | Out-Null
& $venvPip install google-genai pyreadline3 2>&1 | Where-Object { $_ -notmatch "^\s*$" } | Out-Null

Pop-Location

# Create launcher batch file
Write-Host "Creating opsh command..." -ForegroundColor Cyan

$launcherContent = @"
@echo off
call "$INSTALL_DIR\venv\Scripts\activate.bat"
python "$INSTALL_DIR\opsh.py" %*
"@

$launcherPath = "$INSTALL_DIR\opsh.cmd"
Set-Content -Path $launcherPath -Value $launcherContent -Encoding ASCII

# Add to PATH if not already there
$userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($userPath -notlike "*$INSTALL_DIR*") {
    Write-Host "Adding OpenSH to PATH..." -ForegroundColor Cyan
    [Environment]::SetEnvironmentVariable("PATH", "$INSTALL_DIR;$userPath", "User")
    $env:PATH = "$INSTALL_DIR;$env:PATH"
}

# Optionally add to PowerShell profile for auto-start
$profilePath = $PROFILE.CurrentUserAllHosts
$autoStartLine = "# OpenSH auto-start (remove to disable)`nif (Test-Path `"$launcherPath`") { & `"$launcherPath`" }"

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  OpenSH installed successfully!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "To start using OpenSH:" -ForegroundColor Cyan
Write-Host "  1. Open a NEW PowerShell/Terminal window" -ForegroundColor White
Write-Host "  2. Type: opsh" -ForegroundColor Yellow
Write-Host ""
Write-Host "Or run it now:" -ForegroundColor Cyan
Write-Host "  & `"$launcherPath`"" -ForegroundColor Yellow
Write-Host ""
Write-Host "Based on nlsh by Junaid Mahmood" -ForegroundColor DarkGray
Write-Host "Support: https://ko-fi.com/ai_dev_2024" -ForegroundColor DarkGray
Write-Host ""
