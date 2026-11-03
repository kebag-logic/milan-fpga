[A726j] REVIEW READY
Commit: fce77f0efc1425ef7732a8d70c02addc108f7afe
Changed: round 10 on top of round 9 head e803d94b3a11921a293cf036a8eda333d23828f9, 6 one-line commits, one per item of the manager's round 10 ruling (issuecomment-6592794168), tests and docs only; scripts/owned_process.py is byte-identical. Pinned, never narrowed:
- Item 1, R763-9-F3 = R764-9-F1: owner_report takes R763-9-F3's exact fix. Its child writes its PID and waits in signal.pause(), with no timer of its own; STUBBORN is unchanged for the other controls.
  - Round 9's head with only this fix: 0 red in 15,200 runs, 12,000 of them 8 at once and 3200 16 at once, at host load 41 to 78, with busy loops of this round's own on its own CPUs.
  - Round 9's head beside it, the same way: 33 red, every one state R. One-sided Fisher p = 1.1e-10.
  - Both reviewers' drivers are among these runs: R763-9's 0 of 3000 against 12, R764-9's 0 of 3200 against 8. At the final head they give 0 of 3000 and 0 of 3200 again.
  - All 6 owner_report mutants are red with their words.
- Item 2, R763-9-F1: a listing can state a census, a pass the starved clock lands on and the events note, so the listing's own assertion proves it.
  - Each listing whose census grows after the first pass is kept again, early, with a census a tick after the first pass, where its new descendant is first listed.
  - That gives 8 early listings: the trap's command after a first-pass resume, live and not; with no shell, live and not; beside a stopped shell, live and not; and the early forms of items 3 and 4.
  - early-new-sigtermed-0.5 and its three variants join MUTANTS with R763-9's edits byte for byte, named in rows 2 and 6. Each is red on owner_stated_seconds with its words, and on early listings only.
- Item 3, R763-9-F2: R763-9-F2's preferred listing and event list, a live new descendant beside a shell never resumed. It is named in rows 3 and 4 and in the liveness table. Both F2 mutants are red with their words, with R763-9's edits byte for byte, beside one edge mutant red on that cell alone.
- Item 4, R764-9-S1: the live trap command after the 1 s resume; item 3's listing; and a parent beside the stopped shell, not under it, whose live new child spares it to 4 s. Rows 2, 6 and 8 drop "not live" at 1 s.
- Item 5, R763-9-S1: the guide says once that between stated times the starved owner's passes are half a second apart, and a listing's domain is its listed passes. No row's claim changes.
- Item 6, R763-9-R1: its exact fix. R764-9-S2 asks for the same three facts, so it is taken through it. R764-6-S1 is retained, not taken, as in rounds 7 to 9.
- Room under the 1000-line module ratchet, which has no slack: BLOCKING moves unchanged into scripts/process_test_support.py, and 17 MUTANTS entries' words continue at the dict's own 8-space indent. A check at each commit finds every round 9 entry identical and in order, and BLOCKING byte-identical. The lines reviewer probes patch are unchanged.
- MUTANTS: 149 mutants, 146 with a control, all named in the table. The test module is 999 lines, the support module 996.
Validation at this head, one log and rc each, SIGHUP at its default; every gate rc 0:
- every run: step of .github/workflows/docs.yml: verifier 64 steps rc 0, 31 not run with round 1's reasons, 0 bad; builder legs EXCEPT 1 / EXCEPT 16 NOT RUN;
- python3 scripts/test_suite_cancellation.py: PASS;
- --mutants: PASS (149 mutants, 146 with a control that must fail), also at every item's commit;
- --matrix in 4 parts, 1683 runs, each PASS, none cut:
  - none green on all 11;
  - each mutant with a control red on it with its words and red on the whole test;
  - the 3 with no control green on all 11;
- each reviewer's round 9 sweep, at this head:
  - R763-9's: 4224 mutants, 401 survivors (440 at round 9), every F1 and F2 variant killed. Its own classifier finds only its round 9 out-of-domain classes: 6 through its probe's shape, 6 between sampled passes;
  - R764-9's: 24 survive everything (33), all of them its own round 9 equivalent or out-of-domain ones; 9 killed by this round's listings; none new;
  - R763-9's six natural survivors are all red on owner_stated_seconds and the whole test;
- every reviewer probe from rounds 6 to 9, unchanged, from packets checked against their manifests: no survivor inside a stated domain;
  - R763-6's slowed census was green once at 0.5 s a pass for trap-commands-1s, beside the docs.yml jobs; 6 repeats were red with the words. At that pass time the mutant's 1 s kill races the trap's 1.5 s command on wall time. Its own control, owner_stated_seconds, is red every time;
  - every table check passes except R763-6's one-row check, which flags windows-2s, as it accepted, and the four early mutants that the ruling names in rows 2 and 6;
- make -C tb/verilator/gptp_shadow lifecycle: PASS;
- cd tests && behave: 508 scenarios passed;
- git diff --check 1f29f189 HEAD: silent.
Full sweep not rerun: only files round 1 changed.
Acceptance criteria: product code untouched. owner_report no longer fails by chance: 0 of 15,200 under load, against 33. The early edge, the live new descendant beside a shell never resumed and R764-9-S1's three cells each have a listing and red mutants with their words. The preflight grows by about 12 ms: owner_stated_seconds 40 to 52 ms in-process; the whole test a mean of 60.4 s at round 9 and 60.6 s here.
Open risks/questions: none new. R764-7's whole-test mode stops at its own report line on the first red result, as in rounds 8 and 9. r7_mutants.py needs a scratch directory beside its packet; the rerun after creating it is the receipt.
