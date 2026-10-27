[A685d] REVIEW READY
Commit: `e0bb857a9f4b8e9d29736970a1135afde03260c5` on branch `665-s2c-icache`, not pushed. One commit on [A685c]'s REVIEW READY head `de91db59` (PR #796), on S2's final `f58d049b` (PR #792). Base: `dev-soft-core` `e76a755a`. S2's branch has not moved, so there is no re-base.

Changed: the owner's NFR-SCOUT-01 amendment (issuecomment-6434741232), in the corrected wording of issuecomment-6434744436. Four Markdown pages, +8 -6, nothing else. `docs/history/` is not edited.
- `docs/reference/FR_NFR.md:321`: "The release architecture MUST use one RV32I control hart: in the split placement it has a 4 KiB direct-mapped instruction cache (64-byte lines, one refill at a time) and no data cache; in the all-fabric placement it stays cacheless." The rest of the row is unchanged.
- `docs/ARCHITECTURE_HW_SW_SPLIT.md:62`, the page's only "cacheless" for the control hart: the same wording. The verb is "uses", because the page carries no uppercase requirement keyword.
- `docs/design/MARK_II_AREA_PLAN.md:383`: "NFR-SCOUT-01: one RV32I hart, 4 KiB instruction cache, no data cache".
- `docs/design/SPLIT_CONTROL_MEMORY.md:243-247`: the open-conflict paragraph is now a record of the amendment. It gives the 2026-10-27 decision and its correction, the old and new text, and the condition that any change of geometry, or a data cache, needs the owner again.
- PR body: states the amendment, not an open conflict.

Validation, at `e0bb857a`, every gate run one at a time in the foreground, unpiped, with the tree clean after each: **0 of 97 gates nonzero**.
- `python3 scripts/check_baremetal_only.py --check`: rc 0, `baremetal-only: OK (0 findings across 1431 tracked first-party file(s))`. `--selftest`: rc 0.
- The docs workflow's check-mode gates: 87, rc 0 each. Among them: `check_em_dash: 0 finding(s) over 1009 added line(s) in 5 changed Markdown page(s)`, `docs_check: 0 finding(s)`, `TOC gate: OK`, `anchor check: 552 ... reproduced`, `doc path gate: OK`, `documentation style: OK`, `HYGIENE RATCHET: PASS`.
- `cd tests && behave`: rc 0, 14 features, 406 scenarios, 1977 steps passed.
- `python3 sw/litex/test_ctrl_memory.py`, which reads `SPLIT_CONTROL_MEMORY.md`: rc 0, `RESULT: PASS`.
- Also rc 0 at the head: the harness self-test (93 `PASS`, 70 `MUTANT caught`), `test_soc_options.py` (6 killed controls on the split cache) and `git diff --check e76a755a HEAD`.
- Not rerun: the builder bank (`test_builder.py --require-rv32`). It passed at `de91db59`, and it reads none of the four pages.

Acceptance criteria: the four listed edits and the PR body are met, with the evidence above. The PR stays "Relates to #665", because the cache does not close T_svc.

Open risks/questions, outside the listed edits and so not edited:
- `docs/reference/FR_NFR.md:6`, the page's introduction, still says "The release uses one cacheless RV32I control hart". The amendment lists only NFR-SCOUT-01's row on that page.
- `MARK_II_AREA_PLAN.md:383` now carries the owner's text. Its figures come from the plan's historical inventory at `e6172750`, a routed image from before the split, so they describe the all-fabric hart, which stays cacheless.
- The area plan's D5 lines (`:610`, `:1302`, `:1357`) record the 2026-08 D5 decision and the cores as priced. They do not repeat NFR-SCOUT-01, and they are unchanged.
