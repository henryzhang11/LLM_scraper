from typing import Callable, Tuple
import utils
import language_model
import downloader
import extractor

class Scraper:

	def __init__(
		self,
		language_model_function: Callable[[str], str],
		user_input: str
	) -> None:
		self.job_description = user_input
		self.language_model = language_model_function
		# Each element in 'history' maps script, stdout, and stderr to strings
		self.history = []
		
	@classmethod
	def generate(
		cls, 
		language_model_function: Callable[[str], str], 
		user_input: str
	) -> str:
		"""Initialize Scraper and call its instance method.

		Returns:
			str: script for the scraping job
		"""			
		instance = cls(language_model_function, user_input)
		return instance.generate_instance()

	def generate_instance(self) -> str:
		"""Generate scripts until no longer needing revision.

		First ask LLM to generate script to download HTML into specific file. 
		Then work on script that extracts relevant information. Finally 
		concatenate the former 2 scripts and return the script.
		"""
		download_script, file_location = downloader.download()
		extract_script = extractor.extract(file_location)
		final_script = utils.concatenate_scripts(
			download_script, 
			extract_script
		)
		return final_script

if __name__ == '__main__':	
	model = language_model.QuantizedModel()
	job = input("Enter job: ")
	scraper = Scraper.generate(model.generate_response, job)