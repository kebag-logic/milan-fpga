[A665]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN at `5f0d5bf9`: the full sweep 64/64 suites, 2,189,325 checks, 0 failures; `obj_crflic` 427/0 and the new `obj_tspec8` 61/0; `crflic-mutants` 10/10; route-1x1, ooc-1x1 and ooc-8x8 PASS against the eleventh record (route SLICE -4) -- `774-crf-tspec-max-frame` -> `dev`

## Linked Issue / roles

Closes #774
Relates to protocol-processor #190

Executor: `[A665]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

The CRF Talker Advertise declared the AAF talker's MaxFrameSize: 217 on the 1x1 TDM8 image, where Milan v1.2
4.3.3.2 Table 4.4 gives "CRF, 1 ts/pdu" 28 + 1 = 29. The processor has taken one MaxFrameSize per source since
its PR #194 (pin `93fb0b2d`); the wrapper still took one value and copied it into every slot, and the datapath fed it
talker 0's AAF value.

| Piece | Change |
|---|---|
| `hdl/milan/KL_pp_shadow.sv` | `cfg_tspec_max_frame_i` is `[N_STREAM_OUT_P*16-1:0]`, one value per stream output, `[16*s +: 16]` like `cfg_stream_id_i`, passed straight to the processor. The "scratch only" every-slot copy is gone. |
| `hdl/ieee1722/crf/KL_crf_tx.sv` | The AVTPDU length is derived: `CRF_HDR_C` (20, IEEE 1722-2016 10.4) + `CRF_DLEN_C` (crf_data_length 8, one timestamp). A new constant output `tspec_max_frame_o` = AVTPDU + 1 = 29 carries the Table 4.4 value from the PDU shape the module builds. The stale "declare 42, the padded MSDU" comment is corrected. |
| `hdl/milan/milan_datapath.sv` | `g_pp_maxf` builds `pp_src_maxf_w`, one slot per talker source: AAF talker t from its own `tctx_maxf_w[t]` (24*N + 24 + 1), the CRF Media Clock Output slot (`CRF_TUID_C`) from `KL_crf_tx`'s output. No literal. |
| `tb/verilator/milan_dp/sim_crf_licence.cpp` | `[TSPEC]` decodes the TSpec of every Talker Advertise value the DUT sends (FirstValue octets 16..19; a packed vector's value n carries FirstValue's TSpec, IEEE 802.1Q-2018 35.2.2.8) and grades each source against Table 4.4 computed by the harness, MaxIntervalFrames 1, and, on the 1x1, against the longest AVTPDU that source emitted plus one. `TSPEC_ONLY_TB` builds it alone for another shape. The boot checks the source count against `ADP_TALKER`; `MAAP_CTRL` claims one address per source. |
| `tb/verilator/milan_dp/Makefile` | `obj_crflic` passes `WIRE_CHANS_TB`; new `obj_tspec8` leg (AX 8x8, nine sources, the crflic grid) in the default run; `crflic-mutants` depends on both. |
| `tb/verilator/milan_dp/crflic_mutants.py` | The planted control "every source declares talker 0's TSpec" (`{ACMP_SRC_C{tctx_maxf_w[0]}}`, the integration before this change) on both legs, each beside its clean control. |
| docs | `milan_dp` README (leg table, `[TSPEC]` phase, failing arms), `TESTING.md`, IEEE 802.1Q traceability SRP-10, the Milan compliance matrix 4.3.3 row, the `LWSRP_TSPEC` register note, the submodule adoption row, `CHANGELOG.md`, `test_sim_pool.py`'s recorded leg inventory. |

Declared MaxFrameSize, from the DUT's own MSRP frames in simulation:

| Shape | AAF talkers | CRF output |
|---|---|---|
| AX 1x1 TDM8, before (planted control) | 217 | **217** |
| AX 1x1 TDM8, after | 217 | **29** |
| AX 8x8, before (planted control) | 217 x 8 | **217** |
| AX 8x8, after | 217 x 8 | **29** |

## Authoritative references

- Milan v1.2 4.3.3.2 Table 4.4: "AAF PCM32, 48kHz, N channels" MaxFrameSize 24*N + 24 + 1; "CRF, 1 ts/pdu" 28 + 1;
  MaxIntervalFrames 1.
- IEEE 802.1Q-2018 35.2.2.8.4 a) (MaxFrameSize: the maximum frame size the Talker will produce, excluding
  media-specific framing); 35.2.2.8 a) and b) (incrementing FirstValue adds 1 to the Unique ID and the destination
  address only).
- IEEE 1722-2016 10.4 (the CRF AVTPDU header) and 10.4.11 (crf_data_length).
- protocol-processor PR #194 (issue #190): `cfg_tspec_max_frame_i[N_STREAM_OUT_P*16-1:0]`, pin `93fb0b2d`;
  `protocol-processor/docs/guides/integrator.md` (slot s is Stream Output s's MaxFrameSize).

## How to get into the same state

```sh
git fetch origin
git checkout 774-crf-tspec-max-frame
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
```

## How to validate

```sh
make -C tb/verilator/milan_dp crflic
make -C tb/verilator/milan_dp tspec8
make -C tb/verilator/milan_dp crflic-mutants
python3 tb/verilator/milan_dp/test_sim_pool.py
python3 scripts/lint_rtl.py --check
bash scripts/run_all_suites.sh <logs> --wait
bash syn/yosys/run.sh
python3 syn/ooc/pp_resource_gate.py check <route-1x1 directory> --endpoint route-1x1
```

Expected result / pass criteria:

- `crflic`: 427 checks, 0 failures; its `[TSPEC]` section reads 217 for uid 0 and 29 for uid 1, and both match the
  emitted AVTPDU plus one.
- `tspec8`: 61 checks, 0 failures; nine sources, 217 for uids 0..7 and 29 for uid 8.
- `crflic-mutants`: "10 checks: 10 PASS, 0 FAIL"; the talker-0 control fails "CRF TSpec MaxFrameSize is Milan v1.2
  Table 4.4's 28 + 1" with got=217 exp=29 on both shapes.
- The resource gate: route-1x1, ooc-1x1 and ooc-8x8 `RESULT: PASS` against the eleventh record.

Local evidence (the design and tests are identical at `e70a99ba` and `5f0d5bf9`; the two later commits change
Markdown only):

| Gate | Head | Result |
|---|---|---|
| `make -C tb/verilator/milan_dp crflic` / `tspec8` | `e70a99ba` | 427 checks, 0 failures / 61 checks, 0 failures |
| `make -C tb/verilator/milan_dp crflic-mutants` | `e70a99ba` | 10 checks: 10 PASS, 0 FAIL |
| `python3 tb/verilator/milan_dp/test_sim_pool.py` | `e70a99ba` | 17 checks: 17 PASS, 0 FAIL |
| full sweep, `scripts/run_all_suites.sh --wait --shard k/4` x4, pinned Verilator 5.050 | `5f0d5bf9` | 64/64 suites pass, 2,189,325 checks, 0 in-suite failures, every shard exit 0; `tsn_fuzz` then re-run with tsn-gen at CI's `deca300c`: all campaigns pass (164 and 677 field cases), 899 checks, 0 failures |
| `bash syn/yosys/run.sh` (Yosys 0.66, sv2v v0.0.12) | `e70a99ba` | 60/60 tops PASS, tied-input and tap-purity PASS |
| `python3 scripts/lint_rtl.py --check` | `5f0d5bf9` | PASS, 89 <= 89 |
| the docs workflow's gate steps, GNU Make 4.3, CPython 3.12.3 | `5f0d5bf9` | 44 steps, 0 failed, 2 skipped by rule; builder leg 1 with LiteX rc 0; Markdown gates 5/5; the no-git pair rc 0 |
| `syn/ooc/pp_resource_gate.py check` x3 (recipe unchanged, single-thread synthesis, one Vivado run at a time) | `e70a99ba` | all `RESULT: PASS` |

| Endpoint | LUT | FF | SLICE | BRAM / DSP | WNS / WHS ns |
|---|---:|---:|---:|---|---|
| route-1x1, record -> this change | 51,259 -> 51,496 (+237) | 53,208 -> 53,268 (+60) | 15,835 -> 15,831 (-4) | unchanged | 0.236 -> 0.281 / 0.028 -> 0.009 |
| ooc-1x1 | 23,828 -> 23,847 (+19) | 20,000 -> 20,000 | -- | unchanged | -- |
| ooc-8x8 | 32,467 -> 32,512 (+45) | 28,220 -> 28,221 (+1) | -- | unchanged | -- |

All user timing constraints are met on the route (TNS, THS and TPWS 0); 19 of 15,850 slices are free.

## Known limitations / out of scope

- MaxIntervalFrames stays the processor's (1 for every source, Table 4.4); this change only supplies MaxFrameSize.
- Only the formats this device emits are derived: AAF PCM32 48 kHz and CRF with one timestamp per PDU. Other
  Table 4.4 rows (96/192 kHz, PCM24) have no framer here.
- No hardware or bench run: the wire evidence is the simulated DUT's own MSRP frames.
- `ci/image/tool-inventory.json` and `command-table.json` were not regenerated: `scripts/ci_tool_inventory.py
  --check` already refuses at dev `a032c6d6` on an unrelated changed script (`sw/builder/endstation_builder.py`),
  before it reaches this change's `crflic_mutants.py` digest or the new `Vmilan_dp_tspec8` command.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
