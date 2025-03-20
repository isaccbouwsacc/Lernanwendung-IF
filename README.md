# Dokumentation der Projektarbeit

Eine interaktive Lernanwendung für automatisierte Bewertung von Antworten zu bestimmten Fragestellungen.

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

Dieses Projekt ist ein interaktives Lernwerkzeug, welches Fragen aus verschiedenen Themenbereichen stellt und im Anschluss die eingegebenen Antworten automatisch mithilfe eines Sprachmodells bewertet. Zusätzlich zu der Bewertung wird detailliertes Feedback zur Qualität der Antwort, ebenfalls vom Sprachmodell, bereitgestellt. Des Weiteren bietet dieses System eine benutzerfreundliche Web-Ui, in der Themen und Unterthemen ausgewählt werden können.

#### Anmerkung: LLMs (Sprachmodelle) können Fehler machen!

## Systemanforderungen

- [Python 3.8+](https://www.python.org/downloads/) oder höher
- [Git](https://git-scm.com/downloads) (für das Klonen des Repositories)
- Windows-Betriebssystem (für die Batch- und VBS-Skripte + Anwendung ist nicht für Linux gebaut)
- Mindestens 4GB RAM / VRAM für die lokale Ausführung (Modelabhängig)
- Internetverbindung für die API-Nutzung
- [LM Studio](https://lmstudio.ai/) für die lokale Ausführung von Sprachmodellen

### Python-Abhängigkeiten
- [Gradio](https://gradio.app/) - für die Web-Ui
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

### Modi für das Sprachmodell

#### Lokaler Modus
Im lokalen Modus kommuniziert die Anwendung direkt mit einem lokal ausgeführten Sprachmodell, wie z.B. über [LM Studio](https://lmstudio.ai/). Hierfür muss LM Studio auf dem lokalen Rechner gestartet sein und auf Port 1234 hören.

#### API-Modus
Der API-Modus stellt **keine** eigenen Sprachmodelle bereit, sondern ermöglicht lediglich die Kommunikation mit einem externen Netzwerk. Kann also als Host/Client system verwendet werden, ähnlich wie: `share=True` von gradio.

### Proxy-Server

Secure Proxy sorgt für eine gesicherte Verbindung zwischen Host und Client und kann mit ngrok eine öffentliche URL bereitstellen, die den Zugriff von außerhalb des lokalen Netzwerks ermöglicht.

```
run_proxy.vbs
```

#### Anmerkung: Der ngrok-Authtoken im Proxy-Code sollte vor der Verwendung im produktiven Umfeld durch Ihren eigenen ersetzt werden.

## Funktionsweise

### Komponenten

- `webui.py`: Hauptmodul für die Web-Ui und Anwendungslogik
- `chat_logic_api.py` / `chat_logic_local.py`: Verantwortlich für die Kommunikation mit dem Sprachmodell
- `secure_proxy.py`: Stellt eine gesicherte Verbindung her
- `history.py`: Verwaltet den Gesprächsverlauf (veraltet)
- `thema.py` / `dataset.py`: Verwalten Themen und Datensätze
- `_func.py`: Enthält CSS-Funktionen für den Style der Benutzeroberfläche

### Datenstruktur
```
Lernanwendung-IF/
 ├── .venv/                  # Virtuelle Python-Umgebung (wird bei Installation erstellt)
 ├── dataset/                # Enthält JSON-Dateien mit Fragen und erwarteten Antworten
 ├── modules/                # Enthält die Hauptmodule der Anwendung
 │   ├── _func.py            # CSS und JavaScript für die UI
 │   ├── dataset.py          # Datensatz Klasse
 │   ├── thema.py            # Thema Klasse
 │   ├── history.py          # Konversationsverlauf Klasse (veraltet/nicht verwendet)
 │   ├── chat_logic_api.py   # API-Modus Antwort Logik
 │   ├── chat_logic_local.py # Lokaler Modus Antwort Logik
 │   ├── secure_proxy.py     # Sicherer Proxy für API-Kommunikation
 │   └── webui.py            # Hauptwebui
 ├── installer.bat           # Installationsskript
 ├── README.md               # Anweisungsdatei
 ├── requirements.txt        # Abhängigkeiten
 ├── run.vbs                 # Startskript
 ├── run_app.py              # Hauptanwendungsstarter
 ├── run_proxy.vbs           # Proxystarter (falls nicht die ganze Anwendung ausgeführt werden kann, bzw. zum Hosten)
 └── venv_cmd.bat            # Shortcut für cmd in der virtuellen Python-Umgebung
 ```

### Ablauf

1. Nach dem Start wird eine Liste verfügbarer Themen und Unterthemen angezeigt
2. Nach Auswahl eines Themas wird eine Frage präsentiert
3. Der Benutzer gibt seine Antwort in das Textfeld ein
4. Nach dem Absenden wird die Antwort an das Sprachmodell gesendet
5. Das Modell bewertet die Antwort anhand des vorgegebenen Erwartungshorizonts
6. Das Ergebnis wird mit Punktzahl (0-10) und detaillierter Begründung angezeigt

## Konfiguration

### Datensatzformat

Die Fragen werden in JSON-Dateien im Verzeichnis `dataset/` gespeichert. Das Format ist wie folgt:

```json
[
  {
    "type": "question",
    "content": "{Frage}",
    "expected_answer": "{Erwartete Antwort/Erwartungshorizont}"
  }
]
```

### Themenkonfiguration

Themen und Unterthemen werden durch die Dateinamen der JSON-Dateien definiert:
- Hauptthema: `Thema.json`
- Unterthema: `Thema - Unterthema.json`

Die Anwendung scannt das `dataset/`-Verzeichnis beim Start und baut dynamisch eine Themenstruktur auf.

### Proxy-Konfiguration

Der Secure Proxy verwendet ngrok für den externen Zugriff. Im Produktiveinsatz sollten Sie den vorhandenen ngrok-Authtoken in `secure_proxy.py` durch Ihren eigenen ersetzen:

```python
ngrok_auth_token = "IHR_AUTHTOKEN_HIER"
```

## Erweiterungsmöglichkeiten

### Neue Themen hinzufügen

1. Eine neue JSON-Datei im Format `NeuesThema.json` oder `ExistierendesThema - NeuesUnterthema.json` erstellen
2. Die Datei im `dataset/`-Verzeichnis speichern
3. Die Anwendung neu starten

### Integration weiterer Sprachmodelle

Für die Integration neuer Sprachmodelle kann `chat_logic_local.py` angepasst oder das Modell direkt in LM Studio konfiguriert werden.

### Benutzeroberfläche anpassen

Das Erscheinungsbild der Applikation kann durch Änderung der CSS-Definitionen in `_func.py` angepasst werden.

## Debugging

### Bekannte Probleme

- Bei Verbindungsproblemen zum Sprachmodell sollte überprüft werden, ob LM Studio korrekt konfiguriert ist und auf Port 1234 läuft
- Bei API-Verbindungsproblemen sollten eingegebene API-Schlüssel und API-Endpunkt überprüft werden
- Wenn der ngrok-Tunnel nicht startet, könnte der Authtoken abgelaufen sein oder das Limit erreicht haben

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

Die Anwendung sollte Informationen zur Laufzeit in der Konsole ausgebe, diese sind zumeist für die Diagnose von Problemen hilfreich.
