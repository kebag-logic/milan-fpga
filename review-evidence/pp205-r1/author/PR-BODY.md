[A687]

Closes #205

A GET_TX_STATE_COMMAND whose `talker_unique_id` names no valid source is answered TALKER_UNKNOWN_ID with the command's `listener_entity_id` and `listener_unique_id`, as Milan v1.2 5.5.4.3 step 1 and Table 5.46 give them. A successful GET_TX_STATE keeps Table 5.47's zeros. Before this change the talker never fetched the command's listener fields for GET_TX_STATE, and both of its arms took them from the compose block's zero defaults, so the refusal answered 0 and 0 (the observation on the release image at `ed211803`).

## Clauses

- Milan v1.2 5.5.4.3: "1) Extract the talker's source from the talker_unique_id field and check that it is valid. If not, send a GET_TX_STATE_RESPONSE message as shown in Table 5.46 and exit. 2) Send a GET_TX_STATE_RESPONSE message as shown in Table 5.47."
- Table 5.46 (talker_unique_id not valid): status TALKER_UNKNOWN_ID; `controller_entity_id`, `talker_entity_id`, `listener_entity_id`, `talker_unique_id`, `listener_unique_id` and `sequence_id` "Same value as in the GET_TX_STATE_COMMAND message"; `connection_count`, the three flags and the stream fields "Undefined".
- Table 5.47 (success): `listener_entity_id` 00:00:00:00:00:00:00:00 and `listener_unique_id` 0.
- IEEE 1722.1-2021 8.2.5.3, Figure 8-4 (ACMP Talker state machine), GET STATE: when `validTalkerUnique` is false, `response = rcvdCmdResp; error = TALKER_UNKNOWN_ID;`, and `txResponse` (8.2.5.2.3) "sets the ACMPDU fields to the values from the response parameter". The issue cites 8.2.4; in 1722.1-2021 that clause is the ACMP Listener state machine, whose `txResponse` (8.2.4.2.5) has the same wording. The talker's clause is 8.2.5.

## Change

