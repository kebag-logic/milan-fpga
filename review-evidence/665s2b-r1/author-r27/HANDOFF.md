# [A683zj] #665 lane S2b, round 27 (HANDOFF)

**Status: REVIEW READY** (the lane split, item 4) at `e7e2b7444a9859b058deff0d9edb575f2fb1946f` (`665-s2b-cycles`), two commits on round 26's `0b37f3d2ff320e8d84a235e2568aca0fc31cae81`. No merge, rebase, force or amend; nothing pushed. No firmware, RTL, mailbox contract, donor or submodule change.

- Authority: the round 27 ruling (issuecomment-6788828284), items 1 to 7; #882 and its three acceptance items.
- TAKEN: issuecomment-6788936516 (`TAKEN-COMMENT.md`), 2026-11-11 07:36 CET. REVIEW READY: issuecomment-6798000702 (`REVIEW-READY-COMMENT.md`). Nothing else posted.

| Commit | Subject |
|---|---|
| `e5baac61` | Hold every CPU budget harness row that ends at a response to its own response's command type and status, send GET_AVB_INFO on AVB_INTERFACE 0, and name each refusal row (#882) |
| `e7e2b744` | Hold 1x1/1if's long-window load for merge and 8x8/2if's at the pin in a flip check of its own, which fails at this head, and state the baseline #882's re-measure leaves and the SRP record cut measured on a scratch image in section 13 (#665) |

## Contents

1. Outcome against the ruling
2. Changes (file:line, reason)
3. New checks, planted mutants and failing words
4. Measurement: the baseline, the cut, the load
5. Gates
6. Findings, deviations and open questions
7. The flip-gate issue's text (item 4)
8. Run history

## 1. Outcome against the ruling

