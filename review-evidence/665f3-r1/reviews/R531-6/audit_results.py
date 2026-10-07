#!/usr/bin/env python3
"""Recompute header bounds, table times, source delta, and linked-image identity."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument('root', type=Path)
a = ap.parse_args()
root = a.root.resolve()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
head = 'd8060d87f892239ac4e598d0a8556cbfcd4a52ec'
base = '13e715136b0b7c8d9763e0b730d9709f2c9f5932'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')

def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args], env=env).decode()

changed = git('diff', '--name-only', base, head).splitlines()
assert set(changed) == {'docs/design/MAILBOX_SPLIT.md', 'sw/firmware/ctrl/README.md',
                        'sw/firmware/ctrl/test/test_acmp_mbx.cpp',
                        'sw/firmware/ctrl/test/acmp_review_mutants.py'}
history = git('log', '--format=%H %s', f'{base}..{head}').splitlines()
assert len(history) == 3

source = scratch / 'bounds.c'
source.write_text('''#include <stdio.h>
#include "ctrl_app.h"
int main(void) {
 printf("%u %u %u %u %u\\n", MBX_N_IF, ACMP_MBX_PASS_MAX, MAAP_MBX_PASS_MAX,
        CTRL_LOOP_EVENTS_PER_PASS * (MBX_EV_WORDS + 2u), CTRL_APP_PASS_MAX);
 return 0;
}
''')
bounds = []
for interfaces, ctrl in ((1, root / 'sw/firmware/ctrl'),
                         (2, scratch / 'focused/control/acmpif2/ctrl')):
    exe = scratch / f'bounds-{interfaces}'
    includes = ['-I' + str(ctrl / part) for part in ('app','acmp','adp','maap','mbx','loop','port','wire')]
    includes += ['-I' + str(root / 'sw/firmware/ctrl_nvm')]
    subprocess.run(['gcc', '-std=c11', *includes, str(source), '-o', str(exe)], check=True)
    n, acmp, maap, shared, app = map(int, subprocess.check_output([str(exe)]).split())
    assert (n, acmp, maap, shared, app) == ((1,1012,616,48,1580) if interfaces == 1 else (2,1043,664,48,1659))
    assert app == acmp + maap - shared
    bounds.append(dict(interfaces=n, acmp=acmp, maap=maap, shared=shared, app=app))

times = []
doc = (root / 'docs/design/MAILBOX_SPLIT.md').read_text()
for name, passes, expected in (('event',2,4.74), ('owed',8,14.22), ('acmp-ring',10,17.38), ('adp-ring',21,34.76)):
    accesses = (passes + 1) * bounds[0]['app']
    milliseconds = accesses / 1000
    assert milliseconds == expected and f'{expected:.2f} ms' in doc
    times.append(dict(input=name, taken_by_pass=passes, accesses=accesses,
                      assumed_access_us=1, milliseconds=milliseconds,
                      fits_T_svc_10_ms=milliseconds <= 10, fits_ceiling_20_ms=milliseconds <= 20))

images = []
for shape in ('endstation_ax7101_1x1_tdm8','endstation_ax7101_8x8'):
    head_bytes = (scratch / 'images/head' / shape / 'ctrl_app.elf').read_bytes()
    base_bytes = (scratch / 'images/base' / shape / 'ctrl_app.elf').read_bytes()
    assert head_bytes == base_bytes
    images.append(dict(shape=shape, elf_file_bytes=len(head_bytes),
                       head_sha256=hashlib.sha256(head_bytes).hexdigest(),
                       round6_sha256=hashlib.sha256(base_bytes).hexdigest(), byte_identical=True))
receipt = dict(head=head, baseline=base, changed_paths=changed, history=history,
               production_tree_unchanged=True, header_bounds=bounds, derived_times=times, images=images)
print(json.dumps(receipt, indent=2))
