# email-invoice-processor

Bei diesem Projekt handelt es sich um ein automatisiertes Tool zur Erkennung von Rechnungen in einem E-Mail-Posteingang, zur Extraktion relevanter Informationen sowohl aus dem E-Mail-Inhalt als auch aus PDF-Anhängen und zur übersichtlichen Darstellung der Daten. Das Tool nutzt IMAP für den E-Mail-Abruf, Tesseract OCR für die Textextraktion und Regex/AI-Methoden für die Extraktion von Rechnungsfeldern. Die extrahierten Daten werden in MongoDB gespeichert und können über ein einfaches Web-Dashboard eingesehen werden.

## Features

- **E-Mail-Verarbeitung:** Verbindet sich mit einem IMAP-Postfach und filtert Rechnungs-E-Mails.
- **Anhangsverarbeitung:** Lädt PDF-Anhänge herunter und verarbeitet sie.
- **OCR-Extraktion:** Verwendet Tesseract OCR, um Text aus PDFs zu extrahieren.
- **Rechnungsdatenextraktion:** Wendet Regex und optionale AI-Methoden an, um Felder wie Rechnungsnummer, Gesamtbetrag und Fälligkeitsdatum zu extrahieren.
- **Datenbankspeicherung:** Speichert die extrahierten Rechnungsdaten in MongoDB.
- **Dashboard (optionaler Bonus):** Eine Flask-basierte Benutzeroberfläche zum Anzeigen und manuellen Überprüfen von Rechnungsdaten.
- **Bonusfunktionen (optional):**
  - Automatische Erkennung von wiederkehrenden Rechnungen und Duplikaten.
  - UI zur manuellen Überprüfung oder Korrektur der extrahierten Daten.


## Einrichtung und Installation

