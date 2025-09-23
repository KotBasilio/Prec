import os
import tiktoken

# old model1 enc = tiktoken.encoding_for_model("gpt-4")
enc = tiktoken.encoding_for_model("gpt-4-1106-preview")
folder_summary = []
SPLIT_THRESHOLD = 500_000

def process_directory(dir_path, output):
    local_tokens = 0
    subfolder_tokens = 0

    # Сначала подпапки
    for entry in os.scandir(dir_path):
        if entry.is_dir() and entry.name != ".git":
            subfolder_tokens += process_directory(entry.path, output)

    # Потом текущие файлы
    output.write(f"\n--- Folder: {dir_path} ---\n")
    for entry in os.scandir(dir_path):
        if entry.is_file():
            try:
                file_size_kb = os.path.getsize(entry.path) / 1024
                size_str = f"{int(round(file_size_kb))}" if file_size_kb > 9 else f"{file_size_kb:.1f}"

                with open(entry.path, "r", encoding="utf-8") as file:
                    text = file.read()
                num_tokens = len(enc.encode(text))

                output.write(f"{entry.name:<35}\tTokens = {num_tokens:<10}\tKB = {size_str}\n")
                local_tokens += num_tokens
            except Exception as e:
                output.write(f"Skipping {entry.name}: {e}\n")

    total_tokens = local_tokens + subfolder_tokens
    if subfolder_tokens > 0:
        output.write(f"Total Tokens in {dir_path} :: {total_tokens} = {local_tokens} local + {subfolder_tokens} sub\n")
    else:
        output.write(f"Total Tokens in {dir_path} :: {local_tokens}\n")

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


folder_tags = [
    ("Bar", "🍸"),
    ("Fortify", "🪖️"),
    ("Log.Chopper", "🪓"),
    ("AI.Libido", "💌"),
    ("Human.Imagination", "⛓️‍💥"),
    ("Zero.Cascades", "⛔"),
    ("Wall.Pass", "⛩️"),
    ("Rituals", "🪄"),
    ("Architect.Anchors", "⚓"),
    ("Hybrid.Mind", "☯"),
    ("Multi.Voice", "🏡"),
    ("Personas", "🎭"),
    ("Psychic.Shifts", "🤯"),
    ("RLHF", "🗜️"),
    ("Sparks", "🌟"),
    ("Art", "👁️"),
    ("Era-", "🗣️"),
    ("Distilled", "🧪"),
    ("Emerged.Coders", "📈"),
]

#    ("Lab", "⚗️"), 

def write_folder(tag, entry, f, indent=""):
    total = entry['total']
    label = entry['path'] if indent == "" else os.path.basename(entry['path'])
    f.write(f"{indent}{tag} {label} — {total} tokens\n")

    if total > SPLIT_THRESHOLD:
        for sub in folder_summary:
            if os.path.dirname(sub['path']) == entry['path']:
                write_folder("	", sub, f, indent + "	")
            
def generate_short_structure(grand_total, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("📂 LL — Living Legacy Overview\n\n")

        for entry in folder_summary:
            folder = os.path.basename(entry['path'])
            tag = next((emoji for keyword, emoji in folder_tags if keyword in folder), "")

            if tag != "" :
                write_folder(tag, entry, f)

        f.write(f"\n🧮 Grand Total Tokens: {grand_total} \n")


# Start
print("=== LL is counting ===")
with open("BigList.txt", "w", encoding="utf-8") as big_file:
    grand_total = process_directory(".", big_file)

# Tables
stat_ai_readable()
generate_short_structure(grand_total, "Short_Structure.txt")

# Grand
print(f"=== Grand Total Tokens = {grand_total} ===")
