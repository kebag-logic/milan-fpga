[R685] POSITIVE - exact head 15c32d1b65450903355647fc83d10e6dd4d6a7f8

Internal independent review R685-4 of issue #775 / PR #777. Exact head `15c32d1b65450903355647fc83d10e6dd4d6a7f8`, tree `216cc3f8ba735132f876379101d4bbd390866247`. This is a round-4 delta review of one merge commit, `220b51f2..15c32d1b`. It merges dev `50730a19` into the branch, bringing in PR #779 (#773) and PR #782 (#781).

**Why POSITIVE.**
- The merge is textually exact on both sides:
  - Every file this PR changed carries the same added and removed lines against dev as it did against the lane base.
  - Every file dev changed carries the same lines against the branch.
  - The one conflict, `docs/reference/MILAN_COMPLIANCE_MATRIX.md`, is resolved without losing text from either side, and no other row changed.
- On the merged tree I built and ran every check and mutant this PR claims. All pass, and each #775 defect fails its named check:
  - avtp_rxmon `[SQ]`, crf_rx `[SQ]`, `format_mutants.py` and its four two-copy arms;
  - the `sim_nxn.cpp` legs that carry both this PR's `[CTRS-CRF]` change and #773's timestamp grading, on four shapes;
  - #773's `capture_coherence` dp leg against this PR's changed listener RTL.
- Shard selection places all 81 cases once across 17 workers, and the cases cover all 64 inventory suites.

No new BLOCKER, MAJOR or MINOR. One new RESIDUE (PR text) and one new SUGGESTION. The prior RESIDUE and SUGGESTIONs from R685-3 are carried.

## Reconstruction

- **Authorities:** AGENTS.md sections 3 and 5 to 7, and CONTRIBUTING.md, which governs: one-line commits, two positive reviews, lens coverage banked per head.
- **Issue #775 frozen scope:**
  - A discarded off-format PDU still advances the sequence state, on the AAF input (`KL_avtp_rx_monitor_ctx`) and the CRF input (`KL_crf_rx`).
  - It counts only UNSUPPORTED_FORMAT and presents nothing (Milan v1.2 Table 5.6: the off-format PDU is "received").
  - A test plants one off-format PDU mid-stream and shows SEQ_NUM_MISMATCH, MEDIA_RESET, TIMESTAMP_UNCERTAIN, LATE_TIMESTAMP and EARLY_TIMESTAMP unchanged.
  - A control that drops the advance must fail.
- My R685-3 ledger at `220b51f2` stands for everything the delta leaves unchanged. Below I show that the delta leaves every byte of this PR's own change unchanged.
- **Delta under review:** `git show --remerge-diff 15c32d1b` (`receipts/remerge_diff.txt`). The only hand resolution is in the compliance matrix. `docs/testing/TESTING.md` and `tb/verilator/milan_dp/sim_nxn.cpp` merged automatically on both sides (`receipts/both_sides_touched.txt`).

## Delta analysis

1. **This PR's change is preserved byte for byte** (`receipts/branch_delta_preserved.txt`).
   - For each of the 13 files in `a032c6d6..220b51f2`, I compared the +/- lines with those of `50730a19..15c32d1b`. All 13 are SAME.
   - The two file sets are identical: 13 files, 601 insertions, 56 deletions on both sides.
2. **Dev's change is preserved byte for byte** (`receipts/dev_delta_preserved.txt`).
   - For each of the 22 files in `a032c6d6..50730a19`, I compared the +/- lines with those of `220b51f2..15c32d1b`. All 22 are SAME.
