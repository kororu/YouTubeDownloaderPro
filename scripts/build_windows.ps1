param(
    [switch]$Clean
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$SpecFile = Join-Path $ProjectRoot "YouTubeDownloaderPro.spec"
$BuildDirectory = Join-Path $ProjectRoot "build"
$DistDirectory = Join-Path $ProjectRoot "dist"

function Assert-CommandAvailable {
    param(
        [Parameter(Mandatory = $true)]
        [string]$CommandName
    )

    if (-not (Get-Command $CommandName -ErrorAction SilentlyContinue)) {
        throw "$CommandName is not available. Install project build dependencies before running this script."
    }
}

Set-Location $ProjectRoot
Assert-CommandAvailable -CommandName "pyinstaller"

if ($Clean) {
    if (Test-Path $BuildDirectory) {
        Remove-Item -LiteralPath $BuildDirectory -Recurse -Force
    }
    if (Test-Path $DistDirectory) {
        Remove-Item -LiteralPath $DistDirectory -Recurse -Force
    }
}

pyinstaller --noconfirm $SpecFile

$Executable = Join-Path $DistDirectory "YouTubeDownloaderPro\YouTubeDownloaderPro.exe"
if (-not (Test-Path $Executable)) {
    throw "Build completed but executable was not found at $Executable"
}

Write-Host "Build completed: $Executable"
