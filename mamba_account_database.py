# Mamba Password Manager - Account Database

# Modules
import bcrypt
import sqlite3
import uuid
import time
from twilio.rest import Client
import random
import datetime


# Mamba Password Manager - Account Database Class
class MambaAccountDB:
    def __init__(self):
        """This function initialises the 'MambaAccountDB' class and it's attributes,  and to enable a connection with the database
        to allow manipulation of the user data. It connects to the 'mamba_userdata.db' database file, and assigns the cursor object to the 'cur'
        attribute to enable execution of SQL statements."""

        # establishes a connection to the database
        self.conn = sqlite3.connect("mamba_userdata.db")
        # cursor is created to allow for querying the database
        self.cur = self.conn.cursor()

    def create_mamba_account_table(self):
        """This function creates the 'mamba_userdata' table if it doesn't already exist. This table will store account details for each user."""

        # account database is created with required fields
        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS mamba_userdata (
        id INTEGER PRIMARY KEY,
        mamba_account_username VARCHAR(255) NOT NULL,
        mamba_account_password VARCHAR(255) NOT NULL,
        mamba_account_unique_id VARCHAR(36) NOT NULL,
        mamba_account_phone_number VARCHAR(10) NOT NULL,
        mamba_account_login_attempts INTEGER NOT NULL DEFAULT 0,
        mamba_account_last_login_attempt INTEGER NOT NULL DEFAULT 0
        )
        """
        )

    def create_mamba_account(self, username, password, phone_number):
        """This function allows a user to create an account within Mamba, where the details are then securely saved within the 'mamba_userdata'
        database.

        Args:
            username (str): The username associated to the user's Mamba account
            password (str): The password associated to the user's Mamba account
            phone_number (str): The phone number associated to the user's Mamba account

        Returns:
            Boolean: Returns True if the account creation is successful, otherwise it returns False if the password
            requirements aren't met or an account with the entered username already exists.
        """

        mamba_account_username = username
        mamba_account_password = password
        mamba_account_phone_number = phone_number

        if len(mamba_account_password) < 8:
            return False
        # verifies if user's entered password has a length of 8 or greater
        elif not any(char.isupper() for char in mamba_account_password):
            return False
        # verifies if user's entered password has an uppercase letter
        elif not any(char.islower() for char in mamba_account_password):
            return False
        # verifies if user's entered password has a lowercase letter
        elif not any(char.isdigit() for char in mamba_account_password):
            return False
        # verifies if user's entered password has a digit
        else:
            self.cur.execute(
                "SELECT * FROM mamba_userdata WHERE mamba_account_username=? OR mamba_account_phone_number=?",
                (
                    mamba_account_username,
                    mamba_account_phone_number,
                ),
            )
        # selects all fields within 'mamba_userdata' to store the data

        row = self.cur.fetchone()
        # retrives the next row of the query result from 'mamba_userdata'

        if row is None:
            # checks if rows within the 'mamba_userdata' table are empty
            mamba_account_hashed_password = bcrypt.hashpw(
                mamba_account_password.encode(), bcrypt.gensalt(rounds=12)
            ).decode()
            # hashes the password inputted by user with a salt of 12 rounds
            mamba_account_unique_id = str(uuid.uuid4())
            # generates a unique id for each account that is entered into 'mamba_userdata'
            self.cur.execute(
                "INSERT INTO mamba_userdata (mamba_account_username, mamba_account_password, mamba_account_login_attempts, mamba_account_last_login_attempt, mamba_account_unique_id, mamba_account_phone_number) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    mamba_account_username,
                    mamba_account_hashed_password,
                    0,
                    0,
                    mamba_account_unique_id,
                    mamba_account_phone_number,
                ),
            )
            # inserts all inputted/generated values into each corresponding field within 'mamba_userdata'
            self.conn.commit()
            return True
            # commits the changes made in the database and closes the connection
        else:
            return False

    def mamba_account_login(self, username, password):
        """This function allows a user to login to their Mamba account providing they have entered their correct account details, which
        are retrieved from the 'mamba_userdata' database, then logging them in if successful.

        Args:
            username (str): The username associated to the user's Mamba account
            password (str): The password associated to the user's Mamba account

        Returns:
            Boolean: Returns True if the user is successfully logged in, else it returns False if the username doesn't exist in the database,
            the password is incorrect, or the login attempts exceed 3 within 5 minutes.
        """

        mamba_account_username = username
        mamba_account_password = password

        self.cur.execute(
            "SELECT mamba_account_password, mamba_account_login_attempts, mamba_account_last_login_attempt FROM mamba_userdata WHERE mamba_account_username = ?",
            (mamba_account_username,),
        )
        # selects the user's account password, login attempt and last login attempt from 'mamba_userdata'

        row = self.cur.fetchone()
        # retrives the next row of the query result from 'mamba_userdata'

        if row is not None:
            mamba_account_hashed_password = row[0]
            mamba_account_login_attempts = row[1]
            mamba_account_last_login_attempt = row[2]
            # checks if rows contain user data of corresponding variables

            if (
                mamba_account_login_attempts >= 3
                and mamba_account_last_login_attempt + 300 > time.time()
            ):
                return False
            # blocks login attempts for 5 minutes if login attempts exceed 3 within 5 minutes
            elif bcrypt.checkpw(
                mamba_account_password.encode(), mamba_account_hashed_password.encode()
            ):
                self.cur.execute(
                    "UPDATE mamba_userdata SET mamba_account_login_attempts = 0 WHERE mamba_account_username = ?",
                    (mamba_account_username,),
                )
                self.conn.commit()
                return True
            # if successful, the login attempt and last login attempt values are reset, and the user is logged in, commiting changes in the database
            else:
                datetime = datetime.datetime.fromtimestamp(time.time()).strftime("%c")
                self.cur.execute(
                    "UPDATE mamba_userdata SET mamba_account_login_attempts = mamba_account_login_attempts + 1, mamba_account_last_login_attempt = ? WHERE mamba_account_username = ?",
                    (
                        datetime,
                        mamba_account_username,
                    ),
                )
                self.conn.commit()
                return False
            # updates the last login attempt and number of login attempts if user fails to enter correct details
        else:
            return False
            # if details entered by user don't exist in the database, returns False

    def mamba_account_logout(self, username):
        """This is a simple logout function which resets the user's last login attempt and number of login attempts to 0.

        Args:
            username (str): The username which is associated to the user's Mamba account.

        Returns:
            Boolean: When True, the function ends and the changes in the database are saved.
        """
        mamba_account_username = username

        self.cur.execute(
            "UPDATE mamba_userdata SET mamba_account_login_attempts = 0, mamba_account_last_login_attempt = 0 WHERE mamba_account_username = ? ",
            (mamba_account_username,),
        )
        # resets the last login attempt and number of login attempts to 0, logging user out

        self.conn.commit()

        return True

    def delete_mamba_account(self, username, password):
        """This function allows a user to delete their Mamba account permanently, providing they enter the correct account details and the
        correct 2FA code, which then completely removes the account details from the 'mamba_userdata' database.

        Args:
            username (str): The username which is associated to the user's Mamba account.
            password (str): The password which is associated to the user's Mamba account.

        Returns:
            Boolean: Returns True if the account was successfully deleted, otherwise it returns False if the user enters a non-existent
            username, incorrect password or incorrect 2FA code.
        """

        mamba_account_username = username
        mamba_account_password = password

        # creates cursor to query database
        self.conn.cursor()

        # checks if username exists in database
        self.cur.execute(
            "SELECT mamba_account_password FROM mamba_userdata WHERE mamba_account_username = ?",
            (mamba_account_username,),
        )

        # stores query result as a list
        result = self.cur.fetchone()

        if result is None:
            return False
        # returns False if username entered doesn't exist within the database

        hashed_password = result[0]
        if not bcrypt.checkpw(
            mamba_account_password.encode(), hashed_password.encode()
        ):
            return False
        # returns False if the password entered doesn't match the password within the database

        self.cur.execute(
            "SELECT mamba_account_phone_number FROM mamba_userdata WHERE mamba_account_username = ?",
            (username,),
        )
        mamba_account_phone_number = self.cur.fetchone()[0]
        # retrieves the phone number associated to the user's account username

        two_fa_code = random.randint(100000, 999999)
        # generates a random code for the 2FA

        account_sid = "YOUR_SID"
        auth_token = "YOUR_TOKEN"
        client = Client(account_sid, auth_token)
        # twilio account details required to connect to the module, client class from twilio.rest is instantiated
        client.messages.create(
            to=mamba_account_phone_number,
            from_="+YOUR_TWILIO_NUMBER",
            body=f"""Hey there, {mamba_account_username}, here's your 2FA code to delete your Mamba account: {two_fa_code}. 
            If you aren't the owner of this account, please ignore this message.""",
        )
        # sends the 2FA code to the user's phone number

        user_two_fa_code = input("Enter code: ")

        if user_two_fa_code == str(two_fa_code):
            self.cur.execute(
                "DELETE FROM mamba_userdata WHERE mamba_account_username = ?",
                (mamba_account_username,),
            )
            self.conn.commit()
            return True
        # deletes the account within the database if the 2FA code entered matches the one sent
        else:
            return False
        # returns False if the 2FA code entered doesn't match

    def change_mamba_account_password(self, username, new_password):
        """This function allows a user to change their account password, given they have entered their correct username, and
        the correct 2FA code, which then the old password is updated with the new password within the database.

        Args:
            username (str): The username which is associated to the user's Mamba account.
            new_password (str): The new password which is entered to update the user's old password.

        Returns:
            Boolean: Returns True if the password is changed, otherwise it returns False if the username entered doesn't exist
            within the database, or the 2FA code entered is incorrect.
        """
        mamba_account_username = username
        mamba_account_new_password = new_password

        self.conn.cursor()
        self.cur.execute(
            "SELECT mamba_account_password FROM mamba_userdata WHERE mamba_account_username = ?",
            (mamba_account_username,),
        )
        result = self.cur.fetchone()

        if result is None:
            return False
        # returns False if the username entered doesn't exist within the database

        self.cur.execute(
            "SELECT mamba_account_phone_number FROM mamba_userdata WHERE mamba_account_username = ?",
            (username,),
        )
        mamba_account_phone_number = self.cur.fetchone()[0]
        # retrieves the phone number associated to the user's account username

        two_fa_code = random.randint(100000, 999999)
        # generates a random code for the 2FA

        account_sid = "YOUR_SID"
        auth_token = "YOUR_TOKEN"
        client = Client(account_sid, auth_token)

        client.messages.create(
            to=mamba_account_phone_number,
            from_="+YOUR_TWILIO_NUMBER",
            body=f"""Hey {mamba_account_username}, your 2FA code to change your Mamba password is: {two_fa_code}. If
            you didn't aren't the owner of this account, please ignore this message.""",
        )
        # sends a 2FA code to the user's phone number

        user_two_fa_code = input("Enter code: ")

        if user_two_fa_code == str(two_fa_code):
            salt = bcrypt.gensalt(rounds=12)
            mamba_account_new_password_hash = bcrypt.hashpw(
                mamba_account_new_password.encode(), salt
            ).decode()
            # if the entered 2FA code matches, and hashes the new password

            self.cur.execute(
                "UPDATE mamba_userdata SET mamba_account_password = ? WHERE mamba_account_username = ?",
                (mamba_account_new_password_hash, mamba_account_username),
            )

            self.conn.commit()

            print("success")

            return True
            # returns True if the new password is entered into the database
        else:
            return False
            # returns False if the 2FA code entered doesn't match the one sent


# instantiate the 'MambaAccountDB' class object
account_db = MambaAccountDB()

