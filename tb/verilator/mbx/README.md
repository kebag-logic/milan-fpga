<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# mbx: the packet-mailbox fabric skeleton, through both bus adapters

`make` builds and runs three things, exit 0 = all green:

1. `run-wb`: the checks of [`suite.hpp`](suite.hpp) on `KL_mbx` behind
   `KL_mbx_wb` (Wishbone, the on-chip RISC-V's bus);
2. `run-axil`: the same checks on `KL_mbx` behind `KL_mbx_axil` (AXI4-Lite,
   a hard core's bus);
3. `run-cosim`: the control-plane firmware run on the RTL and on the host
   model, one scenario, compared frame by frame.

`make mutants` runs [`mutants.py`](mutants.py), all 30 planted RTL defects;
the default `make` runs four of them (one per leaf, `--quick`).

The contract is [`sw/mailbox/mailbox.yaml`](../../../sw/mailbox/mailbox.yaml);
the design is [MAILBOX_SPLIT.md](../../../docs/design/MAILBOX_SPLIT.md).

## Contents

- **[The top and the bench](#the-top-and-the-bench)** -- One KL_mbx behind the adapter HOST_P selects, driven a clock at a time through real bus handshakes.
- **[What the checks expect](#what-the-checks-expect)** -- Each check group and the contract sentence it grades; the same checks also grade the host model.
- **[The co-simulation](#the-co-simulation)** -- The firmware on the RTL and on the model, one scenario, the same frames at the same millisecond.
- **[Planted defects](#planted-defects)** -- Thirty RTL defects in a scratch copy, each caught by the check it names, after two positive controls; four run in the default make.
- **[Run](#run)** -- The two make targets.

## The top and the bench

[`tb_mbx_top.sv`](tb_mbx_top.sv) is wiring only: one `KL_mbx` and the one
adapter `HOST_P` selects; the other adapter's outputs are driven to zero, so
a check cannot pass through the wrong one. [`bench.hpp`](bench.hpp) drives it
a clock at a time: every host access is a Wishbone or AXI4-Lite transaction
with the bus's own handshake, the ingress stream offers one byte per cycle at
the RTL's pace, the TX sink takes bytes under a programmable ready pattern,
and a modeled millisecond is one `ms_tick_p_i` pulse and 23 idle clocks.

## What the checks expect

The expectations are the contract's sentences, and the frames are written
from the clauses ([`frames.hpp`](frames.hpp)), never from the RTL or the
filter table. Register offsets and field positions are the generated
`mbx_contract.h`.

| Group | What is checked |
|---|---|
| R0, R1 | identity and capabilities, reset values, each writable register's mask, read-only registers ignore writes |
| R2 | a partial-strobe write is refused, counted in BUS_ERR and raises a sticky ERR; a disabled cause leaves the line low; write-1-to-clear |
| F0 to F2 | a closed channel stores nothing; ENTITY_DISCOVER for entity_id 0 or this entity passes, whole, byte k in word 2 + k/4 at bits 8*(k%4); foreign, AVAILABLE, DEPARTING and truncated ADPDUs do not; the RX level and the interrupt follow RX_TAIL |
| C0 to C4 | ACMP by talker or listener entity_id, AECP by target, MAAP range overlap with message types, MSRP and MVRP whole (the MRPDU at byte 14), tagged, foreign and too-short frames nowhere |
| D0, D1 | the ring fills to its last whole record; a frame the space cannot hold, or one over the channel's limit, counts in RX_DROP and never touches an unread record |
| T0, T1 | the token bucket: a burst of its depth, then one frame per refill period |
| X0, X1 | TX records leave byte for byte under backpressure, round-robin between channels; a wrong KIND, a non-zero reserved word, an unknown interface, a short or long LEN, or a payload past TX_HEAD is refused once and flushes the ring |
| E0 to E2 | LINK and GM events with their fields and sequence; a link that flaps while the ring is full posts once, with its level at posting |
| M0 to M2 | a timer expires at its deadline with its arm's tag; a cancel and a replaced arm post nothing; a past deadline expires at once |
| K0 to K2 | no TICK while TICK_CTL.EN is clear; one per period; ticks counted while the ring is full post as one record with the count; clearing EN stops them |
| G0 | GM_HI and DOMAIN read the snapshot GM_LO took |

The host test runs the same `suite.hpp` on the firmware's mailbox model
([`sw/firmware/ctrl/test`](../../../sw/firmware/ctrl/README.md), arm
`model`), so the model and the RTL answer to one set of expectations.

## The co-simulation

[`cosim_main.cpp`](cosim_main.cpp) links the firmware (driver, loop, port
layer, ADP, the app), compiled as C11 exactly as the target builds it, and
answers `mbx_hal.h` once with Wishbone transactions on the RTL and once with
the host model. One scenario runs on each: a link rise, two advertising
cycles, an ENTITY_DISCOVER, a grandmaster change and a shutdown, 21 modeled
seconds. The firmware's random delays are seeded from NOW_MS, so the two runs
must commit the same frames at the same millisecond; they do, five frames.

## Planted defects

`mutants.py` copies the RTL to a scratch directory, writes one defect into
the copy, builds this suite with the Makefile's own recipe
(`make print-vflags`) through the adapter the arm names, and requires exit 1
with a `[FAIL]` naming the arm's check. Both adapters' unmodified builds run
first as positive controls.

| Arm | Defect | Caught by |
|---|---|---|
| `rx-msg-type-ignored` | accept terms ignore message_type | F2, AVAILABLE and DEPARTING not passed |
| `rx-eq-own-is-eq-zero` | eq_own compares with zero | F2, DISCOVER for this entity passes |
| `rx-field-length-unchecked` | a term holds on a truncated field | F2, truncated DISCOVER |
| `rx-writes-past-free-space` | speculative writes ignore the free space | D0, every unread record survives |
| `rx-bucket-never-drains` | a commit takes no token | T0, RATE_DROP |
| `rx-lanes-big-endian` | ring lanes reversed | F1, byte k in word k/4 |
| `rx-subtype-ignored` | classification ignores the subtype | C0, ACMP by entity_id |
| `tx-reserved-word-unchecked` | a non-zero reserved word is sent | X1, counted once |
| `tx-refusal-no-flush` | a refusal leaves the ring | X1, counted once and flushed |
| `tx-fixed-priority` | lowest channel first, always | X0, round-robin |
| `evt-rearm-keeps-tag` | a re-arm keeps the old tag | M1, the second arm's tag |
| `evt-cancel-arms` | a cancel arms | M0, no event by +4 ms |
| `evt-tick-count-lost` | the coalesced count restarts at 1 | K1, every tick |
| `top-tick-always-enabled` | TICK_CTL.EN ignored | K0, no TICK while clear |
| `top-gm-hi-live` | GM_HI read live | G0, the snapshot |
| `top-partial-strobe-accepted` | partial strobes written | R2, the register is left |
| `top-irq-ignores-enable` | IRQ_ENABLE ignored | R2, a disabled cause |
| `rx-maap-empty-count-overlaps` | a requested count of 0 overlaps | C2, MAAP overlap |
| `rx-drop-uncounted` | RX_DROP never moves | D0, counts in RX_DROP |
| `rx-refill-slow` | a token per two refill periods | T1, one refill period |
| `tx-lanes-reversed` | TX byte lanes reversed | X0, byte for byte |
| `evt-link-never-posts` | the LINK source never posts | E0, a LINK event |
| `evt-gm-domain-dropped` | the GM event loses its domain | E1, GM DOMAIN |
| `evt-expires-late` | an expiry one millisecond late | M0, at its deadline |
| `top-irq-enable-unmasked` | IRQ_ENABLE keeps undefined bits | R1, IRQ_ENABLE mask |
| `rx-closed-channel-stores` | FILTER_EN ignored | F0, a closed channel stores nothing |
| `rx-second-ethertype-ignored` | a channel's second EtherType never classifies | C3, MSRP and MVRP |
| `evt-only-exact-deadline` | a deadline already past never expires | M2, at once |
| `wb-address-shifted` | the Wishbone adapter shifts the address | R0, CAPS |
| `axil-read-uses-write-address` | the AXI4-Lite adapter reads at AWADDR | R0, CAPS |

## Run

```sh
make -C tb/verilator/mbx
make -C tb/verilator/mbx mutants
```

The pinned Verilator is the repository's (5.050); `VERILATOR=` selects
another.
