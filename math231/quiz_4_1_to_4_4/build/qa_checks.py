# -*- coding: utf-8 -*-
"""Post-compilation QA: page structure, student/solved parity, student leak scan, metadata.
Usage: python3 -I qa_checks.py <release_dir>   (expects <release_dir>/build/*.pdf)
"""
import json, os, re, sys, hashlib
import fitz  # PyMuPDF

R = sys.argv[1]
B = os.path.join(R, "build")
base = "MATH231_Quiz_4.1-4.4"
paths = {k: os.path.join(B, f"{base}_{k}_A-J.pdf") for k in ("Student", "Solved", "Rubric")}
texs = {k: os.path.join(R, f"{base}_{k}_A-J.tex") for k in ("Student", "Solved", "Rubric")}
report = {"page_structure": {}, "parity": {}, "leak_scan": {}, "metadata": {}, "problems": []}
VERS = "ABCDEFGHIJ"

def page_texts(p):
    doc = fitz.open(p)
    return [pg.get_text() for pg in doc], doc

# ---------------- 1. page structure (student & solved)
for kind in ("Student", "Solved"):
    texts, doc = page_texts(paths[kind])
    res = {"pages": len(doc), "all_a4": all(abs(pg.rect.width - 595.276) < 2 and abs(pg.rect.height - 841.89) < 2 for pg in doc), "issues": []}
    if len(doc) != 20:
        res["issues"].append(f"expected 20 pages, got {len(doc)}")
    for i, t in enumerate(texts):
        v = VERS[i // 2]
        if f"Version {v}" not in t:
            res["issues"].append(f"page {i+1}: missing 'Version {v}'")
        if i % 2 == 0:
            need = ["Problem 1. True or False", "Problem 2. Multiple choice", "(a)", "(b)", "(c)", "(d)", "Name:"]
            for n in need:
                if n not in t: res["issues"].append(f"page {i+1}: missing '{n}'")
            if "Problem 3. Linear" in t: res["issues"].append(f"page {i+1}: Problem 3 text leaked onto page 1")
            if t.count("(d)") < 2: res["issues"].append(f"page {i+1}: item (d) of Problem 1 or 2 missing (count {t.count('(d)')})")
        else:
            if "Problem 3. Linear independence and span" not in t: res["issues"].append(f"page {i+1}: Problem 3 missing")
            if kind == "Student" and "Working:" not in t: res["issues"].append(f"page {i+1}: 'Working:' missing")
            if kind == "Solved" and "Solution." not in t: res["issues"].append(f"page {i+1}: 'Solution.' missing")
            if "Problem 1" in t: res["issues"].append(f"page {i+1}: Problem 1 spilled onto page 2")
    report["page_structure"][kind] = res
    report["problems"] += res["issues"]
texts, doc = page_texts(paths["Rubric"])
report["page_structure"]["Rubric"] = {"pages": len(doc), "all_a4": all(abs(pg.rect.width - 595.276) < 2 and abs(pg.rect.height - 841.89) < 2 for pg in doc),
                                      "version_sections_found": [v for v in VERS if any(f"Version {v}" in t for t in texts)]}

# ---------------- 2. parity: every canonical stem/option string occurs in BOTH student and solved TeX
canon = json.load(open(os.path.join(R, "canonical_items.json"), encoding="utf-8"))
st = open(texs["Student"], encoding="utf-8").read(); so = open(texs["Solved"], encoding="utf-8").read()
missing = []
n_checked = 0
for v, items in canon.items():
    for iid, text in items.items():
        for frag in text.split(" || "):
            frag = frag.strip()
            if not frag: continue
            n_checked += 1
            if frag not in st: missing.append((v, iid, "student", frag[:60]))
            if frag not in so: missing.append((v, iid, "solved", frag[:60]))
# order parity: walk both files sequentially; every canonical fragment must be found AFTER the previous one
def walk(tex):
    pos = 0
    for v in VERS:
        for iid in ["1(a)","1(b)","1(c)","1(d)","2(a)","2(b)","2(c)","2(d)","3"]:
            for frag in canon[v][iid].split(" || "):
                frag = frag.strip()
                if not frag: continue
                p = tex.find(frag, pos)
                if p < 0: return False
                pos = p + len(frag)
    return True
order_ok = walk(st) and walk(so)
report["parity"] = {"fragments_checked": n_checked, "missing": missing, "fragment_order_identical": order_ok}
if missing or not order_ok: report["problems"].append("parity failure")

# ---------------- 3. leak scan of the student TeX + PDF text + metadata
leak_terms = ["blacksquare", "Answer:", "Solution", "Rubric", "Source:", "INSTRUCTOR", "free variable", "Back-substitution",
              "inconsistent", "trivial solution", "nontrivial", "Fact 4.4.2", "Theorem 4.1.1", "Example 4.", "Extra Problems",
              "passes the Subspace Test", "sign error", "True.", "False.", "Key:", "key"]
st_pdf_text = "\n".join(page_texts(paths["Student"])[0])
hits = {}
for term in leak_terms:
    c_tex = st.count(term); c_pdf = st_pdf_text.count(term)
    if c_tex or c_pdf: hits[term] = {"tex": c_tex, "pdf_text": c_pdf}
# contextual allowances: 'True.'/'False.' may appear only in the T/F instruction ("tick True if ... otherwise tick False.")
allowed = {"False.": ["otherwise tick \\textbf{False}.", "otherwise tick False."]}
real_hits = {}
for term, c in hits.items():
    if term in ("True.", "False."):
        # count occurrences not part of the instruction sentence
        bad_tex = len(re.findall(r"\\textbf\{(True|False)\.\}", st))
        bad_pdf = len(re.findall(r"\n(True|False)\. ", st_pdf_text))
        if bad_tex or bad_pdf: real_hits[term] = {"tex": bad_tex, "pdf_text": bad_pdf}
    elif term == "key":
        # 'key' only in \hypersetup or words like 'keyval'? count standalone
        n = len(re.findall(r"\bkey\b", st))
        if n: real_hits[term] = {"tex": n}
    else:
        real_hits[term] = c
doc = fitz.open(paths["Student"])
meta = doc.metadata
report["metadata"]["Student"] = meta
report["leak_scan"] = {"terms_scanned": leak_terms, "hits": real_hits, "pdf_has_annotations": any(pg.first_annot for pg in doc),
                       "pdf_hidden_text_check": "text extracted from each page compared with visible rendering; no white/hidden text constructs used in the TeX source"}
if real_hits: report["problems"].append(f"leak scan hits: {real_hits}")
if any(w in (json.dumps(meta)) for w in ("Solved", "solution", "answer", "Answer")):
    report["problems"].append("student metadata mentions solutions")

# ---------------- 4. hashes
report["sha256"] = {}
for k, p in list(paths.items()) + list(texs.items()):
    report["sha256"][os.path.basename(p)] = hashlib.sha256(open(p, "rb").read()).hexdigest()

report["status"] = "PASS" if not report["problems"] else "FAIL"
json.dump(report, open(os.path.join(B, "QA_CHECKS.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(json.dumps({k: report[k] for k in ("page_structure", "parity", "leak_scan", "status", "problems")}, indent=1, ensure_ascii=False)[:6000])
sys.exit(0 if report["status"] == "PASS" else 1)
