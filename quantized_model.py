from llama_cpp import Llama
import logprob_coloring

class LanguageModel:
	def __init__(self, logprobs=False):
		self.log_probs=logprobs
		if logprobs == True:
			self.model = Llama.from_pretrained(
				repo_id="bartowski/gemma-2-9b-it-GGUF",
				filename="gemma-2-9b-it-IQ2_M.gguf",
				n_ctx = 1024, 
				n_threads=2, 
				seed=42,
				logits_all=True 
			)
		else:
			self.model = Llama.from_pretrained(
				repo_id="bartowski/gemma-2-9b-it-GGUF",
				filename="gemma-2-9b-it-IQ2_M.gguf",
				n_ctx=1024,
				n_threads=2,
				seed=42,
				logits_all=True
			)

	def language_model(self, prompt: str) -> str:
		if self.log_probs == True:
			response = self.model(prompt, max_tokens=1024, logprobs=1, temperature=0.5, top_k=40)
			logprobs = response['choices'][0]['logprobs']
			top_logprobs = logprobs['top_logprobs'] # Top 1 token log probability
			logprob_coloring.color_with_log_probs(top_logprobs)			
		else:
			response = self.model(prompt, max_tokens=1024, temperature=0.5, top_k=40)
		return response['choices'][0]['text']

# Test language generation works
if __name__ == "__main__":
	print("Test logprobs=True mode")
	model = LanguageModel(logprobs=True)
	model.language_model("Once upon a time in a land far far away")
	print("Test logprobs=False mode")
	model = LanguageModel(logprobs=False)
	model.language_model("Once upon a time in a land far far away")

