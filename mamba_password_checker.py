# Mamba Password Manager - Password Data Breach Checker

# Modules
import hashlib
import requests


# Mamba Password Checker Class
class MambaPasswordChecker:
    def __init__(self):
        """This function initialises the MambaPasswordChecker class and sets up the 'pwnedpasswords' API URL"""
        self.url = "https://api.pwnedpasswords.com/range/"

    def get_password_leak_count(self, password):
        """This function checks if a password has been involved in any data breaches by querying the pwnedpasswords API.

        Args:
            password (str): The password to check for data breaches

        Raises:
            RuntimeError: Returns a run time error if an error occurs while fetching data from the API

        Returns:
            breach_count, 0: Returns an integer representing the number of times the password has been involved in a data breach if found, or 0 if not found
        """
        # Hash the password using SHA1 and split into prefix and suffix
        mamba_sha1_password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
        mamba_password_sha1_prefix, mamba_password_sha1_suffix = (
            mamba_sha1_password[:5],
            mamba_sha1_password[5:],
        )
        # Make request to pwnedpasswords API with prefix
        url = self.url + mamba_password_sha1_prefix
        response = requests.get(url)

        # Check response status code
        if response.status_code != 200:
            raise RuntimeError(
                f"Error fetching: {response.status_code}, check the API and try again"
            )
        # Parse response lines into hash and count
        mamba_password_check_hashes = (
            line.split(":") for line in response.text.splitlines()
        )
        # Loop through hashes to find match
        for h, breach_count in mamba_password_check_hashes:
            if h == mamba_password_sha1_suffix:
                # If match found return breach count
                return int(breach_count)
            # Otherwise return 0
        return 0

    def is_valid_password(self, password):
        """Checks if the given password is valid by checking for breaches.

        This function calls get_password_leak_count() to get the number of breaches
        the password has been involved in. It returns a tuple with a boolean
        indicating if the password is valid, and a message about the password's validity.

        Args:
            password (str): The password to validate

        Returns:
            tuple: A tuple containing:
                bool: True if the password is valid, False otherwise
                str: A message indicating the password's validity
        """

        breach_count = self.get_password_leak_count(password)

        if breach_count:
            return (
                False,
                f"Uh-oh, Mamba has found some issues with this password. This password has been leaked in {breach_count} data breaches.",
            )
        return (
            True,
            "Mamba's happy! This password hasn't been recorded in any data breaches.",
        )

    def check_password(self, password):
        """This function checks a password and prints a message about its validity by calling is_valid_password().

        Args:
            password (str): The password to check

        Returns:
            bool: True if the password is valid, False otherwise
        """

        # Checks if the given password is valid by calling is_valid_password()
        is_valid, message = self.is_valid_password(password)
        # and prints a message about the password's validity.
        print(message)
        # Returns a boolean indicating if the password is valid.
        return is_valid