3. **Compliance matrix** (`receipts/matrix_vs_dev.diff`, `receipts/matrix_vs_branch.diff`).
   - Against dev, exactly one line differs: the 4.4.2.2 / 5.3.8.10 row at `MILAN_COMPLIANCE_MATRIX.md:192`. It is dev's row verbatim, followed by this PR's #775 sentence ("A discarded PDU was still received, ... (#775; `avtp_rxmon` `[SQ]` and `crf_rx` `[SQ]`, each with planted mutants)").
   - Against the branch, exactly two rows differ, and both are dev's own edits: the 5.3.7.6 / 4.4.2.1 row at `:191` (#773's rewrite, verbatim) and the 4.3.5 / 10.8 row at `:227` (dev's edit, verbatim).
   - No other row changed, and neither side lost text.
4. **`sim_nxn.cpp` semantics.**
   - This PR's hunk is the `[CTRS-CRF]` event arm: seven rejected type-2 PDUs now advance `cseq` (`sim_nxn.cpp:7044-7067`).
   - Dev's hunks are #773's `periods_on_grid` and `grade_output_timestamps` grading (`sim_nxn.cpp:8654-8880`).
   - The two touch disjoint functions and share no state beyond the harness clock. Both run in the same binary on the merged tree (execution E3 below).
5. **RTL interaction.**
   - Dev's RTL hunks are in the talker path: `KL_aaf_packetizer`, `KL_crf_tx`, `KL_media_domain_event`, `KL_media_if_latency_pkg`, and `milan_datapath.sv:1255-1500, 7112-7440`.
   - This PR's RTL is the two listener engines, whose instances and ports dev does not touch.
   - The `capture_coherence` dp leg elaborates both together and passes (E4).
6. **`TESTING.md`.**
   - The two sides edit different rows: this PR's `avtp_rxmon` row `:617` and `crf_rx` row `:628`; dev's worker count `:541-552` and `capture_coherence` row `:619`.
   - Counts checked against execution on the merged tree:
     - the `avtp_rxmon` row says `lockstep_mutants.py` has 13 defects; the log shows "14 checks: 14 PASS", the clean build plus 13;
     - the row also says `format_mutants.py` has five compare plus seven #775 defects; the log shows "13 checks: 13 PASS", the clean build plus 12;
     - the `crf_rx` row names two #775 mutants, `offformat_no_advance` and `offformat_seeds_sequence`, and both pass;
     - "seventeen ... `--shard INDEX/17`" matches 17 listed shards.
   - Dev's "thirty-two defects" claim for `capture_coherence` `mutants.py` is outside this PR's delta, and I did not execute it.
7. **Merge commit.** One line, no trailers (`git cat-file commit 15c32d1b`). The subject names PR #779 but not PR #782 (#781), which also enters through this merge (`30d35da8f` is not an ancestor of `220b51f2`). See RES-1.
8. **Comment rule.** The resolution adds no source comment. A scan of this PR's source delta on the merged tree found no lane labels, round or reviewer IDs, or comment IDs (`receipts/comment_rule_scan.txt`).

## Prior findings, checked at this head

These were read after my own pass. The merge leaves every byte of this PR's change unchanged, so each resolution stands for the same reason it did at `220b51f2`.

- **R685-1-F1 (MINOR), R685-1-F2 (RESIDUE), R685-2-F1 (MINOR), R685-2-R1 (RESIDUE), R686-2-F1 (MINOR), R685-2-S1 (SUGGESTION): RESOLVED.** Each stays resolved at this head. The `[SQ4]`-`[SQ7]` arms and the two-copy construction execute on the merged tree:
  - `lock_set` fails `[SQ4c]`/`[SQ4f]`;
  - `settle_step` fails `[SQ5c]`/`[SQ5d]`;
  - `mr_seed_set` fails `[SQ6c]`/`[SQ6e]`/`[SQ6i]`;
  - `mr_seed_clear` fails `[SQ7c]`/`[SQ7d]`/`[SQ7e]`;
  - each prints "lockstep on the planted pair, as measured and not graded: rc 0, N=1 116/0, N=8 119/0" (`receipts/avtp_rxmon_make_run.log:1452-1485`).
- **R685-3 commit `220b51f2` tally fix: still VERIFIED.** On the merged-tree log, `scripts/suite_tally.py` counts avtp_rxmon as 577 checks / 0 failures / 6 tallies, and does not count the four planted-pair lines (`receipts/suite_tally.txt`).
- **R685-3-R1 (RESIDUE, Docs): RETAINED, still open.**
  - Where: `tb/verilator/avtp_rxmon/Makefile:47-49`, unchanged by the merge.
  - Exact fix as published: "RXMON_SRC and NX_MDIR do the same for format_mutants.py and the N=4 stack (#765); for #775's two-copy defects format_mutants.py also builds this leg, through RXMON_SRC, REF_SRC and LS_MDIR, from a mutated engine and reference."
- **R685-3-S1 (SUGGESTION, Tests): RETAINED, optional.** Mark the pair's lockstep line when its rc is non-zero (`format_mutants.py:211-221`).
- **R685-1-F3 (SUGGESTION, Tests): RETAINED, out of scope.** The AAF 100 ms silence watchdog across a reject is ungraded, and `TESTING.md:617` says so. Any follow-up issue belongs to the manager.
- **R686-1 / R686-3:** positive, with no findings to resolve.

## Findings (this round)

### RES-1 - RESIDUE - Docs - the merge's subject names one of the two dev PRs it brings in

- **Where:** commit `15c32d1b` subject, "Merge dev 50730a19 (PR #779, #773) into 775-offformat-seq-advance, ...", and any PR #777 text that repeats it.
- **Evidence:** `git log --first-parent a032c6d6..50730a19` lists two merges: `50730a19` (PR #779, #773) and `30d35da8` (PR #782, #781). Neither is an ancestor of `220b51f2`.
- **Impact:** wording only. A reader of the subject alone does not learn that #781's 17-worker schedule entered this branch here. The schedule itself is verified below (E1). No measurement, test, code or claim changes.
- **Exact fix:** do not rewrite published history. Where PR #777's text or the manager's merge record describes this merge, write "Merge dev 50730a19 (PR #779 for #773 and PR #782 for #781)".

### S-1 - SUGGESTION - Tests - `avtp_rxmon`'s scheduling figure predates #765 and #775's added campaigns

- **Where:** `scripts/suite_shards.py:85` (`"avtp_rxmon": 73`, from #727's dev run at `c6bd08c6`). This PR does not change the figure, and neither does the delta.
- **Evidence:**
  - On the merged tree, the suite's default `run` took 356 s wall time locally: `05:45:39Z` to `05:51:35Z` in `receipts/avtp_rxmon_make_run.log`, while three other builds shared the host.
  - The run includes `format_mutants.py`'s 12 arms and eight extra lockstep builds for the two-copy pairs.
  - The per-suite timeout is 1800 s (`run_all_suites.sh:259`). The figure only places suites on shards, and avtp_rxmon sits on 11/17.
- **Suggestion:** when the hosted run at this head completes, the manager may re-measure avtp_rxmon's window with `scripts/suite_shards.py --measure` and refresh the figure in a later scheduling change. This has no verdict effect, and nothing here suggests a timeout risk.

## Executions (this round, on the merged tree)

All builds used the pinned Verilator 5.050 (`verilator --version` prints "Verilator 5.050 2026-07-01 rev v5.050"; the system default is 5.052 and was not used). They ran in two disposable probe trees:
- a shared clone checked out at `15c32d1b`, with every required submodule at its recorded gitlink (`receipts/probe_tree_integrity.txt`, "tracked files == HEAD", submodules clean);
- a byte copy of the clean review clone, whose tracked-file digest equals the clone's (`4dafa250...`).

| ID | Command (dir) | Result | Receipt |
|---|---|---|---|
| E1 | `python3 -I scripts/suite_shards.py --selftest`; `run_all_suites.sh --ci-pieces --shard i/17 --list` for i = 0..16; `run_all_suites.sh --list`; `scripts/check_shard_placement.py` | selftest PASS rc 0. 17 shards rc 0, 81 cases, 81 placements, none multiply placed; 64 inventory suites, none unplaced, none extra. avtp_rxmon on 11/17, crf_rx on 12/17, milan_dp__0..3 one each | `receipts/suite_shards_selftest.log`, `shard_lists_17.log`, `suite_inventory.log`, `shard_placement_check.txt` |
| E2 | `make VERILATOR_JOBS=4 run` (`tb/verilator/avtp_rxmon`) | rc 0. Flat 97/0; NxN stack 218/0, 71 `[SQ]` checks pass; lockstep N=1 116/0, N=8 119/0; `lockstep_mutants.py` 14/14; `format_mutants.py` 13/13, five #765 arms plus seven #775 arms, the four two-copy arms each building the N=4 stack from the planted engine and the lockstep leg from both planted copies | `receipts/avtp_rxmon_make_run.log` |
| E2b | `make VERILATOR_JOBS=4 all` (`tb/verilator/crf_rx`) | rc 0. Unit 15714/0, with `[SQ-0]`..`[SQ-d4]` (23 checks) all PASS; discontinuity 2201/0; talker_step 69/0; mutants 23/23, including `offformat_no_advance` (fails `[SQ-b2]`) and `offformat_seeds_sequence` (fails `[SQ-d1]`) | `receipts/crf_rx_make_all.log` |
| E3 | `make build-<leg> && make exec-<leg>` for `nxn`, `nxn8`, `nxn4c`, `nxndv` (`tb/verilator/milan_dp`) | all rc 0: 2098/0, 3998/0, 2098/0, 2100/0. Every leg runs `[CTRS-CRF] events, all ten` (11 checks, UNSUPPORTED_FORMAT 7 and SEQ_NUM_MISMATCH 4 after the seven advancing rejects) and #773's "#632 exact stamps" and "#773 output n adds one whole number of periods" grading in the same binary | `receipts/milan_dp_{nxn,nxn8,nxn4c,nxndv}.log` |
| E4 | `make VERILATOR_JOBS=8 dp` (`tb/verilator/capture_coherence`) | rc 0, 847/0. #773's `[WIRE]`, `[GRID]` and `[HOLD]` lines, including `DP-CRF125-0..7`, pass on a `milan_datapath` that elaborates this PR's `KL_crf_rx` and `KL_avtp_rx_monitor_ctx` | `receipts/capture_coherence_dp.log` |
| E5 | `scripts/suite_tally.py` over E2, E2b and E3 | 28878 checks, 0 in-suite failures, rc 0 | `receipts/suite_tally.txt` |
| E6 | docs gates: `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`; and an independent U+2014 scan of the Markdown lines added since `50730a19` and since `220b51f2` | three gates rc 0; 0 added em dashes on both bases (grep control on a planted em dash: 1). `gen_toc.py --check --verify-anchors` and `check_em_dash.py --base 50730a19` could not run here (rc 2: the pinned Markdown renderer is not installed), so for those two I rely on the manager's pass | `receipts/docs_gates.txt`, `docs_emdash_grep.txt` |
| E7 | hosted check runs at the exact head (read only) | at read time: `bdd-conformance`, `changes` and `docs-check-no-git` succeeded; every other context was queued or in progress. This is not hosted evidence for any gate | `receipts/hosted_checks_snapshot.txt` |
| E8 | review clone integrity after probes | HEAD and index tree are `216cc3f8...`; worktree equals HEAD; no untracked files; gitlinks `external` `efeb541a`, `gptp-processor` `55680bff`, `protocol-processor` `93fb0b2d`, as recorded in the head tree | `receipts/clone_integrity.txt` |

## Lens results

[R685] PASS Conformance - `docs/reference/MILAN_COMPLIANCE_MATRIX.md:191-192,227`; `receipts/remerge_diff.txt`; `receipts/branch_delta_preserved.txt` (`KL_avtp_rx_monitor_ctx.sv`, `KL_crf_rx.sv` SAME); `receipts/crf_rx_make_all.log` `[SQ-b1]`..`[SQ-b6]`; `receipts/avtp_rxmon_make_run.log` `[SQ2*]` - checked against the #775 criteria and Milan v1.2 Table 5.6:
- the 4.4.2.2 row keeps both #765's text and #775's claim;
- #773's 5.3.7.6 row is verbatim;
- both inputs still meet every criterion on the merged tree.

[R685] PASS RTL - `receipts/dev_delta_preserved.txt`; `hdl/milan/milan_datapath.sv` (dev hunks `:1255-1500,7112-7440`, talker side); `receipts/capture_coherence_dp.log`; `receipts/milan_dp_*.log` - no merge text touches either listener engine:
- the two sides' RTL is disjoint and composes in one elaboration on two shapes (1x1 TDM8 in `capture_coherence`, and the N=4/8 shapes in `sim_nxn`);
- clock, reset, width and port contracts are unchanged.

[R685] PASS Robustness - `receipts/avtp_rxmon_make_run.log` (`[SQ1]`..`[SQ7]`, 71 checks); `receipts/crf_rx_make_all.log` (`[SQ-a*]`..`[SQ-d*]`); `sim_nxn.cpp:7044-7067` - the boundary cases still pass on the merged RTL:
- mid-stream, fresh era, settle window, both sides of the mr seed, and a gap after a reject;
- seven back-to-back rejects advancing the CRF cursor in the full datapath.

[R685] PASS Tests - `receipts/avtp_rxmon_make_run.log:1421-1486`; `receipts/crf_rx_make_all.log:2608-2652`; `receipts/milan_dp_{nxn,nxn8,nxn4c,nxndv}.log`; `receipts/suite_tally.txt`; `receipts/shard_placement_check.txt` - the evidence:
- every claimed check and mutant builds and runs on the merged tree;
- each #775 mutant fails its named check;
- the two-copy arms build both copies;
- this PR's `sim_nxn` change and #773's grading run green together in four legs;
- the 17-worker selection places every case once.

S-1 is a SUGGESTION and does not un-clean this lens.

[R685] PASS Docs - `docs/testing/TESTING.md:541-552,617,619,628`; `MILAN_COMPLIANCE_MATRIX.md:191-192`; `receipts/docs_gates.txt`; `receipts/docs_emdash_grep.txt`; `receipts/comment_rule_scan.txt`; merge commit object - both sides' rows are intact, and their counts match execution (13 and 14 checks; two crf_rx mutants; 17 shards). No comment-rule instance is added. RES-1 (new) and R685-3-R1 (carried) are RESIDUE and leave the lens clean.

## Reviewer-owned coverage ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | matrix `:191-192,227`; remerge diff; branch/dev delta-preservation receipts; `[SQ]` receipts on both inputs; issue #775 criteria | R685-4 | 15c32d1b65450903355647fc83d10e6dd4d6a7f8 |
| RTL | CLEAN | dev RTL hunks (talker side); listener engines byte-preserved; `capture_coherence` dp and four `sim_nxn` elaborations | R685-4 | 15c32d1b65450903355647fc83d10e6dd4d6a7f8 |
| Robustness | CLEAN | avtp_rxmon `[SQ1]`-`[SQ7]`; crf_rx `[SQ-a]`-`[SQ-d]`; `[CTRS-CRF]` seven-reject arm in four legs | R685-4 | 15c32d1b65450903355647fc83d10e6dd4d6a7f8 |
| Tests | CLEAN (S-1 optional; R685-3-S1 and R685-1-F3 SUGGESTIONs carried) | avtp_rxmon `run` incl. `lockstep_mutants.py` and `format_mutants.py`; crf_rx `all` incl. `mutants.py`; `milan_dp` nxn/nxn8/nxn4c/nxndv; `capture_coherence` dp; suite_tally; suite_shards selftest and 17-shard placement | R685-4 | 15c32d1b65450903355647fc83d10e6dd4d6a7f8 |
| Docs | CLEAN (RES-1 new and R685-3-R1 carried, both RESIDUE) | TESTING.md `:541-552,617,619,628`; compliance matrix; docs gates (three run, two relied on); em-dash scan; comment-rule scan; merge commit object | R685-4 | 15c32d1b65450903355647fc83d10e6dd4d6a7f8 |

Every lens is covered at the merge candidate head itself.

## Real limits

- I ran no manager source bank, and none exists at this head. Source-head execution here is my own focused set (E1-E5), not a full parent, PP, gPTP or Yosys bank. Concretely, I did not run:
  - the full `milan_dp` suite (its base, notify, crflic, dynmap, prune, ax1x1, aclk and maprec legs, and `render-mutants`);
  - `milan_dp_mclk`;
  - `capture_coherence`'s junction leg and its 32-arm `mutants.py`;
  - lint and Yosys.
  
  Those are dev's or unchanged content. They belong to the manager's current-dev candidate validation at the merge turn.
- `gen_toc.py --check --verify-anchors` and `check_em_dash.py --base 50730a19` could not execute in this environment, because the pinned Markdown renderer is missing. Only the manager's pass covers them; my em-dash grep is a partial cross-check.
- Hosted evidence at the exact head was still queued or in progress when I read it (E7). Hosted and act acceptance belongs to the manager.
- Physical calibration NOT RUN. Simulation results are not hardware proof.
- Receipts had home-directory path prefixes in compiler command lines replaced by `<pinned-verilator-root>` / `<home>/`, and nothing else was changed.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `50730a19`, live dev `50730a19363c2cf4d3ebfc5123761a480ff45e32`), with builder and native banks, and link their receipts on the PR.
- Own exact-head hosted acceptance: `rtl-fast`, `verilator-suites` across 17 workers, and `yosys-portability`, along with act replication.
- Carry RES-1 and R685-3-R1 to the residue checklist. Optionally carry S-1 (re-measure `avtp_rxmon`'s hosted window) and the retained SUGGESTIONs (R685-3-S1, R685-1-F3) to follow-up.
- Obtain the second independent positive review at this head before any merge. Merging requires explicit maintainer authorization.

R685-4 FINISHED
