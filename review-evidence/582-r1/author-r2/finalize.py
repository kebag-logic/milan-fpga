"""Assemble the final handoff only after every assigned gate succeeds."""
import hashlib
import json
from pathlib import Path
import re
import shlex
import subprocess

ROOT = Path('$LANES/582-baremetal-clock')
OUT = Path(__file__).resolve().parent
HEAD = '77998f14b16bf7605956332d0f0ac8af0cecab5a'
results = json.loads((OUT / 'gate-results.json').read_text())
assert len(results) == 51 and all(r['returncode'] == 0 and r['head'] == HEAD for r in results)
assert subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, check=True,
                      capture_output=True, text=True).stdout.strip() == HEAD
assert not subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout.strip()
commit = subprocess.run(['git', 'show', '-s', '--format=%B', 'HEAD'], cwd=ROOT,
                        check=True, capture_output=True, text=True).stdout.strip()
assert len(commit.splitlines()) == 1
mutants = json.loads((OUT / 'probe-results.json').read_text())
assert len(mutants) == 15 and all(r['status'] in ('KILLED', 'CONTROL-PASS') for r in mutants)

p = OUT / 'HANDOFF.md'
text = p.read_text().split('\n## Live committed-head gate progress', 1)[0]
text = re.sub(r'Status: .*', 'Status: required items 1-6 and assigned local validation complete; ready for independent re-review.', text, count=1)
text = text.replace('Documentation gates pending at the committed head.', 'All documentation gates return rc 0 at the committed head.')
start = text.index('## Gate results at committed head')
text = text[:start] + '''## Gate results at committed head

All 51 commands below returned rc 0 at the committed head
`77998f14b16bf7605956332d0f0ac8af0cecab5a`.
Commands ran sequentially, in the foreground, without pipelines, from the
physical `$LANES/582-baremetal-clock` directory.
`gate-results.json` retains exact argument arrays, working directory, head,
return code, elapsed time, full-log location, SHA-256 and size.
`gates.py` reproduces the sequence. It verifies a clean committed head before
starting and verifies the same clean head after finishing.

For compact commands below, `$PY` is the existing SoC environment's
`$WORKSPACE_HOME/litex-milan/venv/bin/python3`; `$DOC_PY` is the existing pinned
Markdown environment's `/tmp/582-a370-docs/bin/python3`; `$OUT` is this packet.
No environment, installed package, SDK, prefix or tree export is stored here.
Logs over 200 KB remain outside this packet and are represented by hash and size.

| Gate | Command | rc | Seconds | Packet evidence |
|---|---|---:|---:|---|
'''
for row in results:
    command = shlex.join(row['command'])
    command = command.replace('$WORKSPACE_HOME/litex-milan/venv/bin/python3', '$PY')
    command = command.replace('/tmp/582-a370-docs/bin/python3', '$DOC_PY')
    command = command.replace(str(OUT), '$OUT')
    evidence = row.get('packet_log', f'SHA-256 `{row["sha256"]}`, {row["size"]} bytes; full path in gate-results.json')
    text += f'| {row["gate"]} | `{command}` | 0 | {row["seconds"]} | {evidence} |\n'
text += '''
Both builder modes run the complete bank. The absent-mode wrapper hides exactly
the three RV32 compiler selectors; `absent-audit.json` records the selectors and
the expected stand-downs. Host compiler probes remain real. The required-RV32
run covers those compiler-dependent instruments. The existing gate 11 physical
resource-calibration arm is NOT RUN because its historical report is absent.
The bank returns rc 0 with that explicitly reported limit. No hardware claim is made.

The assignment names `check_baremetal_only.py` without a mode. Its bare
invocation returns rc 2 with a usage error. The gate requires `--check` or
`--selftest`; both documented modes are explicitly run above and pass. No
CLI default was changed to accommodate that invocation.

The first committed-head sequence stopped at a stale system-clock mutation
fixture in `check_solution_docs.py --selftest`. The fixture now targets the
default-value prefix, retaining the same mutated value and expected refusal.
All 43 controls pass. The initial result is retained in
`initial-gate-results.json`; the complete sequence above was rerun after
committing the repair. `docs-preflight-results.json` also retains the bare-mode
usage error; it is not a gate verdict.

## Final state and review boundary

Commit: `77998f14b16bf7605956332d0f0ac8af0cecab5a`.
Subjects: `Close clock contract review gaps in CI, ROM checks, refusals and documentation`; `Preserve the system clock mutation after adding CLI help`.
Both round-2 commits have one-line subjects, with no body or trailers. Worktree clean.

The round changes nine files, limited to tests, CI scope registration and
documentation/help. The SoC executable AST is unchanged except help keywords.
No firmware, RTL, configuration, submodule pin, capture recipe or receipt changed.
The out-of-scope simulation clock mirrors and group-5 prose remain unchanged.
No push, PR edit, merge, additional checkout or hardware operation occurred.
The local `PR-BODY.md` keeps its original label and `Closes #582` and adds Round 2.

The assigned local work is complete. Independent re-review, publication of the
branch/PR update, hosted checks and the separate merge process remain with the
assigned reviewers and maintainer. This author supplies evidence, not a review
verdict or lens ledger. `REVIEW-READY.md` is the exact final issue comment.
The final action is to append that comment to issue #582 and stop.
'''
p.write_text(text)

p = OUT / 'PR-BODY.md'
text = p.read_text()
text = re.sub(r'Status: .*', f'Status: round 2 at `{HEAD}`, ready for independent re-review.', text, count=1)
text = text.replace('Validation: both full builder modes, declarations, capture receipt, memory bridge, 11 mutation controls, 31 documentation/related checks and whitespace checks return zero.',
                    'Round 1 recorded passing builder, focused and documentation checks; independent review found the missing CI scope registration and the additional gaps resolved in Round 2.')
text = text.replace('Committed-head gate results are pending.',
                    'Both complete builder compiler modes, declarations, capture receipt, memory bridge, focused contract checks, all 38 documentation/related commands, reviewer probes and whitespace checks return rc 0 at this committed head. The explicit classifier, scope, shape and documentation self-tests pass. The existing physical-calibration report remains unavailable; compiler-absent stand-downs are expected and recorded.')
assert text.startswith('[A370]\n') and 'Closes #582' in text and '## Round 2' in text
assert '/home/' not in text and 'pending' not in text
p.write_text(text)

p = OUT / 'REVIEW-READY.md'
text = p.read_text().replace('Validation: pending completion of the committed-head gate sequence; do not post this draft.',
    'Validation: all 51 recorded commands return rc 0 at this committed head, run in the foreground without pipelines from the physical assigned lane. This includes both complete builder compiler modes, `test_clock_contract.py --soc`, declarations, capture receipt, memory bridge, 38 documentation/related commands, all explicitly assigned self-tests, reviewer probes, artifact identity and both whitespace checks. The existing physical-calibration arm is NOT RUN because its report is absent; the compiler-absent mode records its expected stand-downs.\n\nThe handoff records each item with file:line and mutation/probe evidence, the five-configuration SHA-256 table against the base, and every gate command/result. The local PR body retains its original label and `Closes #582` and includes Round 2.')
p.write_text(text)

manifest = []
for path in sorted(OUT.rglob('*')):
    if not path.is_file() or path.name == 'MANIFEST.json':
        continue
    raw = path.read_bytes()
    assert len(raw) <= 200_000, path
    manifest.append(dict(path=str(path.relative_to(OUT)), size=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
(OUT / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(f'Final handoff prepared: {len(results)} successful commands, 10 killed mutations, 5 controls')
