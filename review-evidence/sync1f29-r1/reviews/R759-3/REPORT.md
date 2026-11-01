[R759] POSITIVE - exact head b2a1d67745229d167a5e70d7e1c5064975f027fd

Round R759-3, issue #665, PR #830: round 3 delta, `fa019799..b2a1d677`, one commit, tree `02313ded7626619109696af06a2e1f1a1371a8e4`.

All five lenses are clean at this head, and no MINOR, MAJOR or BLOCKER is open. R759-2 F3, the one finding behind the previous NEGATIVE, is fixed: line 854 reads 884.91, and the exact window is 884.91464 ms. Two wording items remain in the PR body as RESIDUE. Both can be fixed without a new commit.

## Focus items

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Line 854 reads 884.91 (R759-2 F3) | Holds. Re-derived from the published raw log: 88,491,464 bus cycles at 100 MHz. The value 884.92 appears nowhere else in this README | `receipts/window-recheck.txt`; `reviews/R759-2/receipts/window-exact.txt` |
| 2 | Line 843 against the window receipts (RES-3, R760-2-R1) | Holds. `5b5f4336` has 4 records at open and 13 GM events, and both windows are refused. The head has 5 staged and 4 without the stage, with 12 and 13 GM events | `receipts/window-recheck.txt`; `reviews/R759-2/receipts/windows-reader.txt`; `reviews/R760-2/receipts/ring-at-open.txt` |
| 3 | Line 846 has a verb (RES-4) | Holds. It is RES-4's exact sentence | `tb/verilator/ctrl_service_budget/README.md:846` |
| 4 | The PR body's Status (R760-2-R2) | The substance holds: the rc 1 exception is stated and true. The sentence is garbled, and "the head" is one commit stale (RES-5) | `receipts/live-status-line.txt`; `receipts/budget-arm-rcs.txt` |
| 5 | Nothing else changed | Holds. One blob changed, mode 100644 unchanged, 3 insertions and 3 deletions. The commit message is one line with no trailers. The gitlinks are unchanged. The live PR body differs from `author-r2/PR-BODY.md` only at the Status line, apart from a trailing newline | `receipts/clone-restored.txt`; `git diff --raw fa019799 b2a1d677` |

**"The stage adds the fifth record" is accurate.** The staged and no-stage runs post the same 295 records before the windows open, and they release 290 and 291 of them. The refusal does not depend on the stage: the base and the no-stage head are refused with 4 records.

**No other cell of the window table changed.** R759-2 checked the table's other 15 window and longest-pass cells. This round re-derived the GM and window cells of the four refused-window rows from the raw logs, and all match.

**The status line's rc claim holds.** The published `.rc` receipts give rc 0 on 1x1 cacheless and 1x1 32 KiB, rc 1 on the other four staged arms, and rc 1 on the 1x1, 4 KiB no-stage control. That is what the body's table says.

**The handoff's gates reproduce at this head** (`receipts/doc-gates.txt`):

| Gate | Result |
|---|---|
| `check_doc_style.py` | rc 0 |
| `docs_check.py` | rc 0, 0 findings across 215 Markdown files |
| `check_em_dash.py --base 97aab1d0` | rc 0, 0 findings. The first run stopped at rc 2 because the pinned renderer was absent here; it was installed from the pinned file into a disposable directory |
| `check_doc_paths.py` | rc 0 |
| `git diff --check fa019799 b2a1d677` | rc 0 |

**The comment rule has no new instance.** The delta touches no source comment. README lines 840-860 carry no lane label, review round, reviewer ID or comment ID.

## Findings

### RES-5. RESIDUE. Docs. Live PR body, Status: the appended exception landed in the wrong place

