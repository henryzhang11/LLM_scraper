import unittest
import summarizer
import requests

class TestSummarizer(unittest.TestCase):

	def test_segment_string(self):
		'''
		Test whether segments are short enough strings
		'''
		context_window = 8192 #TODO: Change context_window if necessary
		response = requests.get("https://en.wikipedia.org/robots.txt")
		output = response.text
		self.assertIsInstance(output, str)
		segments = summarizer.segment_string(output, context_window)
		self.assertIsInstance(segments, list)
		self.assertTrue(
			all(isinstance(item, str) for item in segments), 
			"Not all segments are strings."
		)	
		for i in range(len(segments)):
			self.assertLessEqual(
				len(segments[i]), context_window, 
				"Not all segments have length <= context_window"
			)

	def test_summarize_segments(self):
		'''
		Test whether summarizations are short enough strings	
		'''
		context_window = 8192 #TODO: Change context_window if necessary
		response = requests.get("https://en.wikipedia.org/robots.txt")
		output = response.text
		self.assertIsInstance(output, str)
		segments = summarizer.segment_string(output, context_window)
		summaries = summarizer.summarize_segments(segments)
		for i in range(len(summaries)):
			self.assertIsInstance(summaries[i], str)
			self.assertLessEqual(len(summaries[i]), 300)

if __name__ == '__main__':
	unittest.main()	
