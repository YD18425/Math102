# -*- coding: utf-8 -*-
"""Canonical question data for MATH 231 Quiz (Sections 4.1-4.4), versions A-J.

Single source of truth: build_quiz.py renders the student, solved and rubric TeX files
from these structures; verify_math.py independently recomputes every key from them.

Authorized source: Math 231 Overleaf project (uploaded ZIP), file
01_lecture_notes/a4_notes/math231_lecture_notes_v02_2026_fully_solved.tex (sections 4.1-4.4,
lines 10672-13885) and the Chapter 4 Beamer deck. Line numbers below refer to that notes file.
"""

VERSIONS = "ABCDEFGHIJ"

SPEC = dict(
    course="Math 231 -- Linear Algebra",
    university="Qatar University",
    department="Department of Mathematics, Statistics and Physics",
    instructor="Dr. Yousef Dabboorasad",
    term="Fall 2026",
    quiz_label="Quiz 3",                   # confirmed by the instructor (2026-11-04)
    date="Thursday, 5 November 2026",      # confirmed (written 5-11-2026)
    time_limit="20 minutes",               # confirmed
    scope="Sections 4.1--4.4",
    scope_long="Sections 4.1--4.4 (Real Vector Spaces, Subspaces, Spanning Sets, Linear Independence)",
    total=10,
    tf_each=0.5, tf_count=4,
    mcq_each=1.0, mcq_count=4,
    written_total=4.0, written_a=2.5, written_b=1.5,
    textbook="Based on Anton \\& Rorres, \\textit{Elementary Linear Algebra}, 12e",
)
assert abs(SPEC["tf_each"]*SPEC["tf_count"] + SPEC["mcq_each"]*SPEC["mcq_count"] + SPEC["written_total"] - SPEC["total"]) < 1e-9
assert abs(SPEC["written_a"] + SPEC["written_b"] - SPEC["written_total"]) < 1e-9

NOTES = "math231_lecture_notes_v02_2026_fully_solved.tex"

# ----------------------------------------------------------------------------------
# Source locators (file line numbers in the fully solved notes, section 4.x)
# ----------------------------------------------------------------------------------
SRC = {
    "def4.1.1": ("Definition 4.1.1 (Vector Space Axioms)", 10737),
    "rem4.1.1": ("Remark 4.1.1", 10780),
    "thm4.1.1": ("Theorem 4.1.1", 10790),
    "how4.1": ("Info box: To Show That a Set with Two Operations Is a Vector Space", 10806),
    "ex4.1.1": ("Example 4.1.1 ($\\mathbb{R}^n$ is a vector space)", 10847),
    "ex4.1.2": ("Example 4.1.2 ($F(-\\infty,\\infty)$ is a vector space)", 10909),
    "ex4.1.3": ("Example 4.1.3 (NOT a vector space: $k(x_1,x_2)=(kx_1,0)$)", 10977),
    "ex4.1.4": ("Example 4.1.4 (NOT a vector space: $k(x_1,x_2)=(kx_1,x_2)$)", 11026),
    "def4.2.1": ("Definition 4.2.1 (Subspace)", 11129),
    "thm4.2.1": ("Theorem 4.2.1 (The Subspace Test)", 11139),
    "rem4.2.1": ("Remark 4.2.1 (Showing a Set Is NOT a Subspace)", 11154),
    "ex4.2.1": ("Example 4.2.1 (The Zero Subspace)", 11169),
    "ex4.2.2": ("Example 4.2.2 (First Quadrant Is NOT a Subspace)", 11200),
    "ex4.2.3": ("Example 4.2.3 (Symmetric Matrices Form a Subspace)", 11245),
    "ex4.2.4": ("Example 4.2.4 (Invertible Matrices Do NOT Form a Subspace)", 11293),
    "ex4.2.5": ("Example 4.2.5 (Singular Matrices Do NOT Form a Subspace)", 11317),
    "defPn": ("Definition box: The Vector Space $P_n$ / Hierarchy of Function Spaces", 11369),
    "ex4.2.6": ("Example 4.2.6 (Degree Exactly 2 Is NOT a Subspace)", 11424),
    "ex4.2.7": ("Example 4.2.7 (Solution Spaces of Homogeneous Systems)", 11477),
    "ex4.2.8": ("Example 4.2.8 (Solution Set of a Non-Homogeneous System)", 11525),
    "thm4.2.2": ("Theorem 4.2.2 (Intersection of Subspaces)", 11551),
    "rem4.2.2": ("Remark 4.2.2 (Union of Subspaces)", 11677),
    "ex4.2.9": ("Example 4.2.9 (Union of Subspaces Is NOT a Subspace)", 11687),
    "def4.2.4": ("Definition 4.2.4 (Linear Combination)", 11760),
    "ex4.2.10": ("Example 4.2.10 (Vector IS a Linear Combination)", 11774),
    "ex4.2.11": ("Example 4.2.11 (Vector Is NOT a Linear Combination)", 11843),
    "ex4.2.12": ("Example 4.2.12 (Linear Combination of Polynomials)", 11899),
    "xp4.2.1": ("Extra Problems 4.2.1 ($C(-\\infty,\\infty)$ is a subspace)", 11988),
    "xp4.2.2": ("Extra Problems 4.2.2 ($a+b+c=0$ in $P_2$)", 12017),
    "xp4.2.3": ("Extra Problems 4.2.3 (matrices with $a_{11}=1$)", 12077),
    "xp4.2.4": ("Extra Problems 4.2.4 (integer coefficients)", 12098),
    "xp4.2.5": ("Extra Problems 4.2.5 ($C^1(-\\infty,\\infty)$)", 12128),
    "xp4.2.6": ("Extra Problems 4.2.6 (trace zero)", 12157),
    "xp4.2.7": ("Extra Problems 4.2.7 (linear combination in $M_{22}$)", 12202),
    "xp4.2.8": ("Extra Problems 4.2.8 (express $\\mathbf{u}$ as a linear combination)", 12332),
    "xp4.2.9": ("Extra Problems 4.2.9 (subspaces of $P_3$)", 12451),
    "def4.3.1": ("Definition 4.3.1 (Span)", 12614),
    "thm4.3.1": ("Theorem 4.3.1 (Span Is a Subspace)", 12627),
    "rem4.3.1": ("Remark 4.3.1 (Properties of Span)", 12637),
    "rem4.3.2": ("Remark 4.3.2 (Important Spanning Sets)", 12664),
    "ex4.3.1": ("Example 4.3.1 (Testing Whether Vectors Span $\\mathbb{R}^3$)", 12721),
    "ex4.3.2": ("Example 4.3.2 (Testing Whether Polynomials Span $P_2$)", 12779),
    "xp4.3.1": ("Extra Problems 4.3.1 (four polynomials span $P_2$) + Remark", 12842),
    "xp4.3.2": ("Extra Problems 4.3.2 (four vectors span $\\mathbb{R}^3$)", 12992),
    "xp4.3.3": ("Extra Problems 4.3.3 ($M\\notin\\operatorname{span}$)", 13042),
    "def4.4.1": ("Definition 4.4.1 (Linear Independence and Dependence)", 13236),
    "thm4.4.1": ("Theorem 4.4.1", 13253),
    "rem4.4.1": ("Remark after Theorem 4.4.1", 13267),
    "ex4.4.1": ("Example 4.4.1 (Linear Dependence in $\\mathbb{R}^3$)", 13280),
    "ex4.4.2": ("Example 4.4.2 (Linear Independence in $P_3$)", 13357),
    "fact4.4.1": ("Fact 4.4.1 (Dimension Argument for Linear Dependence)", 13452),
    "ex4.4.3": ("Example 4.4.3 (Dimension Argument in $\\mathbb{R}^3$)", 13467),
    "ex4.4.4": ("Example 4.4.4 (Dimension Argument in $P_3$)", 13492),
    "def4.4.2": ("Definition 4.4.2 (Wronskian)", 13526),
    "fact4.4.2": ("Fact 4.4.2 (Wronskian Test)", 13541),
    "remW": ("Remark: Understanding the Wronskian Test", 13547),
    "ex4.4.5": ("Example 4.4.5 (Wronskian with Exponentials)", 13617),
    "ex4.4.6": ("Example 4.4.6 (Wronskian with Polynomial Functions)", 13664),
    "ex4.4.7": ("Example 4.4.7 (Wronskian with Scalar Multiples)", 13707),
    "xp4.4.1": ("Extra Problems 4.4.1 (four matrices in $M_{22}$)", 13787),
}

