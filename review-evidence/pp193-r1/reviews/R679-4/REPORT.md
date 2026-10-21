[R679] POSITIVE - exact head 4f57e22006ca727abace93a0cb8585484a377352

# R679-4: independent round-4 review of processor PR #198 (Closes #193)

Head `4f57e22006ca727abace93a0cb8585484a377352`, tree `4fb74a342879c54b33e9da3d38cb267b53e7205e`. The branch and `refs/pull/198/head` both resolve to this commit (`receipts/env/clone-state.txt`). The round-4 delta is three commits on `47434635` (`4d27f70`, `4179599`, `4f57e22`). It changes tests and docs, plus comment lines in one RTL file.

**Summary.**
- All five lenses are CLEAN. No BLOCKER, MAJOR or MINOR finding is open.
- **R679-3-F1 is resolved.**
  - SH24 requires every Listener push of a walk to come before that walk's done strobe.
  - Its named control, `listener-walk-done-before-second-pass`, is KILLED on SH24.
  - My order probe reports LATE 0 of 72 at the head and LATE 32 of 72 with the control planted.
- **R679-3-S2 was applied in a different form, and the author's explanation holds.**
  - My R679-3-S2 suggestion rested on a wrong premise: that the rider's Empty would only be held back to the next walk. In fact, while the owner declares, the owner's transmit marks the rider in every walk, so the Empty never goes out.
  - With the extra tick alone, the control passes SH1. I reproduced this.
  - The committed VO check fails under the control. The head's rider behaviour is correct.
- **The remaining prior findings are applied:** R679-3-R1, R2 and S1, and R680-3-R1. The RTL change is comments only: 0 non-comment lines changed, and the listener converts to byte-identical Verilog.
- **Records for the residue checklist:** two RESIDUE items (PR text) and three SUGGESTIONs.

## Reconstruction (order followed)

1. **Repository instructions.**
   - This repository has no `AGENTS.md` or `CONTRIBUTING.md`.
   - I read `docs/README.md`, the listener banner, 10 §6.4 and both bench READMEs.
2. **Scope.**
   - Issue #193 body, the frozen acceptance: one declaring applicant per StreamID, a teardown withdraws only when no other settled sink declares, suite cases with planted mutants, and the suites and consumer gates passing.
   - The maintainer ruling on #193: owner election inside the per-sink plane.
   - The round-4 assignment `issuecomment-6320539946`, read exactly. Its items: (1) R679-3-F1 as required, with the named control and the order probe; (2) R679-3-R1 and R2 as written; (3) R679-3-S1 and S2, where S2 needs only a check; (4) R680-3-R1 as written. The RTL may not change unless the new check exposes a defect.
   - The author's REVIEW READY `issuecomment-6323586227`.
3. **Authorities.**
   - IEEE 802.1Q-2018 10.7.7 (one Applicant per attribute value), Table 10-3 (rLA!, tx!, txLA!), the 35.2.6 NOTE and 35.1.2.2.
   - Milan v1.2 4.2.7.2.2 (a peer registrar deregisters on Leave).
   - The interface authority is the `txop_done_o` port contract, `KL_srp_listener_fsm.sv:174`: "tick walk finished, pushes accepted". `KL_srp_top.sv:1164-1169` drains the encoder on the two strobes.
4. **Diff and history.**
   - I read `git diff 47434635..4f57e220` in full. `git diff 21601694..4f57e220` gives the PR context: 57 files.
   - I read the three commit messages, and the PR body as published at the head.
5. **Published evidence.**
   - `kebag-logic/milan-fpga@cb2f05c9`, `review-evidence/pp193-r1/author-r4`, checked against `MANIFEST.json`.
   - I read the prior public findings (R679-3, R680-3) only after my own pass and my own runs.

## Evidence integrity

- **Evidence archive.** Commit `cb2f05c92d46be00b95b29fafa609e38a1510bd2` carries no signature (`%G?` = N). Integrity therefore rests on `MANIFEST.json`. All 2,880 `author-r4` files are listed, and all 2,880 match their `published_sha256`: 0 bad, 0 missing, 0 unlisted (`receipts/env/evidence-check.txt`, `scripts/verify_evidence.py`).
- **Author's repo record.** The sha256 of every changed file in the author's `repo-record.txt` equals my clone's bytes (`receipts/env/clone-state.txt`). Its listener sv2v hash, `8f7f4e3b…`, equals mine.
- **Spot-checked author receipts.**
  - srp_top campaign rc 0: 209/209, coverage 132/132.
  - `compare/srp_top-arms.txt`: 182 arm runs unchanged, and seven rows changed as the README states.
  - Order probes: head LATE 0, control LATE 32, R679-3 arm LATE 32.
  - All seven round-4 head gate rc files are 0.
  - My own runs agree with each of these figures.

