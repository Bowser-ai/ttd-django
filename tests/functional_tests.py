from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def test_can_start_a_list(self):
        self.browser.get('http:localhost:8000')

        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test')

    def tearDown(self):
        self.browser.quit()

if __name__ == '__main__':
    unittest.main(warnings='ignore')