def src(*keys):
    """Human-readable provenance string (TeX)."""
    parts = []
    for k in keys:
        name, line = SRC[k]
        parts.append(f"{name}, line {line}")
    return "; ".join(parts)

# ----------------------------------------------------------------------------------
# TRUE / FALSE POOL   (text is TeX; answer True/False; reason for instructor)
# ----------------------------------------------------------------------------------
TF = {
 # ---- 4.1 ----
 "T1a": dict(sec="4.1", ans=True,
    text=r"In any vector space $V$, $0\mathbf{u}=\mathbf{0}$ for every vector $\mathbf{u}$ in $V$.",
    reason=r"This is Theorem 4.1.1(a).", srcs=("thm4.1.1",)),
 "T1c": dict(sec="4.1", ans=True,
    text=r"If $\mathbf{u}$ is a vector in a vector space and $k$ is a scalar with $k\mathbf{u}=\mathbf{0}$, then $k=0$ or $\mathbf{u}=\mathbf{0}$.",
    reason=r"This is Theorem 4.1.1(d).", srcs=("thm4.1.1",)),
 "T1d": dict(sec="4.1", ans=True,
    text=r"The set $F(-\infty,\infty)$ of all real-valued functions defined on $(-\infty,\infty)$, with pointwise addition and scalar multiplication, is a vector space.",
    reason=r"Example 4.1.2 verifies all ten axioms for $F(-\infty,\infty)$.", srcs=("ex4.1.2",)),
 "T1e": dict(sec="4.1", ans=False,
    text=r"A set with two operations that satisfies nine of the ten vector space axioms is still a vector space.",
    reason=r"All ten axioms must hold (Definition 4.1.1); if even one axiom fails the set is not a vector space (Examples 4.1.3 and 4.1.4 fail a single axiom).", srcs=("def4.1.1","ex4.1.3")),
 "T1f": dict(sec="4.1", ans=True,
    text=r"In a vector space $V$, $(-1)\mathbf{u}=-\mathbf{u}$ for every vector $\mathbf{u}$ in $V$.",
    reason=r"This is Theorem 4.1.1(c).", srcs=("thm4.1.1",)),
 "T1k": dict(sec="4.1", ans=False,
    text=r"To show that a set with two operations is a vector space, it is enough to verify Axiom 1 (closure under addition) and Axiom 6 (closure under scalar multiplication).",
    reason=r"Closure is only Step 3 of the procedure; Step 4 requires Axioms 2, 3, 4, 5, 7, 8, 9, 10 as well. Example 4.1.3 is closed under both operations yet fails Axiom 10.", srcs=("how4.1","ex4.1.3")),
 "T1p": dict(sec="4.1", ans=False,
    text=r"If $\mathbf{u}$ is a vector in a vector space and $k$ is a scalar with $k\mathbf{u}=\mathbf{0}$, then necessarily $k=0$.",
    reason=r"Theorem 4.1.1(d) says $k=0$ \emph{or} $\mathbf{u}=\mathbf{0}$. Counterexample: $k=5$ and $\mathbf{u}=\mathbf{0}$ give $5\mathbf{0}=\mathbf{0}$ with $k\neq0$ (Theorem 4.1.1(b)).", srcs=("thm4.1.1",)),
 "T1x": dict(sec="4.1", ans=False,
    text=r"In a vector space $V$, the equation $k\mathbf{0}=\mathbf{0}$ holds only when the scalar $k$ equals $0$.",
    reason=r"Theorem 4.1.1(b): $k\mathbf{0}=\mathbf{0}$ for \emph{every} scalar $k$.", srcs=("thm4.1.1",)),
 "T1z": dict(sec="4.1", ans=True,
    text=r"In a real vector space, the scalars may be any real numbers, including irrational numbers such as $\sqrt{2}$.",
    reason=r"Scalars are real numbers (Definition 4.1.1); the notes use $k=\sqrt2$ in Extra Problems 4.2.9(c).", srcs=("def4.1.1","xp4.2.9")),
 "T1aa": dict(sec="4.1", ans=False,
    text=r"In a vector space, if $k\mathbf{u}=\mathbf{0}$ for a scalar $k$ and a vector $\mathbf{u}$, then both $k=0$ and $\mathbf{u}=\mathbf{0}$.",
    reason=r"Theorem 4.1.1(d) gives $k=0$ \emph{or} $\mathbf{u}=\mathbf{0}$, not both: e.g. $0\mathbf{u}=\mathbf{0}$ for $\mathbf{u}=(1,1)\neq\mathbf{0}$.", srcs=("thm4.1.1",)),
 # ---- 4.2 ----
 "T2a": dict(sec="4.2", ans=False,
    text=r"The set of all invertible $2\times 2$ matrices is a subspace of $M_{22}$.",
    reason=r"The zero matrix is not invertible, so condition (a) of the Subspace Test fails (Example 4.2.4).", srcs=("ex4.2.4","thm4.2.1")),
 "T2c": dict(sec="4.2", ans=True,
    text=r"If $A$ is an $m\times n$ matrix, then the solution set of the homogeneous system $A\mathbf{x}=\mathbf{0}$ is a subspace of $\mathbb{R}^n$.",
    reason=r"Example 4.2.7: $A\mathbf{0}=\mathbf{0}$, $A(\mathbf{u}+\mathbf{v})=\mathbf{0}$ and $A(k\mathbf{u})=\mathbf{0}$.", srcs=("ex4.2.7",)),
 "T2d": dict(sec="4.2", ans=False,
    text=r"If $A$ is an $m\times n$ matrix and $\mathbf{b}\neq\mathbf{0}$, then the solution set of $A\mathbf{x}=\mathbf{b}$ is a subspace of $\mathbb{R}^n$.",
    reason=r"$A\mathbf{0}=\mathbf{0}\neq\mathbf{b}$, so the zero vector is not a solution; condition (a) fails (Example 4.2.8).", srcs=("ex4.2.8",)),
 "T2e": dict(sec="4.2", ans=True,
    text=r"If $W_1$ and $W_2$ are subspaces of a vector space $V$, then $W_1\cap W_2$ is a subspace of $V$.",
    reason=r"Theorem 4.2.2 (intersection of subspaces).", srcs=("thm4.2.2",)),
 "T2f": dict(sec="4.2", ans=False,
    text=r"If $W_1$ and $W_2$ are subspaces of a vector space $V$, then $W_1\cup W_2$ is always a subspace of $V$.",
    reason=r"Remark 4.2.2 / Example 4.2.9: the union of the $x$-axis and the $y$-axis is not closed under addition, $(0,7)+(2,0)=(2,7)$.", srcs=("rem4.2.2","ex4.2.9")),
 "T2h": dict(sec="4.2", ans=False,
    text=r"The first quadrant $W=\{(x,y)\in\mathbb{R}^2 : x\ge 0,\ y\ge 0\}$ is a subspace of $\mathbb{R}^2$.",
    reason=r"Not closed under scalar multiplication: $(-1)(5,7)=(-5,-7)\notin W$ (Example 4.2.2).", srcs=("ex4.2.2",)),
 "T2j": dict(sec="4.2", ans=True,
    text=r"The set of all $n\times n$ matrices $A$ with $\operatorname{tr}(A)=0$ is a subspace of $M_{nn}$.",
    reason=r"$\operatorname{tr}(O)=0$, $\operatorname{tr}(A+B)=\operatorname{tr}A+\operatorname{tr}B$, $\operatorname{tr}(kA)=k\operatorname{tr}A$ (Extra Problems 4.2.6).", srcs=("xp4.2.6",)),
 "T2k": dict(sec="4.2", ans=True,
    text=r"The set $W=\{a+bx+cx^2 : a+b+c=0\}$ is a subspace of $P_2$.",
    reason=r"The zero polynomial has $0+0+0=0$; the condition is preserved under sums and scalar multiples (Extra Problems 4.2.2).", srcs=("xp4.2.2",)),
 "T2l": dict(sec="4.2", ans=True,
    text=r"The set $C(-\infty,\infty)$ of all continuous functions on $(-\infty,\infty)$ is a subspace of $F(-\infty,\infty)$.",
    reason=r"The zero function is continuous, and sums and scalar multiples of continuous functions are continuous (Extra Problems 4.2.1).", srcs=("xp4.2.1",)),
 "T2q": dict(sec="4.2", ans=False,
    text=r"The set $W=\{a+bx+cx^2 : a,\,b,\,c \text{ are integers}\}$ is a subspace of $P_2$.",
    reason=r"Not closed under scalar multiplication: $\tfrac12(1+x+x^2)\notin W$ (Extra Problems 4.2.4).", srcs=("xp4.2.4",)),
 # ---- 4.3 ----
 "T3a": dict(sec="4.3", ans=True,
    text=r"If $S=\{\mathbf{w}_1,\dots,\mathbf{w}_r\}$ is a set of vectors in a vector space $V$, then $\operatorname{span}(S)$ is a subspace of $V$.",
    reason=r"Theorem 4.3.1.", srcs=("thm4.3.1",)),
 "T3b": dict(sec="4.3", ans=True,
    text=r"Every vector in a set $S$ belongs to $\operatorname{span}(S)$.",
    reason=r"Remark 4.3.1(1): $\mathbf{w}_i=0\mathbf{w}_1+\cdots+1\mathbf{w}_i+\cdots+0\mathbf{w}_r$.", srcs=("rem4.3.1",)),
 "T3c": dict(sec="4.3", ans=True,
    text=r"$\operatorname{span}\{1,\,x,\,x^2\}=P_2$.",
    reason=r"Remark 4.3.2(2): every $a+bx+cx^2$ is a linear combination of $1,x,x^2$.", srcs=("rem4.3.2",)),
 "T3d": dict(sec="4.3", ans=False,
    text=r"$\operatorname{span}\{1,\,x,\,x^2\}=P_3$.",
    reason=r"Every linear combination $k_1+k_2x+k_3x^2$ has no $x^3$ term, so $x^3\in P_3$ is not in the span; the span is $P_2$ (Remark 4.3.2).", srcs=("rem4.3.2","def4.3.1")),
 "T3e": dict(sec="4.3", ans=True,
    text=r"The zero vector belongs to $\operatorname{span}(S)$ for every nonempty set $S$ of vectors in $V$.",
    reason=r"$\mathbf{0}=0\mathbf{w}_1+\cdots+0\mathbf{w}_r$; also $\operatorname{span}(S)$ is a subspace (Theorem 4.3.1).", srcs=("def4.3.1","thm4.3.1")),
 "T3h": dict(sec="4.3", ans=True,
    text=r"If $\mathbf{u}\in\operatorname{span}\{\mathbf{v}_1,\mathbf{v}_2\}$, then $\mathbf{u}=k_1\mathbf{v}_1+k_2\mathbf{v}_2$ for some scalars $k_1,k_2$.",
    reason=r"Definition 4.3.1: the span is the set of all linear combinations.", srcs=("def4.3.1","def4.2.4")),
 "T3k": dict(sec="4.3", ans=False,
    text=r"The vectors $(1,0,0)$ and $(0,1,0)$ span $\mathbb{R}^3$.",
    reason=r"$k_1(1,0,0)+k_2(0,1,0)=(k_1,k_2,0)$ always has third component $0$, so e.g. $(0,0,1)$ is not a linear combination (Definition 4.3.1).", srcs=("def4.3.1","ex4.3.1")),
 "T3z": dict(sec="4.3", ans=False,
    text=r"If $\operatorname{span}(S)=\mathbb{R}^3$, then $S$ must contain exactly three vectors.",
    reason=r"Extra Problems 4.3.2: the four vectors $(1,-1,0),(1,2,1),(1,0,1),(3,3,-1)$ span $\mathbb{R}^3$.", srcs=("xp4.3.2",)),
 "T3aa": dict(sec="4.3", ans=False,
    text=r"The set $S=\{(1,-1,0),\,(1,2,1),\,(1,0,1),\,(3,3,-1)\}$ cannot span $\mathbb{R}^3$ because it contains more than three vectors.",
    reason=r"Extra Problems 4.3.2 row reduces to three pivots: the system is consistent for every $(a,b,c)$, so $\operatorname{span}(S)=\mathbb{R}^3$.", srcs=("xp4.3.2",)),
 "T3dd": dict(sec="4.3", ans=False,
    text=r"The polynomial $x^2$ belongs to $\operatorname{span}\{1+x^2,\;x\}$.",
    reason=r"$k_1(1+x^2)+k_2x=k_1+k_2x+k_1x^2$; matching $x^2$ requires $k_1=0$ (constant term) and $k_1=1$ ($x^2$ term), impossible.", srcs=("def4.3.1","ex4.2.12")),
 # ---- 4.4 ----
 "T4b": dict(sec="4.4", ans=True,
    text=r"A set with exactly two vectors is linearly independent if and only if neither vector is a scalar multiple of the other.",
    reason=r"Theorem 4.4.1(c).", srcs=("thm4.4.1",)),
 "T4c": dict(sec="4.4", ans=True,
    text=r"Every set of four vectors in $\mathbb{R}^3$ is linearly dependent.",
    reason=r"Fact 4.4.1(1) with $r=4>n=3$ (Example 4.4.3).", srcs=("fact4.4.1","ex4.4.3")),
 "T4e": dict(sec="4.4", ans=False,
    text=r"Every set of four polynomials in $P_3$ is linearly dependent.",
    reason=r"Fact 4.4.1(2) needs $r>n+1=4$; $\{1,x,x^2,x^3\}$ has four polynomials and is linearly independent (its Wronskian is the constant $12\neq0$, as in Example 4.4.6).", srcs=("fact4.4.1","ex4.4.6")),
 "T4f": dict(sec="4.4", ans=False,
    text=r"If the Wronskian of $f_1,\dots,f_n$ is identically zero on $(-\infty,\infty)$, then the functions are linearly dependent.",
    reason=r"When $W(x)\equiv0$ the Wronskian test is inconclusive (Remark after Fact 4.4.2, item 5).", srcs=("remW","fact4.4.2")),
 "T4g": dict(sec="4.4", ans=True,
    text=r"If the Wronskian of $f_1,\dots,f_n$ is not identically zero on $(-\infty,\infty)$, then the functions are linearly independent.",
    reason=r"Fact 4.4.2 (Wronskian test).", srcs=("fact4.4.2",)),
 "T4h": dict(sec="4.4", ans=False,
    text=r"The functions $e^{x}$ and $6e^{x}$ form a linearly independent set in $C(-\infty,\infty)$.",
    reason=r"$6e^x$ is a scalar multiple of $e^x$, so the set is linearly dependent (Example 4.4.7, Theorem 4.4.1(c)).", srcs=("ex4.4.7","thm4.4.1")),
 "T4j": dict(sec="4.4", ans=True,
    text=r"Every set of five matrices in $M_{22}$ is linearly dependent.",
    reason=r"Fact 4.4.1(3) with $r=5>2\cdot2=4$.", srcs=("fact4.4.1",)),
 "T4l": dict(sec="4.4", ans=True,
    text=r"A set consisting of a single nonzero vector is linearly independent.",
    reason=r"Theorem 4.4.1(b).", srcs=("thm4.4.1",)),
 "T4m": dict(sec="4.4", ans=False,
    text=r"If the Wronskian $W(x)$ of two functions satisfies $W(0)=0$, then the Wronskian test is inconclusive.",
    reason=r"Only $W(x)\equiv0$ (zero for \emph{every} $x$) makes the test inconclusive; e.g. $W(x)=x^2$ has $W(0)=0$ but $W(1)=1\neq0$, so the functions are linearly independent (Remark, item 2).", srcs=("remW",)),
 "T4r": dict(sec="4.4", ans=False,
    text=r"Every set of two nonzero vectors in $\mathbb{R}^3$ is linearly independent.",
    reason=r"Theorem 4.4.1(c): $(1,0,0)$ and $(2,0,0)$ are nonzero but one is a scalar multiple of the other, so the set is linearly dependent.", srcs=("thm4.4.1",)),
 "T4w": dict(sec="4.4", ans=False,
    text=r"If $\{\mathbf{v}_1,\mathbf{v}_2,\mathbf{v}_3\}$ is linearly dependent, then $\mathbf{v}_3$ must be a linear combination of $\mathbf{v}_1$ and $\mathbf{v}_2$.",
    reason=r"The Remark after Theorem 4.4.1 says \emph{at least one} vector is a linear combination of the others, not necessarily $\mathbf{v}_3$: for $\mathbf{v}_1=(1,0,0)$, $\mathbf{v}_2=(2,0,0)$, $\mathbf{v}_3=(0,1,0)$ the set is dependent but $\mathbf{v}_3\neq k_1\mathbf{v}_1+k_2\mathbf{v}_2$.", srcs=("rem4.4.1","thm4.4.1")),
}

