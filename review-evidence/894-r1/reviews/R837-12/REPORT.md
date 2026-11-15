[R837] NEGATIVE - exact head 4ae887a16674416fdbf9c3dc0a0e3aed056906f6

# R837-12: delta re-review of PR #902 (issue #894), rounds 15 to 18

Scope: the whole delta from round 14's `867faf1e` (R838-9 POSITIVE) to `4ae887a1` (tree `1fc2af28`), seven files:
`SPLIT_CONTROL_MEMORY.md`, `FR_NFR.md`, `aecp_mbx.h`, `ctrl_loop.h`, and the budget harness's `README.md`,
`flip_grade.py` and `rows_tiers.py`. Round 18 (`6ef3be3b`, `4ae887a1`) changes `SPLIT_CONTROL_MEMORY.md` alone.
Every round-18 answer to R837-11 is closed at its cause, and so are the residues. My mechanical sweep at the head
reproduces the author's, byte for byte, and no hit of it states a superseded figure as current. The PR body's and the
REVIEW READY's claims about that sweep are true. The image, ELF, self-test and `tx_statements` proofs still hold, and
every documentation gate exits 0 on a clean clone.

The verdict is NEGATIVE on one new MINOR (F1), which I found by widening the sweep to constants the PR removed. It is
the same cause round 18 fixed at `:2520`, left at two sites in an older subsection of section 13. The sweep's stated
limit puts these sites outside its reach, so the sweep's own claim is not false. Five RESIDUE items and one
SUGGESTION follow, so that everything can be absorbed in one pass.

## Findings

### R837-12-F1 - MINOR - Docs, Conformance - `docs/design/SPLIT_CONTROL_MEMORY.md:1970`, `:2010` (and `:2012-2014`, which the same framing governs) - THE RETRY's by-construction 20 ms and `CTRL_LOOP_SRP_MS`'s 18 ms are stated as current

- **Artifact.** Subsection "THE RETRY's age limit, THE TRANSMIT, THE TICK's cap and every pass class" (`:1967`).
  - It opens as "the record of 2026-11-05 (#665) at the code head `65a56d02`" (`:1969`), then says, in the present:
    > Two of its statements no longer hold at this head. A retried notice is now inside its 20 ms under any input, by construction. (`:1970`)
  - Later, in the present:
    > `CTRL_LOOP_SRP_MS` states SRP's bound beside `CTRL_LOOP_STEP_AGE`, `CTRL_LOOP_RETRY_MS` and `CTRL_LOOP_TX_MS`: min(T_svc = 20 ms, its ceiling), 18 ms, THE SHARE's nine passes ([FR_NFR.md 3.4.1]) (`:2010`)
  - `:2014` adds "At this head it fits", of that 18 ms row.
- **Evidence.**
  - The document itself says THE TIERS "replace the three bounds the loop held by construction before them, a change-notice retry's, THE TRANSMIT's (`CTRL_LOOP_TX_MS`) and SRP's (`CTRL_LOOP_SRP_MS`), each now a row by every source" (`:2519`).
  - This PR removed `CTRL_LOOP_SRP_MS`. It is defined at `66f71326` (`ctrl_loop.h:303`) and nowhere under `sw/` at the head (`receipts/removed_constants.tsv`).
  - At the head, SRP's rows are R5 74.07 and R6 69.86 ms within 90 at 1x1/1if. FR_NFR 3.4.1 now gives SRP's records "decision D's 90 ms" (`FR_NFR.md:415`). The `:2010` sentence cites that clause for 18 ms.
  - The retried notice's bound is now the first queued notice's tier row: 14.66 ms within 20 at 1x1/1if, and 20.93 ms at 8x8/2if, over 20, stated 22 and reported (`receipts/gates_clean2/flip_1x1.log`, `flip_8x8.log`). It is not "inside its 20 ms ... by construction" at either point.
  - Round 18 made the same statement history at `:2520` ("Before THE TIERS ... Under them the first queued notice is a tier row"). Round 17 did the same for THE TRANSMIT in this very subsection (`:2004`). The SRP bound and the retry claim in the subsection's framing were left present.
  - The sweep misses both. `CTRL_LOOP_SRP_MS` never moved, it was removed, so `constant_history.py` does not list it. `:1970` carries no moved figure. Both are outside the reach that PR body 18.3 states.
