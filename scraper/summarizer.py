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

def summarize_segments(segments: List[str]) -> List[str]:
    """
    Summarize output by segments and decide if the entire output 
    """

    return