@echo off
echo ========================================
echo   BUILDING FaceBlurrer
echo ========================================
echo.

echo Checking for haarcascade file...
if not exist haarcascade_frontalface_default.xml (
    echo Downloading haarcascade...
    powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml' -OutFile 'haarcascade_frontalface_default.xml'"
)

echo Cleaning old builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

echo Building .exe...
py -3.11 -m PyInstaller --onefile --noconsole --add-data "haarcascade_frontalface_default.xml;." --name FaceBlurrer face_blurrer.py

echo Copying haarcascade to dist...
copy haarcascade_frontalface_default.xml dist\

echo ========================================
echo   DONE!
echo   .exe: dist\FaceBlurrer.exe
echo ========================================
pause