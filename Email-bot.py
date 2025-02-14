import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import os
import sys

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slow(str):
    for char in str:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    print()

# Sprachdefinitionen
SPRACHEN = {
    "de": {
        "waehle_sprache": "[?] Wählen Sie Ihre Sprache / Choose your language (de/en): ",
        "ungueltige_sprache": "[!] Ungültige Auswahl. Bitte 'de' oder 'en' eingeben.",
        "banner": "CyberMail Exploit Framework v1.0\nCoded by MaxSchueller",
        "config": "Mail-Exploit Konfiguration",
        "empfaenger": "[>] Target Mail-Adresse: ",
        "betreff": "[>] Exploit Betreff: ",
        "nachricht": "[>] Payload (Enter zum Bestätigen):",
        "einstellungen": "Exploit Parameter",
        "anzahl": "[#] Anzahl der Exploits: ",
        "verzoegerung": "[#] Verzögerung zwischen Exploits (sec): ",
        "positive_zahl": "[!] ERROR: Positive Zahl erforderlich!",
        "gueltige_zahl": "[!] ERROR: Ungültige Eingabe!",
        "start": "Initialisiere Exploit-Sequenz...",
        "ende": "Mission accomplished!",
        "sender_email": "[>] Deine E-Mail-Adresse: ",
        "sender_password": "[>] Dein App-Passwort: ",
        "nachricht_wahl": "[?] Nachricht eingeben (1) oder aus Datei laden (2)? ",
        "datei_pfad": "[>] Pfad zur Textdatei: ",
        "datei_error": "[!] Fehler beim Lesen der Datei. Bitte überprüfen Sie den Pfad.",
        "mehrzeilig_ende": "[i] Beenden Sie die Eingabe mit einer leeren Zeile (Enter)"
    },
    "en": {
        "waehle_sprache": "[?] Choose your language / Wählen Sie Ihre Sprache (de/en): ",
        "ungueltige_sprache": "[!] Invalid choice. Please enter 'de' or 'en'.",
        "banner": "CyberMail Exploit Framework v1.0\nCoded by MaxSchueller",
        "config": "Mail-Exploit Configuration",
        "empfaenger": "[>] Target Mail Address: ",
        "betreff": "[>] Exploit Subject: ",
        "nachricht": "[>] Payload (Press Enter to confirm):",
        "einstellungen": "Exploit Parameters",
        "anzahl": "[#] Number of Exploits: ",
        "verzoegerung": "[#] Delay between Exploits (sec): ",
        "positive_zahl": "[!] ERROR: Positive number required!",
        "gueltige_zahl": "[!] ERROR: Invalid input!",
        "start": "Initializing Exploit Sequence...",
        "ende": "Mission accomplished!",
        "sender_email": "[>] Your email address: ",
        "sender_password": "[>] Your app password: ",
        "nachricht_wahl": "[?] Enter message (1) or load from file (2)? ",
        "datei_pfad": "[>] Path to text file: ",
        "datei_error": "[!] Error reading file. Please check the path.",
        "mehrzeilig_ende": "[i] End input with an empty line (Enter)"
    }
}

class EmailBot:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def verbinde(self):
        """Verbindung zum SMTP-Server herstellen"""
        self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        self.server.starttls()
        self.server.login(self.sender_email, self.sender_password)

    def sende_emails(self, empfaenger, betreff, nachricht, anzahl=1, verzoegerung=1):
        """Mehrere E-Mails senden
        
        Args:
            empfaenger: E-Mail-Adresse des Empfängers
            betreff: Betreff der E-Mail
            nachricht: Inhalt der E-Mail
            anzahl: Anzahl der zu sendenden E-Mails (Standard: 1)
            verzoegerung: Wartezeit zwischen E-Mails in Sekunden (Standard: 1)
        """
        for i in range(anzahl):
            # E-Mail erstellen
            email = MIMEMultipart()
            email["From"] = self.sender_email
            email["To"] = empfaenger
            email["Subject"] = f"{betreff} ({i+1}/{anzahl})"

            # Nachricht hinzufügen
            email.attach(MIMEText(nachricht, "plain"))

            try:
                # Verbindung herstellen und E-Mail senden
                self.verbinde()
                self.server.send_message(email)
                print(f"E-Mail {i+1}/{anzahl} wurde erfolgreich an {empfaenger} gesendet!")
            except Exception as e:
                print(f"Fehler beim Senden der E-Mail {i+1}/{anzahl}: {e}")
            finally:
                # Verbindung schließen
                self.server.quit()
            
            # Warte zwischen den E-Mails
            if i < anzahl-1:  # Keine Verzögerung nach der letzten E-Mail
                time.sleep(verzoegerung)

