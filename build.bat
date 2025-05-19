@echo off
echo Building PRRI-RT2025 game executable...

:: Clean up previous build files
echo Cleaning up previous build files...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "__pycache__" rmdir /s /q "__pycache__"

:: Build the executable using the spec file
echo Building executable with PyInstaller...
python -m PyInstaller PRRI-RT2025.spec

:: Check if build was successful
if %ERRORLEVEL% NEQ 0 (
    echo Build failed with error code %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

echo Build completed successfully!
echo Executable is available at: dist\PRRI-RT2025.exe
pause
