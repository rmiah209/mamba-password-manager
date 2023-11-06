# Mamba Password Manager - Password Vault Database

# Modules
import sqlite3
from cryptography.fernet import Fernet
from mamba_account_database import MambaAccountDB
import json


# Mamba Password Manager - Password Vault Class
class MambaPasswordVaultDB:
    def __init__(self):
        """This function initialises the 'MambaPasswordDB' class and it's attributes,  and to enable a connection with the database
        to allow manipulation of the user data. It connects to the 'mamba_password_vault.db' database file, and assigns the cursor object to the 'cur'
        attribute to enable execution of SQL statements."""

        self.conn = sqlite3.connect("mamba_password_vault.db")
        # establish connection to database
        self.cur = self.conn.cursor()
        # cursor is created to allow for querying the database

    def create_mamba_password_vault_table(self):
        """This function creates the 'mamba_password_vault' table if it doesn't exist, and will store the password information linked to each user
        which the account information is retrieved from the 'mamba_userdata' table."""

        # create password vault table with required fields
        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY,
        user_id TEXT,
        website TEXT,
        encrypted_password BLOB
        )
        """
            # create user id and master key table with required fields
        )
        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS keys (
        user_id TEXT PRIMARY KEY,
        key BLOB 
        )
        """
        )

    def get_user_id(self, username):
        """This function retrieves the unique user id which is linked to an account from the 'mamba_userdata' database.

        Args:
            username (str): The username associated to the user's Mamba account

        Returns:
            user_id: Returns the user_id if it is found in the database
        """
        # Query account db directly
        account_db.cur.execute(
            "SELECT mamba_account_unique_id FROM mamba_userdata WHERE mamba_account_username=?",
            (username,),
        )
        user_id = account_db.cur.fetchone()[0]
        return user_id

    def generate_master_key(self, username):
        """This function generates a unique master key which is associated with each user, used for encryption and decryption of their passwords.

        Args:
            username (str): The username associated to the user's Mamba account

        Returns:
            Boolean: Returns False if a master key for the user already exists, otherwise it generates the key and inserts it into the database.
        """
        # Lookup user id in account DB
        user_id = self.get_user_id(username)

        # Generate encryption key
        self.cur.execute("SELECT * FROM keys WHERE user_id=?", (user_id,))

        existing_key = self.cur.fetchone()

        if existing_key:
            return False

        # Only generate new key if one doesn't exist
        if not existing_key:
            key = Fernet.generate_key()
            self.cur.execute("INSERT INTO keys VALUES (?, ?)", (user_id, key))
            self.conn.commit()
            return True

    def add_password(self, username, website, password):
        """This function allows a user to add a new password to their password vault, which is associated to their Mamba account,
        by providing a website and password to store in the database.

        Args:
            username (str): The username associated to the user's Mamba account
            website (str): The website entered by the user to add to the password vault
            password (str): The password entered by the user to add to the password vault

        Returns:
            Boolean: Returns True if the password has been added into the database
        """

        if not website or not password or self.website_exists(username, website):
            return False

        user_id = self.get_user_id(username)
        key = self.get_key(user_id)
        # retrieves user's id and master key
        fernet = Fernet(key)
        # uses master key for encryption and decryption
        encrypted_pwd = fernet.encrypt(password.encode())
        # encrypts the entered password with the key

        # Save encrypted password
        self.cur.execute(
            "INSERT INTO passwords VALUES (?, ?, ?, ?)",
            (None, user_id, website, encrypted_pwd),
        )

        self.conn.commit()
        return True

    def view_passwords(self, username):
        """This function allows a user to retrieve and view all of the passwords from their password vault, which is associated to their Mamba account.

        Args:
            username (str): The username associated to the user's Mamba account

        Returns:
            passwords: Returns all of the passwords in the user's password vault as a list of dictionaries containing the website and decrypted password
        """
        user_id = self.get_user_id(username)
        # retrieves user id

        self.cur.execute("SELECT * FROM passwords WHERE user_id=?", (user_id,))
        # selects all fields from passwords table where user id matches

        rows = self.cur.fetchall()
        # fetches all rows from the query

        passwords = []

        for row in rows:
            id, user_id, website, encrypted_pwd = row
            key = self.get_key(user_id)
            fernet = Fernet(key)
            decrypted_pwd = fernet.decrypt(encrypted_pwd).decode()
            # decrypts the encrypted password with the key

            passwords.append({"website": website, "password": decrypted_pwd})
            # appends the decrypted password to the passwords list as a dictionary

            print(passwords)
        return passwords

    # Update password
    def update_password(self, username, website, new_password):
        """This function allows a user to update an existing password in their password vault.

        Args:
            username (str): The username associated to the user's Mamba account
            website (str): The website entered by the user to update in the password vault
            new_password (str): The new password entered by the user to update in the password vault

        Returns:
            Boolean: True if the password was updated successfully, False otherwise
        """

        if not self.website_exists(username, website) or not new_password:
            return False
        # check if website exists for user

        user_id = self.get_user_id(username)
        # retrieves user id

        key = self.get_key(user_id)
        fernet = Fernet(key)
        encrypted_new_pwd = fernet.encrypt(new_password.encode())
        # encrypts the new password with the key

        self.cur.execute(
            "UPDATE passwords SET encrypted_password=? WHERE user_id=? AND website=?",
            (encrypted_new_pwd, user_id, website),
        )
        self.conn.commit()
        # updates the old encrypted password with the new encrypted password and commits the database changes
        return True

    # Delete password
    def delete_password(self, username, website):
        """This function allows a user to delete an existing password from their password vault.

        Args:
            username (str): The username associated to the user's Mamba account
            website (str): The website associated to the password to delete

        Returns:
            Boolean: True if the password was deleted successfully from the database, False otherwise
        """

        # checks if website exists
        if not self.website_exists(username, website):
            return False
        # returns false if no website found
        user_id = self.get_user_id(username)

        self.cur.execute(
            "DELETE FROM passwords WHERE user_id=? AND website=?", (user_id, website)
        )
        # query to delete password assoicated to website
        self.conn.commit()
        # change saved in database
        return True

    def get_key(self, user_id):
        """This function retrieves the user's master key from the 'keys' table within the password vault database.

        Args:
            user_id (string): The user id of the current user's account.

        Returns:
            string: Returns key if it was found 
        """
        # queries database for user's master key
        self.cur.execute("SELECT key FROM keys WHERE user_id=?", (user_id,))
        key = self.cur.fetchone()[0]
        # stores query result within a list
        return key
        # returns key 

    def website_exists(self, username, website):
        """This function checks whether or not the website entered by the user exists within the password vault database.

        Args:
            username (string): The username of the user's account.
            website (string): The website entered by the user.

        Returns:
            boolean: Returns True if the website was found, otherwise it returns False.
        """
        
        # retrieves user id from username
        user_id = self.get_user_id(username)
        # queries database for website if it exists
        self.cur.execute(
            "SELECT * FROM passwords WHERE user_id=? AND website=?", (user_id, website)
        )
        # returns True if website exists, otherwise it returns False
        return self.cur.fetchone() is not None

    def export_passwords(self, username):
        """This function allows a user to export all of their passwords from the password vault to a JSON file.

        Args:
            username (str): The username associated to the user's Mamba account

        Returns:
            Boolean: True if the passwords have been exported as a JSON file
        """

        # retrieves all passwords with the 'view_passwords' function
        passwords = self.view_passwords(username)

        # Convert passwords to JSON
        json_passwords = json.dumps(passwords)

        if json_passwords != "[]":
            # Write to file
            with open(f"{username}_passwords.json", "w") as f:
                f.write(json_passwords)
                return True
        else:
            return False


account_db = MambaAccountDB()
password_db = MambaPasswordVaultDB()
