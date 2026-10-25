import unittest
from unittest.mock import patch, MagicMock
from app import (
    app,
    send_registration_success_email,
    send_login_success_email,
    send_login_failed_email,
    send_payment_success_email,
    send_payment_failed_email,
)

class MajesticAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    @patch('app.send_email_via_resend')
    def test_registration_email_trigger(self, mock_send):
        mock_send.return_value = (True, "Email sent successfully")
        success, msg = send_registration_success_email('test@example.com', 'Test User')
        self.assertTrue(success)
        mock_send.assert_called_once()
        self.assertEqual(mock_send.call_args[0][0], 'test@example.com')
        self.assertIn("Welcome", mock_send.call_args[0][1])

    @patch('app.send_email_via_resend')
    def test_login_success_email_trigger(self, mock_send):
        mock_send.return_value = (True, "Email sent successfully")
        success, msg = send_login_success_email('test@example.com', 'Test User')
        self.assertTrue(success)
        mock_send.assert_called_once()
        self.assertEqual(mock_send.call_args[0][0], 'test@example.com')
        self.assertIn("Login Successful", mock_send.call_args[0][1])

    @patch('app.send_email_via_resend')
    def test_login_failed_invalid_password_email_trigger(self, mock_send):
        mock_send.return_value = (True, "Email sent successfully")
        success, msg = send_login_failed_email('test@example.com', 'Test User', 'Invalid Password')
        self.assertTrue(success)
        mock_send.assert_called_once()
        self.assertEqual(mock_send.call_args[0][0], 'test@example.com')
        self.assertIn("Invalid Password", mock_send.call_args[0][1])

    @patch('app.send_email_via_resend')
    def test_payment_success_email_trigger(self, mock_send):
        mock_send.return_value = (True, "Email sent successfully")
        success, msg = send_payment_success_email(
            'test@example.com', 'Test User', '1500.00', 'order_123', 'pay_456'
        )
        self.assertTrue(success)
        mock_send.assert_called_once()
        self.assertEqual(mock_send.call_args[0][0], 'test@example.com')
        self.assertIn("Payment Successful", mock_send.call_args[0][1])

    @patch('app.send_email_via_resend')
    def test_payment_failed_email_trigger(self, mock_send):
        mock_send.return_value = (True, "Email sent successfully")
        success, msg = send_payment_failed_email(
            'test@example.com', 'Test User', '1500.00', 'order_123', 'Payment cancelled by user'
        )
        self.assertTrue(success)
        mock_send.assert_called_once()
        self.assertEqual(mock_send.call_args[0][0], 'test@example.com')
        self.assertIn("Payment Incomplete", mock_send.call_args[0][1])

    @patch('app.send_login_failed_email')
    def test_login_route_invalid_password_sends_email(self, mock_send_failed):
        # When attempting login with registered user email but wrong password
        response = self.client.post('/login', data={
            'email': 'piyushpatel131206@gmail.com',
            'password': 'completely_wrong_password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        mock_send_failed.assert_called_once()
        self.assertEqual(mock_send_failed.call_args[0][0], 'piyushpatel131206@gmail.com')
        self.assertEqual(mock_send_failed.call_args[1].get('reason'), 'Invalid Password')

    @patch('app.send_payment_failed_email')
    def test_payment_failure_route_sends_email(self, mock_send_failed):
        response = self.client.get('/payment/failure?order_id=order_test1&amount=500&reason=User+cancelled&email=piyushpatel131206@gmail.com&name=Piyush')
        self.assertEqual(response.status_code, 200)
        mock_send_failed.assert_called_once()

    @patch('app.send_email_via_smtp')
    @patch('app.get_smtp_config')
    def test_smtp_priority_delivers_to_entered_email(self, mock_get_cfg, mock_send_smtp):
        mock_get_cfg.return_value = {"is_configured": True}
        mock_send_smtp.return_value = (True, "Email sent successfully")
        from app import send_email_notification
        success, msg = send_email_notification('particular_entered_user@gmail.com', 'Test Subject', 'Body text')
        self.assertTrue(success)
        mock_send_smtp.assert_called_once()
        self.assertEqual(mock_send_smtp.call_args[0][0], 'particular_entered_user@gmail.com')

    @patch('app.save_users')
    @patch('app.send_registration_success_email')
    def test_register_route_sends_to_entered_email(self, mock_reg_email, mock_save):
        import uuid
        unique_email = f"user_{uuid.uuid4().hex[:8]}@example.com"
        response = self.client.post('/register', data={
            'name': 'New Customer',
            'email': unique_email,
            'phone': '9876543210',
            'password': 'testpassword123',
            'confirm_password': 'testpassword123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        mock_reg_email.assert_called_once_with(unique_email, 'New Customer')

if __name__ == '__main__':
    unittest.main()
