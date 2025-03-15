import os
import tiktoken

# Load the tokenizer
enc = tiktoken.encoding_for_model("gpt-4")

# Process all files in the current directory
for filename in os.listdir():
    if os.path.isfile(filename):  # Ensure it's a file
        try:
            with open(filename, "r", encoding="utf-8") as file:
                text = file.read()
            num_tokens = len(enc.encode(text))
            print(f"{filename}: Token count = {num_tokens}")
        except Exception as e:
            print(f"Skipping {filename}: {e}")