- **Authority:** R760-2-R2's fix said to append the clause. Owner's RESIDUE rule: this is PR-body wording and moves no figure or verdict.
- **Evidence:** "exits 0 on the head, but for the budget harness arms that report refused probes, rc 1 as the table below states `fa019799` (the second table under ...)". The clause went between "the head" and the commit it named, so `fa019799` now follows "states" and has no sentence role. "The head" also no longer means `fa019799`.
- **Impact:** a reader cannot tell at once which commit the results belong to. The results table itself names `fa019799` correctly.
- **Exact fix:** "GREEN locally: every gate round 2 touches exits 0 on `fa019799`, but for the budget harness arms that report refused probes, rc 1 as the second table under [How to validate](#how-to-validate) states; `b2a1d677` changes 3 README lines, and its documentation gates exit 0; `sync-dev-1f29f189-into-dev-soft-core` -> `dev-soft-core`. Base: `dev-soft-core` `5b5f4336`."
- **Verification:** read Status against `receipts/doc-gates.txt` and `receipts/budget-arm-rcs.txt`.

### RES-6. RESIDUE. Docs. Live PR body: `b2a1d677` is not recorded, and the commands still pin `fa019799`

- **Authority:** owner's RESIDUE rule. The README delta moves no gate result, and the commands' tree differs from the head only in these 3 README lines.
- **Evidence:** the live body never contains `b2a1d677`. "How to get into the same state" switches to `fa01979959ebff05af34f5a752408de7b3c41cf1`, and the `git diff --check` line ends at the same commit. A reader who follows them gets the tree that still says 884.92. The heading "Results on this round's head" also labels `fa019799`.
- **Impact:** the body does not describe the head under review. No result is wrong.
- **Exact fix:**
  1. Replace both pinned hashes with `b2a1d67745229d167a5e70d7e1c5064975f027fd`.
  2. Change "Results on this round's head:" to "Results on `fa019799`, whose code `b2a1d677` does not change:".
  3. Add a "Round 3" section after "Round 2", and a matching Contents entry, with this row: "| `b2a1d677` | `[R759]` F3, RES-3, RES-4; `[R760]` R1, R2 | `ctrl_service_budget/README.md`: line 854 reads 884.91, line 843 says the stage adds the fifth record, line 846 has a verb. No harness run. |"
- **Verification:** read the body, then check that `git switch --detach` reaches the head.

### S5. SUGGESTION. Docs. `tb/verilator/ctrl_service_budget/README.md:843`: two sentences on one line

Lines 837-847 otherwise keep one sentence per line. RES-3's exact fix introduced this, and `check_doc_style.py` passes. Moving "The stage adds the fifth record." to its own line would match them. This does not need a commit of its own.

## Prior public findings

I read R760-2's report only after writing `receipts/verdict-before-r760-2.txt`. Reading it changed no result; it gave me the text of R760-2-R1 and R2, which I then checked.

| Finding | Status at this head | Evidence |
|---|---|---|
| R759-2 F3, MINOR | Resolved | focus item 1 |
| R759-2 RES-3 | Resolved, with the exact sentence | focus item 2 |
| R759-2 RES-4 | Resolved, with the exact sentence | focus item 3 |
| R759-2 S4 | Retained as a suggestion; the grader is outside this delta | delta file list |
| R760-2-R1 | Resolved at its cause. The line took RES-3's sentence rather than this finding's own fix. The stage's one GM event is stated at line 842 | focus item 2; `README.md:842-843` |
| R760-2-R2 | Resolved in substance; the wording it left is RES-5 | focus item 4 |
| R760-2-S1 | Retained as a suggestion; same subject as S4 | delta file list |
| R760-2-S2 | Retained as a suggestion. This round's packet relies only on repository gates, so it is not affected | `author-r3/HANDOFF.md` |
| R759-1 F1, F2, RES-1, RES-2; R760-1-R1 to R5 | Resolved at R759-2, per its table; this delta touches none of those lines | R759-2's report; delta |
| R759-1 S1 to S3; R760-1-S1 to S4 | Retained as suggestions, per R759-2's table; this delta touches none of their subjects | R759-2's report; delta |

## Clean lens results

