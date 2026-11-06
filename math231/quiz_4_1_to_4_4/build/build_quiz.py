# -*- coding: utf-8 -*-
r"""Render the three combined TeX documents (Student, Solved, Rubric) and the analysis
records (BLUEPRINT.csv, VERSION_LEDGER.csv, SOURCE_MAP.csv, RUBRIC_CHECKPOINTS.csv,
SOURCE_INVENTORY.csv, canonical_items.json) from quizdata.py.

Usage: python3 -I build_quiz.py <release_dir>
"""
import csv, json, os, sys, shutil
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quizdata as Q
import rowred

OUT = sys.argv[1] if len(sys.argv) > 1 else "release"
os.makedirs(OUT, exist_ok=True)
S = Q.SPEC
BASENAME = "MATH231_Quiz3_4.1-4.4"
LETTERS = "ABCD"

def mk(x):
    """format a number for marks: 0.5 -> 0.5, 1.0 -> 1, 2.5 -> 2.5"""
    return ("%g" % x)

# ------------------------------------------------------------------ math formatting helpers
def vec_tex(t):
    return "(" + ",".join(str(int(c)) if float(c).is_integer() else str(c) for c in t) + ")"

def poly_tex(t):
    """coefficient tuple (a,b,c) -> a+bx+cx^2 with tidy signs"""
    a, b, c = t
    parts = []
    def term(coef, mon):
        if coef == 0: return None
        if mon == "":
            return ("%d" % coef)
        if coef == 1: return mon
        if coef == -1: return "-" + mon
        return "%d%s" % (coef, mon)
    for coef, mon in ((a, ""), (b, "x"), (c, "x^{2}")):
        s = term(coef, mon)
        if s is None: continue
        if parts and not s.startswith("-"):
            parts.append("+" + s)
        else:
            parts.append(s)
    return "".join(parts) if parts else "0"

def elt_tex(space, t):
    return vec_tex(t) if space == "R3" else poly_tex(t)

def linform(coeffs, varnames):
    """TeX of sum coeff_i * var_i with tidy signs (coeffs ints/Fractions)."""
    parts = []
    for c, vname in zip(coeffs, varnames):
        c = Fraction(c)
        if c == 0: continue
        if c == 1: s = vname
        elif c == -1: s = "-" + vname
        else: s = rowred.ftex(c) + vname
        if parts and not s.startswith("-"): s = "+" + s
        parts.append(s)
    return "".join(parts) if parts else "0"

KVARS = ["k_1", "k_2", "k_3"]
VNAME = {"R3": [r"\mathbf{v}_1", r"\mathbf{v}_2", r"\mathbf{v}_3"], "P2": ["p_1", "p_2", "p_3"]}
UNAME = {"R3": r"\mathbf{u}", "P2": "u"}
ZERO = {"R3": r"\mathbf{0}", "P2": "0"}

# ------------------------------------------------------------------ Problem 3 model solution
def written_solution(v, for_rubric=False):
    d = Q.WRITTEN[v]
    sp_ = d["space"]; vs = d["vs"]; u = d["u"]
    V = VNAME[sp_]; U = UNAME[sp_]
    A = [[vs[j][i] for j in range(3)] for i in range(3)]      # rows = components, columns = vectors
    comp_word = "components" if sp_ == "R3" else "coefficients of $1$, $x$ and $x^{2}$"
    sys_rows = [linform(A[i], KVARS) + "=0" for i in range(3)]
    sys_tex = r"\begin{cases}" + r"\\ ".join(sys_rows) + r"\end{cases}"
    expand = "+".join("%s%s" % (KVARS[j], ("(" + elt_tex(sp_, vs[j]) + ")") if sp_ == "P2" else elt_tex(sp_, vs[j])) for j in range(3))
    expand = expand.replace("+-", "-")
    rhs0 = "(0,0,0)" if sp_ == "R3" else "0+0x+0x^{2}"
    out = []
    out.append(r"\textbf{(a)} Set $%s%s+%s%s+%s%s=%s$, i.e. $%s=%s$. Comparing %s gives the homogeneous system and its augmented matrix:"
               % (KVARS[0], V[0], KVARS[1], V[1], KVARS[2], V[2], ZERO[sp_], expand, rhs0, comp_word))
    aug0 = [row + [0] for row in A]
    lines, final0, pivots = rowred.chain_tex(aug0, 3, per_line=2)
    out.append(r"\[ %s \qquad %s \]" % (sys_tex, lines[0]))
    for ln in lines[1:]:
        out.append(r"\[ %s \]" % ln)
    npiv = len(pivots)
    if d["family"] == "D":
        # back-substitute with free k3 = 1
        t = Fraction(1)
        ks = [None, None, t]
        for i in (1, 0):
            row = final0[i]
            s = sum(Fraction(row[j]) * ks[j] for j in range(i + 1, 3))
            ks[i] = (Fraction(row[3]) - s) / Fraction(row[i])
        rel = [rowred.ftex(kk) for kk in ks]
        # v3 = -k1 v1 - k2 v2
        rhs = linform([-ks[0], -ks[1]], V[:2])
        out.append(r"The coefficient matrix has only two pivots: the third row is a zero row, so $k_3$ is a free variable and the homogeneous system has \textbf{nontrivial solutions}. "
                   r"For instance $k_3=1$ gives $k_2=%s$ and $k_1=%s$, so $%s=%s$, i.e. $%s=%s$."
                   % (rel[1], rel[0], linform(ks, V), ZERO[sp_], V[2], rhs))
        out.append(r"\Conclude{$S$ is \textbf{linearly dependent}.}")
    else:
        out.append(r"There are three pivots and no free variables, so the homogeneous system has \textbf{only the trivial solution} $k_1=k_2=k_3=0$.")
        out.append(r"\Conclude{$S$ is \textbf{linearly independent}.}")
    # ---- part (b)
    augu = [row + [u[i]] for i, row in enumerate(A)]
    linesu, finalu, pivotsu = rowred.chain_tex(augu, 3, per_line=2)
    out.append(r"\textbf{(b)} Set $%s%s+%s%s+%s%s=%s$ with $%s=%s$. The coefficient matrix is the same, so the same row operations apply to the new right-hand side:"
               % (KVARS[0], V[0], KVARS[1], V[1], KVARS[2], V[2], U, U, elt_tex(sp_, u)))
    for ln in linesu:
        out.append(r"\[ %s \]" % ln)
    if d["family"] == "D":
        last = finalu[2]
        out.append(r"The last row reads $0k_1+0k_2+0k_3=%s$, i.e. $0=%s$, which is impossible: the system is \textbf{inconsistent}. Hence $%s$ is not a linear combination of $%s,%s,%s$."
                   % (rowred.ftex(last[3]), rowred.ftex(last[3]), U, V[0], V[1], V[2]))
        out.append(r"\Conclude{$%s\notin\operatorname{span}(S)$.}" % U)
        key_b = r"$%s\notin\operatorname{span}(S)$ (inconsistent: $0=%s$)" % (U, rowred.ftex(last[3]))
        key_a = "linearly dependent (zero row; $%s=%s$)" % (V[2], rhs)
    else:
        ks = [None, None, None]
        bs_lines = []
        for i in (2, 1, 0):
            row = finalu[i]
            s = sum(Fraction(row[j]) * ks[j] for j in range(i + 1, 3))
            ks[i] = (Fraction(row[3]) - s) / Fraction(row[i])
            eq = linform(row[:3], KVARS) + "=" + rowred.ftex(row[3])
            if eq == "k_%d=%s" % (i + 1, rowred.ftex(ks[i])):
                bs_lines.append(r"$%s$" % eq)
            else:
                bs_lines.append(r"$%s\Rightarrow k_%d=%s$" % (eq, i + 1, rowred.ftex(ks[i])))
        assert tuple(int(kk) for kk in ks) == tuple(d["coeffs"]), (v, ks, d["coeffs"])
        comb = linform(ks, V)
        out.append(r"Back-substitution: " + "; ".join(bs_lines) + r". Hence $%s=%s$." % (U, comb))
        out.append(r"\Conclude{$%s\in\operatorname{span}(S)$: \ $%s=%s$.}" % (U, U, comb))
        key_b = r"$%s=%s$" % (U, comb)
        key_a = "linearly independent (three pivots)"
    return "\n\n".join(out), key_a, key_b, final0, finalu

