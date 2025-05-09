param (
    [string]$extra_pkgs = ""
)

# Add winget to system path if it's missing.
$windowsAppsPath = "$env:userprofile\AppData\Local\Microsoft\WindowsApps"
if (-not (Get-Command winget -ErrorAction SilentlyContinue) -and (Test-Path "$windowsAppsPath\winget.exe")) {
    Write-Host "Found WinGet on your system, but it is not in the PATH. This is required to install demo dependencies."
    $response = Read-Host "Do you want add WinGet to your PATH? (y/n)"
    if ($response -eq 'y' -or $response -eq 'Y' -or $response -eq 'yes' -or $response -eq 'Yes') {
        [System.Environment]::SetEnvironmentVariable("PATH", "$env:Path;$windowsAppsPath", [System.EnvironmentVariableTarget]::User)
        $env:Path += ";$windowsAppsPath"
        Write-Host "WinGet added to PATH successfully."
    }
}

if (Get-Command winget -ErrorAction SilentlyContinue) {
    winget install miniconda3 --architecture X64
    winget install Microsoft.Git $extra_pkgs
    Write-Host "All platform dependencies installed. Open (or re-open) Anaconda PowerShell Prompt to continue."
} else {
    Write-Host "WinGet could not be found. We need it to install demo dependencies. You can get it in the Windows Store: https://apps.microsoft.com/detail/9nblggh4nns1"
}