TF_ASSIGN = {
 "A": ["T1a", "T2a", "T3a", "T4w"],
 "B": ["T1e", "T2c", "T3d", "T4c"],
 "C": ["T1c", "T2f", "T3k", "T4b"],
 "D": ["T1aa","T2e", "T3b", "T4h"],
 "E": ["T1d", "T2j", "T3z", "T4m"],
 "F": ["T1k", "T2h", "T3c", "T4g"],
 "G": ["T1f", "T2q", "T3e", "T4f"],
 "H": ["T1p", "T2k", "T3aa","T4j"],
 "I": ["T1x", "T2l", "T3h", "T4r"],
 "J": ["T1z", "T2d", "T3dd","T4l"],
}

# ----------------------------------------------------------------------------------
# MCQ (a): which single axiom fails  (Section 4.1, Examples 4.1.3 / 4.1.4 method)
# ----------------------------------------------------------------------------------
AXIOM_TEXT = {
 1: r"Axiom 1: $\mathbf{u}+\mathbf{v}$ is in $V$ (closure under addition)",
 2: r"Axiom 2: $\mathbf{u}+\mathbf{v}=\mathbf{v}+\mathbf{u}$",
 4: r"Axiom 4: there is a zero vector $\mathbf{0}$ with $\mathbf{0}+\mathbf{u}=\mathbf{u}$",
 6: r"Axiom 6: $k\mathbf{u}$ is in $V$ (closure under scalar multiplication)",
 7: r"Axiom 7: $k(\mathbf{u}+\mathbf{v})=k\mathbf{u}+k\mathbf{v}$",
 8: r"Axiom 8: $(k+m)\mathbf{u}=k\mathbf{u}+m\mathbf{u}$",
 9: r"Axiom 9: $k(m\mathbf{u})=(km)\mathbf{u}$",
 10: r"Axiom 10: $1\mathbf{u}=\mathbf{u}$",
}
AXIOM_SHORT = {1:"Axiom 1",2:"Axiom 2",4:"Axiom 4",6:"Axiom 6",7:"Axiom 7",8:"Axiom 8",9:"Axiom 9",10:"Axiom 10"}

