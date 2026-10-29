<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# reboot_ctrl -- the end-station reset on an AECP REBOOT

`make` - exit 0 = PASS. It builds and runs the harness, **133 checks with zero failures**, then `mutants.py`'s
golden run and **sixteen planted mutants, each caught by its own named check**. The suite carries no `-Wno-*`, so any
Verilator warning stops the build.

**What this suite owns.** [`KL_reboot_ctrl`](../../../hdl/milan/KL_reboot_ctrl.sv) as a module (issue #787): the
saved-state drain, the PHY hold and the IPROG words on the ICAPE2 port, graded against the values
[`docs/design/REBOOT_RESET.md`](../../../docs/design/REBOOT_RESET.md) documents. The path from an AECP REBOOT on the
wire, through the processor and `KL_pp_shadow`, to the same outputs at `milan_datapath`'s ports is
[`pp_shadow`](../pp_shadow/README.md)'s section `[RB]`.

## Contents

- **[What it drives](#what-it-drives)** -- The module at its shipping waits, with only the millisecond compressed
- **[What it grades](#what-it-grades)** -- The twelve scenarios and the documented values each is held to
- **[The planted mutants](#the-planted-mutants)** -- Sixteen defects, the request ignored first, each with the check it must break

## What it drives

The module is built at its **shipping** waits, 10,000 ms of drain and 3,500 ms of PHY hold. The harness drives
`ms_tick_i` itself, one pulse every 8 clocks at a phase each scenario chooses, so a millisecond is 8 clocks and the
bounds are counted in ticks. The expected values are literals in `sim_main.cpp`, never read from the RTL: the two
waits and the eight IPROG configuration words (dummy, sync, NOOP, write WBSTAR, 0, write CMD, IPROG, NOOP), bit-reversed
per byte by the harness's own function before they are compared with the ICAPE2 bus.

## What it grades

| Scenario | Graded |
|---|---|
| U0 | no request: no PHY hold, CSIB high and the dummy word for longer than both waits, while the saved-state status moves |
| U1 | no live writer, with dirty and pending work left behind: the hold two clocks after the request, more than 3,500 ms and at most one tick more, then exactly eight clocks of CSIB low carrying the words, the hold up throughout and after, and the words again after another hold |
| U2 | a durable state: the same, at once |
| U3, U4 | dirty and pending work with a live writer: no hold while it lasts, the hold on the clock the work is durable |
| U5 | a writer that never commits: the drain ends after more than 10,000 ms and at most one tick more |
| U6 | the writer lost during the drain: the hold on that clock |
| U7 | a one-clock request still resets |
| U8 | status moves after the drain end change nothing |
| U9, U10 | a reset during the hold, and in the middle of the words: back to idle at once, no word afterwards |
| U11 | two other tick phases keep the hold inside its bound |

## The planted mutants

`mutants.py` plants each defect in a private copy of the module, builds the harness against it through this
directory's `Makefile` (`CTRL_SRC`, `MDIR`) and requires the run to fail on the named check. A copy that does not build
is not caught by a check, so it fails the driver. Mutant logs stay in the private directory.

| Mutant | Named check |
|---|---|
| `request-ignored` | U1 no writer: the PHY hold rises two clocks after the request |
| `drain-ignores-dirty` | U3 dirty work with a live writer: no PHY hold and no IPROG for 4,000 ms |
| `drain-ignores-pend` | U4 pending work with a live writer: no PHY hold for 1,500 ms |
| `drain-ignores-a-lost-writer` | U6 the writer is lost: the PHY hold rises on that clock |
| `no-drain-deadline` | U5 ...and at most one tick after 10,000 ms |
| `drain-deadline-a-tick-early` | U5 a writer that never commits: the drain ends after more than 10,000 ms |
| `hold-skipped`, `hold-a-tick-short` | U1 the hold is longer than 3,500 ms |
| `hold-a-tick-long` | U1 the hold is at most one tick longer than 3,500 ms |
| `bits-not-reversed`, `wbstar-write-dropped`, `desync-for-iprog` | U1 eight consecutive clocks carry dummy, sync, NOOP, WBSTAR, 0, CMD, IPROG, NOOP, bits reversed per byte |
| `words-repeat-without-a-hold` | U1 CSIB is high again after the eighth word |
| `phy-hold-released-for-iprog` | U1 the PHY hold stays up through the IPROG words |
| `request-not-latched` | U7 a one-clock request: the PHY hold still rises |
| `hold-survives-reset` | U9 a reset during the hold: back to idle, and no IPROG afterwards |

```sh
make -C tb/verilator/reboot_ctrl
python3 tb/verilator/reboot_ctrl/mutants.py --list
```
