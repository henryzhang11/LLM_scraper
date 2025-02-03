from llama_cpp import Llama
from rich import print

class QuantizedModel:
	
	def __init__(self, local=False, logprobs=False, threads=2):
		"""
		Loads a language model.
		Args:
			local (bool): Whether to load model from disk.
		"""
		self.log_probs=logprobs
		if logprobs == True:
			self.model = Llama.from_pretrained(
				repo_id="bartowski/gemma-2-9b-it-GGUF",
				filename="gemma-2-9b-it-IQ2_M.gguf",
				n_ctx = 1024, 
				n_threads=threads, 
				seed=42,
				logits_all=True,
				verbose=False
			)
		else:
			self.model = Llama.from_pretrained(
				repo_id="bartowski/gemma-2-9b-it-GGUF",
				filename="gemma-2-9b-it-IQ2_M.gguf",
				n_ctx=1024,
				n_threads=threads,
				seed=42,
				verbose=False
			)

	def language_model(self, prompt: str) -> str:
		if self.log_probs == True:
			response = self.model(prompt, max_tokens=1024, logprobs=1, temperature=0.5, top_k=40)
			logprobs = response['choices'][0]['logprobs']
			top_logprobs = logprobs['top_logprobs'] # Top 1 token log probability
			self.color_with_log_probs(top_logprobs)			
		else:
			response = self.model(prompt, max_tokens=1024, temperature=0.5, top_k=40)
		try:
			text = response['choices'][0]['text']
		except (KeyError, IndexError, TypeError):
			text = None
		return text
	
	def color_with_log_probs(top_logprobs):
		"""
		Print colored string based on 'top_logprobs'.
		"""
		result = ""
		for top_logprob in top_logprobs:
			result += color_with_log_prob(top_logprob)
		print(result)

	def color_with_log_prob(top_logprob):
		"""
		Calculate the color of a single token.
		"""
		# log 0.2, log 0.4, ..., log 1
		bounds = [-float('-inf'), -0.69897, -0.39794, -0.221848749, -0.09691, 0]
		token, logprob = next(iter(top_logprob.items()))
		g = 120
		for i in range(len(bounds) - 1):
			if bounds[i] < logprob and logprob <= bounds[i + 1]:
				g = 160 + i * 20
		color = f"#{0:02x}{g:02x}{0:02x}"
		return f"[{color}]{token}[/{color}]"