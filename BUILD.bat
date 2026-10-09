@echo off
setlocal
if "%~1"=="" (
  echo Uso: BUILD.bat ROM_JP_LIMPIA.wsc [SALIDA_RC7.wsc]
  exit /b 2
)
set "OUT=%~2"
if "%OUT%"=="" set "OUT=%~dp0build\Riviera_EN_v0.116_S463_RC7.wsc"
py -3 "%~dp0build_rc7.py" "%~1" --out "%OUT%"
if errorlevel 1 exit /b %errorlevel%
echo Build RC7 completado: %OUT%
