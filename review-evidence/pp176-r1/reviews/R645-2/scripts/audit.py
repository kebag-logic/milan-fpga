#!/usr/bin/env python3
"""Audit checkout bytes/index/modes, merged arms, ROM semantics and public hashes.
Usage: python3 audit.py SOURCE_CHECKOUT PACKET_DIRECTORY
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

repo, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
def file_at(ref, path):
    return git('show', ref + ':' + path).decode()
expected_head = '26ddcba423a204e75238d737ef41e6cb6e30ebc3'
expected_tree = 'c3f5e8f17caa9dcb64093b01b6ac988c11fe9400'
assert git('rev-parse', 'HEAD').decode().strip() == expected_head
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == expected_tree
entries = {}
links = {}
for row in git('ls-tree', '-rz', 'HEAD').split(b'\0'):
    if not row:
        continue
    meta, path_b = row.split(b'\t', 1)
    mode, kind, oid = meta.decode().split()
    path = os.fsdecode(path_b)
    entries[path] = (mode, oid)
    if mode == '160000':
        links[path] = oid
        continue
    f = repo / path
    if mode == '120000':
        data = os.fsencode(os.readlink(f))
        assert f.is_symlink()
    else:
        data = f.read_bytes()
        actual_mode = '100755' if f.stat().st_mode & 0o111 else '100644'
        assert mode == actual_mode, path
    actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert actual == oid, path
index = {}
for row in git('ls-files', '--stage', '-z').split(b'\0'):
    if row:
        meta, path = row.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        assert stage == '0'
        index[os.fsdecode(path)] = (mode, oid)
assert index == entries
assert not git('status', '--porcelain=v2', '--untracked-files=all')

engine = 'hdl/aecp/KL_aecp_engine.sv'
base, head, author = (file_at(ref, engine) for ref in ['77cf6fb4', 'HEAD', 'bee33ff'])
def block(text, token):
    start = text.index(token)
    # Isolate one begin/end block, including nested blocks.
    depth = 0
    for m in re.finditer(r'\bbegin\b|\bend\b', text[start:]):
        depth += 1 if m.group() == 'begin' else -1
        if depth == 0:
            return text[start:start+m.end()]
    raise AssertionError(token)
arms = {}
for token in ['if (gavb_r) begin', 'if (scfg_r) begin']:
    assert block(base, token) == block(head, token)
    arms[token] = {'equal_to_source_base': True,
                   'sha256': hashlib.sha256(block(head, token).encode()).hexdigest()}
assert block(author, 'if (ssinfo_r) begin') == block(head, 'if (ssinfo_r) begin')
assert re.search(r'assign si21_w = ssinfo_r && \(cmd_r.cdl == SI21_CDL_C\)\s*&& \(pld_cmd_r == SI21_PLD_C\)', head)
assert re.search(r'assign si13_pad_w = si13_w', head)
ucode = 'hdl/aecp/ucode/gen_ucode.py'
assert ast.dump(ast.parse(file_at('77cf6fb4', ucode))) == ast.dump(ast.parse(file_at('HEAD', ucode)))
remerge = git('show', '--format=', '--remerge-diff', 'HEAD').decode()
assert remerge.count('diff --git') == 1
assert 'diff --git a/tb/aecp_cmds/decode.json' in remerge
(packet / 'receipts/merge-resolution.diff').write_text(remerge)

public = []
for row in json.loads((packet/'public/MANIFEST.json').read_text()):
    if not row['file'].startswith('author-r2/'):
        continue
    file = packet/'public'/row['file']
    actual = hashlib.sha256(file.read_bytes()).hexdigest()
    assert actual == row['published_sha256']
    public.append({'file': row['file'], 'sha256': actual})
result = {'head': expected_head, 'tree': expected_tree,
          'tracked_blob_bytes_modes_and_index_equal': True,
          'tracked_entries': len(entries), 'submodule_gitlinks': links,
          'merged_arms': arms, 'set_stream_info_arm_equal_to_author_head': True,
          'microprogram_generator_ast_equal_to_source_base': True,
          'only_manual_merge_resolution': 'tb/aecp_cmds/decode.json engine input digest',
          'public_author_files_verified': public}
(packet/'receipts/artifact-audit.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k != 'public_author_files_verified'}, indent=2))
