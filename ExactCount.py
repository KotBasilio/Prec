import os
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4")

tree_total_tokens = 0

def process_directory(dir_path):
    global tree_total_tokens
    dir_total_tokens = 0
    print(f"\n--- Folder: {dir_path} ---")

    for root, dirs, files in os.walk(dir_path):
        # Remove .git from subdirectory list to prevent descending into it
        if ".git" in dirs:
            dirs.remove(".git")

        if root != dir_path:
            continue  # Skip nested folders until recursion

        for filename in files:
            full_path = os.path.join(root, filename)
            if os.path.isfile(full_path):
                try:
                    file_size_kb = os.path.getsize(full_path) / 1024
                    if file_size_kb > 9:
                        size_str = f"{int(round(file_size_kb))}"
                    else:
                        size_str = f"{file_size_kb:.1f}"

                    with open(full_path, "r", encoding="utf-8") as file:
                        text = file.read()
                    num_tokens = len(enc.encode(text))
                    
                    print(f"{filename:<35}\tTokens = {num_tokens:<10}\tKB = {size_str}")
                    dir_total_tokens += num_tokens
                except Exception as e:
                    print(f"Skipping {filename}: {e}")

    print(f"Total Tokens in {dir_path} = {dir_total_tokens}")
    tree_total_tokens += dir_total_tokens

    # Recurse into subdirectories (except .git, already removed)
    for entry in os.scandir(dir_path):
        if entry.is_dir() and entry.name != ".git":
            process_directory(entry.path)

# Start from current directory
process_directory(".")

print(f"\n=== Grand Total Tokens = {tree_total_tokens} ===")
