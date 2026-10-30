<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# reboot_ctrl -- the end-station reset on an AECP REBOOT

`make` - exit 0 = PASS. It builds and runs the harness on two legs, **229 checks on the default leg and 47 on the
1 Gb/s leg, zero failures**, then `mutants.py`'s golden run and **33 planted mutants, each caught by its own named
check**. The suite carries no `-Wno-*`, so any Verilator warning stops the build.

**What this suite owns.** [`KL_reboot_ctrl`](../../../hdl/milan/KL_reboot_ctrl.sv) as a module (issue #787): the
saved-state drain, the egress wait and the port's stop, the PHY hold and the IPROG words on the ICAPE2 port, graded
against the values [`docs/design/REBOOT_RESET.md`](../../../docs/design/REBOOT_RESET.md) documents. The path from an
AECP REBOOT on the wire, through the processor and `KL_pp_shadow`, to a MAC's wire-side output and the same outputs at
`milan_datapath`'s ports is [`pp_shadow`](../pp_shadow/README.md)'s section `[RB]`.

## Contents

- **[What it drives](#what-it-drives)** -- The module at its shipping waits and two MAC statements, with only the millisecond compressed
- **[What it grades](#what-it-grades)** -- The eighteen scenarios and the documented values each is held to
- **[The planted mutants](#the-planted-mutants)** -- 33 defects, the request ignored first, each with the check it must break

## What it drives

The module is built at its **shipping** waits, 10,000 ms of drain and 3,500 ms of PHY hold. The harness drives
`ms_tick_i` itself, one pulse every 8 clocks at a phase each scenario chooses, so a millisecond is 8 clocks and the
bounds are counted in ticks. The harness is also the datapath and the MAC around the module. As the datapath it
offers frames at the MAC port and lets a beat through only when `mac_tx_stop_o` allows it, the gate
`milan_datapath` applies. As the MAC it flips `mac_txend_tgl_i` when a frame it was given reaches its PHY, and
raises `mac_flush_i` for a link-guard episode.

Each leg is built at one MAC statement, and the Makefile passes the egress bound that statement derives as an
independent literal, `EGRESS_MS`:

| Leg | Statement | Egress bound | Scenarios |
|---|---|---|---|
| default (`make run`) | the module's default, 32,768 octets at 10 Mb/s | 27 ms rounded up, plus the quiet millisecond: 28 ms | all |
| 1 Gb/s (`make run-1g`) | 11,656 octets at 1,000 Mb/s, the AX7101 `MilanMAC`'s statement when the leg was written | 1 ms rounded up, plus the quiet millisecond: 2 ms | U14 and U17 (`--egress-only`) |

The other expected values are literals in `sim_main.cpp`, never read from the RTL: the waits, the stated bounds and
the eight IPROG configuration words (dummy, sync, NOOP, write WBSTAR, 0, write CMD, IPROG, NOOP), bit-reversed per
byte by the harness's own function before they are compared with the ICAPE2 bus.

## What it grades

| Scenario | Graded |
|---|---|
| U0 | no request: no PHY hold, no stop, CSIB high and the dummy word for longer than every wait, while the saved-state status, the toggle and the flush move |
| U1 | no live writer, with dirty and pending work left behind, nothing in the MAC: the egress wait two clocks after the request, the hold more than one tick and at most two ticks and two clocks after it, then more than 3,500 ms and at most one tick more, exactly eight clocks of CSIB low carrying the words, the hold up throughout and after, the words again after another hold, the stop up to the end |
| U2 | a durable state: the same, and the IPROG word inside the stated durable bound |
| U3, U4 | dirty and pending work with a live writer: no stop and no hold while it lasts, the egress wait on the clock the work is durable |
| U5 | a writer that never commits: the drain ends after more than 10,000 ms and at most one tick more |
| U6 | the writer lost during the drain: the egress wait on that clock |
| U7 | a one-clock request still resets |
| U8 | status moves after the drain end change nothing |
| U9, U10 | a reset during the hold, and in the middle of the words: back to idle at once with the port open, no word afterwards |
| U11 | two other tick phases keep the waits and the durable bound inside theirs |
| U12 | three frames in the MAC at the request: no hold while any is left, then more than one tick and at most two ticks and the crossing after the last one's end; a frame taken on the clock another one's end lands is still counted |
| U13 | a frame half taken when the wait starts, held back in its middle across ticks: no hold and the port open while it is taken, the rest taken, no new frame taken after it, the hold after its end, the stop held through the hold |
| U14 | a MAC that never finishes: the hold after more than the derived egress bound and at most one tick more, inside the stated durable bound |
| U15 | a flush in the wait clears what the MAC held: the hold on the quiet tick, not at the bound |
| U16 | two ends with nothing counted do not wrap the count: a frame taken after them is still waited for |
| U17 | a writer that never commits and a MAC that never finishes, at two tick phases: the IPROG word inside `REBOOT_DRAIN_MS_P` + the egress bound + `REBOOT_HOLD_MS_P` + 3 ms + 8 clocks |

## The planted mutants

`mutants.py` plants each defect in a private copy of the module, builds the default leg against it through this
directory's `Makefile` (`CTRL_SRC`, `MDIR`) and requires the run to fail on the named check. A copy that does not build
is not caught by a check, so it fails the driver. Mutant logs stay in the private directory.

| Mutant | Named check |
|---|---|
| `request-ignored` | U1 no writer: the egress wait starts two clocks after the request |
| `drain-ignores-dirty` | U3 dirty work with a live writer: no stop, no PHY hold and no IPROG for 4,000 ms |
| `drain-ignores-pend` | U4 pending work with a live writer: no stop and no PHY hold for 1,500 ms |
| `drain-ignores-a-lost-writer` | U6 the writer is lost: the egress wait starts on that clock |
| `no-drain-deadline` | U5 ...and at most one tick after 10,000 ms |
| `drain-deadline-a-tick-early` | U5 a writer that never commits: the drain ends after more than 10,000 ms |
| `hold-skipped`, `hold-a-tick-short` | U1 the hold is longer than 3,500 ms |
| `hold-a-tick-long` | U1 the hold is at most one tick longer than 3,500 ms |
| `bits-not-reversed`, `wbstar-write-dropped`, `desync-for-iprog` | U1 eight consecutive clocks carry dummy, sync, NOOP, WBSTAR, 0, CMD, IPROG, NOOP, bits reversed per byte |
| `words-repeat-without-a-hold` | U1 CSIB is high again after the eighth word |
| `phy-hold-released-for-iprog` | U1 the PHY hold stays up through the IPROG words |
| `request-not-latched` | U7 a one-clock request: the PHY hold still rises |
| `hold-survives-reset`, `stop-survives-reset` | U9 a reset during the hold: back to idle, the port open, and no IPROG afterwards |
| `hold-on-the-request-alone` (the PHY hold on the request, the shape silicon ran), `egress-ignores-the-mac-fifo`, `frames-taken-not-counted` | U12 ...and no PHY hold 20 ms later with three frames still in the MAC |
| `egress-without-a-bound` | U14 a MAC that never finishes: the PHY hold still rises |
| `egress-bound-a-tick-short`, `egress-bound-rounded-down` | U14 ...after more than the derived egress bound |
| `egress-bound-a-tick-long` | U14 ...and at most one tick more |
| `egress-without-the-quiet-tick` | U12 the last frame reaches the PHY: from its end the PHY hold rises more than one tick later |
| `egress-ignores-the-frame-at-the-port` | U13 a frame still being taken 3 ms into the wait: no PHY hold |
| `end-read-as-a-level` | U12 two frames still in the MAC: no PHY hold |
| `end-wins-over-a-take` | U12 coincide: the second frame is still in the MAC: no PHY hold |
| `count-wraps-below-zero` | U16 it reaches the PHY: from its end ...and at most two ticks and the crossing later |
| `flush-ignored` | U15 a flush in the wait: from the flush ...and at most two ticks and the crossing later |
| `stop-dropped` | U13 ...then starts no new frame |
| `stop-cuts-the-frame-in-progress` | U13 the egress wait starts with a frame half taken: the port stays open for it |
| `stop-released-at-the-hold` | U13 the port stays stopped through the hold |

```sh
make -C tb/verilator/reboot_ctrl
python3 tb/verilator/reboot_ctrl/mutants.py --list
```
