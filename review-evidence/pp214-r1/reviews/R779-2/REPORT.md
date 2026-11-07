[R779] NEGATIVE - exact head 1c8b485f5eebfa8efaba6f5facbade7e5aa4caaa

# R779-2 independent review: processor PR #215, issue #214

Delta review against the round 1 head `cc92e90a`. Tree `48671d7979a85bb2f8e4030d2305ee547af2194c`.

## Verdict

NEGATIVE, on two MINOR test findings. **No RTL defect was found and no RTL change is asked for.** `hdl/` is byte-identical to `cc92e90a` (tree `6f29f715` at both heads).

Four of the five [A10] items are closed, and each new row and arm does what it claims. Item 5 is closed for three behaviours and part of the fourth:

- **F-1:** PV20 grades two of the three start clocks that can lose a push. A fault on the third, the prepared LeaveAll round, loses an event and passes both suites.
- **F-2:** PV20 does not drop its offer when it is taken, although its comment says it does. That hides a lost push on the clock after the start clock.

Both are small bench edits. [A10] also allows F-1 to be closed with a tracking reference.

## Findings

### F-1 MINOR: a push on the prepared round's start clock is not graded

- **Lenses:** Tests.
- **Where:** `tb/srp_encoder/sim_main.cpp` PV20 (`offer_on_the_start_clock`). The ungraded term is `hdl/srp/KL_srp_encoder.sv:415`, `(st_r == E_COLLECT) && go0_w`. The count is taken at `:737`.
- **Authority:** [A10] item 5 and R780-1-F2, "a push on the clock a drain starts must wait; accepted, it is outside the snapshot and is lost". 802.1Q-2022 10.8.3.1 a): further VectorAttributes go in subsequent PDUs. The 09 §8.14 and encoder README rows state the rule without limiting it to one kind of start.
- **Evidence:** `x-start-collect-term-dropped` removes only that term.
  - It reads `888 checks: 888 PASS` and `8683 checks: 8683 PASS`.
  - A scratch row offers a second value on that clock. At head the offer waits, one entry stays pending, and a second MRPDU of 30 octets follows.
  - Under the arm the offer is taken, nothing stays pending and no second MRPDU follows, so the event is lost (`receipts/collect-probes.txt`).
  - The planted `push-on-drain-start` removes all of `start_tgt_w`, so PV20's two idle-start clocks kill it and hide this path. `x-start0-term-dropped` and `x-start1-term-dropped` are each killed by name.
- **Impact:** this is the own LeaveAll round, one of the windows in the issue's acceptance. A later edit to this term could lose a declaration unnoticed. The PR's "needs no tracking reference" holds for the idle starts only.
- **Required outcome:** one of these:
  - a named row and a planted arm in `tb/srp_top/mutants.py` for the `E_COLLECT` start clock, with the 09 §8.14 and README rows updated; or
  - this path recorded as a pre-existing gap with a tracking reference, as [A10] allows, and the PR sentence corrected.
- **Verification:** the arm above fails the new row by name, and the head stays at 0 FAIL.

### F-2 MINOR: PV20 holds its offer through the drain, which hides a lost push

- **Lenses:** Tests, Docs.
- **Where:** `tb/srp_encoder/sim_main.cpp:1908`, "The offer is held only until it is taken, as a producer does."
- **Evidence:** on the head path the row checks one clock only, then holds `enc_ev_valid_i` through `wait_and_drain`. If the offer is taken and lost during the drain, the held offer is simply taken again.
  - `x-busy-not-in-alloc` takes a push in `E_ALLOC` and loses it. It reads 888 of 888 and 8683 of 8683.
  - With a producer that drops its offer on the accepted clock, the head still reads 888 of 888. The same arm then fails 4 named PV20 checks, including "the next frame captured" (`receipts/row-probes.txt`).
