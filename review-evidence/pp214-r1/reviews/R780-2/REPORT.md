[R780] NEGATIVE - exact head 1c8b485f5eebfa8efaba6f5facbade7e5aa4caaa

# R780-2 external independent review: processor PR #215, issue #214

Delta review of `1c8b485f` against `cc92e90a`. Source base `a9e84b66`, tree `48671d7979a85bb2f8e4030d2305ee547af2194c`. `hdl/` is byte-identical to `cc92e90a` (tree `6f29f7158dc4`, `receipts/IDENTITY.txt`).

## Verdict

**The RTL stays correct, and rulings 1 to 4 are closed. One MINOR test gap keeps the verdict NEGATIVE.** PV20 grades a push on a drain's start clock for the two ordinary drain starts, not for the third: the prepared own LeaveAll round. If that one guard term is removed, a value is silently lost, and all 888 encoder checks and all 8683 `srp_top` checks still pass. The PR says this behaviour "needs no tracking reference". The cheapest closure is one row and one arm, and a ready-made row is in this packet. The ruling's other route, a recorded pre-existing gap with a tracking reference, is also open.

All 13 planted arms fail by name in my own run, for the stated reasons (`receipts/arms13.campaign.txt`, 20 of 20 with the control).

## The [A10] ruling, item by item

Each arm below was run by me at this head. The encoding column gives the clause that governs what the row checks byte for byte (see Real limits: the clause text was not available to me).

| Ruling item | Row | Arm and failing check | Encoding clause | Result |
|---|---|---|---|---|
| 1. Isolation, MVRP search beside MSRP drain | PV13 | `msrp-read-taken-by-any-search`: 3 FAIL, all on `the drain reads its own entries` | 10.8.3 packing: the frame holds the drained entries, each once | Closed |
| 1. Isolation, MSRP search beside MVRP drain | PV13 | `mvrp-read-taken-by-any-search`: 2 FAIL, same check; neither arm fails the other direction | as above | Closed |
| 2. StreamID top octet | PV14 | `identity-drops-top-octet`: 6 FAIL, octet 0 of each of three types, no other octet | 10.8.2 FirstValue and NumberOfValues; 10.8.3, two VectorAttributes in one Message | Closed |
| 2. VIDs above bit 7 | PV15 | `identity-vid-low-octet-only`: 8 FAIL, bits 8 to 11 | 10.8.2, with 11.2.3.1.7 for the value | Closed |
| 3. Newer FirstValue | PV16 | `merge-keeps-older-value`: 2 FAIL, Advertise and Failed | 10.8.2 FirstValue; rule from 35.2.2.8 | Closed |
| 4. MVRP JoinIn then Lv, New then Lv, Lv then New | PV17 | one arm per row, 1 FAIL each on its own row only; `mvrp-merge-never-written` fails all three | 10.8.2.7 and 10.8.2.10.1 ThreePackedEvents; expected event from Table 10-3 | Closed |
| 5. F2 row 1 (newer value) | PV16 | as item 3 | as item 3 | Closed |
| 5. F2 row 2 (Listener type) | PV18 | `listener-type-s-over-s-kept`: 2 FAIL, both directions | 10.8.2 with 35.2.2.7.2 FourPackedEvents | Closed |
| 5. F2 row 3 (unknown type) | PV19 | `unknown-type-held-while-pending`: 3 FAIL, no strobe and not taken | none, nothing is encoded | Closed |
| 5. F2 row 4 (push on drain start) | PV20 | `push-on-drain-start`: 6 FAIL. The value really is lost: `the next frame captured` fails | 10.8.3 | **Closed for the two ordinary starts; prepared round open, F1** |

`search-survives-accept` fails 8 checks, all `the search merged into its own table`: the frames grow from 41 to 81 octets, which is the repeat the row is written to catch.

