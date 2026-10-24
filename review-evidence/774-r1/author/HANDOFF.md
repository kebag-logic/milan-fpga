# HANDOFF — [A665], issue #774 (per-source TSpec MaxFrameSize for the CRF Talker Advertise)

Status: REVIEW READY at `5f0d5bf9` (not pushed). Every acceptance item met; every gate rc 0; the STOP conditions are not met.

- Repository: kebag-logic/milan-fpga (origin confirmed `https://github.com/kebag-logic/milan-fpga.git`)
- Branch: `774-crf-tspec-max-frame`, from dev `a032c6d6e3775f145349d5a495c1e1ad12294936` (merge-base confirmed; the
  live remote dev is still `a032c6d6` by `git ls-remote origin refs/heads/dev`)
- Head: `5f0d5bf931c87f3e6e3b813e042c64a61f9cb13e` (not pushed). Pins unchanged: protocol-processor `93fb0b2d`,
  gptp-processor `55680bff`.
- Assignment: https://github.com/kebag-logic/milan-fpga/issues/774#issuecomment-6379902807
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/774#issuecomment-6379948398 (text `receipts/public-taken.txt`)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/774#issuecomment-6382321681 (text `receipts/public-review-ready.txt`)
- Push, PR, merge: none (the manager pushes and opens the PR). `PR-BODY.md` is ready.

## Commits on dev `a032c6d6` (oldest first)

