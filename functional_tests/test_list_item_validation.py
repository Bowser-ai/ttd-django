from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')        
        input_box.send_keys(Keys.ENTER)


        self.wait_for(lambda: self.assertEqual(
                self.browser.find_element_by_css_selector('.has-error').text,
                'You can\'t have an empty list item'
                ))

        input_box = self.browser.find_element_by_id('id_new_item')        
        input_box.send_keys('Buy milk')
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_list_table('1: Buy milk')

        input_box = self.browser.find_element_by_id('id_new_item')        
        input_box.send_keys(Keys.ENTER)


        self.wait_for(lambda: self.assertEqual(
                self.browser.find_element_by_css_selector('.has-error').text,
                'You can\'t have an empty list item'
                ))

        input_box = self.browser.find_element_by_id('id_new_item')        
        input_box.send_keys('Buy tea')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_list_table('1: Buy milk')
        self.wait_for_row_list_table('2: Buy tea')


                
                