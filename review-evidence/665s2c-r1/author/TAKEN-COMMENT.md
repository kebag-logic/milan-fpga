[A685b] TAKEN

Branch: `665-s2c-icache` (local, not pushed), the five S2c commits at `2a7b0df5` on S2 round 3 `f8876638`, on `dev-soft-core` `e76a755a`. The PR targets `dev-soft-core`; the manager pushes.

Authoritative references: this round's assignment (issuecomment-6431653823); S2's final head `f58d049b` (PR #792); the S2c assignment (issuecomment-6421463860) and [A685]'s REVIEW READY (issuecomment-6431631510); `docs/reference/FR_NFR.md` NFR-SCOUT-01 and 3.4.1 (T_svc = 10 ms).

Interpreted scope:
- Re-base the five S2c commits onto `f58d049b`. Resolve the harness conflicts toward S2's round-4 and round-5 rules: the composed maximum over every backlog window, the partial and lower-bound labels, and the fan-out ranges.
- Re-run the harness self-test and its mutants, then regrade every arm on its attested build, with no new measurement. The cacheless tables must be byte-identical to S2's final regrade.
- Re-state the README and design-doc figures in S2's final terms where the rules change their wording.
- The PR body says "Relates to #665" and states the NFR-SCOUT-01 conflict as open for the owner. Nothing edits the requirement.

Validation plan: the harness self-test; the regrade of every arm, compared table by table; `check_baremetal_only.py --check`; the docs gates; `cd tests && behave`; the idiom, hygiene and whitespace gates; `test_soc_options.py`. All run in the foreground, unpiped, and must return rc 0.

Blockers: none. I STOP if the re-base changes a grade.
