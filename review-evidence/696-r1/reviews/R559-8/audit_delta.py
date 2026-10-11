#!/usr/bin/env python3
"""Prove automatic merge equality and record exact delta identities."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

def main():
    root = Path(sys.argv[1]).resolve()
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args])
    source = git('rev-parse', '32582421').decode().strip()
    base = git('rev-parse', '09c7231e').decode().strip()
    merge = git('rev-parse', 'a7291311').decode().strip()
    head = git('rev-parse', 'aa980479').decode().strip()
    parents = git('show', '-s', '--format=%P', merge).decode().strip().split()
    assert parents == [source, base]
    automatic = git('merge-tree', '--write-tree', source, base).decode().strip()
    committed = git('rev-parse', merge + '^{tree}').decode().strip()
    assert automatic == committed
    paths = git('diff', '--name-only', merge, head).decode().splitlines()
    assert paths == ['docs/design/MARK_II_AREA_PLAN.md']
    diff = git('diff', '--no-ext-diff', '--no-textconv', merge, head)
    unchanged = ['hdl/ieee1722/maap/KL_maap.sv', 'tb/verilator/maap',
                 'sw/firmware/ctrl/test/maap_differential.py',
                 'sw/firmware/ctrl/test/test_maap_differential.cpp',
                 'syn/ooc/pp_resource_baseline.json']
    for path in unchanged:
        assert not git('diff', '--raw', source, head, '--', path), path
    # Current dev -> head contains only this lane's two MAAP connections and comment.
    dp = 'hdl/milan/milan_datapath.sv'
    dev_dp = git('diff', base, head, '--', dp).decode()
    assert '.port_operational_i (eff_link_w)' in dev_dp
    assert re.search(r'\.realtime_ns_i\s+\(ptp_now_w\[31:0\]\)', dev_dp)
    packet = Path(__file__).resolve().parent
    (packet / 'composition-wording.diff').write_bytes(diff)
    (packet / 'composition-datapath.diff').write_text(dev_dp)
    print(json.dumps({'source': source, 'dev': base, 'merge': merge, 'head': head,
                      'parents': parents, 'automatic_merge_tree': automatic,
                      'committed_merge_tree': committed, 'automatic_merge_equal': True,
                      'postmerge_changed_paths': paths,
                      'postmerge_diff_sha256': hashlib.sha256(diff).hexdigest(),
                      'unchanged_since_source': unchanged}, indent=2))

if __name__ == '__main__':
    main()
