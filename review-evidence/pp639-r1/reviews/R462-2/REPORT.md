[R462] POSITIVE - exact head 1cba30c91bbc4c0e20343f883b94c3f701cc0dbc

# R462-2: internal independent review, processor PR #155 / milan-fpga #639, round 2

- **Head:** `1cba30c91bbc4c0e20343f883b94c3f701cc0dbc`, tree `c81e4a5e52e223e324813dad900953233a3d087f`.
  This is the manager's `--no-ff` merge of processor `main` `07b1469d` (PR #154) onto the author's round-2 head `2ff8183a`.
- **Source base:** `5c71928ad2bf1a854a5538d69b77214dfdf1697f`.
- **Delta reviewed:** `9e869910..1cba30c9`: four author commits (`89b000c`, `b1b6a5a`, `6b82f9b`, `2ff8183`) and the manager merge.
- **Lane diff against current `main`:** `git diff 07b1469 1cba30c9` touches 12 lane files only.
- **Assignment:** milan-fpga #639 comment 5981052216 (round 2), which carries R462-1 F1 and S1.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR is open. All five lenses are CLEAN. One RESIDUE (R1, PR-body wording) is recorded for the manager's residue checklist.

- **R462-1 F1 is resolved at this head, against every item of its required outcome.**
  - Section AQ's committed drive (AQ3, AQ4) reaches every required state.
  - R462-1's `aq_probe.sh` and every `gen.py --mutant` control, run unchanged, now fail AQ3. Only the `hd_not_reset` probe passes, and it is an equivalent.
  - The same controls pass the round-1 bench, which is the red proof.
  - AQ passes on the head and on `main`'s RTL, with identical coverage lines.
  - The four new controls and the five re-pointed ring arms are KILLED: 33/33 in the ACMP campaign, every arm at its recorded count.
  - Nothing in the tree points at an unpublished bench.
- **R462-1 S1 is resolved.** The banner edit is comment-only.
- **R463-1's F1 (RESIDUE) and S1 (SUGGESTION) are both resolved at this head.** See "Prior public findings".
- **The manager merge keeps both sides exactly.** `git merge-tree --write-tree 2ff8183 07b1469` reproduces tree `c81e4a5e` byte for byte. `docs/guides/hdl-engineer.md` holds both sides' paragraphs as adjacent, separate blocks.

## Findings

### R1: RESIDUE (Docs). The PR body's opening still describes the author's round-2 head

