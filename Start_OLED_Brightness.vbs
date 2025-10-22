Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Получаем путь к текущей папке
currentPath = fso.GetParentFolderName(WScript.ScriptFullName)

' Путь к Python скрипту
scriptPath = currentPath & "\OLED_Auto_Brightness.py"

' Проверяем наличие виртуального окружения
venvPath = currentPath & "\.venv\Scripts\pythonw.exe"

' Если есть виртуальное окружение - используем его, иначе системный Python
If fso.FileExists(venvPath) Then
    pythonPath = venvPath
Else
    ' Пытаемся найти Python в системе
    pythonPath = "pythonw.exe"
End If

' Запускаем скрипт в фоновом режиме (без окна консоли)
WshShell.Run """" & pythonPath & """ """ & scriptPath & """", 0, False
