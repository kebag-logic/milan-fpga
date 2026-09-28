# Firmware service intervals at 50 MHz

The firmware repairs for [#590](https://github.com/kebag-logic/milan-fpga/issues/590),
[#592](https://github.com/kebag-logic/milan-fpga/issues/592) and the simulated portion of
[#599](https://github.com/kebag-logic/milan-fpga/issues/599) retain one cacheless hart.
Both shapes retain continuous backing in every positive plan.
This refresh follows the [combined assignment](https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5859537529)
[merged-pin correction](https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5859930453),
and [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5862495507).
Physical switch-cycle acceptance remains a later lane.
The future-duty inventory and physical torture remain open under #397.

## Contents

- **[Measurement contract](#measurement-contract)** -- Compiled inputs, clock declarations, media fixtures and the scope of each finite plan.
- **[Measured duties](#measured-duties)** -- Per-duty elapsed times, tick gaps, UART allowances and deadline margins on both shapes.
- **[Tick placement and queued service](#tick-placement-and-queued-service)** -- Where service opportunities occur and how actual heartbeat and continuous backing are observed.
- **[PHY poll derivation and simulation](#phy-poll-derivation-and-simulation)** -- The transaction measurements, conservative scheduling charge, publication bound and real fabric observations.
- **[Device waits and limits](#device-waits-and-limits)** -- Modeled flash waits, excluded physical proof and remaining timing limitations.
- **[Controls and reproduction](#controls-and-reproduction)** -- Defect-sensitive controls, retained log bindings and commands for repeating the evidence.

## Measurement contract

The [service harness](../../tb/verilator/fw_service_budget/README.md) links the
unchanged product translation unit on the shipping cacheless RV32I CPU.
CPU and system clocks are 50 MHz and 100 MHz.
Both current configurations declare 50 MHz for Milan, including generated gPTP/lwSRP constants.
The BIOS banner reports the system clock, not the CPU clock.

The historical #397 product base was `ac18b50968b12efe4d15c0a06301264b35656b31`.
Its 8x8 CPU measurement override was 50 MHz, but its generated gPTP/lwSRP declaration remained 100 MHz.
The historical override did not rewrite that declaration.
The old report remains in [the merged findings page](https://github.com/kebag-logic/milan-fpga/blob/8bc97021f28fb7f729418d3a00851c84ea0b50fd/docs/findings/397_SERVICE_BUDGET.md).
Its queued heartbeat gaps were 2569.49201 ms at 1x1 and 2513.33593 ms at 8x8.
Those failures describe the old firmware only.

Measured source head: `ececc631c1f64893223a6d21a2de3c89b5fc7665`.
Protocol-processor pin: `16be6768f710e79450aace277abacd6c2c3336e5`.
Firmware SHA-256: `2e715af6bdb4ffce409ab2f913784dbe71e419dda75091eba16fd015093ade1b`.
CPU netlist SHA-256: `c208df0b7fafcaab190dba3f1734f2a38acd54645b33a834b0e59282e6a7813d`.
Later analysis, documentation and receipt commits do not change the compiled inputs.
Final bound-log regrading verifies the native executable, generated inputs and raw logs
before applying the current analysis; the evidence packet records that final head.

All six plans use populated A/B slots.
`all`, `uart-paced`, `queued-input`, `queued-short` and `queued-builtins` use zero device WIP.
`device-wait` uses 3 s erase and 5 ms page WIP.
The first two plans cover every registered command, boundaries, refused arguments, two commits and wipe.
`queued-input` supplies twelve NVM status commands and register status: 133 bytes on both shapes.
`queued-short` supplies 350 status commands and isolates dispatch service from long-walk service.
`queued-builtins` repeats bounded memory reads, empty lines and unknown commands.
It ends with a status command, totaling 14363 input bytes.
Queues offer each next command immediately at its prompt, without idle time.
They do not inject all bytes simultaneously into a finite RX ring.

Fixtures contain 53 records / 3264 bytes at 1x1 and 156 / 12680 bytes at 8x8.
AEM sizes are 7352 and 18288 bytes.
Restore contains 8 and 32 matched backend requests/responses without errors.
This is the current binding walk, not all remaining saved-state work.

## Measured duties

CPU cycles are elapsed system cycles divided by two, rounded upward.
Milliseconds use the unrounded 100 MHz system count.
Each row selects the maximum elapsed duty across all six finite plans.
Boot starts at reset release and ends at entity enable.
AEM starts at the first accepted flash address and ends at entity enable.
Restore brackets real backend handshakes.
UART commands span first input byte through the returned prompt.
Journal START-to-ACK excludes preceding capture/prefill.
Erase ends at first page acceptance and includes verification.
Wipe has two erase envelopes, ending at the next erase and at the prompt.


**1x1 elapsed duty maxima.**

| Duty | Plan | CPU cycles | Elapsed ms | Deadline ms | Margin ms |
| --- | --- | --- | --- | --- | --- |
| Boot to entity enabled | uart-paced | 18940584 | 378.81167 | 20000.00000 | 19621.18833 |
| AEM copy/CRC | uart-paced | 2901014 | 58.02028 | N/A | N/A |
| Restore walk | all | 32652 | 0.65304 | 3000.00000 | 2999.34696 |
| `milan_status` | uart-paced | 1448819 | 28.97637 | N/A | N/A |
| `milan_gettime` | uart-paced | 265669 | 5.31337 | N/A | N/A |
| `milan_nvm` | uart-paced | 11970942 | 239.41883 | N/A | N/A |
| `milan_nvm commit` | device-wait | 167277045 | 3345.54089 | 8000.00000 | 4654.45911 |
| `milan_nvm wipe` | uart-paced | 2483483 | 49.66965 | N/A | N/A |
| Wipe erase envelope | uart-paced | 1448160 | 28.96320 | 3500.00000 | 3471.03680 |
| `milan_nvm invalid` | uart-paced | 274270 | 5.48539 | N/A | N/A |
| `milan_settime` | uart-paced | 511470 | 10.22939 | N/A | N/A |
| `milan_utc` | uart-paced | 607038 | 12.14075 | N/A | N/A |
| Journal START-to-ACK | device-wait | 161232941 | 3224.65882 | 8000.00000 | 4775.34118 |
| Journal erase envelope | device-wait | 151006997 | 3020.13993 | 3500.00000 | 479.86007 |
| `mem_read 0x40000000 128` | queued-builtins | 1067043 | 21.34085 | N/A | N/A |
| Empty line | queued-builtins | 46611 | 0.93221 | 500.00000 | 499.06779 |
| Unknown line | queued-builtins | 87114 | 1.74227 | 500.00000 | 498.25773 |


**1x1 service opportunities.**

| Duty | Span plan | No-tick ms | TX allowance ms | Heartbeat bound ms | PHY check ms |
| --- | --- | --- | --- | --- | --- |
| Boot to entity enabled | uart-paced | 316.91512 | 0 | Unarmed prefix | N/A |
| AEM copy/CRC | uart-paced | 58.02028 | 0.00000 | 308.02028 | Startup cost 59.78462 |
| Restore walk | all | 0.65181 | 0.00000 | 250.65181 | Startup cost 2.41615 |
| `milan_status` | uart-paced | 15.29568 | 28.47222 | 293.76790 | 170.53224 |
| `milan_gettime` | uart-paced | 1.31620 | 5.20833 | 256.52453 | 133.28887 |
| `milan_nvm` | uart-paced | 24.74636 | 32.55208 | 307.29844 | 184.06278 |
| `milan_nvm commit` | device-wait | 28.57894 | 9.89583 | 288.47477 | 165.23911 |
| `milan_nvm wipe` | uart-paced | 20.61492 | 11.54514 | 282.16006 | 158.92440 |
| Wipe erase envelope | uart-paced | 20.39496 | 11.54514 | 281.94010 | 158.70444 |
| `milan_nvm invalid` | all | 1.33135 | 5.38194 | 256.71329 | 133.47763 |
| `milan_settime` | all | 3.09102 | 8.50694 | 261.59796 | 138.36230 |
| `milan_utc` | all | 3.95678 | 9.46181 | 263.41859 | 140.18293 |
| Journal START-to-ACK | device-wait | 27.23957 | 9.89583 | 287.13540 | 163.89974 |
| Journal erase envelope | device-wait | 20.14441 | 9.89583 | 280.04024 | 156.80458 |
| `mem_read 0x40000000 128` | queued-builtins | 19.60328 | 59.80903 | 329.41231 | 206.17665 |
| Empty line | queued-builtins | 0.88070 | 1.73611 | 252.61681 | 129.38115 |
| Unknown line | queued-builtins | 1.19677 | 4.68750 | 255.88427 | 132.64861 |


**8x8 elapsed duty maxima.**

| Duty | Plan | CPU cycles | Elapsed ms | Deadline ms | Margin ms |
| --- | --- | --- | --- | --- | --- |
| Boot to entity enabled | uart-paced | 55556838 | 1111.13675 | 20000.00000 | 18888.86325 |
| AEM copy/CRC | uart-paced | 6852024 | 137.04048 | N/A | N/A |
| Restore walk | uart-paced | 32681 | 0.65362 | 3000.00000 | 2999.34638 |
| `milan_status` | uart-paced | 1448819 | 28.97637 | N/A | N/A |
| `milan_gettime` | uart-paced | 265667 | 5.31333 | N/A | N/A |
| `milan_nvm` | uart-paced | 41795522 | 835.91043 | N/A | N/A |
| `milan_nvm commit` | device-wait | 216471185 | 4329.42369 | 8000.00000 | 3670.57631 |
| `milan_nvm wipe` | uart-paced | 7912045 | 158.24089 | N/A | N/A |
| Wipe erase envelope | uart-paced | 4167030 | 83.34060 | 3500.00000 | 3416.65940 |
| `milan_nvm invalid` | uart-paced | 274269 | 5.48537 | N/A | N/A |
| `milan_settime` | uart-paced | 511269 | 10.22537 | N/A | N/A |
| `milan_utc` | uart-paced | 606828 | 12.13655 | N/A | N/A |
| Journal START-to-ACK | device-wait | 193441588 | 3868.83176 | 8000.00000 | 4131.16824 |
| Journal erase envelope | device-wait | 153726027 | 3074.52053 | 3500.00000 | 425.47947 |
| `mem_read 0x40000000 128` | queued-builtins | 1089839 | 21.79677 | N/A | N/A |
| Empty line | queued-builtins | 46629 | 0.93257 | 500.00000 | 499.06743 |
| Unknown line | queued-builtins | 87114 | 1.74227 | 500.00000 | 498.25773 |


**8x8 service opportunities.**

| Duty | Span plan | No-tick ms | TX allowance ms | Heartbeat bound ms | PHY check ms |
| --- | --- | --- | --- | --- | --- |
| Boot to entity enabled | uart-paced | 970.13952 | 0 | Unarmed prefix | N/A |
| AEM copy/CRC | uart-paced | 137.04048 | 0.00000 | 387.04048 | Startup cost 138.99434 |
| Restore walk | uart-paced | 0.65241 | 0.00000 | 250.65241 | Startup cost 2.60627 |
| `milan_status` | uart-paced | 15.29560 | 28.47222 | 293.76782 | 170.72168 |
| `milan_gettime` | uart-paced | 1.35670 | 5.20833 | 256.56503 | 133.51889 |
| `milan_nvm` | uart-paced | 85.85876 | 32.72569 | 368.58445 | 245.53831 |
| `milan_nvm commit` | uart-paced | 95.82756 | 9.98264 | 355.81020 | 232.76406 |
| `milan_nvm wipe` | all | 75.16216 | 11.54514 | 336.70730 | 213.66116 |
| Wipe erase envelope | uart-paced | 74.77236 | 11.54514 | 336.31750 | 213.27136 |
| `milan_nvm invalid` | all | 1.33135 | 5.38194 | 256.71329 | 133.66715 |
| `milan_settime` | all | 3.27214 | 8.50694 | 261.77908 | 138.73294 |
| `milan_utc` | all | 4.13830 | 9.46181 | 263.60011 | 140.55397 |
| Journal START-to-ACK | device-wait | 94.10095 | 9.98264 | 354.08359 | 231.03745 |
| Journal erase envelope | device-wait | 74.52173 | 9.98264 | 334.50437 | 211.45823 |
| `mem_read 0x40000000 128` | queued-builtins | 20.06014 | 59.80903 | 329.86917 | 206.82303 |
| Empty line | queued-builtins | 0.88106 | 1.73611 | 252.61717 | 129.57103 |
| Unknown line | queued-builtins | 1.19677 | 4.68750 | 255.88427 | 132.83813 |


The heartbeat bound adds the unchanged 250 ms rate-limit phase, measured no-tick span
and the containing command's full TX serialization at 115200 baud, 8N1.
The table combines the largest span and TX allowance for each duty across plans.
Paced spans already include UART blocking; adding the allowance again is conservative.
Boot's unarmed prefix precedes the first heartbeat.
AEM follows that first service call and restore invokes it internally.
The ordinary-command 500 ms figure is a heartbeat limit, not a UART response deadline.
A long status command passes through bounded internal service opportunities.
Raw receipts retain the historical whole-command comparison separately.

Restore, erase and commit deadlines remain 3000, 3500 and 8000 ms.
AEM shares boot's 20000 ms ADP comparison from Milan v1.2 sections 5.6.2/5.6.3.
Inherited BIOS CRC, startup delays and memory tests remain excluded.
No physical boot acceptance is claimed; AECP response timing remains a fabric duty.
No isolated final-WIP marker measures the 50 ms page timeout.

## Tick placement and queued service

The product BIOS invokes a weak dispatch hook after every line.
Firmware overrides it with one heartbeat and PHY service opportunity.
The call precedes parsing, covering built-in, unknown and empty lines.
The committed patch extends the pinned BIOS without a fork.
The built-in queue requires an observed opportunity for every line.

Long BIOS built-ins remain a residual under the round-2 decision.
Examples include `mem_test` and large-range `mem_read`.
Their bodies contain no internal heartbeat or PHY opportunities.
They can exceed 500 ms heartbeats and 250 ms PHY publication.
After 2000 ms without service, saved-state backing can lapse.
The dispatch hook services their boundaries only.
CRC walks yield every 256 bytes after writer initialization.
Record-validation walks yield every sixteen records.
Wipe yields between its two erase-verification walks.
Existing restore and flash-wait opportunities remain.
The earlier 8x8 wipe chained two approximately 74 ms walks;
the added midpoint permits the derived PHY allowance below.
Measured per-duty maxima above justify these placements.
The heartbeat function's 250 ms rate limit is unchanged.

Retired CPU commit-PC observations count function entries, not speculative fetches.
Compressed blocks preserve internal maxima and both boundary tails.
The actual heartbeat is the standalone `PP_NVM_STAT <- 1` strobe.
Schedule maxima include a right-censored final tail when largest.
The native observer samples backing every system cycle after it first asserts.
Every positive run has zero unbacked cycles and all-positive console samples.

| Shape | Plan | Heartbeat gap ms | 500 ms margin | Final tail | Unbacked cycles | Down/up edges |
| --- | --- | --- | --- | --- | --- | --- |
| 1x1 | all | 264.61056 | 235.38944 | False | 0 | 0/0 |
| 1x1 | uart-paced | 252.67354 | 247.32646 | False | 0 | 1/0 |
| 1x1 | queued-input | 269.06300 | 230.93700 | False | 0 | 1/1 |
| 1x1 | queued-short | 257.65204 | 242.34796 | False | 0 | 1/1 |
| 1x1 | queued-builtins | 269.20674 | 230.79326 | False | 0 | 1/1 |
| 1x1 | device-wait | 250.54144 | 249.45856 | False | 0 | 1/1 |
| 8x8 | all | 322.45756 | 177.54244 | False | 0 | 1/1 |
| 8x8 | uart-paced | 295.44250 | 204.55750 | False | 0 | 1/1 |
| 8x8 | queued-input | 322.45756 | 177.54244 | False | 0 | 1/1 |
| 8x8 | queued-short | 257.65266 | 242.34734 | False | 0 | 1/1 |
| 8x8 | queued-builtins | 258.39768 | 241.60232 | False | 0 | 1/1 |
| 8x8 | device-wait | 275.39434 | 224.60566 | False | 0 | 1/1 |


## PHY poll derivation and simulation

The one-hart allowance is 500 ms minus the heartbeat's 250 ms phase.
The stated publication period bound is 250 ms.
Half that allowance supplies the PHY trigger: `PHY_POLL_NS = 125 ms`.
The other 125 ms covers a pending duty stretch, full UART allowance and a conservative poll scheduling charge.
Thus `125 ms + no-tick stretch + TX allowance + scheduling charge <= 250 ms`.
For startup AEM/restore, the table lists isolated service-plus-poll cost without a phase term.
It is not the full publication interval across intervening startup work.
Actual publication-readback gaps grade that startup sequence separately.
The steady-state rows grade the derived bound and the 500 ms heartbeat bound.
The target grader also refuses observed publication-readback gaps over 250 ms.
This measured bound covers executed duties, not arbitrary new work.

Each MDIO transfer is a full Clause-22 read with a 32-bit preamble.
The poll envelope begins at retired heartbeat entry and includes clock acquisition,
transactions, negotiation resolution and publication bookkeeping.
The scheduling charge is `C = P + 9*T`, where P is the largest measured complete poll
and T is the largest measured transaction. Nine reads cover discovery, two BMSR reads,
BMCR, extended status and both local/peer negotiation pairs.
Using the complete observed poll as bookkeeping allowance deliberately counts observed
transaction time twice; the longer fallback path is bounded, not claimed as target-measured.

| Shape | One transaction ms | Complete poll ms | Scheduling charge ms | 50 ms page-poll margin |
| --- | --- | --- | --- | --- |
| 1x1 | 0.12451 | 0.64375 | 1.76434 | 48.23566 |
| 8x8 | 0.12451 | 0.83327 | 1.95386 | 48.04614 |

| Shape | Worst duty + UART + charge ms | Maximum permissible trigger ms | Selected trigger ms | Remaining reserve ms |
| --- | --- | --- | --- | --- |
| 1x1 | 81.17665 | 168.82335 | 125.00000 | 43.82335 |
| 8x8 | 120.53831 | 129.46169 | 125.00000 | 4.46169 |


Both Clause-22 peers follow IEEE 802.3 section 22.3.4.
Rising edge k launches bit k+1 at simulated MDIO pins.
Firmware samples before rising edges, following the pinned LiteX reader.
Two turnaround clocks precede sixteen data samples.
The unchanged phase probe reads BMSR 0x796d and PHYID1 0x001c.
Its IEEE phase publishes link_status=13 for negotiated 1000/full.
A committed late-sample mutant fails this negotiation check.
Firmware writes the existing link-status CSR.
A separate bus master reads real MAC_STATUS; the observer samples actual fabric link counters.
A drop at 1.5 s and recovery at 1.8 s produce one down and one up in each queued and device-wait plan.
Repeated publications leave counters unchanged.
At 2.4 s negotiation changes from 1000 to 100 Mb/s; MAC_STATUS follows.
Plans ending before recovery claim only the edges shown in the schedule table.
Host tests cover missing PHY, errors, negotiation and forced speed/duplex modes.
A latched short loss is published before a second BMSR read resolves current state in the same poll.
A regression checks both edges and current recovered state in that call, without a second-period delay.
Simulated pins and CSRs do not establish the deferred physical acceptance.

## Device waits and limits

Device-max plans execute one commit with 3 s erase and 5 ms page WIP.
There are 13 and 50 pages, giving 3065 and 3250 ms modeled WIP.
Elapsed minus WIP still includes transfers, polling, verification, bus and DDR waits.
It is not spare CPU capacity.
No device-max two-sector wipe was executed.
The unchanged 30-second guard admits supported finite plans, not arbitrary stalls.

The SPI stream-boundary substitution remains optimistic.
The historical PHY probe measured 67 versus 65 system cycles for 8 bits,
259 versus 257 for 32 bits, and 78 versus 65 after CS reassertion.
That boundary cost is not a uniform percentage correction.
DDR is simulated; the service harness has no external packet traffic.
One deterministic clock phase is exercised.
Physical twofold commit margin, liveness torture, field-update writing,
fault logging and temperature duties remain unproved here.
The separate capture harness measures concurrent request traffic.

## Controls and reproduction

Portable checks pass 43 grading controls and 14 flash controls.
They retain historical traces and their original duration comparisons.
New controls refuse one-cycle overruns, a single unbacked cycle and duplicate link edges.
A target dispatch-removal mutation must lose backing in both `queued-short` and `queued-builtins`.
A target publication-removal mutation must fail the named missing-publication check.
Matching unmodified plans provide positive controls.
The capture harness checks byte-only timing and missing-copy/traffic controls.

Follow the [foreground recipe](../../tb/verilator/fw_service_budget/README.md#run-and-reproduce).
Use `--populated --enforce-service`, each of six plans and separate external directories.
Only `device-wait` adds `--device-wait-us 3000000 --program-wait-us 5000`.
Use `--regrade` with identical arguments to check a retained bound log.
Reuse verifies generated inputs, BIOS, ELF and executable hashes.
The evidence packet records SHA-256 and size for large receipts and logs.
Only small summaries belong in that packet or this repository.
Author validation is not a review verdict.