- **Impact:** the comment is false, and correcting only the comment would leave the gap. `busy_app_w` predates this PR, but this row is where the fix belongs.
- **Required outcome:** drop the offer on the clock it is taken, for the whole of the row. `scripts/03_row_probes.py` has a working form of this edit.
- **Verification:** `x-busy-not-in-alloc` fails PV20 by name, and the head stays at 888 of 888.

### RES-1 RESIDUE: PV19's comment says an unknown type is never held

- **Lenses:** Docs.
- **Where:** `tb/srp_encoder/sim_main.cpp:1885-1886`.
- **Evidence:** an unknown type waits on a full table and beside its own drain, because `ev_ready_o` keeps `base_ok_w` (`receipts/row-probes.txt`). The RTL needs no change, and PV19's checks are correct.
- **Exact fix:** replace "whatever the table holds (E11 with the table empty; the push face is never held for a value it will not keep)" with "beside pending entries, with no search (E11 with the table empty); a full or draining table holds it as it holds any push".

### RES-2 RESIDUE: PR body overstates the equivalence of `rv-search-ignores-start`

- **Lenses:** Docs.
- **Where:** PR body, "so it does not change behaviour".
- **Evidence:** the author's own handoff allows that a push in the `E_COLLECT` corner may be taken a clock sooner, and my reading agrees (see the judgement below).
- **Exact fix:** "so it changes neither what is accepted nor what is sent; at most, a push in the `E_COLLECT` corner is taken a clock sooner".

### Retained for the residue checklist

- **R-2:** still present at `hdl/srp/KL_srp_encoder.sv:76-77`. Exact fix unchanged from R779-1.
- **R-3:** still present at `tb/srp_top/sim_main.cpp:3422`. Exact fix unchanged from R779-1.

### SUGGESTION S-1: walk every StreamID bit in PV14

PV14 flips only bit 7 of each octet. `x-identity-top-octet-low7-dropped` keeps only bit 7 of the top octet and passes both suites. [A10] item 2 is met as written, because the planted arm drops the whole octet. A walk over all 64 bits would close this for a few more frames.

### SUGGESTION S-2: guard E1's frame reads

See the `rv-empty-table-searches` judgement below. `tb/srp_encoder/sim_main.cpp:543` reads `got[14]` from an empty frame. A guard would let the suite print its tally.

## [A10] closure

| Item | Row | Arm and measured failure | Reason confirmed | State |
|---|---|---|---|---|
| 1 Isolation, MVRP search beside MSRP drain | PV13 | `msrp-read-taken-by-any-search`, 3 FAIL on "the drain reads its own entries" | the failing checks are all on the drain's frame | Closed |
| 1 Isolation, MSRP search beside MVRP drain | PV13 | `mvrp-read-taken-by-any-search`, 2 FAIL, same check | as above | Closed |
| 2 StreamID top octet | PV14 | `identity-drops-top-octet`, 6 FAIL, octet 0 of each type | two values merge: 51 octets against 79 for type 1 | Closed |
| 2 VID above bit 7 | PV15 | `identity-vid-low-octet-only`, 8 FAIL, bits 8 to 11 | two values merge: 26 octets against 31 | Closed |
| 3 Newer FirstValue | PV16 | `merge-keeps-older-value`, 2 FAIL | same length, bytes differ, as a kept older value would | Closed |
| 4 MVRP events | PV17 | `mvrp-lv-keeps-joinin`, `mvrp-lv-keeps-new`, `mvrp-new-keeps-lv`, 1 FAIL each on its own row; `mvrp-merge-never-written`, 3 FAIL | each single-rule arm fails only the row it plants | Closed |
| 5 Newer value (F2 first) | PV16 | as item 3 | as item 3 | Closed |
| 5 Declaration type (F2 second) | PV18 | `listener-type-s-over-s-kept`, 2 FAIL | both PV18 rows fail byte-exact | Closed |
| 5 Unknown type (F2 third) | PV19 | `unknown-type-held-while-pending`, 3 FAIL | not taken, 0 drop strobes | Closed |
| 5 Push on a start clock (F2 fourth) | PV20 | `push-on-drain-start`, 6 FAIL | taken, next frame missing | **Part closed: F-1, F-2** |

