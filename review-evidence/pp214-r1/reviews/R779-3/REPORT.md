[R779] POSITIVE - exact head 7feeccea3a6c8210ece8d5d1d8929d67582163f9

# R779-3 independent review: processor PR #215, issue #214

Delta review against `1c8b485f`. Tree `60300bb033d00a47c7187ed07b7aa488a9cec1b5`. Source base `a9e84b66`.

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR finding is open, and no RTL defect was found. `hdl/` is byte-identical to `1c8b485f` (tree `6f29f7158dc4`). The delta closes both required items of the [A10] ruling. One new RESIDUE and two SUGGESTIONS are recorded.

The verdict and ledger were on disk before any prior finding was read, and the prior findings changed neither.

## The five checks

Evidence is from 138 probe runs on private copies, plus the repository's own campaign for the six moved labels, which reads `13 checks: 13 PASS, 0 FAIL` (`receipts/campaign-six-labels.log`). The head control reads `1604 checks: 1604 PASS, 0 FAIL`.

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | PV20's third case grades the prepared round's start clock | Confirmed | `push-on-prepared-start` changes one line and removes only `(st_r == E_COLLECT) && go0_w`. It reads 4 FAIL, all PV20's third case, including `the offer waits` and `the next frame captured`. Against the `1c8b485f` suite it reads 888 of 888, so the row is what catches it |
| 2 | The offer drops on accept in all three cases; the comment is right; `push-taken-in-alloc` fails by name | Confirmed | `drop_on_accept` is set inside the one function all three cases call. The arm reads 4 FAIL by name, and 888 of 888 against the old suite. See below for the comment |
| 3 | The walk covers every StreamID bit and VID bits 0 to 11; bits 12 to 15 are rightly outside | Confirmed | Masking one key bit at a time: 64 of 64 StreamID bits fail PV14, 12 of 12 VID bits fail PV15, and bits 12 to 15 read 1604 of 1604. Every producer zero-extends a 12-bit VID (`KL_srp_vlan.sv:261`, `:273`, `:304`); Talker and Listener are constant MSRP (`KL_srp_talker_fsm.sv:731`, `KL_srp_listener_fsm.sv:1357`). So those bits cannot differ between two values |
| 4 | The empty-frame guard hides no failure | Confirmed | Without the guard the head reads the same tally. Every capture result reaches a `CHECK`, so a failed capture always fails by name. With no frame produced at all, the guard gives `1574 checks: 164 PASS, 1410 FAIL`; without it there is no tally (`receipts/guard-noframe.txt`). The guard only turns a crash into a named failure |
| 5 | `second-queueing` 72 to 68; four hit arms left PV20; each still fails elsewhere for a real reason | Confirmed | See below |

**Check 2, the comment.** "Loses on any clock" needed falsifying, because seven `busy_app_w` openings survive: E_RD, E_CAP, E_BOUND, E_V3PK, E_V4PK, E_COMMIT and E_TXREQ. None hides a loss:

- A search needs two consecutive open clocks. The five visited one-clock windows (E_RD, E_CAP, E_BOUND, E_V3PK, E_COMMIT) cannot finish one, so nothing is taken.
- A take forced in each state fails PV20 in every state from E_HDR to E_COMMIT, 5 or 7 FAIL, with `the next frame captured` first. E_V4PK is the exception: PV20's frames never visit it (Listener only).
- E_TXREQ also passes, correctly: the count is already clear, so the push rides the next frame.
- Five adjacent-state pairs all fail PV20.

The comment holds for the three graded drains.

**Check 5, the reason.** The old row kept the offer up through the frame. It was taken into the empty table and then hit itself, so PV20 exercised the merge by accident. Against the old suite `second-queueing` reads 72 with PV20(4), and each hit arm has PV20(2). At this head they read 68, and 52, 16, 52 and 16, with no PV20 failure.

- `second-queueing` still fails PV1 to PV7, PV9 to PV13 and PV16 to PV18, and every row in the README's list.
- The MSRP hit arms still fail 13 rows, and the MVRP hit arms fail PV9, PV12, PV13 and PV17.
- The failures are real: the count rises on a merge, so the drain walks an extra entry. `PV9 VID 2 New then two re-joins: New` reads length 31 against 26, one extra VID vector.

**Figures reproduced.** Base encoder `1604 checks: 1519 PASS, 85 FAIL`, with PV20(15) and the rows the README lists. 37 README ledger rows match the published counts with no mismatch. 888 + 704 + 2 + 10 = 1604.

## Findings

### RES-1 RESIDUE: the comment on `kMaxFrameBytes` says more than the constant does

- **Lenses:** Docs.
- **Where:** `tb/srp_encoder/sim_main.cpp:282`, "The longest frame a capture can hold: a tagged Ethernet frame."
- **Evidence:** the constant only sets `got`'s starting size. `wait_and_drain` clears and grows the vector with no such limit (`:378`, `:383`), and the slots are 576 and 1600 octets (`hdl/packet_engine/KL_pp_tx_slots.sv:46`, `:48`).
- **Impact:** wording only. It changes no check.
- **Exact fix:** "// The size `got` starts at, longer than any frame a row expects, so reading a frame nothing was captured into stays in bounds."
- **Verification:** the comment reads as above.

### S-1 SUGGESTION: give PV20 a second pending value

