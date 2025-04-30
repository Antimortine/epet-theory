import re
import os
import glob

# --- Конфигурация ---
MANUSCRIPT_DIR = 'manuscript' # Директория с .md файлами
BIB_FILE = 'assets/references.bib' # Путь к .bib файлу

# --- Шаг 1: Найти все .md файлы ---
md_files = glob.glob(os.path.join(MANUSCRIPT_DIR, '*.md'))
# Добавим input_files.txt, если он содержит пути к файлам
input_list_file = os.path.join(MANUSCRIPT_DIR, 'input_files.txt')
if os.path.exists(input_list_file):
     try:
         with open(input_list_file, 'r', encoding='utf-8') as f:
             # Используем set для автоматического удаления дубликатов и объединения
             md_files = set(md_files) | set(line.strip() for line in f if line.strip().endswith('.md'))
     except Exception as e:
         print(f"Warning: Could not read {input_list_file}: {e}")


print(f"Found MD files: {md_files}")

# --- Шаг 2: Извлечь ключи цитирования из .md файлов ---
cited_keys = set()
# Регулярное выражение для поиска ключей в разных форматах Pandoc-цитат
# @key, [@key], [-@key, ...], [@key; @key2], [@key, text]
# Оно может быть не идеальным, но должно покрыть большинство случаев
citation_pattern = re.compile(r'@([a-zA-Z0-9_.-]+)') # Ищет @ и последующие символы ключа

for md_file_path in md_files:
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Находим все совпадения
            matches = citation_pattern.findall(content)
            for key in matches:
                 # Добавляем ключ в множество (дубликаты игнорируются)
                 # Иногда ключ может захватить лишнее (запятую, скобку), можно добавить очистку
                 cleaned_key = key.split(',')[0].split(';')[0].split(']')[0].split(')')[0]
                 if cleaned_key: # Убедимся что ключ не пустой
                      cited_keys.add(cleaned_key)
    except Exception as e:
        print(f"Error reading {md_file_path}: {e}")


print(f"\nFound {len(cited_keys)} unique cited keys in MD files.")
# print(sorted(list(cited_keys))) # Раскомментировать для вывода всех найденных ключей

# --- Шаг 3: Извлечь ключи записей из .bib файла ---
bib_keys = set()
# Регулярное выражение для поиска ключей в начале BibTeX записей
# @type{key,
bib_entry_pattern = re.compile(r'^\s*@\w+\s*\{\s*([^,\s]+)\s*,', re.MULTILINE)

try:
    with open(BIB_FILE, 'r', encoding='utf-8') as f:
        bib_content = f.read()
        matches = bib_entry_pattern.findall(bib_content)
        bib_keys = set(matches)
except FileNotFoundError:
    print(f"Error: BIB file not found at {BIB_FILE}")
    exit()
except Exception as e:
    print(f"Error reading {BIB_FILE}: {e}")
    exit()

print(f"\nFound {len(bib_keys)} keys in BIB file.")
# print(sorted(list(bib_keys))) # Раскомментировать для вывода всех ключей из .bib

# --- Шаг 4: Найти лишние ключи ---
unused_keys = bib_keys - cited_keys

# --- Шаг 5: Вывести результат ---
if unused_keys:
    print(f"\n--- Found {len(unused_keys)} Unused Keys in {BIB_FILE} ---")
    for key in sorted(list(unused_keys)):
        print(key)
else:
    print(f"\n--- All keys in {BIB_FILE} seem to be cited in the MD files. ---")