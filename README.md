# Dokumentation
Interaktives Lernquiz mit LLM-Integration

Inhaltsverzeichnis:
Übersicht
Systemanforderungen
Installation
Programmstart
Benutzung
Architektur und Funktionsweise
Konfiguration
Fehlerbehebung

Übersicht:
Dieses Projekt ist ein interaktives Lernquiz-System, das Large Language Models (LLMs) zur Bewertung von Benutzerantworten nutzt. Das System bietet eine benutzerfreundliche Weboberfläche, in der Benutzer Themen auswählen, Fragen beantworten und automatisiertes Feedback erhalten können. Das System kann sowohl mit lokalen LLMs (über LM Studio) als auch mit Remote-APIs betrieben werden.

Systemanforderungen:
Windows-Betriebssystem
Python 3.8 oder höher
Git (für das Klonen des Repositories)
Internetverbindung (für die Installation von Abhängigkeiten)
Optional: LM Studio (für den lokalen Modus)

Installation:
Repository klonen
´´´
git clone https://github.com/username/quiz-system.git
cd quiz-system
´´´
Automatische Installation:
Führen Sie die Installationsdatei aus, um die virtuelle Umgebung zu erstellen und alle Abhängigkeiten zu installieren:
´´´
installer.bat
´´´
Diese Datei führt folgende Schritte aus:

Erstellt eine virtuelle Python-Umgebung
Aktiviert die virtuelle Umgebung
Installiert alle erforderlichen Pakete aus der requirements.txt
Manuelle Installation (Alternative)

Falls die automatische Installation nicht funktioniert, können Sie die Schritte manuell ausführen:
´´´
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
´´´

Die requirements.txt enthält folgende Hauptabhängigkeiten:

gradio (für die Weboberfläche)
openai (für die API-Kommunikation)
flask (für den Proxy-Server)

Programmstart:
Einfacher Start:
Doppelklicken Sie auf die Datei run.vbs, um das Programm zu starten. Dies öffnet ein Konsolenfenster und startet die Anwendung.

Manueller Start
Alternativ können Sie die Anwendung auch manuell starten:
´´´
call venv\Scripts\activate
python run_app.py
´´´

Benutzung
Startbildschirm
Nach dem Start werden Sie gefragt, ob Sie den API-Modus verwenden möchten:

y: Verwendet eine externe API für die LLM-Anfragen
n: Verwendet den lokalen Modus (erfordert LM Studio)
Bei Auswahl des API-Modus können Sie:

Den sicheren Proxy starten (empfohlen)
Einen eigenen API-Schlüssel und Endpunkt angeben
Themenauswahl
Nach dem Start der Anwendung wird die Weboberfläche in Ihrem Standardbrowser geöffnet. Hier können Sie:

Ein Hauptthema aus den verfügbaren Akkordeons auswählen
Ein Unterthema auswählen, falls verfügbar
Fragen beantworten
Nach der Themenauswahl wird eine Frage angezeigt:

Lesen Sie die Frage sorgfältig
Geben Sie Ihre Antwort in das Textfeld ein
Klicken Sie auf "Antwort abgeben"
Feedback erhalten
Nach dem Absenden Ihrer Antwort:

Das System bewertet Ihre Antwort mit Hilfe des LLM
Sie erhalten eine Punktzahl (0-10) und detailliertes Feedback
Die erwartete Antwort wird angezeigt
Sie können zur Themenauswahl zurückkehren, um weitere Fragen zu beantworten
Architektur und Funktionsweise
Hauptkomponenten
run_app.py: Haupteinstiegspunkt, der die Anwendung startet und den Modus (API/lokal) konfiguriert
webui.py: Implementiert die Gradio-Weboberfläche und die Quiz-Logik
chat_logic_local.py: Verarbeitet Anfragen im lokalen Modus über LM Studio
chat_logic_api.py: Verarbeitet Anfragen im API-Modus
secure_proxy.py: Implementiert einen sicheren Proxy für die API-Kommunikation
_func.py: Enthält CSS- und JavaScript-Funktionen für die Benutzeroberfläche
Dateistruktur
´´´
quiz-system/
├── dataset/                # Enthält JSON-Dateien mit Fragen und erwarteten Antworten
├── modules/                # Enthält die Hauptmodule der Anwendung
│   ├── _func.py            # CSS und JavaScript für die UI
│   ├── chat_logic_api.py   # API-Modus Logik
│   ├── chat_logic_local.py # Lokaler Modus Logik
│   ├── secure_proxy.py     # Sicherer Proxy für API-Kommunikation
│   └── webui.py            # Hauptweboberfläche
├── venv/                   # Virtuelle Python-Umgebung (wird bei Installation erstellt)
├── installer.bat           # Installationsskript
├── requirements.txt        # Abhängigkeiten
├── run.vbs                 # Startskript
└── run_app.py              # Hauptanwendungsstarter
´´´

Funktionsweise
Initialisierung: run_app.py startet die Anwendung und fragt nach dem gewünschten Modus
Proxy (optional): Bei Verwendung des API-Modus kann ein sicherer Proxy gestartet werden
Weboberfläche: webui.py erstellt die Benutzeroberfläche mit Gradio
Themenauswahl: Die verfügbaren Themen werden aus dem Dataset-Verzeichnis geladen
Fragestellung: Nach Auswahl eines Themas wird eine Frage aus der entsprechenden JSON-Datei geladen
Antwortbewertung: Die Benutzerantwort wird an das LLM gesendet, das eine Bewertung und Feedback zurückgibt
Ergebnisanzeige: Die Bewertung, das Feedback und die erwartete Antwort werden angezeigt
Konfiguration
Hinzufügen neuer Fragen
Neue Fragen können als JSON-Dateien im dataset/-Verzeichnis hinzugefügt werden:

Erstellen Sie eine neue JSON-Datei mit dem Namen des Themas (z.B. Thema1.json)
Für Unterthemen verwenden Sie das Format Thema - Unterthema.json
Die JSON-Datei sollte folgendes Format haben:
[
  {
    "type": "question",
    "content": "Hier steht die Frage?",
    "expected_answer": "Hier steht die erwartete Antwort."
  }
]


API-Konfiguration
Für die Verwendung mit einer externen API:

Wählen Sie beim Start y für den API-Modus
Geben Sie Ihren API-Schlüssel und den Endpunkt ein
Alternativ können Sie den sicheren Proxy verwenden, der automatisch konfiguriert wird
Fehlerbehebung
Häufige Probleme
Problem	Lösung
Fehler beim Start	Stellen Sie sicher, dass Python korrekt installiert ist und die virtuelle Umgebung erstellt wurde
Proxy-Fehler	Überprüfen Sie, ob Port 8080 verfügbar ist und nicht von anderen Anwendungen blockiert wird
LM Studio-Verbindungsfehler	Stellen Sie sicher, dass LM Studio läuft und auf Port 1234 hört
Fehlende Themen	Überprüfen Sie, ob das dataset/-Verzeichnis existiert und JSON-Dateien enthält
Logs
Bei Problemen können Sie die Konsolenausgabe überprüfen, die wichtige Diagnoseinformationen enthält.
