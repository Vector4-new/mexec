if (Get-Process mitmdump -ErrorAction SilentlyContinue) {
    "Proxy is already running"
}
else {
    "Starting proxy"
    "If your internet dies check proxy settings or run Stop.ps1"

    Start-Process mitmdump.exe -ArgumentList "--allow-hosts", ".*banland\.xyz.*", "-s", "ProxyScript.py"
    
    Set-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings" -Name ProxyEnable -Value 1
    Set-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings" -Name ProxyServer -Value "http://localhost:8080"

    "Enabled proxy"
}