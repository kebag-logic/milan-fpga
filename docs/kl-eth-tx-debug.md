# kl-eth TX debug — "link up, RX works, but the peer never sees our frames"

**Symptom.** After the FPGA boots Linux and `kl-eth` binds the Milan NIC, `eth0` comes up at
1 Gbps full-duplex and **RX works** (the FPGA receives frames from a peer), but nothing the
FPGA transmits reaches the peer: pings get no reply, the peer's ARP entry for the FPGA stays
`INCOMPLETE`, and the peer's MAC RX counters do not move. `eth0`'s own `tx_packets` counter
*does* increment.

**Root cause (gateware, not the driver).** TX frames were **truncated to their first 8-byte
beat** inside the LiteEth MAC core, then zero-padded to the 60-byte Ethernet minimum. Only the
first 8 bytes (the destination MAC + 2 bytes) survived, so the peer dropped every frame. The
`kl-eth` driver and the DMA were correct all along. **One-line fix in the gateware** (see the
bottom). This bug had been latent since M-A3 because that bring-up only ever checked the peer's
`rx_broadcast`/`rx_unicast` *counters*, which key off the destination MAC — and the destination
MAC lives in the surviving first beat, so a truncated frame still incremented them.

This document records the full diagnostic chain so the technique is reusable.

## Test rig (generic)

- The FPGA `eth0` is connected — directly or through an inline gigabit tap — to a **peer host
  with a known-good gigabit NIC** (an Intel i210 was used here; anything whose `ethtool -S`
  exposes per-frame RX counters works). Call the peer NIC `<peer-nic>`.
- Put both ends in one subnet, e.g. FPGA `eth0 = 192.0.2.10/24`, peer `<peer-nic> = 192.0.2.2/24`.
- The **peer's HW counters are the reliable signal** — on-FPGA there is no `tcpdump`, and a
  monitor capture on the peer (`tcpdump -e -xx -n -i <peer-nic>`) shows the *raw bytes* on the
  wire, which is what finally cracked this.

Useful register windows (all pokeable from the FPGA shell with `devmem`; addresses are for the
fully-FPGA NaxRiscv/LiteX SoC):

