# GATE 2027 – Electronics & Communication Engineering (EC)

Study material for GATE 2027 EC (organising institute: IIT Madras).

## Folder layout

```
00_Syllabus/                 Official GATE 2027 EC syllabus
01_Notes/                    Short notes for revision (all subjects)
02_Previous_Year_Papers/
    <year>/                  One folder per exam year (2019–2026)
        GATE<year>_EC_QuestionPaper.pdf
        GATE<year>_EC_AnswerKey.pdf
03_Study_Plans/              Day-by-day study plans
04_Concept_Notes/            Conceptual notes with worked examples, one folder per subject
    tools/                   check_question_file.py, check_tables.py (structure checks), fig_helpers.py
    01_Network_Theory/       Days 1–6: a note and a 20-question set per day, plus a Day 6 mock test
        figures/             Circuit diagrams and plots used in the notes
        tools/               verify_dayNN.py re-check every number; make_figures_*.py redraw the figures
    02_Signals_and_Systems/  Days 7–9 so far: a note and a 20-question set per day
        figures/
        tools/               verify_day07.py … verify_day09.py, signals_lib.py (system-property tester)
```

## Contents

| Folder | File | Notes |
|---|---|---|
| `00_Syllabus` | `GATE2027_EC_Syllabus.pdf` | Official syllabus, IIT Madras |
| `01_Notes` | `GateOPedia_EC_ShortNotes_PW_2022.pdf` | Physics Wallah Gate-O-Pedia, 751 pages, 2022 edition. Some newer syllabus topics are missing (Smith chart, optical fibres, antenna arrays, IIR filter design, group/phase delay, Miller compensation, SRAM/DRAM, setup/hold time, superheterodyne receiver, regression) |
| `02_Previous_Year_Papers/2019` | Question paper + answer key | IIT Madras. Official key is included in the PDF from the GATE archive. Both PDFs are scanned images |
| `02_Previous_Year_Papers/2020` | Question paper + answer key | IIT Delhi. Split from the archive PDF. Mostly images |
| `02_Previous_Year_Papers/2021` | Question paper + answer key | Organised by IIT Bombay. Both PDFs are scanned images |
| `02_Previous_Year_Papers/2022` | Question paper + answer key | IIT Kharagpur |
| `02_Previous_Year_Papers/2023` | Question paper + answer key | IIT Kanpur |
| `02_Previous_Year_Papers/2024` | Question paper + final answer key | IISc Bengaluru |
| `02_Previous_Year_Papers/2025` | Question paper + answer key | IIT Roorkee |
| `02_Previous_Year_Papers/2026` | Question paper + answer key | IIT Guwahati |
| `03_Study_Plans` | `20_Day_Plan_Networks_Signals_Control.md` | 20-day plan with notes page numbers, daily checklists and links to the concept notes below |

## Concept notes (Days 1–9)

Each day has a **note** (concepts, worked examples, solved past-year questions with the official answers, practice problems, a list of the mistakes that cost marks, a one-page formula sheet, a self-test and a sources section) and a set of **20 GATE-style conceptual questions** (MCQ, MSQ and NAT, each testing one idea, with an answer key and full solutions). Start each day with the note, then take the question set.

