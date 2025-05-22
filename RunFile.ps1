$mercury = Get-Process MercuryPlayerBeta -ErrorAction SilentlyContinue

if (!$mercury) {
    "Mercury is not running"

    Return
}


$in = Get-Content .\loader.rbxmx
$in = $in.Replace("%KEYVALUE%", (Get-Random).ToString())
$in = $in.Replace("%SOURCE%", [System.Security.SecurityElement]::Escape((Get-Content $args[0])))

[IO.File]::WriteAllLines($mercury.MainModule.FileName.Substring(0, $mercury.MainModule.FileName.LastIndexOf("\")) + "\content\loader.rbxmx", $in) | Out-Null