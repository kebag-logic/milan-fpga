"""Render the local acceptance ledger from preserved foreground command receipts."""
from pathlib import Path
import json
import shlex
import subprocess

SCRATCH = Path('/data-2/milan/tmp/opt-a837')
OUTPUT = Path('$MANAGEMENT/2026-09-23/opt-a837/round1')
ROOT = Path('/data-2/milan/lanes/opt-gptp-sw')
NAMES = [
    ('Coverage ratchet', 'coverage-7ad1'),
    *[(f'Firmware shard {i}/4 with RV32 and planted defects', f'fw-shard-{i}-final') for i in range(4)],
    ('Boundary builders without Verilator', 'firmware-boundary-edd31'),
    ('Boundary builders with Verilator', 'firmware-verilator-edd31'),
    ('Documentation workflow aggregate (original result)', 'docs-final'),
    ('Python idiom corrected replay', 'python-idiom-7ad1'),
    ('Final documentation, inventory and whitespace checks', 'docs-44c5'),
    ('Yosys elaborate workflow, five steps', 'yosys-elaboration'),
    ('Ratcheted lint and source-list derivation', 'verilator-lint-retry'),
    ('Specification-facing tests', 'bdd-conformance-retry'),
    ('Split crossing checks', 'split-cdc'),
    ('Publication census and controls', 'publication-census'),
    ('Builder with elaboration and RV32 required', 'builder'),
    ('LiteX aggregate (original timeout retained)', 'litex'),
    ('LiteX timing-cut corrected timeout replay', 'litex-timing-final'),
    ('LiteX runner self-test', 'litex-selftest'),
    ('NVM firmware gate', 'firmware-nvm'),
    ('Coverage controls', 'coverage-selftest'),
    ('Verdict tally controls', 'tally-selftest'),
    ('RV32 gate controls', 'rv32-selftest'),
    ('Runner offline controls inside disposable container', 'act-offline-exec'),
    ('gPTP simulation baseline', 'gptp-simulation'),
    ('gPTP simulation planted defects', 'gptp-simulation-mutants'),
]
head = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()
rows, commands, pending, failed = [], [], [], []
for label, name in NAMES:
    path = SCRATCH / (name + '.log.json')
    if not path.exists():
        rows.append(f'| {label} | pending | | `{name}.log` |')
        pending.append(label)
        continue
    data = json.loads(path.read_text())
    if data['rc'] != 0 and name not in ('docs-final', 'litex'):
        failed.append(label)
    rows.append(f"| {label} | {data['rc']} | {data['seconds']:.1f} | `{name}.log` |")
    commands += [f'### {label}', '', f"Working directory: `{data['cwd']}`.",
                 f"Launch head: `{data.get('head', 'not embedded in this early receipt; see input-equivalence.json')}`.",
                 '', '```sh', shlex.join(data['argv']), '```', '']
docs = json.loads((SCRATCH / 'jobs/docs/results.json').read_text())
failed_docs = [d for d in docs if d['rc']]
assert len(failed_docs) == 1 and 'Python' in failed_docs[0]['name'], failed_docs
status = ('FAILED: ' + '; '.join(failed) if failed else
          'PENDING: ' + '; '.join(pending) if pending else 'LOCAL VALIDATION COMPLETE')
intro = f"""STATUS: {status}

# [A837] Review ready packet for PR 966

Commit: `{head}`. Base of this repair: `165476c755e4728a044c12ea6bc33ce0a0a9d28f`.
Branch: `884-gptp-firmware`; PR base: `dev-soft-core-optimisation`.
Local commits only. No push, PR edit or review verdict is claimed.

The coverage repair adds two AECP face tests and two mailbox-driver tests, with one planted defect per test.
They cover software snapshot fields, path callback capacity/refusal, timestamp flags and both time words across
ring wrap, and publication ordering with one final generation commit. The ratchet restores the face and driver
to 100% lines and branches, removes the stale platform gate exclusion, and records both gPTP files. No recorded
figure is lowered. The cancelled-job replay exposed test-build integration omissions; the gPTP simulation now
honors STACK_DIR and its pin and is captured by the boundary gate. Both defect campaigns have explicit suite
classification. The two driver mutations live in a focused table; all 828 entries and their order are identical
to the inline version used when shard 1 started. No product C or RTL changed.

| File | Lines | Branches |
|---|---:|---:|
| aecp_face.c | 229/229 | 204/204 |
| mbx.c | 384/384 | 202/202 |
| ctrl_plat.c | 224/224 | 110/110 |
| gptp.h | 2/2 | 0/0 |
| gptp.c | 665/704 | 346/437 |

Coverage at 7ad1e7df is rc 0. The final commit corrects README prose only; all 21 parsed exclusions and all ratchet figures are identical (coverage-readme-identity.log). The commands below are the substantive local job steps, with the available
pinned tools. Hosted setup/cache/upload/cancellation actions are not represented as local tests. No hosted green
context or exact-remote-head act replica is claimed; the manager controls pushing and review. The candidate
runner's offline self-test ran only inside a disposable, unprivileged container with no credentials or Docker
socket, not as a host orchestrator.

## Validation

| Check | Exit code | Seconds | Receipt under receipts/966 |
|---|---:|---:|---|
"""
notes = """
Documentation has a passing result for each of its 42 substantive steps after the focused Python idiom replay.
The original aggregate rc 1 is retained; its only failure was the new inline mutation entries taking a module
past 1000 lines. Extracting them fixed it without changing any mutation. LiteX has eight passing checks after
the timing-cut replay: its first run exceeded the default 900 s wall-clock limit (unknown, rc 92); the replay
completed in 1269 s under a 7200 s limit without changing assertions.

The full builder returned rc 0 and explicitly reported two uncovered arms: the build-flags mutation is inert
with the available make, and the historical placed-resource calibration report is absent. Neither is counted
as a pass. Previous failed or superseded runs remain in the receipt index. Their passing replacements are
identified above; an interrupted run does not count as evidence.

`receipts/966/input-equivalence.json` records the tested-input relationship across local commits. The four
firmware shards started with the tests at 17bd60c6; subsequent C/C++ test inputs are identical, and the driver's
mutation serialization proves the refactor preserves all entries. Both boundary legs were restarted after the
registry change. Coverage and the Python idiom check ran at 7ad1e7df before the final README prose correction; the documentation checks were replayed after it. The changed Makefile was exercised
by the closed loop and its planted-copy campaign.

`receipts/INDEX.md` indexes bounded plain-text receipts and hashes. Reproduction wrappers and environment are
under `receipts/reproduce`; source logs and build products remain in the named scratch directory. This packet
provides author evidence for independent review, not an author's approval of the PR.

## Exact commands

"""
(OUTPUT / '966/REVIEW-READY.md').write_text(intro + '\n'.join(rows) + '\n' + notes + '\n'.join(commands))
print(status)
