import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import json
import logging
import re
from threading import Thread
from email.mime.base import MIMEBase
from email import encoders

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class EmailSpammerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Spammer v2.1")
        self.root.geometry("500x700")
        self.root.minsize(500, 700)

        # Farben
        self.bg_color = '#2b2b2b'
        self.fg_color = '#ffffff'
        self.entry_bg = '#3b3b3b'
        self.button_bg = '#404040'
        self.button_active_bg = '#4a4a4a'

        self.root.configure(bg=self.bg_color)

        main_container = tk.Frame(root, bg=self.bg_color)
        main_container.pack(fill="both", expand=True)

        canvas = tk.Canvas(main_container, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)

        self.content_frame = tk.Frame(canvas, bg=self.bg_color)

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        canvas_frame = canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        self.content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_frame, width=e.width))

        self.stop_spam = False
        self.attachments = []

        self.create_widgets()

    def create_widgets(self):
        # Sender Configuration
        sender_frame = self.create_label_frame("Sender Configuration")
        self.sender_email = self.create_labeled_entry(sender_frame, "Your Email:")
        self.sender_password = self.create_labeled_entry(sender_frame, "App Password:", show="*")

        # Target Configuration
        target_frame = self.create_label_frame("Target Configuration")
        self.target_email = self.create_labeled_entry(target_frame, "Target Email:")
        self.subject = self.create_labeled_entry(target_frame, "Subject:")

        # Message Configuration
        message_frame = self.create_label_frame("Message Configuration")
        tk.Label(message_frame, text="Message:", bg=self.bg_color, fg=self.fg_color).pack()
        self.message = tk.Text(message_frame, height=8, bg=self.entry_bg, fg=self.fg_color, insertbackground=self.fg_color)
        self.message.pack(padx=5, pady=5, fill="x")

        load_button = tk.Button(message_frame, text="Load from file", command=self.load_message,
                                bg=self.button_bg, fg=self.fg_color, activebackground=self.button_active_bg,
                                activeforeground=self.fg_color)
        load_button.pack(pady=5)

        attach_button = tk.Button(message_frame, text="Add Attachment", command=self.add_attachment,
                                  bg=self.button_bg, fg=self.fg_color, activebackground=self.button_active_bg,
                                  activeforeground=self.fg_color)
        attach_button.pack(pady=5)

        # Spam Configuration
        spam_frame = self.create_label_frame("Spam Configuration")
        self.num_emails = self.create_labeled_entry(spam_frame, "Number of emails:")
        self.delay = self.create_labeled_entry(spam_frame, "Delay (seconds):")

        # Bottom Buttons
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        self.start_button = tk.Button(button_frame, text="Start Sending", command=self.start_spam_thread,
                                      bg=self.button_bg, fg=self.fg_color, activebackground=self.button_active_bg,
                                      activeforeground=self.fg_color)
        self.start_button.pack(pady=5)

        stop_button = tk.Button(button_frame, text="Stop Sending", command=self.stop_spam_process,
                                bg=self.button_bg, fg=self.fg_color, activebackground=self.button_active_bg,
                                activeforeground=self.fg_color)
        stop_button.pack(pady=5)

        test_button = tk.Button(button_frame, text="Send Test Email", command=self.send_test_email,
                                bg=self.button_bg, fg=self.fg_color, activebackground=self.button_active_bg,
                                activeforeground=self.fg_color)
        test_button.pack(pady=5)

        save_button = tk.Button(button_frame, text="Save Config", command=self.save_config,
                                bg=self.button_bg, fg=self.fg_color, activebackground=self.button_active_bg,
                                activeforeground=self.fg_color)
        save_button.pack(pady=5)

        load_button = tk.Button(button_frame, text="Load Config", command=self.load_config,
                                bg=self.button_bg, fg=self.fg_color, activebackground=self.button_active_bg,
                                activeforeground=self.fg_color)
        load_button.pack(pady=5)

        preview_button = tk.Button(button_frame, text="Preview Message", command=self.preview_message,
                                   bg=self.button_bg, fg=self.fg_color, activebackground=self.button_active_bg,
                                   activeforeground=self.fg_color)
        preview_button.pack(pady=5)

        self.progress = ttk.Progressbar(button_frame, length=300, mode='determinate')
        self.progress.pack(pady=5)

        self.status_label = tk.Label(button_frame, text="Ready", bg=self.bg_color, fg=self.fg_color)
        self.status_label.pack()

    def create_label_frame(self, title):
        frame = tk.LabelFrame(self.content_frame, text=title, bg=self.bg_color, fg=self.fg_color)
        frame.pack(padx=10, pady=5, fill="x")
        return frame

    def create_labeled_entry(self, parent, label, show=None):
        tk.Label(parent, text=label, bg=self.bg_color, fg=self.fg_color).pack()
        entry = tk.Entry(parent, bg=self.entry_bg, fg=self.fg_color, insertbackground=self.fg_color, show=show)
        entry.pack(padx=5, pady=5, fill="x")
        return entry

    def load_message(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.message.delete(1.0, tk.END)
                    self.message.insert(tk.END, file.read())
            except Exception as e:
                logging.error(f"Error loading file: {e}")
                messagebox.showerror("Error", f"Could not load file: {str(e)}")

    def add_attachment(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.attachments.append(file_path)
            messagebox.showinfo("Attachment Added", f"Added: {file_path}")

    def save_config(self):
        config = {
            "sender_email": self.sender_email.get(),
            "sender_password": self.sender_password.get(),
            "target_email": self.target_email.get(),
            "subject": self.subject.get(),
            "message": self.message.get(1.0, tk.END).strip(),
            "num_emails": self.num_emails.get(),
            "delay": self.delay.get(),
            "attachments": self.attachments
        }
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(config, file, indent=4)
                messagebox.showinfo("Success", "Configuration saved successfully!")
            except Exception as e:
                logging.error(f"Error saving config: {e}")
                messagebox.showerror("Error", f"Could not save config: {str(e)}")

    def load_config(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    config = json.load(file)
                self.sender_email.insert(0, config.get("sender_email", ""))
                self.sender_password.insert(0, config.get("sender_password", ""))
                self.target_email.insert(0, config.get("target_email", ""))
                self.subject.insert(0, config.get("subject", ""))
                self.message.insert(1.0, config.get("message", ""))
                self.num_emails.insert(0, config.get("num_emails", ""))
                self.delay.insert(0, config.get("delay", ""))
                self.attachments = config.get("attachments", [])
                messagebox.showinfo("Success", "Configuration loaded successfully!")
            except Exception as e:
                logging.error(f"Error loading config: {e}")
                messagebox.showerror("Error", f"Could not load config: {str(e)}")

    def preview_message(self):
        preview = f"Subject: {self.subject.get()}\n\n{self.message.get(1.0, tk.END).strip()}"
        messagebox.showinfo("Message Preview", preview)

    def stop_spam_process(self):
        self.stop_spam = True
        self.status_label.config(text="Spam process stopped.")

    def start_spam_thread(self):
        self.stop_spam = False
        thread = Thread(target=self.start_spam)
        thread.start()

    def start_spam(self):
        try:
            num_emails = int(self.num_emails.get())
            delay = float(self.delay.get())

            if not all([self.sender_email.get(), self.sender_password.get(),
                        self.target_email.get(), self.subject.get(),
                        self.message.get(1.0, tk.END).strip()]):
                messagebox.showerror("Error", "Please fill all fields!")
                return

            self.start_button.config(state='disabled')
            self.progress['maximum'] = num_emails

            for i in range(num_emails):
                if self.stop_spam:
                    break
                self.send_email(i + 1)
                self.progress['value'] = i + 1
                self.status_label.config(text=f"Sent {i + 1}/{num_emails} emails")
                self.root.update()
                if i < num_emails - 1:
                    time.sleep(delay)

            if not self.stop_spam:
                messagebox.showinfo("Success", "All emails sent successfully!")
            else:
                messagebox.showinfo("Stopped", "Spam process was stopped.")

        except Exception as e:
            logging.error(f"Error during spam: {e}")
            messagebox.showerror("Error", str(e))
        finally:
            self.start_button.config(state='normal')
            self.progress['value'] = 0
            self.status_label.config(text="Ready")

    def send_email(self, count):
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.sender_email.get(), self.sender_password.get())

            msg = MIMEMultipart()
            msg['From'] = self.sender_email.get()
            msg['To'] = self.target_email.get()
            msg['Subject'] = f"{self.subject.get()} ({count})"
            msg.attach(MIMEText(self.message.get(1.0, tk.END), 'plain'))

            # Anhänge hinzufügen
            for attachment in self.attachments:
                try:
                    with open(attachment, 'rb') as file:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(file.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename="{attachment.split("/")[-1]}"')
                        msg.attach(part)
                except Exception as e:
                    logging.error(f"Failed to attach file {attachment}: {e}")
                    messagebox.showerror("Attachment Error", f"Could not attach file: {attachment}")

            server.send_message(msg)
            server.quit()

        except Exception as e:
            logging.error(f"Failed to send email {count}: {e}")
            raise Exception(f"Failed to send email: {str(e)}")

    def send_test_email(self):
        """Sendet eine Test-E-Mail, um die Konfiguration zu überprüfen."""
        try:
            if not self.sender_email.get() or not self.sender_password.get():
                messagebox.showerror("Error", "Please provide sender email and password!")
                return

            if not self.target_email.get():
                messagebox.showerror("Error", "Please provide a target email!")
                return

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.sender_email.get(), self.sender_password.get())

            msg = MIMEMultipart()
            msg['From'] = self.sender_email.get()
            msg['To'] = self.target_email.get()
            msg['Subject'] = "Test Email"
            msg.attach(MIMEText("This is a test email sent from the Email Spammer application.", 'plain'))

            server.send_message(msg)
            server.quit()

            messagebox.showinfo("Success", "Test email sent successfully!")
        except Exception as e:
            logging.error(f"Error sending test email: {e}")
            messagebox.showerror("Error", f"Could not send test email: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmailSpammerGUI(root)
    root.mainloop()
