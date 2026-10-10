# Entity: KL_maap
- **File:** `hdl/ieee1722/maap/KL_maap.sv`
- **Spec:** IEEE 1722-2016 Annex B (MAAP), the authority since #686; the clause-by-clause contract is in [`docs/design/MAAP_FABRIC.md`](../../../../../docs/design/MAAP_FABRIC.md#annex-b-contract)

Dynamic multicast-DMAC allocation for the Milan talker: the Table B.7 probe/defend/announce machine over the `91:E0:F0:00:00:00`/0xFE00 pool. Four PROBEs, the first at once and then 500 < T < 600 ms apart; the first ANNOUNCE follows the fourth PROBE at once and repeats every 30 < T < 32 s. The claim (`addr_o`) is valid only in ANNOUNCE. Every frame carries `control_data_length` 16, and a DEFEND goes to the source MAC of the PROBE that caused it. A conflicting received PROBE applies compare_MAC while probing. It restarts only when this station is not lower. While announced, the engine sends DEFEND with the overlap sub-range. A conflicting DEFEND always restarts while probing. While announced, it applies the same compare_MAC rule. A conflicting ANNOUNCE (judged on its requested fields) re-randomizes while probing, and while announced only when compare_MAC says this station is not the lower. Randomness uses a 32-bit LFSR with period 2^32 - 1 (offset choice + interval draws). First enable samples the low 32 bits of the programmed MAC plus the local real-time clock. A zero seed takes a nonzero fallback. `seed_offset_i`/`seed_valid_i` let provisioning re-claim the previously won block (Table B.7 note a); the supplied range must fit inside the dynamic pool. Invalid supplied ranges fall back to a bounded random draw.

## Contents

- **[Generics](#generics)** — One parameter, `CLK_FREQ_HZ_P` — the base for the millisecond tick divider, so it must match the datapath clock or every PROBE/ANNOUNCE interval scales wrong.
- **[Ports](#ports)** — The interface, including the two that are easy to miss: `seed_offset_i`/`seed_valid_i` let provisioning re-claim a previously won block, and `addr_valid_o` is only high in ANNOUNCE — it is the admission gate, not a "module is running" flag.
- **[Integration](#integration)** — The one expression that decides whether the claimed address or the statically provisioned one reaches the AAF framer, and the guarantee that comes with it: `en = 0` keeps static provisioning bit-exact.

## Generics

| Generic | Type | Default | Description |
|---------|------|---------|-------------|
| `CLK_FREQ_HZ_P` | `int unsigned` | `50_000_000` | ms-tick divider base |

## Ports

| Port | Dir | Type | Description |
|------|-----|------|-------------|
| `clk_i` / `rst_n` | in | `wire` | Clock / active-low sync reset |
| `enable_i` | in | `wire` | CSR MAAP_CTRL.en |
| `port_operational_i` | in | `wire` | Rising link status revokes validity and re-probes |
| `count_i` | in | `wire [7:0]` | Block size to claim (reference: 8) |
| `station_mac_i` | in | `wire [47:0]` | Source MAC + first-enable LFSR seed |
| `realtime_ns_i` | in | `wire [31:0]` | Synchronous local PHC nanoseconds, added to the MAC at first enable |
| `seed_offset_i` / `seed_valid_i` | in | | Provisioning range, validated against the dynamic pool |
| `rx_t*_i` | in | | RX AXIS monitor tap (never driven) |
| `m_axis_*` | out | | MAAP PDUs (60 B padded) to the low-rate TX arbiter |
| `addr_o` | out | `logic [47:0]` | Allocated base DMAC (pool + offset) |
| `addr_valid_o` | out | `logic` | 1 = ANNOUNCE (gates AAF admission when enabled) |
| `state_o` / `offset_o` / `conflicts_o` / `defends_o` | out | | CSR 0x6D0/0x6D4 observability |

## Integration

`milan_datapath`: `eff_aaf_dmac = (MAAP_CTRL.en && addr_valid) ? addr_o : cfg_aaf_dmac` feeds the AAF framer, AECP and ACMP reporting; `aaf_gate` ANDs `addr_valid` when enabled. en=0 keeps static provisioning bit-exact.
