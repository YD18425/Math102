# -*- coding: utf-8 -*-
r"""Exact (Fraction) Gaussian elimination that records every elementary row operation,
in the notation of the Math 231 notes (e.g. "-2R_1+R_2 \to R_2", "R_1 \leftrightarrow R_2").

Pivot policy (mirrors the notes): among the remaining rows with a nonzero entry in the
current column, prefer an entry equal to +-1 (swap it up if needed), otherwise the entry of
smallest absolute value. Rows below the pivot are cleared with  R_j <- R_j - (a_jk/a_kk) R_k.
"""
from fractions import Fraction

def _fr(x):
    return x if isinstance(x, Fraction) else Fraction(x)

def ftex(q):
    q = _fr(q)
    if q.denominator == 1:
        return str(q.numerator)
    s = "-" if q < 0 else ""
    return r"%s\tfrac{%d}{%d}" % (s, abs(q.numerator), q.denominator)

def coef_tex(q, var):
    """q*var with nice signs for an operation label, e.g. -2R_1, R_1, \tfrac12 R_1."""
    q = _fr(q)
    if q == 1: return var
    if q == -1: return "-" + var
    return ftex(q) + var

def matrix_tex(M, ncoef):
    """Augmented matrix [A | b] where the first ncoef columns are coefficients."""
    rows = []
    for r in M:
        rows.append(" & ".join(ftex(x) for x in r))
    cols = "c" * ncoef + ("|" + "c" * (len(M[0]) - ncoef) if len(M[0]) > ncoef else "")
    return r"\left[\begin{array}{%s} %s \end{array}\right]" % (cols, r" \\ ".join(rows))

def reduce_record(A, ncoef):
    """Return (steps, final) where steps = list of (ops_tex_list, matrix_after) and the
    starting matrix is A (list of lists of ints/Fractions). Only the first ncoef columns
    are used to choose pivots."""
    M = [[_fr(x) for x in row] for row in A]
    m = len(M)
    steps = []
    prow = 0
    pivots = []
    for col in range(ncoef):
        if prow >= m:
            break
        cand = [i for i in range(prow, m) if M[i][col] != 0]
        if not cand:
            continue
        ones = [i for i in cand if abs(M[i][col]) == 1]
        if ones:
            pr = ones[0]
        else:
            pr = min(cand, key=lambda i: (abs(M[i][col]), i))
        ops = []
        if pr != prow:
            M[prow], M[pr] = M[pr], M[prow]
            ops.append(r"R_%d \leftrightarrow R_%d" % (prow + 1, pr + 1))
            steps.append((ops, [r[:] for r in M]))
            ops = []
        piv = M[prow][col]
        for i in range(prow + 1, m):
            if M[i][col] != 0:
                mult = M[i][col] / piv          # R_i <- R_i - mult * R_prow
                M[i] = [a - mult * b for a, b in zip(M[i], M[prow])]
                ops.append(r"%s+R_%d \to R_%d" % (coef_tex(-mult, "R_%d" % (prow + 1)), i + 1, i + 1))
        if ops:
            steps.append((ops, [r[:] for r in M]))
        pivots.append((prow, col))
        prow += 1
    return steps, M, pivots

def chain_tex(A, ncoef, per_line=2):
    """Full display chain: start matrix, arrows with stacked operations, result matrices.
    Returns a list of TeX display lines (each to be wrapped in \\[ ... \\])."""
    steps, final, pivots = reduce_record(A, ncoef)
    items = [matrix_tex(A, ncoef)]
    for ops, M in steps:
        if len(ops) == 1:
            arrow = r"\xrightarrow{%s}" % ops[0]
        else:
            # first operation above the arrow, the rest below (notes' style)
            arrow = r"\xrightarrow[%s]{%s}" % (r"\;".join(ops[1:]), ops[0])
        items.append(arrow + " " + matrix_tex(M, ncoef))
    lines = []
    cur = items[0]
    count = 0
    for it in items[1:]:
        cur += " " + it
        count += 1
        if count == per_line:
            lines.append(cur)
            cur = r"\phantom{\left[\begin{array}{c}0\end{array}\right]}"  # continuation indent placeholder
            cur = ""
            count = 0
    if cur:
        lines.append(cur)
    return lines, final, pivots

def is_integer_matrix(M):
    return all(_fr(x).denominator == 1 for r in M for x in r)
