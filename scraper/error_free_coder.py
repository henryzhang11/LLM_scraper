
import re
from typing import Callable, CompletedProcess
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
        """Generate and revise code until getting no erros.
        """
        self.generate_and_run_script(input)
        while self.stderr != "":
            revision_input = (input + 
                "Please do so by revising ```" + 
                self.script + 
                "``` which gives the stdout ```" + 
                self.stdout + 
                "``` and standerr ```" + 
                self.stderr
            )
            self.generate_and_run_script(revision_input)
        return self.current_step['script']

    def generate_and_run_script(self, language_model, input) -> None:
        """Generate and run a script.
        """
        code = utils.generate_script(language_model, input)
        print("Generating script.")
        self.script = code
        print("Running code.")
        result = utils.run_script(code)
        self.stdout = result.stdout
        self.stderr = result.stderr
        print("Current iteration gives " + str(self.current_step) + '.\n')

    # TODO: Run code in container instead of directly
    def run_script(self, code : str) -> CompletedProcess:
        """
        Run generated code.
        """
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
        print("Generating language model response.")
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
            print("Generating new language model response.")
            language_model_response = language_model(model_input)
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