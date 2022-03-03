set psScript="%cd%/%~n0.ps1"
powershell -NoProfile -Command "& {Start-Process PowerShell.exe -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File "%psScript%"' -Verb RunAs}"