from tkinter import *
from tkinter import messagebox

from db_utils import execute_fetchone, execute_update, BASE_DIR
import os

IMAGE_DIR = os.path.join(BASE_DIR, "images")


class SignupWindow:
    def __init__(self, root, on_login_click=None):
        self.root = root
        self.on_login_click = on_login_click
        self.root.geometry("450x400+500+200")
        self.root.config(bg="white")
        self.root.resizable(False, False)
        self.root.title("Sign Up")

        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_password = StringVar()

        title = Label(self.root, text="Create Account", font=("goudy old style", 22, "bold"),
                      bg="#184a45", fg="white").pack(side=TOP, fill=X, pady=20)

        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15), bg="white").place(x=50, y=100)
        Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(x=180, y=100, width=220)

        lbl_email = Label(self.root, text="Email", font=("goudy old style", 15), bg="white").place(x=50, y=150)
        Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15), bg="lightyellow").place(x=180, y=150, width=220)

        lbl_password = Label(self.root, text="Password", font=("goudy old style", 15), bg="white").place(x=50, y=200)
        Entry(self.root, textvariable=self.var_password, font=("goudy old style", 15), bg="lightyellow", show="*").place(x=180, y=200, width=220)

        btn_register = Button(self.root, text="Register", command=self.register,
                             font=("Helvetica", 13, "bold"), bg="#4caf50", fg="white",
                             cursor="hand2", highlightthickness=0).place(x=180, y=260, width=120, height=35)

        btn_login = Button(self.root, text="Back to Login", command=self._go_to_login,
                          font=("Helvetica", 12, "bold"), bg="#607d8b", fg="white",
                          cursor="hand2", highlightthickness=0).place(x=180, y=310, width=120, height=30)

    def _go_to_login(self):
        self.root.destroy()
        if self.on_login_click:
            self.on_login_click()

    def register(self):
        name = self.var_name.get().strip()
        email = self.var_email.get().strip()
        password = self.var_password.get()

        if not name:
            messagebox.showerror("Error", "Name is required", parent=self.root)
            return
        if not email:
            messagebox.showerror("Error", "Email is required", parent=self.root)
            return
        if not password:
            messagebox.showerror("Error", "Password is required", parent=self.root)
            return

        try:
            if execute_fetchone("SELECT * FROM users WHERE email=?", (email,)):
                messagebox.showerror("Error", "Email already registered", parent=self.root)
                return
            execute_update("INSERT INTO users(name,email,password) VALUES(?,?,?)", (name, email, password))
            messagebox.showinfo("Success", "Registration successful. You can now login.", parent=self.root)
            self._go_to_login()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {ex}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = SignupWindow(root)
    root.mainloop()
