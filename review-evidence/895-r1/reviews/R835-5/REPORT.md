[R835] NEGATIVE - exact head 1215bd82f4444ee9d4d9b552a711279a1a5bc1d8

# R835-5: cleared-context internal delta review of PR #901 (issue #895), round 10

- **Head:** `1215bd82f4444ee9d4d9b552a711279a1a5bc1d8`, tree `a547c5a7fae9de4f6e7c0aa1ec4e768325dbdc9f`.
- **Delta:** `056d619d..1215bd82`, two commits. `a97a3c3e` is test-side only. `1215bd82` is markdown only.
- **Source base:** `cec88385`. The PR targets `dev-soft-core`.
- **Author packet:** `review-evidence/895-r1/author-r10` at `ea30c5a0`. REVIEW READY is #895 issuecomment-6901464046.

**Verdict: NEGATIVE.** One MINOR finding is open, under Docs. Every other lens is clean.

All four named prior findings are closed at their causes:

- **R836-4-F2 (MAJOR):** the record classes are graded on the real legs, and the planted controls are refused.
- **R835-4-F1 (MINOR):** the THE TRANSMIT term is now held by a test and by plants, at both interface counts.
- **R836-4-F1 and R835-4-F2 (MINOR):** every line they listed is fixed.

The open finding is in the same class as those last two. The round claims that no tracked statement gives a superseded figure as this head's. That claim is not yet true: seven statements on four lines still give an earlier image's figure as this head's. One is in FR_NFR 3.4.1, and two are in sentences this round edited. They are figure claims, not wording, so they are MINOR and not RESIDUE.

## Findings

### R835-5-F1 — MINOR — Docs — seven statements still give an earlier image's figure as this head's

Each is checked against the head by `scripts/f1_sites.py`, and its output is `receipts/f1-sites.txt`, which reports 7 of 7 present.

