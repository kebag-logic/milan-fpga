[R391] POSITIVE - exact head 9dce84ea60857de74457f74b5bf08d89bd3ba408

# R391-5: independent external review of processor PR #132 (issue #131, D3 lane 1), round 5

- **Repository.** Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #132, issue #131, round R391-5.
- **Head.** Exact head `9dce84ea60857de74457f74b5bf08d89bd3ba408`, tree `1601ef9ed9db2995b73acf8c625f955e5e8c6315`. The live PR head reads the same sha. Base `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`.
- **Delta reviewed.** `84572585..9dce84ea` is one commit, `9dce84e`: 6 files, +216 / -23, all under `tb/` and `docs/`.
  - Tests: `tb/acmp_nvm` N11a-c (`sim_main.cpp`), four new taps in `acmp_nvm_wrap.sv`, and five new controls in `tb/pp_top/d3_mutants.py`.
  - Docs: 09 §8.2 (one row, the 81 count) and the `acmp_nvm` and `pp_top` README mutation records.
  - Also reviewed: the PR body's Round 5 section and its consolidated parent-visible list, and the author's `parent_edits.py` (`author-r5`, sha256 `80d2c396...`, branch `pp131-review-evidence` at `fab7ca16`).
- **No RTL change.** `git diff --quiet 84572585 9dce84ea -- hdl syn scripts .github` is empty.
- **Authorities.**
  - The round-5 assignment (issue #131, 5883464746): items 1-4, the STOP condition and the gates.
  - The earlier rulings, as in round 4: 5880658258, 5876655419, 5873580386 and 5880274287.
  - The arbiter's own banner (`KL_pp_nvm_mgr_arb.sv:20-65`).
  - Parent contract `docs/design/SAVED_STATE_MATERIALIZATION.md` §5.1 and §8.1: AECP is held from reset to the D3 terminal, and the image is loaded before `PP_CTRL[1]`.
- **Reconstruction order.**
  1. Processor README, docs/README and 09. There is still no AGENTS.md or CONTRIBUTING.md.
  2. Issue #131 through the round-5 assignment, the author's TAKEN and REVIEW READY (5884424686), the PR body (rounds 1-5) and the review-start comment 5884454994.
  3. The contract sections above, and the parent at live dev `13eda870`.
  4. `git diff c951a9ff..9dce84ea`, then the round-5 commit in full.
  5. Public evidence:
     - milan-fpga `b657a2de` `review-evidence/pp131-r1`;
     - the author's `author-r5` packet on `pp131-review-evidence` (`fab7ca16`);
     - the hosted check runs at the exact head.
- **Inputs from my earlier rounds.** My own round-4 packet: its scripts, and F1 and S1. No private material was read.
- **The other reviewer's findings.** R390-4's report was opened only after this report's verdict, findings and ledger were fixed in a draft. Its F1, S1 and S2 were known before that only as the round-5 assignment and the PR body state them. R390-5 is concurrent and was not read.

## Verdict

POSITIVE. No MINOR or higher finding is open. Two SUGGESTIONs, S1 and S2, do not affect the verdict.

**Item 1: `ax1x1gptp` (R390-4 F1).**
- The PR body now names `sim_ax1x1gptp.cpp` under the `PP_CTRL[1]` obligation and states that it is outside the consumer set.
- `parent_edits.py` starts the walk at the top of `configure()`:
  - `configure()` follows each of the harness's two `reset()` calls (`sim_ax1x1gptp.cpp:932`, `:994`);
  - the image is loaded from `aemi.bin` before the first reset;
  - the first AECP command is the pre-acquisition GET_AVB_INFO, after `configure()`;
  - the check requires PP_STAT[2] done, not CLOSED.
- The edit is right in placement and strength.
- Measured in my scratch parent at live dev `13eda870`, with every declared edit: `make -C tb/verilator/milan_dp ax1x1gptp` rc 0, **139 checks, 0 failures**. That is the harness's 137 plus the walk check on each of its two boots, both PASS. All 15 GET_AVB_INFO and GET_AS_PATH checks PASS. The run simulated 16.99 s in 3,076 s of simulator wall time (3,103 s with the build) on a shared host, which matches the author's 139/139.

**Item 2: the timed leg (my R391-4 F1).** Resolved.
- The declared `sim_nxn.cpp` edit runs `prove_a_wedged_response_memory_reports_and_heals()` inside `prove_the_shipped_descriptor_image_enumerates()`. It comes after the restore and the first descriptors, and before the `NOTIFY_TIMED_TB` return.
- At `13eda870` with the edits:
  - `notify` passes 378/378 with its 6 `[AECP-WTMO]` checks, where round 4's edit gave 0;
  - `nxn` passes 1,841/1,841, also with 6.
- The base `notify` at `13eda870` has 381 checks: 6 `[AECP-WTMO]` and 5 `[AECP]` degrade checks. 378 = 381 − 5 + 2 hold checks.
- The body states the retirement of the degrade arm and why (§8.1).
- A parent-side side effect of the new order is S2.

**Item 3: `9dce84e`, the arbiter's own contract.**
- N11a-c are correct and cycle-exact.
  - N11a holds manager 1's abort from its WRITE strobe to the write's end. It checks: issued as a commit, never drained, 28/28 bytes, done, one ERASE and one WRITE, and the device byte-exact.
  - N11b presents manager 1's abort alone in the issue cycle of each of the walk's 8 READs. My monitor sees exactly those 8 cycles.
  - N11c: after a completed WRITE, a READ abandoned in its issue cycle is drained from issue+1.
- The head's arbiter passes all three, as its banner permits, so the STOP condition does not apply.
- In my own run of the in-tree campaign, `d3_mutants.py` kills **81 of 81, goldens PASS**, and all 84 result rows equal the README counts.
  - The five new controls are KILLED: `issue_arm_cross_intent`, `issue_arm_ignores_we`, `issue_arm_write_too`, `issue_arm_stale_we` and `owned_arm_write_too`.
  - My three round-4 survivors now fail `tb/acmp_nvm`: `issue_arm_stale_we` fails N11a and N11c, `issue_arm_cross_intent` N11b, `issue_arm_write_too` N11a.
- **The author's statement.** It says a manager-1 grant while manager 0 presents an abort stays ungraded "by construction". That is **true for the input it names, but incomplete** (S1).
  - Why the named input is unreachable: the binding manager raises its abort only in a stalled `H_RS_STREAM` clock (`KL_acmp_nvm_shadow.sv:563-576`), and every done or err leaves that state (`:584-595`). Its strobe is always issued at once. So its abort only ever meets its own READ, owned or being issued, and never a manager-1 grant.
  - Why the statement is incomplete: six single-manager variants of the banner's rules survive every graded suite (`tb/acmp_nvm` 359, `tb/pp_top` 7,868). Each is an input no in-tree manager presents:
    - `cross_iss_m0_drains_m1`, the named one;
    - `cross_own_m0_drains_m1`;
    - `cross_own_m1_drains_m0`;
    - `write_iss_m0_only`;
    - `write_own_m0_only`;
    - `stale_we_m0_only`.
  - My arbiter-input monitor shows that none of those inputs occurs with both real managers: 0 clocks over the whole `tb/pp_top` default run and over 17,406 aggregate-sweep runs. In `tb/acmp_nvm` only manager 1's synthetic N10/N11 inputs occur.
  - So no reachable behaviour is ungraded. The unreachable residue is wider than one input.

**Item 4: R390-4 S2.**
- **(a)** The image-less legs name CLOSED. At `13eda870`, `main` reads `[PASS] PP_STAT the restore walk ended CLOSED (no AEM image: busy 0, done 0, fail 1)` and passes 234/234.
- **(b)** Is item 2.
- **(c)** `wr_chg_o` is on the named no-connect `wr_chg_nc_w`. `nvm_cosim` lint gives rc 0, 85 warnings (the base 84), 0 PINMISSING, and its only `wr_chg` line is one UNUSEDSIGNAL. `nvm_cosim` quick passes 315/315.

**The edits at the manager's dev.**
- The author's `parent_edits.py` applies unchanged at live dev `13eda870`.
  - Dev moved `eaa88a32..13eda870` only in firmware, builder tests, the capture and service-budget benches, and the `nvm_cosim` host.
  - My scratch diff equals the author's `parent-edits.diff`, apart from the gitlink and my two scratch-only make targets.
- The firmware statement in the list still holds at `13eda870`: `nvm_boot()` returns before `nvm_restore_walk()` on "persistence disabled" (`milan_baremetal.c`), and `MILAN_NVM_RESTORE_TIMEOUT_MS` is 3,000.

**No RTL change.**
- The aggregate sweep at this head is identical, line for line, to my round-4 golden: 274 lines, 17,406 runs, 0 BAD.

## Findings

### S1 - SUGGESTION - Tests, Docs - the arbiter's own contract is graded for manager 1's halves only; the "one input stays ungraded" statement undercounts

- **Where.**
  - `tb/acmp_nvm/sim_main.cpp:2597-2664` (N11). `:650` presents manager 1's abort on manager 0's READ only while the binding manager's strobe is out.
  - `docs/architecture/09_verification.md:192` maps "an abort drains only its own manager's READ" to N11b.
  - The REVIEW READY comment (5884424686) says "One arbiter input stays ungraded in the tree, by construction".
- **Authority.** The banner rules, `KL_pp_nvm_mgr_arb.sv:38-65`. The purpose the round-5 assignment gave the arms: "so that a third manager, or a change to either one, meets a graded rule" (the README, 09 and the commit use the same words).
- **Evidence.**
  - `receipts/mutants-r391-5-acmp_nvm.log` has 16 mutants: 9 are KILLED by N10/N11 and 7 pass.
  - `receipts/mutants-r391-5-survivors-pp_top-full.log`: of those 7, only `issue_arm_m1_only` fails `tb/pp_top` (D3R18). The other six pass 7,868/7,868.
  - `receipts/monitor-arbiter-inputs.txt`: 0 occurrences of any of the eight monitored input kinds with both real managers.
- **Impact.**
  - None on the product, because every one of those inputs is unreachable by the two in-tree managers.
  - But the arbiter's rules are graded for manager 1 only. Two consequences:
    - a change that lets manager 1's abort meet a READ manager 0 already *owns* (`cross_own_m1_drains_m0`) is caught nowhere, though N11b could catch it by holding the abort across that READ;
    - manager 0's halves cannot be graded while manager 0 is always the real binding manager.
  - The 09 row reads as if the whole "own manager's READ only" rule were graded.
- **Suggested outcome.** One of:
  - extend N11b so that manager 1's abort is also held across the cycles manager 0 owns its READ (one harness term; it kills `cross_own_m1_drains_m0`);
  - or state in 09 and the `acmp_nvm` README that manager 0's halves, and manager 1's abort during manager 0's owned READ, are ungraded because they are unreachable.

  Either way, carry the accurate list into the pin-adoption record, rather than "one input".
- **Verification.** `scripts/run_r391_5.sh ... acmp cross_own_m1_drains_m0` fails the extended N11b, or the text names the six inputs.

### S2 - SUGGESTION - Tests (parent harness; the pin-adoption lane) - the moved `[AECP-WTMO]` arm no longer precedes the word-36 check, and two harness comments describe the old order

- **Where.** The scratch `sim_nxn.cpp` after `parent_edits.py`, at `13eda870`:
  - `:2484` is the arm's new place, after `grade_the_first_descriptors_on_the_wire()`;
  - `:2609-2610` is "the response buffer reports no fault (word 36)";
  - the comments at `:2547-2549` ("parked in S_BAD with FAULT_TIMEOUT from the two sections above") and `:2560-2562` ("[AECP-WTMO] already moved the error counter").
- **Evidence.** At base, the word-36 check ran after the wedge-and-heal, so it also showed that the response master's fault clears after a heal. It now runs before the wedge. Every other check in that section is a delta and is unaffected: `receipts/parent/13eda870-headedits-dp-*.log` pass.
- **Impact.** Small. The heal is still graded in three places:
  - the arm's own SUCCESS heal, in every leg;
  - pp_shadow `[N]`;
  - the processor's `tb/resp_buf` R10, "it heals on the next response with no reset".

  This is a scratch edit. The pin-adoption lane owns the real change.
- **Suggested outcome.** In the real edit, re-read word 36 after the arm, or leave the arm where it is and add a word-36 read to its heal. Refresh the two comments.

## Items of this round

| Item (5883464746) | Result | Evidence |
|---|---|---|
| 1. `ax1x1gptp` under the `PP_CTRL[1]` obligation, outside the consumer set; edit in `parent_edits.py`; `make ax1x1gptp` measured | **met** | PR body round 5; `parent_edits.py` `sim_ax1x1gptp.cpp` edit; `ax1x1gptp` 139/139 at `13eda870` (`receipts/parent/13eda870-headedits-dp-ax1x1gptp.log`) |
| 2. The timed `notify` leg keeps its 6 `[AECP-WTMO]` checks; the degrade arm's retirement is stated | **met** | `notify` 378/378 with 6 WTMO, `nxn` 1,841/1,841 with 6; base 381 (6 + 5); PR body |
| 3. N11a-c; the four named reviewer mutants and `owned_arm_write_too` KILLED with README rows; STOP not triggered | **met** | `d3_mutants.py` 81/81; `tb/acmp_nvm` 359/359; README counts equal the run; residue in S1 |
| 4. R390-4 S2 (a) CLOSED named, (c) `wr_chg_o` no-connect | **met** | `main` 234/234 naming CLOSED; lint 85 vs base 84, 0 PINMISSING; `nvm_cosim` 315/315 |
| No RTL change | **confirmed** | empty `hdl/`, `syn/`, `scripts/`, `.github/` diff; sweep identical to round 4 |

## Hosted evidence (read-only)

Workflow `hdl` ran at the exact head:
- on `push`, run 36527608601;
- on `pull_request`, run 36527612913.

Both completed with success. Six jobs executed, and none were skipped: `docs-gates`, `portability` and `suites`, once in each run (`receipts/hosted-check-runs-head.txt`). The manager owns hosted and act acceptance.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-5 assignment items 1-4 and STOP. §5.1 and §8.1 against the declared parent edits: `ax1x1gptp` walk placement (`sim_ax1x1gptp.cpp:671-680, 932, 994`); the `sim_nxn` image arm; image-less CLOSED. The PR body's consolidated list and firmware note against `13eda870` (`nvm_boot()` early return, 3,000 ms). The arbiter banner (`KL_pp_nvm_mgr_arb.sv:38-65`) against N11 | R391-5 | 9dce84ea60857de74457f74b5bf08d89bd3ba408 |
| RTL | CLEAN | No RTL change (`hdl/`, `syn/` diff empty since `84572585`). The arbiter's arm terms (`:153-170`) re-read for the author's claim. Binding-manager abort reachability (`KL_acmp_nvm_shadow.sv:563-595`); writer abort only in a stalled `W_RD` (`KL_aecp_nvm_writer.sv:471-480, 534, 691-697, 1095`) | R391-5 | 9dce84ea60857de74457f74b5bf08d89bd3ba408 |
| Robustness | CLEAN | Arbiter-input monitor: 0 of 8 unreachable input kinds with the real managers over `tb/pp_top` (7,868 checks) and the 17,406-run aggregate sweep (0 BAD, identical to round 4). Parent legs at `13eda870` | R391-5 | 9dce84ea60857de74457f74b5bf08d89bd3ba408 |
| Tests | CLEAN (S1, S2 suggestions) | N11a-c code and wrap taps. `tb/acmp_nvm` 359/359; `tb/pp_top` default 7,868/7,868. In-tree `d3_mutants.py` 81/81, goldens PASS, README counts = run. My 16 arbiter mutants: 9 KILLED in `acmp_nvm`, plus `issue_arm_m1_only` by D3R18; 6 unreachable-input survivors (S1). Parent at `13eda870` with the edits: `notify` 378, `nxn` 1,841, `main` 234, `nvm_cosim` 315, lint 85/0 PINMISSING, `ax1x1gptp` 139/139 | R391-5 | 9dce84ea60857de74457f74b5bf08d89bd3ba408 |
| Docs | CLEAN (S1 suggestion) | 09 §8.2 row `:192` and the 81 count; the `acmp_nvm` README (359, N11a-c, the nine-row mutation record) and the `pp_top` README (81); the d3_mutants docstring. PR body round 5 and the consolidated list. `make check` rc 0, `gen_matrix.py --check` rc 0, `git diff --check` rc 0 | R391-5 | 9dce84ea60857de74457f74b5bf08d89bd3ba408 |

## Real limits

- **Simulator.** The named path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host.
  - I used a copy of the byte-identical sibling wrapper (sha256 `905795b9...`, identical across all 186 sibling wrappers).
  - It runs a binary with sha256 `fb2cc573...` that reports `Verilator 5.050 2026-07-01 rev v5.050` (`receipts/verilator-identity.txt`), the same identity as rounds 1-4.
- **Not run:**
  - the full processor bank (`run_suites.sh` over 33 suites), full `lint_hdl.sh`, Yosys, `srp_top` mutants, `nvm_port` figures. There is no `hdl/` change since round 4, where I linted the touched modules;
  - the D1 probe, whose inputs are unchanged. The sweep is identical;
  - any builder, gPTP or Yosys bank; xvlog;
  - the manager's 16-command consumer set as such. I ran only `notify`, `nxn` and `main` (two of them through scratch-only make targets that reuse the recipe's own lines), plus `nvm_cosim` lint and quick, and `ax1x1gptp`. Not run: `nolpf`, `ax1x1`, `aclk`, `nxndv`, `nxn8`, `nxn4c`, `gmstep`, `gptp`, `gptp-lat`, both `milan_dp` mutation campaigns, pp_shadow, `milan_dp_render`, the static gates and `milan_dp_gptp`'s `verify_abort.py`;
  - `ax1x1gptp` without the edit. The author's 15/137 at `84572585` is not reproduced.
