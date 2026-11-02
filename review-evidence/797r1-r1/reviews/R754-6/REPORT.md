[R754] POSITIVE - exact head 2c500d0a9c3eb0ef0c764db6978bf8d0ab217ea2

Round R754-6, external independent review of issue #797 / PR #825. Head `2c500d0a9c3eb0ef0c764db6978bf8d0ab217ea2`, tree `eb629ae988ba3f1e9ef2a15969d39cd5216f76a8`. I reviewed the round 6 delta `ef7dc985..2c500d0a`: one commit, `scripts/register_read_sweep.py` only, +21/-11. I also checked whether the round 5 finding (R753-5 F1 / R754-5 F1) is fixed at its cause.

All five lenses are covered clean at this head. There is no open BLOCKER, MAJOR or MINOR, and no new RESIDUE. Two optional SUGGESTIONS are listed below.

## What the delta does

- **New SRP state 6** (`scripts/register_read_sweep.py:360-362`): a poll is answered (`answer_srp()`), then a provisioning `STRMW_CTRL` write goes out (`wr(0x810, ...)`). `srpw` records whether `o_srp_ctx_we` rose. The write is not answered before the reads.
- **Steal states renumbered:** the old states 6 and 7 are now 7 and 8 (`:363-364`).
- **Loop bound:** 8 becomes 9 (`:342`).
- **Comments:** the harness comment (`:350-359`) and the docstring (`:17-26`) now list the orders the states drive. They also explain why state 8 must run last.
- **Nothing else changed:** no change to the page, the JSON, the RTL, the generator or any gate (`receipts/delta_hygiene.txt`, `receipts/delta_ef7dc985_2c500d0a.diff`).

## Round 5 finding at its cause

R753-5 F1 and R754-5 F1 (MINOR, Tests) found that no swept state separated the clear of `srp_fresh_r` on a provisioning `STRMW_CTRL` write (`hdl/common/csr/milan_csr.sv:3128`). A mutant that drops that clear (m4) passed the sweep, because every write the sweep posted was answered or preceded the poll. The write-answer clear (`:3115`) then hid the missing `:3128` clear.

**At this head, state 6 drives exactly the missing order.** The poll grant sets `srp_fresh_r` (`:3117`). The provisioning write should clear it (`:3128`). No write answer follows (`:3115` does not run), so only `:3128` can clear the word before the reads.

- **The harness record reads the page's words:** `srppoll = ans_poll && at_ans > at_selwr`, so after the write `srppoll` is 0 (`:378`).
- **The page predicts 0:** the clause "the SRP table's latest answer to the window was a poll, after the last `STRM_SEL`/`STRMW_CTRL` write, ..." at `REGISTER_MAP.md:3462`, `:3483`, `:3639` and `:3640` gives 0 for this state.
- **The pending write is answered after the reads** by the existing flush (`:401`), so it does not leak into the next iteration.

All verification items, rerun by me on `git archive` extracts of the head with Verilator 5.050 (`receipts/verilator_version.txt`):

| Probe | Sweep | RTL | rc | Disagreements | Receipt |
|---|---|---|---:|---:|---|
| head | head | head | **0** | 0 (ship and 2x2; 17 tables, 54,007 reads each) | `receipts/sweep_head.log` |
| m4: `:3128` clear removed | head | m4 | **1** | 144 | `receipts/sweep_m4.log` |
| m1: steal clear `:3132` removed | head | m1 | 1 | 144 | `receipts/sweep_m1.log` |
| m2: write answer sets instead of clears, `:3115` | head | m2 | 1 | 288 | `receipts/sweep_m2.log` |
| m3: write-answer clear `:3115` deleted (the R753-5 p3 form) | head | m3 | 1 | 144 | `receipts/sweep_m3.log` |
| m5: `STRM_SEL` clear `:3119` removed | head | m5 | 1 | 96 | `receipts/sweep_m5.log` |
| round 4 wording planted back (page at `79fdea05`) | head | head | 1 | 288 | `receipts/sweep_oldpage.log` |
| control: m4 under the **previous** sweep `ef7dc985` | prev | m4 | 0 | 0 | `receipts/sweep_prev_m4.log` |

