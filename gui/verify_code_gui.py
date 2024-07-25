from tkinter import Toplevel, Label, Entry, Button, messagebox
from utils.account_manager import get_account, update_backup_codes
from utils.backup_manager import generate_backup_codes
from encryption.encryption import verify_code
import logging

class VerifyCodeWindow:
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.logger = logging.getLogger('2FA_Logger')
        self.window = Toplevel(parent_app.root)
        self.language_manager = parent_app.language_manager
        self.window.title(self.language_manager.get_translation("verify_code.title"))

        Label(self.window, text=self.language_manager.get_translation("verify_code.user_email")).pack(pady=5)
        self.verify_email_entry = Entry(self.window)
        self.verify_email_entry.pack(pady=5)

        Label(self.window, text=self.language_manager.get_translation("verify_code.totp_code")).pack(pady=5)
        self.totp_code_entry = Entry(self.window)
        self.totp_code_entry.pack(pady=5)

        self.verify_code_submit_btn = Button(self.window, text=self.language_manager.get_translation("verify_code.title"), command=self.verify_totp_code)
        self.verify_code_submit_btn.pack(pady=10)

    def verify_totp_code(self):
        user_email = self.verify_email_entry.get()
        totp_code = self.totp_code_entry.get()

        if not user_email:
            self.logger.warning("Attempt to verify code without providing an email.")
            messagebox.showerror("Error", self.language_manager.get_translation("verify_code.error_empty_email"))
            return

        if not totp_code:
            self.logger.warning("Attempt to verify code without providing a TOTP code.")
            messagebox.showerror("Error", self.language_manager.get_translation("verify_code.error_empty_totp_code"))
            return

        try:
            secret_key, backup_codes = get_account(self.parent_app.db_path, self.parent_app.encryption_key, user_email)
            if secret_key:
                if verify_code(secret_key, totp_code):
                    self.logger.info(f"Valid TOTP code for {user_email}.")
                    messagebox.showinfo("Success", self.language_manager.get_translation("verify_code.success_valid_code"))
                else:
                    backup_code = messagebox.askstring(self.language_manager.get_translation("verify_code.error_invalid_code"))
                    if backup_code and backup_code in backup_codes:
                        self.logger.info(f"Valid backup code used for {user_email}.")
                        messagebox.showinfo("Success", self.language_manager.get_translation("verify_code.success_backup_code"))
                        backup_codes.remove(backup_code)
                        new_backup_codes = generate_backup_codes()
                        backup_codes.extend(new_backup_codes)
                        update_backup_codes(self.parent_app.db_path, self.parent_app.encryption_key, user_email, backup_codes)
                    else:
                        self.logger.warning(f"Invalid TOTP and backup code for {user_email}.")
                        messagebox.showerror("Error", self.language_manager.get_translation("verify_code.error_invalid_backup_code"))
            else:
                self.logger.warning(f"Attempt to verify code for non-existent account: {user_email}.")
                messagebox.showerror("Error", self.language_manager.get_translation("verify_code.error_no_account"))
        except Exception as e:
            self.logger.error(f"Error verifying code for {user_email}: {e}")
            messagebox.showerror("Error", self.language_manager.get_translation("verify_code.error_general"))