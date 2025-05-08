import argparse
from pathlib import Path
import sys

# Разделитель между файлами
FILE_SEPARATOR = "\n\n---\n\n" # Используем горизонтальную линию Markdown

def concatenate_files(input_list_path, output_md_path, project_root):
    """
    Объединяет содержимое Markdown файлов из списка в один выходной файл.
    """
    output_content = []
    files_processed = 0

    # Читаем список MD файлов
    try:
        with open(input_list_path, 'r', encoding='utf-8') as f:
            md_files_relative = [line.strip() for line in f if line.strip() and line.strip().endswith('.md')]
    except FileNotFoundError:
        print(f"Error: Input list file not found: {input_list_path}", file=sys.stderr)
        return False

    if not md_files_relative:
        print(f"Error: No Markdown files found in list: {input_list_path}", file=sys.stderr)
        return False

    print(f"Concatenating files listed in {input_list_path.name} into {output_md_path.name}...")

    for i, rel_path in enumerate(md_files_relative):
        md_path = project_root / rel_path
        if md_path.exists():
            try:
                with open(md_path, 'r', encoding='utf-8') as infile:
                    print(f"  Adding: {rel_path}")
                    # Добавляем разделитель перед каждым файлом, кроме первого
                    if i > 0:
                        output_content.append(FILE_SEPARATOR)
                    # Добавляем комментарий с именем файла (опционально, но полезно для отладки)
                    # output_content.append(f"<!-- START OF FILE {rel_path} -->\n")
                    output_content.append(infile.read())
                    # output_content.append(f"\n<!-- END OF FILE {rel_path} -->")
                    files_processed += 1
            except Exception as e:
                print(f"Warning: Could not read file {md_path}: {e}", file=sys.stderr)
        else:
            print(f"Warning: File listed in {input_list_path.name} not found: {md_path}", file=sys.stderr)

    # Записываем объединенный контент
    try:
        # Убедимся, что директория для выходного файла существует
        output_md_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_md_path, 'w', encoding='utf-8') as outfile:
            outfile.write("\n".join(output_content))
        print(f"Successfully created concatenated file: {output_md_path}")
        print(f"Processed {files_processed} files.")
        return True
    except Exception as e:
        print(f"Error: Failed to write output file {output_md_path}: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description='Concatenate Markdown files listed in input files.')
    # Определяем пути относительно текущей директории (где запускается скрипт)
    # Предполагаем запуск из корня проекта
    current_dir = Path.cwd()
    default_output_dir = current_dir / 'output'

    parser.add_argument('--main-list', default='manuscript/input_files.txt',
                        help='Path to the list file for the main manuscript.')
    parser.add_argument('--sm-list', default='manuscript/Supplementary_Materials/input_files_sm.txt',
                        help='Path to the list file for the supplementary materials.')
    parser.add_argument('--main-output', default=str(default_output_dir / 'EPET_Main_Manuscript_CONCATENATED.md'),
                        help='Output file path for the concatenated main manuscript.')
    parser.add_argument('--sm-output', default=str(default_output_dir / 'EPET_Supplementary_Materials_CONCATENATED.md'),
                        help='Output file path for the concatenated supplementary materials.')

    args = parser.parse_args()

    project_root = current_dir # Так как запускаем из корня

    print("--- Concatenating Main Manuscript ---")
    main_list_path = project_root / args.main_list
    main_output_path = Path(args.main_output)
    concatenate_files(main_list_path, main_output_path, project_root)

    print("\n--- Concatenating Supplementary Materials ---")
    sm_list_path = project_root / args.sm_list
    sm_output_path = Path(args.sm_output)
    concatenate_files(sm_list_path, sm_output_path, project_root)

if __name__ == '__main__':
    main()