- **m4 fails only in state 6.** All 144 m4 disagreements have the signature `srp=1 srpw=1 srppoll=0 srpsteal=0 srpsince=0` (`receipts/m4_breakdown.txt`): `STRMW_SRP` ship 24 and 2x2 72, `STRMW_SID_LO` and `STRMW_SID_HI` 24 each on 2x2.
  - Only state 6 leaves a poll-set word that `:3128` alone must clear.
  - States 2 and 3 answer the write they post, so the write-answer clear runs.
  - States 4 and 5 give `srppoll=1`.
- **The control shows the delta is the cause.** m4 under the `ef7dc985` sweep stays at rc 0, so the new state is what catches m4.
- **Read count:** 54,007 reads per build matches 9 states. Each stream table gets 2160 reads = 2 x 2 x 5 x 2 x 9 x 2 x 3.
- **Row coverage:** every 2x2 read row is hit at least once. Ship has 6 zero-hit rows, the count the PR body gives for rows above index 0 that are never reached (`receipts/head_totals.txt`).
- **The docstring states the orders driven.** I mapped the docstring against the state code:
  - "no answer" (0); "a poll answered" (1); "a provisioning write answered, alone or then a poll answered" (2, 3);
  - "a write posted, then a poll answered, then the write answered or left unanswered" (4, 5, through `wr_ctrl_answered` `:282-297`);
  - "a poll answered, then a write posted and left unanswered" (6); "a poll answered, then a beat another master used, alone or then a poll answered" (7, 8).
  - The carry-in sentence is also true. The outer loops step after state 8 (snap 1, ks 2), which ends in a poll answer with no write pending. The next state 0 opens with a `STRM_SEL` write and answers nothing. No other state reads a poll answered before the selection with nothing after it: state 1 re-polls, state 2 writes and answers, and the state 6 to 7 boundary is preceded by the flush's write answer.
  - The m5 result (rc 1) confirms this ordering still exposes the `:3119` clear.

**Disposition: R753-5 F1 and R754-5 F1 are RESOLVED at this head.**

## Author evidence cross-check

- **Byte-identical reproduction:** the author's published round 6 sweep logs (`review-evidence/797r1-r1/author-r6/receipts/sweeps/sweep_{head,m1,m2,m4,m5,round4}.log` at evidence commit `f4a3fb86`) match my reruns byte for byte.
- **Manifest hashes:** each of those logs matches the `published_sha256` in the evidence `MANIFEST.json` (`receipts/evidence_commit.txt`).
- **Same mutants:** the author's mutant patches are identical to the round 5 patches.
- **No git signature:** neither the evidence commit nor the head carries one. Integrity here rests on the manifest hashes and the byte-identical reruns, not on a signature.
- **Superseded first attempt:** the author's `sweeps_first_attempt/sweep_m5.log` (12,741 bytes, the size of a 0-disagreement log) supports the PR body's account. Appending the new state last hid m5, and the published order fixes that.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE.

### S1 - SUGGESTION - Tests, Robustness - `scripts/register_read_sweep.py:350-359`, `:342` - the `STRM_SEL`-write clear is read only through loop carry-in

- **Evidence:** m5 (`:3119` removed) is caught only by state 0 of each pass that follows state 8. The author's first attempt shows that one reordering hid it (rc 0). The comment at `:356-357` now states the dependency, and the author lists it as an open risk.
- **Impact:** none at this head (m5 gives rc 1). A future reorder or a new appended state could silently drop the only state that separates `:3119`.
- **Optional outcome:** add a dedicated state, for example a poll answered, then a `STRM_SEL` write to the same selection, then the reads, so that the clear does not depend on loop order. Or make the sweep refuse when no read had `srpsince=0` after a poll answered before the last selection write.
- **Verification:** m5 exits 1 under any order of the states.

