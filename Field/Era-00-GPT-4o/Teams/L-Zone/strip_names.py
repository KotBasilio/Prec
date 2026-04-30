import re
import sys

# Словарь соответствия имен → ников
NAME_MAP = {
    "Valeria Khliustova": "Lady",
    "Serge Mironov": "Archy",
}

def process_chat_log(chat_text: str) -> str:
    lines = chat_text.strip().splitlines()
    result = []
    current_author = None
    current_lines = []

    for line in lines:
        # убираем таймстемп в []
        match = re.match(r"\[.*?\]\s*(.*?):\s*(.*)", line)
        if match:
            # заменяем имя на ник
            author, text = match.groups()
            nick = NAME_MAP.get(author, author)

            # если автор тот же, продолжаем блок
            if nick == current_author:
                current_lines.append(text)
            else:
                # сохраняем предыдущий блок
                if current_author is not None:
                    result.append(f"**{current_author}**: " + "\n".join(current_lines))
                # начинаем новый блок
                current_author = nick
                current_lines = [text]
        else:
            # строка без таймстемпа → продолжаем текущего автора
            if current_author is not None:
                current_lines.append(line.strip())

    # финальный блок
    if current_author is not None:
        result.append(f"**{current_author}**: " + "\n".join(current_lines))

    return "\n".join(result)


def main():
    if len(sys.argv) < 2:
        print("Usage: python strip.py input_file.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = "output.txt"

    # читаем входной файл
    with open(input_file, "r", encoding="utf-8") as f:
        chat_text = f.read()

    # обрабатываем
    processed = process_chat_log(chat_text)

    # пишем результат
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(processed)

    print(f"Processed chat written to {output_file}")


if __name__ == "__main__":
    main()
