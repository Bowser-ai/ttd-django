from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):
                        
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
