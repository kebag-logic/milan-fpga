[R518] POSITIVE - exact head 8947bafdd62b4bf991debf7bfd8cdb73994a3a81

Round R518-3 reviews processor PR #166 (issue #163) at head `8947bafdd62b4bf991debf7bfd8cdb73994a3a81`, tree `9436b17406d7f6a1f9241331781bcc09a5d72633`, source base `86a7b0c57831c15e9cd8b42d64cc4a9843f4e726`. [Public review start](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/166#issuecomment-6036991622).

**Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open, and all five lenses are CLEAN at this head.

- **R519-2-F1 (timing evidence lacked verifiable final-head input digests): RESOLVED.**
  - I recomputed the gate's `inputs_sha256` from source blobs, using the recipe's own read order. At `c4539ff1` it equals the recorded `24ba6a24…` exactly, across all 124 components.
  - At this head it is `09369bc8…`. Only `protocol_processor_top.sv` changes, and that change is comments only: the token streams are identical and no directive is involved.
  - WNS +3.337 ns, 16 levels and 0 pairs above 20 all trace to that record.
- **My R518-2-F1 (the parked cancellation was ungraded): RESOLVED** by round 4's WD4. All eight of my R518-2 probes now behave as required.
- **One new RESIDUE (R518-3-R1).** A replay command in the README omits `mkdir -p obj_dir`.
- **One new SUGGESTION (R518-3-S1).** The mask's two lane-queue readers are not graded by any check. This gap predates the PR, and nothing establishes a behaviour defect.
- **Carried forward.** S1 is retained (SUGGESTION). R518-2-S2 is resolved. R518-2-S3 is resolved in 09 and narrowed to one unwrapped README line.

**Scope note.** The assignment's focus text says "the SAME head c4539ff1". The exact head assigned and published is `8947baf`, which adds round 4 on top of `c4539ff1`: WD4, two mutant arms, documentation, and a comment-only change to the top. I therefore reviewed both:
- the timing evidence, measured at `c4539ff1` and carried to `8947baf` by a digest equivalence;
- the round-4 delta in full.

## 1. Scope reconstruction

I read the sources in the assigned order.

- **Repository instructions.** There is no tracked `AGENTS.md` or `CONTRIBUTING.md`. I read `README.md` and `docs/README.md`.
- **Issue #163.** The frozen acceptance is in the issue body:
  1. find the arbiter input cones above 20 levels;
  2. register or restructure them so that no path exceeds about 20 levels, keeping cycle behaviour equivalent or grading the extra cycle in `tb/pp_top` and `tb/aecp_notify` with planted mutants;
  3. report the OOC 1x1 area delta. The parent three-directive sweep runs at pin adoption.
