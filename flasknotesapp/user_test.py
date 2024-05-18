''' File for testing the user class'''
# As a user I want to be able to input in my information to create an account
# so that I can access the application as a new user
# Source: Chatgpt helped give me examples that I then addapted to fit in more examples
import unittest
from objects.user import User


class TestUserClass(unittest.TestCase):
    '''Class for testing user registration '''

    def test_user_initialization(self):
        ''' User registration test cases'''
        #  Test initialization of User objects
        #  Could not configure a new database but here is one that works,
        #  therefore can test to not make duplicate
        user = User("1", "JohnSmith", "Random12!", "js7456@uncw.edu")
        confirm_password = "Random12!"
        self.assertEqual(user.check_new_user(confirm_password),
                         ("Username is already taken",
                          'Email already registered for account',
                          '', '', False))

        #  Password does not match and original password does not meet criteria
        #  because ther are no capital letters
        user1 = User("10", "LeoDoak", "fdskjfns!df", "cxmvbx@uncw.edu")
        confirm_password = "NotCorrect"
        self.assertEqual(user1.check_new_user(confirm_password),
                         ('', '', 'Password does not meet criteria',
                          'Passwords do not match', False))

        # Password does not match and password does not meet criteria
        user2 = User("1", "ColeThibault", "sdfjjsd$e", "jsdfdsf@uncw.edu")
        confirm_password = "Random12!"
        self.assertEqual(user2.check_new_user(confirm_password),
                         ('', '', 'Password does not meet criteria',
                          'Passwords do not match', False))

        # Admin is already in the system, so error there. Password doesnt contain a number
        user3 = User("1", "admin", "Verygoodpassword!", "xcvxc@uncw.edu")
        confirm_password = "Verygoodpassword!"
        self.assertEqual(user3.check_new_user(confirm_password),
                         ('Username is already taken', '',
                          'Password does not meet criteria', '', False))

        # Password Error
        user4 = User("1", "newuser1", "Verygoodpassword!", "xcvxc@uncw.edu")
        confirm_password = "Verygoodpassword!"
        self.assertEqual(user4.check_new_user(confirm_password), ('', '',
                                                                  'Password does not meet criteria',
                                                                  '', False))

        # Email Error
        user5 = User("1", "newuser1", "Verygoodpassword1!", "notanemail")
        confirm_password = "Verygoodpassword1!"
        self.assertEqual(user5.check_new_user(confirm_password),
                         ('', 'Invalid email entered', '', '', False))

        #  Confirm Password error
        user6 = User("1", "newuser1", "Verygoodpassword1!", "leo@doak.info")
        confirm_password = "Verygoodpassword2!"
        self.assertEqual(user6.check_new_user(confirm_password),
                         ('', '', '', 'Passwords do not match', False))

        #  Username taken error
        user7 = User("1", "admin", "Verygoodpassword1!", "leo@doak.info")
        confirm_password = "Verygoodpassword1!"
        self.assertEqual(user7.check_new_user(confirm_password),
                         ("Username is already taken", '', '', '', False))

        #  Username invalid error
        user8 = User("1", "12", "Verygoodpassword1!", "leo@doak.info")
        confirm_password = "Verygoodpassword1!"
        self.assertEqual(user8.check_new_user(confirm_password),
                         ('Username does not meet criteria', '', '', '', False))

        #  Null values test
        #  (** Shouldn't happen since the html requires
        #  fields to be entered before submitting **)
        user8 = User("", "", "", "")
        confirm_password = ""
        self.assertEqual(user8.check_new_user(confirm_password),
                         ('Username does not meet criteria', 'Invalid email entered',
                          'Password does not meet criteria', '', False))


if __name__ == '__main__':
    unittest.main()
