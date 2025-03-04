from typing import Callable, Tuple
import utils
import language_model
import downloader
import extractor

class Scraper:

	def __init__(
		self,
		language_model_function: Callable[[str], str],
		context_window_length: int,
		user_input: str
	) -> None:
		self.job_description = user_input
		self.language_model = language_model_function
		self.context_window = context_window_length
		# Each element in 'history' maps script, stdout, and stderr to strings
		self.history = []
		
	@classmethod
	def generate(
		cls, 
		language_model_function: Callable[[str], str], 
		context_window: int,
		user_input: str
	) -> str:
		"""Initialize Scraper and call its instance method.

		Returns:
			str: script for the scraping job
		"""			
		instance = cls(language_model_function, context_window, user_input)
		return instance.generate_instance()

	def generate_instance(self) -> str:
		"""Generate scripts until no longer needing revision.

		First ask LLM to generate script to download HTML into specific file. 
		Then work on script that extracts relevant information. Finally 
		concatenate the former 2 scripts and return the script.
		"""
		download_script, file_location = downloader.download(
			self.language_model, 
			self.job_description,
			self.context_window
		)
		extract_script = extractor.extract(
            self.language_model,
			file_location, 
			self.job_description,
			self.context_window
		)
		final_script = utils.concatenate_scripts(
			download_script, 
			extract_script
		)
		return final_script

if __name__ == '__main__':	
	model = language_model.LanguageModel()
	job = input("Enter job: ")
	scraper = Scraper.generate(model.generate_response, 1024, job)
