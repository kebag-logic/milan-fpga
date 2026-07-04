# Pipeline telemetry (`milan_tlm_*`) — in-fabric observability for the TX/RX path

A memory-mapped block of free-running counters at every stage of the packet pipeline —
the numbers a HW developer wants to answer "where did the frame go?" and "where does it
queue up?". Implemented in `sw/litex/milan_soc.py` as `MilanDebug` (the LiteX binding) and
read from Linux via the `kl-eth` driver's `telemetry` sysfs group.

## What it measures

At each TX and RX AXIS stage, three counters:

| suffix | meaning | use |
|--------|---------|-----|
| `*_frames` | completed frames (`valid & ready & last`) | a frame present at stage N but missing at N+1 **localises the loss** |
| `*_beats`  | beats (`valid & ready`)                    | frame size, throughput |
| `*_stalls` | back-pressure cycles (`valid & ~ready`)    | the **bottleneck** is the stage stalled by its consumer |

Stages, in pipeline order:

```
TX:  tx_dma  →  tx_dp  →  tx_core  → [LiteEth core] →  tx_wire (GMII pins)
RX:  rx_wire → [LiteEth core] → rx_core →  rx_dp   →  rx_dma
```

- `tx_dma`/`rx_dma` — the Wishbone DMA read/write (memory edge).
- `tx_dp`/`rx_dp` — the `milan_datapath` AXIS boundary (classifier/shaper live between here
  and the DMA side).
- `tx_core`/`rx_core` — the LiteEth MAC core in/out.
- `tx_wire`/`rx_wire` — **frames actually on the GMII pins** (eth_tx/eth_rx clock domains,
  brought to sys with a `BusSynchronizer`). This is the answer to "did it reach the wire?".

Plus:
- `cycles` (64-bit) — free-running sys cycles; the normaliser for rates/averages.
- `tx_datapath_inflight_acc` / `rx_datapath_inflight_acc` (64-bit) — Σ(frames_in − frames_out)
  per cycle across the datapath. By **Little's law**: `avg occupancy = acc/cycles`, `avg
  latency (wait) = acc/frames`. The average FIFO depth and the average time a frame spends
  crossing the datapath.
- `tx_gptp` / `rx_gptp` — example filtered counter: frames with EtherType `0x88F7` (802.1AS).

## Coherent capture

Every counter runs live. Writing **`capture`** latches ALL of them into shadow registers on
the same clock edge; the CSRs then read the shadow. So software takes **one consistent
snapshot** instead of reading values that keep moving between reads. **`reset`** zeroes the
live counters.

## Reading it from Linux

The `kl-eth` driver maps the `tlm` reg window and exposes a sysfs group:

```sh
cat  /sys/class/net/eth0/telemetry/snapshot   # capture + dump every counter + Little's-law averages
echo 1 > /sys/class/net/eth0/telemetry/reset  # zero the counters
echo 1 > /sys/class/net/eth0/telemetry/capture# just latch (then read milan_tlm_* by hand with devmem)
```

`snapshot` reads are one coherent set. Typical TX-debug flow: `echo 1 > reset`, send N frames,
`cat snapshot` — and read down the TX column: if `tx_dma_frames == tx_dp_frames ==
tx_core_frames` but `tx_wire_frames` is 0, the frames die in the LiteEth core / PHY, not the
datapath. Rising `*_stalls` upstream of a stage points at that stage as the bottleneck.

The raw CSRs are also `devmem`-pokeable at the `tlm` window base (see `csr.json`
`milan_tlm_*`; e.g. `0xf000_4000` on the AX7101 build): `reset +0x00`, `capture +0x04`,
`cycles +0x08` (64-bit MS-word first), then the `frames/beats/stalls` triplets.

## Extending it

The probe primitives are public methods on `MilanDebug` — add an observable in one line,
inline or via the `extra(dbg)` hook:

```python
dbg.sys_probe("my_stage", some_endpoint, "desc")          # frames/beats/stalls
dbg.wire_probe("my_wire", ep, "eth_tx", "desc")           # count in another clock domain
dbg.ethertype_probe("rx_ptp_ev", mac.dbg_rx_dp, 0x88F7, "…")   # filtered by EtherType
dbg.match_probe("drops", ep, drop_condition, "…")         # any per-frame condition
dbg.inflight_acc("seg", frames_in, frames_out, "…")       # occupancy/latency of a segment
```

All are auto-`snapshot`-latched and CSR-mapped; then add a line to the driver's `snapshot_show`
to print it. gPTP (`ethertype_probe`) is the worked example.

## Cross-platform (LiteX vs Zynq)

`MilanDebug` is the **LiteX** binding — it uses LiteX for the LiteX-specific things (LiteX
`CSRStatus`, `BusSynchronizer`, and taps on the `WishboneDMA` and `LiteEthPHYGMII` edges).
The **shared** observables — everything at the `milan_datapath` AXIS boundary (`tx_dp`/`rx_dp`)
and inside it — are identical on Zynq; their cross-platform home is counters in the shared
`milan_datapath.sv` exposed through the shared `milan_csr` block (`0x9000_0000` on LiteX,
`0x43c0_0000` on Zynq), so the Zynq wrapper gets them for free and only re-binds its own edges
(`axi_dma`, its MAC). Rule of thumb: **datapath-internal** probes belong in the SV/`milan_csr`
path (both platforms); **edge/SoC-fabric** probes (DMA↔memory, MAC↔wire) belong in the
per-platform wrapper like `MilanDebug`.

## Addressing note

The block is named `milan_tlm` so its CSRs sort **after** `milan_dma`/`milan_mac`, keeping
their addresses stable — the telemetry window is purely **additive** (nothing else moves
whether or not it is built).
