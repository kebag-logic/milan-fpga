[R398] POSITIVE - exact head 99bfd4bc3180bab97d47f63056513fb39eea6a37

# R398-4: confirmation round for processor PR #133 (lane C1), same head as R398-3

Head `99bfd4bc3180bab97d47f63056513fb39eea6a37`, tree `d8ec1053bf0968ed462d8a419a0cf859c41e9c3c`. There has been no commit since R398-3: `refs/pull/133/head` and the PR's `headRefOid` are both `99bfd4bc`. This round judges only my R398-3 F1, which was addressed by a PR-body amendment with no source change.

## Verdict

**POSITIVE. R398-3 F1 is RESOLVED, and no MINOR, MAJOR or BLOCKER finding is open.**

- **The fix.** The composed-head note, item 1, no longer calls the two lists' parent edits disjoint. It names every `tb/verilator/milan_dp/README.md` update of both lanes, to be made in one edit of that file: `:443`, `:528-530`, `:633-637` and `:877-883`. That is option 1 of F1's required outcome, word for word in substance.
- **Nothing else changed.** Since the revision I reviewed in R398-3, the body has one changed region, inside item 1. The closing references are still exactly #29, #64, #65 and #108.
- **The source is the same bytes.** A focused confirmation on it passes: `srp_top` 2200/2200, ARMDELAY 0 own LeaveAlls at arm delays 3, 4, 8 and 16, and `make check`, `gen_matrix --check` and `git diff --check` all rc 0.

## 1. How this round was reconstructed

1. **Governance and scope.**
   - Governance is unchanged at this head. The repository has no `AGENTS.md`, no `CONTRIBUTING.md` and no submodules (0 gitlinks), so `README.md`, `docs/README.md`, the `Makefile` gates and `scripts/run_suites.sh` govern, as in R398-3.
   - Issue #108 has no comment since 12:00Z today (`receipts/public_thread_state.txt`).
   - The review-start comment 5891715799 restates the rules of the review.
2. **My own round-3 report.** I read my R398-3 report, which states F1, its required outcome and its verification.
3. **The PR body and its public edit history.**
   - I rebuilt the body's revisions from the public edit history: four revisions (`receipts/body/edit_history.txt`).
   - **The body I reviewed in R398-3** is revision 12:13:58Z. It was in place from before R398-3's start comment (12:29:09Z) until after R398-3's publication (13:51:22Z).
   - **The body under review now** is revision 13:52:15Z. It is byte-identical to the current body read through the pulls API, apart from one trailing LF (`receipts/body/current_equals_latest.txt`).
4. **The authorities.**
   - PR #132's body, "Parent-visible for pin adoption: rounds 1-6, consolidated".
   - The parent `tb/verilator/milan_dp/README.md` at dev `79c36963`, read through the public API. It is blob `3f05559f`, the same blob as in R398-3 (`receipts/parent/`).
5. **The diff.** `git diff c951a9ff..99bfd4bc` is unchanged, because the head is the same. The review clone's tree and index equal `d8ec1053`.
6. **Order of reading.** I wrote my verdict draft (`receipts/independent_verdict_draft.md`, 16:00:27 local) before I checked the public thread for review findings. No review finding has been posted since R398-3.

## 2. R398-3 F1 at this head

**F1 as filed in R398-3 (MINOR, Docs).** The composed-head note said "The two lists touch no common parent file". It named only this lane's `milan_dp/README.md` edits (`:443` and `:528-530`), and missed the README updates that #132's harness edits imply:
- the walk-starter list at `:633-637`;
- the retired `[AECP]` degrade arm at `:877-883`.

**What the required outcome asked for (option 1).**
- Name the `:633-637` and `:877-883` edits, to be made in the same edit of that file as `:443` and `:528-530`.
- Replace "touch no common parent file" with an accurate statement: the code edits share no file, and the README updates meet in `milan_dp/README.md`.

### The body now (item 1, lines 225-228)

