from typing import List, Callable

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

def contains_target(
    language_model: Callable[[str], str],
    segment: str, 
    user_request: str
) -> bool:
    """Decides if current segment of HTML contains relevant information.
    """
    request = (
        "Please answer the following question about a chunk of " + 
        "downloaded file by briefly analyzing and answering 'Yes' or 'No' " + 
        "at the end of your answer: Does the chunk contain information " + 
        "relevant to this web-scraping request: \"" + 
        user_request + 
        "\"? Here is the chunk: \"" + 
        segment + 
        "\"."
    )
    language_model_output = language_model(request)
    match = re.search(r'\b(Yes|No)\b', language_model_output)
    result = match.group(0) if match else None
    while match is None:
        print(f"Deciding whether segment[{i}] contains relevant info.")
        language_model_output = language_model(request)
        match = re.search(r'\b(Yes|No)\b', language_model_output)
        result = match.group(0) if match else None
    if result == "Yes":
        return True
    return False
