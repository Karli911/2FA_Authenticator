#from gui.manage_accounts_gui import ManageAccountsWindow
from tkinter import Tk, Button, Entry, Label, Listbox, Toplevel, END, messagebox, OptionMenu, StringVar
from utils.database_manager import initialize_database
from utils.account_manager import get_all_accounts, delete_account
from encryption.encryption import load_encryption_key
from gui.login_gui import LoginWindow
from utils.language_manager import LanguageManager
import logging

class TwoFAGuiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("2FA.C")

        self.logger = logging.getLogger('2FA_Logger')

        self.encryption_key_file = 'data/encryption.key'
        self.db_path = 'data/accounts.db'
        self.encryption_key = load_encryption_key(self.encryption_key_file).decode('utf-8')

        self.language_manager = LanguageManager()
        self.current_language = StringVar(value=self.language_manager.current_language)

        self.logger.info("Initializing database.")
        initialize_database(self.db_path, self.encryption_key)

        self.create_login_window()

    def create_login_window(self):
        LoginWindow(self)

    def show_main_gui(self):
        self.logger.info("Showing main GUI.")
        self.root.title(self.language_manager.get_translation("main.title"))

        language_options = ["en", "es"]
        language_menu = OptionMenu(self.root, self.current_language, *language_options, command=self.change_language)
        language_menu.pack(pady=10)

        Label(self.root, text=self.language_manager.get_translation("main.search_accounts")).pack(pady=5)
        self.search_entry = Entry(self.root)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.filter_accounts)

        self.account_listbox = Listbox(self.root, height=10, width=50)
        self.account_listbox.pack(pady=10)
        self.update_account_listbox()

        self.add_account_btn = Button(self.root, text=self.language_manager.get_translation("main.add_account"), command=self.add_account)
        self.add_account_btn.pack(pady=10)

        self.verify_code_btn = Button(self.root, text=self.language_manager.get_translation("main.verify_code"), command=self.verify_code)
        self.verify_code_btn.pack(pady=10)

        self.manage_accounts_btn = Button(self.root, text=self.language_manager.get_translation("main.manage_accounts"), command=self.manage_accounts)
        self.manage_accounts_btn.pack(pady=10)

        self.backup_restore_btn = Button(self.root, text=self.language_manager.get_translation("main.backup_restore"), command=self.backup_restore)
        self.backup_restore_btn.pack(pady=10)

    def change_language(self, language_code):
        try:
            self.language_manager.set_language(language_code)
            self.logger.info(f"Language changed to {language_code}")
            messagebox.showinfo("Success", "Language changed successfully!")
            self.refresh_ui()
        except Exception as e:
            self.logger.error(f"Error changing language: {e}")
            messagebox.showerror("Error", "Failed to change language.")

    def refresh_ui(self):
        self.root.title(self.language_manager.get_translation("main.title"))
        for widget in self.root.winfo_children():
            widget.destroy()
        self.show_main_gui()

    def update_account_listbox(self):
        try:
            self.account_listbox.delete(0, END)
            accounts = get_all_accounts(self.db_path, self.encryption_key)
            for account in accounts:
                self.account_listbox.insert(END, account)
        except Exception as e:
            self.logger.error(f"Error updating account listbox: {e}")
            messagebox.showerror("Error", "Failed to update account list.")

    def filter_accounts(self, event):
        try:
            search_term = self.search_entry.get().lower()
            self.account_listbox.delete(0, END)
            accounts = get_all_accounts(self.db_path, self.encryption_key)
            for account in accounts:
                if search_term in account.lower():
                    self.account_listbox.insert(END, account)
        except Exception as e:
            self.logger.error(f"Error filtering accounts: {e}")
            messagebox.showerror("Error", "Failed to filter accounts.")

    def add_account(self):
        try:
            self.logger.info("Opening Add Account window.")
            from gui.add_account_gui import AddAccountWindow
            AddAccountWindow(self)
        except Exception as e:
            self.logger.error(f"Error opening Add Account window: {e}")
            messagebox.showerror("Error", "Failed to open Add Account window.")

    def verify_code(self):
        try:
            self.logger.info("Opening Verify Code window.")
            from gui.verify_code_gui import VerifyCodeWindow
            VerifyCodeWindow(self)
        except Exception as e:
            self.logger.error(f"Error opening Verify Code window: {e}")
            messagebox.showerror("Error", "Failed to open Verify Code window.")

    def manage_accounts(self):
        try:
            self.logger.info("Opening Manage Accounts window.")
            ManageAccountsWindow(self)
        except Exception as e:
            self.logger.error(f"Error opening Manage Accounts window: {e}")
            messagebox.showerror("Error", "Failed to open Manage Accounts window.")

    def backup_restore(self):
        try:
            self.logger.info("Opening Backup and Restore window.")
            from gui.backup_restore_gui import BackupRestoreWindow
            BackupRestoreWindow(self)
        except Exception as e:
            self.logger.error(f"Error opening Backup and Restore window: {e}")
            messagebox.showerror("Error", "Failed to open Backup and Restore window.")

class ManageAccountsWindow:
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.logger = logging.getLogger('2FA_Logger')
        self.language_manager = parent_app.language_manager
        self.window = Toplevel(parent_app.root)
        self.window.title(self.language_manager.get_translation("manage_accounts.title"))

        self.account_listbox = Listbox(self.window, height=10, width=50)
        self.account_listbox.pack(pady=10)
        self.update_account_listbox()

        self.delete_account_btn = Button(self.window, text=self.language_manager.get_translation("manage_accounts.delete_account"), command=self.delete_account)
        self.delete_account_btn.pack(pady=10)

    def update_account_listbox(self):
        try:
            self.account_listbox.delete(0, END)
            accounts = get_all_accounts(self.parent_app.db_path, self.parent_app.encryption_key)
            for account in accounts:
                self.account_listbox.insert(END, account)
        except Exception as e:
            self.logger.error(f"Error updating account listbox in Manage Accounts: {e}")
            messagebox.showerror("Error", "Failed to update account list.")

    def delete_account(self):
        try:
            selected_account = self.account_listbox.get(self.account_listbox.curselection())
            if selected_account:
                delete_account(self.parent_app.db_path, self.parent_app.encryption_key, selected_account)
                self.parent_app.logger.info(f"Deleted account: {selected_account}")
                messagebox.showinfo("Success", self.language_manager.get_translation("manage_accounts.success_delete_account").format(selected_account=selected_account))
                self.update_account_listbox()
                self.parent_app.update_account_listbox()
            else:
                messagebox.showerror("Error", self.language_manager.get_translation("manage_accounts.error_no_account_selected"))
        except Exception as e:
            self.logger.error(f"Error deleting account: {e}")
            messagebox.showerror("Error", self.language_manager.get_translation("manage_accounts.error_general"))

def main():
    
    root = Tk()
    app = TwoFAGuiApp(root)
    root.mainloop()