> The two lists' code edits share no parent file. Their documentation updates meet in `tb/verilator/milan_dp/README.md`, which the adoption lane edits once for both (R398-3 F1):
> - this lane's `:443` `[C]` row and `:528-530` sentence (section 4);
> - `:633-637`, the walk-starter list, which gains the harnesses PR #132 adds the `PP_CTRL[1]` walk to (`gmstep`, `gptp`/`gptp-lat` and `ax1x1gptp`);
> - `:877-883`, the `[AECP]` degrade-arm paragraph, rewritten for the two hold checks that replace that arm in every `sim_nxn.cpp` leg.

### The checks

| Check | Result | Receipt |
|---|---|---|
| No sentence says the lists' adoption edits share no parent file | PASS. The only match is the qualified "code edits share no parent file". | `receipts/body/f1_check_current.txt` |
| The note names all four README locations, edited once for both lanes | PASS: `:443`, `:528-530`, `:633-637`, `:877-883`, "edits once for both" | same |
| The cited parent lines hold what the note says (blob `3f05559f` at `79c36963`) | PASS. `:443` is the `[C]` row. `:528-530` is the issue-108 sentence. `:633-637` is the walk-starter list, ending "`sim_main`, `sim_nxn`, `sim_aclk` and `milan_dp_render` now set it at boot". `:877-883` is "The `[AECP]` checks in `sim_nxn.cpp` grade that path … padded to 60." | same; `receipts/parent/milan_dp_README_79c36963.md` |
| The substance matches PR #132's consolidated list | PASS. #132 adds the `PP_CTRL[1]` walk to `gmstep` (`sim_gmstep.cpp`), `gptp` and `gptp-lat` (`sim_gptp.cpp`) and `ax1x1gptp`. It retires the `[AECP]` degrade arm "in every `sim_nxn.cpp` leg", and "Two hold checks replace it". | PR #132 body (read through the API) |
| "Code edits share no parent file" is true | PASS. This lane's code edit is `sim_crf_licence.cpp:953,956`. #132's are `KL_pp_shadow.sv` glue, `sim_gmstep`, `sim_gptp`, `sim_ax1x1gptp`, `sim_main`, `sim_aclk` and `sim_nxn` `.cpp`, and the firmware `nvm_boot()` path. No file is in both lists. | the two bodies |
| Control: the same checker on the R398-3 revision | FAIL (rc 1), on the disjointness sentence and on every README-entry token. The checker tells the two bodies apart. | `receipts/body/f1_check_round3_control.txt` |
| Only item 1 changed since R398-3 | PASS. One changed region: old line 225 is replaced by new lines 225-228, between item 1's sub-list and the item-2 heading. The only other difference is one trailing blank line at the end of the body (whitespace). Items 2 and 3, and every earlier section, are byte-identical. | `receipts/body/scope_check.txt`, `receipts/body/round3_to_now.diff` |
| Closing references are exactly #29, #64, #65 and #108 | PASS. Body lines 3-6 read "Closes #29", "Closes #108", "Closes #64", "Closes #65". The public closing-issue references are the same four. | `receipts/body/f1_check_current.txt`, `receipts/body/closing_refs.json` |
| The combined consumer comment 5890073527 is unchanged | PASS (`updated_at` equals `created_at`, 12:13:48Z) | `receipts/public_thread_state.txt` |

**F1: RESOLVED.** No rerun was required, because no source changed. I still ran a focused confirmation (section 3).

## 3. Source confirmation at the same head

- **Tool.** Verilator 5.050 (`2026-07-01 rev v5.050`); `verilator_bin` sha256 `44898b22…`, the same install as R398-3 (`receipts/confirm/tool_and_head.txt`).
- **Where it ran.** A disposable clone under `scratch/`, checked out at `99bfd4bc`, tree `d8ec1053`.

| Command | rc | Result |
|---|---:|---|
| `make -C tb/srp_top -j8` | 0 | 2200 checks, 2200 PASS. ARMDELAY `own_msrp=0 own_mvrp=0` at delays 3, 4, 8 and 16 (`receipts/confirm/srp_top.log`) |
| `make check` | 0 | the REQ matrix (115 rows, OK), the module matrix (94 rows, 0 untested) and parameters 26/26/26 (`receipts/confirm/make_check.log`) |
| `python3 scripts/gen_matrix.py --check` | 0 | `receipts/confirm/gen_matrix.log` |
| `git diff --check c951a9ff..99bfd4bc` | 0 | empty |

