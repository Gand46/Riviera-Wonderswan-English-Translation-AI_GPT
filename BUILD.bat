@echo off
setlocal
if "%~1"=="" (
  echo Uso: BUILD.bat ROM_JP_LIMPIA.wsc [SALIDA_RC5.wsc]
  exit /b 2
)
set "OUT=%~2"
if "%OUT%"=="" set "OUT=%~dp0build\Riviera_EN_v0.114_S461_RC5.wsc"
py -3 "%~dp0build_rc5.py" "%~1" --out "%OUT%"
if errorlevel 1 exit /b %errorlevel%
echo Build RC5 completado: %OUT%
