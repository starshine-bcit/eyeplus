$original_Location = Get-Location
Set-Location $PSScriptRoot
Write-Host 'Attempting to compile .py'
if (Test-Path '..\qt\qtui.py') {
    Write-Host 'old qtui.py found, removing...'
    Remove-Item '..\qt\qtui.py'
}
& pyuic6 -x -o ..\qt\qtui.py ..\..\qtsrc\eyeplus\mainwindow.ui
Write-Host 'qtui.py successfully written'
Set-Location $Original_location