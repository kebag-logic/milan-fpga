<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->

# The 8×8 board advertised the 1×1 shape — and the CRF talker with it

*2026-07-27. A device that could describe itself wrongly, faithfully, forever.*

## Contents

- **[The symptom](#the-symptom)** — Decoded off the wire beside its neighbours: our 8×8 AX7101 advertising 1 talker source and 2 listener sinks, so every controller on the segment could bind exactly one of its eight streams.
- **[Where the numbers came from](#where-the-numbers-came-from)** — Two lines of a boot script, correct the day they were typed, and a `milan_csr` register that faithfully held whatever was written into it.
- **[The second casualty: the CRF talker](#the-second-casualty-the-crf-talker)** — The media clock output answers ACMP at `talker_unique_id = N_STREAMS` and its PDUs are on the wire every 2 ms; nobody ever asked, because uid 8 sat outside an advertised range of 1.
- **[The fix: the shape is defined by the config](#the-fix-the-shape-is-defined-by-the-config)** — Read-only words whose values are *generated from `configs/endstation_*.yaml`* alongside the AEM descriptor ROM, and included by the same file that sizes the ACMP context arrays.
- **[The listener side had the same hole](#the-listener-side-had-the-same-hole)** — `ACMP_SINKS_C` was `max(N, 2)`, which reserved the CRF sink up to N = 2 and then silently dropped it.
- **[What is gated now](#what-is-gated-now)** — The config→svh→CSR→descriptor agreement check, the pre-build refusal, and the seven mutations that must fail them.
- **[What this does NOT fix](#what-this-does-not-fix)** — M-CLK-2 is a different gap, and none of this has been on silicon.

## The symptom

Our AX7101 is built `N_STREAMS = 8` (`configs/endstation_ax7101_8x8.yaml`).
Decoded from its own ADPDU on the wire, next to its neighbours on the same
segment:

| device | talkers / listeners |
|---|---|
| reference device `3c:c0:c6:01:02:03` | 4 / 10 |
| peer host | 8 / 8 |
| **our AX, built 8×8** | **1 / 2** |

Every controller on the segment — including a validated reference device —
could therefore see and bind **one** stream. Nothing was broken anywhere: the
register read back exactly what had been written to it, the ADP advertiser
serialised exactly what the register held, and the ADPDU on the wire was
byte-correct for the value it carried.

## Where the numbers came from

`milan_csr`'s `ADP_TALKER` (`0x618`) and `ADP_LISTENER` (`0x61C`) were plain
RW words **resetting to zero**. Nothing derived them from anything. The values
came from two hand-typed lines in the board's boot script:

```sh
w 0x618 0x48010001   # talker  {caps, sources}: 1 implemented stream (honest count, Milan strict)
w 0x61C 0x48010002   # listener {caps, sinks}: 2 STREAM_INPUTs (media + CRF desc)
```

Those comments were true. They were written on 2026-07-20 against a 1×1 board,
as the *fix* for an earlier gap where the declared counts exceeded reality —
and they were, at the time, the honest counts. Then the AX went 8×8 and the
script did not.

This is the decorative-ABI pattern running backwards. The usual version is a
register that does nothing; this one is a register that does exactly what it
is told, which is worse, because the lie is invisible at every layer that
could have caught it. A stream count is a **physical fact about the built
bitstream** — software cannot create a ninth stream engine by writing a
register — so a writable count buys nothing at all, and buys a way for the
device to misdescribe itself with no symptom other than controllers quietly
seeing less than there is.

## The second casualty: the CRF talker

The CRF Media Clock Output is a bindable ACMP talker source at
`talker_unique_id = N_STREAMS` (`milan_datapath` `CRF_TUID_C`), shipped
2026-07-26. On the 8×8 build the fabric answers `CONNECT_TX`/`PROBE_TX` for
uid 8 with `stream_id = {station MAC, 8}` and `stream_dest_mac` = MAAP block
base + 8, and `KL_crf_tx` emits that exact stream: AVTP subtype `0x04`, source
`02:00:00:00:00:01`, destination `91:e0:f0:00:b0:83`, every ~2 ms, captured on
the wire.

No controller ever asked for uid 8, because the entity advertised **1** talker
source. [`NXN_ARCHITECTURE.md`](../NXN_ARCHITECTURE.md) had this listed as step (a) of the CRF work
with exactly the right warning — *"without it no controller ever learns the
uid exists"* — and the fabric half shipped without it.

## The fix: the shape is defined by the config

Two things had to change, and only one of them is "make it read-only".

**Read-only.** `0x618` and `0x61C` have no storage, no write arm and no
`is_plain_rw` entry. They are assembled once and served from the defaults ROM
exactly like `CAP` and `VERSION`.

**And the values come from the config.** Making the RTL compute the shape would
be the same mistake one layer down — RTL deciding what the entity is. The
standing rule is that `configs/endstation_*.yaml` is the single declarative
definition and it drives the gateware, the AEM model and lwSRP alike, so
`sw/builder/endstation_builder.py` emits the counts as a generated include:

```systemverilog
// hdl/common/csr/gen/adp_shape_defaults.svh - GENERATED, Source: configs/endstation_arty_current.yaml
localparam int ADP_TALKER_SRC_C    = 1;
localparam int ADP_LISTENER_SINK_C = 2;
localparam logic [15:0] ADP_TALKER_CAPS_C   = 16'h4001;
localparam logic [15:0] ADP_LISTENER_CAPS_C = 16'h4801;
```

`milan_csr` builds the two RO words from it. **`milan_datapath` includes the
same file** and sizes its ACMP context arrays from the same constants:

```systemverilog
`include "gen/adp_shape_defaults.svh"
localparam int ACMP_SRC_C   = ADP_TALKER_SRC_C;     // was (N>1) ? N+1 : 1
localparam int ACMP_SINKS_C = ADP_LISTENER_SINK_C;  // was max(N, 2)
```

`KL_acmp_tlkr_ctx` accepts a probe iff `talker_unique_id < N_SRC_P`, and
`N_SRC_P` **is** `ACMP_SRC_C`. So the number a controller is told, the number
of contexts that can answer it, and the descriptor set it enumerates are one
constant from one config in one pass. Point `+incdir` at
`configs/generated/<config>/` to elaborate a different shape — which is how the
harnesses cover 1×1, 4×4 and 8×8 in the same build.

`talker_capabilities` follows the same rule: `MEDIA_CLOCK_SOURCE` (`0x0800`)
is set only when the config *has* a CRF output, so a 1×1 build advertises
`0x4001` instead of the `0x4801` the boot script had been writing — that bit
had nothing behind it at 1×1.

| build | `0x618` | `0x61C` | before |
|---|---|---|---|
| 1×1 (arty) | `0x4001_0001` | `0x4801_0002` | `0x4801_0001` / `0x4801_0002` from the script |
| 4×4 | `0x4801_0005` | `0x4801_0005` | same script values → 1 / 2 |
| 8×8 (AX) | `0x4801_0009` | `0x4801_0009` | same script values → **1 / 2** |

## The listener side had the same hole

`ACMP_SINKS_C` was `max(N_STREAMS, 2)`. The `2` existed to pin the
`{ctx0 media, ctx1 CRF}` pair at N = 1 — and above N = 2 the `max` silently
dropped the CRF sink, so a 4×4 or 8×8 build had **N** sink contexts where its
own AEM model declares **N + 1** (N AAF `STREAM_INPUT`s plus the CRF one). It
is not computed in the RTL at all now: the config says `N + 1`, and that is
the same number its AEM overlay used. 1×1 still elaborates 2 sinks.

## What is gated now

`scripts/check_entity_shape.py` walks every end-station config and asserts the
same number appears everywhere it has to: what `adp_shape()` computes from the
config, what the generated shape include carries, what the AEM overlay's
`entity_counts` and `descriptor_counts` say, and how many `STREAM_OUTPUT` /
`STREAM_INPUT` descriptors the ROM generated **from that same config** actually
contains. It also checks the tracked pair — `hdl/common/csr/gen/adp_shape_defaults.svh`
and `hdl/ieee17221/aecp/gen/aecp_aem_rom.svh` — name the *same* source config
and match what it generates, and that the RTL consumes the include rather than
recomputing anything.

**And it runs before a build.** `sw/litex/build.sh` and `sw/litex/sweep.sh`
call `check_entity_shape.py --built-config <cfg>` and refuse to launch if the
tree carries another shape's definition, printing the one command that fixes
it. That is the arm that makes the 2026-07-27 defect unreproducible: a
`build.sh ax8x8` against a 1×1 entity definition now stops with

```
tracked ADP shape is endstation_ax7101_8x8's: got False, expected True
  the tree currently carries configs/endstation_arty_current.yaml. Fix:
    python3 sw/builder/endstation_builder.py configs/endstation_ax7101_8x8.yaml --write-rtl
```

Seven mutations must fail the gate, and each is proved to:

1. the builder's talker count excludes the CRF uid — the 2026-07-27 report,
   reproduced at the layer that now owns the number;
2. the sink count excludes the CRF sink (the `max(N, 2)` asymmetry);
3. `MEDIA_CLOCK_SOURCE` claimed by a config with no CRF output — what the boot
   script did for years;
4. the tracked shape include and the tracked descriptor ROM come from
   *different* configs — this defect with the layers swapped;
5. `milan_csr` regains a write arm for `0x618`;
6. `milan_datapath` goes back to computing its own context count;
7. a config edited without regenerating its shape include.

On the RTL side the harnesses elaborate **three different configs in one
suite** and read the shape back: `tb/verilator/csr` `sim_main` on the tracked
1×1 (1/2, caps `0x4001`), `sim_win` on `endstation_arty_4x4` (5/5), `sim_live`
on `endstation_ax7101_8x8` (9/9) — the last two with 0x800 windows of 4×4 and
2×2 respectively, so a value tracking the window instead of the config would
show. `tb/verilator/milan_dp` decodes **ADPDU bytes 38–45 off the MAC TX port**
at N = 1 and reads `0x618`/`0x61C` at N = 4 and N = 8, including "the CRF uid is
inside the advertised range" and a write that must change nothing. Reverting
`milan_csr` to the pre-fix RW behaviour fails 11 checks in `tb/verilator/csr`
and 8 in `tb/verilator/milan_dp`, with the ADPDU fields reading `0x0000` — what
the flashed board would advertise with no boot script at all.

## What this does NOT fix

* **[M-CLK-2] is untouched.** That gap is the CRF stream not being carried as
  a reserved class-A stream ([`NXN_ARCHITECTURE.md`](../NXN_ARCHITECTURE.md)
  step (c): the `0x800` window addresses talker idx `< T` only, so no lwSRP
  attribute row reaches the CRF output). This finding is purely about
  **discoverability** — being advertised so a controller can bind it. The two
  are independent.
* **The ROM consumer cannot express every shape the builder can emit.** A
  config with no CRF sink has no `AEM_CRF_FMTS_C` table, so
  `gen_aem_store.spec_from_overlay` refuses it. `build()` records that instead
  of failing, and `--write-rtl` refuses outright — a shape whose descriptor set
  cannot be generated is a shape that cannot be built, and saying so is better
  than emitting counts with no descriptors behind them.
* **Nothing here has been on silicon.** `VERSION` moved to `0x0001_0015`; the
  flashed bitstream is `0x0001_0014` (see
  [FLASH_0x0014_0727.md](FLASH_0x0014_0727.md)) and still has writable
  `0x618`/`0x61C`. The boot script keeps a `VERSION < 0x15` shim so an
  un-reflashed board does not fall back to advertising nothing at all.
