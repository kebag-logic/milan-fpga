#!/usr/bin/env python3
"""Re-run small documentation checks; record head, diff and text evidence."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

root, packet = map(lambda x: Path(x).resolve(), sys.argv[1:3])
out = packet / 'receipts'
checks = {
    'doc-style': ['python3', 'scripts/check_doc_style.py'],
    'docs-check': ['python3', 'scripts/docs_check.py'],
    'diff-check': ['git', 'diff', '--check', 'e617275074e370cec342af99b929e2588fc8d43f..5747a8cb99495cb0331658cdd499b9c44e3eda91'],
}
def run(item):
    tag, cmd = item
    with (out / (tag + '.log')).open('w') as f:
        r = subprocess.run(cmd, cwd=root, stdout=f, stderr=subprocess.STDOUT)
    (out / (tag + '.rc')).write_text(str(r.returncode) + '\n')
    print(f'{tag}: rc {r.returncode}', flush=True)
    return r.returncode
with ThreadPoolExecutor(max_workers=3) as pool:
    rc = list(pool.map(run, checks.items()))

def collapsed(path):
    return re.sub(r'\s+', ' ', (root / path).read_text())
want = ('The clip raises neither `amap_edit_live_wr_p` nor map-persistence work. '
        'Controller edits raise sticky live-map pending; records `0x60` to `0x7F` '
        'remain unmaterialized in stages 1 and 2. Stage 3 supplies their writer.')
assert want in collapsed('docs/design/SAVED_STATE_MATERIALIZATION.md')
want2 = ('On a shape with dynamic maps, each dynamic direction\'s store and crossbar hold '
         'the #658 power-on map from boot: stream channel c on the port\'s cluster c.')
assert want2 in collapsed('docs/reference/REGISTER_MAP.md')
bullets = ['The CSR map window refuses writes.', "That lasts until one sweep after the restore's terminal."]
assert all('- ' + b in (root / 'CHANGELOG.md').read_text() for b in bullets)
counts = [len(re.findall(r"[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)?(?:-[A-Za-z0-9]+)*", b)) for b in bullets]
assert counts == [6, 9]
receipt = {'persistence_exact_text_match': True, 'per_direction_exact_text_match': True,
           'changelog_bullets': bullets, 'sentence_word_counts': counts,
           'sentence_cap': 10}
(out / 'text-corrections.json').write_text(json.dumps(receipt, indent=2) + '\n')

def git(*args):
    return subprocess.check_output(['git', *args], cwd=root)
head = git('rev-parse', 'HEAD').decode().strip()
full = git('diff', '--no-ext-diff', '--no-textconv', '--no-renames', 'e6172750..' + head)
lane = git('diff', '--no-ext-diff', '--no-textconv', '--no-renames', '510fae60..' + head)
rtl_delta = git('diff', 'fb4953bd..' + head, '--', 'hdl/milan/milan_datapath.sv')
assert not rtl_delta
receipt = {'head': head, 'tree': git('rev-parse', 'HEAD^{tree}').decode().strip(),
           'full_diff_sha256': hashlib.sha256(full).hexdigest(),
           'lane_diff_sha256': hashlib.sha256(lane).hexdigest(),
           'parent_rtl_unchanged_since_round1': True,
           'merge_parents': git('rev-list', '--parents', '-n1', '57155256f').decode().strip(),
           'first_parent_history': git('log', '--first-parent', '--format=%H %s', 'e6172750..' + head).decode().splitlines()}
(out / 'source-provenance.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('PASS: exact text, sentence limits and source/merge provenance')
raise SystemExit(any(rc))
