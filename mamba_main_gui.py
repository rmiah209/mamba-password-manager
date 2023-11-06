# Main GUI - Mamba Password Manager

# Modules
import tkinter as tk
from mamba_password_vault_database import MambaPasswordVaultDB
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from mamba_password_generator import MambaPasswordGenerator
from mamba_password_checker import MambaPasswordChecker
from mamba_account_database import MambaAccountDB
import importlib
from CTkListbox import CTkListbox


# Main GUI Class
class MainGUI:
    def __init__(self, username):
        """This function initialises the 'MambaMainGUI' class and sets its graphical attributes such as the widgets.

        Args:
            username (string): The username of the current logged in user
        """
        # Password Vault Database object
        self.password_vault_db = MambaPasswordVaultDB()
        # Password Generator object
        self.password_generator = MambaPasswordGenerator()
        # Password Checker object
        self.password_checker = MambaPasswordChecker()
        # Account Database object
        self.account_db = MambaAccountDB()
        self.username = username

        # Initialise the root window
        self.root = ctk.CTk()
        # Create title of the main GUI
        self.root.title(f"Welcome, {username}")
        self.root.title(f"Mamba Password Manager - Logged in as: {username}")
        # Set window size and non-resizable
        self.root.resizable(False, False)
        self.root.geometry("1280x720")

        # Create the main frame
        self.main_frame = ctk.CTkFrame(
            master=self.root,
            width=700,
            height=700,
            corner_radius=30,
            border_width=5,
            border_color="purple",
        )
        # Place the main frame in the center of the root window
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create the title frame
        self.mamba_main_gui_title_frame = ctk.CTkFrame(
            master=self.root,
            width=200,
            height=50,
            corner_radius=3,
            border_width=3,
            border_color="purple",
        )

        # Place the title frame in the root window
        self.mamba_main_gui_title_frame.place(x=20, y=55)

        # Create the title label
        self.mamba_title_label = ctk.CTkLabel(
            master=self.mamba_main_gui_title_frame,
            text=f"Mamba Password Manager - {username}'s Vault",
            text_color="purple",
        )

        # Place the title label in the title frame
        self.mamba_title_label.pack(pady=10, padx=10)

        # Create the appearance mode frame
        self.mamba_appearance_mode_frame = ctk.CTkFrame(
            master=self.root,
            width=200,
            height=50,
            corner_radius=3,
            border_width=3,
            border_color="purple",
        )

        # Place the appearance mode frame in the root window
        self.mamba_appearance_mode_frame.place(x=70, y=560)

        # Create the appearance mode label
        self.mamba_appearance_mode_label = ctk.CTkLabel(
            self.mamba_appearance_mode_frame,
            text="Appearance Mode:",
            text_color="purple",
        )

        # Place the appearance mode label in the appearance mode frame
        self.mamba_appearance_mode_label.pack(pady=5, padx=16)

        # Create the appearance mode option menu
        self.mamba_appearance_mode_option_menu = ctk.CTkOptionMenu(
            self.root,
            values=["Light", "Dark", "System"],
            button_color=("purple", "purple"),
            text_color="black",
            fg_color="purple",
            button_hover_color="#FF69B4",
            dropdown_text_color="purple",
            command=self.change_appearance_mode_submit,
        )
        # Create and place the appearance mode option menu in the root window
        self.mamba_appearance_mode_option_menu.place(x=70, y=600)
        # Set the default value of the appearance mode option menu to 'dark'
        self.mamba_appearance_mode_option_menu.set("Dark")

        # Create the add password button
        self.add_password_button = ctk.CTkButton(
            master=self.root,
            width=240,
            height=40,
            text="Add a Password",
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
            command=self.add_password_widget,
        )
        # Place add password button
        self.add_password_button.place(x=530, y=100)

        # Create update password button
        self.update_password_button = ctk.CTkButton(
            master=self.root,
            width=240,
            height=40,
            text="Update a Password",
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
            command=self.update_password_widget,
        )
        # Place update password button
        self.update_password_button.place(x=530, y=200)

        # Create delete password button
        self.delete_password_button = ctk.CTkButton(
            master=self.root,
            width=240,
            height=40,
            text="Delete a Password",
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
            command=self.delete_password_widget,
        )
        # Place delete password button
        self.delete_password_button.place(x=530, y=300)

        # Create view passwords button
        self.view_passwords_button = ctk.CTkButton(
            master=self.root,
            width=240,
            height=40,
            text="View Passwords",
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
            command=self.view_passwords_widget,
        )
        # Place view passwords button
        self.view_passwords_button.place(x=530, y=400)

        # Create generate passwords button
        self.generate_password_button = ctk.CTkButton(
            master=self.root,
            width=240,
            height=40,
            text="Generate a Password",
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
            command=self.generate_password_widget,
        )
        # Place generate passwords button
        self.generate_password_button.place(x=530, y=500)

        # Create check password button
        self.check_password_button = ctk.CTkButton(
            master=self.root,
            width=240,
            height=40,
            text="Check Password Security",
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
            command=self.check_password_widget,
        )
        # Place check password button
        self.check_password_button.place(x=530, y=600)

        # Create export password button
        self.export_password_button = ctk.CTkButton(
            master=self.root,
            width=230,
            height=200,
            text="Export Passwords",
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
            command=self.export_password_vault_submit,
        )
        # Place export password button
        self.export_password_button.place(x=1020, y=250)

        # Create generate master key button
        self.generate_master_key_button = ctk.CTkButton(
            master=self.root,
            width=230,
            height=100,
            text="Generate Master Key",
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
            command=self.generate_master_key_button_submit,
        )
        # Place generate master key button
        self.generate_master_key_button.place(x=1020, y=50)

        # Create quit button
        self.quit_button = ctk.CTkButton(
            master=self.root,
            width=240,
            height=30,
            text="Quit",
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
            command=self.close_mamba,
        )
        # Place quit button
        self.quit_button.place(x=1015, y=600)

        # Create logout button
        self.logout_button = ctk.CTkButton(
            master=self.root,
            width=240,
            height=30,
            text="Logout",
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
            command=self.logout_submit,
        )
        # Place logout button
        self.logout_button.place(x=1015, y=500)

    def change_appearance_mode_submit(self, new_appearance_mode):
        """This function changes the appearance mode of the application depending on the user's choice.

        Args:
            new_appearance_mode (string): The new appearance mode of the application
        """
        # Changes the appearance mode of the application
        ctk.set_appearance_mode(str(new_appearance_mode))

    def generate_master_key_button_submit(self):
        """This function generates a master key for the user's account and saves it to the keys table in the password vault database."""

        username = self.username
        # prompts an error message if the user has already generated a master key
        if self.password_vault_db.generate_master_key(username) == False:
            CTkMessagebox(
                master=self.root,
                title="Master Key already exists",
                message=f"A master key already exists for account: {username}",
                icon="cancel",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )
            # disables the generate master key button
            self.generate_master_key_button.configure(
                state="disabled",
            )
        else:
            # generates a master key for the user's account and saves it to the keys table in the password vault database
            self.password_vault_db.generate_master_key(username)
            # prompts the user that their master key has been generated
            CTkMessagebox(
                master=self.root,
                title="Master Key Generated!",
                message=f"Your master key has been generated, {username}",
                icon="check",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )

    def add_password_widget(self):
        """This function creates the widget for adding a password to the user's password vault."""
        # sets the main properties of the add password window
        self.add_password_window = ctk.CTk()
        self.add_password_window.title("Add a Password")
        self.add_password_window.resizable(False, False)

        # creates the website label
        self.website_label = ctk.CTkLabel(
            master=self.add_password_window,
            text="Enter website name: ",
            text_color="purple",
        )
        # creates the website entry
        self.website_entry = ctk.CTkEntry(
            master=self.add_password_window,
            text_color="#FF69B4",
            border_width=1,
            border_color="purple",
        )

        # creates the password label
        self.add_pw_label = ctk.CTkLabel(
            master=self.add_password_window,
            text="Enter password to add: ",
            text_color="purple",
        )

        # creates the password entry
        self.add_pw_entry = ctk.CTkEntry(
            master=self.add_password_window,
            text_color="#FF69B4",
            show="*",
            border_width=1,
            border_color="purple",
        )

        # creates the submit button
        self.add_password_submit_button = ctk.CTkButton(
            master=self.add_password_window,
            text="Add Password",
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
            command=self.add_password_submit,
        )

        # places the widgets on the window
        self.website_label.grid(row=0, column=0)
        self.website_entry.grid(row=0, column=1, pady=5)

        self.add_pw_label.grid(row=1, column=0)
        self.add_pw_entry.grid(row=1, column=1, pady=5)

        self.add_password_submit_button.grid(row=2, column=1, pady=10)

        self.add_password_window.mainloop()

    def add_password_submit(self):
        """This function adds a password to the database and displays a message to the user on success/failure."""

        # retrieves the values from the add password entry and website entry
        added_pw = self.add_pw_entry.get()
        website = self.website_entry.get()
        username = self.username

        # checks if the website is already in the database
        if self.password_vault_db.add_password(username, website, added_pw):
            # adds the password to the database and displays a message to the user on success
            CTkMessagebox(
                master=self.root,
                title="Password Added Successfully",
                message="Your new password has been added to the vault!",
                icon="check",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )
            # add password window is closed
            self.add_password_window.destroy()
        else:
            # fails to add the password and displays a message to the user on failure
            CTkMessagebox(
                master=self.root,
                title="Failed to add Password",
                message=f"This website: [{website}] already exists or please fill in all required fields.",
                icon="cancel",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )

    def update_password_widget(self):
        """This function creates the widget for updating a password in the user's password vault."""

        # sets the main properties of the update password window
        self.update_password_window = ctk.CTk()
        self.update_password_window.title("Update a Password")
        self.update_password_window.resizable(False, False)

        # creates the website name label
        self.update_pw_website_name_label = ctk.CTkLabel(
            master=self.update_password_window,
            text="Enter the Service name of the password you'd like to update: ",
            text_color="purple",
        )

        # creates the website name entry
        self.update_pw_website_name_entry = ctk.CTkEntry(
            master=self.update_password_window,
            text_color="#FF69B4",
            border_width=1,
            border_color="purple",
        )

        # creates the password label
        self.update_password_label = ctk.CTkLabel(
            master=self.update_password_window,
            text="Enter your new password: ",
            text_color="purple",
        )

        # creates the password entry
        self.update_password_entry = ctk.CTkEntry(
            master=self.update_password_window,
            text_color="#FF69B4",
            show="*",
            border_width=1,
            border_color="purple",
        )

        # creates the update password submit button
        self.update_password_submit_button = ctk.CTkButton(
            master=self.update_password_window,
            text="Update Password",
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
            command=self.update_password_submit,
        )

        # places the widgets on the window
        self.update_pw_website_name_label.grid(row=0, column=0)
        self.update_pw_website_name_entry.grid(row=0, column=1, pady=5)

        self.update_password_label.grid(row=1, column=0)
        self.update_password_entry.grid(row=1, column=1, pady=5)

        self.update_password_submit_button.grid(row=3, column=1, pady=10)

        self.update_password_window.mainloop()

    def update_password_submit(self):
        """This function updates a password in the database and displays a message to the user on success/failure."""

        # retrieves the values from the update password entry and website entry
        username = self.username
        website = self.update_pw_website_name_entry.get()
        new_password = self.update_password_entry.get()

        # checks if the website is already in the database
        if self.password_vault_db.update_password(username, website, new_password):
            # updates the password in the database and displays a message to the user on success
            CTkMessagebox(
                master=self.root,
                title="Password Updated Successfully!",
                message=f"Your old password has been updated with: {new_password}",
                icon="check",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )
            self.update_password_window.destroy()
        else:
            # fails to update the password and displays a message to the user on failure
            CTkMessagebox(
                master=self.root,
                title="Failed to update Password",
                message="The website you've entered doesn't exist, or please enter the password field.",
                icon="cancel",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )

        self.update_password_window.mainloop()

    def delete_password_widget(self):
        """This function creates the widget for deleting a password in the user's password vault."""

        # sets the main properties of the delete password window
        self.delete_password_window = ctk.CTk()
        self.delete_password_window.title("Delete a Password")
        self.delete_password_window.resizable(False, False)

        # creates the website name label
        self.delete_pw_website_label = ctk.CTkLabel(
            master=self.delete_password_window,
            text="Enter website name to delete password: ",
            text_color="purple",
        )

        # creates the website name entry
        self.delete_pw_website_entry = ctk.CTkEntry(
            master=self.delete_password_window,
            text_color="#FF69B4",
            border_width=1,
            border_color="purple",
        )

        # creates the delete password submit button
        self.delete_password_submit_button = ctk.CTkButton(
            master=self.delete_password_window,
            text="Delete Password",
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
            command=self.delete_password_submit,
        )

        # places the widgets on the window
        self.delete_pw_website_label.grid(row=0, column=0)
        self.delete_pw_website_entry.grid(row=0, column=1)

        self.delete_password_submit_button.grid(row=3, column=1, pady=10)

        self.delete_password_window.mainloop()

    def delete_password_submit(self):
        """This function deletes a password in the database and displays a message to the user on success/failure."""

        # retrieves the values from the delete password entry and website entry
        username = self.username
        website = self.delete_pw_website_entry.get()

        # checks if the website is already in the database
        if self.password_vault_db.delete_password(username, website):
            # deletes the password in the database and displays a message to the user on success
            CTkMessagebox(
                master=self.root,
                title="Password Deleted Successfully!",
                message=f"Your password for: {website} has been deleted!",
                icon="check",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )
            self.delete_password_window.destroy()
        else:
            # fails to delete the password and displays a message to the user on failure
            CTkMessagebox(
                master=self.root,
                title="Failed to delete Password",
                message="The website you have entered doesn't exist!",
                icon="cancel",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )

    def view_passwords_widget(self):
        """This function creates the widget for viewing a list of passwords in the user's password vault."""

        # sets the main properties of the view passwords window
        self.view_passwords_window = ctk.CTk()
        self.view_passwords_window.title("Password List")

        # creates the password list
        self.password_list = CTkListbox(
            master=self.view_passwords_window,
            height=100,
            width=300,
            select_color="purple",
            hover_color="#FF69B4",
        )

        # creates the close password list button
        self.close_password_list_button = ctk.CTkButton(
            master=self.password_list,
            text="Close Password List",
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
            command=self.view_passwords_close_submit,
        )

        # places the widgets on the window
        self.password_list.pack(expand=True, fill="both")
        self.close_password_list_button.pack(pady=5)

        # inserts the passwords into the password list widget
        self.view_passwords_insert()

        self.view_passwords_window.mainloop()

    def view_passwords_insert(self):
        """This function inserts the passwords in the user's password vault into the password list widget."""
        username = self.username
        # calls the view passwords function in the database and retrieves the passwords
        passwords = self.password_vault_db.view_passwords(username)

        # inserts the passwords into the password list widget
        for password in passwords:
            self.password_list.insert(
                "end", f"{password['website']} - {password['password']}"
            )

    def view_passwords_close_submit(self):
        """This function closes the view passwords window."""
        # closes the view passwords window
        self.view_passwords_window.destroy()

    def generate_password_widget(self):
        """This function creates the widget for generating a password in the user's password vault."""

        # sets the main properties of the generate password window
        self.generate_password_window = ctk.CTk()
        self.generate_password_window.title("Password Generator")
        self.generate_password_window.resizable(False, False)

        # creates the length label
        self.length_label = ctk.CTkLabel(
            master=self.generate_password_window, text="Length:", text_color="purple"
        )

        # places the label on the window
        self.length_label.grid(row=0, column=0, pady=10, padx=10)

        # creates the length slider
        self.length_slider = ctk.CTkSlider(
            master=self.generate_password_window,
            from_=8,
            to=32,
            button_color="purple",
            button_hover_color="#FF69B4",
        )

        # places the slider on the window
        self.length_slider.grid(row=0, column=1, pady=10, padx=10)

        # Checkboxes frame
        self.checks_frame = ctk.CTkFrame(
            master=self.generate_password_window, border_width=2, border_color="purple"
        )
        self.checks_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

        # Lowercase checkbox
        self.lowercase_var = ctk.BooleanVar(value=True)
        self.lowercase_cb = ctk.CTkCheckBox(
            master=self.checks_frame,
            text="Lowercase",
            text_color="purple",
            fg_color="purple",
            hover_color="#FF69B4",
            variable=self.lowercase_var,
        )

        # Uppercase checkbox
        self.uppercase_var = ctk.BooleanVar(value=True)
        self.uppercase_cb = ctk.CTkCheckBox(
            master=self.checks_frame,
            text="Uppercase",
            text_color="purple",
            fg_color="purple",
            hover_color="#FF69B4",
            variable=self.uppercase_var,
        )

        # Digits checkbox
        self.digits_var = ctk.BooleanVar(value=True)
        self.digits_cb = ctk.CTkCheckBox(
            master=self.checks_frame,
            text="Digits",
            text_color="purple",
            fg_color="purple",
            hover_color="#FF69B4",
            variable=self.digits_var,
        )

        # Symbols checkbox
        self.symbols_var = ctk.BooleanVar(value=True)
        self.symbols_cb = ctk.CTkCheckBox(
            master=self.checks_frame,
            text="Symbols",
            text_color="purple",
            fg_color="purple",
            hover_color="#FF69B4",
            variable=self.symbols_var,
        )

        # Layout checkboxes in frame
        self.lowercase_cb.pack(pady=5, padx=5)
        self.uppercase_cb.pack(pady=5, padx=5)
        self.digits_cb.pack(pady=5, padx=5)
        self.symbols_cb.pack(pady=5, padx=5)

        # Submit button
        self.submit_button = ctk.CTkButton(
            master=self.generate_password_window,
            text="Generate Password",
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
            command=self.generate_password_submit,
        )

        # places the button on the window
        self.submit_button.grid(row=2, column=0, columnspan=2, pady=20)

        self.generate_password_window.mainloop()

    def validate_checkboxes(self):
        """This function validates the checkboxes in the password generator window.

        Returns:
            integer: The number of checked boxes.
        """
        # sets the number of checked boxes to 0
        checked_boxes = 0
        # increments the number of checked boxes by 1 for each checked box
        if self.lowercase_var.get():
            checked_boxes += 1
        if self.uppercase_var.get():
            checked_boxes += 1
        if self.digits_var.get():
            checked_boxes += 1
        if self.symbols_var.get():
            checked_boxes += 1

        # returns the number of checked boxes
        return checked_boxes >= 2

    def generate_password_submit(self):
        """This function generates a password based on the checkboxes selected and inserts it into the user's password vault."""

        # retrieves user input from the password generator window
        int_length = int(self.length_slider.get())
        lowercase = self.lowercase_var.get()
        uppercase = self.uppercase_var.get()
        digits = self.digits_var.get()
        symbols = self.symbols_var.get()

        if self.validate_checkboxes():
            # checks if the user has selected at least two checkboxes to generate a password
            generated_password = self.password_generator.mamba_generate_password(
                int_length, uppercase, lowercase, digits, symbols
            )
            # prompts the user with a messagebox showing the generated password and copies it to the clipboard
            CTkMessagebox(
                master=self.root,
                title="Password Generated",
                message=f"Your generated password and copied to clipboard is: {generated_password}",
                icon="check",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )
            self.generate_password_window.destroy()
        else:
            # prompts the user with a messagebox showing that they must select at least two checkboxes to generate a password
            CTkMessagebox(
                master=self.root,
                title="Password Generation Failed",
                message="Please tick atleast two checkboxes!",
                icon="info",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )

    def check_password_widget(self):
        """This function creates the window for the user to enter their password to check the password vault."""

        # sets the properties of the check password window
        self.check_password_window = ctk.CTk()
        self.check_password_window.title("Password Vault Creation")
        self.check_password_window.resizable(False, False)

        # creates check password label
        self.check_password_label = ctk.CTkLabel(
            master=self.check_password_window,
            text="Enter password to check: ",
            text_color="purple",
        )

        # creates check password entry
        self.check_password_entry = ctk.CTkEntry(
            master=self.check_password_window,
            text_color="#FF69B4",
            show="*",
            border_width=1,
            border_color="purple",
        )

        # creates submit button
        self.check_password_submit_button = ctk.CTkButton(
            master=self.check_password_window,
            text="Check Data Breach Count",
            fg_color="purple",
            text_color="black",
            hover_color="#FF69B4",
            command=self.check_password_submit,
        )

        # places the label, entry and button on the window
        self.check_password_label.grid(row=0, column=0)
        self.check_password_entry.grid(row=1, column=0)
        self.check_password_submit_button.grid(row=3, column=0, pady=20)

        self.check_password_window.mainloop()

    def check_password_submit(self):
        """This function checks the password entered by the user to see if it has been compromised in any data breaches."""

        # retrieves the password entered by the user
        password = self.check_password_entry.get()

        # checks if the password entered is valid using the password checker class
        is_valid = self.password_checker.check_password(password)

        # gets the password leak number  using the password checker class
        message = self.password_checker.get_password_leak_count(password)

        if not password:
            # checks if the password entered is empty
            CTkMessagebox(
                master=self.root,
                title="Password Check Fail",
                message="Please enter a password to check!",
                icon="cancel",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )
        elif is_valid:
            # prompts the user with a messagebox showing that the password entered is valid and that it hasn't been compromised in any data breaches
            CTkMessagebox(
                master=self.root,
                title="Password Check Complete",
                message="Mamba's happy! This password hasn't been compromised in any data breaches!",
                icon="check",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )
            self.check_password_window.destroy()
        else:
            # prompts the user with a messagebox showing that the password entered is invalid and that it has been compromised in some data breaches
            CTkMessagebox(
                master=self.root,
                title="Password Check Complete",
                message=f"Mamba has found this password has been leaked in: [{message}] data breaches.",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )

    def export_password_vault_submit(self):
        """This function exports the user's password vault to a JSON file."""
        username = self.username

        # exports the password vault to a JSON file using the password vault database class
        if self.password_vault_db.export_passwords(username):
            CTkMessagebox(
                master=self.root,
                title="Password Vault Exported",
                message=f"Your passwords have been exported to: {username}_passwords.json",
                icon="check",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )
        else:
            # fails to export the password vault and prompts the user with a messagebox showing that there are no passwords to export
            CTkMessagebox(
                title="No Passwords",
                master=self.root,
                message="There are no passwords to export!",
                icon="info",
                text_color="purple",
                button_color="purple",
                button_hover_color="#FF69B4",
                title_color="purple",
            )

    def logout_submit(self):
        """This function logs the user out of Mamba and closes the main GUI, returning them to the login GUI.

        Returns:
            boolean: Returns False if the user isn't logged out successfully.
        """

        # stores the username and account database object in variables
        username = self.username
        db = self.account_db

        # logs the user out of Mamba and closes the main GUI
        if self.account_db.mamba_account_logout(username):
            self.root.destroy()
            lg_module = importlib.import_module("mamba_login_gui")
            lg_module.LoginGUI(db).root.mainloop()
        else:
            # keeps the user logged in and prompts the user with a messagebox showing that they are already logged out
            return False

    def close_mamba(self):
        """This function closes Mamba and destoys the main GUI."""

        # prompts the user with a messagebox asking if they want to close Mamba
        msg = CTkMessagebox(
            master=self.root,
            title="Exit?",
            message="Do you want to close Mamba?",
            icon="question",
            option_1="Cancel",
            option_2="No",
            option_3="Yes",
            text_color="purple",
            button_color="purple",
            button_hover_color="#FF69B4",
            title_color="purple",
            button_text_color="black",
        )

        # retrieves the response from the messagebox
        response = msg.get()

        # closes Mamba and destroys the main GUI
        if response == "Yes":
            self.root.destroy()
        else:
            # returns False if the user doesn't want to close Mamba
            return False