- **DR4 not re-measured.** There is no RTL change, and the instrument is not on this host.
- **Parent copies.** `--shared` local clones of public milan-fpga at live dev `13eda870`:
  - `protocol-processor` at the head, or at the base for the reference `notify` and lint;
  - `gptp-processor` and `third_party/verilog-axis` at the parent's gitlinks, from their public remotes;
  - `external` not fetched.

  The only edits are the author's `parent_edits.py` (sha256 recorded) and two scratch-only make targets (`receipts/parent/13eda870-headedits-milan_dp-Makefile.txt`).
- **Simulation only.** The sweep overrides `NVM_RS_AGG_CYC_P` to 2,800 in disposable copies. The monitor is a print-only planted edit. Physical calibration was NOT RUN, field skips are not hardware proof, and nothing here is hardware proof.
- **Runtime.** Two jobs outlived this session's per-command limit and finished detached: the in-tree campaign, and `ax1x1gptp`. I read their logs to completion. Neither was a full bank.
- **Clone hygiene.** Every build, probe and mutant ran on `git archive` exports or `--shared` clones under this packet's `scratch/`. At the end:
  - HEAD, the tree and the index agree;
  - all 312 work-tree blobs rehash to their tree blobs, and the modes match;
  - status, ignored files included, is empty;
  - there are no gitlinks and no `.gitmodules`, so no submodule gitlinks are required (`receipts/clone-integrity.txt`).

