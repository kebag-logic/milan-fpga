import json
from pathlib import Path
import subprocess

root = Path('$LANES/400-403-declaration-truth')
out = Path('$MANAGEMENT/2026-09-23/400-403-a323')
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
receipt = json.loads((root / 'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
old = json.loads((out / 'previous-measurements.json').read_text())
runs = json.loads((out / 'measurement-runs.json').read_text())
assert len(runs) == 6 and all(r['rc'] == 0 for r in runs)
lines = [
    '# [A323] Round 5 handoff', '',
    'Local work and assigned verification complete. Independent re-review remains due.', '',
    '## Merge summary', '',
    '- Branch: `400-403-declaration-truth`.',
    '- Starting head: `c6c65e803f9eb270a11dfd65fda5814fb0b0ea55`.',
    '- Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.',
    '- Fetched dev matched `220cb5a34507bb79bbf976b031bb55eb05543d6f`.',
    '- Clean merge: `6d1819220f452ed9dcc086127f3f0695d14642aa`.',
    '- Merge subject: `Merge dev into 400-403-declaration-truth`.',
    f'- Final local head: `{head}`.',
    '- Submodules initialized at the merged pins.',
    '- Only the receipt and ownership document changed after the merge.',
    f"- Firmware SHA-256: `{receipt['product_firmware_sha256']}`.",
    '- Firmware and hold behavior were unchanged by this round.', '',
    'Authority: [assignment](https://github.com/kebag-logic/milan-fpga/issues/400#issuecomment-5838671391),',
    '[R249-4 F1](https://github.com/kebag-logic/milan-fpga/pull/566#issuecomment-5838668746), and',
    '[clock/hold decision](https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5831090112).',
    'Public review receipts were read in read-only scratch storage.', '',
    '## Measurements', '',
    'All six commands returned 0: 16 graded captures each, 96 total.',
    'Every row passes census, attestation, closed ownership, byte equality and timing.',
    'ON counters are positive; OFF counters are zero and timing still grades.',
    'CPU rising edges align with system edges. System frequency is 100 MHz.',
    'The 100 MHz CPU point is a non-contract comparison.', '',
    '| Shape | CPU MHz | Arm | Captures | Minimum ms | Maximum ms | Command | Evidence |',
    '|---|---|---|---|---|---|---|---|',
]
for r in runs:
    a = r['measurement']
    shape = '8x8' if a['shape'].endswith('8x8') else '1x1 TDM8'
    lines.append(f"| {shape} | {a['cpu_hz']//1000000} | {a['traffic'].upper()} | {a['captures']} | {a['minimum_ms']:.5f} | {a['maximum_ms']:.5f} | `{r['command']}` | [{r['log']}]({r['log']}) |")
lines += ['',
    'Common environment: the assigned SDK bin and installed LiteX environment lead PATH.',
    '`LITEX_ENV_CC_TRIPLE=riscv32-linux`, `PYTHONHASHSEED=0`,',
    '`COURSIER_MODE=offline`, and `SBT_OPTS=-Dsbt.offline=true`.',
    'Every capture uses `unshare -Urn`; no dependency was downloaded.',
    'Capture builds use installed Verilator 5.052; suite builds use installed 5.050.',
    'Component revisions and the CPU netlist hash match the prior receipt.',
    'Full identities are recorded in [environment.json](environment.json).',
    'All simulation build trees are under `$VALIDATION_STORAGE/400-403-a323-*`.', '',
    '## Old versus new maxima', '',
    'Each maximum includes every row from both traffic arms.', '',
    '| Shape | CPU MHz | Old ms | New ms | Delta ms | Floor margin |',
    '|---|---|---|---|---|---|',
]
for before, after in zip(old['maxima'], receipt['maxima']):
    lines.append(f"| {after['shape']} | {after['cpu_hz']//1000000} | {before['maximum_ms']:.5f} | {after['maximum_ms']:.5f} | {after['maximum_ms']-before['maximum_ms']:+.5f} | {after['margin']:.4f}x |")
worst = next(a['maximum_ms'] for a in receipt['maxima'] if a['shape'].endswith('8x8') and a['cpu_hz'] == 50000000)
lines += ['', f'**Stop condition not triggered: {worst:.5f} ms <= 24.5 ms.**',
    f'Remaining allowance: **{24.5-worst:.5f} ms**.',
    'The nominal hold remains 50 ms, with its guaranteed 49 ms floor.', '',
    '## Gate table', '',
    'Workflow run steps were executed in order. Existing dependencies were verified',
    'instead of downloaded or installed. The SDK step used `--verify-only`.',
    'The SDK builder maps its fixed compiler selector to the assigned SDK and audits argv.',
    'The absent mode hides the three cross-compiler candidates used by the builder.',
    'The workflow-runner self-test runs inside a disposable network-disabled container,',
    'with candidate files mounted read-only and no host credentials.',
    'No-git checks use a scratch tree export, without an additional checkout.', '',
    '| Gate | Command | Final return code | Evidence |', '|---|---|---|---|',
]
latest = {r['id']: r for r in json.loads((out / 'docs-results.json').read_text())}
rows = [latest[p['id']] for p in json.loads((out / 'docs-command-plan.json').read_text())]
rows += json.loads((out / 'suite-results.json').read_text())
for name in ['builder-absent', 'declarations', 'wire-accountability', 'nogit-docs_check',
             'nogit-check_feature_status', 'final-docs', 'final-doc-style', 'final-em-dash',
             'diff-check', 'diff-base-check']:
    rows.append(json.loads((out / (name + '.json')).read_text()))
for r in rows:
    assert r['rc'] == 0, r
    name = r.get('step', r.get('suite', r.get('name', 'gate')))
    lines.append(f"| {name} | `{r['command']}` | 0 | [{r['log']}]({r['log']}) |")
for name in ['bytes', 'records', 'clock', 'ignore-off-timing']:
    r = json.loads((out / ('capture-mutation-' + name + '.json')).read_text())
    assert r['rc'] == r['expected_rc'] == 1
    lines.append(f"| Capture mutation: {name} | `{r['command']}` | 1 expected; wrapper 0 | [{r['log']}]({r['log']}) |")
for name in ['skip-copy', 'no-traffic']:
    r = json.loads((out / ('control-' + name + '.json')).read_text())
    assert r['rc'] == 0
    lines.append(f"| Simulation control: {name} | `{r['command']}` | 0 | [{r['log']}]({r['log']}) |")
lines += ['',
    'Co-simulation passed 465 checks and detected 39/39 mutants.',
    'Both default register and protocol-wrapper suites passed every leg.',
    'Declaration checks cover five configurations, 26 refusals, binding/reset',
    'mutations and header mutations.', '',
    '## Execution disclosures', '',
    '- Initial dependency preflight omitted installed system package metadata.',
    '  Adding its existing directory to the Python path resolved it.',
    '  No dependency was downloaded or installed.',
    '- Relocated suite builds exposed stale relative C++ dependencies.',
    '  The wrapper resolves source/build paths and caps eight build jobs.',
    '  Clean scratch rebuilds passed. Sources and expectations were unchanged.',
    '  Earlier path-only failure logs remain available.',
    '- The initial serial traffic-ON run was interrupted before grading.',
    '  Its `abandoned-serial` partial log supplies no verdict.',
    '  All six complete runs restarted under a foreground supervisor.',
    '  Every child was awaited; no detached work remains.',
    '- Explicit input mutations intentionally return 1; their wrappers require it.',
    '  Each log names the intended refusal.', '',
    '## Remaining limits and handoff', '',
    'The historical placed-utilization calibration report remains unavailable.',
    'Compiler-dependent arms are intentionally unmeasured in the absent mode;',
    'the separate SDK mode covers them. Physical timing and memory ordering',
    'remain UNRESOLVED 6; #565 owns configuration-clock reconciliation.',
    'No hardware result is claimed.', '',
    'Independent re-review, publication, hosted checks, trusted local workflow',
    'replication, merge authorization and containment remain with the integration owner.',
    'This round performs no push, PR edit, merge into dev, hardware operation,',
    'donor edit or additional checkout.',
    '`PR-BODY.md` contains the full proposed PR body and both close lines.',
    'The final authorized action is `[A323] REVIEW READY` on issue #400.', '',
]
(out / 'HANDOFF.md').write_text('\n'.join(lines))
