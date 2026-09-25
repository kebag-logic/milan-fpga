[A320]

Closes #545

A 100 us PHC slew at 200 ppm could move the CRF integrator and drop LOCKED. The servo now discards and counts every measurement window overlapping the plane's registered correction level, including the partial tail, while holding its integrator, trim and lock. Clean windows resume directly. A boundary-coincident step and slew count their shared window once.

The processor pin advances to `5dce647a`, with regenerated ROM records and current contract references. The level passes through the shadow and follows the effective PHC rate through the existing synchronous pipeline. Correction follows measured completion without a timeout. The connection makes no network-port assumption.

Validation:

- Both 100 us slew directions hold the integrator and command exactly through affected windows. The first clean update stays within 1 ppm and completes within 1.536 s of the disturbance's start; LOCKED holds throughout.
- Boundary, short-pulse, prolonged-level, reset, saturation and replacement-step cases pass. Real Sync pairs prove the level reaches the actual servo. Fractional PHC advances grade tail coverage, and the indication clears after completion.
- Both explicit campaigns pass their named controls: eight servo defects and fourteen datapath defects, with two passing positive controls per campaign.
- All assigned local gate commands return zero, including all 33 commands in the default datapath sweep. The servo suites pass 100 unit, 8 rail, 113 step and 90 slew checks; the connected phase passes 58 checks.
- The builder's board-report calibration arm is NOT RUN because the required report is absent. Hardware was not run. Round-3 hosted checks await publication.

The standalone servo adds 7 LUTs and 2 registers. Isolated release alignment adds 1 LUT and 4 registers; memory and arithmetic resources are unchanged. These are isolated parent-logic measurements, not a whole-datapath area delta. The adopted processor's separate published area measurement is outside these figures.

## Round 2

The default servo suite retains unit, rails, step and slew checks. The long slew mutation campaign now runs through the explicit `slew-mutants` target. The 1800-second default budget is unchanged.

A boundary-coincident step case requires one discard. A unit case requires four fresh guard trips after a slew discard, matching the existing step-discard rule. The tail check measures the PHC itself and verifies eventual release. Added controls remove the step exclusion, retain the guard streak, and insert one addend stage without extending the tail. Each fails its named check. Campaign inventories, trigger files and the streak contract are current. Product RTL behavior is unchanged in this round.

| Clean two-CPU default | Base | Round 1 | Round 2 |
|---|---|---|---|
| Local wall clock | 516.943 s | 1652.793 s | 952.797 s |

The base and round-1 runs use CPUs 8-9; round 2 uses CPUs 10-11 on the same shared host. Round 2 leaves 847.203 seconds, or 47.1%, of the budget. The Makefile records the measurement.

The published coincidence, tail, latency and deduplication probes were rerun. Clean probes pass; the boundary-exclusion mutant fails the new shipped case. Shortened-tail controls fail as expected. The unit-only exclusion mutant remains a recorded survivor; its killing case is in the slew suite.

Round-2 hosted acceptance passed on `b94f53cc`. The current local head needs independent re-review and new hosted evidence after publication. No push, PR edit or dev merge was performed.

## Round 3

Local head: `92ad1687d84ff077f872719b4f1df601f82064d2`.

U15 now starts from one guard trip before two tainted windows. A discard that increments the streak or re-bases like a guard trip fails the fresh-trip check. Both variants join the explicit campaign, which passes 10/10 with every defect rejected by its named check. The unchanged published reviewer script reports one clean pass and four killed variants: the three slew-streak variants fail U15, and removing the step-streak reset fails U12.

