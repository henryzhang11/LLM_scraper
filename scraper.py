import subprocess
from subprocess import CompletedProcess
from typing import Callable, Tuple
import re

class Scraper:
	def __init__(
		self,
		language_model_function: Callable[[str], str],
		user_input: str
	) -> None:
		self.job_description = user_input
		self.language_model = language_model_function
		self.script = ""
		self.stdouts = []
		self.stderrs = []
		
	@classmethod
	def generate_and_revise(cls, language_model_function: Callable[[str], str], user_input: str) -> str:
		"""
		Class method that instantiates Scraper and calls its instance method.I
		"""
		instance = cls(language_model_function, user_input)
		return instance.generate_and_revise_instance()

	def generate_and_revise_instance(self) -> str:
		"""
		Class method that generate scripts until no longer needing revision
		"""
		self.generate_script()
		need_revision  = self.critique()
		while need_revision:
			self.generate_script()
			need_revision = self.critique()
		return self.script

	def critique(self) -> Tuple[bool, str]:
		# TODO: give language model job, code, stdout, and stderr and 
		input_string = (
			"Please judge whether ```" + 
			self.script + 
			"```, which when executed gives the standard output: ```" +
			self.stdout + 
			"''', and the standard error: ```" + 
			self.stderr +
			"```, accomplished the following job: '" + 
			self.job_description +
			"'. Please briefly analyze the script and output 'Yes' or 'No' at the end of your response."
		)
		language_model_output = self.language_model(input_string)
		match = re.search(r'\b(Yes|No)\b$', language_model_output)
		result = match.group(0) if match else None
		if match is None:
			language_model_output = self.language_model(input_string)
			match = re.search(r'\b(Yes|No)\b$', language_model_output)
			result = match.group(0) if match else None
		if result == 'No':
			return False
		return True	

	def format_input_string(self) -> str:
		if self.script == "":
			return (
				"Please write a Python script for the following job: " + 
				self.job_description + 
				" Please surround code by ```."
			)
		# Otherwise, revise the script
		else: 
			return (
				"Please work on a Python script for the following job: " + 
				self.job_description + 
				" Here is the current script: ```" +
				self.script + 
				"```. Here is its standard output: ```" +
				self.stdout +
				"```. Here is its standard error: ```" + 
				self.stderr +
				" Please surround code by ```."
			)

	# Generate scripts until one runs without error
	def generate_script(self) -> None:
		input_string = self.format_input_string()
		code = self.generate_code(input_string)
		self.script.append(code)
		result = self.test_run(code)
		self.stdouts.append(result.stdout)
		self.stderrs.append(result.stderr)

	# Try running code
	# TODO: Run code in container instead of directly
	def test_run(self, code : str) -> CompletedProcess: 
		script_filename = 'script_attempt.py'
		with open(script_filename, 'w') as file:
			file.write(code)
		return subprocess.run(
			["python3", "script_attempt.py"],
			capture_output=True,
			text=True,
			timeout=30)

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
