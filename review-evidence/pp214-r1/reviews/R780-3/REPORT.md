[R780] POSITIVE - exact head 7feeccea3a6c8210ece8d5d1d8929d67582163f9

# R780-3 external independent review: processor PR #215, issue #214

Delta reviewed: `1c8b485f..7feeccea`, tree `60300bb033d00a47c7187ed07b7aa488a9cec1b5`. `hdl/` is byte-identical across the delta.

## Verdict

**Both items the [A10] ruling required are closed, and no finding sits above RESIDUE or SUGGESTION.** PV20 now grades the prepared own LeaveAll round's start clock, and its offer drops on accept in all three cases. Each named arm fails its row by name. All five focus checks hold under my own runs at this head, on the pinned simulator 5.050.

## The five checks

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | The third case grades the push on the prepared round's start clock; `push-on-prepared-start` fails it by name | **Holds.** The patch removes only the `E_COLLECT` term of `start_tgt_w`. It reads 4 FAIL, all in the third case, the first being `the offer waits on the clock its drain starts`. Against the previous suite it reads 888 of 888, so the row is what catches it | `receipts/arms214/push-on-prepared-start.log`, `receipts/probes/prev-push-on-prepared-start.log` |
| 2 | The offer drops on accept in all three cases; the comment is right; `push-taken-in-alloc` fails by name | **Holds.** `H::tick` drops `enc_ev_valid_i` on the accept clock, and the flag is set in the one helper all three cases share. The arm reads 4 FAIL, `the next frame captured` and the frame compare, for both applications, and 888 of 888 against the previous suite | `receipts/arms214/push-taken-in-alloc.log`, `receipts/probes/prev-push-taken-in-alloc.log` |
| 3 | The walk covers every StreamID bit and VID bits 0 to 11; bits 12 to 15 are rightly outside | **Holds.** I masked each key bit alone, 80 builds. All 64 StreamID bits fail their own PV14 row, for all three types, and VID bits 0 to 11 fail their own PV15 row. Only VID bits 12 to 15 survive. The VID is 12 bits (11.2.3.1.7, range 0 to 4094) and `KL_srp_vlan.sv:261`, `:273` and `:304` zero-extend it, so that producer cannot set them | `receipts/walk-check.txt`, `receipts/probes/summary-walk.tsv` |
| 4 | The empty-frame guard hides no failure | **Holds.** With the guard removed the head still reads 1604 of 1604, so no passing row depends on it. The zeros can be read only until the first capture. E1 is the first row and checks its capture, and a sized frame cannot match any expected length: `empty-table-searches` reads `E1: length got 1522 exp 30`, 1574 checks, 1429 FAIL. Without the guard the same arm leaves no tally | `receipts/probes/unsized-head.log`, `empty-table-searches.log`, `unsized-empty-table-searches.log` |
| 5 | `second-queueing` fell from 72 to 68; four rv-hit arms left PV20; each still fails another row for a real reason | **Holds.** Against the previous suite the arm reads 72 with PV20(4), at this head 68 with no PV20. Every PV row except PV8, PV14, PV15, PV19 and PV20 fails, and OV0 to OV7 still fail on the srp_top suite. The count arms read 54 and 18 before, 52 and 16 now. The two lost per arm are the PV20 frame compares, where the repeated offer merged into itself | `receipts/probes/prev-second-queueing.log`, `receipts/arms214/second-queueing.log`, `receipts/probes/hit-counts-*.log` |

On check 5, the real reason is the defect's own symptom. A hit that still counts grows the table, so the frame carries the value again: `PV1 two re-joins of one Domain value: one JoinIn: length got 48 exp 30`, and `PV9 VID 2 New then two re-joins: New: length got 31 exp 26`.

The published evidence holds these arms' results, not their source, so I rebuilt them from their names as one MSRP and one MVRP edit. My counts and rows equal the author's for `rv-hit-still-counts` and `rv-hit-counts-entry` and their MVRP twins, which read alike there. That makes two distinct edits under four names, as far as the published results can show.

