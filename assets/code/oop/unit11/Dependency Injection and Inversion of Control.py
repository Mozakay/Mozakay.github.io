from abc import ABC, abstractmethod
import unittest
import io
from contextlib import redirect_stdout
from dependency_injector import containers, providers


# Interface for notifications
class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, user, message):
        pass


# Email service
class EmailService(NotificationService):
    def send_notification(self, user, message):
        print(f"Sending email to {user}: {message}")


# Extra service
class SMSService(NotificationService):
    def send_notification(self, user, message):
        print(f"Sending SMS to {user}: {message}")


# UserManager receives dependency from outside
class UserManager:
    def __init__(self, notifier: NotificationService):
        self.notifier = notifier

    def register_user(self, user):
        self.notifier.send_notification(user, "Welcome!")


# Mock service for unit testing
class MockNotificationService(NotificationService):
    def __init__(self):
        self.messages = []

    def send_notification(self, user, message):
        self.messages.append((user, message))


# DI container
class Container(containers.DeclarativeContainer):
    notifier = providers.Factory(EmailService)
    user_manager = providers.Factory(UserManager, notifier=notifier)


# Base test class to print test result
class PrintTestResult(unittest.TestCase):
    def tearDown(self):
        result = self._outcome.result
        test_case = self

        failed = any(test_case == test for test, _ in result.failures)
        errored = any(test_case == test for test, _ in result.errors)

        if failed or errored:
            print(f"{self._testMethodName}: FAILED")
        else:
            print(f"{self._testMethodName}: PASSED")


# Unit tests for UserManager in isolation
class TestUserManager(PrintTestResult):
    def test_register_user_sends_welcome_message(self):
        mock_service = MockNotificationService()
        user_manager = UserManager(mock_service)

        user_manager.register_user("alice@example.com")

        self.assertEqual(
            mock_service.messages,
            [("alice@example.com", "Welcome!")]
        )


# Integration test for actual EmailService
class TestEmailServiceIntegration(PrintTestResult):
    def test_email_service_outputs_message(self):
        email_service = EmailService()

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            email_service.send_notification("alice@example.com", "Welcome!")

        self.assertEqual(
            captured_output.getvalue().strip(),
            "Sending email to alice@example.com: Welcome!"
        )


# Test SMSService
class TestSMSService(PrintTestResult):
    def test_sms_service_outputs_message(self):
        sms_service = SMSService()

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            sms_service.send_notification("bob@example.com", "Welcome!")

        self.assertEqual(
            captured_output.getvalue().strip(),
            "Sending SMS to bob@example.com: Welcome!"
        )


# Test DI container wiring
class TestContainer(PrintTestResult):
    def test_container_creates_user_manager(self):
        container = Container()
        user_manager = container.user_manager()

        self.assertIsInstance(user_manager, UserManager)
        self.assertIsInstance(user_manager.notifier, EmailService)


if __name__ == "__main__":
    unittest.main(verbosity=0)