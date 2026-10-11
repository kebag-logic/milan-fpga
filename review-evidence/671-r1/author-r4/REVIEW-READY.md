[A592] REVIEW READY (round 4)
Commit: 7bc7ceca6ba1dd1a268d6fa1704613bb141487fe on `671-read-fault`, new commits on `fc0c517c`. No push, rebase or amend.

Answers [the round-4 assignment](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6104799677), R602-3 and R603-3:

- Check 13 now generates every start in the complete 13-read cold-boot bound and 12-read restart bound, crossed with lengths 1 through 4, plus the whole-boot window. Both orientations and existing layouts remain. The sequence values rotate across windows to control runtime; no window is removed for runtime. Of 2,244 generated cases, 86 are outside the documented detection limit, leaving 2,158 per shape (1,119 cold, 1,039 restart). Every window retains its byte-fault cases.
- One reference model supplies each case’s exact judgement, re-stage and fallback read count and expected hold. The three required named controls fail on arty 4x4 and both product shapes: unbounded re-stage, 52 exact-count findings per shape; four-try re-stage, 68; four-try judgement, 140. The unbounded plant also produces sixteen over-bound findings. The original reviewer bound probe independently rejects both re-stage plants on all three shapes.
- The full writer self-test passes five shapes and catches all 46 controls, including all thirteen #671 controls on three shapes. Runtime: 461.48 s at four jobs. The builder’s writer timeout is 1,200 s.
- Base `e8454e27` produces 2,660 findings per product shape under this harness, including 124 lost-change findings. The reproduction keeps its 15 writer statics and excludes the four absent new statics. The old 645 / 124 result is attributed to round-2 head `9112a0df`.
- The console distinguishes a failed judgement from a picked slot that did not read back as judged within three reads. The same cause is checked on cold boot, restart and console refusal. Held re-attach publication is documented as diagnostic; the existing live window remains untouched.

Validation: all executed gates return zero. The host writer, all 101 builder functions in six consecutive parts, firmware-unit 7/7, 81 applicable documentation commands, lint/BDD 5/5, co-simulation 465/465 with 39/39 mutants, service budget, record-space and hygiene gates pass. All required builder elaboration arms ran. Two builder exclusions remain explicit: the unavailable historical placement report and a Makefile mutation with no effect under GNU make 4.3. The handoff lists exact commands, heads, named defects, receipt identities and replica exclusions. The candidate act-runner self-test was not executed on the host; it remains confined to the disposable CI job.

Capture re-measured: all six arms, 96 clean captures, firmware SHA-256 `41000488944bea651733b9708fa0c3a72926ce2308034c51209f2dd95a27b2a2`. The 8x8 contract maximum is 13.86328 ms against 24.5 ms (margin 10.63672 ms, floor ratio 3.5345x); 1x1 is 3.96548 ms. The non-contract 100 MHz comparison is 10.43406 ms. The receipt gate passes and all four capture mutation controls reject as expected. Capture uses the recipe’s recorded simulator environment; suite runs use pinned 5.050.

Firmware size with the pinned RV32 SDK: text 17,483 B (+186 this round; +1,954 over base), bss 104 B (+4 this round; +16 over base), data 104 B unchanged.

Acceptance items 1–3 are met in the recorded tests. The A/B write path and power-loss guarantees are unchanged. The processor carries no generation and remains at its original pin; no submodule commit is needed. The detection limit remains explicit: identical wrong bytes can be indistinguishable from stored contents. Runtime prefill remains outside this task under #717.

HANDOFF.md and PR-BODY.md have Round 4 sections. The working tree is clean. No STOP condition arose. The new head is local: exact-head hosted/act evidence, independent re-review and merge-candidate validation remain for publication and review. No merge is authorized or performed.
