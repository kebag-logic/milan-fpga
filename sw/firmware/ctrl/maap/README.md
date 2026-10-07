<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Bare-metal MAAP

F2 supplies an opt-in MAAP owner for the control loop.
The shipping image still uses the fabric owner.
IEEE 1722-2016 Annex B defines the protocol.
The [service contract](../../../../docs/reference/FR_NFR.md#342-control-service-test-hooks)
defines H-MAAP; host evidence does not establish target or wire timing.

## Contents

- **[Core](#core)** -- Annex B state, wire, randomization and bounded storage.
- **[Integration](#integration)** -- Mailbox ownership and existing stream CSR output.
- **[Service evidence](#service-evidence)** -- Observation points, work bounds and proof limits.
- **[Verification](#verification)** -- Unit, coverage, mutation and differential gates.

## Core

[`maap.c`](maap.c) implements B.3.2/Table B.7 in static storage.
Each interface owns an INITIAL, PROBE or DEFEND state and one timer.
ReserveAddress sends an initial PROBE, then three retransmissions.
The last retransmission precedes ANNOUNCE and acquisition publication.
B.3.3/Table B.8 supplies the timer constants and retransmission count.
B.3.5.5 and B.3.6.4 select conflict handling by state and reversed-octet MAC priority.
B.3.6.6 sends DEFEND to the requesting source, echoing its range and the intersection.
Loss withdraws the old allocation before selecting and probing another range.
Release stops the timer, drops obsolete output and leaves INITIAL.
Starting with a down link also withdraws the previous allocation.
A supplied Begin range survives until the first operational port.
Table B.7 note a governs that saved-range reuse.
Conflict Restart draws again, after consuming the supplied range.

B.2 encoding uses control_data_length 16, MAAP version 1 and a zero stream ID.
Frames are padded to 60 bytes; the receiver accepts the complete 42-byte minimum.
Known messages from older or future MAAP versions follow B.2.3.
It rejects truncated data, invalid AVTP headers and nonmatching destinations.
Only DEFEND may use the receiving interface's unicast MAC.
B.4 limits allocations to the dynamic pool, including the final fitting range.

A maximal-period xorshift32 uses the low MAC-plus-clock sum from B.3.6.1.
A zero seed becomes one; deterministic rejection sampling removes modulo bias.
Draws reserve the service allowance at both strict interval endpoints:
511 to 589 ms for probes, 30011 to 31989 ms for announcements.
With at most 10 ms jitter at each commitment, intervals remain strictly inside
B.3.4.2's 500/600 ms and B.3.4.1's 30/32 s endpoints.
Wire egress error still needs measurement before a placement switch.

Sixteen static frame slots retain ordered output across backpressure.
Each call attempts at most two sends; overflow is counted as unserved work.
A stalled timer retains its original expiry obligation until output drains.
An over-budget recovery is still a timing failure.
Every public event entry guards synchronous reentry: debug builds assert;
release builds count and ignore the nested call, as required by #678.
Initialization is permitted only before binding ports.

| IEEE 1722-2016 clause | Implementation obligation |
|---|---|
| B.2.1, B.2.2, Table B.1 | Ethernet destination, source, length and defined message types |
| B.2.3.1 through B.2.3.4 | Current version and compatible reception across versions |
| B.2.4 through B.2.8 | Zero stream ID, requested range and conflict intersection fields |
| B.3.2, Table B.7 | Ordered state actions, ignored cells, acquisition and conflict retry |
| B.3.3, Table B.8 | Retransmission count and timer constants |
| B.3.4.1, B.3.4.2 | Strict randomized announcement and probe intervals |
| B.3.5.1 through B.3.5.4 | Begin, release, restart and reserve events |
| B.3.5.5 through B.3.5.9 | Conflicting receive events, count exhaustion and operational port |
| B.3.6.1 through B.3.6.4 | Address draw, counter initialization/decrement and MAC comparison |
| B.3.6.5 through B.3.6.7 | PROBE, DEFEND and ANNOUNCE transmission actions |
| B.4, Tables B.9 and B.10 | Dynamic address pool and reserved protocol multicast address |

## Integration

[`maap_mbx.c`](maap_mbx.c) binds the FC `maap` channel and indexed link events.
Each interface has a distinct timer slot and generation tag.
Stale expiries and foreign interface records cannot change its state.
The contract's single MAAP range filter covers the envelope of live ranges;
the indexed core performs the exact overlap test.
Ports return without blocking and must never invoke a core synchronously.

Call `ctrl_app_start_maap` with an allocation callback for the experimental composition.
It preserves ADP startup, uses separate timer slots and opens ADP plus MAAP.
MAAP reception enables its interrupt alongside ADP and events.
The ordinary `ctrl_app_start` remains the ADP-only entry point.
No builder placement switch or shipping firmware entry point changes.

[`maap_csr_allocation`](maap_csr.c) names the allocation output interface.
Its ordered `maap_csr_port` accesses target the existing datapath CSR window
for the selected interface, documented in the [register map](../../../../docs/reference/REGISTER_MAP.md).
The platform supplies those read/write operations and exclusive stream-window ownership.
The callback first clears AAF and CRF admission and fabric MAAP enable.
It writes AAF stream zero through 0x658/0x65c, later AAF streams through
STRM_SEL and 0x81c/0x820, then CRF through 0x75c/0x760.
Stream k receives base+k; CRF receives base+AAF-output-count.
It restores STRM_SEL and the supplied boot-policy controls after programming.
A count mismatch leaves admission closed and increments a refusal counter.
Loss closes admission immediately; no register definitions change.

The platform must quiesce pre-existing media before first ownership transfer.
The host CSR tests establish ordered programming, not fabric frame quiescence.
The later placement integration owns target bus arbitration and boot-policy binding.

Clearing `MAAP_CTRL[0]` disables the fabric `KL_maap` engine.
Then `KL_pp_maap_shim` cannot answer ALLOC_DA successfully.
The processor's `talker_active` consequently never asserts.
Programmed destinations alone cannot admit the current fabric talker.
Before using this output, integration must supply that allocation.
Feed the processor's MAAP face from the firmware allocation,
or move ACMP onto the core through F3.
This is a #664 decision 3 default-flip condition.
F2 records the dependency; it does not change that wiring.

## Service evidence

H-MAAP records original RX_HEAD publication or the armed timer deadline,
then observes the accepted complete MAAP TX_HEAD write.
The host's monotonic model clock is independent of PHC time.
It assigns 100 ns per ordered mailbox access, with 1 ms timer resolution.
These are explicit simulation assumptions, not a measured core clock.
The required project service limit is 10 ms, below the shared 50 ms ceiling.

A 60-byte send costs 19 mailbox accesses; an arm costs three including the clock read.
A cancel costs one and filter publication costs three.
The final probe expiry costs at most 48 accesses: two sends, two arms,
one cancel and allocation publication.
Receive and per-interface poll callbacks also have a conservative 48-access bound.
This excludes the allocation callback's separate datapath CSR accesses;
that callback must remain bounded and nonblocking.
A standalone MAAP loop pass costs at most
8*(6+48) + 2*(20+48) + interfaces*48 accesses: 616 for one interface, 664 for two.
The receive bound includes the channel's maximum 64-byte record.
Other protocol callbacks must be added for a composed loop.

Tests include event and receive backlog, timer wrap, stale tags, link loss,
short TX stalls and an 11 ms stall that must fail the original bound after recovery.
The full-ring case cannot restart its clock when room returns.
Host results prove access counts and model-time assertions only.
Target CPU time, CSR arbitration, egress, NVM overlap, all placement combinations,
audio deadlines and bench acceptance remain later integration obligations.

## Verification

The control gate runs the core/CSR tests and H-MAAP at one and two interfaces.
Release coverage measures the original portable C sources.
The debug assertion has a separate expected-abort test.
The regular RV32 object gate uses `-DNDEBUG`.
A debug RV32 compile also passes with the assertion header.
Target debug linkage still needs a runtime `__assert_fail` handler.
New firmware must have 100% line and branch coverage without exclusions.
`maap_mutants.py` plants protocol, wire, timer, ordering, adapter and output defects;
the named test and failure text must match, not merely a failed executable.
Generic predicate defects supplement the fixture-specific Table B.7 controls.
R528-1 and R529-1 supplied the added regression probes.
The campaign can be partitioned with `--self-test --mutation-shard INDEX COUNT`.
Run every zero-based index to cover the complete campaign.

```sh
MILAN_RV32_CC=riscv64-elf-gcc python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 sw/firmware/gtest/tally_selftest.py
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 sw/firmware/ctrl/test/maap_differential.py --self-test
```

Use the repository-pinned simulator for the last command.
Set TMPDIR to disk-backed scratch before running the gates.
The differential drives shared probe, per-state conflict, loss and retry stimulus
through the C core and the parent MAAP engine.
Annex B is the oracle for both.
#686 conformed the parent on the six deviations this differential recorded:

- Four PROBEs, the first at Begin! (Table B.7), not three delayed ones.
- Probe draws strictly inside 500/600 ms (B.3.4.2), not 500..627 ms.
- Control-data length 16 (B.2.1), not 28.
- DEFEND to the triggering PROBE's source (B.2.1), not to the multicast address.
- ANNOUNCE conflicts judged on the requested range (Table B.7), not the conflict fields.
- Announcement draws strictly inside 30/32 s (B.3.4.1), not 3..5.047 s.

The parent's frames now equal the core's for every shared stimulus.
The parent deviations that remain are listed in the
[fabric MAAP contract](../../../../docs/design/MAAP_FABRIC.md#annex-b-contract).
This stimulus does not reach them.
The differential observes software deadlines and parent frame completion cycles.
Equal-length frames make completion intervals equal send intervals.
A send at an arbitrary tick phase observes up to 1 ms less than the parent's draw.
Varying the start phase reaches both ends of the parent's 518..581 ms draw.
Firmware sends span both 511/589 ms guarded draw boundaries.
Named controls reject 1, 500 and 600 ms probe intervals.
Separate controls falsify the parent probe bound and count expectations.
