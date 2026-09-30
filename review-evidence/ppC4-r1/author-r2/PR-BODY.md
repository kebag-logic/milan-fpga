[A450]

Closes #45
Closes #47
Closes #48

Lane C4 of the PP program: ACMP (assignment: #45 comment 5891906554; round 2: #45 comment 5903960934). Branch `c4-acmp-coverage` from `main` `b2db3a97`, one or more commits per item, in the assignment's order. Round 1:

| Commit | Item |
|---|---|
| `d87b3d5` | 1. #47: ACMP messages outside the listener set are inert, the probe-response guard per term, the `tb/pp_top` leg, the mutation driver |
| `2a3e608` | 2. #45: the 96-byte IEEE ACMPDU in `tb/rx_validator` and `tb/pp_top`, and the cdl != 44 rejection mutant |
| `af6a5f1` | 3. #48: the integrated settle path to SRP listen in `tb/pp_top`, and the `st_ls_r` glue, bound-view and matcher mutants |
| `20e24d4` | the mutation tables remeasured at the lane head |
| `a7ccd9e` | the parent C++ idiom gate (Rule 11) on the new test code: one array initializer split across lines |
| `a9ce0fa` | item 3 tightened: AS6's quiet window counts every ACMP frame, not only the next probe |

Round 2's commits are listed under [Round 2](#round-2).

**Tests, one mutation driver, suite records and two documentation rows.** No new test exposed an RTL defect, so no RTL changed: `git diff b2db3a97..616cbdf -- hdl` is empty, and no port, parameter or register of `protocol_processor_top` changes. The one non-suite source touched is the `tb/pp_top` wrap, which now connects the top's existing `acmp_bound_eid_o`, `acmp_bound_sid_o`, `acmp_bound_dmac_o` and `acmp_bound_vlan_o` for item 3. Round 2 changes one cell of `docs/00_MILAN_COMPLIANCE_REVIEW.md` F00.2 and one row label of `docs/architecture/09_verification.md` F09.4.

The top-level legs run as a new section AC of `tb/pp_top` on a fresh model (as MP and DV do), so the main DUT's tuned timeline does not move. `./obj_dir/Vpp_top_sim --acmp-only` (after `make gsi-build`) runs it alone. Sink 1 is bound throughout, never sink 0, so a stage that loses the sink index cannot pass by accident.

## 1. #47: messages outside the listener and talker sets are inert (REQ-ACMP-012)

**Clause.** Milan v1.2 §5.5.3.1 gives the listener BIND_RX, GET_RX_STATE and UNBIND_RX commands with its own listener_entity_id; §5.5.3.5.18 step 1 (PRB_W_RESP), which §5.5.3.5.25 applies unchanged in PRB_W_RESP2 ("same treatment"), ignores a PROBE_TX_RESPONSE that does not match the saved command's controller_entity_id, talker_entity_id, talker_unique_id and sequence_id. IEEE 1722.1-2021 §8.2.1.4 Table 8-2 supplies the codes (IEEE 1722.1-2013 §8.2.1.5 Table 8.1 lists the same codes): 3, 5, 7, 9, 11 and 13 are responses other than PROBE_TX_RESPONSE (CONNECT_TX_RESPONSE), and 14 to 15 are reserved.

**Acceptance.**
1. `tb/acmp_listener` **B13** drives message types 3, 5, 7, 9, 11, 13, 14 and 15 with the own listener_entity_id and a valid listener_unique_id, in PRB_W_RESP (status SUCCESS) and PRB_W_RESP2 (TALKER_NO_BANDWIDTH). Each is shaped as the perfect answer to the outstanding probe (all four guard terms equal, stream fields set), so only its type keeps it out. Each is fully inert: no frame, no record write, no timer op, no action strobe, no notify, the record unchanged, and exactly one RX-slot free of the slot it arrived in.
2. `tb/acmp_listener` **B14** grades the guard term by term: a response with the wrong controller_entity_id, talker_entity_id or talker_unique_id is ignored in both probing states, as B8's wrong sequence_id already was. The unaltered response then settles, so a guard that rejected everything would fail.
3. `tb/pp_top` **AI1-AI3**: a BIND_RX_RESPONSE (7) and a reserved type (14), shaped as the answer to probe #1, reach the listener through the real steer. Neither raises an ACMP frame, neither is dropped at the front end, all four RX slots are free and no scoreboard hold is left. The exact duplicate probe then follows at T-ACMP-CMD, which proves the sink never left PRB_W_RESP.
4. **Mutation.** `txn_msg_ok_w` forced to 1 fails 93 of 2988 `tb/acmp_listener` checks (all 16 B13 arms settle or back off) and `tb/pp_top` AI3. Each guard term tied true fails its B14 arms: controller_entity_id 50, talker_entity_id 40, talker_unique_id 30 of 2984. All are recorded in `tb/acmp_listener/README.md` and `tb/pp_top/README.md`.

## 2. #45: ACMPDUs longer than 56 bytes are accepted (REQ-ACMP-001)

**Clause.** Milan v1.2 §5.5.2.2: a Milan device "shall send and accept this truncated PDU, and may accept the longer PDU". The architecture takes that option (03 V3, the F09.4 96-B row). IEEE 1722.1-2021 §8.2.1.6 sets control_data_length to 84 for the 96-byte form of Figure 8-1 (ip_flags, reserved, source_port, destination_port and two 128-bit IP addresses after connected_listeners_entries @54); IEEE 1722.1-2013 §8.2.1.7 sets it to 44, the 56-byte length Milan keeps.

**Acceptance.**
1. `tb/rx_validator` **F29** drives the 96-byte form, cdl 84, with its 40-byte IP tail filled with a pattern, as a BIND_RX and as a PROBE_TX. Each is committed, no counter moves (rx_length above all), and the slot holds all cdl + 12 = 96 bytes. The header beat is field-exact against the offset model and equal to the truncated form's but for cdl, including the listener or talker unique_id.
2. `tb/pp_top` **AL1-AL4**: a 96-B UNBIND_RX is answered by the 56-B cdl-44 UNBIND_RX_RESPONSE. A 96-B BIND_RX gets the same response as AI1's 56-B BIND_RX, byte for byte, and the PROBE_TX regenerated from its record is byte-exact, so the long command's fields reached the binding and not only the echo. A PROBE_TX to our talker gets one byte-exact answer for the 56-B and the 96-B form (TALKER_DEST_MAC_FAILED: no allocator is wired on that model, as S10 (c) grades on the main DUT). There are no front-end drops and no slot leak.
3. **Mutation.** A validator that accepts ACMP only at cdl 44 fails 27 of 495 `tb/rx_validator` checks (F29 both forms, and F4's cdl-24 short form too) and 19 of 43 in section AC (AL1-AL4, then the legs that need the long BIND_RX's binding). It is recorded in `tb/rx_validator/README.md` (M5) and `tb/pp_top/README.md`.

## 3. #48: the settle path to SRP listen, end to end (REQ-ACMP-016)

**Clause.** Milan v1.2 §5.5.3.5.18 step 4: on a matching PROBE_TX_RESPONSE SUCCESS, note stream_id, stream_dest_mac and stream_vlan_id, initiate SRP reservation, start TMR_NO_TK (10 s), go to SETTLED_NO_RSV. §5.3.8.9: the recorded values are exactly the last response's, and a divergent talker attribute is ignored. §5.3.8.5: with a matching Talker Advertise registered, the sink declares Listener Ready. §5.5.3.5.42: EVT_TK_REGISTERED clears TMR_NO_TK and goes to SETTLED_RSV_OK. §5.5.3.5.36: TMR_NO_TK in SETTLED_NO_RSV tears SRP down. §5.5.3.5.45: UNBIND_RX in SETTLED_RSV_OK stops SRP and clears the binding. Tables 5.37 to 5.39 give the GET_RX_STATE forms. IEEE 802.1Q-2018 §35.2.2.7.2 gives the Listener FourPackedType.

**Path under test.** The listener's A15 reaches the SRP listener matcher only through the top's service stage (`st_ls_r`: DECLARE_LISTENER, op 2, state READY, the sink index, stream_id, DA and VID), and returns as TK_ATTR_REGISTERED through the event router.

**Acceptance** (`tb/pp_top` AS1-AS6, about 19 s of simulated time on the phase's own model).
1. **AS1-AS2.** PROBE_TX #2 goes unanswered: its exact duplicate follows, T-ACMP-RETRY finds no talker and re-probes nothing, and GET_RX_STATE answers the probing form (Table 5.37). The talker's ENTITY_AVAILABLE drives discovery and T-ACMP-DELAY to PROBE_TX #3, byte-exact, which the bench answers with a PROBE_TX_RESPONSE SUCCESS. After that, `acmp_bound_o`/`eid`/`sid`/`dmac`/`vlan_o[1]` carry exactly the response's stream, every other sink's view stays clear, and GET_RX_STATE answers the settled form (Table 5.38) byte-exact.
2. **AS3-AS5.** Near misses on the DA, the VLAN and the stream_id put no Listener vector on the wire, register nothing on the class-D face and route no TK_ATTR_REGISTERED{1}. The matching Talker Advertise then yields Listener Ready New byte-exact (alone in its MRPDU), class-D READY and ADVERTISE for sink 1, exactly one TK_ATTR_REGISTERED{1}, and GET_RX_STATE in Table 5.39's form. Table 5.39's bytes equal Table 5.38's while the registered attribute is an Advertise, so the state itself is graded too: 11.5 s after the settle, with the bench re-joining its Advertise every second, there is no re-probe and no Lv, and the declaration, the GET_RX_STATE stream fields and the bound view all hold. A sink left in SETTLED_NO_RSV cannot do that past T-ACMP-NOTK.
3. **AS6.** UNBIND_RX from SETTLED_RSV_OK: the response is byte-exact, and the Listener attribute is withdrawn on the wire (Lv, FourPackedType Ready) byte-exact. The bound view clears, no declaration or match is held, GET_RX_STATE answers the unbound form byte-exact, nothing probes the sink from the unbind on (round 2: no ACMP frame between the UNBIND_RX_RESPONSE and the GET_RX_STATE, whose answer must be the next ACMP frame, and none in the 1.5 s after it), and no RX slot or scoreboard hold is left.
4. **Mutation** (failing checks of 43, all KILLED, recorded in `tb/pp_top/README.md`). In `st_ls_r`: settle issued as WITHDRAW 7, teardown issued as DECLARE 1, stream_id/DA swapped 7, state NONE 7, VID dropped 7, sink index 0 6 (the wire frame is identical there, so only the per-sink faces and the state show it), teardown strobe lost 2. The bound view: latch removed 2, DA latched from the stream_id 2, not cleared on unbind 1. The SRP listener matcher ignoring the DA or the VLAN fails the three AS3 near-miss checks (5 each).

## Validation, round 1

At `a9ce0fa`, Verilator 5.052, make capped at eight jobs; the parent consumer set in scratch parents at milan-fpga dev `79c36963`. All processor commands rc 0: `./scripts/run_suites.sh` (33 suites, 1,016,816 checks, 0 failing), `./scripts/lint_hdl.sh`, `make check`, `python3 scripts/gen_matrix.py --check`, `acmp_mutants.py` (19 of 19 KILLED), `gsi_mutants.py`, `name_wr_mutant.py`, `d3_mutants.py` (83 of 83 KILLED), `git diff --check`. The parent set failed only where it failed identically at the lane base, all attributed to processor #132 and #133 pending parent adoption; the head added one finding, `acmp_mutants.py` in `measure_test_evidence`. Round 2 re-runs everything at its head against dev `ec0cc0c1` with the combined #132 + C1 adaptation.

## Round 2

Round 2 answers R410-1 (F-1, S-1, S-2), R411-1 (S1, S4) and the manager's parent consumer bank (5903837095), in the assignment's order. Item 4 (R411-1 S4) was made, stopped the round on the parent's wall-clock ratchet (5906502273), and is withdrawn by a revert commit under the manager's ruling on that STOP (5906539259); S4 is retained. R411-1 S2's snapshot reading is not taken, per the ruling on F-1; R411-1 S3 (the bound stream identity survives an A8 teardown) is pre-existing, port-visible behaviour, recorded by the manager on the residue checklist and not changed here.

| Commit | Item |
|---|---|
| `9151e8b` | 1. R410-1 F-1: F00.2's GAP-15 open residue reads "none found" |
| (no tree change) | 2. the parent disposition line for `acmp_mutants.py`, below |
| `f55a25f` | 3. R411-1 S1 and R410-1 S-2: the IEEE 1722.1 edition named on every message_type and flags table citation and on F09.4's 96-byte row |
| `dbd8624` | 4. R411-1 S4: a per-run timeout in `acmp_mutants.py` (reverted by `616cbdf`) |
| `06a84f5` | 5. R410-1 S-1: AS6's ACMP queue graded empty before the GET_RX_STATE, whose answer is read as the next ACMP frame |
| `bf764ac` | the `tb/pp_top` mutation table remeasured after items 3 to 5 (section AC is 43 checks); the same records again at `616cbdf` |
| `616cbdf` | item 4 withdrawn per the ruling on the STOP: the revert of `dbd8624`; R411-1 S4 retained |

The round-2 head is `616cbdf`.

### 1. F00.2, GAP-15 (R410-1 F-1)

The F00.2 caption defines the Open residue column: a linked issue tracks what is still unimplemented or ungraded, and "none found" means the resolution is implemented and a suite of the named category grades it. GAP-15's category is TOL. The residue #45 carried (REQ-ACMP-001, Milan v1.2 §5.5.2.2: no suite fed an ACMPDU longer than 56 bytes) is graded by `tb/rx_validator` F29 and `tb/pp_top` AL, and this PR closes #45; no other issue names GAP-15. Under the ruling that a PR closing the residue issue updates the cell by the table's rule (precedent `05fd9e1`, the GAP-03 row), the GAP-15 cell now reads "none found" (`docs/00_MILAN_COMPLIANCE_REVIEW.md:509`). Nothing else in 00 changes; the column stays the dated audit of 2026-09-18 for every other row. Round 1's "per that table's own rule it reads none found" overstated the rule: the rule defines what "none found" means, and the ruling is what applies it when the residue issue closes.

### 2. The parent disposition for `acmp_mutants.py`

In the form of the `d3_mutants.py` entry, for `DUT_READER_DISPOSITIONS` in the parent's `scripts/measure_test_evidence.py`:

```
    "protocol-processor/tb/pp_top/acmp_mutants.py":
        "mutation campaign; it plants one ACMP listener, validator, top SRP-service, bound-view or "
        "SRP matcher defect from its own table into an isolated copy and requires every named check "
        "to fail in a completed run; no expected value is read from the text",
```

With the combined adaptation and this line, `measure_test_evidence.py --check` is rc 0 at the round-2 head: 0 <= 0 unexplained DUT-source readers, 3 <= 3 wall-clock-dependent suite files. The sixteen consumer commands are rc 0; see Validation, round 2.

### 3. The IEEE 1722.1 editions (R411-1 S1, R410-1 S-2)

Checked against both editions:

| Field | IEEE 1722.1-2021 | IEEE 1722.1-2013 |
|---|---|---|
| message_type | §8.2.1.4, Table 8-2 | §8.2.1.5, Table 8.1 (the same codes: 0 to 13, 14 to 15 reserved) |
| status | §8.2.1.5, Table 8-3 | §8.2.1.6, Table 8.2 |
| control_data_length | §8.2.1.6: 84 (the 96-byte ACMPDU of Figure 8-1) | §8.2.1.7: 44 (56 bytes) |
| flags | §8.2.1.16, Table 8-4 | §8.2.1.17, Table 8.3 |

The lane's "IEEE 1722.1-2021 Table 8-2" was right for 2021. `tb/acmp_nvm`'s "Table 8.1" used 2013 numbering with no edition, and its "Table 8.2" for the flags names the status table in 2013; the flags are 2013 Table 8.3, 2021 Table 8-4. F09.4's "2013 96-B ACMPDU" named the wrong edition: the 96-byte form is 2021's (its §8.2.1 NOTE 2: the ACMPDU has additional fields compared with 2013), and 56 bytes is the 2013 length that Milan v1.2 §5.5.2.2 keeps. Every citation the lane added, and `tb/acmp_nvm`'s, now names its edition: `tb/acmp_listener/README.md:69`, `tb/acmp_listener/sim_main.cpp:1209-1210,1221`, `tb/pp_top/README.md:1141`, `tb/pp_top/sim_main.cpp:8812,8976-8977,9018`, `tb/rx_validator/sim_main.cpp:754`, `tb/acmp_nvm/sim_main.cpp:176,185` and `docs/architecture/09_verification.md:62` ("96-B IEEE 1722.1-2021 ACMPDU (cdl 84) and 56-B Milan ACMPDU (cdl 44, the IEEE 1722.1-2013 length)"). Comments and one table row only; every suite's tally is unchanged.

### 4. R411-1 S4: retained (item 4 withdrawn)

`dbd8624` gave each build and run of `acmp_mutants.py` a per-run timeout: at the bound the command's process group was killed and the copy recorded SURVIVED/TIMEOUT, never KILLED, and two scratch probes showed it held. A process deadline in a suite file counts towards the parent's wall-clock ratchet, though: the fourth number in `scripts/test_evidence.budget`, at 3, which "may only go down". So `measure_test_evidence.py --check` failed with "4 wall-clock-dependent suite file(s) > ratchet 3" even with the item-2 line, and the round stopped on that conflict. The manager's ruling on the STOP withdraws item 4 by a revert commit and records S4 as retained, for these reasons:
- S4 was a suggestion. R411-1 itself states that a hang can never produce a false KILLED: it yields no tally, so its only cost is wall time. The driver counts a copy KILLED only when the run completes with its tally, exits non-zero and fails every named check.
- The parent's wall-clock ratchet may only go down, and raising it for a suggestion defeats the ratchet.
- `d3_mutants.py` follows the same pattern without a timeout.

`616cbdf` reverts `dbd8624` as a new commit; no history is rewritten. `tb/pp_top/acmp_mutants.py` is byte-identical to round 1's (`a9ce0fa`) again, and `tb/pp_top/README.md` loses the timeout usage text. Re-measured at `616cbdf`, the ACMP mutation table matches `bf764ac`'s record for record, so the recorded table stands unchanged.

### 5. AS6 grades the ACMP queue from the unbind on (R410-1 S-1)

`get_rx_state()` waited with `wait_acmp`, which drops any non-matching frame, so an ACMP frame emitted between the UNBIND_RX_RESPONSE and the GET_RX_STATE_RESPONSE went ungraded. AS6 now grades `q_acmp` empty before the GET_RX_STATE feed, counts a stray frame once, and reads the answer as the next ACMP frame (`tb/pp_top/sim_main.cpp:8916,9258-9261`). Clause: Milan v1.2 §5.5.3.5.45 (UNBIND_RX in SETTLED_RSV_OK stops SRP and discovery and clears the binding; nothing probes an unbound sink). A scratch defect proves the check has teeth: UNBIND_RX in SETTLED_RSV_OK also runs A5, so the unbound sink sends one PROBE_TX right after its response (T-ACMP-CMD then expires in an inert cell). The round-1 bench (`a9ce0fa`) lets it SURVIVE with no check failing; this head KILLS it on the new check alone (1 of 43). Both goldens PASS. Section AC is 43 checks; every mutant's failing count is unchanged.

### Validation, round 2

At the round-2 head `616cbdf`, after the revert: Verilator 5.052, Verilator's build make capped at eight jobs, one heavy build at a time. The same commands were all rc 0 at `bf764ac` too, with the same totals and records.

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, 1,016,817 checks, 0 failing (acmp_listener 2988, acmp_nvm 360, rx_validator 495, pp_top 7931) |
| `./scripts/lint_hdl.sh` | 0 | 41 modules |
| `make check` | 0 | lint 41 mermaid + 18 wavedrom, links 976, matrix 115 REQ / 17 GAP, modmatrix 94 rows 0 untested, params 26 |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `python3 tb/pp_top/acmp_mutants.py` | 0 | 19 of 19 KILLED by their named checks; three goldens PASS; every record (build and run rc, completion, named, missing and failing checks) equal to the `bf764ac` run; counts equal to round 1 but for the section AC denominator (43) |
| `python3 tb/pp_top/gsi_mutants.py` | 0 | 20 detected; golden and restored PASS |
| `python3 tb/pp_top/name_wr_mutant.py` | 0 | decode killed; golden and restored PASS |
| `python3 tb/pp_top/d3_mutants.py` | 0 | 83 of 83 KILLED; goldens of `tb/acmp_nvm`, `tb/pp_top` and `tb/rx_validator` PASS (it builds three of this lane's changed suites) |
| `git diff --check b2db3a97..616cbdf` | 0 | also `a9ce0fa..616cbdf` |

Mutation table (`acmp_mutants.py`, failing checks):

| Mutant | Suite | Failing |
|---|---|---|
| `msg_ok_forced` | acmp_listener / pp_top AC | 93 of 2988 / 1 of 43 |
| `guard_ctlr_dropped` | acmp_listener | 50 of 2984 |
| `guard_talker_eid_dropped` | acmp_listener | 40 of 2984 |
| `guard_talker_uid_dropped` | acmp_listener | 30 of 2984 |
| `cdl_not_44_rejected` | rx_validator / pp_top AC | 27 of 495 / 19 of 43 |
| `st_ls_settle_as_withdraw`, `st_ls_sid_da_swapped`, `st_ls_state_none`, `st_ls_vid_dropped` | pp_top AC | 7 of 43 each |
| `st_ls_index_zero` | pp_top AC | 6 of 43 |
| `st_ls_teardown_as_declare`, `bound_view_not_cleared` | pp_top AC | 1 of 43 each |
| `st_ls_teardown_lost`, `bound_view_not_latched`, `bound_dmac_from_sid` | pp_top AC | 2 of 43 each |
| `matcher_da_ignored`, `matcher_vid_ignored` | pp_top AC | 5 of 43 each |

Parent consumer set: a scratch parent exported from milan-fpga dev `ec0cc0c1` (its index identical to the trusted checkout's, 977 entries), `gptp-processor` and `third_party/verilog-axis` at their recorded pins, `external` recorded and uninitialized as in the trusted checkout, and the `protocol-processor` gitlink staged at `616cbdf`, with the combined #132 + C1 adaptation and the item-2 line applied. Its only changes against dev `ec0cc0c1` are the gitlink and the 13 files of that adaptation plus the line, each byte-equal to a fresh apply; `scripts/test_evidence.budget` is untouched.

| # | Command | rc |
|---:|---|---:|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 |
| 2 | `python3 scripts/check_py_idiom.py` | 0 |
| 3 | `python3 scripts/xvlog_gate.py --check` | 0 (xvlog run: 4 findings == ratchet, pinned at `protocol-processor@616cbdf1`) |
| 4 | `python3 scripts/check_rtl_source_lists.py` | 0 |
| 5 | `python3 scripts/pp_srcs.py --check --selftest` | 0 |
| 6 | `python3 sw/builder/test_builder.py` | 0 (one calibration gate not run: its build tree is not on this host) |
| 7 | `make -C tb/verilator/pp_shadow -j8` | 0 (295 checks, 0 failures) |
| 8 | `python3 scripts/check_port_contracts.py` | 0 |
| 9 | `python3 scripts/measure_naming.py --check` | 0 |
| 10 | `python3 scripts/measure_test_evidence.py --check` | 0 (0 <= 0 unexplained DUT-source readers, 3 <= 3 wall-clock-dependent suite files) |
| 11 | `python3 scripts/docs_check.py` | 0 |
| 12 | `make -C tb/verilator/nvm_cosim lint` | 0 |
| 13 | `make -C tb/verilator/nvm_cosim quick` | 0 (315 of 315) |
| 14 | `make -C tb/verilator/milan_dp -j8` | 0 |
| 15 | `make -C tb/verilator/milan_dp_render -j8` | 0 |
| 16 | `python3 scripts/lint_rtl.py --check` | 0 (90 <= 90) |

16 of 16 are rc 0, one at a time, from clean build trees; command 10 is rc 0 again after the builds. The five failures round 1 attributed to #132 and #133 are gone with the combined adaptation. Before the revert, at `bf764ac`, the same set was 15 of 16: command 10 failed with "4 wall-clock-dependent suite file(s) > ratchet 3", which is what stopped the round (item 4 above).

### Parent-visible, for the pin-adoption lane

- **No interface or behaviour change.** No file under `hdl/` changes: no port, parameter, register or ROM. `KL_pp_shadow`, `milan_datapath` and every parent bench see the same RTL as at `b2db3a97`. The two documentation edits (00 F00.2's GAP-15 cell, 09 F09.4's row label) change no parent reference: the parent cites processor 00 and 09 only at a pinned older commit and for other rows (`docs/design/SAVED_STATE_MATERIALIZATION.md`).
- **One parent registry entry.** `protocol-processor/tb/pp_top/acmp_mutants.py` in `DUT_READER_DISPOSITIONS` of the parent's `scripts/measure_test_evidence.py`, with the item-2 line. The `protocol-processor/tb/pp_top/d3_mutants.py` entry from #132 is already in the combined adaptation.
- **No parent budget change.** With item 4 withdrawn, `scripts/test_evidence.budget` is untouched: the wall-clock ratchet stays at 3 <= 3, and the DUT-source reader ratchet is 0 <= 0 with the item-2 line.
- **Processor suite totals move.** `tb/acmp_listener` 2544 to 2988, `tb/rx_validator` 437 to 495, `tb/pp_top` 7888 to 7931 checks; the processor sweep is 1,016,817 checks. No parent file at dev `ec0cc0c1` quotes these counts.
- **Parent document that can cite the new grading at adoption:** `docs/reference/MILAN_COMPLIANCE_MATRIX.md` section 1.6, row "5.5.2 / 5.5.3" (evidence "PP acmp_listener + pp_top"). It can name §5.5.2.2's longer PDU (`tb/rx_validator` F29, `tb/pp_top` AL), §5.5.3.1's inert messages and the guard per term (`tb/acmp_listener` B13/B14, `tb/pp_top` AI), and the integrated settle path (`tb/pp_top` AS).

### What remains

- R411-1 S4 (a per-run timeout in `acmp_mutants.py`) is retained, not implemented, per the ruling on the STOP: a hang yields no tally and so can never count as KILLED, and the parent's wall-clock ratchet may only go down. The only cost of a hang is wall time.
- R411-1 S3: the bound stream identity survives an A8 teardown. It is pre-existing, port-visible behaviour, recorded by the manager on the residue checklist.
- Outside item 3's list and unchanged: 03 V3's "96-B IEEE form" names no edition; `hdl/acmp/KL_acmp_talker.sv:228,294` and 05 §3 (`acmpsta`) cite "IEEE Table 8-3", which is the 2021 numbering with no edition.
- No hardware was used. Bench evidence for #76 is unchanged by this lane (no RTL change).
