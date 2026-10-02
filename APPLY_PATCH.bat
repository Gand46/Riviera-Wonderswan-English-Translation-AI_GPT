@echo off
setlocal
if "%~2"=="" (
  echo Usage: APPLY_PATCH.bat CLEAN_JP_ROM OUTPUT_ROM
  exit /b 2
)
py -3 apply_patch.py "%~1" "%~2"
exit /b %errorlevel%
