import subprocess

class scraper:
	user_inputs = []
	language_model_output = []
	interpreter_feedback = []

	def __init__ scraper(self, language_model : Callable[str, str]) -> None:
		# Prompt user for input
		user_input = input("Please enter scraping job:")
		user_inputs.append(user_input)
		language_model_output.append(language_model(user_input))
		with open(f'scraper_attempt.py', 'w') as file:
			file.write(language_model_output[-1])
		result = subprocess.run(['python', 'scraper_attempt.py'], capture_output=True, text=True)
		if result.returncode == 0:
			interpreter_feedback.append(result.stdout)
		else:
			interpreter_feedback.append(result.stderr)
		
