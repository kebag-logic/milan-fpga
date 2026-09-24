[A256]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Decisions this change rests on](#decisions-this-change-rests-on)** -- The readings a reviewer should confirm.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

GREEN locally -- `387-media-rebase` -> `dev`, head `00d388d8`, base dev `59b81670`. The `milan_dp` sweep runs all 47 recipe commands with exit 0 (9775 checks, 0 failures); the gmstep leg passes 48/48 at every feed delay 0 to 41; `tkdiag` 90/90 with its mutation arm; Yosys `milan_datapath` full synthesis PASS. Four one-line commits.

## Linked Issue / roles

Relates to #387: this is the datapath half of acceptance 3. Acceptance 4, the two-board grandmaster-handover measurement, remains open on the issue.

Acceptance 4 (the booted-board handover measurement) stays the manager's #117 bench step after merge, as assigned.

Executor: `[A256]`
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Description

Issue #387 acceptance 3, the datapath half ([assignment](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5814963103)), starting from the proposed datapath patch of the #540 round, plus the pending-restart merge of [ruling 5802264260](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5802264260) item 2.

| Piece | Change |
|---|---|
| `hdl/milan/milan_datapath.sv` | `media_rebase_p_w` = the PHC step (the plane's step pulse, CLKV adjtime when the plane is off, a software settime). It joins `mcr_restart_p_w` ungated by the clock source, so every step toggles `mr` once (IEEE 1722-2016 4.4.4.3) and Milan Table 5.4 MEDIA_RESET counts it. The render stage re-centres on it and on a settled source change only: the grandmaster identity is no longer a trigger, so a change that steps counts one re-base, not two |
| `hdl/ieee1722/avtp/KL_media_clock_restart.sv` | A request sets each stream's target to the complement of the level it stamps (`tgt_r <= ~mr_o`), so a request landing on a pending one merges: exactly one toggle, never a cancellation. The target is per stream. Before, every request flipped one shared target, and a second request inside a hold flipped it back, so neither restart reached the wire |
| `tb/verilator/tkdiag` | T17 (7 checks) grades the merge on the engine and the MEDIA_RESET counter, PDU by PDU. `make` now also runs `mcr_mutants.py`: the dev engine's flip-per-request rule and a shared target that merges whenever any stream is pending must each fail a named T17 check. The dev engine fails exactly T17's two merge checks |
| `tb/verilator/milan_dp` | `run` builds and runs the gmstep leg (48/48) and then `gmstep_mutants.py`, the three controls the acceptance names; `make gmstep-mutants` runs all nine. `sim_nxn.cpp`'s q2 injection flips every context's target. `sim_main.cpp`: see the Tests note below |
| Docs | `GM_LOSS_RECOVERY.md` "Not yet" rows -> "Yes" with evidence; `TIME_SYNC.md` render recentre row; `REGISTER_MAP.md` (what the CRF selection gates); `TESTING.md`; the suite README; `CHANGELOG.md` |

Negative controls, each failing its named check by the harness's own verdict:

| Control | Named check it fails |
|---|---|
| the step does not toggle `mr` | restart: the outgoing mr toggles exactly once |
| the identity re-bases as well as the step (double re-base) | render: the GM change is one counted re-base event |
| the step does not re-centre the render stage (ruling item 1) | render: the GM change is one counted re-base event |
| a request cancels a pending restart | T17 talker 1 puts exactly ONE toggle on the wire, never none |
| a shared target merging whenever any stream is pending | T17 talker 0 had stamped the disruption: the step is its 2nd toggle |

The first three run in the default sweep, the last two in `tkdiag`'s default target. `make gmstep-mutants` adds six more: the render re-base keyed to the identity, `tu` four cycles late, the holdover not re-armed, `tu` stopping the talker, the talker stopped for good, and a re-centre snapped one event off.

**Tests note (existing check changed).** `sim_main.cpp` "CLKV: ownerless frame keeps tv=1" compared the whole AVTP header byte to `0x81`, so it also asserted `mr = 0`. The leg issues one CLKV adjtime earlier; under the decision that is a PHC step, and the byte reads `0x89`. The check now grades every bit of that byte except `mr`, and a new check grades `mr` against the parity of the PHC steps the harness itself commanded. obj_dir and obj_nolpf go 230 -> 231 checks, obj_ax1x1 227 -> 228.

## Decisions this change rests on

1. **Pending means requested and not yet stamped.** A request waits while the stream's previous toggle has not held eight PDUs; a second request in that window merges. A request after the stream has stamped the earlier one is a new restart, sent once the earlier toggle has held (as T12 already grades), because that stream's listeners have seen the earlier toggle.
2. **The restart target is per stream.** Whether a request is pending depends on one stream's hold: the CRF output's eight PDUs at 500/s outlast an AAF talker's at 8000/s. One shared target cannot merge on the first and restart on the second. So two streams can end on opposite `mr` levels. The old "two outputs never on opposite levels" note is removed; 10.4.3 makes only the mr of the stream a Listener recovers its clock from valid.
3. **The step's toggle is not gated by clock-source selection**, per decision part b and the 2026-09-23 decision ("every step is one counted event"). The CRF disruption and echo stay gated.
4. **A step** is the set that already raised `tu` and re-centred the render stage: the plane's step (CLKV adjtime with the plane off) and a software settime.
5. **`KL_i2s_playback`** (the Arty I2S element) still re-centres on the grandmaster identity: the decision names the render stage and the aligner only. On the AX7101 shape the identity detector now has no reader.
6. **The merge arm lives in `tkdiag`.** The gmstep leg keeps the 48 checks the acceptance names, and its scenario has no restart pending at the step.

## Authoritative references

- Issue #387: decision 5606198212 part b, owner decision 5794731090, rulings 5802264260 items 1 and 2, aligner decision 5810378282 (unchanged).
- IEEE 1722-2016 4.4.4.3 (mr, the eight-AVTPDU hold) and 10.4.3; Milan v1.2 Table 5.4 (MEDIA_RESET); REQ-PTP-08.
- `docs/design/GM_LOSS_RECOVERY.md` "Media re-base on a PHC step"; `docs/design/TIME_SYNC.md` "Step policy".

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
make -C tb/verilator/milan_dp
make -C tb/verilator/milan_dp gmstep-mutants
syn/yosys/run.sh --top milan_datapath
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
python3 scripts/measure_test_evidence.py --check
```

Expected result / pass criteria: every command exits 0. `tkdiag` prints `checks: 90   failures: 0` and `3 checks: 3 PASS, 0 FAIL`; gmstep prints `== gmstep: checks: 48   failures: 0 ==`; the sweep's last runner prints `4 checks: 4 PASS, 0 FAIL`; `gmstep-mutants` prints `10 checks: 10 PASS, 0 FAIL`.

Measured locally (eight build jobs, a shared host): the change adds about 182 s to the `milan_dp` sweep's 1367 s (gmstep build 12 s, leg 24 s, three controls 147 s). `gmstep-mutants` took 372 s.

## Known limitations / out of scope

- **Sweep time.** At the documented 1.58x hosted slowdown the added 182 s is about 290 s against the #444 hosted worst case of about 1815 s, so roughly 595 s of the 2700 s budget remains instead of 885 s. The deadline is not raised; the other six controls are an explicit target.
- **Lane conflict with PR #547 (#539).** It rewrites the aligner and CRF-servo rows adjacent to the rows turned to "Yes" here, and the README bullet next to the pending-restart one. Whichever lands second resolves a textual conflict; the contents do not overlap. This change leaves those rows and bullets as they are.
- No datapath-level leg drives a CRF disruption and a step inside one hold; the merge is graded on the engine (T17), and the step's wiring into the engine by gmstep.
- The physical re-base (acceptance 4) is the #117 bench.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (acceptance 4 is the post-merge bench step)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes (the assigned gates pass; the whole `scripts/run_all_suites.sh` and the 52 Yosys tops that read no edited file were not run)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

## Dev merge

[A268], `e68c1b1a`, merges dev `57456af9`, which carries #539 (PR #547). The only conflict was `docs/design/GM_LOSS_RECOVERY.md`. The merge keeps #539's CRF servo and grid-aligner rows, including the #387 part b aligner decision, and this branch's `tu`, render-stage, `mr`, MEDIA_RESET and pending-restart rows. The `gmstep`, `tkdiag` and `mmcm_servo` suites and the docs gates pass at the merge.