- **Where:** PR #155 body, the opening paragraph: "with `main` merged twice as it moved (`83999eba`, then `c050d971`); eleven commits, head `2ff8183`".
- **Evidence:** the exact head is `1cba30c9`, which adds a third merge of `main` (`07b1469d`, PR #154). The manager's closing line in the same body states that merge correctly. `git log --first-parent` shows 12 commits from `5c71928a` to `1cba30c9`, three of them merges.
- **Impact:** wording only. The body gives the correct head in its last line. No figure, test, code, conformance claim or privacy rule is affected.
- **Required outcome (exact fix):** replace "with `main` merged twice as it moved (`83999eba`, then `c050d971`); eleven commits, head `2ff8183`" with "with `main` merged three times as it moved (`83999eba`, `c050d971`, then `07b1469d` by the manager); twelve commits, head `1cba30c9`".
- **Verification:** read the edited paragraph against `git log --first-parent --oneline 5c71928a..1cba30c9`.

There is no other finding.

### Prior public findings, explicitly resolved

These were read only after this review's own pass over the diff and its probes.

| Finding | Severity | Status at `1cba30c9` | Evidence |
|---|---|---|---|
| R462-1 F1: no committed check of the rings' full-queue path | MINOR | **RESOLVED** | See "Tests" and "Robustness" below. Each item of its required outcome is met: the drive covers counts 2 to 4, the full pop+push, the refused push and its drop, two faces dropping, saturation, and reset with arms queued. `armq_write_refused` and `armq_write_wrap_hi` are KILLED by AQ3 and recorded in `tb/pp_top/README.md:2065-2066`. 09 §8.8, section AQ (`README.md:1982-2072`) and `acmp_mutants.py:164-169` were corrected. The bar holds: `aq_probe.sh` rc 1 for both probes, and every `gen.py --mutant` control fails AQ3. |
| R462-1 S1: name the source of "1,153 flops" | SUGGESTION | **RESOLVED** (taken) | `protocol_processor_top.sv:3002-3007`. The edit is comment-only (`receipts/static/hdl-diff-r1-to-head.txt`). |
| R463-1 F1: 09 §8.8 says the benches are "recorded in the issue's pull request" | RESIDUE | **RESOLVED** | The sentence is gone (`09_verification.md:390-392`). The benches are now published at milan-fpga `b95bc644` `review-evidence/pp639-r1/author-r2/lockstep/`. |
| R463-1 S1: three ring defects pass every committed check | SUGGESTION | **RESOLVED** | (1) write on offer = `armq_write_refused`, KILLED. (3) a full pop refuses the push = `armq_full_pop_refuses`, KILLED. (2) a write-first read on a full pop+push was planted here as `own_mutants.py` `write_first_read`: AQ3 fails on 12,481 of 90,172 edges, exactly the drive's full pop+push count. |

## Evidence by lens

### Conformance: CLEAN

- **Scope of the round.** The round-2 assignment allows no behaviour-changing HDL edit. `git diff 9e869910 1cba30c9 -- hdl/` is the banner comment at `protocol_processor_top.sv:3002-3007`, and every changed line is a `//` comment. The arm-port block re-cut at the head differs from the published `dut.sv` (cut at `9eebc61`) only in that comment and in the generator's first line (`receipts/static/lockstep-armq-recut-r2.diff`). So the round-1 equivalence evidence carries to this head.
- **Issue #639's rules.** These are no port, parameter or register change, behaviour identical, and equivalence proven with planted controls.
  - The lane's HDL against `main` (`git diff 07b1469 1cba30c9 -- hdl/`) is confined to the arm-port block and the listener's record RAM.
  - The new test ports (`dbg_aq_drive_i`, `dbg_aq_drv_*_i`) are on the test wrap, not on `protocol_processor_top`.
- **Behaviour against `main`.**
  - The published arm-port lockstep was re-run with the block cut from `1cba30c9`. Candidate: 32 × 1,000,000 cycles at slot widths 5, 6, 7 and 8, with 0 mismatches. Six controls are caught in 8 of 8 runs. The probe `ctl_probe_head_unreset` gives 0 of 8, as an equivalent should (`receipts/lockstep/armq-results-r2head/summary.txt`). `dut_aw6_s1.log` is byte-identical to the published log.
  - The listener RTL blob is unchanged since `9eebc61` (`082b6dad`). `tb/acmp_listener` passes 3,111 of 3,111 on both the head's RTL and `main`'s.
- **Closing keyword.** "Relates to milan-fpga#639" is unchanged and still justified: the resource gate's baseline lives in the parent.

### RTL: CLEAN

- **The ring at the head.** Read in full at `protocol_processor_top.sv:2948-3049`.
  - `wr_ix = hd + cnt[1:0]` puts the write after the survivors in every case. With the count at 4, only a popping clock admits a push (`mid != 4`), and that push lands on the leaving head. The asynchronous read sees the old entry and the write lands at the edge.
  - The head index advances on a pop. The count is reset and the entries are not, and no entry is read before a push wrote it.
  - The drop counter saturates, and rises once per dropping clock, as the banner and 08 §3 state.
- **Listener read path.** `rec_rd_w` (`KL_pp_acmp_listener.sv:746`) is consumed only in X_LATCH and X_STRT_AP (`:1051-1074`). Those states are entered only from X_RDREC and X_STRT_RD. Records are written only in X_INIT, X_PRELOAD and X_WB (`:744-745`), and `sink_r` changes only in X_IDLE. So the asynchronous read returns what the removed read register held.
- **Lint.** The gate's flags (`-Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM`, whole tree visible) report 0 warnings for both changed tops, with rc 0 (`receipts/static/lint-two-tops.txt`).
- **The manager merge.** `git merge-tree --write-tree 2ff8183 07b1469` gives `c81e4a5e`, the head's own tree. No lane file is touched by PR #154, apart from `docs/guides/hdl-engineer.md` in a separate hunk.

### Robustness: CLEAN

- **R462-1's probes, unchanged** (`aq_probe.sh` from milan-fpga `b95bc644`), on an export of the head:

  | Probe | rc | Failing | Edges differing |
  |---|---|---|---|
  | `write_refused` | 1 | AQ3 | 8,272 of 90,172 |
  | `wr_wrap_hi` | 1 | AQ3 | 19,343 of 90,172 |

  Both figures match the author's.
- **Every `gen.py --mutant` control, planted into the full head top** (`scripts/aq_gen_mutant.sh`, with `gen.py`'s `MUTANTS` imported unchanged):

  | Control | Failing (edges differing) |
  |---|---|
  | `write_refused` | AQ3 (8,272) |
  | `wr_wrap_hi` | AQ3 (19,343) |
  | `full_pop_refuses` | AQ3 (61,730) |
  | `drop_skip_sat` | AQ3 (4,099) |
  | `wr_at_head` | AQ2 + AQ3 (59,652) |
  | `wr_at_mid` | AQ2 + AQ3 (65,779) |
  | `head_stuck` | AQ2 + AQ3 (68,820) |
  | `read_tail` | AQ2 + AQ3 (74,397) |
  | `ring_of_three` | AQ2 + AQ3 (36,176) |
  | `hd_not_reset` (probe, an equivalent) | passes, AQ 4 of 4 |

- **Red proof.** The four full-queue controls, run on the round-1 bench (`9e869910`'s `tb/pp_top`), each pass with AQ 2 of 2 and rc 0. So the new drive, and not something else, kills them.
- **Reach past the required list.** Six controls of this review's own (`scripts/own_mutants.py`) are all killed by AQ3 alone. AQ2 passes for each, which shows that only the drive reaches them.

  | Control | Edges differing |
  |---|---|
  | count not reset (arms survive a reset) | 12,835 |
  | drop counter not reset | 85,658 |
  | saturation at 0xFFFE | 4,100 |
  | full pop+push writes one past the head | 15,355 |
  | drop counted on a full face that pops | 69,179 |
  | write-first read on a full pop+push | 12,481 |

- **Forces are test-only and do what the README says.**
  - The 41 force targets (`pp_top_wrap.sv:919-961`) are the 40 face nets plus `u_dut.u_timer.arm_valid_i`. They are raised once by a port that every other build leaves at 0.
  - In the generated model, the timer reads its arm input through the force (held at 0). The port taps read the unforced `tmr_arm_valid_w`, so the timer is idle while AQ3 still grades the mux's own port.
  - `hdl/` holds no `force`.
- **Receipts:** `receipts/aq/SUMMARY.txt` and one log, rc and time file per run.

### Tests: CLEAN

- **AQ3/AQ4 coverage against the required list.** Each item has a nonzero count in AQ4's guard, and every count equals the README table at `tb/pp_top/README.md:2040-2046`:

  | Required by R462-1 F1 | Measured at the head |
  |---|---|
  | counts 2 to 4: pushes onto faces holding 1, 2, 3 | 48,239 / 3,636 / 5,594 |
  | full queue pops and pushes in one clock, leaving head overwritten | 12,481 |
  | refused push with its drop | 352,294 arms in 80,719 drop clocks |
  | two faces dropping in one clock | 78,930 clocks |
  | counter saturation (drop clocks held at 0xFFFF) | 4,096 |
  | reset with arms queued / arms offered in reset | 36 / 366 |

  - The `AQ drive:` line is identical in the `--arm-queue-only` run and in the full default run (`receipts/aq/aq-head-none.log`, `receipts/suites/pp_top-make-run.log`).
  - It is also identical on `main`'s RTL (`receipts/aq/main-rtl-none.log`; all AQ lines `diff`-equal).
- **Independence from the RTL.**
  - `ArmQueueModel` (`sim_main.cpp:722`) is eight `std::deque` FIFOs fed from the face taps (the forced nets). It compares only the registered port, its valid and the drop counter, and reads no ring index or entry.
  - AQ4 (`:13940`) reads only the model.
  - The model passes on the shift-queue RTL of `main` and on the ring at the head. It is therefore not shaped to either implementation.
  - Every arm carries a serial deadline (`drive_arm_faces`, `:13844`), so a misplaced, overwritten, lost or repeated arm is visible.
- **Controls.**
  - `edit_identity.py` shows that each of the nine `armq_*` arms plants a top byte-identical to the matching `gen.py` control (9 of 9, `receipts/static/edit_identity.log`).
  - The five round-1 ring arms name AQ2 and AQ3. The four new arms name AQ3, and the campaign requires every named check to fail.
  - `acmp_mutants.py --jobs 7` gives 33 of 33 KILLED with the four goldens PASS (`receipts/campaigns/acmp_mutants.log`).
  - Every arm fails the count its README records. `armq_*`: 72, 3, 12, 3, 3, 1, 1, 1, 1. The 14 `tb/pp_top` ACMP rows, 9 `tb/acmp_listener` rows and the `rx_validator` row (27) are all equal.
- **Suites at the head.**
  - `tb/pp_top` `make run` (five builds): 10,420 checks, 0 failures. That is +2 over round 1's 10,418 (AQ3, AQ4).
  - `tb/acmp_listener`: 3,111 of 3,111.
  - The `tb/pp_top` build's warning set is identical to the round-1 bench's, with no new warning.

### Docs: CLEAN (R1 RESIDUE recorded)

- **No pointer to an unpublished bench remains.**
  - 09 §8.8 (`09_verification.md:388-400`), `tb/pp_top/README.md` section AQ (`:1982-2072`), the ACMP-controls paragraph (`:1959-1962`) and `acmp_mutants.py:164-169` all describe the in-tree drive.
  - A search of the tree for "lockstep", "unpublished" and "pull request" finds no #639 text that points at an out-of-tree bench.
- **The figures and claims in section AQ and in 09 §8.8 match the runs above.** That covers the edges, arms, reach table, nine control counts, the red proof and "passes on `main`'s RTL".
- **S1 banner.** It reads 1,152 at `5c71928a`, consistent with the PR body's census, and 1,153 at `631eeb34`, which is the figure in the issue #639 body.
- **The published lockstep benches regenerate as stated.**
  - Following the packet README's steps, all 19 `GENERATED.sha256` inputs regenerate byte for byte (`receipts/static/lockstep-generated-check.log`).
  - `SHA256SUMS` matches 184 of the 186 published files. The two mismatches are `armq/build.sh` and `lsn/build.sh`, which the publisher path-redacted. `MANIFEST.json` lists their original digests, and those equal `SHA256SUMS`, so the mismatch is a disclosed redaction, not a defect.
- **`make check`** passes in a git clone at the head: 1,134 links, 115 REQ rows, 94 matrix rows with 0 untested, and 28 parameters (`receipts/static/make-check.log`). `gen_matrix.py --check` passes. In an exported tree, the stale-figure check misfires on archive mtimes; the clone run is the verdict.
- **Merged `hdl-engineer.md` §3.1.** PR #154's SRP paragraph and this lane's "A few memories" paragraph read as two separate, consistent paragraphs (`:84-106`).

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #639 body, assignment 5976100204 and round-2 assignment 5981052216; `git diff 9e869910 1cba30c9 -- hdl/` (comment-only); lane HDL vs `main` `07b1469`; arm-port lockstep re-run from the head's cut (32 × 1M, 0 mismatches; 6 controls 8/8; probe 0/8); listener blob identity; `acmp_listener` on head and `main` RTL | R462-2 | `1cba30c91bbc4c0e20343f883b94c3f701cc0dbc` |
| RTL | CLEAN | `protocol_processor_top.sv:2948-3049`; `KL_pp_acmp_listener.sv:379-412,740-770,1032-1075`; lint of both tops (0 warnings); `git merge-tree` of the manager merge (tree identical) | R462-2 | `1cba30c91bbc4c0e20343f883b94c3f701cc0dbc` |
| Robustness | CLEAN | R462-1 `aq_probe.sh` ×2 unchanged (rc 1, AQ3); `gen.py` 9 controls (all fail AQ3) + `hd_not_reset` (passes); red proof ×4 on round-1 bench (pass); 6 own controls (all AQ3); force targets and generated-model force wiring | R462-2 | `1cba30c91bbc4c0e20343f883b94c3f701cc0dbc` |
| Tests | CLEAN | `tb/pp_top` AQ3/AQ4, `ArmQueueModel` and `drive_arm_faces` (`sim_main.cpp:722`, `:13844`, `:13902-13944`); `pp_top_wrap.sv:491-507,889-961`; `acmp_mutants.py` (33/33 KILLED, counts equal README); edit identity 9/9; `tb/pp_top` `make run` 10,420/0; `tb/acmp_listener` 3,111/0; AQ on `main` RTL identical | R462-2 | `1cba30c91bbc4c0e20343f883b94c3f701cc0dbc` |
| Docs | CLEAN (R1 RESIDUE) | 09 §8.8; `tb/pp_top/README.md:940-952,1955-2072`; `acmp_mutants.py:164-232`; banner `:2994-3007`; `hdl-engineer.md:84-106`; PR body; published lockstep packet (`GENERATED.sha256` 19/19, `SHA256SUMS` 184/186 with 2 disclosed redactions); `make check`, `gen_matrix --check` | R462-2 | `1cba30c91bbc4c0e20343f883b94c3f701cc0dbc` |

## Real limits

- **Not run, as outside this reviewer's allowance:**
  - `run_suites.sh` (all 33 suites), `lint_hdl.sh` over all 41 modules, and `syn/yosys/run.sh`.
  - Campaigns other than the ACMP one: notify, ctr, aecp, aecp_dispatch, d3, gsi, name_wr, adp, maap.
  - The parent consumer set and Vivado.

  Round 2 changes `hdl/` by one comment only, and changes `tb/pp_top` by a drive that runs only inside `run_arm_queue`. That run is the last stimulus of the default build, so other sections' runs are unaffected. The manager's source banks at this head are the evidence for the rest.
- **The manager's source-bank receipts were not found published.** The assignment cites milan-fpga `f0e730f8` `review-evidence/pp639-r1/`. At that commit the directory holds only the round-1 author packet. The branch head `b95bc644` adds the Vivado receipts, both round-1 reviews and the round-2 author packet, but no manager bank log for `1cba30c9`. Their pass is taken from the assignment, not verified.
- **Not re-derived:** the "1,152 flops at `5c71928a`" in the S1 comment is the author's census. The cell census is not published, so it was checked only for consistency with the PR body.
- **The listener lockstep matrix was not re-run.** It was regenerated byte for byte, and the listener RTL is unchanged since the candidate it ran on.
- **Hosted CI at the exact head**, read at review time (`receipts/github/checkruns-1cba30c9.json`): `docs-gates` and `portability` succeeded in both workflow runs, and both `suites` jobs were still `in_progress`.
- **Build parallelism.** Builds used the pinned simulator 5.050 (identity verified), through a wrapper that only caps a build's own `-j 0`.
- **Redaction.** The pinned simulator's home-directory install prefix was replaced by `<VERILATOR_ROOT>` / `<SIM_PREFIX>` in the 40 receipt files listed in `receipts/REDACTED-FILES.txt`. Nothing else in the receipts was edited.
- **Shared host.** The load average was 60-85 from other units throughout. Every golden passed.
- **Clone integrity.** All probes ran on exported copies under `scratch/`. The review clone is at `1cba30c9`, with tree and index `c81e4a5e`, a clean worktree and no untracked or ignored files (`receipts/static/clone-integrity.txt`). This repository has no gitlinks, so none were required.

## Pending manager duties

- **Parent consumer set of 17** at dev `6c22d3ca` + c8, p2-p1, c10 and 232 with this head pinned. This includes the port-contract gate's inventory of 297 test-only hierarchical observations.
  - This review confirms the +41 is exactly the drive's `force` targets: hierarchical `u_dut.` references in the wrap go from 157 at `9e869910` to 198 at the head, and all 41 are `force` lines (`receipts/static/wrap-hier-counts.txt`).
  - It is an inventory, not a ratchet. The parent gate itself was not run here.
- **Final current-dev candidate build at the merge turn.** Source base `5c71928a`, live dev `6c22d3ca`.
- **Gate-related duties at the adoption pin:**
  - re-record the resource gate's baseline (#639's "same reviewed change");
  - bank PR #153's xvlog finding in the parent's `scripts/xvlog.budget`;
  - gate 16 T30 against #643.
- **Hosted and act acceptance at the exact head.** The `suites` jobs were in progress when read.
- **Carry RESIDUE R1** (PR-body opening paragraph) to the residue checklist.
- **Physical calibration NOT RUN.** No hardware was used, and field skips are not hardware proof.

R462-2 FINISHED
