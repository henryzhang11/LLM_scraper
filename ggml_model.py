from llama_cpp import Llama

llm = Llama(
	model_path="models/gemma-2-9b-it/gemma-2-9b-it.ggmlv3.bin"
	n_ctx = 2048,
	n_threads=8,
	seed=42,
	f16_kv=False,
	logits_all=False,
	vocab_only=False,
	use_mlock=True,
	embedding=False,
)

def language_model(self, prompt: str) -> str:
  return llm(prompt, max_tokens=1000, temperature=0.5, top_k=40)