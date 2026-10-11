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
informative, and the harness grades both. Every table is written, read and
reset in traffic, at every index its use reaches. How full it gets is what
that use allows:

| Table | Reached | Why no further |
|---|---|---|
| `rx_fifo` | full: bursts overflow it; its pointers wrap | - |
| `tx_fifo` | 27 of 256 beats; its pointers wrap; every lane count 0 to 8 through the decode | admission bounds it to a few frames; the engine's frames end in two, four or eight lanes, so the other counts are driven directly |
| `ledger` | 3 of 8 entries; every entry is the head in turn | the engine keeps few frames outstanding |
| `results` | 3 of 8 entries, in the slow-engine phase only; every entry is the head in turn | without that phase the engine takes each result as soon as its dispatch is free, and this stimulus never queues two |
| `timer` | slots 0 to 5 of 8 | the microcode arms no other slot |

The stimulus is reproducible from a fixed seed. A peer answers each of the
engine's Pdelay requests, timed from the engine's own accepted egress result,
so the measured link delay is 600 ns. In most phases the peer is a better
master, and the engine follows it as a synchronised slave; in the stall phase
the peer stops announcing, so the engine becomes grandmaster. Around the peer
runs a mix of every message type, malformed, foreign, runt and oversize
frames, and corrupted byte enables. The mix also has bursts that overflow the
tap FIFO, long transmit stalls, held launch records, and warm resets in the
middle of traffic.

Two test-only forces in the wrapper reach what the traffic does not. In the
slow-engine phase the result face's handshake is held off on both sides for
drawn stretches, so the engine sees no offer and the queue sees no ready.
Results then wait in the queue, and a result is written behind one still
waiting to be taken. Before the traffic starts, with the plane in reset, the
transmit FIFO's lane count is forced to each value 0 to 8. The plane's own
decode must give lanes 0 to count-1, which is what the old gearbox stored.
Count 0 is a never-written FIFO word. The run prints the enables the plane
presented for each count. `waivers.vlt` scopes the lint waiver these forces
need to the three nets they drive.

Limits of the evidence. A lockstep cannot see a column stuck at the only
value the stimulus gives it, because the column then matches its old form.
So the run also takes a census of every column of every table. For each
column it collects the distinct values the plane gave its consumer on the
cycles the lockstep compared that column, and prints them. The transmit
FIFO's lane count is read while a beat is offered, because only then does a
consumer take it. A column with one value must be declared in
[`one_valued.tsv`](one_valued.tsv) with that value, and a declared column must
show exactly that value; otherwise its `<table> values: <column>` check fails.
These are the declared columns. `one_valued.py` writes this table from the
list, and `make` fails if the table is stale.

<!-- one-valued-columns:start -->
| Column | Value | Why this stimulus gives no other | Covered by |
|---|---|---|---|
| `ledger` `tag` | `0x1` | `KL_gptp_txticket` tags every frame long enough to carry its sequenceId, and every frame the engine emits is that long. A tag stuck at 0 is caught here; a tag stuck at 1 cannot be seen here or in the plane. | none |
| `results` `ok` | `0x1` | Every result is a measurement: the run prints 0 lost results. A result is a loss only for an entry a barrier cancelled, an untagged entry, an aborted record, an ineligible PHC window or an unexpected cycle distance, and this stimulus raises no barrier and ties record faults off. `gptp_shadow` drives record faults and barriers, and fails with this column stuck at 1. | [`gptp_shadow`](../gptp_shadow) |
| `results` `gen` | `0x1` | The generation moves only at a barrier, and a reset restores 1; this stimulus raises no barrier (the run prints 0 barriers). The engine carries the generation at event bits 27:24, above its masked claim compare (`TXQ_MASK_C`), and it has no consumer past that compare. | none |
<!-- one-valued-columns:end -->

Coverage is graded over the whole run, not per reset segment. The plane's
transmit FIFO can pop under the departure fence, which can wedge the plane
after a warm reset ([#714](https://github.com/kebag-logic/milan-fpga/issues/714)).
Whether a run reaches it depends on timing. At this seed the plane stays live
after both warm resets, but a regression that silenced it after a reset would
still leave every check green. Per-segment coverage follows the fix of #714.

`mutants.py` plants three defects in each table: a wrong depth, a wrong read
latency and an index alias. Two more aim at what those leave unexercised. The
result queue written at its head instead of its tail must fail `results
lockstep`, which needs a result waiting while the next is written. Odd lane
counts decoded one lane short must fail `tx_fifo decode`. Five more stick one
undeclared column of each table at a single value, and each must fail that
column's `values` check. Four edit the list: the tag column's row made a
comment, the tag declared with another value, and the ledger's type column
declared one-valued must each fail that column's `values` check, and a row
naming no censused column must fail `values: declarations that name no
censused column`. The driver edits
private copies of the inputs `make print-inputs` names, with the slice suite's
input copier, and requires each control's own named check to fail. Each wrong
depth is one the table's reachable use exposes. The tap FIFO is halved and the timer loses its upper
half. The transmit FIFO keeps 16 of its 256 beats: admission bounds it to
a few frames, so only a shallower FIFO is observable, and the resource gate
prices a deeper one. The ledger and result queue are one entry short, because
they hold only a few entries at a time and a power-of-two-short table would
alias harmlessly.

```sh
git submodule update --init third_party/verilog-axis gptp-processor   # once
make        # regenerates gptp_ucode.hex, builds, runs, then mutants.py
```

Exit 0 = PASS; the tally line is the record.
