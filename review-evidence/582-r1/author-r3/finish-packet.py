"""Finalize the handoff only after every committed-head gate succeeds."""
import hashlib
import json
from pathlib import Path
import shlex
import subprocess

ROOT = Path('$LANES/582-baremetal-clock')
OUT = Path(__file__).resolve().parent
BASE = '9e9954e96bf55181edb9949ae94c9abd4ab6aaf5'
START = '77998f14b16bf7605956332d0f0ac8af0cecab5a'


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, capture_output=True,
                          text=True, check=True, timeout=120).stdout.strip()


head = git('rev-parse', 'HEAD')
assert head == 'aafcae59732c0a12333b73d82d5cdcbcbf90c47f'
assert git('remote', 'get-url', 'origin') == 'https://github.com/kebag-logic/milan-fpga.git'
assert git('branch', '--show-current') == '582-baremetal-clock'
assert not git('status', '--porcelain')
assert len(git('show', '-s', '--format=%B', 'HEAD').splitlines()) == 1
assert set(git('diff', '--name-only', START, head).splitlines()) == {
    'docs/testing/CI_WORKFLOWS.md', 'sw/builder/test_clock_contract.py', 'sw/litex/milan_soc.py'}
assert not git('diff', '--name-only', BASE, head, '--', 'configs', 'hdl', 'tb',
               'sw/firmware', '.gitmodules', 'protocol-processor', 'gptp-processor',
               'third_party/verilog-axis')
for row in json.loads((OUT / 'review-input-identities.json').read_text()):
    data = Path(row['path']).read_bytes()
    assert len(data) == row['size'] and hashlib.sha256(data).hexdigest() == row['sha256']

gates = json.loads((OUT / 'gate-results.json').read_text())
assert len(gates) == 48, len(gates)
assert all(g['head'] == head and g['returncode'] == 0 for g in gates)
assert gates[-1]['gate'] == 'diff-base'
actual = json.loads((OUT / 'final-sha256.json').read_text())
assert actual == json.loads((OUT / 'baseline-sha256.json').read_text())
assert len(actual) == 5

table = '| Configuration | Entries | Base SHA-256 = candidate SHA-256 |\n|---|---:|---|\n'
for name, value in actual.items():
    table += f'| `{name}` | {len(value["files"])} | `{value["sha256"]}` |\n'
gate_table = '| Gate | Exact command | rc | Seconds | Evidence |\n|---|---|---:|---:|---|\n'
for g in gates:
    command = shlex.join(g['command']).replace('$WORKSPACE_HOME/litex-milan/venv/bin/python3', '$PY')
    command = command.replace('/tmp/582-a370-docs/bin/python3', '$DOC_PY').replace(str(OUT), '$OUT')
    gate_table += (f'| {g["gate"]} | `{command}` | 0 | {g["seconds"]} | '
                   f'`{g.get("packet_log", "gate-results.json: hash and size")}` |\n')

