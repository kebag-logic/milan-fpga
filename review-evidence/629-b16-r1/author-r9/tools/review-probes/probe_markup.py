#!/usr/bin/env python3
"""Reviewer's markup and digit probes; copied pages only, no source edits.
Usage: python probe_markup.py REPO AUTHOR_PACKET OUT
"""
import json
from pathlib import Path
import shutil
import subprocess
import sys

repo, packet, out = (Path(x).resolve() for x in sys.argv[1:])
scratch = out / 'scratch' / 'own-markup'
receipts = out / 'receipts'
receipts.mkdir(exist_ok=True)
page_name = '629_MEDIA_CLOCK_FOLLOWING_BENCH.md'
source = repo / 'docs/findings'
needle = '| Attribution | No loss in the network or the DUT | Every stage at the path\'s floor.'
cases = [('unchanged', '', 'page')]
for location in ['page', 'index']:
    for name, addition in [
        ('comment', ' CLOCK_DOMAIN 7<!-- -->ppm.'),
        ('short-comment', ' CLOCK_DOMAIN 7<!-->ppm<!-- -->.'),
        ('tag', ' Residual 7<span></span>ppm.'),
        ('tag-no-digit', ' <b>evidence</b>'),
        ('ordinary-digit', ' Residual 7.25 ppm.'),
    ]:
        cases.append((location + '-' + name, addition, location))
for i, addition in enumerate([
    ' CLOCK_DOMAIN 7\u202fppm.', ' CLOCK_DOMAIN 7\u2009furlongs.',
    ' CLOCK_DOMAIN 7e2 ppm.', ' CLOCK_DOMAIN -.25 ppm.',
    ' CLOCK_DOMAIN 7&#32;ppm.', ' CLOCK_DOMAIN 7\\*ppm.',
    ' CLOCK_DOMAIN 7\u2060furlongs.', ' CLOCK_DOMAIN 7/**/ppm.',
    ' CLOCK_DOMAIN 7<SPAN\n></SPAN>ppm.',
    ' CLOCK_DOMAIN 7\n<span>ppm</span>.',
    ' `CLOCK_DOMAIN 7<!-- -->ppm`.',
    ' CLOCK_DOMAIN 7<!--\n-->ppm.',
    ' The residual was \u2167 ppm.', ' The residual was \uff17 ppm.',
]):
    cases.append((f'own-digit-{i}', addition, 'page'))
results = []
for name, added, location in cases:
    work = scratch / name
    copied = work / 'docs/findings'
    copied.mkdir(parents=True, exist_ok=True)
    for file in [page_name, 'README.md']:
        shutil.copyfile(source / file, copied / file)
    target = copied / ('README.md' if location == 'index' else page_name)
    text = target.read_text()
    if location == 'index':
        lines = text.splitlines(keepends=True)
        index = next(i for i, s in enumerate(lines) if s.startswith('| [' + page_name + ']'))
        lines[index] = lines[index].rstrip('\n').rstrip('|') + added + ' |\n'
        changed = ''.join(lines)
        line = index + 1
    else:
        assert text.count(needle) == 1
        line = text[:text.index(needle)].count('\n') + 1
        changed = text.replace(needle, needle + added)
    target.write_text(changed)
    cmd = [sys.executable, '-I', str(packet / 'tools/check_b16_figures.py'), str(copied / page_name),
           str(packet), str(work / 'rows.tsv'), str(work / 'coverage.tsv'), '--repo', str(repo), '--show', '200']
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    def safe(s):
        for a, b in [(str(repo), '{repo}'), (str(packet), '{packet}'), (str(out), '{review}')]:
            s = s.replace(a, b)
        return s
    result = dict(name=name, source=target.name, line=line, added=added, rc=p.returncode,
                  stdout=safe(p.stdout), stderr=safe(p.stderr), rows_written=(work/'rows.tsv').exists(),
                  coverage_written=(work/'coverage.tsv').exists())
    results.append(result)
    print(name, 'rc', p.returncode, 'MARKUP', 'MARKUP' in p.stdout,
          'UNCOVERED', 'UNCOVERED' in p.stdout, 'exception', 'Traceback' in p.stderr, flush=True)
(receipts/'own-markup.json').write_text(json.dumps(results, indent=2, ensure_ascii=True)+'\n')
