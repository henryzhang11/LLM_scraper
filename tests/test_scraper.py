import unittest
from scraper.scraper import Scraper

def dummy_language_model(prompt: str) -> str:
    if (
        "Please write a Python script" in prompt or
        "Please work on a Python script" in prompt
    ):
        return "```\nprint('Hello World')\n```"
    if "Please judge whether" in prompt:
        return "The script meets the requirements. Yes"
    return ""

class TestScraper(unittest.TestCase):

    def test_generate_instance(self):
        scraper = Scraper(dummy_language_model, "Print 'Hello World'")
        script = scraper.generate_instance()
        self.assertEqual(script, "print('Hello World')")

    def test_critique(self):
        scraper = Scraper(dummy_language_model, "Print 'Hello World'")
        scraper.generate_and_run_script()
        result = scraper.critique()
        self.assertEqual(result, False)

    def test_format_input_string(self):
        scraper = Scraper(dummy_language_model, "Print 'Hello World'")
        input = scraper.format_input_string()
        string = (
            "Please write a Python script for the following job: \"" + 
			"Print 'Hello World'" + 
			"\". Please surround code by ```."
        )
        self.assertEqual(input, string)

    def test_generate_and_run_script(self):
        scraper = Scraper(dummy_language_model, "Print 'Hello World'")
        scraper.generate_and_run_script()
        self.assertEqual(len(scraper.history), 1)
    
    def test_generate_script(self):
        scraper = Scraper(dummy_language_model, "Print 'Hello World'")
        prompt = scraper.format_input_string()
        code = scraper.generate_script(prompt)
        self.assertIsInstance(code, str)

    def test_run_script(self):
        scraper = Scraper(dummy_language_model, "Print 'Hello World'")
        input = "print(\"Hello World!\")"
        result = scraper.run_script(input)
        self.assertEqual(result.stdout, "Hello World!\n")
        input = "number = 3\nprint(number[0])"
        result = scraper.run_script(input)
        self.assertNotEqual(result.stderr, "")

if __name__ == '__main__':
    unittest.main()
