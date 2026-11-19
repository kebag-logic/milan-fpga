[A800]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `943-out-status` -> `flip-train-1117`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN at `a16899b1` (15 commits on the flip train's head `0839453f`), `943-out-status` -> `flip-train-1117`.
Round 2 answers the external review R872-1 (F1, F2, R1) and the internal review R871-1 (F1, S1, S2); round 1's
head was `502b041c`.
- the CPU service-budget harness's new `declaring-outputs` arm, whose face reports every STREAM_OUTPUT declaring so
  the AECP bridge completes each whole observation of one, at 1x1/1if and 8x8/1if: 0 refusals, 0 budget misses, every
  pass within the share but the two of `aecp-largest-notice` at 8x8/1if that arm B records there too; every record of
  a whole output observation ran exactly one completion, every other record none; THE RETRY's rounds ran the declared
  Talker's; every GET_STREAM_INFO of an output carried its MAAP address and its Listener's flags. Its three planted
  defects (the completion never run, a brief observation completed, the completion dearer) are each caught at both
  points;
- the AECP records by class `RESULT: PASS` at both points with the arm's legs held, and refused without them;
  `flip_grade.py --check` PASS at both, unchanged; the harness self-test PASS;
- the firmware gate's four shards PASS with the AECP campaign's 17 output plants, two new; coverage PASS;
- carried from round 1, the firmware unchanged since (`git diff 502b041c..a16899b1 -- sw/firmware` touches only
  `test_aecp.cpp` and `aecp_output_mutants.py`): the two-placement simulation (0 findings, 32 refusals), the platform
  ledger and memory test, the release image byte-identical, arm A over every group, the answering-ports,
  answering-every-port and talker-notices arms;
- the docs workflow's gate steps rc 0.
- One gate refuses, as it does on the train's head: `firmware-boundary` (see Known limitations).

This PR joins the flip train as step 13 under the owner's 2026-11-19 decision (#665, issuecomment-7007273447, item
1). Its commits sit on the train's head `0839453f` (PR #945); if the train merges first, its base becomes
`dev-soft-core` and the diff is this branch's commits only. Firmware, tests and the harness only, and round 2
changes no firmware source: no RTL, no mailbox-contract change, no change to the face block, no CPU-budget bound
changed.

