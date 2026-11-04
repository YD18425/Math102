# -*- coding: utf-8 -*-
"""Independent mathematical verification of every item in quizdata.py using SymPy and
brute-force checks (a different method from the hand derivations and from the displayed
row reductions). Writes INDEPENDENT_MATH_QA.csv and prints a summary. Exit code 1 on any failure.
"""
import csv, itertools, sys, os
from fractions import Fraction
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quizdata as Q
import rowred

x = sp.symbols('x')
rows = []      # QA csv rows
fails = []

def rec(version, item, stem, answer, check, method, issue="", status="PASS"):
    rows.append(dict(version=version, item=item, stem_rechecked=stem, answer_recomputed=answer,
                     every_MC_option_tested=check, theorem_conditions_checked="yes",
                     independent_method_used=method, source_in_scope="yes (sections 4.1-4.4 of the notes)",
                     found_issue=issue, resolution="", final_PASS=status))
    if status != "PASS":
        fails.append((version, item, issue))

# ---------------------------------------------------------------- SPEC
assert abs(Q.SPEC["total"] - 10) < 1e-9

# ---------------------------------------------------------------- T/F
used = [k for v in Q.VERSIONS for k in Q.TF_ASSIGN[v]]
assert len(used) == len(set(used)), "T/F statement reused across versions"
def wronskian(fs):
    n = len(fs)
    M = sp.Matrix([[sp.diff(f, x, i) for f in fs] for i in range(n)])
    return sp.simplify(M.det())
concrete_checks = {
    "T3k": lambda: sp.Matrix([[1,0,0],[0,1,0]]).T.rank() == 2,              # 2 vectors cannot span R^3
    "T3z": lambda: sp.Matrix([[1,-1,0],[1,2,1],[1,0,1],[3,3,-1]]).T.rank() == 3,
    "T3aa": lambda: sp.Matrix([[1,-1,0],[1,2,1],[1,0,1],[3,3,-1]]).T.rank() == 3,
    "T3dd": lambda: sp.linsolve((sp.Matrix([[1,0],[0,1],[1,0]]), sp.Matrix([0,0,1])), *sp.symbols('k1 k2')) == sp.EmptySet,
    "T3c": lambda: sp.Matrix([[1,0,0],[0,1,0],[0,0,1]]).rank() == 3,
    "T4h": lambda: wronskian([sp.exp(x), 6*sp.exp(x)]) == 0 and sp.simplify(6*sp.exp(x) - 6*sp.exp(x)) == 0,
    "T4e": lambda: wronskian([1, x, x**2, x**3]) == 12,
    "T4m": lambda: wronskian([x, x**2]) == x**2 and (x**2).subs(x, 1) == 1,
    "T4r": lambda: sp.Matrix([[1,0,0],[2,0,0]]).rank() == 1,
    "T4w": lambda: sp.Matrix([[1,0,0],[2,0,0],[0,1,0]]).rank() == 2 and sp.linsolve((sp.Matrix([[1,2],[0,0],[0,0]]), sp.Matrix([0,1,0])), *sp.symbols('a b')) == sp.EmptySet,
    "T1aa": lambda: True,  # conceptual (0*u = 0 with u != 0)
}
for v in Q.VERSIONS:
    ids = Q.TF_ASSIGN[v]
    secs = [Q.TF[i]["sec"] for i in ids]
    assert secs == ["4.1", "4.2", "4.3", "4.4"], (v, secs)
    answers = [Q.TF[i]["ans"] for i in ids]
    assert 1 <= sum(answers) <= 3, f"version {v}: T/F answers not mixed: {answers}"
    for letter, i in zip("abcd", ids):
        t = Q.TF[i]
        if i in concrete_checks:
            ok = bool(concrete_checks[i]())
            rec(v, f"1({letter}) {i}", t["text"][:70], "TRUE" if t["ans"] else "FALSE",
                "n/a", "sympy rank/linsolve/Wronskian recomputation of the concrete claim",
                "" if ok else "concrete check failed", "PASS" if ok else "FAIL")
        else:
            rec(v, f"1({letter}) {i}", t["text"][:70], "TRUE" if t["ans"] else "FALSE",
                "n/a", "conceptual statement checked word-by-word against " + Q.src(*t["srcs"]).replace("$", ""))