| What | Address | Notes |
|------|---------|-------|
| `milan_csr` ID | `0x90000000` | reads `0x4D494C4E` = "MILN" |
| MAC_CTRL / MAC_STATUS | `0x90000100` / `0x90000110` | `0x13`=tx+rx+1G, status `0x0D`=up/1000/FDX |
| TX-DMA base/len/enable/done/offset | `0xf0003000`/`08`/`0c`/`10`/`18` | base 64-bit MSW-first; len+offset in **bytes**/**words** |
| RX-DMA base/len/enable/done/offset | `0xf000301c`/`24`/`28`/`2c`/`34` | |
| MAC internal loopback | `0xf0003810` | `1` = loop datapath TX→datapath RX, bypassing the LiteEth core+PHY |

> The RMON good/error counters (`0x90000210…0x90000230`) read **0 in this build** — the LiteEth
> core does not drive `i_mac_events`, so they are hardwired 0. Do **not** use them as a signal.

## The diagnostic chain (each step ruled something in or out)

1. **Driver vs. link.** `ip -s link` showed `tx_packets` climbing while the peer's `rx_*`
   counters were frozen → frames leave the driver but don't land. Not a "TX disabled" problem
   (`MAC_CTRL = 0x13`, `MAC_STATUS = 0x0D` → up, 1000, full-duplex).

2. **Is the physical path even bidirectional?** Had the peer ping the FPGA: the FPGA's RX
   counter climbed and it received correct 64-byte ARP frames. So **RX works** and the medium
   carries both directions (a 1000BASE-T link that's up is inherently bidirectional). The
   failure is TX-specific, not a broken cable.

3. **Does anything reach the peer at all?** A promiscuous `tcpdump` on the peer **did** capture
   the FPGA's frames — so they *are* on the wire, just malformed (the peer's MAC drops them, so
   the counters stay flat). Not physical.

4. **What exactly is on the wire?** `tcpdump -xx` of a normal ARP showed
   `00 00 ff ff ff ff ff ff` then **all zeros** — i.e. ~8 bytes then nothing. Two hypotheses:
   truncation, or the DMA reading stale/zero DRAM (a coherency signature).

5. **Controlled frame (removes all skb/stack ambiguity).** Wrote a known frame to a scratch
   DRAM address with `devmem` — `ff ff ff ff ff ff 06 07 08 09 0a 0b … 3f` (broadcast dst +
   incrementing payload) — pointed the TX-DMA at it, fired it, and captured the wire:

   ```
   wire:  ff ff ff ff ff ff 06 07   00 00 … 00      (60 bytes total)
   mem:   ff ff ff ff ff ff 06 07   08 09 0a 0b …    (64 bytes)
   ```

   - **Byte 0-7 are byte-perfect** → byte order is correct and coherency works (the DMA read
     word 0 exactly). Rules out endianness and cache-coherency.
   - **Bytes 8-63 are gone** and the frame is exactly **60 bytes** = 8 data bytes MAC-padded to
     the 60-byte minimum → the frame was **truncated to one 8-byte beat**, not "full frame with
     zero content" (that would be 64 bytes on the wire).

6. **DMA vs. datapath vs. MAC core.** `milan_dma_tx_offset` read **8** after the transfer → the
   DMA read all 8 words; it does not truncate. Then the internal **loopback** (which taps the
   datapath's `m_axis_mac_tx` output, *before* the LiteEth core) was armed with a manual RX-DMA:
   the looped frame came back **8 words, byte-exact** (`ff ff ff ff` … and byte 8 = `08 09 0a 0b`).
   So **the datapath emits the full, correct frame** — the truncation is strictly inside the
   **LiteEth MAC core TX path** (`core.sink` → 64→8 conversion → GMII), which loopback bypasses.

7. **The exact line.** The MAC's AXIS→LiteEth glue drove `core.sink.last_be` **on every beat**
   (`keep & ~(keep>>1)` = `0x80`, because the datapath forces `tkeep=0xff` on all beats). In the
   64→8 down-converter that `last_be=0x80` maps to `last_be=1` on **byte 7 of every 64-bit
   beat**, and LiteEth's `LiteEthMACTXLastBE`/`LiteEthLastHandler` does:

   ```python
   source.last.eq(sink.last_be != 0)                 # end-of-frame on ANY beat with last_be != 0
   If(source.last & ~sink.last, NextState("WAIT-LAST"))   # …then discard the rest of the frame
   ```

   So the first beat's byte 7 was tagged "last", the FSM went to WAIT-LAST, and **bytes 8..N were
   discarded**. `last_be` is only valid on the *last* beat — driving it on every beat is a
   protocol violation. (M-A3's earlier fix corrected the *byte count* — `0x80` instead of the low
   bit, so 8 bytes survived instead of 1 — but left `last_be` asserted on every beat, so the
   frame was still cut to one beat. The counter-only check couldn't see it.)

## The fix (gateware — `milan-fpga`, `sw/litex/milan_soc.py`, `MilanMAC`)

Gate `last_be` by `last` so it is non-zero only on the final beat:

```python
self.core.sink.last_be.eq(Mux(tx_dp.sys.last,
                              tx_dp.sys.keep & ~(tx_dp.sys.keep >> 1), 0)),
```

Requires a gateware rebuild + reflash. Verify with step 5's controlled `devmem` frame (wire ==
memory, full length) and then an end-to-end ping to the peer + the peer's `rx_*` counters moving.

## Reusable takeaways

- **Never trust dst-MAC-keyed counters (`rx_broadcast`/`rx_unicast`) as proof of TX** — a frame
  truncated to its first beat still increments them. Capture *raw bytes* or use a full-length
  echo/ping round-trip.
- The **internal loopback CSR** cleanly splits "datapath output" from "LiteEth core + PHY" — arm
  a manual RX-DMA and read its `offset` to measure the datapath's output frame length.
- A **controlled `devmem` frame** (known bytes to scratch DRAM → TX-DMA → wire capture) removes
  the skb/stack/coherency variables and gives an exact memory→wire transform.
- `dma_tx_offset == length/8` proves the DMA moved the whole frame; truncation after that is
  downstream (datapath or MAC core), which loopback then localizes.

## Second bug — TX-to-wire: the 2026-07-04 investigation log (OPEN, bisection running)

After the `last_be` fix, TX to the peer kept failing. This section is the **complete,
chronological experiment log** — including two wrong theories that measurements later
killed, because knowing *why they were wrong* is as valuable as the result.

### The instrument set

* `milan_tlm` pipeline telemetry ([pipeline-telemetry.md](pipeline-telemetry.md)) — frame
  counts at every fabric stage, readable from Linux sysfs **and from the BIOS**
  (`mem_write 0xf0004004 1` = capture, `mem_read 0xf0004058` = tx_wire).
* Controlled BIOS-level TX (no kernel needed): boot to `litex>` (no uploader), then
  `mem_write 0x90000100 0x13` (MAC en), frame words at `0x40000000` (wire byte order),
  TX-DMA `0xf0003000/4/8` (base hi/lo, length bytes), toggle `0xf000300c` 0→1 per frame;
  `mem_read 0xf0003010` = done, `0xf0003018` = offset in 8-byte words.
* Peer i210: `ethtool -S` **full-diff** (not selected counters) + promiscuous
  `tcpdump -e -xx`.
* Vivado `open_checkpoint` on the routed `.dcp` — physical placement of the TX launch FFs.

### The result matrix (identical 10-frame broadcast burst everywhere)

| build | source/flags | DMA | TXD launch (DCP-verified) | gtx phase | tx_wire | peer |
|---|---|---|---|---|---|---|
| build_gmii_final (Jul 3) | pre-gating `last_be` (truncates to 8 B!) | coherent | fabric `SLICE_X1` | edge | 10 | **10/10** ⚠ truncated frames |
| build_qspi_gtx | Jul 4 code | **non-coherent** | fabric | 180° | 10 | 0/10 |
| build_qspi_gtx_coh | Jul 4 code | coherent | fabric | 180° | 10 | 0/10 |
| build_final | Jul 4 code | coherent | fabric `SLICE_X14` | edge | 6 | 0/6 |
| build_iob/_inv | Jul 4 code (IOB constraint **silently skipped**) | coherent | fabric `SLICE_X14` | edge/180° | 10 | 0/10 |
| build_iob2/_inv | Jul 4 code (IOB fixed) | coherent | **OLOGIC_X0** | edge/180° | 10 | 0/10 |

Plus, under Linux on `build_qspi_gtx_coh`/`build_final` (coherent): **RX is fully healthy**
(peer ARPs → `rx_wire=rx_core=rx_dp=rx_dma` → netdev 0-dropped → neighbor learned,
`devmem` of the RX buffer shows correct wire bytes), and TX is fabric-perfect with real
data (`tx_dma=tx_dp=tx_core=tx_wire`, byte counts matching) — yet nothing reaches the peer.

### What is PROVEN

1. **`--coherent-dma` is mandatory** (not implied by `--all-blocks`; deploy.sh now carries
   it). Without it: RX skbs are all zeros (stack drops 100 %), TX reads stale DRAM (frames
   egress with garbage dst-MAC that the peer silently address-filters — Δ0 *without* CRC
   errors, a perfect PHY-problem impostor). Boot-to-boot "intermittency" = cache-eviction
   luck.
2. **The FPGA fabric TX path is correct in every build** (counters + real data verified).
3. **The wire + PHY TX are capable** — gmii_final transmits 10/10 *today*.
4. **On every Jul-4 build the PHY emits NOTHING onto copper**: full peer counter diff shows
   no movement (not even undersize/CRC/error counters); promiscuous tcpdump captures zero
   frames — while `tx_wire` counts frames *into* the PHY and the eth_tx clock demonstrably
   runs (the counter lives in that domain). Silence, not corruption ⇒ **not a
   sampling-margin problem**.

### What is DISPROVEN (and by what)

* **"gtx_clk↔TXD phase (edge-aligned) is the bug"** — OLOGIC-placed data with 180°-shifted
  clock (textbook mid-bit sampling) is equally silent. Phase changes nothing measurable.
* **"TX FF placement/skew is the bug"** — OLOGIC (pad-locked, skew≈0) equally silent.
  (Placement *does* matter for margin once TX talks again — keep the IOB constraint — but
  it is not what silences the PHY.)
* **My `--gtx-tx-invert` "fix"** — never validated; keep OFF pending re-test.

### Traps documented (each cost real time)

1. **dst-keyed counters lie — twice now.** gmii_final "passing 10/10" was itself the trap
   re-sprung: its pre-gating `last_be` truncates every frame to 8 bytes + MAC padding, and
   the peer's `rx_broadcast` counts truncated frames indistinguishably from full ones. A
   valid TX pass **requires tcpdump content verification** of the full frame.
2. **XDC does not execute TCL control flow.** A `set_property` wrapped in `if {…}` is
   silently ignored — verify constraints took effect in the routed `.dcp`
   (`get_cells -of …` → expect `OLOGIC`, not `SLICE`), never trust the .xdc text.
3. **buildroot `linux-reconfigure` does not rebuild out-of-tree modules** (and MODVERSIONS
   is off): a stale `kl-eth.ko` vermagic-matches, loads, and oopses on shifted struct
   layouts (`devm_register_netdev → devres_add`, NULL+0x270). Always
   `make kl-eth-rebuild rootfs-cpio` after kernel .config changes.
4. **The peer NIC address-filters garbage-MAC frames without counting them anywhere** —
   "nothing at the peer" ≠ "nothing on the wire" unless tcpdump ran in promisc.

### Open question + bisection (running)

The one systematic difference between the *talking* build and every *silent* one is the
**Jul-4 source itself** — prime suspect: the gated `last_be` change (its full-frame TX has
in fact never been observed working), plus telemetry/MilanMAC edits, spiflash, 1.5 M UART.
Two concurrent discriminating builds:

* **B1** — Jul-4 code, gmii_final-equivalent flags (no spiflash, 115200): splits
  {feature set} vs {code}.
* **R0** — the actual `bc5783b` source rebuilt with today's toolchain (worktree):
  splits {source} vs {toolchain/patch drift}.

| B1 | R0 | conclusion |
|---|---|---|
| talks | talks | spiflash or 1.5 M UART silences the PHY |
| silent | talks | Jul-4 milan-fpga code (bisect: last_be gate → telemetry → MilanMAC edits) |
| silent | silent | toolchain / liteeth-or-litex patch drift |

Acceptance for ANY "fixed" claim: 10/10 at the peer **and** tcpdump shows the full 64-byte
payload **and** a Linux ping round-trip completes.