Counts reproduced at this head: suite 888 of 888; against the `a9e84b66` encoder 810 PASS and 78 FAIL on the rows the README lists (`receipts/base-encoder-a9e84b66.log`); `second-queueing` 72, `leave-does-not-replace` 4, `listener-type-oldest` 4. `mutants.py` holds 289 rows, 256 names and 256 patches, matching the PR's figures.

## Findings

### R780-2-F1: MINOR: a push on a prepared round's drain start has no check and no arm

- **Lenses:** Tests, Robustness.
- **Location:** `hdl/srp/KL_srp_encoder.sv:414-416` (the `(st_r == E_COLLECT) && go0_w` term of `start_tgt_w`), `:736-739` (snapshot on leaving `E_COLLECT`), `:883` (count cleared at commit); `tb/srp_encoder/sim_main.cpp:1909` (PV20 starts only from `E_IDLE`); PR body, "so it needs no tracking reference".
- **Authority:** [A10] ruling item 5; R780-1-F2 row 4 ("a push on the clock a drain starts must wait; accepted, it is outside the snapshot and is lost"); issue #214 acceptance 1 (an own LeaveAll in the same window); 10 §3 ("A push that a drain start overtakes rides the next MRPDU").
- **Evidence:**
  - `start-term-collect-dropped` removes only that term. It reads `888 checks: 888 PASS` and `8683 checks: 8683 PASS` (`receipts/probes/SUMMARY.tsv`, `receipts/top/SUMMARY.txt`).
  - `push-on-drain-start` removes all three terms at once, so it fails on the `E_IDLE` starts and says nothing about this one.
  - The same stimulus as PV20, with a prepared round in front of it, separates the two (`scripts/collect_row.py`). The head waits, and the next frame carries the offer: 897 of 897. Under the arm the offer is taken on the start clock with the count at 2, the drain snapshots 1, the commit clears the count, and no next frame exists: `FAIL: PC the offer waits`, `FAIL: PC the next frame captured` (`receipts/directed/collect-head.log`, `collect-arm.log`).
- **Impact:** the head is correct. One edit to this term would lose a value in the own LeaveAll round with `tb/srp_encoder` and `tb/srp_top` green. By reading, the path is live at the top level: `KL_srp_top.sv:1167-1170` raises the join tick at round completion, and 10 §3 says the Domain's re-join on a tx! clock is not waited for. I did not drive it end to end.
- **Required outcome:** either a PV20 case for the prepared round with a planted arm that removes only this term and fails it by name, or the gap recorded with a tracking reference as the ruling allows, with the PR sentence changed to match. The term predates this PR (`a9e84b66` line 344), and no RTL change is needed.
- **Verification:** `scripts/collect_row.py` adds a passing row. The arm's edit is in `scripts/probe_arms.py`, and it must fail the new row by name.

### Suggestions (no effect on the verdict)

- **R780-2-S1 (Tests):** make PV14 and PV15 walk every bit. `sim_main.cpp:1810` flips only bit 7 of each octet. Masking one identity bit at a time leaves 51 of 64 MSRP bits and VID bits 2 to 7 unkilled (`receipts/probes/SUMMARY.tsv`; VID bits 12 to 15 also survive but lie outside the VID). The ruling is met, because octet truncation is the realistic fault and it fails. A loop over bits is a few lines and would make "the whole identity" literal.
- **R780-2-S2 (Tests, Robustness):** make the suite survive an empty frame. `sim_main.cpp:543` indexes `got[14]` after a failed capture. Guarding that read, or setting line buffering, gives such an arm a tally so the campaign can count it.

### Residue (wording only, for the checklist)

