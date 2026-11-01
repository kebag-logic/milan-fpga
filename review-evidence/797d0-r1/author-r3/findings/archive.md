# D0 findings: archive

Verified against dev `1e80128f`.
Source lines cite dev `1f29f189`.

## D0-057: docs/history/v1/NXN_ARCHITECTURE.md:807

- Statement: presentation-time offset is pinned at the Milan 2 ms
- Contradicted by: Copy of the D0-057 statement on `docs/reference/REGISTER_MAP.md`. `docs/reference/REGISTER_MAP.md`'s own 0x0053 note (lines 351-356): SET_STREAM_INFO is served and "the stored offset feeds the framers' transit entries"; `docs/reference/MILAN_COMPLIANCE_MATRIX.md` row 5.3.7.6 / 4.4.2.1: the 2 ms default is settable via SET_STREAM_INFO and the stamp adds the offset as set
- Correction: Say that 2 ms is the default and that SET_STREAM_INFO sets each Stream Output's offset, which the framers apply.

## D0-057: docs/history/v1/SPEC_TRACEABILITY.md:379

- Statement: presentation-time offset is pinned at the Milan 2 ms
- Contradicted by: Copy of the D0-057 statement on `docs/reference/REGISTER_MAP.md`. `docs/reference/REGISTER_MAP.md`'s own 0x0053 note (lines 351-356): SET_STREAM_INFO is served and "the stored offset feeds the framers' transit entries"; `docs/reference/MILAN_COMPLIANCE_MATRIX.md` row 5.3.7.6 / 4.4.2.1: the 2 ms default is settable via SET_STREAM_INFO and the stamp adds the offset as set
- Correction: Say that 2 ms is the default and that SET_STREAM_INFO sets each Stream Output's offset, which the framers apply.

## D0-040: docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:95

- Statement: **Nothing in this device persists a binding across a power cycle**
- Contradicted by: Copy of the D0-040 statement on `docs/reference/REGISTER_MAP_CLASSES.md`. `docs/design/SAVED_STATE_MATERIALIZATION.md` line 163: the binding survives a cold power cycle on silicon since 2026-09-21 (#70), through `KL_nvm_backend` (`hdl/milan/KL_pp_shadow.sv` line 1128) and the firmware journal writer (`sw/firmware/milan_baremetal/milan_baremetal.c` lines 1405 and 1656); only this retired journal-ingest CSR face is a structural zero (`hdl/milan/milan_datapath.sv` line 6709)
- Correction: Keep the row a structural zero for its CSR face and point at the saved-state store that does persist bindings (`PP_NVM_*`, 0x934-0x93C).

## D0-040: docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:229

- Statement: **Nothing in this device persists a binding across a power cycle**
- Contradicted by: Copy of the D0-040 statement on `docs/reference/REGISTER_MAP_CLASSES.md`. `docs/design/SAVED_STATE_MATERIALIZATION.md` line 163: the binding survives a cold power cycle on silicon since 2026-09-21 (#70), through `KL_nvm_backend` (`hdl/milan/KL_pp_shadow.sv` line 1128) and the firmware journal writer (`sw/firmware/milan_baremetal/milan_baremetal.c` lines 1405 and 1656); only this retired journal-ingest CSR face is a structural zero (`hdl/milan/milan_datapath.sv` line 6709)
- Correction: Keep the row a structural zero for its CSR face and point at the saved-state store that does persist bindings (`PP_NVM_*`, 0x934-0x93C).

## D0-057: docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:80

- Statement: presentation-time offset is pinned at the Milan 2 ms
- Contradicted by: Copy of the D0-057 statement on `docs/reference/REGISTER_MAP.md`. `docs/reference/REGISTER_MAP.md`'s own 0x0053 note (lines 351-356): SET_STREAM_INFO is served and "the stored offset feeds the framers' transit entries"; `docs/reference/MILAN_COMPLIANCE_MATRIX.md` row 5.3.7.6 / 4.4.2.1: the 2 ms default is settable via SET_STREAM_INFO and the stamp adds the offset as set
- Correction: Say that 2 ms is the default and that SET_STREAM_INFO sets each Stream Output's offset, which the framers apply.

## D0-057: docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:148

- Statement: presentation-time offset is pinned at the Milan 2 ms
- Contradicted by: Copy of the D0-057 statement on `docs/reference/REGISTER_MAP.md`. `docs/reference/REGISTER_MAP.md`'s own 0x0053 note (lines 351-356): SET_STREAM_INFO is served and "the stored offset feeds the framers' transit entries"; `docs/reference/MILAN_COMPLIANCE_MATRIX.md` row 5.3.7.6 / 4.4.2.1: the 2 ms default is settable via SET_STREAM_INFO and the stamp adds the offset as set
- Correction: Say that 2 ms is the default and that SET_STREAM_INFO sets each Stream Output's offset, which the framers apply.

## D0-040: docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md:326

- Statement: **Nothing in this device persists a binding across a power cycle**
- Contradicted by: Copy of the D0-040 statement on `docs/reference/REGISTER_MAP_CLASSES.md`. `docs/design/SAVED_STATE_MATERIALIZATION.md` line 163: the binding survives a cold power cycle on silicon since 2026-09-21 (#70), through `KL_nvm_backend` (`hdl/milan/KL_pp_shadow.sv` line 1128) and the firmware journal writer (`sw/firmware/milan_baremetal/milan_baremetal.c` lines 1405 and 1656); only this retired journal-ingest CSR face is a structural zero (`hdl/milan/milan_datapath.sv` line 6709)
- Correction: Keep the row a structural zero for its CSR face and point at the saved-state store that does persist bindings (`PP_NVM_*`, 0x934-0x93C).

## D0-040: docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md:171

- Statement: **Nothing in this device persists a binding across a power cycle**
- Contradicted by: Copy of the D0-040 statement on `docs/reference/REGISTER_MAP_CLASSES.md`. `docs/design/SAVED_STATE_MATERIALIZATION.md` line 163: the binding survives a cold power cycle on silicon since 2026-09-21 (#70), through `KL_nvm_backend` (`hdl/milan/KL_pp_shadow.sv` line 1128) and the firmware journal writer (`sw/firmware/milan_baremetal/milan_baremetal.c` lines 1405 and 1656); only this retired journal-ingest CSR face is a structural zero (`hdl/milan/milan_datapath.sv` line 6709)
- Correction: Keep the row a structural zero for its CSR face and point at the saved-state store that does persist bindings (`PP_NVM_*`, 0x934-0x93C).

## D0-057: docs/history/v1/traceability/milan-v12.md:119

- Statement: presentation-time offset is pinned at the Milan 2 ms
- Contradicted by: Copy of the D0-057 statement on `docs/reference/REGISTER_MAP.md`. `docs/reference/REGISTER_MAP.md`'s own 0x0053 note (lines 351-356): SET_STREAM_INFO is served and "the stored offset feeds the framers' transit entries"; `docs/reference/MILAN_COMPLIANCE_MATRIX.md` row 5.3.7.6 / 4.4.2.1: the 2 ms default is settable via SET_STREAM_INFO and the stamp adds the offset as set
- Correction: Say that 2 ms is the default and that SET_STREAM_INFO sets each Stream Output's offset, which the framers apply.
