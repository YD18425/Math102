#!/usr/bin/env python3
"""Compile three standalone quiz TeX sources and perform objective PDF QA.

This helper DOES NOT replace mathematical review or a page-by-page human visual inspection.
Dependencies: pdflatex, PyMuPDF (fitz), Pillow.
Example:
python scripts/compile_check.py \
  --student-tex release/Quiz_Student.tex \
  --solved-tex release/Quiz_Solved.tex \
  --rubric-tex release/Quiz_Rubric.tex \
  --output-dir release/build --version-ids A,B,C,D,E,F,G,H,I,J \
  --pages-per-version 2

Run from a writable project directory. A returned nonzero code means a release gate failed.
"""
import argparse, hashlib, json, os, re, subprocess, sys, tempfile
from pathlib import Path

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()

def pdf_check(pdf, expected_pages, *, version_ids, per_version, enforce_versions=False):
    import fitz
    doc = fitz.open(str(pdf))
    result = {'file': pdf.name, 'pages': len(doc), 'expected_pages': expected_pages,
              'sha256': sha256(pdf), 'size_bytes': pdf.stat().st_size,
              'a4_pages': [], 'version_label_mismatches': [], 'human_visual_review_required': True}
    for i,p in enumerate(doc):
        is_a4 = abs(p.rect.width - 595.276) < 2 and abs(p.rect.height - 841.89) < 2
        if is_a4: result['a4_pages'].append(i + 1)
        if enforce_versions and per_version and version_ids:
            v = version_ids[i // per_version] if i//per_version < len(version_ids) else None
            if v and not re.search(r'\bversion\s*' + re.escape(v) + r'\b',p.get_text(),re.I):
                result['version_label_mismatches'].append({'page':i+1,'wanted':v})
    result['all_a4'] = len(result['a4_pages']) == len(doc)
    result['page_count_pass'] = expected_pages is None or len(doc) == expected_pages
    result['version_labels_pass'] = len(result['version_label_mismatches']) == 0
    return result

def contact_sheets(pdf, outdir, size=(470, 665), cols=3, rows=2):
    import fitz
    from PIL import Image,ImageOps,ImageDraw,ImageFont
    doc=fitz.open(str(pdf)); outdir.mkdir(parents=True,exist_ok=True)
    page_w,page_h=size; pad=14; label_h=25
    thumbs=[]
    for i,p in enumerate(doc):
        pix=p.get_pixmap(matrix=fitz.Matrix(0.6,0.6),alpha=False)
        im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        im.thumbnail((page_w, page_h),Image.Resampling.LANCZOS)
        thumbs.append((i+1,im))
    out=[]
    group=cols*rows
    for idx in range(0,len(thumbs),group):
        cell_h=page_h+label_h; W=pad+cols*(page_w+pad); H=pad+rows*(cell_h+pad)
        sheet=Image.new('RGB',(W,H),'#eff0f2');d=ImageDraw.Draw(sheet)
        for j,(n,im) in enumerate(thumbs[idx:idx+group]):
            r,c=divmod(j,cols); x=pad+c*(page_w+pad); y=pad+r*(cell_h+pad)
            d.rectangle((x-1,y-1,x+page_w+1,y+page_h+1),fill='white',outline='#a7a7a7',width=1)
            sheet.paste(im,(x+(page_w-im.width)//2,y+(page_h-im.height)//2))
            d.text((x+5,y+page_h+3),f'{pdf.name} | page {n}',fill='#222222')
        dest=outdir/f'{pdf.stem}_contact_{idx//group+1:02d}.png'
        sheet.save(dest,optimize=True);out.append(str(dest))
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for kind in ('student','solved','rubric'):
        p.add_argument(f'--{kind}-tex',required=True,type=Path)
    p.add_argument('--output-dir',type=Path,default=Path('build'))
    p.add_argument('--engine',choices=['pdflatex','xelatex','lualatex'],default='pdflatex')
    p.add_argument('--version-ids',default='',help='Comma separated IDs A,B,C,...')
    p.add_argument('--pages-per-version',type=int,default=2)
    p.add_argument('--expected-rubric-pages',type=int,default=None)
    p.add_argument('--skip-compile',action='store_true',help='Inspect already-compiled PDFs in output-dir')
    p.add_argument('--skip-contact-sheets',action='store_true')
    args=p.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    version_ids=[v.strip() for v in args.version_ids.split(',') if v.strip()]
    result={'status':'HELD','tool':'compile_check.py','source_hashes':{},'files':{},
            'notes':['Automated PDF review is NOT a substitute for a human examination of every page.',
            'Page-size/page-count checks do not prove student/solved text parity, source fidelity or mathematical correctness.',
            'Absence of answer leakage requires a separate manual scan.'],
            'visual_review_completed':False,'math_independently_verified':False,
            'student_answers_separately_checked':False}
    failure=False
    for kind in ('student','solved','rubric'):
        tex=getattr(args,kind+'_tex')
        if not tex.exists():
            print(f'MISSING TEX: {tex}',file=sys.stderr);failure=True;continue
        result['source_hashes'][str(tex)] = sha256(tex)
        target=args.output_dir/(tex.stem+'.pdf')
        logs=[]
        if not args.skip_compile:
            for pass_i in (1,2):
                cmd=[args.engine,'-interaction=nonstopmode','-halt-on-error','-file-line-error',
                     '-output-directory',str(args.output_dir.resolve()),str(tex.resolve())]
                proc=subprocess.run(cmd,cwd=str(tex.parent.resolve()),stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True,errors='replace')
                log=args.output_dir/(tex.stem+f'_pass{pass_i}.log')
                log.write_text(proc.stdout,encoding='utf-8')
                logs.append(str(log))
                if proc.returncode:
                    failure=True
                    print(f'COMPILATION FAIL {kind}: see {log}',file=sys.stderr)
                    break
        if not target.exists():
            failure=True;continue
        expected = (len(version_ids)*args.pages_per_version if version_ids and kind!='rubric'
                    else args.expected_rubric_pages if kind=='rubric' else None)
        checked=pdf_check(target,expected,version_ids=version_ids,
                          per_version=args.pages_per_version,
                          enforce_versions=kind!='rubric')
        checked['compilation_log_paths']=logs
        if not args.skip_contact_sheets:
            checked['contact_sheets']=contact_sheets(target,args.output_dir/'contact_sheets')
        result['files'][kind]=checked
        if not (checked['all_a4'] and checked['page_count_pass'] and checked['version_labels_pass']):failure=True
    result['status']='AUTOMATED_CHECKS_PASSED_HUMAN_REVIEW_PENDING' if not failure else 'FAILED_AUTOMATED_CHECKS'
    (args.output_dir/'QA_REPORT_AUTOMATED.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'], 'files':{k:{'pages':v['pages'],
           'all_a4':v['all_a4'],'page_count_pass':v['page_count_pass'],
           'version_labels_pass':v['version_labels_pass']} for k,v in result['files'].items()}},indent=2))
    return 1 if failure else 0
if __name__=='__main__':sys.exit(main())