```text
[R759] PASS Conformance - tb/verilator/ctrl_service_budget/README.md:840-858 against receipts/window-recheck.txt - F3's figure and the ring and GM claims re-derived with the head's own grade.py from the published raw logs; the issue's acceptance was not re-read, because the delta changes nothing it judges
[R759] PASS RTL - git diff --raw fa019799 b2a1d677 (receipts/clone-restored.txt) - no RTL path and no gitlink in the delta; R759-2's verdict on hdl/milan/mailbox/KL_mbx_evt.sv and R759-1's on the RTL carry
[R759] PASS Robustness - same delta list; reviews/R759-2/receipts/raw-windows/ - no behaviour changed; the refused-window path is re-read at the head, control and base, and R759-2's verdict carries
[R759] PASS Tests - same delta list; receipts/doc-gates.txt - no test, harness or generator path in the delta; the documentation gates that do read the README pass; R759-2's verdict carries
[R759] PASS Docs - README.md:843,846,854, receipts/doc-gates.txt, live PR body - the three README items are true and the gates pass; RES-5, RES-6 and S5 are recorded as wording or optional
```

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `ctrl_service_budget/README.md:840-858`, `receipts/window-recheck.txt`, R759-2 window receipts, R760-2 `ring-at-open.txt` | R759-3 | `b2a1d67745229d167a5e70d7e1c5064975f027fd` |
| RTL | CLEAN | delta file list and gitlinks; no RTL in the delta | R759-3 for the delta; R759-1 and R759-2 for the unchanged RTL | `b2a1d67745229d167a5e70d7e1c5064975f027fd` |
| Robustness | CLEAN | delta file list; refused-window raw logs re-read | R759-3 for the delta; R759-1 and R759-2 for unchanged code | `b2a1d67745229d167a5e70d7e1c5064975f027fd` |
| Tests | CLEAN | delta file list; `receipts/doc-gates.txt`; published arm `.rc` receipts | R759-3 for the delta; R759-1 and R759-2 for unchanged tests | `b2a1d67745229d167a5e70d7e1c5064975f027fd` |
| Docs | CLEAN | README delta, doc gates, live PR body against `author-r2` and `author-r3` packets | R759-3 | `b2a1d67745229d167a5e70d7e1c5064975f027fd` |

RESIDUE leaves no lens unclean.

## Real limits

- **No harness run,** as the round's scope directs. The figures rest on the published raw logs from `fa019799`, its no-stage control and `5b5f4336`. The README is the only file changed since those runs.
- **Not re-run or re-read:** the mailbox, census, firmware, native, builder and LiteX banks, and the issue's acceptance text and rulings. Their prior verdicts carry because the delta touches nothing they depend on.
- **Evidence integrity rests on digests, not signatures.** All 24 published evidence files I relied on match `MANIFEST.json` (`receipts/published-digests.txt`). The evidence commit `723eb53c` and the head commit are both unsigned, so the digests show the files match the manifest, not who published them.
- **Hosted runs are not judged.** At the snapshot, this head had 7 successful, 1 skipped, 20 in-progress and 17 queued check runs (`receipts/hosted-snapshot.txt`). The skipped context is not execution evidence.
- **No manager source bank is claimed or inferred at this head.** Source-head execution evidence is the author's published receipts.
- **Physical calibration NOT RUN.** Field skips are not hardware proof, and this round used no hardware.

## Pending manager duties

- Carry RES-5, RES-6 and S5 to the residue checklist.
- Confirm that the hosted and local replica contexts finish on this exact head.
- Obtain the second independent verdict at this head and publish the completion ledger.
- Build and validate the current-dev merge candidate (source base `5b5f4336`, live dev `1f29f189`) and link its receipts on the PR.
- Obtain explicit maintainer merge authorization, then check post-merge containment.

Clone state after the round: `HEAD` and tree as above, working tree and index equal to `HEAD`, no untracked or ignored file, gitlinks as recorded (`receipts/clone-restored.txt`). The clone was never modified; the only probes were read-only.

R759-3 FINISHED
