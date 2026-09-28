[A429] REVIEW READY

Head: `cbbb5acc77e9e068c3313d78ed4c1e5e79299a71`, branch `131-d3-core-scalars` (round-2 head `2b38d68e`). Not pushed; the PR is not edited (PR-BODY.md in the packet carries a Round 3 section).

All four round-3 items and the taken suggestion are committed in the assigned order:
1. `f8d1a83` An aggregate expiry never closes a provable image (clarification 5876655419). Before the proof the aggregate aborts nothing: the writer's `agg_o` makes a binding walk still reading take its own per-wait path (`KL_acmp_nvm_shadow` input `rs_agg_i`), it fails whole and releases the listener, and the D3 walk proves the image, reads no record and ends DEFAULTS, cause 3; CLOSED only if the image cannot be proven (cause 7). D3R14, the reviewers' probe D1 device: DEFAULTS by clock 1,000,005 against the bound's 1,000,001, image valid, AECP answering, the enable released, the drained READ ending and a later SET persisting; with the image refused, CLOSED cause 7. The pre-walk-close mutant and two others are killed.
2. `9d66095` Both guides state every terminal the aggregate can take and both causes of CLOSED, as 07 §5.3 now lists them (parameter row, bring-up step 3, outcome table, CLOSED paragraph, troubleshooting row, diagram 23).
3. `58c5fe9` D3R15: a bound inside the roll-back's debt wait (cause 6) or its re-LOCATE (cause 2) ends CLOSED on the bound's own clock; `agg_not_in_rollback` is killed.
4. `e94bea8` D3R16: COMPLETE, rolled-back DEFAULTS and CLOSED keep verdicts, ownership and rows past the bound; D3R17: the writer's grant landed on the bound's own clock is drained and a later SET persists. `agg_not_stopped_at_terminal` and `agg_fires_with_event_in_hand` are killed.
5. `cbbb5ac` Taken, R391-2 S1: D3O7 grades the resident count's return through the external drain; `resident_never_returned` is killed.

Gates at the head:
- Processor: every suite (33 suites, 1,016,016 checks, 0 failing) and every entry point rc 0; `tb/pp_top/d3_mutants.py` 69 of 69 KILLED, goldens PASS.
- Parent consumer set (scratch parent at `7a7582f0`, gitlink at the head): 9 of 11 rc 0. Not rc 0, both declared: `pp_shadow` rc 2 on the five round-1 ports only (the same 20 PINMISSING as the bank at `2b38d68`); the evidence classifier rc 1 on `retry_mutants.py` (explained at the dev pin) and `d3_mutants.py`, rc 0 with both disposition lines and nothing else.
- The reviewers' own scripts at the head: every mutant they reported surviving is KILLED (R390-2's two, R391-2's three); probe D1 and P8 case A end DEFAULTS; P6 differs from its round-2 oracle in exactly the 452 pre-proof expiries, now DEFAULTS.

DR3a at the ratified values: unchanged, plus the new path (the per-byte device ends DEFAULTS 4 clocks after the bound). DR4, same-instrument 1x1 out-of-context synthesis: lane 1 +1,030 LUT / +559 FF / 0 BRAM / 0 DSP (round 3 adds +9 / -1).

Parent-visible for pin adoption (no top port or parameter change):
- The aggregate terminals above: DEFAULTS where round 2 ended CLOSED for a binding walk that alone outlasts 1,000 ms.
- `KL_acmp_nvm_shadow`'s new input `rs_agg_i`: the parent's `nvm_cosim` instantiates that module directly, and its lint gains one PINMISSING (rc 0); tie it to 0 there.
- Found this round, from round 1's `f72a2d2` (binding DR2c backoff) on: the parent's `nvm_cosim` quick loop fails 7 of 315 checks (315 of 315 at base); identical at `2b38d68` and at this head.

Readings stated for review: a bound inside a roll-back still ends CLOSED with the pass-1 cause (§6.3 as the clarification keeps it); a pre-proof expiry followed by an unprovable image carries cause 7.

The `pp131-a429` packet has HANDOFF.md, PR-BODY.md, TABLE-15.2.md (15 rows updated), SWEEP.md (681 matches, 0 unreviewed), MUTANTS.md, SUITES.md, GATES.md and REVIEWER-RERUNS.md with receipts.