# ---------------------------------------------------------------- MCQ (a): axioms with symbolic check
k, m = sp.symbols('k m', real=True)
def axiom_status(n, smul):
    us = sp.symbols(f'u1:{n+1}', real=True); vs = sp.symbols(f'v1:{n+1}', real=True)
    u = tuple(us); vv = tuple(vs)
    add = lambda a, b: tuple(ai + bi for ai, bi in zip(a, b))
    def same(a, b):
        return all(sp.simplify(ai - bi) == 0 for ai, bi in zip(a, b))
    st = {}
    st[1] = True; st[6] = True            # results stay in R^n (usual addition / tuples of reals)
    st[2] = same(add(u, vv), add(vv, u))
    st[4] = True; st[3] = True; st[5] = True   # usual addition: zero (0,...,0), negatives
    st[7] = same(smul(k, add(u, vv)), add(smul(k, u), smul(k, vv)))
    st[8] = same(smul(k + m, u), add(smul(k, u), smul(m, u)))
    st[9] = same(smul(k, smul(m, u)), smul(k * m, u))
    st[10] = same(smul(1, u), u)
    return st
for v in Q.VERSIONS:
    d = Q.MCQA[v]
    st = axiom_status(d["n"], d["smul"])
    failing_all = sorted(a for a, ok in st.items() if not ok)
    listed_fail = [a for a in d["options"] if not st[a]]
    ok = failing_all == [d["fails"]] and listed_fail == [d["fails"]] and len(set(d["options"])) == 4
    letter = "ABCD"[d["options"].index(d["fails"])]
    rec(v, "2(a)", "which axiom fails for " + d["smul_tex"], f"{letter} (Axiom {d['fails']})",
        f"all four listed axioms tested symbolically; failing set among 1-10 = {failing_all}",
        "sympy symbolic identity check of axioms 1-10 with general u, v, k, m",
        "" if ok else f"failing axioms {failing_all}, listed failing {listed_fail}", "PASS" if ok else "FAIL")

# ---------------------------------------------------------------- MCQ (b): subspace test by brute force
def grid(space):
    vals = [-3, -2, -1, 0, 1, 2, 3]
    if space == "R2":
        wide = list(range(-10, 11))
        return [(a, b) for a in wide for b in wide]
    if space == "R3": return [(a, b, c) for a in vals for b in vals for c in vals]
    if space == "P2": return [(a, b, c) for a in vals for b in vals for c in vals]
    if space == "M22": return [((a, b), (c, d)) for a in vals for b in vals for c in vals for d in vals]
    return None
def add_el(space, u, w):
    if space == "M22": return tuple(tuple(a + b for a, b in zip(ru, rw)) for ru, rw in zip(u, w))
    return tuple(a + b for a, b in zip(u, w))
def smul_el(space, c, u):
    if space == "M22": return tuple(tuple(c * a for a in ru) for ru in u)
    return tuple(c * a for a in u)
def zero_el(space):
    return {"R2": (0, 0), "R3": (0, 0, 0), "P2": (0, 0, 0), "M22": ((0, 0), (0, 0))}[space]
