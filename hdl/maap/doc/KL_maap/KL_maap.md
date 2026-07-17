# Entity: KL_maap
- **File:** `hdl/maap/KL_maap.sv`
- **Spec:** IEEE 1722-2016 Annex B (MAAP); contract byte-extracted from pipewire module-avb `maap.c` (see `docs/design/MAAP_FABRIC.md`)

Dynamic multicast-DMAC allocation for the Milan talker: probe/defend/announce state machine over the `91:E0:F0:00:00:00`/0xFE00 pool. Three PROBEs at 500 ms + jitter, then ANNOUNCE at 3-5 s forever; the claim (`addr_o`) is valid only in ANNOUNCE. A conflicting received PROBE re-randomizes while probing and is DEFENDed (with the exact overlap sub-range) while announced; a conflicting received DEFEND/ANNOUNCE (their CONFLICT fields - reference behavior) re-randomizes unconditionally. Randomness = a station-MAC-seeded 16-bit LFSR (offset choice + interval jitter). `seed_offset_i`/`seed_valid_i` let provisioning re-claim the previously won block (the reference's persisted state).

## Generics

| Generic | Type | Default | Description |
|---------|------|---------|-------------|
| `CLK_FREQ_HZ_P` | `int unsigned` | `50_000_000` | ms-tick divider base |

## Ports

| Port | Dir | Type | Description |
|------|-----|------|-------------|
| `clk_i` / `rst_n` | in | `wire` | Clock / active-low sync reset |
| `enable_i` | in | `wire` | CSR MAAP_CTRL.en |
| `count_i` | in | `wire [7:0]` | Block size to claim (reference: 8) |
| `station_mac_i` | in | `wire [47:0]` | Source MAC + LFSR seed |
| `seed_offset_i` / `seed_valid_i` | in | | Provisioning re-claim seed |
| `rx_t*_i` | in | | RX AXIS monitor tap (never driven) |
| `m_axis_*` | out | | MAAP PDUs (60 B padded) to the low-rate TX arbiter |
| `addr_o` | out | `logic [47:0]` | Allocated base DMAC (pool + offset) |
| `addr_valid_o` | out | `logic` | 1 = ANNOUNCE (gates AAF admission when enabled) |
| `state_o` / `offset_o` / `conflicts_o` / `defends_o` | out | | CSR 0x6D0/0x6D4 observability |

## Integration

`milan_datapath`: `eff_aaf_dmac = (MAAP_CTRL.en && addr_valid) ? addr_o : cfg_aaf_dmac` feeds the AAF framer, AECP and ACMP reporting; `aaf_gate` ANDs `addr_valid` when enabled. en=0 keeps static provisioning bit-exact.
