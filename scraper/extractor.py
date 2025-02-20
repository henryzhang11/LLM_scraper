import utils
import re

def generate():
    utils.generate_and_run_script()
    need_revision  = critique()
    print("Finished an iteration.")
    while need_revision:
        utils.generate_and_run_script()
        need_revision = critique()
        print("Finished an iteration.")
    return history[-1]['script']

def critique() -> bool:
    """
    Decide if the script needs revision
    """
    # If the code produces errors, revise it.
    if history[-1]['stderr'] != "":
        return True
    # If the code doesn't do what the prompt asks, revise it.
    input_string = (
        "Please judge whether ```" + 
        history[-1]['script'] + 
        "```, which when executed gives the standard output: ```" +
        history[-1]['stdout'] + 
        "```, accomplished the following job: '" + 
        job_description +
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
    """
    Generate input string 
    """
    if self.history == []:
        return (
            "Please write a Python script for the following job: \"" + 
            self.job_description + 
            "\". Please surround code by ```."
        )
    # Otherwise, revise the script
    # TODO: Change the input string for revisions to account for summaries
    else: 
        return (
            "Please work on a Python script for the following job: \"" + 
            self.job_description + 
            "\". Here is history of past scripts, stdouts, and stderrs: " +
            str(self.history) +
            " Please surround code by ```."
        )