| Commit | Subject |
|---|---|
| `e70a99ba` | Declare each talker source's own Milan Table 4.4 TSpec MaxFrameSize, 29 for the CRF Media Clock Output, graded on the wire at the AX 1x1 and 8x8 shapes (#774) |
| `124adf7e` | Regenerate the module traceability matrix for the per-source TSpec MaxFrameSize (#774) |
| `5f0d5bf9` | Write the three edited table rows without em dashes, as the added-line gate requires (#774) |

`124adf7e` and `5f0d5bf9` change Markdown only: no `.sv`, `.svh`, `.v`, `.xdc`, `.tcl`, `.py`, `.cpp`, `.hex`,
Makefile, `syn`, `configs` or `sw` file differs between `e70a99ba` and `5f0d5bf9`
(`receipts/diff_e70a99ba_5f0d5bf9_names.txt`). So the Vivado bank, Yosys and the leg runs at `e70a99ba` measure the
head's design and tests; the sweep, lint and the docs gates ran at `5f0d5bf9` itself.

## Assignment items

| Item | Outcome |
|---|---|
| 1. Widen `KL_pp_shadow.cfg_tspec_max_frame_i` to one 16-bit value per stream output | Done: `[N_STREAM_OUT_P*16-1:0]`, passed straight to the processor's per-source port |
| 2. Each source's value from its own format, never a literal; remove "scratch only" | Done: AAF slot t = `tctx_maxf_w[t]` (24 x channels + 24 + 1), CRF slot = `KL_crf_tx.tspec_max_frame_o` (20-octet header + crf_data_length 8 + 1 = 29); the comment is gone |
| 3. Prove the declared MaxFrameSize per source on the wire model, 1x1 and 8x8; the talker-0 control must fail | Done: `[TSPEC]` on `obj_crflic` (AX 1x1 TDM8) and the new `obj_tspec8` (AX 8x8); the control fails both |
| 4. Gates | All rc 0 (table below). route-1x1 SLICE -4 against the eleventh record: the +5 STOP is not met; no tolerance exceeded |

## Changes (file:line at `5f0d5bf9`; clause)

| File:line | Change | Clause |
|---|---|---|
| `hdl/milan/KL_pp_shadow.sv:294-303` | port `cfg_tspec_max_frame_i [N_STREAM_OUT_P*16-1:0]`, flat `[16*s +: 16]`, banner rewritten | IEEE 802.1Q-2018 35.2.2.8.4 a); Milan v1.2 4.3.3.2 Table 4.4 |
| `hdl/milan/KL_pp_shadow.sv:1283-1284` | `.cfg_tspec_max_frame_i(cfg_tspec_max_frame_i)`; the "scratch only" every-slot copy removed | processor #190 / PR #194 |
| `hdl/ieee1722/crf/KL_crf_tx.sv:216-221` | new output `tspec_max_frame_o [15:0]` | Table 4.4 "CRF, 1 ts/pdu" 28 + 1 |
| `hdl/ieee1722/crf/KL_crf_tx.sv:226-233` | `CRF_HDR_C = 20` (pdu[0..19]); `CRF_PDU_C = CRF_HDR_C + CRF_DLEN_C` (28) instead of a literal | IEEE 1722-2016 10.4, 10.4.11 |
| `hdl/ieee1722/crf/KL_crf_tx.sv:242-246` | `assign tspec_max_frame_o = 16'(CRF_PDU_C + 1)`; the stale "declare 42, the padded MSDU" comment corrected (the table's bandwidth rule pays for the pad) | Table 4.4 and its bandwidth note |
| `hdl/milan/milan_datapath.sv:1959-1961` | `crft_maxf_w` | -- |
| `hdl/milan/milan_datapath.sv:2404-2405` | `pp_src_maxf_w [ACMP_SRC_C*16-1:0]` | -- |
| `hdl/milan/milan_datapath.sv:7426-7427` | `crf_tx.tspec_max_frame_o -> crft_maxf_w` | -- |
| `hdl/milan/milan_datapath.sv:9046-9060` | `g_pp_maxf`: slot `CRF_TUID_C` from `crft_maxf_w`, every other slot t from `tctx_maxf_w[t]` | Table 4.4; 802.1Q 35.2.2.8.4 a) |
| `hdl/milan/milan_datapath.sv:9404-9407` | `.cfg_tspec_max_frame_i (pp_src_maxf_w)` (was `tctx_maxf_w[0]`) | -- |
| `hdl/milan/milan_datapath.sv:6762-6764` | the surviving-derivation note names the per-source law | -- |
| `tb/verilator/milan_dp/sim_crf_licence.cpp:176-187` | `TspecSeen`: per-source TSpec of the DUT's own Talker Advertise values | 802.1Q-2018 35.2.2.8.4, Figure 35-2, 35.2.2.8 a) b) |
| `sim_crf_licence.cpp:96-109`, `:207-209` | `WIRE_CHANS_TB`, `SOURCES_TB` (default 2), `TSPEC_ONLY_TB`; `kUidCrf = kSources - 1` | -- |
| `sim_crf_licence.cpp:694-703` | longest CRF and AAF AVTPDU on the wire (header + crf_data_length / stream_data_length) | IEEE 1722-2016 10.4, 7.2 |
| `sim_crf_licence.cpp:744-747` | every Talker Advertise value of a vector graded with FirstValue's TSpec | 802.1Q-2018 35.2.2.8 a) b) |
| `sim_crf_licence.cpp:888-897` | boot: `ADP_TALKER[15:0]` equals the source count; `MAAP_CTRL` claims one address per source (0x201 at 1x1, unchanged) | -- |
| `sim_crf_licence.cpp:1264-1324` | `table44_max_frame` (the table's numbers, not the gateware's), `on_dut_tspec`, `phase_tspec_open`, `grade_tspec` | Table 4.4 |
| `sim_crf_licence.cpp:1338-1362` | `TSPEC_ONLY_TB` run (boot, open, grade); the full 1x1 run grades `[TSPEC]` after `[E]`, before `[G]`'s staged TSpecs | -- |
| `tb/verilator/milan_dp/Makefile:304-331` | `CRFLIC_BUILD` passes `-DWIRE_CHANS_TB=$(AX_CHANS)`; `TSPEC8_BUILD` (AX 8x8, `TSPEC8_STREAMS` = 8, `SOURCES_TB` = 8 + 1) | -- |
| `Makefile:562-566`, `:568-573`, `:643`, `:652`, `:803-807` | `tspec8`, `tspec8-build`; `crflic-mutants: crflic tspec8`; `tspec8` in `ORDINARY_CASES` with its banner; `build-`/`exec-tspec8` | -- |
| `tb/verilator/milan_dp/crflic_mutants.py:55-58`, `:92-100`, `:184-195` | `LEGS`; `TSPEC_MUTATIONS` (talker 0's TSpec on every source, per leg); both clean controls | -- |
| `tb/verilator/milan_dp/test_sim_pool.py:75-86`, `:37`, `:871` | the recorded ordinary-leg inventory gains `obj_tspec8` (fifteen legs) | -- |
| `tb/verilator/milan_dp/README.md:4`, `:87-88`, `:447`, `:516`, `:585` | fifteen elaborations; the `obj_crflic` row and the new `obj_tspec8` row; `[TSPEC]` phase row; the failing-arms row | -- |
| `docs/testing/TESTING.md:274`, `:405-407` | the `crflic-mutants` row; the fifteen-leg order | -- |
| `docs/traceability/ieee8021q.md:154` (SRP-10) | per-source TSpec and its evidence | 802.1Q-2018 35.2.2.8.4 a) |
| `docs/reference/MILAN_COMPLIANCE_MATRIX.md:99` (4.3.3) | per-source TSpec, AAF and CRF values, the `[TSPEC]` evidence | Milan v1.2 4.3.3 |
| `docs/reference/REGISTER_MAP.md:1226` (`0x690 LWSRP_TSPEC`) | who derives the declared MaxFrameSize | -- |
| `docs/reference/SUBMODULES.md:232` | the #190 adoption row states the slot copy was at that adoption, and #774 took it out | -- |
| `CHANGELOG.md:11`, `:47-58` | the per-source TSpec entry (its Contents line through `scripts/gen_toc.py --write`) | -- |
| `docs/traceability/MODULE_MATRIX.md:67,98,173`, `hdl/*/README-tests.md` | regenerated by `docs/traceability/gen_module_matrix.py` | -- |

## New checks (planted mutant; failing words)

The checks (`[TSPEC]`, per source): "a Talker Advertise value names this source"; "AAF TSpec MaxFrameSize is Milan
v1.2 Table 4.4's 24*N + 24 + 1" / "CRF TSpec MaxFrameSize is Milan v1.2 Table 4.4's 28 + 1"; "TSpec MaxIntervalFrames
is Table 4.4's 1"; "every Talker Advertise for it carried that TSpec"; on the 1x1 also "the CRF MaxFrameSize is the
emitted CRF AVTPDU plus one octet" and "the AAF MaxFrameSize is the emitted AAF AVTPDU plus one octet"; at boot
"ADP_TALKER[15:0] talker_stream_sources is this leg's source count".

| Planted control | Where | Leg | Failing words (got / exp) | Receipt |
|---|---|---|---|---|
| every source declares talker 0's TSpec: `.cfg_tspec_max_frame_i ({ACMP_SRC_C{tctx_maxf_w[0]}})`, the integration before this change (dev's `{N_STREAM_OUT_P{tctx_maxf_w[0]}}`) | `milan_datapath.sv:9407` | `obj_crflic` (AX 1x1 TDM8) | 3 of 427 fail: "CRF TSpec MaxFrameSize is Milan v1.2 Table 4.4's 28 + 1" got=217 exp=29; "every Talker Advertise for it carried that TSpec" got=104 exp=0; "the CRF MaxFrameSize is the emitted CRF AVTPDU plus one octet" got=217 exp=29 | `receipts/talker0_control/crflic-talker0.log`, `planted.diff` |
| the same | the same | `obj_tspec8` (AX 8x8) | 2 of 61 fail: "CRF TSpec MaxFrameSize is Milan v1.2 Table 4.4's 28 + 1" got=217 exp=29; "every Talker Advertise for it carried that TSpec" got=4 exp=0 | `receipts/talker0_control/tspec8-talker0.log` |
| both, through the campaign | `make crflic-mutants` | both | "[PASS] mutant caught: every source declares talker 0's TSpec on the 1x1 / on the 8x8 - breaks \"CRF TSpec MaxFrameSize is Milan v1.2 Table 4.4's 28 + 1\""; "10 checks: 10 PASS, 0 FAIL" (two clean controls, the six #530/#551 controls, the two new) | `receipts/crflic_mutants/crflic-mutants-head.log` |

Clean legs at the head's design: `obj_crflic` 427 checks, 0 failures (uid 0 AAF 217 over 27 values, uid 1 CRF 29
over 102 values; wire AVTPDU + 1 = 29 and 217); `obj_tspec8` 61 checks, 0 failures (uids 0..7 217, uid 8 29, four
values each). `receipts/legs/`.

