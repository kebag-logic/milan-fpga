[OBSOLETE + 2026-08-16]

<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# The protocol-processor plane, measured — 2026-08-12

The first **measurement** of what the protocol-processor architecture of record
costs on the die this board ships. Everything before this was estimate:
the processor repo's `10_RESOURCE_AND_EFFORT` resource study prices scenario B at
`−3,250 … +11,150` net LUT, central `≈ +3,000`, and says outright that the
spread is "owned by three unmeasured numbers". Two of them are measured here.

> **STATUS 2026-08-13 — the µCPU landed, the substitution happened, and none of
> these numbers moved.** Every figure below was taken while the AECP pop face
> was tied `ready = 0`, and every "when P4 lands" / "do not delete anything
> yet" sentence on this page is the record of a decision as it stood on 08-12,
> not a standing instruction. Both have been overtaken: the protocol
> processor's **AECP µCPU is in**, and the shipping 1722.1 / SRP planes are
> **deleted**. The device is not silent on AECP — it answers `READ_DESCRIPTOR`
> (`SUCCESS` with the configuration index and descriptor, `NO_SUCH_DESCRIPTOR`
> on a locate miss, `BAD_ARGUMENTS` on a bad configuration index, both errors
> carrying the IEEE 1722.1 §7.4.5 4-byte `{descriptor_type, descriptor_index}`
> stub) and returns a conformant `NOT_IMPLEMENTED` echo to every other AECP
> command. Enumeration is reachable rather than working: nothing in this
> repository builds or loads the descriptor image those reads need, so on a
> stock build every `READ_DESCRIPTOR` answers `BAD_ARGUMENTS`.
>
> What this page does **not** contain is a re-measurement. The AECP engine's
> `+3,150 … +7,000` bracket below is still an estimate, and the mass constant
> propagation pruned while the pop face was tied off is still un-repriced. Do
> not quote this page as post-µCPU area; quote it as the measurement that
> decided substitution over coexistence.
>
> One structural change is worth carrying here because it is an area fact: the
> entity model is **not** in fabric memory. The µCPU's descriptor store fetches
> it from DDR3 over a read-only master with a compile-time base (`DESC_BASE_P`
> in the submodule's `KL_aecp_desc_store`, surfaced in the parent as
> `milan_datapath`'s `PP_DESC_BASE_P`; no base register), which the LiteX SoC
> **derives** as the top 1 MiB of `main_ram` rather than mirroring a literal.
> So the descriptor mass that used to be a fabric ROM is main memory now, and
> any area accounting that still charges LUT or BRAM for an AEM ROM is stale.
> Software must load the image before the entity is enabled — nothing in this
> repository does, per the note above — and a missing image is a clean refusal
> rather than a lockup: the all-zero region fails the `"AEMI"` magic compare,
> the store's watchdog (`MEM_TIMEOUT_CYC_P` = 4096 cycles, about 41 µs at
> 100 MHz) abandons a stalled burst and covers the request handshake too, and a
> late load heals without a reset.

## Contents

