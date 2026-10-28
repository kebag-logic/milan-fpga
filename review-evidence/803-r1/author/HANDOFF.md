# HANDOFF — #803 gPTP pin adoption (FPGA-gPTP main f97c1803), executor [A693]

Status: **REVIEW READY** at `fb182b19925b9ea24443d48d0e71b656de52b8ae` (worktree clean, every submodule at its
gitlink, live remote dev `5fcec84b` unchanged). Every gate the issue lists is rc 0 at this head (table below).
Nothing pushed. One open decision is published, not resolved (slice headroom, section Resources). STOP conditions
not met: no top-level port or register-map change beyond the companions; route-1x1 +0.94 %.

## Gate table (head `fb182b19` unless noted; every command unpiped, its own rc and log)

| Gate | rc | Seconds | Result | Receipt |
|---|---:|---:|---|---|
| Full sweep, 4 shard units (`native-shards.py`, MemoryMax 10G, -j4, CPUs 96-103 / 104-111 / 112-119 / 120-127) | 0, 0, OOM, 0 | 4288, 2749, -, 2785 | shard 0 15/15 (250,958 checks), 1 17/17 (1,536,446), 3 16/16 (23,927); shard 2 OOM-killed in `capture_coherence` | `receipts/sweep/shard-*` |
| Shard 2 re-run (`rerun_shard.py`, VERILATOR_JOBS=2, CPUs 112-115) | 0 | 5069 | 16/16 (380,086 checks), `capture_coherence` PASS within its 2,400 s | `receipts/sweep/shard-2-rerun` |
| `python3 scripts/suite_tally.py <union> --quiet --expect-suite-root tb/verilator` | 0 | - | **64 / 64 suites, 2,191,417 checks, 0 in-suite failures, 0 timed out** | `suite-tally-quiet.out`, `suite-tally-per-suite.txt`, `union-logs.sha256` |
| milan_dp `gptp` and `gptp-lat` legs (inside `milan_dp`, shard 0) | 0 | - | 200 / 200 each; `milan_dp` 13,613 checks over 18 tallies | sweep |
| milan_dp_gm_steps (shard 1) | 0 | - | 202 checks, 0 failures | sweep |
| tsn_fuzz (shard 3), its `ptp` campaign | 0 | - | `gPTP/802.1AS field campaign: 675 pass, 0 fail, 0 known gaps`; artifact freshness 1/1; suite 897 | sweep |
| `make -C tb/verilator/tsn_fuzz ptp` in the lane (at `ab73efa1`; regenerated the committed artifact) | 0 | 33 | 675 pass; freshness PASS | `receipts/tsnfuzz-ptp/` |
| milan_dp_gptp, `scripts/run_all_suites.sh <logs> --wait --physical-gptp` with `SUITE_TIMEOUT=14400`, then `suite_tally.py` | 0, 0 | 5494 | 1/1; 205 checks, 0 failures: physical 151, setup abort 6, no-TX 20, no-Pdelay 14, recentre 14; 17.992742740 simulated s, 899,637,137 cycles; simulation 4,390 s | `receipts/physical/` |
| rtl-fast replica (`rtl_fast_steps.py`, every job of the aggregate's `needs:`) | 0 | 5908 | `rtl-fast: success`; 12 / 12 jobs success; behave 14 features, 495 scenarios, 2,286 steps passed | `receipts/rtl-fast/` |
| `syn/yosys/run.sh` (full serial; Yosys 0.66, sv2v v0.0.12) | 0 | 1224 | tops 60, pass 60, fail 0; tied inputs 29, justified 2, unjustified 0; TAP-PURITY PASS | `receipts/yosys/` |
| `python3 scripts/lint_rtl.py --check` (and `--self-test`) | 0, 0 | 20, 23 | LINT GATE: PASS (89 <= ratchet 89; 19 waived, 0 justified lint_off) | `receipts/static/` |
| `python3 scripts/check_sv_idiom.py`, `check_sh_idiom.py`, `check_cpp_idiom.py` (+`--selftest` 75/75), `check_py_idiom.py` (+`--selftest` 54/54) | 0 x6 | <7 each | every ratchet at or under its budget | `receipts/static/` |
| `flock -x $VIVADO_LOCK python3 scripts/xvlog_gate.py --check` | 0 | 371 (incl. lock wait) | 0 findings == ratchet (0 hdl/, 0 pinned processors) | `receipts/static/xvlog.log` |
| Pin records: `pp_resource_gate.py check-baseline`; `ooc.sh --record-rom-digests` + `git diff --exit-code syn/yosys/rom_digests.tsv`; both diagram `--check`; `check_submodule_docs.py`; `check_gptp_docs.py` (with and without `--with-submodule`) | 0 x8 | <2 each | baseline PASS 3 endpoints; ledger byte-identical; diagrams OK; 6 exact gitlinks; 8 current pages, donor checkout verified | `receipts/static/` |
| `check_port_contracts.py`, `measure_naming.py --check`, `measure_test_evidence.py --check`, `check-integrator-params.py`, `check_rtl_source_lists.py` (+selftest), `pp_srcs.py --check --selftest`, `check_hygiene.py --check`, `measure_fail_fast.py --check`, `check_todo_ownership.py`, `gen_module_matrix.py --check`, `check_soc_sources.py`, `check_nvm_capture.py`, `check_feature_status.py`, `docs_check.py` | 0 x15 | - | all within budget / OK / PASS | `receipts/static/table.txt` |
| `python3 sw/builder/test_builder.py` | 0 | 1741 | ALL GATES PASS EXCEPT 2 NOT RUN (gate 1b inert under Make 4.3; gate 11 needs the absent mf48 calibration build): the two arms #771 recorded | `receipts/static/builder_bank.log` |
| Docs workflow replica (`docs_steps.py`, the `run:` bodies literally, GNU Make 4.3, CPython 3.12.3; Markdown gates with the md venv) | 0 | 2,785 (whole replica) | 44 steps: 42 run, all rc 0; 2 skipped by rule (gate_42 runs the candidate act runner on the host; docs-check-no-git deletes `.git`) | `receipts/docs/all.out`, `all-receipts.json` |
| Builder leg 1 again with `MILAN_LITEX_PYTHON` | 0 | 337 | 1 NOT RUN (gate 11) | `receipts/docs/leg1-litex*` |
| The five Markdown gates on CPython 3.12.3 (`docs_steps_md312.py`) | 0 | - | 5 / 5 rc 0 | `receipts/docs/md312*` |
| No-git job's gates on a `git archive` export: `docs_check.py`, `check_feature_status.py` | 0, 0 | - | 0 findings each | `receipts/docs/nogit_*` |
| Vivado: route-1x1, ooc-1x1, rtl-8x8, ooc-8x8, each `pp_resource_gate.py check` | 0 x4, gates 0 x3 | 3114, 816, 238, 1792 | all three endpoints PASS against the record (section Resources) | `receipts/vivado/` |
| Parent mutant campaign (`parent_mutants.py`) | 0 | - | 4 clean passes; 23 (defect, suite) rows, every one KILLED on every named check | `receipts/mutants/` |

Acceptance (#803): "all consumer gates rc 0": **met** (above). "FPGA-gPTP #87 to #91 close once this is in an
image and the in-house gPTP scenarios pass": after merge, outside this lane (no image or bench access here).
Required list: gitlink bumped; companions applied in order and finished (review fixes in commit 5); every
pin-derived record regenerated through its generator; every listed consumer gate run; route-1x1, ooc-1x1 and
ooc-8x8 run against the current record with the delta recorded; the adoption recorded in the pin page and the
changelog.

- Lane: $LANES/803-adopt-gptp, branch 803-adopt-gptp-f97c1803, from dev 5fcec84b
- origin: https://github.com/kebag-logic/milan-fpga.git (verified); gptp-processor toplevel and origin
  (https://github.com/Mister-M-alt/FPGA-gPTP.git) verified before every submodule git command
- gPTP pin: 55680bff -> f97c1803 (first-parent: merge of PR #92 `3426089a`, merge of PR #93 `f97c1803`)
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/803#issuecomment-6477798636
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/803#issuecomment-6482493009

## Commits

| # | Commit | Change |
|---|---|---|
| 1 | `1d68756c` | gitlink 55680bff -> f97c1803 |
| 2 | `a701de12` | companion b53944d5 (PR #92 parent test patch), applied with `git apply --index` |
| 3 | `3ef8d86d` | companion 3a3db518 (PR #93), applied with `git apply --index` |
| 4 | `cf188b2b` | pin-derived records through their generators |
| 5 | `ab73efa1` | review fixes: stale statements the companions left |
| 6 | `46588545` | `TEST_RESULTS.md` regenerated at this tree; tsn_fuzz README current tally 675 |
| 7 | `5e7e120f` | loss page sentence split to the concise-style limit (gate_9 finding on commit 5) |
| 8 | `fb182b19` | adoption record: pin page #803 section, changelog entry and Contents line |

Head: `fb182b19925b9ea24443d48d0e71b656de52b8ae`. Live remote dev at every check: `5fcec84b` (unchanged).

## Companion application

Both sha256 verified in full before use:
- b53944d52a51323b267b0a91dbfd6bd1aeaabcacf26d31b246b19318d56a1b7a (22.9 KiB)
- 3a3db51805985df7a19bfc2308c8e6602b9784cf305746e18796e11b15376451 (83.4 KiB)

`git apply --check` then `git apply --index`, both "Applied cleanly", no offset, no fuzz.
Pre-image blobs equal dev's for every file except two that dev moved since the companions' base (97aab1d0):
`docs/testing/TESTING.md` (companion 1) and `README.md` (companion 2) apply by context; every other
post-image blob equals the companion's recorded post-image exactly.

## Engine interface check (raw diff 55680bff..f97c1803 of gptp-processor/hdl)

- One port change: `KL_gptp_engine.pub_path_o` `[7*64-1:0]` -> `[8*64-1:0]` (entry 0 first). Authorised in #803.
- One internal localparam removed (`OFF_AN_SR_END_C`, parser). No parameter change. Source set unchanged
  (no `.sv` added/removed; one test script added: `tb/verilator/engine/receipt_mutants.py`).
- Consumers of the engine in this tree: `KL_gptp_shadow` (updated by companion 2),
  `tb/verilator/gptp_plane/gptp_plane_wrap.sv` (leaves `pub_path_o` unconnected: unaffected),
  `tb/verilator/gptp_txts/gptp_txts_wrap.sv` (shadow, `pub_path_o ()`: unaffected).

## Changes, file:line at the head, and the clause each answers

RTL (companion 2, reviewed as milan-fpga code; no further RTL edit in this lane):

| File:line | Change | Clause / issue |
|---|---|---|
| `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:199-200` | `pub_path_count_o` counts entries 0..8; `pub_path_o` widens to `[8*64-1:0]`, entry k at `64*k` | FPGA-gPTP #87, #88; the engine's one authorised port change |
| `KL_gptp_shadow.sv:632, 647-664` | raw and canonical path 8 entries wide; copy entries `pk < count` from entry 0 | IEEE 802.1AS-2011 10.3.10.2.1 d) |
| `KL_gptp_shadow.sv:665-666` | path generation = count or any entry (entry 0 included); the old `count ? GM : 0` head term removed | Milan v1.2 Table 5.22 ("path sequence changes"); 10.3.10.2.1 d) |
| `hdl/milan/milan_datapath.sv:1633-1635` | `gptp_pub_path_w` 8 entries; head = entry 0, tail = entries 1..7 | IEEE 1722.1-2021 7.4.41.2 (count, path_sequence) |
| `milan_datapath.sv:2304, 2310` | `asp_owner_head_w` / `asp_live_head_w`: entry 0 from the engine head (owner-selected, zero option OFF, zero without a GM) where it was the CSR GM | 7.4.41.2; FPGA-gPTP #88 (head as received) |
| `milan_datapath.sv:2700` | CSR AS_PATH face takes entries 1..7 (width unchanged) | no CSR port change |
| `milan_datapath.sv:6070, 6305` | GET_AS_PATH response snapshot and entry-0 pick use the head | 7.4.41.2 |
| `milan_datapath.sv:6488, 6509` | AS_PATH change comparator watches entry 0, count and entries | Milan v1.2 Table 5.22 |
| `hdl/common/csr/milan_csr.sv:292-293, 603-604` | port comments only (entries 1..7; count incl entry 0) | none |

Tests (companion 1 = PR #92 parent patch; companion 2 = PR #93 companion):

| File:line | Change | Clause / issue |
|---|---|---|
| `tb/verilator/gptp_plane/sim_phc_step.cpp:323, 349, 372, 390` and `phc_step.py:62-63` | asCapable falls at the fifth (crossing answered) / fourth (crossing unanswered) request; longer drives | 802.1AS-2011 Figure 11-8 RESET; FPGA-gPTP #90 |
| `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:1068-1090` | 375 ms Sync timeout makes this station grandmaster; five unanswered intervals; deadline 6.05 s | 10.3.11 / Figure 10-13 with Cor1 (#89); Figure 11-8 (#90) |
| `tb/verilator/milan_dp/sim_gptp.cpp:495` | `run_selected`: the selected peer sends one Sync pair before each long wait | #89 (keeps the peer selected) |
| `sim_gptp.cpp:1311, 1407` | TLV-less Announce keeps path B (count 5, generation, no push); GM switch keeps entry 0 GMID | 10.3.10.2.1 d) (#87) |
| `sim_gptp.cpp:1468` | empty TLV (`{thisClock}`, count 1) as the in-flight cut | 10.3.10.2.1 d) (#88) |
| `sim_gptp.cpp:1553, 1588` | path headed elsewhere served from that head; entry-0-only change is a path change (generation and push) | 7.4.41.2; Table 5.22; #88 |
| `sim_gptp.cpp:1666` | #207 full-queue arm forces the level every cycle until the event | #89 (dispatch can pop inside the window) |
| `tb/verilator/gptp_shadow/gptp_shadow_wrap.sv:122, 408` | `pub_path_head_o` = entry 0; tails k = entry k+1 | #87, #88 |
| `tb/verilator/gptp_shadow/sim_main.cpp:600, 901, 960` | `announce_path`; empty / headed-elsewhere / entry-0-only; TLV-less keeps the path | #87, #88 |
| `tb/verilator/tsn_fuzz/fuzz_ptp_timing.py:66, 176, 179` | `_btca_adopt`: head-not-GM and count-not-stepsRemoved+1 adopted, no parser drop; stepsRemoved 255 one-hop refused by (b) | 10.3.10.2.1 a)-c) only (#88) |
| `fuzz_ptp_timing.py:73, 239, 346` | one usable Sync pair heard as master before the rejection/adoption probes | #89 |

Records and documentation (this lane):

| File | Change | Generator / gate |
|---|---|---|
| `syn/yosys/rom_digests.tsv` | row `f97c1803 gptp_ucode.hex b21b244f...ba56` (equals the donor's `syn/ooc/work/gptp_ucode.hex` and PR #92's merge) | `bash syn/yosys/ooc.sh --record-rom-digests` |
| `docs/reference/SUBMODULES.md:24` | pin row | `scripts/check_submodule_docs.py` |
| `docs/diagrams/submodule_boundaries.*`, `timesync_chain.*`, `PNG_MANIFEST.json` | pin labels | the two `.gen.py` generators (`--check` rc 0) |
| 8 gPTP pages (18 URLs, 35 gate findings) | donor deep links 55680bff -> f97c1803 | `scripts/check_gptp_docs.py --with-submodule` |
| `scripts/port_docs.budget` | header `hdl 2121 -> 2158` only: dev drift since #771 (this lane adds no hdl port) | `check_port_contracts.py --write-budget` |
| `scripts/naming.budget` | byte-identical | `measure_naming.py --write-budget` |
| `hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md` | regenerated at this head; differs from the companion's only in the date stamp (675 pass) | `make -C tb/verilator/tsn_fuzz ptp` (freshness check PASS) |
| `tb/verilator/tsn_fuzz/README.md:202, 213` | current tally 638 -> 675 (the README's own re-measure rule; the N10-N15 rows are dated measurements, pre-existing drift, unchanged) | - |
| `tb/verilator/milan_dp/README.md:407, 426-434, 447` | "four" -> "five" unanswered intervals; the deadline projection re-scaled to 899637137 cycles: 5347 / 5484 s, 99.0 / 101.6 % of 5400 s | 802.1AS-2011 Figure 11-8 (#90) |
| `docs/design/GM_LOSS_RECOVERY.md:37-49` | Sync timeout rows split by gmPresent; fifth lost response | Figure 10-13 with Cor1 (#89); Figure 11-8 (#90) |
| `docs/reference/milan_feature_status.json:298` | AS_PATH trigger: served pathTrace, entry 0 included | Table 5.22; #87, #88 |
| `tb/verilator/csr/sim_gptp.cpp:235-239` | comment: fabric count zero only without a GM | #87 |
| `docs/reference/SUBMODULES.md` (#803 section), `CHANGELOG.md` | adoption record | `check_doc_style.py`, `gen_toc.py --check` |

## Resources: route-1x1, ooc-1x1, ooc-8x8 against the current record

Bank: `scripts/vivado_bank.sh` (the #780 and #799 lanes' bank, paths only), `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`,
single-worker synthesis, `general.maxThreads` 32, Vivado 2026.1 Build 6511674, one run at a time, each under
`flock -x $VIVADO_LOCK`, each only above 20 GB MemAvailable, in a clean clone at `cf188b2b` (synthesis
inputs equal the head's: later commits change no `hdl/` statement, `sw/`, `configs/` or submodule; `TEST_RESULTS.md`
is not read). Then `python3 syn/ooc/pp_resource_gate.py check <dir> --endpoint <e>` against the committed record
(the 2026-10-23 #632 record at dev `e5b480a3` + #770). Receipts: `receipts/vivado/`.

| Run | rc | Minutes | Peak MB | Log SHA-256 (bytes) |
|---|---:|---:|---:|---|
| route-1x1 | 0 | 51.9 | 8,541 | `d23462b7...` (888,208) |
| ooc-1x1 (`--integrated-clock`, 20 ns) | 0 | 13.6 | 5,141 | `65e0b70a...` (316,927) |
| rtl-8x8 (elaboration for the 8x8 parameters) | 0 | 4.0 | - | `19b5b088...` (211,678) |
| ooc-8x8 | 0 | 29.9 | 6,141 | `206f2549...` (324,986) |

| Endpoint | Gate rc | LUT record -> head (delta, tol.) | FF (delta, tol.) | Other |
|---|---:|---|---|---|
| route-1x1 | **0 PASS** | 51,259 -> 51,740 (**+481**, 500) | 53,208 -> 53,391 (+183, 600) | slices 15,835 -> 15,843 (+8, tol. 80); RAMB36 74, RAMB18 27, DSP 13 unchanged; WNS +0.236 -> +0.333, WHS +0.028 -> +0.020 ns |
| ooc-1x1 | **0 PASS** | 23,828 -> 23,845 (+17, 250) | 20,000 -> 20,000 (0, 250) | RAMB 16/3, DSP 8 unchanged |
| ooc-8x8 | **0 PASS** | 32,467 -> 32,530 (+63, 316) | 28,220 -> 28,222 (+2, 339) | RAMB 21/5, DSP 8 unchanged |

route-1x1 moves +0.94 % LUT, +0.34 % FF, +0.05 % slices: under the assignment's 2 % STOP.

**This adoption's share** (route-1x1 against dev's own route): the host's nightly #640 measurement of dev `97aab1d0`
(RTL inputs identical to `5fcec84b`: `git diff 97aab1d0 5fcec84b -- hdl sw/litex configs <submodules>` empty), the
same shipping directive (ExtraPostPlacementOpt); its figure for dev `a032c6d6` equals the record exactly
(51,259 / 53,208 / +0.236), so the two flows agree. Dev 51,430 LUT / 53,236 FF / 15,823 slices / WNS +0.233.
Head minus dev: **+310 LUT, +155 FF, +20 slices**; the record-to-dev drift (#773, #774, #775, #780) is +171 LUT,
+28 FF, -12 slices. Placed hierarchy (receipt `route-hierarchy-head-minus-dev.txt`): `KL_gptp_shadow` +251 / +119
(its own logic +231 / +64: entry 0 and its compare; engine +55 FF; parser -65 / -80, the strict PathTrace rules
retired; uCPU +71 LUT); unchanged blocks (`csr`, `pp_shadow`, `chan_map_capture`, `talker_diag`) move by about
100 LUTs either way, as earlier rebaselines record for placement.

The ooc top is `KL_pp_shadow`; its hierarchy report instantiates none of the three RTL files this lane changes
(`milan_csr.sv` comments, `KL_gptp_shadow.sv`, `milan_datapath.sv`), so the ooc +17 / +63 LUT are dev's drift since
the record (`KL_pp_shadow.sv` and processor `ed211803` moved on dev), not this adoption.

Route detail: 101,739 of 101,739 routable nets routed, 0 routing errors; IOB packing 21 PASS, 0 FAIL, 1 INERT
(`eth0_rx_er`, no net). Corners: Slow 0C / 85C WNS +0.333, WHS +0.050 ns; Fast 0C / 85C WNS +1.638, WHS +0.020 ns.
Logs: no CRITICAL WARNING or ERROR line; the one `Synth 8-4445` match is the echoed severity command; the one
`Synth 8-6901` is dev's `crft_emit_en_w` (`milan_datapath.sv:3371`), as at #771.

**Open decision (published, not resolved here):** `docs/design/AREA_BUDGET.md:140-141` records 15 free slices and
says "The next growth on the shipping image therefore has no slice room and needs its own owner decision". This
route leaves 7 of 15,850 free (+20 over dev). The gate passes and the assignment's STOP (2 %) is not reached, so no
record was rewritten and the area pages are unchanged; the owner decides whether this growth is accepted.

## New checks, their planted defects and the words they fail with

Runner: `scripts/parent_mutants.py` (one defect at a time, a clean clone, a fresh build, the file restored after; a
clean pass first in the same clone must print no FAIL). Parent defects (P) revert the companion RTL one property at
a time; engine defects (D, X) are the donor's own planted texts taken by name from
`gptp-processor/tb/verilator/engine/mutants.py` (MUTATIONS, RECEIPT_MUTATIONS, the parser arm's PARSER_EDITS).
Clones at `46588545` (light suites), `5e7e120f` (milan_dp leg) and `fb182b19` (physical): identical `hdl/`, `tb/`,
`scripts/`, `syn/`, `sw/`, `configs/` and submodules to the head (they differ only in three documentation files).
Full table with every named check and its printed line: `receipts/mutants/mutant-table.md`; per-run JSON beside it.

| Suite | Clean pass | Defects | Killed (every named check FAIL) |
|---|---|---:|---:|
| gptp_shadow `run` | 325 checks, 0 FAIL | 7 (P1 P2 D1 D2 D3 D4 D6) | 7 |
| milan_dp `gptp` leg | 200 checks, 0 FAIL | 11 (P1-P6 D1 D2 D3 D4 D6) | 11 |
| tsn_fuzz `ptp` | 675 pass, 0 FAIL | 2 (D4 D5) | 2 |
| gptp_plane `phc_step.py` | 62 checks, 0 FAIL | 1 (D7) | 1 |
| milan_dp `ax1x1gptp` (physical) | the clean leg in the gate table | 2 (X7 X8) | 2 |

| Defect | File | New/changed check(s) it fails, words as printed |
|---|---|---|
| P1 path generation ignores entry 0 | `KL_gptp_shadow.sv` | `FAIL entry-0-only change spends one path generation got ..05 exp ..06`; milan_dp `entry-0-only change advances generation once` |
| P2 the shadow publishes no entry 0 | `KL_gptp_shadow.sv` | `published path head is the received head`, `explicit one-entry PathTrace head is the GM`, `empty PathTrace publishes thisClock at entry 0`, `path headed elsewhere publishes the received head`, `entry-0-only change publishes the new head` (each `got 0`); milan_dp `#88 post-cut response is {thisClock}`, `#88 GET_AS_PATH entry 0 is the received head`, `entry-0-only change: GET_AS_PATH serves the new entry 0` |
| P3 GET_AS_PATH entry 0 is the grandmaster again | `milan_datapath.sv` | `#87 TLV-less GM switch: GET_AS_PATH entry 0 is still GMID`, `#88 post-cut response is {thisClock}`, `#88 GET_AS_PATH entry 0 is the received head`, `entry-0-only change: GET_AS_PATH serves the new entry 0` |
| P4 AS_PATH notification ignores entry 0 | `milan_datapath.sv` | `entry-0-only change emits one GET_AS_PATH push` |
| P5 CSR face takes entries 0..6 | `milan_datapath.sv` | `#87 TLV-less GM switch: GET_AS_PATH still ends with thisClock`, `#88 GET_AS_PATH entry 1 is the parent`, `#88 GET_AS_PATH ends with thisClock` |
| P6 a full event queue refuses uncounted | `KL_gptp_engine.sv` | `a full queue moves only the event count` (the #207 arm as companion 1 rewrote it) |
| D1 a TLV-less Announce publishes {thisClock} (#87) | engine | `TLV-less selected PathTrace keeps its count got 1 exp 4`, `TLV-less selected path keeps its head`, `better TLV-less Announce keeps the previous count`, `TLV-less refresh keeps the explicit path`; milan_dp `TLV-less fabric publication keeps the path count`, `TLV-less GM switch keeps the path count`, `#87 TLV-less GM switch: GET_AS_PATH keeps count five` |
| D2 the empty sequence without a TLV (#87, the 2020 rule) | engine | `TLV-less selected PathTrace keeps its count`, `TLV-less selected path keeps its head`; milan_dp `TLV-less fabric publication keeps the path count`, `#87 TLV-less GM switch: GET_AS_PATH keeps count five` |
| D3 the received head replaced by the grandmaster (#88) | engine | `path headed elsewhere publishes the received head`, `entry-0-only change publishes the new head`; milan_dp `#88 GET_AS_PATH entry 0 is the received head`, `entry-0-only change: GET_AS_PATH serves the new entry 0` |
| D4 the path-head refusal restored (#88) | parser | `path headed elsewhere publishes count three`; milan_dp `#88 path headed elsewhere serves count three`; tsn_fuzz `better vector, path-trace head is not the announced grandmaster (10.3.10.2.1): adopted`, `...: parser drop counter unmoved` |
| D5 the path-count refusal restored (#88) | parser | tsn_fuzz `better vector, one path-trace hop against stepsRemoved 1 (10.3.10.2.1): adopted`, `...: parser drop counter unmoved`, `better vector, stepsRemoved 255 on a one-hop path trace (10.3.10.2.1b): parser drop counter unmoved` |
| D6 the empty-path refusal restored (#88) | parser | `empty PathTrace publishes count one`; milan_dp `empty PathTrace serves count one`, `#88 post-cut response is {thisClock}` |
| D7 asCapable at the fourth loss (#90) | generator | `[FAIL] asCapable falls at the fifth unanswered request after a crossing exchange got=4 exp=5`, `[FAIL] asCapable falls at the fourth unanswered request after an unanswered crossing request got=3 exp=4` |
| X7 the same, physical leg | generator | `[FAIL] five unanswered Pdelay intervals elapsed` ("LOSS elapsed 4.999445 s") |
| X8 a Sync receipt timeout only clears sync-ok (#89) | generator | `[FAIL] the 375 ms Sync timeout makes this station grandmaster`, `[FAIL] 375 ms Sync timeout asserts tu in the synchronised master role got=0x1 exp=0x3` |

Checks the companions changed but that no defect here targets on its own: the `run_selected` Sync pairs and the
tsn_fuzz `_sync_pair(0)` lines keep the selected peer alive under #89 (they are accommodations, not detectors;
X8 is the parent's #89 detector); the renamed "fifth"/"five" check names are graded by D7 and X7.

## Run notes (launch incidents, all recorded, none hides a result)

- Physical leg, attempt 1 (`setsid nohup`): the driver's own cancellation self-test aborted it after 48 s
  ("ABORTING: sweep cancellation controls failed", `hard-HUP` timed out): `nohup` makes SIGHUP ignored in the
  driver and every child, as #771 recorded. No suite ran. Kept: `r/gptp-fb182b19-nohup-aborted`.
- Attempt 2 (`setsid`, no `nohup`) did start; a `ps | grep` probe of mine missed it, so I launched attempt 3, which
  only queued on the tree lock (`flock 9`) and was cancelled by TERM before it ran anything ("logs were not prepared
  for this invocation"). Attempt 2's output directory, renamed in the confusion, was restored to its own path while
  it ran (its open log resolved again).
- Attempt 2 ran at about 0.22 simulated s per minute on the loaded host (host load average about 75; another lane's
  act replay and this lane's four sweep shards beside it), so the 5,400 s wall clock could not be met (the sibling
  lane's passing run on this host took 6,154 s). Cancelled by TERM after 975 s at 3.0 simulated s (rc 143,
  "CANCELLED: TERM"). Attempt 4 runs with the documented override `SUITE_TIMEOUT=14400` (CI_WORKFLOWS.md: "An
  explicit SUITE_TIMEOUT still overrides every selected suite's limit"); its wall time is reported against 5,400 s.
- Mutant physical legs X7 and X8 were stopped by TERM after their named checks had printed FAIL (at about 13
  simulated s of 22); the verdict is read from those lines.
- Sweep shard 2 (CPUs 112-119): the kernel OOM killer stopped its unit at its 10 GB MemoryMax during
  `capture_coherence` (third of its 16 suites, after `aaf_clock_meter` and `avtp_rxmon` passed), the failure the
  sibling #799 lane recorded: that suite's mutation bank sizes its datapath builds from the CPU affinity. Re-run
  as `scripts/rerun_shard.py` (the sibling's helper, paths only): the clone reset to the head, `VERILATOR_JOBS=2`,
  MemoryMax 10 GB, pinned to 112-115. The tally reads the union of shards 0, 1, 3 and the re-run of 2.
- Light mutant stream, first try: the restore's cleanliness assert tripped on tsn_fuzz's own `TEST_RESULTS.md`
  date-stamp rewrite; the runner now restores both campaign artifacts, and the stream was re-run from the start.

## STOP conditions

- milan-fpga top-level port or register-map change beyond the companions: none. `milan_datapath` ports
  unchanged; `milan_csr` port comments only (companion); register map text only for 0x7DC / classes (companion);
  no VERSION change.
- route-1x1 delta > 2 %: not met. +481 LUT on 51,259 (+0.94 %), +183 FF (+0.34 %), +8 slices (+0.05 %).

## Open risks and questions (published in REVIEW READY)

1. **Slice headroom, a decision for the owner.** `docs/design/AREA_BUDGET.md:140-141` says the shipping image had
   15 free slices and that the next growth needs its own owner decision. This head leaves 7 of 15,850 free (+20 over
   dev's own route, +8 over the record). The gate passes and the assignment's 2 % STOP is not reached; no record
   was rewritten.
2. **The physical leg's hosted deadline.** PR #92's companion lengthens the scenario to 899,637,137 cycles. Scaled
   the way the suite README derives it, the hosted projection is 5,347 to 5,484 s, 99.0 to 101.6 % of the 5,400 s
   budget (the README now says so); the hosted record already holds one 5,400.003 s timeout, and the workflow
   policy assigns this suite's scheduling to a follow-up. Locally, on this contended host, the leg passed in
   5,494 s only with `SUITE_TIMEOUT=14400`.
3. Pre-existing, not changed here: the tsn_fuzz README's N10-N15 pass counts are dated measurements at a 638-check
   total; `docs/MILAN_V12_ROADMAP.md:438-440`'s AS_PATH sentence is a dated record of what landed at 0x0055.