Author packets: [`review-evidence/943-r1/author-r1`](https://github.com/kebag-logic/milan-fpga/tree/943-review-evidence/review-evidence/943-r1) on branch `943-review-evidence` (archive `2c500f73`), and round 2's beside it.

## Linked Issue / roles

Closes #943
Relates to #665

Executor: `[A800]`
Internal cleared-context reviewer: `[R871]`
External reviewer: `[R872]`

## Description

On the split image a declaring STREAM_OUTPUT's GET_STREAM_INFO, solicited or notified, carried `stream_dest_mac` 0
with STREAM_DEST_MAC_VALID set, and never set REGISTERING (`flags_ex`) or REGISTERING_FAILED (`flags`
`0x00000040`). The split datapath's GSI face answers an output's destination from the fabric MAAP engine, which the
split does not build, and ties the Listener registration to 0. The firmware holds both: the MAAP owner's range
through ACMP's source port, and each Listener registration in SRP's registrar copy.

| Piece | Change |
|---|---|
| `sw/firmware/ctrl/app/ctrl_app_aecp.c`, `stream()` and `output()` | For a whole observation of a STREAM_OUTPUT the face reports declaring (its STREAM_DEST_MAC_VALID), the bridge completes the face's answer: `stream_dest_mac` is ACMP's source port's address, the value PROBE_TX_RESPONSE carries (0 while MAAP holds no range); from SRP's registrar copy on the output's own interface (ACMP's `source_interface`), for its stream_id, REGISTERING while a matching Listener is registered, of any declaration, and REGISTERING_FAILED while that Listener is Asking Failed. Undeclared, the face's answer stands, and it is the fabric's: `stream_dest_mac` 0 and neither flag. A brief observation, a running check's, stays the face's (bound and running alone). An output ACMP holds no source for is not answered. |
| `sw/firmware/ctrl/aecp/aecp_commands.c`, `aecp_internal.h`, `aecp_maps.c` | `aecp_stream_read` keeps the caller's `brief`; an output map edit's check of its stream (`idle`) is a running check, so it observes briefly, as SET_CONFIGURATION's and SET_STREAM_FORMAT's do. GET and SET_STREAM_INFO still read whole. The reason is the CPU budget (below). |
| `sw/firmware/ctrl/test/test_aecp.cpp` | `AppOutputs.OutputInfoCarriesItsTalkersAddressAndItsListenersRegistration`: every STREAM_OUTPUT, each on its own interface (n % MBX_N_IF), real MSRP Listener MRPDUs through the SRP channel, GET_STREAM_INFO read on the wire: Ready, Ready Failed and Asking Failed in turn, each pinning the whole flags word (the face's, and REGISTERING_FAILED for Asking Failed alone, never MSRP_FAILURE_VALID), at two interfaces its stream's Listener on the other interface first, showing neither flag, the Talker withdrawn and declared again, the Listener's Lv, every other output read while it declares and showing none of it, MAAP holding no range, no SRP, a source past SRP's shape, an output ACMP holds no source for, and a brief observation. `Core.TheRunningCheckObservesEveryStreamBriefly` holds an output map edit's check brief. A `connecting()` hook in the `App` fixture sets the streams before the composition. |
| `sw/firmware/ctrl/test/aecp_arms.py` | The test also runs at the 8x8 shape at one interface (`OUTPUTS`), beside the shipping 1x1 shape's App arm at one and two interfaces. |
| `sw/firmware/ctrl/test/aecp_output_mutants.py`, `aecp_mutants.py`, `aecp_configuration_mutants.py` | 17 planted defects, each caught by its named words in the AECP campaign's arm (1x1, two interfaces): round 2 adds `output-registering-failed-msrp-failure-valid` (the STREAM_INPUT's failure constant, `0x08000040`, copied) and `output-listener-any-interface` (either interface's registrar copy), and names `output-listener-on-interface-zero` and `output-listener-of-output-zero` by the checks that now catch them; `stream-read-brief` re-anchored on `aecp_stream_read`'s new lines, the same defect. |
| `tb/verilator/milan_dp/twin_compare.py`, `twin_plants.py`, `Makefile`, `README.md` | The owed row `stream-output-0-dest-mac` is deleted: both halves now send the same four STREAM_OUTPUT 0 notices, `91e0f0000100` in the declared ones. `vanished-owed` gives way to `output-dest-mac-zero` (this defect back); `output-notice-dropped` is refused by the notice comparison's own words. |
| `tb/verilator/ctrl_service_budget/declaring_outputs.py`, `build.py`, `run.py` | The `declaring-outputs` arm: answering-ports' fixture with valid-destinations' ACMP source port and a stream observation that answers as the face block's does for a declaring STREAM_OUTPUT (word 0's flags, STREAM_DEST_MAC_VALID among them, in a brief observation as in a whole one, the caller's brief kept); the bridge's ACMP owner enters the source port through `completion_source`, whose entry the testbench reports, so each entry inside an AECP record or a round is one completion. It runs arm B's AECP groups as answering-ports builds them, and `aecp-outputs`: a declared Talker's completed notice to every registration, a Listener Ready for output 0, GET_STREAM_INFO of every output, SET_STREAM_INFO refused NOT_SUPPORTED and ENTITY_LOCKED after its whole observation, and, behind a held egress, an accepted SET_STREAM_INFO whose notices pass the AECP ring's room and a GET_STREAM_INFO behind them. The run fails on `declaring_outputs.findings` (a whole observation's record with no completion, any other record with one, no round with one, an answer without the completion's values). Three plants: `completion-unexecuted`, `brief-completed`, `completion-dearer`. |
| `tb/verilator/ctrl_service_budget/record_classes.py` | Each record counts its completions; the declaring arm's records that ran one are held at their class's statement, the rest reported; a pass is refused at 1x1/1if and 8x8/1if without a declaring leg that ran an answered GET_STREAM_INFO, an accepted SET_STREAM_INFO and a refused one, each with its completion. Six new self-test controls, and the arm's own checks (`declaring_outputs.checks`, a fixture that clears brief among them). |
| `tb/verilator/ctrl_service_budget/rows_tiers.py` | 8x8/1if's largest legal command's record restated by the rule at this image, 1,715 to 1,720 us. |
| `sw/firmware/ctrl/aecp/README.md`, `docs/design/SPLIT_CONTROL_MEMORY.md`, `docs/DOCUMENTATION_AUDIT.md`, `tb/verilator/ctrl_service_budget/README.md` | The bridge's output answer and the brief map check; the restated record and the declaring arm's records; the regenerated inventory; the arm, its checks and its plants. |

**REGISTERING under Asking Failed.** Milan v1.2 Table 5.8 (and 5.12) defines REGISTERING for a Stream Output as
declaring a Talker attribute and registering a matching Listener attribute: Listener Ready, Listener Ready Failed or
Listener Asking Failed. So under Asking Failed both REGISTERING and REGISTERING_FAILED are set, as the release
fabric's flag law sets them (`milan_datapath.sv`, `gsi_flag_law`). #665's ruling names Ready and Ready Failed for
REGISTERING and cites Table 5.8; the branch follows the table, said so in the takeover comment, and the test asserts it.

**The CPU budget.** The answering-ports arm's AECP groups were measured on the base and on each image the branch went
through (same harness, same groups). The 1x1/1if paced one-row edit (a REMOVE of one output row) is stated 310 us and
measures 29,331 cycles on the base. With the completion run inside the edit's whole-read check, and the code moves
that came with it, it measured 30,744 to 31,749 cycles (325 to 335 us by the rule). Restated to 325 us, 1x1/1if's
last queued notice row is 141.54 ms against its 140 ms bound, so the rule could not be applied there. In the final
shape the edit's check is brief and the completion runs on no running check: 29,422 cycles, 310 us, within its
statement. At 8x8/1if the largest legal command's record (63 output rows) is 152,504 cycles on the base and 163,520
here, 1,720 us by the rule, 5 us over its 1,715 statement, which is restated (`rows_tiers.LONG_RECORD_US`). 8x8/1if's
rows by every source are reported, not held, and `flip_grade.py --check` passes at both points with it: 1x1/1if's
rows unchanged, 8x8/1if's load 0.744 of 0.75 and THE TRANSMIT's row 76.81 of 77 ms, unchanged.

**A declaring output's completion, graded (round 2).** The `declaring-outputs` arm runs the completion on every path
a whole observation of an output takes, and counts it: at 1x1/1if (two outputs) 6 completions in 6 records of
`aecp-outputs` and 1 in a round of THE RETRY, at 8x8/1if (nine outputs, the CRF output among them) 13 and 1, each
record of a whole observation exactly one, every other record of the arm none (the map edits', the largest legal
command's and the running checks' observations are brief). The records that ran one are held by class: at 1x1/1if
the dearest is an accepted SET_STREAM_INFO's, 23,330 cycles, 245 of `record.aecp`'s 245 us (arm B's, which runs no
completion, 21,409); at 8x8/1if 20,707, 220 of 265. Its rows all fit their 20 ms: the declared Talker's completed
notice to every registration 1.337 and 1.615 ms, GET_STREAM_INFO 0.215 to 0.264 and 0.135 to 0.182 ms, the refusals
0.240 to 0.268 and 0.183 to 0.194 ms, and behind the held egress the SET's last notice 9.104 and 9.138 ms and the GET
4.068 and 4.103 ms. Every round is within its stated costs (`round_grade.py`) and the rows by every source charge
AECP's records at the statements those records keep, so `flip_grade.py --check` is unchanged.

## Authoritative references

- Milan v1.2 5.4.2.10 and 5.4.2.10.2, Table 5.8 (flags_ex), Table 5.11 (Stream Output flags: REGISTERING_FAILED,
  STREAM_DEST_MAC_VALID), Table 5.12 (Stream Output flags_ex: REGISTERING): "the stream_id, stream_dest_mac and
  stream_vlan_id fields shall be set to the corresponding values of the declared Talker attribute".
- IEEE 1722.1-2021 7.4.16 (GET_STREAM_INFO).
- IEEE 802.1Q-2018 35.2.2.7.2 and 35.2.2.7.4 (the Listener declaration types: 1 Asking Failed, 2 Ready, 3 Ready Failed).
- Milan v1.2 5.5.4.1 (PROBE_TX_RESPONSE's stream_dest_mac, the source's MAAP address).
- #665's ruling of 2026-11-19 (issuecomment-7007273447, item 1); #943.
- `docs/design/SPLIT_CONTROL_MEMORY.md` (the queued notices at stated costs, the AECP records by class) and
  `tb/verilator/ctrl_service_budget/README.md` (the stated-cost rule: the most measured plus 5 %, rounded up to 5 us).

## How to get into the same state

```sh
git fetch origin 943-out-status
git checkout 943-out-status
git submodule update --init gptp-processor protocol-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
# the repository's pinned toolchain, Verilator 5.050 and the RV32 SDK (sw/firmware/gtest/README.md,
# docs/testing/CI_WORKFLOWS.md); the CPU budget harness's prerequisites (tb/verilator/ctrl_service_budget/README.md)
```

## How to validate

```sh
# the new test at every output of both shapes (it fails on the parent of the fix commit, b605d1fa)
python3 sw/firmware/ctrl/test/aecp_arms.py --output "$W/a" --app --interfaces 1 --filter 'AppOutputs.*'
python3 sw/firmware/ctrl/test/aecp_arms.py --output "$W/b" --app --interfaces 2 --filter 'AppOutputs.*'
python3 sw/firmware/ctrl/test/aecp_arms.py --output "$W/c" --app --interfaces 1 --config configs/endstation_ax7101_8x8.yaml --filter 'AppOutputs.*'
# the firmware gate: every arm and every planted-defect campaign (the 15 output plants among them), and coverage
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4   # and 1/4, 2/4, 3/4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
# the two-placement simulation and its plants
make -C tb/verilator/milan_dp twin twin-plants
# the platform image at every ledger point, and the memory test
python3 tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir "$W/ledger"
python3 sw/litex/test_ctrl_memory.py
# the CPU service-budget harness at 1x1/1if and 8x8/1if, then the AECP records by class over arm A, arm B and the
# declaring arm (and answering-every-port's legs)
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir "$B1" --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir "$B8" --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --variant answering-ports --groups aecp,aecp-fanout,aecp-largest-notice,aecp-reboot --build-dir "$B1P" --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --variant answering-ports --groups aecp,aecp-fanout,aecp-largest-notice,aecp-reboot --build-dir "$B8P" --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --variant declaring-outputs --build-dir "$B1D" --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --variant declaring-outputs --build-dir "$B8D" --record-share-findings
for m in completion-unexecuted brief-completed completion-dearer; do
  python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --variant declaring-outputs --mutation $m --build-dir "$W/$m-1x1"
  python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --variant declaring-outputs --mutation $m --build-dir "$W/$m-8x8"
done
python3 -I tb/verilator/ctrl_service_budget/record_classes.py "$B1/results" "$B1P/results" "$B1D/results" "$B8/results" "$B8P/results" "$B8D/results"
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -I tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -I tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/1if
python3 scripts/docs_check.py
```

Expected result / pass criteria: 
- `AppOutputs` passes at 1x1 one and two interfaces and at 8x8 one interface, and fails on `36f89b45` (the test
  alone) at every output: the destination MAC, REGISTERING and REGISTERING_FAILED. Each of the 17 output plants,
  planted alone, fails it on its named words at 1x1 two interfaces, the campaign's arm (at one interface
  `output-listener-on-interface-zero` and `output-listener-any-interface` are the same code as the fix).
