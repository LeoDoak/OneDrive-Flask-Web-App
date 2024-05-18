"Image library, need to 'pip install Pillow'"
import sqlite3
import re
from PIL import Image
import numpy as np


# https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/


class User():
    """Represents a user in the system."""
    user_id: str
    username: str
    password: str
    email: str
    profile_picture: Image
    priv_groups: list
    public_groups: list
    access_token = ""

    def __init__(self, user_id: str, username: str, password: str, email: str):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email

    def __str__(self):
        """String method for class

        Parameters:
        None.

        Returns:
        str: string representation of class.
        """
        string = (
                "User ID: " + str(self.user_id) + " Username: " +
                str(self.username) + " Password: " + str(self.password) +
                " email: " + str(self.email))
        return string

    def get_id(self):
        """Part of necessary flask-login module. Gets the user_id.

        Parameters:
        None.

        Returns:
        str: user_id, unique number to each user.
        """
        return str(self.user_id)

    def is_active(self):
        """Part of necessary flask-login module, checks if user is active.

        Parameters:
        None.

        Returns:
        bool: True since the users are active if logged in.
        """
        return True

    def is_anonymous(self):
        """Checks if the user is anonymous, part of necesary
        flask-login module.

        Parameters:
        None.

        Returns:
        bool: False, we don't have anonymous users.
        """
        return False

    def set_access_token(self, ac):
        """Sets the access token , part of necessary flask-login
        module.

        Parameters:
        None.

        Returns:
        None.
        """
        self.access_token = ac

    def get_access_token(self):
        """Part of necesary flask-login module.

        Parameters:
        None.

        Returns:
        str: The access token associated with the user.
        """
        return self.access_token

    def is_authenticated(self):
        """Authenticates user part of necessary flask-login.

        Parameters:
        None.

        Returns:
        bool: True if user is authenticated. False otherwise.
        """
        connection = sqlite3.connect("user.db")
        cursor = connection.cursor()
        cursor.execute(
            """SELECT user_id, username, password,
            email FROM user where (username = ? and password = ?)""",
            (self.username, self.password))
        row = cursor.fetchall()
        connection.close()
        return len(row) == 1

    def get_user_from_id(self, user_id):
        """gets the user object from the user_id

        Parameters:
        user_id (int): The unique identifier of the user.

        Returns:
        None. Sets the instance variables.
        """
        connection = sqlite3.connect("user.db")
        cursor = connection.cursor()
        cursor.execute(
            """SELECT user_id, username, password,
            email FROM user where (user_id = ?)""",
            (user_id,))
        row = cursor.fetchall()
        connection.close()
        self.user_id = row[0][0]
        self.username = row[0][1]
        self.password = row[0][2]
        self.email = row[0][3]
        # return user

    def set_login_user_id(self):
        """Sets the login user_id from the database.

        Parameters:
        None.

        Returns:
        None.
        """
        connection = sqlite3.connect("user.db")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT user_id FROM user where (username = ? and password = ?)",
            (self.username, self.password))
        row = cursor.fetchall()
        if len(row) == 1:
            self.user_id = row[0][0]
        else:
            self.user_id = None

    def set_login_email(self):
        """Sets the login email from the database.

        Parameters:
        None.

        Returns:
        None.
        """
        connection = sqlite3.connect("user.db")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT email FROM user where (username = ? and password = ?)",
            (self.username, self.password))
        row = cursor.fetchall()
        if len(row) == 1:
            self.email = row[0][0]
        else:
            self.email = None

    def _check_valid_username(self):
        """checks if username fits criteria.

        Parameters:
        None.

        Returns:
        str: empty string if valid, error message if not.
        """
        pattern = r'^(?=.*[a-zA-Z].*[a-zA-Z].*[a-zA-Z].*[a-zA-Z]).{5,}$'
        if re.match(pattern, self.username):
            return ''
        return 'Username does not meet criteria'

    def _check_duplicate_username(self):
        """Checks for duplicate username within database.

        Parameters:
        None.

        Returns:
        str: empty string or error message.
        """
        connection = sqlite3.connect("user.db")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT username FROM user where username = ?", (self.username,))
        row = cursor.fetchall()
        connection.close()
        if len(row) == 1:
            return 'Username is already taken'
        return ''

    def _check_username(self):
        """Checks if username is not already taken and valid.

        Parameters:
        None.

        Returns:
        str: empty string or error message.
        """
        message = self._check_valid_username()
        if message == '':
            message = self._check_duplicate_username()
            return message
        return message

    def _check_valid_email(self):
        """Checks to make sure for valid email.

        Parameters:
        None.

        Returns:
        str: empty if email passes, error mesage if not.
        """
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.fullmatch(regex, self.email):
            return ''
        return "Invalid email entered"

    def _check_duplicate_email(self):
        """Checks the database that email isn't already in the system.

        Parameters:
        None.

        Returns:
        str: empty if not, error message if so.
        """
        connection = sqlite3.connect("user.db")
        cursor = connection.cursor()
        cursor.execute("SELECT email FROM user where email = ?", (self.email,))
        row = cursor.fetchall()
        connection.close()
        if len(row) == 1:
            return "Email already registered for account"
        return ''

    def _check_email(self):
        """method that checks the email criteria.

        Parameters:
        None.

        Returns:
        str: error message or empty string.
        """
        message = self._check_valid_email()
        if message == '':
            message = self._check_duplicate_email()
            return message
        return message

    def _validate_password(self):
        """Checks that the password matches the criteria.

        Parameters:
        None.

        Returns:
        str: empty string if password passes, message if it doesn't.
        """
        pattern = r'^(?=.*[0-9])(?=.*[^a-zA-Z0-9]).{9,}$'
        if re.match(pattern, self.password):
            return ""
        return "Password does not meet criteria"

    def _check_confirm_password(self, confirm_password):
        """Checks to make sure that the paswords match each other.

        Parameters:
        confirm_password (str): the password confirmation to be checked.

        Returns:
        str: empty if passwords match, message that passwords do not match.
        """
        if self.password == confirm_password:
            return ''
        return 'Passwords do not match'

    def check_new_user(self, confirm_password):
        """Public method that handles all the private check methods.

        Parameters:
        confirm_password (int) : the confirm password the user enters.

        Returns:
        String username_message : username error message.
        String email_message : email error message.
        String password_message : password not match criteria message.
        String confirm_password_message : confirm password message.
        String register_status : User registriation credentials pass all checks.
        """
        username_message = self._check_username()
        email_message = self._check_email()
        password_message = self._validate_password()
        confirm_password_message = self._check_confirm_password(confirm_password)
        register_status = False
        if (username_message == '' and
                email_message == '' and
                password_message == '' and
                confirm_password_message == ''):
            register_status = True
            self._set_user_id()
            self._update_database()
        return (
            username_message,
            email_message,
            password_message,
            confirm_password_message,
            register_status
        )

    def _set_user_id(self):
        """Sets the user ID from numpy random int.

        Parameters:
        None.

        Returns:
        None.
        """
        id_num = np.random.randint(0, 99, 2)
        get_user_id = str(id_num[0]) + str(id_num[1])
        self.user_id = get_user_id

    def _update_database(self):
        """Updates the database with the new user information.

        Parameters:

        Returns:
        None.
        """
        connection = sqlite3.connect("user.db")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO user VALUES (?,? ,? ,?)",
            (self.user_id, self.username, self.password, self.email,))
        connection.commit()
        connection.close()


SAMPLE_USERS = [
    # Sample List
    User("1", "JohnSmith1", "Random12", "js7456@uncw.edu"),
    User("2", "AliceBarnes", "Password10", "ab1234@uncw.edu"),
    User("3", "BobbyHill123", "Qwerty123", "bh4201@uncw.edu"),
    User("4", "JettHoward", "Random12", "jh4321@uncw.edu"),
    User("0", "Admin", "1234", "admin@uncw.edu")  # admin access
]
