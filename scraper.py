import subprocess
from subprocess import CompletedProcess
from typing import Callable
import re
import os
import ggml_model

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
		self.openai_API_key = input("Please enter OpenAI API key:")

	# Generate scripts until all requirements from user are met
	def generate_working_code(
			self,
			language_model : Callable[[str], str]
	):
		self.generate_error_free_code(language_model)
		critique = input("Please enter scraping problem:")
		while critique:
			self.user_inputs.append(critique)
			self.generate_error_free_code(language_model)
	
	# Generate scripts until one runs without error
	def generate_error_free_code(
		self, 
		language_model : Callable[[str], str], 
		maximum_refinement_attempts=20
		) -> None:
		input_string = self.user_inputs[0] + " Please surround code by ```."
		code = self.generate_code(
			input_string, 
			language_model, 
			maximum_refinement_attempts
		)
		self.language_model_output.append(code)
		self.user_inputs.append("")
		result = self.test_run(code)
		self.stdouts.append(result.stdout)
		self.stderrs.append(result.stderr)
		script_revision_attempt = 0
		while (
			result.returncode != 0 and 
			script_revision_attempt < maximum_refinement_attempts):
			input_string = (
				"Please fix the following error: \"" + 
				self.stderrs[-1][:1000] + 
				"\" which results from executing the code: \"" + 
				self.language_model_output[-1] + 
				"\" for the task " + 
				self.user_inputs[0] + 
				" Please surround code by ```."
			)
			code = self.generate_code(
				input_string, 
				language_model, 
				maximum_refinement_attempts
			) # TODO: include stdout and limit stdout/stderr output to first 1000 characters
			self.language_model_output.append(code)
			self.user_inputs.append("")
			result = self.test_run(code)
			self.stdouts.append(result.stdout)
			self.stderrs.append(result.stderr)
			script_revision_attempt += 1
		if result.returncode != 0:
			raise ValueError("Couldn't generate error free code.")

	# Try running code
	def test_run(self, code : str) -> CompletedProcess: 
		script_filename = 'script_attempt.py'
		with open(script_filename, 'w') as file:
			file.write(code)
		try:
			return subprocess.run(
				[
					'docker', 'run', '--rm', '-v', f"{os.getcwd()}:/app", 'python:3.9', 
		 			'python', f"/app/{script_filename}"
				],
				capture_output=True,
				text=True,
				timeout=30)
		finally:
			os.remove('script_attempt.py')

	# Generate responses until one contains a code block
	def generate_code(
			self, 
			input, 
			language_model : Callable[[str], str], 
			maximum_refinement_attempts=20
		) -> str:
		language_model_response = language_model(input)
		match = re.search(
			r"```(?:python)?\n(.*?)\n```", 
			language_model_response, 
			re.DOTALL
		)
		format_revision_attempt = 0
		while not match and format_revision_attempt < maximum_refinement_attempts:
			language_model_response = language_model(input)
			match = re.search(
				r"```(?:python)?\n(.*?)\n```", 
				language_model_response, 
				re.DOTALL
			)
			format_revision_attempt += 1
		if match:
			return match.group(1)
		else:
			raise ValueError("Couldn't generate code block.")

if __name__ == "__main__":
	model = Scraper()
	model.generate_error_free_code(ggml_model.language_model)