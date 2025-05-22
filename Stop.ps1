$proxy = Get-Process mitmdump -ErrorAction SilentlyContinue

Set-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings" -Name ProxyEnable -Value 0

"Disabled proxy settings"

if ($proxy) {
    "Stopping $($proxy.Id)"

    $proxy.CloseMainWindow()
}
else {
    "Proxy is not running"
}