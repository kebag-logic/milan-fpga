[A691c]

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
| `hdl/top/protocol_processor_top.sv:3578-3588` | while unsettled: selector 0 clears `0x52000000`, selector 2 answers 0, selector 4 `[63:16]` answers 0; selector 4's failure-code byte is still the SRP registrar's |
| `docs/architecture/06_aecp_engine.md` §6.2, F06.12, F06.13 | the GET_STREAM_INFO rows: the three fields and flags pass only while settled |
| `docs/architecture/02_interfaces.md` §4.4, `docs/guides/integrator.md` §8, `docs/00_MILAN_COMPLIANCE_REVIEW.md` REQ-AEM-010 | the same rule where the integrator's words are described |

While settled, selectors 0, 2 and 4 pass the integrator's words unchanged. All three still raise the external request and honour `gsi_wait_i`.

## Tests (`tb/pp_top`, section GI)

The harness integrator gains a mode for the new section. It answers selectors 2 and 4 from the published binding view and claims all three flags in every answer, so each response grades the processor's gate alone. Real BIND_RX, PROBE_TX_RESPONSE, ADP and UNBIND_RX frames drive sink 0. Each status change's unsolicited response and the solicited read are checked byte-exact and by name (the three flags, stream_id, stream_dest_mac, stream_vlan_id, pbsta/acmpsta). Premise checks read the binding view.