# smul: python lambda on (k, tuple) -> tuple ; smul_tex: display; n: dimension
MCQA = {
 "A": dict(n=2, smul=lambda k,x:(k*x[0],0),          smul_tex=r"k(x_1,x_2)=(kx_1,\;0)",        fails=10, options=[7,10,8,9],
           test=r"Take $\mathbf{u}=(7,8)$: $1\mathbf{u}=(1\cdot7,\;0)=(7,0)\neq(7,8)=\mathbf{u}$, so Axiom 10 fails. The usual addition makes Axioms 7, 8, 9 hold: e.g. $(k+m)\mathbf{u}=((k+m)u_1,0)=(ku_1,0)+(mu_1,0)=k\mathbf{u}+m\mathbf{u}$.",
           adapt="Identical operations to Example 4.1.3 (the notes' own example); re-set as a four-option item."),
 "B": dict(n=2, smul=lambda k,x:(k*x[0],x[1]),        smul_tex=r"k(x_1,x_2)=(kx_1,\;x_2)",      fails=8,  options=[10,7,8,6],
           test=r"Take $\mathbf{u}=(2,5)$, $k=2$, $m=3$: $(k+m)\mathbf{u}=5(2,5)=(10,5)$ but $k\mathbf{u}+m\mathbf{u}=(4,5)+(6,5)=(10,10)$, so Axiom 8 fails. Axiom 10: $1\mathbf{u}=(u_1,u_2)=\mathbf{u}$ holds; Axiom 7: $k(\mathbf{u}+\mathbf{v})=(k(u_1+v_1),u_2+v_2)=k\mathbf{u}+k\mathbf{v}$ holds; Axiom 6 holds since $(ku_1,u_2)\in\mathbb{R}^2$.",
           adapt="Identical operations to Example 4.1.4 (the notes' own example); re-set as a four-option item."),
 "C": dict(n=2, smul=lambda k,x:(k*k*x[0],k*k*x[1]),  smul_tex=r"k(x_1,x_2)=(k^2x_1,\;k^2x_2)",  fails=8,  options=[8,9,10,7],
           test=r"Take $\mathbf{u}=(1,1)$, $k=m=1$: $(k+m)\mathbf{u}=2(1,1)=(4,4)$ but $k\mathbf{u}+m\mathbf{u}=(1,1)+(1,1)=(2,2)$, so Axiom 8 fails. Axiom 9: $k(m\mathbf{u})=k^2m^2\mathbf{u}=(km)^2\mathbf{u}=(km)\mathbf{u}$ holds; Axiom 10: $1^2\mathbf{u}=\mathbf{u}$ holds; Axiom 7: $k^2(\mathbf{u}+\mathbf{v})=k^2\mathbf{u}+k^2\mathbf{v}$ holds.",
           adapt="New scalar multiplication in the style of Examples 4.1.3-4.1.4; only Axiom 8 fails."),
 "D": dict(n=2, smul=lambda k,x:(0,k*x[1]),           smul_tex=r"k(x_1,x_2)=(0,\;kx_2)",        fails=10, options=[6,4,7,10],
           test=r"Take $\mathbf{u}=(3,4)$: $1\mathbf{u}=(0,4)\neq(3,4)=\mathbf{u}$, so Axiom 10 fails. Axiom 6 holds since $(0,ku_2)\in\mathbb{R}^2$; Axiom 4 holds with $\mathbf{0}=(0,0)$ (usual addition); Axiom 7: $k(\mathbf{u}+\mathbf{v})=(0,k(u_2+v_2))=(0,ku_2)+(0,kv_2)$ holds.",
           adapt="Mirror image of Example 4.1.3 (the zero is placed in the first component)."),
 "E": dict(n=3, smul=lambda k,x:(k*x[0],x[1],x[2]),   smul_tex=r"k(x_1,x_2,x_3)=(kx_1,\;x_2,\;x_3)", fails=8, options=[9,8,10,2],
           test=r"Take $\mathbf{u}=(1,1,1)$, $k=m=1$: $(k+m)\mathbf{u}=2\mathbf{u}=(2,1,1)$ but $k\mathbf{u}+m\mathbf{u}=(1,1,1)+(1,1,1)=(2,2,2)$, so Axiom 8 fails. Axiom 9: $k(m\mathbf{u})=(kmu_1,u_2,u_3)=(km)\mathbf{u}$ holds; Axiom 10: $1\mathbf{u}=\mathbf{u}$ holds; Axiom 2 holds for the usual addition.",
           adapt=r"Example 4.1.4 extended to $\mathbb{R}^3$."),
 "F": dict(n=3, smul=lambda k,x:(k*x[0],k*x[1],0),    smul_tex=r"k(x_1,x_2,x_3)=(kx_1,\;kx_2,\;0)", fails=10, options=[1,8,9,10],
           test=r"Take $\mathbf{u}=(1,2,3)$: $1\mathbf{u}=(1,2,0)\neq\mathbf{u}$, so Axiom 10 fails. Axiom 1 holds (usual addition); Axiom 8: $(k+m)\mathbf{u}=((k+m)u_1,(k+m)u_2,0)=k\mathbf{u}+m\mathbf{u}$ holds; Axiom 9: $k(m\mathbf{u})=(kmu_1,kmu_2,0)=(km)\mathbf{u}$ holds.",
           adapt=r"Example 4.1.3 extended to $\mathbb{R}^3$."),
 "G": dict(n=2, smul=lambda k,x:(k*x[0],k*k*x[1]),    smul_tex=r"k(x_1,x_2)=(kx_1,\;k^2x_2)",    fails=8,  options=[10,9,8,7],
           test=r"Take $\mathbf{u}=(1,1)$, $k=m=1$: $(k+m)\mathbf{u}=2(1,1)=(2,4)$ but $k\mathbf{u}+m\mathbf{u}=(1,1)+(1,1)=(2,2)$, so Axiom 8 fails. Axiom 10: $1\mathbf{u}=(u_1,u_2)$ holds; Axiom 9: $k(m\mathbf{u})=(kmu_1,k^2m^2u_2)=(km)\mathbf{u}$ holds; Axiom 7: $k(\mathbf{u}+\mathbf{v})=(k(u_1+v_1),k^2(u_2+v_2))=k\mathbf{u}+k\mathbf{v}$ holds.",
           adapt="New scalar multiplication in the style of Examples 4.1.3-4.1.4; only Axiom 8 fails."),
 "H": dict(n=3, smul=lambda k,x:(0,k*x[1],k*x[2]),    smul_tex=r"k(x_1,x_2,x_3)=(0,\;kx_2,\;kx_3)", fails=10, options=[10,8,4,1],
           test=r"Take $\mathbf{u}=(5,1,2)$: $1\mathbf{u}=(0,1,2)\neq\mathbf{u}$, so Axiom 10 fails. Axiom 8: $(k+m)\mathbf{u}=(0,(k+m)u_2,(k+m)u_3)=k\mathbf{u}+m\mathbf{u}$ holds; Axioms 4 and 1 hold for the usual addition.",
           adapt=r"Mirror image of Example 4.1.3 in $\mathbb{R}^3$."),
 "I": dict(n=2, smul=lambda k,x:(x[0],k*x[1]),        smul_tex=r"k(x_1,x_2)=(x_1,\;kx_2)",      fails=8,  options=[7,9,8,10],
           test=r"Take $\mathbf{u}=(5,2)$, $k=2$, $m=3$: $(k+m)\mathbf{u}=5(5,2)=(5,10)$ but $k\mathbf{u}+m\mathbf{u}=(5,4)+(5,6)=(10,10)$, so Axiom 8 fails. Axiom 7: $k(\mathbf{u}+\mathbf{v})=(u_1+v_1,k(u_2+v_2))=k\mathbf{u}+k\mathbf{v}$ holds; Axiom 9: $k(m\mathbf{u})=(u_1,kmu_2)=(km)\mathbf{u}$ holds; Axiom 10: $1\mathbf{u}=\mathbf{u}$ holds.",
           adapt="Mirror image of Example 4.1.4."),
 "J": dict(n=3, smul=lambda k,x:(x[0],x[1],k*x[2]),   smul_tex=r"k(x_1,x_2,x_3)=(x_1,\;x_2,\;kx_3)", fails=8, options=[6,8,10,9],
           test=r"Take $\mathbf{u}=(1,1,1)$, $k=m=1$: $(k+m)\mathbf{u}=2\mathbf{u}=(1,1,2)$ but $k\mathbf{u}+m\mathbf{u}=(1,1,1)+(1,1,1)=(2,2,2)$, so Axiom 8 fails. Axiom 6 holds since $(u_1,u_2,ku_3)\in\mathbb{R}^3$; Axiom 10: $1\mathbf{u}=\mathbf{u}$ holds; Axiom 9: $k(m\mathbf{u})=(u_1,u_2,kmu_3)=(km)\mathbf{u}$ holds.",
           adapt=r"Example 4.1.4 extended to $\mathbb{R}^3$ (modified third component)."),
}

