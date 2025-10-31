# Install GitHub CLI on Windows
# Run this script as Administrator

Write-Host "Installing GitHub CLI..." -ForegroundColor Green

# Method 1: Try winget (requires user confirmation)
Write-Host "`n[Option 1] Installing via winget..." -ForegroundColor Yellow
try {
    winget install --id GitHub.cli --accept-source-agreements
    Write-Host "✓ GitHub CLI installed via winget" -ForegroundColor Green
    exit 0
}
catch {
    Write-Host "✗ Winget installation failed" -ForegroundColor Red
}

# Method 2: Download and install MSI
Write-Host "`n[Option 2] Downloading installer..." -ForegroundColor Yellow
$installerPath = "$env:TEMP\gh_installer.msi"
$downloadUrl = "https://github.com/cli/cli/releases/download/v2.40.0/gh_2.40.0_windows_amd64.msi"

try {
    Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath
    Write-Host "✓ Installer downloaded to $installerPath" -ForegroundColor Green

    Write-Host "`nInstalling GitHub CLI..." -ForegroundColor Yellow
    Start-Process msiexec.exe -ArgumentList "/i `"$installerPath`" /quiet /qn /norestart" -Wait -NoNewWindow

    Write-Host "✓ GitHub CLI installed!" -ForegroundColor Green
    Write-Host "`nNext step: Restart your terminal and run:" -ForegroundColor Cyan
    Write-Host "  gh auth login" -ForegroundColor White
}
catch {
    Write-Host "✗ Installation failed: $_" -ForegroundColor Red
    Write-Host "`nManual installation:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://cli.github.com/" -ForegroundColor White
    Write-Host "2. Run the installer" -ForegroundColor White
    Write-Host "3. Restart terminal" -ForegroundColor White
    Write-Host "4. Run: gh auth login" -ForegroundColor White
}
