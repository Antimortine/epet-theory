# === Переменные ===

# --- Имена файлов ---
OUTPUT_PDF = output/EPET_Theory_1.5.pdf
ANONYMOUS_PDF_OUTPUT = output/EPET_Manuscript_Anonymous_1.5.pdf
SM_PDF_OUTPUT = output/EPET_Supplementary_Materials_1.5.pdf

# --- Исходные Markdown файлы ---
MD_FILES_LIST_ANON = manuscript/input_files.txt # Список для анонимной версии и подсчета слов
MD_FILES_ANON = $(shell cat $(MD_FILES_LIST_ANON))
MD_FILES_LIST_FULL = manuscript/input_files_full.txt # Список для полной версии (с заголовком References)
MD_FILES_FULL = $(shell cat $(MD_FILES_LIST_FULL))
SM_MD_FILES_LIST = manuscript/Supplementary_Materials/input_files_sm.txt
SM_MD_FILES = $(shell cat $(SM_MD_FILES_LIST))
WORD_COUNT_FILE = output/word_count_header.md # Временный файл со счетчиком

# --- Метаданные ---
METADATA = assets/metadata.yaml
ANONYMOUS_METADATA = assets/metadata_anonymous.yaml
SM_METADATA = assets/metadata_sm.yaml

# --- Библиография ---
SUBMISSION_BIB_DEPENDS_ON = $(MD_FILES_LIST_ANON) $(shell cat $(MD_FILES_LIST_ANON))
COMMON_BIB = assets/references_common.bib
SUBMISSION_BIB = output/references_for_submission.bib
SM_BIB = output/references_for_sm.bib
CSL_FILE = assets/csl/chicago-note-bibliography-with-ibid.csl

# --- Скрипт генерации Bib ---
PYTHON = python3
BIB_SCRIPT = scripts/generate_filtered_bib.py

# --- Прочее ---
PDF_ENGINE = xelatex
PANDOC = pandoc

# === Зависимости Файлов ===
# Список всех MD файлов основного текста
ALL_MD_FILES_ANON = $(shell cat $(MD_FILES_LIST_ANON)) # Основные файлы MD
ALL_MD_FILES_FULL = $(shell cat $(MD_FILES_LIST_FULL)) # Основные + заголовок References
# Список всех MD файлов SM
ALL_SM_MD_FILES = $(shell find manuscript/Supplementary_Materials -name '*.md')

# === Цели ===

# Цель по умолчанию: собрать все 3 PDF
all: $(OUTPUT_PDF) $(ANONYMOUS_PDF_OUTPUT) $(SM_PDF_OUTPUT)

# --- Генерация отфильтрованных Bib файлов ---

# Генерация bib для основного текста
$(SUBMISSION_BIB): $(BIB_SCRIPT) $(COMMON_BIB) $(MD_FILES_LIST_ANON) $(ALL_MD_FILES_ANON) Makefile
	@echo ">>> Generating submission bib file: $(SUBMISSION_BIB)"
	@mkdir -p output
	$(PYTHON) $(BIB_SCRIPT) --md-list $(MD_FILES_LIST_ANON) --common-bib $(COMMON_BIB) --output $(SUBMISSION_BIB)

# Генерация bib для SM
$(SM_BIB): $(BIB_SCRIPT) $(COMMON_BIB) $(SM_MD_FILES_LIST) $(ALL_SM_MD_FILES) Makefile
	@echo ">>> Generating SM bib file: $(SM_BIB)"
	@mkdir -p output
	$(PYTHON) $(BIB_SCRIPT) --md-list $(SM_MD_FILES_LIST) --common-bib $(COMMON_BIB) --output $(SM_BIB)

# --- Генерация файла со счетчиком слов ---
$(WORD_COUNT_FILE): $(MD_FILES_LIST_ANON) $(ALL_MD_FILES_ANON) Makefile
	@echo ">>> Calculating word count..."
	@mkdir -p output
	@WORD_COUNT=$$( $(PANDOC) \
		--metadata-file=$(ANONYMOUS_METADATA) \
		-V bibliography=false \
		$(MD_FILES_ANON) --to=plain | wc -w ); \
	echo "Word Count (excluding bibliography): $$WORD_COUNT" > $(WORD_COUNT_FILE)
	@echo ">>> Word count file generated: $(WORD_COUNT_FILE)"

# --- Сборка PDF файлов ---

# 1. Полный PDF (использует MD_FILES_FULL и SUBMISSION_BIB)
$(OUTPUT_PDF): $(MD_FILES_LIST_FULL) $(METADATA) $(SUBMISSION_BIB) $(CSL_FILE) Makefile $(ALL_MD_FILES_FULL)
	@echo ">>> Building FULL PDF: $(OUTPUT_PDF)..."
	@mkdir -p output
	$(PANDOC) \
		--metadata-file=$(METADATA) \
		--bibliography=$(SUBMISSION_BIB) \
		--citeproc \
		--standalone \
		--pdf-engine=$(PDF_ENGINE) \
		--toc \
		$(MD_FILES_FULL) -o $@
	@echo ">>> Building FULL PDF finished."

# 2. Анонимный PDF
$(ANONYMOUS_PDF_OUTPUT): $(MD_FILES_LIST_FULL) $(ANONYMOUS_METADATA) $(SUBMISSION_BIB) $(CSL_FILE) Makefile $(ALL_MD_FILES_FULL)
	@echo ">>> Building ANONYMOUS PDF for submission: $(ANONYMOUS_PDF_OUTPUT)..."
	@mkdir -p output
	$(PANDOC) \
		--metadata-file=$(ANONYMOUS_METADATA) \
		--bibliography=$(SUBMISSION_BIB) \
		--citeproc \
		--standalone \
		--pdf-engine=$(PDF_ENGINE) \
		--toc \
		$(MD_FILES_FULL) -o $@
	@echo ">>> Building ANONYMOUS PDF finished."

# 3. SM PDF (остается без изменений, использует SM_MD_FILES и SM_BIB)
$(SM_PDF_OUTPUT): $(SM_MD_FILES_LIST) $(SM_METADATA) $(SM_BIB) $(CSL_FILE) Makefile $(ALL_SM_MD_FILES)
	@echo ">>> Building Supplementary Materials PDF: $(SM_PDF_OUTPUT)..."
	@mkdir -p output
	$(PANDOC) \
		--metadata-file=$(SM_METADATA) \
		--bibliography=$(SM_BIB) \
		--citeproc \
		--standalone \
		--pdf-engine=$(PDF_ENGINE) \
		--toc \
		$(SM_MD_FILES) -o $@
	@echo ">>> Building Supplementary Materials PDF finished."


# --- Вспомогательные цели ---

# Подсчет слов (теперь просто выводит значение из файла)
count_words: $(WORD_COUNT_FILE)
	@echo ">>> Approximate word count (excluding bibliography): $$(cat $(WORD_COUNT_FILE) | sed 's/Word Count (excluding bibliography): //')"


# Очистка (добавить удаление файла счетчика)
clean:
	@echo ">>> Cleaning output directory..."
	@rm -rf output/*
	@echo ">>> Cleaning finished."

# Фиктивные цели
.PHONY: all clean count_words $(OUTPUT_PDF) $(ANONYMOUS_PDF_OUTPUT) $(SM_PDF_OUTPUT) $(SUBMISSION_BIB) $(SM_BIB) $(WORD_COUNT_FILE)