# ------------------------------------------------------------------ item stems (shared by student & solved)
def tf_items(v):
    return [(letter, Q.TF[i]) for letter, i in zip("abcd", Q.TF_ASSIGN[v])]

def mcqa_stem(v):
    d = Q.MCQA[v]
    if d["n"] == 2:
        add = r"(x_1,x_2)+(y_1,y_2)=(x_1+y_1,\;x_2+y_2)"; Vn = r"\mathbb{R}^2"
    else:
        add = r"(x_1,x_2,x_3)+(y_1,y_2,y_3)=(x_1+y_1,\;x_2+y_2,\;x_3+y_3)"; Vn = r"\mathbb{R}^3"
    return (r"Let $V=%s$ with the usual addition $%s$ and the scalar multiplication $%s$. "
            r"With these operations exactly one of the following four axioms fails. Which one?"
            % (Vn, add, d["smul_tex"]))

def mcqa_options(v):
    d = Q.MCQA[v]
    return [Q.AXIOM_TEXT[a] for a in d["options"]], d["options"].index(d["fails"])

def mcqb_stem(v):
    d = Q.MCQB[v]
    if d["ask"] == "is":
        return r"Which of the following subsets $W$ is a \textbf{subspace} of $V=%s$ (with the usual operations)?" % d["V"]
    return r"Which of the following subsets of $V=%s$ (with the usual operations) is \textbf{not} a subspace of $V$?" % d["V"]

def mcqb_options(v):
    d = Q.MCQB[v]
    truth = [o[1] for o in d["options"]]
    key = truth.index(True) if d["ask"] == "is" else truth.index(False)
    return [o[0] for o in d["options"]], key

def _elt_short(space, e):
    if space == "M22":
        return r"\begin{bmatrix}%s&%s\\%s&%s\end{bmatrix}" % (e[0][0], e[0][1], e[1][0], e[1][1])
    if space == "P2":
        return poly_tex(e)
    if space == "F":
        return str(e)
    return vec_tex(e)

def mcqb_short(v):
    """One-line reasons for the solved page (full reasons are in the rubric)."""
    d = Q.MCQB[v]
    parts = []
    for i, (tex, is_sub, reason, meta) in enumerate(d["options"]):
        if is_sub:
            parts.append(r"%s: subspace (passes the Subspace Test)." % LETTERS[i])
            continue
        w = meta.get("witness")
        if w[0] == "zero":
            parts.append(r"%s: $\mathbf{0}\notin W$." % LETTERS[i])
        elif w[0] == "scalar":
            if d["space"] == "F":
                parts.append(r"%s: $f=1\in W$ but $(-1)f\notin W$." % LETTERS[i])
            else:
                k = w[2]; kt = rowred.ftex(Fraction(k)) if not isinstance(k, float) else rowred.ftex(Fraction(k).limit_denominator())
                parts.append(r"%s: $%s\in W$ but $%s\left(%s\right)\notin W$." % (LETTERS[i], _elt_short(d["space"], w[1]), kt, _elt_short(d["space"], w[1])))
        elif w[0] == "add":
            parts.append(r"%s: $%s,\,%s\in W$ but their sum $\notin W$." % (LETTERS[i], _elt_short(d["space"], w[1]), _elt_short(d["space"], w[2])))
    return " ".join(parts)

def mcqc_stem(v):
    d = Q.MCQC[v]
    if d["space"] == "R3":
        return (r"Let $\mathbf{v}_1=%s$ and $\mathbf{v}_2=%s$ in $\mathbb{R}^3$. Which of the following vectors belongs to $\operatorname{span}\{\mathbf{v}_1,\mathbf{v}_2\}$?"
                % (vec_tex(d["v1"]), vec_tex(d["v2"])))
    return (r"Let $p_1=%s$ and $p_2=%s$ in $P_2$. Which of the following polynomials belongs to $\operatorname{span}\{p_1,p_2\}$?"
            % (poly_tex(d["v1"]), poly_tex(d["v2"])))

def mcqc_key_and_coeffs(v):
    """Solve k1 v1 + k2 v2 = candidate exactly (Fractions) for each candidate; return key index and per-option info."""
    d = Q.MCQC[v]
    v1, v2 = d["v1"], d["v2"]
    info = []
    key = None
    for idx, c in enumerate(d["options"]):
        # solve via 2x2 on the two coordinates where [v1 v2] has rank 2
        sol = None
        for (i, j) in ((0, 1), (0, 2), (1, 2)):
            det = v1[i] * v2[j] - v1[j] * v2[i]
            if det != 0:
                kk1 = Fraction(c[i] * v2[j] - c[j] * v2[i], det)
                kk2 = Fraction(v1[i] * c[j] - v1[j] * c[i], det)
                sol = (kk1, kk2, i, j); break
        kk1, kk2, i, j = sol
        rem = [t for t in range(3) if t not in (i, j)][0]
        pred = kk1 * v1[rem] + kk2 * v2[rem]
        ok = (pred == c[rem])
        info.append((idx, kk1, kk2, rem, pred, ok))
        if ok:
            assert key is None, "two options in span"
            key = idx
    return key, info

def mcqc_options(v):
    d = Q.MCQC[v]
    key, _ = mcqc_key_and_coeffs(v)
    opts = [elt_tex(d["space"], c) for c in d["options"]]
    return opts, key

def mcqc_explanation(v, short=False):
    d = Q.MCQC[v]
    key, info = mcqc_key_and_coeffs(v)
    sp_ = d["space"]
    V = (r"\mathbf{v}_1", r"\mathbf{v}_2") if sp_ == "R3" else ("p_1", "p_2")
    comp = {"R3": ["first", "second", "third"], "P2": ["constant", "$x$", "$x^{2}$"]}[sp_]
    compname = lambda r_: (comp[r_] + " component") if sp_ == "R3" else (comp[r_] + " coefficient")
    parts = []
    for idx, kk1, kk2, rem, pred, ok in info:
        c = d["options"][idx]
        tag = LETTERS[idx]
        if ok:
            parts.append(r"\textbf{%s}: $k_1=%s$, $k_2=%s$ give %s $=%s$ \checkmark, so $%s=%s%s%s$."
                         % (tag, rowred.ftex(kk1), rowred.ftex(kk2), compname(rem), rowred.ftex(pred),
                            elt_tex(sp_, c), linform([kk1], [V[0]]), "+" if kk2 >= 0 else "", linform([kk2], [V[1]])))
        else:
            parts.append(r"%s: $k_1=%s$, $k_2=%s$ would force the %s to be $%s\neq%s$."
                         % (tag, rowred.ftex(kk1), rowred.ftex(kk2), compname(rem), rowred.ftex(pred), c[rem]))
    if short:
        lead = r"Match $k_1%s+k_2%s$ with each candidate (two %s fix $k_1,k_2$; the third must agree). " % (V[0], V[1], "components" if sp_ == "R3" else "coefficients")
        return lead + " ".join(parts)
    lead = (r"Write $k_1%s+k_2%s$ and match the candidate: two of the three %s determine $k_1,k_2$ uniquely, and the remaining one must agree (Examples 4.2.10--4.2.11 method). "
            % (V[0], V[1], "components" if sp_ == "R3" else "coefficients"))
    return lead + " ".join(parts)

