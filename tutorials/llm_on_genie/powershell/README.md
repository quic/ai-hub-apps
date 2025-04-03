# Genie PowerShell script for Windows

This script simplifies the steps in the [LLM On-Device Deployment](..)
tutorial. It is assumed that you have followed the tutorial and prepared a
Genie bundle with the context binaries and tokenizer.

From the parent directory (`llm_on_genie`), please run the command in a
PowerShell terminal:

```powershell
.\powershell\RunLlm1.ps1
```

For more information, run:

```powershell
Get-Help .\powershell\RunLlm1.ps1
```

If it says that you do not have permission to run PowerShell scripts, you may
need to enable this first with this command:

```powershell
Set-ExecutionPolicy -Scope CurrentUser Unrestricted -Force
```
