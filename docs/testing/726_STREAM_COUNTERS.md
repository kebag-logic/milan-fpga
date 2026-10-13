# Stream counter packet counts and notification gaps

## Contents

- **[Counter contract](#counter-contract)** -- Packet totals, reset edges, and the retained rate limit.
- **[Parent path measurements](#parent-path-measurements)** -- MAC observations at both declared descriptor geometries.
- **[Firmware path](#firmware-path)** -- Mailbox completion timing with delayed transmission.
- **[Reproduction and planted controls](#reproduction-and-planted-controls)** -- Commands, expected failures, and check-omission controls.

## Counter contract

The [2026-10-12 counter ruling](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125741685)
defines FRAMES_TX and FRAMES_RX as per-AVTPDU totals.
IEEE 1722.1-2021 7.4.42.2.5 Tables 7.157 and 7.159 supply their wire meanings.
Both totals wrap at 32 bits.

FRAMES_TX resets at each talker start, including the CRF output.
FRAMES_RX resets on not-bound to bound and survives unbind.
MEDIA_RESET and TIMESTAMP_UNCERTAIN retain their Milan observation intervals.

AAF receive totals retain coalesced publication at the interval commit.
Their pending total also uses 32 bits.
A 16-bit saturating batch lost packets above 65,535 accepted AVTPDUs.
The boundary check seeds 65,534 pending packets and receives three more.
It requires 65,537 after publication.

Every counter update marks its descriptor dirty, including healthy receive traffic.
The previous input producers excluded healthy TV and FRAMES_RX updates.
Consequently, initial input notifications were followed by silence despite advancing counters.

The existing scheduler retains Milan v1.2 5.4.5.2 Table 5.22 spacing.
The [corrected cadence ruling](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6132483068)
replaces the earlier fixed-window criterion with two conditions.
Notifications for each descriptor and recipient respect that spacing.
The [Round 6 precision](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6134121887)
fixes the service allowance at 25 ms.
The 1012.029 ms maximum gap motivated that ceiling, including margin.
Each consecutive gap must therefore be at most 1025 ms.
Measurements cannot enlarge this fixed bound.
The scheduler stamps the latest recipient's completion.
Service adds delay, so notifications drift across fixed one-second bins.
An empty fixed bin can therefore occur on correct behavior.
Fixed bins describe observations; they never decide the verdict.

## Parent path measurements

The [standing fixture](../../tb/verilator/milan_dp/stream_counters.hpp)
uses the actual parser, counter engines, descriptor arbiter, processor and response memory.
It records completed frames at the parent MAC transmit interface.
Two controllers register through AECP before streaming starts.
Every AAF input and the appended CRF input receives continuous valid packets.
All outputs emit concurrently, with silence fill supplying unused audio channels.

The clock parameter remains 50 MHz.
Protocol milliseconds use 1000 simulation cycles; counter intervals use 1,000,000 cycles.
The TDM8 and TDM32 elaborations retain their respective shipping geometry.
Simulation clocks run together; these measurements establish protocol behavior, not physical timing.

Five simulated seconds are recorded for every descriptor and recipient.
Every consecutive gap is graded, starting with the first notification.
There is no startup exclusion or fixed-grid grading.
At least two observations prevent a vacuous gap result.
The final wait also cannot exceed the refresh bound.
Frames after measurement ends are excluded from cadence grading.
Service is measured from dirty eligibility through the final recipient's MAC tail.
Measured service is descriptive only; the fixed ceiling remains 25 ms.
Every gap and final wait must satisfy the 1025 ms bound.

| Shape | Inputs / outputs, including CRF | Recipients | Graded consecutive gaps | Minimum gap | Maximum gap | Maximum measured service |
|---|---|---:|---:|---:|---:|---:|
| Shipping TDM8 | 2 / 2 | 2 | 28 | 1001.000 ms | 1001.867 ms | 3.263 ms |
| Largest TDM32 | 9 / 9 | 2 | 126 | 1000.982 ms | 1012.029 ms | 14.058 ms |

Each input row has four notifications; each output row has five.
The same fixture with `c6bd08c6` engines lacks recurring input notifications.
Its named `CADENCE` failures expose that silence.
The original runs use `uncertain`: every output stamps `tu=1`.
TIMESTAMP_UNCERTAIN changes alongside FRAMES_TX; `mr` stays clear.
Corrected input and output rows satisfy spacing and bounded refresh.

The raw fixed bins retain the observed drift.
Shipping input 0, recipient 0, has an empty bin 1.
The largest shape has that empty bin for both recipients.
Those gaps are about 1001 ms and satisfy the corrected criterion.
They were previously mislabeled as startup transients.
The revised fixture checks every discrete measurement start through one second.
It compares both verdicts at 1,000,001 cycle positions per row.
This includes notification boundaries and the reviewer's sub-millisecond shifts.
Changing measurement origin never changes the corrected verdict.
The `fixed-grid` plant restores the superseded grader.
It fails `PHASE` and escapes only with that check omitted.

Round 2 also measures `frames-only` at both shapes.
Its scratch parent clears uncertainty at both talker inputs.
The actual packetizers stamp those bits into their outgoing AVTPDUs.
The fixture checks clear wire `tu` and `mr` on every output.
TU and MEDIA_RESET counters remain zero throughout these finite runs.
Only the initial start occurs; no stop occurs during measurement.
FRAMES_TX is therefore the only changing output counter during measurement.
This models the locked-PHC condition, without establishing physical synchronization.

| Condition | Output rows | Consecutive output gaps | Total checks |
|---|---|---:|---:|
| `frames-only`, shipping | AAF 0 and CRF 1, both recipients | 16 | 70 |
| `frames-only`, largest | AAF 0 through 7 and CRF 8, both recipients | 72 | 301 |

Their gaps and service maxima equal the table above.
Removing the per-AVTPDU output event fails `OUTPUT_CADENCE`.
That shipping plant escapes when only `OUTPUT_CADENCE` is omitted.

| Shape | Output | Baseline FRAMES_TX | MAC AVTPDUs | Corrected FRAMES_TX |
|---|---|---:|---:|---:|
| Shipping | AAF 0 | 5 | 799 | 799 |
| Shipping | CRF 1 | 5 | 101 | 101 |
| Largest | Each AAF 0 through 7 | 5 | 800 | 800 |
| Largest | CRF 8 | 5 | 101 | 101 |

The fixture also counts each transmitted AAF and CRF AVTPDU at the MAC.
It drains each run before comparing totals, covering start, stop and restart.
Near-wrap seeds test modulo-32-bit addition using actual emitted packets.
GET_COUNTERS reads verify 500 received packets per input and both bind transitions.

The AVB_INTERFACE producer and its #60 throttle are unchanged.
The existing notification integration checks continue to cover that descriptor.
The unbind-order fixture briefly pauses its packet source while pending updates
drain, below the receiver's silence timeout, then resumes after the response.
Its previous quiet-row premise depended on suppressing healthy refresh events.
The response-ordering checks and their planted defects remain in force.
These finite simulations do not measure maximum controller fanout or a physical link.
The reference-peer and controller comparison remains the merge-turn bench check.

## Firmware path

The [firmware gap check](../../tb/verilator/milan_dp/stream_counter_f5.py)
extends the existing mailbox fixture using the unchanged AECP core and adapter.
It generates both descriptor shapes and registers two recipients.
All served Stream Input and Output counters change every ten milliseconds.
A two-millisecond output stall tests completion-based scheduling.

Both shapes grade consecutive gaps from the first notification onward.
They also bound the final wait and reject insufficient observations.
Every millisecond measurement start through one second preserves both verdicts.
The minimum gap is 1000 ms; the maximum is 1002 ms.
The measured stall is 2 ms, with a one-millisecond service polling allowance.
This deterministic fixture retains its stricter 1003 ms ceiling.
That also satisfies the fixed 1025 ms contract.
This tests the observation-port and mailbox contract, not processor instruction timing.
The mailbox `fixed-grid` plant detects phase-dependent grading.
No firmware implementation or saved-state capture input changes.
This opt-in path injects counter-change calls explicitly.
It does not prove a production caller supplies those events.

## Reproduction and planted controls

Set `VERILATOR` to the pinned 5.050 executable.
Use CPython 3.12.3 with PyYAML and the existing firmware test dependencies.
Set `TMPDIR` to disk scratch and `SCRATCH` to a writable evidence directory.
Builds use two workers; run at most two concurrently.

```sh
python3 tb/verilator/milan_dp/stream_counters.py --shape 1 --work "$SCRATCH/stream-1"
python3 tb/verilator/milan_dp/stream_counters.py --shape 8 --work "$SCRATCH/stream-8"
python3 tb/verilator/milan_dp/stream_counters.py --shape 1 --output-condition frames-only --work "$SCRATCH/frames-only-1"
python3 tb/verilator/milan_dp/stream_counters.py --shape 8 --output-condition frames-only --work "$SCRATCH/frames-only-8"
python3 tb/verilator/milan_dp/stream_counters.py --shape 1 --variant before --work "$SCRATCH/before-1"
python3 tb/verilator/milan_dp/stream_counters.py --shape 8 --variant before --work "$SCRATCH/before-8"
python3 tb/verilator/milan_dp/stream_counter_f5.py --shape 1 --work "$SCRATCH/f5-1"
python3 tb/verilator/milan_dp/stream_counter_f5.py --shape 8 --work "$SCRATCH/f5-8"
MAKEFLAGS=" -w" python3 tb/verilator/milan_dp/stream_counters.py --shape 1
make -C tb/verilator/milan_dp counters
make -C tb/verilator/milan_dp counters-mutants
```

Clean checks must exit zero.
Their `RESULT: PASS` lines also appear in the suite log.
Both make exports suppress inherited directory banners explicitly.
Hosted shard 4/5 must retain these results in `suite-logs-4`.
The `before` variant reads the three original counter engines from `c6bd08c6`.
Its driver requires named `TX`, `RX` and `CADENCE` failures.
Any other failure group, missing group or exit status is rejected.
Each mutation driver requires a named failure, then a passing check-omission run.
A crash, compilation error or unrelated failure does not count as detection.
No submodule source changes during these runs.

| Variant | Planted defect | Required failing group |
|---|---|---|
| `tx-interval` | TX counts occupied intervals | `TX` |
| `rx-interval` | CRF RX counts occupied intervals | `RX` |
| `tx-reset` | Previous TX total survives start | `TX_RESET` |
| `aaf-reset` | Previous AAF RX total survives bind | `RX_RESET` |
| `crf-reset` | Previous CRF RX total survives bind | `RX_RESET` |
| `rx-saturation` | AAF pending total saturates at 65,535 | `RX` |
| `late` | Parent suppresses input change events | `CADENCE` |
| `egress-stall` | Parent holds eligible control frames for 900 ms | `CADENCE` |
| `rate` | Parent supplies a timer divisor halved in error | `RATE` |
| `tx-nodirty` | Output packet event removed under `frames-only` | `OUTPUT_CADENCE` |
| `fixed-grid` | Superseded fixed-bin grader | `PHASE` |
| Firmware `fixed-grid` | Fixed-bin mailbox grader | `PHASE` |
| Firmware `late` | Completion deadline advances by 2000 ms | `CADENCE` |
| Firmware `rate` | Completion deadline advances by 500 ms | `RATE` |

The standing egress plant runs at both shapes.
It delays frames before the parent's control transmit arbiter.
Each run fails `CADENCE` and escapes with that check omitted.
The unchanged review probes also plant 1600/2000 ms scheduler spacing.
Those and the reviewer's egress stall must fail `CADENCE`.
Measured service cannot excuse these planted refresh failures.

The required behavior gate includes the bind-era and receive-law contracts.
Round 3 adds the unpublished-zero receive snapshot to the standing contract.
Three accepted packets give TV=3, TNV=0 and FRAMES_RX=0 before publication.
That snapshot is inconclusive; after publication FRAMES_RX=3 passes the identity.
A measured flowing window still rejects interval-rate FRAMES_RX.

The cross-device helpers apply Tables 7.159/7.157 to both packet totals.
A per-AVTPDU pair passes; an interval-rate side receives its own finding.
Concurrent-flow checks require the measured shared window for a packet-rate PASS.
Matching positive deltas without a measured duration remain inconclusive.
The historical helper and assertion identifiers remain compatible with existing callers.
Their `tx_ticks` and `rx_ticks` fields now mean packet deltas.
Compare matching traffic within one streaming or binding era.
The rate band separates supported AAF/CRF traffic from one-per-second regressions.
Packet comparisons separately allow the documented non-atomic snapshot skew.

```sh
cd tests
python3 -m behave --no-capture -f plain
cd ..
python3 tb/tools/torture_campaign.py --self-test
```

Run the complete [documentation workflow](../../.github/workflows/docs.yml) locally.
Install its pinned dependencies before running its commands.
Every gate must return zero without increasing ratchet budgets.
This includes boundary units, evidence readers, and language idioms.
Retain each command's result, including explicit environment-dependent skips.
