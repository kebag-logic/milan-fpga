#!/usr/bin/env python3
"""Verify exact tracked bytes, modes, index, gitlinks, and merge composition."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, required=True)
p.add_argument('--packet', type=Path, required=True)
a = p.parse_args()
def git(*args):
    return subprocess.check_output(['git', *args], cwd=a.repo)
expected_head = '42eb9aef3642f6d98058fe634a70f6a9c749cd25'
expected_tree = 'f7319d373b083043cf896a68712302f640212838'
assert git('rev-parse', 'HEAD').decode().strip() == expected_head
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == expected_tree
assert git('merge-tree', '--write-tree', '16c89c53', '77cf6fb4').decode().strip() == expected_tree
records, gitlinks = [], []
for entry in git('ls-tree', '-rz', 'HEAD').split(b'\0'):
    if not entry: continue
    metadata, path = entry.split(b'\t', 1)
    mode, typ, oid = metadata.decode().split()
    filename = os.fsdecode(path)
    f = a.repo / filename
    if mode == '160000':
        gitlinks.append({'path': filename, 'oid': oid})
        continue
    raw = os.fsencode(os.readlink(f)) if mode == '120000' else f.read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    assert actual == oid, filename
    if mode != '120000':
        expected_exec = mode == '100755'
        assert bool(f.stat().st_mode & stat.S_IXUSR) == expected_exec, filename
    records.append({'path': filename, 'mode': mode, 'blob': oid})
initial = (a.packet / 'receipts/initial-index.txt').read_bytes()
assert git('ls-files', '--stage') == initial
assert not git('status', '--porcelain=v1', '--untracked-files=all')
delta = git('diff', '--name-only', '77cf6fb4..HEAD').decode().splitlines()
inherited = git('diff', '--name-only', '22c139a4..77cf6fb4').decode().splitlines()
for filename in inherited:
    if filename != 'docs/architecture/06_aecp_engine.md':
        assert git('rev-parse', 'HEAD:' + filename) == git('rev-parse', '77cf6fb4:' + filename), filename
for filename in ('hdl/aecp/KL_aecp_notify.sv', 'hdl/packet_engine/KL_pp_event_router.sv'):
    assert git('rev-parse', 'HEAD:' + filename) == git('rev-parse', '16c89c53:' + filename)
    for revision in ('HEAD', '77cf6fb4'):
        source = git('show', revision + ':' + filename).decode()
        header = source[source.index('module '):source.index(');')+2]
        if revision == 'HEAD': saved = header
        else: assert header == saved, filename
result = {'head': expected_head, 'tree': expected_tree, 'all_tracked_blobs_and_modes_match': True,
          'index_unchanged': True, 'clean_status': True, 'tracked_file_count': len(records),
          'gitlinks': gitlinks, 'merge_tree_reconstructed': True,
          'changed_module_ports_and_parameters_unchanged': True,
          'inherited_main_files_match_except_combined_document': True,
          'delta': delta, 'files': records}
(a.packet / 'receipts/final-source-audit.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k != 'files'}, indent=2))