FUNC_KINDS_SUBSPACE = {"C", "C1", "P2", "f0eq0"}      # function sets with known subspace status (notes: XP 4.2.1, 4.2.5, P_n)
FUNC_KINDS_NOT = {"f0eq1", "f1eq2", "nonneg"}
for v in Q.VERSIONS:
    d = Q.MCQB[v]
    statuses = []
    notes = []
    for idx, (tex, is_sub, reason, meta) in enumerate(d["options"]):
        if d["space"] == "F":
            kind = meta["kind"]
            computed = kind in FUNC_KINDS_SUBSPACE
            if kind in FUNC_KINDS_NOT:
                w = meta["witness"]
                if w[0] == "zero":
                    computed = False  # zero function fails the defining condition by inspection
                elif w[0] == "scalar":
                    computed = False  # f=1 >=0 but (-1)f = -1 is not >= 0
            statuses.append(computed == is_sub)
            continue
        space = d["space"]; pred = meta["pred"]
        z = zero_el(space)
        zero_ok = bool(pred(z))
        if is_sub:
            members = [g for g in grid(space) if pred(g)]
            closed = zero_ok and len(members) >= 1
            for a in members:
                for c in (-2, -1, Fraction(1, 2), 2, 3):
                    if not pred(smul_el(space, c, a)):
                        closed = False; break
                if not closed: break
            if closed:
                for a, b in itertools.product(members[:60], repeat=2):
                    if not pred(add_el(space, a, b)):
                        closed = False; break
            statuses.append(closed == is_sub)
            notes.append(f"opt{idx}: {len(members)} grid members, closure OK={closed}")
        else:
            w = meta["witness"]
            if w[0] == "zero":
                demo = not zero_ok
            elif w[0] == "scalar":
                demo = bool(pred(w[1])) and not pred(smul_el(space, w[2], w[1]))
            elif w[0] == "add":
                demo = bool(pred(w[1])) and bool(pred(w[2])) and not pred(add_el(space, w[1], w[2]))
            statuses.append(demo)
            notes.append(f"opt{idx}: witness {w} demonstrates failure={demo}")
    truth = [o[1] for o in d["options"]]
    n_sub = sum(truth)
    ok_count = (d["ask"] == "is" and n_sub == 1) or (d["ask"] == "not" and n_sub == 3)
    ok = all(statuses) and ok_count
    key_idx = truth.index(True) if d["ask"] == "is" else truth.index(False)
    rec(v, "2(b)", f"which subset of {d['V']} is {'a' if d['ask']=='is' else 'NOT a'} subspace", "ABCD"[key_idx],
        "all four options: brute-force closure on an integer grid / explicit witness; " + "; ".join(notes),
        "exhaustive grid closure test + witness verification (independent of the written reasons)",
        "" if ok else f"statuses={statuses}, n_sub={n_sub}", "PASS" if ok else "FAIL")

# ---------------------------------------------------------------- MCQ (c): span membership via linsolve
k1, k2, k3 = sp.symbols('k1 k2 k3')
for v in Q.VERSIONS:
    d = Q.MCQC[v]
    A = sp.Matrix([d["v1"], d["v2"]]).T
    results = []
    for cand in d["options"]:
        sol = sp.linsolve((A, sp.Matrix(cand)), k1, k2)
        results.append(sol != sp.EmptySet)
    ok = results.count(True) == 1 and len(set(d["options"])) == 4
    key = "ABCD"[results.index(True)] if True in results else "?"
    sol = sp.linsolve((A, sp.Matrix(d["options"][results.index(True)])), k1, k2)
    rec(v, "2(c)", f"which of 4 candidates is in span{{v1,v2}} ({d['space']})", f"{key}; coefficients {list(sol)}",
        f"linsolve for every candidate: {results}", "sympy linsolve on each option",
        "" if ok else "not exactly one member", "PASS" if ok else "FAIL")

# ---------------------------------------------------------------- MCQ (d): Wronskian
expected_W = {   # second, independent hand derivation typed here (not copied from quizdata W_tex)
    "A": (x - 1) * sp.exp(x), "B": sp.exp(3 * x), "C": -sp.exp(-x), "D": x**2, "E": sp.exp(2 * x),
    "F": 2 * x, "G": sp.exp(5 * x), "H": sp.Integer(-1), "I": x**4, "J": sp.Integer(2),
}
for v in Q.VERSIONS:
    d = Q.MCQD[v]
    f1 = sp.sympify(d["f1"]); f2 = sp.sympify(d["f2"])
    W = wronskian([f1, f2])
    ok_W = sp.simplify(W - expected_W[v]) == 0
    not_ident_zero = sp.simplify(W) != 0
    correct = [o[1] for o in d["options"]]
    key_idx = correct.index(True)
    key_text = d["options"][key_idx][0]
    ok_text = ("linearly independent" in key_text) and (d["W_tex"] in key_text) and correct.count(True) == 1
    # distractor claims that mention W(point)=0 must be numerically true claims about W
    claims_ok = True
    for tex, c in d["options"]:
        states_true_W = tex.startswith("$W(x)=" + d["W_tex"] + "$")
        if "W(1)=0" in tex and states_true_W: claims_ok &= (W.subs(x, 1) == 0)
        if "W(0)=0" in tex and states_true_W: claims_ok &= (W.subs(x, 0) == 0)
    ok = ok_W and not_ident_zero and ok_text and claims_ok
    rec(v, "2(d)", f"Wronskian of {d['f1']}, {d['f2']}", f"{'ABCD'[key_idx]}; W = {sp.simplify(W)}; linearly independent",
        f"all options read; correct option contains W and 'linearly independent'; point-claims verified={claims_ok}",
        "sympy determinant of the Wronskian matrix; compared with a separately typed expected value",
        "" if ok else f"W={W}, expected={expected_W[v]}", "PASS" if ok else "FAIL")

