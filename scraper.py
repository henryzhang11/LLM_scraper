import subprocess
from subprocess import CompletedProcess
from typing import Callable, Tuple
import re
import quantized_model

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
		"""
		Class method that instantiates Scraper and calls its instance method.I
		"""			
		instance = cls(language_model_function, user_input)
		return instance.generate_instance()

	def generate_instance(self) -> str:
		"""
		Class method that generate scripts until no longer needing revision
		"""
		self.generate_and_run_script()
		need_revision  = self.critique()
		print("Finished an iteration.")
		while need_revision:
			self.generate_and_run_script()
			need_revision = self.critique()
			print("Finished an iteration.")
		return self.history[-1]['script']

	def critique(self) -> bool:
		# If the code produces errors, revise it.
		if self.history[-1]['stderr'] != "":
			return True
		# If the code doesn't do what the prompt asks, revise it.
		input_string = (
			"Please judge whether ```" + 
			self.history[-1]['script'] + 
			"```, which when executed gives the standard output: ```" +
			self.history[-1]['stdout'] + 
			"```, accomplished the following job: '" + 
			self.job_description +
			"'. Please analyze and output 'Yes' or 'No' in the end."
		)
		print("Generating critique for latest attempt.")
		language_model_output = self.language_model(input_string)
		match = re.search(r'\b(Yes|No)\b$', language_model_output)
		result = match.group(0) if match else None
		if match is None:
			print("Generating new critique for latest attempt.")
			language_model_output = self.language_model(input_string)
			match = re.search(r'\b(Yes|No)\b$', language_model_output)
			result = match.group(0) if match else None
		if result == 'Yes':
			return False
		return True	

	def format_input_string(self) -> str:
		if self.history == []:
			return (
				"Please write a Python script for the following job: \"" + 
				self.job_description + 
				"\". Please surround code by ```."
			)
		# Otherwise, revise the script
		else: 
			return (
				"Please work on a Python script for the following job: \"" + 
				self.job_description + 
				"\". Here is history of past scripts, stdouts, and stderrs: " +
				str(self.history) +
				" Please surround code by ```."
			)

	# Generate and run a script.
	def generate_and_run_script(self) -> None:
		input_string = self.format_input_string()
		code = self.generate_script(input_string)
		print("Generating script.")
		current_step = {}
		current_step['script'] = code
		print("Running code.")
		result = self.run_script(code)
		current_step['stdout'] = result.stdout
		current_step['stderr'] = result.stderr
		self.history.append(current_step)
		print("Current iteration gives " + str(current_step) + '.\n')

	# Generate responses until one contains a code block.
	def generate_script(self, model_input, maximum_refinement_attempts=20) -> str:
		print("Generating language model response.")
		language_model_response = self.language_model(model_input)
		match = re.search(
			r"```(?:python)?\n(.*?)\n```", 
			language_model_response, 
			re.DOTALL
		)
		format_revision_attempt = 0
		while (
			not match 
			and format_revision_attempt < maximum_refinement_attempts
		):
			print("Generating new language model response.")
			language_model_response = self.language_model(model_input)
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
			print("Trying to run the following code:" + match.group(1))
			return match.group(1)
		else:
			raise ValueError("Couldn't generate code block.")

	# Run generated code.
	# TODO: Run code in container instead of directly
	def run_script(self, code : str) -> CompletedProcess: 
		script_filename = 'script_attempt.py'
		with open(script_filename, 'w') as file:
			file.write(code)
		return subprocess.run(
			["python3", "script_attempt.py"],
			capture_output=True,
			text=True,
			timeout=30)

if __name__ == '__main__':	
	quantized_model = quantized_model.QuantizedModel()
	job = input("Enter job: ")
	scraper = Scraper.generate(quantized_model.language_model, job)
