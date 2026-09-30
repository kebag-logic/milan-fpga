[A450]

Closes #45
Closes #47
Closes #48

Lane C4 of the PP program: ACMP (assignment: #45 comment 5891906554). Branch `c4-acmp-coverage` from `main` `b2db3a97`, one or more commits per item, in the assignment's order:

| Commit | Item |
|---|---|
| `d87b3d5` | 1. #47: ACMP messages outside the listener set are inert, the probe-response guard per term, the `tb/pp_top` leg, the mutation driver |
| `2a3e608` | 2. #45: the 96-byte IEEE ACMPDU in `tb/rx_validator` and `tb/pp_top`, and the cdl != 44 rejection mutant |
| `af6a5f1` | 3. #48: the integrated settle path to SRP listen in `tb/pp_top`, and the `st_ls_r` glue, bound-view and matcher mutants |
| `20e24d4` | the mutation tables remeasured at the lane head |
| `a7ccd9e` | the parent C++ idiom gate (Rule 11) on the new test code: one array initializer split across lines |
| `a9ce0fa` | item 3 tightened: AS6's quiet window counts every ACMP frame, not only the next probe |

**Tests, one mutation driver and suite records only.** No new test exposed an RTL defect, so no RTL changed: `git diff b2db3a97..a9ce0fa -- hdl docs` is empty, and no port, parameter or register of `protocol_processor_top` changes. The one non-suite source touched is the `tb/pp_top` wrap, which now connects the top's existing `acmp_bound_eid_o`, `acmp_bound_sid_o`, `acmp_bound_dmac_o` and `acmp_bound_vlan_o` for item 3.

The top-level legs run as a new section AC of `tb/pp_top` on a fresh model (as MP and DV do), so the main DUT's tuned timeline does not move. `./obj_dir/Vpp_top_sim --acmp-only` (after `make gsi-build`) runs it alone. Sink 1 is bound throughout, never sink 0, so a stage that loses the sink index cannot pass by accident.

## 1. #47: messages outside the listener and talker sets are inert (REQ-ACMP-012)

**Clause.** Milan v1.2 §5.5.3.1 gives the listener BIND_RX, GET_RX_STATE and UNBIND_RX commands with its own listener_entity_id; §5.5.3.5.18 step 1 (PRB_W_RESP), which §5.5.3.5.25 applies unchanged in PRB_W_RESP2 ("same treatment"), ignores a PROBE_TX_RESPONSE that does not match the saved command's controller_entity_id, talker_entity_id, talker_unique_id and sequence_id. IEEE 1722.1-2021 Table 8-2 supplies the codes: 3, 5, 7, 9, 11 and 13 are responses other than PROBE_TX_RESPONSE (CONNECT_TX_RESPONSE), and 14 to 15 are reserved.

**Acceptance.**
1. `tb/acmp_listener` **B13** drives message types 3, 5, 7, 9, 11, 13, 14 and 15 with the own listener_entity_id and a valid listener_unique_id, in PRB_W_RESP (status SUCCESS) and PRB_W_RESP2 (TALKER_NO_BANDWIDTH). Each is shaped as the perfect answer to the outstanding probe (all four guard terms equal, stream fields set), so only its type keeps it out. Each is fully inert: no frame, no record write, no timer op, no action strobe, no notify, the record unchanged, and exactly one RX-slot free of the slot it arrived in.
2. `tb/acmp_listener` **B14** grades the guard term by term: a response with the wrong controller_entity_id, talker_entity_id or talker_unique_id is ignored in both probing states, as B8's wrong sequence_id already was. The unaltered response then settles, so a guard that rejected everything would fail.
3. `tb/pp_top` **AI1-AI3**: a BIND_RX_RESPONSE (7) and a reserved type (14), shaped as the answer to probe #1, reach the listener through the real steer. Neither raises an ACMP frame, neither is dropped at the front end, all four RX slots are free and no scoreboard hold is left. The exact duplicate probe then follows at T-ACMP-CMD, which proves the sink never left PRB_W_RESP.
4. **Mutation.** `txn_msg_ok_w` forced to 1 fails 93 of 2988 `tb/acmp_listener` checks (all 16 B13 arms settle or back off) and `tb/pp_top` AI3. Each guard term tied true fails its B14 arms: controller_entity_id 50, talker_entity_id 40, talker_unique_id 30 of 2984. All are recorded in `tb/acmp_listener/README.md` and `tb/pp_top/README.md`.

## 2. #45: ACMPDUs longer than 56 bytes are accepted (REQ-ACMP-001)

**Clause.** Milan v1.2 §5.5.2.2: a Milan device "shall send and accept this truncated PDU, and may accept the longer PDU". The architecture takes that option (03 V3, the F09.4 96-B row). IEEE 1722.1-2021 §8.2.1.6 sets control_data_length to 84 for the 96-byte form of Figure 8-1 (ip_flags, reserved, source_port, destination_port and two 128-bit IP addresses after connected_listeners_entries @54).

**Acceptance.**
1. `tb/rx_validator` **F29** drives the 96-byte form, cdl 84, with its 40-byte IP tail filled with a pattern, as a BIND_RX and as a PROBE_TX. Each is committed, no counter moves (rx_length above all), and the slot holds all cdl + 12 = 96 bytes. The header beat is field-exact against the offset model and equal to the truncated form's but for cdl, including the listener or talker unique_id.
2. `tb/pp_top` **AL1-AL4**: a 96-B UNBIND_RX is answered by the 56-B cdl-44 UNBIND_RX_RESPONSE. A 96-B BIND_RX gets the same response as AI1's 56-B BIND_RX, byte for byte, and the PROBE_TX regenerated from its record is byte-exact, so the long command's fields reached the binding and not only the echo. A PROBE_TX to our talker gets one byte-exact answer for the 56-B and the 96-B form (TALKER_DEST_MAC_FAILED: no allocator is wired on that model, as S10 (c) grades on the main DUT). There are no front-end drops and no slot leak.
3. **Mutation.** A validator that accepts ACMP only at cdl 44 fails 27 of 495 `tb/rx_validator` checks (F29 both forms, and F4's cdl-24 short form too) and 19 of 42 in section AC (AL1-AL4, then the legs that need the long BIND_RX's binding). It is recorded in `tb/rx_validator/README.md` (M5) and `tb/pp_top/README.md`.

## 3. #48: the settle path to SRP listen, end to end (REQ-ACMP-016)

**Clause.** Milan v1.2 §5.5.3.5.18 step 4: on a matching PROBE_TX_RESPONSE SUCCESS, note stream_id, stream_dest_mac and stream_vlan_id, initiate SRP reservation, start TMR_NO_TK (10 s), go to SETTLED_NO_RSV. §5.3.8.9: the recorded values are exactly the last response's, and a divergent talker attribute is ignored. §5.3.8.5: with a matching Talker Advertise registered, the sink declares Listener Ready. §5.5.3.5.42: EVT_TK_REGISTERED clears TMR_NO_TK and goes to SETTLED_RSV_OK. §5.5.3.5.36: TMR_NO_TK in SETTLED_NO_RSV tears SRP down. §5.5.3.5.45: UNBIND_RX in SETTLED_RSV_OK stops SRP and clears the binding. Tables 5.37 to 5.39 give the GET_RX_STATE forms. IEEE 802.1Q-2018 §35.2.2.7.2 gives the Listener FourPackedType.

**Path under test.** The listener's A15 reaches the SRP listener matcher only through the top's service stage (`st_ls_r`: DECLARE_LISTENER, op 2, state READY, the sink index, stream_id, DA and VID), and returns as TK_ATTR_REGISTERED through the event router.

**Acceptance** (`tb/pp_top` AS1-AS6, about 19 s of simulated time on the phase's own model).
1. **AS1-AS2.** PROBE_TX #2 goes unanswered: its exact duplicate follows, T-ACMP-RETRY finds no talker and re-probes nothing, and GET_RX_STATE answers the probing form (Table 5.37). The talker's ENTITY_AVAILABLE drives discovery and T-ACMP-DELAY to PROBE_TX #3, byte-exact, which the bench answers with a PROBE_TX_RESPONSE SUCCESS. After that, `acmp_bound_o`/`eid`/`sid`/`dmac`/`vlan_o[1]` carry exactly the response's stream, every other sink's view stays clear, and GET_RX_STATE answers the settled form (Table 5.38) byte-exact.
2. **AS3-AS5.** Near misses on the DA, the VLAN and the stream_id put no Listener vector on the wire, register nothing on the class-D face and route no TK_ATTR_REGISTERED{1}. The matching Talker Advertise then yields Listener Ready New byte-exact (alone in its MRPDU), class-D READY and ADVERTISE for sink 1, exactly one TK_ATTR_REGISTERED{1}, and GET_RX_STATE in Table 5.39's form. Table 5.39's bytes equal Table 5.38's while the registered attribute is an Advertise, so the state itself is graded too: 11.5 s after the settle, with the bench re-joining its Advertise every second, there is no re-probe and no Lv, and the declaration, the GET_RX_STATE stream fields and the bound view all hold. A sink left in SETTLED_NO_RSV cannot do that past T-ACMP-NOTK.
3. **AS6.** UNBIND_RX from SETTLED_RSV_OK: the response is byte-exact, and the Listener attribute is withdrawn on the wire (Lv, FourPackedType Ready) byte-exact. The bound view clears, no declaration or match is held, GET_RX_STATE answers the unbound form byte-exact, nothing probes the sink afterwards, and no RX slot or scoreboard hold is left.
4. **Mutation** (failing checks of 42, all KILLED, recorded in `tb/pp_top/README.md`). In `st_ls_r`: settle issued as WITHDRAW 7, teardown issued as DECLARE 1, stream_id/DA swapped 7, state NONE 7, VID dropped 7, sink index 0 6 (the wire frame is identical there, so only the per-sink faces and the state show it), teardown strobe lost 2. The bound view: latch removed 2, DA latched from the stream_id 2, not cleared on unbind 1. The SRP listener matcher ignoring the DA or the VLAN fails the three AS3 near-miss checks (5 each).

## 4. Parent-visible, for the pin-adoption lane

- **No interface or behaviour change.** No file under `hdl/` or `docs/` changes: no port, parameter, register or ROM. `KL_pp_shadow`, `milan_datapath` and every parent bench see the same RTL as at `b2db3a97`.
- **One parent registry entry.** The new mutation driver `protocol-processor/tb/pp_top/acmp_mutants.py` reads and rewrites DUT sources in its private copies, so the parent's `scripts/measure_test_evidence.py --check` counts it as an unexplained DUT-source reader until `DUT_READER_DISPOSITIONS` records it. Suggested text: "mutation campaign; it plants one ACMP listener, validator, top SRP-service or SRP matcher defect from its own table into an isolated copy and requires the named checks to fail; no expected value is read from RTL". The same gate already needs an entry for `protocol-processor/tb/pp_top/d3_mutants.py` from merged PR #132. With both entries (scratch only) the gate is rc 0 at the head.
- **Processor suite totals move.** `tb/acmp_listener` 2544 to 2988, `tb/rx_validator` 437 to 495, `tb/pp_top` 7888 to 7930 checks; the processor sweep is 1,016,816 checks. No parent file at dev `79c36963` quotes these counts.
- **Parent document that can cite the new grading at adoption:** `docs/reference/MILAN_COMPLIANCE_MATRIX.md` section 1.6, row "5.5.2 / 5.5.3" (evidence "PP acmp_listener + pp_top"). It can name §5.5.2.2's longer PDU (`tb/rx_validator` F29, `tb/pp_top` AL), §5.5.3.1's inert messages and the guard per term (`tb/acmp_listener` B13/B14, `tb/pp_top` AI), and the integrated settle path (`tb/pp_top` AS).

## Validation

Verilator 5.052, make capped at eight jobs.

Processor, at `a9ce0fa`:

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, 1,016,816 checks, 0 failing (acmp_listener 2988, rx_validator 495, pp_top 7930) |
| `./scripts/lint_hdl.sh` | 0 | 41 modules |
| `make check` | 0 | lint, WaveDrom, links, both matrices, parameters, stale |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `python3 tb/pp_top/acmp_mutants.py` | 0 | 19 of 19 KILLED by their named checks (14 `tb/pp_top`, 4 `tb/acmp_listener`, 1 `tb/rx_validator`); three goldens PASS |
| `python3 tb/pp_top/gsi_mutants.py` | 0 | 20 detected; golden and restored PASS (it builds this lane's `tb/pp_top`) |
| `python3 tb/pp_top/name_wr_mutant.py` | 0 | killed; golden and restored PASS |
| `python3 tb/pp_top/d3_mutants.py` | 0 | 83 of 83 KILLED; goldens of `tb/acmp_nvm`, `tb/pp_top` and `tb/rx_validator` PASS (it builds this lane's `tb/pp_top` and `tb/rx_validator`) |
| `git diff --check b2db3a97..a9ce0fa` | 0 | |

Not re-run: `make -C tb/srp_top mutants`, `make -C tb/nvm_port figures`, `./syn/yosys/run.sh`, `tb/srp_admission/mutants.py` and `tb/acmp_talker/retry_mutants.py`, whose inputs (`hdl/` and their own suite directories) this lane does not touch.

Parent consumer set (the manager's sixteen commands) in scratch parents exported from milan-fpga dev `79c36963`. Every regular file is identical to the trusted index; `third_party/verilog-axis` and `gptp-processor` are at their recorded pins, `external` is recorded and uninitialized as in the trusted checkout, and the `protocol-processor` gitlink is staged at the lane head `a9ce0fa`. Two control columns use the same export: the gitlink at the lane base `b2db3a97` (processor `main`), and, for every command that fails there, at the parent's own pin `c951a9ff`.

| Command | head `a9ce0fa` | base `b2db3a97` | pin `c951a9ff` |
|---|---:|---:|---:|
| `python3 scripts/check_cpp_idiom.py` | 0 | 0 | |
| `python3 scripts/check_py_idiom.py` | 0 | 0 | |
| `python3 scripts/xvlog_gate.py --check` | 0 | 0 | |
| `python3 scripts/check_rtl_source_lists.py` | 0 | 0 | |
| `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0 | |
| `python3 sw/builder/test_builder.py` | 0 | 0 | |
| `make -C tb/verilator/pp_shadow -j8` | 2 | 2 | 0 |
| `python3 scripts/check_port_contracts.py` | 0 | 0 | |
| `python3 scripts/measure_naming.py --check` | 0 | 0 | |
| `python3 scripts/measure_test_evidence.py --check` | 1 | 1 | 0 |
| `python3 scripts/docs_check.py` | 0 | 0 | |
| `make -C tb/verilator/nvm_cosim lint` | 0 | 0 | 0 |
| `make -C tb/verilator/nvm_cosim quick` | 2 | 2 | 0 |
| `make -C tb/verilator/milan_dp -j8` | 2 | 2 | 0 |
| `make -C tb/verilator/milan_dp_render -j8` | 2 | 2 | 0 |
| `python3 scripts/lint_rtl.py --check` | 1 | 1 | 0 |

**Attribution.** Every failure at the head fails identically at the lane base. The sorted failure and warning lines of `pp_shadow`, both `nvm_cosim` targets, `milan_dp` and `milan_dp_render` hash equal, and the `lint_rtl` output is byte-identical. Every one of them passes at the parent's pin, so they come from the two processor PRs merged to `main` after that pin, #132 and #133, whose parent adoption is pending:
- `KL_pp_shadow` leaves #132's new top outputs (`restore_cause_o`, `d3_unflushed_o`, `restore_closed_o`, `restore_rb_o`, `rs_cause_o`) unconnected: PINMISSING, which is fatal in `pp_shadow` and one over the `hdl/milan` ratchet in `lint_rtl`.
- `nvm_cosim` quick fails 7 of 315, and its harness (`cosim_top.sv`) leaves #132's new `rs_agg_i` and `wr_chg_o` pins unconnected (PINMISSING in its lint output).
- `measure_test_evidence` at the base counts #132's `d3_mutants.py`.
- `milan_dp` and `milan_dp_render` fail the same legs at the base as at the head.
- #133's own PR body names a `milan_dp` `obj_crflic` re-base.
- This lane did not attribute each `milan_dp` leg to #132 or #133.

The head adds exactly one finding, `acmp_mutants.py` in `measure_test_evidence` (section 4), and removes none. `check_cpp_idiom` failed once on this lane's new test code (a one-line array initializer read as a multi-declarator, Rule 11) and passes since `a7ccd9e`. Every command above was also run with the gitlink at `a7ccd9e`, with the same verdicts.

## What remains

- No hardware was used. Bench evidence for #76 is unchanged by this lane (no RTL change).
- The disposition table of `docs/00_MILAN_COMPLIANCE_REVIEW.md` (F00.2) still names #45 as GAP-15's open residue. With #45 closed, it reads "none found" per that table's own rule; this lane left the document untouched.
- Noted from the top's source, not graded and not changed: the top's `acmp_bound_sid_o`, `acmp_bound_dmac_o` and `acmp_bound_vlan_o` are latched at A15 and cleared only with the binding (A9), as their port comment says. After an A8 teardown without an unbind (T-ACMP-NOTK in SETTLED_NO_RSV, EVT_TK_UNREGISTERED in SETTLED_RSV_OK), they keep the last settled stream until the next settle, while GET_RX_STATE reports zeros (Milan §5.3.8.9). Section AC asserts neither way. Changing it would be a class-D behaviour change for the parent, so it needs its own decision.
- The parent consumer set cannot be green at dev `79c36963` with any processor head past `c951a9ff` until #132 and #133 are adopted. The table above is the attribution, not a pass.