- **Lenses:** Tests.
- **Where:** `tb/srp_encoder/sim_main.cpp`, `offer_on_the_start_clock`.
- **Evidence:** PV20's drains hold one entry. With E_RD alone opened in `busy_app_w`, a held search takes the read port from the drain, and no row sees it: 1604 of 1604. With a second pending value (a few lines), the head reads `1607 checks: 1607 PASS, 0 FAIL` and the same arm fails `the drain carries what it counted` (`receipts/probe-two-entry.tsv`).
- **Impact:** none at this head. `busy_app_w` is correct, and the ruling does not ask for this.
- **Required outcome:** optional.

### S-2 SUGGESTION: the `the offer is taken after the drain` check does not grade the order

- **Lenses:** Tests, Docs.
- **Where:** `tb/srp_encoder/sim_main.cpp`, `offer_on_the_start_clock`; `docs/architecture/09_verification.md:845`, "taken only after it".
- **Evidence:** the check requires only that the offer has gone by then. Order is proved by the next-frame checks, and only for a take that loses the push. A take in E_TXREQ, after the commit, passes and is safe.
- **Impact:** none at this head. The README and PR body already bound the rule at the commit.
- **Required outcome:** optional: in 09, "taken only after its commit".

## Prior public findings

| Finding | State at this head |
|---|---|
| R779-2 F-1, R780-2-F1 | Resolved: PV20's third case and `push-on-prepared-start` |
| R779-2 F-2, R780-2-R2 | Resolved: the offer drops on accept, the comment is corrected, and the "held only until" text is gone |
| R779-2 RES-1, R780-2-R1 (PV19's comment) | Retained as RESIDUE: `tb/srp_encoder/sim_main.cpp:1894-1895`, exact fix as those reviews give it |
| R779-2 RES-2, R780-2-R3 | Resolved: the PR body now reads "changes neither what is accepted nor what is sent" |
| R-2 (R780-1-R2) | Retained as RESIDUE: `hdl/srp/KL_srp_encoder.sv:76-77` |
| R-3 (R780-1-R3) | Retained as RESIDUE: `tb/srp_top/sim_main.cpp:3422` |
| R779-2 S-1, R780-2-S1 | Taken: the bit walk |
| R779-2 S-2, R780-2-S2 | Taken: the guard |
| R779-1 F-1, F-2; R780-1-F1 to F4 | Resolved in round 2. The delta touches those rows only in PV14, PV15 and PV20, and the moved rows are re-measured above |
| R-1, R780-1-R1 | Resolved: the overstated sentence is no longer in the PR body |
| `rv-search-ignores-start`, `rv-empty-table-searches` | Accepted by the ruling. The PR body records both as judged, and the "no tally" wording is corrected |
| R779-1 S-1, S-2; R780-1-S1 to S3 | Suggestions outside the ruling; not re-judged |

## Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | PV14, PV15 and PV20 against the published quotes of 10.8.3.1 a), 11.2.3.1.7, 10.7.7 and 35.2.2.8.2; issue acceptance 1 and 2. RTL conformance keeps its prior verdict, `hdl/` unchanged | R779-3 | `7feeccea` |
| RTL | CLEAN | `hdl/` tree equal to `1c8b485f`; `start_tgt_w`, `busy_app_w`, `key_f`, E_COLLECT, E_COMMIT and both arm patches read against it | R779-3 | `7feeccea` |
| Robustness | CLEAN | `drop_on_accept`, the empty-frame guard, forced takes, no-frame fault with and without the guard | R779-3 | `7feeccea` |
| Tests | CLEAN (S-1, S-2 recorded) | 138 probe runs, six-label campaign, old-suite arms, base encoder, published receipts and handoff verified against the manifest (13 of 13) | R779-3 | `7feeccea` |
| Docs | CLEAN (RES-1 recorded) | Encoder README, 09 8.14, PR body, comments in the delta; no new lane label, round or reviewer ID in the delta | R779-3 | `7feeccea` |

## Real limits

- The 802.1Q-2022 text was not available to me. Clause wording rests on the author's published quotes.
- The four hit arms are my own reconstruction from their names, not the original patches. Counts and failing rows equal the published figures.
- The guard comparison is thin at the head: a passing run prints only its tally. The no-frame fault is the stronger evidence.
- E_V4PK is not reached by any PV20 frame, so a take there is ungraded. It clears at the same commit.
- My first head control failed to build because my driver did not copy `tb/common`. That was a driver fault, not a result about the head; I fixed it, reran, and dropped that receipt.
- Process disclosures: one disposable file list was written to `/tmp` and deleted, outside the allowed area. A name search for the standard listed three lane directory paths; nothing under them was opened.

## Open, not findings

- Not re-run by me: the full mutant sweep, the other 16 campaign gates, area, and the other 27 consumer gates. The author's published receipts for this head report the campaign at `314 checks: 314 PASS, 0 FAIL`.
- Hosted, at last read (`receipts/hosted-checks.tsv`): `portability` and `docs-gates` completed with success, and `suites` still in progress in both of its runs, so no suites result exists yet. The manager owns hosted acceptance.
- No manager source bank runs at this head. The manager validates the current-dev merge candidate and the donor bar on live dev (`3f6bef88bd8a78cb2833a12572b9c4a9013f9bdf`) at the merge turn.
- Physical calibration NOT RUN. Field skips are not hardware proof.
- Merge still needs the second independent positive review.

The clone is at exact head with no changes, no ignored files and no index difference (`receipts/IDENTITY.txt`). The repository has no submodule gitlinks.

R779-3 FINISHED
