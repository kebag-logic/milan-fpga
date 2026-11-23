[A826] REVIEW READY

Local head `2e278379c1ae9ea09063b3e3cb183d0e8a3f0929`, branch `pf-loopbram-1`, intended base `dev-soft-core`. No push, PR publication, merge or board operation.

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

Both disabled shapes match the round-1 baseline byte for byte for 12 builder artifacts, descriptor images, firmware ROM load bytes, and generated memory initialization files. The additional SoC text comparison excludes generated timestamp and hierarchy comments; raw text hashes differ in those comments. FPGA configuration bitstreams and ELF debug sections are outside this identity claim.

Firmware ROM sizes: 126,432 bytes at 1x1 and 140,544 bytes at 8x8. Descriptor images: 7,512 and 20,800 bytes. Per-file hashes and independent baseline reproduction are in the identity receipts. `head-compatibility.json` proves that later fixture and documentation commits changed none of the audio-test or physical-export inputs.

## Physical measurements

As required by docs/design/AREA_BUDGET.md, the selected recipe has the largest minimum setup slack among the prescribed recipes and must pass every floor. The fixed Slow/Fast timing models are each reported at 0 C and 85 C; these temperature settings are power metadata, not four independent timing models. Part: xc7a100t-fgg484-2, commercial grade. Recipe: AreaOptimized_high synthesis, ExploreArea optimization, the listed placement directive, AggressiveExplore physical optimization and routing, then physical optimization and signoff reports. Every build uses the required slot wrapper with `VIVADO_SLOTS=2` and `VIVADO_MIN_GB=20`.

| Shape | Placement | LUT | FF | RAMB36 / RAMB18 | Slices | Min WNS ns | Min WHS ns | Floor |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 1x1/1if | AltSpreadLogic_high | 32971 | 42686 | 63 / 37 | 14290 | 0.290 | 0.036 | PASS |
| 8x8/1if | ExtraPostPlacementOpt | 49097 | 54663 | 94 / 34 | 15803 | 0.233 | 0.025 | PASS |

Complete prescribed sweep:

| Shape | Placement | LUT | FF | RAMB36 / RAMB18 | Slices | Min WNS ns | Min WHS ns | Floor |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 1x1/1if | ExtraPostPlacementOpt | 32886 | 42687 | 63 / 37 | 13687 | 0.099 | 0.025 | PASS |
| 1x1/1if | AltSpreadLogic_high | 32971 | 42686 | 63 / 37 | 14290 | 0.290 | 0.036 | PASS |
| 1x1/1if | ExtraTimingOpt | 32959 | 42686 | 63 / 37 | 14288 | 0.175 | 0.036 | PASS |
| 8x8/1if | ExtraPostPlacementOpt | 49097 | 54663 | 94 / 34 | 15803 | 0.233 | 0.025 | PASS |
| 8x8/1if | AltSpreadLogic_high | 49072 | 54661 | 94 / 34 | 15701 | 0.106 | 0.036 | PASS |
| 8x8/1if | ExtraTimingOpt | 49114 | 54660 | 94 / 34 | 15716 | 0.176 | 0.036 | PASS |

Each accepted route has zero routing errors. Reports preserve DRC warnings; no zero-warning or bitstream-generation claim is made.

## Leaf comparison

Fresh same-source measurements, 8x8/1if, 50 MHz, AreaOptimized_high synthesis and ExploreArea optimization:

| Increment over disabled leaf | LUT | FF | RAMB36 | RAMB18 |
|---|---:|---:|---:|---:|
| Mapped-copy render queue | 585 | 202 | 0 | 1 |
| Synchronous capture source | 65 | 57 | 0 | 0 |
| New lane total, 63 destinations | 650 | 259 | 0 | 1 |
| Legacy capture lane, 64 channels | 2088 | 2360 | 1 | 0 |

These increments isolate the leaves. Integrated figures include input-map and control-image growth. The new lane provides 63 independent destinations; the legacy lane exposes 64 stream channels with different mapping semantics. Historical +2303 LUT / +1542 FF figures remain context only; the table is the fresh comparison.

## S14 debt and proof limits

The enabled 8x8 control-memory allocation is 70.5 RAMB36-equivalent tiles: +11.5 above the unchanged 59.0 ledger entry, or +14.5 above the 56-tile default budget. This is S14 debt. The normal allocator still refuses that enabled image. The separate measurement export records the refusal and overrides the allocation check only in its temporary process; no owner ledger or product guard changed. The 1x1 allocation is 46.5 tiles (45.0 disabled), within 56.

No owner bound, interface capacity, shipping configuration or bench image changed. Independent review and hosted merge evidence remain outside this author verdict.

## Reproduction

`$SCRATCH` is `/data-2/milan/tmp/loopbram-a826`. Commands remained foreground children of logged runners, with at most four harness legs. Physical runners record exact commands, durations and exit statuses; waiting for a slot contributes to those durations. Receipt copies replace local roots with `$CHECKOUT` and `$SCRATCH` and include runners and measurement configurations.

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
VIVADO_SLOTS=2 VIVADO_MIN_GB=20 $MANAGEMENT/2026-09-23/vivado-slot.sh python3 scripts/xvlog_gate.py --check
python3 "$SCRATCH/run_leaf.py"
python3 "$SCRATCH/run_capture_leaf.py"
python3 "$SCRATCH/run_routes.py"
```

[receipts/INDEX.md](receipts/INDEX.md) indexes compressed evidence, hashes and privacy assertions. The builder union binds head `2e278379c1ae9ea09063b3e3cb183d0e8a3f0929` and tree `3ae715044d525c20cffba94f4cabb2c3370803b2`.
