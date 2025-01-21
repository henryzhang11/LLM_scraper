# %%
from rich import print
r, b = 0, 0
for g in range(120, 220, 20):
    color = f"#{r:02x}{g:02x}{b:02x}"
    word = "word"
    print(f"[{color}]{word}[/{color}]")
