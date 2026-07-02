# `kl-eth` — Milan TSN NIC Linux driver

The platform net driver that binds to the [`kl,dma-ether`](../dts/milan.dtsi) device
tree node and drives the Milan NIC over its CSR/DMA ABI
([`docs/REGISTER_MAP.md`](../../docs/REGISTER_MAP.md)). It lives in the sibling repo
**`../../kl-linux-drivers`** (`kl-eth.c`); this note is the contract it implements.

## DT match & resources
- `of_match`: `compatible = "kl,dma-ether-0.9"` (FR-DT-01).
- `reg`/`reg-names`: `csr` (`0x43C0_0000`), `dma-tx`, `dma-rx`, `dma-ts`.
- `interrupts`/`-names`: `tx-dma`, `rx-dma`, `ts-dma`, `csr` → NAPI + link/PTP events.
- `kl,txq-cnt`/`kl,rxq-cnt`, `kl,shaped-queues` (`<0 1>`), `phy-handle`, `phy-mode`,
  `local-mac-address`, `kl,ptp*`.

## Feature surface → CSR (see `docs/FR_NFR.md` §2.10 `FR-DRV-*`)
| Linux feature | Hook | HW / CSR |
|---------------|------|----------|
| NAPI RX/TX, N queues | `netif_napi_add`, `netif_set_real_num_*_queues` | DMA rings + `IRQ_STATUS` |
| XDP + AF_XDP ZC | `ndo_bpf`, `ndo_xdp_xmit`, `xsk_pool` | RX DMA, page-pool |
| PHC + HW timestamps | `ptp_clock_info`, `ndo_hwtstamp_set` | PTP `0x500`, ts-metadata DMA |
| ethtool | `get_ts_info`/`-S`/`-l`/`-g`/`-c` | RMON `0x200`, CAP `0x008` |
| CBS/mqprio offload | `ndo_setup_tc` `TC_SETUP_QDISC_CBS` | CBS `0x400` (only `kl,shaped-queues`) |
| MDIO/phylib | `phy_connect`, `adjust_link` | fabric MDIO master, `MAC_STATUS`/`PHY_RESET` |
| RX filter | `ndo_set_rx_mode` | MC_HASH `0x114/0x118` + TCAM `0x700` |
| AVDECC entity_id | derive EUI-64 from MAC | ADP `0x600` (`ADP_ENTITY_ID`) |

## CBS offload policy
`ndo_setup_tc(CBS)` only accepts offload for queues listed in `kl,shaped-queues`
(reset `<0 1>`); Σ idleSlope of the shaped queues must stay ≤ 75 % of the port rate
(the HW forces every other queue to strict priority — `credit_based_shaper.sv`,
`REGISTER_MAP` §0x400).
