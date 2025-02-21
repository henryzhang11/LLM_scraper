    def test_run_script(self):
        scraper = Scraper(dummy_language_model, "Print 'Hello World'")
        input = "print(\"Hello World!\")"
        result = scraper.run_script(input)
        self.assertEqual(result.stdout, "Hello World!\n")
        input = "number = 3\nprint(number[0])"
        result = scraper.run_script(input)
        self.assertNotEqual(result.stderr, "")