- the firmware gate's four shards `PASS` (the control campaign 825 of 825, the AECP campaign's 383 defects, the 17
  output plants among them, and the SRP campaigns all caught, 0 escaped); `firmware coverage: PASS`
  (40 files; `ctrl_app_aecp.c`, `aecp_commands.c` and `aecp_maps.c` at 100 % lines and branches);
- the twin: 0 findings, and `twin-plants` refuses every plant (32 refusals, 0 escapes);
- `plat_ledger: PASS (0 finding(s))` (rom +280 B at every point, the RAMB36 counts unchanged: 45, 46, 58, 63) and
  `test_ctrl_memory: 0 failure(s)`;
- the CPU budget harness: no refusal and no budget miss in the answering-ports, answering-every-port,
  talker-notices and declaring-outputs arms at either point (the declaring arm exits 0, no `DECLARING` finding);
  arm A as in Status; each declaring plant prints `CONTROL <name> caught`; `record_classes.py` within every statement
  it holds (the paced edit 310 of 310 us and the declaring SET_STREAM_INFO 245 of 245 us at 1x1/1if; the largest
  legal command 1,720 of 1,720 us at 8x8/1if), and `RESULT: FAIL` with the declaring legs left out;
  `flip_grade.py --check` `RESULT: PASS` at both points; the harness self-test `self-test: 0 failures`;
