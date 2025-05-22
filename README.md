Old executor for 2014L and earlier clients, before they switched to ticket-based authentication and used joinscripts.

mitmproxy is required for this. You will need to follow the [advanced installation](https://docs.mitmproxy.org/stable/overview/installation/#advanced-installation) so you can use `pipx` to inject the required libraries.  
Also, you should change the base URL in Start.ps1, as otherwise some sites like Discord block proxies and you won't be able to use them.  

./Start.ps1 and ./Stop.ps1 automatically set and unset your proxy settings. If you can't connect to the internet, either run ./Stop.ps1 or manually reset your proxy settings.

You can use Visual Studio Code as an executor by making a build job and putting the following:
```js
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run script",
            "type": "shell",
            "command": "./RunFile.ps1 ${file}",
            "problemMatcher": [],
            "group": {
                "kind": "build",
                "isDefault": true
            }
        }
    ]
}
```  

Then CTRL+B and select `Run script`

In some versions, using this will crash the client, you will have to uncomment the lines that check for the first instance only.
