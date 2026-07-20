param(
    [switch]$SkipBuild,
    [switch]$CleanBuild
)

$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$BuildScript = Join-Path $ProjectRoot "scripts\build_windows.ps1"
$DistAppDirectory = Join-Path $ProjectRoot "dist\YouTubeDownloaderPro"
$Executable = Join-Path $DistAppDirectory "YouTubeDownloaderPro.exe"
$ReleaseRoot = Join-Path $ProjectRoot "release"
$PortableRoot = Join-Path $ReleaseRoot "YouTubeDownloaderPro_Portable"
$PortableAppDirectory = Join-Path $PortableRoot "YouTubeDownloaderPro"
$InstallScript = Join-Path $ProjectRoot "install_dependencies.bat"
$RunScript = Join-Path $ProjectRoot "run_app.bat"
$InstallReadme = Join-Path $ProjectRoot "README_INSTALL.txt"
$ReleaseNotes = Join-Path $ProjectRoot "RELEASE.md"
$ConstantsFile = Join-Path $ProjectRoot "core\constants.py"

function Assert-FileExists {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [string]$Description
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "$Description was not found: $Path"
    }
}

function Assert-DirectoryInside {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Directory,
        [Parameter(Mandatory = $true)]
        [string]$ParentDirectory
    )

    $FullDirectory = [System.IO.Path]::GetFullPath($Directory)
    $FullParent = [System.IO.Path]::GetFullPath($ParentDirectory)
    if (-not $FullDirectory.StartsWith($FullParent, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to modify directory outside release root: $FullDirectory"
    }
}

function Get-ApplicationVersion {
    Assert-FileExists -Path $ConstantsFile -Description "Application constants file"
    $VersionMatch = Select-String -Path $ConstantsFile -Pattern '^APPLICATION_VERSION:\s*str\s*=\s*"([^"]+)"' | Select-Object -First 1
    if ($null -eq $VersionMatch) {
        throw "Application version could not be read from $ConstantsFile"
    }
    return $VersionMatch.Matches[0].Groups[1].Value
}

Set-Location $ProjectRoot

Assert-FileExists -Path $BuildScript -Description "Windows build script"
Assert-FileExists -Path $InstallScript -Description "Dependency installer"
Assert-FileExists -Path $RunScript -Description "Application launcher"
Assert-FileExists -Path $InstallReadme -Description "Portable install README"
Assert-FileExists -Path $ReleaseNotes -Description "Release notes"

if (-not $SkipBuild) {
    $BuildArguments = @("-ExecutionPolicy", "Bypass", "-File", $BuildScript)
    if ($CleanBuild) {
        $BuildArguments += "-Clean"
    }
    & powershell @BuildArguments
}

Assert-FileExists -Path $Executable -Description "PyInstaller executable"

if (-not (Test-Path -LiteralPath $ReleaseRoot)) {
    New-Item -ItemType Directory -Path $ReleaseRoot | Out-Null
}

Assert-DirectoryInside -Directory $PortableRoot -ParentDirectory $ReleaseRoot
if (Test-Path -LiteralPath $PortableRoot) {
    Remove-Item -LiteralPath $PortableRoot -Recurse -Force
}

New-Item -ItemType Directory -Path $PortableRoot | Out-Null

Copy-Item -LiteralPath $DistAppDirectory -Destination $PortableAppDirectory -Recurse -Force
Copy-Item -LiteralPath $InstallScript -Destination (Join-Path $PortableRoot "install_dependencies.bat") -Force
Copy-Item -LiteralPath $RunScript -Destination (Join-Path $PortableRoot "run_app.bat") -Force
Copy-Item -LiteralPath $InstallReadme -Destination (Join-Path $PortableRoot "README_INSTALL.txt") -Force
Copy-Item -LiteralPath $ReleaseNotes -Destination (Join-Path $PortableRoot "RELEASE.md") -Force

$ExcludedDirectoryNames = @(".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "tests", "logs", "downloads")
Get-ChildItem -LiteralPath $PortableRoot -Directory -Recurse -Force |
    Where-Object { $ExcludedDirectoryNames -contains $_.Name } |
    ForEach-Object { Remove-Item -LiteralPath $_.FullName -Recurse -Force }

$ExcludedFileExtensions = @(".log", ".tmp", ".temp", ".pyc", ".pyo")
Get-ChildItem -LiteralPath $PortableRoot -File -Recurse -Force |
    Where-Object { $ExcludedFileExtensions -contains $_.Extension.ToLowerInvariant() } |
    ForEach-Object { Remove-Item -LiteralPath $_.FullName -Force }

$Version = Get-ApplicationVersion
$BuildDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
$VersionText = @"
Program: YouTube Downloader Pro
Version: $Version
Author: Ariel Ponce
Build date: $BuildDate
Platform: Windows
Type: Portable onedir
"@
$VersionText | Set-Content -Path (Join-Path $PortableRoot "VERSION.txt") -Encoding UTF8

$PortableExecutable = Join-Path $PortableAppDirectory "YouTubeDownloaderPro.exe"
Assert-FileExists -Path $PortableExecutable -Description "Portable executable"
Assert-FileExists -Path (Join-Path $PortableRoot "install_dependencies.bat") -Description "Portable dependency installer"
Assert-FileExists -Path (Join-Path $PortableRoot "run_app.bat") -Description "Portable launcher"
Assert-FileExists -Path (Join-Path $PortableRoot "README_INSTALL.txt") -Description "Portable install README"
Assert-FileExists -Path (Join-Path $PortableRoot "VERSION.txt") -Description "Portable version file"
Assert-FileExists -Path (Join-Path $PortableRoot "RELEASE.md") -Description "Portable release notes"

Write-Host "Portable package completed: $PortableRoot"
