# Emergent Predictive Experience Theory (EPET) - Manuscript [EN]

This repository contains the source files for the manuscript **"Emergent Predictive Experience Theory (EPET): An Integrative Philosophy of Consciousness"**.

*(Note: An earlier version of the theory was developed in Russian under the acronym ТЭПО (TEPO). This repository contains the current English manuscript using the acronym EPET.)*

## About the Theory (EPET)

EPET is an integrative philosophical theory of consciousness grounded in **non-reductive (emergentist) physicalism**. It aims to formulate an account of consciousness that satisfies three criteria:

1.  **Scientific Plausibility:** Consistency with data from modern sciences (neuroscience, cognitive science, physics).
2.  **Consistency with Core Buddhist Insights:** Compatibility with key philosophical concepts from Buddhism (*Anattā*, process ontology derived from *Anicca* & *Paṭiccasamuppāda*), used as conceptual constraints and heuristics.
3.  **Form and Style:** Exposition within the terminology and argumentative style of contemporary philosophy of mind.

The theory integrates key ideas from:
*   **Predictive Processing (PP):** As the primary mechanism generating the content and quality (qualia) of experience.
*   **Global Workspace Theory (GWT):** As the mechanism enabling conscious access, integration, and unity.
*   **Embodied Cognition:** Emphasizing the role of the living body, action, and interoception.

EPET offers a **constitutive explanation** for qualia as intrinsic properties of the emergent, integrated predictive modeling process. It explains the phenomenal **"self"** as a dynamic, constructed self-model arising from recursive predictive processing, compatible with the Buddhist principle of **Anattā** (no-self).

## Target Audience

The manuscript is primarily aimed at **philosophers of mind**, **cognitive scientists**, **neuroscientists**, and anyone interested in foundational questions about consciousness and interdisciplinary approaches to the study of mind.

## Repository Structure

*   `manuscript/`: Source files of the main manuscript in Markdown (`.md`), divided by sections. Contains `input_files.txt` (for anonymous PDF) and `input_files_full.txt` (for full PDF).
*   `manuscript/Supplementary_Materials/`: Source files (`.md`) for the Supplementary Materials. Contains `input_files_sm.txt`. Includes a `README.md` describing the SM contents.
*   `assets/`: Auxiliary resources (metadata `.yaml` files, common bibliography `.bib` file, CSL citation style).
*   `scripts/`: Utility scripts (e.g., `generate_filtered_bib.py`, `check_bib.py`).
*   `output/`: Directory for generated PDF files and filtered `.bib` files (excluded from Git by `.gitignore`).
*   `Makefile`: Defines build commands and dependencies.
*   `README.md`: This file.
*   `.gitignore`: List of files ignored by Git.
*   `LICENSE`: License file (CC BY 4.0 International). *(Note: Changed from BY-NC-SA based on PsyArXiv choice)*

## Building the Document

To build the PDF documents from the source files, you need:

1.  **Pandoc:** A universal document converter.
2.  **A LaTeX Distribution:** Such as TeX Live or MiKTeX (XeLaTeX engine is used by default).
3.  **Python 3:** Required for the bibliography generation script.
4.  **Python `bibtexparser` library:** Install via `pip install bibtexparser`.
5.  **Fonts:** Ensure DejaVu fonts (Serif, Sans, Sans Mono) are installed.

**Build Commands (using Make):**

(Run these commands from the root directory of the repository)

*   **Build all main PDFs (Full, Anonymous, SM):**
    ```bash
    make all
    ```
*   **Build only the Full PDF (with author info & references):**
    ```bash
    make output/EPET_Theory.pdf
    ```
*   **Build only the Anonymous PDF (for journal submission):**
    ```bash
    make output/EPET_Manuscript_Anonymous.pdf
    ```
*   **Build only the Supplementary Materials PDF:**
    ```bash
    make output/EPET_Supplementary_Materials.pdf
    ```
*   **Generate filtered bibliography files (optional, usually done automatically):**
    ```bash
    make output/references_for_submission.bib
    make output/references_for_sm.bib
    ```
*   **Clean the output directory:**
    ```bash
    make clean
    ```
*   **Count words (main manuscript, excluding bibliography):**
    ```bash
    make count_words
    ```

The `Makefile` handles dependencies, including the automatic generation of filtered `.bib` files required for PDF compilation.

## Status

*   **Current Version:** 1.3 (Post-reduction, ~11.9k words main text).
*   **Preprint:** An updated version corresponding to the full PDF (`EPET_Theory.pdf`) and Supplementary Materials (`EPET_Supplementary_Materials.pdf`) will be submitted to PsyArXiv.
*   **Journal Submission:** The anonymous version (`EPET_Manuscript_Anonymous.pdf`), filtered bibliography (`references_for_submission.bib`), and Supplementary Materials PDF (`EPET_Supplementary_Materials.pdf`) are being prepared for submission to *Philosophy and the Mind Sciences*.

## License

The text of the manuscript and supplementary materials is distributed under the terms of the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.

This means you are free to:

*   **Share:** copy and redistribute the material in any medium or format.
*   **Adapt:** remix, transform, and build upon the material for any purpose, even commercially.

Under the following terms:

*   **Attribution:** You must give appropriate credit, provide a link to the license, and indicate if changes were made.

The full legal text of the license is available in the `LICENSE` file. *(Note: Switched to CC BY 4.0 to match PsyArXiv's recommended open license and facilitate wider dissemination, removing NC and SA restrictions).*