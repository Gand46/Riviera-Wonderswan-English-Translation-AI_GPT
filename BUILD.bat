@echo off
setlocal
if "%~1"=="" (
  echo Usage: BUILD.bat CLEAN_JP_ROM [OUTPUT_ROM]
  exit /b 2
)
if "%~2"=="" (
  py -3 build.py "%~1"
) else (
  py -3 build.py "%~1" "%~2"
)
exit /b %errorlevel%
