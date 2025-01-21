from llama_cpp import Llama

model = Llama.from_pretrained(
    repo_id="bartowski/gemma-2-9b-it-GGUF", 
    filename="gemma-2-9b-it-IQ2_M.gguf",
    n_ctx = 1024, 
    n_threads=2, 
    seed=42 
)

def language_model(prompt: str) -> str:
    response = model(prompt, max_tokens=1000, temperature=0.5, top_k=40)
    response_text = response['choices'][0]['text']
    return response_text