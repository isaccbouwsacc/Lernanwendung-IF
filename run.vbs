'shell-objekt zur interaktion mit commands
Set WshShell = CreateObject("WScript.Shell")
'path zum projekt finden
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
'path zum projekt als aktulle umgebung setzten
WshShell.CurrentDirectory = strPath
'venv aktuvieren und script ausführen
WshShell.Run "cmd /c .venv\Scripts\activate.bat && python run_app.py", 1, True