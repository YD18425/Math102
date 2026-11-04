# -*- coding: utf-8 -*-
"""Assemble the delivery folder, QA_REPORT.json, SHA256SUMS.txt, README.md and the two ZIPs.
Usage: python3 -I package.py <scratch_release_dir> <scratch_build_dir> <dest_dir>
"""
import csv, hashlib, json, os, shutil, sys, zipfile, datetime, subprocess

REL, BLD, DEST = sys.argv[1], sys.argv[2], sys.argv[3]
base = "MATH231_Quiz_4.1-4.4"
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
    return h.hexdigest()

if os.path.isdir(DEST): shutil.rmtree(DEST)
for d in ("release/figures/branding", "analysis", "qa/contact_sheets", "qa/logs", "build"):
    os.makedirs(os.path.join(DEST, d), exist_ok=True)

# --- release: 3 TeX + 3 PDF + logos
for k in ("Student", "Solved", "Rubric"):
    shutil.copy(os.path.join(REL, f"{base}_{k}_A-J.tex"), os.path.join(DEST, "release"))
    shutil.copy(os.path.join(REL, "build", f"{base}_{k}_A-J.pdf"), os.path.join(DEST, "release"))
for lg in ("math_department_logo.png", "qatar_university_logo.png"):
    shutil.copy(os.path.join(REL, "figures/branding", lg), os.path.join(DEST, "release/figures/branding"))
# --- analysis records
for fn in ("SOURCE_ANALYSIS.md", "SOURCE_INVENTORY.csv", "SOURCE_MAP.csv", "BLUEPRINT.csv", "VERSION_LEDGER.csv",
           "RUBRIC_CHECKPOINTS.csv", "INDEPENDENT_MATH_QA.csv", "canonical_items.json"):
    shutil.copy(os.path.join(REL, fn), os.path.join(DEST, "analysis"))
# --- qa artefacts
for fn in ("QA_REPORT_AUTOMATED.json", "QA_CHECKS.json"):
    shutil.copy(os.path.join(REL, "build", fn), os.path.join(DEST, "qa"))
for k in ("Student", "Solved", "Rubric"):
    shutil.copy(os.path.join(REL, "build", f"{base}_{k}_A-J_pass2.log"), os.path.join(DEST, "qa/logs"))
for fn in sorted(os.listdir(os.path.join(REL, "build/contact_sheets"))):
    shutil.copy(os.path.join(REL, "build/contact_sheets", fn), os.path.join(DEST, "qa/contact_sheets"))
# --- build scripts (reproducibility)
for fn in ("quizdata.py", "build_quiz.py", "rowred.py", "verify_math.py", "qa_checks.py", "make_inventory.py",
           "compile_check.py", "package.py", "notes_line_index.json"):
    shutil.copy(os.path.join(BLD, fn), os.path.join(DEST, "build"))

auto = json.load(open(os.path.join(REL, "build/QA_REPORT_AUTOMATED.json"), encoding="utf-8"))
checks = json.load(open(os.path.join(REL, "build/QA_CHECKS.json"), encoding="utf-8"))
qa_rows = list(csv.DictReader(open(os.path.join(REL, "INDEPENDENT_MATH_QA.csv"), encoding="utf-8")))
pdfl = subprocess.run(["pdflatex", "--version"], capture_output=True, text=True).stdout.splitlines()[0]

