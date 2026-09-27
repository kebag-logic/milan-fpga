# Firmware service intervals at 50 MHz

This records the measurement-only scope of [issue #397](https://github.com/kebag-logic/milan-fpga/issues/397#issuecomment-5854787465)
and its [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/397#issuecomment-5855879265).
The product base is `ac18b50968b12efe4d15c0a06301264b35656b31`.
Firmware, RTL, submodule pins and the capture harness remain unchanged.
Queued console input lapses writer liveness in **both** shipped shapes.
The firmware repair is [#590](https://github.com/kebag-logic/milan-fpga/issues/590).
These measurements do not close the future-duty inventory, hart decision or physical torture work.

## Contents

- **[Measured duties](#measured-duties)** -- External boundaries, elapsed cycles, deadlines and margins for each current duty.
- **[Heartbeat opportunities and schedules](#heartbeat-opportunities-and-schedules)** -- Duty-specific service gaps, conditional period comparisons and executed liveness failures.
- **[Device waits and substitution limits](#device-waits-and-substitution-limits)** -- Measured device-max runs, polling behavior and the direction of simulation bias.
- **[Controls and validation](#controls-and-validation)** -- Fixed traces, public mutation probes and gate results.
- **[Reproduction and evidence](#reproduction-and-evidence)** -- Named command plans, evidence identities and reproduction commands.

## Measured duties

The [sibling harness](../../tb/verilator/fw_service_budget/README.md) links the
unchanged product translation unit on the shipping cacheless RV32I core.
CPU and system clocks are driven at 50 MHz and 100 MHz.
The BIOS banner prints the system-clock constant; it does not select the CPU clock.
The 8x8 configuration's Milan-clock declaration is overridden by the existing
capture recipe to satisfy this assignment's explicit 50 MHz contract.
CPU cycles below are elapsed system cycles divided by two, rounded upward.
Milliseconds use the unrounded system count, not instruction counts or utilization.

These are maxima across four finite scenarios at one deterministic clock phase
with populated A/B slots; each row identifies the plan containing its maximum.
They are not a worst-case proof for arbitrary console input or bus contention.
The `all` plan uses 0 ms erase/page WIP at 1x1 and 1 ms of each at 8x8.
`uart-paced` and `queued-input` use zero WIP; `device-wait` uses 3 s erase and 5 ms page WIP.
The `all` plan covers every product command registration, numeric boundaries,
refused arguments, two successive commits and a wipe.
The fixtures contain 53 records / 3,264 bytes at 1x1 and 156 / 12,680 at 8x8.
Their AEM images contain 7,352 and 18,288 bytes.
Restore contains 8 and 32 matching backend requests/responses with no errors.
It measures the current binding walk, not the remaining saved-state work in
[section 12.2](../design/SAVED_STATE_FASTCONNECT.md#122-where-they-go-today).

Boot begins at reset release, system cycle 64, and ends at entity enable.
AEM copy/CRC begins when the first read's address at `0x400000` is accepted
by the flash model, before its data transfer, and ends at the same enable write.
This is a conservative marked AEM envelope, no longer the whole boot.
The independent public observer starts at completion of the first read,
so its AEM envelope is slightly shorter by the initial transfer overhead.
Restore uses control writes enclosing the real backend handshakes.
UART commands span the first input byte through the returned prompt.
Journal START-to-ACK excludes the console's preceding capture/prefill.
The erase envelope ends at first page acceptance and includes verification.
Wipe has two separate erase envelopes: erase-to-next-erase and erase-to-prompt.
There is no whole-wipe commit timer.

**1x1: populated A/B slots, maxima over all four plans.**

| Duty | Plan at maximum | Elapsed CPU cycles | Elapsed ms | Budget ms | Margin ms |
| --- | --- | ---: | ---: | ---: | ---: |
| Boot to entity enabled | `uart-paced` | 18,698,731 | 373.97461 | 20,000 | 19626.02539 |
| AEM copy/CRC | `uart-paced` | 2,899,797 | 57.99594 | N/A | N/A |
| Binding restore walk | `all` | 1,138 | 0.02276 | 3,000 | 2999.97724 |
| Journal erase envelope | `device-wait` | 151,005,855 | 3020.11709 | 3,500 | 479.88291 |
| Journal START-to-ACK | `device-wait` | 161,067,660 | 3221.35320 | 8,000 | 4778.64680 |
| `milan_status` | `uart-paced` | 1,448,542 | 28.97083 | 500 | 471.02917 |
| `milan_gettime` | `uart-paced` | 265,586 | 5.31171 | 500 | 494.68829 |
| `milan_settime`, maximum tested case | `uart-paced` | 510,995 | 10.21989 | 500 | 489.78011 |
| `milan_utc`, maximum tested case | `uart-paced` | 605,880 | 12.11759 | 500 | 487.88241 |
| `milan_nvm` status | `uart-paced` | 11,682,149 | 233.64297 | 500 | 266.35703 |
| `milan_nvm commit` | `device-wait` | 166,979,731 | 3339.59461 | 8,000 | 4660.40539 |
| `milan_nvm wipe`, whole command | `uart-paced` | 2,472,810 | 49.45619 | N/A | N/A |
| Wipe erase envelope, maximum of two | `uart-paced` | 1,448,160 | 28.96320 | 3,500 | 3471.03680 |
| `milan_nvm invalid` | `uart-paced` | 273,914 | 5.47827 | 500 | 494.52173 |

**8x8: populated A/B slots, maxima over all four plans.**

| Duty | Plan at maximum | Elapsed CPU cycles | Elapsed ms | Budget ms | Margin ms |
| --- | --- | ---: | ---: | ---: | ---: |
| Boot to entity enabled | `uart-paced` | 54,724,259 | 1094.48517 | 20,000 | 18905.51483 |
| AEM copy/CRC | `uart-paced` | 6,850,696 | 137.01392 | N/A | N/A |
| Binding restore walk | `uart-paced` | 2,706 | 0.05412 | 3,000 | 2999.94588 |
| Journal erase envelope | `device-wait` | 153,725,874 | 3074.51747 | 3,500 | 425.48253 |
| Journal START-to-ACK | `device-wait` | 192,836,355 | 3856.72710 | 8,000 | 4143.27290 |
| `milan_status` | `uart-paced` | 1,448,542 | 28.97083 | 500 | 471.02917 |
| `milan_gettime` | `uart-paced` | 265,595 | 5.31189 | 500 | 494.68811 |
| `milan_settime`, maximum tested case | `uart-paced` | 510,995 | 10.21989 | 500 | 489.78011 |
| `milan_utc`, maximum tested case | `uart-paced` | 605,880 | 12.11759 | 500 | 487.88241 |
| `milan_nvm` status | `uart-paced` | 40,703,945 | 814.07889 | 500 | -314.07889 |
| `milan_nvm commit` | `device-wait` | 215,384,150 | 4307.68299 | 8,000 | 3692.31701 |
| `milan_nvm wipe`, whole command | `uart-paced` | 7,910,620 | 158.21239 | N/A | N/A |
| Wipe erase envelope, maximum of two | `uart-paced` | 4,167,030 | 83.34060 | 3,500 | 3416.65940 |
| `milan_nvm invalid` | `uart-paced` | 273,914 | 5.47827 | 500 | 494.52173 |

The ordinary-command 500 ms comparison comes from the maximum heartbeat period
in [saved-state section 9.4](../design/SAVED_STATE_FASTCONNECT.md#94-the-deadlines).
It is a service-window comparison, not a UART protocol deadline.
Restore, erase and commit use the existing 3,000, 3,500 and 8,000 ms limits.
Page programming is inside the commit bracket; no isolated last-WIP-poll
marker exists, so no separate margin against the 50 ms page-poll timeout is claimed.
AEM shares boot's window and has no independent deadline.

Milan v1.2 sections 5.6.2/5.6.3 provide the requested ADP comparison:
`valid_time = 10`, in two-second units, gives 20,000 ms.
The boot maxima come from `uart-paced`, but still exclude inherited BIOS CRC,
startup delays and memory tests. The `all` plan excludes UART serialization as well.
Those exclusions prevent a physical boot-time acceptance claim.
IEEE 1722.1-2021 section 9.3.2.6's AECP response timing belongs to the fabric,
consistent with NFR-SCOUT-03, not this control hart.

## Heartbeat opportunities and schedules

An actual heartbeat is the CSR strobe `PP_NVM_STAT <- 1`.
A call to the rate-limited heartbeat function is only an opportunity to issue it.
The passive observer uses the linked ELF entry address and the existing CPU
commit-valid/commit-PC signals, sampled on a CPU rising edge.
It does not count speculative fetches or stalled instructions.
Every external boundary flushes a compressed block of calls, preserving its
first/last entries, count and maximum internal separation.
Duty maxima include both boundary tails and gaps between blocks.
No firmware source or CPU netlist is changed.

For an isolated duty with service available on either side, the conditional
period comparison is **250 ms rate-limit phase + no-tick span + TX allowance**.
TX allowance serializes the containing command's entire observed output at
115,200 baud, 8N1; it is deliberately conservative for nested duty envelopes.
The tables take the longest no-tick span across all four executed plans,
then add the largest TX allowance for that duty group.
These two maxima need not come from the same occurrence.
The plan column identifies the measured span, not an unconditional schedule guarantee.
Paced spans already include UART blocking; adding the full TX allowance again
is conservative. A negative conditional margin means the bound does not
establish that limit; the actual observed violations appear in the schedule table.
Boot's largest span precedes the first heartbeat and is not an armed-writer period.
The listed startup span still identifies that unserviced prefix.

**1x1 duty opportunities, maxima over all four plans.**

| Duty | Longest no-tick span ms | Plan at maximum | TX allowance ms | Conditional period ms | 500 ms margin | 2,000 ms margin |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| Boot to entity enabled | 312.73952 | `uart-paced` | 0.00000 | Unarmed prefix | N/A | N/A |
| AEM copy/CRC | 57.99594 | `uart-paced` | 0.00000 | 307.99594 | 192.00406 | 1692.00406 |
| Binding restore walk | 0.01111 | `all` | 0.00000 | 250.01111 | 249.98889 | 1749.98889 |
| Journal erase envelope | 20.14069 | `device-wait` | 9.89583 | 280.03652 | 219.96348 | 1719.96348 |
| Journal START-to-ACK | 121.19479 | `device-wait` | 9.89583 | 381.09062 | 118.90938 | 1618.90938 |
| `milan_status` | 15.54534 | `uart-paced` | 28.47222 | 294.01756 | 205.98244 | 1705.98244 |
| `milan_gettime` | 2.31391 | `all` | 5.20833 | 257.52224 | 242.47776 | 1742.47776 |
| `milan_settime`, maximum tested case | 5.17229 | `all` | 8.50694 | 263.67923 | 236.32077 | 1736.32077 |
| `milan_utc`, maximum tested case | 5.97003 | `all` | 9.46181 | 265.43184 | 234.56816 | 1734.56816 |
| `milan_nvm` status | 220.48254 | `uart-paced` | 32.55208 | 503.03462 | -3.03462 | 1496.96538 |
| `milan_nvm commit` | 137.09021 | `all` | 9.89583 | 396.98604 | 103.01396 | 1603.01396 |
| `milan_nvm wipe`, whole command | 40.34359 | `all` | 11.54514 | 301.88873 | 198.11127 | 1698.11127 |
| Wipe erase envelope, maximum of two | 20.39232 | `uart-paced` | 11.54514 | 281.93746 | 218.06254 | 1718.06254 |
| `milan_nvm invalid` | 1.96577 | `all` | 5.38194 | 257.34771 | 242.65229 | 1742.65229 |

**8x8 duty opportunities, maxima over all four plans.**

| Duty | Longest no-tick span ms | Plan at maximum | TX allowance ms | Conditional period ms | 500 ms margin | 2,000 ms margin |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| Boot to entity enabled | 954.12026 | `uart-paced` | 0.00000 | Unarmed prefix | N/A | N/A |
| AEM copy/CRC | 137.01392 | `uart-paced` | 0.00000 | 387.01392 | 112.98608 | 1612.98608 |
| Binding restore walk | 0.01111 | `all` | 0.00000 | 250.01111 | 249.98889 | 1749.98889 |
| Journal erase envelope | 74.51875 | `device-wait` | 9.98264 | 334.50139 | 165.49861 | 1665.49861 |
| Journal START-to-ACK | 470.23145 | `device-wait` | 9.98264 | 730.21409 | -230.21409 | 1269.78591 |
| `milan_status` | 15.54488 | `uart-paced` | 28.47222 | 294.01710 | 205.98290 | 1705.98290 |
| `milan_gettime` | 2.32535 | `all` | 5.20833 | 257.53368 | 242.46632 | 1742.46632 |
| `milan_settime`, maximum tested case | 5.17229 | `all` | 8.50694 | 263.67923 | 236.32077 | 1736.32077 |
| `milan_utc`, maximum tested case | 5.97003 | `all` | 9.46181 | 265.43184 | 234.56816 | 1734.56816 |
| `milan_nvm` status | 800.91654 | `uart-paced` | 32.72569 | 1083.64223 | -583.64223 | 916.35777 |
| `milan_nvm commit` | 523.18408 | `uart-paced` | 9.98264 | 783.16672 | -283.16672 | 1216.83328 |
| `milan_nvm wipe`, whole command | 148.49474 | `uart-paced` | 11.54514 | 410.03988 | 89.96012 | 1589.96012 |
| Wipe erase envelope, maximum of two | 74.76972 | `uart-paced` | 11.54514 | 336.31486 | 163.68514 | 1663.68514 |
| `milan_nvm invalid` | 1.96577 | `all` | 5.38194 | 257.34771 | 242.65229 | 1742.65229 |

These conditional duty comparisons do not bound a queued schedule.
Continuously available console input suppresses the BIOS idle hook.
Several individually short handlers can therefore concatenate into an
unbounded no-tick interval until a handler that polls, or an input gap, permits service.
The heartbeat function checks the PHC; the time-setting cases deliberately
change that clock, while the measurement's event counter stays monotonic.
The finite plan results below retain their actual strobe timings.

The `uart-paced` plan spaces both directions at 115,200 baud without operator think time.
It rounds a frame upward to 8,681 system cycles; unchanged public P1 uses 8,680.
It permits idle calls between received characters and includes TX blocking.
`queued-input` uses twelve NVM status commands then register status at 1x1,
matching public P3's 133-byte plan; at 8x8 it uses three then register status,
extending public PD with a final `PP_STAT[6]` sample.
It models immediate succession at each prompt, not simultaneous RX-ring injection.

| Shape / plan | Largest observed gap ms | 500 ms margin | 2,000 ms margin | Gap endpoints ms | Final tail? | Printed backing samples |
| --- | ---: | ---: | ---: | --- | --- | --- |
| 1x1 / `all` | 430.62305 | 69.37695 | 1569.37695 | 942.86687 to 1373.48992 | Yes | 1, 1, 1, 1, 1 |
| 1x1 / `uart-paced` | 332.34992 | 167.65008 | 1667.65008 | 312.74513 to 645.09505 | No | 1, 1, 1, 1, 1 |
| 1x1 / `queued-input` | 2569.49201 | -2069.49201 | -569.49201 | 252.58315 to 2822.07516 | Yes | 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0 |
| 1x1 / `device-wait` | 250.00968 | 249.99032 | 1749.99032 | 252.58315 to 502.59283 | No | 1 |
| 8x8 / `all` | 1449.77764 | -949.77764 | 550.22236 | 3390.63747 to 4840.41511 | No | 1, 1, 1, 1, 1 |
| 8x8 / `uart-paced` | 991.91598 | -491.91598 | 1008.08402 | 954.12589 to 1946.04187 | No | 1, 1, 1, 1, 1 |
| 8x8 / `queued-input` | 2513.33593 | -2013.33593 | -513.33593 | 893.96257 to 3407.29850 | Yes | 1, 1, 0, 0 |
| 8x8 / `device-wait` | 588.61054 | -88.61054 | 1411.38946 | 893.96257 to 1482.57311 | No | 1 |

The maximum is from one strobe to the next, or from the last strobe to the final prompt.
A final tail is right-censored; it is not a completed heartbeat period.
Printed backing samples are listed in command order, with `PP_STAT[6]` used
for register status. A printed one does not prove uninterrupted backing.
The backend's **2,000 ms T-NVM-WRITER-ALIVE** is separate from the 500 ms period rule.

The `all` 1x1 maximum starts in the second commit and spans its tail,
the following NVM status and wipe, and the remaining console cases through final status.
The `all` 8x8 maximum spans the second commit's tail, the following NVM status,
and the start of wipe. Only two system cycles of prompt-to-next-input spacing
separate those three 8x8 commands; that is not an idle-service opportunity.
Both paced maxima span startup after the first heartbeat and the initial
register-status, get-time and NVM-status commands.
The device-wait maxima span startup and the first commit.
Both queued maxima span startup after the first heartbeat and the complete
queued status sequence through final register status.

In P3, the last printed one is command 8, completed by 2,188.86040 ms;
command 9 prints zero by 2,397.34614 ms, and the final register sample is zero.
In the corrected 8x8 queued plan, backing samples are 1, 1, 0, 0.
Public PD directly observes the backend clear backing at 2,893.00065 ms,
1,999.03810 ms after its only kick, with `stale=1` and `alive=0`.
The millisecond countdown phase explains the small difference from 2,000 ms.

The public probes were extracted from
[the review evidence branch](https://github.com/kebag-logic/milan-fpga/tree/397-review-evidence)
and executed unchanged. Shell wrappers that background jobs or pipe results
were replaced by foreground invocations of their unchanged probe programs.
P1, P2 and P3 logs reproduced byte-for-byte.
Removing only the new passive observation lines from the corrected immediate
1x1/8x8 `all` logs reproduces the original external event/UART streams.

| Public probe | Executed scenario | Result |
| --- | --- | --- |
| P1 | 1x1 paced full command plan | CSR gap 332.34734 ms; printed backing samples remain one |
| P2 | 1x1 full plan, 1 s erase / 5 ms page WIP | CSR gap 412.37988 ms; four heartbeats per erase, maximum spacing 250.00068 ms; printed backing samples remain one |
| P3 | 1x1 twelve queued NVM status commands, then register status | CSR tail 2569.49201 ms; backing falls to zero |
| PA | 1x1 independent full-plan observer | Original raw stream reproduced; no backing lapse; AEM read-completion-to-enable 55.76477 ms |
| PC | 8x8 independent 3 s erase / 5 ms page commit | Commit 4307.68299 ms; START-to-ACK 3856.72710 ms; fabric-kick gap 588.61054 ms; no backing lapse; twelve erase heartbeats at up to 250.00068 ms spacing |
| PD | 8x8 three queued NVM status commands | Fabric-kick tail 2505.57721 ms; direct backing lapse and final printed zero |

The executed queued runs demonstrate a liveness defect in each shape.
The scope remains measurement only: the dispatch/long-loop service repair
belongs to #590, within the manager's one-hart direction.
A short ordinary schedule with all printed samples set does not establish queued-input safety.

## Device waits and substitution limits

Erase and page waits are independent inputs.
The supported ranges include the cited device maxima: 3,000,000 us per erase
and 5,000 us per page; out-of-range values fail before building or simulating.
The largest supported command plan has four erases and 100 pages, or 12.5 s WIP.
Measured no-WIP work leaves room under the unchanged 30-second guard.
This is a supported-scenario limit, not a bound on arbitrary stalls.

The following are **executed** `device-wait` runs with 3 s erase and 5 ms page WIP.
They replace the previous additive device-corner projection for these duties.
The 13-page and 50-page commits contain exactly 3,065 and 3,250 ms modeled WIP.

| Shape / device-max duty | CPU cycles | Service ms | WIP ms | Measured ms | Budget ms | Margin ms |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1x1 / Erase envelope | 151,005,855 | 20.11709 | 3000 | 3020.11709 | 3,500 | 479.88291 |
| 1x1 / Journal START-to-ACK | 161,067,660 | 156.35320 | 3065 | 3221.35320 | 8,000 | 4778.64680 |
| 1x1 / Whole console commit | 166,979,731 | 274.59461 | 3065 | 3339.59461 | 8,000 | 4660.40539 |
| 8x8 / Erase envelope | 153,725,874 | 74.51747 | 3000 | 3074.51747 | 3,500 | 425.48253 |
| 8x8 / Journal START-to-ACK | 192,836,355 | 606.72710 | 3250 | 3856.72710 | 8,000 | 4143.27290 |
| 8x8 / Whole console commit | 215,384,150 | 1057.68299 | 3250 | 4307.68299 | 8,000 | 3692.31701 |

Service time subtracts only modeled WIP from the elapsed envelope.
It still includes SPI transfers, polling overhead, verification, bus and DDR waits.
The CPU polls during WIP; subtraction does not measure CPU capacity available
to another task. P2 and PC show heartbeat service during long erase polling,
while capture, validation and readback still contain long intervals without it.
The exact no-tick spans for the device-wait plan remain in its receipt.
A two-sector wipe would add 6,000 ms device WIP; the device-max plan here
executes a commit, not a device-max wipe, so no measured wipe-corner result is claimed.
These runs do not prove the required twofold commit margin on physical hardware.

The SPI stream-boundary substitution is **optimistic**.
The unchanged public PHY probe measured 67 system cycles versus the model's
65 for an 8-bit transfer, and 259 versus 257 for 32 bits.
The first transfer after CS reassertion takes 78 versus 65, adding another
11 cycles relative to steady transfers.
Consequently, modeled service can understate the physical PHY cost.
This is a per-boundary difference, not a uniform percentage correction for whole duties.
DDR uses the existing simulation model; there is no external packet traffic.
Only one deterministic clock phase is exercised.
Field-update writing, fault logging, PHY management, temperature logging and
the remaining persistence duties are unmeasured future work.
Physical liveness torture and the complete architecture decision remain open.

## Controls and validation

The portable oracle pins three fixed traces: both `all` shapes and paced 1x1.
Fixtures contain raw markers and expected analysis, without generated-file
inventories, compiler strings or host header paths.
They pin marker selection, integer conversion, deadlines, duty tick gaps,
backing samples and findings.
A planted final-response delay must fail that command's budget specifically.
A combined control word must not count as the exact standalone heartbeat strobe.
UART reconstruction is exercised where passive events split a printed word.
An exact-budget interval passes; one more system cycle fails.
Missing/out-of-order evidence, dispatch census and wait input limits are checked.
Explicit counter controls also check inter-block gaps, a duty with no calls,
an invalid internal maximum and a block crossing a duty boundary.

The portable gate passes **30 oracle controls and 14 flash controls**.
The unchanged external mutation suite rejects 11/11 mutants; its unmodified
control passes and reproduces both expected analyses.
The unchanged internal suite rejects 15/15 mutants.
Fourteen change or invalidate a recorded analysis; the bitmask mutation is
equivalent on those standalone-write traces and is caught by the added
combined-word marker control instead.
Four unsupported CLI wait cases fail before creating a build directory.
The default queued-input regrade fails with the named heartbeat-budget refusal;
the reporting-mode regrade retains that finding and returns zero.

The unchanged mutation scripts ran in a disposable harness mirror.
That mirror supplied the two round-2 `all` receipts at the scripts' legacy
lookup paths; those compatibility files are not in the product tree.

The flash busy-refusal control prepares WEL at completion, then explicitly
tests an earlier busy cycle. This isolates the busy predicate independently
of WEL; it is a nonmonotonic predicate test, not a physical command sequence.
Removing the busy check makes this named control fail.
The default grader retains a receipt then refuses any budget finding.
`--record-budget-findings` prints and retains every refusal while allowing
measurement completion. Its success is not timing approval.
Missing markers, invalid interval ordering and a changed bound log still fail.

The assignment's host, capture, feature, documentation, whitespace and builder
gates returned zero. The full builder bank also returned zero; its calibration
arm did not run because the physical utilization report is absent.
All elaboration arms ran; no claim is made for the missing calibration arm.
Source-idiom, hygiene and test-evidence checks returned zero.
These are author validation results, not review verdicts.

## Reproduction and evidence

Follow the [harness recipe](../../tb/verilator/fw_service_budget/README.md#run-and-reproduce)
with separate external build directories for each scenario.
The Makefile's default target runs portable controls only.
Build reuse verifies generated inputs, BIOS, ELF and native executable hashes.
Receipts retain the raw UART/event text, its digest and the build/input inventory.
Bound-log regrading verifies the raw digest and unchanged compiled inputs.
Analysis-only corrections were regraded from preserved successful native runs.

The CPU netlist SHA-256 remains
`c208df0b7fafcaab190dba3f1734f2a38acd54645b33a834b0e59282e6a7813d`.
The unchanged firmware source SHA-256 remains
`0bf43cd4fe02b110fb1ae4f051b3bc7baa6bb62c3769962520ed1f4bd12247a6`.
The existing dependency revisions and capture hashes remain intact.
Product patches are unchanged; the physical GMII patch is not exercised
because this simulation has no MAC.

Raw per-run receipts were removed from `docs/findings/`.
The handoff evidence packet contains the original receipts and all eight
round-2 receipts; only summary tables remain here.
The packet is prepared for the manager to publish; this lane has no push authority.
The following SHA-256 values identify the complete receipt files, including their raw logs.

| Receipt | SHA-256 |
| --- | --- |
| `round1-1X1.json` | `7063dc22566acd341af23aab33efbc1aea1b20ab475dece30224fb90fde2b80f` |
| `round1-8X8.json` | `d5f15a116e3037caec6b4601b6e810ba2927768f037e4d0fba4f8633dd296971` |
| `round2-1x1-all.json` | `1839bb8ec891bcbfb7ebb83f78bf94ebdbd105aa4c99bd27f16479b2b03ea865` |
| `round2-1x1-device-wait.json` | `6f5e8816a592161fd54a07147bf9921434710b7c31a6bd1e69349867f2539025` |
| `round2-1x1-queued-input.json` | `97b9ec9d89b56c5c90a301ec104fcad95cb3f40a32d8ef1f9162aca2b59717f5` |
| `round2-1x1-uart-paced.json` | `2c6202502147e2e12fe50afa6d78f814162c7e4f075c8400558c7a7f610f552f` |
| `round2-8x8-all.json` | `b68a1c4cb31f17ed87a244817d10cebdda72eacc54fad152acaf17e1291b6467` |
| `round2-8x8-device-wait.json` | `aecbf0521ba19004c8c1c224a50d4d40e46c9ee0ff52aa94f41d447c29c63c2f` |
| `round2-8x8-queued-input.json` | `231538aa71fb8f5af13e69988f338ed912ce97414bfdc069e71e1dd7218ae966` |
| `round2-8x8-uart-paced.json` | `8fa6a0be185b758b8fcb3e89b750a6b447dc9ea3886347e32f075bdeafc4b068` |

For the `all` cases, use zero waits at 1x1 and `--device-wait-us 1000
--program-wait-us 1000` at 8x8.
Use zero waits for `uart-paced` and `queued-input`.
Use `--device-wait-us 3000000 --program-wait-us 5000` for `device-wait`.
All cases use `--populated --record-budget-findings`.
Append `--regrade` with identical arguments to recheck an existing bound log.

```sh
python3 -B tb/verilator/fw_service_budget/run.py --self-test
python3 -B sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
python3 -B scripts/check_nvm_capture.py
python3 -B scripts/check_feature_status.py --self-test
python3 -B scripts/pp_srcs.py --check
python3 -B scripts/check_baremetal_only.py --check
python3 -B scripts/check_entity_shape.py --self-test
python3 -B scripts/docs_check.py
python3 -B scripts/check_doc_paths.py
python3 -B scripts/check_doc_style.py
python3 -B scripts/check_archive.py
python3 -B scripts/gen_toc.py --check
python3 -B scripts/check_em_dash.py --base ac18b50968b12efe4d15c0a06301264b35656b31
git diff --check
```
