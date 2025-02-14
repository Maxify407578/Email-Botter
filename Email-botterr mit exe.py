import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

class EmailSpammerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Spammer v1.0")
        self.root.geometry("500x700")
        self.root.minsize(500, 700)
        
        self.bg_color = '#2b2b2b'
        self.fg_color = '#ffffff'
        self.entry_bg = '#3b3b3b'
        self.button_bg = '#404040'
        self.button_active_bg = '#4a4a4a'
        
        self.root.configure(bg=self.bg_color)
        
        logo = """
        ╔══════════════════════════════════════════════════╗
        ║  ┏━┓╺┳╸╺┳╸┏━┓┏━┓╻┏ ╻ ╻╻  ╻     ┏┓ ┏━┓╺┳╸       ║
        ║  ┣━┫ ┃  ┃ ┣━┫┃ ┃┣┻┓┃ ┃┃  ┃     ┣┻┓┃ ┃ ┃        ║
        ║  ╹ ╹ ╹  ╹ ╹ ╹┗━┛╹ ╹┗━┛┗━╸┗━╸   ┗━┛┗━┛ ╹        ║
        ╚══════════════════════════════════════════════════╝
        """
        
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
        
        banner = tk.Label(self.content_frame, text=logo, font=('Courier', 8),
                         bg=self.bg_color, fg=self.fg_color)
        banner.pack(pady=10)

        sender_frame = tk.LabelFrame(self.content_frame, text="Sender Configuration", 
                                   bg=self.bg_color, fg=self.fg_color)
        sender_frame.pack(padx=10, pady=5, fill="x")

        target_frame = tk.LabelFrame(self.content_frame, text="Target Configuration",
                                   bg=self.bg_color, fg=self.fg_color)
        target_frame.pack(padx=10, pady=5, fill="x")

        message_frame = tk.LabelFrame(self.content_frame, text="Message Configuration",
                                    bg=self.bg_color, fg=self.fg_color)
        message_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(sender_frame, text="Your Email:", bg=self.bg_color, fg=self.fg_color).pack()
        self.sender_email = tk.Entry(sender_frame, bg=self.entry_bg, fg=self.fg_color,
                                   insertbackground=self.fg_color)
        self.sender_email.pack(padx=5, pady=5, fill="x")

        tk.Label(sender_frame, text="App Password:", bg=self.bg_color, fg=self.fg_color).pack()
        self.sender_password = tk.Entry(sender_frame, show="*", bg=self.entry_bg, 
                                      fg=self.fg_color, insertbackground=self.fg_color)
        self.sender_password.pack(padx=5, pady=5, fill="x")

        tk.Label(target_frame, text="Target Email:", bg=self.bg_color, fg=self.fg_color).pack()
        self.target_email = tk.Entry(target_frame, bg=self.entry_bg, fg=self.fg_color,
                                   insertbackground=self.fg_color)
        self.target_email.pack(padx=5, pady=5, fill="x")

        tk.Label(target_frame, text="Subject:", bg=self.bg_color, fg=self.fg_color).pack()
        self.subject = tk.Entry(target_frame, bg=self.entry_bg, fg=self.fg_color,
                              insertbackground=self.fg_color)
        self.subject.pack(padx=5, pady=5, fill="x")

        tk.Label(message_frame, text="Message:", bg=self.bg_color, fg=self.fg_color).pack()
        self.message = tk.Text(message_frame, height=8, bg=self.entry_bg, fg=self.fg_color,
                             insertbackground=self.fg_color)
        self.message.pack(padx=5, pady=5, fill="x")

        load_button = tk.Button(message_frame, text="Load from file", command=self.load_message,
                              bg=self.button_bg, fg=self.fg_color, 
                              activebackground=self.button_active_bg,
                              activeforeground=self.fg_color)
        load_button.pack(pady=5)

        spam_frame = tk.LabelFrame(self.content_frame, text="Spam Configuration",
                                 bg=self.bg_color, fg=self.fg_color)
        spam_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(spam_frame, text="Number of emails:", bg=self.bg_color, fg=self.fg_color).pack()
        self.num_emails = tk.Entry(spam_frame, bg=self.entry_bg, fg=self.fg_color,
                                 insertbackground=self.fg_color)
        self.num_emails.pack(padx=5, pady=5, fill="x")

        tk.Label(spam_frame, text="Delay (seconds):", bg=self.bg_color, fg=self.fg_color).pack()
        self.delay = tk.Entry(spam_frame, bg=self.entry_bg, fg=self.fg_color,
                            insertbackground=self.fg_color)
        self.delay.pack(padx=5, pady=5, fill="x")

        button_frame = tk.Frame(root, bg=self.bg_color)
        button_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        self.start_button = tk.Button(button_frame, text="Start Sending", command=self.start_spam,
                                    bg=self.button_bg, fg=self.fg_color,
                                    activebackground=self.button_active_bg,
                                    activeforeground=self.fg_color)
        self.start_button.pack(pady=5)

        self.progress = ttk.Progressbar(button_frame, length=300, mode='determinate')
        self.progress.pack(pady=5)
        
        self.status_label = tk.Label(button_frame, text="Ready", bg=self.bg_color, fg=self.fg_color)
        self.status_label.pack()

    def load_message(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.message.delete(1.0, tk.END)
                    self.message.insert(tk.END, file.read())
            except Exception as e:
                messagebox.showerror("Error", f"Could not load file: {str(e)}")

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
                self.send_email(i+1)
                self.progress['value'] = i + 1
                self.status_label.config(text=f"Sent {i+1}/{num_emails} emails")
                self.root.update()
                if i < num_emails - 1:
                    time.sleep(delay)
            
            messagebox.showinfo("Success", "All emails sent successfully!")
            
        except Exception as e:
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

            server.send_message(msg)
            server.quit()
            
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailSpammerGUI(root)
    root.mainloop()
