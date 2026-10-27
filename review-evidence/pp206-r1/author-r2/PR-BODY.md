[A691d]

Closes #206

GET_STREAM_INFO on a Stream Input now reports stream_id, stream_dest_mac and stream_vlan_id, and STREAM_ID_VALID, STREAM_DEST_MAC_VALID and STREAM_VLAN_ID_VALID, only while the input is settled. Settled is the committed probing status PROBING_COMPLETED, the value the same response carries in its pbsta field. Before this change a bound sink back in PROBING_PASSIVE answered with the three flags set and the stream it was last settled on.

## Clauses

- Milan v1.2 5.4.2.10.1, Table 5.9: STREAM_ID_VALID (`0x40000000`), STREAM_DEST_MAC_VALID (`0x10000000`) and STREAM_VLAN_ID_VALID (`0x02000000`): each field "shall contain valid information if, and only if, the Stream Input is settled".
- Milan v1.2 5.3.8.5: a bound Stream Input is either probing or settled. 5.3.8.6, Table 5.5: PROBING_COMPLETED (3) is "not probing because it is settled".
- IEEE 1722.1-2021 7.4.16.2: the flags field indicates "all fields that currently have valid values".

## Cause

The intercept in `protocol_processor_top.sv` already gated selector 6's stream_vlan_id on `pbsta == PB_COMPLETED_C`. Selectors 0 and 2, and selector 4's destination MAC bits, passed the integrator's word through. An integrator that folds the published binding view cannot tell settled from probing: `acmp_bound_sid_o` and `acmp_bound_dmac_o` are latched at the A15 settle and cleared only at unbind, so after a T-ACMP-NOTK teardown they still name the old stream.

## Change

No top-level port, parameter or register-map change.

| File:line | Change |
|---|---|
| `hdl/top/protocol_processor_top.sv:3532`, `:3554-3564` | `gsi_settled_w`: an in-range index whose committed status is PROBING_COMPLETED, the test selector 6 used inline |
| `hdl/top/protocol_processor_top.sv:3573-3574` | selector 6 reads the same wire; its behaviour is unchanged |
| `hdl/top/protocol_processor_top.sv:3578-3588` | while unsettled: selector 0 clears `0x52000000` and nothing else, selector 2 answers 0, selector 4 `[63:16]` answers 0; selector 4's failure-code byte is still the SRP registrar's |
| `docs/architecture/06_aecp_engine.md` §6.2, F06.12, F06.13 | the GET_STREAM_INFO rows: the three fields and flags pass only while settled |
| `docs/architecture/02_interfaces.md` §4.4, `docs/guides/integrator.md` §8, `docs/00_MILAN_COMPLIANCE_REVIEW.md` REQ-AEM-010 | the same rule where the integrator's words are described |

While settled, selectors 0, 2 and 4 pass the integrator's words unchanged. All three still raise the external request and honour `gsi_wait_i`.

## Tests (`tb/pp_top`, section GI)

The harness integrator gains a mode for the new section. It answers selectors 2 and 4 from the published binding view. It also claims every flag in every STREAM_INPUT flags word (`H::GSI_FOLD_FLAGS`): the three Table 5.9 flags and every integrator-owned flag besides, BOUND, MSRP_ACC_LAT_VALID and MSRP_FAILURE_VALID among them. Each response therefore grades the processor's gate alone, and a gate that clears more than `0x52000000` fails a named check. Real BIND_RX, PROBE_TX_RESPONSE, ADP and UNBIND_RX frames drive sink 0. Each status change's unsolicited response and the solicited read are checked byte-exact and by name: the three flags, every other claimed flag, stream_id, stream_dest_mac, stream_vlan_id, and pbsta/acmpsta. Premise checks read the binding view at RESET, PROBING, SETTLED, REPROBE, PASSIVE-STALE and UNBOUND.

