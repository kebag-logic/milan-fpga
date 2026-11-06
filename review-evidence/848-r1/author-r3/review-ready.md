[A739c] REVIEW READY
Commit: 171fd56b2c50a44ed75a32c1b9bbd7ae818f2c22
**One required gate is not met locally: `gate_25_0` is not proved at this head.** See Validation and open risk 1.
Changed: two commits on 91c115b5, against the [A10] round 3 ruling (issuecomment-6694897633). `d8a6cfb3` merges dev 3f6bef88. `171fd56b` changes only selftest code in `scripts/docs_inventory.py`: `control`, `copy_controls` and `selftest` differ, and 99 other top-level names are identical. The digest is re-pinned to `092505ae`. `docs/DOCUMENTATION_AUDIT.md` is byte-identical to 91c115b5.
Validation, on clean clones of that head, base dev 3f6bef88bd8a78cb2833a12572b9c4a9013f9bdf, fast gates first:
- `python3 scripts/docs_inventory.py --check`: rc 0
- `python3 scripts/docs_inventory.py --selftest`: rc 0, 56 controls
- every `run:` step of `.github/workflows/docs.yml`: 71 rc 0, `gate_25_0` rc 124, 24 not run with a stated reason (hosted context, apt or sudo). The verifier exits 1 on that one step. Every job's tree was clean after it, and all 72 logs name the exact head
- `git diff --check`: rc 0
- privacy check of the added lines against origin/dev: 0 private lines
- module size: 1000 lines; the limit is not raised and the long-module ratchet holds at 10
Ruling, item by item:
- Lane control (R787-2-F1 = R788-2 F1): met. A control fails when an entry is filed outside its page's lane, or when lanes merge into one file. W8, W9, W11 and W12 survived at 91c115b5 and are killed here.
- Banner window (R787-2-F2 = R788-2 F2): met. A banner on line 16 is not read and a banner on line 15 is read. N14, N16 and N19 survived at 91c115b5 and are killed here, as are B01 to B03 and windows of 17 and 18.
- Module within 1000 lines, ratchet unchanged, digest re-pinned: met.
- Merge dev 3f6bef88, then regenerate through `--write`: met. The only conflict was the audit page. `--write` then changed nothing, because the merge moved page lengths and the page stayed fresh, so no regenerate commit exists.
- Fast gates before long ones: met.
- Suggestions: only those the lane needles cover. R788-2 S3 is closed in full (W13, W15, W16, W17), and R787-2-S3 apart from W20 (W13, W14, W15, W18, W19). The route needles, the swapped baselines, W20 and the reused `DIR` stay out, as they need a separate edit.
Mutants, on the new head:
- Beyond both reviews: a needle opening at a lane's title still passed two mutants that merge the lanes into one file but keep each lane's titled section, because the lane files are read as one string. Each file's start is now marked and the lane needles anchor to it, at no line cost. Those two, and two that file a finding under a wrong named lane, are killed.
- R787's 62: 52 killed, 10 survive. P04 to P07, L07 and W20 are the suggestions left out. C03 is S9. H01, H03 and X01 edit the grader itself.
- R788's 60: 54 killed, 6 survive. T4 and B1 are suggestions left out, S9 is the third, and IDENTITY, G0 and P1+G0 are harness controls.
- My 25 from round 2 met their expectations, my 13 from round 1 are all killed, and the round 2 ruling's four plants are all killed.
- Both reviewers' harnesses pin the old grader text, so their copies carry that one string updated. Nothing else in them changed.
Acceptance criteria:
- Page changes only on status, finding or page set, not length: met as ruled. One line and 500 lines appended to all 212 pages, and a blank line above every recorded finding, each gave rc 0. A real dev merge also left the page unchanged.
- Self-test proof: met. On the real tree a banner, a recorded status, a new page and a removed page each gave rc 1.
- `--check`, `--selftest` and the re-pin: met. The docs gates: **not met in full**, for the one step above.
Open risks/questions:
1. `gate_25_0` is not proved here. It is one indivisible gate of about 16 minutes of serial CPU, measured at 945 s in `scripts/ci_builder_legs.py`, and a foreground call is limited to about 10 minutes. The attempt reached my 585 s step limit with no verdict printed, so rc 124 is that limit and not a failure of the gate. Unlike last round, I did not run it as a user service, because that was never authorized. The hosted run on this exact head would close it. Decision requested: accept that hosted result for this step, or authorize a capped run outside the foreground.
2. Context for that step, not a substitute: dev 3f6bef88 has the same tree as `cf4120f4`, whose hosted `docs.yml` run 42209249596 passed both builder legs. This head differs from that tree in four files, and nothing under `sw/builder` references them by name. `gate_25_1` passed here in the foreground in about 8.5 minutes.
3. `--check` stays rc 0 under the lane mutants on the real tree, because lane files are not committed. The selftest is their only guard, and it now sees them.
4. `scripts/docs_inventory.py` is at exactly 1000 lines, with no headroom. Three lines were rejoined inside the selftest to pay for the needles, with no behaviour change.
5. `scripts/ci_tool_inventory.py --check` was not run: the pinned shell parser is not available here. The digest was compared directly. The local replica was not run, because nothing is pushed.
