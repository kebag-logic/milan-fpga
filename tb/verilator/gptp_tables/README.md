<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# gptp_tables -- per-table lockstep of the fabric gPTP plane

Issue [#640](https://github.com/kebag-logic/milan-fpga/issues/640), lane M7,
moved five tables of the fabric gPTP plane into another storage form with
identical function. This bench runs the real plane inside the
[`gptp_shadow`](../gptp_shadow) slice bench (tap, frame FIFOs, engine, egress
ledger, launch observer, link guard, PHC) and keeps, beside it, each table in
the storage form it had before. A reference is written under the same
conditions the old RTL used, from signals the change did not touch. It is
compared every cycle with what the table's consumer receives.

| Table | Storage now | Reference | Compared, every cycle |
|---|---|---|---|
| `rx_fifo` | tap frame FIFO carrying the highest enabled lane | the same FIFO with eight `tkeep` bits | ready, valid, overflow/bad/good strobes; data, last and highest lane while valid |
| `tx_fifo` | transmit FIFO carrying the beat's lane count | the old gearbox enables into the eight-bit FIFO | ready, valid, last, data and `tkeep` |
| `ledger` | the egress ledger's type, sequence and tag fields in distributed RAM | reset-cleared registers | the head entry while the ledger holds one |
| `results` | the egress result queue in distributed RAM | reset-cleared registers | the head while it offers a result |
| `timer` | the engine timer's deadlines in distributed RAM | reset-cleared registers | the sweep's deadline distance for an armed slot |

Each table counts its mismatches and the coverage that makes a zero count
informative, and the harness grades both. The stimulus is reproducible from a
fixed seed. A peer answers each of the engine's Pdelay requests, timed from
the engine's own accepted egress result, so the measured link delay is
600 ns. In most phases the peer is a better master, and the engine follows it
as a synchronised slave; in the stall phase the peer stops announcing, so the
engine becomes grandmaster. Around the peer runs a mix of every message type,
malformed, foreign, runt and oversize frames, and corrupted byte enables. The
mix also has bursts that overflow the tap FIFO, long transmit stalls, held
launch records, and warm resets in the middle of traffic.

`mutants.py` plants three defects in each table: a wrong depth, a wrong read
latency and an index alias. It edits private copies of the inputs `make
print-inputs` names, with the slice suite's input copier, and requires each
table's own named lockstep check to fail. Each wrong depth is one the table's
reachable use exposes. The tap FIFO is halved and the timer loses its upper
half. The transmit FIFO keeps 16 of its 256 beats: admission bounds it to
a few frames, so only a shallower FIFO is observable, and the resource gate
prices a deeper one. The ledger and result queue are one entry short, because
the engine keeps only a few entries outstanding and a power-of-two-short table
would alias harmlessly.

```sh
git submodule update --init third_party/verilog-axis gptp-processor   # once
make        # regenerates gptp_ucode.hex, builds, runs, then mutants.py
```

Exit 0 = PASS; the tally line is the record.