The budget now records the hosted 1159.1-second window, leaving 640.9 seconds (35.6%), for head `b94f53cc` in merge `4bb4317`: [run 36113401588](https://github.com/kebag-logic/milan-fpga/actions/runs/36113401588), [job 108001867446](https://github.com/kebag-logic/milan-fpga/actions/runs/36113401588/job/108001867446). The Makefile labels its margin as local and points to this hosted basis.

The clean two-CPU default completes in **936.448 seconds** on CPUs 8-9, compared with round 2's 952.797 seconds. All 100 unit, 8 rail, 113 step and 90 slew checks pass. This leaves 863.552 seconds (48.0%) of the unchanged 1800-second budget. These are shared-host local samples.

Connected-campaign triggers now include the shadow addend latch, slew pass-through and processor pin changes. The campaign table and suite index both name eight servo defects and two positive controls.

The connected leg passes 58/58 and its full campaign passes 16/16. All 33 commands in the default datapath sweep and every assigned local gate return zero. The builder's board-report calibration arm remains NOT RUN because its required report is absent; no compiler-related arm was skipped.

No RTL logic or processor pin changed in this round. Area reproduces the prior isolated measurements, with no round-3 delta. The conservative release-tail observation remains outside this assignment, under #495. The current head remains unpushed; no PR edit or dev merge was performed.

## Merge-dev

Local merge head: `b376f6113b388929fe82e883d400e5361319b966`.

Merged dev `864b36f5e9450ef64f75ca3f0d68c44330e447d7` into the reviewed lane head `92ad1687d84ff077f872719b4f1df601f82064d2`. Both changelog entries and both campaign inventories are retained. The pin pair is gPTP `5dce647a` and processor `990f9652`. The submodule diagram and raster manifest were regenerated; ROM records reproduce the merged ledger. Conflict resolution adds no product behavior.

All requested documentation, static and behavior checks pass. The existing frontend and lint ratchets are unchanged. Behavior coverage is 344 scenarios and 1,739 steps. The builder passes with its existing board-report calibration arm NOT RUN because the required report is absent; no compiler-related arm was skipped. The clean two-CPU default completes in 944.14 seconds, with all 100 unit, 8 rail, 113 step and 90 slew checks passing. It leaves 855.86 seconds (47.5%) of the unchanged 1800-second budget. The full connected mutation campaign passes 16/16. The servo campaign passes 10/10, including two positive controls and eight named defect rejections. All 34 commands in the default datapath sweep return zero across four recorded chunks; its render and GM-step controls pass 6/6 and 4/4. The connected leg passes 58/58, and the clock-ratio leg passes 144/144. Final root and submodule cleanliness checks pass. No new validation failure was found.

The isolated area measurements reproduce 864 to 871 LUTs and 790 to 792 registers for the servo, plus 1 LUT and 4 registers for release alignment. No merge-round change affects those blocks; these remain isolated estimates.

The merge head requires its assigned delta review. This body is prepared locally for publication.

## Docs round

Local head: `4538d7c03dc4f56d7ed4c971603e15bda82050a8`.

The datapath suite README now derives fourteen explicit controls from the executable inventory: eleven tabulated controls plus three slew controls. The evidence-reader disposition now names all eight servo defects, including streak increment and slew discard counted as a guard trip.

Both documentation CI modes and all assigned evidence, style, contents, anchor, path, language-idiom and whitespace gates pass at this head. The changes are limited to documentation and disposition text. The merge-round assignment records the review bar met at this head.

## Second merge-dev round

Local merge head: `ddf8151c478fc54c98608589c1afe9525739d6a4`.

Merged dev `5c78ce2e9d831e588e759b696ed549804327e4d8` into reviewed head `4538d7c03dc4f56d7ed4c971603e15bda82050a8`, as assigned on #545. The three conflicting hunks retain both changelog sections and both campaign classifications. The #545 eight-defect servo classification and connected slew controls remain intact; the #443 render-CSR classification is retained. There is no additional manual source change, pin change or ratchet change. Generated contents reproduce without a tracked-file update.

The clean two-CPU servo default passes in 938.63 seconds on CPUs 8 and 9, with 100 unit, 8 rail, 113 step and 90 slew checks. The unchanged 1,800-second budget leaves 861.37 seconds (47.9%) of local margin. Both documentation modes, the static gates and all 101 evidence-reader controls pass. Behavior coverage passes 344 scenarios and 1,739 steps. The builder returns zero with only its existing board-report calibration arm NOT RUN; no compiler-related arm is skipped.

The isolated servo area reproduces 864 to 871 LUTs and 790 to 792 registers, with memory and arithmetic resources unchanged. The servo source is unchanged from the reviewed head, so this merge adds no servo area. This is an isolated estimate, not a whole-datapath area claim.

Both explicit campaigns pass: 10/10 for the standalone slew controls and 16/16 for the connected controls. All 33 commands in the default datapath sweep return zero across four recorded chunks; its render and GM-step controls pass 6/6 and 4/4. The connected leg passes 58/58, and the clock-ratio leg passes 190 checks, including the incoming render-status cases. The receiver and shadow suites pass. Final root and submodule checks are clean. No new source-level validation failure was found. The initial missing documentation dependency was supplied in an isolated environment; no tracked file was changed for setup. The assignment requires one independent merge-delta review. No push, PR edit or merge into dev was performed.
