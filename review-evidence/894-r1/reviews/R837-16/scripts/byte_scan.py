"""List every sentence, on a line the PR adds or changes (base..head), with a byte count, RAMB36, tile, granule,
spare or KiB figure, in SPLIT_CONTROL_MEMORY.md (with its section) and FR_NFR.md, and in a PR body file.
Usage: python3 -I byte_scan.py <repo> <base> <prbody.md>  (prints TSV: file:line, section, sentence)"""
import re, subprocess, sys
repo, base, body = sys.argv[1:4]
PAT = re.compile(r'\d[\d,]*(\.\d+)? ?(B\b|bytes|KiB|RAMB36|RAMB18|tiles?\b)|granule|spare|\bledger', re.I)
def added(path):
    out = subprocess.run(['git', '-C', repo, 'diff', '-U0', base, 'HEAD', '--', path], capture_output=True,
                         text=True, check=True).stdout
    lines = set()
    for m in re.finditer(r'^@@ -\S+ \+(\d+)(?:,(\d+))? @@', out, re.M):
        start, n = int(m.group(1)), int(m.group(2) or 1)
        lines.update(range(start, start + n))
    return lines
def sentences(text):
    return [s for s in re.split(r'(?<=[.;:])\s+(?=[A-Z(`*|])', text) if s.strip()]
for path in ('docs/design/SPLIT_CONTROL_MEMORY.md', 'docs/reference/FR_NFR.md'):
    text = open(f'{repo}/{path}').read().split('\n')
    sec = ''
    for no, line in enumerate(text, 1):
        if line.startswith('## '):
            sec = line[3:].split(' ')[0]
        if no in added(path) if False else None:
            pass
    keep = added(path)
    sec = ''
    for no, line in enumerate(text, 1):
        if line.startswith('## '):
            sec = line[3:].split(' ')[0]
        if no in keep:
            for s in sentences(line):
                if PAT.search(s):
                    print(f'{path.split("/")[-1]}:{no}\t{sec}\t{s.strip()}')
for no, line in enumerate(open(body).read().split('\n'), 1):
    for s in sentences(line):
        if PAT.search(s):
            print(f'PR-BODY:{no}\t-\t{s.strip()}')