def mcqd_stem(v):
    d = Q.MCQD[v]
    return (r"Let $f_1=%s$ and $f_2=%s$ be functions in $C^{\infty}(-\infty,\infty)$. Compute the Wronskian $W(x)$ of $f_1,f_2$ and choose the correct statement."
            % (d["f1_tex"], d["f2_tex"]))

def mcqd_options(v):
    d = Q.MCQD[v]
    return [o[0] for o in d["options"]], [o[1] for o in d["options"]].index(True)

def written_stem(v):
    d = Q.WRITTEN[v]
    sp_ = d["space"]; vs = d["vs"]; u = d["u"]
    if sp_ == "R3":
        intro = (r"Let $S=\{\mathbf{v}_1,\mathbf{v}_2,\mathbf{v}_3\}$ be the set of vectors in $\mathbb{R}^3$ given by"
                 r"\[\mathbf{v}_1=%s,\qquad \mathbf{v}_2=%s,\qquad \mathbf{v}_3=%s,\]"
                 r"and let $\mathbf{u}=%s$." % (vec_tex(vs[0]), vec_tex(vs[1]), vec_tex(vs[2]), vec_tex(u)))
        parts = (r"Determine whether $S$ is linearly independent or linearly dependent. Show all your work.",
                 r"Determine whether $\mathbf{u}$ belongs to $\operatorname{span}(S)$, that is, whether $\mathbf{u}$ is a linear combination of $\mathbf{v}_1,\mathbf{v}_2,\mathbf{v}_3$. If it is, write $\mathbf{u}$ as such a linear combination; if it is not, explain why. (You may reuse the row operations from part (a).)")
    else:
        intro = (r"Let $S=\{p_1,p_2,p_3\}$ be the set of polynomials in $P_2$ given by"
                 r"\[p_1=%s,\qquad p_2=%s,\qquad p_3=%s,\]"
                 r"and let $u=%s$." % (poly_tex(vs[0]), poly_tex(vs[1]), poly_tex(vs[2]), poly_tex(u)))
        parts = (r"Determine whether $S$ is linearly independent or linearly dependent. Show all your work.",
                 r"Determine whether $u$ belongs to $\operatorname{span}(S)$, that is, whether $u$ is a linear combination of $p_1,p_2,p_3$. If it is, write $u$ as such a linear combination; if it is not, explain why. (You may reuse the row operations from part (a).)")
    return intro, parts

# ------------------------------------------------------------------ TeX building blocks
PREAMBLE_QUIZ = r"""\documentclass[14pt,a4paper]{extarticle}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb}
\usepackage{newtxtext,newtxmath}
\usepackage[a4paper,top=10mm,bottom=15mm,left=13mm,right=13mm,footskip=9mm]{geometry}
\usepackage{xcolor,graphicx,array,tabularx,booktabs,enumitem,fancyhdr}
\usepackage[hidelinks]{hyperref}
\graphicspath{{figures/branding/}}
\definecolor{Brand}{RGB}{0,90,170}
\definecolor{WorkBlue}{HTML}{174CA0}
\definecolor{RuleGray}{HTML}{B9BEC5}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\setlength{\abovedisplayskip}{4pt}\setlength{\belowdisplayskip}{4pt}
\setlength{\abovedisplayshortskip}{2pt}\setlength{\belowdisplayshortskip}{2pt}
\raggedbottom
\emergencystretch=1.5em
%% ---- editable labels -------------------------------------------------------
\newcommand{\QuizLabel}{%(quiz)s}
\newcommand{\TermLabel}{%(term)s}
\newcommand{\DateLabel}{%(date)s}
\newcommand{\TimeLabel}{%(time)s}
%% ----------------------------------------------------------------------------
\newcommand{\CurVersion}{A}
\newcommand{\CurPage}{1}
\pagestyle{fancy}\fancyhf{}
\renewcommand{\headrulewidth}{0pt}\renewcommand{\footrulewidth}{0.3pt}
\fancyfoot[L]{\fontsize{8}{9.5}\selectfont\begin{tabular}[b]{@{}l@{}}%(instructor)s\quad|\quad Math 231 -- \QuizLabel{} (%(scope)s)%(instr_tag)s\\ \textcolor{gray}{%(textbook)s}\end{tabular}}
\fancyfoot[R]{\fontsize{8.5}{10}\selectfont Version \CurVersion\quad\CurPage/2}
\newcommand{\Logo}[2]{\IfFileExists{figures/branding/#1}{\includegraphics[height=#2]{#1}}{}}
\newcommand{\LogoW}[2]{\IfFileExists{figures/branding/#1}{\includegraphics[width=#2]{#1}}{}}
\newcommand{\HeaderOne}[1]{%%
\renewcommand{\CurVersion}{#1}\renewcommand{\CurPage}{1}%%
\noindent\begin{minipage}[c]{34mm}\LogoW{math_department_logo.png}{33mm}\end{minipage}%%
\hfill\begin{minipage}[c]{\dimexpr\linewidth-56mm\relax}\centering
{\fontsize{10.5}{12}\selectfont\bfseries %(university)s}\\[-1pt]
{\fontsize{9.5}{11}\selectfont %(department)s}\\[2pt]
{\fontsize{16}{18}\selectfont\bfseries Math 231 -- Linear Algebra\quad\textcolor{Brand}{\QuizLabel}}\\[2pt]
{\fontsize{9}{10.5}\selectfont %(scope_long)s}\\[1pt]
{\fontsize{10}{11.5}\selectfont \TermLabel\quad\textbullet\quad \DateLabel\quad\textbullet\quad Time: \TimeLabel\quad\textbullet\quad Total: %(total)s marks}
\end{minipage}\hfill
\begin{minipage}[c]{18mm}\raggedleft\Logo{qatar_university_logo.png}{14mm}\end{minipage}\par
\vspace{1.5mm}\textcolor{Brand}{\rule{\linewidth}{0.8pt}}\par\vspace{1.5mm}
{\fontsize{11}{13}\selectfont Name: \rule{58mm}{0.3pt}\quad ID: \rule{30mm}{0.3pt}\quad Section: \rule{16mm}{0.3pt}}\hfill
{\fontsize{13}{15}\selectfont\bfseries\textcolor{Brand}{Version #1}}\par\vspace{1mm}
{\fontsize{9}{10.5}\selectfont\color{black!70}%(instructions)s}\par\vspace{2mm}
}
\newcommand{\HeaderTwo}[1]{%%
\renewcommand{\CurVersion}{#1}\renewcommand{\CurPage}{2}%%
\noindent{\fontsize{10.5}{12}\selectfont\bfseries Math 231 -- Linear Algebra\quad\textcolor{Brand}{\QuizLabel}\quad %(scope)s}\hfill
{\fontsize{12}{14}\selectfont\bfseries\textcolor{Brand}{Version #1}}\quad{\fontsize{10}{11.5}\selectfont Page 2 of 2}\par
\vspace{1mm}\textcolor{Brand}{\rule{\linewidth}{0.8pt}}\par\vspace{1.2mm}
{\fontsize{10}{11.5}\selectfont Name: \rule{58mm}{0.3pt}\quad ID: \rule{30mm}{0.3pt}}\par\vspace{2mm}
}
\newcommand{\PTitle}[2]{{\bfseries #1}\hfill{\bfseries [#2]}\par}
\newcommand{\PNote}[1]{{\fontsize{9.5}{11}\selectfont\color{black!70}#1}\par}
\newcommand{\Opt}[2]{$#1$~#2}
\newcommand{\Sol}[1]{{\fontsize{9.5}{11}\selectfont\color{WorkBlue}#1}\par}
\newcommand{\Conclude}[1]{\par\vspace{1pt}\noindent\fcolorbox{WorkBlue}{blue!4}{\textbf{\textcolor{WorkBlue}{#1}}}\par\vspace{2pt}}
\newcommand{\workline}{\noindent\textcolor{RuleGray}{\makebox[\linewidth]{\dotfill}}\par}
"""

