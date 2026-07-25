<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->
# AAF end-to-end latency — where every tap sits (roadmap item-11)

This is deliverable #2 of the AAF-latency-breakdown directive: a picture of
**where in the TX and RX pipeline each latency point is measured**, mapped to
the exact RTL trigger and the CSR that reports it. The measurement engine is
`hdl/ieee1722/aaf/KL_aaf_latency_taps.sv`; the register block is
`REGISTER_MAP.md` §0x870; the per-sample DDR3 history is
[`LATENCY_HISTORY_RING.md`](LATENCY_HISTORY_RING.md).

All deltas are in **`axis_clk` cycles** — divide by the datapath clock
(100 MHz on the AX7101 ⇒ 10 ns/cycle) for seconds. Each chain follows **one
in-flight frame at a time**: it arms on a stage-0 edge (latching the gPTP
epoch) and takes the next edge at each later stage, so min/last/max
characterise the latency *envelope*, not one threaded frame id.

## TX pipeline (talker: capture → wire)

```mermaid
flowchart LR
    CAP["CAP<br/>pair captured<br/><small>aafcap_pv_w</small>"]
      -->|"D0 · CAP→SOF<br/>0x87C / 0x880"| SOF["PKT_SOF<br/>packetizer first beat<br/><small>aaf_tx_acc &amp; ~inframe</small>"]
    SOF -->|"D1 · SOF→EOF<br/>0x884 / 0x888"| EOF["PKT_EOF<br/>packetizer last beat<br/><small>aaf_tx_acc &amp; tlast</small>"]
    EOF -->|"D2 · EOF→MAC_TX<br/>0x88C / 0x890"| MAC["MAC_TX<br/>frame egress<br/><small>mac_tx_acc &amp; tlast</small>"]
    MAC -.->|"gPTP ns @ CAP"| EP["TX_EPOCH 0x874<br/>TX_INFO 0x878<br/><small>samples · timeouts</small>"]
```

* **CAP → PKT_SOF** (`D0`) spans up to one 6-sample AAF accumulation window —
  the packetizer only starts a frame once it has a full PDU's worth of pairs.
* **PKT_SOF → PKT_EOF** (`D1`) is the packetizer's own serialization time.
* **PKT_EOF → MAC_TX** (`D2`) is the CBS/shaper queue + MAC boundary. Under
  mixed traffic this shared boundary may catch a nearer non-AAF edge, which is
  why the envelope (min/max) matters more than a single sample here.
* The existing `ptp_ts_top` **TX hardware timestamp** stamps the actual wire
  egress independently; `TX_EPOCH` records the gPTP ns at the CAP edge so the
  fabric delta and the on-wire stamp can be reconciled.

## RX pipeline (listener: wire → PCM ring)

```mermaid
flowchart LR
    MRX["MAC_RX<br/>frame ingress<br/><small>mac_rx_acc &amp; ~inframe</small>"]
      -->|"D0 · MAC_RX→ACCEPT<br/>0x89C / 0x8A0"| ACC["ACCEPT<br/>AVTP monitor parse+accept<br/><small>avtprx_accept_p</small>"]
    ACC -->|"D1 · ACCEPT→DEPKT<br/>0x8A4 / 0x8A8"| DPK["DEPKT<br/>payload last beat<br/><small>dpkt_acc &amp; tlast</small>"]
    DPK -->|"D2 · DEPKT→PCM_RING<br/>0x8AC / 0x8B0"| RNG["PCM_RING<br/>payload into the ring<br/><small>ring_acc &amp; tlast</small>"]
    RNG -.->|"gPTP ns @ MAC_RX"| EP["RX_EPOCH 0x894<br/>RX_INFO 0x898<br/><small>samples · timeouts</small>"]
    RNG -.->|"playout"| I2S["I2S DAC fetch<br/><small>FIFO-fill dominated —<br/>see I2SPB_STAT</small>"]
```

* **MAC_RX → ACCEPT** (`D0`) is classify + stream-table match + the AVTP
  monitor's parse-to-accept verdict.
* **ACCEPT → DEPKT** (`D1`) is the depacketizer draining the accepted PDU.
* **DEPKT → PCM_RING** (`D2`) is the write into the `_PCMRingNxN` DRAM ring
  the ALSA card / PipeWire source consume.
* The final **I2S DAC playout** stage is FIFO-fill dominated (the CDC pair
  FIFO decouples PDUs from DAC frames), so it is characterised by the
  `I2SPB_STAT` fill/converged rails rather than a delta here.

## Tap → trigger → CSR (the authoritative map)

| # | stage edge | RTL trigger (`milan_datapath.sv`) | delta CSR (last/max · min) |
|---|---|---|---|
| TX0 | CAP (pair captured) | `aafcap_pv_w` | `0x87C` · `0x880` |
| TX1 | PKT_SOF (first beat) | `aaf_tx_acc_w & ~aaf_tx_inframe_r` | `0x884` · `0x888` |
| TX2 | PKT_EOF (last beat) | `aaf_tx_acc_w & aaf_tx_tlast` | `0x88C` · `0x890` |
| TX3 | MAC_TX (egress) | `mac_tx_acc_w & m_axis_mac_tx_tlast` | — (chain end) |
| RX0 | MAC_RX (ingress) | `mac_rx_acc_w & ~mac_rx_inframe_r` | `0x89C` · `0x8A0` |
| RX1 | ACCEPT (monitor) | `avtprx_accept_p` | `0x8A4` · `0x8A8` |
| RX2 | DEPKT (payload last) | `dpkt_acc_w & dpkt_pcm_tlast_w` | `0x8AC` · `0x8B0` |
| RX3 | PCM_RING (ring write) | `ring_acc_w & m_axis_pcm_tlast` | — (chain end) |

`TX_EPOCH`/`RX_EPOCH` (`0x874`/`0x894`) carry the gPTP ns latched at the
stage-0 edge; `TX_INFO`/`RX_INFO` (`0x878`/`0x898`) carry `{timeouts, samples}`.
A per-stage timeout (`MILAN_CLK_FREQ_HZ/2000` ≈ 0.5 ms) aborts and re-arms a
stuck token so a dropped frame can never wedge a chain (counted in `timeouts`).

## Reading it live

```sh
# one-shot snapshot of every stage (on the board)
for a in 874 878 87C 884 88C  894 898 89C 8A4 8AC; do
  printf '0x%s = %s\n' $a "$(devmem 0x90000$a 32)"; done
# clear stats and re-measure:  devmem 0x90000870 32 0x3   (W1S clear + enable)
```

The full per-sample time series (not just min/last/max) is streamed to a
DDR3-backed ring and read back through its own CSR window — see
[`LATENCY_HISTORY_RING.md`](LATENCY_HISTORY_RING.md).