- **R780-2-R1:** `tb/srp_encoder/sim_main.cpp:1884-1886`, "whatever the table holds" and "never held" overstate: `base_ok_w` (`KL_srp_encoder.sv:443`) still holds an unknown type at a full table, during its drain and on the start clock. Exact fix: "PV19: an unknown AttributeType has no value to search for, so no search holds it: it is taken and dropped on the clock it is offered, unless the table is full or its drain owns the table, which hold every push (E11 with the table empty)".
- **R780-2-R2:** `sim_main.cpp:1908`, "The offer is held only until it is taken" is true only in the arm's branch: at the head `:1921` keeps it up through the whole frame, so it merges into itself after the commit. Exact fix: "At the head the offer stays up through the frame and merges into itself; if the start clock takes it, it drops at once, as a producer does, so the next frame shows the loss."
- **R780-2-R3:** PR body, on `rv-search-ignores-start`: "so it does not change behaviour". Exact fix: "so nothing is taken on a start clock; the one difference measured is that a search running through a clock with `la_prepare_i` and a join tick in `E_COLLECT` is taken sooner, from the same table."
- **R-2 (R780-1-R2):** carried, still at `KL_srp_encoder.sv:76-77`.
- **R-3 (R780-1-R3):** carried, still at `tb/srp_top/sim_main.cpp:3422`.

## The two arms the author could not settle, and one of mine

- **`rv-search-ignores-start`: not equivalent, but harmless. No finding.** The author's reading is right in substance, and the survivor needs no row. I ran head and arm in lockstep on random stimulus: 300 seeds, 8,356,623 clocks, 22 first differences (`receipts/diff-search-ignores-start-300.txt`). All 22 are `ev_ready_o` alone, in `E_COLLECT`, with the arm ready and the head not, and each follows a clock with `la_prepare_i`, a join tick and a held offer. None falls outside that corner. So it is not cycle-equivalent, though the PR body says it does not change behaviour (R780-2-R3). It is safe: nothing is accepted on the blocked clock, the table does not move, and `base_ok_w` holds on the accept clock in both versions, so the arm takes the same value from the same table sooner. It also passes 8683 of 8683. The lockstep stops a seed at its first difference, so frames after that point were not compared.
- **`rv-empty-table-searches`: caught by name; the crash only hides it. No finding beyond S2.** With line-buffered output, E1 prints five named failures first, `E1 push accepted` among them, then `got[14]` on the empty frame crashes the suite (`receipts/probes/rv-empty-table-searches.log`). The arm is a total deadlock of the push face, and every row depends on that term. It is not a campaign arm, so no gate relies on the missing tally, but the campaign would rightly call it unproven as things stand.
- **`start-term-prepare-dropped` (mine): survives, latency only. No finding.** The `E_IDLE` prepare term also survives both suites, but `E_COLLECT` takes a fresh snapshot, so nothing is lost. A directed row reads 894 of 894 under the arm, with both values in the prepared frame (`receipts/directed/prepare-arm.log`).

## Prior public findings

Read only after `receipts/verdict-before-prior-findings.txt` was on disk. Nothing in them changed that verdict.

| Finding | State at this head |
|---|---|
| R780-1-F1 | Closed: PV15, PV17 and their arms |
| R780-1-F2 rows 1 to 3 | Closed: PV16, PV18, PV19 |
| R780-1-F2 row 4 | Closed for the arm it named; retained in part as R780-2-F1 |
| R780-1-F3 = R779-1 F-1 | Closed: PV13, both directions |
| R780-1-F4 = R779-1 F-2 first half | Closed: PV14 |
| R779-1 F-2 second half | Closed: PV16 |
| R780-1-R1 = R-1 | Closed: the sentence is gone from the PR body |
| R780-1-R2 = R-2, R780-1-R3 = R-3 | Open, wording only, to the residue checklist |
| R780-1-S3 = S-1 | Closed by PV13's held offer and `search-survives-accept` |
| R780-1-S1, R780-1-S2 = S-2 | Not adopted; the ruling keeps suggestions out. They remain suggestions |

## Lens results

