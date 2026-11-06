[A739b] REVIEW READY
Commit: 91c115b576601139c53038440f0987412d5172e8
Changed: three commits on 212b7d6e, against the [A10] ruling (issuecomment-6691621111). `scripts/docs_inventory.py`: page needles are graded on the page alone and lane-file needles on the lane files alone; new controls require the audit page's own Inventory row, a lane's second finding with every field, and the Findings intro text; extra needles and one arm kill the other survivors. `docs/DOCUMENTATION_AUDIT.md`: two short paragraphs say what `Located` means, where a finding's line lives and how to reach a copy a text search misses. Same 76 findings, 546 lines. Digest re-pinned to `25dda680`. No workflow file changed.
Validation, all on clean clones of that head, base dev 87e9d03aa2a4797957ac0124d0c7851a2eec234c:
- `python3 scripts/docs_inventory.py --check`: rc 0
- `python3 scripts/docs_inventory.py --selftest`: rc 0, 56 controls
- every `run:` step of `.github/workflows/docs.yml`: 72 ran rc 0, 24 not run with a stated reason (hosted context, apt or sudo), 0 bad; every job's tree clean after it
- `git diff --check`: rc 0
- privacy check of the added lines against origin/dev: 0 private lines
- module size: 1000 lines; the limit is not raised and the long-module ratchet holds at 10
Ruling, item by item:
- R787-1-F1 = R788-1 F1: met. Mutant R1 is killed at base, f5ccb318 and this head; it survived only at 212b7d6e. Putting the old grading back makes it survive again.
- R787-1-F2: met. Mutant O1 has the same history, and the new arm `the audit page lists itself` kills it.
- R787-1-F3 = R788-1 F2: met. W7 and W8 survived on every earlier head, and the new control kills them. It also kills the source and correction droppers.
- R787-1-F4 = R788-1 F3: met. Three mutants drop the new text, and each is killed. On the real tree all 7 rows a text search misses were followed through `--findings-dir`, and each named line carries its statement. The 76 lane entries match the 76 page rows, and the 3 unlocated entries are the 3 rows the page flags.
- Surviving mutants: 16 rows across both reviews, 12 distinct mutants. 11 are killed. R787 and R788 now each leave one survivor, the same mutant.
- S9 = R788's `check ignores the status rule`, answered as equivalent. `broken` with `actual == expected` needs a fresh render that marks current a page its own Findings table lists. A hand edit that breaks the rule differs from the render, so it fails anyway. Only a generator that lost the rule could reach that branch, and that mutant is killed alone and with S9 on top.
- Docstring overclaim: fixed in the same edit at no line cost, so nothing goes to #495. Line 42 uses R787's wording.
- Audience, Purpose and Describes: unchanged, as ruled.
Acceptance criteria:
- Page changes only on status, finding or page set, not length: met as ruled. One line and 500 lines appended to all 212 pages, and a blank line above every recorded finding, each gave rc 0.
- Self-test proof: met. On the real tree a banner, a recorded status, a new page and a removed page each gave rc 1.
- `--check`, `--selftest`, the re-pin and the docs gates: met.
Open risks/questions:
1. One step did not run in the foreground. `gate_25_0`, the isolated builder leg, ran as a capped user service, waited on in the session. It is serial: 15m47s of CPU over 15m39s of wall time, against a roughly 10-minute limit on a foreground call. So "every step rc 0" and "every command in the foreground" could not both hold for it, and I chose to get the gate's evidence. It gave rc 0 on a fresh clone. Every other step ran in the foreground.
2. The [A10] ruling landed at 17:53Z, after my TAKEN and after my first commit, which I had based on the two reviews. That commit met neither the "7 rows" clause nor the one-by-one survivor clause; 2344d147 added both. Please read the three commits as one change.
3. 2344d147 failed a gate: its new sentence broke the concise documentation limits (`gate_9`, 20 words against 10). 91c115b5 fixes that, and every gate above was rerun on it. Neither e3aec77d nor 2344d147 is a merge candidate.
4. Beyond the minimum: the ruling allowed an answer for S6, the verified baseline, the correction cell and the heading-less purpose. I killed them, because each cost a needle or one arm. To stay inside the limit, six wrapped statements or docstrings were rejoined with no behaviour change, and a fixture page lost its heading.
5. `scripts/docs_inventory.py` is at exactly 1000 lines, with no headroom. The next change must cut lines first.
6. `gate_25_1` passed in the foreground at 577 s, close to the limit, and timed out twice under load on the superseded head. Those two rc 124 results were my step limit, not gate verdicts.
7. R787-1-S1 is unaddressed, as the ruling is silent on it: 18 generated pages change their Evidence cell if 7 or more lines are added above the marker. Their status does not change.
8. `scripts/ci_tool_inventory.py --check` was not run: the pinned shell parser is not available here. The local replica was not run, because nothing is pushed.