`hdl/acmp/KL_acmp_talker.sv` (the issue's line numbers are those of `ed211803`; these are at the head):

| Line | Change | Clause |
|---|---|---|
| `:809` (the gate under the `:671` comment) | the RX-slot fetch (`needs_pdu_w`) also runs for GET_TX_STATE with an unknown `talker_unique_id`; a successful GET_TX_STATE still fetches nothing, so its latency is unchanged | Table 5.46 |
| `:1632-1637` (was `:1317-1319`) | the unknown-ID arm answers TALKER_UNKNOWN_ID with the fetched `pdu_leid_r` / `pdu_luid_r` | 5.5.4.3 step 1, Table 5.46 |
| `:1629-1631` | the success arm sets both listener fields to 0 itself instead of inheriting the defaults | Table 5.47 |
| `:1569-1572` (was `:1258`/`:1260`) | the defaults stay 0 as idle values; no response takes its listener fields from them any more | — |
| `:24-30`, `:800-804`, `:1553-1558` (were `:24`, `:671`, `:1246-1247`) | the design comments: a successful GET_TX_STATE zeroes the listener fields, every TALKER_UNKNOWN_ID response echoes them (Tables 5.40, 5.44, 5.46) | — |

No top-level port, parameter or register-map change. The flags and stream fields of the refusal, undefined in Table 5.46, are still answered 0. The top latches every talker response field unchanged and builds one 56-byte ACMPDU for every talker message (`hdl/top/protocol_processor_top.sv:3376-3379`, `:3399-3418`), so the wire carries what the talker's response port carries. The fetch adds the 13-clock RX-slot read to the refusal only; PROBE_TX, DISCONNECT_TX and GET_TX_CONNECTION already take it, so the talker's longest command path is unchanged.

## Tests

`tb/acmp_talker` (1,561 checks; 1,545 at main):

| Case | Contract |
|---|---|
| B2 | a successful GET_TX_STATE whose command carries listener fields `0x1111222233334444` / 7 answers them 0 (Table 5.47); tagged REQ-ACMP-008 |
| C2 | source 15, out of range, with listener fields `0xF1E2D3C4B5A69788` / `0x8C17`, every byte distinct: TALKER_UNKNOWN_ID, both fields echoed byte for byte, every other field checked; tagged REQ-ACMP-008 |
| H3 (new) | source 6, disabled: the same echo; tagged REQ-ACMP-008 |

On the talker RTL of main the new suite fails exactly the four listener-field checks of C2 and H3:

```
FAIL: C2 unknown-id listener_eid got 0000000000000000
FAIL: C2 unknown-id listener_uid got 0
FAIL: H3 disabled source GET_TX_STATE listener_eid got 0000000000000000
FAIL: H3 disabled source GET_TX_STATE listener_uid got 0
1561 checks: 1557 PASS, 4 FAIL
```

Mutant arms, `tb/pp_top/acmp_mutants.py` group `TX_STATE_ECHO`, each KILLED by its named checks:

| Mutant | Defect planted | Named checks, each failing | Failing checks |
|---|---|---|---|
| `tx_state_unknown_zeroes_listener` | the TALKER_UNKNOWN_ID answer zeroes the listener fields (the reported defect) | `C2 unknown-id listener_eid`, `C2 unknown-id listener_uid`, `H3 disabled source GET_TX_STATE listener_eid`, `H3 disabled source GET_TX_STATE listener_uid` | 4 |
| `tx_state_unknown_not_fetched` | the echo kept, the command's listener fields never fetched from the RX slot | the same four | 4 |
| `tx_state_success_echoes_listener` | every GET_TX_STATE fetched and its listener fields echoed, the SUCCESS answer included | `B2 listener_eid`, `B2 listener_uid` | 2 |

## Documents

- `docs/architecture/05_acmp_engine.md`: F05.11's GET_TX_STATE leaves (TALKER_UNKNOWN_ID echoes the listener fields, Table 5.46; SUCCESS zeroes them, Table 5.47) and a paragraph after the DISCONNECT_TX one.
- `docs/00_MILAN_COMPLIANCE_REVIEW.md`: REQ-ACMP-008 names Tables 5.46/5.47 and 1722.1-2021 8.2.5.3 and states both responses.
- `tb/acmp_talker/README.md`: the case list, the check count, the issue #205 section with the arms, and the talker retry campaign re-measure.
- `tb/pp_top/acmp_mutants.py`: the docstring names issue #205.

## Gates

Two commits: `c7250d65` (the change) and `7bad3943` (the talker README records measured at `c7250d65`; `git diff c7250d65 7bad3943` is that README only). Every gate below ran in a disposable clone at the simulator version CI pins; each return code is the command's own.

| Gate | Result |
|---|---|
| `scripts/lint_hdl.sh` | rc 0 at `c7250d65` |
| `REQ_TAG_LOG=… scripts/run_suites.sh` | rc 0 at `c7250d65`: `suites: 1030609 checks total, 0 failing`; against the #202 sweep at `b2b2bfd` (1,030,593) only `acmp_talker` moves, 1,545 → 1,561; `pp_top` 10,753 |
| `scripts/check-req-tags.py --suites … --evidence …` | rc 0: 249 tags ran, in 14 suites that passed (REQ-ACMP-008 now also from B2, C2 and H3) |
| `make check` | rc 0 at `c7250d65` and at `7bad3943` |
| `scripts/gen_matrix.py --check` | rc 0 at both |
| `make -C tb/acmp_talker run`, `lint` | rc 0 at `7bad3943`: `1561 checks: 1561 PASS, 0 FAIL`; lint clean |
| `make -C tb/pp_top` (all seven builds) | rc 0 in the sweep, `10753 checks: 10753 PASS, 0 FAIL` |
| `tb/pp_top/acmp_mutants.py` (the whole ACMP campaign) | rc 0 at `c7250d65`: **101 of 101 KILLED** by their named checks (98 before, plus the three above), the eight goldens PASS |
| `tb/acmp_talker/retry_mutants.py` (the talker retry campaign) | rc 0 at `c7250d65`: 62 killed, seven equivalent and one performance control; baseline and restored pass 1,561 checks. `no_command_ready` (771 → 782) and `no_get_tx_state_response` (133 → 144) fail more checks because H3 adds a GET_TX_STATE case; every other count is unchanged |
| the off-vendor elaboration of every top, and `tb/elab_guards/guards.py` | rc 0 at `c7250d65` |
| `make -C tb/nvm_port figures` | rc 0 at `c7250d65` |
| `git diff --check 097a7987 HEAD` | rc 0 |

## Parent consumer gate

A local scratch clone of milan-fpga dev `97aab1d0` (never pushed), with this head `7bad3943` as the `protocol-processor` gitlink and the #202 source-stream-ID wiring patch (sha256 `ff5068d2…1275`, 70,091 bytes, `git apply --check --index` clean on dev) applied. Its seventeen commands are those of the #202 consumer run, in its order:

| # | Command | Result |
|---|---|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | rc 0 |
| 2 | `python3 scripts/check_py_idiom.py` | rc 0 |
| 3 | `python3 scripts/xvlog_gate.py --check` | rc 0 |
| 4 | `python3 scripts/check_rtl_source_lists.py` | rc 0 |
| 5 | `python3 scripts/pp_srcs.py --check --selftest` | rc 0 |
| 6 | `python3 sw/builder/test_builder.py` | rc 0; the same one calibration arm not run as in the #202 run (its build report is not on the machine) |
| 7 | the `pp_shadow` suite (`make -j8`) | rc 0, 2,187 checks, 0 failures |
| 8 | `python3 scripts/check_port_contracts.py` | rc 0 |
| 9 | `python3 scripts/measure_naming.py --check` | rc 0 |
| 10 | `python3 scripts/measure_test_evidence.py --check` | rc 0 |
| 11 | `python3 scripts/docs_check.py` | rc 0 |
| 12 | `python3 scripts/lint_rtl.py --check` | rc 0 |
| 13 | the `nvm_cosim` lint target | rc 0 |
| 14 | the `nvm_cosim` quick target | rc 0, 315 checks, 0 failures |
| 15 | the `milan_dp` suite, every leg (`make -j8`) | rc 0, 13,685 checks, 0 failures |
| 16 | the `milan_dp_render` suite (`make -j8`) | rc 0, 347 checks, 0 failures (models built from scratch) |
| 17 | `python3 scripts/check_rtl_source_lists.py --selftest` | rc 0 |

The parent's own tally of legs 7, 14, 15 and 16 (`scripts/suite_tally.py`) is 16,534 checks, 0 failures, identical to the #202 consumer run. The parent's tracked tree was clean after the run.

## Not changed

No top-level port, parameter or register map; the talker's parameter and port list is byte-identical to main. No other module. `tb/pp_top` carries no TALKER_UNKNOWN_ID case for any talker command, before or after this change; the talker suite grades the response port, and the top passes it to the wire unchanged (above).
