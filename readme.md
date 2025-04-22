# 📧 Email Spammer Tool

Ein leistungsstarkes Python-Tool zum automatisierten Versenden von E-Mails mit modernem Dark-Mode Interface.

## 🚀 Features

- Modernes Dark-Mode Interface
- ASCII-Art Logo Design
- Scrollbare Benutzeroberfläche
- Datei-Upload für Nachrichten
- Fortschrittsanzeige in Echtzeit
- Fehlerbehandlung und Status-Updates
- Konfigurierbare Versandparameter:
  - Absender E-Mail
  - Ziel E-Mail
  - Betreff
  - Nachricht
  - Anzahl der E-Mails
  - Verzögerung zwischen E-Mails
  - Anhänge hinzufügen
- Unterstützung für das Speichern und Laden von Konfigurationen
- Vorschau der Nachricht vor dem Versand
- Möglichkeit, den Spam-Prozess zu stoppen
- Test-E-Mail-Funktion zur Überprüfung der Konfiguration

## ⚙️ Installation

1. Stelle sicher, dass Python 3.x installiert ist
2. Installiere die benötigten Bibliotheken:
```bash
pip install tkinter
```

## 📋 Voraussetzungen

- Python 3.x
- Gmail-Konto
- Gmail App-Passwort

### Gmail App-Passwort einrichten:

1. Gehe zu [Google-Kontoeinstellungen](https://myaccount.google.com/)
2. Aktiviere 2-Faktor-Authentifizierung
3. Gehe zu "Sicherheit" → "App-Passwörter"
4. Wähle "Sonstige (Benutzerdefinierter Name)"
5. Gib einen Namen ein (z.B. "Email Spammer")
6. Kopiere das generierte 16-stellige Passwort

## 🎮 Verwendung

1. Starte das Programm:
```bash
python Email-botterr mit exe.py
```

2. Konfiguriere die Einstellungen im GUI:
   - Gib deine Gmail-Adresse ein
   - Gib dein App-Passwort ein
   - Konfiguriere die Ziel-E-Mail-Adresse
   - Stelle Betreff ein
   - Gib die Nachricht direkt ein oder lade sie aus einer Datei
   - Füge Anhänge hinzu (optional)
   - Lege Anzahl der E-Mails und Verzögerung fest
   - Klicke "Start Sending"

3. Zusätzliche Funktionen:
   - Speichere deine Konfiguration mit "Save Config"
   - Lade eine gespeicherte Konfiguration mit "Load Config"
   - Vorschau der Nachricht mit "Preview Message"
   - Sende eine Test-E-Mail mit "Send Test Email"
   - Stoppe den Spam-Prozess mit "Stop Sending"

## ⚠️ Wichtige Hinweise

- Verwende NIEMALS dein normales Gmail-Passwort
- Nutze ausschließlich ein App-Passwort
- Gmail hat Versandlimits:
  - 500 E-Mails pro Tag
  - 100 Empfänger pro E-Mail
  - Maximal 2000 E-Mails in 24 Stunden

## 🛡️ Haftungsausschluss

Dieses Tool wurde zu Bildungszwecken erstellt. Der Missbrauch des Tools ist nicht gestattet. Der Entwickler übernimmt keine Verantwortung für eventuellen Missbrauch.

## 🔧 Technische Details

- Sprache: Python 3
- GUI: Tkinter
- Hauptbibliotheken:
  - tkinter
  - smtplib
  - email.mime
  - time
  - json
  - threading

## 🤝 Beitragen

1. Fork das Projekt
2. Erstelle einen Feature Branch
3. Committe deine Änderungen
4. Push zu dem Branch
5. Öffne einen Pull Request

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.

## 👨‍💻 Entwickler

Entwickelt von MaxSchueller

## 📞 Support

Bei Fragen oder Problemen öffne bitte ein Issue im GitHub Repository.

---
⚡ Powered by Python & Gmail
