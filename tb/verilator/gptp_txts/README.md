# `gptp_txts` - the gPTP egress timestamp closed loop

One live simulation containing the whole causal path from the engine's last
committed byte to the wire, grading the timestamp the plane returns against
the instant the pads actually launched the frame.

## Contents

- **[What is inside the loop](#what-is-inside-the-loop)** -- where each piece comes from, and which one is converted rather than written
- **[The two seams, and why the oracle is independent](#the-two-seams-and-why-the-oracle-is-independent)** -- the design reads the MAC's transmit stream, the oracle reads the pads
- **[Clocks](#clocks)** -- the product's ratio, the oscillator offset and the swept phase, and what is compressed instead
- **[What it proves, and what it does not](#what-it-proves-and-what-it-does-not)** -- the digital claim it carries, and the physical one it does not
- **[Running it](#running-it)** -- the command, its mutation arm, and the interpreter that re-converts the MAC

## What is inside the loop

| Piece | Where it comes from |
|---|---|
| gPTP engine | the pinned `gptp-processor` submodule, unmodified |
| plane, ledger, launch observer | `hdl/ieee8021as/gptp_plane/`, unmodified |
| PHC | `hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv` |
| merge in front of the MAC | `hdl/ieee17221/adp/adp_tx_arbiter.sv`, the product mux |
| link guard | `hdl/common/KL_link_guard.sv`, at a bench-scaled settle |
| MAC transmit chain | CONVERTED from the product's own migen source by `sw/litex/gen_mac_tx_model.py` |

The converted chain is both `mac_tx_cdc` halves, the `last_be` conversion and
the loopback mux, the store-and-forward `tx_sf`, `LiteEthMACCore` with
preamble, FCS, padding and width conversion, the inter-frame gap stage and
the PHY transmit register stage, in the product's own shadow clock domains.
`make` regenerates it and refuses a stale artifact before compiling anything:
with the pinned LiteX interpreter it is re-converted and compared byte for
byte, and without it the artifact is still compared against the `MilanMAC`
source region it came from, its recorded pins and its own bytes.

That is one half of the claim. The other half - that the conversion BEHAVES
like the source - is `sw/litex/test_gptp_tx_timestamp.py`, in the LiteX
simulation aggregate: it drives one fixed stimulus through this artifact
(`pad_trace_main.cpp`, built by `make padtrace`, the chain alone) and the
same stimulus through the migen objects themselves, and requires the two pad
traces to agree frame for frame, octet for octet and gap for gap.

## The two seams, and why the oracle is independent

The launch observer under test reads `phy.sink` - the product connection,
exported from the converted chain. The harness's oracle reads the PADS,
counts octets there itself, and takes the reference launch instant from PHC
samples it collected at the plane's own clock edges. It never reads the
design's computed t1 and never adjusts anything to reach an expected answer,
so a dropped register stage moves the answer by a whole clock period instead
of being absorbed.

## Clocks

125 MHz at the wire, 100 MHz at the MAC system side, 50 MHz at the plane -
the product's shape, so the egress correction this bench grades is the
product's own 426 ns. The wire clock carries a relative frequency offset at
the declared 200 ppm envelope and the system clock's phase is swept, because
the two domains are independent oscillators in the product and a bench that
held their phase still would sample one value of the dominant error term and
report it as the mean. The engine's own timers are generated for a faster
second so a protocol run fits in a simulation; no timestamp arithmetic
changes with that.

## What it proves, and what it does not

It proves the reconstruction is the launch: every frame inside the published
digital bound, a mean inside one nanosecond over two hundred phase-varied
frames, and the same answer whether the frame left an empty MAC or queued
behind other traffic. It measures the retired capture in the same run and
prints how far ahead of the launch it was, isolated and queued, which is the
defect as a number.

It proves nothing physical. No measured PHY latency, no pad clock-to-out, no
cable, no silicon. Its reference plane is the registered GMII launch edge,
and the physical terms belong to the qualification issues that own them.

## Running it

    make -C tb/verilator/gptp_txts

The default target runs the suite and then `mutants.py`, which plants one
defect at a time - the observation point, each register-stage term of the
correction, the measured cycle distance - and requires the suite to notice,
restoring the exact source afterwards.

    MILAN_LITEX_PYTHON=/path/to/litex/python make -C tb/verilator/gptp_txts

names the interpreter that can re-convert the chain. Without it the suite
still runs and still checks the artifact, and says which level it checked.