| Item | Outcome |
|---|---|
| 1. #882 first | `e5baac61`. The `get_avb_info` row sends GET_AVB_INFO `0x0027` on AVB_INTERFACE 0 with its 7.4.40.1 command (descriptor_type 9, descriptor_index 0: four bytes). Every harness row that ends at a response states its command or message type and its status (`answers.py`); the grader holds the probe's own response, the one answering its sequence_id, to both, and a type or status other than the stated one is an unexpected response that fails the run. A row that states a status other than SUCCESS is a refusal row and is named as one, `<row>, refused <status>`; the run refuses a group with a row that states no response, or a refusal its row does not name. The plant restoring the refused command (GET_AS_PATH on AVB_INTERFACE 9) is caught by the self-test, and in a real run would be refused by status in both arms (arm B: NO_SUCH_DESCRIPTOR against the stated SUCCESS; arm A: against the stated ENTITY_MISBEHAVING). **SUCCESS is asserted in arm B** (`answering-ports`), the harness's arm whose observation ports answer: in arm A the test SoC's idle datapath never answers the face block's window, so GET_AVB_INFO there answers ENTITY_MISBEHAVING once the window read's bound has passed, a named refusal (section 6, deviation D1). The baseline, on unchanged firmware: every leg rebuilt byte-identical to round 26's, the `aecp` group re-simulated at 1x1/1if and 8x8/2if in arm A, in arm B and with tsn-c-stack#32, every other recorded group regraded under the new checks: 0 refusals, the tallies round 26's, **no stated cost moves**, the load unchanged (section 4) |
| 2. One cut | The baseline gap at 8x8/2if is 0.019, under 0.03, so the cut was made: this tree's share of SRP's record (the adapter's StreamID and MAC comparisons with their last byte compared inline, `same` only on a match; a sink's `capture` only where its kind was or is one; `ctrl_mem.c`'s `memcmp` four bytes a turn where the two alignments differ). **Measured on a scratch image, not committed** (deviation D2): the heaviest SRP record 34,361 to 33,741 cycles (the notice arm's `notice-every-3`) and 33,260 to 33,251 (arm A's `backlog-owed`); stated 365 to about 355 us, 8x8/2if about 0.713 graded and 0.809 at the pin, over 0.70 either way; and the cut (+152 B at the pin, +160 B with tsn-c-stack#32) takes arm A's image with tsn-c-stack#32 over the 8x8/2if ROM ledger (122,936 B in 122,880), so the graded column's leg would not build. No firmware change, so no firmware mutant |
| 3. No STOP before the gate pass | The full clean-clone gate pass at `e7e2b744`, once: every gate rc 0 but the flip check, which exits 1 by design (section 5) |
| 4. Outcome | **8x8/2if over, 1x1/1if under: the lane splits.** `load_grade.py --check` holds 1x1/1if for merge (0.450 with tsn-c-stack#32, 0.463 at the pin; rc 0). 8x8/2if moved to `flip_grade.py`, a separately invoked check read at the pin: `--check` exits 1 at this head (`OVER 8x8/2if: the load 0.815 at the pin is over the flip ceiling 0.70`); `--selftest` refuses all six of its controls, the over-ceiling row among them. REVIEW READY; the flip-gate issue's text is section 7 (`FLIP-GATE-ISSUE.md`), for the manager to open |
| 5. Tripwire | Fires: 8x8/2if is over 0.70 at round 27's head. The memo's inputs: the baseline 0.719 graded, 0.815 at the pin; the after-cut figure about 0.713 graded, 0.809 at the pin; the movement between images on the same groups, the heaviest work pass -15,987 to +2,056 cycles (`receipts/cut/heaviest-records.txt`) |
| 6. Donor | tsn-c-stack, lwSRP and every donor clone untouched. The graded column's legs apply round 26's port of tsn-c-stack#32 (`donor-core.patch`, sha256 `8befae7e...`, receipts/baseline/donor-core.patch.sha256) in a scratch clone; their images are byte-identical to round 26's. The flip check reads `load_grade.STATED_US`, the pin's column. tsn-c-stack#34 (tsn-c-stack#32) merged on the stack's `main` at `715589c` at 10:40, during this round, by its own review; this tree's pin is still `70936b77`, and the pin move is its own lane |
| 7. S9 (#870) | Its `KL_mbx` round had not landed by the measurement (08:06 to 09:22): its round 3 posted REVIEW READY at 12:37 at `a91fb27d`, both reviews then NEGATIVE (MINOR only), and its round 4 was taken at 13:47, with nothing in `dev-soft-core`. The grade uses the harness's own access cycles, and the flip-gate issue carries #870's (its acceptance item 3) |

## 2. Changes (file:line, reason)

All in `tb/verilator/ctrl_service_budget/` but the last row.

| Commit | File:line | Change | Reason |
|---|---|---|---|
| `e5baac61` | `answers.py` (new, 119 lines): `aem`/`mvu`/`acmp` :24-37, `refused` :39, `unstated` :49, `answered` :65, `differs` :76, `check` :87, `AVB_INFO` :102, `UNKNOWN` :105, `TALKER` :109, `aecp_statuses` :113 | a row's stated response (command or message type and status), the check of the probe's own response against it, the rows' statuses | #882 acceptance 1 and 2; the ruling's item 1 |
| `e5baac61` | `frames.py:30-38` | `ACMP_STATUS` (IEEE 1722.1-2021 Table 8-3) and `AEM_STATUS` (Table 7-141, Milan v1.2 Table 5.19 for MVU) | the status names a row states |
| `e5baac61` | `grade.py:641-650` (`own_response`), `:652-660` (`expectation`) | the probe's own response found by its `resp:` end's sequence_id, held to the stated type and status; the old `aecp_response` (any AECP response on the interface), `acmp_type` and `acmp_status` (the first frame of a type) kinds removed, so an old-form expectation is refused as unknown | a row's response is its own, never another of the channel's |
| `e5baac61` | `run.py:458-463` (`unstated`), `:470` | a group whose response row states no type and status, or a refusal its row does not name, is a refusal of the run, by name | every row asserts what it measures |
| `e5baac61` | `scenario.py:431-440` (`aecp_groups.cmd`) | each AEM row states its command_type and status, SUCCESS unless `answers.aecp_statuses` states another; the row named for a refusal | #882 |
| `e5baac61` | `scenario.py:458` | `get_avb_info`: GET_AVB_INFO `0x0027` on AVB_INTERFACE 0, four bytes (was GET_AS_PATH `0x0028`, descriptor_index 9, 20 bytes) | #882 acceptance 1 |
| `e5baac61` | `scenario.py:459` | the unknown command `0x3FF0` (was `0x7FF0`) | `aecp.c` keeps 14 bits of command_type and answers `0x7FF0` as `0x3FF0` (finding F1); the firmware's path is the same either way, since it sees `0x3FF0` for both |
| `e5baac61` | `scenario.py:331`, `:337`, `:342`, `:345-347`, `:452`, `:464`, `:562`, `:607`, `:831`, `:840`, `:878`, `:968`, `:976` | every other response row states its response: ACMP's BIND_RX, GET_RX_STATE, UNBIND_RX and the four talker commands (PROBE_TX refused TALKER_DEST_MAC_FAIL, GET_TX_CONNECTION refused NOT_SUPPORTED), READ_DESCRIPTOR, MVU GET_MILAN_INFO, the fan-outs, arm B's cross-channel BIND_RX, the backlog and owed rows, the fixture's two | the structural check found each, `aecp_fanout.bind_rx_stream_info` among them |
| `e5baac61` | `scenario.py:443` | the descriptor rows' table built by one dict comprehension (the loop it replaces kept the last row a type, as this does) | keeps the module at the 1,000-line ratchet |
| `e5baac61` | `selftest_answers.py` (new, 161 lines), `selftest.py:55`, `:280`, `:356`, `:931` | the rows' checks (section 3), registered with the self-test; the two old-form expectations of the synthetic probes in the new form | |
| `e5baac61` | `selftest_mutants.py:446-463` | ten mutants (section 3) | each new rule has a plant it kills |
| `e5baac61` | `README.md:303-311` (Markers and grading), `:490-492` (AECP), `:509-519` (S2's three rows relabelled with what they measured), `:1088`, the mutant table | the rule, the refusal rows, the arm A/arm B split, the historical rows' labels | the authoritative doc |
| `e7e2b744` | `flip_grade.py` (new, 125 lines): `FLIP` :25, `COLUMN` :27, `findings` :30, `report` :49, `controls` :61, `flip_checks` :97, `main` :105 | the flip check: 8x8/2if at the pin held to 0.70, its own `--check` and `--selftest` | the ruling's items 4 and 6 |
| `e7e2b744` | `load_grade.py:7-13`, `:86-92` (`CEILING = {'1x1/1if': 0.70}`, `FLIPPED`), `:111-112`, `:340-343`, `:367-389`, `:509-515` | the merge gate holds 1x1/1if; the table names 8x8/2if's ceiling as the flip check's; the control "a held point not held" holds 1x1/1if by this gate and 8x8/2if by the flip check at the pin; the self-test runs the flip check's controls | item 4 |
| `e7e2b744` | `selftest_mutants.py:464-469` | four mutants (section 3) | |
| `e7e2b744` | `README.md:131-145`, `:195`, `:1390`, the mutant table | the split and the flip check's command; arm B's `aecp` group as a load-gate leg | |
| `e7e2b744` | `docs/design/SPLIT_CONTROL_MEMORY.md:2077-2082`, `:2136`, `:2138`, `:2140-2150`, `:2171` | section 13: the split, every row's response and the baseline, the cut measured and not committed, the load table with the flip check's ceiling | |

## 3. New checks, planted mutants and failing words

**The rows' responses** (`selftest_answers.py`, run by `run.py --self-test`). Each check below passes unplanted; each mutant makes the named check fail (the self-test prints its first failing check):

| Check (its words) | Holds |
|---|---|
| "a response with the type and status its row states is measured" | a GET_AVB_INFO response, SUCCESS |
| "a response with another status than its row states is refused" | NO_SUCH_DESCRIPTOR against SUCCESS: `status NO_SUCH_DESCRIPTOR, not the stated SUCCESS` |
| "a response to another command type than its row states is refused" | `0x0028` against `0x0027`: `answered as 0028` |
| "a probe's response is the one answering its sequence_id, not an earlier one on its channel" | an earlier GET_AS_PATH refusal, then its own |
| "a refusal its row states and names is measured" | the unknown command, NOT_IMPLEMENTED |
| "an MVU response with its stated command type and status is measured", "an MVU response with another status is refused", "an AEM response where an MVU response is stated is refused" | MVU at byte 42 |
| "an ACMP response of another message type is refused", "an ACMP response with another status is refused", "an ACMP refusal its row states and names is measured" | ACMP |
| "every row of the scenario that ends at a response states its type and status, each refusal named" | the real scenario's groups at one and two interfaces, arm A and arm B |
| "the get_avb_info row sends GET_AVB_INFO on AVB_INTERFACE 0 at its length, SUCCESS where the ports answer" | command_type `0x0027`, payload `0009 0000`, control_data_length 16; `aem:0027:SUCCESS` in arm B, `aem:0027:ENTITY_MISBEHAVING` as `get_avb_info, refused ENTITY_MISBEHAVING` in arm A |
| "the talker rows state the statuses Milan gives them, restated" | PROBE_TX TALKER_DEST_MAC_FAIL, GET_TX_STATE and DISCONNECT_TX SUCCESS, GET_TX_CONNECTION NOT_SUPPORTED |
| "a probe that ends at a response and states no type and status is named", "a refusal its row does not name is named", "a stated status that is no code of its kind is named" | `answers.unstated` |
| "a run refuses a group whose row states no response, by name" | `run.graded` |

| Mutant | Planted defect | Caught by |
|---|---|---|
| answers: a response's status is not checked | `differs` ignores the status | the expected response is checked |
| answers: a response's command or message type is not checked | `differs` ignores the type | a response to another command type than its row states is refused |
| answers: a probe's response is the first on its channel, whatever its sequence_id | `own_response` takes any response | a probe's response is the one answering its sequence_id, not an earlier one on its channel |
| answers: an MVU response read as an AEM response | MVU read at AEM's offset and type | an MVU response with its stated command type and status is measured |
| answers: a row that ends at a response need not state it (earlier rule) | `unstated` finds nothing | a probe that ends at a response and states no type and status is named |
| answers: a refusal row need not name its refusal | `refused` returns the bare row | every row of the scenario that ends at a response states its type and status, each refusal named |
| run: a group whose row states no response is graded as any other | `run.unstated` finds nothing | a run refuses a group whose row states no response, by name |
| scenario: get_avb_info sent as GET_AS_PATH on AVB_INTERFACE 9, the refused command (earlier rule) | `AVB_INFO` restored to `0x0028` with descriptor_index 9 and 16 bytes more | the get_avb_info row sends GET_AVB_INFO on AVB_INTERFACE 0 at its length, SUCCESS where the ports answer |
| scenario: the face's getters stated SUCCESS on the image as linked | arm A's two refusals stated SUCCESS | the same |
| scenario: the talker's refusals stated SUCCESS | every talker row SUCCESS | the talker rows state the statuses Milan gives them, restated |
| flip: an over-ceiling row passes | `flip_grade.findings` finds nothing | the load gate refuses a held point not held |
| flip: read on the column graded with tsn-c-stack#32 | `COLUMN = STATED_US_DONOR` | the flip check refuses the graded column read, not the pin |
| flip: 8x8/2if held to a looser ceiling | `FLIP = {'8x8/2if': 0.80}` | the load gate refuses a held point not held |
| load: 8x8/2if held by the merge gate again (earlier rule) | `CEILING` with 8x8/2if | the load gate refuses a held point not held |

The ten `answers`/`run`/`scenario` mutants were each run against the full check list before `e5baac61` and caught; the full self-test with every mutant runs in the gate pass (section 5). The flip check's own controls (`flip_grade.py --selftest`, `receipts/load/flip_grade.py_selftest.txt`): 6 of 6 refused (an over-ceiling row, a row within its ceiling passing, a raised cost, a missing cost, the ceiling other than 0.70, the graded column read); `load_grade.py --selftest`: 23 of 23.

## 4. Measurement: the baseline, the cut, the load

**The rows as they were** (round 26's recorded logs decoded, `receipts/rows882.txt`; the `acmp-cmd` rows by `tools/audit_rows.py`): arm A answered `get_avb_info` with GET_AS_PATH NO_SUCH_DESCRIPTOR, `get_counters` ENTITY_MISBEHAVING, `unknown_command` NOT_IMPLEMENTED under `0x3FF0`, PROBE_TX TALKER_DEST_MAC_FAIL and GET_TX_CONNECTION NOT_SUPPORTED, at both points; the notice arm's rows all SUCCESS. Every other row SUCCESS.

**The legs** (`receipts/baseline/`): each a fresh build on a clean clone of `e5baac61` (the donor's with round 26's port), its three images byte-identical to round 26's build (objcopy -O binary and ELF), its sample log byte-identical (`control` in arm A and with the donor, `notice-burst-6` in the notice arm); the five other input differences are generation stamps (`gateware/sim.v`, the runtime archives, `flash_port.json`, `tree:firmware`, which round 26's `f19c32d9` changed in tests). The `aecp` group run again on each; every other group's recorded log regraded:

| Leg | Groups | Refusals | Budget misses | Passes over the share | Against round 26 |
|---|---:|---:|---|---|---|
| GA8, arm A, 8x8/2if | 93 | 0 | 6 of 996 instances, 3 of 136 paths | 0 of 264,961 | the same; one pass fewer (the `aecp` group) |
| GA1, arm A, 1x1/1if | 94 | 0 | 6 of 945, 3 of 87 | 0 of 178,192 | the same |
| GN8, the notice arm, 8x8/2if | 16 | 0 | 0 of 736 | 0 of 14,133 | the same |
| GN1, the notice arm, 1x1/1if | 16 | 0 | 0 of 280 | 0 of 21,631 | the same |
| GB8, arm B, 8x8/2if (new: `aecp`) | 1 | 0 | 0 of 39 | 0 of 130 | new |
| GB1, arm B, 1x1/1if (new: `aecp`) | 1 | 0 | 0 of 25 | 0 of 110 | new |
| D8, tsn-c-stack#32, 8x8/2if | 18 | 0 | 6 of 182, 3 of 129 | 0 of 12,871 | the same |
| D1, tsn-c-stack#32, 1x1/1if | 19 | 0 | 6 of 141, 3 of 81 | 0 of 10,249 | the same; one pass more |

The six misses at each arm A and donor point are round 26's three egress-held paths (tsn-c-stack#26).

**The changed rows** (`receipts/rows882.txt`, each the row's ms and its taking pass): at 8x8/2if `get_avb_info` 0.338 ms in arm A (refused ENTITY_MISBEHAVING; was 0.316 as GET_AS_PATH) and 0.341 ms in arm B (SUCCESS); `get_counters` 0.255 (arm A, refused) and 0.284 (arm B); at 1x1/1if `get_avb_info` 0.118 (arm A, refused ENTITY_MISBEHAVING; was 0.095 as GET_AS_PATH) and 0.143 (arm B, SUCCESS). The `aecp` group's heaviest AECP record: 20,893 cycles (arm A) and 21,201 (arm B) at 8x8/2if, 15,322 and 15,838 at 1x1/1if, under the stated AECP record (265 and 205 us; its heaviest is `aecp-fanout`'s 24,848 and the notice arm's 18,381).

**The costs** (round 26's parsers on the merged legs with the arm B legs added, `receipts/costs/`; against round 26's, `receipts/costs/against-round26.txt`): every figure identical but the notice's instance count (35 to 41 at 8x8/2if, 29 to 32 at 1x1/1if, arm B's notices) and D1's ADP event (9,940 to 9,482 cycles, under the column's stated cost, which keeps its larger). The tables (`receipts/costs/tables27.txt`): **every stated cost unchanged**.

**The cut** (item 2, `receipts/cut/`: `q1.diff` on `e5baac61`, not committed; quick legs on scratch builds; `heaviest-records.txt`):

| Group (8x8/2if) | Heaviest SRP record, baseline | With the cut | Second heaviest | Heaviest work pass |
|---|---:|---:|---|---|
| `notice-every-3` (notice arm) | 34,361 | 33,741 | 23,475 to 22,458 | 179,486 to 181,542 |
| `notice-every-1` (notice arm) | 34,269 | 33,248 | 23,496 to 22,544 | 180,126 to 176,535 |
| `backlog-owed` (arm A) | 33,260 | 33,251 | 22,742 to 22,667 | 171,404 to 167,983 |
| `backlog` (arm A) | 26,664 | 26,691 | | 193,609 to 177,622 |

Closing 8x8/2if needs the heaviest record at 31,428 cycles (stated 330 us). The cut takes about as much from the second heaviest record as from the heaviest, so the heaviest's excess over the second, some 11,000 cycles, is not in what it reaches. ROM: the notice arm 122,788 B and arm A 122,480 B with the cut (under 122,880); arm A with tsn-c-stack#32 122,936 B, refused by the 8x8/2if ledger (`QD8.log`).

**The load at this head** (`receipts/load/`):

| Point | At the pin | With tsn-c-stack#32 (graded) | Held by | Compute for 0.70 |
|---|---:|---:|---|---:|
| 1x1/1if | 0.463 | 0.450 | `load_grade.py --check`, 0.70, for merge: rc 0 | 1.00x |
| 8x8/2if | **0.815** | 0.719 | `flip_grade.py --check`, 0.70 at the pin: rc 1 | 1.16x at the pin, 1.03x graded |
| 32x32/2if | 2.150 | 1.659 | reported: the more-compute image, #872 | 2.37x |

## 5. Gates

The full gate pass ran once, at `e7e2b7444a9859b058deff0d9edb575f2fb1946f`, each job and gate on a fresh clean clone of it, never piped. Every gate rc 0 but the flip check, which exits 1 by design (item 4). The receipts are in `receipts/gates/` (`workflows/` the job drivers, every step's log and rc, each job's tree check, `not_run.json` with every reason and `verify-table.md`; `sweep/`; `lane/`; the dispatcher logs and queues).

| Gate | Where it ran | Result | Receipt |
|---|---|---|---|
| Every `run:` step of `rtl-fast.yml`, `rtl.yml`, `elaborate.yml` and `docs.yml` (the four a pull request to `dev-soft-core` triggers) | each job its own clone (`run_wf.py`), the firmware jobs with the LiteX venv | **139 steps rc 0, 226 not run, each with its reason, 0 bad** (`verify_wf.py`, rc 0) | `workflows/verify-table.md` |
| `rtl-fast.yml`: `changes`, `verilator-lint`, `bdd-conformance`, `yosys-tool`, `yosys-elaboration`, `publication-census`, `split-cdc`, `rtl-fast` | 10:08 to 10:53 | every step rc 0; `behave` 508 scenarios, 2,330 steps passed | `workflows/drivers/rtl-fast-*.driver.log` |
| `firmware-unit` | 10:09 to 10:40 | every step rc 0: `test_ctrl_firmware.py --require-rv32 --self-test` PASS; the saved-state store gate's 455 tests; `fw_coverage.py --check` PASS (38 files) | `workflows/logs/rtl-fast__firmware-unit__ci_step_1{0,1,2}.log` |
| `firmware-control-mutants` | 10:17 to 10:45 | 672 of 672 caught | `..._firmware-control-mutants__ci_step_9.log` |
| `firmware-srp-mutants` | 10:45 to 11:00 | 340 `[ok]`, `test_ctrl_firmware: PASS` | `..._firmware-srp-mutants__ci_step_9.log` |
| `firmware-aecp-mutants` | 11:13 to 11:40 | 220 `[ok]`, `test_ctrl_firmware: PASS` | `..._firmware-aecp-mutants__ci_step_9.log` |
| `firmware-boundary` | 11:17 to 11:37 | `ctrl_boundary: PASS`: 3,311 compiled sources, 0 findings | `..._firmware-boundary__ci_step_9.log` |
| `firmware-verilator` | 11:13 to 11:40 | `ctrl_boundary: PASS`: 1,123 compiled sources, 0 findings | `..._firmware-verilator__ci_step_14.log` |
| `rtl.yml`: `full-ci-gate`, `yosys-tool`, `yosys-shards` 0/4 to 3/4 | 11:53 to 12:07 | every step rc 0 | `workflows/drivers/rtl-*.driver.log` |
| `elaborate.yml`: `elaborate-gates-0`, `elaborate-gates-1`, `elaborate` | 11:18 to 12:00 | every step rc 0 | `workflows/drivers/elaborate-*.driver.log` |
| `docs.yml`: `wire-accountability`, `docs-check-no-git`, `docs-gates-0` (43 steps), `docs-gates-1`, `docs-gates-2`, `docs-check` | 11:06 to 12:20 | every step rc 0; `docs-check-no-git`'s three steps rc 0, and the job removes `.git`, so the runner's own tree check after it cannot run (as in rounds 25 and 26) | `workflows/drivers/docs-*.driver.log` |
| The full sweep (`rtl.yml`'s `verilator-shards` suites), `scripts/run_all_suites.sh` as four `native-shards.py` units, MemoryMax 10G, `-j4 --no-print-directory`, shard 2 (`capture_coherence`) on four CPUs | 12:11 to 13:46 on 24-31, 80-87, 68-71, 88-95 | **65 suites, 65 passed, 0 failed, 0 timed out; 2,613,726 checks, 0 in-suite failures**; every shard's preflight PASS (suite cancellation among them: no #833 re-run). Tree after: clean in shards 0 to 2; in shard 3 the two `TEST_RESULTS.md` files the `tsn_fuzz` campaign writes in place show a new date stamp only, their counts unchanged | `sweep/shard-*-01.log`, `shard-*.complete.json`, `preflight-*/`, `shard-*-tree-after.txt` |
| `git diff --check` against the merge base `1d6bf555` (the live `dev-soft-core` tip) and against `0b37f3d2` | lane clone | rc 0, no output | `lane/diffcheck_*.log` |
| `check_py_idiom.py`, `check_cpp_idiom.py`, `check_baremetal_only.py --check`, `docs_check.py` | lane clone | rc 0 (`docs_check`: 0 findings across 217 md files) | `lane/` |
| `ctrl_hot.py --self-test`, `--check` | lane clone | rc 0 (208 entries in the recorded order) | `lane/ctrl_hot_*.log` |
| The harness self-test (`run.py --self-test`) | lane clone | **`self-test: 0 failures`**: the rows' eighteen checks pass and the fourteen new mutants are caught (196 `MUTANT caught`, none escaped) | `lane/harness_selftest.log.tail` |
| `load_grade.py --selftest`, `--check` | lane clone | 23 of 23 controls refused; `RESULT: PASS` (1x1/1if 0.450 against 0.70) | `lane/load_*.log` |
| `flip_grade.py --selftest`, `--check` | lane clone | 6 of 6 controls refused; **`--check` rc 1 by design**: `OVER 8x8/2if: the load 0.815 at the pin is over the flip ceiling 0.70` | `lane/flip_*.log` |
| `ctrl_service_hooks/run.py --self-test`, `nvm_split_target/run.py --self-test` | lane clone | 28 of 28 checks and 96 of 96 mutants; 73 checks, 0 failures | `lane/hooks_selftest.log`, `lane/target_selftest.log` |
| `test_ctrl_nvm.py --require-rv32 --self-test --jobs 8` | lane clone | rc 0: 455 tests, all 121 planted defects reddened | `lane/nvm_selftest.log` |
| `gen_mailbox.py --check --crosscheck`, `--selftest`; `lint_rtl.py --check`; `test_soc_options.py`; `test_ctrl_memory.py` | lane clone | rc 0 each (lint 89 within its ratchet of 89) | `lane/` |
| `test_builder.py --require-rv32` | lane clone | rc 0, `ALL GATES PASS EXCEPT 2 NOT RUN` (the same two arms as round 14's, each with the tool's reason) | `lane/test_builder.log` |
| `ctrl_split_boot` at 1x1, 8x8, `--native-controls`, `--self-test` | lane clone | `ctrl_split_boot: PASS (0 finding(s))` at both shapes; 6 of 6 native controls; 3 of 3 plants, 8 of 8 placement controls | `lane/boot_*.log` |
| `cd tests && behave` | lane clone | 508 scenarios, 2,330 steps passed | `lane/behave.log` |
| `make -C tb/verilator/milan_dp twin` | lane clone | `twin: 0 finding(s)` | `lane/twin.log` |
| The harness at both points (S2's harness): every recorded group of arm A, of the `answering-every-port` arm and arm B's `aecp` group at 1x1/1if and 8x8/2if, regraded at the head from the legs' builds (`--reuse-build`, refused unless every recorded input and tree digest resolves unchanged at the head) | clone K at `e7e2b744`, clean | rc 0 each: 0 refusals; GA8 93 groups, 6 of 996 instances (3 of 136 paths); GA1 94, 6 of 945 (3 of 87); GN8 0 of 736; GN1 0 of 280; GB8 0 of 39; GB1 0 of 25; 0 passes over the share in every leg | `receipts/head/` |

The lane clone's tree after its gates and every job's tree check are clean (`lane/tree-after.txt`, empty; `workflows/tree-after/`, 28 of 28 clean). Memory: since 11:12 every gate ran in a unit of its own with MemoryMax 10G, none in this session's unit (under 1 GB throughout); the largest was the lane clone's, peak 9.2 GB (its NVM self-test and builder test, within its cap). The jobs kept from before the 11:07 cut (`rtl-fast.yml`'s eight fast jobs, `firmware-unit` and `wire-accountability`) ran in the earlier session's own unit, as its dispatcher then placed them (`dispatch-to-1107.txt`); `firmware-control-mutants` and `firmware-srp-mutants` ran as booked units. Host MemAvailable fell to 13.9 GB at 13:13, all of it other lanes' use (this lane's units then held 1.2 GB), and rose again; no gate was started below the floor.

## 6. Findings, deviations and open questions

- **D1, deviation: SUCCESS asserted in arm B, a named refusal in arm A.** The ruling's item 1 asks the row to assert SUCCESS. GET_AVB_INFO's values come through the face block's GSI window (`aecp_face.c`), and the test SoC holds the datapath idle (README, The test SoC), so in arm A, the image as linked, the window read finds no answer within its bound (`MBX_WIN_GSI_WAIT_CYCLES`, 64 polls) and the command answers ENTITY_MISBEHAVING (`aecp_commands.c`, `avb`). SUCCESS is reachable only where the observation ports answer, arm B, whose `aecp` group is now one of the load gate's legs at both points; arm A's row is a named refusal. GET_COUNTERS is in the same case (it was measured as a refusal, unnamed, before #882).
- **F1, a firmware finding (for a new issue):** `aecp.c:428` masks command_type with `0x3fff`, so a command at or above `0x4000` is answered under another command_type: `0x7FF0` is answered NOT_IMPLEMENTED as `0x3FF0` (round 26's logs, `receipts/rows882.txt`). An AEM response carries the command_type of the command it answers, a 15-bit field (IEEE 1722.1-2021 9.2.1.2). Proposed issue: "AECP answers a command_type at or above 0x4000 under another command_type (`aecp.c` keeps 14 bits)", acceptance: the response echoes the 15-bit command_type; a firmware test with `0x7FF0` and `0x4000`; the harness's unknown command back to `0x7FF0`. Out of this lane's scope (no firmware change this round).
- **F2, a measurement limit (for the flip-gate issue or a new one):** no arm measures GET_AVB_INFO, GET_COUNTERS or GET_STREAM_INFO with their window reads answered: arm A's are refused at the window's bound, and arm B's stubs read no window (README, `answering-ports`). The product's SUCCESS path makes three GSI reads (GET_AVB_INFO) or 33 CTR reads (GET_COUNTERS), each answered within the bound. A testbench model of the face's answer would measure it.
- **F3:** `acmp-cmd`'s PROBE_TX row measures TALKER_DEST_MAC_FAIL (the source has no stream destination in that group, Milan v1.2 Tables 5.42 and 5.43), now named as a refusal; the SUCCESS path of a talker's PROBE_TX is measured by no row.
- **D2, deviation: the cut measured, not committed, so no firmware mutant.** Item 2 asks for the cut, measured, with a mutant. The cut is measured (section 4) and it neither closes 8x8/2if (about 0.713 graded) nor fits the ROM ledger with tsn-c-stack#32: arm A's image with the donor would go 56 B over 122,880, so the graded column's 8x8/2if leg would not build. Committing it would have cost a full re-measure of every leg (about 17 CPU-hours) for 0.006, at a ledger the pin move cannot meet. The tree keeps the baseline's firmware; `q1.diff` and its legs are the evidence. The images' `rom` (each build's `image.log`): at the pin arm A 122,328 to 122,480 B and the notice arm 122,636 to 122,788 B (+152 B each, the figure section 13 states), arm A with tsn-c-stack#32 122,776 to 122,936 B (+160 B), which the ledger refuses (`receipts/cut/QD8.log`). A trimmed cut under the 104 B the donor arm has left would take less than the measured 620 cycles. The PR targets `dev-soft-core`, where the TSN stack pin move that carries tsn-c-stack#32 is in flight (tsn-c-stack#34 merged on the stack's `main` at `715589c`; its lane took the move at 09:46): a committed cut would have put that move's 8x8/2if arm A image over its ledger.
- **Interpretation:** "S2's tallies" read as the harness's tallies at both gated points (groups, refusals, misses by instance and path, passes over the share) and the changed rows' figures. The README's Results tables are S2's own run at firmware `e76a755a` and are not re-measured; their three refusal rows are relabelled with what they measured (#882).
- **The host and the filesystem:** the session was cut at 08:23 by a host reset; the root filesystem went read-only (`emergency_ro`) at about 08:3x, so the next session staged this file and the receipts on scratch; a second reset at 09:51 cut that session's gate pass at its start and left the files written in its last minutes empty (the sweep's source clone, the gate scripts, the venv, clone K's moved head). Each was rebuilt: the scripts from round 26's copies, the venv afresh, clone K reset to `e7e2b744` (its tree then clean, `hdl`, `sw/firmware`, `sw/mailbox` and the harness byte-equal to the commit). The early self-test run on the working tree before `e5baac61` was cut with no verdict and is not cited.
- **#870** had not landed by the measurement, nor by the end of the gate pass; the flip-gate issue carries its access cycles.

## 7. The flip-gate issue's text (item 4)

The manager opens it; its text is `FLIP-GATE-ISSUE.md` in this directory.

## 8. Run history

- 2026-11-11 07:32 CET start; head `0b37f3d2` and origin verified; #882 read (no comments); the ruling read; #870 round 3 TAKEN only (06:23).
- 07:36 TAKEN posted (issuecomment-6788936516).
- 07:4x to 08:05 #882's harness change: the rows of round 26's logs decoded (the refusal rows found), `answers.py`, the scenario's rows, the self-test checks and mutants; `e5baac61` committed 08:05.
- 08:06 to 08:15 the baseline legs (eight builds, booked units and the session); 08:10 to 08:40 their regrades; 08:15 to 08:29 the cut's quick legs on scratch builds (`QD8` refused by the ledger).
- 08:23 a host reset cut the session; about 08:3x the root filesystem went read-only. The next session (08:3x to 09:51) finished the regrades and the costs, decided the cut (not committed), wrote the flip check and committed `e7e2b744` (09:22), and started the gate pass (09:27); the 09:51 reset cut it at its start.
- 09:55 this session: the state reconstructed from the commits, the staged handoff and the receipts; the empty files rebuilt; 10:00 the sweep's launcher started (waiting for four free ranges); 10:05 the harness's head regrades (six legs from clone K at `e7e2b744`); 10:08 the workflow jobs and the lane's gates through the dispatcher.
- 10:08 to 11:05 at `e7e2b744`: the head regrades rc 0 (all six); `rtl-fast.yml`'s eight fast jobs, `firmware-unit`, `firmware-control-mutants`, `firmware-srp-mutants` and `docs.yml`'s `wire-accountability` ended, every step rc 0. 11:05 `firmware-aecp-mutants` and `firmware-boundary` failed with their job clones gone from under them (`FileNotFoundError` on the job's `wt`), no verdict; restarted 11:06 with `firmware-verilator` and `docs-check-no-git`, all four cut at about 11:07 when the session ended (an API refusal of one message). The sweep's launcher was still waiting for four free ranges; no shard had started. Every one of these outputs is kept aside unused (`killed-1105`, `killed-1107`).
- 11:08 the session resumed: no unit or process of the lane alive. The remaining gates restarted at 11:12 through `dispatch3.py`, which starts every job as its own transient unit with MemoryMax 10G, on a range `cpu_ranges.py pick8` books when one is free, else on the shared session pool (96-127, which every booking already counts as busy, so it holds nothing from another lane); never in the session's unit. The sweep's launcher restarted at 11:12, the four shard clones prepared again at `e7e2b744`.
- 11:12 to 12:20 the workflow jobs left ended, every step rc 0; 12:2x `verify_wf.py`: 139 steps rc 0, 226 with a reason, 0 bad.
- About 12:06 the dispatcher and the sweep's launcher were found gone, with no traceback, no OOM and the units they had started still running (each unit writes its own rc, so no result was lost). Both had generic script names; the launcher was restarted as `a683zj_sweep_wait.py`, which also takes a free aligned 4-CPU block for shard 2, the shard run on four CPUs: four free 8-CPU halves at one moment had not come in an hour. It launched the four shards at 12:11 on 24-31, 80-87, 68-71 and 88-95.
- 13:18 to 13:46 the four shards ended, rc 0 each. 14:34 `test_builder.py` rc 0 (82 minutes on the shared pool, about a quarter of a core); a second dispatcher (`a683zj_disp.py`) waited eight minutes to run the six gates after it on a booked range, and was stopped by its PID, unused, once `boot_1x1` took two minutes. 15:00 the lane gates' last, `twin`, rc 0.
- 15:0x the receipts collected and scrubbed of host paths, this file and `PR-BODY.md` written, `receipts/INDEX.md` generated, REVIEW READY posted.
