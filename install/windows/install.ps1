param(
  [string]$PyzPath = ""
)

$ErrorActionPreference = "Stop"

function Resolve-PyzPath {
  param([string]$PathInput)
  if ($PathInput -and (Test-Path $PathInput)) {
    return (Resolve-Path $PathInput).Path
  }
  $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
  $defaultPyz = Join-Path $scriptDir "..\\..\\dist\\cli\\aethercore-installer.pyz"
  if (Test-Path $defaultPyz) {
    return (Resolve-Path $defaultPyz).Path
  }
  throw "PYZ not found. Pass -PyzPath or build first."
}

$pyz = Resolve-PyzPath -PathInput $PyzPath
$installRoot = Join-Path $env:LOCALAPPDATA "AetherCoreInstaller"
$binDir = Join-Path $installRoot "bin"

New-Item -ItemType Directory -Force -Path $installRoot | Out-Null
New-Item -ItemType Directory -Force -Path $binDir | Out-Null

Copy-Item -Force $pyz (Join-Path $installRoot "aethercore-installer.pyz")

$cmdPath = Join-Path $binDir "aethercore-installer.cmd"
@"
@echo off
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 "%~dp0..\\aethercore-installer.pyz" %*
) else (
  python "%~dp0..\\aethercore-installer.pyz" %*
)
"@ | Set-Content -Encoding ASCII -Path $cmdPath

$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -notlike "*$binDir*") {
  [Environment]::SetEnvironmentVariable("Path", "$currentPath;$binDir", "User")
  Write-Host "Added to PATH. Open a new terminal to use 'aethercore-installer'."
} else {
  Write-Host "PATH already contains $binDir"
}

Write-Host "Installed to $installRoot"
