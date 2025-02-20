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