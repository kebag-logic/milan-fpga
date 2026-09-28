# Firmware service intervals at 50 MHz

The firmware repairs for [#590](https://github.com/kebag-logic/milan-fpga/issues/590),
[#592](https://github.com/kebag-logic/milan-fpga/issues/592) and the simulated portion of
[#599](https://github.com/kebag-logic/milan-fpga/issues/599) retain one cacheless hart.
Both shapes retain continuous backing in every executed plan.
This refresh follows the [combined assignment](https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5859537529)
and [merged-pin correction](https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5859930453).
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

Measured source head: `5e8edc86822a5cd2ba11da41dec0df7397d76da0`.
Protocol-processor pin: `16be6768f710e79450aace277abacd6c2c3336e5`.
Firmware SHA-256: `91d6ca57937530e429985e08e687b4e6949e074a7b75f38bfdf47c554430be7d`.
CPU netlist SHA-256: `c208df0b7fafcaab190dba3f1734f2a38acd54645b33a834b0e59282e6a7813d`.
Later analysis, documentation and receipt commits do not change the compiled inputs.
Final bound-log regrading verifies the native executable, generated inputs and raw logs
before applying the current analysis; the evidence packet records that final head.

All five plans use populated A/B slots.
`all`, `uart-paced`, `queued-input` and `queued-short` use zero device WIP.
`device-wait` uses 3 s erase and 5 ms page WIP.
The first two plans cover every registered command, boundaries, refused arguments, two commits and wipe.
`queued-input` supplies twelve NVM status commands and register status: 133 bytes on both shapes.
`queued-short` supplies 350 status commands and isolates dispatch service from long-walk service.
Queues offer each next command immediately at its prompt, without idle time.
They do not inject all bytes simultaneously into a finite RX ring.

Fixtures contain 53 records / 3264 bytes at 1x1 and 156 / 12680 bytes at 8x8.
AEM sizes are 7352 and 18288 bytes.
Restore contains 8 and 32 matched backend requests/responses without errors.
This is the current binding walk, not all remaining saved-state work.

## Measured duties

CPU cycles are elapsed system cycles divided by two, rounded upward.
Milliseconds use the unrounded 100 MHz system count.
Each row selects the maximum elapsed duty across all five finite plans.
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
| Boot to entity enabled | uart-paced | 18941168 | 378.82335 | 20000.00000 | 19621.17665 |
| AEM copy/CRC | uart-paced | 2901072 | 58.02144 | N/A | N/A |
| Restore walk | all | 33175 | 0.66350 | 3000.00000 | 2999.33650 |
| `milan_status` | uart-paced | 1448759 | 28.97517 | N/A | N/A |
| `milan_gettime` | uart-paced | 265178 | 5.30355 | N/A | N/A |
| `milan_nvm` | uart-paced | 11971340 | 239.42679 | N/A | N/A |
| `milan_nvm commit` | device-wait | 167277443 | 3345.54885 | 8000.00000 | 4654.45115 |
| `milan_nvm wipe` | uart-paced | 2483617 | 49.67233 | N/A | N/A |
| Wipe erase envelope | uart-paced | 1448160 | 28.96320 | 3500.00000 | 3471.03680 |
| `milan_nvm invalid` | uart-paced | 274251 | 5.48501 | N/A | N/A |
| `milan_settime` | uart-paced | 511629 | 10.23257 | N/A | N/A |
| `milan_utc` | uart-paced | 606362 | 12.12723 | N/A | N/A |
| Journal START-to-ACK | device-wait | 161233092 | 3224.66184 | 8000.00000 | 4775.33816 |
| Journal erase envelope | device-wait | 151006085 | 3020.12169 | 3500.00000 | 479.87831 |


**1x1 service opportunities.**

| Duty | Span plan | No-tick ms | TX allowance ms | Heartbeat bound ms | PHY check ms |
| --- | --- | --- | --- | --- | --- |
| Boot to entity enabled | uart-paced | 316.91512 | 0 | Unarmed prefix | N/A |
| AEM copy/CRC | uart-paced | 58.02144 | 0.00000 | 308.02144 | Startup cost 59.81091 |
| Restore walk | all | 0.66227 | 0.00000 | 250.66227 | Startup cost 2.45174 |
| `milan_status` | uart-paced | 15.12404 | 28.47222 | 293.59626 | 170.38573 |
| `milan_gettime` | all | 1.21557 | 5.20833 | 256.42390 | 133.21337 |
| `milan_nvm` | uart-paced | 24.74636 | 32.55208 | 307.29844 | 184.08791 |
| `milan_nvm commit` | device-wait | 28.58932 | 9.89583 | 288.48515 | 165.27462 |
| `milan_nvm wipe` | uart-paced | 20.61798 | 11.54514 | 282.16312 | 158.95259 |
| Wipe erase envelope | uart-paced | 20.39496 | 11.54514 | 281.94010 | 158.72957 |
| `milan_nvm invalid` | all | 1.49913 | 5.38194 | 256.88107 | 133.67054 |
| `milan_settime` | all | 2.92286 | 8.50694 | 261.42980 | 138.21927 |
| `milan_utc` | all | 3.80082 | 9.46181 | 263.26263 | 140.05210 |
| Journal START-to-ACK | device-wait | 27.24995 | 9.89583 | 287.14578 | 163.93525 |
| Journal erase envelope | device-wait | 20.14383 | 9.89583 | 280.03966 | 156.82913 |


**8x8 elapsed duty maxima.**

| Duty | Plan | CPU cycles | Elapsed ms | Deadline ms | Margin ms |
| --- | --- | --- | --- | --- | --- |
| Boot to entity enabled | uart-paced | 55557223 | 1111.14445 | 20000.00000 | 18888.85555 |
| AEM copy/CRC | uart-paced | 6851914 | 137.03828 | N/A | N/A |
| Restore walk | all | 33178 | 0.66356 | 3000.00000 | 2999.33644 |
| `milan_status` | uart-paced | 1449078 | 28.98155 | N/A | N/A |
| `milan_gettime` | uart-paced | 265176 | 5.30351 | N/A | N/A |
| `milan_nvm` | uart-paced | 41798623 | 835.97245 | N/A | N/A |
| `milan_nvm commit` | device-wait | 216474273 | 4329.48545 | 8000.00000 | 3670.51455 |
| `milan_nvm wipe` | uart-paced | 7911755 | 158.23509 | N/A | N/A |
| Wipe erase envelope | uart-paced | 4167030 | 83.34060 | 3500.00000 | 3416.65940 |
| `milan_nvm invalid` | uart-paced | 274250 | 5.48499 | N/A | N/A |
| `milan_settime` | uart-paced | 511770 | 10.23539 | N/A | N/A |
| `milan_utc` | uart-paced | 606535 | 12.13069 | N/A | N/A |
| Journal START-to-ACK | device-wait | 193443894 | 3868.87788 | 8000.00000 | 4131.12212 |
| Journal erase envelope | device-wait | 153725245 | 3074.50489 | 3500.00000 | 425.49511 |


**8x8 service opportunities.**

| Duty | Span plan | No-tick ms | TX allowance ms | Heartbeat bound ms | PHY check ms |
| --- | --- | --- | --- | --- | --- |
| Boot to entity enabled | uart-paced | 970.13952 | 0 | Unarmed prefix | N/A |
| AEM copy/CRC | uart-paced | 137.03828 | 0.00000 | 387.03828 | Startup cost 139.01833 |
| Restore walk | all | 0.66235 | 0.00000 | 250.66235 | Startup cost 2.64240 |
| `milan_status` | uart-paced | 15.12396 | 28.47222 | 293.59618 | 170.57623 |
| `milan_gettime` | all | 1.21557 | 5.20833 | 256.42390 | 133.40395 |
| `milan_nvm` | uart-paced | 85.85876 | 32.72569 | 368.58445 | 245.56450 |
| `milan_nvm commit` | uart-paced | 95.82806 | 9.98264 | 355.81070 | 232.79075 |
| `milan_nvm wipe` | all | 75.17266 | 11.54514 | 336.71780 | 213.69785 |
| Wipe erase envelope | uart-paced | 74.77236 | 11.54514 | 336.31750 | 213.29755 |
| `milan_nvm invalid` | all | 1.49913 | 5.38194 | 256.88107 | 133.86112 |
| `milan_settime` | all | 3.10698 | 8.50694 | 261.61392 | 138.59397 |
| `milan_utc` | all | 3.98534 | 9.46181 | 263.44715 | 140.42720 |
| Journal START-to-ACK | uart-paced | 94.10101 | 9.98264 | 354.08365 | 231.06370 |
| Journal erase envelope | device-wait | 74.52111 | 9.98264 | 334.50375 | 211.48380 |


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

Each registered Milan command begins with one opportunity.
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
| 1x1 | all | 264.62414 | 235.37586 | False | 0 | 0/0 |
| 1x1 | uart-paced | 252.67354 | 247.32646 | False | 0 | 1/0 |
| 1x1 | queued-input | 269.07786 | 230.92214 | False | 0 | 1/1 |
| 1x1 | queued-short | 257.67502 | 242.32498 | False | 0 | 1/1 |
| 1x1 | device-wait | 250.41246 | 249.58754 | False | 0 | 1/1 |
| 8x8 | all | 322.47112 | 177.52888 | False | 0 | 1/1 |
| 8x8 | uart-paced | 295.46250 | 204.53750 | False | 0 | 1/1 |
| 8x8 | queued-input | 322.47112 | 177.52888 | False | 0 | 1/1 |
| 8x8 | queued-short | 257.67564 | 242.32436 | False | 0 | 1/1 |
| 8x8 | device-wait | 275.41748 | 224.58252 | False | 0 | 1/1 |


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
| 1x1 | 0.12616 | 0.65403 | 1.78947 | 48.21053 |
| 8x8 | 0.12624 | 0.84389 | 1.98005 | 48.01995 |

| Shape | Worst duty + UART + charge ms | Maximum permissible trigger ms | Selected trigger ms | Remaining reserve ms |
| --- | --- | --- | --- | --- |
| 1x1 | 59.08791 | 190.91209 | 125.00000 | 65.91209 |
| 8x8 | 120.56450 | 129.43550 | 125.00000 | 4.43550 |


An independent Clause-22 peer drives simulated MDIO pins.
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

Portable checks pass 42 grading controls and 14 flash controls.
They retain historical traces and their original duration comparisons.
New controls refuse one-cycle overruns, a single unbacked cycle and duplicate link edges.
A target dispatch-removal mutation must lose backing in `queued-short`.
A target publication-removal mutation must fail the named missing-publication check.
Matching unmodified plans provide positive controls.
The capture harness checks byte-only timing and missing-copy/traffic controls.

Follow the [foreground recipe](../../tb/verilator/fw_service_budget/README.md#run-and-reproduce).
Use `--populated --enforce-service`, each of five plans and separate external directories.
Only `device-wait` adds `--device-wait-us 3000000 --program-wait-us 5000`.
Use `--regrade` with identical arguments to check a retained bound log.
Reuse verifies generated inputs, BIOS, ELF and executable hashes.
The evidence packet records SHA-256 and size for large receipts and logs.
Only small summaries belong in that packet or this repository.
Author validation is not a review verdict.
