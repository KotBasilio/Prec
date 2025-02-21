import tiktoken

# Load the tokenizer
enc = tiktoken.encoding_for_model("gpt-4")

# Read your file
with open("Octopus2.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Count tokens
num_tokens = len(enc.encode(text))
print(f"Token count: {num_tokens}")
