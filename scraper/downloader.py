import os
from typing import Tuple, Callable
from error_free_coder import ErrorFreeCoder
import utils
import re

# TODO: Add code for page navigation.
def download(
    language_model: Callable[[str], str],
    user_request: str,
    context_window: int
) -> Tuple[str, str]:
    """Write a file that downloads the HTML until it succeeds
    Returns:
        tuple: A tuple containing:
            download_script (str): A script for downloading the HTML file
    """
    print("Generating script for downloading HTML.")
    # Compute a hash number to avoid conflict
    hash_value = str(hash(user_request))[:4] 
    file_path = "./temp" + hash_value
    # Remove 'temp' file
    if os.path.exists(file_path):
        os.remove(file_path)
    download_request = (
        "Please download the HTML file needed for the " +
        "following request: \"" +
        user_request + 
        f'" to "{file_path}".'
    )                 
    coder = ErrorFreeCoder(language_model, download_request)
    script = coder.generate_error_free_code()
    attempts = 1
    while (
        (not os.path.exists(file_path) or 
        contains_no_target(
            file_path, 
            user_request, 
            language_model,
            context_window
        )) and attempts <= 5
    ):
        coder = ErrorFreeCoder(language_model, download_request)
        script = coder.generate_error_free_code()
        attempts += 1
    return script, file_path

def contains_no_target(
    file_path, 
    user_request: str,
    language_model: Callable[[str], str],
    context_window: int
) -> bool:
    print("Generating critique for latest download_script attempt.")
    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except Exception as e:
        print(f"An error {e} occured reading {file_path}.")
        return True
    segments = utils.segment_string(content, context_window // 2)
    contains_target = False
    for i in range(len(segments)):
        result = utils.contains_target(
            language_model, 
            segments[i], 
            user_request
        )
        if result == "Yes":
            contains_target = True
    return not contains_target
