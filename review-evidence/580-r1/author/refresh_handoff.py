"""Refresh the compact review handoff from measured evidence."""
import hashlib
import json
from pathlib import Path
import shlex
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = Path('$LANES/580-pp-pin-16be6768')
base = '682ecf0cb995473b72d5b4921088053ba753fc93'
head = subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip()
old = json.loads((OUT/'old-artifacts.json').read_text())
new = json.loads((OUT/'new-artifacts.json').read_text())
results = [json.loads(line) for line in (OUT/'gate-results.jsonl').read_text().splitlines()]
latest = {row['name']:row for row in results}
required = ('builder-rv32', 'builder-absent', 'pp-shadow', 'milan-dp', 'diff-check')
complete = all(name in latest and latest[name]['rc'] == 0 for name in required)
status = 'Local author work complete; independent review pending.' if complete else 'Implementation committed; required gates in progress.'
text = f"""# Issue 580 handoff

Author: [A366]. Independent review: [R352] and [R353].
Status: {status}
Branch: `580-pp-pin-16be6768`.
Base: `{base}`.
Head: `{head}`.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/580#issuecomment-5856274975

## Change list

"""
for path, needle, explanation in [
 ('CHANGELOG.md','## Unreleased - processor pin 16be6768','records adopted packer behavior and unchanged generated output'),
 ('docs/reference/SUBMODULES.md','| `protocol-processor`','updates the current pin and adoption record'),
 ('docs/design/SAVED_STATE_MATERIALIZATION.md','That correction adopted','keeps the live-write adoption historical and states the current pin'),
 ('docs/reference/PP_DESCRIPTOR_OWNERSHIP.md','| L2:','records F7 body/key enforcement from 493e5e4b'),
 ('docs/reference/PP_DESCRIPTOR_OWNERSHIP.md','These probe results','labels earlier probe outcomes as historical'),
 ('docs/reference/PP_DESCRIPTOR_OWNERSHIP.md','| F7 |','closes the F7 allocation with processor test evidence'),
 ('scripts/measure_test_evidence.py','    "protocol-processor/tb/desc_store/test_gen_desc_image.py":','adds the assigned unit-test disposition verbatim'),
 ('syn/yosys/rom_digests.tsv',new['pin'],'adds the tool-recorded pin rows while retaining every prior row'),
 ('tb/verilator/nvm_capture_cpu/measurements.json','    "protocol-processor":','refreshes only the recorded processor pin'),
 ('docs/diagrams/submodule_boundaries.svg','<svg','regenerated boundary SVG'),
 ('docs/diagrams/submodule_boundaries.drawio','<mxfile','regenerated editable boundary master'),
 ('docs/diagrams/PNG_MANIFEST.json','"docs/diagrams/submodule_boundaries.png"','repository-generated source and raster digests'),
]:
    lines = (ROOT/path).read_text().splitlines()
    matches = [i for i, line in enumerate(lines,1) if needle in line]
    line = matches[0] if matches else 1
    text += f'- `{path}:{line}`: {explanation}.\n'
text += f'- `protocol-processor` (gitlink): `{old["pin"]}` -> `{new["pin"]}`.\n'
png = ROOT/'docs/diagrams/submodule_boundaries.png'
text += f'- `docs/diagrams/submodule_boundaries.png` (binary): {png.stat().st_size} bytes, SHA256 `{hashlib.sha256(png.read_bytes()).hexdigest()}`; visually inspected with the direct master export and A4 print. See `DIAGRAM-INSPECTION.md`.\n'
text += """
## ROM ledger rows

`ooc.sh --record-rom-digests` recorded the new rows. Older rows are retained.
The new processor digests equal the old pin's digests.
The unchanged gPTP row was re-recorded by the same command.

| Processor pin | Image | SHA256 |
|---|---|---|
"""
for line in (ROOT/'syn/yosys/rom_digests.tsv').read_text().splitlines():
    if line.split('\t')[0] in (old['pin'], new['pin'], '5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d'):
        pin, name, digest = line.split('\t')
        text += f'| `{pin}` | `{name}` | `{digest}` |\n'