## Pending manager duties

- Consider S1 (an N11b extension or a precise statement) and S2 (for the pin-adoption lane).
- Run the donor full bank and the patched parent consumer bank at dev `13eda870` (the 16 commands), plus `milan_dp_gptp`.
- Build the final current-dev candidate at the merge turn (source base `c951a9ff`).
- Carry into the pin-adoption lane:
  - the consolidated list, including `ax1x1gptp`;
  - the firmware persistence-disabled boot path with its host test;
  - S2.
- Adjudicate R390-3-S2, which is still unruled.
- Own hosted and act acceptance, and record that physical calibration is NOT RUN.

## Prior public findings, resolved or retained at this head

These were read after the verdict, findings and ledger above were fixed. R390-5 is concurrent and was not read.

| Finding | Status at 9dce84ea | Evidence |
|---|---|---|
| R391-4 F1 MINOR, the declared `sim_nxn.cpp` edit drops `[AECP-WTMO]` from `notify`, and the degrade arm's retirement is unstated | **Resolved** | `notify` 378/378 with 6 WTMO at `13eda870`; the body states the retirement (5 → 2). The side effect is S2 |
| R391-4 S1, pin the arbiter's own contract | **Taken** (N11a-c). Residue is S1 of this report | 81/81; my three round-4 survivors KILLED |
| R390-4 F1 MINOR, `ax1x1gptp` missing from the `PP_CTRL[1]` obligation | **Resolved** | PR body; `parent_edits.py`; `ax1x1gptp` 139/139 at `13eda870` (`receipts/parent/13eda870-headedits-dp-ax1x1gptp.log`) |
| R390-4 S1, issue-cycle cross intent and ignored `we` | **Taken** | `issue_arm_cross_intent` KILLED by N11b, `issue_arm_ignores_we` by N11a |
| R390-4 S2 (a) name CLOSED, (b) timed WTMO, (c) `wr_chg_o` lint | **Taken** | `main` 234/234 naming CLOSED; (b) as R391-4 F1; lint 85 vs 84 |
| R390-3-S2, D3R15's re-LOCATE arm; asks for a manager confirmation | **Open for the manager, unchanged** | not ruled in round 5; RTL and D3R15 unchanged |
| R390-2-S1, no `RX_SLOTS_P >= 2` floor | **Not taken (not assigned)** | `hdl/` unchanged |
| Earlier R390 and R391 findings (rounds 1-3) | stay **resolved or taken** | no `hdl/` change since round 4. `tb/pp_top` 7,868/7,868 and `d3_mutants.py` 81/81 include all their controls |

