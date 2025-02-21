import utils
from error_free_coder import ErrorFreeCoder
from typing import Callable

def extract(
    language_model: Callable[[str], str],
    file_location: str, 
    job_description: str,
    context_window
) -> str:
    try:
        with open(file_location, 'r') as file:
            content = file.read()
    except Exception as e:
        print(f"An error {e} occured reading HTML.")
        return ""
    segments = utils.segment_string(content, context_window // 2)
    script = ""
    for i in range(len(segments)):
        if not utils.contains_target(language_model, segment, job_description):
            continue
        revision_request = (
            "Please revise a script that extracts information from the " +
            "downloaded HTML file for the following request: \"" + 
            job_description + 
            f'". Here is the script: "' + 
            script + 
            "\" and here is the HTML segment: \"" + 
            segments[i] + 
            "\"."
        )
        coder = ErrorFreeCoder(language_model, revision_request)
        script = coder.generate_error_free_code()
    return script