@echo off

::venv erstellen
python -m venv venv
::venv aktivieren
call .venv\Scripts\activate
::Inhalt aus requirements.txt auf venv installieren
pip install -r requirements.txt
::venv deaktivieren
call deactivate