# ----------------------------------------------------------------------------------
# MCQ (b): subspace identification (Section 4.2, Subspace Test)
# each option: (tex, is_subspace, reason_tex). 'ask' = "is" (exactly one subspace) or "not" (exactly one non-subspace)
# For verify_math.py: 'space' and 'pred' define membership tests; 'witness' gives the explicit failure.
# ----------------------------------------------------------------------------------
MCQB = {
 "A": dict(ask="is", V=r"\mathbb{R}^2", space="R2",
   options=[
    (r"$W=\{(x,y) : x+y=1\}$", False, r"$(0,0)\notin W$ since $0+0\neq1$ (condition (a) fails).",
       dict(pred=lambda v: v[0]+v[1]==1, witness=("zero",))),
    (r"$W=\{(x,y) : y=x^2\}$", False, r"$(1,1)\in W$ but $2(1,1)=(2,2)\notin W$ since $2\neq2^2$ (condition (c) fails).",
       dict(pred=lambda v: v[1]==v[0]**2, witness=("scalar",(1,1),2))),
    (r"$W=\{(x,y) : y=3x\}$", True, r"$(0,0)\in W$; if $y_1=3x_1,\ y_2=3x_2$ then $y_1+y_2=3(x_1+x_2)$ and $ky_1=3(kx_1)$, so $W$ is closed under both operations.",
       dict(pred=lambda v: v[1]==3*v[0])),
    (r"$W=\{(x,y) : x\ge0,\ y\ge0\}$", False, r"$(5,7)\in W$ but $(-1)(5,7)=(-5,-7)\notin W$ (Example 4.2.2).",
       dict(pred=lambda v: v[0]>=0 and v[1]>=0, witness=("scalar",(5,7),-1))),
   ], srcs=("thm4.2.1","ex4.2.2","rem4.2.1"), adapt="Line through the origin and three non-subspaces modelled on Example 4.2.2 / Remark 4.2.1."),
 "B": dict(ask="not", V=r"M_{22}", space="M22",
   options=[
    (r"all symmetric matrices ($A^T=A$)", True, r"Example 4.2.3: $O^T=O$, $(A+B)^T=A+B$, $(kA)^T=kA$.",
       dict(pred=lambda M: M[0][1]==M[1][0])),
    (r"all invertible matrices", False, r"The zero matrix is not invertible, so $O\notin W$ (Example 4.2.4).",
       dict(pred=lambda M: M[0][0]*M[1][1]-M[0][1]*M[1][0]!=0, witness=("zero",))),
    (r"all matrices with $\operatorname{tr}(A)=0$", True, r"Extra Problems 4.2.6: $\operatorname{tr}(O)=0$, $\operatorname{tr}(A+B)=\operatorname{tr}A+\operatorname{tr}B=0$, $\operatorname{tr}(kA)=k\operatorname{tr}A=0$.",
       dict(pred=lambda M: M[0][0]+M[1][1]==0)),
    (r"all matrices $\begin{bmatrix}a&b\\ c&d\end{bmatrix}$ with $a=0$", True, r"$O$ has $a=0$; the $(1,1)$ entry of $A+B$ is $0+0=0$ and of $kA$ is $k\cdot0=0$.",
       dict(pred=lambda M: M[0][0]==0)),
   ], srcs=("ex4.2.3","ex4.2.4","xp4.2.6","thm4.2.1"), adapt="Three subspaces from the notes' examples plus the non-subspace of Example 4.2.4."),
 "C": dict(ask="is", V=r"P_2", space="P2",
   options=[
    (r"$W=\{p\in P_2 : \deg(p)=2\}$", False, r"The zero polynomial does not have degree 2, so $\mathbf{0}\notin W$ (Example 4.2.6).",
       dict(pred=lambda p: p[2]!=0, witness=("zero",))),
    (r"$W=\{a+bx+cx^2 : a,b,c \text{ are integers}\}$", False, r"$1+x+x^2\in W$ but $\tfrac12(1+x+x^2)\notin W$ (Extra Problems 4.2.4).",
       dict(pred=lambda p: all(float(c).is_integer() for c in p), witness=("scalar",(1,1,1),0.5))),
    (r"$W=\{p\in P_2 : p(0)=1\}$", False, r"The zero polynomial has $p(0)=0\neq1$, so $\mathbf{0}\notin W$.",
       dict(pred=lambda p: p[0]==1, witness=("zero",))),
    (r"$W=\{a+bx+cx^2 : a+b+c=0\}$", True, r"Extra Problems 4.2.2: $0+0+0=0$, and the coefficient sum of $p_1+p_2$ and of $kp$ is $0$.",
       dict(pred=lambda p: p[0]+p[1]+p[2]==0)),
   ], srcs=("xp4.2.2","ex4.2.6","xp4.2.4","thm4.2.1"), adapt="Direct use of the notes' $P_2$ examples; $p(0)=1$ added as a non-subspace."),
 "D": dict(ask="not", V=r"\mathbb{R}^3", space="R3",
   options=[
    (r"$W=\{(x,y,z) : x+y+z=1\}$", False, r"$(0,0,0)\notin W$ since $0\neq1$ (condition (a) fails; compare Example 4.2.8).",
       dict(pred=lambda v: v[0]+v[1]+v[2]==1, witness=("zero",))),
    (r"$W=\{(x,y,z) : x+y+z=0\}$", True, r"Solution space of the homogeneous equation $x+y+z=0$ (Example 4.2.7).",
       dict(pred=lambda v: v[0]+v[1]+v[2]==0)),
    (r"$W=\{(x,y,z) : x=y=z\}$", True, r"Solution space of the homogeneous system $x-y=0,\ y-z=0$ (Example 4.2.7).",
       dict(pred=lambda v: v[0]==v[1]==v[2])),
    (r"$W=\{(x,y,z) : x=2y \text{ and } z=0\}$", True, r"Solution space of the homogeneous system $x-2y=0,\ z=0$ (Example 4.2.7).",
       dict(pred=lambda v: v[0]==2*v[1] and v[2]==0)),
   ], srcs=("ex4.2.7","ex4.2.8","thm4.2.1"), adapt="Homogeneous versus non-homogeneous solution sets (Examples 4.2.7-4.2.8) written as explicit subsets of $\\mathbb{R}^3$."),
 "E": dict(ask="is", V=r"F(-\infty,\infty)", space="F",
   options=[
    (r"$W=\{f : f(0)=1\}$", False, r"The zero function has $f(0)=0\neq1$, so $\mathbf{0}\notin W$.",
       dict(kind="f0eq1", witness=("zero",))),
    (r"$W=\{f : f(x)\ge0 \text{ for all } x\}$", False, r"$f(x)=1$ is in $W$ but $(-1)f=-1$ is not (condition (c) fails).",
       dict(kind="nonneg", witness=("scalar","1",-1))),
    (r"$W=C(-\infty,\infty)$, all continuous functions", True, r"Extra Problems 4.2.1: the zero function is continuous; sums and scalar multiples of continuous functions are continuous.",
       dict(kind="C")),
    (r"$W=\{f : f(1)=2\}$", False, r"The zero function has $f(1)=0\neq2$, so $\mathbf{0}\notin W$.",
       dict(kind="f1eq2", witness=("zero",))),
   ], srcs=("xp4.2.1","ex4.1.2","thm4.2.1"), adapt="Extra Problems 4.2.1 as the subspace; non-subspaces built from the function-space examples."),
 "F": dict(ask="is", V=r"M_{22}", space="M22",
   options=[
    (r"all matrices with $\det(A)=0$", False, r"Example 4.2.5: $A=\begin{bmatrix}1&2\\1&2\end{bmatrix}$ and $B=\begin{bmatrix}3&-1\\6&-2\end{bmatrix}$ have determinant $0$ but $\det(A+B)=-7\neq0$.",
       dict(pred=lambda M: M[0][0]*M[1][1]-M[0][1]*M[1][0]==0, witness=("add",((1,2),(1,2)),((3,-1),(6,-2))))),
    (r"all matrices with $\operatorname{tr}(A)=0$", True, r"Extra Problems 4.2.6: $\operatorname{tr}(O)=0$, $\operatorname{tr}(A+B)=\operatorname{tr}A+\operatorname{tr}B$, $\operatorname{tr}(kA)=k\operatorname{tr}A$.",
       dict(pred=lambda M: M[0][0]+M[1][1]==0)),
    (r"all matrices of the form $\begin{bmatrix}1&a\\ b&c\end{bmatrix}$", False, r"$O\notin W$ because its $(1,1)$ entry is $0\neq1$ (Extra Problems 4.2.3).",
       dict(pred=lambda M: M[0][0]==1, witness=("zero",))),
    (r"all matrices whose four entries are all $\ge0$", False, r"$I_2\in W$ but $(-1)I_2\notin W$ (condition (c) fails).",
       dict(pred=lambda M: all(M[i][j]>=0 for i in range(2) for j in range(2)), witness=("scalar",((1,0),(0,1)),-1))),
   ], srcs=("xp4.2.6","ex4.2.5","xp4.2.3","thm4.2.1"), adapt="Notes' matrix examples; non-negative entries added as a non-subspace."),
 "G": dict(ask="not", V=r"\mathbb{R}^2", space="R2",
   options=[
    (r"$W=\{(x,y) : x=0\}$ (the $y$-axis)", True, r"Example 4.2.9: a line through the origin; $(0,y_1)+(0,y_2)=(0,y_1+y_2)$ and $k(0,y)=(0,ky)$.",
       dict(pred=lambda v: v[0]==0)),
    (r"$W=\{(x,y) : 2x-5y=0\}$", True, r"Solution space of a homogeneous equation (Example 4.2.7).",
       dict(pred=lambda v: 2*v[0]-5*v[1]==0)),
    (r"$W=\{(0,0)\}$", True, r"The zero subspace (Example 4.2.1).",
       dict(pred=lambda v: v[0]==0 and v[1]==0)),
    (r"$W=\{(x,y) : xy\ge0\}$", False, r"$(1,0)\in W$ and $(0,-1)\in W$, but their sum $(1,-1)$ has $xy=-1<0$ (condition (b) fails).",
       dict(pred=lambda v: v[0]*v[1]>=0, witness=("add",(1,0),(0,-1)))),
   ], srcs=("ex4.2.9","ex4.2.7","ex4.2.1","rem4.2.1"), adapt="The set $xy\\ge0$ (closed under scalars but not sums) tests condition (b) as in Remark 4.2.1."),
 "H": dict(ask="not", V=r"F(-\infty,\infty)", space="F",
   options=[
    (r"$W=\{f : f(0)=1\}$", False, r"The zero function has $f(0)=0\neq1$, so $\mathbf{0}\notin W$.",
       dict(kind="f0eq1", witness=("zero",))),
    (r"$W=\{f : f(0)=0\}$", True, r"$\mathbf{0}(0)=0$; $(f+g)(0)=0+0=0$; $(kf)(0)=k\cdot0=0$.",
       dict(kind="f0eq0")),
    (r"$W=C^1(-\infty,\infty)$, all continuously differentiable functions", True, r"Extra Problems 4.2.5.",
       dict(kind="C1")),
    (r"$W=P_2$, all polynomials of degree at most 2", True, r"$P_2$ is a vector space under the same operations (Definition of $P_n$, hierarchy of function spaces), hence a subspace of $F(-\infty,\infty)$.",
       dict(kind="P2")),
   ], srcs=("xp4.2.5","defPn","thm4.2.1"), adapt="Function-space hierarchy from the notes; $f(0)=1$ added as the non-subspace."),
 "I": dict(ask="is", V=r"\mathbb{R}^3", space="R3",
   options=[
    (r"$W=\{(x,y,z) : x\ge0\}$", False, r"$(1,0,0)\in W$ but $(-1)(1,0,0)=(-1,0,0)\notin W$ (condition (c) fails).",
       dict(pred=lambda v: v[0]>=0, witness=("scalar",(1,0,0),-1))),
    (r"$W=\{(x,y,z) : x^2+y^2+z^2\le1\}$", False, r"$(1,0,0)\in W$ but $2(1,0,0)=(2,0,0)\notin W$ since $4>1$ (condition (c) fails).",
       dict(pred=lambda v: v[0]**2+v[1]**2+v[2]**2<=1, witness=("scalar",(1,0,0),2))),
    (r"$W=\{(x,y,z) : xyz=0\}$", False, r"$(1,1,0)\in W$ and $(0,0,1)\in W$, but $(1,1,0)+(0,0,1)=(1,1,1)$ has $xyz=1\neq0$ (condition (b) fails).",
       dict(pred=lambda v: v[0]*v[1]*v[2]==0, witness=("add",(1,1,0),(0,0,1)))),
    (r"$W=\{(x,y,z) : z=x-2y\}$", True, r"Solution space of the homogeneous equation $x-2y-z=0$ (Example 4.2.7).",
       dict(pred=lambda v: v[2]==v[0]-2*v[1])),
   ], srcs=("ex4.2.7","rem4.2.1","ex4.2.2"), adapt="Homogeneous plane as the subspace; three non-subspaces built with Remark 4.2.1 counterexamples."),
 "J": dict(ask="not", V=r"P_2", space="P2",
   options=[
    (r"$W=\{p\in P_2 : p(0)=0\}$", True, r"$p(0)=a$, so $W=\{bx+cx^2\}$: the zero polynomial is in $W$ and sums/scalar multiples keep $a=0$ (compare Extra Problems 4.2.9(a)).",
       dict(pred=lambda p: p[0]==0)),
    (r"$W=\{a+bx+cx^2 : a+b+c=2\}$", False, r"The zero polynomial has coefficient sum $0\neq2$, so $\mathbf{0}\notin W$.",
       dict(pred=lambda p: p[0]+p[1]+p[2]==2, witness=("zero",))),
    (r"$W=\{a+bx+cx^2 : a=2c\}$", True, r"$0=2\cdot0$; if $a_1=2c_1$ and $a_2=2c_2$ then $a_1+a_2=2(c_1+c_2)$ and $ka_1=2(kc_1)$.",
       dict(pred=lambda p: p[0]==2*p[2])),
    (r"$W=\{p\in P_2 : p(1)=0\}$", True, r"$p(1)=a+b+c$, so this is the subspace of Extra Problems 4.2.2.",
       dict(pred=lambda p: p[0]+p[1]+p[2]==0)),
   ], srcs=("xp4.2.2","xp4.2.9","ex4.2.6","thm4.2.1"), adapt="Homogeneous coefficient conditions (subspaces) versus a non-homogeneous one."),
}

