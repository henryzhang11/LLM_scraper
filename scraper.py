import subprocess
from subprocess import CompletedProcess
from typing import Callable
import re

class Scraper:
	def __init__(self) -> None:
		# "" for steps within a self-debugging session
		self.user_inputs = []
		# Attempts for the script
		self.language_model_output = []
		self.stdouts = []
		self.stderrs = []
		# Prompt user for input
		user_input = input("Please enter scraping job:")
		self.user_inputs.append(user_input)

	# Prompts for new user feedback until no more feedback
	
	# Generate scripts until one runs without error
	def generate_error_free_code(self, language_model : Callable[[str], str], maximum_refinement_attempts=20) -> None: 
		code = self.generate_code(self.user_inputs[0] + " Please surround code by '''.", language_model, maximum_refinement_attempts)
		self.language_model_output.append(code)
		self.user_inputs.append("")
		result = self.test_run(code)
		self.stdouts.append(result.stdout)
		self.stderrs.append(result.stderr)
		script_revision_attempt = 0
		while result.returncode != 0 and script_revision_attempt < maximum_refinement_attempts:
			code = self.generate_code("Please fix the following error: \"" + self.stderrs[-1] + "\" which results from executing the code: \"" + self.language_model_output[-1] + "\" for the task " + self.user_inputs[0] + " Please surround code by '''.", language_model, maximum_refinement_attempts) # TODO: include stdout
			self.language_model_output.append(code)
			self.user_inputs.append("")
			result = self.test_run(code)
			self.stdouts.append(result.stdout)
			self.stderrs.append(result.stderr)
			script_revision_attempt += 1
		if result.returncode != 0:
			raise ValueError("Failed to generate syntactically correct code.")

	# Try running code
	def test_run(self, code : str) -> CompletedProcess: 
			with open(f'script_attempt.py', 'w') as file:
				file.write(code)
			return subprocess.run(['python', 'script_attempt.py'], capture_output=True, text=True)

	# Generate responses until one contains a code block
	def generate_code(self, input, language_model : Callable[[str], str], maximum_refinement_attempts=20) -> str:
		language_model_response = language_model(input)
		match = re.search(r"'''\n(.*?)\n'''", language_model_response, re.DOTALL)
		format_revision_attempt = 0
		while not match and format_revision_attempt < maximum_refinement_attempts:
			language_model_response = language_model(input)
			match = re.search(r"'''\n(.*?)\n'''", language_model_response, re.DOTALL)
			format_revision_attempt += 1
		if match:
			return match.group(1)
		else:
			raise ValueError("Failed to generate response containing code block.")

def language_model_function(prompt: str) -> str:
    # Implement the function to call your language model API
    pass

if __name__ == "__main__":
	model = Scraper()
	# TODO: Implement a sandbox for language model
	model.generate_error_free_code(language_model_function)