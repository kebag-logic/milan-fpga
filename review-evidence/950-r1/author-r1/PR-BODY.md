[A811]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN at `287ca1ee` (9 commits on the flip train's head `15168e14`, PR #945; the firmware final since `c7cfba76`),
`pf-950-954-1` -> `dev-soft-core`, the diff this branch's commits once the train merges:
- the new tests fail on the base at every stream they name, at 8x8/1if and 1x1/1if, and pass;
- the firmware gate's four shards PASS (1,856 invocations; the control campaign 832 of 832, the AECP and SRP
  campaigns, this branch's 13 plants among them, 0 escaped); `fw_coverage.py --check` PASS (40 files); both
  firmware boundary gates PASS;
- the two-placement simulation: 0 findings, every plant refused (32), the maps leg and its plant;
- the release (all-fabric) image byte-identical to the base's;
- `plat_ledger.py` PASS with the 8x8 one-interface entry at 58.5 (below), `test_ctrl_memory.py` PASS;
- the CPU budget measured again in full at both points (every arm and group, 64 parts a point): 0 of 69 statements
  exceeded at either; 1x1/1if's SET_STREAM_INFO record raised by the rule to 255 us; `flip_grade.py --check` PASS at
  both points, every row within its bound;
- the docs workflow's gate steps rc 0 but the three RV32 SDK install-verify steps, which this host's SDK refuses the
  same way on the base (no provenance receipt).

## Linked Issue / roles

Closes #950
Closes #954
Relates to #665
Relates to #947
Relates to #943

Executor: `[A811]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

**#950.** When the platform applies a waiting SET_STREAM_FORMAT, the AECP core did it again without repeating the
command's running check, so a STREAM_INPUT bound, or a STREAM_OUTPUT started, while it waited took the new format
anyway. #947 closed that window for inputs 1 to 7, whose receive-monitor context the platform serializes with the
bind; input 0, the CRF input and every STREAM_OUTPUT kept the unchecked re-run. The core now makes the check again
at the wait's end and refuses with the status the dispatch gives.

**#954.** The split platform's ACMP source port always reported `asking_failed` false, so GET_TX_STATE never carried
REGISTERING_FAILED. It now reports a Listener Asking Failed from SRP's registrar on the source's interface.

| Piece | Change |
|---|---|
| `sw/firmware/ctrl/aecp/aecp_commands.c`, `aecp_again` | The checks a waiting command makes again once the platform applied it: a SET_STREAM_FORMAT's own running check (`running`, brief: a STREAM_INPUT bound, a STREAM_OUTPUT running), so a bind or start that settled during the wait refuses it with its dispatch's status (STREAM_IS_RUNNING; ENTITY_MISBEHAVING when the stream cannot be observed). The waiting command is named by the change it noted: only SET_STREAM_FORMAT notes a format, and nothing notes while one waits (`aecp_rx` refuses every change, and `aecp_poll` returns before the lock expiry while one waits). |
| `sw/firmware/ctrl/aecp/aecp.c`, `aecp_poll` | At the wait's end: taken by every interface, the checks are made again; passed, the change is done again, answered and notified; refused, or not taken in time, it stays undone, answers the check's status (or ENTITY_MISBEHAVING), notifies no one, and the face is given the values in force, as before. |
| `sw/firmware/ctrl/plat/ctrl_plat.c`, `source()` | `asking_failed` while SRP's registrar on the source's interface holds a Listener for its stream that is not Ready or Ready Failed (`listener_present && !registered`), the registration #943's GET_STREAM_INFO reads, whatever the Talker declares, as the release processor's talker answers it (`KL_acmp_talker.sv`, `rf_live_w`). The ACMP core already maps it to REGISTERING_FAILED (Milan v1.2 Table 5.47). |
| `sw/firmware/ctrl/plat/ctrl_plat.c`, wrapped ports | Comments: after an applied wait the core's next change is that change, done again or refused with the values in force. #947's serialization for inputs 1 to 7 is unchanged (ENTITY_MISBEHAVING at `AECP_WAIT_MS` while bound). |
| `sw/firmware/ctrl/test/test_aecp.cpp` | `Core.AWaitingFormatChangeMakesItsRunningCheckAgainOnceApplied`: every STREAM_INPUT and STREAM_OUTPUT of the configuration in force; bound or streaming meanwhile, STREAM_IS_RUNNING, undone, no notification, the face given the values in force; not observable, ENTITY_MISBEHAVING; the other flag alone, SUCCESS (an input judged by its binding, an output by its streaming); the check brief. |
| `sw/firmware/ctrl/test/test_plat_sinks.cpp` | Fixture `Streams` on the platform's composition at 8x8/1if and 1x1/1if: S13 (input 0 and the CRF input bound during the wait: STREAM_IS_RUNNING once acknowledged; unbound, taken), S14 (every STREAM_OUTPUT started during the wait by a bridge's Listener Ready, so SRP declares its Talker and licenses it: STREAM_IS_RUNNING; stopped, taken), T1 (GET_TX_STATE at every output: REGISTERING_FAILED for a Listener Asking Failed on its interface, not for Ready or Ready Failed nor at another output, dropped once the registration goes). |
| `sw/firmware/ctrl/test/aecp_mutants.py`, `sink_mutants.py` | 13 planted defects (below) and 5 existing waiting-command plants re-anchored on the core's new status, the same defects. |
| `sw/firmware/ctrl/aecp/README.md`, `aecp.h`, `plat/README.md`, `test_ctrl_firmware.py` | The waiting contract, the source port's Asking Failed (the stale "reads false" limitation removed), the platsinks arm's tests. |
| `sw/litex/ctrl_memory.py`, `ctrl_memory_ledger.py`, `test_ctrl_memory.py` | The platform's 8x8 one-interface image needs 139,304 B of `rom`, 40 B past the 139,264 B that 58.0 RAMB36 holds (both changes add 96 to 104 B an image, `sram` and `ctrl_plat` unchanged), so its entry is 58.5, refused at 59.0, by the owner's rule of 2026-11-15 (an image past its entry raises it to its measured size at the next half tile, as debt owed to S14). Only the platform image reads it. |
| `tb/verilator/ctrl_service_budget/load_grade.py` | 1x1/1if's AECP record raised by the rule to 255 us, in both columns (below). |
| `docs/design/SPLIT_CONTROL_MEMORY.md`, `tb/verilator/ctrl_split_boot/README.md` | The ledger's tables and the plan at this head; section 13 records the re-measure. |

**The CPU budget.** The change runs only at a waiting command's end, which no group of the harness reaches,
but it moves AECP's code (`aecp_poll` 20 B, `aecp_again` 40 B), and with it every image's placement. Measured again in
full on its images (every arm and group, 64 parts a point, against the base's figures, the train's measurement on
byte-identical images): at 8x8/1if no statement moves past its own; at 1x1/1if one does, the SET_STREAM_INFO record
(23,858 CPU cycles against 23,726 on the base), 255 us by the rule against the 250 stated, so it is raised by the usual
rule in both columns of `load_grade`, as the flip train raised the costs its own placement moved. The paced map edit,
29,993 cycles on the base against the 30,000 its 315 us holds, ranged 29,960 to 30,224 over the eight code shapes
measured; the shape kept, the simplest, is the only one measured that keeps it within, at 29,960. A committed-PC trace
of that record shows the same instructions at the same addresses on the base and on a shape whose hot code does not
move, 231 cycles apart: the fetch L1's state when the record starts follows the cold code's placement. Every row holds:
at 1x1/1if the last queued notice 127.43 of 130 ms, ACMP 29.15 of 30, txL 47.98 of 49, the load 0.512 of 0.70; at
8x8/1if the load 0.744 of 0.75 and THE TRANSMIT 76.81 of 77 ms, unchanged. No bound moves.

## Authoritative references

- IEEE 1722.1-2021 7.4.9 (SET_STREAM_FORMAT: STREAM_IS_RUNNING for a bound or running stream), 8.2 (each sink binds
  independently), 9.3.2.6 (IN_PROGRESS).
- Milan v1.2 5.5.4.3 and Table 5.47 (GET_TX_STATE_RESPONSE: REGISTERING_FAILED), 5.3.7.3 (a Stream Output streams
  while it declares and a Listener Ready or Ready Failed registers).
- IEEE 802.1Q-2018 35.2.2.7.2 and 35.2.2.7.4 (the Listener declarations: 1 Asking Failed, 2 Ready, 3 Ready Failed).
- #947 (inputs 1 to 7's serialization), #943 (the registrar state), #665's rulings (the CPU budget's stated-cost
  rule, `tb/verilator/ctrl_service_budget/README.md`; the 2026-11-20 decision, item 4).

## How to get into the same state

```sh
git fetch origin pf-950-954-1
git checkout pf-950-954-1
git submodule update --init gptp-processor protocol-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
# the repository's pinned toolchain, Verilator 5.050 and the RV32 SDK (sw/firmware/gtest/README.md,
# docs/testing/CI_WORKFLOWS.md); the CPU budget harness's prerequisites (tb/verilator/ctrl_service_budget/README.md)
```

## How to validate

```sh
# the new core test (it fails on the test commit's parent's code: 9ed4fc95 on 15168e14)
python3 sw/firmware/ctrl/test/aecp_arms.py --output "$W/core" --app --interfaces 2 --filter 'Core.AWaitingFormatChange*'
# the platform tests at both shapes: the platsinks arm of the firmware gate (plat_arms.arm_platsinks)
# the firmware gate: every arm and every planted-defect campaign, and coverage
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4   # and 1/4, 2/4, 3/4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
# the two-placement simulation and its plants
make -C tb/verilator/milan_dp twin twin-plants twin-maps twin-maps-plants
# the CPU service-budget harness at 1x1/1if and 8x8/1if: every arm (arm A and each of build.py's VARIANTS) and
# every group, then the AECP records by class and the rows
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir "$B" --record-budget-findings --record-share-findings   # and --variant V for each arm, and --point 8x8-1if
python3 -I tb/verilator/ctrl_service_budget/record_classes.py "$B"/results ...
python3 -I tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -I tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/1if
python3 scripts/docs_check.py
```

Expected result / pass criteria:
- the core test passes at 1x1 with one and two interfaces and fails on `9ed4fc95` (the tests on the base) at
  STREAM_INPUT 0: the status, the undone change, the notice; S13, S14 and T1 pass at 8x8/1if and 1x1/1if and fail
  there at every stream they name;
- the firmware gate's four shards `PASS` (1,856 invocations; 0 escaped; `again-*` and `asking-failed-*` caught on
  their words); `firmware coverage: PASS` (40 files; `aecp.c` and `aecp_commands.c` at 100 % lines and branches);
- the twin: 0 findings, `twin-plants` refuses every plant;
- `plat_ledger: PASS (0 finding(s))` (the 8x8 one-interface image 58.5 RAMB36) and `test_ctrl_memory: 0 failure(s)`;
- the CPU budget harness: 0 refusals and only the seven held-egress rows' misses (tsn-c-stack #26) in each arm that
  runs them, at both points; at 8x8/1if `egress_ledger.py` PASS and the largest legal command's four passes over the
  share as on the base; the statement survey 0 of 69 exceeded at each point; `record_classes.py` `RESULT: PASS` at
  both points; `flip_grade.py --check` `RESULT: PASS` at both points;
- `docs_check: 0 finding(s)`, and every docs workflow gate step rc 0.

## Known limitations / out of scope

- **SET_CONFIGURATION and SET_STREAM_INFO** wait the same way, and their bound and running checks (`any_running`,
  `info.running`) are not made again at the wait's end either. #950's acceptance names SET_STREAM_FORMAT, so this
  branch leaves them; the gap wants an Issue of its own. Inputs 1 to 7 are covered for SET_CONFIGURATION by #947's
  serialization.
- **The CPU budget harness's size fixture** keeps its stub ACMP source port (no destination, no Listener), as before:
  #954's port is the platform's, which no CPU-budget image links.
- **The two-placement simulation's scenario registers no Listener**, so it does not exercise #954; both halves
  answer its GET_TX_STATE alike.
- **One interface.** Every arm the platform has is one interface; a Listener on another interface than the source's
  is held by the core test of #943 at two interfaces, not by T1.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