INSTRUCTIONS = (r"Tick exactly one box for each True/False statement and exactly one option for each multiple-choice question; "
                r"an item with more than one answer receives zero. Show all your work in Problem 3. "
                r"Programmable calculators and mobile phones are not allowed.")

def preamble(mode):
    instr_tag = "" if mode == "student" else r"\quad|\quad \textcolor{red!70!black}{INSTRUCTOR COPY -- SOLVED -- NOT FOR STUDENTS}"
    return PREAMBLE_QUIZ % dict(quiz=S["quiz_label"], term=S["term"], instructor=S["instructor"], scope=S["scope"],
                                textbook=S["textbook"], university=S["university"], department=S["department"],
                                scope_long=S["scope_long"], total=S["total"], instructions=INSTRUCTIONS, instr_tag=instr_tag,
                                date=S["date"], time=S["time_limit"])

def short_until(text, marker):
    """Sentences of `text` up to and including the first sentence that contains `marker`."""
    sents = text.split(". ")
    out = []
    for snt in sents:
        out.append(snt)
        if marker in snt:
            break
    res = ". ".join(out)
    return res if res.endswith(".") else res + "."

def box(mark):
    return r"$\blacksquare$" if mark else r"$\square$"

def tf_block(v, solved):
    items = tf_items(v)
    rows = []
    gap = r"\\ \addlinespace[4.2mm]" if not solved else r"\\ \addlinespace[1.2mm]"
    for letter, t in items:
        cell = r"\textbf{(%s)}~%s" % (letter, t["text"])
        if solved:
            cell += r"\newline{\fontsize{9.5}{11}\selectfont\color{WorkBlue}\textbf{%s.} %s}" % ("True" if t["ans"] else "False", t["reason"])
        boxes = (box(solved and t["ans"]) + r"\hfill" + box(solved and not t["ans"]))
        rows.append(cell + " & " + boxes)
    body = (r"\PTitle{Problem 1. True or False}{%s marks}" % mk(S["tf_each"] * S["tf_count"]) + "\n" +
            r"\PNote{Each statement is worth %s mark. Tick \textbf{True} if the statement is always true, otherwise tick \textbf{False}. No justification is needed.}" % mk(S["tf_each"]) + "\n" +
            r"\begin{tabularx}{\linewidth}{@{}X@{\hspace{3mm}}>{\centering\arraybackslash}p{21mm}@{}}" + "\n" +
            r" & {\fontsize{9}{10}\selectfont True\hfill False}\\[0.5mm]" + "\n" +
            (gap + "\n").join(rows) + "\n" + r"\end{tabularx}\par")
    return body

def options_grid(opts, key, solved, mode="grid"):
    """mode 'grid' = 2x2 tabularx (long options); 'row' = four in one row (short math)."""
    cells = []
    for i, o in enumerate(opts):
        cells.append(r"%s %s.~%s" % (box(solved and i == key), LETTERS[i], o))
    if mode == "row":
        return (r"\begin{tabular*}{\linewidth}{@{}l@{\extracolsep{\fill}}lll@{}}" + "\n" +
                " & ".join(cells) + r"\end{tabular*}\par")
    return (r"{\hyphenpenalty=10000\exhyphenpenalty=10000\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}X@{\hspace{3mm}}>{\raggedright\arraybackslash}X@{}}" + "\n" +
            cells[0] + " & " + cells[1] + r"\\[0.8mm]" + "\n" + cells[2] + " & " + cells[3] + "\n" + r"\end{tabularx}}\par")

def mcq_block(v, solved):
    gap = r"\vspace{2.6mm}" if not solved else r"\vspace{1.2mm}"
    out = [r"\PTitle{Problem 2. Multiple choice}{%s marks}" % mk(S["mcq_each"] * S["mcq_count"]),
           r"\PNote{Each question is worth %s mark. Tick exactly one option.}" % mk(S["mcq_each"]), r"\vspace{0.8mm}"]
    # (a)
    opts, key = mcqa_options(v)
    out.append(r"\textbf{(a)}~" + mcqa_stem(v) + r"\par\vspace{0.8mm}")
    out.append(options_grid(opts, key, solved, "grid"))
    if solved:
        out.append(r"\Sol{\textbf{Answer: %s (Axiom %d).} %s}" % (LETTERS[key], Q.MCQA[v]["fails"], short_until(Q.MCQA[v]["test"], "fails.")))
    out.append(gap)
    # (b)
    opts, key = mcqb_options(v)
    out.append(r"\textbf{(b)}~" + mcqb_stem(v) + r"\par\vspace{0.8mm}")
    out.append(options_grid(opts, key, solved, "grid"))
    if solved:
        out.append(r"\Sol{\textbf{Answer: %s.} %s}" % (LETTERS[key], mcqb_short(v)))
    out.append(gap)
    # (c)
    opts, key = mcqc_options(v)
    out.append(r"\textbf{(c)}~" + mcqc_stem(v) + r"\par\vspace{0.8mm}")
    out.append(options_grid(["$%s$" % o for o in opts], key, solved, "row"))
    if solved:
        out.append(r"\Sol{\textbf{Answer: %s.} %s}" % (LETTERS[key], mcqc_explanation(v, short=True)))
    out.append(gap)
    # (d)
    opts, key = mcqd_options(v)
    out.append(r"\textbf{(d)}~" + mcqd_stem(v) + r"\par\vspace{0.8mm}")
    out.append(options_grid(opts, key, solved, "grid"))
    if solved:
        out.append(r"\Sol{\textbf{Answer: %s.} %s}" % (LETTERS[key], short_until(Q.MCQD[v]["why"], "linearly independent")))
    return "\n".join(out)

def page_one(v, solved):
    body = (tf_block(v, solved) + "\n" +
            (r"\vspace{3mm}\textcolor{RuleGray}{\rule{\linewidth}{0.4pt}}\par\vspace{2mm}" if not solved else r"\vspace{1.5mm}\textcolor{RuleGray}{\rule{\linewidth}{0.4pt}}\par\vspace{1mm}") + "\n" +
            mcq_block(v, solved) + "\n")
    if solved:
        body = r"\begingroup\fontsize{11.5}{13.5}\selectfont" + "\n" + body + r"\endgroup" + "\n"
    return r"\HeaderOne{%s}" % v + "\n" + body + r"\newpage" + "\n"