# ----------------------------------------------------------------------------------
# MCQ (c): membership in span{v1, v2}  (Section 4.3 / Definition 4.3.1, Examples 4.2.10-4.2.12 method)
# space 'R3' -> vectors as tuples; 'P2' -> coefficient tuples (a,b,c) for a+bx+cx^2
# options: list of candidate tuples; exactly one is in the span (checked by verify_math.py)
# ----------------------------------------------------------------------------------
MCQC = {
 "A": dict(space="R3", v1=(1,0,2),  v2=(0,1,-1), options=[(3,1,7),(3,1,5),(1,1,2),(2,2,0)]),
 "B": dict(space="P2", v1=(1,0,1),  v2=(0,1,0),  options=[(3,2,-3),(2,3,3),(3,2,3),(3,3,2)]),
 "C": dict(space="R3", v1=(1,0,-1), v2=(0,1,3),  options=[(2,1,1),(2,1,5),(1,2,-5),(2,1,-1)]),
 "D": dict(space="P2", v1=(1,1,0),  v2=(0,0,1),  options=[(2,-2,-1),(2,1,-1),(1,2,2),(2,2,-1)]),
 "E": dict(space="R3", v1=(1,1,0),  v2=(0,1,1),  options=[(2,3,5),(2,5,3),(2,5,4),(1,1,1)]),
 "F": dict(space="P2", v1=(1,-1,0), v2=(1,0,1),  options=[(1,2,-3),(3,2,1),(1,2,3),(1,-2,3)]),
 "G": dict(space="R3", v1=(1,0,0),  v2=(0,1,2),  options=[(4,2,1),(1,2,3),(0,1,3),(4,1,2)]),
 "H": dict(space="P2", v1=(0,1,1),  v2=(1,0,0),  options=[(5,2,2),(5,2,5),(2,5,2),(5,2,-2)]),
 "I": dict(space="R3", v1=(1,0,1),  v2=(0,1,1),  options=[(3,-1,4),(3,1,2),(3,-1,2),(1,1,1)]),
 "J": dict(space="P2", v1=(1,2,0),  v2=(0,0,1),  options=[(2,2,-1),(2,4,-1),(4,2,-1),(1,4,-1)]),
}

