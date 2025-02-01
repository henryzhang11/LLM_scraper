import unittest
from quantized_model import QuantizedModel
import time

def dummy_language_model(**kwargs):
    return None

class TestQuantizedModel(unittest.TestCase):

    def test_language_model_logprobs_true(self):
        print("Test logprobs=True mode")
        self.quantized_model = QuantizedModel(logprobs=True)
        self.quantized_model.language_model("Once upon a time in a land far far away")
 
    def test_language_model_logprobs_false(self):
        # Test "language_model" finishes in 5 minutes (generating 1000 tokens).
        tic = time.time()
        print("Test logprobs=False mode")
        self.quantized_model = QuantizedModel(logprobs=False)
        self.quantized_model.language_model("Once upon a time in a land far far away")
        toc = time.time()
        seconds = toc - tic
        self.assertLess(seconds, 300)
        # Test "language_model" doesn't raise an error getting wrong responses.
        self.quantized_model.model = dummy_language_model
        self.quantized_model.language_model("Once upon a time in a land far far away")

if __name__ == "__main__":
    unittest.main()
