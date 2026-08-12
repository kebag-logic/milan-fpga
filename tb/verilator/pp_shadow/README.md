<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# pp_shadow — milan_datapath with the protocol-processor plane ON

The only suite in this tree that elaborates the `protocol-processor` submodule
into the consumer. `milan_dp` keeps proving the OFF side — its source list does
not even name the processor — so the two together are the parity contract:
**OFF is what ships, ON is what this suite grades.**

`make` — exit 0 = PASS.

## BLOCKED (2026-08-12): duplicate package names

This suite **cannot build today**, and the Makefile refuses to pretend
otherwise: a preflight compares the package names in the two repositories and,
on a collision, prints a `[SKIP]` naming the blocker and exits 0 rather than
producing a build that is quietly wrong.

The protocol-processor declares `package adp_pkg` (`hdl/adp/adp_pkg.sv`) and
`package acmp_pkg` (`hdl/acmp/acmp_pkg.sv`). This repository declares its own
packages with **those exact names and different contents**
(`hdl/ieee17221/adp/adp_pkg.sv`, `hdl/ieee17221/acmp/acmp_pkg.sv`).
SystemVerilog packages share one global namespace per compilation unit, so the
two cannot coexist.

Verified with Verilator 5.050:

| Flags | Result |
|---|---|
| strict | `%Warning-MODDUP: Duplicate declaration of package: 'adp_pkg'` → exit 1 |
| `-Wno-fatal` (what **every** suite here uses, incl. `milan_dp`) | **exit 0**, silently keeps the FIRST declaration |

The second row is the dangerous one and the reason `-Werror-MODDUP` is in this
Makefile's flags: as a plain warning the processor's ADP/ACMP engines compile
against *the consumer's* constants and nothing says a word. That is silent
wrong code, not a build failure.

**The fix belongs in the protocol-processor repository**, whose own HDL README
makes interface stability its responsibility: rename `adp_pkg` →
`pp_adp_pkg` and `acmp_pkg` → `pp_acmp_pkg`, consistent with the `pp_pkg` /
`KL_pp_*` naming it already uses everywhere else. Only these two collide —
`pp_pkg`, `srp_pkg` and `ucpu_pkg` are already unique. When it lands and the
submodule pin moves, this suite starts running with no change here.

## What it proves (once unblocked)

| # | Check group | What it establishes |
|---|---|---|
| A | presence + CSR window | `PP_STAT[31:24]` is a constant `0x5B` tag, so a structural zero can never be read as "present and idle" (the `STATS_CAP` rule) |
| B | RX classify → FIFO → serializer → validator | an ADP `ENTITY_DISCOVER` is accepted end to end; the counter only moves when the **processor** took a whole frame |
| C | the classifier rejects non-control traffic | 8 IPv4 frames leave `rx_frames` flat. This is the check that protects the board — see the rate note below |
| D | **shadow discipline** | the processor is run until *it* wants to transmit (`tx_frames > 0`) and the MAC TX port must stay **silent** across the same window |
| E | side port over the CSR bridge | the snapshot window answers with the processor's own magic `0x4B4C5050` "KLPP" — generated inside `protocol_processor_top`, so it is proof the fabric is alive and clocked, not that the bridge returns a plausible constant |

Group D is the safety property the whole landing rests on. The shipping
ADP/ACMP/lwSRP planes are still live and still own the wire; a processor that
also transmitted would put a second `ENTITY_AVAILABLE` — and a second answer to
every controller command — on the segment from the same `entity_id`.

## Two traps this suite exists to not fall into

**Lane order.** Frames are injected LITTLE-LANE (`tdata[7:0]` = first wire
byte). That is the silicon convention of the RX tap: `KL_maap.sv:154` states it
outright and tests the EtherType at lanes 4/5, and `KL_aecp_ingress.sv`
documents the same. The `vlan_frame()` helper in `milan_dp/sim_main.cpp` packs
the **other** way for the TX classifier path — copying it here would feed the
processor byte-swapped frames and every accept check in group B would read a
silent zero.

**Rate.** `protocol_processor_top` eats a 1 byte/clk stream, which at 100 MHz is
100 MB/s against gigabit's 125 MB/s. A serializer fed from the raw tap cannot
keep up with line rate and would corrupt frames by lagging rather than by
dropping them — so the tap is classified first and only control frames reach
the FIFO. Group C is what keeps that filter honest.

## Time compression

`-GPP_TIM_DIV_US_P=1 -GPP_TIM_DIV_MS_P=100` gives 1 ms = 100 clk (the
`tb/pp_top` ratio). The ADP advertise cadence is *seconds* of real time; at
silicon rates group D would need ~10⁹ cycles to see a single attempt. Both
values feed the gateware only, and the C++ side is told the ratio by `-D` so
the two cannot drift into disagreeing about what a millisecond is.
