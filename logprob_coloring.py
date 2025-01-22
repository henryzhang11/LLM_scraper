# %%
from rich import print

# log 0.2, log 0.4, ..., log 1
bounds = [-float('-inf'), -0.69897, -0.39794, -0.221848749, -0.09691, 0]

def color_with_log_probs(top_logprobs):
	result = ""
	for top_logprob in top_logprobs:
		result += color_with_log_prob(top_logprob)
	print(result)

def color_with_log_prob(top_logprob):
	token, logprob = next(iter(top_logprob.items()))
	g = 120
	for i in range(len(bounds) - 1):
		if bounds[i] < logprob and logprob <= bounds[i + 1]:
			g = 160 + i * 20
	color = f"#{0:02x}{g:02x}{0:02x}"
	return f"[{color}]{token}[/{color}]"
