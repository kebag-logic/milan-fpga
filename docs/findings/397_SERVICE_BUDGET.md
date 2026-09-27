# Firmware service intervals at 50 MHz

This records the measurement-only scope of [issue #397](https://github.com/kebag-logic/milan-fpga/issues/397#issuecomment-5854787465),
on product base `ac18b50968b12efe4d15c0a06301264b35656b31`. The shipping firmware
and capture harness are unchanged. The one-hart rule remains in force; the
architecture decision and AX7101 liveness torture remain open.

The 8x8 populated-media scenario exceeds the 500 ms service-window comparison
for NVM status and the required maximum heartbeat period. These are measured
budget findings, not timing approval. The final tables below retain their
negative margins.

## Contents

- **[Measured intervals](#measured-intervals)** -- Scenario maxima, marker boundaries and the deadlines used for comparison.
- **[Device waits and proof limits](#device-waits-and-proof-limits)** -- Separates execution from flash waits and identifies what simulation does not establish.
- **[Reproduction and evidence](#reproduction-and-evidence)** -- Commands, input identities, receipts and executable controls.

## Measured intervals

The [sibling harness](../../tb/verilator/fw_service_budget/README.md) runs the
unmodified product translation unit on the shipping cacheless RV32I core.
CPU and system clocks are explicitly 50 MHz and 100 MHz. The BIOS banner
prints the system-clock constant as its CPU frequency; that banner does not
set the driven CPU clock. Receipts retain integer system cycles, and the table
rounds elapsed CPU clock units upward. These are elapsed cycles, not retired
instructions or CPU utilization.
The 8x8 YAML still declares a 100 MHz Milan clock; the harness applies the
assignment's explicit 50 MHz contract through the existing capture recipe.

The measurements below are maxima over the stated deterministic scenarios.
Coverage is one cold boot per shape at a fixed clock phase and the listed
command sequence.
They are not a worst-case execution-time proof for arbitrary bus contention,
arbitrary console input, future duties or the physical board. AEM copy/CRC has
no separate marker, so its bound is the complete reset-to-entity-enable
interval, including NVM boot. Restore's control-write envelope includes real
backend memory handshakes. Each UART envelope includes its input, response
and returned prompt. The command plan covers all five product registrations,
two successive commits, wipe, status, numeric limits and refused arguments.

The populated fixtures contain 53 records / 3,264 bytes at 1x1 and 156 records /
12,680 bytes at 8x8. The AEM images are 7,352 and 18,288 bytes respectively.
The observed restore envelopes contain 8 and 32 backend read handshakes,
with matching responses and no backend errors. This is the current binding
restore walk; it does not implement or time the remaining seven saved-state
items in [section 12.2](../design/SAVED_STATE_FASTCONNECT.md#122-where-they-go-today).

**1x1: populated A/B slots, 0 ms WIP per erase/page.**

| Duty | Elapsed CPU cycles | Elapsed ms | Budget ms | Margin ms |
| --- | ---: | ---: | ---: | ---: |
| Boot to entity enabled | 15,548,512 | 310.97023 | N/A | N/A |
| AEM copy/CRC, enclosed by boot | 15,548,512 | 310.97023 | N/A | N/A |
| Binding restore walk | 1,138 | 0.02276 | 3,000 | 2999.97724 |
| Journal erase envelope | 1,006,829 | 20.13657 | 3,500 | 3479.86343 |
| Journal START-to-ACK | 7,826,455 | 156.52910 | 8,000 | 7843.47090 |
| Maximum heartbeat gap | 21,531,153 | 430.62305 | 500 | 69.37695 |
| `milan_status` | 388,880 | 7.77759 | 500 | 492.22241 |
| `milan_gettime` | 115,696 | 2.31391 | 500 | 497.68609 |
| `milan_settime`, maximum tested case | 258,615 | 5.17229 | 500 | 494.82771 |
| `milan_utc`, maximum tested case | 298,502 | 5.97003 | 500 | 494.02997 |
| `milan_nvm` status | 10,425,165 | 208.50329 | 500 | 291.49671 |
| `milan_nvm commit` | 13,738,559 | 274.77117 | 8,000 | 7725.22883 |
| `milan_nvm wipe`, whole command | 2,017,180 | 40.34359 | N/A | N/A |
| Wipe erase envelope, maximum of two | 1,005,511 | 20.11022 | 3,500 | 3479.88978 |
| `milan_nvm invalid` | 98,289 | 1.96577 | 500 | 498.03423 |

**8x8: populated A/B slots, 1 ms WIP per erase/page.**

| Duty | Elapsed CPU cycles | Elapsed ms | Budget ms | Margin ms |
| --- | ---: | ---: | ---: | ---: |
| Boot to entity enabled | 51,571,981 | 1031.43961 | N/A | N/A |
| AEM copy/CRC, enclosed by boot | 51,571,981 | 1031.43961 | N/A | N/A |
| Binding restore walk | 2,700 | 0.05400 | 3,000 | 2999.94600 |
| Journal erase envelope | 3,775,572 | 75.51143 | 3,500 | 3424.48857 |
| Journal START-to-ACK | 32,909,891 | 658.19782 | 8,000 | 7341.80218 |
| Maximum heartbeat gap | 72,488,882 | 1449.77764 | 500 | -949.77764 |
| `milan_status` | 388,880 | 7.77759 | 500 | 492.22241 |
| `milan_gettime` | 116,268 | 2.32535 | 500 | 497.67465 |
| `milan_settime`, maximum tested case | 258,615 | 5.17229 | 500 | 494.82771 |
| `milan_utc`, maximum tested case | 298,502 | 5.97003 | 500 | 494.02997 |
| `milan_nvm` status | 39,443,853 | 788.87705 | 500 | -288.87705 |
| `milan_nvm commit` | 55,457,868 | 1109.15735 | 8,000 | 6890.84265 |
| `milan_nvm wipe`, whole command | 7,554,712 | 151.09423 | N/A | N/A |
| Wipe erase envelope, maximum of two | 3,774,257 | 75.48514 | 3,500 | 3424.51486 |
| `milan_nvm invalid` | 98,289 | 1.96577 | 500 | 498.03423 |

The ordinary-command comparison uses the 500 ms maximum heartbeat period from
[saved-state section 9.4](../design/SAVED_STATE_FASTCONNECT.md#94-the-deadlines).
It is a service-window budget, not a protocol deadline for UART. Restore and
erase use the firmware's 3,000 ms and 3,500 ms polling limits; the erase
envelope also includes erase verification and the first page transmission.
The commit bracket uses the existing 8,000 ms deadline. The console's commit
envelope is wider because capture and prefill precede START.
The wipe has no single 8,000 ms timer. Each of its two erase envelopes is
compared with 3,500 ms: the first ends at the second accepted erase, and the
second at the returned UART prompt. Both include verification and some
surrounding service. Page-program activity is included in the commit bracket;
no separate last-WIP-poll marker is recorded, so an isolated margin against
the 50 ms program polling limit is not claimed.

Milan v1.2 section 5.6.3 specifies ADP `valid_time = 10` and an advertisement
period of 5 s. It does not establish a power-on-to-entity-enable deadline.
Accordingly boot and AEM have no claimed numeric deadline or margin here.
IEEE 1722.1-2021 section 9.3.2.6's AECP response timing belongs to the fabric,
consistent with NFR-SCOUT-03; it is not assigned to this control hart.

## Device waits and proof limits

The flash model gives each serial bit eight system cycles, then one completion
cycle per transfer. Its configured erase/program WIP durations are explicit
scenario inputs. CPU-side service is measured elapsed time minus those WIP
spans; it still includes bus and DDR waits, serial transfers, polling overhead
and verification. The CPU polls during WIP, so this decomposition cannot be
read as idle CPU time available to another duty.

The existing [device maxima](../design/SAVED_STATE_FASTCONNECT.md#94-the-deadlines)
are 3,000 ms per 64 KiB erase and 5 ms per page program. They give 3,065 ms
of device wait for the 3,264-byte/13-page 1x1 image and 3,250 ms for the
12,680-byte/50-page 8x8 image. A two-sector wipe has 6,000 ms of device wait.
Those waits must be added to service work; the design page's wire read-back
term alone is not the CPU's complete transaction cost. The tables keep
measured intervals and device-limit projections distinct.

| Shape / operation | Measured service (ms) | Modeled WIP (ms) | Device maxima (ms) | Conditional total (ms) |
| --- | ---: | ---: | ---: | ---: |
| 1x1 journal START-to-ACK | 156.52910 | 0 | 3,065 | 3221.52910 |
| 1x1 whole console commit | 274.77117 | 0 | 3,065 | 3339.77117 |
| 1x1 journal erase envelope | 20.13657 | 0 | 3,000 | 3020.13657 |
| 1x1 whole wipe | 40.34359 | 0 | 6,000 | 6040.34359 |
| 8x8 journal START-to-ACK | 607.19782 | 51 | 3,250 | 3857.19782 |
| 8x8 whole console commit | 1058.15735 | 51 | 3,250 | 4308.15735 |
| 8x8 journal erase envelope | 74.51143 | 1 | 3,000 | 3074.51143 |
| 8x8 whole wipe | 149.09423 | 2 | 6,000 | 6149.09423 |

Long device waits exercise more heartbeat-poll iterations. A projection made
by adding datasheet waits to measured short-wait service is conditional on the
same bus service and polling overhead. It is not a measured worst-device run,
a bound on arbitrary arbitration stalls, or proof of the required twofold
commit margin. The physical SPI PHY is replaced at its stream boundary, DDR
uses the existing simulation model, external packet traffic is absent, and
UART transfers have immediate handshakes. The UART byte count gives a
separate 115,200 baud, 8N1 serialization allowance; host pacing can add more.
BIOS CRC, delay and memory-test exclusions are inherited from the capture
SoC. None of these exclusions may be carried into a physical boot-time claim.

The heartbeat observations end at the final command. Clock-setting commands
deliberately change the PHC used by firmware, while the event counter remains
monotonic. A short run with no reported lapse cannot prove the issue's
release-gates torture. The field-update writer, fault log, PHY management,
temperature logging and remaining persistence duties are unmeasured future
work. The manager must account for them before making the hart decision.

## Reproduction and evidence

Use the [harness recipe](../../tb/verilator/fw_service_budget/README.md#run-and-reproduce)
from the repository root. Each shape has a separate external build directory.
The default Makefile target runs only the portable controls. Product simulation
is an explicit build/run, with no firmware substitutions or fast-forwarded
clock intervals. Build reuse verifies source, generated input, BIOS and
executable hashes; receipts also identify the scenario media and raw log.

The dependency revisions match the capture measurement. Existing product
patches are retained, including the cacheless CPU adapter; the physical GMII
patch is not exercised because this simulation instantiates no MAC. The CPU
netlist SHA-256 is
`c208df0b7fafcaab190dba3f1734f2a38acd54645b33a834b0e59282e6a7813d`,
identical to the capture receipt. The unchanged firmware source SHA-256 is
`0bf43cd4fe02b110fb1ae4f051b3bc7baa6bb62c3769962520ed1f4bd12247a6`.
The receipts include dependency revisions, generated SoC and BIOS hashes,
input-file hashes, raw UART/event text and its digest.

The eight oracle controls accept a duty exactly at its budget, plant one
system cycle beyond it, and require the named over-budget refusal. They also
grade the recorded 1x1 trace, delay its final UART response by 500 ms, and
require the specific command refusal; a heartbeat refusal alone cannot pass
that control. Missing and unordered
markers are refused, and the command plan is checked against the product
dispatch. Fourteen independent device checks cover erased media, full pages,
WIP boundaries, WEL, erase, forbidden addresses and page wrapping.

The default invocation fails on a budget refusal after preserving the receipt.
For this measurement-only assignment, `--record-budget-findings` prints and
records those refusals while checking measurement integrity. A successful
measurement gate therefore does not mean every budget was met. The self-test
also requires this reporting path to retain the planted refusal. It does not
relax a threshold or turn an overrun into timing approval.

The committed [1x1 receipt](397_SERVICE_BUDGET_1X1.json) and
[8x8 receipt](397_SERVICE_BUDGET_8X8.json) each contain all 17 command intervals.
The native completion counters are 137,348,992 and 503,436,696 system cycles.
Each scenario completes two acknowledged commits and four erases; page-program
counts are 26 and 100, with 6,528 and 25,360 programmed bytes. The 1x1 scenario
has no measured budget refusal. The 8x8 scenario has three: two populated NVM
status commands and the maximum heartbeat gap. No timing approval is implied.
The largest UART serialization allowance is 33.07292 ms at 8x8; the per-command
counts and allowances remain in the receipts.

Reproduce the recorded scenarios with these arguments after the corresponding
build-only commands in the harness recipe:

```sh
python3 -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_1x1_tdm8 --build-dir /tmp/service-1x1 --reuse-build --populated
python3 -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_8x8 --build-dir /tmp/service-8x8 --reuse-build --populated --device-wait-us 1000 --record-budget-findings
python3 -B tb/verilator/fw_service_budget/run.py --self-test
python3 -B scripts/check_nvm_capture.py
python3 -B scripts/check_feature_status.py --self-test
python3 -B scripts/docs_check.py
python3 -B scripts/check_doc_paths.py
python3 -B scripts/check_doc_style.py
python3 -B scripts/check_archive.py
python3 -B scripts/gen_toc.py --check
python3 -B scripts/check_em_dash.py --base ac18b50968b12efe4d15c0a06301264b35656b31
git diff --check
```

Both measurement runs and their bound-log regrades returned zero. The portable
controls report 14 device checks and eight oracle checks, all passing. Capture
integrity retains all seven controls, and feature-status retains 46/46.
Documentation and whitespace gates pass. Python/C++ idiom, hygiene and test
evidence checks also pass. These are author validation results; independent
review, the architecture decision and physical liveness proof remain open.