`search-survives-accept` fails 8 checks in PV13, all on the searched table, whose frame grows. That closes the round 1 back-to-back suggestion.

## Clause check for rows that claim encoding

Read in the 802.1Q-2022 text (sha256 `283e041a...`, the file the author's `STANDARDS.txt` names). I found no wrong citation among the clauses the delta cites.

| Row | Encoding claim | Clause |
|---|---|---|
| PV13 | a value is carried once, in its own frame | 10.8.2.5 (each AttributeEvent is applied to that attribute's state machine), 10.8.2.10.1, 10.8.3.1 |
| PV14 | two StreamIDs are two FirstValues | 10.8.2.7, 35.2.2.8.1, 35.2.2.8.2 |
| PV15 | the VID is the whole two-octet FirstValue, 0 through 4094 | 10.8.2.7, 11.2.3.1.7 |
| PV16 | later FirstValue fields travel with the entry | 10.8.2.7; 35.2.2.8 "does not support changes in any of the FirstValue" fields |
| PV17 | event codes 5 and 0 in the packed vector | 10.8.2.5, 10.8.2.10.1; Table 10-3 rows Lv! and New! confirmed, including VN, AA and QA to LA, and LA to VN |
| PV18 | the declaration type in the packed vector | 10.8.2.10.2 |
| PV19 | none: this is a port contract | not applicable |
| PV20 | a later event goes in a subsequent PDU | 10.8.3.1 a) |

## Judgement on the two arms the author left open

**`rv-search-ignores-start`: acceptable, no row needed.**

- It changes `sr_engage_w` only on a clock where `start_tgt_w` is high. `ev_ready_o` stays low, so nothing is written or counted.
- On the next clock the offered application is busy, or the offer has changed and its key differs, so the search state matches the head.
- `msrp_q_r` and `mvrp_q_r` are read again every clock, and the drain first reads after `E_ALLOC` and `E_HDR`.
- One corner remains: `E_COLLECT` with `la_prepare_i` and `go0_w` together does not leave the state, so the search can finish a clock sooner. That is latency only; the table contents are the same. This corner is from reading the RTL, not from a run.
- Measured: 888 of 888, and the same results as the head in both prepared-round probes.

So it is not cycle-identical, but it is equivalent in what is accepted and sent. See RES-2.

**`rv-empty-table-searches`: caught, by name, in the first row.** With unbuffered output it prints 5 named failures, starting `FAIL: E1 push accepted`, then segfaults; the unguarded reads start at `sim_main.cpp:543`. The arm stops all first pushes, so it cannot pass unnoticed: the suite exits non-zero. It cannot be a planted arm, because the campaign requires a tally. The older-row crash is not a gap in this delta. See S-2.

`x-start-laprepare-term-dropped` also passes both suites, but it is not a gap. The push is taken a clock sooner and is inside the later `E_COLLECT` count, so the frame is the same 128 octets long as at the head (`receipts/collect-probes.txt`).

## Prior findings at this head

| Finding | State |
|---|---|
| R779-1 F-1 = R780-1-F3 | Resolved, PV13 and two arms |
| R779-1 F-2 = R780-1-F4 | Resolved, PV14, PV16 and arms |
| R780-1-F1 | Resolved, PV15, PV17 and arms |
| R780-1-F2 | Three behaviours resolved; the fourth is part resolved and continues as F-1 and F-2 |
| R779-1 R-1 = R780-1-R1 | Resolved, the PR body carries the exact fix |
| R779-1 R-2 = R780-1-R2, R-3 = R780-1-R3 | Retained, residue checklist |
| R779-1 S-1 = R780-1-S3 | Resolved, `search-survives-accept` |
| R779-1 S-2 = R780-1-S2, R780-1-S1 | Open suggestions, left out under [A10] |

## Measured at this head

- `tb/srp_encoder`: `888 checks: 888 PASS, 0 FAIL`.
- The same suite against the base encoder RTL: `888 checks: 810 PASS, 78 FAIL`, spread as the README says.
- The repository's campaign driver on every `srp_encoder` arm label: `57 checks: 57 PASS, 0 FAIL`. Every README arm count reproduced, including `second-queueing` at 72.
- `tb/srp_top` was run only under the five reviewer arms that survived the encoder suite, not as a head control. The head's 8683 of 8683 is the author's receipt; four of those arms read the same count, and `x-identity-octet3-bit0-dropped` fails one check there (N9).
- `MUTANTS` holds 289 rows, which with 20 controls and the coverage check matches the PR's 310. The full campaign was not re-run.
- Docs gates on a clean clone: links, matrix, reqtags, modmatrix, params, aecpcmd, ids and figures, rc 0. `git diff --check` is clean. The lint, wavedrom-check and stale targets were not run; the author's `make_check` receipt reads rc 0.
- Comment rule scan over the added lines: one hit, "Listener lane", a protocol term, so no new instance. No stale figure remains outside the history pages.

## Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | PV13 to PV20 expected messages and clause citations against the 2022 text; 10 §3 rule | R779-2 | 1c8b485f5eebfa8efaba6f5facbade7e5aa4caaa |
| RTL | CLEAN | `hdl/` tree identity with `cc92e90a`; R779-1 verdict kept; start and search logic read for the arms | R779-2 on R779-1 | 1c8b485f5eebfa8efaba6f5facbade7e5aa4caaa |
| Robustness | CLEAN | start, busy and prepared-round paths probed; the head waits correctly on each | R779-2 | 1c8b485f5eebfa8efaba6f5facbade7e5aa4caaa |
| Tests | UNCLEAN (F-1, F-2) | `sim_main.cpp` delta, `mutants.py`, 13 patches, campaign, 7 reviewer arms, scratch rows | R779-2 | 1c8b485f5eebfa8efaba6f5facbade7e5aa4caaa |
| Docs | UNCLEAN (F-2) | encoder README, 09 §8.14, 10 §3, PR body, source comments in the delta | R779-2 | 1c8b485f5eebfa8efaba6f5facbade7e5aa4caaa |

## Real limits

- Not re-run, and labelled as `cc92e90a` figures by the author: the full sweep, the other 16 campaign gates, area, and the executed REQ-tag check. `make reqtags` was run here; it is the static gate, not the executed check.
- The published evidence was checked by hash only. The manifest has 1509 entries; I spot-checked 4 files and all matched. The evidence commit `c617176d` reads as unsigned on the host, and the packet contains no detached signature file, so I could not verify a signature.
- Reviewer arms are disposable probes, not an exhaustive fault list.
- Physical calibration was not run, and field skips are not hardware proof.

## Pending manager duties

- **Open, not a finding:** the parent consumer gates ran on `604899c0`. The manager reruns them on live dev at the donor bar.
- The final current-dev merge candidate, source base `a9e84b66`, live dev `3f6bef88bd8a78cb2833a12572b9c4a9013f9bdf`, with its builder and native banks. No manager source bank ran at this head.
- Hosted acceptance. At review time `portability` and `docs-gates` read success, and both `suites` runs were still in progress.
- Carry RES-1, RES-2, R-2 and R-3 to the residue checklist.

## Restoration

The clone was not edited; all probes ran in scratch copies. It reads head `1c8b485f`, tree `48671d79`, an empty status and no difference from HEAD. The repository has no submodule gitlinks (`receipts/clone-state.txt`).

## Receipts

Listed in `MANIFEST.sha256`. `receipts/independent-pass-before-prior-findings.md` records this pass before any prior finding was read. Run logs are published as result extracts (`*.results.txt`: failing checks, tallies and probe lines); the compile output stays unpublished because it carries local build paths.

R779-2 FINISHED