**Hosted checks at the exact head** (read-only; the manager owns acceptance). Workflow `hdl` ran twice: run 36558392722 (pull_request) and run 36558385720 (push). All six check runs completed with success: `suites`, `docs-gates` and `portability` in each run (`receipts/hosted_check_runs.txt`). As I recorded in R398-3, the only skipped steps are the Verilator build steps, skipped on a cache hit.

## 4. Findings

**No open MINOR, MAJOR or BLOCKER finding.** This round raises no new finding.

State of the earlier findings at this head:

| Finding | State at `99bfd4bc` | Evidence |
|---|---|---|
| R398-3 F1 (MINOR, Docs): the combined list leaves `milan_dp/README.md` half-updated and calls the lists disjoint | **RESOLVED** | section 2 |
| R398-1 F1, R398-1 S1-S3, R399-1 S1 and S3, R399-3 F1 | RESOLVED (as in R398-3) | source and body unchanged outside item 1 |
| R398-2 S1 = R399-2 S1 (a dropped LeaveAll re-arm silences that application's own LeaveAll) | RETAINED, SUGGESTION | source unchanged |
| R398-2 S2 = R399-2 S2 (no committed `now_ms` wrap check) | RETAINED, SUGGESTION | source unchanged |
| R399-2 S3 (superseded counts in the first tables of `tb/srp_top/README.md`) | RETAINED, SUGGESTION | source unchanged |
| R399-3 S1 (no in-tree full-top check of C1 under #132's hold) | RETAINED, SUGGESTION | source unchanged |
| R399-4 S2 (same substance as R398-3 F1) | RESOLVED by the same amendment | section 2 |

**A note for the adoption lane.** This is not a finding, and it is outside F1's required outcome. The parent paragraph that holds `:877-883` opens at `:869` ("This suite backs no descriptor memory, on purpose and on record."), and its `:869-876` text is the premise of the `[AECP]` sentences. R398-3 recorded that `:869` is already inaccurate at `79c36963` and attributed it to neither lane. The one edit of this README will naturally rewrite `:869-883` as a whole.

## 5. Lens results

- **Conformance: CLEAN.**
  - This head is the same tree as R398-3's. Table 10-5 rLA!, the 10.7.5.20 scoping, the 10.7.5.22 stale-expiry guard, and the Milan Table 4.3 and 4.3.2 terms are graded as before.
  - Re-confirmed here: `srp_top` P1-P8, Q1-Q4 and R1-R4 pass 2200/2200, with ARMDELAY 0.
- **RTL: CLEAN.**
  - The tree `d8ec1053` is unchanged, so R398-3's merge-tree recomputation, lane provenance and shared-block identity all still hold.
  - The review clone's index tree is `d8ec1053`, with 0 rehash and 0 mode mismatches.
- **Robustness: CLEAN.**
  - The arm path, the drop behaviour and #132's hold admission are unchanged bytes.
  - The P8 arm-latency sweep passes again at this head.
- **Tests: CLEAN (SUGGESTIONs only).**
  - The focused `srp_top` suite passes 2200/2200, and the F1 checker has a discriminating control (PASS now, FAIL on the round-3 body).
  - R398-3's full suite and mutation results stand for the same bytes.
  - R399-3 S1 is retained.
- **Docs: CLEAN.**
  - F1 is resolved: the combined list covers both lanes' `milan_dp/README.md` updates, and the disjointness sentence is corrected. Every citation matches parent blob `3f05559f`.
  - `make check` and `gen_matrix --check` are rc 0, and the closing references are exact.

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | tree identity against R398-3; `srp_top` P1-P8, Q1-Q4 and R1-R4 at the head (2200/2200, ARMDELAY lines); docs 10 §6.2 and §6.5 unchanged | R398-4 (confirmation; full pass R398-3) | 99bfd4bc3180bab97d47f63056513fb39eea6a37 |
| RTL | CLEAN | HEAD, tree and index tree `d8ec1053`; 329 files rehashed, 0 mismatches, 0 mode mismatches, 0 gitlinks; `git diff --check` | R398-4 (confirmation; full pass R398-3) | 99bfd4bc3180bab97d47f63056513fb39eea6a37 |
| Robustness | CLEAN | unchanged arm-queue and hold-admission bytes; P8 arm-delay sweep at delays 3, 4, 8 and 16 | R398-4 (confirmation; full pass R398-3) | 99bfd4bc3180bab97d47f63056513fb39eea6a37 |
| Tests | CLEAN (SUGGESTIONs only) | `make -C tb/srp_top` 2200/2200; F1 checker with its control; hosted check runs at the head | R398-4 (confirmation; full pass R398-3) | 99bfd4bc3180bab97d47f63056513fb39eea6a37 |
| Docs | CLEAN | PR #133 body: revision 13:52:15Z against 12:13:58Z, and the current body; composed-head note item 1; closing references; PR #132 consolidated list; parent `milan_dp/README.md` blob `3f05559f` at `79c36963`; comment 5890073527; `make check`; `gen_matrix --check` | R398-4 | 99bfd4bc3180bab97d47f63056513fb39eea6a37 |

## 7. Real limits

- **Verilator path.** The supplied path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used a scratch wrapper around the same Verilator 5.050 install as R398-3 (`verilator_bin` sha256 `44898b22…`). The host default is 5.052 and was not used.
- **Scope of the rerun.** It was deliberately narrow: the `srp_top` suite, `make check`, `gen_matrix --check` and `git diff --check`. The full suite set, the mutation campaigns, lint and scoped `yosys` are carried from R398-3 on the identical tree. They were not rerun.
- **Parent reads only.** Parent files were read through the public API at `79c36963`. I built no parent, and I did not reproduce the manager's 16/16 combined bank or the donor 9/9.
- **The body history.** The comparison uses the platform's public edit history. The current body equals the newest revision apart from one trailing LF.
- **Hardware.** Physical calibration NOT RUN. Field skips are not hardware proof. No hardware was used.
- **Not run (not allowed):** full banks, act, and any GitHub write.
- **Redaction.** In the published `receipts/confirm/*.log`, the local tool install prefix is replaced by `<VERILATOR_5050_PREFIX>` and the scratch clone path by `<SCRATCH_CLONE>`. Nothing else in the logs is changed.
- **Clone integrity.** The review clone is byte-identical to the head, with a clean status and nothing ignored (`receipts/clone_integrity.txt`). All builds ran in a disposable clone under `scratch/`.

## 8. Pending manager duties

1. **Publish** this report, and collect the second independent review at this head.
2. **Merge-turn candidate.** Build the final current-dev candidate (source base `c951a9ff`, live dev `79c36963`). It is distinct from this source validation. The manager owns hosted and act acceptance.
3. **At pin adoption:**
   - the combined parent edits: #132's harness, glue and firmware items, and C1's crflic `>= 3` at `sim_crf_licence.cpp:953,956`;
   - C1's parent documents;
   - one edit of `milan_dp/README.md` at `:443`, `:528-530`, `:633-637` and `:877-883`. The surrounding `:869-876` should be taken into that one edit.
4. **Route the retained SUGGESTIONs:** R398-2 S1 = R399-2 S1, R398-2 S2 = R399-2 S2, R399-2 S3 and R399-3 S1.

## 9. Packet

- `REPORT.md` and `MANIFEST.sha256`.
- `scripts/`:
  - `f1_body_check.py` (the F1 criteria);
  - `body_scope_check.py` (proves the change is confined to item 1).
- `receipts/`:
  - `body/`: the body revisions, the history, the diff, the checks, the control and the closing references;
  - `parent/`: the README at `79c36963` and its blob;
  - `confirm/`: the tool and head, `srp_top`, `make check`, `gen_matrix`, `diff --check`;
  - `hosted_check_runs.txt`, `public_thread_state.txt`, `clone_integrity.txt` and `independent_verdict_draft.md`.

R398-4 FINISHED
