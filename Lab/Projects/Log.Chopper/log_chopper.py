import os

def estimate_token_count(text):
    return len(text.split())

def split_into_turns(text):
    # Splits by speaker tags
    import re
    pattern = r"(Architect said:|ChatGPT said:)"
    parts = re.split(pattern, text)
    
    turns = []
    for i in range(1, len(parts), 2):
        speaker = parts[i].strip()
        message = parts[i+1].strip()
        full = f"{speaker} {message}"
        turns.append(full)
    return turns

def chunk_turns(turns, max_tokens=3000, overlap=1):
    chunks = []
    current = []
    token_count = 0

    for i, turn in enumerate(turns):
        turn_tokens = estimate_token_count(turn)
        if token_count + turn_tokens > max_tokens and current:
            chunks.append(current)
            current = current[-overlap:]  # retain overlap
            token_count = sum(estimate_token_count(t) for t in current)
        current.append(turn)
        token_count += turn_tokens

    if current:
        chunks.append(current)

    return chunks

def extract_toc(turns):
    toc = []
    for i, turn in enumerate(turns):
        first_line = turn.strip().splitlines()[0]
        toc.append(f"{i+1:04d}: {first_line[:120]}")
    return toc

def process_chat_file(input_file, output_dir="chunks"):
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    turns = split_into_turns(text)
    chunks = chunk_turns(turns)
    toc = extract_toc(turns)

    os.makedirs(output_dir, exist_ok=True)

    for idx, chunk in enumerate(chunks):
        chunk_text = "\n\n".join(chunk)
        with open(f"{output_dir}/chunk_{idx+1:03d}.txt", "w", encoding="utf-8") as f:
            f.write(chunk_text)

    with open("toc.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(toc))

    print(f"Done: {len(chunks)} chunks saved, TOC created.")

# Запуск
process_chat_file("to_chop.txt")