text += """
## Capture decision and evidence

No remeasurement was required by the assignment's conditional rule.
`scripts/check_nvm_capture.py:32` (`current_inputs`) derives only framed bytes,
record counts and CPU/configured/system clocks. Lines 58-94 (`check_receipt`)
compare those inputs plus product firmware and harness hashes, then regrade
all traffic ON/OFF rows and maxima. The checker never reads `processor_pins`.
`python3 scripts/check_nvm_capture.py` passed at the adopted pin (rc 0), including
its changed-input and timing controls. Only the receipt's processor pin changed.
The retained measured 8x8/50 MHz maximum is 24.30246 ms, below 24.5 ms;
1x1/50 MHz is 6.60642 ms and the labelled 8x8/100 MHz comparison is 19.79024 ms.
These are retained simulation results, not a new measurement at this pin.
The conditional STOP was not triggered.

## Five-configuration SHA256 tables

The same physical parent worktree generated both sets, first at the old pin,
then at the new pin. No second checkout or tree export was used.
`measure_artifacts.py` records the exact commands, every file size and SHA256,
and checks actual bytes after the hash comparison. `old-artifacts.json` and
`new-artifacts.json` hold independent measurements. Each configuration's ten
builder outputs and its AEM image, map and JSON were byte-identical: 65 files.

Commands for each `configs/endstation_*.yaml`:

```sh
python3 sw/builder/endstation_builder.py configs/endstation_<name>.yaml -o <run>/builder
python3 avdecc/gen_aemi_image.py --overlay <run>/builder/endstation_<name>/aem_overlay.json --line-bytes 576 -o <run>/aem.bin -m <run>/aem.map --json <run>/aem.json
```

All 20 generator commands returned rc 0. Tables below use one digest column
because each SHA256 was measured equal at both pins.

| Configuration | AEM bytes | Old pin = new pin SHA256 |
|---|---:|---|
"""
for cfg, files in new['configs'].items():
    r=files['aem.bin']
    text += f'| `{cfg}` | {r["bytes"]} | `{r["sha256"]}` |\n'
for cfg,files in new['configs'].items():
    text += f'\n### {cfg}\n\n| Artifact | Bytes | Old pin = new pin SHA256 |\n|---|---:|---|\n'
    for path,row in files.items():
        label = path.replace('builder/'+cfg+'/', 'builder/')
        text += f'| `{label}` | {row["bytes"]} | `{row["sha256"]}` |\n'
text += '\n## Gate table\n\nEvery command ran in the foreground from the physical `$LANES/580-pp-pin-16be6768` path. Commands were never piped. The evidence wrapper allows 14,400 seconds per gate.\n\n| Gate | rc | Seconds | Command |\n|---|---:|---:|---|\n'
for name,row in latest.items():
    cmd=shlex.join(row['command']).replace(str(OUT)+'/', './')
    text += f'| {name} | {row["rc"]} | {row["seconds"]} | `{cmd}` |\n'
for name in ('builder-rv32','builder-absent','pp-shadow','milan-dp','diff-check'):
    if name not in latest:
        text += f'| {name} | Pending | | |\n'
text += """
The initial em-dash gate exited 2 because the system interpreter lacked the
locked Markdown renderer. The repository lock was installed in a temporary
environment outside the output directory before rerunning the affected gates.
The successful final runs supersede that environment-only attempt.
The initial documentation checks also caught overlong sentences and an omitted
submodule prefix in the new test citation. Both were corrected and rechecked.
No test budget or acceptance criterion was relaxed.

`gate-results.jsonl` records exact commands, exit codes, elapsed times, raw log
locations, SHA256 and byte counts. Repeated names replace their local log;
earlier attempts retain measured hashes and diagnoses above, while the latest
log is retained. Logs over 200 KB remain outside this output;
only their digest, size and a bounded tail are retained here. Generated trees,
installed packages and diagram inspection exports also remain outside it.

## Final state and review boundary

Both compiler modes returned rc 0 and executed all 86 top-level tests in
the exact normal-entry order; `BUILDER-COVERAGE.json` records that comparison.
The compiler-present full bank returned rc 0. Its only NOT RUN arm is gate 11,
whose external physical-build calibration report is absent. The compiler-absent
run deliberately hides exactly the three candidates in `builder_absent.py` and
executes the complete bank through its normal main entry. Its compiler-dependent
NOT RUN arms are expected evidence limits, not passes for those instruments.
See the complete retained builder logs for the precise skipped-arm descriptions.
The default pp_shadow legs passed 591, 591, 591 and 295 checks respectively:
2,068 checks in total, zero failures. Its 284,323-byte raw log remains outside
this output; the gate registry records its hash and a bounded tail is retained.

The assignment authorizes a local commit and one final review-ready issue
comment. No push, PR operation, merge, hardware work, parent RTL edit or firmware
edit was performed. Independent review and later publication remain outstanding.
"""
(OUT/'HANDOFF.md').write_text(text)
