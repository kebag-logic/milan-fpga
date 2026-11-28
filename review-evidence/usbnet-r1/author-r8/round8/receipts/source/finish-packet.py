"""Publish the local review packet only after all requested final-head evidence passes."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

OUT = Path(__file__).resolve().parent.parent
ROUND = OUT.parent
PACKET = ROUND.parent
ROOT = Path.cwd()
def read(name):
    return json.loads((OUT / name).read_text())
def git(*args):
    return subprocess.check_output(['git', *args], text=True).strip()

head = git('rev-parse', 'HEAD')
qualification = read('qualification.json')
gates = read('final-gates.json')
identity = read('identity.json')
assert qualification['status'] == 'PASS' and qualification['head'] == head
assert len(gates) == 14 and all(g['head'] == head and g['returncode'] == 0 for g in gates)
assert identity['head'] == head and identity['status'] == 'PASS'
assert not git('status', '--porcelain=v1')
dep = '640699e6866602b2a5de5d404c43f3bd4df8037c'
pins = ['external', 'gptp-processor', 'protocol-processor', 'third_party/lwSRP',
        'third_party/tsn-c-stack', 'third_party/verilog-axis']
assert git('ls-tree', head, *pins) == git('ls-tree', dep, *pins)
assert git('merge-base', '--is-ancestor', dep, head) == ''
for row in identity['dependency_files']:
    assert hashlib.sha256((ROOT / row['path']).read_bytes()).hexdigest() == row['sha256']
scratch = Path('$VALIDATION_STORAGE/usbnet-a855')
scratch_bytes = int(subprocess.check_output(['du', '-s', '-B1', str(scratch)], text=True).split()[0])
free = shutil.disk_usage('/data').free
assert scratch_bytes < 25_000_000_000 and free >= 18 * 1024**3
unit = Path('/proc/self/cgroup').read_text().strip().split('::', 1)[1]
cgroup = Path('/sys/fs/cgroup') / unit.lstrip('/')
resources = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),unit=unit,
    cpu_weight=(cgroup/'cpu.weight').read_text().strip(),cpu_max=(cgroup/'cpu.max').read_text().strip(),
    cpu_affinity=sorted(os.sched_getaffinity(0)),scratch_bytes=scratch_bytes,data_free_bytes=free,
    shared_ccache='$VALIDATION_STORAGE/ccache',cleanup_log='$MANAGEMENT/2026-09-23/disk-cleanup.log',
    native_rerun=False,no_push=True,no_post=True,no_bench=True,no_flash=True,no_route=True)
(OUT/'resources-final.json').write_text(json.dumps(resources,indent=2)+'\n')
checks = '''| Check | Result | Bound or figure |
|---|---:|---:|
| Load | 0.501397114035 | 0.70 |
| ACMP | 29.84000 ms | 30 ms |
| txL | 48.90000 ms | 49 ms |
| Last notice | 117.58000 ms | 140 ms |
| THE SHARE | 1.7923875 ms | 2 ms |
| Complete wire egress | 644.980750 us | 1000 us |
| USB held AECP last delivery | 62.03635 ms | 62.14 ms |
'''
elfs = '''| Image | ELF SHA-256 |
|---|---|
| Arty | `f17d1a9da8ba6e50a1e8cf0af9b77ed434288a1d0a689a357a0c6a57ecda92cf` |
| ALINX 1x1 | `6e0a54124483adfadd04e8e6f62d296bdf884794b197d0ed9dc24c71de49fd56` |
| ALINX 8x8 | `0f1450acefdd7fa0173d1de3221f8c5a6456e59d96fc99611b5121b1c26a2c3f` |
'''
handoff = f'''Status: REVIEW READY for round-8 desk scope. ETA: complete.

Local head: `{head}` on `1011-usbnet`. Two local commits; nothing pushed or posted. Bench, flash and physical implementation were untouched.

Applied the [held-egress ruling](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7234489667) exactly. The separate `arty-usbnet-1x1` point derives each figure from the larger original Arty or injected measurement under #894's unchanged rule. The table lives in `docs/design/USB_NET_PATH.md`. The original `arty-1x1` and `8x8-1if` figures are unchanged. Six figures match the original Arty ledger; the last AECP figure derives as `60 + 1.05 * 2.03635 = 62.1381675` ms, rounded upward to 62.14 ms. Its measurement has 103.65 us margin. All seven remain recorded service-budget misses, within their ruled ledger; this is not a waiver of service budgets.

Regraded all 159 retained traces across the same eight images. Every raw trace and stimulus was verified against the retained packet; every regenerated grade is byte-identical to round 7. All eight complete per-image regrades pass with the existing #969 disposition. The final ledger leg passes with no new miss, no larger miss and no missing measurement. No native measurement was rerun.

{checks}
The installed scheduling row remains slice 1250 us, pace 10 ms, queued bound 125 ms and stated transmit bound 35 ms. Its costs, derivation and fixed-point evidence are unchanged. The current owner model equals the retained model exactly. Adding the local mailbox bound of 38.075 us gives ACMP 29.878075 ms, still below 30 ms. The wire evidence was carried only after verifying every retained replay's trace, source and parameter binding and rerunning its aggregate verdict; no fresh wire replay is claimed.

Controls at the final head:

- The complete retained data still fails at `arty-1x1`, solely for 62.03635 ms versus 61.99 ms. That expected failure is retained, not cleared at the old point.
- A retained-data fixture at 62.14 ms passes the USB point. At one 80 MHz cycle higher, 62.1400125 ms (62.14001 at the existing grade resolution), it fails solely for that row.
- The ledger self-test passes 218 control executions and catches all 25 mutations. It reads both documents and tests all three points, including every row's one-cycle excess.
- All fourteen focused final-head gates pass. Contents controls pass 1501/1501; inventory controls pass 60/60. The generated inventory was written by its own generator in its own commit. Whitespace checks and the final worktree are clean.

No firmware, RTL, queue model, configuration, scheduling constant or submodule pin changed. The other thirteen files from #1004's `{dep}` remain byte-identical, including `SPLIT_CONTROL_MEMORY.md`. The inventory is the sole authorized exception among those fourteen dependency files.

The six retained same-pin builds were rehashed, and their implementation inputs are unchanged since the measured merge. Both sides of each Arty and ALINX comparison still match. This is an identity carry with fresh hash verification, not a new build.

{elfs}
All control map headers: `5f0c602687dacba302959ebb99763e5922aff8ad19f76e7c7c05919b45a936fa`.

Pins on both sides:

```text
{chr(10).join(identity['pins'])}
```

Commits:

- `9da0ba5fc17201e6b030babb8f73714d96f14306` Derive a separate held-egress ledger for USB networking
- `701f294405d47a81eed1079d32b54e1eea4a4f31` Regenerate the documentation inventory for USB networking

Round-7 simulation, filter/LED plants, injection controls and shaping evidence remain applicable because their sources and implementation inputs are unchanged; they were not rerun in this ledger-only round. Earlier physical-route, attachment, external-I/O and whole-image crossing limitations remain open. No new routed image, board observation, independent approval, hosted gate success or issue completion is claimed. The separate source points and existing #969 debt remain explicit. Use `Relates to #1011` and `Relates to #1018`.

Receipts and reproduction: [INDEX.md](receipts/INDEX.md), [derivation](receipts/DERIVATION.md), [qualification](receipts/qualification.json). The foreground jobs retained the unit's CPU weight {resources['cpu_weight']}; scratch used {scratch_bytes/1024**3:.2f} GiB and /data retained {free/1024**3:.2f} GiB free. Gate cleanup removals were logged before execution. No additional build or implementation run was needed.
'''
review = f'''Status: REVIEW READY for the round-8 ledger and inventory change. Local head `{head}`.

The new USB-network ledger point follows the [ruling](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7234489667); existing points and owner bounds are unchanged. All 159 retained traces across eight images regrade identically, and the new point's ledger qualification passes without a new or larger miss. The seven known held-egress service-budget misses remain recorded.

{checks}
The 62.03635-versus-61.99 failure is preserved at the original Arty point. One cycle above 62.14 fails at the USB point; the exact figure passes. The ledger self-test catches all 25 mutations. Fourteen focused final-head gates pass, including documentation, contents and generated-inventory checks. The inventory regeneration is a separate commit.

Arty and both ALINX ELF/map-header identities remain exact at #1004's same pins. Firmware, RTL, queue model and scheduling costs are unchanged. All other thirteen dependency files remain byte-identical. Full receipt bindings, controls and boundaries are in [HANDOFF-r8.md](HANDOFF-r8.md) and [receipts](receipts/INDEX.md).

This is executor evidence for the requested desk scope, not an independent review verdict or whole-issue completion. Physical-route, attachment and board acceptance remain open. Nothing was pushed, posted, flashed or run on the bench.
'''
pr = '''The USB network path copies permitted frames and injects rate-limited best-effort traffic while preserving endpoint priority. Arty status LEDs follow the [fabric-level ruling](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7213370880): LD2 means any media-locked input or open output transmit gate; LD3 means internal selection or a locked selected source. The control image contains no LED register or LED handling.

The [held-egress ruling](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7234489667) gives USB-network Arty its own ledger point under #894's rule. Each row uses the larger original Arty or injected measurement. The table is in `docs/design/USB_NET_PATH.md`; only its last AECP figure differs, at 62.14 ms. The original Arty and 8x8/1if ledgers remain unchanged. These remain seven recorded service-budget misses, bounded by their separate ledger.

All 159 retained traces across eight images regrade identically. Qualification passes at the USB point with no new or larger miss. The unchanged owner row gives load 0.501397, ACMP 29.84 ms, txL 48.90 ms and last notice 117.58 ms. The retained complete wire result is 644.981 us against 1000 us. Controls preserve the 62.03635-versus-61.99 rejection at the original Arty point and reject one cycle over 62.14 at the USB point. All 25 ledger mutations are detected; final documentation and inventory gates pass. Inventory regeneration is a separate commit.

Firmware, RTL, the queue model and scheduling costs are unchanged. The Arty and both ALINX control ELF/map-header comparisons remain byte-identical to #1004's same-pin builds. The other thirteen dependency files are unchanged. Previous simulation, filter and LED plants, injection controls and shaping evidence retain their exact inputs.

Board observations, attachment integration, physical-route qualification, broader candidate gates and independent review remain open. Existing whole-image crossing and external-I/O limitations remain. No physical release or issue completion is claimed.

Relates to #1011
Relates to #1018
'''
(ROUND/'HANDOFF-r8.md').write_text(handoff)
(ROUND/'REVIEW-READY.md').write_text(review)
(ROUND/'PR-BODY.md').write_text(pr)
index = f'''Status: PASS for the round-8 desk scope at `{head}`. No native rerun, implementation change, push, posting or bench operation.

## Decision and qualification

- [ruling.json](ruling.json): exact public ruling and link.
- [DERIVATION.md](DERIVATION.md), [ledger-derivation.json](ledger-derivation.json): all seven original and injected measurements, maxima, figures and margins; both existing ledgers preserved.
- [qualification.json](qualification.json), [qualification-commands.json](qualification-commands.json), [qualification-run.log](qualification-run.log): final-head ledger leg and complete census checks with the unchanged owner model and #969 disposition.
- [egress-ledger.log](egress-ledger.log): all regraded probe instances against the new point.
- [original-arty-negative.log](original-arty-negative.log): expected exit 1 for the retained 62.03635 ms measurement against 61.99 ms, with exactly one finding.
- [usb-at-figure.log](usb-at-figure.log), [usb-one-cycle-over.log](usb-one-cycle-over.log), [boundary-controls.json](boundary-controls.json), [controls/](controls/): exact-limit pass and one-cycle excess rejection using a copy of the retained grade. Production grades are untouched.
- [owner-model.json](owner-model.json): current model equals the retained fixed point; all unchanged owner bounds pass.

## Retained trace regrade

- [retained-trace-identity.json](retained-trace-identity.json): all 159 raw trace hashes and lengths verified against the round-7 archive and completion records; stimuli/status bytes also checked.
- [regraded-identity.json](regraded-identity.json): every regenerated grade matches its retained SHA-256.
- [regrade-commands.json](regrade-commands.json), [regrade-run.log](regrade-run.log), `regrade-<variant>.log`: eight complete regrades, no native execution. The measurement geometry remains `arty-1x1`; only the separate ledger leg selects `arty-usbnet-1x1`.
- [census/](census/): fresh grade files, scripts, status files, journals and per-image summaries. Full raw traces remain in the [round-7 archive](../../round7/receipts/census/ARCHIVE.json), with the original raw and compressed digests; no trace was overwritten.
- [record-classes.log](record-classes.log): cross-image class coverage after regrading.
- [qualification-setup-correction.json](qualification-setup-correction.json), [staged-build-metadata.json](staged-build-metadata.json), [initial-qualification/](initial-qualification/): the first class-check invocation refused missing staged metadata before grading. The unchanged build records were copied beside the results and qualification rerun; no source or trace changed.
- [egress-evidence-identity.json](egress-evidence-identity.json), [egress-evidence-identity.log](egress-evidence-identity.log): all 159 retained wire replay receipts checked against unchanged traces, source bytes and parameters; aggregate verdict rerun. This is evidence carry, not a new wire replay.

## Final-head gates and identity

- [final-gates.json](final-gates.json), [final-gates-run.log](final-gates-run.log): fourteen passing gates and exact CI arguments, interpreter, removal-audit wrapper, head and output digests.
- [ledger-selftest.log](ledger-selftest.log): 218 control executions, all 25 mutations caught. Includes both documentation tables and all three ledger points.
- [inventory-generate.log](inventory-generate.log), [inventory-check.log](inventory-check.log), [inventory-selftest.log](inventory-selftest.log): own-generator regeneration and final freshness; 60 controls pass.
- [contents-selftest.log](contents-selftest.log), [contents-anchors.log](contents-anchors.log), [contents-check.log](contents-check.log), [docs-check.log](docs-check.log), [doc-paths.log](doc-paths.log): final documentation gates, including 1501 contents controls.
- [identity.json](identity.json), [firmware/](firmware/): thirteen unchanged dependency files, unchanged implementation inputs and same pins; six retained ELF/header pairs rehashed and preserved. Arty ELF SHA-256 is `f17d1a9da8ba6e50a1e8cf0af9b77ed434288a1d0a689a357a0c6a57ecda92cf`. No new build is claimed.
- [round8.patch](round8.patch), [local-history.txt](local-history.txt), [final-git-checks.json](final-git-checks.json), [final-head.json](final-head.json): two local commits, separate inventory commit and clean worktree.
- [resources-final.json](resources-final.json): unit weight, CPU affinity, scratch cap and free-space checks. [source/audited-python.py](source/audited-python.py) logs removal paths before deletion by gate fixtures.

## Reproduction

- [source/regrade-retained.py](source/regrade-retained.py) uses unchanged per-group grading and full per-image cross-checks, verifies the retained data and requires exact output hashes. It runs only the regrade path.
- [source/qualify-retained.py](source/qualify-retained.py) runs the new ledger leg, original-point negative control, exact-limit and one-cycle plants, class gate and current owner model.
- [source/verify-egress-carry.py](source/verify-egress-carry.py) checks every retained wire binding and reruns the aggregate verdict.
- [source/final-gates.py](source/final-gates.py) records CI arguments and results at the final head; the wrapper only audits deletions.
- [source/finish-packet.py](source/finish-packet.py) refuses an incomplete or mismatched packet before writing the handoff.

The [round-7 index](../../round7/receipts/INDEX.md) retains native build provenance, full census and fixed-point derivation, injection-chain measurements, filter/LED plants, shaping regressions and their original limitations. Those checks were not rerun here. [MANIFEST.sha256](MANIFEST.sha256) binds this receipt set. Prior root packet entry points are preserved under `prior-root/` before their current links are refreshed.
'''
(OUT/'INDEX.md').write_text(index)
prior = OUT/'prior-root'
prior.mkdir(exist_ok=True)
for name in ('HANDOFF.md','REVIEW-READY.md','PR-BODY.md','receipts/INDEX.md'):
    source=PACKET/name
    if source.is_file():
        target=prior/name
        target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists():
            shutil.copyfile(source,target)
(PACKET/'HANDOFF.md').write_text(f'Status: REVIEW READY for round-8 desk scope. ETA: complete.\n\nCurrent local head: `{head}`.\n\nSee [HANDOFF-r8.md](round8/HANDOFF-r8.md) and [receipts](round8/receipts/INDEX.md). Earlier physical and board acceptance remains open. Nothing pushed or posted.\n')
(PACKET/'REVIEW-READY.md').write_text(review.replace('(HANDOFF-r8.md)','(round8/HANDOFF-r8.md)').replace('(receipts/INDEX.md)','(round8/receipts/INDEX.md)'))
(PACKET/'PR-BODY.md').write_text(pr)
(PACKET/'receipts/INDEX.md').write_text(f'Status: PASS for round-8 desk scope at `{head}`.\n\nThe current packet is [round8/receipts/INDEX.md](../round8/receipts/INDEX.md). It records all 159 retained regrades, final-head gates, identities and negative controls. Prior round-7 evidence remains [available](../round7/receipts/INDEX.md).\n')
record = dict(head=head,branch=git('branch','--show-current'),dependency=dep,tree=git('rev-parse','HEAD^{tree}'),
              commits=git('log','-2','--format=%H %s').splitlines(),worktree_clean=True,
              status='REVIEW READY for round-8 desk scope',qualification_sha256=hashlib.sha256((OUT/'qualification.json').read_bytes()).hexdigest(),
              no_push=True,no_post=True,no_native_rerun=True,no_bench=True)
(OUT/'final-head.json').write_text(json.dumps(record,indent=2)+'\n')
lines=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(OUT))
       for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='MANIFEST.sha256']
(OUT/'MANIFEST.sha256').write_text('\n'.join(lines)+'\n')
print(json.dumps(record,indent=2))
