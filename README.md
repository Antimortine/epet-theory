
# Emergent Predictive Experience Theory (EPET) / Теория Эмерджентного Предиктивного Опыта (ТЭПО) - Manuscript [EN]

This repository contains the source files for a manuscript outlining the **Emergent Predictive Experience Theory (EPET)** – an integrative philosophical theory of consciousness.

*(Note: The original version of the manuscript was written in Russian under the acronym ТЭПО (TEPO). This repository contains the English adaptation using the acronym EPET.)*

## About the Theory (EPET)

EPET aims to formulate a theory of consciousness that satisfies three criteria:

1.  **Scientific Plausibility:** Consistency with data from modern sciences (neuroscience, cognitive science, physics).
2.  **Consistency with the Core of Buddhism:** Compatibility with key philosophical and psychological concepts of Buddhism (*Anattā*, *Anicca*, *Paṭiccasamuppāda*, *Khandhas*), interpreted in a contemporary context.
3.  **Form and Style:** Exposition within the traditions and terminology of Western philosophy of mind.

The theory is positioned as **non-reductive (emergentist) physicalism** and integrates key ideas from:
*   **Predictive Processing (PP):** As the primary mechanism for generating the content and quality of experience (qualia).
*   **Global Workspace Theory (GWT):** As the mechanism for integration and conscious access.
*   **Embodied Cognition:** Emphasizing the role of the body and action.

EPET offers an explanation for the nature of qualia as properties of the emergent predictive modeling process and explains the sense of "self" as a dynamic construct of self-modeling, compatible with the doctrine of *Anattā*.

## Target Audience

The manuscript is primarily aimed at **philosophers of mind** and **neuroscientists/cognitive scientists** interested in fundamental questions of consciousness, as well as anyone interested in an interdisciplinary approach to the study of mind.

## Repository Structure

*   `manuscript/`: Source files of the manuscript in Markdown format, divided by sections.
*   `assets/`: Auxiliary resources (metadata, bibliography, citation styles).
*   `output/`: Directory for the generated PDF file (excluded from Git).
*   `Makefile` / `build.sh`: Script for automatic document building.
*   `README.md`: This file.
*   `.gitignore`: List of files ignored by Git.
*   `LICENSE`: License file (CC BY-NC-SA 4.0).

## Building the Document

To build the PDF file of the manuscript from the source Markdown files, you need:

1.  **Pandoc:** A universal document converter.
2.  **A LaTeX Distribution:** Such as TeX Live or MiKTeX (using the XeLaTeX or LuaLaTeX engine is recommended for Unicode support).
3.  **Bibliography Manager:** Required for processing the `.bib` file (included in LaTeX distributions).
4.  **Fonts:** Ensure that the fonts specified in `metadata.yaml` or the LaTeX template (if used) are installed (e.g., DejaVu fonts).
5.  **CSL Style:** The citation style file (e.g., `chicago-author-date.csl`) must be located in `assets/csl/` or be accessible to Pandoc.

**Build Command (Example):**

```bash
# Open a terminal in the root directory of the repository
# Run the command from Makefile or build.sh, or directly:
# (Ensure input_files.txt lists the correct order of .md files)
pandoc --metadata-file=assets/metadata.yaml \
       --citeproc \
       -s \
       $(cat manuscript/input_files.txt) \
       -o output/EPET_Theory.pdf \
       --pdf-engine=xelatex
```
(Note: The method $(cat ...) for passing the file list might differ on Windows; Makefile handles this.)

The generated file EPET_Theory.pdf will appear in the output/ directory.

## Status

This project represents the English adaptation of the EPET manuscript. The original Russian version is also available. Both are under active development and refinement.

## License

The text of the manuscript is distributed under the terms of the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://www.google.com/url?sa=E&q=https%3A%2F%2Fcreativecommons.org%2Flicenses%2Fby-nc-sa%2F4.0%2F).

This means you are free to:

-   **Share:** copy and redistribute the material in any medium or format.
    
-   **Adapt:** remix, transform, and build upon the material for non-commercial purposes.
    

Under the following terms:

-   **Attribution:** You must give appropriate credit, provide a link to the license, and indicate if changes were made.
    
-   **NonCommercial:** You may not use the material for commercial purposes.
    
-   **ShareAlike:** If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.
    

The full legal text of the license is available in the LICENSE file in the root of the repository.
