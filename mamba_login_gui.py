# Mamba Password Manager - Login GUI

# Modules
import tkinter as tk
import customtkinter as ctk
from mamba_account_database import MambaAccountDB
from PIL import Image
from CTkMessagebox import CTkMessagebox
import sqlite3
from mamba_main_gui import MainGUI

# Constants
FONT = "Century Gothic"
FG_COLOR = "purple"
TEXT_COLOR = "black"
HOVER_COLOR = "#FF69B4"
MISSING_USERNAME = CTkMessagebox


# Login GUI Class
class LoginGUI:
    def __init__(self, db):
        self.db = db
        self.conn = sqlite3.connect("mamba_userdata.db")
        self.cur = self.conn.cursor()

        self.root = ctk.CTkToplevel()
        self.root.title("Mamba Password Manager - Login")
        self.root.resizable(False, False)
        self.root.geometry("600x440")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Create login form
        self.bg_login_image = ctk.CTkImage(
            dark_image=Image.open(
                "gui_images/login_gui_image.jpg",
            ),
            size=(600, 440),
        )
        self.image_label = ctk.CTkLabel(master=self.root, image=self.bg_login_image)
        self.image_label.pack()

        # Create Login Frame
        self.login_frame = ctk.CTkFrame(
            master=self.image_label,
            width=320,
            height=360,
            corner_radius=5,
            border_width=3,
            border_color="purple",
        )
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create Mamba Title Label
        mamba_title_label = ctk.CTkLabel(
            master=self.login_frame,
            text="Mamba - Password Manager",
            font=(
                FONT,
                20,
            ),
            text_color="purple",
        )
        mamba_title_label.place(x=30, y=45)

        # Create Username Entry

        self.username_entry = ctk.CTkEntry(
            master=self.root,
            textvariable=self.username_var,
            text_color="#FF69B4",
            placeholder_text="Username",
            placeholder_text_color="purple",
            width=200,
            border_width=2,
            border_color="purple",
        )
        self.username_entry.place(x=200, y=150)

        # Create Password Entry

        self.password_entry = ctk.CTkEntry(
            master=self.root,
            textvariable=self.password_var,
            show="*",
            text_color="#FF69B4",
            placeholder_text="Password",
            placeholder_text_color="purple",
            width=200,
            border_width=2,
            border_color="purple",
        )
        self.password_entry.place(x=200, y=200)

        # Create Login Button
        self.login_mamba_button = ctk.CTkButton(
            master=self.login_frame,
            width=240,
            height=30,
            text="Login",
            command=self.login,
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
        )
        self.login_mamba_button.place(x=40, y=220)

        # Create Change Password Button
        self.change_password_button = ctk.CTkButton(
            master=self.login_frame,
            width=100,
            height=10,
            text="Change Password",
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
            command=self.change_password_widget,
        )
        self.change_password_button.place(x=155, y=280)

        # Create Account Button
        self.create_account_button = ctk.CTkButton(
            master=self.login_frame,
            width=100,
            height=10,
            text="Create Account",
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
            command=self.create_account_widget,
        )
        self.create_account_button.place(x=50, y=280)

        self.delete_account_button = ctk.CTkButton(
            master=self.login_frame,
            width=100,
            height=10,
            text="Delete Account",
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
            command=self.delete_account_widget,
        )

        self.delete_account_button.place(x=105, y=325)

        # Create Raheem Label
        self.raheem_label = ctk.CTkLabel(
            master=self.login_frame, text="Raheem Miah - Gamon", text_color="purple"
        )
        self.raheem_label.place(x=100, y=10)

    def login(self):
        """This function logs the user into the application on successful authentication or displays an error message if authentication fails."""

        # get username and password entries
        username = self.username_var.get()
        password = self.password_var.get()

        # call login method from account database class
        if self.db.mamba_account_login(username, password):
            CTkMessagebox(
                master=self.root,
                title="Login Successful",
                icon="check",
                message=f"Welcome back, {username}!",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )
            # open up main GUI and close login GUI
            main_gui = MainGUI(username)
            self.root.destroy()
            main_gui.root.mainloop()
            # missing username presents error message
        elif not username:
            missing_username()
            # missing password presents error message
        elif not password:
            missing_password()
            # invalid username / password presents error message
        else:
            CTkMessagebox(
                master=self.root,
                title="Login Failed",
                message="Incorrect username or password.",
                icon="cancel",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )

    def delete_account_widget(self):
        """This function creates a popup window to allow a user to delete their Mamba account"""
        # set up popup window attributes
        self.delete_account_window = ctk.CTk()
        self.delete_account_window.title("Delete Account")
        self.delete_account_window.resizable(False, False)

        # Username label
        self.username_label = ctk.CTkLabel(
            master=self.delete_account_window,
            text="Enter your Mamba username to delete account:",
            text_color="purple",
        )
        # Password label
        self.password_label = ctk.CTkLabel(
            master=self.delete_account_window,
            text="Enter your Mamba password to delete your account:",
            text_color="purple",
        )

        # Username Entry
        self.username_entry = ctk.CTkEntry(
            master=self.delete_account_window,
            text_color="#FF69B4",
        )
        # Password Entry
        self.password_entry = ctk.CTkEntry(
            master=self.delete_account_window,
            show="*",
            text_color="#FF69B4",
        )

        # Delete account submit button
        self.delete_account_window_submit_button = ctk.CTkButton(
            master=self.delete_account_window,
            text="Submit",
            command=self.delete_account_submit,
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
        )

        # GUI elements layout
        self.username_label.grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1, pady=5)

        self.password_label.grid(row=1, column=0)
        self.password_entry.grid(row=1, column=1, pady=5)

        # Place password submit button
        self.delete_account_window_submit_button.grid(row=2, column=1, pady=20)

        self.delete_account_window.mainloop()

    def delete_account_submit(self):
        """This function deletes the user's account from the database and closes the popup window"""

        # Username and password data
        username = self.username_entry.get()
        password = self.password_entry.get()

        # call delete account function from account database
        if self.db.delete_mamba_account(username, password):
            # messagebox for successful deletion
            CTkMessagebox(
                master=self.root,
                title="Account Deleted Successfully",
                message="Mamba is sad to see you go, come back soon!",
                icon="check",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )
            self.delete_account_window.destroy()
        elif not username:
            # missing username presents error message
            missing_username()
        elif not password:
            # missing password presents error message
            missing_password()
        else:
            # incorrect account or 2FA details
            CTkMessagebox(
                master=self.root,
                title="Account Deletion Failed",
                message="Mamba failed to delete your account, please try again.",
                icon="cancel",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )

    def create_account_widget(self):
        """This function creates a popup window to allow a user to create a new Mamba account"""

        # sets main properties of popup window
        self.create_window = ctk.CTk()
        self.create_window.geometry()
        self.create_window.title("Create Account")
        self.create_window.resizable(False, False)

        # Username Label
        self.username_label = ctk.CTkLabel(
            master=self.create_window, text="Username:", text_color="purple"
        )
        # Password Label
        self.password_label = ctk.CTkLabel(
            master=self.create_window, text="Password:", text_color="purple"
        )
        # Re-enter password Label
        self.re_enter_password_label = ctk.CTkLabel(
            master=self.create_window, text="Re-enter Password:", text_color="purple"
        )
        # Phone Number Label
        self.phone_label = ctk.CTkLabel(
            master=self.create_window, text="Phone:", text_color="purple"
        )

        # Username Entry
        self.username_entry = ctk.CTkEntry(
            master=self.create_window,
            text_color="#FF69B4",
        )
        # Password Entry
        self.password_entry = ctk.CTkEntry(
            master=self.create_window, show="*", text_color="#FF69B4"
        )
        # Re-enter password Entry
        self.re_enter_password_entry = ctk.CTkEntry(
            master=self.create_window, text_color="#FF69B4", show="*"
        )
        # Phone number Entry
        self.phone_entry = ctk.CTkEntry(master=self.create_window, text_color="#FF69B4")

        # Create account submit button
        self.create_account_submit_button = ctk.CTkButton(
            master=self.create_window,
            text="Submit",
            command=self.create_account_submit,
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
        )

        # GUI elements layout
        self.username_label.grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1, pady=5)

        self.password_label.grid(row=1, column=0)
        self.password_entry.grid(row=1, column=1, pady=5)

        self.re_enter_password_label.grid(row=2, column=0)
        self.re_enter_password_entry.grid(row=2, column=1, pady=5)

        self.phone_label.grid(row=3, column=0)
        self.phone_entry.grid(row=3, column=1, pady=5)

        # Submit Button layout
        self.create_account_submit_button.grid(row=4, column=1, pady=10)

        self.create_window.mainloop()

    def create_account_submit(self):
        """This function creates a new account in the database and closes the popup window"""

        # Retrieves user input data
        username = self.username_entry.get()
        password = self.password_entry.get()
        phone_number = self.phone_entry.get()
        re_enter_password = self.re_enter_password_entry.get()

        # checks for missing username
        if not username:
            missing_username()
        # checks for missing password
        elif not password:
            missing_password()
        # checks passwords match
        elif password != re_enter_password:
            CTkMessagebox(
                master=self.root,
                title="Passwords don't match",
                message="Please re-enter your new password and make sure they match.",
                icon="cancel",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )
        # checks for missing phone number
        elif not phone_number:
            missing_phone_number()
        elif "+44" not in phone_number[0:3]:
            # checks for incorrect phone number format
            CTkMessagebox(
                master=self.root,
                title="Account Creation Failed",
                message="Please start your phone number with: +44",
                icon="cancel",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )
        else:
            # message to show account created
            if self.db.create_mamba_account(username, password, phone_number) == True:
                CTkMessagebox(
                    master=self.root,
                    title="Account Creation Successful",
                    message=f"Welcome to Mamba, {username}!",
                    icon="check",
                    text_color="purple",
                    button_color="purple",
                    button_hover_color="#FF69B4",
                    title_color="purple",
                )
                self.create_window.destroy()
            # username entered already exists
            else:
                CTkMessagebox(
                    master=self.root,
                    title="Account Creation Failed",
                    message="The username or phone number already exists.",
                    icon="cancel",
                    text_color="purple",
                    button_color="purple",
                    button_hover_color="#FF69B4",
                    title_color="purple",
                )

    def change_password_widget(self):
        """This function creates a popup window to change a password"""

        # sets main properties of the popup window
        self.change_password_window = ctk.CTk()
        self.change_password_window.title("Change Password")
        self.change_password_window.resizable(False, False)

        # Labels
        self.username_label = ctk.CTkLabel(
            master=self.change_password_window, text="Username:", text_color="purple"
        )

        self.new_password_label = ctk.CTkLabel(
            master=self.change_password_window,
            text="New Password:",
            text_color="purple",
        )

        # Entries
        self.username_entry = ctk.CTkEntry(
            master=self.change_password_window, text_color="#FF69B4"
        )

        self.new_password_entry = ctk.CTkEntry(
            master=self.change_password_window, text_color="#FF69B4", show="*"
        )

        # Button
        self.change_password_submit_button = ctk.CTkButton(
            master=self.change_password_window,
            text="Submit",
            command=self.change_password_submit,
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
        )

        self.username_label.grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1, pady=5)

        self.new_password_label.grid(row=1, column=0)
        self.new_password_entry.grid(row=1, column=1, pady=5)

        self.change_password_submit_button.grid(row=3, column=1, pady=20)

        self.change_password_window.mainloop()

    def change_password_submit(self):
        """This function changes the password of a user in the database and closes the popup window"""

        # Retrieves user input data
        username = self.username_entry.get()
        new_password = self.new_password_entry.get()

        # checks for missing username
        if self.db.change_mamba_account_password(username, new_password) == True:
            # changes account password and provides success message
            CTkMessagebox(
                master=self.root,
                title="Password Change Successful",
                message=f"Don't forget your password this time, {username}!",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )
            self.change_password_window.destroy()
        else:
            # password change fails and provides error message
            CTkMessagebox(
                master=self.root,
                title="Password Change Failed",
                message="Please Try Again",
                icon="warning",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )


def missing_username():
    CTkMessagebox(
        title="Missing Username",
        message="Please fill in the username field.",
        icon="cancel",
        text_color="purple",
        button_color="purple",
        button_hover_color="#FF69B4",
        title_color="purple",
    )


def missing_password():
    CTkMessagebox(
        title="Missing Password",
        message="Please fill in the password field.",
        icon="cancel",
        text_color="purple",
        button_color="purple",
        button_hover_color="#FF69B4",
        title_color="purple",
    )


def missing_phone_number():
    CTkMessagebox(
        title="Missing Phone Number",
        message="Please fill in the phone number field.",
        icon="cancel",
        text_color="purple",
        button_color="purple",
        button_hover_color="#FF69B4",
        title_color="purple",
    )


db = MambaAccountDB()
app = LoginGUI(db)
app.root.mainloop()