| Day | Note | 20 questions | What it covers |
|---|---|---|---|
| 1 | [`Day01_Circuit_Analysis_Fundamentals.md`](04_Concept_Notes/01_Network_Theory/Day01_Circuit_Analysis_Fundamentals.md) | [`Day01_Conceptual_Questions.md`](04_Concept_Notes/01_Network_Theory/Day01_Conceptual_Questions.md) | KCL/KVL, nodal, mesh, supernode/supermesh, dependent sources, source transformation, star–delta |
| 2 | [`Day02_Network_Theorems.md`](04_Concept_Notes/01_Network_Theory/Day02_Network_Theorems.md) | [`Day02_Conceptual_Questions.md`](04_Concept_Notes/01_Network_Theory/Day02_Conceptual_Questions.md) | Superposition, Thevenin, Norton (with dependent sources), Millman, maximum power transfer, reciprocity |
| 3 | [`Day03_Transient_Analysis.md`](04_Concept_Notes/01_Network_Theory/Day03_Transient_Analysis.md) | [`Day03_Conceptual_Questions.md`](04_Concept_Notes/01_Network_Theory/Day03_Conceptual_Questions.md) | Initial and final conditions, RC, RL and RLC circuits, state equations, Laplace-domain analysis |
| 4 | [`Day04_Sinusoidal_Steady_State_and_Resonance.md`](04_Concept_Notes/01_Network_Theory/Day04_Sinusoidal_Steady_State_and_Resonance.md) | [`Day04_Conceptual_Questions.md`](04_Concept_Notes/01_Network_Theory/Day04_Conceptual_Questions.md) | Phasors, complex power, power-factor correction, AC maximum power, series and parallel resonance, the tank circuit |
| 5 | [`Day05_Two_Port_Networks.md`](04_Concept_Notes/01_Network_Theory/Day05_Two_Port_Networks.md) | [`Day05_Conceptual_Questions.md`](04_Concept_Notes/01_Network_Theory/Day05_Conceptual_Questions.md) | Z, Y, h, g and ABCD parameters, conversions, interconnections, terminated two-ports. **Coupled inductors and the ideal transformer are not in the GATE 2027 syllabus**; they are kept in a short optional section |
| 6 | [`Day06_Networks_Revision.md`](04_Concept_Notes/01_Network_Theory/Day06_Networks_Revision.md) | [`Day06_Conceptual_Questions.md`](04_Concept_Notes/01_Network_Theory/Day06_Conceptual_Questions.md) | Map of all 43 Networks questions of 2019–2026, master formula sheet, method chooser, 20 mixed questions, and a timed 25-question mock test: [`Day06_Mock_Test.md`](04_Concept_Notes/01_Network_Theory/Day06_Mock_Test.md) |
| 7 | [`Day07_Signals_and_System_Properties.md`](04_Concept_Notes/02_Signals_and_Systems/Day07_Signals_and_System_Properties.md) | [`Day07_Conceptual_Questions.md`](04_Concept_Notes/02_Signals_and_Systems/Day07_Conceptual_Questions.md) | Periodicity, even/odd, energy and power, step/impulse, time-axis operations, system properties (memory, causality, linearity, time invariance, stability) |
| 8 | [`Day08_Convolution_and_LTI_Systems.md`](04_Concept_Notes/02_Signals_and_Systems/Day08_Convolution_and_LTI_Systems.md) | [`Day08_Conceptual_Questions.md`](04_Concept_Notes/02_Signals_and_Systems/Day08_Conceptual_Questions.md) | Convolution (DT and CT), its properties, step response, causality and BIBO stability from h, cascade and parallel, which interconnections are LTI, frequency response |
| 9 | [`Day09_Fourier_Series.md`](04_Concept_Notes/02_Signals_and_Systems/Day09_Fourier_Series.md) | [`Day09_Conceptual_Questions.md`](04_Concept_Notes/02_Signals_and_Systems/Day09_Conceptual_Questions.md) | Continuous-time Fourier series: orthogonality, forms, standard waveforms, symmetry, properties, Parseval, Gibbs, periodic input to an LTI system, spectrum types |

Days 10–20 (Fourier transform and sampling, Laplace, z-transform, DFT, Control Systems, the combined test) have **no concept notes yet**; the plan points to the Gate-O-Pedia pages for them.

### How the concept notes are checked

- **Numbers.** Every number in a note is re-derived by a script, `tools/verify_dayNN.py` in the subject folder: circuits by a solver (`mna.py`), signals and systems by numerical integration, FFT-based coefficients and a numerical system-property tester (`signals_lib.py`). The past-year answers in the notes are checked against the official keys.
- **Structure.** `04_Concept_Notes/tools/check_question_file.py` checks each question file (20 questions, 20 solutions, 20 key rows, answer shapes, images). `check_tables.py` checks that markdown tables render on GitHub (an unescaped `|` inside a table cell splits the cell).
- **Sources.** Each note ends with a sources section that separates what was read from web pages (and says when a page was only partly read) from what was derived and verified in this repository.
- **Coverage limit.** The 2019 and 2021 papers and keys are scanned images, and 2020 is mostly images, so the maps of past questions for those years were made by reading the pages by eye. A missed question is possible.

To re-run the checks (needs `numpy`, `scipy`, `matplotlib`; the circuit figures also need `schemdraw`):

```bash
cd 04_Concept_Notes/02_Signals_and_Systems/tools && python3 verify_day09.py
cd ../.. && python3 tools/check_question_file.py 02_Signals_and_Systems/Day09_Conceptual_Questions.md
python3 tools/check_tables.py 01_Network_Theory/*.md 02_Signals_and_Systems/*.md
```

## How to use the answer keys

- Key question numbers follow the order of the **master question paper** in the same folder.
- **MCQ**: one correct option. Wrong answer costs 1/3 mark (1-mark questions) or 2/3 mark (2-mark questions).
- **MSQ**: all correct options and no wrong ones are needed. No partial marks, no negative marks.
- **NAT**: your answer must fall inside the range given in the key. No negative marks.
- **MTA** (Marks To All): the question was dropped and everyone got the marks.

## Sources

All question papers and answer keys are the official files published by the GATE organising institutes:

- 2019–2024 papers and 2021–2024 keys: GATE 2026 archive, <https://gate2026.iitg.ac.in/download.html> (the 2019 and 2020 files already contain their answer keys on the last pages)
- 2025 paper and key: <https://gate2025.iitr.ac.in/question-papers.html>
- 2026 paper and key: <https://gate2026.iitg.ac.in/QPs-answer-keys.html>
