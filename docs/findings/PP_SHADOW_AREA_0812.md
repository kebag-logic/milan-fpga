<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# The protocol-processor plane, measured — 2026-08-12

The first **measurement** of what the protocol-processor architecture of record
costs on the die this board ships. Everything before this was estimate:
the processor repo's `10_RESOURCE_AND_EFFORT` resource study prices scenario B at
`−3,250 … +11,150` net LUT, central `≈ +3,000`, and says outright that the
spread is "owned by three unmeasured numbers". Two of them are measured here.

## Instrument

Out-of-context Vivado synthesis of `KL_pp_shadow` — the consumer-side wrapper,
which contains the whole `protocol_processor_top` (packet engine + ADP + ACMP +
SRP + side port + NVM port) plus the RX classifier, control-frame FIFO and byte
serializer that feed it. Same instrument as the protocol-processor's own
`syn/ooc/ucpu_ooc.tcl` (post-synthesis hierarchical utilization, ship part,
100 MHz OOC), so these numbers are directly comparable to that document's
anchors and to its 1,068 LUT µCPU measurement of record.

```sh
cd <workdir>
python3 <pp>/hdl/acmp/rom/gen_ltn_rom.py -o ltn_rom.hex
PP_N_IN=1 PP_N_OUT=1 vivado -mode batch -source <repo>/syn/ooc/pp_shadow_ooc.tcl -nojournal
```

Vivado 2026.1, `xc7a100t-fgg484-2`, `-mode out_of_context`, 100 MHz.

## Result

| Shape | Slice LUTs | FFs | BRAM tiles | DSP | WNS @ 100 MHz | Failing endpoints |
|---|---|---|---|---|---|---|
| `N_STREAM_IN/OUT = 8` | **11,508** | 15,127 | 27 | 3 | **−2.854 ns** | **11** |
| `N_STREAM_IN/OUT = 1` | **7,463** | 11,540 | 21.5 | 3 | **+1.409 ns** | 0 |

The 8×8 shape **does not close timing out of context** — with nothing else on
the die competing for routing, before any placement pressure at all. The 1×1
shape closes with 1.4 ns to spare.

### Where the LUTs are (8×8 hierarchical)

| Block | LUTs | Share |
|---|---|---|
| `KL_srp_top` | **6,014** | **52 %** |
| ├ `KL_srp_talker_fsm` | 1,505 | |
| ├ `KL_srp_listener_fsm` | 1,231 | |
| ├ glue in `KL_srp_top` itself | 1,056 | |
| ├ `KL_srp_decoder` | 950 | |
| ├ `KL_srp_encoder` | 732 | |
| └ `KL_srp_admission` | 375 (+2 DSP) | |
| `KL_acmp_listener` | 923 | 8 % |
| `KL_acmp_nvm_shadow` | 703 | 6 % |
| `KL_acmp_talker` | 572 | 5 % |
| `KL_pp_rx_validator` | 497 | 4 % |
| `KL_adp_engine` | 440 (+1 DSP) | 4 % |
| `KL_pp_event_router` | 417 | 4 % |
| `KL_pp_timer_service` | 413 | 4 % |
| everything else | ~1,529 | 13 % |

At 1×1 the SRP engine falls to 3,198 LUT (43 %), which is the per-stream FSM
array shrinking; the rest is shape-independent mass.

## What it means against the board

The shipping AX7101 build (`build_ax7101_csm_v0043b`, 2026-08-11, VERSION
0x0043, post-place) sits at **52,827 LUT = 83.32 %**. The shape it flashes is
1×1×8 TDM8, so the 1×1 row above is the relevant one.

