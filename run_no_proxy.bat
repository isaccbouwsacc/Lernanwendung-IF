echo off

:: Activate virtual environment
call .venv\Scripts\activate.bat

set LAUNCH_ARGS=--api

:: Run the main application
python ".\modules\webui.py" %LAUNCH_ARGS%

:: Deactivate virtual environment
call deactivate