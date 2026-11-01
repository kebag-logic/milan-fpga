[A711b] REVIEW READY
Commit: `96bfa8513978ebc8c2f2e73bd98914b56e84bf12` (local branch `797-r1-regref`; live dev `1f29f189` merged, one merge base; not pushed)
Changed: every finding of R753-1 and R754-1 is closed, except S4 (RTL comments, outside this PR). No RTL changed.
- Resets are computed by running the CSR's own read decodes in the reset state. `X` remains only on a bit an input or an unreset flop sets.
- `--check` fails on a new register window, a literal decode, a reset or behaviour change, and a flop that disagrees with the defaults ROM. A word the parser cannot read refuses and is never published as read-only. A digest of the comment-stripped sources catches a code change no page text shows.
- Every generated paragraph is read by the concise-prose gate. A one-column table refuses, and a table cell over 200 words refuses. Bit meanings moved to field rows. Rationale and the version log moved to `docs/design/CSR_REGISTER_NOTES.md`, a record linked from each section.
- Side effects are in the field's row, conditions are in plain words, ten generated Mermaid diagrams explain the page's mechanisms, and the memory map has no overprinted labels.
- Device labels are gone. The ETH_GUARD row still states that nothing in the SoC consumes the guard.
Validation:
- On a clean clone of the head, each step of `.github/workflows/docs.yml` ran as its job runs it, output to a file, never piped: 58 steps, all rc 0. 38 were not run: GitHub-only recording and the jobs that verify uploaded receipts, plus apt, sudo and pip installs the scratch environment already provides.
- Builder leg 1 reads `ALL GATES PASS EXCEPT 16 NOT RUN` with rc 0: those arms need a LiteX interpreter or a local Arty build report.
- `gen_register_reference.py --selftest` 58/58; `git diff --check 1f29f189 HEAD` rc 0; `--check --soc-from <export>` rc 0; `counters_contract_milan.feature` 88 scenarios pass.
- Both reviewers' simulations of `milan_csr` at shipping parameters rerun: the only "X, but no input moves it" row is `RST_EPOCH`, which has no reset clause. No undocumented decoded word.
- Both reviewers' plants rerun: 45 plants with 0 misses, and 38 of 39 rows failing, the 39th being the comment-only control that must stay fresh.
- Not run: the Verilator sweep, Yosys and the full behave suite (documentation lane).
Acceptance criteria: the manager's rulings on merge, Reset and Type cells, the freshness gate, the prose gate, device labels, ETH_GUARD, and side effects, conditions and diagrams: met.
Open risks/questions:
1. ETH_GUARD: the gating, or correcting the RTL comments, still needs a decision.
2. The design-notes page, about 31,000 words of carried prose, is not held to the concise-prose rule. Its banner says it is a record, not current reference. If it should be rewritten, that is new work.
3. The Mermaid blocks were not rendered here: no local renderer exists, and a web renderer would publish the source. Read the page once on the PR.
4. Lane conflict with PR #815: both add a docs-check step, and D0's inventory must list the new page.
5. A plant driver that copies part of the tree needs three more inputs: the design notes, `KL_link_guard.sv` and `KL_mmcm_drp_servo.sv`.
