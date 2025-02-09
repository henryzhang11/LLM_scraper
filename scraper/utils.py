import subprocess
from subprocess import CompletedProcess
import re
from typing import Callable
from typing import List

def segment_string(string: str, context_window: int) -> List[str]:
    """
    Segment the string into a list of strings with length < context_window / 2
    """
    segments = []
    current_segment_start = 0
    current_segment_end = min(len(string), context_window // 2)
    segments.append(str[current_segment_start : current_segment_end])
    while current_segment_end < len(string) - 1:
        current_segment_start = current_segment_end
        current_segment_end = min(
            current_segment_start + context_window // 2, 
            len(string) - 1
        )
        segments.append(str[current_segment_start, current_segment_end])
    return segments

# TODO: Run code in container instead of directly
def run_script(code : str) -> CompletedProcess:
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

def concatenate_scripts(script_1, script_2) -> str:
    """
    Refactor script 1 and script 2 into functions, concatenate them, and 
    return the concatenated function.  
    """
    # Add a tab in front of all lines in script 1

    script_1 = "def func_1():\n" + script_1

    # Add a tab in front of all lines in script 2
    
    script_2 = "def func_2():\n" + script_2
    final_script = (script_1 + "\n" 
        + script_2 
        + "\n" + "def main():\n\tfunc_1()\n\tfunc_2()"
    )
    return final_script