## Receipts and reproduction

Every file below is listed in `MANIFEST.sha256`.

**Scripts** (`scripts/`). They take a processor checkout, a revision, a scratch directory and a directory holding a Verilator 5.050 `verilator`. None of them writes into the checkout.

- `run_r391_5.sh <checkout> <rev> <scratch> <verilator dir> <probe> [args]` runs these probes:
  - `acmp [MUTANT]`: `tb/acmp_nvm` `make run`;
  - `full [MUTANT]`: the `tb/pp_top` default build;
  - `d3 [MUTANT]`: `tb/pp_top` `--d3-only`;
  - `sweep AGG STEP SCENS [MUTANT]`: the aggregate sweep, `r391_4_sweep.hpp`, run as `sweep 2800 1 0,1`, then `2,3`, then `4,5`;
  - `d1`: `r391_4_d1.hpp`.
- `r391_5_mutants.py` holds my 16 arbiter mutants and the print-only monitor `mon_unreachable_inputs`.
- `parent_scratch.sh <parent clone> <parent rev> <checkout> <rev> <scratch> <verilator dir> <name> <edits|none> <target>` builds a scratch parent and runs one target. It needs `GPTP` and `VAXIS`.
- `check_readme_counts.py <checkout> <results.json>` checks the README counts against a campaign's results.
- `summarize_monitor.py LABEL=LOG ...` tallies the monitor's lines.
- The in-tree campaign ran as `python3 tb/pp_top/d3_mutants.py --output DIR --verilator V --jobs 6` from a `git archive` export, with builds at `-j 2`.

