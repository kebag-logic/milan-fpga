[A425] REVIEW READY

Head: `2b38d68e704e8a62fbeae8171c9195ca93728488`, branch `131-d3-core-scalars` (round-1 head `e1ae468f`). Not pushed; the PR is not edited (PR-BODY.md in the packet carries a Round 2 section).

All six round-2 items are committed in the assigned order:
1. `380a3e4` The DR3a aggregate, enforced: the D3 writer counts `NVM_RS_AGG_CYC_P` = `CLK_HZ_P` clocks (1,000 ms) from the accepted `restore_go_i` through both walks and the roll-back, then takes the per-wait path (cause 3; CLOSED before the image is proven, DEFAULTS in pass 0, roll-back in pass 1). The bench now times the top's own derivations. D3R13: a device answering every wait 200 cycles inside the deadline ends at exactly the bound.
2. `83e708a` The AECP hold admission: while held, one AECP record in the shared ingress; the rest dropped at the slot gate and counted (snapshot word 37). D3O5 (CLOSED, 6 AECP) and D3O6 (slowed restore, 6 queued) answer every GET_RX_STATE in the idle 168 cycles, and the unbounded-gating mutant fails both. The three documentation corrections are made, and rule (e) now states the boot-hold exception.
3. `b06130d` R390-1 F3: the derived backoff, dispatch free during it, blank-then-whole disagreement, the two-cycle strobe.
4. `85b2f6f` R391-1 F3: the pass-1 drain with the later SET, a silent judge, the rate walk to its eight-entry bound.
5. `2fbe792` `tb/pp_top/d3_mutants.py` in the tree: 62 of 62 mutants KILLED from the tree, goldens PASS, with mutation records in the suite READMEs.
6. `2b38d68` Port contracts (111 <= 111) and parameter units (naming PASS).

Also taken: R391-1 S1 (one conversion, ceil).

Gates at the head:
- Processor: every suite (33 suites, 1,016,000 checks, 0 failing) and every entry point rc 0. `nvm_port figures` passed only after PR #13's history was fetched into the scratch clone.
- Parent consumer set (scratch parent at `7a7582f0`, gitlink at the head): 9 of 11 rc 0. Not rc 0:
  - `pp_shadow` rc 2: the same 20 PINMISSING warnings as round 1, for the five declared round-1 ports only.
  - The evidence classifier rc 1: `retry_mutants.py`, already unexplained at that pin, and the new driver, which needs its `DUT_READER_DISPOSITIONS` line in the pin-adoption lane. With that line added it returns rc 0 and reports nothing else.
- The reviewers' own probes and eleven mutants, rerun at the head: every GET_RX_STATE is answered and every mutant is KILLED.

DR3a at the ratified values: healthy restores end within 2,661 cycles; the just-inside device ends at 1,000 ms. DR4, same-instrument 1x1 out-of-context synthesis: lane 1 is +1,021 LUT / +560 FF / 0 BRAM / 0 DSP (round 2 adds +48 / +120).

Parent-visible changes for pin adoption (no new top port):
- New parameter `NVM_RS_AGG_CYC_P`.
- The per-wait default is now ceil(`CLK_HZ_P` / 50).
- Snapshot word 37.
- The admission behaviour and the aggregate terminals.
- The classifier disposition for the new driver.

The `pp131-a425` packet has HANDOFF.md, PR-BODY.md, TABLE-15.2.md (18 rows updated), SWEEP.md (658 matches, 0 unreviewed), MUTANTS.md, SUITES.md, GATES.md and REVIEWER-RERUNS.md.
