from llama_cpp import Llama
import logprob_coloring

class QuantizedModel:
	def __init__(self, logprobs=False, threads=2):
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
			logprob_coloring.color_with_log_probs(top_logprobs)			
		else:
			response = self.model(prompt, max_tokens=1024, temperature=0.5, top_k=40)
		try:
			text = response['choices'][0]['text']
		except (KeyError, IndexError, TypeError):
			text = None
		return text