"""Prepare the final author handoff only after every assigned gate has passed."""
import hashlib
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = Path('$LANES/580-pp-pin-16be6768')
latest = {row['name']: row for row in map(json.loads, (OUT/'gate-results.jsonl').read_text().splitlines())}
required = ['builder-rv32', 'builder-absent', 'rom-check', 'capture', 'test-evidence', 'port-contracts',
            'pp-shadow', 'milan-dp', 'docs_check', 'check_doc_style', 'check_submodule_docs',
            'check_diagram_pngs', 'gen_toc-check', 'check_em_dash-base', 'diff-check', 'worktree-diff-check']
assert all(name in latest and latest[name]['rc'] == 0 for name in required)
assert all(row['rc'] == 0 for row in latest.values())
assert subprocess.check_output(['git','status','--porcelain'], cwd=ROOT, text=True) == ''
head = subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip()
subprocess.run([sys.executable, str(OUT/'refresh_handoff.py')], check=True)
handoff = (OUT/'HANDOFF.md').read_text()
dp_log = Path(latest['milan-dp']['log']).read_text(errors='replace')
summary = [line for line in dp_log.splitlines()
           if re.search(r'checks:|checks, [0-9]+ failures|RESULT:|mutants.*PASS|controls.*PASS', line)]
(OUT/'INTEGRATION-SUMMARY.txt').write_text('pp_shadow: 591 + 591 + 591 + 295 = 2068 checks, zero failures\n'
                                           + '\n'.join(summary) + '\n')
handoff = handoff.replace('Independent review and later publication remain outstanding.',
                         'Independent review and later publication remain outstanding.\nThe final public notice is `[A366] REVIEW READY` on issue #580;\n`REVIEW-READY.md` contains its exact body. This ends the authorized author work.')
handoff += '\nThe datapath normal simulation tally is 11,196 checks across 14 legs, zero failures; `INTEGRATION-TALLIES.json` records each result.\n'
handoff += '\n## Datapath result lines\n\n```text\n' + '\n'.join(summary) + '\n```\n'
(OUT/'HANDOFF.md').write_text(handoff)
pr = f"""[A366]

Closes #580

## Status

Local validation complete at `{head}`. Independent review pending.

## Description

Adopt processor `16be6768`, including descriptor body/key refusal from `493e5e4b`.
Record the new ROM digests while retaining earlier rows, classify the packer unit
test, update the F7 ownership record and pin references, regenerate the boundary
diagram, and refresh the capture receipt's processor pin.

## How to reproduce

Generate all five shipping configurations at `870ff88a` and `16be6768`, then pack
their AEM overlays with a 576-byte line limit. The five images and all 50 builder
output files are byte-identical. The handoff includes per-file sizes and hashes.

## How to validate

All assigned gates returned zero: the full builder bank in both compiler modes,
ROM digests, capture receipt, test evidence, port contracts, default wrapper and
datapath suites, documentation, and whitespace checks. Both builder modes ran
all 86 top-level tests in the normal order. The existing calibration arm lacks
its external report; absent mode additionally marks compiler-dependent checks
as not run.

The capture checker does not use the recorded pin as a measured input.
Its census, clocks, firmware and harness hashes remain valid. The retained
8x8 maximum is 24.30246 ms; no remeasurement was required.

## DoD

- [x] Adopted pin and accompanying records updated.
- [x] Five-configuration output equality measured.
- [x] Assigned local gates complete.
- [ ] Independent review complete.
"""
assert pr.startswith('[A366]') and 'Closes #580' in pr and '/home/' not in pr
(OUT/'PR-BODY.md').write_text(pr)
notice = f"""[A366] REVIEW READY

Commit: `{head}` (local head), branch `580-pp-pin-16be6768`, base `682ecf0cb995473b72d5b4921088053ba753fc93`.
Independent reviewers: [R352] and [R353].

Changed: processor gitlink `870ff88a` -> `16be6768`; two new ROM ledger rows with all prior rows retained; assigned packer-test disposition; F7 enforcement record; pin text, boundary renders/manifest and changelog; capture receipt pin.

Acceptance criteria: met for the assigned local author work. All five AEM images, their maps/JSON and all 50 builder outputs are byte-identical between pins. No parent RTL or firmware change was committed.

Capture decision: no remeasurement required. `scripts/check_nvm_capture.py:32` derives census and clock inputs; `check_receipt` at line 58 compares them, product firmware and harness hashes and regrades the recorded rows. It never reads `processor_pins`. The check passed with the adopted pin. The retained 8x8/50 MHz maximum is 24.30246 ms, below 24.5 ms; this is retained evidence, not a new measurement. The conditional STOP was not triggered.

Validation: every assigned command returned rc 0, from the physical worktree, in the foreground and without a pipeline.

| Gate | Command | rc |
|---|---|---:|
"""
for name in required:
    command = latest[name]['command'].copy()
    if command[0].endswith('/python3'):
        command[0] = 'python3'
    command = [arg.replace(str(OUT)+'/', '') for arg in command]
    notice += f'| {name} | `{shlex.join(command)}` | 0 |\n'
notice += """
Both builder modes ran all 86 top-level tests, in the exact normal-entry order.
The compiler-present run has one NOT RUN arm: gate 11's absent external
calibration report. Absent mode additionally marks the RV32-dependent instruments
as NOT RUN. These are recorded limits, not passing claims for those arms.
The wrapper suite passed 2,068 checks across all four default legs.
The datapath ran 14 normal simulation legs with 11,196 checks and zero failures,
followed by its required render and grandmaster-step mutation campaigns.
The documentation set also includes the generation guide's required checks and
self-tests, reference paths, feature status, traceability, Contents/anchors,
archive, solution/submodule references and decoded raster checks. The generated
PNG, direct editable-master export and A4 print were visually inspected.

The absent run used the complete normal main entry with only the three compiler
candidate calls reporting their deliberate absence. Reproduction wrapper:

<details><summary>Compiler-absent wrapper</summary>

```python
"""
absent = (OUT/'builder_absent.py').read_text().replace("ROOT = Path('$LANES/580-pp-pin-16be6768')", 'ROOT = Path.cwd()')
notice += absent + '\n```\n\n</details>\n'
rom = handoff.split('## ROM ledger rows\n',1)[1].split('## Capture decision',1)[0]
notice += '\n<details><summary>ROM ledger rows</summary>\n\n' + rom + '\n</details>\n'
artifacts = handoff.split('## Five-configuration SHA256 tables\n',1)[1].split('## Gate table',1)[0]
notice += '\n<details><summary>Five-configuration SHA256 evidence</summary>\n\n' + artifacts + '\n</details>\n'
notice += '\n<details><summary>Final gate log identities</summary>\n\n| Gate | Bytes | SHA256 |\n|---|---:|---|\n'
for name,row in latest.items():
    notice += f'| {name} | {row["bytes"]} | `{row["sha256"]}` |\n'
notice += '\n</details>\n\nOpen risks/questions: the recorded calibration limit above; independent review remains pending. Local handoff and PR body are prepared. Publication and PR operations remain with the next authorized step.\n'
assert '/home/' not in notice
assert len(notice.encode()) < 65000
(OUT/'REVIEW-READY.md').write_text(notice)
for path in OUT.iterdir():
    assert path.is_file() and path.stat().st_size <= 200000, path
print('Prepared final handoff, PR body and review-ready notice for', head)
print('Notice bytes:', len(notice.encode()))
