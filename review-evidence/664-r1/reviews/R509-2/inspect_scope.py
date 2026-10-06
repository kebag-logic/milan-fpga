#!/usr/bin/env python3
"""Record exact document-only scope and unchanged VERSION inputs."""
import argparse
import json
import os
from pathlib import Path
import subprocess

BASE = '423ac5d910d09ab189b3acc39ae3ae1d10d50b19'
PREVIOUS = 'a27808375427859dc357f6bfd0a88842062b20ed'
HEAD = '8fb296e3e02985aee27ef04cb08278836b734a14'

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('repo', type=Path)
    a = ap.parse_args()
    def git(*args):
        return subprocess.check_output(['git', '-C', str(a.repo), *args], text=True,
                                       env={**os.environ, 'GIT_NO_REPLACE_OBJECTS': '1'})
    changed = git('diff', '--name-only', BASE, HEAD).splitlines()
    delta = git('diff', '--name-only', PREVIOUS, HEAD).splitlines()
    assert len(changed) == 21 and all(x.endswith('.md') for x in changed)
    assert delta == ['docs/design/MAILBOX_SPLIT.md', 'docs/reference/FR_NFR.md']
    assert git('rev-list', '--count', PREVIOUS + '..' + HEAD).strip() == '4'
    assert not git('diff', '--check', BASE, HEAD)
    paths = ['hdl/common/csr/milan_csr.sv', 'tb/verilator/csr/sim_main.cpp',
             'tb/verilator/milan_dp/sim_main.cpp', 'tb/verilator/milan_dp/sim_nxn.cpp',
             'tb/verilator/milan_dp/sim_gptp.cpp', 'tb/verilator/milan_dp/sim_prune.cpp']
    identities = []
    for path in paths:
        old = git('rev-parse', BASE + ':' + path).strip()
        new = git('rev-parse', HEAD + ':' + path).strip()
        assert old == new, path
        data = (a.repo / path).read_text()
        needle = "32'h0002_0060" if path.endswith('.sv') else '0x00020060'
        assert needle in data, path
        identities.append({'path': path, 'blob': new, 'value': needle,
                           'lines': [i for i, line in enumerate(data.splitlines(), 1) if needle in line]})
    retired = subprocess.run(['git', '-C', str(a.repo), 'cat-file', '-e', BASE + ':tb/verilator/hostplane'],
                             capture_output=True)
    assert retired.returncode != 0
    print(json.dumps({'base': BASE, 'previous_head': PREVIOUS, 'head': HEAD,
                      'tree': git('rev-parse', HEAD + '^{tree}').strip(),
                      'changed_files': changed, 'round2_files': delta,
                      'round2_commits': git('log', '--format=%H %s', PREVIOUS + '..' + HEAD).splitlines(),
                      'version_inputs_unchanged': identities, 'retired_suite_absent_at_base': True,
                      'diff_check': 'PASS'}, indent=2))

if __name__ == '__main__':
    main()
