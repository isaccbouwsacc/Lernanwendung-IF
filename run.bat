@echo off

:: Activate virtual environment
call .venv\Scripts\activate.bat

set LAUNCH_ARGS=--api

:: Start proxy first
start /b python ".\modules\secure_proxy.py"
timeout /t 2 > nul

:: Run the main application
python ".\modules\webui.py" %LAUNCH_ARGS%

:: When main application exits, kill the proxy server using its PID
if exist proxy_pid.txt (
    set /p PROXY_PID=<proxy_pid.txt
    taskkill /f /pid %PROXY_PID% > nul 2>&1
    del proxy_pid.txt
    echo Proxy server shut down.
) else (
    echo Proxy PID file not found.
)

:: Deactivate virtual environment
call deactivate