**Receipts** (`receipts/`).

- **Suites:**
  - `suite-acmp_nvm-head.log` (359);
  - `suite-pp_top-default-head.log` (7,868).
- **Mutants:**
  - `d3_mutants-intree.log` and `d3_mutants-intree-results.json` (81/81);
  - `readme-counts-vs-run.txt`;
  - `mutants-r391-5-acmp_nvm.log` (16);
  - `mutants-r391-5-survivors-pp_top-full.log`.
- **Probes:**
  - `monitor-arbiter-inputs.txt` and `monitor-acmp_nvm-run.log`;
  - `probe-P9-aggsweep-head-with-monitor.log`.
- **Parent** (`parent/`):
  - `13eda870-headedits-dp-{notify,r391-main,r391-nxn,ax1x1gptp}.log`;
  - `13eda870-headedits-cosim-{lint,quick}.log`;
  - `13eda870-base-dp-notify.log` and `13eda870-base-cosim-lint.log`;
  - `13eda870-headedits-parent.diff`, `13eda870-headedits-gitlink.txt` and `13eda870-headedits-milan_dp-Makefile.txt`;
  - `author-r5-parent_edits.sha256`.
- **Gates and environment:**
  - `make-check-head.log`, `gen-matrix-check-head.log` and `diff-check-head.txt`;
  - `hosted-check-runs-head.txt`, `clone-integrity.txt` and `verilator-identity.txt`.

R391-5 FINISHED