I also tested the comment's "any clock" with `busy_app_w` lifted one state at a time. The whole-drain arm and the arms for `E_HDR`, `E_MSGHDR`, `E_VHDR`, `E_VFV`, `E_MSGCLOSE`, `E_PATCH` and `E_PDUEND` fail PV20. `E_RD`, `E_CAP`, `E_BOUND`, `E_V3PK` and `E_COMMIT` survive: in these rows each lasts one clock, and a search of a non-empty table needs two, so nothing can be taken there. `E_TXREQ` survives because it follows the commit, so a push taken there is kept. None of these is a gap in the row (`receipts/probes/summary-drain.tsv`).

Other measured counts: head 1604 of 1604; base RTL 1604 with 85 FAIL, PV20(15) and O8(2), every PV row except PV8, PV14, PV15 and PV19. All match the README and the PR body.

## Findings

### R780-3-R1: RESIDUE: `kMaxFrameBytes`'s comment overstates what it bounds

- **Lenses:** Docs.
- **Where:** `tb/srp_encoder/sim_main.cpp:282`.
- **Evidence:** "The longest frame a capture can hold" is not a limit: `wait_and_drain` appends with `push_back`, so a capture grows past 1522. The constant only sizes the frame before the first capture.
- **Impact:** wording only. No check, count or behaviour depends on it.
- **Exact fix:** "The size of the frame before any capture: a tagged Ethernet frame, longer than any frame this suite expects."
- **Verification:** read the line.

### R780-3-S1: SUGGESTION: a tick latched in `E_ALLOC` can hold a canceled empty round

- **Lenses:** RTL, Robustness.
- **Where:** `hdl/srp/KL_srp_encoder.sv:415`, `:736`, `:896`.
- **Evidence:** at the encoder's ports, with `la_cancel_i` high, an empty table and an MSRP join tick in `E_ALLOC`, `join_pend_r[0]` reaches `E_COLLECT` set. `go0_w` then stays high and `start_tgt_w` holds MSRP pushes, so the table stays empty and the round cannot start. In my probe a push went untaken for 200,000 clocks and a push after the next prepare was taken. Without the tick the first push is taken. Head and base behave alike (`receipts/probes/stall-head.log`, `stall-base.log`).
- **Impact:** none reachable that I can find. `KL_srp_top.sv:1169` and `:1175` raise that tick only with `rnd_act_r` or `la_done_w`, and `la_wait_r` excludes `rnd_act_r`, so the top gives no such tick in `E_ALLOC`. This rests on reading, not on a top-level run. It predates #214 and the delta does not touch it.
- **Suggested outcome:** none needed for this PR. If the encoder is reused, `E_COLLECT` could expire a deferred tick with nothing pending, as `E_IDLE` does.
- **Verification:** the probe row in `scripts/run_probes.py`.

## Prior public findings at this head

| Finding | State |
|---|---|
| R779-2 F-1 = R780-2-F1 | **Closed:** PV20's third case and `push-on-prepared-start` |
| R779-2 F-2 | **Closed:** the offer drops on accept, `push-taken-in-alloc`, and the corrected comment |
| R780-2-R2 | **Closed:** the comment it named is replaced |
| R779-2 RES-2 = R780-2-R3 | **Closed:** the PR body now carries the corrected wording |
| R779-2 S-1 = R780-2-S1 | **Closed:** the walk is taken, check 3 |
| R779-2 S-2 = R780-2-S2 | **Closed:** the guard is taken, check 4 |
| `rv-search-ignores-start`, `rv-empty-table-searches` | Accepted by the ruling. Both are recorded as judged and the "no tally" wording is corrected in the PR body. The second reads as stated; I did not re-run the first |
| R779-2 RES-1 = R780-2-R1 | **Open, residue:** PV19's comment, now at `tb/srp_encoder/sim_main.cpp:1894-1895` |
| R-2 and R-3 | **Open, residue:** `hdl/srp/KL_srp_encoder.sv:76-77` and `tb/srp_top/sim_main.cpp:3422`; the delta does not touch either file |
| R780-1-S1, R780-1-S2 = S-2 | Open suggestions, as before |

## Lens results