## Resources (before = the eleventh record, after = `e70a99ba`) and route timing

Recipe `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` unchanged, `--single-thread-synthesis`, `--integrated-clock`, one
Vivado run at a time under the exclusive lock (`scripts/vivado_bank.sh`; Vivado 2026.1). `check` against
`syn/ooc/pp_resource_baseline.json` as on dev (the eleventh record, 15 free slices); `check-baseline` "baseline PASS:
3 endpoints".

| Endpoint | LUT | FF | SLICE | RAMB36 | RAMB18 | DSP | WNS ns | WHS ns | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| route-1x1 before | 51,259 | 53,208 | 15,835 | 74 | 27 | 13 | 0.236 | 0.028 | -- |
| route-1x1 after | 51,496 (+237) | 53,268 (+60) | 15,831 (-4) | 74 | 27 | 13 | 0.281 (+0.045) | 0.009 (-0.019) | `RESULT: PASS`, route complete, no unrouted net |
| ooc-1x1 before / after | 23,828 / 23,847 (+19) | 20,000 / 20,000 | -- | 16 / 16 | 3 / 3 | 8 / 8 | -- | -- | `RESULT: PASS` |
| ooc-8x8 before / after | 32,467 / 32,512 (+45) | 28,220 / 28,221 (+1) | -- | 21 / 21 | 5 / 5 | 8 / 8 | -- | -- | `RESULT: PASS` |