# ----------------------------------------------------------------------------------
# MCQ (d): Wronskian of two functions + conclusion (Section 4.4, Definition 4.4.2 / Fact 4.4.2)
# f1,f2 : sympy-parsable strings in x ; W_tex: correct Wronskian (TeX) ; options: (tex, correct?)
# ----------------------------------------------------------------------------------
MCQD = {
 "A": dict(f1="x", f2="exp(x)", f1_tex="x", f2_tex="e^{x}", W_tex=r"(x-1)e^{x}",
   options=[(r"$W(x)=(x-1)e^{x}$; the set is linearly dependent because $W(1)=0$", False),
            (r"$W(x)=(x-1)e^{x}$; the set is linearly independent", True),
            (r"$W(x)=(x+1)e^{x}$; the set is linearly independent", False),
            (r"$W(x)=0$ for all $x$; the Wronskian test is inconclusive", False)],
   why=r"$W(x)=\begin{vmatrix}x&e^{x}\\1&e^{x}\end{vmatrix}=xe^{x}-e^{x}=(x-1)e^{x}$. This is not identically zero (e.g. $W(0)=-1$), so by Fact 4.4.2 the set is linearly independent. $W(1)=0$ at a single point does not matter (Remark, item 2); $(x+1)e^x$ is a sign error; $W$ is not the zero function."),
 "B": dict(f1="exp(x)", f2="exp(2*x)", f1_tex="e^{x}", f2_tex="e^{2x}", W_tex=r"e^{3x}",
   options=[(r"$W(x)=3e^{3x}$; the set is linearly independent", False),
            (r"$W(x)=0$ for all $x$; the Wronskian test is inconclusive", False),
            (r"$W(x)=e^{3x}$; the set is linearly dependent because $e^{2x}$ is a multiple of $e^{x}$", False),
            (r"$W(x)=e^{3x}$; the set is linearly independent", True)],
   why=r"$W(x)=\begin{vmatrix}e^{x}&e^{2x}\\e^{x}&2e^{2x}\end{vmatrix}=2e^{3x}-e^{3x}=e^{3x}\neq0$ for every $x$, so the set is linearly independent (Fact 4.4.2; compare Example 4.4.5). $3e^{3x}$ is an arithmetic error; $e^{2x}=e^{x}\cdot e^{x}$ is not a \emph{scalar} multiple of $e^{x}$; $W$ is never zero."),
 "C": dict(f1="1", f2="exp(-x)", f1_tex="1", f2_tex="e^{-x}", W_tex=r"-e^{-x}",
   options=[(r"$W(x)=-e^{-x}$; the set is linearly independent", True),
            (r"$W(x)=e^{-x}$; the set is linearly independent", False),
            (r"$W(x)=-e^{-x}$; the set is linearly dependent because $W(x)<0$", False),
            (r"$W(x)=0$ for all $x$; the Wronskian test is inconclusive", False)],
   why=r"$W(x)=\begin{vmatrix}1&e^{-x}\\0&-e^{-x}\end{vmatrix}=-e^{-x}\neq0$ for every $x$, hence linearly independent (Fact 4.4.2). The sign of $W$ is irrelevant; only $W\equiv0$ would be inconclusive; $e^{-x}$ is a sign error in the derivative."),
 "D": dict(f1="x", f2="x**2", f1_tex="x", f2_tex="x^{2}", W_tex=r"x^{2}",
   options=[(r"$W(x)=x^{2}$; the set is linearly dependent because $W(0)=0$", False),
            (r"$W(x)=x^{2}$; the Wronskian test is inconclusive because $W(0)=0$", False),
            (r"$W(x)=x^{2}$; the set is linearly independent", True),
            (r"$W(x)=3x^{2}$; the set is linearly independent", False)],
   why=r"$W(x)=\begin{vmatrix}x&x^{2}\\1&2x\end{vmatrix}=2x^{2}-x^{2}=x^{2}$. Since $W(1)=1\neq0$, $W$ is not identically zero and the set is linearly independent (Fact 4.4.2). $W(0)=0$ at one point neither proves dependence nor makes the test inconclusive (Remark, item 2); $3x^2$ is an arithmetic error."),
 "E": dict(f1="exp(x)", f2="x*exp(x)", f1_tex="e^{x}", f2_tex="xe^{x}", W_tex=r"e^{2x}",
   options=[(r"$W(x)=e^{2x}$; the set is linearly independent", True),
            (r"$W(x)=xe^{2x}$; the set is linearly independent", False),
            (r"$W(x)=xe^{2x}$; the set is linearly dependent because $W(0)=0$", False),
            (r"$W(x)=e^{2x}$; the set is linearly dependent because $xe^{x}$ is a multiple of $e^{x}$", False)],
   why=r"$(xe^{x})'=e^{x}+xe^{x}$, so $W(x)=\begin{vmatrix}e^{x}&xe^{x}\\e^{x}&e^{x}+xe^{x}\end{vmatrix}=e^{2x}+xe^{2x}-xe^{2x}=e^{2x}\neq0$; linearly independent by Fact 4.4.2. $xe^{x}$ is $x$ times $e^{x}$, not a \emph{scalar} multiple; $xe^{2x}$ comes from forgetting the product rule."),
 "F": dict(f1="1", f2="x**2", f1_tex="1", f2_tex="x^{2}", W_tex=r"2x",
   options=[(r"$W(x)=2x$; the set is linearly dependent because $W(0)=0$", False),
            (r"$W(x)=-2x$; the set is linearly independent", False),
            (r"$W(x)=2x$; the Wronskian test is inconclusive because $W(0)=0$", False),
            (r"$W(x)=2x$; the set is linearly independent", True)],
   why=r"$W(x)=\begin{vmatrix}1&x^{2}\\0&2x\end{vmatrix}=2x$. $W(1)=2\neq0$, so $W\not\equiv0$ and the set is linearly independent (Fact 4.4.2). A zero at the single point $x=0$ is irrelevant (Remark, item 2); $-2x$ is a sign error."),
 "G": dict(f1="exp(2*x)", f2="exp(3*x)", f1_tex="e^{2x}", f2_tex="e^{3x}", W_tex=r"e^{5x}",
   options=[(r"$W(x)=5e^{5x}$; the set is linearly independent", False),
            (r"$W(x)=e^{5x}$; the set is linearly independent", True),
            (r"$W(x)=e^{5x}$; the set is linearly dependent because $e^{3x}=e^{x}\cdot e^{2x}$", False),
            (r"$W(x)=e^{6x}$; the set is linearly independent", False)],
   why=r"$W(x)=\begin{vmatrix}e^{2x}&e^{3x}\\2e^{2x}&3e^{3x}\end{vmatrix}=3e^{5x}-2e^{5x}=e^{5x}\neq0$; linearly independent (Fact 4.4.2). $5e^{5x}$ adds instead of subtracting; $e^{3x}$ is not a scalar multiple of $e^{2x}$; $e^{6x}$ multiplies the functions instead of computing the determinant."),
 "H": dict(f1="x", f2="1+x", f1_tex="x", f2_tex="1+x", W_tex=r"-1",
   options=[(r"$W(x)=1$; the set is linearly independent", False),
            (r"$W(x)=-1$; the set is linearly dependent because $W(x)$ is negative", False),
            (r"$W(x)=-1$; the set is linearly independent", True),
            (r"$W(x)=0$ for all $x$; the Wronskian test is inconclusive", False)],
   why=r"$W(x)=\begin{vmatrix}x&1+x\\1&1\end{vmatrix}=x-(1+x)=-1\neq0$ for every $x$, so the set is linearly independent (Fact 4.4.2). The sign of $W$ does not matter; $W=1$ is a sign error; $W$ is not the zero function."),
 "I": dict(f1="x**2", f2="x**3", f1_tex="x^{2}", f2_tex="x^{3}", W_tex=r"x^{4}",
   options=[(r"$W(x)=x^{4}$; the set is linearly dependent because $W(0)=0$", False),
            (r"$W(x)=x^{4}$; the set is linearly independent", True),
            (r"$W(x)=5x^{4}$; the set is linearly independent", False),
            (r"$W(x)=0$ for all $x$; the Wronskian test is inconclusive", False)],
   why=r"$W(x)=\begin{vmatrix}x^{2}&x^{3}\\2x&3x^{2}\end{vmatrix}=3x^{4}-2x^{4}=x^{4}$. $W(1)=1\neq0$, so $W\not\equiv0$ and the set is linearly independent (Fact 4.4.2). $W(0)=0$ at one point does not give dependence (Remark, item 2); $5x^4$ adds instead of subtracting."),
 "J": dict(f1="exp(-x)", f2="exp(x)", f1_tex="e^{-x}", f2_tex="e^{x}", W_tex=r"2",
   options=[(r"$W(x)=2$; the set is linearly independent", True),
            (r"$W(x)=0$ for all $x$; the Wronskian test is inconclusive", False),
            (r"$W(x)=-2$; the set is linearly independent", False),
            (r"$W(x)=2$; the set is linearly dependent because $W(x)$ is constant", False)],
   why=r"$W(x)=\begin{vmatrix}e^{-x}&e^{x}\\-e^{-x}&e^{x}\end{vmatrix}=e^{-x}e^{x}-e^{x}(-e^{-x})=1+1=2\neq0$, so the set is linearly independent (Fact 4.4.2). $W=0$ comes from the sign error $1-1$; $-2$ is a sign error; a constant nonzero Wronskian is exactly what Fact 4.4.2 needs."),
}

