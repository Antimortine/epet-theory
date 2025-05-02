# --- Переменные ---

# Имя основного выходного PDF файла
OUTPUT_PDF = output/EPET_Theory.pdf
ANONYMOUS_PDF_OUTPUT = output/EPET_Manuscript_Anonymous.pdf

# Исходные Markdown файлы (читаем из файла)
# Используем find для поиска md файлов в директории manuscript,
# затем sort для предсказуемого порядка (хотя input_files.txt надежнее)
# Или используем input_files.txt напрямую
# MD_FILES = $(shell find manuscript -name '*.md' | sort)
MD_FILES_LIST = manuscript/input_files.txt
MD_FILES = $(shell cat $(MD_FILES_LIST)) # Читаем порядок из файла

# Файл метаданных
METADATA = assets/metadata.yaml
ANONYMOUS_METADATA = assets/metadata_anonymous.yaml

# Файл библиографии
BIB_FILE = assets/references.bib

CSL_FILE = assets/csl/chicago-author-date.csl

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
$(OUTPUT_PDF): $(MD_FILES_LIST) $(METADATA) $(BIB_FILE) $(CSL_FILE) Makefile $(shell find manuscript -name '*.md')
	@echo ">>> Собираем PDF файл: $(OUTPUT_PDF) ..."
	@mkdir -p output # Создаем директорию output, если ее нет
	$(PANDOC) $(PANDOC_OPTIONS) $(MD_FILES) -o $@
	@echo ">>> Сборка PDF завершена."

# Новая цель для сборки анонимного PDF для журнала
submission_pdf: $(MD_FILES_LIST) $(ANONYMOUS_METADATA) Makefile $(shell find manuscript -name '*.md')
	@echo ">>> Собираем АНОНИМНЫЙ PDF для журнала: $(ANONYMOUS_PDF_OUTPUT) ..."
	@mkdir -p output
	$(PANDOC) \
		--metadata-file=$(ANONYMOUS_METADATA) \
		--standalone \
		--pdf-engine=$(PDF_ENGINE) \
		--toc \
		-V bibliography=false \
		$(MD_FILES) -o $(ANONYMOUS_PDF_OUTPUT)
	@echo ">>> Сборка АНОНИМНОГО PDF завершена."

# Цель для очистки сгенерированных файлов
clean:
	@echo ">>> Очистка директории output..."
	@rm -rf output/*
	@echo ">>> Очистка завершена."

# Фиктивные цели (чтобы make не путал их с файлами)
.PHONY: all clean submission_pdf