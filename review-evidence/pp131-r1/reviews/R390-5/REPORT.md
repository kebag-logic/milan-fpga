[R390] NEGATIVE - exact head 9dce84ea60857de74457f74b5bf08d89bd3ba408

# R390-5: independent internal review of processor PR #132 (issue #131, D3 lane 1), round 5

| | |
|---|---|
| Head / tree | `9dce84ea60857de74457f74b5bf08d89bd3ba408` / `1601ef9ed9db2995b73acf8c625f955e5e8c6315` (verified in the review clone) |
| Delta reviewed | `84572585..9dce84ea` (one test commit, `9dce84e`), the PR body's Round 5 section and consolidated parent-visible list, and the author's round-5 `parent_edits.py` (public archive `kebag-logic/milan-fpga` branch `pp131-review-evidence` at `fab7ca16`, `review-evidence/pp131-r1/author-r5/`) |
| Assignment | processor #131 comment 5883464746 (round 5); review start 5884450356 |
| Verdict | **NEGATIVE**: one MINOR (Tests, Docs) is open. Conformance, RTL and Robustness are CLEAN. Every round-4 finding and suggestion is resolved or taken (section 4). |

## 1. How the review was reconstructed

- **Scope.** The repository has no `AGENTS.md` or `CONTRIBUTING.md`. I read `docs/README.md` (conventions, single-source rules), the issue body (contract section 18.1 at parent `7a7582f0`, DR1a-DR6, DR2c-carrier), and every manager comment on #131: the rulings 5868716919 and 5873580386, the round assignments, and round 5 (5883464746). I also read the manager's bank comment 5880274287 on #132.
- **Authority for the arbiter.** Parent `docs/design/SAVED_STATE_MATERIALIZATION.md` at `7a7582f0`: section 6.4, lines 797-808 (the drain equation) and 820-835, and the section 15 port row (line 535). The round-4 ruling (5880658258 item 1) adds the issue-cycle arm.
- **Diff and history.** `git diff 84572585..9dce84ea`: `tb/acmp_nvm/{sim_main.cpp, acmp_nvm_wrap.sv, README.md}`, `tb/pp_top/{d3_mutants.py, README.md}`, `docs/architecture/09_verification.md`. `git diff --quiet 84572585..HEAD -- hdl syn scripts .github Makefile` is true, so **no RTL changed**. The whole-lane diff from `c951a9ff` was reviewed in rounds 1-4. This round re-reads only the arbiter (`KL_pp_nvm_mgr_arb.sv`, unchanged) that N11 grades.
- **Parent.** A public clone at live dev `13eda870` (first parent `eaa88a32`, the author's measurement base), used read-only for facts. The author's `parent_edits.py` was applied to a disposable copy under `scratch/`.
- **Public evidence.**
  - `review-evidence/pp131-r1` at `b657a2de`, which is the round-1 author packet.
  - The round-5 author archive named above: receipts `milan_dp_gptp-9dce84e.txt`, `ax1x1gptp-84572585.txt`, `r391-4-parent-notify-9dce84e.txt` and `parent-edits.diff`.
  - The manager's comments.
- **Prior findings.** I read the prior public findings (R390-4 and R391-4) only after my independent pass. That pass is recorded in `receipts/independent-verdict-before-prior-findings.txt`, timestamped before the reading. I did not read the concurrent R391-5 review.
- **Tool.** The assigned wrapper `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. I used `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator` instead: Verilator 5.050, rev v5.050, wrapper sha256 `905795b9...`. It is byte-identical to all 186 pinned wrappers under `$VALIDATION_STORAGE/*/pinned-tool-bin` (`receipts/tool-identity.txt`).

## 2. Findings

### R390-5-F1: MINOR. The owned half of "an abort drains only its own manager's READ" is ungraded, though the bench can present it; 09 and the author's limit statement claim otherwise

- **Lenses:** Tests, Docs.
- **Where:**
  - `docs/architecture/09_verification.md:192`: "the arbiter's own contract for inputs neither in-tree manager presents: ... an abort drains only its own manager's READ ..." is graded by "`tb/acmp_nvm` N11a, N11b, N11c".
  - `tb/acmp_nvm/README.md:220-222`, and the banner comment at `tb/acmp_nvm/sim_main.cpp:2592-2594`: "**N11b** an abort names its own manager's READ only". The check body drives the abort only in the issue cycle: `sim_main.cpp:650`, `m1_abort_on_m0 && d->mgr_req_o && !d->mgr_we_o`, and `:2621-2636`.
  - The author's REVIEW READY statement (#131 5884424686): "One arbiter input stays ungraded in the tree, by construction: a manager-1 grant while manager 0 presents an abort."
- **Authority:**
  - Contract section 6.4, lines 803-804, gives the drain as owner-matched: `drain' = ... (owner = writer AND m_abort) OR (owner = binding AND m0_abort)`. The section 15 port row (line 535) says "Either abort abandons the READ the port serves for **that** manager".
  - The arbiter implements the same pairing: `KL_pp_nvm_mgr_arb.sv:157-160`, `(own_r == O_M0) && !we_r && m0_abort_i`, and its banner at `:38-46`.
  - The purpose of the round-5 item 3 arms, as the assignment states it (from R391-4 S1): a third manager, or a change to either manager, should meet a graded rule.
- **Evidence (executed; receipts `r5-extra/`, `r5-extra-full/`, `r5-owned-probe/`, `arb-unit-r5.txt`; scripts `r5_extra_mutants.py`, `r5_owned_cross_probe.py`, `run_arb_unit_mutants.py`):**

  | Arbiter edit (reviewer's) | `tb/acmp_nvm` (359) | `tb/pp_top --d3-only` (133) | `tb/pp_top make run` (7,888) | my R390-4 unit probe (9) |
  |---|---|---|---|---|
  | `r5_owned_cross_m0_only`: manager 1's abort drains manager 0's **owned** READ | passes | passes | passes | passes |
  | `r5_owned_cross_m1_only`: manager 0's abort drains manager 1's owned READ | passes | passes | passes | passes |
  | `r5_issue_cross_m1_only`: manager 0's abort in manager 1's **issue** cycle (the author's stated gap) | passes | passes | passes | fails case F |
  | `r5_issue_cross_m0_only`: manager 1's abort in manager 0's issue cycle | **KILLED** by N11b | passes | not run | fails E, G |

  - **The owned m0 case can be presented in-tree, and presenting it grades it.** The disposable check R5P (`r5_owned_cross_probe.py`, about 20 harness lines in an isolated copy) holds manager 1's abort from each walk READ's strobe to that READ's end. At the head it passes, 360 of 360; the abort was present in owned cycles, which the check requires as proof it is not vacuous. Under `r5_owned_cross_m0_only` it fails: the first READ is drained, and "the walk is not done, or failed".
  - **So the author's statement is correct for the input it names, but incomplete.** Manager 0 is the real binding manager and raises its abort only while it owns or strobes its own READ. Both manager-0-abort cases are therefore unreachable in every in-tree bench: the issue-cycle grant the author names, and manager 0's abort while manager 1 owns a READ, which the author does not name. The owned manager-1 case is different: `tb/acmp_nvm`'s synthetic manager 1 can present it, as R5P shows, and nothing grades it.
  - Both by-construction cases are stated only in the author's issue comment, not in the tree.
  - **This gap predates the round**, and my own R390-4 S1 and unit probe scoped the cross rule to the issue cycle. It is a finding now because this delta adds the 09 row and the N11b heading, which claim the whole rule as graded.
- **Impact:** The RTL is correct (section 3), so there is no functional defect today. But the verification document of record states that the owner-matched drain is graded, and a regression that breaks the owned half would pass every processor suite. A third manager or a changed D3 writer that raises its abort while the other manager owns a READ would drain the wrong manager's READ. The binding walk would then fail whole, exactly the R5P mutant reading, and nothing in the tree would flag it.
- **Required outcome:** One of:
  - **(preferred)** A named `tb/acmp_nvm` check in which manager 1's abort is held through manager 0's owned READs (for example an N11b arm or an N11d), with a non-vacuity count. Add an `owned_arm_cross_intent`-style mutant (the owned term takes the other manager's abort) to `d3_mutants.py` with a README row, KILLED.
  - **or** narrow the claims to what is graded: the 09 row and the N11b heading say "in its issue cycle". Then the `tb/acmp_nvm` README states the ungraded arbiter inputs and why.

  In either case, the `tb/acmp_nvm` README records the two inputs that stay ungraded by construction: manager 0's abort in manager 1's grant cycle, and manager 0's abort while manager 1 owns a READ. It names the out-of-tree probe that covers the first.
- **Verification:**
  - `r5_extra_mutants.py --suites acmp_nvm --only r5_owned_cross_m0_only`: KILLED by the new named check, with the golden passing. Or, under the narrowing option, the 09 row and README read against this finding.
  - `d3_mutants.py` all KILLED, with README counts equal to the run.

### Suggestions (they do not affect the verdict)

- **R390-2-S1 (RTL, Docs), carried:** No `RX_SLOTS_P >= 2` floor is checked or stated (`protocol_processor_top.sv:86`, unchanged).

## 3. Round-5 assignment items verified

| Item | Result | Evidence |
|---|---|---|
| **(1) R390-4 F1: `ax1x1gptp` under the `PP_CTRL[1]` obligation** | **resolved** | Details below |
| **(2) R391-4 F1: the timed leg keeps the wedged-memory arm; the degrade arm's retirement declared** | **resolved** | Details below |
| **(3) `9dce84e`: N11a-c and the five new controls** | **N11a-c correct, and the five new controls KILLED; the author's ungraded-input statement is incomplete (F1)** | Details below |
| **(4) R390-4 S2 refinements** | **taken** | Details below |
| **No RTL change** | **confirmed** | `git diff --quiet 84572585..HEAD -- hdl syn scripts .github Makefile`. The only changes are to `tb/` and `docs/`. |

**Item (1) detail.**
- **The PR body.** Round 5 item 1 and the consolidated list (`PP_CTRL[1]` bullet 2) name `sim_ax1x1gptp.cpp`, `milan_dp` `ax1x1gptp`, run nightly by `milan_dp_gptp`. They state that it is outside the consumer set and give the measurement.
- **The edit.** `parent_edits.py` starts the walk at the top of `configure()`, which follows every `reset()` (`sim_ax1x1gptp.cpp:643-671` at `13eda870`). The image is loaded at start-up (`:918`). The edit asserts done (`PP_STAT[2]`), not "either terminal", which is right for an image-served boot.
- **Author receipts, cross-checked.**
  - With the edit: 139/0, `wall_clock_seconds=3251.88`. The body's 3,277 s is the whole make step (`rc 0 seconds 3277.1`). `verify_abort.py` passes 6 + 20 + 14 = 40.
  - Without the edit (at `84572585`): 137 checks, 15 failures, every GET_AVB_INFO and GET_AS_PATH check. Adding 556 s for `verify_abort.py`, the nightly suite totals about 3,833 s, inside its 5,400 s budget.
- **#609.** `eaa88a32..13eda870` touches no `milan_dp`, `milan_dp_gptp`, `milan_dp_render`, `pp_shadow` or HDL file (`receipts/parent-facts-13eda870.txt`), so the `eaa88a32` measurement's inputs are unchanged at live dev, apart from the gitlink.
- **The harness survey at `13eda870`.** No other `milan_dp` harness speaks AECP without starting the walk or being edited. `crflic` and `prune` send no AECP. `option-off` reuses `sim_main.cpp`, whose edit is file-level. `fw_service_budget`'s suite target is `run.py --self-test` only.

**Item (2) detail.**
- **The edit.** The published edit places `prove_a_wedged_response_memory_reports_and_heals()` after `grade_the_first_descriptors_on_the_wire()`, before the `#ifdef NOTIFY_TIMED_TB` return, in every leg. It calls `prove_aecp_is_held_until_the_restore()` in place of the degrade arm.
- **At `13eda870`.** The WTMO arm has 6 checks (`sim_nxn.cpp:2398-2440`) and the degrade arm 5 (`:2359-2380`). The published `r391-4-parent-notify-9dce84e.txt` reads 378 checks, 0 failures.
- **The PR body.** It states the degrade arm's retirement in every `sim_nxn` leg, with its reason (section 8.1: AECP held from reset, and CLOSED keeps it held), and the two replacing hold checks.

**Item (3) detail.**
- **N11 read against the banner and section 6.4.** The three arms are correct, and they are not vacuous:
  - **N11a.** The abort is held across the strobe and every owned cycle (`sim_main.cpp:650-651`). The check requires a commit issue, no drain, every byte, done without err, and the record byte-exact with one ERASE and one WRITE. `issue_arm_ignores_we`, `issue_arm_write_too`, `issue_arm_stale_we` and `owned_arm_write_too` fail it.
  - **N11b.** The monitor requires 8 of 8 walk READ issues to carry manager 1's abort (`:759-762`).
  - **N11c.** It requires `drain_on == issued + 1` after a completed WRITE (`we_r` still 1), so only the issue term can satisfy it. `issue_arm_stale_we` fails it.
- **The wrap taps** (`acmp_nvm_wrap.sv:541-544`) are the arbiter's `p_req_o`/`p_we_o` and manager 0's `m0_req_i`/`m0_we_i`.
- **N1-N10 are unchanged in effect.** `m1_we` defaults to 0, and `m1_abandoned` gains `&& !m1_we_i` only. Base `84572585` runs 355/355; the head runs 359/359, +4 = N11a 1, N11b 1, N11c 2. The warning set is identical (13).
- **The mutation campaign, run by me from the tree** (`receipts/d3-*`): **81 of 81 KILLED**, all goldens PASS, in four batches (acmp_nvm 9; pp_top/rx_validator 36 + 18 + 18). Every failing-check count equals its README row: `drain_misses_issue_cycle_m1` 4, `issue_arm_stale_we` 3, the four other N11 controls 1 each, and all 72 others as documented.
- **The author's statement** that a manager-1 grant while manager 0 presents an abort stays ungraded by construction: **true for that input.** My R390-4 unit probe (carried in `scripts/arb_unit/`) kills it in case F and passes 9/9 at the head. **Incomplete:** see F1.

**Item (4) detail.**
- **(a)** `sim_main.cpp` and `sim_aclk.cpp` now assert CLOSED strictly: the busy 0, done 0, fail 1 predicate, with the check named for CLOSED.
- **(b)** This is item (2).
- **(c)** `wr_chg_o` goes to `wr_chg_nc_w`, matching `cosim_top.sv:177-185`'s `*_nc_w` convention (`cfg_nc_w`, `wr_nc_w` and others).
- **Applies at live dev.** `parent_edits.py` applies cleanly to parent `13eda870`, every exact text once, and its changed lines are identical to the author's published `parent-edits.diff` (`receipts/parent-edits-apply-13eda870.txt`).

## 4. Prior public findings, resolved or retained at this head

| Finding | Status | Basis |
|---|---|---|
| R390-4-F1 (MINOR, `ax1x1gptp` missing from the list) | **RESOLVED** | Section 3, item (1) |
| R390-4-S1 (arbiter cross and WRITE rules ungraded) | **TAKEN** for the issue cycle; the owned half is F1 | Section 3, item (3) |
| R390-4-S2 (a)-(c) | **TAKEN** | Section 3, item (4) |
| R390-3-S2 (a bound inside a healthy re-LOCATE ends CLOSED) | stated in the docs; the manager's ruling is still open | not in the round-5 assignment |
| R390-2-S1 (`RX_SLOTS_P` floor) | not taken; carried | unchanged |
| R390-1…R390-3 findings | **still RESOLVED** | their controls are among the 81 KILLED |
| R391-4 F1 (MINOR, WTMO lost from `notify`; degrade retirement undeclared) | **RESOLVED** | Section 3, item (2) |
| R391-4 S1 (three arbiter-contract arms) | **TAKEN** | N11a-c; `issue_arm_write_too`, `issue_arm_cross_intent` and `issue_arm_stale_we` KILLED |
| R391-1…R391-3 findings | **still RESOLVED** | their controls are among the 81 KILLED; `pp_top` 7,888/7,888 |

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | N11a-c against contract 6.4 (797-808, 820-835), the line-535 port row, the round-4 issue-cycle ruling and the arbiter banner. Parent edits against 8.1 and the hold-admission ruling. Firmware `nvm_boot()` persistence-disabled path unchanged at `13eda870` (still declared). | R390-5 | `9dce84ea60857de74457f74b5bf08d89bd3ba408` |
| RTL | CLEAN | No `hdl/` change. `KL_pp_nvm_mgr_arb.sv` re-read: the owned and issue terms are owner-matched and READ-only. The four wrap taps map to the right nets. | R390-5 | `9dce84ea60857de74457f74b5bf08d89bd3ba408` |
| Robustness | CLEAN | N11 waits are bounded (`run_until` 200 and 4000). Under every mutant the run completes with its tally, with no hang or crash across 81 + 14 + 3 mutant runs. Same warnings as base. | R390-5 | `9dce84ea60857de74457f74b5bf08d89bd3ba408` |
| Tests | **UNCLEAN (F1)** | `acmp_nvm` 359/359; `pp_top make run` 7,888/7,888 (D3 133); `d3_mutants.py` 81/81 with README equality; 6 reviewer arbiter edits × 3 suites; R5P probe; R390-4 unit probe 9/9; base-round comparison 355 → 359 | R390-5 | `9dce84ea60857de74457f74b5bf08d89bd3ba408` |
| Docs | **UNCLEAN (F1)** | 09 section 8.2 row and counts (81), `acmp_nvm` README (359, N11 text, mutation table), `pp_top` README (81). PR body Round 5 and the consolidated list against the parent at `13eda870` and the published edit script. `make check` rc 0; `git diff --check c951a9ff..HEAD` rc 0. | R390-5 | `9dce84ea60857de74457f74b5bf08d89bd3ba408` |

## 6. Real limits of this review

- **Parent benches not run by me.**
  - `milan_dp_gptp` / `ax1x1gptp` (about 55 min), the `milan_dp` pool legs, `pp_shadow`, `nvm_cosim` and `milan_dp_render`. These are the manager's patched consumer bank, outside what this review may run.
  - For those I rely on the author's published receipts (read, not reproduced), the parent source facts at `13eda870`, and the edit script applying cleanly there.
- **Physical calibration NOT RUN.** Field skips are not hardware proof. No hardware, Docker or act was used.
- **Firmware-driven full-SoC measurement harnesses were not assessed for re-measurement.**
  - These are `nvm_capture_cpu` and the full `fw_service_budget` run: product firmware on the SoC, outside CI.
  - The firmware starts the walk, so the `PP_CTRL[1]` obligation does not apply to them.
  - The added D3 walk and D3 record traffic may move their recorded numbers at pin adoption. That belongs to the pin-adoption lane and is not a finding here.
- **Hosted checks at `9dce84ea`.**
  - The workflow `hdl` ran twice (push 36527608601, pull_request 36527612913). In both, `docs-gates` and `portability` completed successfully.
  - `suites` was still **in progress** in both at my last poll (06:26 UTC) (`receipts/hosted-checks.tsv`). No hosted suite result is claimed.
- **Tool path.** The assigned wrapper path was absent; an identical 5.050 wrapper was used (section 1).

## 7. Pending manager duties

- **Adjudicate F1**, either option in its required outcome. A test and doc change; no RTL.
- **The patched parent consumer bank** at dev `13eda870` with the regenerated `parent_edits.py`, the 16 commands. Plus `milan_dp_gptp` (`ax1x1gptp`, outside the 16), whose last measurement is the author's at `eaa88a32`. #609 changes none of its inputs besides the gitlink.
- **The hosted `suites` job** at `9dce84ea`, and hosted/act acceptance.
- **The final current-dev candidate** build at the merge turn (source base `c951a9ff`, live dev `13eda870`).
- **Still open:** the R390-3-S2 ruling (a bound inside a healthy re-LOCATE ends CLOSED with the pass-1 cause). The firmware persistence-disabled boot path is declared for the pin-adoption lane.

## 8. Receipts and reproduction

- **Scripts.** `scripts/r5_extra_mutants.py` (reviewer arbiter edits over the tree's own `d3_mutants.judge`), `scripts/r5_owned_cross_probe.py` (the R5P check, in an isolated copy), `scripts/run_arb_unit_mutants.py` and `scripts/arb_unit/` (the unit probe carried from R390-4).
- **Commands.** Run from the review clone with `TMPDIR` under `scratch/`, 8 jobs or fewer, in the foreground:
  - `python3 tb/pp_top/d3_mutants.py --output <dir> --verilator <v> --jobs 8 [--only ...]`
  - `python3 <packet>/scripts/r5_extra_mutants.py --tree . --output <dir> --verilator <v> [--suites acmp_nvm pp_top pp_top_full]`
  - `python3 <packet>/scripts/r5_owned_cross_probe.py --tree . --output <dir> --verilator <v>`
- **Receipts.** `receipts/d3-acmp_nvm`, `d3-batch1`, `d3-batch2a`, `d3-batch2b`, `r5-extra`, `r5-extra-full`, `r5-owned-probe`, `arb-unit-r5.txt`, `base84-acmp_nvm.log`, `make-check.txt`, `diff-check.txt`, `hosted-checks.tsv`, `parent-facts-13eda870.txt`, `parent-edits-apply-13eda870.txt`, `tool-identity.txt`, `clone-integrity.txt`, `independent-verdict-before-prior-findings.txt`. Private tool paths are redacted to `<pinned-tool-root>`.
- **Clone restored.** After the probes, the tree is `1601ef9e`, the index equals the tree (312 files, modes and blob ids), there are no untracked or ignored entries, and the repository has no gitlinks. The two ignored artifacts my runs created (`.venv-wavedrom/`, `tb/pp_top/__pycache__/`) were removed (`receipts/clone-integrity.txt`).

R390-5 FINISHED
