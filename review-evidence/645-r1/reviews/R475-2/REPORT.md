[R475] POSITIVE - exact head 886e16201654ba0fd0c60c41c228ea4c75b2f6d3

R475-2 applied all five lenses to issue #645 / PR #672, including #647. All five are CLEAN at this head. Every prior required finding is resolved under the public amendments. Two optional suggestions remain, and two wording residues belong on the manager's checklist. This source-review verdict does not authorize merge or establish hardware acceptance.

Reviewed tree: `f2eb9b9b349fd5a1c13df31143c7e20df40e1ba7`.

Reconstruction and scope

Read the operating contract, contribution rules and documentation index, then issue bodies and public scope decisions, requirements and interface authorities, diff/history, and published executable evidence. Governing round-2 decisions: [6009543884](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6009543884), [6009767440](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6009767440), [6010634115](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6010634115), and [6009790232](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6009790232). Earlier rulings establish depth 16, target 11, both arrival margins, own-area accounting and manager-owned bench work.

Examined the requested `fea346e7..886e1620` comparison, the whole `4e1ddee9..886e1620` round-2 delta, first-parent history, both parents of every merge, and the 38-file net lane delta against incorporated dev `09f1841b`. The round-2 range contains the initial `f06c7426` merge plus the seven later dev merges named by the author. Seven of these eight merge trees reproduce automatically. The manual resolution at `132d79e7` preserves both dynamic-map and physical-build targets and transfers both reader dispositions into `measure_test_evidence_readers.py`, removing the obsolete duplicate module/import. See `receipts/first-parent.txt`, `receipts/merge-audit.json` and `receipts/measurement-input-identity.json`.