- **Impact.**
  - At the PR head, a reader is told that only two of the subsection's statements no longer hold. One of those two corrections is itself superseded.
  - So SRP's bound reads as a compile-time 18 ms stated by a constant that does not exist, under a clause that now says 90 ms. THE RETRY's 20 ms reads as holding by construction at both points, where 8x8/2if is over it by every source.
  - These are bound statements interpreting FR_NFR 3.4.1. Under the maintainer's ruling, a sentence that states a superseded verdict as current is MINOR. This is not wording alone.
- **Required outcome.**
  - At the head, `:1970` and `:2010` read as the 2026-11-05 record's, with what governs under THE TIERS beside them. That means `CTRL_LOOP_SRP_MS` removed, SRP's R5 and R6 tier rows at 90 ms, and the first queued notice a tier row (14.66 within 20 at 1x1/1if; 20.93 at 8x8/2if, stated 22, reported).
  - One way: `:1970` says the two statements no longer held at the head that wrote the note, and that THE TIERS (#894) since replaced the retry's, THE TRANSMIT's and SRP's bounds ([below](#the-tiers)). `:2010` says "stated" and "was", with the head's rows beside it.
- **Verification.**
  - Run `scripts/removed_constants.py` at the new head: every line naming a removed constant is history-framed.
  - `grep -n "by construction"` over section 13 returns only history.
  - The documentation gates stay rc 0.

### Residue (wording only around figures correct at their own head; no lens made unclean)

- **R837-12-R1:** `SPLIT_CONTROL_MEMORY.md:2522`. The bullet says "SRP's 18 ms, `CTRL_LOOP_SRP_MS`, is THE SHARE's nine passes ... that row fits". It sits under `:2519`'s "The three bullets below record the loop before them", and its sibling `:2520` is now past tense. Exact fix: "SRP's 18 ms, `CTRL_LOOP_SRP_MS` (removed under THE TIERS), was THE SHARE's nine passes, ... that row fitted by the measured cost of its passes".
- **R837-12-R2:** `tb/verilator/ctrl_service_budget/README.md:1490`. "`AECP_QUEUED_MS` planted in a copy of `aecp_mbx.h` past 125 ms at 1x1/1if" is true of the plant (1,250, `flip_grade.py:251`), but it is labelled by the superseded bound. The head's bound is 130. Exact fix: "past its 130 ms bound (at 1,250 ms) at 1x1/1if".
- **R837-12-R3:** PR body, Contents `:9` and `:10`, the Status Round 14 bullet (`:27`) and 14.1.
  - Each states its round's completeness unscoped: "every cost, slice and load figure the round-12 and round-13 moves touched ... is the head's or stated as history". It does not name round 14's miss: `EDIT_RECORD_US`, a cost round 12's `e4d80a8a` moved and round 18 fixed (18.2).
  - The claim is true at the head, but the REVIEW READY's "the completeness claims in the PR body (Status, 14.1, ...) ... say what each missed" is not true of these lines.
  - Exact fix: add "Round 14's tokens named no `EDIT_RECORD_US`, which round 18 found (18.2)" to the Status Round 14 bullet and to 14.1's "Every row moved too" paragraph. Add "(completed in 18.2)" to Contents `:9` and "(completed in 18.1)" to `:10`.
- **R837-12-R4:** PR body 18.3 and the REVIEW READY say `scripts/constant_history.py` is "copied unchanged". The packet's copy adds a one-line provenance comment: its sha256 is `031eb748…` against the original's `6b338c4e…`, and the code is identical. Exact fix: "copied unchanged but for a one-line provenance comment".
- **R837-12-R5:** `author-r18/receipts/figure-classes.txt` gives the reason for `ctrl_service_budget/README.md:172` as "a plant, a per-path T_svc bound". The line is decision D's 125 ms, with the 1x1/1if 130 ms in the next sentence. The class (not current-superseded) is right. Exact fix: give the reason as "decision D's bound, the 1x1/1if 130 ms beside it".

### Suggestions

- **R837-12-S1 (SUGGESTION, Tests, Docs):** extend the sweep in two ways.
  - Constants the PR removed: one AUTO rule for each `#define` at the base that is gone at the head, with its name as the subject and its history's numbers as the values. `scripts/removed_constants.py` lists them: 10 constants, 3 lines.
  - Verdict phrases ("by construction", "now inside") within reach of the three bounds THE TIERS replaced.
  - Together these would have found F1 mechanically.
- **Retained, unchanged causes, optional:**
  - R837-10-S1: `tx_statements` holds "at or over", so a planted `100u` passes.
  - R837-10-S3: `aecp_mbx.h:50` could give the head's 8 ms result.
  - R837-7-S2: arm B's unanswered over-cost record is reported, not held.
  - R838-8-S1: the receipt label.

### Known, not a finding of this PR

#916: `tb/verilator/milan_dp/srptx.hpp:82-83` (`kJoinCs = 20` against the firmware's 19 cs), and its README `:1610` and `:1639`. Both are listed under the PR's Known limitations. 8x8/2if rows are reported only, by decision (#890).

## Prior findings at this head (read after my own pass over the diff and the sweep)

| Finding | State at `4ae887a1` | Evidence |
|---|---|---|
| R837-11-F1 (MINOR): the queued-notice table gave `12180198`'s rows and decision D's 125 ms as current | **Closed** at site and cause | `:2204-2205` give 14.66/20, 127.21/130, 20.93 (stated 22) and 806.60 (stated 62, ceiling 70), equal to `flip_grade.py --check` at both points. `12180198`'s figures (14.60, 91.59 to 125, 20.25, 647.23) are beside them, and I reproduced each by running the check at `12180198` (`receipts/f1_12180198_rows.txt`). `:2207` names the amendment's 130 ms. A grep of `91.59\|14.60\|20.25\|647.23` returns only those labelled cells, `:2342` (history) and an unrelated `:1742` cell (`receipts/f1_f2_verification_grep.txt`). |
| R837-11-F2 (MINOR): `EDIT_RECORD_US` at 260/325 | **Closed** | `:2477` says "was then charged ... 260 ... 325", with "At the head ... 300 and 595 us" beside it. `edit_rows.EDIT_RECORD_US` is `max(PACED)`, i.e. 300 and 595. No present-tense sentence pairs it with 240, 260 or 325. `:2491`'s 260 and 325 are `PACED`'s one-row-edit members at the head. |
| R837-11-F3 (MINOR): the sweeps' "none current" claims were false | **Closed** | The sweep is now derived mechanically. I re-ran it and got 824 hits, sha256 `bcf3c3ee…`, the author's file byte for byte. My triage of every unmarked hit and every weak-marker hit finds none current-superseded (`receipts/sweep_triage.md`). 18.3 and the REVIEW READY state the sweep's reach exactly, and F1 lies outside that reach. R3 is a wording residue in the per-round attribution. |
| R837-11-R1 to R4 (RESIDUE) | **Closed** | `:2427` reads "None (the head lever c measured)". `:2432` reads "was 125.87 ms then". `:2244` uses "was" and "were" throughout. PR body `:69` reads "stood at round 12's start (its TICK restated to 55 us by the final pass, below)". |
| R837-10-F1 (MINOR): `:2004`'s 176 ms product | **Closed**, unchanged since `478ff78c` | `:2004` gives it as history, with `CTRL_LOOP_TX_BOUND_MS` and #890 beside it. |
| R837-9-F1, R837-9-F2 (MINOR) | **Closed**, unchanged since `b6f5c638` | `aecp_mbx.h:50` reads "txL was 49.69 ms at 7 ms, and 8 ms did". `ctrl_loop.h:371` is `34u : 99u`. `tx_statements` is `[]` at both points. Each leg planted one under its row is refused at its own point only, and a check blind to either point is caught by both self-test controls (`receipts/tx_probe.txt`, `receipts/tx_mutation_probe.txt`, RESULT PASS). |
| R837-8-F1, R837-10-R1, R838-9-R1 | **Closed**, unchanged | As recorded at R837-11. Round 18 does not touch them. |
| R837-10-S1/S3, R837-7-S2, R838-8-S1, R837-11-S1 | S1 of R837-11 taken; the rest retained, optional | PR body Findings rows `:619`, `:621`, `:628`. |

## What I checked

1. **The packet** (`receipts/packet_r18_verify.txt`).
   - `author-r18` INDEX: 41 rows, 0 mismatched. The outer `MANIFEST.json`: 42 entries for the round, 0 mismatched.
   - `PR-BODY.md` is identical to the live PR body (sha256 `4a81e3ad…`).
   - The archive commit `76cd0754` is not GPG-signed. Its integrity rests on those hashes.
2. **Round 18's figures against the head.**
   - `:2204-2207`: as in the table above.
   - `:2284`: `item.acmp` 55/55 and 70/70. These are `poll_grade.STATED_US` `acmp=55` and `70`, and `load_grade.STATED_US_DONOR` `item.acmp` 55 and 70. Round 30's 120/125 and 185/165 agree with `:2287`'s own history.
   - `:2287`: the polls' base is 205 and 325 in both columns, as at the head.
   - `:2379`: 87,895 and 146,678 cycles come from the author-r13 class receipts. The rule gives 925 us (878.95 us, plus 5 %, rounded up) and 1,545 us, within `LONG_RECORD_US` 975 and 1,650.
   - `:2477`: as in the table above.
   - `:2479`, `:2480`: the TICK is 55 and ACMP's owed frame 55 at 1x1/1if. At 8x8/2if `events_none` is 35 and the owed frame 70. The 8x8/2if load is 0.794.
   - `:2520`, `:2521`: 14.66, 20.93 (stated 22, `AECP_QUEUED_FIRST_MS` `20u : 22u`), 33.38, and 34/99.
3. **The sweep, all instances, in one pass.**
   - `constant_history.py` (mine, unchanged) gives 125 snapshots and 73 moved constants, the author's receipt byte for byte.
   - My unchanged `figure_sweep.py` gives 727 hits, 463 unmarked. The author's adaptation (`figure_sweep_auto.py`, my rules plus AUTO) gives 824 hits, 541 unmarked, byte-identical to the author's TSV.
   - I read every unmarked hit and every weak-marker HIST hit (40 sentences; `receipts/weak_marker_hits.txt`). The classes are in `receipts/sweep_triage.md`. No hit states a superseded figure as current. README:1490 is R2.
   - My off-sweep probe of removed constants (`scripts/removed_constants.py`) found F1's `:2010` and R1's `:2522`. Reading the subsection's framing then found `:1970`.
4. **The claims.**
   - The PR body Status Round 18 bullet, 18.3 and the REVIEW READY say "every hit ... classified, none ... current". Their limit is "beside no moved constant's name or subject ... outside its reach". Both are true of the sweep, and F1 lies within the stated limit.
   - The Status Round 15 bullet, 15.1, 16.5, 17.2 and the R837-8-F1 row are scoped to their sweeps and name what each missed. The round-14 lines are R3.
5. **What R837-10 checked still holds.**
   - `git diff --name-only b6f5c638 4ae887a1` lists `SPLIT_CONTROL_MEMORY.md` alone. So the 332 image files and 14 harness ELFs that round 16 hashed identical to `234bc149`'s are unchanged by construction. I did not rebuild them.
   - Self-tests on the clean clone: `flip_grade.py --selftest` 585/585, `rows_tiers.py --selftest` 1033/1033, `load_grade.py --selftest` 26/26.
   - `tx_statements` is `[]` at both points.
6. **Gates on a clean clone of `4ae887a1`.** Submodules are at their gitlinks; there were 0 changed paths before and after (`receipts/gates_clean2/SUMMARY.txt`).
   - `docs_check`, `check_em_dash` from `66f71326`, `867faf1e` and `478ff78c`, doc style and its self-test, gPTP docs and its self-test, `DOC_MAP.gen.py --check`, the TOC anchors and check, `git diff --check`, the solution, submodule, feature-status, TODO-ownership, hygiene, py/cpp idiom, archive and doc-path gates: all rc 0.
   - The flip check at 1x1/1if and the load check: rc 0. The flip check at 8x8/2if and over both points: rc 1, by design (#890). The rows are identical to the author's receipts.
7. **The comment rule.** The delta's source comments (`aecp_mbx.h:50`, `flip_grade.py:176-177`, `rows_tiers.py:929`) carry no lane label, round, reviewer ID or comment ID. Round 18 has no source change.
8. **Hosted runs at the exact head**, a snapshot at 2026-11-15T10:23Z (`receipts/hosted_check_runs.tsv`).
   - 50 check runs: 13 success, 36 queued or in progress (the Verilator and Yosys shards among them), and 1 skipped, the "Physical gPTP (nightly and manual)" context. None failed.
   - The skipped context is not hardware proof. The manager owns hosted and act acceptance.

## Lens results

```text
[R837] MINOR Conformance — docs/design/SPLIT_CONTROL_MEMORY.md:1970, :2010 — F1: superseded FR_NFR 3.4.1 bound statements (the retry's 20 ms by construction, CTRL_LOOP_SRP_MS's 18 ms) stated as current; the round-18 rows (:2204-2207, :2520-2521) equal flip_grade.py --check at both points and FR_NFR.md:376-443 is consistent with them
[R837] PASS RTL — git diff --raw 867faf1e 4ae887a1 (seven files, no hdl/, syn/, constraints/ or submodule path); ctrl_loop.h:371 CTRL_LOOP_TX_MS, read only by ctrl_loop.c:203's _Static_assert, vacuous at two interfaces; aecp_mbx.h:50, comment only — no clock, reset, CDC, FSM, width or timing effect
[R837] PASS Robustness — flip_grade.py:171-184 and rows_tiers.py:926-936 plant each interface count's leg under its row and require refusal at its own point; receipts/tx_probe.txt (each leg refused only at its own point, 34u:99u clean) and receipts/tx_mutation_probe.txt (a check blind to either point is caught by both controls)
[R837] PASS Tests — receipts/gates_clean2 (planted controls refused: flip 585/585, rows_tiers 1033/1033, load 26/26; flip at 1x1/1if rc 0); receipts/figure_sweep_auto.tsv reproduced byte for byte and triaged (sweep_triage.md); PR body 18.3 and the REVIEW READY's sweep claims true of it
[R837] MINOR Docs — docs/design/SPLIT_CONTROL_MEMORY.md:1970, :2010 — F1; residues R1 to R5 recorded; every other round 15-18 change checked against the head's tables (What I checked, 2)
```

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `SPLIT_CONTROL_MEMORY.md:1967-2016`, `:2198-2207`, `:2244`, `:2281-2287`, `:2376-2380`, `:2473-2480`, `:2517-2522`; `FR_NFR.md:376-443`; `aecp_mbx.h:54-70`; `ctrl_loop.h:263-284`, `:368-371`; flip and load checks at both points | R837-12 | `4ae887a16674416fdbf9c3dc0a0e3aed056906f6` |
| RTL | CLEAN | the delta's raw diff (seven files, no HDL); `ctrl_loop.h:371`, `ctrl_loop.c:203`; `aecp_mbx.h:50` | R837-12 | `4ae887a16674416fdbf9c3dc0a0e3aed056906f6` |
| Robustness | CLEAN | `flip_grade.py:171-184`, `rows_tiers.py:926-936`; `tx_probe.txt`, `tx_mutation_probe.txt` | R837-12 | `4ae887a16674416fdbf9c3dc0a0e3aed056906f6` |
| Tests | CLEAN | self-tests and gates on a clean clone (`gates_clean2`); the sweep's reproduction and triage; the `12180198` reproduction | R837-12 | `4ae887a16674416fdbf9c3dc0a0e3aed056906f6` |
| Docs | UNCLEAN (F1) | the seven files' delta; the PR body (Status, Contents, 14.1 to 18.6, Findings); the REVIEW READY text in the packet; `figure-classes.txt` | R837-12 | `4ae887a16674416fdbf9c3dc0a0e3aed056906f6` |

This round covers the whole delta from `867faf1e` at the exact head, so R838-9 at `867faf1e` stands as the ancestor review for code the delta does not touch.

## Real limits

- I did not rebuild the images or ELFs. Their identity rests on round 16's published hashes and on `b6f5c638..4ae887a1` being documentation-only.
- I did not run the CPU budget harness. The 87,895 and 146,678 cycle figures rest on the author-r13 receipts.
- The sweep and my probes are textual. A superseded claim that names no moved or removed constant, carries no two-decimal row or three-decimal load figure, and uses no verdict phrase I searched remains out of reach. F1 shows that class exists.
- I did not re-review round 13's code.
- The hosted runs were still in progress at the snapshot.
- Physical calibration was NOT RUN, and field skips are not hardware proof.
- There is no manager source bank at this head, and I claim none.

## Pending manager duties

- Publish this report and the manifest-listed receipts.
- Carry R1 to R5 to the residue checklist.
- Hosted and act acceptance at the exact head, including the Verilator and Yosys shards still running at the snapshot.
- The current-dev merge candidate (source base `66f71326`, live dev `6b66f66d`), built with the builder and native banks at the merge turn.
- #916 stays open, outside this lane.

R837-12 FINISHED
