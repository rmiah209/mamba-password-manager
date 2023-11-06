# Mamba Password Manager - Password Generator

# Modules
import secrets
import pyperclip
import string


# Mamba Password Generator Class
class MambaPasswordGenerator:
    def __init__(self):
        self.length = (12,)
        self.symbols = (True,)
        self.digits = (True,)
        self.upper_case = (True,)
        self.lower_case = (True,)
        """This function initalises the 'MambaPasswordGenerator' class and attributes which are: the password length, special_chars, digits, 
        upper_case and lower_case all included within the generated password's properties."""

    def mamba_generate_password(self, length, uppercase, lowercase, digits, symbols):
        """This function generates a random password based on the given length, uppercase, lowercase, digit, and symbols value given

        Args:
            length (int): Length of the password to be generated
            uppercase (boolean): True if uppercase letters should be included, otherwise it is False
            lowercase (boolean): True if lowercase letters should be included, otherwise it is False
            digits (boolean): True if digits should be included, otherwise it is False
            symbols (boolean): True if symbols should be included, otherwise it is False

        Returns:
            self.mamba_password: Returns the generated password string
        """

        # password characteristic attributes
        self.length = length
        self.symbols = symbols
        self.digits = digits
        self.upper_case = uppercase
        self.lower_case = lowercase
        self.mamba_password = None

        # empty variable to add attributes
        chars = ""

        # adds attributes to chars variable depending on the user's selection
        if self.lower_case:
            chars += string.ascii_lowercase
        if self.upper_case:
            chars += string.ascii_uppercase
        if self.digits:
            chars += string.digits
        if self.symbols:
            chars += string.punctuation

        while True:
            try:
                # checks length is valid
                if self.length < 8 or self.length > 32:
                    # returns false if invalid length
                    return False
                else:
                    break
            except ValueError:
                return False

        self.mamba_password = "".join(secrets.choice(chars) for _ in range(self.length))
        # generates a random password based on the user's selection

        pyperclip.copy(self.mamba_password)
        # copies the generated password to the user's clipboard

        return self.mamba_password
        # returns generated password
