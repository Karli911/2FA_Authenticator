from tkinter import Toplevel, Label, Entry, Button, messagebox
from utils.account_manager import add_account
from utils.backup_manager import generate_backup_codes, save_backup_codes
from utils.qr_code_manager import generate_qr_code
from encryption.encryption import generate_secret_key
from PIL import Image, ImageTk
import logging

class AddAccountWindow:
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.logger = logging.getLogger('2FA_Logger')
        self.window = Toplevel(parent_app.root)
        self.language_manager = parent_app.language_manager
        self.window.title(self.language_manager.get_translation("add_account.title"))

        Label(self.window, text=self.language_manager.get_translation("add_account.user_email")).pack(pady=5)
        self.user_email_entry = Entry(self.window)
        self.user_email_entry.pack(pady=5)

        self.add_account_submit_btn = Button(self.window, text=self.language_manager.get_translation("add_account.generate_qr_code"), command=self.generate_qr_code_gui)
        self.add_account_submit_btn.pack(pady=10)

    def generate_qr_code_gui(self):
        user_email = self.user_email_entry.get()

        if not user_email:
            self.logger.warning("Attempt to add account without providing an email.")
            messagebox.showerror("Error", self.language_manager.get_translation("add_account.error_empty_email"))
            return

        try:
            secret_key = generate_secret_key()
            qr_path, provisioning_uri = generate_qr_code(secret_key, user_email)

            backup_codes = generate_backup_codes()
            add_account(self.parent_app.db_path, self.parent_app.encryption_key, user_email, secret_key, backup_codes)
            save_backup_codes(user_email, backup_codes, self.parent_app.backup_file)

            self.logger.info(f"Added new account for {user_email}.")
            self.show_qr_code(qr_path, provisioning_uri)
        except Exception as e:
            self.logger.error(f"Error generating QR code for {user_email}: {e}")
            messagebox.showerror("Error", "Failed to generate QR code. Please try again.")

    def show_qr_code(self, qr_path, provisioning_uri):
        self.qr_code_window = Toplevel(self.window)
        self.qr_code_window.title("QR Code")

        try:
            img = Image.open(qr_path)
            img = ImageTk.PhotoImage(img)

            img_label = Label(self.qr_code_window, image=img)
            img_label.image = img  # Keep a reference!
            img_label.pack(pady=10)

            Label(self.qr_code_window, text="Provisioning URI:").pack(pady=5)
            uri_text = Text(self.qr_code_window, height=2, width=50) # noqa: F821
            uri_text.pack(pady=5)
            uri_text.insert("1.0", provisioning_uri)
            uri_text.config(state="disabled")
        except Exception as e:
            self.logger.error(f"Error displaying QR code: {e}")
            messagebox.showerror("Error", "Failed to display QR code.")