def page_two(v, solved, nlines=12):
    intro, parts = written_stem(v)
    out = [r"\HeaderTwo{%s}" % v,
           r"\PTitle{Problem 3. Linear independence and span}{%s marks}" % mk(S["written_total"]),
           r"\vspace{1.5mm}" + intro,
           r"\begin{enumerate}[label=\textbf{(\alph*)},leftmargin=9mm,itemsep=1.5mm,topsep=2mm]",
           r"\item \textbf{[%s marks]} %s" % (mk(S["written_a"]), parts[0]),
           r"\item \textbf{[%s marks]} %s" % (mk(S["written_b"]), parts[1]),
           r"\end{enumerate}"]
    if not solved:
        out.append(r"\vspace{2mm}\textbf{Working:}\par\vspace{5.5mm}")
        out.append((r"\workline\vspace{6.6mm}" + "\n") * (nlines - 1) + r"\workline")
    else:
        sol, key_a, key_b, _, _ = written_solution(v)
        out.append(r"\vspace{1mm}{\fontsize{10.5}{12.5}\selectfont\color{WorkBlue}\setlength{\abovedisplayskip}{3pt}\setlength{\belowdisplayskip}{3pt}")
        out.append(r"\textbf{Solution.}\par\vspace{1mm}")
        out.append(sol)
        out.append(r"\par\vspace{1mm}{\fontsize{8.5}{10}\selectfont\color{black!60}Source: " + Q.src("ex4.4.1" if Q.WRITTEN[v]["space"] == "R3" else "ex4.4.2", "ex4.2.10", "ex4.2.11", "def4.4.1", "def4.3.1") +
                   r" ($\mathtt{" + Q.NOTES.replace("_", r"\_") + r"}$). New vectors/polynomials; method, structure and hypotheses unchanged.}")
        out.append("}")
    out.append(r"\newpage")
    return "\n".join(out)

def quiz_document(mode):
    solved = (mode == "solved")
    title = "MATH 231 %s Sections 4.1-4.4 -- %s -- Versions A-J" % (S["quiz_label"], "Student paper" if not solved else "Instructor solved copy")
    doc = [preamble(mode),
           r"\hypersetup{pdftitle={%s},pdfauthor={%s},pdfsubject={MATH 231 %s; %s; versions A--J}}" % (title, S["instructor"], S["quiz_label"], S["scope"]),
           r"\begin{document}"]
    for v in Q.VERSIONS:
        doc.append(r"\pdfbookmark[0]{Version %s}{version-%s}" % (v, v))
        doc.append(page_one(v, solved))
        doc.append(r"\pdfbookmark[1]{Version %s: Problem 3}{written-%s}" % (v, v))
        doc.append(page_two(v, solved))
    doc[-1] = doc[-1].rsplit(r"\newpage", 1)[0]   # no trailing blank page
    doc.append(r"\end{document}")
    return "\n".join(doc)

# ------------------------------------------------------------------ RUBRIC document
PREAMBLE_RUBRIC = r"""\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb}
\usepackage{newtxtext,newtxmath}
\usepackage[a4paper,top=16mm,bottom=16mm,left=16mm,right=16mm]{geometry}
\usepackage{xcolor,graphicx,array,tabularx,booktabs,longtable,enumitem,fancyhdr,colortbl,needspace}
\usepackage[hidelinks]{hyperref}
\definecolor{Brand}{RGB}{0,90,170}
\definecolor{WorkBlue}{HTML}{174CA0}
\setlength{\parindent}{0pt}\setlength{\parskip}{4pt}
\emergencystretch=1.5em
\pagestyle{fancy}\fancyhf{}
\renewcommand{\headrulewidth}{0.3pt}
\fancyhead[L]{\small Math 231 -- %(quiz)s (%(scope)s) -- Detailed rubric, versions A--J}
\fancyhead[R]{\small\textcolor{red!70!black}{INSTRUCTOR ONLY}}
\fancyfoot[C]{\small Page \thepage}
\newcommand{\Conclude}[1]{\par\noindent\fcolorbox{WorkBlue}{blue!4}{\textbf{\textcolor{WorkBlue}{#1}}}\par}
\newcommand{\Src}[1]{{\footnotesize\color{black!65}Source: #1}}
\hypersetup{pdftitle={MATH 231 %(quiz)s Sections 4.1-4.4 -- Detailed rubric -- Versions A-J},pdfauthor={%(instructor)s}}
"""

def esc(s):
    return s.replace("_", r"\_")

