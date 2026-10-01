# [A479] Lane C6 round 3 handoff: notifications and Identify

Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, branch `c6-notifications`
(PR #139), round-3 start `88e0bf82888d6ad83b500425a786814da467610b` (origin URL and HEAD
confirmed). Assignment: #80 comment 5932649053. Reviews: R420-2 (#139 comment 5930357457,
one MINOR), R421-2 (#139 comment 5930105280, one MINOR, the same). Roles: executor [A479],
manager [A10], reviewers [R420] (internal), [R421] (external).

## Status

REVIEW READY at `9624ef4c452d708de68a901d5e645bdfa1f5d6f5` (#80 comment 5938882964, posted once,
after this file and PR-BODY.md were final). TAKEN posted on #80 (comment 5932660024). Two commits on `88e0bf8`, no
merge, no rebase; the lane tree is clean.

| Item | State |
|---|---|
| Merge | none this round (the assignment has no merge of main) |
| 1. Latch a press made during the post-burst gap (R420-2 F1, R421-2 F1) | committed `ed000fe` |
| 2. Suggestions (R421-2 S1, R420-2 S2, R420-2 S1 / R421-2 S2) | committed `9624ef4` |
| Gates | done at the head `9624ef4`, all rc 0 (below) |

## Merge resolution

None. The round-3 assignment has no merge of main, and the branch is not rebased.

## 1. A press made during the gap is latched (R420-2 F1, R421-2 F1), commit `ed000fe`

**Ruling** (#80 comment 5932649053): latch, do not document the window.

**Clause.** IEEE 1722.1-2021 Figure 7-142: WAITING moves to IDENTIFY on
`identifyButtonPressed`, and IDENTIFY's entry action is txIdentify(). §7.5.1 and
§7.5.1.2.1: three transmissions "with a delay of 150 milliseconds between
transmissions". Milan §5.4.5.4: the variable is TRUE while the user wants the PAAD to
report itself.

**Defect.** Round 2 added `&& !gap_r` to the WAITING start (`KL_aecp_notify.sv:794` at
`88e0bf8`) and read the button as a level, with no latch. A press that began and ended
inside the T-IDENT-BURST gap after a burst's third frame sent nothing. The same guard on
the HOLD start had a second form of it: a release and a new press inside a burst, still
held when the third frame left and let go inside the gap, also sent nothing. And a new
press made and let go inside a running burst was never seen (R421-2's related wording).

**RTL fix** (`hdl/aecp/KL_aecp_notify.sv`, line numbers at `ed000fe`):
- `:728` new flop `prs_r`: a press is owed a burst when the gap ends. Reset at `:777`.
- `:801-804` (before the case): a new press after a release seen inside a burst
  (`btn_q2_r && rel_r` in I_SEND, I_GAP or I_HOLD) is latched.
- `:806-818` I_WAIT: a press seen while `gap_r` runs is latched (`:810`), and the burst
  starts on `(btn_q2_r || prs_r) && !gap_r` (`:811`), clearing the latch. The gap still
  holds: every start waits for `!gap_r`, so no inter-frame gap goes under T-IDENT-BURST.
- `:863` the I_HOLD start clears the latch too; a release in I_HOLD goes to WAITING with
  the latch kept.
- Banner `:170-176`. Lint clean at `EN_IDENTIFY_NOTIF_P` 0 and 1. No port, no parameter.

**Tests** (`tb/pp_top/notify_phases.hpp` section ID8; section ID 106 -> 166 checks at
`ed000fe`). The gap's end is the IDENT-BURST expiry on the shared timer bus; the wrap
(`tb/pp_top/pp_top_wrap.sv`) gains three observe-only taps, `dbg_ident_gap_arm_o`,
`dbg_ident_gap_deadline_o`, `dbg_ident_gap_end_o` (test RTL only, like its other taps;
not a processor port):
- ID8-ID8e: a 30 ms press made 2 ms after the third frame left: one burst, 15,301
  clocks after the third frame, first frame 166 clocks after the expiry (the expiry
  came 63 clocks into its deadline's ms).
- ID8f-ID8i: a 200 ms press at the same point: one burst, the same 166.
- ID8j-ID8n: a 30 ms press whose synchronised level the sequencer first samples one
  edge before the expiry's edge, on it (k = 0, "exactly at gap end"), and one and two
  edges after it. The expiry is predicted from the arm and ID8's 63 (ID8j checks it).
  k = -1, 0, +1 start on the same edge as the latched press (166), k = +2 one clock
  later (167): the measure resolves one clock, and k = 0 is really the boundary.
- ID8o-ID8r: a release and a new press inside a burst, held past the third frame, let
  go 30 ms into the gap: one more burst at the gap's end.
- ID8s-ID8v: a release and a new 30 ms press between frames 1 and 2, let go before the
  burst ends: one more burst at the gap's end.
- ID1-ID7 measured values are byte-identical to `88e0bf8`'s.

**Failing arm on the round-2 RTL** (the new tests on `88e0bf8`'s `hdl/`, scratch copy):
at `ed000fe` 23 of 143 checks fail; with the head's tests (ID9 added, ID8 and ID9 moved before
ID6) 29 of 155 (`receipts/id-head-tests-on-round2-rtl.log`). Three are the
lost presses (ID8, ID8o, ID8s: 3 frames, want 6); the rest follow (identifySequenceID
short by the lost bursts: ID8g, ID8l, ID9b, ID9f; ID8's start never measured: ID8i, ID8n).

**Controls** (`tb/pp_top/notify_mutants.py`), all KILLED:

| Mutant | Planted | Named checks |
|---|---|---|
| `ident_wait_ignores_gap` (the single-guard control) | `&& !gap_r` dropped from the WAITING start only; the latch stays | ID8c, ID8h |
| `ident_press_not_latched` | the WAITING latch line removed | ID8 |
| `ident_burst_press_not_latched` | the in-burst latch line removed | ID8o, ID8s |
| `ident_next_burst_at_once` (kept) | both starts' `!gap_r` dropped | ID3f, ID7r |

`ident_t0_at_request` and `ident_next_burst_at_once` were re-anchored to the new WAITING
start text. All 18 identify controls KILLED at `ed000fe` (one run, 6 min 31 s).

**Docs**: 06 §7 "Identify" and F06.16, integrator guide §6, operator guide (the button
row), 08 F08.1 T-IDENT-BURST, 09 §8.3 TIM row, `tb/pp_top/README.md` section ID and the
mutation record. The three now say the same: every new press after a release is answered
with a burst, a press made while a burst or the gap after it runs is latched and its
burst starts when the gap ends, and presses while one is owed add none.

## 2. Suggestions, commit `9624ef4`

| Suggestion | Disposition |
|---|---|
| R421-2 S1: a MAC stall on a frame's last byte; a control that drops `ready` from the departure check | **Taken.** Section ID9 (`tb/pp_top/notify_phases.hpp:848-900` at `9624ef4`): the bench's `stall_tx_at_eof` hook, armed once the identify frame is part-way out, holds `tx_ready_i` low on the eof beat for 400 ms. ID9-ID9d frame 1's last byte (it leaves 40,001 clocks after the stall began; frame 2 follows by 15,232 clocks), ID9e-ID9h frame 2's (frame 3 follows by 15,299). Control `ident_departure_ignores_ready` (`hdl/top/protocol_processor_top.sv:4319`, `&& arb_tx_ready_w` dropped from `busy_r`'s clear): KILLED by ID9d and ID9h (63 clocks, the round-1 bunching). Clause: IEEE 1722.1-2021 §7.5.1 (150 ms between transmissions) |
| R420-2 S2: the `tb/pp_top/sim_main.cpp` "two builds" comment | **Taken.** The tally comment in `main()` now says three builds, and the file header ("The suite builds twice") now names the third build too. Comment only |
| R420-2 S1, R421-2 S2: the one-tick timer margins (`now_ms_i + 151`, `t0 = now_ms_i + 1`), invisible on the compressed timebase | **Taken: a full-timebase check, cheap enough.** `tb/aecp_notify` gains a second build (`EN_IDENTIFY_NOTIF_P` = 1, `-DAECP_NOTIFY_IDENT`, `make identify`) running section FT (`tb/aecp_notify/sim_main.cpp:211-390`). 1 ms is 100,000 clocks (the F01.5 default P-CLK-HZ of 100 MHz with the top's default prescaler); the bench is the engine, the MAC and a timer model that fires a due slot on the first clock of its deadline's ms with no sweep delay (the least favourable placement). FT2: frame 1 leaves two clocks before a ms boundary, frame 2 is presented 15,000,004 clocks later (window 15,000,000 to 15,000,008). FT3: frame 2 leaves on a ms's first clock, frame 3 presented 15,100,002 later (under one tick more). FT4: held, the next burst 100,000,004 clocks after frame 1 left. Controls `ident_burst_deadline_one_tick_short` (`+ 1` dropped: FT2 14,900,004) and `ident_t0_same_ms` (FT4 99,900,004): both KILLED. The suite runs 10 + 4 checks; the Makefile sums the two builds' tallies as `tb/pp_top`'s does. 20 s of simulation |

**Arm order** in section ID: ID8 and ID9 run after ID5 and before ID6's reset (sequence_ids
10 to 27), so the section still ends with ID7. Both reviewers' probe scripts anchor on
`a_tx_stall_mid_burst_never_bunches_it();` being the last call in `run()`; this keeps them
applicable unchanged. Every ID1-ID7 measured value is byte-identical to `88e0bf8`'s.

**Docs:** `tb/pp_top/README.md` (ID9, the margins paragraph, the mutation record: 40 of 40,
the counts re-measured at `9624ef4`), `tb/aecp_notify/README.md` (both builds, section FT,
its mutation record), 09 §8.3 (the FT row; ID9 in the ID row), 08 F08.1 T-IDENT-BURST (the
deadline counts from the first boundary after its arm, made on the departure's next clock or
later, so never less than T-IDENT-BURST: FT2 grades exactly that).

## Parent-visible list, round 3

Read against the parent at milan-fpga dev `ea3fb388`. Round 3 adds no top port, no top
parameter, no register and no module port; nothing changes at the parent's setting
(`EN_IDENTIFY_NOTIF_P` = 0). `parent-adoption-c4c6-ea3fb388.patch` is unchanged
(sha256 `67bcd69852e5d090abc635e8dd66e5159667847ebf83d85aba9599d7cff7bd7c`).

| # | Change | Parent effect | Parent disposition |
|---|---|---|---|
| 1 | `KL_aecp_notify` gains one flop, `prs_r`, inside the identify generate | none at 0 (the generate is not built); at 1, one FF | none |
| 2 | `tb/pp_top/pp_top_wrap.sv` gains three observe-only outputs (`dbg_ident_gap_*`) | test RTL inside the processor's own suite; the parent's port-contract gate reads only `hdl/` | none |
| 3 | `tb/aecp_notify` builds twice and prints one summed tally | the processor suite runner reads the summed line (run_suites.sh rc 0) | none |
| 4 | `tb/pp_top/notify_mutants.py`: 40 controls (34 at round 2), a `tb/aecp_notify` suite target and one more tally shape | the combined patch's `DUT_READER_DISPOSITIONS` entry covers the driver as a whole | none |
| 5 | docs: 06 §7 / F06.16, 08 F08.1, 09 §8.3, integrator §6, operator guide | the parent's matrix may cite `tb/aecp_notify` FT beside section ID for 5.4.5.4 | optional |

## Gates

Verilator 5.050 (the CI pin, `$VALIDATION_TOOLS/verilator-v5.050`) behind a scratch shim
that caps `--build -j 0` at 8; one heavy command at a time. Yosys 0.66, sv2v 0.0.13. Every
processor command ran on a `git archive` export of the head under `$VALIDATION_STORAGE/c6r3/head`,
except `make -C tb/nvm_port figures` and the SRP campaign, which ran in a scratch shared clone
at the head (`$VALIDATION_STORAGE/c6r3/headclone`); the lane tree's `git status` stayed empty. Receipts: `receipts/` in this directory (the
home-directory prefix in them is written `~`).

### Processor, every command at the head `9624ef4` (all rc 0)

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | UPC map gate PASS (58 constants, 82 entry points); 33 suites, 1,018,160 checks, 0 failing (round 2: 1,018,084). `pp_top` 8,242 (default 8,044, fixture 20, identify 178), `aecp_notify` 14 (10 + FT 4), `originator` 107, `ucpu` 396; 12 min 31 s on a shared host. `receipts/run_suites-9624ef4.log` |
| `./scripts/lint_hdl.sh` | 0 | 41 modules LINT OK; `KL_aecp_notify`, `KL_aecp_engine`, `protocol_processor_top` also 0 findings at `-GEN_IDENTIFY_NOTIF_P=1`. `receipts/lint_hdl-9624ef4.log`, `lint-en1-9624ef4.log` |
| `make check` (lint, wavedrom-check, links, matrix, modmatrix, params on the export; stale in the lane tree, read-only) | 0 | 41 mermaid + 18 wavedrom, links 999, 115 REQ / 17 GAP, 94 rows 0 untested, parameters 27 = 27 = 27, stale clean |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` | 0 | 36 tops YOSYS OK and the Xilinx memory-map check (`KL_aecp_engine`); 88 s |
| `git diff --check 88e0bf82..HEAD`, `3f3ea56b..HEAD` | 0, 0 | |

### Mutation campaigns at `9624ef4`

| Campaign | rc | Result |
|---|---:|---|
| `python3 tb/pp_top/notify_mutants.py --jobs 1 --only ...` (four chunks: 11, 10, 8, 11) | 0 x 4 | **40 of 40 KILLED** by their named checks; goldens `pp_top` identify build, `--identify-only`, `--notify-only`, `aecp_notify` identify and `originator` PASS. 4 min 19 s + 4 min 37 s + 2 min 29 s + 2 min 49 s. `receipts/notify-mutants-9624ef4.json` (per-mutant failing checks) and `.stdout`. Anchors: 40 mutants, 43 anchors, each exactly once (`receipts/mutant-anchor-check-9624ef4.txt`; d3 92 and acmp 19 likewise) |
| `python3 tb/pp_top/acmp_mutants.py --jobs 1` | 0 | goldens `acmp_listener`, `pp_top`, `rx_validator` PASS; 19 of 19 KILLED; 4 min 59 s |
| `make -C tb/adp_engine mutants MUTANT_OUTPUT=DIR` | 0 | 30 of 30 KILLED; 32 checks, 0 FAIL; 5 min 56 s |
| `make -C tb/maap mutants MUTANT_OUTPUT=DIR` | 0 | 3 controls PASS (maap 196, pp_top maap-internal 34, rx_validator 555); 29 of 29 KILLED; 32 checks, 0 FAIL; 4 min 23 s |
| `python3 tb/pp_top/gsi_mutants.py --output DIR` | 0 | 20 of 20 detected by named checks; golden and restored PASS; 13 min 26 s (ran past the 10-minute foreground limit, so the harness moved it to the background; it finished rc 0) |
| `python3 tb/acmp_talker/retry_mutants.py --logs DIR` | 0 | 62 mutants KILLED; 7 equivalence and 1 performance controls retained; baseline and restored rc 0; 6 min 41 s |
| `make -C tb/nvm_port figures` | 0 | every measured figure agrees with the tree (baseline 136 PASS; 2 waivers printed with their reasons); 4 min 2 s. Run in a scratch shared clone at the head: on the `git archive` export it exits 2 with every figure `[ok]`, because its provenance check reads git revisions (`dc354be~1`, `62d96d6~1`) that an export does not carry (`receipts/nvm-figures-9624ef4-export-no-git.log`) |
| `make -C tb/srp_top mutants MUTANT_OUTPUT=DIR` (in the clone) | 0 | 11 controls PASS; 78 of 78 KILLED; assertion coverage 65/65; 90 checks, 0 FAIL; 32 min 31 s (past the foreground limit, finished in the background) |
| `python3 tb/pp_top/d3_mutants.py --jobs 1 --only ...` (five chunks: 6, 25, 17, 18, 17) | 0 x 5 | **83 of 83 KILLED** by their named checks; goldens `acmp_nvm`, `pp_top`, `rx_validator` PASS in each chunk that uses them; 8 min, 30 min 41 s, 17 min 52 s, 23 min, 11 min (the longer chunks finished in the background). `receipts/d3-mutants-9624ef4-chunk{1-5}.stdout` |

### Parent consumer set at milan-fpga dev `ea3fb388`

Scratch copy `$VALIDATION_STORAGE/c6r3-parent/src`; the trusted checkout was not touched. Commits:
1. `7ebe2b0`: `git archive ea3fb388` of the trusted checkout; `external` (`efeb541`),
   `gptp-processor` (`5dce647`) and `third_party/verilog-axis` (`48ff7a7`) cloned from their
   `.gitmodules` URLs at the recorded pins (the trusted checkout carries no submodule
   objects); `protocol-processor` a shared clone of this lane at `9624ef4`. `git submodule
   init` registers them, with no fetch. Its 981-entry index equals the trusted tree's except
   the processor gitlink (`b2db3a97` there, `9624ef4c` here).
2. `8b777d7`: `git apply parent-adoption-c4c6-ea3fb388.patch` (unchanged, from this directory;
   `git apply --check` clean).

| # | Command | rc | Result |
|---:|---|---:|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | every ratchet at or under budget (multi-declarator 0 <= 0, long function 0 <= 0, build without warnings 0 <= 0) |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | every ratchet at or under budget (too many parameters 7 <= 7, over-long line 0 <= 0) |
| 3 | `python3 scripts/check_rtl_source_lists.py` | 0 | OK: 107 files in the milan_datapath closure, 4 of 4 consumer lists; protocol-processor 36/42 tops, 6 recorded |
| 4 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | OK |
| 5 | `python3 scripts/check_port_contracts.py` | 0 | OK: 3,793 first-party ports (protocol-processor 1,752, as at round 2); undocumented protocol-processor 111 <= 111; 52 literal-bound, 62 without a local rationale, all recorded |
| 6 | `python3 scripts/measure_naming.py --check` | 0 | PASS: 96 candidates, all recorded by identity |
| 7 | `python3 scripts/measure_test_evidence.py --check` | 0 | PASS: 73 <= 77 without a mutation arm, 10 <= 10 unseeded, 0 <= 0 unexplained DUT-source readers, 3 <= 3 wall-clock |
| 8 | `python3 scripts/docs_check.py` | 0 | 0 findings across 182 md + 953 scrubbed files; scrub self-test 23/23; routing 4/4 |
| 9 | `python3 scripts/xvlog_gate.py --check` | 0 | PASS: 4 findings == ratchet (hdl/ 0, pinned processors 4, the same four keys as the trusted budget); 2 min 19 s; the scratch tree clean after it |
| 10 | `python3 sw/builder/test_builder.py` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11: the calibration report needs a local mf48 build tree, as in rounds 1 and 2); 17 min 40 s |
| 11 | `python3 scripts/lint_rtl.py --check` | 0 | PASS: 90 <= ratchet 90 (17 waived, 0 justified lint_off) |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | 311 checks, 0 failures; RESULT: PASS; 4 min |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | both lint passes |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 checks, 315 PASS |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | gmstep 104; 182 + 182; milan_datapath 235, 235, 232; media_aclk 191; 382, 416, 1,845, 1,847, 3,525, 1,845 and 33 checks in the other benches; 9 RESULT: PASS, 0 FAIL; the 6 + 6 mutant arms pass; 25 min 45 s (finished in the background) |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | tdm8_render 65 and 152 checks, 0 failures; 5 of 5 leg-defect arms caught; 5 min 36 s |

Logs over 200 KB, not copied:

| Log | Bytes | sha256 |
|---|---:|---|
| parent `pp_shadow` (gate 12) | 308,393 | `f684315f788af2c65321e8ab9975b253042e60640f1152ee1cd3f2d0c2649953` |
| parent `milan_dp` (gate 15) | 2,001,623 | `3b513fd84bc1d2d4e6dd699db4cb45d2515c1afac3a54e2572f5ff884ac32a15` |

Receipts for gates 1-11, 13, 14 and 16: `receipts/parent-gates/`.

### Both reviewers' probes, re-run unchanged at `9624ef4`

Read-only scripts from the review packets, outputs in scratch; `receipts/reviewer-probes/`.

- `r420_probes.py --head <export> --work <dir> --out <dir>` (R420-2):
  - `head_with_probe`: 180 checks, 0 failures. RP1: 6 frames, the second burst 15,301
    clocks after the third frame (RP1b >= 15,000). **RP2: 3 frames after the press** (0 at
    `88e0bf8`).
  - `head_with_sweeps`: 184 checks, 0 failures; RS1 (ten stalls) smallest gap 15,233; RS2
    31 bursts, smallest gap 15,232, largest 1->2 16,250.
  - `hold_ignores_gap`: 4 failures (ID3f, ID7r, ID8q, ID8r): KILLED.
  - `wait_ignores_gap`, `wait_ignores_gap_with_probe`: REFUSED by the script itself (its
    anchor is round 2's `I_WAIT: if (btn_q2_r && !gap_r) begin`, which the latch replaced).
    `ident_wait_ignores_gap` is the same control on the new start, KILLED by ID8c and ID8h.
  - `burst_deadline_one_tick_short`: passes section ID (178 checks), as expected on the
    compressed timebase; `ident_burst_deadline_one_tick_short` is KILLED by `tb/aecp_notify`
    FT2.
- `r421_arms.py <export>` then section ID (R421-2): 188 checks, 0 failures. R421c (30 ms
  press 2 ms after frame 3): 6 frames, the next burst 15,301 clocks after frame 3. R421d
  (200 ms): the same. R421a/R421b (eof-beat stalls of frames 1 and 2): gaps 15,232 and
  15,299.

Both scripts' anchors apply at the head because ID8 and ID9 run before ID6, so section ID's
`run()` still ends with `a_tx_stall_mid_burst_never_bunches_it();`.

### Resource cost, out of context (module level)

Yosys 0.66, `sv2v` of `pp_pkg` and `KL_aecp_notify`, `synth_xilinx -family xc7 -flatten
-top KL_aecp_notify`, the parameter set by `chparam` (`receipts/notify-module-synth.txt`):

| Revision | EN | LUT | FF | CARRY4 | RAM32M |
|---|---:|---:|---:|---:|---:|
| `88e0bf8` | 0 | 6,523 | 1,721 | 249 | 1,048 |
| `9624ef4` | 0 | 6,523 | 1,721 | 249 | 1,048 |
| `88e0bf8` | 1 | 8,128 | 1,787 | 279 | 1,048 |
| `9624ef4` | 1 | 6,656 | 1,788 | 279 | 1,048 |

At 0 the module is round 2's exactly. At 1 the latch adds one flip-flop and no carry; the
LUT figure at 1 moves by mapper variance (as recorded in round 2). The whole top was not
re-synthesised: at 0 nothing in it changed, so round 2's whole-top figures at 0 stand.

## What remains

- Hosted CI on the PR, and the round-3 reviews ([R420] internal, [R421] external).
- The parent adopts `parent-adoption-c4c6-ea3fb388.patch` (unchanged) when it moves its
  processor pin past this head.
- Retained, unchanged and recorded in `tb/pp_top/README.md`: R420-1 S1 (three controls
  survive with every section-ID check passing) and R420-1 S4 (the shared limiter's
  one-tick reading).
- One reading this round relied on, stated for the manager: the ruling asks to latch a press
  made during the gap. The same §6 promise ("a burst for every new press after a release")
  was also broken by a new press made inside a running burst and let go before the gap ended
  (R421-2's related note), so that press is latched too (ID8o, ID8s; control
  `ident_burst_press_not_latched`). No press is now lost anywhere; no port, parameter or
  parent-visible behaviour changed.
- Process notes: the commands that ran past the 10-minute foreground limit (run_suites, the
  GSI, SRP and three d3 chunks, the builder tests and `milan_dp`) were moved to the
  background by the harness and finished rc 0; nothing ran beside them. The host was shared
  with other lanes' jobs, so wall times are longer than round 2's.
- No hardware was used. The resource figures are yosys out of context; a Vivado
  out-of-context run at the parent is the authoritative figure.
- Unchanged from round 1: the optional overflow eviction sweep is not attempted (a recorded
  decision), and the solicited DEREGISTER that does not push is recorded, not changed.
