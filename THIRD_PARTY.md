# Third-party (vendored) cores

Open-source RTL vendored as git submodules under `third_party/`. See the de-Xilinx
plan in [`docs/OPEN_SOURCE_MIGRATION.md`](docs/OPEN_SOURCE_MIGRATION.md).

| Submodule | Upstream | License | Pinned commit | Used by |
|-----------|----------|---------|---------------|---------|
| `third_party/verilog-axis` | [github.com/alexforencich/verilog-axis](https://github.com/alexforencich/verilog-axis) | MIT | `48ff7a7` | `axis_fifo` → `traffic_classifier`, `ptp_ts_top` (replacing `xpm_fifo_axis`, T1.2). `axis_demux`/`axis_arb_mux` planned for T1.3. |

Planned (later tracks):
- `third_party/verilog-axi` — `axi_dma`, `axi_crossbar`, `axil_crossbar`, `axil_cdc` (host / T2).
- `third_party/verilog-ethernet` — `mdio_master`, `ptp_clock_cdc` (T1.4 / T2). *(The MAC
  `eth_mac_1g_rgmii_fifo` is from this project and assumed present at synth time.)*

## Working with submodules
```sh
git clone --recurse-submodules <repo>       # fresh clone
git submodule update --init --recursive     # existing clone
```
Bump a core by checking out a new commit inside the submodule and committing the new
gitlink. Do not copy files in — keep upstream fixes flowing via submodule bumps.
