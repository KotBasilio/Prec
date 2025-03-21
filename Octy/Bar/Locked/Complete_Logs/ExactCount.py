import os
import tiktoken

# Load the tokenizer
enc = tiktoken.encoding_for_model("gpt-4")

# tokens in dir
total_tokens = 0

# Process all files in the current directory
for filename in os.listdir():
    if os.path.isfile(filename):  # Ensure it's a file
        try:
            file_size_kb = os.path.getsize(filename) / 1024  # File size in KB
            if file_size_kb > 9:
                file_size_kb = round(file_size_kb)
                size_str = f"{int(file_size_kb)}"
            else:
                size_str = f"{file_size_kb:.1f}"                
                
            with open(filename, "r", encoding="utf-8") as file:
                text = file.read()
            num_tokens = len(enc.encode(text))  # Token count
            
            print(f"{filename:<35}\tTokens = {num_tokens:<10}\tSize(KB) = {size_str}")
            total_tokens += num_tokens
        except Exception as e:
            print(f"Skipping {filename}: {e}")

# out
print(f"\nTotal Tokens = {total_tokens}")

