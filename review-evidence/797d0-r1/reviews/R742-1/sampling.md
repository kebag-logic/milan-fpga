Source head: `bd16b371ae5de1c4d36ea2a018e7d756c62d4b5a`.

All 23 finding quotations were located independently. Twenty findings were checked against source or public issue state; the three clause-only findings D0-006/007/008 were not independently rederived from licensed standards. `source-excerpts.txt` and `public-issue-states.json` retain evidence.

| Existing finding | Independent evidence and correction assessment |
|---|---|
| D0-001 | `sw/litex/milan_soc.py:3838`: opt-in mailbox defaults off. Distinguishing split placement from the shipping default is correct. |
| D0-002 | `hdl/milan/milan_datapath.sv:1750`: stored source resolves to live internal/CRF/AAF selections. Media-selection correction is supported. |
| D0-003 | Issue #75 closed; the dated reconnect finding exists and limits its measurement to CRF. Replace the open-status section with the finding without implying AAF measurement. |
| D0-004 | No tracked `KL_lwsrp_ctx.sv`; the obsolete analysis remains in README. Removing it is supported. |
| D0-005 | `KL_media_nco.sv` has runtime trim, instantiated by the datapath. This contradicts the constant-divider claim. |
| D0-009 | Firmware heartbeat returns before publication when `nvm_started` is false; the inconsistent-shape boot path leaves it false. The publication condition needs documentation. |
| D0-010 | Issue #599 closed; the dated link-cycle finding records acceptance. Replace the open-acceptance pointer. |
| D0-011 | `boot_policy.py:58` supplies bit 3 and firmware `:1808` writes it. Issue #403 closed. Remove the pending claim. |
| D0-012 | Firmware `:1814` writes the generated reservation word OR 3. Issue #400 closed. State the forced bits. |
| D0-013 | `boot_policy.py:56` counts declared outputs; the extra CRF block is conditional. Correction is supported. |
| D0-014 | CSR `:897`, `:1578`, `:1688`, `:1726`, `:1731`, `:2389`: address, armed reset, dropped/masked writes, magic disarm and readback match the proposed row. |
| D0-015 | SoC wiring has no connected datapath PHY-reset output; the PHY patch drives physical reset. Documenting the inert CSR and actual reset surface is supported. |
| D0-016 | CSR `:1726` forces LINK_CTRL bit 1 to zero while guarded. Correction is supported. |
| D0-017 | SoC `:1893` supplies status reset; `:2084` wires it to the datapath. Preserve the GMII/MII speed distinction stated in the finding evidence. |
| D0-018 | CSR `:897` allocates 0x7D8; the production-class table omits it. Adding the group is supported. |
| D0-019 | CAP.CBS=0 at CSR `:1996`; no product shaper/classifier instance. The MET classification is contradicted. |
| D0-020 | Same product boundary contradicts the already-in-hardware heading. |
| D0-021 | The shipping compliance row claims implementation while its named priority shaper is absent. Qualify it as standalone verified RTL. |
| D0-022 | Same discrepancy for the credit-based shaper row. |
| D0-023 | README includes CBS in the shipping datapath despite the absent instance and zero capability bit. Correction is supported. |

Twelve pages marked current were sampled. README and FR_NFR were additionally checked through their stale findings. A sample is not full independent verification of every sentence.

| Current page | Sample and result |
|---|---|
| `docs/README.md` | Authorities/navigation and media-following entry agree with requirements, targets and live media selection. |
| `REQUIREMENTS.md` | Version, all-fabric default, CSR base and absent product CBS agree with CSR version/CAP and SoC CLI/wiring. |
| `docs/guides/IMPLEMENTATION_DEVELOPER.md` | Module/test ownership entries point to existing source and suite entry points. |
| `docs/guides/SYSTEM_INTEGRATOR.md` | Port groups and bridge commands checked against wrapper/SoC contract gates. |
| `docs/guides/PROJECT_MANAGER.md` | Two independent reviews, lens coverage and candidate validation agree with repository workflow authorities. |
| `docs/guides/VERIFICATION_DEVELOPER.md` | Runner existence contradicts the text: F2. The changed single-simulation path is valid. |
| `docs/guides/BOARD_DEPLOYMENT.md` | Identity derivation keys and priorities 248 agree with the shipping YAML and builder entry points. Physical timing promises were not measured. |
| `docs/integration/INTEGRATION_GUIDE.md` | Shipping clock/CSR boundary and port groups agree with SoC clock enforcement and wrapper contract checks. |
| `docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md` | Fabric shipping control, optional mailbox and inactive generic shaper agree with SoC/datapath. |
| `docs/integration/PORTING_GUIDE.md` | Reusable `MilanNIC`, `MilanMAC` and `add_milan_datapath` symbols exist. |
| `docs/integration/QSPI_FLASHBOOT.md` | Absent-persistence claim contradicts backend/firmware: F1. |
| `docs/reference/EGRESS_QUEUE_MAP.md` | q2/q3 reset roles contradict enum/reset map: F3. Absent shipping shaper statement is correct. |