- **Conformance: CLEAN.** No RTL change. PV17's expected messages match Table 10-3 as stated in the author's standards receipt; PV14 to PV16 rest on 35.2.2.8, 35.2.2.8.1 and 11.2.3.1.7, the clauses the RTL comment already cites. Every frame row compares byte for byte with the independent packer.
- **RTL: CLEAN.** `hdl/` is byte-identical, so the prior verdict stands. The delta's rows found no defect, and neither did my probes: the head passes the two directed rows and every lockstep difference is the arm's.
- **Robustness: UNCLEAN (F1).** The lost-value mode on the prepared path is unguarded by any test. S2 is a harness weakness, not a blocker.
- **Tests: UNCLEAN (F1).** Everything else asked for is graded, and each arm fails for its stated reason.
- **Docs: CLEAN.** The README, 09 §8.14 and 10 §3 match the rows and my counts. No lane label, reviewer ID, round or comment ID appears in the delta's source comments. R780-2-R1 to R3 are wording only.

## Ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | PV13 to PV20 expected messages, 10 §3 rule, author standards receipt | R780-2 | 1c8b485f5eebfa8efaba6f5facbade7e5aa4caaa |
| RTL | CLEAN | `hdl/` tree identity, `KL_srp_encoder.sv` push face and FSM read against the rows | R780-2 (prior verdict kept from R780-1) | 1c8b485f5eebfa8efaba6f5facbade7e5aa4caaa |
| Robustness | UNCLEAN (F1) | drain-start terms, directed rows, lockstep compare, crash path | R780-2 | 1c8b485f5eebfa8efaba6f5facbade7e5aa4caaa |
| Tests | UNCLEAN (F1) | 13 arms, 3 moved arms, 84 probe arms, base run, `srp_top` under 3 arms | R780-2 | 1c8b485f5eebfa8efaba6f5facbade7e5aa4caaa |
| Docs | CLEAN | README, 09 §8.14, 10 §3, PR body, comment-rule scan of the delta | R780-2 | 1c8b485f5eebfa8efaba6f5facbade7e5aa4caaa |

## Real limits

- The text of 802.1Q-2022 was not available at any path I may read. The clause numbers in the ruling table are cited as asked; 10.8.2.x comes from the repository's own citations, and 10.8.3 is cited nowhere in the repository, so that attribution is mine and unchecked against the text. Table 10-3 and clause 35 readings rest on the author's receipt and the prior reviews.
- `start-term-collect-dropped` ran on `tb/srp_encoder` and `tb/srp_top` only, not on other suites. F1's top-level reachability comes from reading.
- The published evidence is hash-checked, not signature-checked: 12 `author-r3` files match `MANIFEST.json`, the other 334 were not downloaded, the evidence commit reads as unsigned, and I found no detached signature in the tree.
- `make check`, lint and the idiom gates were not re-run; I rely on the author's receipts for those.
- Compiler command lines were stripped from the published logs because they carry local paths.
- My first campaign run left an ignored `tb/common/__pycache__` in the clone. I removed it. The clone is at exact head with a clean status including ignored files; index and tree hashes match, and this repository has no gitlinks (`receipts/IDENTITY.txt`).

## Pending manager duties

- Parent consumer gates ran on `604899c0`. The rerun on live dev at the donor bar is open; this is not a finding.
- The full sweep, the other 16 campaign gates, area and the executed REQ-tag check were not re-run and carry `cc92e90a` figures. Also open, not a finding.
- Hosted runs at this head, as read: `docs-gates` and `portability` passed, `suites` was pending. Hosted acceptance is the manager's.
- The current-dev merge candidate (builder and native banks) is built at the merge turn. No manager source bank ran at this head, and physical calibration was not run.
- Carry R-2, R-3 and R780-2-R1 to R3 to the residue checklist.

## Receipts

Listed in `MANIFEST.sha256`: `receipts/arms13*`, `receipts/arms3*`, `receipts/probes/`, `receipts/top/`, `receipts/directed/`, `receipts/diff-search-ignores-start*.txt`, `receipts/base-encoder-a9e84b66.log`, `receipts/verdict-before-prior-findings.txt`, `receipts/IDENTITY.txt`, and `scripts/`.

R780-2 FINISHED
