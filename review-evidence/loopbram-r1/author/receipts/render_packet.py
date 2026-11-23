import json,subprocess
from pathlib import Path
s=Path('$SCRATCH')
out=Path('<home-path>/milan-fpga-management/2026-09-23/loopbram-a826/round2')
root=Path('$CHECKOUT')
def read(name):return json.loads((s/name).read_text())
head=read('source_identity.json')['head']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()==head
assert not subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True)
rows=read('route-summary.json');leaf=read('leaf-capture-summary.json');queue=read('leaf-queue-summary.json')
assert len(rows)==6 and all('run' in r for r in rows),'Physical sweep still running'
assert 'new_total_delta' in leaf,'Capture comparison still running'
for name in ['off','mapped','legacy']:assert read(f'leaf-capture/{name}/result.json')['exit']==0
union=read('builder-union/union.json')
assert union['head']==head and union['union']=='pass' and len(union['inventory'])==114
assert read('yosys/run.json')['exit']==0
assert all(r['exit']==0 for r in read('regression-summary.json')['cases'])
assert all(r['passed'] for r in read('mutants-head/results.json'))
shapes=['endstation_ax7101_1x1_tdm8','endstation_ax7101_8x8']
short={shapes[0]:'1x1/1if',shapes[1]:'8x8/1if'}
best={shape:max((r for r in rows if r['shape']==shape and r.get('complete') and r.get('run',{}).get('exit')==0),key=lambda r:(r['min_WNS_ns'],r['min_WHS_ns'])) for shape in shapes}
assert all(r.get('floor_pass') for r in best.values()), 'Selected best-WNS recipe does not meet every floor'
def num(x):return f'{x:g}'
def route_table(selected):
 lines=['| Shape | Placement | LUT | FF | RAMB36 / RAMB18 | Slices | Min WNS ns | Min WHS ns | Floor |','|---|---|---:|---:|---:|---:|---:|---:|---|']
 for r in selected:
  if not r.get('complete'):
   lines.append(f"| {short[r['shape']]} | {r['directive']} | - | - | - | - | - | - | exit {r['run']['exit']}; see log |")
   continue
  u=r['utilization']
  lines.append(f"| {short[r['shape']]} | {r['directive']} | {num(u['Slice LUTs*'])} | {num(u['Slice Registers'])} | {num(u['RAMB36/FIFO*'])} / {num(u['RAMB18'])} | {num(u['Occupied slices'])} | {r['min_WNS_ns']:.3f} | {r['min_WHS_ns']:.3f} | {'PASS' if r.get('floor_pass') else 'FAIL'} |")
 return '\n'.join(lines)
selected=route_table([best[x] for x in shapes]);sweep=route_table(rows)
new=leaf['new_total_delta'];old=leaf['legacy_delta'];capture=leaf['mapped_delta'];q=queue['delta']
leaf_lines=['| Increment over disabled leaf | LUT | FF | RAMB36 | RAMB18 |','|---|---:|---:|---:|---:|']
for name,v in [('Mapped-copy render queue',q),('Synchronous capture source',capture),('New lane total, 63 destinations',new),('Legacy capture lane, 64 channels',old)]:
 leaf_lines.append(f"| {name} | {num(v['Slice LUTs*'])} | {num(v['Slice Registers'])} | {num(v['RAMB36/FIFO*'])} | {num(v['RAMB18'])} |")