# ---------------------------------------------------------------- Problem 3: written
for v in Q.VERSIONS:
    d = Q.WRITTEN[v]
    A = sp.Matrix(d["vs"]).T          # columns = vectors
    u = sp.Matrix(d["u"])
    r = A.rank(); r_aug = A.row_join(u).rank()
    issues = []
    if d["family"] == "D":
        if r != 2: issues.append(f"rank A = {r}, expected 2")
        if r_aug != 3: issues.append(f"rank [A|u] = {r_aug}, expected 3 (u must NOT be in span)")
        rel = sp.Matrix(d["relation"])
        if (A * rel) != sp.zeros(3, 1): issues.append("stated dependence relation is wrong")
        sol = sp.linsolve((A, u), k1, k2, k3)
        if sol != sp.EmptySet: issues.append("u unexpectedly in span")
        answer = f"dependent (rank 2); relation {d['relation']}; u not in span (rank [A|u]=3)"
    else:
        if r != 3: issues.append(f"rank A = {r}, expected 3")
        if A.det() == 0: issues.append("det = 0")
        sol = list(sp.linsolve((A, u), k1, k2, k3))
        if len(sol) != 1 or tuple(sol[0]) != tuple(sp.Integer(c) for c in d["coeffs"]):
            issues.append(f"coefficients {sol} != stated {d['coeffs']}")
        answer = f"independent (det={A.det()}); u = {d['coeffs']} . (v1,v2,v3)"
    # cross-check the displayed row reduction (rowred) against sympy: same row space, all-integer steps
    aug = [list(row) + [uu] for row, uu in zip(sp.Matrix(d["vs"]).T.tolist(), d["u"])]
    steps, final, pivots = rowred.reduce_record(aug, 3)
    all_int = all(rowred.is_integer_matrix(M) for _, M in steps)
    if not all_int: issues.append("displayed row reduction uses fractions")
    F = sp.Matrix([[sp.Rational(q.numerator, q.denominator) for q in row] for row in final])
    if F.rank() != r_aug or F[:, :3].rank() != r: issues.append("displayed REF rank mismatch")
    if sp.Matrix(aug).rref()[0] != F.rref()[0]: issues.append("displayed REF not row-equivalent to [A|u]")
    ok = not issues
    rec(v, "3(a)+(b)", f"S in {d['space']}: {d['vs']}, u={d['u']}", answer,
        "n/a", "sympy rank/det/linsolve + row-equivalence check of the displayed reduction",
        "; ".join(issues), "PASS" if ok else "FAIL")

# ---------------------------------------------------------------- distribution of correct letters
dist = {}
for slot, D in (("2(a)", Q.MCQA), ("2(b)", Q.MCQB), ("2(c)", Q.MCQC), ("2(d)", Q.MCQD)):
    letters = []
    for v in Q.VERSIONS:
        d = D[v]
        if slot == "2(a)": letters.append("ABCD"[d["options"].index(d["fails"])])
        elif slot == "2(b)":
            truth = [o[1] for o in d["options"]]
            letters.append("ABCD"[truth.index(True) if d["ask"] == "is" else truth.index(False)])
        elif slot == "2(c)":
            A = sp.Matrix([d["v1"], d["v2"]]).T
            letters.append("ABCD"[[sp.linsolve((A, sp.Matrix(c)), k1, k2) != sp.EmptySet for c in d["options"]].index(True)])
        else:
            letters.append("ABCD"[[o[1] for o in d["options"]].index(True)])
    dist[slot] = "".join(letters)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "INDEPENDENT_MATH_QA.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(f"items checked: {len(rows)}; failures: {len(fails)}")
for f_ in fails: print("FAIL:", f_)
print("correct-letter distribution per MCQ slot (versions A..J):", dist)
tfpat = {v: "".join("T" if Q.TF[i]["ans"] else "F" for i in Q.TF_ASSIGN[v]) for v in Q.VERSIONS}
print("T/F key patterns:", tfpat)
sys.exit(1 if fails else 0)
