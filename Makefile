# --- Переменные ---

# Имя основного выходного PDF файла
OUTPUT_PDF = output/EPET_Theory.pdf

# Исходные Markdown файлы (читаем из файла)
# Используем find для поиска md файлов в директории manuscript,
# затем sort для предсказуемого порядка (хотя input_files.txt надежнее)
# Или используем input_files.txt напрямую
# MD_FILES = $(shell find manuscript -name '*.md' | sort)
MD_FILES_LIST = manuscript/input_files.txt
MD_FILES = $(shell cat $(MD_FILES_LIST)) # Читаем порядок из файла

# Файл метаданных
METADATA = assets/metadata.yaml

# Файл библиографии
BIB_FILE = assets/references.bib

# (Опционально) Файл шаблона LaTeX
# LATEX_TEMPLATE = assets/templates/default.latex

# Движок LaTeX (xelatex рекомендуется для Unicode/русского)
PDF_ENGINE = xelatex

# Команда Pandoc
PANDOC = pandoc

# Опции Pandoc
PANDOC_OPTIONS = \
	--metadata-file=$(METADATA) \
	--citeproc \
	--standalone \
	--pdf-engine=$(PDF_ENGINE) \
	--toc # Включить оглавление (можно также управлять из metadata.yaml)
	# --template=$(LATEX_TEMPLATE) # Раскомментировать, если используется кастомный шаблон
	# --highlight-style=pygments # (Опционально) Стиль подсветки кода, если есть блоки кода

# --- Цели ---

# Цель по умолчанию: собрать PDF
all: $(OUTPUT_PDF)

# Правило для сборки PDF
# Зависит от всех .md файлов, файла метаданных, файла библиографии и самого Makefile
$(OUTPUT_PDF): $(MD_FILES_LIST) $(METADATA) $(BIB_FILE) Makefile $(shell find manuscript -name '*.md')
	@echo ">>> Собираем PDF файл: $(OUTPUT_PDF) ..."
	@mkdir -p output # Создаем директорию output, если ее нет
	$(PANDOC) $(PANDOC_OPTIONS) $(MD_FILES) -o $@
	@echo ">>> Сборка PDF завершена."

# Цель для очистки сгенерированных файлов
clean:
	@echo ">>> Очистка директории output..."
	@rm -rf output/*
	@echo ">>> Очистка завершена."

# Фиктивные цели (чтобы make не путал их с файлами)
.PHONY: all clean