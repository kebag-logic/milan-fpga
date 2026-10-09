[A577]

Closes #170

Saved-name coverage now spans every generated writable ordinal instead of five selected names: 39 names in the 1x1 TDM8 and 107 in the 8x8 diagnostic. Real SET_NAME and GET_NAME transactions are compared with an independent ordinal/name record oracle before and after reset. The tests cover:

- full 64-byte and empty values;
- capture overlap and separate record completion;
- late image initialization and failed restoration;
- CONTROL names, while IDENTIFY stays volatile.

The governing clauses are Milan v1.2 §5.3.12 and §5.3.13, and IEEE 1722.1-2021 §7.4.17.1 and §7.4.18.2.

The existing production capture and replay path passes the expanded coverage. This change adds only tests (`tb/name_state/`) and one verification-table row. RTL, NVM framing, registers, ports, parameters and the 128-record name allocation are unchanged.

The parent adoption remains a separate lane. It needs one evidence-classification entry for the new mutation driver.

Validation at base `09e357fb` and at this head:

- **Name campaign:** the generated inventories pass 169 + 441 = 610 checks. Each of the 14 planted controls, covering every §18.3 negative control, fails its named name-value assertion in a completed run. The retained descriptor-debt control fails D3R10. Base and head campaign records are identical.
- **Processor gates:** all five required gates return 0: all suites, HDL lint, the check target, the matrix check and the portable synthesis flow. The suite total rises from 1,028,293 to 1,028,903 checks, and every record of the 33 existing suites is unchanged.
- **DR3a:** all twelve simulated restore-timing records are identical and within the ratified budgets. The longest terminal measurement is 29,008 of 1,000,001 clocks.
- **DR4:** same-session 1x1 TDM8 out-of-context synthesis gives +0 LUT (LUTRAM +0) / +0 FF / 0 BRAM / 0 DSP against the names-stage ceiling of +750 / +400 / 0 / 0. WNS is unchanged at +3.203 ns. Design inputs and every hierarchy row are identical.
- **8x8 diagnostic:** unchanged. Its post-place obligation stays open and blocked.
- **Firmware:** unchanged.
- **Parent consumer** (pinned parent dev revision with this head): all seventeen gates pass at base and head, including the frontend check. The eleven retained output blocks and all 724 NVM case files match; only host metadata is normalized.

Physical cold-cycle evidence and the combined fault campaign keep their separate acceptance.
