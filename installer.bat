@echo off
::venv aktivieren
call .venv\Scripts\activate
::installation von inhalten von requirements.txt
pip install -r requirements.txt
::venv deaktivieren
call deactivate