leaf_table='\n'.join(leaf_lines)
limits='The enabled 8x8 control-memory allocation is 70.5 RAMB36-equivalent tiles: +11.5 above the unchanged 59.0 ledger entry, or +14.5 above the 56-tile default budget. This is S14 debt. The normal allocator still refuses that enabled image. The separate measurement export records the refusal and overrides the allocation check only in its temporary process; no owner ledger or product guard changed. The 1x1 allocation is 46.5 tiles (45.0 disabled), within 56.'
identity='Both disabled shapes match the round-1 baseline byte for byte for 12 builder artifacts, descriptor images, firmware ROM load bytes, and generated memory initialization files. The additional SoC text comparison excludes generated timestamp and hierarchy comments; raw text hashes differ in those comments. FPGA configuration bitstreams and ELF debug sections are outside this identity claim.'
review=f'''[A826] REVIEW READY

Local head `{head}`, branch `pf-loopbram-1`, intended base `dev-soft-core`. No push, PR publication, merge or board operation.

## Scope and authority

Implements the [A10 ruling](https://github.com/kebag-logic/milan-fpga/issues/979#issuecomment-7096503041) on #979. Milan v1.2 5.3.3.8 and IEEE 1722.1-2021 7.2.19 remain authoritative. The first round-2 probe accepted a nine-cluster port with page size eight. Selected input widths: `[9,8,8,8,8,8,8,7]`. There are 63 independent mono loopback destinations plus the independent physical destination. The 65-key negative control remains refused. The 1x1 shape has eight physical plus eight loopback destinations, using 16 keys.

`INPUT_LOOPBACK_P` defaults to zero. An optional scheduled read copies samples selected by committed input mappings from the render queue into a separate four-page synchronous block RAM. Capture source bucket 6 reads these destinations sequentially, with one media frame added latency. Missing, expired or invalidated availability produces silence. Clock-loss handling flushes retained source rows before restart. Already captured packet data remains in flight, as specified in DESIGN.md.

The split backend uses its existing layout-3 NAME capacity. The all-fabric 128-name bound remains unchanged; its capacity fixtures now select that backend explicitly, preserving their original negative controls. Parameter documentation and the authoritative key table describe the new option.

## Acceptance evidence

| Obligation | Result |
|---|---|
| Nine-cluster port, 64/65-key boundary, 1x1 16-key shape | PASS; topology probe, complete descriptors and builder gate |
| Disabled identity | PASS within the scope below |
| Received AAF through mapped copy to transmitted AAF | PASS; 8x8: 79,587 checks / 468 packets; 1x1: 76,017 checks / 447 packets |
| Copy, schedule and invalidation controls | PASS; clean control and all seven planted defects detected |
| Affected render/capture regressions | PASS; capture lockstep, render queue including 28 mutants, datapath render including five leg controls, and capture coherence |
| Builder union | PASS; 114 gates exactly once on this head; required elaboration and RV32 checks satisfied |
| Portability and local quality gates | PASS; 63 synthesis tops and structural checks; lint 89 <= 89; analysis gate zero findings; documentation, paths, style, hygiene, idiom, source-list and saved-state checks |
| Physical timing | PASS at both selected shapes, all required corner reports, WNS >= +0.030 ns and WHS >= 0 |
| Resource bounds | Unchanged; enabled 8x8 overflow recorded as S14 debt |

The wire harness instantiates the real parser, monitor, depacketizer, render queue, capture mapper and packetizer. It supplies committed logical maps directly. Protocol command acceptance and physical projection remain the existing datapath campaigns' responsibility; the new harness is not a board soak. It covers cross-stream mapping, channel permutations, fan-out, invalid destinations, missing data, map replacement/REMOVE, invalidation during copying, reset, bind flush, long absence, live timestamp wrap and clock stop/restart.

Planted defects: ignored mapping, wrong bank parity, skipped copy, ignored invalidation, retained word, missing clock-loss flush and wrong latency. Each must fail the unchanged sample scoreboard; a compiler failure is not a catch. `mutants-head/results.json` records every command and verdict.

The builder union records one pre-existing row as not run: gate 11's historical Arty mf48 placement-report calibration, because that external report is absent. No elaboration arm was skipped for a toolchain reason. Full repository simulation aggregation and hosted checks are not claimed by this author handoff.

## Disabled identity

{identity}

Firmware ROM sizes: 126,432 bytes at 1x1 and 140,544 bytes at 8x8. Descriptor images: 7,512 and 20,800 bytes. Per-file hashes and independent baseline reproduction are in the identity receipts. `head-compatibility.json` proves that later fixture and documentation commits changed none of the audio-test or physical-export inputs.

## Physical measurements

As required by docs/design/AREA_BUDGET.md, the selected recipe has the largest minimum setup slack among the prescribed recipes and must pass every floor. The fixed Slow/Fast timing models are each reported at 0 C and 85 C; these temperature settings are power metadata, not four independent timing models. Part: xc7a100t-fgg484-2, commercial grade. Recipe: AreaOptimized_high synthesis, ExploreArea optimization, the listed placement directive, AggressiveExplore physical optimization and routing, then physical optimization and signoff reports. Every build uses the required slot wrapper with `VIVADO_SLOTS=2` and `VIVADO_MIN_GB=20`.

{selected}

Complete prescribed sweep:

{sweep}

Each accepted route has zero routing errors. Reports preserve DRC warnings; no zero-warning or bitstream-generation claim is made.

## Leaf comparison

Fresh same-source measurements, 8x8/1if, 50 MHz, AreaOptimized_high synthesis and ExploreArea optimization:

{leaf_table}

These increments isolate the leaves. Integrated figures include input-map and control-image growth. The new lane provides 63 independent destinations; the legacy lane exposes 64 stream channels with different mapping semantics. Historical +2303 LUT / +1542 FF figures remain context only; the table is the fresh comparison.

## S14 debt and proof limits

{limits}

No owner bound, interface capacity, shipping configuration or bench image changed. Independent review and hosted merge evidence remain outside this author verdict.

## Reproduction

`$SCRATCH` is `$SCRATCH`. Commands remained foreground children of logged runners, with at most four harness legs. Physical runners record exact commands, durations and exit statuses; waiting for a slot contributes to those durations. Receipt copies replace local roots with `$CHECKOUT` and `$SCRATCH` and include runners and measurement configurations.

```sh
make -s -C tb/verilator/input_loopback VERILATOR_JOBS=4 MDIR="$SCRATCH/regressions/input-final"
python3 tb/verilator/input_loopback/mutants.py --output "$SCRATCH/mutants-head"
make -s -C tb/verilator/chmap_capture VERILATOR_JOBS=4 run MDIR="$SCRATCH/regressions/capture"
make -s -C tb/verilator/render_queue VERILATOR_JOBS=4 all
make -s -C tb/verilator/milan_dp_render VERILATOR_JOBS=4 run ship8
make -s -C tb/verilator/capture_coherence VERILATOR_JOBS=4 run dp
python3 "$SCRATCH/run_builder_union.py"
syn/yosys/run.sh --results "$SCRATCH/yosys/results"
python3 scripts/lint_rtl.py --check
VIVADO_SLOTS=2 VIVADO_MIN_GB=20 <home-path>/milan-fpga-management/2026-09-23/vivado-slot.sh python3 scripts/xvlog_gate.py --check
python3 "$SCRATCH/run_leaf.py"
python3 "$SCRATCH/run_capture_leaf.py"
python3 "$SCRATCH/run_routes.py"
```

[receipts/INDEX.md](receipts/INDEX.md) indexes compressed evidence, hashes and privacy assertions. The builder union binds head `{head}` and tree `{union['tree']}`.
'''
(out/'REVIEW-READY.md').write_text(review)
handoff=f'''Status: REVIEW READY for independent review. ETA: author work complete.

[A826], issue #979, round 2. Local head `{head}` on `pf-loopbram-1`; intended base `dev-soft-core`. Worktree clean. No push or board operation.

The nine-cluster port probe passed. Implemented widths are `[9,8,8,8,8,8,8,7]`: port 0 retains physical plus eight loopback destinations; port 7 has seven. The 63 independent loopback destinations and independent physical destination fit 64 keys. The 1x1 shape has 16 keys. The option defaults off.

The separate sample RAM, scheduled mapped copy, synchronous reads, one-frame delay and invalidation/silence behavior are implemented. Both wire shapes pass, all seven fault plants are detected, affected render/capture suites pass, the 114-gate builder union passes, and all 63 portability tops pass. One existing historical calibration row remains unrun because its external Arty report is absent. Disabled builder artifacts, descriptor images and firmware ROM bytes match the baseline.

{selected}

The fresh leaf increment is {num(new['Slice LUTs*'])} LUTs, {num(new['Slice Registers'])} FFs and {num(new['RAMB18'])} RAMB18, versus {num(old['Slice LUTs*'])} LUTs, {num(old['Slice Registers'])} FFs and {num(old['RAMB36/FIFO*'])} RAMB36 for the legacy capture-lane increment. Integrated figures include map and control-image growth.

{limits}

[REVIEW-READY.md](REVIEW-READY.md) records commands, the complete placement sweep, proof limits and acceptance evidence. [PR-BODY.md](PR-BODY.md) is prepared for `pf-loopbram-1` into `dev-soft-core`. [receipts/INDEX.md](receipts/INDEX.md) indexes compressed, privacy-checked receipts. [DESIGN.md](DESIGN.md) records the chosen design. No independent review or merge approval is claimed.

REVIEW READY {head}
'''
(out/'HANDOFF-r2.md').write_text(handoff)
u8=best[shapes[1]]['utilization']
pr=f'''Target: `pf-loopbram-1` into `dev-soft-core`. Closes #979.

Adds optional loopback controlled by the input map. At 8x8, 63 independent mono loopback destinations share the existing 64-key space with an independent physical destination: port 0 has physical plus eight loopback destinations, and port 7 has seven. The 1x1 shape has eight physical and eight loopback destinations.

`INPUT_LOOPBACK_P` defaults to zero. Received samples are copied from the presentation queue into a separate block RAM and read synchronously by the capture mapper, adding one media frame. Missing, expired and invalidated data produces silence. Disabled builder artifacts, descriptor images and firmware ROM bytes match the baseline at both sizes.

Sample-exact wire tests pass at both sizes, all seven planted copy/scheduling/invalidation defects are detected, affected render and capture regressions pass, and the 114-gate builder union passes. Selected routes meet the unchanged setup and hold floors at every required corner. The 8x8 route uses {num(u8['Slice LUTs*'])} LUTs, {num(u8['Slice Registers'])} FFs and {num(u8['Block RAM Tile'])} BRAM tiles; the new leaf increment is {num(new['Slice LUTs*'])} LUTs, {num(new['Slice Registers'])} FFs and one RAMB18.

The enabled 8x8 control-memory allocation is 70.5 tiles, 11.5 above its existing ledger entry. This remains S14 debt: the normal allocation guard still refuses that image, and owner bounds remain unchanged. Resource measurements use a separate measurement export. The builder union records one existing historical calibration row as unrun because its external report is absent.
'''
(out/'PR-BODY.md').write_text(pr)
(out/'DESIGN.md').write_bytes((root/'docs/design/INPUT_MAPPED_LOOPBACK.md').read_bytes())
print('Rendered final packet for',head)