- **[Instrument](#instrument)** — Out-of-context Vivado synthesis of `KL_pp_shadow` — the wrapper containing the whole `protocol_processor_top` plus the RX classifier, control-frame FIFO and byte serializer that feed it. Same instrument as the processor's own µCPU measurement of record, so the numbers here are directly comparable to it, with the exact invocation and part given.
- **[Result](#result)** — The two shapes, and the finding that matters more than the LUT count: at `N_STREAM_IN/OUT = 8` the plane is 11,508 LUT and **does not close timing out of context** (WNS −2.854 ns, 11 failing endpoints) with nothing else on the die competing for routing. At 1×1 it is 7,463 LUT and closes with 1.4 ns to spare. The sub-table locates the mass: `KL_srp_top` is 52 % of it.
- **[What it means against the board](#what-it-means-against-the-board)** — Priced against the shipping AX7101 build at 52,827 LUT (83.32 %). The verdict is neither "fits" nor "impossible": physically it fits at 1×1 (95.1 %) but lands about 11 points past this board's 84.77 % conformance cliff, where closure has been measured as roughly a one-in-three lottery; the 8×8 shape is over the die. Present headroom to the cliff is 917 LUT and the plane needs 7,463.
- **[Two things that make these numbers OPTIMISTIC](#two-things-that-make-these-numbers-optimistic)** — Constant propagation deleted real blocks because shadow mode ties the AECP pop face `ready = 0` — 6 BRAM of dispatch queue, an RX pool and `tx_slots` — and all of that mass comes back with the µCPU that has since landed, its own skeleton on top; none of it is re-measured here. And because this is a shadow, every number is pure addition with nothing netted against it.
- **[THE SUBSTITUTION CASE — measured 2026-08-12, and it reverses the verdict](#the-substitution-case--measured-2026-08-12-and-it-reverses-the-verdict)** — The right question for scenario B, which deletes the old planes rather than coexisting with them. Both sides measured on the **same instrument**: the removable planes give back 14,489 LUT standalone and 15,474 in context, against the processor's 6,956 in context — **net −8,518 LUT, a 25 % reduction**. The single fact that drives it is that `KL_aecp_top` alone (8,645 in context) is larger than the entire processor plane, and nobody had measured it before. After P4 restores a working AECP the net is a saving at both ends of the bracket.
- **[SETTLED ON THE REAL BUILD — 2026-08-13: shadow mode does not fit the die](#settled-on-the-real-build--2026-08-13-shadow-mode-does-not-fit-the-die)** — The question out-of-context synthesis cannot answer: does a whole SoC with the plane on place on the board? It does not. `--with-pp-plane` — the first build in this project's history to contain the processor — failed `place_design` identically on all three seeds, before timing was ever reached. Shadow mode is therefore not a shipping option, and substitution is the only path.
- **[Reproduce](#reproduce)** — `syn/ooc/pp_shadow_ooc.tcl`, with `PP_N_IN`/`PP_N_OUT` selecting the shape. The script prints the shape it used, deliberately: a utilization figure quoted without its shape is a figure that gets misapplied.
- **[THE SUBSTITUTION ON THE REAL BUILD — 2026-08-13](#the-substitution-on-the-real-build--2026-08-13)** — the legacy planes deleted and the processor sole: LUTs fall 1,313 below a tree that never had it, but BRAM hits 135 of 135 and placement fails on the AECP response buffer spilling into 5,079 flops. The binding constraint moves from logic to memory

## Instrument

Out-of-context Vivado synthesis of `KL_pp_shadow` — the consumer-side wrapper,
which contains the whole `protocol_processor_top` (packet engine + ADP + ACMP +
SRP + side port + NVM port) plus the RX classifier, control-frame FIFO and byte
serializer that feed it. Same instrument as the protocol-processor's own
syn/ooc/ucpu_ooc.tcl (deleted since; post-synthesis hierarchical utilization, ship part,
100 MHz OOC), so these numbers are directly comparable to that document's
anchors and to its 1,068 LUT µCPU measurement of record.

```sh
cd <workdir>
python3 <pp>/hdl/acmp/rom/gen_ltn_rom.py -o ltn_rom.hex
python3 <pp>/hdl/aecp/ucode/gen_ucode.py -o ucode.hex
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
   `u_tx_slots/i_0`. The µCPU has since landed and does consume that queue, so
   the pruned mass is back *and* the µCPU's own 1,068 LUT skeleton sits on top
   — neither has been re-synthesised into a figure on this page.
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
(syn/ooc/old_planes_ooc.tcl, deleted 2026-08-13 with the planes it measured; same part, same 100 MHz OOC) to price what they
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

### The ASSEMBLED design, not just the blocks

Per-block OOC numbers are standalone costs — they do not carry the datapath's
own interconnect to each plane. `syn/ooc/milan_datapath_ooc.tcl` closes that
gap by synthesising the whole `milan_datapath` at the 1×1 shape, baseline
versus plane-ON, same instrument:

| milan_datapath, 1×1 | LUT | FF | BRAM | WNS @ 100 MHz | Failing |
|---|---|---|---|---|---|
| baseline (`PP_PLANE_P=0`) | 33,704 | 31,321 | 24.5 | +0.825 ns | 0 |
| + shadow plane (`PP_PLANE_P=1`) | 40,660 | 41,978 | 46 | **+0.264 ns** | 0 |
| **in-context cost** | **+6,956** | +10,657 | +21.5 | −0.561 ns | |

Two things worth having:

- **+6,956 in-context is LESS than the 7,463 the plane costs standalone.**
  Synthesis shares logic across the boundary, so the standalone figure was
  mildly conservative rather than optimistic — the arithmetic above stands.
- **The assembled design still CLOSES at 100 MHz out of context**, with
  0.264 ns to spare. That is a much better result than the standalone 8×8
  shape (−2.854 ns) predicted, and it says the timing risk lives in the *8×8
  shape*, not in the plane as such. It is still OOC: no placement pressure
  from a die that is already 83 % full, so it is not a closure promise.

### The net, measured IN CONTEXT — no RTL change required

The removable figures in the table above are **standalone** OOC costs: each
block elaborated on its own, at its own default parameters. That is not what it
costs inside the datapath, where `KL_lwsrp_top` is built with the build's real
`N_LISTENERS_P`/`N_TALKERS_P`/`N_CTX_P` and the ACMP arrays are sized by the
entity shape. Vivado's **hierarchical** utilization report for the baseline
synthesis already prices every instance as-assembled, so the honest in-context
figure needs no parameter, no tie-off, and no new RTL — just reading
`util_hier_base.rpt`:

| Instance | Module | LUT (in context) | FF |
|---|---|---|---|
| `aecp_listener` | `KL_aecp_top` | **8,645** | 5,075 |
| `lwsrp` | `KL_lwsrp_top` | 3,021 | 2,407 |
| `acmp_listener_sm` | `KL_acmp_listener` | 2,746 | 2,192 |
| `persist_journal` | `KL_persist_journal` | 429 | 465 |
| `adp_adv` | `adp_advertiser` | 302 | 210 |
| `acmp_responder` | `KL_acmp_tlkr_ctx` | 298 | 198 |
| `talker_diag` | `KL_talker_diag_ctx` | 33 | 360 |
| **total removable** | | **15,474** | 10,907 |

In context the old planes cost **more** than standalone (15,474 vs 14,489) —
they are elaborated at the build's real shape rather than at module defaults.

**So the net, both sides measured in context, same instrument:**

| | LUT |
|---|---|
| protocol processor, added to the assembled datapath | **+6,956** |
| shipping AECP + ACMP + ADP + lwSRP + journal, removed | **−15,474** |
| **net** | **−8,518** |

The substituted datapath lands at roughly **25,186 LUT against a 33,704
baseline — a 25 % reduction**, and `KL_aecp_top` alone (8,645) is larger than
the entire processor plane costs in context (6,956).

After P4 puts a working AECP back (+3,150 … +7,000, plus the mass constant
propagation pruned while the pop face was tied off), the net is **−5,368
(optimistic) to −1,518 (pessimistic)**. It is a saving at *both* ends of that
bracket — which is a different conclusion from the one the resource study
reached from estimates, and the reason it is different is that nobody had
measured `KL_aecp_top`.

### What must be subtracted back before anyone spends this

The processor's 7,463 LUT is measured with **no working AECP**: the pop face is
tied `ready = 0`, and Vivado constant-propagated away the AECP dispatch queue
(6 BRAM), an RX pool and `tx_slots` precisely because nothing consumes them.
A real substitution has to put that mass back and add the µCPU on top —
1,068 LUT for the skeleton of record, and the resource study brackets the full
AECP engine at **+3,150 … +7,000**. That is exactly what the landed µCPU did,
and the bracket has **not** been replaced by a measurement: the table below is
still the estimate it always was.

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

## SETTLED ON THE REAL BUILD — 2026-08-13: shadow mode does not fit the die

Everything above is out-of-context synthesis. The question it could not answer
is whether a whole SoC with the plane ON places on the board. It does not.

`--with-pp-plane` (the first time anything set `PP_PLANE_P`; no bitstream in
this project's history had ever contained the processor) was built at the
shipping AX7101 config as a 3-seed sweep. **All three seeds failed identically
at `place_design`**, before timing was ever reached:

> ERROR: [Place 30-487] … There are a total of 15850 slices in the device, of
> which 11286 slices are available, however, the unplaced instances require
> **12530 slices**. … Luts: **63540** (combined) 74582 (total), available
> capacity: **63400**

Like-for-like, both post-synthesis (the earlier 52,827 figure is post-PLACE and
must not be compared against a synth number):

| post-synthesis | baseline | + shadow plane | delta |
|---|---|---|---|
| Slice LUTs | 56,779 (89.6 %) | **64,241 (101.3 %)** | **+7,462** |
| Block RAM | 109 (80.7 %) | **131 (97.0 %)** | +22 |
| Registers | — | 66,738 (52.6 %) | — |

Two things worth keeping:

- **+7,462 LUT in a real SoC against 7,463 measured standalone OOC.** The
  out-of-context number was accurate to one LUT. That is a useful calibration
  for every future estimate made with `syn/ooc/pp_shadow_ooc.tcl`.
- **BRAM is the quieter problem.** 131 of 135 tiles is 97 %, and placement does
  not recover BRAM the way it recovers LUTs. Even a design that squeezed under
  the LUT ceiling would have almost no block memory left.

**Consequence: coexistence is not merely expensive, it is unbuildable here.**
The processor cannot reach this silicon as a second plane at any effort level —
no seed, no directive, no floorplan. The ONLY path to silicon is the
SUBSTITUTION, which removes 15,474 LUT of shipping planes to make room for
7,462. That is no longer the cheaper option; it is the only option.

A coexistence (shadow) flash of the 1×1 plane is buildable and worth
attempting, but should be expected to fail timing closure at 95.1 %. The path
that is actually affordable is **substitution**, which required the µCPU to
land at `protocol_processor_top` before the shipping AECP plane could be
deleted, because it is that deletion — not the addition — that pays for the new
plane. The section above measures exactly how much it pays: 14,489 LUT back,
against 7,463 spent at the shipping shape.

**That sequence has since run to completion.** The condition written here as
"do not delete anything yet" was: land the µCPU, prove the processor answers
AECP on the wire, then delete plane by plane at parity, measuring after each,
per the standing rule that a block-scale change is judged in LUT and packing
density, never in slices. The µCPU landed, the entity answers `READ_DESCRIPTOR`
(against whatever descriptor image DRAM holds, and nothing here loads one) and
echoes `NOT_IMPLEMENTED` at everything else, and the old planes are gone.
The caveat attached to the removable figures still holds and is worth
re-reading before anyone reuses them: they are *standalone* costs, and the
datapath's own interconnect to those planes (CSR fan-out, the arbiter legs, the
cross-plane wiring documented in `milan_datapath.sv`) is in neither column.

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

Run it from an empty working directory outside the tree: both `$readmemh`
images are generated into that directory, and the three reports land beside
them.

Both images are required, and the Instrument block above is the whole recipe.
`ltn_rom.hex` on its own is not: the AECP microcode ROM reads `ucode.hex` by the
same relative name, Vivado answers a missing image with a CRITICAL WARNING
ending in "ignoring" rather than with an error, and the run completes and
reports the area of a ROM full of X. On the 1x1 shape that omission understates
the plane by 2,871 LUT (13,676 against 16,547) and by 5 block RAM tiles. The
script refuses to synthesize unless both images are present, and its read set is
derived from the `KL_pp_shadow` entry in `syn/yosys/run.sh` rather than
assembled here, so it cannot again name a top it does not read.

Figures at a later head, for scale rather than as a replacement: the same
instrument at `dev` `04b55dad` with that read set corrected, protocol-processor
pinned at `a25b5cc9`, reports 16,547 LUT / 19,473 FF / 17 BRAM / 4 DSP /
WNS -0.486 ns at `N_STREAM_IN/OUT = 1`, and 22,817 LUT / 25,922 FF /
24.5 BRAM / 4 DSP / WNS -7.573 ns at 8. The table under Result is the
2026-08-12 measurement and stays that; the plane roughly doubled in between,
most of it the AECP engine, its descriptor store and its microcoded core.

## THE SUBSTITUTION ON THE REAL BUILD — 2026-08-13

The legacy planes are deleted (`eff99a9c`) and the processor — now including the
AECP µCPU, descriptor store and engine — is the only control plane. Shipping
AX7101 config, one seed.

| post-synth | baseline | substituted | delta |
|---|---|---|---|
| Slice LUTs | 56,779 (89.6 %) | **55,466 (87.5 %)** | **−1,313** |
| Block RAM | 109 (80.7 %) | **135 (100.0 %)** | **+26** |
| Registers | — | 62,138 (49.0 %) | — |

**LUTs went the right way** — smaller than the tree that had no processor in it
at all. But −1,313 is far from the −8,518 predicted earlier, and the reason is
not an arithmetic error: that prediction measured a processor with **no AECP
engine**. The µCPU, descriptor store and dispatch queue landed in between, so
the thing being added grew. The earlier note that constant propagation was
pruning `u_dispatch/u_aecp_q` "until P4 lands" was exactly this bill arriving.

**PLACEMENT FAILED, on memory, not logic.**

> ERROR: [Place 30-433] Unplaced instances found …
> `milan_datapath/pp_shadow/u_pp/u_aecp/rbuf_r_reg[3][97][0]` … could not be placed
> ERROR: [Place 30-99] Placer failed with error: 'failed to commit all instances'

The unplaced instances are the AECP **response buffer**, `rbuf_r`, carried as
**5,079 flip-flops** in `KL_aecp_engine`'s own glue. A buffer that shape wants
to be a block RAM — and cannot be, because BRAM is at **135 of 135**. So it
spilled into fabric, and with LUTs already at 87.5 % the placer had nowhere to
pack it.

Where the processor's 38 RAMB36 + 3 RAMB18 go:

| block | RAMB36 |
|---|---|
| `u_aecp_q` (AECP dispatch queue) | 5 |
| `u_aecp` (descriptor line buffer etc.) | 5 |
| `u_ucpu` (µcode ROM, 2048 × 48 b) | 3 |
| RX slot pools + TX slots + the rest | ~25 |

**The binding constraint has moved from LUTs to BRAM.** Freeing block RAM in the
processor — the dispatch queue and the RX pools are the obvious candidates — is
now what decides whether this flashes, and it is a submodule change. Cutting
LUTs further buys nothing.