| | LUTs | % of die |
|---|---|---|
| shipping AX7101 build today | 52,827 | 83.32 % |
| the conformance cliff (this board's closure line) | 53,744 | 84.77 % |
| **+ shadow plane at 1×1** | **60,290** | **95.1 %** |
| + shadow plane at 8×8 | 64,335 | 101.5 % — over the die |

So the honest verdict is neither "fits" nor "impossible":

- **It physically fits at 1×1** (95.1 %), with 3,110 LUT to spare.
- **It lands ~11 points past the conformance cliff.** This board's record is
  that closure is met at 84.77 % and missed above it, and the fit campaign
  measured closure above that line as roughly a one-in-three lottery. 95.1 %
  is not a place this design has ever closed.
- **The 8×8 shape is out of reach** on any build: over the die on the AX7101,
  and 115.9 % against the 8×8 build's own 61,959 LUT baseline.

Present headroom to the cliff is **917 LUT**. The plane needs 7,463.

## Two things that make these numbers OPTIMISTIC

1. **Constant propagation removed real blocks.** Shadow mode ties the AECP pop
   face `ready = 0` (the unlanded P4 µCPU seam), the SRP service face
   `valid = 0`, and `cfg_src_en = 0`. Vivado pruned what those unreach:
   `u_dispatch/u_aecp_q` (6 BRAM), one `g_rx_pool[3].u_rx_slots` BRAM, and
   `u_tx_slots/i_0`. When P4 lands and the µCPU consumes that queue, the
   pruned mass returns *and* the µCPU's own 1,068 LUT skeleton arrives on top.
2. **It is a shadow, so nothing is deleted.** Every number here is pure
   addition. The substitution case — which is what scenario B actually
   proposes — would net the shipping planes' removal against it, and only
   then does the SRP engine's 6,014 LUT trade against the consumer's
   removable 5,758–6,358 LUT lwSRP plane.

That second point is the one that matters strategically: **the measurement
confirms `10_RESOURCE_AND_EFFORT.md` §10's own recommendation** not to swap the
lwSRP plane on resource grounds. Its estimate for that swap was
`≈ −500 … +6,600`, central `≈ +2,200`; the engine measures 6,014 LUT at 8×8 and
3,198 at 1×1, i.e. at or above the pessimistic end of a bracket the document
already judged not worth taking.

## THE SUBSTITUTION CASE — measured 2026-08-12, and it reverses the verdict

Everything above prices the plane as an ADDITION (shadow mode: nothing deleted).
That is the wrong question for scenario B, which deletes the old planes. So the
shipping 1722.1 + SRP planes were synthesised with the **same instrument**
(`syn/ooc/old_planes_ooc.tcl`, same part, same 100 MHz OOC) to price what they
give back. A net figure built from two different instruments would not be a net
figure.

| Removable plane | top | LUT | FF | BRAM |
|---|---|---|---|---|
| AECP / AEM | `KL_aecp_top` | **10,018** | 5,086 | 4 |
| ACMP listener | `KL_acmp_listener` (+`lstn_ctx`) | 2,270 | 2,394 | 5.5 |
| lwSRP | `KL_lwsrp_top` | 1,563 | 1,397 | 1.5 |
| ACMP talker | `KL_acmp_responder` (+`tlkr_ctx`) | 261 | 216 | 0 |
| ADP | `adp_advertiser` | 377 | 211 | 0 |
| **total removable** | | **14,489** | 9,304 | 11 |

Against the processor's measured cost:

| | LUT | net |
|---|---|---|
| old planes removed | −14,489 | |
| protocol processor, 1×1 | +7,463 | **−7,026** |
| protocol processor, 8×8 | +11,508 | **−2,981** |

**The substitution SAVES LUTs — a lot of them.** The single fact that drives it:
`KL_aecp_top` alone is 10,018 LUT, larger than the *entire* protocol processor
at the 1×1 shape the AX7101 flashes. The additive reading above ("does not
fit") is correct only for coexistence, and coexistence was never the goal.

### What must be subtracted back before anyone spends this

The processor's 7,463 LUT is measured with **no working AECP**: the pop face is
tied `ready = 0`, and Vivado constant-propagated away the AECP dispatch queue
(6 BRAM), an RX pool and `tx_slots` precisely because nothing consumes them.
A real substitution has to put that mass back and add the µCPU on top —
1,068 LUT for the skeleton of record, and the resource study brackets the full
AECP engine at **+3,150 … +7,000**.

So the honest net, at the 1×1 shape:

| P4 AECP lands at | net LUT |
|---|---|
| optimistic (+3,150) | ≈ **−3,900** |
| pessimistic (+7,000) | ≈ **0** (break-even) |

That is a materially better answer than the estimate this document set started
from (central `≈ +3,000`, "not worth it for area"): **at worst break-even, and
plausibly several thousand LUT to the good**, on a board where the shipping
build sits 917 LUT above the closure cliff and every LUT below it buys closure
probability.

## Consequence for the integration

A coexistence (shadow) flash of the 1×1 plane is buildable and worth
attempting, but should be expected to fail timing closure at 95.1 %. The path
that is actually affordable is **substitution**, which requires P4: the µCPU
must land at `protocol_processor_top` before the shipping AECP plane can be
deleted, and it is that deletion — not the addition — that pays for the new
plane. The section above now measures exactly how much it pays: 14,489 LUT
back, against 7,463 spent at the shipping shape.

**Do not delete anything yet.** The removable figures are what the old planes
cost *standalone*; the datapath's own interconnect to them (CSR fan-out, the
arbiter legs, the cross-plane wiring documented in `milan_datapath.sv`) is not
in either column, and the processor cannot answer an AECP command until P4
lands. The sequence that stays honest is: land P4, prove the processor answers
AECP on the wire in `pp_shadow`, then delete plane by plane at parity —
measuring after each, per the standing rule that a block-scale change is judged
in LUT and packing density, never in slices.

Also worth recording: **3 DSP blocks are inferred** (1 in `KL_adp_engine`, 2 in
`KL_srp_admission`). the processor repo's HDL rule 1 forbids
vendor primitives, and these are inferences rather than instantiations, so the
rule is not broken — but this board's area work removed DSPs from `hdl/`
deliberately, and the µCPU measurement of record reports `DSP 0`. Worth a look
before anyone quotes these as vendor-neutral.

## Reproduce

`syn/ooc/pp_shadow_ooc.tcl` (this repo). `PP_N_IN` / `PP_N_OUT` select the
shape and default to 8; the script prints the shape it used, because a
utilization figure quoted without its shape is a figure that gets misapplied.
