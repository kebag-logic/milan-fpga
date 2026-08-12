<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# pp_shadow — milan_datapath with the protocol-processor plane ON

The only suite in this tree that elaborates the `protocol-processor` submodule
into the consumer. `milan_dp` keeps proving the OFF side — its source list does
not even name the processor — so the two together are the parity contract:
**OFF is what ships, ON is what this suite grades.**

`make` — exit 0 = PASS.

## The package collision that used to block this suite — RESOLVED

This suite once could not build at all: the protocol-processor declared
`package adp_pkg` / `package acmp_pkg` and `module KL_acmp_listener`, and this
repository declares its own with those exact names and different contents.
SystemVerilog packages and modules share one global namespace per compilation
unit, so the two could not coexist.

The trap worth remembering is how QUIETLY it failed. Verilator rates a
duplicate as `MODDUP`, a *warning* — and under the `-Wno-fatal` that every
other suite in this tree carries it **exits 0 and silently keeps the FIRST
declaration**, compiling the processor's engines against the consumer's
constants with no error anywhere. It is only visible because this suite carries
no `-Wno-*` at all (a USER RULE; warnings are fatal by default in Verilator, so
removing every suppression IS the `-Werror` build).

Fixed at the source, not waived: the processor namespaced its copies to
`pp_adp_pkg`, `pp_acmp_pkg` and `KL_pp_acmp_listener`.

## What it proves

| # | Check group | What it establishes |
|---|---|---|
| A | presence + CSR window | `PP_STAT[31:24]` is a constant `0x5B` tag, so a structural zero can never be read as "present and idle" (the `STATS_CAP` rule) |
| B | RX classify → FIFO → serializer → validator | an ADP `ENTITY_DISCOVER` is accepted end to end; the counter only moves when the **processor** took a whole frame |
| C | the classifier rejects non-control traffic | 8 IPv4 frames leave `rx_frames` flat. This is the check that protects the board — see the rate note below |
| D | **shadow discipline** | the processor is run until *it* wants to transmit (`tx_frames > 0`) and the MAC TX port must stay **silent** across the same window |
| E | side port over the CSR bridge | the snapshot window answers with the processor's own magic `0x4B4C5050` "KLPP" — generated inside `protocol_processor_top`, so it is proof the fabric is alive and clocked, not that the bridge returns a plausible constant |
| F | the byte→AXIS packer runs while draining | a packer bypassed until substitution day would be untested on the day it matters |
| G | the **class-D fabric face** is reachable *and live* | `adp_next_avail_index_o` reads 0 before the first advertisement and has advanced after it. A port read once at reset proves only that a wire exists |
| H | the **MAAP adapter refuses safely** | with no claimed block, every request is still accepted **and answered** (`ok = 0`), the DA gate stays shut, and the plane keeps serving |
| I | the **MAAP adapter grants** | with `KL_maap` in ANNOUNCE the same request returns `ok = 1` with `base + source_index` (checked against `MAAP_STAT0`'s offset), and `acmp_declaring_o` goes HIGH |
| J | global anti-wedge invariant | `accepted == answered` over every cycle simulated |

Group D is the safety property the whole landing rests on. The shipping
ADP/ACMP/lwSRP planes are still live and still own the wire; a processor that
also transmitted would put a second `ENTITY_AVAILABLE` — and a second answer to
every controller command — on the segment from the same `entity_id`.

Group J is the one hazard `KL_pp_maap_shim` can create. `KL_acmp_talker` clears
its allocator-busy flag **only** on a response: accept a request once without
answering and that source can never allocate again — it does not wedge, commands
still answer, which is exactly why nothing else would notice. So the invariant
is graded globally rather than per case.

Groups H and I need the processor's talker half awake, and the wrapper ties
`cfg_src_en_i` to 0 by default (a shadow must not reserve a stream the shipping
lwSRP plane owns). `-GPP_SRC_EN_P=1` enables source 0. It stays wire-safe — TX
is still drained, and group D still grades absolute silence, before MAAP is
enabled.

Once MAAP **is** enabled the fabric's own `KL_maap` legitimately transmits
PROBE/ANNOUNCE PDUs, so group I grades the honest form of the same property:
every frame that egressed was a MAAP PDU (DA `91:E0:F0:00:FF:00`) — still
nothing from the shadow.

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

**ONE GRID.** `KL_maap` keeps its *own* millisecond (`CLK_FREQ_HZ_P/1000`
cycles) and its Annex B claim walk is 3 probes × ~500 ms — 1.5·10⁸ cycles at a
real 100 MHz, which no harness can run, so `addr_valid_o` would never assert and
group I would be unreachable. `-GMAAP_CLK_HZ_P=100000` makes one MAAP
millisecond 100 clk, **the same** compressed millisecond the processor uses.
Two planes on two different compressed scales would be a harness measuring its
own arithmetic. `MAAP_CLK_HZ_P` defaults to `MILAN_CLK_FREQ_HZ`, so silicon and
`milan_dp` are untouched.

## Note on group B's frame (corrected 2026-08-12)

`build_adp_discover()` used to put the message type in wire byte 16 and leave
byte 15 at 0 — but byte 15 is sv/version/**message_type** and byte 16 is
valid_time + `control_data_length[10:8]`, so the frame declared msg_type 0 with
`control_data_length` 512 against a 68-byte payload and the processor's V1
length rule discarded it every time. Group B stayed green throughout, because
`rx_frames_o` counts frames the **wrapper** handed to the processor, not frames
the processor **accepted**. What exposed it was group G: a level that only moves
when the ADP engine actually transmits cannot be satisfied by a frame the ADP
engine never took.
