import unittest
from user_management import UserService, InMemoryUserRepository


# Sample test input values used in different test cases
TEST_USERNAME = "sarah1"
TEST_PASSWORD = "StrongPass456"
TEST_ROLE = "student"
DUPLICATE_PASSWORD = "AnotherPass789"
WRONG_PASSWORD = "WrongPass123"
UNKNOWN_USERNAME = "unknown_sarah"


# Test class for the User Management module
class TestUserManagement(unittest.TestCase):

    def setUp(self):
        # Create a fresh repository and service before each test
        self.repository = InMemoryUserRepository()
        self.service = UserService(self.repository)

    def test_01_register_user_successfully(self):
        # Test that a user can be registered with valid details
        print("\n[Test 1] Register user successfully")
        user = self.service.register_user(TEST_USERNAME, TEST_PASSWORD, TEST_ROLE)
        print(f"Input: username={TEST_USERNAME}, password={TEST_PASSWORD}, role={TEST_ROLE}")
        print(f"Stored user: username={user.username}, role={user.role}")

        # Check that the stored username and role are correct
        self.assertEqual(user.username, TEST_USERNAME)
        self.assertEqual(user.role, TEST_ROLE)
        print("Result: Registration successful")

    def test_02_register_duplicate_username_raises_error(self):
        # Test that duplicate usernames are not allowed
        print("\n[Test 2] Duplicate username check")
        self.service.register_user(TEST_USERNAME, TEST_PASSWORD, TEST_ROLE)
        print(f"First registration successful for username={TEST_USERNAME}")

        # Check that registering the same username again raises an error
        with self.assertRaises(ValueError):
            self.service.register_user(TEST_USERNAME, DUPLICATE_PASSWORD, TEST_ROLE)

        print(f"Second registration rejected for duplicate username={TEST_USERNAME}")
        print("Result: ValueError raised as expected")

    def test_03_register_empty_username_raises_error(self):
        # Test that registration fails when the username is empty
        print("\n[Test 3] Empty username check")
        print(f"Input: username='', password={TEST_PASSWORD}, role={TEST_ROLE}")

        with self.assertRaises(ValueError):
            self.service.register_user("", TEST_PASSWORD, TEST_ROLE)

        print("Result: Empty username rejected")

    def test_04_register_empty_password_raises_error(self):
        # Test that registration fails when the password is empty
        print("\n[Test 4] Empty password check")
        print(f"Input: username={TEST_USERNAME}, password='', role={TEST_ROLE}")

        with self.assertRaises(ValueError):
            self.service.register_user(TEST_USERNAME, "", TEST_ROLE)

        print("Result: Empty password rejected")

    def test_05_login_success_with_correct_credentials(self):
        # Test that login succeeds with the correct username and password
        print("\n[Test 5] Login with correct credentials")
        self.service.register_user(TEST_USERNAME, TEST_PASSWORD, TEST_ROLE)
        result = self.service.login(TEST_USERNAME, TEST_PASSWORD)

        print(f"Login input: username={TEST_USERNAME}, password={TEST_PASSWORD}")
        print(f"Login result: {result}")

        self.assertTrue(result)
        print("Result: Login successful")

    def test_06_login_fails_with_wrong_password(self):
        # Test that login fails when the password is incorrect
        print("\n[Test 6] Login with wrong password")
        self.service.register_user(TEST_USERNAME, TEST_PASSWORD, TEST_ROLE)
        result = self.service.login(TEST_USERNAME, WRONG_PASSWORD)

        print(f"Login input: username={TEST_USERNAME}, password={WRONG_PASSWORD}")
        print(f"Login result: {result}")

        self.assertFalse(result)
        print("Result: Login failed as expected")

    def test_07_login_fails_with_unknown_user(self):
        # Test that login fails when the username does not exist
        print("\n[Test 7] Login with unknown user")
        result = self.service.login(UNKNOWN_USERNAME, TEST_PASSWORD)

        print(f"Login input: username={UNKNOWN_USERNAME}, password={TEST_PASSWORD}")
        print(f"Login result: {result}")

        self.assertFalse(result)
        print("Result: Unknown user rejected")

    def test_08_password_is_not_stored_in_plain_text(self):
        # Test that the password is stored as a hash, not plain text
        print("\n[Test 8] Password is not stored in plain text")
        user = self.service.register_user(TEST_USERNAME, TEST_PASSWORD, TEST_ROLE)

        print(f"Original password: {TEST_PASSWORD}")
        print(f"Stored password hash: {user.password_hash}")

        self.assertNotEqual(user.password_hash, TEST_PASSWORD)
        print("Result: Password stored as hash, not plain text")
    
    def test_09_repository_add_stores_user(self):
        # Test that the repository stores a registered user correctly
        print("\n[Test 9] Repository add stores user")
        user = self.service.register_user(TEST_USERNAME, TEST_PASSWORD, TEST_ROLE)
        stored_user = self.repository.get_by_username(TEST_USERNAME)

        print(f"Stored username: {stored_user.username}")

        self.assertEqual(stored_user.username, TEST_USERNAME)
        print("Result: Repository stored the user correctly")

    def test_10_repository_get_by_username_returns_none_for_missing_user(self):
        # Test that the repository returns None when the user does not exist
        print("\n[Test 10] Repository returns None for missing user")
        missing_user = self.repository.get_by_username("missing_user")

        print(f"Lookup result: {missing_user}")

        self.assertIsNone(missing_user)
        print("Result: Missing user was not found, as expected")


if __name__ == "__main__":
    # Run the unit tests
    unittest.main(verbosity=0, buffer=False)