# CBS default-shaping bug  -  reset config paced ALL best-effort TX at 300 Mb/s [FIXED]

> ⚠️ **Point-in-time snapshot (2026-07-08).** Superseded  -  for current RX/TX numbers and the live bottleneck/lever see [`RX_TX_PERFORMANCE.md`](RX_TX_PERFORMANCE.md) + [`../CHANGELOG.md`](../../CHANGELOG.md). Numbers and "next steps" below are historical.

*Found 2026-07-08 during the >500 Mbit/s campaign, by following the datapath-input
probe's 39–42 % `stall` to its source instead of assuming it; verified live on silicon
with two devmem writes; **fixed** the same night (`CBS_EN_RST = 4'b0000`, commit
`34cc2bc`, gateware `build_dp100_cbs0`, WNS +0.031). Regression:
`tb/verilator/csr` (76 checks, reset-default assertions updated).*

Sibling doc: [`CBS_DATAPATH_BUG.md`](CBS_DATAPATH_BUG.md)  -  an unrelated 2026-07-05
classifier-timing bug in the same subsystem. This one is **pure configuration**: the
RTL shaped correctly; the *defaults* told it to shape the wrong traffic.

## Symptom

TCP TX plateaued at **238–247 Mbit/s** on the 100 MHz datapath with the datapath-input
probe showing a persistent **`stall` ≈ 39–42 %** (reader has a beat, datapath refuses).
The stall survived the reader-prefetch refutation (reader was 3.8 % busy  -  see
`TX_READER_PREFETCH_PLAN.md`), so the back-pressure had to originate *inside*
`traffic_controller_802_1q`. A stage-probe triangulation pinned it:

| probe | stalls | conclusion |
|---|---|---|
| `tx_dma` (reader → datapath in) | **418 ‰** | input refused 41.8 % of cycles |
| `tx_dp` (datapath → MAC out) | **0 ‰** | the MAC/store-and-forward NEVER back-pressures |
| `tx_core` (post-SF → LiteEth) | 179 ‰ | normal wire pacing, absorbed by tx_sf |

Output never blocked + input stalled 42 % + only 4 % busy ⇒ **long no-grant windows
while data is queued**  -  the CBS credit gate.

## Root cause  -  two defaults contradicting each other

`hdl/csr/milan_csr.sv` reset values:

```systemverilog
localparam int CBS_IDLE_RST [0:3] = '{300_000_000, 200_000_000, 150_000_000, 100_000_000};
localparam bit [3:0] CBS_EN_RST   = 4'b0011;   // (old) shape q0,q1 at reset
```

…while the classifier defaults route **untagged/best-effort traffic to q0**
(`cls_ctrl=1` → PCP mode, `cls_dpcp=0` → PCP 0, identity `cls_map`, `cls_tcq=0xE4` →
TC0 → q0). The comment above the CBS block even says non-SR classes stay unshaped per
REQ-CBS-02  -  the intent assumed q0/q1 were SR classes, but the default class map sends
plain TCP exactly there. Net effect: **every best-effort frame was credit-paced at
idleSlope = 300 Mb/s** from power-on. (At the earlier 50 MHz datapath the mis-scaled
`CLK_FREQ_HZ` made the effective slope lower still  -  a contributor to the old
145–186 Mbit/s era that was attributed to other walls.)

Nothing in the boot chain reprograms the CBS group, so the default *was* the product
behaviour.

## Verification on silicon (before fixing)

Read back live (`build_dp100_p0`): `q0 idle=0x11E1A300` (= 300,000,000) `en=1`,
`q1 en=1`, q2/q3 `en=0`  -  exactly the RTL defaults. Then, mid-session:

```
devmem 0x9000040C 32 0     # q0 CBS_CTRL.en = 0   (0x0900_0400 + q*0x20, +0xC = en)
devmem 0x9000042C 32 0     # q1
```

→ `tx_dma` stalls collapsed **418 ‰ → 4 ‰ on the spot**, and the TX wall moved cleanly
to the CPU (reader `idle` 394 ‰ → 809 ‰). With the shaper out of the way and coalesce
tuning, TX measured **265 single / 339 −P4 / 354 dual-process** at 84–96 % CPU  -  the
~250 plateau was the shaper all along.

## The fix

```systemverilog
localparam bit [3:0] CBS_EN_RST = 4'b0000;  // ALL unshaped at reset
```

CBS shapes **reserved SR classes only, never best-effort**: software (SRP/AVDECC stream
reservation, or `tc … cbs`) opts a queue in by setting `CBS_CTRL[0]` at reservation
time. The slope/credit reset values stay (they are sensible SR-class presets); only the
enable default changes. `tb/verilator/csr` reset-default checks updated
(`CBS0_EN(reset) == 0`); 76 checks green. Built as `build_dp100_cbs0` (WNS +0.031) and
**verified at reset on silicon** (q0–q3 `en=0`).

## Lessons

* **A default is product behaviour.** The shaper RTL was correct and sim-proven; the
  power-on register file quietly imposed a 300 Mb/s policy on all plain traffic. Config
  defaults deserve the same cross-checking as logic  -  here two default groups
  (classifier map, CBS enables) each looked fine alone and contradicted each other.
* **Never assume, always measure** (the campaign's standing rule): the 39 % stall had
  already been mis-attributed twice (datapath cycle cost, then the reader). The
  three-probe triangulation (`in` stalled / `out` clean / wire paced) took one script
  and pointed at the only remaining stage; two devmem writes proved it reversibly,
  before any rebuild.
* Probe-triangulation recipe for "who back-pressures": put busy/stall counters at a
  block's input **and** output  -  `in.stall high + out.stall 0` means the block itself;
  equal stalls mean it merely propagates.