| Step | State | Expected |
|---|---|---|
| RESET | unbound | cleared, zero |
| PROBING, PROBING-SENT | bound and probing, before the first answer (after the bind's push and after its PROBE_TX) | cleared, zero |
| SETTLED | PROBING_COMPLETED | the integrator's flags, stream_id and MAC and the stored VLAN pass |
| REPROBE, REPROBE-SENT | T-ACMP-NOTK with no Talker registered and the talker discovered: probing again, the settled identity still published | cleared, zero |
| SETTLED-AGAIN | PROBING_COMPLETED | pass |
| PASSIVE-STALE | the talker departs (a settled sink only notes it), then T-ACMP-NOTK: PROBING_PASSIVE with the settled identity still published | cleared, zero |
| UNBOUND | after UNBIND_RX | cleared, zero |

The suite's shared expected-body helper now clears the three flags and zeroes stream_id and the destination MAC of every STREAM_INPUT body below PROBING_COMPLETED, so the existing GI, G and D3 expectations grade the same rule on the fixed integrator words.

## Negative controls (`tb/pp_top/gsi_mutants.py`)

The six arms live in `settled_gate_mutations()`, which `mutations()` splices in at the same place in the table. That way no function in the driver is over the parent's 100-line limit (`mutations()` is now exactly 100 lines), and the 29 arms stay identical, in the same order.

| Mutation | Required failing check |
|---|---|
| Selectors 0, 2 and 4 passed through while unsettled (the defect as reported) | `GI GATE PASSIVE-STALE solicited: stream_id sink 0 is zero` |
| Selector 0's three flags passed through | `GI GATE PASSIVE-STALE solicited: STREAM_ID_VALID, STREAM_DEST_MAC_VALID and STREAM_VLAN_ID_VALID clear` |
| Selector 2 passed through | `GI GATE PASSIVE-STALE solicited: stream_id sink 0 is zero` |
| Selector 4's destination MAC passed through | `GI GATE PASSIVE-STALE solicited: stream_dest_mac sink 0 is zero` |
| The gate closed while settled | `GI GATE SETTLED solicited: stream_id sink 0 is the settled stream's` |
| Settled read as bound | `GI GATE PROBING solicited: STREAM_ID_VALID, STREAM_DEST_MAC_VALID and STREAM_VLAN_ID_VALID clear` |

The first arm fails 32 `GI GATE` checks, in every unsettled step.

## Gates

Run on clean clones; every result is the command's own exit status. The branch has two commits. The second, `e9272b5`, changes only `tb/pp_top/gsi_mutants.py` (the split above). No RTL, test bench build or check reads that file, and the processor's sweep and CI do not run it. The pp_top README gives its command line, which is unchanged. The gates that do read it were re-run at `e9272b5`: the driver, `make check`, and the parent's Python and C++ idiom gates with their neighbours. The other rows are from the first commit, `9abb41f`, which has the same RTL, tests and docs.

| Gate | Result |
|---|---|
| `bash scripts/run_suites.sh` (full sweep, with the requirement-tag evidence) | rc 0; 1,030,712 checks, 0 failing; pp_top 10,872 (+119, section GI's new steps) |
| `python3 scripts/check-req-tags.py --suites <sweep log> --evidence <evidence>` | rc 0; 247 tags, each with evidence |
| `python3 tb/pp_top/gsi_mutants.py --output <dir> --jobs 3` (at `e9272b5`) | rc 0; 29 of 29 arms killed by their named checks, the six above included; golden and restored PASS |
| `python3 tb/pp_top/acmp_mutants.py --only gsi_vlan_external parent_vlan_shifted stored_vlan_truncated retry_probe_status_cleared` (the arms planted on the selector 6 line this change rewrote) | rc 0; 5 of 5 killed |
| `make check` (at `e9272b5`) | rc 0 |
| `bash scripts/lint_hdl.sh` | rc 0 |
| `make -C tb/pp_top gsi-internal` at the base | rc 0; 6,254 checks (6,373 at this head) |
| this head's tests on the base RTL | fail: 82 FAIL lines, 32 of them `GI GATE`, the same lines as the first arm |

## Consumer gate

milan-fpga dev `97aab1d0` with the #202 source-stream-ID wiring patch (sha256 `ff5068d2…1275`) applied and this branch as the `protocol-processor` gitlink, in a local scratch clone. ROM digests were recorded for each pin with `./syn/yosys/ooc.sh --record-rom-digests`: the same contents as the `ed211803` rows at both `9abb41f` and `e9272b5`. The idiom rows ran with `e9272b5` as the gitlink. The other rows ran with `9abb41f`. In the parent, only the static scanners read the file: they walk all first-party Python, and `scripts/measure_test_evidence_readers.py` names it in its registry. Those scanners were re-run with `e9272b5`.

| Gate | Result |
|---|---|
| `python3 scripts/check_py_idiom.py` and `--selftest` (gitlink `e9272b5`) | rc 0: `long function: 9 <= 9`. With `9abb41f` as the gitlink it failed (`long function 10 > ratchet 9`), and `--list` blamed `protocol-processor/tb/pp_top/gsi_mutants.py` |
| `python3 scripts/check_cpp_idiom.py` and `--selftest` (gitlink `e9272b5`) | rc 0 |
| `python3 scripts/measure_test_evidence.py --check` and `--selftest`, `python3 scripts/check_hygiene.py --check` and `--selftest`, `python3 scripts/measure_fail_fast.py --check` and `--selftest`, `python3 scripts/check_todo_ownership.py` and `--selftest`, `python3 scripts/check_doc_paths.py`, `python3 scripts/measure_naming.py --check` and `--selftest` (the other CI gates that scan every first-party file; gitlink `e9272b5`) | all rc 0 |
| lint (`scripts/lint_rtl.py --check --self-test`), port contracts, wire accountability, SV idiom, RTL source lists, behave, yosys elaboration of `milan_datapath`, `KL_pp_shadow` and `KL_gptp_shadow`, the parser gate | all rc 0 |
| the full default Verilator sweep (`scripts/run_all_suites.sh --shard k/4`; `capture_coherence` in its CI piece form with the piece union) and `scripts/suite_tally.py --expect-suite-root tb/verilator` over all of it | every shard and piece rc 0; tally rc 0: 64 suites, each exactly once, 2,190,635 checks, 0 failures |
| `milan_dp` / `pp_shadow` / `maap` / `milan_dp_render` / `capture_coherence` | 13,685 / 2,187 / 251 / 347 checks / 43 cases: the same counts as the #202 consumer gate |
| `make -C tb/verilator/milan_dp notify` (the `[GSI]` section), at the base pin and at this head | rc 0 both; 461 checks, 0 failures both; the 234 `[GSI]` lines identical |
| `make -C tb/verilator/milan_dp gsi-mutants` | rc 0; 11 of 11 mutants caught by their named checks; clean control PASS |
| `./syn/yosys/ooc.sh KL_pp_shadow` | rc 0; 61,883 LUT, 4,332 LUTRAM, 28,346 FF, 15 RAMB36, 4 RAMB18, 10 DSP, 2,428 CARRY4. At the base pin: 61,219 LUT, 28,334 FF, the rest equal. This change costs 664 LUT (1.1%) and 12 FF |

## For the parent adoption (milan-fpga #790)

- milan_datapath may keep its `bound && sid != 0` rule: at this pin the processor clears what that rule over-reports. Its ledger line on "settled" can now point at the processor's gate.
- The four `[GSI]` cases in `milan_dp` and `pp_shadow`, and a `gsi_mutants.py` arm that restores the pass-through in the processor copy, land with the pin adoption. The processor text that arm needs is the line `      if (!gsi_settled_w) begin`.
- The ROM images are unchanged: the digests at `e9272b5` equal the `ed211803` rows.
