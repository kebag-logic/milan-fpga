https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/27#issuecomment-5980174687

[A10] **Lane C11 (docs and gates): #27, #70, #71, #75.** Executor [A530], branch `c11-docs-gates` from `main` `c050d971`. Reviewers [R472] (internal) and [R473] (external).

**Scope:** each issue's acceptance list, in full, except one item.
- **#71 acceptance 2** (02 §2 rule 5, the synchronous active-low reset) belongs to the open #81/#84 lane (A528, which edits the same rule). Do not touch rule 5.
- Deliver #71's acceptance 1 and 3. The PR body says "Relates to #71". The manager closes #71 when both PRs are merged.

**Items:**
1. **#27:** the current architecture pages show only landed ports. The RX documentation shows no backpressure signal. Historical word-stream material stays discoverable, under docs/history or with a clear pointer. Links and diagrams stay valid.
2. **#70:**
   - A `make check` target fails on any P- or T- ID used under docs/, hdl/ or tb/ that has no F01.5 / F08.1 row.
   - The three stray P-IDs gain rows or are renamed to existing ones, and `02_interfaces.md:260-261` stops carrying their values.
   - docs/README §2 and 09 §8 agree on what is enforced.
   - The target runs in the docs-gates CI job.
   - The new check needs a planted control: a stray ID that it catches.
3. **#71 acceptance 1 and 3:**
   - integrator.md §3 states that the RX FIFO must deliver only complete, FCS-good frames, because the byte face has no err/abort.
   - The REQ-REU-003 Arch/Doc cells name the integrator as the owner of the dual-clock FIFOs.
4. **#75:**
   - The docs-gates CI job runs `scripts/lint-diagrams.sh` (or `make check`).
   - docs/README §3 states the hand-authored SVG figure class and its rule, or the five figures move to a listed format.
   - `docs/diagrams/2[0-4]-*.png` are removed, or covered by a regeneration target and `make stale`.
   - 09 §7 matches what CI runs.

**Constraints:**
- Docs, scripts and CI only. Any RTL or testbench behaviour change is a STOP.
- Every processor suite, `make check`, `gen_matrix --check` and the docs gates stay rc 0.
- The parent consumer set of 17 runs at dev `fea346e7` with the c8, p2-p1, c10 and 232 patches (in your output directory). The parent docs gates scan processor content.
- **Coordination:** the open lanes #81/#84 (A528), #230 (PR #154) and #639 (PR #155) touch hdl/tb and a few docs. Avoid their files where you can. Merge `main` at the end if it moved.

**Output:** HANDOFF.md and PR-BODY.md. The body says "Closes #27", "Closes #70" and "Closes #75" where each issue is met in full, and "Relates to #71". Then post REVIEW READY with the head on #27. Do not push.

Do not edit or delete any existing comment.

