# HANDOFF — [A665], issue #774, Round 2 (answers R687-1 on PR #778)

Status: REVIEW READY at `01fc5475` (not pushed). Every R687-1 item answered (S1 optional, not taken); every gate rc 0 at the head or carried to it by a change no gate of that kind reads (below); the STOP (route-1x1 > +5 slices or any tolerance) is not met.

- Assignment: https://github.com/kebag-logic/milan-fpga/pull/778#issuecomment-6382693550, answering R687-1
  https://github.com/kebag-logic/milan-fpga/pull/778#issuecomment-6382684028 (NEGATIVE at `5f0d5bf9`: F1 BLOCKER,
  F2 and F3 MINOR, R1 residue, S1 suggestion). Its packet: branch `774-review-evidence` at `bfa27774`,
  `review-evidence/774-r1/reviews/R687-1/`. Its three probes are reused unchanged (sha256 equal to its MANIFEST:
  `receipts/round2/reviewer-probes.sha256`).
- Checkout: same lane, branch `774-crf-tspec-max-frame`, HEAD confirmed `5f0d5bf9` before the first edit; origin
  `https://github.com/kebag-logic/milan-fpga.git`; live remote dev still `a032c6d6`. New commits only (no rebase, no
  amend), not pushed. Submodule toplevels and origins checked (`receipts/round2/submodule-check.txt`); pins
  unchanged (protocol-processor `93fb0b2d`, gptp-processor `55680bff`).
- Head: `01fc54756f1ffb0a3aa836681215e8321ee7e86c`.

## Round 2 commits (on `5f0d5bf9`, oldest first)

