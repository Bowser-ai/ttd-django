from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from list.views import home_page

class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'list/home.html')

    def test_can_save_a_post_request(self):
        response = self.client.post('/', data={"item_text": "new_item"})
        self.assertIn('new_item', response.content.decode('utf8'))
        self.assertTemplateUsed(response, 'list/home.html')
                
