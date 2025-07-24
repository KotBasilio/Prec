import os
import tiktoken

# old model enc = tiktoken.encoding_for_model("gpt-4")
enc = tiktoken.encoding_for_model("gpt-4-1106-preview")
folder_summary = []

def process_directory(dir_path):
    local_tokens = 0
    subfolder_tokens = 0

    # Сначала подпапки
    for entry in os.scandir(dir_path):
        if entry.is_dir() and entry.name != ".git":
            subfolder_tokens += process_directory(entry.path)

    # Потом текущие файлы
    print(f"\n--- Folder: {dir_path} ---")
    for entry in os.scandir(dir_path):
        if entry.is_file():
            try:
                file_size_kb = os.path.getsize(entry.path) / 1024
                size_str = f"{int(round(file_size_kb))}" if file_size_kb > 9 else f"{file_size_kb:.1f}"

                with open(entry.path, "r", encoding="utf-8") as file:
                    text = file.read()
                num_tokens = len(enc.encode(text))

                print(f"{entry.name:<35}\tTokens = {num_tokens:<10}\tKB = {size_str}")
                local_tokens += num_tokens
            except Exception as e:
                print(f"Skipping {entry.name}: {e}")

    total_tokens = local_tokens + subfolder_tokens
    if subfolder_tokens > 0:
        print(f"Total Tokens in {dir_path} :: {total_tokens} = {local_tokens} local + {subfolder_tokens} sub")
    else:
        print(f"Total Tokens in {dir_path} :: {local_tokens}")

    # Добавим в сводную таблицу
    folder_summary.append({
        "path": dir_path,
        "total": total_tokens,
        "local": local_tokens,
        "sub": subfolder_tokens
    })

    return total_tokens

def stat_ai_readable():
    # AI-readable (CSV-like)
    csv_path = "LL_Summary.csv"
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("FolderPath,TotalTokens,LocalTokens,SubfolderTokens\n")
        for entry in folder_summary:
            f.write(f"{entry['path']},{entry['total']},{entry['local']},{entry['sub']}\n")
    #print(f"--- AI-readable summary saved to: {csv_path} ---")

def stat_human_readable():
    print("\n--- Folder Summary ---")
    for entry in folder_summary:
        if entry["sub"] > 0:
            print(f"{entry['path']} => {entry['total']} tokens = {entry['local']} local + {entry['sub']} sub")
        else:
            print(f"{entry['path']} => {entry['local']} tokens")

# Запуск
grand_total = process_directory(".")

# Tables
stat_ai_readable()
#stat_human_readable()

# Grand
print(f"\n=== Grand Total Tokens = {grand_total} ===")