handoff = f'''# Round 3 handoff

Executor: [A379]. Delta reviewer: [R354].
Issue: https://github.com/kebag-logic/milan-fpga/issues/582
PR: https://github.com/kebag-logic/milan-fpga/pull/596
Assignment: https://github.com/kebag-logic/milan-fpga/issues/582#issuecomment-5859065834
Takeover: https://github.com/kebag-logic/milan-fpga/issues/582#issuecomment-5859076610

Status: assigned implementation and committed-head validation complete;
ready for independent delta review. No review verdict is supplied here.
Branch: `582-baremetal-clock`.
Starting head: `{START}`.
Final head: `{head}`.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
One commit: `Clarify clock CI policy and complete product clock test controls`.
The commit has one subject line, no body and no trailers.

## Assigned items

| Item | Change and file:line | Mutant/probe and result |
|---|---|---|
| Required F1 / SG5 | `docs/testing/CI_WORKFLOWS.md:64,71` explicitly retains the relevant classification because the reader is outside `DOCS_JOB_PY`, and removes its row from the documentation-only table | R355 classification inputs replayed without pipelines: tap page `true`, plain-doc control `false`; explicit table audit passes; `ci_scope.py --selftest` rc 0 |
| Taken R354 SG1 | `sw/litex/milan_soc.py:3623` says the no-Milan option is a CLI smoke path that cannot finish a bare-metal image | R354 `soc_usage_probe.py`: seven documented invocations reach the pre-platform boundary with their stated options; 54 options have identical non-help keywords; rendered help states the limitation; all rc 0 |
| Taken R355 SG6 | `sw/builder/test_clock_contract.py:133` appends each configuration's `configs/generated/<stem>` entity directory to both accepted and divergent product argv cases | R355 mutant S9 KILLED, rc 1, owning `clock accepted before platform` assertion includes the entity path; identity control C1 rc 0 |
| Taken R355 SG7 | `sw/builder/test_clock_contract.py:94` retains the default control and skips only the system-clock control when the two configured clocks equal, with a named report | Unmodified R355 probe 39: builder accepts the equal-clock variant, test PASS and named SKIP; C4 distinct-clock control rc 0; R1 (system clock fed) and R2 (clock argument omitted) remain KILLED, rc 1 with owning ROM diagnostic |

`round3-probes.py` uses the exact mutation declarations from the read-only
round-2 reviewer script. Its copy loop is replaced with lane-local mutation
and restoration in `finally`; fresh temporary bytecode caches isolate runs.
The controls are C1, C4 and C5, all rc 0. The three assigned/regression
mutations fail by the expected owning assertion. The campaign itself returns 0.
Probe 39 reports assertion failures without changing its exit status, so the
wrapper also requires its PASS and SKIP text. Temporary variant files live
outside this packet. The usage probe runs unchanged.
`probe-results.json` records exact commands, exits, log hashes and sizes.
`review-input-identities.json` records the read-only inputs; all were rechecked.

The CLI probes stop before platform construction. They demonstrate the
argument checks, not a complete image or a hardware result. No default or
runtime guard changed. The full builder bank separately exercises elaboration.

## Five-configuration SHA-256 comparison

Base: `{BASE}`.
The base artifact manifest comes from the allowed previous author packet;
it was not regenerated with another checkout in this round. `identity.py`
regenerates all current outputs and compares every role and file hash with it.
All 61 artifact-role entries match. Each set digest hashes compact sorted
JSON mapping artifact roles to their file SHA-256 values.
`unchanged-configs.json` separately proves the five YAML files equal base bytes.
All five tracked configurations build; the STOP condition did not trigger.

{table}
## Gates at the committed head

All 48 commands below returned rc 0 at `{head}`.
They ran sequentially in the foreground, without pipelines, from the physical
`$LANES/582-baremetal-clock` directory. `gates.py` checks a clean
committed head before and after the sequence. `gate-results.json` records
the full argument arrays, cwd, head, elapsed time, return code, log hash and size.

`$PY` is `$WORKSPACE_HOME/litex-milan/venv/bin/python3`.
`$DOC_PY` is `/tmp/582-a370-docs/bin/python3`, the existing pinned renderer environment.
`$OUT` is this packet. No environment, package, SDK, tool prefix or tree export
is stored here. Logs over 200 KB stay outside the packet with hash/size receipts.

{gate_table}
Both compiler modes run the complete builder bank. The absent wrapper hides
exactly the three RV32 compiler selectors and leaves host probes real;
`absent-audit.json` records the expected compiler-dependent stand-downs.
The required-RV32 run covers those instruments. Both banks report the existing
gate-11 physical-resource calibration as NOT RUN because its historical
placement report is absent. Their command return codes are 0. These are
reported limitations, not hardware or timing-closure evidence.

`check_baremetal_only.py` requires a mode; both supported `--check` and
`--selftest` invocations pass. No CLI default was changed.
Pre-commit style checking found one overlong help line. It was wrapped and
the idiom gate passed before the commit; no assertion or acceptance criterion
was weakened. Every final gate above ran after that commit.

## Final boundary

Only the three assigned documentation/help/test files changed this round.
The worktree is clean. No firmware, RTL, configuration, gitlink, capture
recipe or capture receipt changed. The out-of-scope sweep entity-path omission,
clock-shadowing issue, simulation mirrors and group-5 prose remain unchanged.
No push, PR mutation, merge, additional checkout or hardware action occurred.

`PR-BODY.md` preserves its original `[A370]` label and `Closes #582`, and adds
Round 3 with this head and the validation results. It contains no absolute
home paths or attribution footer.

Independent delta review, publication of the branch/PR update, hosted checks
and the separate merge process remain with the reviewer and maintainer.
`REVIEW-READY.md` is the final issue comment. The only remaining action in
this assignment is to append it to issue #582, then stop.
'''
(OUT / 'HANDOFF.md').write_text(handoff)

p = OUT / 'PR-BODY.md'
text = p.read_text().replace(f'Status: round 3 at `{head}`, local validation in progress.',
                           f'Status: round 3 at `{head}`, ready for independent delta review.')
text = text.replace('Full committed-head validation is in progress.',
    'All 48 validation commands return rc 0 at this committed head: both complete builder compiler modes, '
    'the focused SoC clock contract, declarations, capture receipt, memory bridge, reviewer probes, '
    'artifact identity, all 38 documentation/policy commands and both whitespace checks. '
    'This includes every explicitly assigned policy self-test. The existing physical-calibration '
    'report is absent; compiler-absent stand-downs are expected and recorded.')
assert text.startswith('[A370]\n') and 'Closes #582' in text and '/home/' not in text
assert text.count('## Round 3') == 1
p.write_text(text)

(OUT / 'REVIEW-READY.md').write_text(f'''[A379] REVIEW READY
Commit: {head}
Changed: consistent tap-page CI policy; no-Milan smoke-path help; configured entity directories in product refusal tests; reported equal-clock ROM-control skip.
Validation: all 48 committed-head commands rc 0, including both complete builder compiler modes, test_clock_contract.py --soc, declarations, capture, memory bridge, 38 documentation/policy commands and whitespace checks. The explicitly assigned self-tests all pass.
Reviewer evidence: S9 KILLED; equal-clock probe PASS with named SKIP; ROM mutants R1/R2 remain KILLED; controls pass; CLI defaults unchanged.
Acceptance: required item and all three taken suggestions met. All five configurations and all 61 generated artifact-role hashes match base 9e9954e9. No tracked configuration refused; STOP condition not triggered.
Open risks/questions: none newly introduced. Existing gate-11 physical calibration remains NOT RUN because its historical report is absent; compiler-absent stand-downs are expected and recorded. Independent delta review remains outstanding.
Handoff and updated PR body prepared. No push, PR edit or merge performed.
''')

manifest = []
for path in sorted(OUT.rglob('*')):
    if path.is_file() and path.name != 'MANIFEST.json':
        data = path.read_bytes()
        assert len(data) <= 200_000, path
        manifest.append(dict(path=str(path.relative_to(OUT)), size=len(data),
                             sha256=hashlib.sha256(data).hexdigest()))
(OUT / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(f'Packet finalized: {len(gates)} passing commands; head {head}; {len(manifest)} bounded files')
