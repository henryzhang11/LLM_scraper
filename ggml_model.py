from llama_cpp import Llama

model = Llama(
	model_path="google/gemma-2-9b-it", n_ctx = 1024, 
  n_threads=2, seed=42, f16_kv=True, logits_all=False, 
  vocab_only=False, use_mlock=True, embedding=False
)

def language_model(prompt: str) -> str:
  return model(prompt, max_tokens=1000, temperature=0.5, top_k=40)