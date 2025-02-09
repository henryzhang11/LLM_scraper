import unittest
import scraper.downloader as downloader
from typing import Callable, Tuple
from scraper.language_model import QuantizedModel
import os

class TestDownloadFile(unittest.TestCase):

    def test_download_script(self) -> Tuple[str, str]:
        """Test download_script.

        Test download_script returns a Python script that runs without error and
        a file location that exists after running the script.
        """
        model = QuantizedModel(logprobs=True)

        script, file = downloader.download(
            model.language_model, 
            user_request
        )
        
        if os.path.exists(file):
            os.remove(file)
        
        self.assertTrue(
            os.path.exists(file),
            "The script doesn't generate the file."
        )

        

        