Slices: 15,831 of 15,850, 19 free (the STOP is > +5). All user timing constraints met (TNS 0, THS 0, TPWS 0; 179,533
setup endpoints). Route 05:03-05:52 UTC, ooc-1x1 to 06:05, rtl-8x8 06:05-06:07, ooc-8x8 06:07-06:34. Sub-block
movements (not gated) are in each `receipts/vivado/*-check.log`; the integrated route's largest are `u_pp` +118 LUT
(`u_aecp` +83, `u_srp` +73), from the processor's per-source TSpec now carrying two different constants.
Large artifacts by digest and size: `receipts/vivado/large-artifacts.sha256`, `.sizes`.

## Gate table

| Gate | Command | Head | Result | Receipt |
|---|---|---|---|---|
| crflic leg | `make -C tb/verilator/milan_dp crflic-build`, then `./obj_crflic/Vmilan_dp_crflic` | `e70a99ba` design | rc 0, 427 checks, 0 failures, 65 s | `receipts/legs/crflic-head.log` |
| tspec8 leg | `make -C tb/verilator/milan_dp tspec8-build`, then `./obj_tspec8/Vmilan_dp_tspec8` | same | rc 0, 61 checks, 0 failures, 3 s | `receipts/legs/tspec8-head.log` |
| crflic-mutants | `make -C tb/verilator/milan_dp crflic-mutants VERILATOR_JOBS=8` | same | make exit 0, "10 checks: 10 PASS, 0 FAIL" | `receipts/crflic_mutants/` |
| sim_pool self-test | `python3 tb/verilator/milan_dp/test_sim_pool.py` | same | rc 0, "17 checks: 17 PASS, 0 FAIL" | `receipts/legs/test_sim_pool.log` |
| full sweep | `native-shards.py 774-a665 full-native.json <out> 4 0-15 16-31 32-47 64-79` (`scripts/run_all_suites.sh --wait --shard k/4`, pinned Verilator 5.050) | `5f0d5bf9` | every shard exit 0: 64/64 suites pass, 2,189,325 checks, 0 in-suite failures, 0 timed out (shard 0 15/15 54,146 incl. `milan_dp` with `obj_crflic` 427 and `obj_tspec8` 61; shard 1 16/16 331,530; shard 2 17/17 262,066; shard 3 16/16 1,541,583). 09:58-11:01 local. The only SKIPPED lines are `tsn_fuzz`'s two tsn-gen field campaigns and their freshness checks (no `TSN_GEN_ROOT` in the spec) | `receipts/sweep/shard-*/`, `milan_dp-tspec-excerpt.txt` |
| tsn_fuzz with tsn-gen | `make -C tb/verilator/tsn_fuzz` in the shard-0 clone, `TSN_GEN_ROOT` = a tsn-gen build at CI's `TSN_GEN_REV` `deca300c` | `5f0d5bf9` | rc 0, "tsn_fuzz: all campaigns passed": AAF/AVTP 164 pass, gPTP 677 pass, 0 fail, 0 known gaps; suite_tally 899 checks, 0 failures. Its two `TEST_RESULTS.md` rewrites (date stamp only) were reverted in that scratch clone | `receipts/sweep/tsn_fuzz_rerun/` |
| Yosys | `bash syn/yosys/run.sh --results <dir>` (Yosys 0.66, sv2v v0.0.12) in a clean clone | `e70a99ba` | rc 0, 60/60 tops PASS (`KL_crf_tx` 2,687 cells, `KL_pp_shadow` 1,241,733, `milan_datapath` 1,778,782), tied-input and tap-purity PASS, 996 s | `receipts/yosys/run.log` |
| lint | `python3 scripts/lint_rtl.py --check` | `5f0d5bf9` | rc 0, "LINT GATE: PASS (89 violation(s) <= ratchet 89)" | `receipts/lint/lint_rtl_check_5f0d5bf9.log` |
| docs gates (GNU Make 4.3, CPython 3.12.3 with the workflow's pins) | `scripts/docs_run.sh 5f0d5bf9...` (the docs workflow's gate step bodies, literally) | `5f0d5bf9` | 44 steps, 0 failed, 2 skipped by rule (gate_42 runs the candidate's act runner on the host; the no-git step's body deletes `.git`, its two gates run on an archive export: `docs_check` rc 0, `feature_status` rc 0); builder leg 1 with LiteX rc 0; Markdown gates on 3.12.3 5/5 | `receipts/docs_5f0d5bf9/` |
| docs gates, earlier heads | same | `e70a99ba`, `124adf7e` | `e70a99ba`: gate_16 (stale generated matrix, fixed in `124adf7e`) and gate_8 (no `dev` in the clone's origin, an environment fault); `124adf7e`: gate_8, three em dashes in edited rows (fixed in `5f0d5bf9`) | -- |
| resource gate | `python3 syn/ooc/pp_resource_gate.py check <dir> --endpoint <e>` x3; `check-baseline` | `e70a99ba` design | all `RESULT: PASS`; `baseline PASS: 3 endpoints` | `receipts/vivado/` |
| quick checks | `check_port_contracts`, `check_sv_idiom`, `check_cpp_idiom`, `check_py_idiom`, `check_entity_shape`, `check_doc_style`, `check_doc_paths`, `check_hygiene`, `check_wire_accountability`, `check_sweep_shape`, `check_todo_ownership`, `check_em_dash --base a032c6d6`, `gen_toc.py --check`, `gen_module_matrix.py --check` | working tree / `5f0d5bf9` | all rc 0 | in the docs gates |

## Notes for the manager

- `python3 scripts/ci_tool_inventory.py --check` (with the pinned parser) refuses at dev `a032c6d6` already:
  "REFUSED: changed declared script 'sw/builder/endstation_builder.py'". The builder is unchanged by this lane
  (sha256 `a489a095...` at dev and head). The check stops there, before this lane's changed `crflic_mutants.py` and the
  new `Vmilan_dp_tspec8` command, so `ci/image/tool-inventory.json` and `command-table.json` were not regenerated.
- A local branch `dev` at `a032c6d6` was created in the lane checkout so the em-dash gate's `git fetch origin dev`
  resolves from the lane in the docs clones. Nothing was pushed.
- The `TSPEC_ONLY_TB` leg grades declarations only: at 8x8 no Listener Ready opens a stream, so the wire half
  (declared = AVTPDU + 1) is graded on the 1x1 only.

## STOP conditions

- route-1x1 grows by more than +5 slices, or any tolerance exceeded (15 free slices on the eleventh record): not met
  (SLICE -4; every figure `ok`).
