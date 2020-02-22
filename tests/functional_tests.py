from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = self.browser.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list(self):
        self.browser.get('http:localhost:8000')

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'),
                'Enter a to-do item')

        input_box.send_keys('Buy Peacock Feathers')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use Peacock feathers to make a fly')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_list_table('1: Buy Peacock Feathers')
        self.check_for_row_list_table('2: Use Peacock feathers to make a fly')

        self.fail('Finish the test')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
