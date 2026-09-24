[A270]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Decisions this change rests on](#decisions-this-change-rests-on)** -- The readings a reviewer should confirm, and the one decision still open.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.
- **[History of this lane](#history-of-this-lane)** -- The rounds and merges that produced the head.

## Status

GREEN locally, with one published decision point -- `387-media-rebase` -> `dev`, head `a21cd3585abdd3cdf4ac5774a048361a66fed043`, which carries dev `57456af9` through the merge `e68c1b1a`.

- The `milan_dp` default `run` sweep: all 47 recipe commands exit 0, 9781 checks, 0 failures (run at `c14f96ed5`; the head adds only one README timing line). Its last runner prints `4 checks: 4 PASS, 0 FAIL`.
- The gmstep leg passes 48/48. `make gmstep-mutants` catches all eleven controls: `13 checks: 13 PASS, 0 FAIL`.
- `tkdiag` passes 96/96, and its mutation arm catches four engine mutants: `5 checks: 5 PASS, 0 FAIL`.
- The full builder passes in both modes, with the pinned RV32 SDK (224/224 mutations rejected) and without a compiler (189/189 applicable). Gate 11's hardware-report calibration is not run in either mode.
- The docs gates pass in both CI modes, and so do the static gates, `behave` (344 scenarios) and a Yosys `milan_datapath` elaborate smoke.
- Open: R277-3's property probe P1 is not clean at this head. It flags requests that land between a PDU's launch and its report. See decision 1.

## Linked Issue / roles

Relates to #387: this is the datapath half of acceptance 3. Acceptance 4, the two-board grandmaster-handover measurement, remains open on the issue.

Acceptance 4 (the booted-board handover measurement) stays the manager's #117 bench step after merge, as assigned.

Executor: `[A270]` for round 2 (earlier rounds `[A256]`, `[A268]`, `[A269]`)
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Description

Issue #387 acceptance 3, the datapath half ([assignment](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5814963103)). It starts from the proposed datapath patch of the #540 round. It adds the pending-restart merge of [ruling 5802264260](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5802264260) item 2, with the boundary set by [ruling 5818091077](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5818091077): pending ends on the wire.

| Piece | Change |
|---|---|
| `hdl/milan/milan_datapath.sv` | `media_rebase_p_w` is the PHC step: the plane's step pulse, a CLKV adjtime when the plane is off, or a software settime. It joins `mcr_restart_p_w` ungated by the clock source, so every step toggles `mr` once (IEEE 1722-2016 4.4.4.3) and Milan Table 5.4 MEDIA_RESET counts it. The render stage re-centres on it and on a settled source change only. The grandmaster identity is no longer a trigger, so a change that steps counts one re-base, not two |
| `hdl/ieee1722/avtp/KL_media_clock_restart.sv` | A request sets each stream's target to the complement of the level it stamps (`tgt_r <= ~mr_o`, `:230`), so a request landing on a restart that waits for its hold merges. Round 2 adds the wire boundary (`:236-238`): a streaming talker that has adopted a level no reported PDU has carried yet (`hold_r == 0`) keeps that level as its target, so a request then merges too. A request after the first PDU at the adopted level is a new restart. The target is per stream. Before #387, every request flipped one shared target, and a second request inside a hold flipped it back, so neither restart reached the wire |
| `hdl/ieee1722/aaf/KL_render_setpoint.sv` | The banner (`:81-89`) and the `recentre_p_i` port spec (`:169-173`) name the #387 trigger set: a PHC step and a settled clock-source change. A grandmaster identity change is no trigger of its own. Comment only |
| `tb/verilator/tkdiag` | T17 now lands the step in both parts of the pending window: talker 1 waits for its hold, and talker 0 has adopted the disruption without a PDU at that level. Each stream shows one toggle and one MEDIA_RESET. The new T18 (6 checks) grades the other side of the boundary. Once talker 0's first PDU at the adopted level has gone out, the step is its second toggle, counted twice, while talker 1 still merges. `mcr_mutants.py` plants four engine defects: the flip-per-request rule, a shared target that merges while any stream is pending, a window that ends at the adoption (the `a9636e0f` engine), and a window that stays open for the whole hold |
| `tb/verilator/milan_dp` | `run` builds and runs the gmstep leg (48/48), then `gmstep_mutants.py` with the three controls the acceptance names. `sim_main.cpp` (the option-off leg: `obj_dir`, `obj_nolpf`, `obj_ax1x1`) grades the software settime it issues: one more `mr` toggle, and MEDIA_RESET counting it once (`:1028-1072`). `gmstep_mutants.py` gains an option-off leg (`make option-off-build`, `OPTOFF_MDIR`) for two controls. Both runners rebuild a stale clean binary instead of grading it |
| `sw/builder/test_builder.py`, `docs/integration/BAREMETAL_FIRMWARE.md` | `[A269]`: builder gate 1b pins the decided PHC consumers, `media_rebase_p_w` and its render and restart readers, with seven new refusal entries |
| Docs | `GM_LOSS_RECOVERY.md`: the pending row states the wire boundary, and the `mr` and MEDIA_RESET rows cite the INTERNAL-source option-off evidence. `TIME_SYNC.md` has the render recentre row, `REGISTER_MAP.md` what the CRF selection gates, and `TESTING.md` the tkdiag and `gmstep-mutants` rows. `CI_WORKFLOWS.md` records the measured `milan_dp` window. The suite README and `CHANGELOG.md` are updated too |

Negative controls, each failing its named check by the harness's own verdict:

| Control | Named check it fails | Runs in |
|---|---|---|
| the step does not toggle `mr` | restart: the outgoing mr toggles exactly once | the sweep |
| the identity re-bases as well as the step (double re-base) | render: the GM change is one counted re-base event | the sweep |
| the step does not re-centre the render stage (ruling item 1) | render: the GM change is one counted re-base event | the sweep |
| a request cancels a pending restart | T17 talker 1 puts exactly ONE toggle on the wire, never none | `tkdiag` default |
| a shared target merging whenever any stream is pending | T18 talker 0 had put the disruption on the wire: the step is its 2nd toggle | `tkdiag` default |
| the pending window ends at the adoption, not at the first PDU | T17 talker 0 sent no PDU at the adopted level: the step merges, ONE toggle | `tkdiag` default |
| the pending window stays open for the whole hold | T18 talker 0 had put the disruption on the wire: the step is its 2nd toggle | `tkdiag` default |
| a software settime does not toggle `mr` (`settime_no_mr`) | CLKV: the settime toggled mr once more (#387) | `gmstep-mutants`, option-off leg |
| the step's `mr` toggle gated by the CRF clock-source selection | CLKV: its mr toggled once per PHC step issued so far (#387) | `gmstep-mutants`, option-off leg |

`make gmstep-mutants` adds six more gmstep controls. They are the render re-base keyed to the identity, `tu` four cycles late, the holdover not re-armed, `tu` stopping the talker, the talker stopped for good, and a re-centre snapped one event off.

**Tests note (existing checks changed).**

- `sim_main.cpp` "CLKV: ownerless frame keeps tv=1" compared the whole AVTP header byte to `0x81`, so it also asserted `mr = 0`. The leg issues one CLKV adjtime earlier. Under the decision that is a PHC step, and the byte reads `0x89`. The check now grades every bit of that byte except `mr`, and a new check grades `mr` against the parity of the PHC steps the harness itself commanded.
- Round 2 adds two checks after the leg's software settime, and a 4096-cycle settle before and after it so each MEDIA_RESET interval has closed. `obj_dir` and `obj_nolpf` are now 233 checks, and `obj_ax1x1` 230.
- `tkdiag` T12 and T15: talker 1 now sends one PDU at its adopted level before the second request. With none, that request would merge under the wire boundary (T17), and the per-stream hold those checks name would go ungraded. The expected values are unchanged; the check labels say "sent one PDU".

## Decisions this change rests on

1. **Pending ends on the wire** ([ruling 5818091077](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5818091077), reading (b) of R276-4 F2 and R277-3 F3). A request is pending on a stream while it waits for the hold of the stream's previous toggle. It stays pending after the stream adopts the new level, until the stream's first PDU at that level. A second request anywhere in that window merges: one toggle, one MEDIA_RESET. A request after that first PDU is a new restart, sent once the earlier toggle has held eight PDUs.
   - **Where the engine measures "on the wire".** `KL_media_clock_restart` sees a PDU only on its transmitted-PDU feed (`frame_p_i`, `frame_mr_i`). That is the same feed the eight-PDU hold counts and MEDIA_RESET reads, so the hold, the count and the merge share one definition of a PDU on the wire. The window closes when that feed reports the first PDU at the adopted level.
   - **The residue.** A talker latches `mr` when it launches a PDU (`KL_aaf_packetizer.sv:616`, `KL_crf_tx.sv:502`). The feed reports the PDU once it has been sent on (`KL_aaf_packetizer.sv:695-698`, `KL_crf_tx.sv:518-523`). So a request between the launch of that first PDU and its report still merges, although the PDU already carries the toggle. The banner states this.
   - **Decision requested: the probe conflict.** R277-3's property probe models that report 3 cycles after the launch and grades P1 at the launch. Run unchanged at this head, D3/D4 give one toggle, and P2, P3 and P4 are clean over seeds 1-6. P1 records 10 requests over seeds 2, 3, 5 and 6 (0 on seeds 1 and 4). A print-only copy of the probe places every one 0-3 cycles after the first launch at the adopted level, inside that latency. No engine with the existing ports can satisfy both D3/D4 = 1 and P1 in that model. At the moment such a request lands, the engine's inputs are the same as in D3.
   - **Two ways to close it.** (a) Rule that the feed report is the engine's "launched", and grade P1 against the report. (b) Add a launch strobe from `KL_aaf_packetizer` and `KL_crf_tx` into the engine: new ports, and the probe would have to drive them. This change implements (a) and keeps the ports.
2. **The restart target is per stream.** Whether a request is pending depends on one stream: its hold, and whether its adopted level has gone out. The CRF output's eight PDUs at 500/s outlast an AAF talker's at 8000/s, and one shared target cannot merge on the first and restart on the second. So two streams can end on opposite `mr` levels. The old "two outputs never on opposite levels" note is removed. 10.4.3 makes only the mr of the stream a Listener recovers its clock from valid.
3. **The step's toggle is not gated by clock-source selection.** Decision part b and the 2026-09-23 decision say "every step is one counted event". The CRF disruption and echo stay gated. The option-off leg grades this on an INTERNAL media clock, and a control that gates the step by CRF selection fails it.
4. **A step** is the set that already raised `tu` and re-centred the render stage: the plane's step (a CLKV adjtime with the plane off) and a software settime. Both are graded: the adjtime by the existing parity check, and the settime by the round-2 checks and their `settime_no_mr` control.
5. **`KL_i2s_playback`** (the Arty I2S element) still re-centres on the grandmaster identity: the decision names the render stage and the aligner only. On the AX7101 shape the identity detector now has no reader.
6. **The merge arms live in `tkdiag`** (T17, T18). The gmstep leg keeps the 48 checks the acceptance names, and its scenario has no restart pending at the step.
7. **The two option-off controls run in the explicit `gmstep-mutants` campaign, not the sweep.** Each costs one datapath elaboration, and the `milan_dp` margin is the one in Known limitations. The two checks they prove run in the sweep's three `sim_main` legs.

## Authoritative references

- Issue #387: decision 5606198212 part b, owner decision 5794731090, rulings 5802264260 items 1 and 2, ruling 5818091077 (the wire boundary), aligner decision 5810378282 (unchanged).
- IEEE 1722-2016 4.4.4.3 (mr, the eight-AVTPDU hold) and 10.4.3; Milan v1.2 Table 5.4 (MEDIA_RESET); REQ-PTP-08.
- `docs/design/GM_LOSS_RECOVERY.md` "Media re-base on a PHC step"; `docs/design/TIME_SYNC.md` "Step policy"; `docs/testing/CI_WORKFLOWS.md` per-suite budgets.

## How to get into the same state

```sh
git fetch origin 387-media-rebase && git checkout 387-media-rebase
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

## How to validate

```sh
make -C tb/verilator/tkdiag
make -C tb/verilator/milan_dp gmstep
make -C tb/verilator/milan_dp option-off
make -C tb/verilator/milan_dp
make -C tb/verilator/milan_dp gmstep-mutants
syn/yosys/run.sh --mode elaborate --top milan_datapath
python3 sw/builder/test_builder.py
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base 57456af96b3127b9d309a995bbbd35a6113ce52d
python3 scripts/measure_test_evidence.py --check
```

Expected result / pass criteria: every command exits 0.

- `tkdiag` prints `checks: 96   failures: 0` and `5 checks: 5 PASS, 0 FAIL`.
- gmstep prints `== gmstep: checks: 48   failures: 0 ==`, and `option-off` prints `milan_datapath: 233 checks, 0 failures`.
- The sweep's last runner prints `4 checks: 4 PASS, 0 FAIL`, and `gmstep-mutants` prints `13 checks: 13 PASS, 0 FAIL`.
- `test_builder.py` ends `ALL GATES PASS EXCEPT 1 NOT RUN` with an RV32 compiler (gate 11's calibration report), and `EXCEPT 2 NOT RUN` without one.

Measured locally on 2026-09-24 (eight build jobs, a shared host): the sweep's 47 commands took 1339 s. Its three gmstep controls took 133 s, and `make gmstep-mutants` took 405 s.

## Known limitations / out of scope

- **Sweep time, from measurements.** The exact-head hosted run at `a9636e0f` measured the `milan_dp` window at 2264.9 s, 9775 checks. It is shard 4/5, job 107720800104, on the candidate merge `1e3a115` onto dev `57456af9`, timed from its `shard: 4/5` line to `PASS milan_dp`. That leaves 435 s (16%) of the 2700 s budget. The same window on dev `57456af9` was 2133.3 s, and on dev `59b81670` 2099.5 s, so this change's hosted cost is about 130 s on one sample each. Round 2 adds six checks and two 4096-cycle settles to each of three short `sim_main` legs, and no elaboration to the sweep; the local sweep went from 1367 s to 1339 s. The budget basis in `CI_WORKFLOWS.md` (about 1815 s plus 885 s) predates both; the page now records these figures beside it. The deadline is not raised. Whether the three gmstep controls stay in `run` on a 435 s margin is a maintainer decision.
- **The launch-to-report residue** (decision 1). A request between the first PDU's launch and its report on the feed merges. R277-3's P1 flags exactly these.
- No datapath-level leg drives a CRF disruption and a step inside one pending window. The merge is graded on the engine (T17, T18), and the step's wiring into the engine by gmstep and the option-off leg.
- The physical re-base (acceptance 4) is the #117 bench.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (acceptance 4 is the post-merge bench step)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes. The assigned gates pass. The whole `scripts/run_all_suites.sh`, the other Yosys tops and full `milan_datapath` synthesis were not run this round
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains. The residue in decision 1 is documented, and the probe conflict awaits a decision
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

## History of this lane

- `[A256]` (`29036eb4`..`00d388d8`): the datapath edit, the per-stream merge, T17, the gmstep sweep leg and its controls, and the docs.
- `[A268]` (`e68c1b1a`): merges dev `57456af9`, which carries #539 (PR #547). The only conflict was `docs/design/GM_LOSS_RECOVERY.md`. The merge keeps #539's CRF servo and grid-aligner rows, including the #387 part b aligner decision, and this branch's `tu`, render-stage, `mr`, MEDIA_RESET and pending-restart rows.
- `[A269]` (`a9636e0f`): builder gate 1b follows the decided PHC consumers (R276-4 F1 = R277-3 F1).
- `[A270]` (`d5dc47c0`..`a21cd358`), answering R276-4 and R277-3:
  - the wire boundary with T17, T18 and four engine mutants (F2 = F3);
  - the settime check with its `settime_no_mr` control (R277-3 F2);
  - the render-stage spec (R276-4 F3 = R277-3 F4);
  - the measured margin (R276-4 F4, R277-3 S1);
  - the status and INTERNAL-source citations (S1, S2, S3);
  - stale-binary rebuilds in both runners (R276-4 S2 = R277-3 S4).
