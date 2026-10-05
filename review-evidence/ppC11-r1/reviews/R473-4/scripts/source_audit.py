#!/usr/bin/env python3
"""Reproduce scope lineage, comment-only changes and historical provenance."""
import argparse
import json
from pathlib import Path
import re
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
a = p.parse_args()
def git(*args):
    return subprocess.check_output(['git', '-C', str(a.source), *args], text=True)
head = '7124bde172a523179a2788dca825587aa5a2a1e6'
base = 'c050d97153dd0480ae741102c1647eeda9b7f273'
integration = '054d01c79e59c3f80454ad9cdefd8e914b540bb4'
round3 = '5123548eb4de35f24d43eb088c12dab70b06d01d'
def executable(body):
    body = re.sub(r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|//[^\n]*|/\*[\s\S]*?\*/',
                  lambda m: m.group(1) or '', body)
    return ''.join(body.split())
lane = []
for rel in git('diff', '--name-only', integration, head, '--', 'hdl', 'tb').splitlines():
    if not rel.endswith(('.sv', '.cpp', '.hpp', '.h')):
        continue
    same = executable(git('show', integration + ':' + rel)) == executable((a.source / rel).read_text())
    lane.append({'file': rel, 'same_noncomment_tokens': same})
assert all(r['same_noncomment_tokens'] for r in lane)
preserved = []
for rel in ['scripts/check-ids.py', 'scripts/check-figures.py', 'scripts/render-wavedrom.py',
            'docs/architecture/02_interfaces.md', 'docs/diagrams/wavedrom/fig-02-txwave.svg',
            'docs/diagrams/wavedrom/fig-02-memwave.svg']:
    old = git('rev-parse', round3 + ':' + rel).strip()
    new = git('rev-parse', head + ':' + rel).strip()
    preserved.append({'file': rel, 'old_blob': old, 'new_blob': new, 'equal': old == new})
assert all(r['equal'] for r in preserved)
old = git('show', base + ':docs/architecture/02_interfaces.md')
history = (a.source / 'docs/history/02-class-a-word-stream.md').read_text()
prose = old[old.index('Word-oriented stream,'):old.index('\nThe RX stream carries')]
provenance = {
    'prose_table_verbatim': prose.strip() in history,
    'wave_sources_verbatim': re.findall(r'```wavedrom\n(.*?)\n```', old, re.S)[:2] ==
                             re.findall(r'```json\n(.*?)\n```', history, re.S),
    'original_commit_permalinks': history.count(base) == 4,
}
assert all(provenance.values())
current = (a.source / 'docs/architecture/02_interfaces.md').read_text()
mac = current[current.index('## 3. Class A'):current.index('## 4. Class B')]
waves = [json.loads(x) for x in re.findall(r'```wavedrom\n(.*?)\n```', mac, re.S)]
rxnames = [s['name'] for s in waves[0]['signal']]
assert rxnames == ['clk', 'rx_valid_i', 'rx_data_i', 'rx_last_i']
print(json.dumps({'head': head, 'base': base, 'integration_parent': integration,
                  'aggregate_changed_files': len(git('diff', '--name-only', base, head).splitlines()),
                  'lane_comment_only_files': lane, 'preserved_round3_blobs': preserved,
                  'historical_provenance': provenance, 'rx_wave_signals': rxnames,
                  'merge_delta_files': git('diff', '--name-only', round3, head).splitlines()}, indent=2))
