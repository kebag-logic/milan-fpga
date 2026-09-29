import re, sys, subprocess
import cmarkgfm
from cmarkgfm.cmark import Options

def source_tables(text):
    tables, cur = [], []
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith('|'):
            cur.append((i, line))
        elif cur:
            tables.append(cur); cur = []
    if cur: tables.append(cur)
    return tables

def cells(line):
    s = line.strip()
    s = re.sub(r'`[^`]*`', lambda m: m.group(0).replace('|', 'X').replace('\\|','X'), s)
    s = s.replace('\\|', 'X')
    return len(s.strip('|').split('|'))

for path in sys.argv[1:]:
    text = open(path, encoding='utf-8').read()
    bad = 0
    for t in source_tables(text):
        want = cells(t[0][1])
        for ln, line in t:
            if cells(line) != want:
                bad += 1; print(f"SOURCE MISMATCH {path}:{ln} {cells(line)} != {want}")
    html = cmarkgfm.github_flavored_markdown_to_html(text, options=Options.CMARK_OPT_UNSAFE)
    rbad = 0; nt = 0; nrows = 0
    for tbl in re.findall(r'<table>(.*?)</table>', html, re.S):
        nt += 1
        rows = re.findall(r'<tr>(.*?)</tr>', tbl, re.S)
        counts = [len(re.findall(r'<t[hd][ >]', r)) for r in rows]
        nrows += len(rows)
        if len(set(counts)) != 1:
            rbad += 1; print(f"RENDER MISMATCH {path} table {nt}: {counts}")
    print(f"{path}: {len(source_tables(text))} source tables, {nt} rendered tables, {nrows} rendered rows, source mismatches {bad}, rendered mismatches {rbad}")
    # conflict markers
    for i, line in enumerate(text.splitlines(), 1):
        if re.match(r'^(<<<<<<<|=======|>>>>>>>|\|\|\|\|\|\|\|)( |$)', line):
            print(f"MARKER {path}:{i}")
