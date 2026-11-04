# SOURCE ANALYSIS — MATH 231 (Linear Algebra), Sections 4.1–4.4

Prepared for the paper-based quiz **MATH 231 Quiz 3, Sections 4.1–4.4, versions A–J** (Fall 2026, Thursday 5 November 2026, 20 minutes; instructor Dr. Yousef Dabboorasad, Qatar University). This document records what the authorized sources contain, how the instructor solves each kind of task, what was and was not inspected, the source issues found, and how the quiz items map to the sources.

## 1. Source intake (gate G0)

| Item | Value |
|---|---|
| Uploaded course archive | `Math_231__Linear_Algebra___Complete_.zip` — SHA-256 `30c895a1a2dd989d59d999786c6557eb799f6f2465e257df0e62c0b12b73ded3` (159 files; TeX sources only, no compiled PDFs) |
| Uploaded workflow handoff | `Paper_Based_Quiz_New_Course_Handoff.zip` — SHA-256 `39331164a0fb9d71aeb5e3d149a954759c0b9cf5d6785aae9c8dd5281707a439`; `scripts/verify_handoff.py` → PASS (34 files, hashes match) |
| **Primary authorized source** | `01_lecture_notes/a4_notes/math231_lecture_notes_v02_2026_fully_solved.tex` — SHA-256 `861b3d9d5f1c71b2aae75908a595f31401f6e17f0f6e2f3e3dad4af3aa8cad21`; Chapter 4 begins at line 10672; §4.1 lines 10703–11089, §4.2 lines 11094–12575, §4.3 lines 12576–13196, §4.4 lines 13201–13885 (§4.5 begins at 13889) |
| Secondary source | `01_lecture_notes/slides/math231_lecture_beamer_chapter_04_vector_spaces.tex` — SHA-256 `5aadd1f593759e996b07fe2003d47e3afa573ceb0fb961593819bfadc2bdf018` (317 frames; §§4.1–4.4 frames 338–3160; same examples and extra problems as the notes, except Extra Problems 4.2.8–4.2.9 appear only in the notes) |
| Also inspected | `math231_lecture_notes_v02_2026_partially_solved.tex` (identical to the fully solved file in §§4.1–4.4 — verified by `diff`); `03_assessments/quizzes/math231_quiz_chapter_04_version_{a,b}_*.tex` and the Spring 2026 midterm (used only for the instructor's house conventions: True/False with no justification, 1-mark MCQs, "more than one answer = zero", no programmable calculators/phones); `00_admin/latex/branding.tex` (course line, instructor, textbook attribution); `figures/branding/*.png` (official logos, SHA-256 recorded in `SHA256SUMS.txt`) |
| Homework files for §§4.1–4.4 | `02_homeworks/by_section/section_4_{1..4}/*.tex` are **empty placeholders** (0 bytes) — no homework content exists for these sections |
| Not available | No compiled PDF of the notes was supplied and the notes require XeLaTeX with locally installed fonts that are not bundled; therefore **no physical PDF page numbers are cited anywhere**. All provenance uses file + line numbers + the notes' own example/theorem labels. Nothing was invented. |

Everything in §§4.1–4.4 of the notes was read in full from the TeX source (definitions, theorems, remarks, every Example, every Extra Problem, every solution box, TikZ illustrations). Because the sources are TeX rather than scanned PDFs, there was no handwriting to interpret; figures were read from their TikZ code.

## 2. Section-by-section synthesis (gate G1)

### §4.1 Real Vector Spaces (lines 10703–11089)
* **Taught content.** Definition 4.1.1 (ten axioms, numbered 1–10 exactly as in Anton & Rorres), Remark 4.1.1 (operations need not resemble those of ℝⁿ), Theorem 4.1.1 (0**u** = **0**, k**0** = **0**, (−1)**u** = −**u**, k**u** = **0** ⇒ k = 0 or **u** = **0**), and a four-step procedure box ("identify the set; identify the operations; check closure Axioms 1 and 6; check the remaining axioms").
* **Worked examples.** 4.1.1 ℝⁿ is a vector space (all ten axioms written out); 4.1.2 F(−∞,∞) is a vector space; 4.1.3 ℝ² with k(x₁,x₂) = (kx₁, 0) is **not** a vector space — the instructor picks the test vector (7,8) and shows Axiom 10 fails; 4.1.4 ℝ² with k(x₁,x₂) = (kx₁, x₂) is **not** a vector space — test vector (2,5), k = 2, m = 3, Axiom 8 fails.
* **Instructor's method for "not a vector space".** Choose one axiom, choose concrete numbers, compute both sides, exhibit the inequality, conclude. One failing axiom suffices.
* **Assessable in 1–3 steps.** Recognising Theorem 4.1.1 consequences (T/F); deciding which axiom fails for a modified scalar multiplication (MCQ with concrete computation).
* **Misconceptions to target.** "Nine axioms are enough"; "only closure needs checking"; confusing *or* with *and* in Theorem 4.1.1(d); k**0** = **0** "only for k = 0".

### §4.2 Subspaces (lines 11094–12575)
* **Taught content.** Definition 4.2.1; **Theorem 4.2.1 (Subspace Test) in the instructor's three-condition form**: (a) **0** ∈ W, (b) closed under addition, (c) closed under scalar multiplication; Remark 4.2.1 (to disprove, show one condition fails); M_mn and P_n as vector spaces with the hierarchy F ⊃ C ⊃ C¹ ⊃ Cᵐ ⊃ C^∞ ⊃ P_n; Theorem 4.2.2 (intersection of subspaces is a subspace, with proof); Remark 4.2.2 and Example 4.2.9 (union need not be a subspace); Definition 4.2.4 (linear combination).
* **Worked examples.** 4.2.1 {**0**} is a subspace; 4.2.2 first quadrant is not ((−1)(5,7)); 4.2.3 symmetric matrices are; 4.2.4 invertible matrices are not (zero matrix); 4.2.5 singular 2×2 matrices are not (explicit A, B with det(A+B) = −7); 4.2.6 polynomials of degree exactly 2 are not (zero polynomial); 4.2.7 solution space of A**x** = **0** is; 4.2.8 solution set of A**x** = **b**, **b** ≠ **0**, is not; 4.2.9 x-axis ∪ y-axis is not ((0,7)+(2,0)); 4.2.10 **u** = (9,2,7) *is* a combination of (1,2,−1),(6,4,2) (augmented matrix → RREF, k₁ = −3, k₂ = 2); 4.2.11 **u** = (4,−1,8) is *not* (row 0 = 3); 4.2.12 polynomial combination in P₂ (coefficient matching → RREF).
* **Extra Problems 4.2.1–4.2.9.** C(−∞,∞) ✓, {a+b+c = 0} in P₂ ✓, matrices with a₁₁ = 1 ✗, integer coefficients ✗ (k = ½), C¹ ✓, trace zero ✓, a 2×2-matrix linear combination (4 equations, 3 unknowns), express (−1,2,4) as a combination (c = (−15,−4,9)), four subsets of P₃ (a₀ = 0 ✓, coefficient sum 0 ✓, rational coefficients ✗ with k = √2, degree ≤ 1 ✓).
* **Instructor's method.** For "is a subspace": verify (a), (b), (c) in order with general elements. For "not": one explicit counterexample. For "is **u** a combination": set k₁**v**₁ + … = **u**, match components/coefficients, augmented matrix, row reduce, read off or detect inconsistency.
* **Assessable in 1–3 steps.** Subspace status of standard sets (T/F and MCQ); union/intersection facts (T/F).

### §4.3 Spanning Sets (lines 12576–13196)
* **Taught content.** Definition 4.3.1 (span = set of all linear combinations); Theorem 4.3.1 (span is a subspace); Remark 4.3.1 (every vector of S is in span(S); span(S) is the smallest subspace containing S; "S spans V" means span(S) = V); standard unit vectors; Remark 4.3.2 (span{i,j,k} = ℝ³, span{1,x,…,xⁿ} = P_n, the mn standard matrices span M_mn, illustrated for M₃ₓ₄).
* **Worked examples.** 4.3.1 (1,1,2),(1,0,1),(2,1,3) do **not** span ℝ³ (reduce with general (a,b,c); consistent only if c = a + b); 4.3.2 1+x, 1+x², 2+x+3x² **do** span P₂ (three pivots).
* **Extra Problems 4.3.1–4.3.4.** Four polynomials span P₂ (plus a remark on dependence, pivot columns, determinant 16 and an explicit relation p₄ = (10p₁ − 7p₂ − p₃)/8); four vectors span ℝ³ (4.3.2 and 4.3.4 are the same problem); a 2×2 matrix M is **not** in span{M₁,M₂,M₃} (row 0 = 4).
* **Instructor's method.** Spanning: augment with symbolic (a,b,c), reduce, check whether a zero row forces a condition. Membership: augment with the concrete vector, reduce, check consistency.
* **Assessable in 1–3 steps.** Properties of span (T/F); membership of a candidate in span{**v**₁,**v**₂} when the generators make k₁,k₂ readable from two coordinates (MCQ).

### §4.4 Linear Independence (lines 13201–13885)
* **Taught content.** Definition 4.4.1 (independent iff only the trivial solution); Theorem 4.4.1 (a set containing **0** is dependent; one vector is independent iff nonzero; two vectors are independent iff neither is a scalar multiple of the other); Remark (if dependent, at least one vector is a combination of the others; {i,j,k} is independent); **Fact 4.4.1** (dimension argument: r > n in ℝⁿ, r > n+1 in P_n, r > mn in M_mn ⇒ dependent); Definition 4.4.2 (Wronskian); **Fact 4.4.2** (W not identically zero ⇒ independent); a long remark distinguishing "zero at a point" from "identically zero", warning that W ≡ 0 is inconclusive, and the triangular shortcut.
* **Worked examples.** 4.4.1 (1,−2,3),(5,6,−1),(3,2,1) dependent (free variable); 4.4.2 three cubics independent (unique trivial solution, four equations); 4.4.3 four vectors in ℝ³ dependent (dimension argument); 4.4.4 five polynomials in P₃ dependent; 4.4.5 W(1, eˣ, e²ˣ) = 2e³ˣ ⇒ independent; 4.4.6 W(1,x,x²,x³,x⁴) = 288 (upper triangular); 4.4.7 {eˣ, 6eˣ}: W ≡ 0, dependence confirmed by the explicit relation (Theorem 4.4.1(c)).
* **Extra Problem 4.4.1.** Four 2×2 matrices (the three of Extra 4.3.3 plus M) are independent (four pivots).
* **Instructor's method.** Set k₁**v**₁ + … + k_r**v**_r = **0**, match entries, row reduce the homogeneous augmented matrix, interpret: free variable ⇒ dependent, no free variable ⇒ independent. For functions: build the Wronskian, compute, interpret.
* **Assessable in 1–3 steps.** Theorem 4.4.1 and Fact 4.4.1 (T/F); 2×2 Wronskian + interpretation (MCQ); full 3×3 reduction with interpretation (written).

## 3. Source issues found (reported, not silently corrected)

1. **Example 4.4.3 solution text (line ~13480) is a copy of the Example 4.4.4 solution**: it says "the number of polynomials r = 5 > n + 1 = 4, by Fact 4.4.1(2)" and concludes about {p₁,…,p₅}, although the example has four vectors in ℝ³. The correct argument is r = 4 > n = 3 by Fact 4.4.1(1) — exactly what the Beamer deck prints (frame at line 2861). No quiz item uses the erroneous text; T/F statement T4c cites the correct argument.
2. **Extra Problems 4.2.7 (line 12202)** ends with "The set is linearly dependent (4 equations, 3 unknowns, consistent with a zero row)". The computation shows three pivots, so {M₁,M₂,M₃} is linearly **independent**; the zero row reflects four equations in three unknowns. The remark is mathematically wrong (or refers loosely to the four-matrix set including the target). Not used in the quiz.
3. **Extra Problems 4.3.2 and 4.3.4** are duplicates (same S, same question). Treated as one source item.
4. **Notation.** The notes use P_n in §§4.2–4.3 and 𝔽_n-style blackboard **P**_n in §4.4/Fact 4.4.1. The quiz uses P_n throughout (the definition box, line 11369).
5. **§4.2 learning outcomes** list "Determine whether a set of vectors spans a given vector space", but that skill is taught in §4.3. Harmless; noted for completeness.
6. **Extra 4.3.2** prints the augmented matrices without the separator bar (cosmetic).

## 4. Quiz specification adopted (gate G2) and assumptions

The original request named only the course and coverage ("quiz for 4.1 to 4.4 of Math 231"); the values below were first fixed from the course's own conventions and the proven two-page layout, and the marks, label, date and time were then confirmed by the instructor on 2026-11-04. Each remains a single macro or number in `build/quizdata.py` / the TeX preamble:

| Field | Adopted value | Basis |
|---|---|---|
| Course / institution strings | Math 231 — Linear Algebra; Qatar University; Department of Mathematics, Statistics and Physics; Dr. Yousef Dabboorasad; "Based on Anton & Rorres, Elementary Linear Algebra, 12e" | `branding.tex`, Spring 2026 midterm title page |
| Term | Fall 2026 | `main.tex` of the uploaded project (`\date{Fall 2026}`) |
| Quiz label | "Quiz 3" (macro `\QuizLabel`) | confirmed by the instructor on 2026-11-04 |
| Date / time limit | Thursday, 5 November 2026; 20 minutes (printed in the header) | confirmed by the instructor on 2026-11-04 (written "5-11-2026, 20 minutes") |
| Total marks | **10** | confirmed by the instructor on 2026-11-04 |
| Problem 1 | 4 True/False × 0.5 = 2 marks, no justification (one statement per section) | midterm/quiz convention "no justification needed" |
| Problem 2 | 4 MCQ × 1 = 4 marks, exactly one option, >1 tick = 0 (one question per section) | midterm convention "questions with more than one answer will be marked zero" |
| Problem 3 | written, 4 marks = (a) 2.5 + (b) 1.5, eight 0.5-mark checkpoints | proven checkpoint pattern |
| Versions | A–J (10) | handoff default |
| Paper | A4, two pages per version; page 1 = Problems 1–2, page 2 = Problem 3 with 12 dotted working lines | handoff default |
| Materials | "Programmable calculators and mobile phones are not allowed" | midterm instruction 3 |

## 5. Design decisions worth the instructor's attention

* **Problem 3 families.** Versions A, D, E, H, I: S linearly dependent (**v**₃ = α**v**₁ + β**v**₂ with the relation hidden) and **u** ∉ span(S). Versions B, C, F, G, J: S linearly independent and **u** ∈ span(S) with unique integer coefficients. Both families use one 3×3 elimination per part; every displayed elimination uses integers only (verified). Spaces alternate ℝ³ (A, C, E, G, I) and P₂ (B, D, F, H, J).
* **MCQ (a)** reuses the operations of Examples 4.1.3 and 4.1.4 verbatim in versions A and B (the notes' own examples), with new operations in the other eight versions; every listed non-failing axiom was verified symbolically to hold.
* **MCQ (d)** uses 2×2 Wronskians only, with exponentials and polynomials as in the notes; distractors encode the notes' own warning (zero at a point vs. identically zero), a sign/derivative error, and "W = 0 ⇒ inconclusive".
* **T/F keys** are mixed in every version (patterns TFTF, FTFT, TFFT, FTTF, TTFF, FFTT, …); each statement is used once across the ten versions. No MCQ in the same version gives away a T/F answer.
* **Timing.** Estimated 19–20 minutes for a prepared student (T/F about 3, MCQ about 8.5, written about 8); part (b) of Problem 3 tells students they may reuse the row operations of part (a).
* **Out of scope on purpose:** basis, dimension, coordinates (§4.5–4.6), row/column/null space (§4.8–4.9). Where the notes mention dim(P₂) = 3 inside the §4.3 remark, the quiz does not rely on it.

## 6. Verification performed

* `build/verify_math.py` (SymPy + exhaustive integer-grid closure tests + witness checks): 90 items, 0 failures — see `INDEPENDENT_MATH_QA.csv`.
* `build/compile_check.py` (handoff script): three documents compile twice with pdfLaTeX; Student 20 pages, Solved 20 pages, Rubric 32 pages; all pages A4; "Version X" found on the expected pages; **zero** overfull/underfull boxes in the final logs.
* `build/qa_checks.py`: page structure (Problems 1–2 only on odd pages, Problem 3 only on even pages), student/solved parity (270 canonical stem/option fragments present in both files in the same order), student leak scan (no answers, keys, solution phrases, instructor tags, annotations or metadata), SHA-256 of all deliverables — see `QA_CHECKS.json`.
* Every page of the three PDFs was rendered and inspected visually (contact sheets for all 72 pages plus high-resolution checks of versions A, B, C, E, H, J pages and rubric pages 1–5).

See `QA_REPORT.json` for the consolidated record.
