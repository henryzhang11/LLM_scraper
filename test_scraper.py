import unittest
from unittest.mock import patch
import re
from subprocess import CompletedProcess

from scraper import Scraper

def dummy_language_model(prompt: str) -> str:
    if (
        "Please write a Python script" in prompt or
        "Please work on a Python script" in prompt
    ):
        return "```python\nprint('Hello World')\n```"
    if "Please judge whether" in prompt:
        return "The script meets the requirements. Yes"
    return ""

class TestScraper(unittest.TestCase):
    def setUp(self):
        # Initialize the Scraper with the dummy language model
        self.scraper = Scraper(dummy_language_model)
        # Set default values used in methods.
        self.scraper.job_description = "Print 'Hello World'"
        self.scraper.script = "print('Hello World')"
        self.scraper.stdout = "Hello World\n"
        self.scraper.history = []
    
    def test_generate_script(self):
        prompt = "dummy prompt"
        code = self.scraper.generate_script(prompt)
        self.assertIsInstance(code, str)

    def test_run_script(self):
        input = "print(\"Hello World!\")"
        result = self.scraper.test_run(input)
        self.assertEqual(result.standout, "Hello World!")
        input = "number = 3\nprint(number[0])"
        result = self.scraper.test_run(input)
        self.assertNotEqualt(result.standerr, "")

if __name__ == '__main__':
    unittest.main()