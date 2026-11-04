# MATH 231 -- Quiz, Sections 4.1--4.4 (versions A--J)

Paper-based quiz for **Math 231 -- Linear Algebra** (Qatar University, Dr. Yousef Dabboorasad), covering
Sections 4.1 Real Vector Spaces, 4.2 Subspaces, 4.3 Spanning Sets and 4.4 Linear Independence of the course notes.
Ten parallel versions (A--J), two A4 pages each, 10 marks: Problem 1 True/False (4 x 0.5), Problem 2 MCQ (4 x 1),
Problem 3 written (2.5 + 1.5 with eight 0.5-mark checkpoints).

**Assumptions to confirm** (none was supplied in the request; each is one edit in the sources):
quiz number/label (`\QuizLabel` in the TeX preambles), date and time limit (not printed), total marks and weights
(`SPEC` in `build/quizdata.py`), and the Problem 3 design (dependent set + u not in span in versions A, D, E, H, I;
independent set + u in span in versions B, C, F, G, J).

## Contents
| Path | What it is |
|---|---|
| `release/MATH231_Quiz_4.1-4.4_Student_A-J.tex` / `.pdf` | STUDENT paper, versions A--J, 20 A4 pages (pages 1--2 = A, ..., 19--20 = J). No answers. **This is the only file to print for students.** |
| `release/MATH231_Quiz_4.1-4.4_Solved_A-J.tex` / `.pdf` | INSTRUCTOR solved copy, same 20 pages, answers marked and worked solutions in blue. |
| `release/MATH231_Quiz_4.1-4.4_Rubric_A-J.tex` / `.pdf` | Detailed rubric (32 pages): conventions, master answer grid, checkpoints, per-version keys with option-by-option reasons, model solutions, source provenance. |
| `release/figures/branding/` | The two official logos copied from the course project (used by the TeX files; guarded by `\IfFileExists`). |
| `analysis/SOURCE_ANALYSIS.md` | Section-by-section analysis of the notes, taught methods, source issues, specification and design decisions. |
| `analysis/SOURCE_INVENTORY.csv`, `SOURCE_MAP.csv`, `BLUEPRINT.csv`, `VERSION_LEDGER.csv`, `RUBRIC_CHECKPOINTS.csv`, `INDEPENDENT_MATH_QA.csv` | Inventory of every source item (62 rows), item-to-source map (90 rows), blueprint, version ledger, checkpoint table, independent verification log (90 rows, 0 failures). |
| `qa/QA_REPORT.json`, `qa/QA_REPORT_AUTOMATED.json`, `qa/QA_CHECKS.json`, `qa/logs/`, `qa/contact_sheets/` | QA records: consolidated report, compile/page-size/page-count checks, parity + leak scan, final compile logs, thumbnails of all 72 pages. |
| `build/` | Generator and checks: `quizdata.py` (all questions and keys), `build_quiz.py` (renders the three TeX files and the CSVs), `verify_math.py`, `qa_checks.py`, `compile_check.py`, `make_inventory.py`, `package.py`. |
| `COMPLETE_INSTRUCTOR.zip` | Everything above. **Do not distribute to students.** |
| `PRINT_ONLY.zip` | The student PDF only. |
| `SHA256SUMS.txt` | Hashes of every delivered file. |

## Recompiling
Each TeX file is standalone: run `pdflatex` twice from the `release/` folder (packages: extsizes, newtxtext/newtxmath,
TeX Gyre Termes, amsmath/amssymb, geometry, fancyhdr, tabularx, booktabs, longtable, enumitem, hyperref; all in a full TeX Live
and on Overleaf with the pdfLaTeX compiler). Compiled with TeX Live 2023 pdfTeX 1.40.25 here.

## Regenerating with different marks or labels
1. Edit `SPEC` (marks, labels, term) or any item in `build/quizdata.py`.
2. `python3 build/build_quiz.py release` (rewrites the three TeX files and the CSV records).
3. `python3 build/verify_math.py` (independent recomputation; must report 0 failures).
4. `python3 build/compile_check.py --student-tex ... --solved-tex ... --rubric-tex ... --output-dir release/build --version-ids A,B,C,D,E,F,G,H,I,J --pages-per-version 2`
5. `python3 build/qa_checks.py release` and inspect `release/build/contact_sheets/`.

Generated 2026-11-04T17:01:04Z.
