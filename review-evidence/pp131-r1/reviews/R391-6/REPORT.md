[R391] POSITIVE - exact head 9b4da6b5753fec8f5b2bba605c47af56c6cf1a0f

# R391-6: independent external review of processor PR #132 (issue #131, D3 lane 1), round 6

- **Repository.** Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #132, issue #131, round R391-6.
- **Head.** Exact head `9b4da6b5753fec8f5b2bba605c47af56c6cf1a0f`, tree `ec8876e6c9d1670a745bc0ffd00134d6ddcfea92`. The live PR head reads the same sha. Base `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`.
- **Delta reviewed.** `9dce84ea..9b4da6b5` is one commit, `9b4da6b`: 6 files, +142 / -26, all under `tb/` and `docs/`.
  - Tests: `tb/acmp_nvm` N11d (`sim_main.cpp`), the wrap tap `arb_end_o` (`acmp_nvm_wrap.sv`), and two new controls in `tb/pp_top/d3_mutants.py`.
  - Docs: the 09 §8.2 row and the 83 count; the `tb/acmp_nvm` README (N11a-d, the ungraded-by-construction list, the mutation record) and the `tb/pp_top` README count.
  - Also reviewed: the PR body's Round 6 section and the consolidated parent-visible list, and the public round-6 author packet (milan-fpga branch `pp131-review-evidence` at `3ad574a4`, `author-r6`), whose `parent_edits.py` is byte-identical to round 5's (sha256 `80d2c396...`).