### S2 - SUGGESTION - Docs - `scripts/register_read_sweep.py:24-26`, `:356-357` - "pass" is not defined

- **Issue:** the docstring and the comment say "each pass after the first", but "pass" is not defined. It means one run of the `srpmode` loop for one selection and ACMP setting. "that last poll answer" in the docstring relies on the reader taking "last" as state 8's.
- **Optional wording:** "Each run of the SRP states after the first opens, in state 0, with a `STRM_SEL` write that follows the previous run's final poll answer (state 8), and nothing answered after it".
- **Why not RESIDUE:** the current text is not false, so this is optional clarity.

### Prior suggestions and residue carried

- R754-5 S1 (the `srp` comment at `:358` says "since the selection"; true for the new state 6, unchanged) and R754-5 S2: optional, not taken.
- R753-5 S1 ("since" anchor in `register_descriptions.json:4086-4087`): optional, not taken. The JSON and the page are unchanged in the delta.
- R754-4 S1, S2 and R753-4 S1-S4: optional, not taken.
- R753-3 RES2 (`REGISTER_MAP.md:4503`), R753-3 RES3 (`CSR_REGISTER_NOTES.md:974`) and R754-3 R1 (`CSR_REGISTER_NOTES.md:78`): retained as RESIDUE on the manager's list. They are untouched by the delta (only the script changed).

### Residue check of the delta

- **None new** (`receipts/delta_hygiene.txt`).
- The added lines contain 0 non-ASCII characters and no bench lane label, lane name, review round, reviewer ID or comment ID.
- The new comments state behaviour.
- The commit message is one line with `(#797)` and no trailers.
- `git diff --check ef7dc985 HEAD` exits 0.

## Lens results (each applied at `2c500d0a`)

```text
[R754] PASS Conformance - REGISTER_MAP.md:3462,3483,3639,3640 vs milan_csr.sv:3108-3133; receipts/sweep_head.log - the SRP-served clause holds in all 9 SRP states on both builds (0 disagreements). The new state 6 is the case the clause words as "after the last ... STRMW_CTRL write", and the head RTL reads 0 there as printed. Page and RTL are unchanged since ef7dc985 (delta_hygiene.txt), so the other rows keep the R754-5 clean result
[R754] PASS RTL - hdl/common/csr/milan_csr.sv (byte-identical to ef7dc985; diff empty) at :3086-3136 - the five srp_fresh_r clears (:3109, :3115, :3119, :3128, :3132) are each now shown live by a mutant that exits 1 (m1-m5). The delta changes no RTL or anything the RTL verdict depends on
[R754] PASS Robustness - register_read_sweep.py:360-364, :401; receipts/sweep_head.log, sweep_m5.log - the new pending-write state is flushed after its reads (:401) and does not perturb later states (head rc 0). The carried-in STRM_SEL-clear state still separates m5 (rc 1). Out-of-range and index-0-talker selections in state 6 post nothing (srp_prov_w, milan_csr.sv:3091-3093) and read the fallback rows without disagreement
[R754] PASS Tests - register_read_sweep.py:342,350-364,378; receipts/sweep_{head,m1,m2,m3,m4,m5,oldpage,prev_m4}.log, m4_breakdown.txt - head rc 0 on both builds. Every srp_fresh_r clear mutant and the round 4 wording exit 1. m4 fails only in the new state, and stays rc 0 under the previous sweep, so the added test can fail for the defect it targets
[R754] PASS Docs - register_read_sweep.py:17-26 and :350-359 vs the state code at :360-373 and :282-297; PR #825 body "Round 6" section - the docstring and the harness comment state the orders actually driven and the ordering dependency. The PR body's round 6 counts (54,007 reads; m4 144, m1 144, m2 288, m5 96, round 4 wording 288) match my reruns exactly. No page, JSON or description change was needed
```

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `REGISTER_MAP.md:3462,3483,3639,3640`; `milan_csr.sv:3108-3133`; `receipts/sweep_head.log` | R754-6 | `2c500d0a9c3eb0ef0c764db6978bf8d0ab217ea2` |
| RTL | CLEAN | `milan_csr.sv:3086-3136` (unchanged since `ef7dc985`); `receipts/sweep_m{1,2,3,4,5}.log` | R754-6 | `2c500d0a9c3eb0ef0c764db6978bf8d0ab217ea2` |
| Robustness | CLEAN | `register_read_sweep.py:360-364,401`; `milan_csr.sv:3091-3093`; `receipts/sweep_head.log`, `sweep_m5.log` | R754-6 | `2c500d0a9c3eb0ef0c764db6978bf8d0ab217ea2` |
| Tests | CLEAN | `register_read_sweep.py:342,350-364,378`; all eight sweep receipts (`sweep_m3.log` included); `receipts/m4_breakdown.txt` | R754-6 | `2c500d0a9c3eb0ef0c764db6978bf8d0ab217ea2` |
| Docs | CLEAN | `register_read_sweep.py:17-26,350-359`; PR #825 body "Round 6" | R754-6 | `2c500d0a9c3eb0ef0c764db6978bf8d0ab217ea2` |

