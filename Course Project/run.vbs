Set objShell = WScript.CreateObject("WScript.Shell")  
intWindowStyle = 0 ' 0 = Hide the window  
strCommand = "python.exe main.py"  
objShell.Run strCommand, intWindowStyle, false