def rubric_document():
    doc = [PREAMBLE_RUBRIC % dict(quiz=S["quiz_label"], scope=S["scope"], instructor=S["instructor"]), r"\begin{document}"]
    doc.append(r"{\LARGE\bfseries\textcolor{Brand}{Math 231 -- Linear Algebra: %s, %s}}\par" % (S["quiz_label"], S["scope"]))
    doc.append(r"{\large Detailed marking rubric and answer keys, versions A--J}\par\vspace{2mm}")
    doc.append(r"\textbf{Course:} %s, %s, %s. \quad \textbf{Instructor:} %s. \quad \textbf{Term:} %s. \quad \textbf{Date:} %s. \quad \textbf{Time allowed:} %s.\par" % (S["course"], S["university"], S["department"], S["instructor"], S["term"], S["date"], S["time_limit"]))
    doc.append(r"\textbf{Scope:} %s. \quad \textbf{Maximum marks:} %s per version. \quad \textbf{Authorized source:} the Math 231 Overleaf project notes, file %s, lines 10672--13885 (Chapter 4, Sections 4.1--4.4), and the Chapter 4 Beamer deck.\par" % (S["scope_long"], S["total"], r"\url{" + Q.NOTES + "}"))
    doc.append(r"\section*{1. Structure and marking conventions}")
    doc.append(r"""\begin{itemize}[leftmargin=5mm,itemsep=1pt]
\item \textbf{Problem 1 (True/False, 4 statements $\times$ %s = %s marks).} One statement from each of Sections 4.1, 4.2, 4.3, 4.4. Full credit for a single clearly ticked correct box; zero for a blank, for two ticks, or for the wrong box. No justification is required and none is marked.
\item \textbf{Problem 2 (Multiple choice, 4 questions $\times$ %s = %s marks).} (a) Section 4.1: identify the single failing vector-space axiom; (b) Section 4.2: Subspace Test; (c) Section 4.3: membership in a span; (d) Section 4.4: Wronskian computation and interpretation. Exactly one option is correct; a question with more than one option ticked receives zero (course policy, as on the midterm).
\item \textbf{Problem 3 (written, %s marks).} Part (a) linear independence/dependence of three vectors (polynomials) [%s]; part (b) membership of a given vector in $\operatorname{span}(S)$ [%s]. Marked with the eight evidence checkpoints a1--a5, b1--b3 below (same structure and maxima in every version). Any mathematically valid method within Sections 1.1--2.3 and 4.1--4.4 (row reduction, determinant criterion, Cramer's rule, an explicit verified dependence relation) earns the corresponding checkpoints.
\item \textbf{Follow-through.} An arithmetic slip is penalized once, at the checkpoint where it occurs; later checkpoints are awarded if the subsequent logic is valid for the (incorrect) numbers obtained. A bare final classification with no supporting work earns a5 (or b3) only when the stated reason is itself valid (e.g. an explicit nontrivial relation).
\item \textbf{Equivalent forms.} Accept vectors written as rows or columns, any order of elementary row operations, REF or RREF, and the polynomial/coefficient-vector identification $a+bx+cx^2\leftrightarrow(a,b,c)$.
\item \textbf{Design note.} In every version the written problem has the same two-part structure; versions A, D, E, H, I have a linearly dependent $S$ with $\mathbf{u}\notin\operatorname{span}(S)$, and versions B, C, F, G, J have a linearly independent $S$ with $\mathbf{u}\in\operatorname{span}(S)$ (unique integer coefficients). Workload is comparable: a $3\times3$ elimination in both parts, with back-substitution (independent versions) or an inconsistency check (dependent versions).
\end{itemize}""" % (mk(S["tf_each"]), mk(S["tf_each"]*S["tf_count"]), mk(S["mcq_each"]), mk(S["mcq_each"]*S["mcq_count"]), mk(S["written_total"]), mk(S["written_a"]), mk(S["written_b"])))
    # master grid
    doc.append(r"\section*{2. Master answer grid}")
    doc.append(r"{\small\begin{tabularx}{\linewidth}{@{}c cccc cccc l X@{}}\toprule")
    doc.append(r"Ver. & 1(a) & 1(b) & 1(c) & 1(d) & 2(a) & 2(b) & 2(c) & 2(d) & 3(a) & 3(b) \\\midrule")
    grid_rows = []
    for v in Q.VERSIONS:
        tfk = ["T" if Q.TF[i]["ans"] else "F" for i in Q.TF_ASSIGN[v]]
        ka = LETTERS[mcqa_options(v)[1]]; kb = LETTERS[mcqb_options(v)[1]]; kc = LETTERS[mcqc_options(v)[1]]; kd = LETTERS[mcqd_options(v)[1]]
        _, key_a, key_b, _, _ = written_solution(v)
        short_a = "dependent" if Q.WRITTEN[v]["family"] == "D" else "independent"
        if Q.WRITTEN[v]["family"] == "D":
            short_b = r"no: $\mathbf{u}\notin\operatorname{span}(S)$ (inconsistent row)"
        else:
            short_b = r"yes: $(k_1,k_2,k_3)=(%s)$" % ",".join(str(c) for c in Q.WRITTEN[v]["coeffs"])
        grid_rows.append((v, tfk, ka, kb, kc, kd, short_a, short_b))
        doc.append(r"\textbf{%s} & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s \\" % (v, tfk[0], tfk[1], tfk[2], tfk[3], ka, kb, kc, kd, short_a, short_b))
    doc.append(r"\bottomrule\end{tabularx}}")
    doc.append(r"\section*{3. Checkpoints for Problem 3 (identical in all versions)}")
    doc.append(r"\begin{tabularx}{\linewidth}{@{}l r X X@{}}\toprule Check & Marks & Required evidence & Accepted alternatives / notes\\\midrule")
    for cid, marks, ev, alt in Q.CHECKPOINTS:
        doc.append(r"%s & %s & %s & %s\\" % (cid, mk(marks), ev, alt))
    doc.append(r"\midrule Total & %s & & \\\bottomrule\end{tabularx}" % mk(S["written_total"]))
    doc.append(r"\section*{4. Notes on the source (instructor information)}")
    doc.append(r"""\begin{itemize}[leftmargin=5mm,itemsep=1pt]
\item The A4 notes' solution to \textbf{Example 4.4.3} (line 13467) is a copy of the Example 4.4.4 solution: it speaks of ``$r=5$ polynomials'' and ``Fact 4.4.1(2)'' although the example has four vectors in $\mathbb{R}^3$; the correct argument is $r=4>n=3$ by Fact 4.4.1(1), as printed in the Beamer deck. No quiz item depends on the erroneous text.
\item In \textbf{Extra Problems 4.2.7} (line 12202) the sentence ``The set is linearly dependent (4 equations, 3 unknowns, consistent with a zero row)'' is not justified by the computation: the coefficient matrix has three pivots, so $\{M_1,M_2,M_3\}$ is linearly independent; the zero row only reflects that four equations were used for three unknowns. The quiz does not use this remark.
\item \textbf{Extra Problems 4.3.2 and 4.3.4} (lines 12992, 13115) are the same problem with the same set $S$. Both were treated as one source item.
\item The notes write $P_n$ in Sections 4.2--4.3 and $\mathbb{P}_n$ in Section 4.4; the quiz uses $P_n$ throughout, as in the definition box (line 11369).
\end{itemize}""")
    # per version
    for v in Q.VERSIONS:
        doc.append(r"\clearpage\section*{Version %s}" % v)
        doc.append(r"\subsection*{Problem 1 -- True/False (%s mark each)}" % mk(S["tf_each"]))
        doc.append(r"\begin{tabularx}{\linewidth}{@{}l >{\raggedright\arraybackslash}X l >{\raggedright\arraybackslash}X@{}}\toprule & Statement & Key & Reason / source\\\midrule")
        for letter, t in tf_items(v):
            doc.append(r"(%s) & %s & \textbf{%s} & %s \Src{%s}\\\addlinespace" % (letter, t["text"], "TRUE" if t["ans"] else "FALSE", t["reason"], Q.src(*t["srcs"])))
        doc.append(r"\bottomrule\end{tabularx}")
        doc.append(r"\subsection*{Problem 2 -- Multiple choice (%s mark each)}" % mk(S["mcq_each"]))
        # (a)
        opts, key = mcqa_options(v); d = Q.MCQA[v]
        doc.append(r"\Needspace{12\baselineskip}\textbf{(a)} " + mcqa_stem(v) + r"\par")
        doc.append(r"\begin{itemize}[leftmargin=8mm,itemsep=0pt]" + "".join(r"\item[%s%s] %s" % (LETTERS[i], r"$^{\ast}$" if i == key else "", o) for i, o in enumerate(opts)) + r"\end{itemize}")
        doc.append(r"\textbf{Key: %s (Axiom %d).} %s\par" % (LETTERS[key], d["fails"], d["test"]))
        doc.append(r"\Src{%s. Adaptation: %s}\par" % (Q.src("ex4.1.3", "ex4.1.4", "def4.1.1"), d["adapt"]))
        # (b)
        opts, key = mcqb_options(v); d = Q.MCQB[v]
        doc.append(r"\Needspace{12\baselineskip}\textbf{(b)} " + mcqb_stem(v) + r"\par")
        doc.append(r"\begin{itemize}[leftmargin=8mm,itemsep=0pt]" + "".join(r"\item[%s%s] %s --- %s %s" % (LETTERS[i], r"$^{\ast}$" if i == key else "", o[0], r"\textbf{subspace.}" if o[1] else r"\textbf{not a subspace.}", o[2]) for i, o in enumerate(d["options"])) + r"\end{itemize}")
        doc.append(r"\textbf{Key: %s.} \Src{%s. Adaptation: %s}\par" % (LETTERS[key], Q.src(*d["srcs"]), d["adapt"]))
        # (c)
        opts, key = mcqc_options(v); d = Q.MCQC[v]
        doc.append(r"\Needspace{12\baselineskip}\textbf{(c)} " + mcqc_stem(v) + r"\par")
        doc.append(r"\begin{itemize}[leftmargin=8mm,itemsep=0pt]" + "".join(r"\item[%s%s] $%s$" % (LETTERS[i], r"$^{\ast}$" if i == key else "", o) for i, o in enumerate(opts)) + r"\end{itemize}")
        doc.append(r"\textbf{Key: %s.} %s\par" % (LETTERS[key], mcqc_explanation(v)))
        doc.append(r"\Src{%s. Adaptation: new generators and candidates; same method as the notes.}\par" % Q.src("def4.3.1", "ex4.2.10", "ex4.2.11", "ex4.2.12"))
        # (d)
        opts, key = mcqd_options(v); d = Q.MCQD[v]
        doc.append(r"\Needspace{12\baselineskip}\textbf{(d)} " + mcqd_stem(v) + r"\par")
        doc.append(r"\begin{itemize}[leftmargin=8mm,itemsep=0pt]" + "".join(r"\item[%s%s] %s" % (LETTERS[i], r"$^{\ast}$" if i == key else "", o) for i, o in enumerate(opts)) + r"\end{itemize}")
        doc.append(r"\textbf{Key: %s.} %s\par" % (LETTERS[key], d["why"]))
        doc.append(r"\Src{%s. Adaptation: new pair of functions ($2\times2$ Wronskian); same test and interpretation as the notes.}\par" % Q.src("def4.4.2", "fact4.4.2", "remW", "ex4.4.5", "ex4.4.7"))
        # Problem 3
        intro, parts = written_stem(v)
        sol, key_a, key_b, final0, finalu = written_solution(v, for_rubric=True)
        doc.append(r"\subsection*{Problem 3 -- Written (%s marks)}" % mk(S["written_total"]))
        doc.append(intro + r"\par (a) [%s] %s\par (b) [%s] %s\par" % (mk(S["written_a"]), parts[0], mk(S["written_b"]), parts[1]))
        doc.append(r"\textbf{Model solution.}\par{\color{WorkBlue}" + sol + "}")
        doc.append(r"\textbf{Version-specific marking guide.}\par")
        fam = Q.WRITTEN[v]["family"]
        ref0 = rowred.matrix_tex(final0, 3); refu = rowred.matrix_tex(finalu, 3)
        doc.append(r"\begin{tabularx}{\linewidth}{@{}l r >{\raggedright\arraybackslash}X@{}}\toprule Check & Marks & What to look for in this version\\\midrule")
        doc.append(r"a1 & 0.5 & Vector equation / coefficient matching set up with unknowns $k_1,k_2,k_3$ and right-hand side $%s$.\\" % ZERO[Q.WRITTEN[v]["space"]])
        doc.append(r"a2 & 0.5 & The system shown in the model solution (or its augmented matrix). Row/column transposition accepted.\\")
        doc.append(r"a3 & 0.5 & Zeros below the first pivot with correct operations (any valid pivot choice).\\")
        doc.append(r"a4 & 0.5 & A correct row echelon form, e.g. $%s$ (any row-equivalent REF/RREF accepted)%s.\\" % (ref0, r"; or $\det(A)=0$" if fam == "D" else r"; or $\det(A)\neq0$ computed correctly"))
        if fam == "D":
            doc.append(r"a5 & 0.5 & Conclusion \textbf{linearly dependent} with reason (zero row / free variable / nontrivial solution / $\det=0$). An explicit verified relation such as %s is a complete justification.\\" % key_a.replace("linearly dependent (zero row; ", "").rstrip(")"))
        else:
            doc.append(r"a5 & 0.5 & Conclusion \textbf{linearly independent} with reason (three pivots / only the trivial solution / $\det\neq0$).\\")
        doc.append(r"b1 & 0.5 & System or augmented matrix with right-hand side $%s$ (re-using the matrix of (a) is fine).\\" % elt_tex(Q.WRITTEN[v]["space"], Q.WRITTEN[v]["u"]))
        doc.append(r"b2 & 0.5 & Correct REF of $[A\mid\mathbf{u}]$, e.g. $%s$.\\" % refu)
        if fam == "D":
            Vn = VNAME[Q.WRITTEN[v]["space"]]; Un = UNAME[Q.WRITTEN[v]["space"]]
            doc.append(r"b3 & 0.5 & States that the last row is impossible ($0=%s$), hence $%s\notin\operatorname{span}(S)$. Also accepted: using the dependence relation to note that $\operatorname{span}(S)=\operatorname{span}\{%s,%s\}$ and then showing that the system $k_1%s+k_2%s=%s$ is inconsistent.\\" % (rowred.ftex(finalu[2][3]), Un, Vn[0], Vn[1], Vn[0], Vn[1], Un))
        else:
            doc.append(r"b3 & 0.5 & Correct coefficients and the combination written out: %s. Cramer's rule / inverse matrix accepted.\\" % key_b)
        doc.append(r"\midrule Total & %s & \\\bottomrule\end{tabularx}" % mk(S["written_total"]))
        doc.append(r"\Src{%s. Adaptation: new numbers; the structure (set up, system, reduce, interpret) is exactly the taught method.}\par" % Q.src("ex4.4.1" if Q.WRITTEN[v]["space"] == "R3" else "ex4.4.2", "ex4.2.10", "ex4.2.11", "def4.4.1"))
    doc.append(r"\end{document}")
    return "\n".join(doc)

