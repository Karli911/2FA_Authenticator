from tkinter import Toplevel, Label, Entry, Button, messagebox
from utils.auth_manager import verify_user
import logging

class LoginWindow:
  def __init__(self, parent_app):
    self.parent_app = parent_app
    self.logger = logging.getLogger("2FA Logger")
    self.window = Toplevel(parent_app.root)
    self.window.title("Login")
    Label(self.window, text = "Username: ").pack(pady=5)
    self.username_entry = Entry(self.window)
    self.username_entry.pack(pady=5)
    Label(self.window, text="Password").pack(pady=5)
    self.password_entry = Entry(self.window, show="*")
    self.password_entry.pack(pady=5)
    self.login_btn = Button(self.window, text="Login", command=self.login)
    self.login_btn.pack(pady=10)

  def login(self):
    username = self.username_entry.get()
    password = self.password_entry.get()
    if not username or not password:
      self.logger.warning("Login attempt with empty fields.")
      messagebox.showerror("Error", "Please enter both username and password.")
      return
    if verify_user(self.parent_app.db_path, self.parent_app.encryption_key, username, password):
      self.logger.info(f"User {username} logged i  successfully.")
      messagebox.showinfo("Success", "Login successful!")
      self.window.destroy()
      self.parent_app.show_main_gui()
    else:
      self.logger.warning(f"Failed login attempt for username {username}")
      messagebox.showerror("Error", "Invalid username or password.")