| Where | Stated as current | This head's figure |
|---|---|---|
| `sw/firmware/ctrl/plat/README.md:110` (edited this round) | 8x8/2if platform "392 B of `rom` past 60.0" | 131,752 B: 680 B past the 131,072 B granule. The sentence's own "1,368 B left at this head" implies 680. 392 B was round 6's 131,464 B. |
| `docs/reference/FR_NFR.md:383` (FR_NFR 3.4.1) | "the slice rule chose 950 us, which the built slice now is …: there 8 ms holds txL, 48.43 ms, … every 1x1/1if row holds … (the last queued notice 127.21 ms, ACMP 28.95)" | `CTRL_LOOP_SLICE_US` is 900 at one interface (`ctrl_loop.h:282`). `AECP_PACE_MS` is 9 (`aecp_mbx.h:57`). txL is 48.58, last 136.65, ACMP 29.63 (`receipts/flip-1x1-1if.log`). The same paragraph states the 900 us and 9 ms later on, so the clause contradicts itself in the present tense. |
| `docs/design/SPLIT_CONTROL_MEMORY.md:2603` (round 5's subsection) | "at this head a paced edit is at most 245 us by the rule and every other record 220" | The dearest edit is 23,877 cycles, which is 255 us. The ordinary class is 225 us (packet `classes/plants/summary.md`, `record_classes-real.log`). |
| `SPLIT_CONTROL_MEMORY.md:2605` (round 5's subsection, edited this round) | "(33.69 at this head …)" and "(94.99 at this head)" | The tx rows are 34.00 and 104.25 ms (`receipts/flip-1x1-1if.log`, `flip-8x8-2if.log`). |
| `SPLIT_CONTROL_MEMORY.md:2606` (round 5's subsection) | "1,864 B left then (1,656 at this head …)" | 1,368 B left (the section 5 table at the head; packet `ledger-final/summary.md`). |

- **Authority:**
  - The Docs lens requires changed contracts and stated figures to agree with the head.
  - R836-4-F1's required outcome reads: "point current-head claims to the final rows and images".
  - The round's own claims say the same: the PR's Round 10 row for R836-4-F1, and `receipts/docs/superseded-inventory.md` ("none states a superseded figure as this head's").
- **Why the inventory missed them:**
  - Its figure list has no 392 B, 245/220 us, 33.69, 94.99, 1,656 at 2606 or 1,864.
  - It filed `FR_NFR.md:383` as "attributed: #894's head", but the sentence names no head and says "now".
  - It filed `plat/README.md:110`'s 1,656 B as "#894's head", but that figure is round 6's of this branch, `bf0844f1`.
- **On the subsection markers:** the new markers at `:2599`, `:2613`, `:2630` and `:2647` say "the figures are that image's". That does not repair a parenthesis that contrasts "then" with "at this head". Under the marker it would have to mean round 5's head, which contradicts its own sentence. At the real head it is false.
- **Impact:**
  - FR_NFR 3.4.1 is a requirements authority, and it tells a cold reader the built slice is 950 us with an 8 ms pace.
  - The platform README gives a ROM overrun past 60.0 that is 288 B too small.
  - No code, image, measurement or gate is wrong. The correct figures are on the same pages.
- **Required outcome:**
  - Each listed statement either gives this head's figure, or names the image it describes (for example "at round 6's `bf0844f1`" or "on #894's head `07ed787e`").
  - The "at this head" parentheses inside the subsections marked superseded are restated or bound to their image.
  - `plat/README.md:110`'s "(1,656 B at round 6's)" names its commit, `bf0844f1`.
  - The inventory's figure list and dispositions are corrected, so its "none" claim is true.
- **Verification:**
  - `python3 -I -B scripts/f1_sites.py <tree>` reports 0 present.
  - A sweep of "at this head" and "at the head" inside `SPLIT_CONTROL_MEMORY.md` section 13's marked subsections, and of FR_NFR 3.4.1, finds only this head's figures.
  - `docs_check.py` reports 0 findings.
  - A markdown-only fix needs no firmware rerun.

### RESIDUE (purely wording; does not affect the verdict or any lens)

- **R835-5-RS1 — Docs — `docs/design/SPLIT_CONTROL_MEMORY.md:515`.** "the harness's `answering-every-port` arm, that image with its test port, holds 124,876 B". The paragraph is bound to `9e30c2c3` and the same sentence already says "held … there". **Exact fix:** "holds 124,876 B" -> "held 124,876 B".
- **R835-5-RS2 — Docs — `docs/design/SPLIT_CONTROL_MEMORY.md:2529`.** This is #894's passage, which the new section 13 preface (`:1170`) attributes to #894's head: "so by the amendment … its bound at 1x1/1if is that row rounded up to the next 5 ms, 130 ms". **Exact fix:** "its bound at 1x1/1if is" -> "its bound at 1x1/1if was, on #894's head,".

### SUGGESTIONS (optional; no effect on coverage)

- **R835-5-S1 — Tests, Docs — the graded real legs are not public.**
  - `record_classes-real.log` and the survey receipts are hashed and consistent. My recomputation agrees with every class maximum (`receipts/packet-verify.log`).
  - But the leg directories they grade are not published (only the drivers name them). So a cold reviewer can check the receipts but cannot grade the legs again.
  - Optional: publish each graded group's `read_leg` records, as start, cycles, command and status, as JSON beside the receipts.
- **R835-5-S2 — Docs — the inventory's next run.** Optional: add a phrase sweep ("at this head", "at the head", "now") to the figure sweep, limited to the marked historical subsections and to FR_NFR 3.4.1. That would have found every F1 site.
- **R835-4-S3 (retained, optional) — Robustness.** A plant that drops `gate_seen` from the gate's early return. Its premise still holds at this head: no firmware changed since `056d619d`.

## Prior findings at this head

| Finding | State | Evidence at `1215bd82` |
|---|---|---|
| R836-4-F2 MAJOR (the survey's paced key and command-blind `held`; no real-leg class grade) | **CLOSED** | See (a) to (e) below this table. |
| R835-4-F1 MINOR (no control holds `SRP_REDECLARE_CS`'s THE TRANSMIT term) | **CLOSED** | See (f) to (h) below this table. |
| R836-4-F1 MINOR (the listed lines 519-530, 2551, 2682, 2688, 2689 and FR_NFR:390) | **CLOSED as listed** | Each listed line is restated or given its subject, and its figures match the head: section 5's table against `ledger-final/summary.md`; 14.72 / 21.11, 136.65, 857.77, 75.84 / 73.36 and 34.00 / 104.25 against my flip logs; 130,341 and 218,322 passes. The class claim it rests on is not yet met: R835-5-F1. |
| R835-4-F2 MINOR (`:2266`, `:2689`, `aecp/README.md:120`, `ctrl_service_budget/README.md:172`) | **CLOSED** | All four state 140 ms and 105 ms with #894's figures attributed. A sweep of 130 next to `AECP_QUEUED_MS`, 99 next to `CTRL_LOOP_TX_MS`, 2,029 next to `SRP_REDECLARE_CS` and 950 next to `CTRL_LOOP_SLICE_US` finds only attributed or historical uses, apart from RS2. |
| R835-4-RS1 = R836-4-RS1 (roles) | **CLOSED** | The PR body names R835-4 and R836-4 with their starts and verdicts, and R835-5 and R836-5 as next. |
| R835-4-S1 (the 18 us headroom) | Taken | `SPLIT_CONTROL_MEMORY.md:2682`. Packet `flip-226.log`: tx 34.02 refused, which matches my R835-4 probe. "No wire change until it passes 40 ms" is right: (TX + 9) / 10 = 4 for TX from 31 to 40. |
| R835-4-S2 (`per_pass_threshold.py`'s path) | Taken | The cited `review-evidence/895-r1/author-r8/scripts/per_pass_threshold.py` exists at `ea30c5a0`. |
| R835-4-S3 | Retained, optional | Above. |

Detail for R836-4-F2:

- **(a)** The corrected survey reads `classes.paced` for `edit_rows.EDIT_RECORD_US` and `classes.other` for `record.aecp`, and it passes `r.command` to `held` (packet `scripts/costs_vs_stated.py:145,162,185`).
- **(b)** `record_classes-real.log` gives rc 0 and RESULT PASS over 8 legs.
- **(c)** My recomputation with the tree's `rule` and `statements` agrees with all 9 claimed maxima: 300/300, 225/235, 915/975, 585/595, 200/265, 1,325/1,650, and SET_STREAM_INFO 215/235 and 185/265 (`receipts/packet-verify.log`).
- **(d)** The survey has 63 statements a point: 57 "within" and 6 "not staged". The 6 are the probe item ×2, the owed MRPDU in the polls and in the donor column, and the build in the donor column and in the pass given whole. The paced row is measured at 28,288 and 55,365 cycles.
- **(e)** The four over-cost plants are each rc 1 on the class grader and on the corrected survey, and rc 0 on round 8's survey. The unplanted copies are rc 0 on all three (18 rc files).

Detail for R835-4-F1:

- **(f)** My run of the tree's own campaign over the `talker-hold-off` defects catches all six by name at 8x8/2if and at 1x1/1if (`receipts/talker-hold-off-plants.log`).
- **(g)** The gaps the failing assertion prints are exactly the stated ones (`receipts/hold-off-gaps.txt`):
  - THE TRANSMIT term dropped: 19,895 ms at two interfaces and 19,966 at one.
  - The term rounded down: 19,995 and 19,996.
  - The test asserts the Leave at request + 190 + `CTRL_LOOP_TX_MS`, that is at 695 and 624 ms.
- **(h)** A reviewer-own plant that drops only the JoinTime term is caught by both the new and the earlier test at both counts (`receipts/join-term-probe.log`, `join-term-gaps.txt`).

## Lens results

```text
[R835] PASS Conformance — sw/firmware/ctrl/test/srp_talker.cpp:331-361, sw/firmware/ctrl/srp/srp_mbx.c:29,35, tb/verilator/ctrl_service_budget/record_classes.py:81-200, packet classes/record_classes-real.log — the 35.2.2.8 / Table 10-7 hold-off is now checked against the Leave on the wire at the latest departure THE TRANSMIT allows, with a literal 20,000 ms that is not derived from the macros under test (srp_talker.cpp:54), so the check is not circular; acceptance 2 holds at both counts (receipts/talker-arms.log: 12/12 at each count, SrpGate 7/7); acceptance 4's cost survey now covers both AECP record classes on the real legs and no statement moves; acceptance 5: plat_ledger rc 0, ctrl_memory_ledger.py:35 records 17,536/19,072/18,240/20,352 against packet ledger-final/summary.md
[R835] PASS RTL — git diff --stat 056d619d..1215bd82 (7 paths: 5 *.md, srp_talker.cpp, srp_talker_mutants.py), packet identity/compare-056d619d-1215bd82.txt — no RTL, firmware, mailbox-contract, submodule or image input changed; 552 of 552 image files identical by sha256; gitlinks unchanged (receipts/clone-integrity.txt); the prior RTL verdict carries, since nothing it depends on moved
[R835] PASS Robustness — srp_talker.cpp:331-361, srp_talker_mutants.py:60-62,118-126, receipts/join-term-probe.log — the boundary case (the latest Leave) is now staged; under-statement of each hold-off term (TX dropped, TX rounded down, JoinTime dropped, both dropped) fails at both counts; no firmware path changed; R835-4-S3 retained as optional
[R835] PASS Tests — receipts/talker-hold-off-plants.log, receipts/talker-arms.log, receipts/record_classes-selftest.log, packet classes/plants/*.rc and gates/campaigns.txt — each new test and plant can fail for the defect it names (my runs: 6/6 hold-off plants caught at each count, my extra JoinTime plant caught); the unplanted arms pass; the talker defect count is 38 (35 at 056d619d + 3), and the campaign gives 421 rows with 76 talker rows (38 × 2) and 0 escaped; the planted over-cost controls are refused on the real evidence path where round 8's survey passed them
[R835] UNCLEAN Docs — R835-5-F1 (plat/README.md:110, FR_NFR.md:383, SPLIT_CONTROL_MEMORY.md:2603,2605,2606); every other changed passage checked: the section 5 head table against ledger-final/summary.md, the section 13 class table and coverage text against the packet receipts, the head's rows against receipts/flip-*.log, docs_check.py 0 findings (receipts/docs_check.log), 0 added lines with an em dash (receipts/em_dash_added.txt)
```

**Comment rule.** The added source lines (`*.cpp`, `*.py`) carry no lane label, review round, reviewer ID or issue-comment ID. The only "round" hits are "rounded" and "rounds-the-transmit-term-down". The new test's comment cites IEEE 802.1Q-2018 35.2.2.8 and Table 10-7, and the file header cites #895. The tracked design doc's new "R835-4's review" and "R836-4's review" links are doc text, not source comments.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `srp_talker.cpp:331-361`, `srp_mbx.c:29,35`, `ctrl_loop.h:282,342,377`, `aecp_mbx.h:57,75`, `record_classes.py`, `FR_NFR.md` 3.4.1, packet class receipts, `receipts/talker-arms.log` | R835-5 | `1215bd82f4444ee9d4d9b552a711279a1a5bc1d8` |
| RTL | CLEAN | delta stat (no RTL or firmware), packet image identity 552/552, `receipts/clone-integrity.txt` gitlinks | R835-5 (the earlier RTL coverage carries: nothing in scope changed) | `1215bd82f4444ee9d4d9b552a711279a1a5bc1d8` |
| Robustness | CLEAN | `srp_talker.cpp:331-361`, `srp_talker_mutants.py:60-62,118-126`, `receipts/join-term-probe.log` | R835-5 | `1215bd82f4444ee9d4d9b552a711279a1a5bc1d8` |
| Tests | CLEAN | `receipts/talker-hold-off-plants.log`, `talker-arms.log`, `record_classes-selftest.log`, `packet-verify.log`, packet `classes/plants/`, `gates/campaigns.txt` | R835-5 | `1215bd82f4444ee9d4d9b552a711279a1a5bc1d8` |
| Docs | UNCLEAN (R835-5-F1) | the full markdown delta (`SPLIT_CONTROL_MEMORY.md`, `FR_NFR.md`, three READMEs), `receipts/f1-sites.txt`, `docs_check.log`, the PR body's Round 10 section, packet `docs/superseded-inventory.md` | R835-5 | `1215bd82f4444ee9d4d9b552a711279a1a5bc1d8` |

## Real limits

- **Delta review only.** Code the delta does not touch keeps its earlier lens verdicts. I ran no full parent, PP, gPTP, Yosys or builder bank, and no CPU-budget-harness leg.
- **The real-leg class grade is checked through its receipts, not regraded.** The legs it reads are not published (S1). I checked:
  - the packet INDEX: 226 of 226 rows match their bytes, and no file is unlisted;
  - the rule recomputation;
  - the tree's grader self-test: 11 of 11 controls refused.
- **The em-dash gate did not run here.** Its pinned markdown renderer is not installed, so it returned rc 2. I ran a direct scan of the added lines instead (0). The author's docs workflow receipts report it passing.
- **No other execution evidence of mine.** Source-head execution evidence is the author's published gate receipts plus my focused runs above. No manager source bank ran at this head, and none is claimed.
- **Hosted checks were still in flight when I looked:** 4 success, 1 skipped, 34 queued or in progress. I judged none of them.
- **No hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof. Acceptance 6 (bench) is out of scope here.
- **Clone state.** It is restored and verified: `write-tree` equals the head tree `a547c5a7`, the index equals the head tree, nothing is untracked or ignored, and the six gitlinks are unchanged (`receipts/clone-integrity.txt`). Every plant ran in a disposable copy under `scratch/`.

## Pending manager duties

- Carry R835-5-RS1 and RS2 to the residue checklist.
- After the F1 repair, run the second-review pairing at the new head, and confirm hosted and act acceptance on that head.
- At the merge turn, build and validate the current-dev merge candidate, source base `cec88385` against live dev `6b66f66d`. Run the builder and the native banks, and link their receipts on the PR.
- Keep 8x8/1if out of scope here, as ruled: it is measured on the composed image before the flip, and this lane has no leg there.

R835-5 FINISHED