# ------------------------------------------------------------------ records
def write_records():
    # BLUEPRINT
    bp = [
        ("1(a)", "True/False", S["tf_each"], "4.1", "def4.1.1/thm4.1.1/ex4.1.2", "Recognise vector-space axioms and Theorem 4.1.1 consequences", "single tick", 3, 0.75, "statement", "proofs of axioms", "page 1", "verified"),
        ("1(b)", "True/False", S["tf_each"], "4.2", "thm4.2.1 and Examples 4.2.2-4.2.9, Extra 4.2.1-4.2.6", "Decide subspace status of standard sets; union/intersection", "single tick", 3, 0.75, "statement", "full Subspace Test proof", "page 1", "verified"),
        ("1(c)", "True/False", S["tf_each"], "4.3", "def4.3.1/thm4.3.1/rem4.3.1-2, Extra 4.3.2", "Properties of span and spanning sets", "single tick", 3, 0.75, "statement", "general spanning test", "page 1", "verified"),
        ("1(d)", "True/False", S["tf_each"], "4.4", "thm4.4.1/fact4.4.1/fact4.4.2/remW", "Theorems on independence, dimension argument, Wronskian interpretation", "single tick", 3, 0.75, "statement", "computations", "page 1", "verified"),
        ("2(a)", "MCQ", S["mcq_each"], "4.1", "ex4.1.3/ex4.1.4", "Test scalar-multiplication axioms with a concrete vector; identify the failing axiom", "single tick", 5, 2.0, "operations and the fact that exactly one listed axiom fails", "full ten-axiom verification", "page 1", "verified"),
        ("2(b)", "MCQ", S["mcq_each"], "4.2", "thm4.2.1, Examples 4.2.2-4.2.8, Extra 4.2.1-4.2.6", "Apply the Subspace Test (zero vector, closure) to four subsets", "single tick", 5, 2.5, "four subsets of one space", "written proof", "page 1", "verified"),
        ("2(c)", "MCQ", S["mcq_each"], "4.3", "def4.3.1, ex4.2.10-4.2.12", "Decide membership in span{v1,v2} by matching coefficients", "single tick", 4, 1.5, "two generators, four candidates", "general spanning test", "page 1", "verified"),
        ("2(d)", "MCQ", S["mcq_each"], "4.4", "def4.4.2/fact4.4.2/remW, ex4.4.5-4.4.7", "Compute a 2x2 Wronskian and interpret (not identically zero => independent)", "single tick", 5, 2.0, "two functions", "3x3 Wronskians", "page 1", "verified"),
        ("3", "Written", S["written_total"], "4.4 + 4.2/4.3", "ex4.4.1/ex4.4.2 (independence), ex4.2.10/4.2.11 (membership)", "Row-reduce a 3x3 homogeneous system; interpret pivots/free variables; test membership in a span", "set-up, system, reduction, conclusion, coefficients", 6, 8.0, "three vectors and one target vector", "bases/dimension (4.5-4.6)", "page 2", "verified"),
    ]
    with open(os.path.join(OUT, "BLUEPRINT.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["item_id","question_type","marks","covered_section","source_id","target_skill","student_expected_evidence","difficulty_1_to_10","time_minutes","provided_information","not_assessed","page_assignment","verification_status"])
        w.writerows(bp)
    # VERSION LEDGER + SOURCE MAP + canonical items
    ledger = []; smap = []; canon = {}
    for v in Q.VERSIONS:
        items = {}
        for letter, t in tf_items(v):
            iid = "1(%s)" % letter
            ledger.append((v, iid, t["text"], ";".join(t["srcs"]), "n/a", "TRUE" if t["ans"] else "FALSE", S["tf_each"], "read statement; recall theorem/example", 0.75, "conceptual; balanced keys per version", "PASS"))
            smap.append((v, iid, t["sec"], Q.NOTES, "n/a (TeX source; PDF not compiled here)", "n/a", "; ".join(Q.SRC[s][0] for s in t["srcs"]), "lines " + ", ".join(str(Q.SRC[s][1]) for s in t["srcs"]), "statement paraphrases the source result", "new statement on the source result", ""))
            items[iid] = t["text"]
        opts, key = mcqa_options(v)
        ledger.append((v, "2(a)", mcqa_stem(v) + " | " + " / ".join(opts), "ex4.1.3;ex4.1.4", Q.MCQA[v]["smul_tex"], "%s (Axiom %d)" % (LETTERS[key], Q.MCQA[v]["fails"]), S["mcq_each"], "test 1u=u and (k+m)u; compare", 2.0, "all four listed axioms checked symbolically", "PASS"))
        smap.append((v, "2(a)", "4.1", Q.NOTES, "n/a", "n/a", "Example 4.1.3 / Example 4.1.4", "lines 10977, 11026", "pick a test vector, compute both sides, exhibit the failing axiom", Q.MCQA[v]["adapt"], ""))
        items["2(a)"] = mcqa_stem(v) + " || " + " || ".join(opts)
        opts, key = mcqb_options(v)
        ledger.append((v, "2(b)", mcqb_stem(v) + " | " + " / ".join(opts), ";".join(Q.MCQB[v]["srcs"]), Q.MCQB[v]["V"], LETTERS[key], S["mcq_each"], "zero vector, closure under + and scalar", 2.5, "exactly one option differs in status", "PASS"))
        smap.append((v, "2(b)", "4.2", Q.NOTES, "n/a", "n/a", "; ".join(Q.SRC[s][0] for s in Q.MCQB[v]["srcs"]), "lines " + ", ".join(str(Q.SRC[s][1]) for s in Q.MCQB[v]["srcs"]), "Subspace Test (Theorem 4.2.1) / Remark 4.2.1 counterexamples", Q.MCQB[v]["adapt"], ""))
        items["2(b)"] = mcqb_stem(v) + " || " + " || ".join(opts)
        opts, key = mcqc_options(v)
        ledger.append((v, "2(c)", mcqc_stem(v) + " | " + " / ".join(opts), "def4.3.1;ex4.2.10;ex4.2.11", "v1=%s v2=%s" % (Q.MCQC[v]["v1"], Q.MCQC[v]["v2"]), LETTERS[key], S["mcq_each"], "match two coordinates, check the third", 1.5, "candidates distinct; one member", "PASS"))
        smap.append((v, "2(c)", "4.3", Q.NOTES, "n/a", "n/a", "Definition 4.3.1; Examples 4.2.10-4.2.12", "lines 12614, 11774, 11843, 11899", "write candidate as k1 v1 + k2 v2, solve, check consistency", "new generators/candidates; same method", ""))
        items["2(c)"] = mcqc_stem(v) + " || " + " || ".join(opts)
        opts, key = mcqd_options(v)
        ledger.append((v, "2(d)", mcqd_stem(v) + " | " + " / ".join(opts), "def4.4.2;fact4.4.2;remW", "f1=%s f2=%s" % (Q.MCQD[v]["f1"], Q.MCQD[v]["f2"]), "%s (W=%s)" % (LETTERS[key], Q.MCQD[v]["W_tex"]), S["mcq_each"], "derivatives, 2x2 determinant, interpret", 2.0, "distractors: misconception W(x0)=0, sign error, W=0", "PASS"))
        smap.append((v, "2(d)", "4.4", Q.NOTES, "n/a", "n/a", "Definition 4.4.2; Fact 4.4.2; Remark; Examples 4.4.5-4.4.7", "lines 13526, 13541, 13547, 13617, 13707", "Wronskian determinant; not identically zero => independent", "new pair of functions", ""))
        items["2(d)"] = mcqd_stem(v) + " || " + " || ".join(opts)
        intro, parts = written_stem(v)
        _, key_a, key_b, _, _ = written_solution(v)
        ledger.append((v, "3", intro + " " + parts[0] + " " + parts[1], "ex4.4.1;ex4.4.2;ex4.2.10;ex4.2.11", "vs=%s u=%s" % (Q.WRITTEN[v]["vs"], Q.WRITTEN[v]["u"]), key_a + " | " + key_b, S["written_total"], "set up; system; REF; interpret; membership; coefficients", 8.0, "family %s; integer-only elimination" % Q.WRITTEN[v]["family"], "PASS"))
        smap.append((v, "3", "4.4 (+4.2/4.3)", Q.NOTES, "n/a", "n/a", "Example 4.4.1 / 4.4.2; Examples 4.2.10-4.2.11", "lines 13280, 13357, 11774, 11843", "homogeneous system -> REF -> pivots/free variables; augmented system -> consistency", "new numbers; same structure", ""))
        items["3"] = intro + " || " + parts[0] + " || " + parts[1]
        canon[v] = items
    with open(os.path.join(OUT, "VERSION_LEDGER.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["version","item","final_stem_fingerprint","source_id","variation_parameters","key_or_expected_result","marks","solution_stages","estimated_minutes","fairness_notes","independent_QA_status"])
        w.writerows(ledger)
    with open(os.path.join(OUT, "SOURCE_MAP.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["version","question_id","section","file","pdf_physical_page","printed_page_label","real_example_name","solution_page","source_method","adaptation_disclosure","review_notes"])
        w.writerows(smap)
    with open(os.path.join(OUT, "RUBRIC_CHECKPOINTS.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["version","problem_id","checkpoint_id","required_mathematical_evidence","checkpoint_marks","valid_alternate_evidence","follow_through_rules","source_id"])
        for v in Q.VERSIONS:
            for cid, marks, ev, alt in Q.CHECKPOINTS:
                w.writerow([v, "3", cid, ev, marks, alt, "one deduction per error; follow through when later logic is valid", "ex4.4.1;ex4.4.2;ex4.2.10;ex4.2.11"])
    with open(os.path.join(OUT, "canonical_items.json"), "w", encoding="utf-8") as f:
        json.dump(canon, f, indent=1, ensure_ascii=False)

# ------------------------------------------------------------------ main
if __name__ == "__main__":
    with open(os.path.join(OUT, BASENAME + "_Student_A-J.tex"), "w", encoding="utf-8") as f:
        f.write(quiz_document("student"))
    with open(os.path.join(OUT, BASENAME + "_Solved_A-J.tex"), "w", encoding="utf-8") as f:
        f.write(quiz_document("solved"))
    with open(os.path.join(OUT, BASENAME + "_Rubric_A-J.tex"), "w", encoding="utf-8") as f:
        f.write(rubric_document())
    write_records()
    print("written to", OUT)