## Real limits

- **Block-level evidence only.** The sweep elaborates `milan_csr` alone. The shipping datapath ties the SRP grant and the steal input to 0, so the SRP-answered states exist only in the harness.
- **Not run by me:** full Verilator suites, Yosys, the parent/PP/gPTP banks, the docs-workflow steps, generator `--check`/`--selftest`, hardware and Vivado. The generator inputs are unchanged in the delta, and the author's receipts (`author-r6/receipts/lane/gen_*`, `gates/`) are the source-head evidence for those.
- **Physical calibration NOT RUN.** Field skips are not hardware proof.
- **No manager source bank** runs at this head, and none is claimed or inferred.
- **Base history:** the head contains `1f29f189` (merge of PR #822 into dev), a descendant of the stated source base `1e80128f`. The author records the merge base with dev as `1f29f189`. Live dev `503bc97c` is not merged.
- **Hosted contexts at this head were still running** when snapshotted (`receipts/hosted_checks_snapshot.txt`). Completed successes: `bdd-conformance`, `changes`, `docs-check-no-git`, `wire-accountability`, `Prepare pinned Yosys`. In progress or queued: `docs-gates-*`, `elaborate-gates-*`, firmware jobs, `verilator-lint`, `yosys-elaboration`, `full-ci-gate`, `publication-census`. That is not an executed result.

## Pending manager duties

- Build and validate the current-dev merge candidate (live dev `503bc97c`) with the builder and native banks, and link the receipts.
- Accept the exact-head hosted and act contexts once they finish.
- Carry R753-3 RES2, R753-3 RES3 and R754-3 R1 on the residue checklist.
- Obtain explicit maintainer authorization before any merge.

## Clone integrity after probes

`receipts/clone_integrity.txt` checks the clone after the probes. All probes ran on `git archive` extracts under the packet's `scratch/`, and the review clone was never modified.

- HEAD and the index tree equal `2c500d0a` / `eb629ae9`.
- The worktree is clean.
- The `ls-files -s` modes and blobs are identical to `ls-tree -r HEAD`.
- All six gitlinks (`external`, `gptp-processor`, `protocol-processor`, `third_party/lwSRP`, `third_party/tsn-c-stack`, `third_party/verilog-axis`) are as recorded at HEAD.

Scripts: `setup_trees.sh` (extract and patch), `run_probes.sh` (seven sweeps, two at a time), `run_m3.sh`.

R754-6 FINISHED
