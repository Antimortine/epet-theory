import re
import os
import glob
from pathlib import Path # Используем pathlib для удобной работы с путями

# --- Определяем базовую директорию проекта ---
# Путь к директории, где лежит сам скрипт
SCRIPT_DIR = Path(__file__).parent.resolve()
# Путь к корневой директории проекта (на один уровень выше scripts)
PROJECT_ROOT = SCRIPT_DIR.parent

# --- Конфигурация (пути относительно PROJECT_ROOT) ---
MANUSCRIPT_DIR = PROJECT_ROOT / 'manuscript'
BIB_FILE = PROJECT_ROOT / 'output' / 'references_for_submission.bib'
INPUT_LIST_FILE = MANUSCRIPT_DIR / 'input_files.txt' # Используем input_files.txt как основной источник

print(f"Project Root: {PROJECT_ROOT}")
print(f"Manuscript Dir: {MANUSCRIPT_DIR}")
print(f"Bib File: {BIB_FILE}")
print(f"Input List File: {INPUT_LIST_FILE}")

# --- Шаг 1: Получить список .md файлов из input_files.txt ---
md_files_paths = []
if INPUT_LIST_FILE.exists():
    try:
        with open(INPUT_LIST_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                stripped_line = line.strip()
                if stripped_line and stripped_line.endswith('.md'):
                    # Создаем абсолютный путь к файлу
                    md_path = PROJECT_ROOT / stripped_line
                    if md_path.exists():
                        md_files_paths.append(md_path)
                    else:
                         print(f"Warning: File listed in {INPUT_LIST_FILE} not found: {md_path}", file=sys.stderr)
    except Exception as e:
        print(f"Error: Could not read {INPUT_LIST_FILE}: {e}", file=sys.stderr)
        exit()
else:
    print(f"Error: Input list file not found: {INPUT_LIST_FILE}", file=sys.stderr)
    exit()

if not md_files_paths:
    print("Error: No valid Markdown files found from the input list.", file=sys.stderr)
    exit()

print(f"\nProcessing {len(md_files_paths)} MD files listed in {INPUT_LIST_FILE.name}:")
# for p in md_files_paths: print(f"  {p}") # Раскомментировать для отладки

# --- Шаг 2: Извлечь ключи цитирования из .md файлов ---
cited_keys = set()
# Регулярное выражение (исправленное)
citation_pattern = re.compile(r'@([^\s;,\]]+)')

for md_file_path in md_files_paths:
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = citation_pattern.findall(content)
            # Очистка ключей (на всякий случай, хотя регулярка должна быть точнее)
            cleaned_keys_in_file = set(key.split(',')[0].split(';')[0].split(']')[0].split(')')[0] for key in matches if key)
            if cleaned_keys_in_file:
                 # print(f"  Found keys in {md_file_path.name}: {cleaned_keys_in_file}") # Отладка
                 cited_keys.update(cleaned_keys_in_file)
    except Exception as e:
        print(f"Error reading {md_file_path}: {e}")


print(f"\nFound {len(cited_keys)} unique cited keys in MD files.")
# print(f"Cited keys: {sorted(list(cited_keys))}") # Отладка

# --- Шаг 3: Извлечь ключи записей из .bib файла ---
bib_keys = set()
bib_entry_pattern = re.compile(r'^\s*@\w+\s*\{\s*([^,\s]+)\s*,', re.MULTILINE)

try:
    with open(BIB_FILE, 'r', encoding='utf-8') as f:
        bib_content = f.read()
        matches = bib_entry_pattern.findall(bib_content)
        bib_keys = set(matches)
except FileNotFoundError:
    print(f"Error: BIB file not found at {BIB_FILE}", file=sys.stderr)
    exit()
except Exception as e:
    print(f"Error reading {BIB_FILE}: {e}", file=sys.stderr)
    exit()

print(f"\nFound {len(bib_keys)} keys in BIB file.")
# print(f"Bib keys: {sorted(list(bib_keys))}") # Отладка

# --- Шаг 4: Найти лишние ключи ---
unused_keys = bib_keys - cited_keys

# --- Шаг 5: Вывести результат ---
if unused_keys:
    print(f"\n--- Found {len(unused_keys)} Unused Keys in {BIB_FILE.name} ---")
    for key in sorted(list(unused_keys)):
        print(key)
else:
    print(f"\n--- All keys in {BIB_FILE.name} seem to be cited in the MD files listed in {INPUT_LIST_FILE.name}. ---")

# --- Шаг 6: Найти недостающие ключи (опционально, но полезно) ---
missing_keys = cited_keys - bib_keys
if missing_keys:
    print(f"\n--- Found {len(missing_keys)} Cited Keys MISSING in {BIB_FILE.name} ---")
    for key in sorted(list(missing_keys)):
        print(key)