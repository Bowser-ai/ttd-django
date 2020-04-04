from unittest.mock import patch

from django.test import TestCase

from accounts import views


class SendLoginEmailViewTest(TestCase):

    @patch('accounts.views.send_mail')
    def test_send_email_to_address_from_post(self, patched_send_mail):
        self.send_email_called = False

        self.client.post('/accounts/send_login_email/', data={
            'email': 'edith@example.com'
            })

        self.assertTrue(patched_send_mail.called)
        (subject, body, from_email, to_list), kwargs = patched_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(body, 'body')
        self.assertEqual(from_email, 'noreply@superlists.com')
        self.assertEqual(to_list, ['edith@example.com'])
    
    def test_redirects_to_home_page(self):
        response = self.client.post('/accounts/send_login_email/', data={
            'email': 'edith@example.com'
            })
        self.assertRedirects(response, '/')

    def test_adds_success_message(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com',
            }, follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(
                message.message,
                'Check your email, we\'ve sent you a link you can use to log in.'
                )
        self.assertEqual(message.tags, 'success')
