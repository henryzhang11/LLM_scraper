# Scraper & Quantized Model Repository

Welcome to the **Scraper & Quantized Model** repository! This project integrates a Python-based web scraping automation tool (`scraper.py`) with a **quantized language model** (`quantized_model.py`) for efficient script generation and evaluation.

## Features

- **Automated Script Generation & Execution** 
  The `Scraper` class iteratively refines Python scripts using a language model.
  
- **Quantized Language Model** 
  Uses `Llama` with a pre-trained **Gemma-2-9B-IT** model to generate scripts and provide critiques.

- **Error Handling & Iterative Refinement** 
  Scripts are evaluated for correctness and revised until they meet the job description.

---

## Installation

### 1. Clone the Repository  
```bash
git clone https://github.com/henryzhang11/LLM_scraper/
cd your-repo
```

### 2. Create a Virtual Environment  
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies  
```bash
pip install -r requirements.txt
```
---

## Usage

### Running the Scraper
```python
from scraper import Scraper
from quantized_model import QuantizedModel

# Initialize the model
model = QuantizedModel()

# Define a job description
job_description = "Extract all hyperlinks from ."

# Generate a script dynamically
script = Scraper.generate(model.language_model, job_description)

# Output the final script
print("Generated Script:\n", script)
```

### Using the Quantized Model Directly
```python
from quantized_model import QuantizedModel

# Load the model
model = QuantizedModel(logprobs=True)

# Generate text from a prompt
response = model.language_model("Write a Python script to scrape titles from a webpage.")
print(response)
```

---

## Project Structure

```
LLM_scraper/
│── scraper.py        # Main Scraper class with iterative script refinement
│── quantized_model.py # Quantized Llama model with Gemma-2-9B-IT
│── requirements.txt   # Python dependencies
│── README.md          # Project documentation
```

---

## License

This project is licensed under the **MIT License**.