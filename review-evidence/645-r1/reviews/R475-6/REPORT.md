[R475] NEGATIVE - exact head 1e79ebdc06528edff74c0a7f530f20f99e3326a2

External independent review R475-6 of issue #645 / PR #672, including the publicly assigned #647 work. Tree: `067514daece6faf87e9d675bd628759c7bec83fa`; comparison base: `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`.

All five lenses were applied. One new MINOR affects Tests and Docs. The source repair for the prior MAJOR R474-4-F1 is verified, but its required exact-head hosted verification remains open. Conformance, RTL and Robustness are CLEAN; Tests and Docs are UNCLEAN. This review does not authorize merge.

The review followed the requested reconstruction order: repository contract and documentation map; issue body and public scope decisions; requirements and interface authorities; complete base-to-head diff and history; public executable evidence. The independent verdict and ledger were written in `independent-verdict.txt` before reading prior public reviewer findings. Its preliminary F1 locator `:69` is corrected to `:64` below. No private author material or other checkout was used.

**Scope and authority.** The [issue acceptance](https://github.com/kebag-logic/milan-fpga/issues/645) asks for an established cause, removal or explicit bounded declaration of the discontinuity, and a bench repeat. The public stage-2 and subsequent rulings assign the simulation/implementation work to this lane and retain the bench repeat as a manager duty. They include the INTERNAL hold from #647, both directions of the settle action, the [two-output-PDU span amendment](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6009767440), [qualified recovery and its narrow residual](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6010634115), resource/timing acceptance, and the [default-suite scheduling decision](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6073617515). `scope-decisions.txt` preserves the public manager rulings examined.

The operative contract is eight consecutive LOCKED windows under following; 2,048 qualifying ticks at INTERNAL; a 2^20-tick ceiling; a depth-16 loopback ring targeting eleven events at PDU end; exact symmetric holds/drops, paired channels, at most two consecutive affected output PDUs, strict ordering outside the action, and unchanged slip counters for the declared action. Recovery requires 2,048 consecutive quiet engaged ticks. The second-hold residual during recovery is expressly bounded in scope; it grants no steady-state slip allowance. The arrival campaign crosses both offset signs, sixteen phases and four envelopes through 60 us, with both ring margins above one tick. Render-law checks use gradable windows. The original bench requirement remains pending, rather than being represented as satisfied by simulation.

**R475-6-F1 — MINOR — Tests, Docs — `tb/verilator/follow_ring/trace_table.py:64` — The diagnostic table reports a declared recenter as a slipped frame.**

Authority/evidence: `docs/design/MEDIA_CLOCK_FOLLOWING.md:1096,1232` and `docs/reference/REGISTER_MAP.md:1870` separate the declared recenter from slips. The helper promises “frames the ring slipped” at line 13, but increments that column whenever adjacent margins rise by more than half a tick. It does not distinguish the declared action. On unchanged reviewed source, `run-trace-probe.py` runs the normal INTERNAL pull-in case, then the helper over the same trace. `trace-probe.log` reports 18 passing checks, zero slips before the action and zero after it. The action is at 5.454116560 s, or +0.854116560 s after the hold. `trace-table.csv` reports `slips=1` in the +0.90 s row, where the margin jumps from approximately 1.3 to 5.3 ticks. `evidence-audit.json` independently records this discrepancy.

Impact: a passing settle action produces a false measured slip in the generated diagnostic table. This can misdiagnose the mechanism and contradict the actual counter evidence. The running RTL counters and the harness's acceptance verdict are correct in this probe; the finding is against the diagnostic measurement and its documented meaning. Because a generated number changes, this is not wording RESIDUE.

Required outcome: the table must distinguish actual slips from declared recenter actions, or cease presenting the margin-jump heuristic as a measured slip count. Its description must match the resulting quantity.

Verification: repeat `run-trace-probe.py`; the normal passing trace must report zero actual slips. Add controls demonstrating that genuine duplicate/skip events remain observable and are not masked with the recenter. The current reproducer intentionally retains the faulty output as evidence. Source was not edited.

**R474-4-F1 — MAJOR — Tests, Docs — RETAINED pending final verification — default-suite wall clock.**

Artifacts: `tb/verilator/follow_ring/Makefile:22,70`; `tb/verilator/milan_dp_render/Makefile:45,210`; `docs/testing/TESTING.md:271,295`; [original finding](https://github.com/kebag-logic/milan-fpga/pull/672#issuecomment-6073609394); `hosted-status.json`.

Authority/evidence: the public round-2g decision keeps the existing 1,800-second guard and requires the cold defaults within its 1,440-second headroom limit, preserves moved campaigns, and requires an exact-head hosted pass. The default follow target now retains four standing legs and moves twelve rebuilt controls to an explicit target. The render pull-in campaign retains eighteen boot phases plus the former activity history. The public author receipts record 354.107 and 733.249 seconds for the two defaults: 559.489 and 1,158.533 seconds at the assigned 1.58 factor. Final file hashes match the author's source-binding receipt. The published nineteen-leg render campaign has 830 passing checks, and its missing-action control is caught. The evidence-contract check and 105/105 self-checks pass independently here.

Impact and remaining outcome: the source-side scheduling and measurement corrections are demonstrated, but a successful hosted aggregate at this head has not yet been observed. At the saved snapshot four long simulation shards are still in progress; one has completed successfully. Do not substitute the local projection for the requested hosted result. No repeat of the former timeout is alleged at this head.

Verification: the manager must obtain the exact-head hosted aggregate with both affected suites PASS within their guards and accept the required local replica. Retain this finding until that evidence is published and reviewed. The previous review's severity and lenses are preserved.

**Independent checks and public evidence.** Commands, raw logs, return codes and elapsed seconds accompany the packet; `README-reproduce.md` describes portable reproduction. The pinned simulator executable's identity was checked before use. Independent jobs were concurrent under foreground parents, with at most sixteen compiler workers and no detached shell job.

| Reviewer execution | Result / receipt |
|---|---|
| Capture crossbar suite, including LRC, held-empty-pair and SPAN cases | 785 checks, zero failures; `chmap.log` |
| Extracted production settle controller at 6.25, 25, 50 and 100 MHz | All four pass; `settle-control.log`, `control-receipts/` |
| Fine and paired INTERNAL pulls at 25 MHz | 10/10 pass; `small-pulls.log`, `small-pull-receipts/` |
| Normal INTERNAL pull-in | 18 checks, zero failures; `pullin.log` |
| Long B8 source-switch run, nominal arrivals | 48 checks, zero failures; all three post-settle render windows on the law and zero post-settle slips; `b8.log` |
| Long B8 run, reversed offset and 0–60 us arrival lateness | 45 checks, zero failures; zero post-settle slips and minimum empty/full margins 4.139520/3.048960 ticks; render windows ungradable, not a render-law pass; `b8-fast-wide.log` |
| Passing pull-in plus diagnostic-table counterexample | Simulation passes; table discrepancy reproduced; `trace-probe.log`, `trace-table.csv`, raw CSVs |
| Traceability regeneration check | Current, seven generator controls pass; `matrix.log` |
| Evidence-contract check and self-checks | Pass, 105/105; `evidence-contract.log` |
| Resource baseline consistency | Three endpoints pass; `resource-baseline.log` |
| Public measurement/source binding audit | Records, policy and final file hashes match; `evidence-audit.json` |
| Final raw source, modes, index and gitlink verification | Exact and clean; `tree-verification.json` |

The [published author evidence](https://github.com/kebag-logic/milan-fpga/tree/1747b39f600de8e8c4b22437817984aa9430a33e/review-evidence/645-r1) supplies the broader campaigns and full gate receipts. Inspected files and their verified published blob identities are indexed in `public-evidence-index.json`; selected public receipts are copied under `author-receipts/`. The author records 44 command results at zero, twelve caught follow controls, the preserved render defaults, and the nineteen pull-in legs. Earlier author arrival and quiet-distribution receipts support the declared four-envelope/two-sign campaign and the quiet-band choice. These are author execution evidence, not reviewer reruns or a manager source bank.

The own-logic measurement at `85db353400c6bf3965d279a9f5b5d47e08a0d1ed` is 113 LUTs / 78 registers, below the ruled 120/120 limit. The current capture blob matches that measurement input and the production settle extraction is byte-identical to that head (`own-area-source-audit.json`). This is preserved public measurement evidence, not a new synthesis run.

The resource rebaseline was measured at `a5ca6e5110d515bf5f894f87b94f9bf6f6836bbb`. No HDL or synthesis recipe changed from that measurement to this head. All three current baseline records equal those measured records; tolerance/floor/ceiling policy equals the comparison base. The routed record is 50,267 LUTs, 54,413 registers, 15,779 slices, WNS +0.299 ns and WHS +0.031 ns. The inspected raw utilization and route-status reports agree, with zero routing errors. The standalone records remain 23,179/19,779 and 30,135/27,380 LUTs/registers. The standalone timing numbers are not routed timing acceptance. The documented 71-slice remaining capacity and existing resource-policy exception remain real limits.

**Prior public findings, resolved or retained at this head.** These dispositions follow the independent pass and preserve the original lenses. Sources are the [first external round](https://github.com/kebag-logic/milan-fpga/pull/672#issuecomment-6009109435), [first internal round](https://github.com/kebag-logic/milan-fpga/pull/672#issuecomment-6009527655), [second internal round](https://github.com/kebag-logic/milan-fpga/pull/672#issuecomment-6032462363), and subsequent public verdicts on this PR. Formal review and inline-comment collections were also checked; both were empty.

| Prior ID | Severity / all attributable lenses | Disposition and current evidence |
|---|---|---|
| R475-1-F1 | MAJOR / Conformance, RTL, Robustness, Tests, Docs | RESOLVED under the explicit two-PDU amendment. `chmap_capture/sim_main.cpp:1920` checks 72 direction/phase/offset cases at both outputs, exact consecutiveness and strict outside order; current capture run passes. |
| R474-1-F1 | MAJOR / Conformance, RTL, Robustness, Tests, Docs | RESOLVED. `KL_chan_map_capture.sv:957` drops the full excess; the ten-left case at `sim_main.cpp:1869`, public both-sign campaigns and current capture run support the symmetric law. |
| R474-1-F2 | MAJOR / Conformance, RTL, Robustness, Tests, Docs | RESOLVED under the recovery ruling. Two-cycle excursion arm, qualified recovery and declared second-hold residual are implemented at `milan_datapath.sv:6589`; all ten current fine-pull cases and four controller rates pass. |
| R475-1-F2; R474-1-F4 | MINOR / Docs | RESOLVED. `MEDIA_CLOCK_FOLLOWING.md:1092` and `TIME_SYNC.md:386` explicitly state the 2,048-tick disengaged dwell, checked by the controller cases. |
| R475-1-F3 | MINOR / Conformance, Tests, Docs | RESOLVED in source. The text-input marker at `follow_ring/Makefile:37`, generator exclusion and current matrix check preserve truthful hierarchy credit. |
| R474-1-F3 | BLOCKER / Tests, Docs | RESOLVED in source by the same correction and passing check. Hosted acceptance remains separately pending; local success is not described as hosted success. |
| R474-2-F1, superseding R474-1-S1 | MINOR / Conformance, RTL, Robustness, Tests, Docs | RESOLVED. `KL_chan_map_capture.sv:896` excludes held pops from duplicate counting; the case at `chmap_capture/sim_main.cpp:1793` passes with an empty pair before its first commit. Public HELD-DUP and STARVED-HELD-DUP controls are caught. |
| R474-4-F1 | MAJOR / Tests, Docs | RETAINED pending hosted verification, as detailed above. |
| R475-2-R1 | RESIDUE / Docs | RESOLVED: the old “not pushed” sentence is gone. Current Status names this head and keeps the outstanding hosted condition. |
| R475-2-R2 | RESIDUE / Docs | RESOLVED: `MEDIA_CLOCK_FOLLOWING.md:1086` now locates the preserved old trigger as `g_src_recentre`. |
| R474-2-R1; R474-2-R2 | RESIDUE / Docs | RESOLVED: `TIME_SYNC.md:489` states the recovery exception; `REGISTER_MAP.md:1870` uses dropped “events.” |
| R474-3-R1 | RESIDUE / Docs | RESOLVED: `follow_ring/mutants.py:6,11` identifies four capture plants and documents `--select`. |
| R474-3-R2; R474-4-R1 | RESIDUE / Docs | RESOLVED: `TESTING.md:525` names the full twelve-control list and links to the simulation plan's controls column. |
| R474-2-S1 | SUGGESTION / Tests | RETAINED; details below. |
| R474-2-S2 | SUGGESTION / Tests, Docs | RETAINED in its remaining 50 MHz scope; details below. |
| R474-2-S3 / R474-1-S2 | SUGGESTION / Tests | RETAINED; details below. |

R475-3, R475-4 and the R475-5 composition review introduced no additional unresolved required finding. Their carried residues and suggestions are accounted for above. The current resource rebaseline addresses the earlier composition review's remeasurement duty; final merge-candidate validation remains separate.

**Retained optional suggestions.**

- **R474-2-S1; SUGGESTION; Tests.** Artifacts: `follow_ring/settle_control.py:53,58`, `quiet_distributions.py:68`, and production `SETTLE_EXC_ERR_C`. The directed cases exercise ±1 as quiet and 3 as an excursion, leaving 2 unpinned; the distribution reader accepts a supplied band. Impact: an unintended one-cycle band reduction has a coverage gap. Optional outcome: pin the inclusive two-cycle boundary to the production constant. Verification: ±2 stays quiet and a one-cycle-band mutation is rejected.
- **R474-2-S2; SUGGESTION; Tests, Docs.** Artifacts: `MEDIA_CLOCK_FOLLOWING.md:1161,1215` and the clock configurations in the follow and render Makefiles. The 100 MHz integration logs now retain measured latency, while quiet distributions and fine pulls use reduced rates. There is still no standing 50 MHz quiet-distribution and recovery-latency campaign. Impact: shipping-clock dynamics rely partly on the documented scaling argument; the four-rate controller test checks the FSM, not full-loop dynamics. Optional outcome: record those 50 MHz measurements. Verification: a gradable full-loop run records quiet extrema and action/rearm times.
- **R474-2-S3 / R474-1-S2; SUGGESTION; Tests.** Artifact: `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:1101`. The physical-network simulation can report its declared-action checks as uncounted NOT RUN when it sees no decisions. Separate controller and missing-action tests provide non-vacuity evidence. Optional outcome: require an action in the scenario expected to produce one. Verification: suppress that action and require the scenario to fail.

These suggestions do not affect clean coverage. No new wording residue is raised.

[R475] PASS Conformance — `docs/design/MEDIA_CLOCK_FOLLOWING.md:1084,1190,1232`; issue #645 public rulings; resource audit — Applied the settled lane acceptance to the implemented trigger, exact bounded discontinuity, campaign envelopes and resource policy. The original bench repeat is an explicit manager duty.

[R475] PASS RTL — `hdl/milan/milan_datapath.sv:6566`; `hdl/ieee1722/aaf/KL_chan_map_capture.sv:879,1069`; `follow_ring/dp_glue.py:46`; capture/controller receipts — Checked clock/reset ownership, finite counters and ceiling, pulse routing, priority, per-stream pending state, symmetric pointer/count updates, simultaneous pop/push and pair alignment. No new crossing or unresolved architecture defect found.

[R475] PASS Robustness — `chmap_capture/sim_main.cpp:1740,1793,1907,1920`; `follow_ring/settle_control.py:35`; `small_pulls.py`; current focused receipts — Checked unprimed/empty/full states, first-beat ordering, flush/reset, no-op action, interrupted dwell, re-engagement, ceiling and recovery, subthreshold and repeated holds, output epochs and late arrivals against the explicit residual.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #645 body/rulings; REQUIREMENTS.md; MEDIA_CLOCK_FOLLOWING.md:1084–1258; REGISTER_MAP.md:1870; resource/evidence audits | R475-6 | 1e79ebdc06528edff74c0a7f530f20f99e3326a2 |
| RTL | CLEAN | milan_datapath.sv:6566–6667; KL_chan_map_capture.sv:879–1104; dp_glue.py; four controller-rate receipts; capture log | R475-6 | 1e79ebdc06528edff74c0a7f530f20f99e3326a2 |
| Robustness | CLEAN | Capture LRC/SPAN and reset/flush cases; controller recovery/ceiling cases; fine-pull and long-switch receipts; public arrival campaigns | R475-6 | 1e79ebdc06528edff74c0a7f530f20f99e3326a2 |
| Tests | UNCLEAN | trace_table.py:64 and counterexample; default target/campaign wiring; public controls; traceability/evidence checks; hosted snapshot | R475-6 applied; no clean covering round: F1 and retained R474-4-F1 | 1e79ebdc06528edff74c0a7f530f20f99e3326a2 |
| Docs | UNCLEAN | trace_table.py:13 measurement promise; design/time/register/testing docs; generated matrix; resource records; public PR/evidence | R475-6 applied; no clean covering round: F1 and retained R474-4-F1 | 1e79ebdc06528edff74c0a7f530f20f99e3326a2 |

**Limits and pending manager duties.** This is source review with focused executions, not a fresh full-bank run. No manager source bank exists at this exact head and none is inferred. Source validation here uses the author's published gate receipts plus the reviewer checks described above. Historical resource measurements and earlier candidate banks are not the final current-dev candidate evidence.

The saved hosted snapshot (`2026-10-09T04:25:20.421225+00:00`) has four completed successful synthesis shards and several completed fast/documentation jobs; one completed successful simulation shard; four simulation shards and other jobs remain in progress. The Physical gPTP context is SKIPPED. Its skipped status and the successful scheduling job do not establish execution. Hardware calibration is NOT RUN; field skips and simulation logs are not hardware proof. The build receipt's historical gate-11 calibration gap remains uncovered.

The manager must publish the review, obtain correction and independent re-review of F1, finish hosted/replica acceptance and R474-4-F1 verification, obtain both required positive reviews with no review in flight, construct and validate the final candidate against current remote dev using its builder/native banks, and link those receipts on the PR. Source base and supplied live dev were both `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`; they must be checked again at the merge turn. Explicit maintainer merge authorization, post-merge containment, the assigned physical bench repeat, and issue/project closure remain manager duties. Nothing in this packet grants any of those results.

No source changes, commits, pushes, GitHub writes, hardware actions or full banks were performed. The final verification checks 1,231 root tracked blobs and the initialized required dependencies (104, 562 and 214 tracked blobs), all raw bytes/modes and indexes exact. All five root gitlinks match the reviewed tree. Disposable files remain only in this packet's `scratch/`; all publishable receipts are listed in `MANIFEST.sha256`. All reviewer-launched jobs have completed.

R475-6 FINISHED
