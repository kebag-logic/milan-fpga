# Firmware service intervals at 50 MHz

The firmware repairs for [#590](https://github.com/kebag-logic/milan-fpga/issues/590),
[#592](https://github.com/kebag-logic/milan-fpga/issues/592) and the simulated portion of
[#599](https://github.com/kebag-logic/milan-fpga/issues/599) retain one cacheless hart.
Both shapes retain continuous backing in every positive plan.
This refresh follows the [combined assignment](https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5859537529)
[merged-pin correction](https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5859930453),
and [round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5865679172).
#70 lane 2 re-measured it after the [AEM-first ruling](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5894183475).
Its firmware loads the AEM image before `nvm_boot()` and walks on every boot path.
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

Measured source head: `18199bacae847f8f3c1a31ee9b62d0086c8abf41`.
Protocol-processor pin: `b2db3a970cedbbff2f8ba813acb96122c442bc58`.
Firmware SHA-256: `a73ecc25c77bfb7c4e1c2c711d72f0b560dd7e8d18cde92f40e67efcc84f0eb3`.
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
Restore contains 42 and 144 matched backend requests/responses without errors.
They are the binding walk and the D3 walk, not all remaining saved-state work.

## Measured duties

CPU cycles are elapsed system cycles divided by two, rounded upward.
Milliseconds use the unrounded 100 MHz system count.
Each row selects the maximum elapsed duty across all six finite plans.
Boot starts at reset release and ends at entity enable.
AEM starts at the first accepted flash address and ends at entity enable.
Since the AEM image loads first, that span also holds `nvm_boot()` and the restore.
Restore brackets real backend handshakes.
UART commands span first input byte through the returned prompt.
Journal START-to-ACK excludes preceding capture/prefill.
Erase ends at first page acceptance and includes verification.
Wipe has two erase envelopes, ending at the next erase and at the prompt.


**1x1 elapsed duty maxima.**

| Duty | Plan | CPU cycles | Elapsed ms | Deadline ms | Margin ms |
| --- | --- | --- | --- | --- | --- |
| Boot to entity enabled | uart-paced | 18920042 | 378.40083 | 20000.00000 | 19621.59917 |
| AEM read to entity enabled | uart-paced | 14512581 | 290.25161 | N/A | N/A |
| Restore walk | uart-paced | 33059 | 0.66118 | 3000.00000 | 2999.33882 |
| `milan_status` | uart-paced | 1449097 | 28.98193 | N/A | N/A |
| `milan_gettime` | uart-paced | 265603 | 5.31205 | N/A | N/A |
| `milan_nvm` | uart-paced | 11948323 | 238.96645 | N/A | N/A |
| `milan_nvm commit` | device-wait | 167259017 | 3345.18033 | 8000.00000 | 4654.81967 |
| `milan_nvm wipe` | uart-paced | 2473645 | 49.47289 | N/A | N/A |
| Wipe erase envelope | uart-paced | 1448160 | 28.96320 | 3500.00000 | 3471.03680 |
| `milan_nvm invalid` | uart-paced | 275058 | 5.50115 | N/A | N/A |
| `milan_settime` | uart-paced | 511284 | 10.22567 | N/A | N/A |
| `milan_utc` | uart-paced | 606531 | 12.13061 | N/A | N/A |
| Journal START-to-ACK | device-wait | 161236677 | 3224.73354 | 8000.00000 | 4775.26646 |
| Journal erase envelope | device-wait | 151007338 | 3020.14675 | 3500.00000 | 479.85325 |
| `mem_read 0x40000000 128` | queued-builtins | 1067063 | 21.34125 | N/A | N/A |
| Empty line | queued-builtins | 46630 | 0.93259 | N/A | N/A |
| Unknown line | queued-builtins | 87133 | 1.74265 | N/A | N/A |


**1x1 service opportunities.**

| Duty | Span plan | No-tick ms | TX allowance ms | Heartbeat bound ms | PHY check ms |
| --- | --- | --- | --- | --- | --- |
| Boot to entity enabled | uart-paced | 373.90220 | 0 | Unarmed prefix | N/A |
| AEM read to entity enabled | uart-paced | 4.49863 | 0.00000 | 254.49863 | Startup cost 6.26998 |
| Restore walk | uart-paced | 0.65955 | 0.00000 | 250.65955 | Startup cost 2.43090 |
| `milan_status` | uart-paced | 15.29606 | 28.47222 | 293.76828 | 170.53963 |
| `milan_gettime` | uart-paced | 1.31658 | 5.20833 | 256.52491 | 133.29626 |
| `milan_nvm` | uart-paced | 24.74722 | 32.55208 | 307.29930 | 184.07065 |
| `milan_nvm commit` | uart-paced | 28.70514 | 9.89583 | 288.60097 | 165.37232 |
| `milan_nvm wipe` | uart-paced | 20.43068 | 11.54514 | 281.97582 | 158.74717 |
| Wipe erase envelope | uart-paced | 20.39496 | 11.54514 | 281.94010 | 158.71145 |
| `milan_nvm invalid` | all | 1.33135 | 5.38194 | 256.71329 | 133.48464 |
| `milan_settime` | all | 3.09140 | 8.50694 | 261.59834 | 138.36969 |
| `milan_utc` | all | 3.95716 | 9.46181 | 263.41897 | 140.19032 |
| Journal START-to-ACK | uart-paced | 27.05799 | 9.89583 | 286.95382 | 163.72517 |
| Journal erase envelope | device-wait | 20.14419 | 9.89583 | 280.04002 | 156.81137 |
| `mem_read 0x40000000 128` | queued-builtins | 19.60368 | 59.80903 | 329.41271 | 206.18406 |
| Empty line | queued-builtins | 0.88108 | 1.73611 | 252.61719 | 129.38854 |
| Unknown line | queued-builtins | 1.19677 | 4.68750 | 255.88427 | 132.65562 |


**8x8 elapsed duty maxima.**

| Duty | Plan | CPU cycles | Elapsed ms | Deadline ms | Margin ms |
| --- | --- | --- | --- | --- | --- |
| Boot to entity enabled | uart-paced | 55566448 | 1111.32895 | 20000.00000 | 18888.67105 |
| AEM read to entity enabled | uart-paced | 51158971 | 1023.17942 | N/A | N/A |
| Restore walk | all | 63486 | 1.26972 | 3000.00000 | 2998.73028 |
| `milan_status` | uart-paced | 1449097 | 28.98193 | N/A | N/A |
| `milan_gettime` | uart-paced | 265603 | 5.31205 | N/A | N/A |
| `milan_nvm` | uart-paced | 41797519 | 835.95037 | N/A | N/A |
| `milan_nvm commit` | device-wait | 216465324 | 4329.30647 | 8000.00000 | 3670.69353 |
| `milan_nvm wipe` | uart-paced | 7911333 | 158.22665 | N/A | N/A |
| Wipe erase envelope | uart-paced | 4167030 | 83.34060 | 3500.00000 | 3416.65940 |
| `milan_nvm invalid` | uart-paced | 275058 | 5.50115 | N/A | N/A |
| `milan_settime` | uart-paced | 511328 | 10.22655 | N/A | N/A |
| `milan_utc` | uart-paced | 606574 | 12.13147 | N/A | N/A |
| Journal START-to-ACK | device-wait | 193453499 | 3869.06998 | 8000.00000 | 4130.93002 |
| Journal erase envelope | device-wait | 153725940 | 3074.51879 | 3500.00000 | 425.48121 |
| `mem_read 0x40000000 128` | queued-builtins | 1067063 | 21.34125 | N/A | N/A |
| Empty line | queued-builtins | 46640 | 0.93279 | N/A | N/A |
| Unknown line | queued-builtins | 87133 | 1.74265 | N/A | N/A |


**8x8 service opportunities.**

| Duty | Span plan | No-tick ms | TX allowance ms | Heartbeat bound ms | PHY check ms |
| --- | --- | --- | --- | --- | --- |
| Boot to entity enabled | uart-paced | 1106.14204 | 0 | Unarmed prefix | N/A |
| AEM read to entity enabled | uart-paced | 3.93371 | 0.00000 | 253.93371 | Startup cost 5.88859 |
| Restore walk | uart-paced | 0.66038 | 0.00000 | 250.66038 | Startup cost 2.61526 |
| `milan_status` | uart-paced | 15.29598 | 28.47222 | 293.76820 | 170.72308 |
| `milan_gettime` | uart-paced | 1.35708 | 5.20833 | 256.56541 | 133.52029 |
| `milan_nvm` | uart-paced | 85.85904 | 32.72569 | 368.58473 | 245.53961 |
| `milan_nvm commit` | uart-paced | 95.82864 | 9.98264 | 355.81128 | 232.76616 |
| `milan_nvm wipe` | all | 75.16206 | 11.54514 | 336.70720 | 213.66208 |
| Wipe erase envelope | uart-paced | 74.77236 | 11.54514 | 336.31750 | 213.27238 |
| `milan_nvm invalid` | all | 1.33135 | 5.38194 | 256.71329 | 133.66817 |
| `milan_settime` | all | 3.27252 | 8.50694 | 261.77946 | 138.73434 |
| `milan_utc` | all | 4.13868 | 9.46181 | 263.60049 | 140.55537 |
| Journal START-to-ACK | uart-paced | 94.10159 | 9.98264 | 354.08423 | 231.03911 |
| Journal erase envelope | device-wait | 74.52235 | 9.98264 | 334.50499 | 211.45987 |
| `mem_read 0x40000000 128` | queued-builtins | 19.60368 | 59.80903 | 329.41271 | 206.36759 |
| Empty line | queued-builtins | 0.88128 | 1.73611 | 252.61739 | 129.57227 |
| Unknown line | queued-builtins | 1.19677 | 4.68750 | 255.88427 | 132.83915 |


The heartbeat bound adds the unchanged 250 ms rate-limit phase, measured no-tick span
and the containing command's full TX serialization at 115200 baud, 8N1.
The table combines the largest span and TX allowance for each duty across plans.
Paced spans already include UART blocking; adding the allowance again is conservative.
Boot's unarmed prefix precedes the first heartbeat opportunity.
Reset to the first PHY publication spans that prefix, which only boot's 20000 ms comparison grades; the AEM-first order added the AEM copy and CRC to it, from 316.91802 ms at 1x1 and 970.14222 ms at 8x8.
The AEM read now falls inside it, so the AEM row is charged from that opportunity.
Its unarmed part is boot's: 283.12954 to 285.75298 ms at 1x1.
At 8x8 it is 1015.35487 to 1017.99251 ms.
Restore invokes the service internally.
N/A means no separate protocol deadline for that duty.
This includes bounded memory reads, empty lines and unknown lines.
Their heartbeat and PHY allowances remain in the service tables.
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
Identity and shape checks must first admit the writer.
Rejected startup cannot arm backing through console input.
Patch 0006 supplies a required link marker.
Firmware fails linking when the BIOS lacks that marker.
The call precedes parsing, covering built-in, unknown and empty lines.
The committed patch extends the pinned BIOS without a fork.
The built-in queue requires an observed opportunity for every line.

Long BIOS built-ins remain a residual under the round-2 decision.
Examples include `mem_test` and large-range `mem_read`.
Their bodies contain no internal heartbeat or PHY opportunities.
They can exceed 500 ms heartbeats and 250 ms PHY publication.
A built-in body can lapse backing after about 1,750 ms.
The 2,000 ms deadline includes up to 250 ms beforehand.
That phase can suppress the dispatch heartbeat write.
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
| 1x1 | all | 262.44494 | 237.55506 | False | 0 | 0/0 |
| 1x1 | uart-paced | 262.55614 | 237.44386 | False | 0 | 1/0 |
| 1x1 | queued-input | 265.42240 | 234.57760 | False | 0 | 1/1 |
| 1x1 | queued-short | 257.66520 | 242.33480 | False | 0 | 1/1 |
| 1x1 | queued-builtins | 260.22818 | 239.77182 | False | 0 | 1/1 |
| 1x1 | device-wait | 250.46200 | 249.53800 | False | 0 | 1/1 |
| 8x8 | all | 304.49776 | 195.50224 | False | 0 | 1/1 |
| 8x8 | uart-paced | 294.40442 | 205.59558 | False | 0 | 1/1 |
| 8x8 | queued-input | 294.43206 | 205.56794 | False | 0 | 1/1 |
| 8x8 | queued-short | 257.66520 | 242.33480 | False | 0 | 1/1 |
| 8x8 | queued-builtins | 260.89732 | 239.10268 | False | 0 | 1/1 |
| 8x8 | device-wait | 290.09722 | 209.90278 | False | 0 | 1/1 |


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
| 1x1 | 0.12455 | 0.65040 | 1.77135 | 48.22865 |
| 8x8 | 0.12457 | 0.83375 | 1.95488 | 48.04512 |

| Shape | Worst duty + UART + charge ms | Maximum permissible trigger ms | Selected trigger ms | Remaining reserve ms |
| --- | --- | --- | --- | --- |
| 1x1 | 81.18406 | 168.81594 | 125.00000 | 43.81594 |
| 8x8 | 120.53961 | 129.46039 | 125.00000 | 4.46039 |


Both Clause-22 peers follow IEEE 802.3 section 22.3.4.
Rising edge k launches bit k+1 at simulated MDIO pins.
Firmware samples before rising edges, following the pinned LiteX reader.
Two turnaround clocks precede sixteen data samples.
The [unchanged phase probe](https://github.com/kebag-logic/milan-fpga/blob/a1c4d79f/review-evidence/590-r1/reviews/R369-1/probe_mdio_phase.py) reads BMSR 0x796d and PHYID1 0x001c.
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

Portable checks pass 52 grading controls and 14 flash controls.
They retain historical traces and their original duration comparisons.
New controls refuse one-cycle overruns, a single unbacked cycle and duplicate link edges.
A target dispatch-removal mutation must lose backing in both `queued-short` and `queued-builtins`.
Its verdict also requires the named per-line dispatch finding.
Portable controls reject missing opportunities despite otherwise healthy backing.
A target publication-removal mutation must fail the named missing-publication check.
Matching unmodified plans provide positive controls.
The capture harness checks byte-only timing and missing-copy/traffic controls.

Follow the [foreground recipe](../../tb/verilator/fw_service_budget/README.md#run-and-reproduce).
Use `--populated --enforce-service`, each of six plans and separate external directories.
Only `device-wait` adds `--device-wait-us 3000000 --program-wait-us 5000`.
Use `--regrade` with identical arguments to check a retained bound log.
Reuse verifies generated inputs, BIOS, ELF and executable hashes.
The evidence packet records SHA-256 and size for large receipts and logs.
Raw logs and JSON receipts remain in the evidence packet.
Large files are compressed, with raw and compressed SHA-256 bindings.
Only summaries belong in this repository.
Author validation is not a review verdict.