# ----------------------------------------------------------------------------------
# Problem 3 (written): linear independence of S={v1,v2,v3} and membership u in span(S)
# space 'R3': vectors; 'P2': coefficient tuples (a,b,c) of a+bx+cx^2
# family 'D': dependent, u not in span ; 'I': independent, u in span with integer coefficients
# ----------------------------------------------------------------------------------
WRITTEN = {
 "A": dict(space="R3", vs=[(1,2,-1),(2,1,1),(5,4,1)],   u=(1,1,3),   family="D", relation=(1,2,-1)),   # v3 = v1 + 2 v2
 "B": dict(space="P2", vs=[(1,1,1),(1,-1,2),(2,1,-1)],  u=(3,-2,2),  family="I", coeffs=(-1,2,1)),
 "C": dict(space="R3", vs=[(1,1,2),(1,0,1),(2,1,1)],    u=(3,3,4),   family="I", coeffs=(2,-1,1)),
 "D": dict(space="P2", vs=[(1,1,0),(1,-1,1),(1,3,-1)],  u=(1,2,1),   family="D", relation=(2,-1,-1)),  # p3 = 2 p1 - p2
 "E": dict(space="R3", vs=[(1,-1,2),(1,1,0),(1,-3,4)],  u=(1,2,1),   family="D", relation=(2,-1,-1)),  # v3 = 2 v1 - v2
 "F": dict(space="P2", vs=[(1,0,1),(0,1,1),(1,-1,1)],   u=(-1,4,1),  family="I", coeffs=(1,2,-2)),
 "G": dict(space="R3", vs=[(1,2,1),(2,1,-1),(1,1,2)],   u=(4,3,-3),  family="I", coeffs=(1,2,-1)),
 "H": dict(space="P2", vs=[(2,1,-1),(1,1,1),(4,3,1)],   u=(1,2,1),   family="D", relation=(1,2,-1)),   # p3 = p1 + 2 p2
 "I": dict(space="R3", vs=[(1,-2,1),(3,1,2),(5,-3,4)],  u=(2,1,3),   family="D", relation=(2,1,-1)),   # v3 = 2 v1 + v2
 "J": dict(space="P2", vs=[(1,2,0),(0,1,-1),(1,0,1)],   u=(1,-1,1),  family="I", coeffs=(-1,1,2)),
}

# Written-problem rubric checkpoints (identical structure for every version)
CHECKPOINTS = [
 ("a1", 0.5, r"Sets up the vector equation $k_1\mathbf{v}_1+k_2\mathbf{v}_2+k_3\mathbf{v}_3=\mathbf{0}$ (for polynomials: equates coefficients of $1,x,x^2$) and states that the question is whether only the trivial solution exists.",
         r"Writing the homogeneous augmented matrix directly, or stating the determinant criterion for three vectors in a 3-dimensional space, is accepted."),
 ("a2", 0.5, r"Writes the correct homogeneous linear system (three equations) or the correct coefficient/augmented matrix $[A\mid\mathbf{0}]$.",
         r"Transposed set-up (vectors as rows) is accepted provided the subsequent reasoning is consistent."),
 ("a3", 0.5, r"First elimination stage correct: zeros below the first pivot with correct row operations.",
         r"Any valid sequence of elementary row operations; a determinant expansion with correct cofactors earns a3+a4 together."),
 ("a4", 0.5, r"Completes the reduction to a row echelon form correctly (identifies the zero row, or the third pivot) or computes $\det(A)$ correctly.",
         r"One arithmetic slip that does not change the structural outcome: deduct here only, follow through in a5."),
 ("a5", 0.5, r"Correct conclusion with a valid reason: a free variable / nontrivial solutions $\Rightarrow$ linearly dependent, or only the trivial solution $\Rightarrow$ linearly independent (or $\det=0$ / $\det\neq0$ respectively).",
         r"Exhibiting an explicit nontrivial relation such as $\mathbf{v}_3=\mathbf{v}_1+2\mathbf{v}_2$ proves dependence and earns a5 (and a1--a4 if the relation is verified by computation)."),
 ("b1", 0.5, r"Sets up $k_1\mathbf{v}_1+k_2\mathbf{v}_2+k_3\mathbf{v}_3=\mathbf{u}$ as a linear system or augmented matrix $[A\mid\mathbf{u}]$.",
         r"Re-using the matrix from part (a) with the new right-hand side is accepted and encouraged."),
 ("b2", 0.5, r"Row reduces $[A\mid\mathbf{u}]$ correctly (or applies the same operations as in (a) to the new column) to a row echelon form.",
         r"If (a) was reduced incorrectly, award b2 for consistent application of the (wrong) operations only when the resulting logic is sound; otherwise follow through once."),
 ("b3", 0.5, r"Correct final answer: inconsistent system $\Rightarrow\mathbf{u}\notin\operatorname{span}(S)$; or consistent $\Rightarrow\mathbf{u}\in\operatorname{span}(S)$ with correct $k_1,k_2,k_3$ and the combination written out.",
         r"For the independent versions, $k_1,k_2,k_3$ may also be found by Cramer's rule or the inverse matrix (Chapter 2); the written combination $\mathbf{u}=k_1\mathbf{v}_1+k_2\mathbf{v}_2+k_3\mathbf{v}_3$ must be stated."),
]
assert abs(sum(c[1] for c in CHECKPOINTS if c[0].startswith("a")) - SPEC["written_a"]) < 1e-9
assert abs(sum(c[1] for c in CHECKPOINTS if c[0].startswith("b")) - SPEC["written_b"]) < 1e-9