- **Manager scope decisions.**
  - [6015580618](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/163#issuecomment-6015580618): measure first; no port, register-map or parameter change; STOP above 60 LUT or 120 FF.
  - [6023618295](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/163#issuecomment-6023618295): round 2, merge #42.
  - [6028791146](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/163#issuecomment-6028791146): round 3, merge #69. The OOC result must hold.
  - [6033185530](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/163#issuecomment-6033185530): round 4, tests and docs only. It asks for WD4, arms `withdraw_mask_dropped` and `withdraw_two_clocks`, the parked case in the 03 row, the top comment and the WD README, and a re-run of the reviewer probes.
  - The evidence addenda [6032822370](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/166#issuecomment-6032822370) and [6033119744](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/166#issuecomment-6033119744).
- **Authorities.**
  - Processor documentation: 03 F03 arbiter table (Withdrawal row), 09 §8.4, and the `tb/pp_top` and `tb/aecp_notify` READMEs.
  - Milan §5.4.5.3 (a command supersedes the CONTROLLER_AVAILABLE probe).
  - The parent measurement authorities at milan-fpga `28f9666f`: `syn/ooc/pp_resource_gate.py`, whose `inputs()` is at `:186` and `located()` at `:168`, and `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.
- **Diff and history.**
  - `git diff 86a7b0c5..8947baf` covers 47 files, including the merged #42 and #69.
  - The PR's own diff against main `c9f74b68` covers 13 files.
  - The round-4 delta `c4539ff..8947baf` covers 7 files.
- **Public evidence.** The assigned `fc004672` holds only round-1 files. The current files are on milan-fpga branch `pp163-review-evidence`:
  - `7e552ca5`: the measurement record and its inputs;
  - `90f80dda`: the input components and the four non-tree inputs;
  - `386d2f42`: the digest equivalence at `8947baf`;
  - `350e06ae`: the round-4 author receipts.
- **Prior findings.** I read other reviewers' reports and the earlier findings only after my own diff pass, runs and probes. See §5.

## 2. R519-2-F1: the final-head timing evidence

### 2.1 Input digest, recomputed independently

My script `scripts/recompute_inputs.py` does not use the published component list or replay helper to build the digest; it uses them only for comparison.

- **Order.** It takes the file order, the include folders and the generics from the published `ooc-m3final/baseline_ooc.tcl`, using the gate's own `READS`, `INCLUDES` and `GENERICS` expressions.
- **Repository files.** Every repository file is hashed from its git blob:
  - processor files from this clone;
  - parent files from milan-fpga `28f9666f`;
  - `gptp-processor` at `5dce647a` and `verilog-axis` at `48ff7a7e`, the pins recorded in `parent-final-m3.json`.
- **Non-repository inputs.** The four non-repository inputs and `clock.xdc` come from their published copies.

| Item | Result |
|---|---|
| Recipe reads + headers | 121 + 3 = 124 components; names and order equal the published list; the 21 generics are equal |
| Sources | 46 processor, 60 parent, 3 parent headers, 6 gptp, 4 verilog-axis (all from blobs); 3 VexiiRiscv/RAM files, 1 normalized generated top and `clock.xdc` (published copies) |
| Digest with processor `c4539ff1` | `24ba6a244a83a0b764e6de5131a9c94752135f01ecab5afad83258c7b4767be1`, equal to `record-m3final.stdout` `inputs_sha256`; all 124 components equal the published ones |
| Digest with processor `8947baf` (this head) | `09369bc8e21e2dc00a94de148b927a4f41602ac282b18dc8bdbb12a6b5d7eaa9`, equal to `author-r4/measurement-digest/inputs-components-8947baf.json`; 123 of 124 equal, and only #46 `protocol_processor_top.sv` changes (`64a6c7f8…` to `7abc4b2b…`) |

**Why the digest moves.** The gate hashes processor sources raw. It strips comments only under the export root (`pp_resource_gate.py:194-199`), so any comment edit in the top changes the digest.

**The change is comments only** (`scripts/comment_only.py`, `receipts/digest/comment-only-top.json`):
- After stripping `//` and `/* */`, both versions give 24,634 identical tokens.
- All 12 changed lines start with `//!`, and none carries a synthesis, lint or pragma keyword or a backtick directive.
- The diff equals the published `protocol_processor_top.comment-only.diff` byte for byte.
- **Control.** The same script on `c9f74b6..c4539ff`, a real RTL change, reports unequal streams (rc 1).

All other 45 processor inputs are byte-identical between `c4539ff1` and `8947baf`. The synthesized design at this head is therefore the one measured.

### 2.2 The figures come from that record

`scripts/verify_measurement.py` (rc 0, `receipts/digest/verify-measurement.json`) checks the following:

- **Exit codes.** All six `*.rc` files (prepare, ooc, record, gate, cone, paths) are 0.
- **Record.** `record-m3final.stdout` has design `KL_pp_shadow`, a 20.000 ns clock, flow `synth_design -directive AreaOptimized_high … -mode out_of_context` with `maxThreads 2`, **WNS_ns 3.337**, WHS_ns 0.159, and `inputs_sha256` `24ba6a24…`.
- **Gate.** `gate-m3final.stdout` reports endpoint `ooc-1x1` on the same directory, `RESULT: PASS`, and LUT 23,160 against 23,179.
- **Cone run.** `cone-m3final.stdout` opens that directory's `baseline_synth.dcp`. It finds 187 arbiter cells, 561 endpoint pins and 328 startpoints, and writes 17,990 pairs. These equal the cone block of `evidence/measurement-m3final.json`.
- **Histogram.** The histogram sums to 17,990, its deepest bin is **16**, and no bin is above 20 (**0 pairs above 20**).
- **Per-group summary.** `cone-summary-m3final-all.txt` accounts for all 17,990 pairs, and its deepest group is 16.
- **Setup slack.** The setup worst slack in `measurement-m3final.json` is 3.337 with 0 failing endpoints, equal to the record.
- **Manifest.** All 32 files read match their `published_sha256` in `MANIFEST.json`.

The PR body's table ("Final `c4539ff1`": WNS +3.337 ns, 16 levels, 0 pairs above 20) and its round-4 statement ("the preceding timing and area measurements stand") agree with these receipts. **R519-2-F1 is resolved.**

## 3. The round-4 delta

| File | Change | Reviewer check |
|---|---|---|
| `tb/pp_top/notify_phases.hpp:2000-2207` | `ParkedWithdrawPhase` (WD4), run in `run_withdraw` | read in full; run at head in two builds |
| `tb/pp_top/notify_mutants.py:411-434` | `MASK_DECL`/`MASK_STAGE`; arms `withdraw_mask_dropped`, `withdraw_two_clocks` | each edit plants once; arms run |
| `tb/pp_top/sim_main.cpp:41,14064` | root header; the sixth build takes `--withdraw-only` | ran it |
| `tb/pp_top/README.md:2524-2580,2642-2647,2715-2718` | WD4 text; 91 controls; table rows | compared with the runs |
| `hdl/top/protocol_processor_top.sv:4449-4455` | comment only | §2.1 |
| `docs/architecture/03_packet_engine.md:488` | Withdrawal row states the parked case | compared with the WD4 trace |
| `docs/architecture/09_verification.md:298-320` | `--withdraw-only`; "six"; WD and CX rows | compared with the table |

### WD4 trace at head

From `receipts/runs/wd-default-run.log`:

| Clock | Cancel | Response | Release | Arbiter |
|---|---|---|---|---|
| c | yes | none | none | idle, queue 2 |
| c+1 | none | matched for row 1 | slot 2 | START, orig lane, slot 3, no start |
| c+2 | none | none | slot 3 | idle, no start, queue 0 |

- The registered mask (c+1) leads row 0's release (c+2) by one clock.
- It alone withdraws the probe that was selected at c.
- The 03 row, the top's comment, 09 and the README all state exactly this.

### WD4's fixture

- The default build moves the already-armed TIME_LIMITED deadline by 70 s in the timer RAM. It locates the entry by owner tag `0xA0`, keeps the owner and armed bit, and deposits no cancellation, response, mask, queue or arbiter state.
- The calibration pass is silent, and the replay grades every premise again: cancel clock = target, commit, matched-response owner, two distinct releases, selected slot, and three arbiter clocks.
- I ran the sixth build (shipping TIME_LIMITED default, **no deposit**) with `--withdraw-only`: **WD 4 of 4 pass** (`receipts/runs/wd-tdf-run-with-objdir.*`, rc 0). See R518-3-R1 for the invocation.

## 4. Lenses

### 4.1 Conformance: CLEAN
- **Milan §5.4.5.3 supersession is unchanged.** A cancellation on the acceptance clock lets one complete probe leave (WD1), and one on the selection clock withdraws it (WD2).
- **New case.** WD4 adds the parked case: a TIME_LIMITED drain (Table 7-147) coinciding with another exchange's matched response. The probe never reaches the wire, and the single DEREGISTER and both solicited answers leave.
- **Interfaces.** Ports, parameters and register map are unchanged against main `c9f74b68`. Round 4 changes no RTL token (§2.1).
- **Timing acceptance (items 1 to 3).**
  - Item 1: before, 146,535 pairs above 20 and a deepest path of 51 levels.
  - Item 2: after, 0 pairs above 20 and a deepest path of 16 levels.
  - Item 3: area delta, gate PASS.
  - All are evidenced by a record whose inputs I reproduced (§2). The parent sweep is a pin-adoption duty (§8).

### 4.2 RTL: CLEAN
- **Arbiter** (`KL_pp_tx_arbiter.sv:161-196`). Requester `i` wins if it is eligible, no eligible `j<i` has `key_j <= key_i`, and no eligible `j>i` has `key_j < key_i`. That is exactly the old scan's lowest-index minimum key. `pick_ok_w = |elig_w`, and at most one requester wins, so the OR-encoding of the index is exact.
- **Stage** (`protocol_processor_top.sv:4456-4461`). It is a synchronous reset to zero, the same idiom as `lane_queues`. All three readers take the registered copy (`:4482`, `:4502`, `:4580`), and the combinational mask has one reader.
- **No stale mask on a reused slot.** A mask bit at c+1 can never hit a reused slot. Reuse requires the pool release, which arrives with the mask (immediate case) or after it (parked case, or contention in `KL_pp_release_merge`).
- **Lint.** `scripts/lint_hdl.sh` with the pinned simulator: rc 0, every module `LINT OK` (`receipts/docs/lint-hdl.*`).

### 4.3 Robustness: CLEAN
- **WD4.** The parked case is now graded at the top, and the shipping-default build passes it without the deadline deposit.
- **Reviewer probes at head** (`scripts/probe_withdraw.py`, `receipts/runs/probes/`; golden WD 4 of 4):

| Probe | Defect | Result |
|---|---|---|
| `rp-abort-mask-dropped` | the arbiter abort loses the mask; both lane readers keep it | KILLED (WD4) |
| `rp-mask-lowest-only` | the stage keeps only the lowest set slot | KILLED (WD4) |
| `rp-head-mask-dropped` | the lane head's withdraw drop loses the mask | survived WD 4 of 4 |
| `rp-compact-mask-dropped` | the lane compaction loses the mask | survived WD 4 of 4 |
| `rp-lane-mask-dropped` | both lane readers lose it | survived WD 4 of 4 and the whole default build, 9,975 of 9,975 |
| `rp-mask-held-two` | old bits kept when a new mask arrives the next clock | survived; benign (no slot reuse within two clocks, §4.2) |

- **Lane-reader survivors.**
  - Without the head and compaction readers, a stale handle can be selected at c+1. The arbiter's release term then aborts it at c+2 unless `KL_pp_release_merge` holds that slot's pool release behind a lower-index release.
  - So these readers are load-bearing only under release-merge contention, which no bench constructs.
  - The same two readers dropped on main `c9f74b68` (combinational mask) also pass the whole default build, 9,971 of 9,971 (`receipts/runs/probes/main-lane-mask-dropped-*`).
  - The gap predates this PR, and the PR's readers are correct. Recorded as R518-3-S1 (SUGGESTION).

### 4.4 Tests: CLEAN
**Runs at head with the pinned Verilator 5.050** (`receipts/identity/toolchain.txt`):

| Run | Result |
|---|---|
| `tb/pp_top` default build, `--withdraw-only` | rc 0, WD 4 checks, 0 failures |
| `tb/pp_top` sixth build (`PP_TOP_TIM_DEFAULTS`), `--withdraw-only` | WD 4 of 4; rc 0 with `obj_dir` present |
| `tb/pp_top` default build, whole run (golden) | rc 0, **9,975** checks, 0 failures, as in the PR body |
| `notify_mutants.py --jobs 3 --only` the 4 WD arms and 2 cancel arms | rc 0, 3 goldens PASS, **6 of 6 KILLED** |
| Driver arm count | `len(MUTANTS)` = **91**, as in the README |

**Failing checks per arm** (`receipts/runs/mutants/failing-checks.txt`), each equal to its README row at `tb/pp_top/README.md:2715-2734`:

| Arm | Failing checks |
|---|---|
| `withdraw_unregistered` | WD1, WD2, WD4 |
| `withdraw_abort_ignored` | WD2, WD3, WD4 |
| `withdraw_mask_dropped` | WD4 |
| `withdraw_two_clocks` | WD4 |
| `cancel_one_clock_late` | CX1, IX3 |
| `cancel_one_per_command` | CA1, CA1b |

**My R518-2 probes, re-run at head** (`scripts/r518_2_reviewer_probes.py`, unchanged from the R518-2 packet; `receipts/r518-2-probes/`): rc 0, **8 of 8 as expected**.
- `ctl-withdraw` PASS.
- `r-wd-mask-dropped` and `r-wd-two-clocks` KILLED (WD 4, 1 failure each).
- `r-full-mask-dropped` and `r-full-two-clocks` KILLED (9,975, 1 failure each).
- `r-wd-sticky`, `r-wd-abort-only-comb` and `r-wd-lane-only-comb` KILLED.

At `c4539ff1`, `r-wd-mask-dropped`, `r-wd-two-clocks` and both `r-full` probes survived.

### 4.5 Docs: CLEAN (one RESIDUE)
- **Statements match the WD4 trace.** The 03 Withdrawal row, the top comment, 09 §8.4 (`--withdraw-only`, the WD and CX rows, "six", which counts FT, IX, TS, TW, DR and CX) and the WD README all state the immediate and parked cases as the trace shows.
- **README counts match the runs.** 91 controls, four WD checks, and the failing-check rows.
- **Gates** in a disposable clone at the head: `make check` rc 0 (links 1,179; IDs; figures; matrices), and `gen_matrix.py --check` rc 0 (`receipts/docs/`).
- **PR body.** The round-4 section matches the runs I made: 9,975 in the default build, 91 controls, WD4-only arms, and WD4 passing without the deposit.
- **Hosted CI at the head.** Runs 37614443898 (pull_request) and 37614439430 (push): `docs-gates` and `portability` completed with success. `suites` was still in progress at 2026-10-07T12:11:52Z, with its "Build Verilator v5.050" step skipped. No credit is taken for running or skipped steps.
- **RESIDUE.** R518-3-R1 below.

## 5. Findings

**R518-3-R1 - RESIDUE - Docs.** The documented no-deposit replay command exits 1 in a fresh tree.
- **Location.** `tb/pp_top/README.md:2575-2577`.
- **Evidence.** The text says: "build the existing sixth build (`make timer-defaults-build`) and run `./obj_tdf/Vpp_top_tdf --withdraw-only`". Done exactly so on a fresh export:
  - the run prints `WD: 4 checks, 0 failures`;
  - it then prints `FAIL: this build's tally cannot be recorded for the Makefile` and exits 1 (`receipts/runs/wd-tdf-run.*`);
  - the cause is that the binary appends to `obj_dir/build_tally.txt` (`tb/pp_top/sim_main.cpp:14026-14028`), and only the `timer-defaults` target creates `obj_dir` (`Makefile:202`);
  - with `mkdir -p obj_dir` the same binary exits 0, 4 of 4 (`receipts/runs/wd-tdf-run-with-objdir.*`).
- **Classification.** This is wording only. The test, the binary, the figures and the claim "all four WD checks pass" are all correct.
- **Exact fix.** Replace "and run `./obj_tdf/Vpp_top_tdf --withdraw-only`." with "and run `mkdir -p obj_dir && ./obj_tdf/Vpp_top_tdf --withdraw-only` (the binary appends its tally to `obj_dir/build_tally.txt`)."
- **Verification.** The corrected command on a fresh export returns rc 0 with WD 4 of 4.

**R518-3-S1 - SUGGESTION - Tests, Robustness.** The withdraw mask's two lane-queue readers are graded by no check.
- **Locations.** `hdl/top/protocol_processor_top.sv:4481-4482` (head drop) and `:4502` (compaction).
- **Evidence.** §4.3. Dropping both survives WD and the whole default build at head (9,975/9,975) and at main (9,971/9,971).
- **Impact.**
  - None is shown today. The readers are needed only when `KL_pp_release_merge` delays the cancelled slot's pool release behind a lower-index release.
  - Without them, a stale handle could then be selected and started.
  - The gap is not introduced by #163, and #163's added cycle is graded at the abort reader and the boundary (WD1 to WD4).
- **Optional outcome.** A top-level case in which a CA-builder release of a lower slot coincides with the cancelled slot's release, with a control that drops the lane readers.
- **Verification.** The control fails its named check, and the head passes.

**S1 (retained, narrowed) - SUGGESTION - Tests, Docs.** This is R518-1-S1, R519-1-S1 and R518-2-S1.
- **Already inspectable.** The cone and paths traversal commands appear in the published stdout, and the summary accounts for all 17,990 pairs (§2.2).
- **Still unpublished.** The raw per-pair tables (`arb_cone.tsv`, `arb_paths.tsv`) and the summary transformation.
- **Optional outcome.** As in round 1.

**R518-2-S3 (retained, narrowed) - SUGGESTION - Docs.**
- **Fixed.** The 09 §8.4 part: WD, CX, `--withdraw-only` and "six" are now present.
- **Remaining.** `tb/aecp_notify/README.md:15` is still a 146-character prose line.
- **Optional outcome.** Wrap it without changing its text.

### Prior public findings at this head

I read these after my own pass.

| Finding | Status at `8947baf` | Basis |
|---|---|---|
| R519-2-F1 (MINOR; retained by R519-3) | **RESOLVED** | §2: 124-component recomputation equals `24ba6a24…` at `c4539ff1`; this head's `09369bc8…` differs only by a comment-only top; figures trace to the record |
| R518-2-F1 (MINOR) | **RESOLVED** | WD4 added; arms `withdraw_mask_dropped` and `withdraw_two_clocks` fail WD4; the parked case is stated in the 03 row, the top comment and the WD README; the required probe set gives 8 of 8 as expected; the campaign arms are KILLED with goldens PASS; `make check` rc 0 |
| R519-2-S2 (SUGGESTION) | **RESOLVED** | WD4 distinguishes the mask from the release path; the extra-stage variant (`withdraw_two_clocks`, `r-wd-two-clocks`) now fails |
| R518-2-S2 (SUGGESTION) | **RESOLVED** | final `inputs_sha256` and the top blob identity are published and reproduced (§2.1) |
| R518-1-S1 / R519-1-S1 / R518-2-S1 (SUGGESTION) | **RETAINED, narrowed** | S1 above |
| R518-2-S3 (SUGGESTION) | **RETAINED, narrowed** | the 09 part is fixed; one README line remains |
| R518-1, R519-1 | POSITIVE at `cd9825c9`; no findings beyond S1 | — |

There are no submitted reviews or inline review comments on #166.

## 6. Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #163 acceptance and four manager decisions; Milan §5.4.5.3 supersession via WD1, WD2 and WD4; unchanged ports and parameters vs `c9f74b68`; timing acceptance via the reproduced record (WNS +3.337, 16 levels, 0 above 20; gate PASS) | R518-3 | 8947bafdd62b4bf991debf7bfd8cdb73994a3a81 |
| RTL | CLEAN | arbiter parallel rank (equivalence argued); stage reset and its three readers; slot-reuse safety vs release merge; round-4 top change comment-only (token-equal, no directives); `lint_hdl.sh` rc 0 | R518-3 | 8947bafdd62b4bf991debf7bfd8cdb73994a3a81 |
| Robustness | CLEAN (S1 suggestion) | WD4 parked case, with and without the deadline deposit; 6 reviewer probes at head; lane-reader survivor classified with a run on main | R518-3 | 8947bafdd62b4bf991debf7bfd8cdb73994a3a81 |
| Tests | CLEAN | pp_top default `--withdraw-only` 4/4; sixth build 4/4; whole default build 9,975/0; notify arms 6/6 KILLED + 3 goldens; 91-arm count; README failing-check rows; R518-2 probe set 8/8 as expected | R518-3 | 8947bafdd62b4bf991debf7bfd8cdb73994a3a81 |
| Docs | CLEAN (R518-3-R1 residue) | 03 Withdrawal row; top comment; 09 §8.4; `tb/pp_top` README WD and campaign text; PR body round-3 and round-4 sections; `make check` rc 0; `gen_matrix --check` rc 0; measurement-record and digest receipts | R518-3 | 8947bafdd62b4bf991debf7bfd8cdb73994a3a81 |

## 7. Real limits

- **No Vivado run.** No synthesis tool is installed on this host. The figures rest on the published record, whose inputs I reproduced from source; the netlist was not rebuilt.
- **Inputs taken on trust.**
  - The six memory-image digests (`baseline_images.json`) are taken from the manifest; their producers (LiteX/builder) were not run.
  - The three VexiiRiscv/RAM files, the normalized generated top and `clock.xdc` are hashed from their published copies.
  - No `hdl/` source in this PR feeds those images.
- **Raw cone tables are unpublished.** The 16-level and 0-above-20 figures are checked through the published JSON, the summary and the stdout counts (S1).
- **Not run by me.**
  - The full 33-suite bank (1,028,291 claimed) and the other `tb/pp_top` builds.
  - The other 85 notify arms and the other campaigns.
  - Yosys, the parent consumer set of 17, and the manager's source static/builder and native banks.
  - These are author or manager claims at this head.
- **Lane-reader impact is argued, not shown.** The R518-3-S1 contention scenario was argued from the RTL; no bench reproduces it.
- **Hosted CI.** `suites` was still in progress at inspection.

## 8. Pending manager duties

- Hosted and local workflow acceptance at the exact head, including the pending `suites` jobs of runs 37614443898 and 37614439430.
- The full source static/builder and native banks at this head are recorded as passed by the manager. They are source validation, distinct from the final current-dev candidate.
- The final current-dev candidate at the merge turn: source base `86a7b0c57831c15e9cd8b42d64cc4a9843f4e726`, live dev `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`.
- The parent three-directive sweep on the merged pin, at +0.03 ns or better in each directive (acceptance item 3, at pin adoption).
- Carry R518-3-R1 to the residue checklist.
- Physical calibration is NOT RUN. Field skips are not hardware proof.

## 9. Replay and integrity

Scripts are in `scripts/`; the exact commands are in `receipts/digest/command.txt`.
- `recompute_inputs.py`, `comment_only.py` and `verify_measurement.py` cover the timing evidence.
- `probe_withdraw.py TREE WORK OUT V --jobs 3` runs the round-3 probes.
- `r518_2_reviewer_probes.py TREE OUT V 4 NAMES…` runs the R518-2 probe set.
- `notify_mutants.py --output DIR --verilator V --jobs 3 --only …` runs the campaign arms, from an exported head tree.
- `verify_state.py REPO HEAD TREE OUT` checks the clone.

Home-directory prefixes in the receipts are shown as `$HOME`.

**Integrity.**
- The reviewed clone is byte-exact at the head: 581 tracked entries by raw blob bytes and modes, HEAD tree = index tree = `9436b17406d7f6a1f9241331781bcc09a5d72633`, status empty, and no submodule gitlinks (`receipts/checkout-state-final.json`).
- Builds and probes ran only in disposable exports under `scratch/`.
- No source fix, commit, push, merge, GitHub write, author contact, other-checkout edit or hardware use took place.
- Unit memory peak: 12,211,933,184 bytes, including page cache, under the 12,884,901,888-byte cap.

R518-3 FINISHED
