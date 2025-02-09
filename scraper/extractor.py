
def summarize_segments(segments: List[str]) -> List[str]:
    """
    While any HTML chunk hints at a revision:
        Give LLM (user_request, HTML_chunk[i], code) and ask it to summarize 
            anything worth noting relevant to revision of the script and 
            decide if anything has to be done.
        Give LLM (user_request, stdout_chunk[i], code) and ask it to 
            summarize anything worth noting relevant to revision of the 
            script and plan what it should do (next_step).
        Give LLM (user_request, stdout_chunk[i], next_step, code) and ask it
            to revise the code.   
    """
    return

def generate(self):
    utils.generate_and_run_script()
    need_revision  = self.critique()
    print("Finished an iteration.")
    while need_revision:
        utils.generate_and_run_script()
        need_revision = self.critique()
        print("Finished an iteration.")
    return self.history[-1]['script']

def critique(self) -> bool:
    """
    Decide if the script needs revision
    """
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

def generate_and_run_script(self) -> None:
    """
    Generate and run a script.
    """
    input_string = self.format_input_string()
    code = utils.generate_script(input_string)
    print("Generating script.")
    current_step = {}
    current_step['script'] = code
    print("Running code.")
    result = utils.run_script(code)
    current_step['stdout'] = result.stdout
    current_step['stderr'] = result.stderr
    self.history.append(current_step)
    print("Current iteration gives " + str(current_step) + '.\n')

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