| Commit | Subject | Files |
|---|---|---|
| `bf95d757` | Widen crf_data_length into the CRF AVTPDU length with a size cast the BDD frame-size steps resolve, FRAME_BYTES still 60 (#774) | `hdl/ieee1722/crf/KL_crf_tx.sv` |
| `53cd0d38` | Cite SRP-10's Table 4.4 clause without the Milan edition so the regenerated module matrix lists only clause ids, and state Q-10's per-source MaxFrameSize (#774) | `docs/traceability/ieee8021q.md`, regenerated `MODULE_MATRIX.md` and three `README-tests.md` |
| `0d4b4620` | Re-pin crflic_mutants.py and register the Vmilan_dp_tspec8 runtime command in the CI command table (#774) | `ci/image/command-table.json` |
| `2a0085dd` | Record the obj_crflic and obj_tspec8 Verilator build forms in the CI command table, leaving only dev's own source-list drift (#774) | `ci/image/command-table.json` |
| `01fc5475` | Count the obj_tspec8 leg's two tsn-c-stack pin controls on the control-plane firmware page, 167 (#774) | `sw/firmware/ctrl/README.md` |

## Round 2 items

| Item | Outcome |
|---|---|
| F1 BLOCKER, `features/crf_sr_class_a.feature:48` | Fixed in the RTL (option 1). `cd tests && behave --no-capture -f plain` rc 0, 406 of 406; the reviewer's `bdd_frame_bytes_probe.py` prints `FRAME_BYTES = 60` at the head; `obj_crflic` and `obj_tspec8` report 29 for CRF. The scenario and its steps are untouched. |
| F2 MINOR, matrix `1.2` | Row reworded (option 1). The reviewer's `matrix_clause_probe.py` keeps `35.2.2.8.4, 802.3, 4.3.3.2`; the three matrix rows read `35.2.2.8.4, 4.3.3.2, 802.3` (two) and `34.4, 35.2.2.8.4, 35.2.7, 4.3.3.2`; `gen_module_matrix.py --check` rc 0. |
| F3 MINOR, command table | The two named entries, plus this PR's two Verilator build forms (below). At the head the walk refuses on neither name, and this PR leaves no command-table difference of its own. |
| R1 residue, `ieee8021q.md:103` | The exact wording given, verbatim; `--check` rc 0 (the matrix did not move for it). |
| S1 suggestion | Not taken (optional). |
| Found while gating | `firmware-verilator` (rtl-fast) failed at `2a0085dd`: `sw/firmware/ctrl/README.md` gave 165 pin controls where the self-test has 167. The two are the new leg's `make build-tspec8` / `make run-tspec8` tsn-c-stack pin controls, added in round 1 (hosted CI at `5f0d5bf9` was cancelled before this job). Fixed in `01fc5475`. |

### F1: why the RTL and not the resolver

`CRF_PDU_C = CRF_HDR_C + 32'(CRF_DLEN_C)` (`hdl/ieee1722/crf/KL_crf_tx.sv:235`; comment `:231-233`) replaces
`int'(CRF_DLEN_C)`. The value and width are the same (the sum is 32-bit; 28 into an `int`), it is still the header
(IEEE 1722-2016 10.4) plus crf_data_length (10.4.11) with no new literal, and the BDD step's resolver already reads
a size cast. The oracle is left exactly as reviewed, so no fixture had to prove it unweakened. The plain sum
`CRF_HDR_C + CRF_DLEN_C` was rejected because it adds a Verilator WIDTHEXPAND (16 into 32 bits) and breaks the lint
ratchet (`hdl/ieee1722/crf` 3 <= 3). The netlist does not move: Yosys `KL_crf_tx` 2,687 cells and `milan_datapath`
1,778,782 (round 1 the same), and route-1x1 reproduces round 1's figures exactly.

Planted faults against the unchanged step (`scripts/round2/bdd_frame_mutants.py`, `receipts/round2/bdd/frame_mutants.log`),
6 of 6:

| Plant in `KL_crf_tx.sv` | Failing words |
|---|---|
| none (clean) | passes |
| crf_data_length 12 (frame 64) | `ASSERT FAILED: FRAME_BYTES is not 60` |
| header 24 (frame 64) | `ASSERT FAILED: FRAME_BYTES is not 60` |
| the tag grows the frame (`+ VTAG_C`) | `ASSERT FAILED: FRAME_BYTES is not 60` |
| round 1's `int'(...)` | `ASSERT FAILED: no localparam int found` |
| non-arithmetic `$bits(...)` | `ASSERT FAILED: no localparam bits found` |

### F2

`docs/traceability/ieee8021q.md:154` (SRP-10): "(Milan v1.2 4.3.3.2 Table 4.4)" reads "(Milan 4.3.3.2 Table 4.4)".
The generator is unchanged; the edition is the repository's profile throughout. `milan_datapath` still shows four
clauses in sort order, so `802.1` (a standard number, not a clause) stays outside the display, now behind the real
`4.3.3.2` rather than `1.2`. Receipts: `receipts/round2/docs/matrix_clause_probe.log`.

### F3

| File:line at the head | Entry |
|---|---|
| `ci/image/command-table.json:14079-14083` | `crflic_mutants.py` sha256 `baec486a...` (was `ce4c4ff1...`), class "reviewed non-installing" kept, as the reviewer confirmed |
| `ci/image/command-table.json:967-977` | `Vmilan_dp_tspec8`, shaped like `Vmilan_dp_crflic` (non-installing, `./obj_tspec8/Vmilan_dp_tspec8`, one empty pattern) |
| `ci/image/command-table.json:12917` | the `obj_crflic` Verilator build's `-CFLAGS` word gains `-DWIRE_CHANS_TB=8` (round 1's Makefile change) |
| `ci/image/command-table.json:12991-13116` | the `obj_tspec8` Verilator build, the crflic pattern with exactly the four differences of the real command (8x8 config, `obj_tspec8 -GN_STREAMS=8`, a runtime `-CFLAGS`, `-o Vmilan_dp_tspec8`) |

Why the last two: the reviewer's walk (`inventory_walk.py`) stops at dev's own drift long before milan_dp, at
`tb/verilator/avtp_rxmon/format_mutants.py` (undeclared) after eleven re-pins, on dev, the old head and the new
head alike (`receipts/round2/inventory/walk-*.log`). So "no refusal names either one" holds at the head, but that
walk cannot show what milan_dp itself needs. `scripts/round2/inventory_learn.py` runs the tree's own walker over
the milan_dp Makefile, answering each refusal in memory, and lists every entry the tree's committed table lacks.
Compared with dev (`receipts/round2/inventory/milan_dp-learn-compare.txt`), the old head needed five entries more:
the two named ones, and the two Verilator build forms. `scripts/round2/pattern_residue.py`
(`milan_dp-pattern-residue.txt`) then shows that at the head the `obj_crflic` and `obj_tspec8` patterns differ from
the real commands by exactly dev's own residue, the RTL source-list drift every milan_dp leg carries
(`KL_render_setpoint.sv` became `KL_render_queue.sv`, plus three new CRF sources; `obj_dynmap` and every other leg the
same). So this PR leaves no difference of its own. `pr-additions.txt`: `crflic_mutants.py` file = pin MATCH at
the head; its `tool-inventory.json` input is still `ce4c4ff1`, which only a regeneration changes, and that stays
blocked by dev's drift (`ci_tool_inventory.py --check` still refuses first on `sw/builder/endstation_builder.py`,
as on dev). The CI-image self-tests: `ci_tool_inventory_selftest`, `ci_inventory_patterns_selftest`,
`ci_inventory_nodes_selftest` rc 0 at `2a0085dd`; `ci_differential_selftest` rc 1 there and rc 1 at dev, refusing on
dev's drifted scripts.

### R1

`docs/traceability/ieee8021q.md:103` (Q-10) now reads the reviewer's exact text: "MaxFrameSize still derives from
real frame geometry in [`milan_datapath`](../../hdl/milan/milan_datapath.sv), one slot per source: each AAF
talker's channel count and the CRF output's PDU shape (#774), passed as `cfg_tspec_max_frame_i`."

## Round 2 gate table

| Gate | Command | Head | Result | Receipt |
|---|---|---|---|---|
| rtl-fast replica | `python3 scripts/round2/rtl_fast_steps.py <out> <clean clone> <head>` (every job of the fast gate's `needs:`, `run:` bodies literally, as a pull_request against dev `a032c6d6`) | `01fc5475` | rc 0, "rtl-fast: success; failed jobs: none": changes, verilator-lint, bdd-conformance, yosys-elaboration, publication-census, firmware-unit, firmware-control/aecp/srp-mutants, firmware-boundary, firmware-verilator all success; clone HEAD unchanged, no tracked change | `receipts/round2/rtl-fast/` |
| rtl-fast replica, earlier heads | same | `0d4b4620` (partial), `2a0085dd` | `0d4b4620`: changes, lint, bdd (406/406), yosys, census success; firmware jobs refused by my SDK path (a symlinked prefix), not run. `2a0085dd`: firmware-boundary failed for want of the LiteX pins (my replica skipped the step that installs them; fixed in the driver), firmware-verilator failed on the README's 165 pin controls, fixed in `01fc5475` | `receipts/round2/rtl-fast-history/` |
| behave | `cd tests && behave --no-capture -f plain` | `01fc5475` (and `0d4b4620`) | rc 0, 14 features, 406 scenarios, 1977 steps passed, 0 failed | `receipts/round2/bdd/behave-head.log` |
| frame-bytes probe (reviewer's) | `python3 bdd_frame_bytes_probe.py <repo> a032c6d6 5f0d5bf9 <head>` | `01fc5475` | dev 28/60; `5f0d5bf9` "no localparam int found" (F1 reproduced); head `CRF_PDU_C = 28`, `FRAME_BYTES = 60` (head-only run rc 0) | `receipts/round2/bdd/frame_bytes_probe*.log` |
| BDD step planted faults | `python3 scripts/round2/bdd_frame_mutants.py <repo> <head>` | `01fc5475` | rc 0, "6 checks: 6 PASS, 0 FAIL" | `receipts/round2/bdd/frame_mutants.log` |
| matrix clause probe (reviewer's); `gen_module_matrix.py --check` | `python3 matrix_clause_probe.py <repo> a032c6d6 5f0d5bf9 <head>`; `python3 docs/traceability/gen_module_matrix.py --check` | `01fc5475` | kept `35.2.2.8.4, 802.3, 4.3.3.2` (no `1.2`); "traceability matrix up to date", rc 0 | `receipts/round2/docs/` |
| `obj_crflic` / `obj_tspec8` | `make -C tb/verilator/milan_dp crflic-build` / `tspec8-build`, then each binary | `0d4b4620` | rc 0: 427 checks, 0 failures ("CRF TSpec MaxFrameSize is Milan v1.2 Table 4.4's 28 + 1" got=29; "the CRF MaxFrameSize is the emitted CRF AVTPDU plus one octet" got=29) / 61 checks, 0 failures (CRF 29) | `receipts/round2/legs/` |
| crflic-mutants | `make -C tb/verilator/milan_dp crflic-mutants VERILATOR_JOBS=8` | `0d4b4620` | make rc 0, "10 checks: 10 PASS, 0 FAIL" (log 227,777 bytes, kept outside by digest) | `receipts/round2/crflic_mutants/` |
| crf_tx suite | `make -C tb/verilator/crf_tx -j16` | `0d4b4620` | rc 0, "KL_crf_tx: 129 checks, 0 failures" | `receipts/round2/legs/crf_tx.log` |
| sim_pool self-test | `python3 tb/verilator/milan_dp/test_sim_pool.py` | `2a0085dd` | rc 0, "17 checks: 17 PASS, 0 FAIL" | `receipts/round2/legs/test_sim_pool.log` |
| lint | `python3 scripts/lint_rtl.py --check` (pinned Verilator 5.050) | `0d4b4620`; replica `01fc5475` | rc 0, "LINT GATE: PASS (89 violation(s) <= ratchet 89)", `hdl/ieee1722/crf` 3 <= 3 | `receipts/round2/lint/`, `rtl-fast/logs/verilator-lint.7.log` |
| full sweep | `native-shards.py 774-a665 full-native.json <out> 4 0-15 32-47 64-79 80-95` (`scripts/run_all_suites.sh --wait --shard k/4`, pinned Verilator 5.050) | `0d4b4620` | every shard exit 0: 64/64 suites, 2,189,325 checks, 0 in-suite failures, 0 timed out (shard 0 15/15 54,146; 1 16/16 331,530; 2 17/17 262,066; 3 16/16 1,541,583). Only SKIPPED: `tsn_fuzz`'s two tsn-gen field campaigns and their freshness checks, as in round 1 | `receipts/round2/sweep/` |
| Yosys | `bash syn/yosys/run.sh --results <dir>` (Yosys 0.66, sv2v v0.0.12), clean clone | `2a0085dd` | rc 0, "tops: 60 pass: 60 fail: 0", tied-input and tap-purity PASS | `receipts/round2/yosys/run.log` |
| route-1x1 | `scripts/round2/vivado_route.sh`; `python3 syn/ooc/pp_resource_gate.py check <dir> --endpoint route-1x1` | `2a0085dd` | `RESULT: PASS` (table below) | `receipts/round2/vivado/` |
| docs gates (GNU Make 4.3, CPython 3.12.3 with the workflow's pins) | `scripts/docs_run.sh <head>` (the docs workflow's gate step bodies, literally) | `01fc5475` | 44 steps, 0 failed, 2 skipped by rule (as round 1); builder leg 1 with LiteX rc 0; Markdown gates on 3.12.3 5/5; the no-git pair `docs_check` rc 0, `feature_status` rc 0 | `receipts/round2/docs_gates/` |
| CI-image inventory | `python3 scripts/ci_tool_inventory.py --check`; `inventory_walk.py` (reviewer's) on disposable copies; `scripts/round2/inventory_learn.py`, `inventory_compare.py`, `pattern_residue.py` | `2a0085dd` (= head for these files) | `--check` refuses first on `sw/builder/endstation_builder.py` as on dev; the walk names neither `crflic_mutants.py` nor `Vmilan_dp_tspec8` (it stops at dev's undeclared `format_mutants.py`); on the milan_dp walk the head needs nothing dev does not, but dev's own source-list residue | `receipts/round2/inventory/` |
| CI-image self-tests | `ci_tool_inventory_selftest.py`, `ci_inventory_patterns_selftest.py`, `ci_inventory_nodes_selftest.py`, `ci_differential_selftest.py` | `2a0085dd` | rc 0, 0, 0; the differential one rc 1, and rc 1 at dev too (dev's drifted scripts) | `receipts/round2/inventory/ci_*` |

Carry: `0d4b4620..01fc5475` changes `ci/image/command-table.json` (named by no workflow, Makefile, `tb/` file or the
suite driver: `receipts/round2/carry-0d4b4620-to-2a0085dd.txt`) and `sw/firmware/ctrl/README.md` (Markdown, read by
the firmware self-test, which the replica ran at the head). So the sweep, legs, campaign and lint at `0d4b4620`,
and Yosys and the route at `2a0085dd`, measure the head's design and tests.

## Resources and route timing (round 2, route-1x1 only, RTL changed)

Against the eleventh record (`syn/ooc/pp_resource_baseline.json`, unchanged), recipe unchanged
(`scripts/round2/vivado_route.sh`, the round-1 bank's route leg), `--single-thread-synthesis`, one Vivado run under
the exclusive lock, at `2a0085dd` (the RTL is the same at `01fc5475`).

| Figure | Record | `2a0085dd` | Delta | Verdict |
|---|---:|---:|---:|---|
| LUT | 51,259 | 51,496 | +237 | ok |
| FF | 53,208 | 53,268 | +60 | ok |
| SLICE | 15,835 | 15,831 | -4 | ok, below the record |
| RAMB36 / RAMB18 / DSP | 74 / 27 / 13 | 74 / 27 / 13 | 0 | ok |
| WNS ns | 0.236 | 0.281 | +0.045 | ok |
| WHS ns | 0.028 | 0.009 | -0.019 | ok |

`RESULT: PASS`; route complete, 101,866 of 101,866 routable nets routed, no routing error; all user timing
constraints met (TNS, THS, TPWS 0; 179,533 setup endpoints). 15,831 of 15,850 slices. Identical to round 1's
`e70a99ba` route in every figure. Vivado 11:15-12:04 UTC. The STOP (+5 slices or any tolerance) is not met.
Large artifacts by digest and size: `receipts/round2/vivado/large-artifacts.sha256`, `.sizes`.

## Notes for the manager

- The rtl-fast replica is native (`scripts/round2/rtl_fast_steps.py`): the act runner rechecks the pushed remote
  head, and this head is not pushed. It runs every job's `run:` bodies literally, one job at a time; what it skips
  or rewrites is listed in its docstring and per step in its `receipts.json`. Hosted and act acceptance at the
  pushed head remain the manager's.
- `tool-inventory.json` regeneration stays blocked by dev's drift (eleven changed declared scripts, an undeclared
  one, and stale Verilator source lists for every milan_dp leg). That is the manager's item; this PR now carries
  every command-table entry of its own.
- No TAKEN was posted again (round 2 rule). REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/774#issuecomment-6385545886 (text `receipts/round2/public-review-ready.txt`)

---

# Round 1: HANDOFF — [A665], issue #774 (per-source TSpec MaxFrameSize for the CRF Talker Advertise)

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