- `docs_check: 0 finding(s)`, and every docs workflow gate step rc 0.

## Known limitations / out of scope

- **A Listener registration change of a STREAM_OUTPUT raises no GET_STREAM_INFO notice** on the split (Milan v1.2
  Table 5.22, "MSRP Listener attribute registration state (Stream Output only)"), where the release processor sends
  one. REGISTERING and REGISTERING_FAILED are right in every response and in every notice the split sends (a Talker
  declared, withdrawn or swapped, #936); a controller sees a Listener's change at its next read. As #943 records it.
- **The output's declaring bit is the face's, the DA gate,** not SRP's TALKER_DECL; the completion and both flags
  follow it, as the release fabric's flag law follows its own declaring bit. As #943 records it.
- **MSRP_FAILURE_VALID, the failure code and the failure bridge ID** of a Talker Failed are still never set for an
  output on the split. As #943 records it.
- **Round 1's declaring-face figures are withdrawn** (R872-1-F2). Its measurement-only fixture cleared the caller's
  `brief` (`memset`, then STREAM_DEST_MAC_VALID set), so every brief check of an output ran the completion too: the
  round-1 claim that the paced edit's 325 us and the largest legal command's 1,920 us on that image were placement
  alone was wrong, and its excess is not apportioned between placement and execution. The maintained arm keeps
  brief: a probe of its observation under the bridge returns brief=1 with 0 source calls for a brief read, and 1 call
  with the source's address for a whole one, and on its image every record of the map edits and of the largest legal
  command counts 0 completions.
- **The AECP class statements stand close to code placement** (R871-S1's second half, the owner's). On the declaring
  arm's image the records that run no completion are arm B's commands on another placement and are reported, not
  held: the paced one-row REMOVE 30,226 cycles, 320 us by the rule, at 1x1/1if (arm B 29,422, 310 of 310), and the
  largest legal command's record 167,522 cycles, 1,760 us, at 8x8/1if (arm B 163,520, 1,720 of 1,720). The held
  declaring SET_STREAM_INFO is 3 cycles inside 1x1/1if's 245 us. Restating the paced edit to 320 us would put 1x1/1if's
  last queued notice row over its 140 ms (325 us gives 141.54 ms), so a merged image whose placement moves these
  records can refuse where this head passes.
- **Seen beside it, not changed:** the split's ACMP GET_TX_STATE never sets REGISTERING_FAILED (Milan v1.2 Table
  5.47): the platform's ACMP source port reports `asking_failed` false always (`plat/ctrl_plat.c`, `source`). It is
  ACMP's, not GET_STREAM_INFO's; a new issue, the manager's to file.
- **The firmware-boundary gate refuses two files this branch does not touch**, on the train's head as here:
  `sw/firmware/ctrl/test/sink_mutants.py` (#946) and `tb/verilator/ctrl_service_budget/talker_notice.py` (#936)
  name the firmware's tree and are classified nowhere in `ctrl_configs.py` (BUILDERS, OUTSIDE or SUITES).
  `ctrl_boundary.py --require-rv32 --selftest --without verilator` refuses the same two at `0839453f`, and the
  Verilator half passes. Classifying them is outside #943; this PR's `firmware-boundary` job will refuse them until
  the train or a follow-up does.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
