param (
    [string]$name = "AI_Hub",
    [string]$python = "3.10"
)

# Check if conda is available
if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
    Write-Host "Anaconda could not be found!"
    Write-Host "Run install_platform_deps.ps1 to install miniconda3. Open Anaconda PowerShell Prompt and re-run this script to continue."
} else {
    # Create & activate environment
    $condaEnvExists = conda env list | Select-String -Pattern $name
    if (-not $condaEnvExists) {
        Write-Host "Conda environment '$name' does not exist. Creating it now..."
        conda create -n $name -y python=$python
        Write-Host "Conda environment '$name' created."
    }
    conda activate $name
    Write-Host "Your environment is activated and ready to run demos!"
}
