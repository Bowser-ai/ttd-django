from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        input_box = self.get_item_input_box()
        input_box.send_keys(Keys.ENTER)

        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

        input_box = self.get_item_input_box()
        input_box.send_keys('Buy milk')
        input_box.send_keys(Keys.ENTER)

        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))

        self.wait_for_row_list_table('1: Buy milk')

        input_box = self.get_item_input_box()
        input_box.send_keys(Keys.ENTER)

        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

        input_box = self.get_item_input_box()
        input_box.send_keys('Buy tea')
        input_box.send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))

        self.wait_for_row_list_table('1: Buy milk')
        self.wait_for_row_list_table('2: Buy tea')
