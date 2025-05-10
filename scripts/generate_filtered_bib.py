import argparse
import re
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bparser import BibTexParser
from pathlib import Path
import sys

# Регулярное выражение для поиска ключей цитирования Pandoc [@key]
# Оно ищет @, затем один или более символов, не являющихся пробелом, ], ; ,
CITATION_PATTERN = re.compile(r"@([^\s;,\]]+)")

def find_cited_keys(md_files):
    """
    Находит все уникальные ключи цитирования в списке Markdown файлов.
    """
    cited_keys = set()
    print(f"Searching for citation keys in: {md_files}") # Debug print
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Находим все совпадения с паттерном
                # findall вернет список строк, соответствующих группе захвата (то, что в скобках)
                keys_in_file = CITATION_PATTERN.findall(content)
                if keys_in_file: # Debug print
                    print(f"  Found keys in {md_file}: {len(keys_in_file)}")
                cited_keys.update(keys_in_file)
        except FileNotFoundError:
            print(f"Warning: Markdown file not found: {md_file}", file=sys.stderr)
        except Exception as e:
            print(f"Warning: Error reading file {md_file}: {e}", file=sys.stderr)

    print(f"Total unique keys found: {len(cited_keys)}") # Debug print
    # print(f"Keys: {sorted(list(cited_keys))}") # Uncomment for detailed debug
    return cited_keys

def filter_bib_database(common_bib_path, cited_keys):
    """
    Фильтрует базу данных BibTeX, оставляя только записи с ключами из cited_keys.
    """
    try:
        with open(common_bib_path, 'r', encoding='utf-8') as bibtex_file:
            # Используем common_strings=True для обработки @string
            parser = BibTexParser(common_strings=True)
            bib_database = bibtexparser.load(bibtex_file, parser=parser)
    except FileNotFoundError:
        print(f"Error: Common BibTeX file not found: {common_bib_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to parse common BibTeX file {common_bib_path}: {e}", file=sys.stderr)
        sys.exit(1)

    filtered_entries = []
    found_keys = set()

    for entry in bib_database.entries:
        if entry['ID'] in cited_keys:
            filtered_entries.append(entry)
            found_keys.add(entry['ID'])

    # Проверяем, все ли найденные ключи были в bib файле
    missing_keys = cited_keys - found_keys
    if missing_keys:
        print(f"Warning: The following cited keys were not found in {common_bib_path}:", file=sys.stderr)
        for key in sorted(list(missing_keys)):
            print(f"- {key}", file=sys.stderr)

    filtered_db = bibtexparser.bibdatabase.BibDatabase()
    filtered_db.entries = filtered_entries
    # Копируем preamble и strings из оригинальной базы, если они есть
    if hasattr(bib_database, 'preambles'):
         filtered_db.preambles = bib_database.preambles
    if hasattr(bib_database, 'strings'):
        filtered_db.strings = bib_database.strings


    return filtered_db

def main():
    parser = argparse.ArgumentParser(description='Filter a BibTeX file based on citations found in Markdown files.')
    parser.add_argument('--md-list', required=True, help='Path to a file containing a list of Markdown files (one per line).')
    parser.add_argument('--common-bib', required=True, help='Path to the common BibTeX file.')
    parser.add_argument('--output', required=True, help='Path to the output filtered BibTeX file.')

    args = parser.parse_args()

    # Читаем список MD файлов
    try:
        with open(args.md_list, 'r', encoding='utf-8') as f:
            md_files = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Markdown list file not found: {args.md_list}", file=sys.stderr)
        sys.exit(1)

    if not md_files:
        print(f"Warning: Markdown list file {args.md_list} is empty.", file=sys.stderr)
        # Создаем пустой выходной bib файл
        with open(args.output, 'w', encoding='utf-8') as out_file:
            out_file.write("")
        print(f"Created empty output file: {args.output}")
        sys.exit(0)


    # Находим все цитируемые ключи
    cited_keys = find_cited_keys(md_files)
    if not cited_keys:
         print(f"Warning: No citation keys found in the specified Markdown files.", file=sys.stderr)
         # Создаем пустой выходной bib файл
         with open(args.output, 'w', encoding='utf-8') as out_file:
             out_file.write("")
         print(f"Created empty output file: {args.output}")
         sys.exit(0)

    # Фильтруем базу данных BibTeX
    filtered_db = filter_bib_database(args.common_bib, cited_keys)

    # Записываем отфильтрованную базу данных
    try:
        # Убедимся, что директория для выходного файла существует
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        writer = BibTexWriter()
        # Настройки для более чистого вывода
        writer.indent = '    ' # 4 пробела для отступа
        writer.comma_first = False
        with open(args.output, 'w', encoding='utf-8') as out_file:
            out_file.write(writer.write(filtered_db))
        print(f"Successfully generated filtered BibTeX file: {args.output}")
        print(f"Included {len(filtered_db.entries)} entries.")

    except Exception as e:
        print(f"Error: Failed to write output BibTeX file {args.output}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()