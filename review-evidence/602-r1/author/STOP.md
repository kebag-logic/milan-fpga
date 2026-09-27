[A383] STOP

Commit: `f7660247e2df93f83b6ac1998bcc90870684153a` on local branch `602-phc-step-mr`.

The PHC-only restart term is removed; render re-base and tu remain intact. Simulation, mutations and documentation follow the #602 ruling. The worktree is clean.

Blocker: `python3 sw/builder/test_builder.py` exits 1 at gate 1b. `sw/builder/test_builder.py:10719` requires three live references to `media_rebase_p_w`; removing its restart use correctly leaves two. Lines 10775-10780 also pin the superseded PHC-inclusive restart expression. Related mutation anchors and diagnostics require matching updates. Later bank checks did not execute.

The assignment explicitly excludes builder edits, so that file is untouched. A concrete test-only patch is prepared but unapplied and unvalidated. Updating these contract assertions requires an explicit scope correction before the full bank can be rerun.

Completed evidence at the committed head: full milan_dp target rc 0; gmstep 64/64 and all 16 mutants caught with both clean controls passing; tkdiag 96 checks and four mutants caught; lint, scope self-test, bare-metal checks, documentation checks and diff check rc 0. All 50 generated artifacts across five configurations are byte-identical. AX 1x1 and 8x8 OOC before/after runs return 0: mapped LUT deltas +182 and +1606, with unchanged FF, memory, DSP and carry counts.

No push, PR operation or merge occurred. REVIEW READY is withheld because the required all-green result is not met.
