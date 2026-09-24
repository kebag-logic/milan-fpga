#!/usr/bin/env python3
"""Complete the handoff only after every required gate returns zero."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

PACKET = Path(__file__).resolve().parent
SOURCE = Path('$LANES/pp94-desc-mem-guard')
PARENT = Path('$LANES/pp94-parent-consumer')


def git(root: Path, *args: str) -> str:
    """Read a Git receipt while keeping its meaningful leading whitespace."""
    return subprocess.check_output(['git', *args], cwd=root, text=True, timeout=60,
                                   env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0'}).rstrip()


def main() -> int:
    """Write final documents, exact-head receipts and a packet digest manifest."""
    ci = json.loads((PACKET / 'ci-results.json').read_text())
    parent = json.loads((PACKET / 'parent-results.json').read_text())
    state = json.loads((PACKET / 'parent-state.json').read_text())
    assert len(ci) == 12 and len(parent) == 5
    assert all(row['rc'] == 0 for row in ci + parent)
    assert state['index_restored']
    head = git(SOURCE, 'rev-parse', 'HEAD')
    assert head == state['tested_pin'] == git(PARENT, '-C', 'protocol-processor', 'rev-parse', 'HEAD')
    assert not git(SOURCE, 'status', '--porcelain')
    assert not git(PARENT, 'diff', '--cached', '--name-only')
    subject = git(SOURCE, 'log', '-1', '--format=%B')
    assert len(subject.splitlines()) == 1
    subprocess.run(['git', 'diff', '--check', 'cc077a6ffe20585d20b116f008e07189ba1bb7f8..HEAD'],
                   cwd=SOURCE, check=True, timeout=60)
    source_state = {'head': head, 'tree': git(SOURCE, 'rev-parse', 'HEAD^{tree}'),
                    'subject': subject, 'status': git(SOURCE, 'status', '--porcelain'),
                    'diff_check_rc': 0,
                    'parent_status': git(PARENT, 'status', '--porcelain'),
                    'parent_head': git(PARENT, 'rev-parse', 'HEAD'),
                    'parent_index_pin': git(PARENT, 'rev-parse', ':protocol-processor')}
    assert source_state['parent_head'] == state['parent_head']
    assert source_state['parent_index_pin'] == state['pin_before']
    state['status_after'] = source_state['parent_status']
    parent_index = Path(git(PARENT, 'rev-parse', '--path-format=absolute', '--git-path', 'index'))
    assert hashlib.sha256(parent_index.read_bytes()).hexdigest() == state['index_sha256_before']
    (PACKET / 'parent-state.json').write_text(json.dumps(state, indent=2) + '\n')
    (PACKET / 'source-state.json').write_text(json.dumps(source_state, indent=2) + '\n')
    pp_log = (PACKET / 'parent-pp-shadow.log').read_text()
    counts = re.findall(r'pp_shadow: (\d+) checks, (\d+) failures', pp_log)[-1]
    tally = (counts[0], str(int(counts[0]) - int(counts[1])), counts[1])
    assert tally[0] == tally[1] and tally[2] == '0'
    assert 'SKIPPED' not in (PACKET / 'parent-xvlog.log').read_text()
    table = ['| Repository command | rc | Receipt |', '|---|---|---|']
    for row in ci:
        table.append(f'| `{" ".join(row["command"])}` | {row["rc"]} | `ci-{row["gate"]}.log` |')
    table.extend(['', 'The suite sweep passed **32 suites, 15,895 checks, zero failures**:',
                  'guard 78, descriptor store 584, product top 1,454. The NVM figure',
                  'gate completed 46 builds. Portability passed every listed top and the',
                  'engine memory-mapping assertions. `make check` passed 41 Mermaid',
                  'blocks, 18 WaveDrom blocks, 838 links and both matrix checks.',
                  '', 'Parent preparation, run in the requested consumer checkout:', '',
                  '```sh',
                  'git -C protocol-processor fetch $LANES/pp94-desc-mem-guard HEAD && git -C protocol-processor checkout --detach FETCH_HEAD',
                  '```', '',
                  f'Parent HEAD stayed `{state["parent_head"]}`. To satisfy the gates\' pin',
                  'checks, only the processor gitlink was staged temporarily at the tested',
                  'head. After all five gates, the original index was restored byte for',
                  'byte (matching SHA-256), including its original gitlink. No budget,',
                  'checker or parent source was changed, and no parent commit was made.',
                  'The submodule checkout remains at the final source head. See',
                  '`parent-fetch-checkout.log`, `parent-state.json` and `source-state.json`.',
                  '', '| Parent command | rc | Receipt |', '|---|---|---|'])
    for row in parent:
        table.append(f'| `{" ".join(row["command"])}` | {row["rc"]} | `parent-{row["gate"]}.log` |')
    table.extend(['', f'Parent simulation: **{tally[0]} checks, {tally[1]} PASS, 0 FAIL**.',
                  'The frontend gate executed; it was not skipped. All required gate',
                  'commands returned 0. The intentional priority mutant alone returned',
                  'nonzero, as required. The final source tree is clean, and',
                  '`git diff --check cc077a6f..HEAD` returns 0.'])
    handoff_path = PACKET / 'HANDOFF.md'
    handoff = handoff_path.read_text().replace(
        'Final head and gate results are recorded below after validation.',
        f'Final head: `{head}`. Final tree: `{source_state["tree"]}`.\n'
        'The worktree is clean. The single commit subject has no body or trailers.')
    handoff = handoff.replace('VALIDATION_RESULTS_PENDING', '\n'.join(table))
    handoff_path.write_text(handoff)
    pr_path = PACKET / 'PR-BODY.md'
    validation = f'''Round-2 local gates all returned 0:

- Every validation step in `.github/workflows/hdl.yml`: links, requirement
  matrix, WaveDrom freshness, `make stale`, RTL lint, the full simulation bank,
  generated matrix, the 46-build NVM figure gate and portability including
  engine memory mapping. `make check` also returned 0.
- Full bank: 32 suites, 15,895 checks, zero failing. Guard: 78/78; descriptor
  store: 584/584; product top: 1,454/1,454, including the wire-level late and
  stuck-burst cases. Store-only reset, hard reset, terminal error, payload and
  handshake coverage remains green.
- With `{head}` checked out in the parent consumer,
  `python3 scripts/check_cpp_idiom.py`, `python3 scripts/check_py_idiom.py`,
  `python3 scripts/xvlog_gate.py --check`,
  `python3 scripts/check_rtl_source_lists.py` and
  `make -C tb/verilator/pp_shadow -j8` all returned 0. The parent simulation
  passed {tally[0]} checks. The processor gitlink was staged only while running
  the pin-verifying gates; the original parent index was restored byte for
  byte afterward. No parent commit was made.
- `git diff --check` passes, both PNGs match their final SVG renders, and
  the priority mutation controller returns 0 after the expected assertion
  failure. The source worktree is clean.'''
    pr = pr_path.read_text().replace('ROUND2_VALIDATION_PENDING', validation)
    pr = pr.replace('ROUND2_HEAD_PENDING', head)
    pr_path.write_text(pr)
    for path in [handoff_path, pr_path]:
        text = path.read_text()
        assert text.startswith('[A252]') and 'PENDING' not in text
        assert '/home/' not in text
    ready = f'''[A252] REVIEW READY

Local head: `{head}` (branch `94-desc-mem-guard`).

Round 2 addresses R290-2 F1 = R291-2 F1 and R291-2 S1-S4. Both PNGs are
regenerated at the required widths and visually checked. The new priority
test passes at 78/78; the inverted-priority mutant fails only its new
completed assertion (77 PASS / 1 FAIL, make rc 2).

Every repository CI gate and all five requested parent consumer gates
returned 0. Full source bank: 32 suites / 15,895 checks. NVM figures:
46 builds. Parent simulation: {tally[0]} checks. The parent index was restored
byte for byte, and its submodule checkout remains at this source head.

`HANDOFF.md`, the full replacement `PR-BODY.md`, and receipts are ready in
the round-2 packet `2026-09-23/pp94-a252` for manager archival. No push, PR
edit, merge, parent commit, or hardware operation was performed. Independent
re-review and the manager's publication and remaining gates are pending.
'''
    (PACKET / 'REVIEW-READY.md').write_text(ready)
    # Receipts remain complete; replace machine-local paths with named roots.
    for path in PACKET.iterdir():
        if not path.is_file() or path.suffix not in {'.log', '.json', '.txt'}:
            continue
        text = path.read_text()
        text = text.replace(str(PACKET), '$PACKET').replace(str(SOURCE), '$SOURCE')
        text = text.replace(str(PARENT), '$PARENT')
        text = re.sub(r'$WORKSPACE_HOME/\.local/share/containers/storage/overlay/[^/]+/diff/usr',
                      '$VERILATOR_PREFIX', text)
        text = text.replace('$WORKSPACE_HOME', '$HOME')
        path.write_text(text)
    manifest = []
    for path in sorted(PACKET.iterdir()):
        if path.is_file() and path.name != 'MANIFEST.sha256':
            manifest.append(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}')
    (PACKET / 'MANIFEST.sha256').write_text('\n'.join(manifest) + '\n')
    print(f'Finalized packet for {head}; parent {tally[0]} checks; {len(manifest)} files.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
