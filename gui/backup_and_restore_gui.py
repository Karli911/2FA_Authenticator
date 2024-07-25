from tkinter import Toplevel, Label, Button, filedialog, messagebox
from utils.backup_manager import backup_database, restore_database
import logging

class BackupRestoreWindow:
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.logger = logging.getLogger('2FA_Logger')
        self.window = Toplevel(parent_app.root)
        self.window.title("Backup and Restore")

        self.backup_btn = Button(self.window, text="Backup Database", command=self.backup_database)
        self.backup_btn.pack(pady=10)

        self.restore_btn = Button(self.window, text="Restore Database", command=self.restore_database)
        self.restore_btn.pack(pady=10)

    def backup_database(self):
        try:
            backup_dir = filedialog.askdirectory(title="Select Backup Directory")
            if backup_dir:
                backup_file = backup_database(self.parent_app.db_path, backup_dir)
                self.logger.info(f"Database backed up to {backup_file}")
                messagebox.showinfo("Success", f"Database backed up to {backup_file}")
        except Exception as e:
            self.logger.error(f"Error during backup: {e}")
            messagebox.showerror("Error", "Failed to backup database.")

    def restore_database(self):
        try:
            backup_file = filedialog.askopenfilename(title="Select Backup File", filetypes=[("Database Files", "*.db")])
            if backup_file:
                restore_database(backup_file, self.parent_app.db_path)
                self.logger.info(f"Database restored from {backup_file}")
                messagebox.showinfo("Success", f"Database restored from {backup_file}")
                self.parent_app.update_account_listbox()
        except Exception as e:
            self.logger.error(f"Error during restore: {e}")
            messagebox.showerror("Error", "Failed to restore database.")