## Findings

### R679-4-R1 — RESIDUE — Docs (PR text): R679-3-R2's exact fix left a sentence whose subject is the reviewer

- **Where.** PR #198 body, Round 2 section, bullet "A handover to a slot the walk has passed (S2)". It reads: "R679-2 (F1) found that in a txLA! walk the LeaveAll re-declaration was lost instead, and corrects it (below)".
- **Cause.** The author applied my R679-3-R2 fix as written. The fix changed the subject of "corrects" from "Round 3" to the reviewer. The fix is in that wording, not in the author's application of it.
- **Impact.** Wording only. The text attributes the correction to the reviewer, while round 3 made it.
- **Exact fix.** Replace ", and corrects it (below)" with "; round 3 corrects it (below)".
- **Verification.** Read the revised sentence. No code, test or measurement changes.

### R679-4-R2 — RESIDUE — Docs (PR text): the Behaviour bullet on one transmit per walk omits the group mark's LA/LO exception

- **Where.** PR #198 body, Behaviour, "One transmit per walk (round 3)": "The walk marks every slot it passes and every member of a group whose applicant it serves, and a handover carries the applicant's mark…".
- **State of the other descriptions.**
  - The banner (`KL_srp_listener_fsm.sv:110-116`) and 10 §6.4 (`docs/architecture/10_srp_engine.md:644-647`) now state the exception (R679-3-S1).
  - The PR's Round 3 section states it only for txLA! → LO.
  - The RTL skips the group mark when the transmit leaves the applicant LA or LO (`KL_srp_listener_fsm.sv:1006`).
- **Impact.** Wording only. R679-3 found the exception suite-equivalent. The figures, tests and conformance claims are unchanged.
- **Exact fix.** After "every member of a group whose applicant it serves", insert ", unless the transmit leaves the applicant LA or LO, where a handover carries the mark instead". The bullet then matches the banner and §6.4.

### R679-4-S1 — SUGGESTION — Docs/RTL comment: the new clause and the old one state "a handover carries the mark" twice in one sentence

- **Where.** Banner `KL_srp_listener_fsm.sv:112-116` and 10 §6.4 `docs/architecture/10_srp_engine.md:645-648`.
  - The text reads: "…unless the transmit leaves it LA or LO, where a handover carries the mark instead; a handover carries the applicant's mark, and…".
  - This is my R679-3-S1 wording placed in front of the existing clause.