- **No RTL change.** `git diff --quiet 9dce84ea 9b4da6b5 -- hdl syn scripts .github Makefile` returns 0.
- **Authorities.**
  - The round-6 assignment (issue #131, 5885497133): items 1-3, the gates, and "No RTL change".
  - The arbiter's banner and arm terms (`hdl/packet_engine/KL_pp_nvm_mgr_arb.sv:20-65`, `:147-151`).
  - The binding manager's abort and walk (`hdl/acmp/KL_acmp_nvm_shadow.sv:547-576`, `:733-770`); the D3 writer's aggregate and commit (`hdl/aecp/KL_aecp_nvm_writer.sv:562`, `:1090`).
  - My round-5 S1 and S2 (PR #132 comment 5885492313), which are the subject of this round.
- **Reconstruction order.**
  1. Processor README, docs/README and 09. There is still no AGENTS.md or CONTRIBUTING.md.
  2. Issue #131 through the round-6 assignment, the author's TAKEN (5885505757) and REVIEW READY (5886545587), the PR body (rounds 1-6), and the review-start comment 5887943588.
  3. The authorities above.
  4. `git diff c951a9ff..9b4da6b5` and its history, then the round-6 commit in full.
  5. Public evidence:
     - milan-fpga `b657a2de` `review-evidence/pp131-r1`;
     - the `author-r6` packet (`3ad574a4`);
     - the hosted check runs at the exact head.
- **Inputs from my earlier rounds.** My own round-5 packet: its scripts, its receipts and its S1 and S2. No private material was read.
- **The other reviewer.** R390-5's report was not opened before this report's verdict, findings and ledger were fixed. Its F1 was known only as the round-6 assignment and the PR body state it. R390-6 is concurrent and was not read.

## Verdict

POSITIVE. No MINOR or higher finding is open. Three SUGGESTIONs, S1-S3, do not affect the verdict.

**Item 1: N11d, the owned half of the owner-matched drain (R390-5 F1 = my R391-5 S1).** Met.

- **Stimulus** (`tb/acmp_nvm/sim_main.cpp:661`, `:693-705`, `:787-792`, `:2702-2722`).
  - N11d drives manager 1's abort only while the harness's `m0_rd_own` is set.
  - `m0_rd_own` is set in the clock the arbiter issues manager 0's READ (`arb_req_o && mgr_req_o && !mgr_we_o`), and cleared on the port's done or err (`arb_end_o`). So the abort runs from issue+1 through that READ's end, inclusive.
  - The check requires all of the following:
    - the abort in every owned clock (`m0_own_cyc_m1_abort == m0_own_cyc > 0`);
    - 8 READs ended, and at least one owned clock before each end;
    - 0 of 8 issue clocks with the abort;
    - no drain, no leak and no manager-0 abort;
    - the walk complete as saved, and the device untouched.
- **Cross-check against the arbiter's own ownership.** My print-only monitor `mon_own0_reads` reports every READ with `own_r == O_M0 && !we_r` at its `end_w` (`receipts/monitor-arbiter-9b4da6b5.txt`).
  - Over the whole `tb/acmp_nvm` run, 5,479 manager-0 READs end. Exactly 16 of them carry manager 1's abort in any clock:
    - **N11b's 8:** the abort in the issue clock only, and 0 owned clocks with it.
    - **N11d's 8:** the abort in 168 of 168 owned clocks and 0 of 8 issue clocks. At least 12 of those clocks come before each READ's end (44 for the first and the last READ). Nothing is drained.
  - That equals the author's `n11d-counts` receipt (168 / 168, min 12, 0 of 8).
  - So the harness's notion of "owned" matches the RTL's own clock for clock, and the two checks each grade one term.
- **Controls.**
  - `d3_mutants.py` over all 83 controls, run by me in six `--only` partitions of the exact-head extract: **83 of 83 KILLED**, all goldens PASS, and the driver's list equals the run's set (`receipts/d3_mutants-intree-results.json`, `receipts/d3_mutants-intree.log`).
  - `owned_arm_cross_intent` and `cross_own_m1_drains_m0` each fail exactly one check, N11d. `issue_arm_cross_intent` still fails N11b alone.
  - `check_readme_counts.py`: **86 entries, 0 problems** (83 controls and 3 goldens; `receipts/readme-counts-vs-run.txt`).
- **My round-5 scripts, re-run unchanged.** `r391_5_mutants.py`, loaded through `run_r391_6.sh`, on `tb/acmp_nvm` at the head (`receipts/mutants-r391-6-acmp_nvm.log`):
  - `cross_own_m1_drains_m0` now fails N11d (359 of 360 pass). At round 5 it passed 359 of 359.
  - Every other edit's failing count equals my round-5 receipt.
  - Six edits pass `tb/acmp_nvm` 360 of 360:
    - the five manager-0 halves: `cross_iss_m0_drains_m1`, `cross_own_m0_drains_m1`, `write_iss_m0_only`, `write_own_m0_only` and `stale_we_m0_only`;
    - `issue_arm_m1_only`, which D3R18 kills in `tb/pp_top` (round-5 receipt, `tb/pp_top` unchanged).
- **N11d's own strength (round-6 probes, `scripts/r391_6_mutants.py`).**
  - All four harness or tap weakenings fail N11d:
    - `h_n11d_no_drive`: 0 of 168;
    - `h_n11d_half_drive`: 83 of 168;
    - `h_n11d_also_issue`: the issue term;
    - `t_arb_end_stuck0`: 0 READs ended.
  - A narrower arbiter variant, `cross_own_m1_drains_m0_first_clk`, which arms only in the first owned clock, also fails N11d.
  - The issue-term failure's message misreports its count; that is S1.
- **The named script files.** `r5_extra_mutants.py` and `r5_owned_cross_probe.py` are the other reviewer's round-5 scripts, not mine. My round-5 scripts are `run_r391_5.sh`, `r391_5_mutants.py` and `check_readme_counts.py`, and I re-ran them as above. I did not run the other reviewer's scripts. The author's public receipt of them (`author-r6/receipts/r390-5-*`) is noted, not reproduced.

**Item 2: docs.** Met.

- **09 §8.2 row** (`docs/architecture/09_verification.md:192`).
  - It now names manager 1's half of each rule, each with its graded check: N11a; N11b (issue) and N11d (owned); N11c.
  - It names the manager-0 halves as ungraded by construction, and refers to the README.
  - The 83 count (`:200-201`) equals the run.
- **`tb/acmp_nvm` README** (`:213-263`, `:375-387`). It lists the five manager-0 inputs, and each row names the edit that passes every in-tree suite. All five are my R391-5 S1 edits other than `cross_own_m1_drains_m0`, which N11d now kills.
- **The README's "why" holds in the RTL.**
  - Manager 0 raises `nvm_abort_o` only as `rs_tmo_w` in `H_RS_STREAM` (`KL_acmp_nvm_shadow.sv:566-576`).
  - In its READ's issue clock, `rs_wd_r` is 0 (reset in the preceding non-stalled `H_RS_REQ` clock), so only `rs_agg_i` can raise it there. Every bench's `RS_TMO_CYC_P` is at least 3,000.
  - `H_WAIT` is entered only from `H_INIT` (`:736-770`), so the binding walk runs once per reset, and manager 0 writes only from `H_RUN`, after it (`H_FL_REQ`, `:906-912`).
  - Manager 1 writes only once `done_r` is set (`KL_aecp_nvm_writer.sv:1090`), and the aggregate is live only while `!done_r` (`:562`).
  - So no aggregate expiry follows any WRITE: "both managers only read" there is true.
- **The README's probe attributions.**
  - To my own monitor: `m0_abort_on_m1`, `m0_abort_with_write` and `m0_issue_abort_after_write` are its kinds. It still sees none of them with both real managers over the whole `tb/pp_top` default run at the head (7,868 of 7,868, `receipts/monitor-arbiter-9b4da6b5.txt`).
  - To the other reviewer's unit probe (case F for `cross_iss_m0_drains_m1`; case B for `write_iss_m0_only` and `stale_we_m0_only`; neither kills `cross_own_m0_drains_m1` or `write_own_m0_only`): consistent with the author's public receipt of that probe run against my 16 edits (`author-r6/receipts/unit-probe-r391-5-mutants-9b4da6b.txt`). I did not run that probe.
- **One stale count outside the item's scope.** The README's "Pinned wiring" paragraph still reads 107 of 349. That is S2.

**Item 3: PR body.** Met.

- The Round 6 section and the consolidated list carry my R391-5 S2:
  - the word-36 check now runs before the moved `[AECP-WTMO]` arm;
  - the real edit must re-read word 36 after the arm, or in its heal;
  - three stale harness comments (my two plus a third of the same kind).
- The list also carries the five ungraded manager-0 inputs, and "Whatever makes manager 0 present one of them must grade it first".
- Checked against a copy of public milan-fpga dev `9e3ccbfb` with the unchanged `author-r6/parent_edits.py` applied (rc 0, all three groups):
  - the arm's call is at `sim_nxn.cpp:2484`;
  - the word-36 check is at `:2609-2610`;
  - the comments are at `:2547-2549` and `:2560-2562`;
  - the third comment is at `:2604-2606`, where the body says `:2605-2607` (S3).

  Receipt: `receipts/parent/9e3ccbfb-author-r6-edits-sim_nxn-S2.txt`.

**Gates reproduced here at the head.**
- `tb/acmp_nvm` `make run`: 360 of 360 (`receipts/suite-acmp_nvm-head.log`).
- `tb/pp_top` `make run`: 7,888 of 7,888 (default build 7,868, plus fixture build 20), in 308 s (`receipts/suite-pp_top-make-run-head.log`). This matches the body's 7,888.
- `make check` rc 0, `gen_matrix.py --check` rc 0, `git diff --check c951a9ff..9b4da6b5` rc 0.
- Hosted: workflow `hdl` ran at the exact head:
  - on `push`, run 36552529765;
  - on `pull_request`, run 36552533874.

  Both completed with success. Six jobs executed and none was skipped. The only skipped step is `Build Verilator v5.050`, on a cache hit (`receipts/hosted-check-runs-head.txt`). The manager owns hosted and act acceptance.

## Findings

### S1 - SUGGESTION - Tests - N11d's failure text asserts "in none of their %d issue cycles" whatever the count it checks

- **Where.** `tb/acmp_nvm/sim_main.cpp:2714-2721`. The CHECK requires `m0_rd_issues_m1_abort == 0`, but the message prints `m0_rd_issues` into the fixed text "and in none of their %d issue cycles".
- **Evidence.** `receipts/mutants-r391-6-acmp_nvm.log`:
  - `h_n11d_also_issue` (manager 1's abort also in manager 0's issue clocks) fails N11d, as it should, with the text "... and in none of their 8 issue cycles ...".
  - Its diagnostic twin `h_n11d_also_issue_diag`, whose message prints the checked count, reads "in 8 of their 8 issue cycles".
  - N11b's message, by contrast, prints its count ("%d of the walk's %d READs issued with it").
- **Impact.** None on grading: the check fails when it must. On that failure, though, the message tells whoever triages it the opposite of the fact, and the pass run prints no line, so the text is the only record. The same pattern ("none drained") is harmless there, because `drain_on` is printed beside it.
- **Suggested outcome.** Print `m0_rd_issues_m1_abort` ("in %d of their %d issue cycles").
- **Verification.** `scripts/run_r391_6.sh <clone> <rev> <scratch> <vdir> acmp h_n11d_also_issue` shows the true count.

### S2 - SUGGESTION - Docs - the `tb/acmp_nvm` README's `make pinned` count is the base's, not the head's

- **Where.** `tb/acmp_nvm/README.md:265-273`: "`make pinned` ... exits non-zero. It is the reproduction of the recorded L05 control: 107 of 349 checks fail".
- **Evidence** (`receipts/acmp_nvm-pinned-counts.txt`):
  - base `c951a9ff`: 349 checks, **107** FAIL, as the text says;
  - `9dce84ea`: 359 checks, 109 FAIL;
  - this head: **360 checks, 110 FAIL**. The added failures are N10, N11b and N11d, whose walks cannot complete "as saved" without the gate (`receipts/acmp_nvm-pinned-9b4da6b5.log`).
- **Impact.** Small. `make pinned` is outside the suite's run and outside every gate, and the L05 evidence the paragraph describes is unchanged. But it is the only present-tense count in that README that no longer matches the tree, and this lane's N10/N11 checks moved it.
- **Suggested outcome.** Refresh it to 110 of 360, or date the 107 of 349 as the base measurement. Carry it with the next edit of that README; it needs no round of its own.
- **Verification.** `make -C tb/acmp_nvm pinned` tally.

### S3 - SUGGESTION - Docs (PR body) - the third stale comment's line reference is one line late

- **Where.** PR body, Round 6 consolidated list, "The order the moved arm leaves": "the comments `:2547-2549`, `:2560-2562` and `:2605-2607`".
- **Evidence.** In the edited scratch `sim_nxn.cpp` (identical at `eaa88a32` and at `9e3ccbfb`), "[AECP-WTMO] added one deliberately" spans `:2604-2606`. `:2607` is the `ck(... no response was voided ...)` line (`receipts/parent/9e3ccbfb-author-r6-edits-sim_nxn-S2.txt`).
- **Impact.** Negligible: the quoted text identifies the comment, and these are scratch-file lines for the pin-adoption lane.
- **Suggested outcome.** Use `:2604-2606`, or quote only the text, when the list is carried.

## Items of this round

| Item (5885497133) | Result | Evidence |
|---|---|---|
| 1. N11d holds manager 1's abort across manager 0's owned READs, with a non-vacuity count; `owned_arm_cross_intent` and `cross_own_m1_drains_m0` KILLED with README rows, every count equal to the run | **met** | `tb/acmp_nvm` 360/360; arbiter-side monitor 168/168 owned, 0/8 issue, 0 drained; `d3_mutants.py` 83/83, goldens PASS; README 86 entries 0 problems; both new controls fail N11d alone |
| 2. 09 §8.2 and the `acmp_nvm` README grade exactly what the tree grades; the manager-0 inputs listed with why and the out-of-tree probes | **met** | `09:192`; README `:213-263`; RTL premises verified; my monitor 0 manager-0 inputs in `tb/pp_top`; stale pinned count outside the item (S2) |
| 3. PR body Round 6 and the consolidated list carry R391-5 S2 | **met** | word-36 order, re-read requirement and three comments stated; anchors verified at `9e3ccbfb` (S3 one-line offset) |
| No RTL change | **confirmed** | `git diff --quiet 9dce84ea 9b4da6b5 -- hdl syn scripts .github Makefile` rc 0 |
| Gates: suites rc 0, `d3_mutants.py` all KILLED, reviewers' round-5 scripts reproduce | **met (my scope)** | `tb/acmp_nvm`, `tb/pp_top`, `make check`, matrix and diff-check here; my round-5 scripts reproduce with the one intended change; the full 33-suite bank is the manager's |

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-6 assignment items 1-3 and the gates, against the commit, 09 §8.2, both READMEs and the PR body. The arbiter banner rules (`KL_pp_nvm_mgr_arb.sv:38-65`) against N11a-d. The five manager-0 inputs against my R391-5 S1 count. S2 carried in the body's consolidated list | R391-6 | 9b4da6b5753fec8f5b2bba605c47af56c6cf1a0f |
| RTL | CLEAN | No RTL change (`hdl/`, `syn/`, `scripts/`, `.github/`, `Makefile` diff empty since `9dce84ea`). Arm terms `KL_pp_nvm_mgr_arb.sv:147-151` re-read against N11d. Binding-manager abort, per-wait count and walk entry (`KL_acmp_nvm_shadow.sv:547-576, 733-770, 866-925`). The D3 writer's aggregate liveness and commit (`KL_aecp_nvm_writer.sv:562, 1090`). The wrap tap `arb_end_o` is test-bench only (`acmp_nvm_wrap.sv:88, 544`) | R391-6 | 9b4da6b5753fec8f5b2bba605c47af56c6cf1a0f |
| Robustness | CLEAN | Arbiter-side ownership monitor: the harness's owned window equals `own_r == O_M0 && !we_r` clock for clock. Four weakenings of N11d's stimulus and bookkeeping, all caught. A narrower arbiter variant (first owned clock only), caught. `mon_unreachable_inputs` over `tb/pp_top` at the head: 0 manager-0 inputs. `d3_mutants.py` refuses an unknown mutant name (rc 2, observed) | R391-6 | 9b4da6b5753fec8f5b2bba605c47af56c6cf1a0f |
| Tests | CLEAN (S1 suggestion) | N11d code and tap. `tb/acmp_nvm` 360/360; `tb/pp_top` `make run` 7,888/7,888. `d3_mutants.py` 83/83 KILLED, goldens PASS, README counts = run (86, 0 problems). My 16 round-5 edits plus 7 round-6 probes and 2 monitors. `make pinned` at base, `9dce84ea` and head | R391-6 | 9b4da6b5753fec8f5b2bba605c47af56c6cf1a0f |
| Docs | CLEAN (S2, S3 suggestions) | 09 §8.2 row `:192` and the 83 count; the `acmp_nvm` README (360, N11a-d, the ungraded list and its premises, the eleven-row record, "Pinned wiring"); the `pp_top` README (83, seven N11 controls); the `d3_mutants.py` block. PR body Round 6 and the consolidated list, against the edited scratch `sim_nxn.cpp` at `9e3ccbfb`. `make check` rc 0, `gen_matrix.py --check` rc 0, `git diff --check` rc 0 | R391-6 | 9b4da6b5753fec8f5b2bba605c47af56c6cf1a0f |

## Real limits

- **Simulator.** The named path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host.
  - I used a copy of the byte-identical sibling wrapper (sha256 `905795b9...`, identical across all 195 sibling wrappers).
  - It runs a binary with sha256 `fb2cc573...` that reports `Verilator 5.050 2026-07-01 rev v5.050` (`receipts/verilator-identity.txt`), the same identity as rounds 1-5.
- **Not run:**
  - the full processor bank (`run_suites.sh`, 33 suites), full lint, Yosys, `srp_top` mutants, `nvm_port` figures, the aggregate sweep and the D1 probe. There is no `hdl/` change since round 5, and those inputs are unchanged. I ran only the two suites the commit touches, plus `make check`, the matrix and diff-check;
  - any parent, builder or gPTP bank. The parent was only cloned and edited to read the S2 anchors; nothing in it was built or run;
  - the other reviewer's round-5 scripts and the arbiter unit probe. The README's statements about that probe are checked only against the author's public receipt.
- **The campaign.** It ran as six `--only` partitions of one exact-head `git archive` extract (compile jobs capped at 2, `--jobs` at most 8). The `tb/pp_top` golden therefore ran five times, all PASS. The union equals the driver's 83 names.
- **Simulation only.** The monitors and probes are disposable edits in exports. Physical calibration was NOT RUN, field skips are not hardware proof, and nothing here is hardware proof.
- **DR3a and DR4 not re-measured.** There is no RTL or synthesized-file change.
- **Clone hygiene.** Every build and probe ran on `git archive` exports under this packet's `scratch/`.
  - The one file written into the clone was a `tb/pp_top/__pycache__`, from importing `d3_mutants.py` for its mutant list. I removed it.
  - At the end:
    - HEAD, the tree and the index agree;
    - all 312 work-tree blobs rehash to their tree blobs, and the modes match;
    - status, ignored files included, is empty;
    - there are no gitlinks and no `.gitmodules`, so no submodule gitlinks are required (`receipts/clone-integrity.txt`).

## Pending manager duties

- Consider S1-S3. None needs a round of its own.
- Run the donor full bank at the head, and the patched parent consumer bank (the manager's regenerated `parent_edits.py` at dev `9e3ccbfb`, carrying #616, #619 and #617).
  - The author's unchanged `author-r6/parent_edits.py` also applies cleanly at `9e3ccbfb` (text only; not built here).
  - Live dev read `79c36963` at 2026-09-29T10:40Z, past `9e3ccbfb`.
- Build the final current-dev candidate at the merge turn (source base `c951a9ff`).
- Carry into the pin-adoption lane the consolidated list, including the word-36 order and the three comments (S3's line fix), and the five ungraded manager-0 arbiter inputs.
- Own hosted and act acceptance, and record that physical calibration is NOT RUN.

## Receipts and reproduction

Every file below is listed in `MANIFEST.sha256`.

**Scripts** (`scripts/`). None of them writes into the checkout; every tree is a `git archive` export.

- `run_r391_6.sh <checkout> <rev> <scratch> <verilator dir> <probe> [args]`. It is `run_r391_5.sh` with the mutant table switched to `r391_6_mutants.py`, and `R391OWN` added to the `acmp` grep. Probes: `acmp|full|d3 [MUTANT]` and `sweep|d1`.
- `r391_6_mutants.py` loads `r391_5_mutants.py` unchanged and adds:
  - the round-6 arbiter variant `cross_own_m1_drains_m0_first_clk`;
  - four harness or tap weakenings: `h_n11d_no_drive`, `h_n11d_half_drive`, `h_n11d_also_issue` and `t_arb_end_stuck0`;
  - the diagnostic twin `h_n11d_also_issue_diag`;
  - the print-only monitor `mon_own0_reads`.
- `r391_5_mutants.py`, `run_r391_5.sh`, `r391_4_d1.hpp`, `r391_4_sweep.hpp`, `check_readme_counts.py` and `summarize_monitor.py`: my round-5 scripts, unchanged.
- The campaign ran as `python3 tb/pp_top/d3_mutants.py --output DIR --verilator V --jobs 8 --only NAMES...` from a `git archive` export of the head, in six partitions.

**Receipts** (`receipts/`).

- **Suites:**
  - `suite-acmp_nvm-head.log` (360);
  - `suite-pp_top-make-run-head.log` (7,888);
  - `suite-pp_top-default-head.log` (7,868).
- **Mutants:**
  - `d3_mutants-intree.log` and `d3_mutants-intree-results.json` (83/83);
  - `readme-counts-vs-run.txt`;
  - `mutants-r391-6-acmp_nvm.log` (the golden, 23 edits and the diagnostic twin).
- **Monitors:**
  - `monitor-arbiter-9b4da6b5.txt`.
- **`make pinned`:**
  - `acmp_nvm-pinned-counts.txt` and `acmp_nvm-pinned-9b4da6b5.log`.
- **Parent:**
  - `parent/9e3ccbfb-author-r6-edits-sim_nxn-S2.txt`;
  - `author-r6-parent_edits.sha256`.
- **Gates and environment:**
  - `make-check-head.log`, `gen-matrix-check-head.log` and `diff-check-head.txt`;
  - `hosted-check-runs-head.txt`, `clone-integrity.txt` and `verilator-identity.txt`.

## Prior public findings, resolved or retained at this head

These were read after the verdict, findings and ledger above were fixed. R390-5's report (5884919813) was read for its findings.

R390-6 is concurrent and was not read. A comment search for R390-3-S2's ruling, made after this report's verdict was fixed, listed R390-6's first line. Nothing of its content was read.

| Finding | Status at 9b4da6b5 | Evidence |
|---|---|---|
| R390-5 F1 MINOR, the owned half of "an abort drains only its own manager's READ" is ungraded; 09 and the author's statement overclaim | **Resolved**, by its preferred outcome | N11d holds manager 1's abort through manager 0's owned READs, with a non-vacuity requirement (168/168, 0/8 issue: my arbiter-side monitor). `cross_own_m1_drains_m0` (the same edit as that finding's `r5_owned_cross_m0_only`) and `owned_arm_cross_intent` are in `d3_mutants.py` with README rows, both KILLED by N11d; 83/83. 09 `:192` now claims manager 1's half only. The README records the two by-construction inputs the finding names, plus three more, and names the unit probe's case F for the first. I did not run that reviewer's `r5_extra_mutants.py` |
| R391-5 S1 SUGGESTION, the arbiter contract is graded for manager 1's halves only; "one input" undercounts | **Taken** | Item 1 and item 2 above; the five-input list is in the README and in the PR body's consolidated list. The residue is S1 and S2 of this report |
| R391-5 S2 SUGGESTION, the moved `[AECP-WTMO]` arm and the word-36 order, and two stale comments | **Taken** (for the pin-adoption lane) | Item 3 above; a third comment added; the line offset is S3 |
| R390-5 carried R390-2-S1, no `RX_SLOTS_P >= 2` floor | **Not taken (not assigned)** | `hdl/` unchanged |
| R390-3-S2, D3R15's re-LOCATE arm; asks for a manager confirmation | **Open for the manager, unchanged** | no ruling found on issue #131 or PR #132; RTL and D3R15 unchanged |
| R390-4 F1, S1, S2; R391-4 F1, S1 | stay **resolved or taken** | no change to their subjects since round 5; their controls are among the 83 KILLED; the parent edit script is byte-identical |
| Earlier R390 and R391 findings (rounds 1-3) | stay **resolved or taken** | no `hdl/` change since round 4. `tb/pp_top` 7,888/7,888 and `d3_mutants.py` 83/83 include all their controls |

R391-6 FINISHED
