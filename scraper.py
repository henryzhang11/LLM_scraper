import subprocess
from typing import Callable
import re

class scraper:
	def __init__(self) -> None:
		self.user_inputs = []
		self.language_model_output = []
		self.interpreter_feedback = []
		# Prompt user for input
		user_input = input("Please enter scraping job:")
		self.user_inputs.append(user_input)
	
	def scrape(self, language_model : Callable[[str], str]) -> None: 
		maximum_refinement_attempts = 20
		language_model_response = language_model(self.user_inputs[0] + " Please put your code in a block surrounded by '&&&&'s.")
		match = re.search(r'&&&&\n(.*?)\n&&&&', language_model_response, re.DOTALL)
		format_revision_attempt = 0
		while not match and format_revision_attempt < maximum_refinement_attempts:
			language_model_response = language_model(self.user_inputs[0] + " Please put your code in a block surrounded by '&&&&'s.")
			match = re.search(r'&&&&\n(.*?)\n&&&&', language_model_response, re.DOTALL)
			format_revision_attempt += 1
		code = match.group(1)
		with open(f'scraper_attempt.py', 'w') as file:
			file.write(code)
		result = subprocess.run(['python', 'scraper_attempt.py'], capture_output=True, text=True)
		script_revision_attempt = 0
		while result.returncode != 0 and script_revision_attempt < maximum_refinement_attempts:
			self.interpreter_feedback.append(result.stderr)
			language_model_response = language_model("Please help me fix the following error: \"" + self.interpreter_feedback[-1] + "\" which results from executing the code: \"" + self.language_model_output[-1] + "\" for the task " + self.user_inputs[0] + "Please put your code in a block surrounded by '&&&&'s.")
			match = re.search(r'&&&&\n(.*?)\n&&&&', language_model_response, re.DOTALL)
			format_revision_attempt = 0
			while not match and format_revision_attempt < maximum_refinement_attempts:
				language_model_response = language_model("Please help me fix the following error: \"" + self.interpreter_feedback[-1] + "\" which results from executing the code: \"" + self.language_model_output[-1] + "\" for the task " + self.user_inputs[0] + "Please put your code in a block surrounded by '&&&&'s.")
				match = re.search(r'&&&&\n(.*?)\n&&&&', language_model_response, re.DOTALL)
				format_revision_attempt += 1
			fixed_code = match.group(1)
			self.user_inputs.append("")
			self.language_model_output.append(fixed_code)
			with open(f'scraper_attempt.py', 'w') as file:
				file.write(fixed_code)
			result = subprocess.run(['python', 'scraper_attempt.py'], capture_output=True, text=True)			
			script_revision_attempt += 1

if __name__ == "__main__":
	model = scraper()
	model.scrape(language_model_function)