# Beispiel für die Verwendung
if __name__ == "__main__":
    clear()
    
    # Matrix-Style Banner
    banner = """
    \033[32m
    ╔══════════════════════════════════════════════════╗
    ║  ╔═╗┌┬┐┌─┐┬┬    ╔═╗┌─┐┌─┐┌┬┐┌┬┐┌─┐┬─┐         ║
    ║  ║╣ │││├─┤││    ╚═╗├─┘├─┤││││││├┤ ├┬┘         ║
    ║  ╚═╝┴ ┴┴ ┴┴┴─┘  ╚═╝┴  ┴ ┴┴ ┴┴ ┴└─┘┴└─         ║
    ╚══════════════════════════════════════════════════╝
    \033[0m"""
    
    print(banner)
    time.sleep(1)

    # Sprachauswahl
    while True:
        sprache = input("\033[32m" + "\nWählen Sie Ihre Sprache / Choose your language (de/en): " + "\033[0m").lower()
        if sprache in SPRACHEN:
            break
        print("\033[31m" + "Invalid choice. Please enter 'de' or 'en'." + "\033[0m")

    text = SPRACHEN[sprache]
    clear()
    print(banner)

    # Exploit Konfiguration
    print("\n" + "="*50)
    print_slow("\033[32m[*] " + text['config'] + "\033[0m")
    print("="*50)

    # Mail Credentials
    print("\033[32m" + "\n[*] Sender Konfiguration" + "\033[0m")
    sender_email = input("\033[32m" + f"{text['sender_email']}" + "\033[0m")
    sender_password = input("\033[32m" + f"{text['sender_password']}" + "\033[0m")

    bot = EmailBot(sender_email, sender_password)

    # Target Konfiguration
    print("\033[32m" + "\n[*] Target Konfiguration" + "\033[0m")
    empfaenger = input("\033[32m" + f"{text['empfaenger']}" + "\033[0m")
    betreff = input("\033[32m" + f"{text['betreff']}" + "\033[0m")
    print("\033[32m" + f"\n{text['nachricht']}" + "\033[0m")

    # Nachrichteneingabe
    print("\033[32m" + f"\n{text['nachricht']}" + "\033[0m")
    while True:
        nachricht_option = input("\033[32m" + f"{text['nachricht_wahl']}" + "\033[0m")
        if nachricht_option in ['1', '2']:
            break
        print("\033[31m" + text['gueltige_zahl'] + "\033[0m")

    if nachricht_option == '1':
        # Mehrzeilige Eingabe
        print("\033[32m" + text['mehrzeilig_ende'] + "\033[0m")
        nachricht_zeilen = []
        while True:
            zeile = input("\033[32m" + "> " + "\033[0m")
            if zeile == "":
                break
            nachricht_zeilen.append(zeile)
        nachricht = "\n".join(nachricht_zeilen)
    else:
        # Aus Datei laden
        while True:
            datei_pfad = input("\033[32m" + f"{text['datei_pfad']}" + "\033[0m")
            try:
                with open(datei_pfad, 'r', encoding='utf-8') as file:
                    nachricht = file.read()
                break
            except:
                print("\033[31m" + text['datei_error'] + "\033[0m")

    print("\n" + "="*50)
    print_slow("\033[32m[*] " + text['einstellungen'] + "\033[0m")
    print("="*50)

    while True:
        try:
            anzahl_emails = int(input("\033[32m" + f"\n{text['anzahl']}" + "\033[0m"))
            if anzahl_emails > 0:
                break
            print("\033[31m" + text['positive_zahl'] + "\033[0m")
        except ValueError:
            print("\033[31m" + text['gueltige_zahl'] + "\033[0m")

    while True:
        try:
            verzoegerung = float(input("\033[32m" + f"{text['verzoegerung']}" + "\033[0m"))
            if verzoegerung >= 0:
                break
            print("\033[31m" + text['positive_zahl'] + "\033[0m")
        except ValueError:
            print("\033[31m" + text['gueltige_zahl'] + "\033[0m")

    print("\n" + "="*50)
    print_slow("\033[32m[*] " + text['start'] + "\033[0m")
    print("="*50 + "\n")

    # Loading animation
    for i in range(10):
        sys.stdout.write("\033[32m" + "\rInitializing system [" + "=" * i + ">" + " " * (9-i) + "]" + "\033[0m")
        sys.stdout.flush()
        time.sleep(0.2)
    print("\n")

    bot.sende_emails(empfaenger, betreff, nachricht, anzahl_emails, verzoegerung)

    print("\n" + "="*50)
    print_slow("\033[32m[+] " + text['ende'] + "\033[0m")
    print("="*50)
