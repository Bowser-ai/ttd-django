from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import unittest
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()


    def wait_for_row_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:

                table = self.browser.find_element_by_id('id_list_table')
                rows = self.browser.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width'] / 2,
                512,
                delta=10
                )
                        
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'),
                'Enter a to-do item')

        input_box.send_keys('Buy Peacock Feathers')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_list_table('1: Buy Peacock Feathers')

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use Peacock feathers to make a fly')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_list_table('2: Use Peacock feathers to make a fly')
        self.wait_for_row_list_table('1: Buy Peacock Feathers')

        self.fail('Finish the test')

    def test_multiple_users_can_start_list_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy Peacock Feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_list_table('1: Buy Peacock Feathers')
        user_url = self.browser.current_url
        self.assertRegex(user_url, '/lists/.+/')

        self.browser.close()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Peacock Feathers', body_text)
        self.assertNotIn('feathers to make a fly', body_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy Milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_list_table('1: Buy Milk')

        second_user_url = self.browser.current_url
        self.assertRegex(second_user_url, '/lists/+./')

        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Peacock Feathers', body_text)
        self.assertNotIn('feathers to make a fly', body_text)
        self.assertIn('Buy Milk', body_text)

