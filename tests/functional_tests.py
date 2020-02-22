from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

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
        input_box.send_keys('Use Peacock feather to make a fly')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = self.browser.find_elements_by_tag_name('tr')

        self.assertIn('1: Buy Peacock Feathers', [row.text for row in rows],
                f'list item did not appear in the table, item in table: {table.text}')

        self.assertIn('2: Use Peacock feather to make a fly', [row.text for row in rows],
                f'list item did not appear in the table, item in table: {table.text}')


        self.fail('Finish the test')

    def tearDown(self):
        self.browser.quit()

if __name__ == '__main__':
    unittest.main(warnings='ignore')
