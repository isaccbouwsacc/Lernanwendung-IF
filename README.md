# Dokumentation

## Inhaltsverzeichnis
- [Übersicht](#übersicht)
- [Systemanforderungen](#systemanforderungen)
- [Installation](#installation)
- [Programmstart](#programmstart)
- [Benutzung](#benutzung)
- [Architektur und Funktionsweise](#architektur-und-funktionsweise)
- [Konfiguration](#konfiguration)
- [Fehlerbehebung](#fehlerbehebung)

## Übersicht
Dieses Projekt ist ein interaktives Lernquiz-System, das Large Language Models (LLMs) zur Bewertung von Benutzerantworten nutzt. Das System bietet eine benutzerfreundliche Webui, in der Benutzer Themen auswählen, Fragen beantworten und automatisiertes Feedback erhalten können. Das System kann sowohl mit lokalen LLMs (über [LM Studio](https://lmstudio.ai/)) als auch mit Remote-APIs betrieben werden.
#### Anmerkung: LLMs können Fehler bei der Auswertugn machen!

## Systemanforderungen
- Windows-Betriebssystem
- [Python](https://www.python.org/downloads/) 3.8 oder höher
- [Git](https://git-scm.com/downloads) (für das Klonen des Repositories)
- Internetverbindung (für die Installation von Abhängigkeiten)
- Optional: [LM Studio](https://lmstudio.ai/) (für den lokalen Modus)

## Installation

### Repository klonen
```bash
git clone https://github.com/username/gog.git
cd gog
```

### Automatische Installation
Installationsdatei ausführen, um die virtuelle Umgebung zu erstellen und alle Abhängigkeiten zu installieren:
```bash
installer.bat
```

Diese Datei führt folgende Schritte aus:
1. Erstellt eine virtuelle Python-Umgebung
2. Aktiviert die virtuelle Umgebung
3. Installiert alle erforderlichen Pakete aus der requirements.txt

### Manuelle Installation (Alternative)
Falls die automatische Installation nicht funktioniert, können manuelle Schritte ausgeführt werden:
```bash
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
```

Die requirements.txt enthält folgende Hauptabhängigkeiten:
- [gradio](https://gradio.app/) (für die Webui)
- [openai](https://github.com/openai/openai-python) (für die API-Kommunikation)
- [flask](https://flask.palletsprojects.com/) (für den Proxy-Server)

## Programmstart

### Einfacher Start
Doppelklick auf die Datei `run.vbs`, um das Programm zu starten. Dies öffnet ein Konsolenfenster und startet die Anwendung.

### Manueller Start
Alternativ können die Anwendung auch manuell gestartet werden:
```bash
call venv\Scripts\activate
python run_app.py
```

## Benutzung

### Startbildschirm
Bei dem Startbildschirm, also noch bevor die Applikation ausgeführt wird, werden einige Perefärenzen mit einem "Ja"(y) oder "Nein"(n) erfragt.

#### Anmerkung:
Der dark mode funktioniert nur lokal, kann aber mit einem manuellem Beifügen von "?__theme=dark" and das Ende der public URL aktiviert werden!

### Themenauswahl
Nach dem Start der Anwendung wird eine Webui in Ihrem Standardbrowser geöffnet. Hier kann Folgendes auswählen werden:
- Ein Hauptthema aus den verfügbaren "Akkordeons" auswählen
- Ein Unterthema auswählen, falls verfügbar

### Fragen beantworten
Nach der Themenauswahl wird eine Frage angezeigt:
1. Lesen Sie die Frage sorgfältig
2. Geben Sie Ihre Antwort in das Textfeld ein
3. Klicken Sie auf "Antwort abgeben"

### Feedback erhalten
Nach dem Absenden Ihrer Antwort:
1. Das System bewertet Ihre Antwort mit Hilfe einer LLM
2. Sie erhalten eine Punktzahl (0-10) und detailliertes Feedback
3. Die erwartete Antwort wird angezeigt
4. Sie können zur Themenauswahl zurückkehren, um weitere Fragen zu beantworten

## Architektur und Funktionsweise

### Hauptkomponenten
- `run_app.py`: Haupteinstiegspunkt, der die Anwendung startet und den Modus (API/lokal) konfiguriert
- `webui.py`: Implementiert die Gradio-Webui und die Quiz-Logik
- `chat_logic_local.py`: Verarbeitet Anfragen im lokalen Modus über LM Studio
- `chat_logic_api.py`: Verarbeitet Anfragen im API-Modus
- `secure_proxy.py`: Implementiert einen sicheren Proxy für die API-Kommunikation
- `_func.py`: Enthält CSS- und JavaScript-Funktionen für die Benutzeroberfläche

### Dateistruktur
```
quiz-system/
├── dataset/                # Enthält JSON-Dateien mit Fragen und erwarteten Antworten
├── modules/                # Enthält die Hauptmodule der Anwendung
│   ├── _func.py            # CSS und JavaScript für die UI
│   ├── dataset.py          # Datensatz Klasse
│   ├── thema.py            # Thema Klasse
│   ├── history.py          # Konversationsverlauf Klasse (veraltet)
│   ├── chat_logic_api.py   # API-Modus Logik
│   ├── chat_logic_local.py # Lokaler Modus Logik
│   ├── secure_proxy.py     # Sicherer Proxy für API-Kommunikation
│   └── webui.py            # Hauptwebui
├── venv/                   # Virtuelle Python-Umgebung (wird bei Installation erstellt)
├── installer.bat           # Installationsskript
├── requirements.txt        # Abhängigkeiten
├── run.vbs                 # Startskript
└── run_app.py              # Hauptanwendungsstarter
```

### Funktionsweise
1. **Initialisierung**: `run_app.py` startet die Anwendung und fragt nach dem gewünschten Modus
2. **Proxy (optional)**: Bei Verwendung des API-Modus kann ein sicherer Proxy gestartet werden
3. **Webui**: `webui.py` erstellt die Benutzeroberfläche mit Gradio
4. **Themenauswahl**: Die verfügbaren Themen werden aus dem Dataset-Verzeichnis geladen
5. **Fragestellung**: Nach Auswahl eines Themas wird eine Frage aus der entsprechenden JSON-Datei geladen
6. **Antwortbewertung**: Die Benutzerantwort wird an das LLM gesendet, das eine Bewertung und Feedback zurückgibt
7. **Ergebnisanzeige**: Die Bewertung, das Feedback und die erwartete Antwort werden angezeigt

## Konfiguration

### Hinzufügen neuer Fragen
Neue Fragen können als JSON-Dateien im `dataset/`-Verzeichnis hinzugefügt werden:

1. Erstellen Sie eine neue JSON-Datei mit dem Namen des Themas (z.B. `Thema1.json`)
2. Für Unterthemen verwenden Sie das Format `Thema - Unterthema.json`
3. Die JSON-Datei sollte folgendes Format haben:
```json
[
  {
    "type": "question",
    "content": "Hier steht die Frage?",
    "expected_answer": "Hier steht die erwartete Antwort."
  }
]
```

### API-Konfiguration
Für die Verwendung mit einer externen API:
1. Wählen Sie beim Start `y` für den API-Modus
2. Geben Sie Ihren API-Schlüssel und den Endpunkt ein
3. Alternativ können Sie den sicheren Proxy verwenden, der automatisch konfiguriert wird

## Fehlerbehebung

### Häufige Probleme

| Problem | Lösung |
|---------|--------|
| Fehler beim Start | Stellen Sie sicher, dass Python korrekt installiert ist und die virtuelle Umgebung erstellt wurde |
| Proxy-Fehler | Überprüfen Sie, ob Port 8080 verfügbar ist und nicht von anderen Anwendungen blockiert wird |
| LM Studio-Verbindungsfehler | Stellen Sie sicher, dass LM Studio läuft und auf Port 1234 hört |
| Fehlende Themen | Überprüfen Sie, ob das `dataset/`-Verzeichnis existiert und JSON-Dateien enthält |

### Logs
Bei Problemen können Sie die Konsolenausgabe überprüfen, die wichtige Diagnoseinformationen enthält.