- **Accuracy.** The text is accurate. It matches `:1005-1010` (only the passed slot is marked) and `:1074` (the taker gets the giver's mark).
- **Optional tightening.** "…unless the transmit leaves the applicant LA or LO, where it marks only that slot. A handover carries the applicant's mark, so a handover during a walk never gives it two."

### R679-4-S2 — SUGGESTION — Docs: overlong line in the stream-FSM README

- **Where.** `tb/srp_stream_fsms/README.md:106`, 109 columns. The surrounding paragraph wraps near 76.
- **Optional fix.** Rewrap the SH1/SH2 sentences. The rendered output does not change.

### R679-4-S3 — SUGGESTION — Docs (PR text): the Round 3 section keeps the superseded premise about SH1's rider

- **Where.** PR #198 body, Round 3 section, the `listener-rider-not-quiet` paragraph: "its Empty cannot go out in that walk, … it fails 12 checks in all".
- **What round 4 established.** The Empty never goes out while the owner declares, not just "in that walk". The control now fails 15 checks.
- **Current state.** The Round 4 section already says so, and the README paragraph (`tb/srp_top/README.md:902-908`) is correct.
- **Optional fix.** Append "(superseded: see Round 4)" to that paragraph, so a reader of the history is not misled.

## Prior public findings on this PR, at this head

| Finding | Status | Evidence at this head |
|---|---|---|
| R679-3-F1, MINOR, Tests: the done strobe's wait for the second pass had no killing check | **Resolved** | **The check.** SH24 (`tb/srp_stream_fsms/sim_main.cpp:2101-2154`): taker sink 4, holder 7, handover at clocks 1-12 of a tx! walk (AN) and an own-LeaveAll txLA! walk (QA). It requires one message for SID0, equal to the model's, before the strobe; no push in the 60 clocks after it; and the taker holding the model state.<br>**The harness.** `step()` clears `join_tick_i`/`evt_valid_i` after each edge (`:238-241`), so no second walk starts in the window. Pushes are harvested before the edge and the strobe is read after it, so the before/after split is exact. `kTxopPollSteps` = 300 covers strobe + 60.<br>**The control.** `listener-walk-done-before-second-pass` is exactly `txop_done_o <= 1'b1` in W_DONE with `walk_r <= (&wdone_r) ? W_IDLE : W_EVAL` kept. It is registered in `mutants.py:257` with the named check `SH24:`. My campaign spot-check lists it KILLED, failures=2, tags=SH24 (`receipts/runs/camp.log`). My own planted suite run gives 1,420 PASS, 2 FAIL, both SH24: "tx! walk, clock 3: strobe at clock 9, before it '', after it '0/2'" and the txLA! row with '3/2' (`receipts/runs/ctl-order.log:27-28`).<br>**The order probe** (`probes/order_probe.py`, the R679-3 probe, unchanged; takers 0, 2 and 4, both walk kinds, clocks 1-12): head **LATE 0 of 72** (`receipts/runs/head-order.log`); control **LATE 32 of 72** (`receipts/runs/ctl-order.log`). For taker 4, the LATE rows are handovers at clocks 3-6, the second-pass window. That window lies inside SH24's range. |
| R679-3-R1, RESIDUE: review round named in README | **Applied as written** | `tb/srp_top/README.md:887`: "(the form before this change)". |
| R679-3-R2, RESIDUE: S2 finder in the PR text | **Applied as written** | PR body Round 2 section: "R679-2 (F1) found that…". The follow-on wording is R679-4-R1. |
| R679-3-S1, SUGGESTION: state the LA/LO exception | **Applied** (banner and §6.4, as the suggestion named) | Banner `:112-116` and §6.4 `:645-647`. The PR Behaviour bullet does not state it yet: R679-4-R2. The wording repeats itself: R679-4-S1. The change is comment-only; see the RTL lens. |
| R679-3-S2, SUGGESTION: SH1 no longer sees a non-quiet rider | **Applied in a corrected form**; the suggestion's premise was wrong | See "Assignment item 2" below. |
| R680-3-R1, RESIDUE: qualify the implementation-scope sentence | **Applied as written** | PR Behaviour: "The issue #193 implementation changes RTL only inside `KL_srp_listener_fsm`, whose ports are unchanged; the branch also includes the main merges for #192 and #199." The opening lists the merge of main 859b537b. |
| Earlier rounds (R679-1/2, R680-1/2/3 findings) | **Still resolved** | The delta changes no RTL logic (sv2v byte-identical). All 1,422 suite checks pass at the head, including SH10-SH23 and the walk-record arms (`receipts/runs/head-full.log`). Every control in my spot-check is KILLED with the README's counts. |

## The round-4 assignment's checks

### Item 1 — R679-3-F1 (Tests, Robustness): met

See the first row of the table above.

- SH24 also passes with the handover ahead of the walk, at clocks 1-2: the message goes from sink 4 in the first pass. It passes with the handover after the walk has ended, at clocks 11-12, with the strobe at clock 10. So the check is not limited to the second-pass case.
- `done_at >= 0` is required, so a walk that never ends fails it.

### Item 2 — R679-3-S2 and the rider (Tests, Conformance): the author's explanation is correct, and the committed check is sound

**Reproduced.** `probes/drop_sh1_vo_check.py` removes only the new VO check and keeps SH1's 4-tick `ticks_follow_the_model`. With `listener-rider-not-quiet` planted, the suite then gives 14 FAIL and **no SH1 failure**; the control is still killed on SH14 (`receipts/runs/rider-novo-mut.log`). With the committed check, the same control fails 15 checks, including "SH1: … still VO (rider LO)" (`receipts/runs/rider-mut.log:27`).

**Measured with the control** (`probes/rider_probe.py`, `receipts/runs/rider-probe-mut.log:42-53`):
- The rider goes VO → LO on rLA! and stays LO for all 8 ticks.
- Every tick sends exactly the one-applicant model's messages: '3/2', '3/2', then nothing.
- After the rider's own A8, three more ticks send nothing either.
- Summary: wire-diffs 0, rider-not-VO-ticks 8.
- The owner's non-LA/LO transmit marks the whole group (`:1006-1010`), so the rider's slot never gets its own tx! while the owner declares.

**Why no wire check can see it.** In SH1's geometry the control's LO is unobservable on the wire. A state check of the documented rider invariant is therefore the only check that can see it there:
- Banner `:89-90`: "every other sink on the stream_id is a rider, its slot VO, taking no event".
- §6.4 Role table: "VO: it takes no event".
- SH14 keeps the wire-level grade, with the rider below the parked holder.

**At the head the rider behaviour is correct, not a defect.** `receipts/runs/rider-probe-head.log`: rider VO in every row, wire-diffs 0.
- **802.1Q-2018 10.7.7:** one Applicant per attribute value. The received LeaveAll is applied once, to the single (owner) applicant.
- **Table 10-3:** rLA! takes AA/QA to VP, and the next two tx! send JoinMt, '3/2' twice. This matches the model row for row.
- **Milan v1.2 4.2.7.2.2:** the rider sends no Empty and no Leave, so nothing can make the peer registrar deregister the still-wanted stream.

A rider that processed rLA! (the control) would be a second applicant state for one value. That is exactly what 10.7.7 excludes.

### Item 3 — R679-3-R1, R2, S1 and R680-3-R1 applied; S1 is comments only

- See the table above.
- S1 is the only RTL-file edit of the round.
  - Raw diff of `hdl/`: 18 changed lines, all `//` comments, 0 others.
  - The listener converts to byte-identical Verilog at `47434635` and at the head: `8f7f4e3b…` (`receipts/sv2v/RESULT.txt`).
  - The netlist input is therefore unchanged, and area carries from round 3: +1,303 LUT / +618 FF at 8x8, as accepted. I did not re-synthesize.

### Item 4 — no RTL, port, parameter or register-map change: met

- The only file changed under `hdl/` is `KL_srp_listener_fsm.sv`, with comments only.
- `docs/architecture/02*` and `07*` are untouched.
- The author's `scope-ports.txt` module-header hashes are identical for the top, the listener and `KL_srp_top`. This agrees with my 0-non-comment-line count.

### Comment rule

I scanned the delta's added lines for lane labels, review rounds, reviewer IDs and comment IDs.
- None appear in source comments: the banner, `sim_main.cpp` and `mutants.py`.
- The README's round name was removed (R679-3-R1).
- The PR body names reviewers and rounds, which the rule allows.
- The only hit is "goes round again", which is ordinary prose.

## Reviewer runs (all on disposable `git archive` copies of the head; `scripts/r4_runs.sh`)

| Run | Result | Receipt |
|---|---|---|
| Stream-FSM `make`, head: walk-record arms plus the suite | rc 0. Walk arms 43/57/87/155 PASS; suite **1,422 PASS, 0 FAIL** | `receipts/runs/head-full.log` |
| Head + order probe | 1,422 PASS; PROBE ORDER rows 72 **LATE 0** | `receipts/runs/head-order.log` |
| Control + order probe | 1,420 PASS, 2 FAIL (SH24 x2); rows 72 **LATE 32** | `receipts/runs/ctl-order.log` |
| `listener-rider-not-quiet` | 15 FAIL: SH1, SH14, SH2 x2, SH4, SH6 x4, SH18 x2, SH19, SH21, SH24 x2 | `receipts/runs/rider-mut.log` |
| The same control, with SH1's VO check removed | 14 FAIL, no SH1 | `receipts/runs/rider-novo-mut.log` |
| Rider probe, head / control | wire-diffs 0 / 0; rider-not-VO ticks 0 / 8 | `receipts/runs/rider-probe-head.log`, `rider-probe-mut.log` |
| srp_top `mutants.py --only` the eight arms whose rows changed, with both positive controls | **11/11 PASS**. Kill counts: settle-compare-dropped 5 + 35, rider-not-quiet 15, handover-drops-state 14, group-order-reversed 13, handover-forgets-walk-mark 3, walk-ends-owing-a-transmit 7, walk-marks-group-only-on-retire 1, walk-done-before-second-pass 2. Each equals its README row, tag for tag. | `receipts/runs/camp.log`, `receipts/runs/camp-out/` |
| sv2v of the listener at `47434635` and at the head | byte-identical | `receipts/sv2v/RESULT.txt` |

Tool identity: Verilator 5.050, pinned wrapper (`receipts/env/tools.txt`). The compile job count was capped through `scripts/vwrap`, which changes only `-j 0` to `-j 3`. After the runs the clone is at the exact head:
- HEAD and tree are as above, and `write-tree` equals the head tree.
- Status, including ignored files, is empty.
- The tree has no gitlinks: this repository has no submodules.

In the published logs, absolute paths under the operator's home directory are replaced by `<home-path>`; nothing else was edited (`receipts/REDACTION.txt`). Every published receipt is listed in `MANIFEST.sha256`.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | SH24 and SH1 expectations against the one-applicant model (Table 10-3 rLA!/tx!/txLA!); the head rider behaviour against 10.7.7, the 35.2.6 NOTE and Milan 4.2.7.2.2 (rider probe, head and control); one message per StreamID per walk before the strobe (SH24, order probe 72 rows). The delta changes no behaviour; the round-3 conformance verdict carries. | R679-4 | 4f57e22006ca727abace93a0cb8585484a377352 |
| RTL | CLEAN | Raw `hdl/` diff (comment lines only); listener sv2v byte-identical; W_DONE (`:1035-1045`), group mark (`:1005-1010`) and handover mark (`:1074`) against the new comments; `txop_done_o` contract (`:174`) and `KL_srp_top.sv:1164-1169`; no port, parameter or register-map change | R679-4 | 4f57e22006ca727abace93a0cb8585484a377352 |
| Robustness | CLEAN | Strobe ordering at the head for takers 0, 2 and 4, both walk kinds, handover at clocks 1-12 (LATE 0/72); walk termination required by SH24 (`done_at >= 0`); the harness's one-shot input clearing, so no second walk falls in the window | R679-4 | 4f57e22006ca727abace93a0cb8585484a377352 |
| Tests | CLEAN | SH24 and the SH1 VO check (source and runs); the new control KILLED on SH24 (own suite run and campaign); S2 extension-only variant (no SH1 kill, reproduced); seven changed control rows re-run with counts and tags equal to the README; suite 1,422 PASS plus the walk arms; author campaign 209/209, coverage 132/132 (receipt verified) | R679-4 | 4f57e22006ca727abace93a0cb8585484a377352 |
| Docs | CLEAN (RESIDUE R679-4-R1, R2 carried; S1-S3 optional) | Banner `:84-122`; 10 §6.4 `:625-660`; stream-FSM README (SH1, SH24, count 1,422); srp_top README (rows, coverage SH1-SH24, rider paragraph); `mutants.py` comment; PR body (Behaviour, Round 2-4 sections); commit messages; comment-rule scan of the delta | R679-4 | 4f57e22006ca727abace93a0cb8585484a377352 |

## Real limits

- **No source bank at this head.** No manager source bank ran here, and I claim none. I did not run the full suite bank (`run_suites`), the full srp_top campaign, the pp_top, name_state or elab-guard campaigns, the consumer gates, Yosys or synthesis. For those, source-head execution evidence is the author's published gate receipts, which I verified by hash and spot-checked.
- **Area** is carried from round 3 on the basis of byte-identical sv2v output. I did not re-measure it.
- **The wire-level consequence of a late push** is inferred from the `KL_srp_top` drain-on-strobe RTL, as in R679-3. SH24 and the probe grade it at the FSM interface, not through an srp_top MRPDU.
- **Hosted checks at the head**, when I checked: docs-gates and portability completed with success (push and pull_request runs); both suites jobs were still in progress (`receipts/env/hosted-checks.txt`). The manager owns hosted and act acceptance.
- **Physical calibration** NOT RUN; field skips are not hardware proof.
- **The evidence archive commit is unsigned.** Its integrity rests on `MANIFEST.json` hashes. The redacted paths in two documents (`path_redacted`) were not checked against their originals.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base 21601694, live dev d77a8afdbc960d70d1ceeee9af1163624f102b16) with the builder and native banks at the merge turn, and link those receipts on the PR.
- Confirm the hosted `suites` jobs at the head, and hosted/act acceptance.
- Carry R679-4-R1 and R679-4-R2 to the residue checklist. S1-S3 are optional.
- Merge still requires two independent positive reviews and the full completion bar.

R679-4 FINISHED