| Step | State | Expected |
|---|---|---|
| RESET | unbound | the three cleared and zero, every other flag passes |
| PROBING, PROBING-SENT | bound and probing, before the first answer (after the bind's push and after its PROBE_TX) | the same |
| SETTLED | PROBING_COMPLETED | every claimed flag, stream_id and MAC, and the stored VLAN pass |
| REPROBE, REPROBE-SENT | T-ACMP-NOTK with no Talker registered and the talker discovered: probing again, the settled identity still published | the three cleared and zero, every other flag passes |
| SETTLED-AGAIN | PROBING_COMPLETED | everything passes |
| PASSIVE-STALE | the talker departs (a settled sink only notes it), then T-ACMP-NOTK: PROBING_PASSIVE with the settled identity still published | the three cleared and zero, every other flag passes |
| UNBOUND | after UNBIND_RX | the same |

The suite's shared expected-body helper clears the three flags and zeroes stream_id and the destination MAC of every STREAM_INPUT body below PROBING_COMPLETED. The existing GI, G and D3 expectations therefore grade the same rule on the fixed integrator words.

Selector 4's failure-code byte stays the SRP registrar's while unsettled, but no reachable unsettled state has a non-zero code, so no step can grade one. SRP reports a code only while the sink's matcher is armed and a Talker Failed is registered (`KL_srp_listener_fsm.sv:1268-1275`). The matcher is armed by the A15 settle, the only writer of PROBING_COMPLETED (`KL_pp_acmp_listener.sv:1311-1313`), and disarmed by the A8 teardown (`:1204`). Every F05.3 arc out of SNR or SOK carries A8: BIND_NEW, UNBIND, TMR_NOTK and TK_UNREG (`hdl/acmp/rom/gen_ltn_rom.py:48-64`, `:83`, `:97`; Milan Table 5.30). A8 runs before the arc's pbsta write in the canonical action order. REPROBE and PASSIVE-STALE keep the old stream published in the binding view, but SRP's matcher is already disarmed there.

## Negative controls (`tb/pp_top/gsi_mutants.py`)

The seven arms live in `settled_gate_mutations()` (38 lines), which `mutations()` (100 lines) splices in at the same place in the table.

| Mutation | Required failing check |
|---|---|
| Selectors 0, 2 and 4 passed through while unsettled (the defect as reported) | `GI GATE PASSIVE-STALE solicited: stream_id sink 0 is zero` |
| Selector 0's three flags passed through | `GI GATE PASSIVE-STALE solicited: STREAM_ID_VALID, STREAM_DEST_MAC_VALID and STREAM_VLAN_ID_VALID clear` |
| Selector 2 passed through | `GI GATE PASSIVE-STALE solicited: stream_id sink 0 is zero` |
| Selector 4's destination MAC passed through | `GI GATE PASSIVE-STALE solicited: stream_dest_mac sink 0 is zero` |
| The gate closed while settled | `GI GATE SETTLED solicited: stream_id sink 0 is the settled stream's` |
| Settled read as bound | `GI GATE PROBING solicited: STREAM_ID_VALID, STREAM_DEST_MAC_VALID and STREAM_VLAN_ID_VALID clear` |
| Selector 0's mask also clears BOUND (`~0x56000000`) | `GI GATE RESET solicited: every other flag the integrator claims passes for sink 0` |

The first arm fails 32 `GI GATE` checks, in every unsettled step. The last fails 22, the other-flags check and byte-exact at every unsettled response. Masks that also clear MSRP_ACC_LAT_VALID (`~0x72000000`) or BOUND (`~0x56000000`), planted independently, fail the same 22 named checks.

## Review round 2

- R724-1-F1: the harness integrator claims every flag; the expected bodies keep every other flag settled and unsettled; a new named check per graded response; the BOUND arm above.
- R724-1-S1: no step is possible, for the reason given under Tests.
- R724-1-W1: the README's premise sentence names the six steps that read the binding view.
- R723-1-RES-01: the 133-column line in `06_aecp_engine.md`'s ownership paragraph is broken after "owners." and the paragraph's tail rewrapped; its words are unchanged.

## Gates

Run on clean clones at this head; every result is the command's own exit status. The branch has four commits. The last two, the round-2 commits, change only `tb/pp_top` test files, the pp_top README and one docs paragraph, and no `hdl/` file. Rows marked "first commit" are carried from `9abb41f`, which has the same RTL.

| Gate | Result |
|---|---|
| `make -C tb/pp_top run` | rc 0; 10,887 checks, 0 failures (10,872 + 15, the new check on each graded response; GI 6,388) |
| `python3 tb/pp_top/gsi_mutants.py --output <dir> --jobs 3` | rc 0; 30 of 30 arms killed by their named checks, the seven above included; golden and restored PASS. The 29 earlier arms fail with the same named lines as before |
| `make check` | rc 0 |
| this head's tests on the base RTL | fail: 82 FAIL lines, 32 of them `GI GATE`, the same lines as the first arm |
| `bash scripts/run_suites.sh` (full sweep, with the requirement-tag evidence; first commit) | rc 0; 1,030,712 checks, 0 failing |
| `python3 scripts/check-req-tags.py --suites <sweep log> --evidence <evidence>` (first commit) | rc 0; 247 tags, each with evidence |
| `python3 tb/pp_top/acmp_mutants.py --only gsi_vlan_external parent_vlan_shifted stored_vlan_truncated retry_probe_status_cleared` (first commit) | rc 0; 5 of 5 killed |
| `bash scripts/lint_hdl.sh` (first commit) | rc 0 |

## Consumer gate

milan-fpga dev `97aab1d0` with the #202 source-stream-ID wiring patch (sha256 `ff5068d2…1275`) applied and this branch as the `protocol-processor` gitlink, in a local scratch clone. The ROM images are unchanged: no `hdl/` file changed after `9abb41f`, whose digests equal the `ed211803` rows.

| Gate | Result |
|---|---|
| `python3 scripts/check_py_idiom.py`, `--selftest` and `--list` (gitlink at this head) | rc 0: `long function: 9 <= 9` |
| `python3 scripts/check_cpp_idiom.py` and `--selftest` (gitlink at this head) | rc 0 |
| `python3 scripts/measure_test_evidence.py --check` and `--selftest`, `python3 scripts/check_hygiene.py --check` and `--selftest`, `python3 scripts/measure_fail_fast.py --check` and `--selftest`, `python3 scripts/check_todo_ownership.py` and `--selftest`, `python3 scripts/check_doc_paths.py`, `python3 scripts/measure_naming.py --check` and `--selftest` (gitlink at this head) | all rc 0 |
| lint (`scripts/lint_rtl.py --check --self-test`), port contracts, wire accountability, SV idiom, RTL source lists, behave, yosys elaboration of `milan_datapath`, `KL_pp_shadow` and `KL_gptp_shadow`, the parser gate (first commit) | all rc 0 |
| the full default Verilator sweep (`scripts/run_all_suites.sh --shard k/4`; `capture_coherence` in its CI piece form) and `scripts/suite_tally.py --expect-suite-root tb/verilator` (first commit) | every shard and piece rc 0; tally rc 0: 64 suites, each exactly once, 2,190,635 checks, 0 failures |
| `make -C tb/verilator/milan_dp notify` (the `[GSI]` section), at the base pin and at the first commit | rc 0 both; 461 checks, 0 failures both; the 234 `[GSI]` lines identical |
| `make -C tb/verilator/milan_dp gsi-mutants` (first commit) | rc 0; 11 of 11 mutants caught by their named checks; clean control PASS |
| `./syn/yosys/ooc.sh KL_pp_shadow` (first commit) | rc 0; 61,883 LUT, 28,346 FF. At the base pin: 61,219 LUT, 28,334 FF. This change costs 664 LUT (1.1%) and 12 FF |

## For the parent adoption (milan-fpga #790)

- milan_datapath may keep its `bound && sid != 0` rule: at this pin the processor clears what that rule over-reports. Its ledger line on "settled" can now point at the processor's gate.
- The four `[GSI]` cases in `milan_dp` and `pp_shadow`, and a `gsi_mutants.py` arm that restores the pass-through in the processor copy, land with the pin adoption. The processor text that arm needs is the line `      if (!gsi_settled_w) begin`.