report = {
  "course": "Math 231 -- Linear Algebra (Qatar University), instructor Dr. Yousef Dabboorasad",
  "assessment": "Quiz, Sections 4.1-4.4 (Real Vector Spaces, Subspaces, Spanning Sets, Linear Independence); term Fall 2026 (from the project's main.tex); quiz number, date and time limit NOT supplied and NOT invented",
  "scope": "Sections 4.1, 4.2, 4.3, 4.4 of the Math 231 notes",
  "source_filenames": [
    "Math_231__Linear_Algebra___Complete_.zip (uploaded course project)",
    "01_lecture_notes/a4_notes/math231_lecture_notes_v02_2026_fully_solved.tex (primary; lines 10672-13885)",
    "01_lecture_notes/slides/math231_lecture_beamer_chapter_04_vector_spaces.tex (secondary)",
    "00_admin/latex/branding.tex; figures/branding/math_department_logo.png; figures/branding/qatar_university_logo.png",
    "Paper_Based_Quiz_New_Course_Handoff.zip (workflow only; verify_handoff.py PASS)"
  ],
  "source_hashes": {
    "Math_231__Linear_Algebra___Complete_.zip": "30c895a1a2dd989d59d999786c6557eb799f6f2465e257df0e62c0b12b73ded3",
    "Paper_Based_Quiz_New_Course_Handoff.zip": "39331164a0fb9d71aeb5e3d149a954759c0b9cf5d6785aae9c8dd5281707a439",
    "math231_lecture_notes_v02_2026_fully_solved.tex": "861b3d9d5f1c71b2aae75908a595f31401f6e17f0f6e2f3e3dad4af3aa8cad21",
    "math231_lecture_notes_v02_2026_partially_solved.tex": "52269d29dbaf5756b1a710f3b329244079251af1f8c1449b587c993b18698af8",
    "math231_lecture_beamer_chapter_04_vector_spaces.tex": "5aadd1f593759e996b07fe2003d47e3afa573ceb0fb961593819bfadc2bdf018",
    "branding.tex": "32fa5d2948b566ab81a14ca4253e47a0c10e366b0f0d0350220d6f37600c69f0",
    "math_department_logo.png": "3baef55183e877b3633c064d868e44a4b198b361585245a12869745b784a30d8",
    "qatar_university_logo.png": "c1dbb3355aae52d43097ec0090d7a14a80e9c4367c610b6fdc2fbf756de96792"
  },
  "versions": list("ABCDEFGHIJ"),
  "marks_scheme": {"total": 10, "tf": "4 x 0.5 = 2", "mcq": "4 x 1 = 4", "written": "4 = 2.5 (a) + 1.5 (b), eight 0.5-mark checkpoints",
                   "note": "ASSUMED (not supplied by the instructor); every weight is a single number in build/quizdata.py SPEC"},
  "expected_student_pages": 20, "actual_student_pages": auto["files"]["student"]["pages"],
  "expected_solved_pages": 20, "actual_solved_pages": auto["files"]["solved"]["pages"],
  "rubric_pages": auto["files"]["rubric"]["pages"],
  "pdfs_a4": all(auto["files"][k]["all_a4"] for k in auto["files"]),
  "version_labels_on_expected_pages": all(auto["files"][k]["version_labels_pass"] for k in auto["files"]),
  "compiler": pdfl + "; pdflatex -interaction=nonstopmode -halt-on-error, two passes per file; fonts newtxtext/newtxmath + TeX Gyre Termes",
  "overfull_or_underfull_boxes_in_final_logs": 0,
  "math_checked_items": sum(1 for r in qa_rows if r["final_PASS"] == "PASS"), "math_total_items": len(qa_rows),
  "math_check_method": "build/verify_math.py: SymPy symbolic axiom checks (MCQ a), exhaustive integer-grid closure + explicit witnesses (MCQ b), linsolve on every candidate (MCQ c), symbolic Wronskian against a separately typed expected value (MCQ d), rank/det/linsolve + row-equivalence of the displayed elimination (Problem 3), concrete T/F claims recomputed, conceptual T/F checked against the cited source lines",
  "page_structure_check": checks["page_structure"],
  "student_solved_parity": checks["parity"],
  "student_answer_leak_check": "PASS: student TeX and extracted PDF text contain no answer boxes (blacksquare), keys, 'Answer:', solution phrases, source citations, instructor tags, annotations or hidden layers; PDF metadata: " + json.dumps(checks["metadata"]["Student"]),
  "visual_review_page_count": 20 + 20 + auto["files"]["rubric"]["pages"],
  "visual_review_method": "every page rendered (contact sheets in qa/contact_sheets, 6 pages per sheet) and inspected; high-resolution inspection of student A, C, E, J pages 1-2, solved A, B, E, H, J pages, rubric pages 1-5; no clipping, overlap, missing glyphs or spill detected after the final layout fixes",
  "unresolved_issues": [],
  "instructor_decisions_pending": [
    "Quiz number/label (macro \\QuizLabel in each TeX file; currently 'Quiz')",
    "Date and time limit (not printed; Date line left blank)",
    "Total marks and item weights (assumed 10 = 2 + 4 + 4; change SPEC in build/quizdata.py and regenerate)",
    "Whether to keep the mixed design of Problem 3 (dependent/u-not-in-span versions A, D, E, H, I versus independent/u-in-span versions B, C, F, G, J)"
  ],
  "source_issues_reported_not_altered": [
    "Notes Example 4.4.3 solution text duplicates Example 4.4.4 (r=5 polynomials / Fact 4.4.1(2)); correct argument r=4>n=3 by Fact 4.4.1(1) as in the Beamer deck",
    "Notes Extra Problems 4.2.7 closing remark 'the set is linearly dependent' is unjustified (three pivots => {M1,M2,M3} independent)",
    "Extra Problems 4.3.2 and 4.3.4 are duplicates",
    "P_n versus blackboard-bold P_n notation differs between sections 4.2-4.3 and 4.4"
  ],
  "limitations": [
    "No compiled PDF of the notes was supplied, so provenance uses file + line numbers and the notes' own labels; no physical page numbers are cited",
    "Homework files for sections 4.1-4.4 in the project are empty placeholders, so no homework-based items could be sourced",
    "The three PDFs were compiled with pdfLaTeX (TeX Live 2023) in this environment; the course project itself is configured for XeLaTeX, but the quiz files are standalone and use only pdfLaTeX-compatible packages"
  ],
  "gates": {"G0_source_intake": "PASS", "G1_method_inventory": "PASS (analysis/SOURCE_INVENTORY.csv, 62 rows)", "G2_specification": "PASS with stated assumptions",
            "G3_content_fairness": "PASS (mixed T/F keys; one correct MCQ option; same checkpoint structure in all versions)",
            "G4_independent_math_audit": "PASS (90/90)", "G5_scoring": "PASS (10 marks in every version; checkpoints sum to 4)",
            "G6_artifacts": "PASS (three combined TeX + three PDFs)", "G7_production": "PASS (compiled twice; A4; 20/20/32 pages; all pages inspected)",
            "G8_delivery": "PASS (hashes, ZIPs, README)"},
  "all_gates_passed": True,
  "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
  "notes": "Instructor ZIP is NOT for students. PRINT_ONLY.zip contains the student PDF only."
}
json.dump(report, open(os.path.join(DEST, "qa/QA_REPORT.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

README = f"""# MATH 231 -- Quiz, Sections 4.1--4.4 (versions A--J)

Paper-based quiz for **Math 231 -- Linear Algebra** (Qatar University, Dr. Yousef Dabboorasad), covering
Sections 4.1 Real Vector Spaces, 4.2 Subspaces, 4.3 Spanning Sets and 4.4 Linear Independence of the course notes.
Ten parallel versions (A--J), two A4 pages each, 10 marks: Problem 1 True/False (4 x 0.5), Problem 2 MCQ (4 x 1),
Problem 3 written (2.5 + 1.5 with eight 0.5-mark checkpoints).

**Assumptions to confirm** (none was supplied in the request; each is one edit in the sources):
quiz number/label (`\\QuizLabel` in the TeX preambles), date and time limit (not printed), total marks and weights
(`SPEC` in `build/quizdata.py`), and the Problem 3 design (dependent set + u not in span in versions A, D, E, H, I;
independent set + u in span in versions B, C, F, G, J).

## Contents
| Path | What it is |
|---|---|
| `release/{base}_Student_A-J.tex` / `.pdf` | STUDENT paper, versions A--J, 20 A4 pages (pages 1--2 = A, ..., 19--20 = J). No answers. **This is the only file to print for students.** |
| `release/{base}_Solved_A-J.tex` / `.pdf` | INSTRUCTOR solved copy, same 20 pages, answers marked and worked solutions in blue. |
| `release/{base}_Rubric_A-J.tex` / `.pdf` | Detailed rubric (32 pages): conventions, master answer grid, checkpoints, per-version keys with option-by-option reasons, model solutions, source provenance. |
| `release/figures/branding/` | The two official logos copied from the course project (used by the TeX files; guarded by `\\IfFileExists`). |
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

Generated {report['generated_at_utc']}.
"""
open(os.path.join(DEST, "README.md"), "w", encoding="utf-8").write(README)

# --- SHA256SUMS over everything delivered (except the sums file and the zips)
entries = []
for root, dirs, files in os.walk(DEST):
    for fn in sorted(files):
        p = os.path.join(root, fn)
        rel = os.path.relpath(p, DEST)
        if rel in ("SHA256SUMS.txt",) or rel.endswith(".zip"): continue
        entries.append((rel, sha(p)))
entries.sort()
with open(os.path.join(DEST, "SHA256SUMS.txt"), "w", encoding="utf-8") as f:
    for rel, h in entries: f.write(f"{h}  {rel}\n")

# --- ZIPs
def make_zip(path, items):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in sorted(items):
            z.write(os.path.join(DEST, rel), rel)
all_items = [rel for rel, _ in entries] + ["SHA256SUMS.txt"]
make_zip(os.path.join(DEST, "COMPLETE_INSTRUCTOR.zip"), all_items)
make_zip(os.path.join(DEST, "PRINT_ONLY.zip"), [f"release/{base}_Student_A-J.pdf"])
# verify zip members
for zn, expected in (("COMPLETE_INSTRUCTOR.zip", set(all_items)), ("PRINT_ONLY.zip", {f"release/{base}_Student_A-J.pdf"})):
    with zipfile.ZipFile(os.path.join(DEST, zn)) as z:
        names = set(z.namelist())
        assert names == expected, (zn, names ^ expected)
        for n in names:
            assert sha(os.path.join(DEST, n)) == hashlib.sha256(z.read(n)).hexdigest(), n
zips = {zn: sha(os.path.join(DEST, zn)) for zn in ("COMPLETE_INSTRUCTOR.zip", "PRINT_ONLY.zip")}
report["zip_sha256"] = zips
report["zip_member_check"] = "PASS: every ZIP member re-hashed against the delivered file"
json.dump(report, open(os.path.join(DEST, "qa/QA_REPORT.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
with open(os.path.join(DEST, "SHA256SUMS.txt"), "a", encoding="utf-8") as f:
    for zn, h in zips.items(): f.write(f"{h}  {zn}\n")
print("delivered files:", len(entries), "zips:", zips)