- **Conformance: CLEAN.** Acceptance 1 and 2 stay proven: `second-queueing` fails OV1 and PV1 by name. PV20's own LeaveAll case is the issue's "own LeaveAll in the window". The clause reads for 10.8.3.1 a) and 11.2.3.1.7 come from the author's published `STANDARDS.txt`; I did not re-read the standard.
- **RTL: CLEAN.** No RTL change in the delta. Both new patches apply to the head and change one term each. R780-3-S1 is a suggestion on code that predates the issue.
- **Robustness: CLEAN.** The new loop is bounded by `kHandshakeTimeoutCycles` and fails by name, the flag is cleared on every path, and the guard hides nothing.
- **Tests: CLEAN.** Checks 1 to 5, all by my own runs. The driver's run of the six named arms reads `13 checks: 13 PASS, 0 FAIL`.
- **Docs: CLEAN.** The README and 09 §8.14 match my counts. No lane label, reviewer ID, round or comment ID appears in the delta's added lines. `check-links`, `check-req-tags` and `check-matrix` pass at this head. R780-3-R1 is wording only.

## Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue acceptance, [A10] rulings, PV14, PV15, PV20, published clause quotes | R780-3 | 7feeccea3a6c8210ece8d5d1d8929d67582163f9 |
| RTL | CLEAN | `KL_srp_encoder.sv` guard, FSM and search; `KL_srp_top.sv` tick drivers; both new patches | R780-3 | 7feeccea3a6c8210ece8d5d1d8929d67582163f9 |
| Robustness | CLEAN | `H::tick`, `offer_on_the_start_clock`, frame guard, unsized and stall probes | R780-3 | 7feeccea3a6c8210ece8d5d1d8929d67582163f9 |
| Tests | CLEAN | `sim_main.cpp` delta, `mutants.py`, driver run of six arms, 80 walk arms, 14 drain arms, previous-suite and base runs | R780-3 | 7feeccea3a6c8210ece8d5d1d8929d67582163f9 |
| Docs | CLEAN | encoder README, 09 §8.14, PR body, source comments, three docs checks | R780-3 | 7feeccea3a6c8210ece8d5d1d8929d67582163f9 |

## Real limits

- I ran the encoder suite, the driver for the six named arms (with the srp_top `onevec` group), and my own probes. I did not run `make check` whole, the full mutant campaign, or `tb/srp_top` beyond that group. Those stand on the author's published receipts.
- The evidence commit `66695bcb` reads unsigned on the host. I checked four author-r4 files against `MANIFEST.json` by hash and all match, but a manifest is not a signature.
- `git diff a9e84b66..head` also shows `KL_srp_listener_fsm.sv` and `KL_srp_top.sv`, because the PR's base `92100657` descends from `a9e84b66`. Against that PR base only the encoder changes under `hdl/`, and the encoder is the same at both bases. My base run used `a9e84b66`.
- Hosted runs at this head: `docs-gates` and `portability` read success; `suites` was still in progress when I looked. That is a snapshot, not an acceptance.
- Physical calibration NOT RUN; field skips are not hardware proof. No manager source bank runs at this head and none is claimed.

## Open, not findings

The full sweep, the other 16 campaign gates, area, and the other 27 consumer gates were not re-run. The donor bar on live dev `3f6bef88bd8a78cb2833a12572b9c4a9013f9bdf` is the manager's.

## Pending manager duties

- Build and validate the current-dev merge candidate and link its receipts on the PR.
- Own hosted and act acceptance, including `suites` at this head.
- Carry R780-3-R1, R779-2 RES-1 = R780-2-R1, R-2 and R-3 to the residue checklist.

## Restoration

The clone was never written: probes ran on exports under the packet's scratch directory. HEAD, tree, index blobs and modes and worktree bytes all match, status is empty, and the processor has no gitlinks (`receipts/restore.txt`).

## Receipts

`scripts/run_probes.py`, `scripts/check_walk.py`, `receipts/arms214/`, `receipts/probes/`, `receipts/walk-check.txt`, `receipts/simulator-identity.txt`, `receipts/restore.txt`, `receipts/own-pass-before-prior-findings.txt`. Home-directory paths in the logs are replaced with `$HOME`; nothing else was edited.

R780-3 FINISHED
