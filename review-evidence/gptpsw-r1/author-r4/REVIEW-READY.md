# [A814] Round 4 corrections and the ruled hot-list relearn, PR #966

Branch `opt-gptp-sw-1`, head `8267b8951616cfd570baf690835d4b0d38f14596`, nine local commits on `8167b70d`.
Nothing pushed; no PR or issue comment added or edited. HANDOFF-r4.md carries the integration details;
PR-BODY.md is the replacement body draft, with no attribution footer.

The earlier STOP at `e81cecdb` is superseded by the relearn required by #884
[issuecomment-7084113326](https://github.com/kebag-logic/milan-fpga/issues/884#issuecomment-7084113326).
The approved limits did not move. All seven held 8x8/1if rows now pass their ledger; the AECP row is
62.12258 ms against 62.16 ms, the ACMP row 62.45305 ms against 62.62 ms. Both turnaround measurements
are below 10 ms, and neither image has a work pass above 2.0 ms.

Validation collection is complete. The full final-head builder suite passes with the same two explicitly
NOT RUN arms as before; the fresh closed-loop baseline and all 14 plants pass. The packet is ready for
independent re-review, with no claim that the earlier negative reviews approve these corrections.

## What each finding became

| Finding | Severity | Fix at its cause | Regression test that fails at `8167b70d` | Plants |
|---|---|---|---|---|
| R884-2-F1 multiple responders without Follow_Up keep asCapable | MAJOR | `pd_multi` clears asCapable, and so the publication, when a second response is received, in flight or after its exchange completed; the cease counts distinct clock identities and keeps its resume rules (`4e934621`) | `Scripted.MultipleResponsesWithoutFollowUpClearAsCapableAtOnce` (the reviewer's probe, from an asCapable port, through the cease and its five-minute end), `ASecondResponseClearsAsCapableBeforeItsExchangeCompletes` (a late Follow_Up restores nothing), `OneClockAnsweringTwiceClearsAsCapableAtOnceAndDoesNotCease`; coverage, passing there too: `ALateSecondResponderClearsTheAsCapableOfACompletedExchange` | `multiple-responses-cleared-at-completion` (four kills) |
| R884-2-F2 a review named in a source comment | RESIDUE | the reviewer's exact text (`07784595`) | | |
| R883-2-F1 a slave step inside the envelope's span drops the far port | MAJOR | peer delay runs on the LocalClock 802.1AS-2020 11.2.19.3.3 assumes, the PHC less every step the servo applied (`local_off`): the port's own t1, t4 and the t2, t3 it reports are taken on it, so a step of either port, of any size, reaches no rate window and no turnaround (`4e934621`) | `Net.AForwardStepOf300us`, `AForwardStepOf400us`, `ABackwardStepOf300us`, `ABackwardStepOf400us` at 10 ms, `ABackwardStepOf475usKeepsAsCapableAt5msTurnaround`; coverage: `AForwardStepOf150us` at 10 ms, `Scripted.AResponderThatStepsItsClockReachesNoRate` (the envelope, for a peer that stamps on a stepped PHC) | `steps-left-on-the-local-clock` (the own-step test and the five mid-step cases); `rate-envelope-dropped` now kills the third-party responder's test |
| R883-2-F2 two builder assertions fail, caused by the PR | MAJOR | at the cause: the software arm's copy of the engine's PHC tie-offs is one block, `g_gptp_engine_off`, for every build without the plane, so the datapath census keeps its sole driver of each; the census states the timestamp unit's five reads of the PHC crossing nets, gate 1c the `--sw-gptp` opt-in of #884's ruling item 6 (`7d4dc57c`); gate 1d, which the first failure had hidden in the same leg, names the split tap and the timestamp unit as gPTP EtherType owners (`ba2c8ed6`) | `test_baremetal_profile_contract` and `test_gptp_product_default_and_legacy_option`, each failing at `8167b70d` (`receipts/builder/`) | the census's planted extra reader still refused, its expected count following the census |
| R883-2-R1, R2 heads and reviews named in source comments | RESIDUE | the reviewer's exact texts, and S2's README wording (`07784595`) | | |
| R883-2-S1 the dead ternary in `rx_follow_up` | SUGGESTION | not taken: it keeps the TLV read in bounds should the refusal above it go, which the plant `follow-up-without-tlv-used` does | | |
| R883-2-S3 bind the xvlog receipt to its head | SUGGESTION | taken: the gate run's SUMMARY.txt opens with the clone's head and status | | |
| R883-2-S4 a wider crossing bench | SUGGESTION | not taken | | |

The reviewers' own probes at the fix: R884-2's `run_multi.py`, asCapable 0 from the first multi-response exchange
through the cease and ten seconds after it, its control too; R883-2's probes, 144 sweep rows (48 step sizes from
−600 to +600 us, at 1, 5 and 10 ms turnarounds), 8 probe and 11 outage cases, 0 ms out of asCapable on either port.

Found on the way: `local_off` grew the port's state 8 B, so the three gPTP memory-ledger points no longer matched
their pinned symbol sizes and the harness and the route prep refused the images; measured again in `a6323318`
(`image_gptp` 1,104 and 2,152 B, `ctrl_plat` 20,160 B; tiles unchanged at 59.0, 64.0, 62.0).

## The relearn and measurements

The list was learned at `e81cecdb` by the optimisation line's recorded procedure: the same three windows
(`backlog`, `backlog-adp`, `aecp-largest-notice`) in the 1x1/1if split image, now built with gPTP. The trace
contains 1,960,622 committed PCs and 288 sections, none outside a function section. The filter used 144 link
maps from 48 builds (three points, eight arms, plain and gPTP). It dropped the same two unlinked sections as
before, leaving 286 entries, including 15 from the gPTP port and adapter. No window was selected to fit a row.
See `receipts/hotlist/`, including the scripts, trace hashes and map-build log.

The LINKED rule now leaves aside an entry only when its whole object is compiled out. The image builder passes
`gptp` and `gptp_mbx` only for builds without gPTP. A named-absent object that actually links is refused.
The two added plants fail with `LINKED: object ... is named compiled out, yet the image links its sections` and
`LINKED: hot-list name ... is no section of the linked image`; all eight earlier plants still fail.
The hot-list check has two passing controls and ten caught plants (`receipts/final-docs/hot_plants.log`).

Measured at `631dc544`, whose executable sources are the final head's:

| Condition | 8x8/1if, burst 7 | 8x8/2if, burst 14 |
|---|---:|---:|
| Held ACMP last record | 62.45305 ms <= 62.62 ms | 62.587 ms |
| Held AECP last record | 62.12258 ms <= 62.16 ms | 61.819 ms, interface 1 |
| Pdelay responder turnaround, maximum | 0.30882 ms <= 10 ms | 0.29195 ms <= 10 ms |
| Last gPTP record under composed load | 6.11505 ms <= 10 ms | 7.75006 ms <= 10 ms |
| Composed maximum | 1.67518 ms <= 2.0 ms | 1.65729 ms <= 2.0 ms |
| Work passes above THE SHARE | 0 / 5,139 | 0 / 5,217 |
| gPTP CPU after link-up, maximum measured group | 0.212 % | 0.269 % |
| Largest gPTP contribution to one work pass | 28,640 cycles | 37,430 cycles |

`receipts/after-relearn/measurement-audit.json` independently recomputes the cost maxima and module totals from
raw logs, identifies those logs by size and full sha256, and checks both turnaround conditions and share limits.
The final head's egress checker passes both the gPTP and plain 8x8/1if images; complete seven-row tables are in
`receipts/after-relearn/egress-final-gptp.txt` and `egress-final-plain.txt`.

The harness still reports the seven known held rows over their nominal 20 ms service budgets; those are the
rows governed by the separate egress ledger, not seven new misses. The ledger passes at 8x8/1if. There is no
8x8/2if ledger: its five owed rows are 63.910 to 64.957 ms, 0.05 to 0.10 ms beyond the 1if figures; its last AECP
record is on interface 1. Applying the 1if ledger to that shape fails and is recorded as such, never as a pass.
No admission rule, service bound, share, or held-row figure was changed by this round.

For the STOP's phase analysis and before-values, see `receipts/harness/aecp-row-phase.md`. Over backlog-owed's
work passes, the unchanged adapter now takes 104,430 cycles, versus 214,320 before the relearn (149,287 before
the protocol corrections). The port takes 237,926 versus 271,145. `measurement-audit.json` distinguishes these
work-pass totals from whole-run totals that also include boot. The plain 8x8/1if AECP row is 61.84002 ms.

Memory is within every recorded image ledger. The platform gPTP image has 152,072 B ROM and 99,392 B SRAM,
62 RAMB36, with `ctrl_plat` at 20,160 B and 1,528 B ROM allocation spare. The fixture gPTP entries remain
59 and 64 RAMB36; `image_gptp` is 1,104 B at one interface and 2,152 B at two. The relearn changes alignment,
not the allocated tiles. `receipts/memory-631dc544/` contains the five-point platform gate and memory tests.

## Gate evidence and its scope

Every receipt below is under this packet's `receipts/`, indexed from the files present. A result is attached to
its actual run head. `after-relearn/source-equivalence.txt` proves the unchanged inputs where an earlier run is
retained; it does not represent an earlier run as an exact-head run.

| Gate | Run head | Result | Receipt |
|---|---|---|---|
| Full simulation sweep, four shards | `e81cecdb` | 67/67 suites, zero in-suite failures; includes mbx publication crossing, TSU and split-sw | `sweep/` |
| Field campaigns | `e81cecdb` | 164 and 675 cases pass; no skips in this supplemental run | `sweep/tsn_fuzz-field-campaigns-e81cecdb.log` |
| 73 docs, idiom and light rtl-fast commands after relearn | `334ca4b7` | 73/73 rc=0; xvlog executed, 142 files, zero findings | `gates-334ca4b7/` |
| Final documentation correction, paths, audit, hot-list check/plants, diff check | `8267b895` | All nine commands pass | `final-docs/` |
| Full builder suite, required RV32 and elaboration | `8267b895` | rc=0; every gate passes except two explicitly NOT RUN arms: the ineffective MAKEFLAGS plant and the absent calibration report | `builder-final/` |
| Four firmware-gate shards after relearn | `631dc544` | 4/4 rc=0; 826/826 controls caught; gPTP and UBSan 63 tests each; hot-list plants caught | `fwgate-631dc544/` |
| Eight added port regressions against reviewed port | `4e934621` test suite, `8167b70d` port | Eight fail on the old port, 55 pass | `gptp/test_gptp-on-8167b70d-port.log` |
| Port suite with UBSan; port mutation campaign | `4e934621` | 63/63 tests; 41/41 plants caught | `gptp/` |
| Reviewers' multi-response and step probes | `4e934621` | Immediate capability invalidation; no capability outage in all step/turnaround cases | `gptp/` |
| Fresh closed loop and planted defects | `334ca4b7` | 48/48 checks and 14/14 plants caught; flood: 490 stamped, zero unstamped or lost egress records, lock 2.9 s, worst later offset 95 ns | `closedloop-final/` |
| Datapath split-cdc / split-sw | `a6323318` | 13 / 152 checks pass | `milan_dp/` |
| Publication census and self-test | `a6323318` | 246 checks, 164 control arms, 57/57 rules proved | `census/` |
| Synthesis portability, four shards | `a6323318` | 64 tops and the tied-input/tap-purity gates pass | `yosys/` |
| Platform memory ledger and memory tests after relearn | `631dc544` | Five points, nine controls; no findings | `memory-631dc544/` |
| Budget harness self-test after relearn | `631dc544` | Zero failures | `after-relearn/harness-selftest-631d-tail.log` |
| Split CPU boot, 1x1/1if and 8x8/1if, rebuilt after relearn | `631dc544` | Both pass; expected non-evidentiary board-grader diagnostics retained | `after-relearn/splitboot-631d.log` |
| Six budget groups each, both 8x8 points, gPTP and plain | `631dc544` | Zero refusals, zero share misses; held findings treated as described above | `harness-631dc544/` |
| Seven held 8x8/1if rows, rechecked with final checker | `631dc544` data, `8267b895` checker | All seven pass, gPTP and plain | `after-relearn/egress-final-*.txt` |
| Routed 8x8/1if software-gPTP build, three directives | `a6323318` | All three meet #818: +0.292/+0.036, +0.281/+0.036, +0.173/+0.067 ns setup/hold | `route/` |

No RTL changed after the routed `a6323318` head. The routes remain evidence of that head's image, not of a
newly routed post-relearn firmware image. Re-routing was conditional on further RTL change, so was not repeated.
After the sweep at `e81cecdb`, executable changes were confined to the hot list and its linker checker/caller;
those are covered by the post-relearn firmware gate, image measurements, harness self-test and rebuilt split boot.
The host-compiled closed-loop port, model, benches and RTL are unchanged. After `631dc544`, only explanatory text
changed. The final commit corrects the largest gPTP work-pass contribution to 0.374 ms.

The timestamp-unit source, bench and plants are unchanged since round 3; its 24/24 mutation result remains in
that packet, while this round's sweep reran its 36 checks. This report makes no new timestamp-unit mutation run claim.

## Handoff boundaries

Mailbox contract 2.5 is unchanged from `8167b70d`; it remains additive and hart-neutral. The second-hart lane
can retain 2.6 on top, and must relearn the hot list for its composed image. `receipts/after-relearn/hunks.md`
lists every diff hunk with file:line and reason, including the tie-off block, builder census, memory keys and layout.

One MAC remains in the product; the second MAC is #962. The software-gPTP census shape and its row list remain
owed to the census owner before onward integration. Bench qualification remains owed; no bench was accessed.
The fresh reviews of these fixes are still the reviewers' responsibility; this is an author evidence packet.

REVIEW READY 8267b8951616cfd570baf690835d4b0d38f14596
