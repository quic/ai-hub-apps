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
    $missing_deps = $false

    $choice = Read-Host "Install miniconda3? (y/n)"
    if ($choice -eq "y") {
        $spaceCount = ($env:userprofile -split " ").Length - 1
        if ($spaceCount -gt 0) {
            # Anaconda PowerShell breaks when there is a space in the base install path.
            #
            # The installation directory that winget uses includes the current username. If the current username
            # has a space, we need to elevate privileges and install globally, so conda is installed in C:\ProgramFiles instead.
            Write-Output "`n!!!!!`n"
            Write-Output "Your home directory has a space, which can break conda packages. Conda must be installed globally to avoid this."
            Write-Output "Open PowerShell in administrator mode and run:`n"
            Write-Output "    winget install miniconda3 --architecture X64 --scope machine"
            Write-Output "`nto install conda."
            Write-Output "`n!!!!!`n"
            $missing_deps = $true
        } else {
            winget install miniconda3 --architecture X64
        }
    } else {
        $missing_deps = $true
    }

    $choice = Read-Host "Install Git (Microsoft.Git)? (y/n)"
    if ($choice -eq "y") {
        winget install Microsoft.Git
    } else {
        $missing_deps = $true
    }

    if ($extra_pkgs -ne "") {
        $choice = Read-Host "Install packages: $extra_pkgs ? (y/n)"
        if ($choice -eq "y") {
            winget install $extra_pkgs
        } else {
            $missing_deps = $true
        }
    }

    if ($missing_deps) {
        Write-Output "`n!!!!!`n"
        Write-Host "Some dependencies were not installed."
        Write-Output "`n!!!!!`n"
    } else {
        Write-Host "`nAll platform dependencies installed.`n"
    }
    Write-Host "Open Anaconda PowerShell Prompt in a NEW WINDOW to continue.`n"
} else {
    Write-Host "WinGet could not be found. We need it to install demo dependencies. You can get it in the Windows Store: https://apps.microsoft.com/detail/9nblggh4nns1"
}