Evidence came from [the initial archive](https://github.com/kebag-logic/milan-fpga/tree/6efdd2447c72b9b60f5d0d9e393c851bb742945a/review-evidence/645-r1), [the round-2 archive](https://github.com/kebag-logic/milan-fpga/tree/b6f2890678684aee8483f61e393167cae02cf2da/review-evidence/645-r1/author-r2c), and [the readiness comment](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6031559796). No private author material informed this review. The independent verdict and ledger were written before reading prior public reviewer reports for reconciliation. No current parallel review report was read.

Independent lens results

| Lens | Applied check and result |
|---|---|
| Conformance | `KL_chan_map_capture.sv:949-959,1051-1099` holds the shortfall below five or drops the full excess above five, preserving target eleven at PDU end. `milan_datapath.sv:6584-6649` implements the two-cycle arm, 196,608-tick following dwell, 2,048-tick INTERNAL dwell and 2^20 ceiling. The amended consecutive/two-output-PDU rule is enforced. `KL_render_setpoint.sv` is unchanged; the AAF presentation law remains the law in `TIME_SYNC.md:368-391`. |
| RTL | Reviewed widths, bounded drop arithmetic, pointer wrap, simultaneous push/pop composition, per-stream decisions, per-pair hold transfer, reset and flush precedence at `KL_chan_map_capture.sv:501-526,805-1099`. New state remains in the axis domain. Root bindings at `milan_datapath.sv:1308-1313,6657-6666` deliver the pulse to both rings; the original source-change trigger remains. Area input hashes match the current source. |
| Robustness | `chmap_capture/sim_main.cpp:1702-1975` covers hold five/one, drop one/five, no-op, unprimed state, flush, coincident first beat, pair coherence, six output phases and six fanout offsets in both directions. `settle_control.py:36-104` checks quiet noise, interrupted recovery, subsequent pull, active reset, source priority, disengaged settling, following dwell and ceiling at four rates. Paired pulls exercise both sides of recovery. |
| Tests | Independently built and ran capture (777/0), four controller rates, ten fine cases and 32 INTERNAL cases. Five independently planted RTL faults compiled and failed their named assertions. Decoded wire samples check exact count and strict outside order; span controls reject separated repeats, a third PDU and an extra repeat. Reviewed `sim_ax1x1gptp.cpp:669-823,1093-1106` and `verify_recentres.py`; full physical execution rests on public receipts. |
| Docs | Compared design, time, register and testing contracts against the rulings and measured receipts. `gen_module_matrix.py:140-163,536-548` excludes the marked text-only input. The exact-head check passes, including 7/7 generator controls. The matrix credits compiled leaves, not `follow_ring` coverage of `milan_datapath`, the packetizer or unrelated descendants. |

Measurements and declared residual

The two-cycle band is 320/80/40/20 ns at 6.25/25/50/100 MHz. Independent regrading of all 128 published candidate logs finds 512 quiet windows and exactly 320,462,699 samples: 5,308,613 at -1, 309,865,796 at zero, and 5,288,290 at +1 axis cycle. All 384 transient windows have one action and zero post-settle slips. Minimum empty/full margins are 2.17344/2.23488 ticks. Both signs and all four arrival envelopes are present. These are regraded public simulations, not 128 fresh reviewer executions. The standing quiet reader also passes. Receipts: `public-independent-audit.json`, `published-quiet.json`.

Recovery re-arms after 2,048 consecutive quiet ticks; an out-of-band cycle or disengagement resets that dwell. Source changes and re-engagement retain immediate arming priority. The fresh fine campaign passes 10/10, including the formerly missed boundary holds and the no-hold control. A second pull 0.10 s after the action starts inside recovery and leaves the graded shift with zero additional actions. At 1.50 s, the same pull produces one action and restores the law. The isolated first recovery is 0.409918800 s; the disturbed inside-window case itself recovers in 0.317771480 s. These are distinct observations, not a fixed timer.

`MEDIA_CLOCK_FOLLOWING.md:1143-1168` honestly states the ruled residual: another recentre is not guaranteed for a pull beginning during recovery. It names the measured stimulus set and observed maximum, and explicitly states that continuing disturbance can extend the window without a finite bound. It grants no steady-state slip allowance. The fresh 32-case campaign reproduces the 0.551148640 s isolated maximum and exactly four pre-settle slip phases for the 56 us hold, phases 0-3. All 32 have zero post-settle slips. Four before/after windows are ungradable and receive no render-law credit. Receipts: `fine/`, `pullin/`, `pullin-summary.json`.

Independent fault probes

| Planted RTL defect | Build | Named rejection observed |
|---|---|---|
| Full-side correction removed | rc 0 | `LRC: ten left drops five excess events on both pairs` |
| Held pops increment duplicate counter | rc 0 | `LRC: no recentre moved the dup counter` |
| Excursion band raised from 2 to 10 | rc 0 | `excursion did not arm` |
| Quiet band lowered to zero | rc 0 | `quiet noise armed` |
| Recovery re-arms at 1,024 ticks | rc 0 | `re-armed before quiet dwell` |

Each executable returns nonzero for its named behavioral failure. The driver returns zero only after confirming all five rejections. These are independently planted source copies, not modified expected values. `scripts/fault_probes.py`, `receipts/faults/` and `receipts/own-faults.log` retain substitutions, build receipts and raw verdicts.

Area and broader evidence

The published OOC rows sum to **+119 LUT / +82 FF**, inside 120/120: controller +33/+42, capture +86/+40. Current capture bytes and extracted controller hash match the measured sources. The routed conservative own-logic bound is +92 LUT/+80 FF. Unrelated routed variance is separate under the ruling. No new area run was performed.

The public three-directive sweep selects ExtraPostPlacementOpt: slow WNS/WHS +0.368/+0.062 ns, fast +1.633/+0.034 ns at both recorded temperatures, zero TNS/THS and zero critical warnings. AltSpreadLogic_high also qualifies; ExtraTimingOpt's +0.017 ns WNS is recorded and not selected. This meets the clarified best-of-three bar. The receipt is at `f6bd415f`; later mailbox changes are outside the shipping image elaboration. No new timing run was performed.

Public receipts report the 61-suite source sweep, physical 197/0, ordering controls 14/0, 18 render pull-in phases and 81 LAW-boundary cases. At the reviewed head, the changed-mailbox, firmware, 58-top portability and source/parser receipts pass. Lane inputs are byte-identical across the cited measurement commits; the merge audit separates inherited work. These are published broader-bank results, not independent reruns of prohibited banks.

Prior findings

Sources: [R475-1](https://github.com/kebag-logic/milan-fpga/pull/672#issuecomment-6009109435), [R474-1](https://github.com/kebag-logic/milan-fpga/pull/672#issuecomment-6009527655). Original severities and lenses are retained in this disposition table.

| Prior ID | Original severity / lenses | Disposition at this head |
|---|---|---|
| R475-1 F1 | MAJOR / Conformance, RTL, Robustness, Tests, Docs | RESOLVED by the two-PDU ruling, matching design/checker changes, and passing six-phase/two-output/six-offset checks in both directions. Count, consecutiveness and outside order remain exact. |
| R475-1 F2 | MINOR / Docs | RESOLVED: disengaged INTERNAL now explicitly waits 2,048 ticks; controller checks pass at four rates. |
| R475-1 F3 | MINOR / Conformance, Tests, Docs | RESOLVED in source: text-only exclusion, truthful regeneration and exact-head check rc 0. Hosted completion remains a manager duty. |
| R474-1 F1 | MAJOR / Conformance, RTL, Robustness, Tests, Docs | RESOLVED: full excess drop, ten-left test, physical expectation `fill - 5`, both-sign campaign evidence; independent one-sided mutation rejected. |
| R474-1 F2 | MAJOR / Conformance, RTL, Robustness, Tests, Docs | RESOLVED under the recovery ruling: measured two-cycle band, fine resolution, passing boundary cases, qualified recovery and narrow declared/graded residual. Wrong-band and early-rearm faults rejected. |
| R474-1 F3 | BLOCKER / Tests, Docs | RESOLVED in source by the traceability correction and exact-head check. No hosted success inferred from local success. |
| R474-1 F4 | MINOR / Docs | RESOLVED by accurate and tested disengaged dwell. |
| R474-1 S1 | SUGGESTION / Robustness, Docs | RETAINED as optional boundary-case clarification below. |
| R474-1 S2 | SUGGESTION / Tests | RETAINED as optional physical-oracle strengthening below. |

Suggestions and wording residues

- **R474-1 S1; SUGGESTION; Robustness, Docs, Tests.** Artifact: `KL_chan_map_capture.sv:894-895`, `REGISTER_MAP.md:1870`, physical counter comparison at `sim_ax1x1gptp.cpp:755-762`. Authority/evidence: the prior suggestion observes an actually empty fed queue counting a duplicate when a held walk precedes the first new committed event; `pop_dup_w` still does not exclude `pop_hold_w`. Impact: ordinary starvation and correction accounting need a more explicit boundary example. Optional outcome: clarify that coincidence and add a directed checker case without granting post-decision grace. Verification: move the first commit across the held walk and account for starvation separately from the declared step. Not represented as fixed or independently re-executed here.
- **R474-1 S2; SUGGESTION; Tests.** Artifact: `sim_ax1x1gptp.cpp:1096-1105`. Authority/evidence: the physical leg prints an uncounted omission if no decision occurs. Impact: that leg alone can omit its declaration checks; separate controller/following tests and missing-action mutations provide current non-vacuity evidence. Optional outcome: require a startup decision in the scenario expected to produce one. Verification: suppress it and require that scenario's check to fail.
- **R475-2 R1; RESIDUE; Docs.** Artifact: PR body, Status paragraph (`receipts/pr-state.json`). Authority/evidence: the published head is the pinned commit, but the paragraph says `Not pushed; awaiting independent re-review.` Impact: stale publication wording only; no measurement, test, verdict, generated artifact or conformance claim changes. Exact fix: `Published at this head; awaiting independent re-review.` Verification: compare the paragraph with the published head. Manager residue checklist.
- **R475-2 R2; RESIDUE; Docs.** Artifact: `MEDIA_CLOCK_FOLLOWING.md:1086`. Authority/evidence: the parenthetical locator for the preserved #386 trigger says `g_settle_recentre`; the preserved trigger is `g_src_recentre`. Impact: incorrect neighboring-block locator only; the behavioral table and implementation stay unchanged. Exact fix: replace only that parenthetical `g_settle_recentre` with `g_src_recentre`. Verification: follow the corrected locator in `milan_datapath.sv`. Manager residue checklist.

Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #645/#647 and four round-2 rulings; `MEDIA_CLOCK_FOLLOWING.md:1091-1251`; `TIME_SYNC.md:368-391`; controller and capture correction; public/fresh campaigns | R475-2 | 886e16201654ba0fd0c60c41c228ea4c75b2f6d3 |
| RTL | CLEAN | `KL_chan_map_capture.sv:501-526,805-1099`; `milan_datapath.sv:1308-1313,6015-6025,6501-6666`; merge audit; area input hashes; controller and fault receipts | R475-2 | 886e16201654ba0fd0c60c41c228ea4c75b2f6d3 |
| Robustness | CLEAN | `chmap_capture/sim_main.cpp:1702-1975`; four-rate controller; ten fine cases; 32 pull-in cases; five independent faults | R475-2 | 886e16201654ba0fd0c60c41c228ea4c75b2f6d3 |
| Tests | CLEAN | Capture 777/0; span/fanout controls; `follow_ring/sim_main.cpp:669-1090`, extraction/mutation drivers; physical checker/public controls; traceability 7/7; raw receipts | R475-2 | 886e16201654ba0fd0c60c41c228ea4c75b2f6d3 |
| Docs | CLEAN | Design/time/register/testing contracts; independently recomputed quiet/recovery figures; generated matrix check and rows; issue/PR evidence; prior-finding dispositions | R475-2 | 886e16201654ba0fd0c60c41c228ea4c75b2f6d3 |

Limits and manager duties

Fresh runs are focused simulations. The full arrival grid was publicly regraded, not independently rerun. Late-arrival campaigns omit 288 render-law windows while grading slips/margins. Ambiguous windows earn no law credit. Four pre-existing render-mutation failures remain with #657. The ruled second-pull residual is accepted scope, not a repaired guarantee. The absent Arty build-tree arm is unchanged and NOT RUN. Physical calibration is NOT RUN; field skips and simulations are not hardware proof.

The exact-head hosted snapshot (`receipts/hosted-checks.json`) records successful executed lint, firmware, conformance and selected portability jobs, with other jobs still in progress. Physical gPTP is **skipped**, not executed. No aggregate completion is claimed. The manager owns hosted/local-replica acceptance; neither was launched here.

The manager must finish required hosted acceptance, reconcile the companion review, carry residues, validate the final current-dev candidate with the full required bar, obtain maintainer merge authorization, complete containment, and run the #645/#647 physical repeats. Source base `fea346e7`, reviewed head `886e1620`, and incorporated dev `09f1841b` are distinct evidence identities; this review does not validate a later candidate.

Reproduction and restoration

Set `REPO` to the detached clone, `PACKET` to this packet and `SIM` to the scoped simulator. Its verified version and launcher digest are in `receipts/identity.json`. With the public archive object present:

```sh
python3 "$PACKET/scripts/reproduce.py" --repo "$REPO" --sim "$SIM"
```

Portable scripts keep disposable trees/builds in `scratch/`, cap concurrent builds at two and campaign jobs at four, and wait for each foreground subprocess. Captured commands, logs and return codes distinguish clean runs from expected fault failures. Build-output copies in `receipts/build-public/` replace one private home prefix; `redactions.json` records original and published hashes. Simulation outputs are raw. No source fixes, commits, pushes, GitHub writes, shared installs, hardware work or other-checkout edits occurred.

`receipts/final-tree.json` verifies 1,162 tracked superproject blobs and all required submodule blobs directly against raw Git bytes and modes, with each index matching its tree. Pins: processor `ead8036035affd53ef4b29979190f2f4f67084c0`, time processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, AXIS `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. Status is clean. The unused external gitlink is unchanged and uninitialized. Only `MANIFEST.sha256` entries and this report are publication inputs; scratch is excluded.

R475-2 FINISHED
