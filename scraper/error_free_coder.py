import re
from typing import Callable
from subprocess import CompletedProcess
import subprocess
import utils

class ErrorFreeCoder:
    """An LLM wrapper that generates a script until there are no errors.
    """

    def __init__(
        self, 
        language_model: Callable[[str], str], 
        request: str
    ) -> None:
        self.context = request
        self.sript = ""
        self.stdout = ""
        self.stderr = ""
        self.model = language_model

    def generate_error_free_code(self) -> str:
        """Generate and revise code until getting no errors.
        """
        self.generate_and_run_script(self.model, self.context)
        while self.stderr != "":
            revision_input = (
				"Please write a Python script to fulfill the following request: \"" +
				self.context + 
                "\" Please do so by revising ```" + 
                self.script + 
                "``` which gives the stdout ```" + 
                self.stdout + 
                "``` and standerr ```" + 
                self.stderr
            )
            self.generate_and_run_script(self.model, revision_input)
        return self.script

    def generate_and_run_script(self, language_model, request) -> None:
        """Generate and run a script.
        """
        print("Generating and running script.")
        code = self.generate_script(language_model,request)
        self.script = code
        result = self.run_script(code)
        self.stdout = result.stdout
        self.stderr = result.stderr

    # TODO: Run code in container instead of directly
    def run_script(self, code : str) -> CompletedProcess:
        """
        Run generated code.
        """
        print("Running the following code: \"" + code + "\".")
        script_filename = 'script_attempt.py'
        with open(script_filename, 'w') as file:
            file.write(code)
        return subprocess.run(
            ["python3", "script_attempt.py"],
            capture_output=True,
            text=True,
            timeout=30)
      
    def generate_script(
        self,
        language_model: Callable[[str], str],
        model_input: str,
        maximum_refinement_attempts=20
    ) -> str:
        """
        Generate responses until one contains a code block.
        """
        print(f"Generating script.")
        language_model_response = language_model(model_input)
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
            print(f"Generating script another time.")
            language_model_response = language_model(model_input)
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
