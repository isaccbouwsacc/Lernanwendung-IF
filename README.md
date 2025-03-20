# Dokumentation der Projektarbeit

Eine interaktive Lernanwendung für automatisierte Bewertung von Fragestellungen in der Informatik.

## Inhaltsverzeichnis
- [Übersicht](#übersicht)
- [Systemanforderungen](#systemanforderungen)
- [Installation](#installation)
- [Verwendung](#verwendung)
- [Funktionsweise](#funktionsweise)
- [Konfiguration](#konfiguration)
- [Erweiterungsmöglichkeiten](#erweiterungsmöglichkeiten)
- [Debugging](#debugging)

## Übersicht

Dieses Projekt ist ein interaktives Lernwerkzeug, welches Fragen aus verschiedenen Themenbereichen stellt und im Anschluss die eingegebenen Antworten automatisch mithilfe eines Sprachmodells bewertet. Zusätzlich zu der Bewertung wird detailliertes Feedback zur Qualität der Antwort, ebenfalls vom Sprachmodell, bereitgestellt. Des Weiteren bietet dieses System eine benutzerfreundliche Weboberfläche, in der Themen und Unterthemen ausgewählt werden können.

#### Anmerkung: LLMs (Sprachmodelle) können Fehler machen!

## Systemanforderungen

- [Python 3.8+](https://www.python.org/downloads/) oder höher
- [Git](https://git-scm.com/downloads) (für das Klonen des Repositories)
- Windows-Betriebssystem (für die Batch- und VBS-Skripte)
- Mindestens 4GB RAM (Modelabhängig) für die lokale Ausführung
- Internetverbindung für die API-Nutzung
- [LM Studio](https://lmstudio.ai/) für die lokale Ausführung von Sprachmodellen

### Python-Abhängigkeiten
- [Gradio](https://gradio.app/) - für die Weboberfläche
- [OpenAI API](https://github.com/openai/openai-python) - für die Kommunikation mit dem Sprachmodell
- [Flask](https://flask.palletsprojects.com/) - für den Proxy-Server
- [pyngrok](https://pyngrok.readthedocs.io/) - für den externen Zugriff

## Installation

1. Repository klonen:
```bash
git clone https://github.com/isaccbouwsacc/Lernanwendung-IF.git
cd Lernanwendung-IF
```

2. Installation der Abhängigkeiten mithilfe des Installationsskripts:
```bash
installer.bat
```

Dieses Skript erstellt eine virtuelle Python-Umgebung und installiert alle erforderlichen Pakete aus der `requirements.txt` Datei.

## Verwendung

### Starten der Anwendung

Die Anwendung kann auf zwei Arten gestartet werden:

1. **Einfache Ausführung mit VBS-Skript (empfohlen):**
```
run.vbs
```
Dieses Skript startet die Anwendung und erfragt nach den Startoptionen (y/n).

2. **Manueller Start mit Optionen:**
```
venv_cmd.bat
python modules\webui.py [OPTIONEN]
```

### Verfügbare Startoptionen

- `--api-key [KEY]`: Nutzt den API-Endpunkt mit dem angegebenen Schlüssel
- `--api-endpoint [URL]`: Definiert den API-Endpunkt
- `--share`: Aktiviert die öffentliche Freigabe der Anwendung über eine temporäre URL
- `--username [NAME]`: Legt einen Benutzernamen für die Authentifizierung fest
- `--password [PASSWORT]`: Legt ein Passwort für die Authentifizierung fest

### Proxy-Server

Für eine gesicherte Verbidung zwischen Host und Client kann `run_proxy.vbs` ausgeührt werden.
```
run_proxy.vbs
```
Dieses Skript startet einen Proxy-Server, der durch ngrok einer öffentliche URL zugewiesen bekommt und so nicht nur auf lokaler Ebene benutzt werden kann.

## Funktionsweise

### Komponenten

- `webui.py`: Hauptmodul für die Weboberfläche und Anwendungslogik
- `chat_logic_api.py` / `chat_logic_local.py`: Verantwortlich für die Kommunikation mit dem Sprachmodell
- `secure_proxy.py`: Stellt eine gesicherte Verbindung her
- `history.py`: Verwaltet den Gesprächsverlauf (veraltet)
- `thema.py` / `dataset.py`: Verwalten Themen und Datensätze
- `_func.py`: Enthält CSS-Funktionen für den Style der Benutzeroberfläche

### Datenstruktur
Lernanwendung-IF/
 ├── .venv/                  # Virtuelle Python-Umgebung (wird bei Installation erstellt)
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
 ├── installer.bat           # Installationsskript
 ├── requirements.txt        # Abhängigkeiten
 ├── run.vbs                 # Startskript
 ├── run_app.py              # Hauptanwendungsstarter
 ├── run_proxy.vbs           # Proxystarter (falls nicht die ganze Anwendung ausgeführt werden kann)
 └── venv_cmd.bat            # Shortcut für cmd in der virtuellen Python-Umgebung
 ```

### Ablauf

1. Nach dem Start wird eine Liste verfügbarer Themen und Unterthemen angezeigt
2. Nach Auswahl eines Themas wird eine Frage präsentiert
3. Die eingegebene Antwort wird an das Sprachmodell gesendet
4. Das Modell bewertet die Antwort und generiert Feedback
5. Das Ergebnis wird mit Punktzahl und Begründung angezeigt

## Konfiguration

### Datensatzformat

Die Fragen werden in JSON-Dateien im Verzeichnis `dataset/` gespeichert. Das Format ist wie folgt:

```json
[
  {
    "type": "question",
    "content": "{Frage}",
    "expected_answer": "{Antwort}"
  }
]
```

### Themenkonfiguration

Themen werden durch die Dateinamen der JSON-Dateien definiert:
- Hauptthema: `Thema.json`
- Unterthema: `Thema - Unterthema.json`

## Erweiterungsmöglichkeiten

### Neue Themen hinzufügen

1. Eine neue JSON-Datei im Format `NeuesThema.json` oder `ExistierendesThema - NeuesUnterthema.json` erstellen
2. Die Datei im `dataset/`-Verzeichnis speichern
3. Die Anwendung neu starten

### Integration weiterer Sprachmodelle

Für die Integration neuer Sprachmodelle kann `chat_logic_local.py` oder auch in LM Studio angepasst werden:

```python
MODEL = "neues-modell-name"
```

### Benutzeroberfläche anpassen

Das Erscheinungsbild der Applikation kann durch Änderung der CSS-Definitionen in `_func.py` angepasst werden.

## Debugging

### Bekannte Probleme

- Bei Verbindungsproblemen zum Sprachmodell sollte überprüft werden, ob LM Studio korrekt konfiguriert ist und auf Port 1234 läuft
- Bei API-Verbindungsproblemen sollten eingegebene API-Schlüssel und API-Endpunkt überprüft werden

### Fehlerbehebung

1. **Virtuelle Umgebung prüfen:**
```bash
venv_cmd.bat
pip list
```

2. **Proxy-Server-Logs überprüfen:**
Beim Start des Proxy-Servers werden API-Schlüssel und Endpunkt-URL angezeigt.

3. **LM Studio-Verbindung testen:**
```bash
curl http://127.0.0.1:1234/v1/models
```

### Logging

Die Anwendung gibt Informationen zur Laufzeit in der Konsole aus, die für die Diagnose von Problemen hilfreich sein können.
