import utils
from typing import Callable
import re

def extract(
    language_model: Callable[[str], str],
    file_location: str, 
    job_description: str
) -> str:
    try:
        with open(file_location, 'r') as file:
            content = file.read()
    except Exception as e:
        print(f"An error {e} occured reading HTML.")
        return ""
    

def revise(
    language_model: Callable[[str], str],
    segment: str, 
    job_description: str, 
    script: str
) -> str:
    """Revise script based on new segment of HTML.
    """
    if not utils.contains_target(language_model, segment, job_description):
        return script
    