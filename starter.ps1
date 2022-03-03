$fullPath = $MyInvocation.MyCommand.Path
$curDir = Split-Path $fullPath -Parent
$sessionFileName = "session"
$requirementsFileName = "requirements"
$pythonFileName = "main.py"

Write-Host "[Current directory: $curDir]" 
Write-Host "[Python file name: $pythonFileName]"

if (Test-Path -Path "$curDir\$sessionFileName") {
    Write-Host "[File session exists]" -ForegroundColor Green
    $clients = Get-Content -Path "$curDir\$sessionFileName"
    $numbers = $clients.Split(' ')

    for ($i = 0; $i -lt $numbers.Count - 1; $i++) {
        Write-Host ("[user: $i][$($numbers[$i])]")
    }

    $userAnswer = Read-Host -Prompt "[Select user]";

    if ($userAnswer -ge 0 -and $userAnswer -lt $numbers.Count - 1) {
        "pip install -r $curDir\$requirementsFileName.txt" | cmd
        & python.exe "$curDir\$pythonFileName" "$($numbers[$userAnswer])"
        Pause
    }
}
else {
    Write-Host "[File session is invalid]" -ForegroundColor Red
    "pip install -r $curDir\$requirementsFileName.txt" | cmd
    & python.exe "$curDir\$pythonFileName"
    Pause
}
