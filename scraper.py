import subprocess
from subprocess import CompletedProcess
from typing import Callable
import re
import os
import quantized_model

class Scraper:
	def __init__(self, language_model_function : Callable[[str], str]) -> None:
		self.language_model = language_model_function
		# "" for steps within a self-debugging session
		self.user_inputs = []
		# Attempts for the script
		self.language_model_output = []
		self.stdouts = []
		self.stderrs = []

	# Generate scripts until all requirements from user are met
	def generate_working_code(self):
		# Prompt user for input
		user_input = input("Please enter scraping job:")
		self.user_inputs.append(user_input.strip())
		self.generate_error_free_code()
		critique = input("Please enter issue(s) with scraping job:")
		while critique:
			self.user_inputs.append(critique.strip())
			self.generate_error_free_code()

	def format_input_string(self) -> str:
		if len(self.user_inputs) == 1:
			return (
				"Please write a Python script written for the following job: " + 
				self.user_inputs[0] + 
				" Please surround code by ```."
			)
		# Check if this is not a syntax revision, which has "" as user_inputs
		if self.user_inputs[-1] != "": 
			return (
				"Please revise a Python script written to do: " + 
				self.user_inputs[0] + 
				"```. Please make the following revision: " + 
				self.user_inputs[-1] +
				" Here is the script: ```" +
				self.language_model_output[-1] + 
				"```. Here is its standard output: ```" +
				self.stdouts[-1] +
				" Please surround code by ```."
			)
		# If this is a syntax revision
		else:
			return (
				"Please fix an error of a Python script written to do this: " + 
				self.user_inputs[0] + 
				" Here is the script: ```" +
				self.language_model_output[-1] + 
				"```. Here is its standard error: ```" +
				self.stderrs[-1] + 
				"```. Here is its standard output: ```" + 
				self.stdouts[-1] + 
				"```. Please surround code by ```."
			)

	# Generate scripts until one runs without error
	def generate_error_free_code(self, maximum_refinement_attempts=20) -> None:
		input_string = self.format_input_string()
		code = self.generate_code(input_string, maximum_refinement_attempts)
		self.language_model_output.append(code)
		result = self.test_run(code)
		self.stdouts.append(result.stdout)
		self.stderrs.append(result.stderr)
		script_revision_attempt = 0
		while (
			result.returncode != 0 and 
			script_revision_attempt < maximum_refinement_attempts
			):
			self.user_inputs.append("")
			input_string = self.format_input_string()
			code = self.generate_code(input_string, maximum_refinement_attempts) # TODO: include stdout and limit stdout/stderr output to first 1000 characters
			self.language_model_output.append(code)
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
	def generate_code(self, input, maximum_refinement_attempts=20) -> str:
		language_model_response = self.language_model(input)
		match = re.search(
			r"```(?:python)?\n(.*?)\n```", 
			language_model_response, 
			re.DOTALL
		)
		format_revision_attempt = 0
		while not match and format_revision_attempt < maximum_refinement_attempts:
			language_model_response = self.language_model(input)
			match = re.search(
				r"```(?:python)?\n(.*?)\n```", 
				language_model_response, 
				re.DOTALL
			)
			format_revision_attempt += 1
		if match:
			print(
				"Found code snippet in language model response text" + 
				f" at attempt {format_revision_attempt}"
			)
			print(
				"Trying to run the following code:" +
				match.group(1)
			)
			return match.group(1)
		else:
			raise ValueError("Couldn't generate code block.")

if __name__ == "__main__":
	model = Scraper(quantized_model.language_model)
	model.generate_working_code()
