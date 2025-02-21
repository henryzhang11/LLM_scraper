import unittest
from scraper.scraper import Scraper

"""
Get the number of datasets currently listed on "https://data.gov".
Get the name of the most recently added dataset on "http://catalog.data.gov/dataset?q=&sort=metadata_created+desc".
Get h1 tag from "example.com".
Get the header tags from "en.wikipedia.org/wiki/Main_Page".
Get all image links from "en.wikipedia.org/wiki/Peter_Jeffrey_(RAAF_officer)".(scraper_venv)
"""

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


if __name__ == '__main__':
    unittest.main()
