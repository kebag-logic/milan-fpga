import json,subprocess
from pathlib import Path
s=Path('$SCRATCH')
out=Path('<home-path>/milan-fpga-management/2026-09-23/loopbram-a826/round2')
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd='$CHECKOUT',text=True).strip()
assert (out/'HANDOFF-r2.md').read_text().splitlines()[-1]=='REVIEW READY '+head
rows=json.loads((s/'route-summary.json').read_text())
assert len(rows)==6 and all('run' in r for r in rows)
leaf=json.loads((s/'leaf-capture-summary.json').read_text())
lines=['[A826] REVIEW READY',f'Commit: {head} (local only, unpushed). Branch: pf-loopbram-1; intended base: dev-soft-core.','',
'Changed: implemented the option-B input-mapped BRAM loopback behind INPUT_LOOPBACK_P=0 by default. The nine-cluster-port probe passed before implementation. Selected input widths [9,8,8,8,8,8,8,7] keep port 0 physical + 8 and port 7 at 7: 63 independent mono loopback destinations plus the independent physical destination use 64 keys. The 65-key negative control still refuses. The 1x1 shape has 8 physical + 8 loopback destinations (16 keys).',
'',
'Acceptance: synchronous mapped source reads, a separate block RAM, scheduled copy, one media frame of added latency, and silence after missing/expired/invalidated data are implemented. Sample-exact received-AAF → mapped-copy → transmitted-AAF checks pass: 79,587 checks / 468 packets at 8x8 and 76,017 / 447 at 1x1. The clean control and seven fault plants pass their expected verdicts, including mapping, bank, skipped copy, invalidation, retained words, clock-loss flush and latency defects.',
'',
'Disabled identity: both shapes match the round-1 baseline byte for byte for all 12 builder artifacts, descriptor images, firmware ROM load bytes and generated initialization files. Generated SoC text comparison excludes timestamp/hierarchy comments; raw text hashes differ there. No FPGA bitstream or ELF debug-section identity claim.',
'',
'Validation: affected capture, render queue (28 mutants), full datapath render and capture-coherence campaigns pass. Complete builder union passes all 114 gates exactly once on this head, with mandatory elaboration and RV32 requirements satisfied. One existing calibration row remains unrun because the external historical Arty mf48 placement report is absent. Portability passes 63 tops and structural controls; lint is 89 <= 89; analysis has zero findings; documentation, style, paths, hygiene, idiom, saved-state and source-list gates pass.',
'',
'Physical evidence: all builds used vivado-slot.sh with VIVADO_SLOTS=2 and VIVADO_MIN_GB=20. Best worst-corner WNS selects the recipe; the selected recipe meets #818 at every corner (WNS >= +0.030 ns; WHS >= 0). Full three-directive sweeps are in the receipt packet.',
'',
'| Shape | Selected placement | LUT | FF | RAMB36 / RAMB18 | Occupied slices | Min WNS / WHS ns |',
'|---|---|---:|---:|---:|---:|---|']
for shape,label in [('endstation_ax7101_1x1_tdm8','1x1/1if'),('endstation_ax7101_8x8','8x8/1if')]:
 r=max((r for r in rows if r['shape']==shape and r.get('complete') and r['run']['exit']==0),key=lambda r:(r['min_WNS_ns'],r['min_WHS_ns']))
 assert r['floor_pass']
 u=r['utilization'];lines.append(f"| {label} | {r['directive']} | {u['Slice LUTs*']:g} | {u['Slice Registers']:g} | {u['RAMB36/FIFO*']:g} / {u['RAMB18']:g} | {u['Occupied slices']:g} | +{r['min_WNS_ns']:.3f} / +{r['min_WHS_ns']:.3f} |")
a=leaf['new_total_delta'];b=leaf['legacy_delta']
lines += ['',f"Fresh leaf increment at 8x8/1if: new lane +{a['Slice LUTs*']:g} LUT / +{a['Slice Registers']:g} FF / +{a['RAMB18']:g} RAMB18; legacy capture lane +{b['Slice LUTs*']:g} LUT / +{b['Slice Registers']:g} FF / +{b['RAMB36/FIFO*']:g} RAMB36. These are fresh measurements, separate from the historical comparison; the new lane has 63 independent destinations and the legacy lane has 64 stream channels.",'',
'Open debt: enabled 8x8 control allocation is 70.5 BRAM tiles, +11.5 over the unchanged 59-tile ledger entry (+14.5 over the default 56). Recorded as S14 debt. The normal allocator still refuses that enabled image; physical measurements use a separate temporary measurement export. No owner bound or product guard moved. Enabled 1x1 is 46.5 tiles, within 56.',
'',
'Reproduction: `make -s -C tb/verilator/input_loopback VERILATOR_JOBS=4`; `python3 tb/verilator/input_loopback/mutants.py --output <scratch>/mutants-head`; `make -s -C tb/verilator/chmap_capture run`; `make -s -C tb/verilator/render_queue all`; `make -s -C tb/verilator/milan_dp_render run ship8`; `make -s -C tb/verilator/capture_coherence run dp`; builder union with `--require-elaboration --require-rv32`; `syn/yosys/run.sh`. Exact commands, leaf/sweep runners, per-corner reports, hashes, source-compatibility proof and privacy checks are archived in the packet.',
'',
'Packet: <home-path>/milan-fpga-management/2026-09-23/loopbram-a826/round2/ — HANDOFF-r2.md, REVIEW-READY.md, PR-BODY.md, DESIGN.md and receipts/INDEX.md. All compressed receipts and decompressed payloads satisfy privacy.scrub_redact(b)==b. Scratch remains below 15 GB; no push or board operation. This is an author handoff; independent review remains pending.']
(s/'issue-comment.txt').write_text('\n'.join(lines)+'\n')
print('Prepared one final issue-comment body; no network write performed')