1. **Klone das Repository:**

   ```bash
   git clone https://github.com/iamdurgesh/email-invoice-processor.git
   cd email-invoice-processor

## Erstellung einer virtuellen Umgebung und deren Aktivierung:
python -m venv aivenv
source aivenv/bin/activate   # On Windows: aivenv\Scripts\activate

## Abhängigkeiten installieren:
pip install -r requirements.txt
Hinweis: Stellen Sie sicher, dass Sie Tesseract OCR auf Ihrem System installiert haben (und poppler für die PDF-Konvertierung).
brew install tesseract poppler (*Für macOS*)

## Setup MongoDB:

Installieren und starten Sie MongoDB lokal (oder verwenden Sie MongoDB Atlas).
Für die lokale Installation unter macOS können Sie Homebrew verwenden:

brew tap mongodb/brew
brew install mongodb-community@6.0
brew services start mongodb-community@6.0

 Verarbeitung von Rechnungen
Bevor die Hauptpipeline ausgeführt wird, müssen die Umgebungsvariablen gesetzt werden.

## 1. .env-Datei erstellen und konfigurieren
Falls noch nicht geschehen, erstelle eine .env-Datei im Hauptverzeichnis des Projekts und füge folgende Zeilen hinzu:
IMAP_SERVER=imap.gmail.com
EMAIL_ACCOUNT=dein-email@gmail.com
EMAIL_PASSWORD=dein-sicheres-app-passwort
MAILBOX=INBOX

##  2️. Abhängigkeiten installieren
Falls nicht bereits geschehen, installiere die benötigten Pakete:
pip install -r requirements.txt

##  3️. Rechnungen verarbeiten
Um Rechnungen zu extrahieren, führen Sie die Hauptpipeline aus:
python -m src.main

### 4. Workflow
🚀 Projektablauf
1️⃣ E-Mails über IMAP abrufen
🔹 Die Anwendung stellt eine Verbindung zum IMAP-E-Mail-Postfach her und ruft alle relevanten E-Mails ab.
🔹 Anhand von Betreffzeilen (z. B. "Rechnung", "Invoice") werden Rechnungen automatisch identifiziert.
🔹 Der E-Mail-Text und alle Anhänge werden für die weitere Verarbeitung gespeichert.

📂 Wichtige Dateien:

email_processor.py → Verbindet sich mit dem E-Mail-Server und ruft Rechnungen ab.
utils.py → Extrahiert den Klartext aus der E-Mail.
2️⃣ Anhänge (Rechnungen im PDF-Format) verarbeiten
🔹 Falls eine E-Mail eine PDF-Rechnung enthält, wird diese automatisch heruntergeladen und gespeichert.
🔹 Das PDF wird mit pdf2image in Bilder umgewandelt.
🔹 OCR (Optical Character Recognition) mit Tesseract extrahiert den reinen Text aus der Rechnung.

📂 Wichtige Dateien:

attachments.py → Speichert Anhänge aus E-Mails.
ocr.py → Nutzt OCR-Technologie zur Textextraktion aus PDFs.
3️⃣ Rechnungsdaten mit KI & Regex extrahieren
🔹 Der aus der E-Mail und dem Anhang extrahierte Text wird an eine KI-gestützte Named Entity Recognition (NER) weitergegeben, um folgende Felder zu erkennen:

Absender (E-Mail-Adresse des Rechnungsstellers)
Rechnungsnummer
Gesamtbetrag
Fälligkeitsdatum
🔹 Falls die KI nicht alle Daten erkennt, wird ein Regex-gestützter Fallback-Mechanismus verwendet.
🔹 Die extrahierten Rechnungsdaten werden in eine strukturierte JSON-Datei umgewandelt.
📂 Wichtige Dateien:

ai_extraction.py → Nutzt ein BERT-gestütztes KI-Modell zur Datenextraktion.
utils.py → Wendet reguläre Ausdrücke (Regex) als Backup-Methode an.
4️⃣ Speicherung der Rechnungsdaten in MongoDB
🔹 Die strukturierten Rechnungsinformationen werden in MongoDB gespeichert.
🔹 Vor der Speicherung wird geprüft, ob die Rechnung bereits existiert, um Dubletten zu vermeiden.
🔹 Jede Rechnung enthält:

Absender (E-Mail des Rechnungsstellers)
Rechnungsnummer
Betrag
Fälligkeitsdatum
Zeitstempel der Extraktion
📂 Wichtige Dateien:

db.py → Verbindet sich mit der MongoDB-Datenbank.
main.py → Führt den gesamten Verarbeitungsprozess durch und speichert Rechnungsdaten.
5️⃣ Rechnungen in einem Web-Dashboard anzeigen (Flask)
🔹 Die gespeicherten Rechnungen können über ein Flask-Web-Dashboard angezeigt und manuell bearbeitet werden.
🔹 Benutzer können nach Rechnungen suchen, diese filtern und korrigieren.
🔹 Das Dashboard ruft alle Rechnungen aus MongoDB ab und stellt sie in einer übersichtlichen Benutzeroberfläche dar.

📂 Wichtige Dateien:

dashboard.py → Flask-Server zur Anzeige der Rechnungen.
templates/index.html → Web-UI für die Darstellung der Rechnungsdaten





### 5. Features 

- **Erkennung von wiederkehrenden Rechnungen:** Das System prüft auf doppelte Rechnungsnummern, um zu vermeiden, dass dieselbe Rechnung mehrfach bearbeitet wird. (in der db.py: Es wurde eine Datenbank-Speicherfunktion zur Überprüfung auf Duplikate hinzugefügt. Jedes Mal, wenn eine Rechnung verarbeitet wird, prüft das System vor dem Speichern, ob es sich um ein Duplikat handelt).


Add Email Classification 
Instead of searching for "Invoice" in the subject line, you can train or fine-tune a text classification model (e.g., a small BERT or DistilBERT) to determine whether an email is likely an invoice. This would reduce reliance on a strict keyword match.