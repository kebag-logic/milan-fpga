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
- **[The fix: the shape is elaborated, not provisioned](#the-fix-the-shape-is-elaborated-not-provisioned)** — `0x618`/`0x61C` become read-only words built from the same localparams that size the ACMP context arrays, so the advertised range *is* the addressable range by construction.
- **[The listener side had the same hole](#the-listener-side-had-the-same-hole)** — `ACMP_SINKS_C` was `max(N, 2)`, which reserved the CRF sink up to N = 2 and then silently dropped it.
- **[What is gated now](#what-is-gated-now)** — The three-way agreement check and the five mutations that must fail it.
- **[What this does NOT fix](#what-this-does-not-fix)** — The AEM descriptor ROM is not regenerated per build, and M-CLK-2 is a different gap.

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

## The fix: the shape is elaborated, not provisioned

`0x618` and `0x61C` are now **read-only**. They are assembled once from
elaboration parameters and served from the defaults ROM exactly like `CAP` and
`VERSION` — no storage, no write arm, no `is_plain_rw` entry:

```systemverilog
localparam logic [31:0] ADP_TALK_C = {ADP_TALKER_CAPS_P,   16'(N_TALKER_SRC_P)};
localparam logic [31:0] ADP_LIST_C = {ADP_LISTENER_CAPS_P, 16'(N_LISTENER_SINK_P)};
```

and `milan_datapath` passes **the very localparams that size the ACMP context
arrays**:

```systemverilog
localparam int ACMP_SRC_C   = (N_STREAMS > 1) ? N_STREAMS + 1 : 1;   // AAF talkers + CRF output
localparam int ACMP_SINKS_C = (N_STREAMS > 1) ? N_STREAMS + 1 : 2;   // AAF sinks   + CRF sink
...
milan_csr #(.N_TALKER_SRC_P(ACMP_SRC_C), .N_LISTENER_SINK_P(ACMP_SINKS_C), ...)
```

`KL_acmp_tlkr_ctx` accepts a probe iff `talker_unique_id < N_SRC_P`, and
`N_SRC_P` **is** `ACMP_SRC_C`. So the advertised range and the bindable range
are now the same expression, not two numbers that happen to agree. There is no
edit that can move one without moving the other.

`talker_capabilities` follows the same rule: `MEDIA_CLOCK_SOURCE` (`0x0800`)
is set only when a CRF source context exists, so a 1×1 build advertises
`0x4001` instead of the `0x4801` the boot script had been writing — that bit
had nothing behind it at N = 1.

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
is now `(N > 1) ? N + 1 : 2`, symmetric with the talker side and byte-identical
at N = 1.

## What is gated now

`scripts/check_entity_shape.py` asserts, per end-station config, that the same
number appears in all three places: the ADPDU counts `milan_csr` will serve,
the AEM `STREAM_OUTPUT`/`STREAM_INPUT` descriptor counts the builder emits, and
the ACMP context counts the gateware elaborates. It **parses the two localparam
expressions out of `milan_datapath.sv`** and evaluates them, so the gate cannot
drift away from the design it is checking.

Five mutations must fail it, and each is proved to:

1. the advertised talker count drops the CRF uid (`ACMP_SRC_C = N_STREAMS`) —
   the 2026-07-27 report, reproduced;
2. the sink count regresses to `max(N_STREAMS, 2)`;
3. `milan_csr` regains a write arm for `0x618`;
4. `milan_csr` regains the `is_plain_rw` entries (the half that actually makes
   a written value stick on readback);
5. a config whose model loses one `STREAM_INPUT` while `N_STREAMS` does not
   move.

On the RTL side the harnesses decode **ADPDU bytes 38–45 off the MAC TX port**
(`tb/verilator/milan_dp`, N = 1) and read `0x618`/`0x61C` at N = 4 and N = 8,
including "the CRF uid is inside the advertised range" and a write that must
change nothing. Reverting `milan_csr` to the pre-fix RW behaviour fails 11
checks in `tb/verilator/csr` and 8 in `tb/verilator/milan_dp`, with the ADPDU
fields reading `0x0000` — which is what the flashed board would have advertised
without the boot script at all.

## What this does NOT fix

* **The AEM descriptor ROM is not regenerated per build.**
  `hdl/ieee17221/aecp/gen/aecp_aem_rom.svh` is a single tracked artifact
  generated from the 1×1 `endstation_arty_current` shape (2 `STREAM_INPUT`,
  1 `STREAM_OUTPUT`), and **every** build includes it — the 8×8 one too. The
  builder already emits the correct overlay and `avdecc/gen_aem_store.py
  --overlay` already consumes it (a 4×4 CRF-output overlay is test-gated), but
  nothing in `sw/litex/build.sh` or `sweep.sh` runs that step, and no config
  owns the tracked ROM the way `srp.rtl_table` owns the lwSRP tables. So the
  ADPDU counts are now right and an 8×8 board's descriptor set is still the
  1×1 one. **Before flashing an N > 1 build, the ROM has to be regenerated
  from that config's overlay**, or a controller enumerating
  `STREAM_OUTPUT[1..8]` gets `NO_SUCH_DESCRIPTOR`. The gate checks the tracked
  ROM against the config that owns the RTL tables, which is where this
  ownership hole becomes visible.
* **[M-CLK-2] is untouched.** That gap is the CRF stream not being carried as
  a reserved class-A stream ([`NXN_ARCHITECTURE.md`](../NXN_ARCHITECTURE.md) step (c): the `0x800`
  window addresses talker idx `< T` only, so no lwSRP attribute row reaches
  the CRF output). This finding is purely about **discoverability** — being
  advertised so a controller can bind it. The two are independent.
* **Nothing here has been on silicon.** `VERSION` moved to `0x0001_0015`; the
  flashed bitstream is `0x0001_0014` (see
  [FLASH_0x0014_0727.md](FLASH_0x0014_0727.md)) and still has writable
  `0x618`/`0x61C`. The boot script keeps a `VERSION < 0x15` shim so an
  un-reflashed board does not fall back to advertising nothing at all.
