import utils

class Downloader:
    
    def __init__(self):
        return

    def download(self):
        """
        While step 2 returns True:
                Give LLM user_request and ask it to write code that downloads the 
                    HTML into a temp.html file. 
                Give LLM (user_request, HTML_chunk[i]) and ask it to decide if any 
                    stdout_chunk[i] contains relevant data.
        Returns the 
        """