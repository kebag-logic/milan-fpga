# Third-party (vendored) cores

Open-source RTL vendored as git submodules under `third_party/` (plus the `external`
AVB/Ethernet submodule and the `protocol-processor` control-plane submodule at the
repo root). See the de-Xilinx plan in
[`OPEN_SOURCE_MIGRATION.md` (archived)](historical_now_obsolete/integration/OPEN_SOURCE_MIGRATION.md) (archived).

| Submodule | Upstream | License | Pinned commit | Used by |
|-----------|----------|---------|---------------|---------|
| `external` | [github.com/kebag-logic/fpga-avb-ethernet](https://github.com/kebag-logic/fpga-avb-ethernet) | see submodule | `efeb541` | AVB/Ethernet MAC + PHY RTL for the datapath (`eth_mac_1g` family); vendored, no longer "assumed present at synth time". |
| `protocol-processor` | `protocol-processor-control-plane-avb-milan` (private upstream) | see submodule | `91f3b7c` | **This device's entire IEEE 1722.1 / SRP control plane** since 2026-08-13: ADP, ACMP talker and listener, SRP, and the live AECP micro-coded uCPU. Consumed through [`hdl/milan/KL_pp_shadow.sv`](hdl/milan/KL_pp_shadow.sv), instantiated unconditionally by `milan_datapath`. The processor contains an internal MAAP engine, but this shipping integration holds it disabled with `cfg_maap_internal_i = 0`; allocation stays in this fabric through `KL_maap` and `KL_pp_maap_shim`. Its served AECP inventory and remaining mandatory gaps are recorded in the [current Milan v1.2 audit](docs/testing/MILAN_V12_AUDIT_2026-08-16.md). Verify the live pin with `git submodule status protocol-processor` rather than trusting this cell. |
| [`third_party/verilog-axis`](third_party/verilog-axis) | [github.com/alexforencich/verilog-axis](https://github.com/alexforencich/verilog-axis) | MIT | `48ff7a7` | `axis_fifo` → `traffic_classifier`, `ptp_ts_top` (replacing `xpm_fifo_axis`, T1.2). `axis_demux`/`axis_arb_mux` planned for T1.3. |

## Generated third-party C (not a submodule)

| Path | Upstream | License | How it got there |
|------|----------|---------|------------------|
| `sw/trace/generated/barectf.[ch]`, `barectf-bitfield.h` | [barectf](https://barectf.org/) 3.1.2 | MIT (header in each file) | **Generated**, not copied: `barectf generate` over [`sw/trace/milan_trace.yaml`](sw/trace/milan_trace.yaml). Checked in so the repo gate runs without barectf installed; [`sw/trace/test_trace_roundtrip.py`](sw/trace/test_trace_roundtrip.py) gate 2 re-generates and byte-diffs when barectf *is* importable. Regeneration recipe: [`sw/trace/README.md`](sw/trace/README.md). |

[`sw/trace/generated/metadata`](sw/trace/generated/metadata) is the CTF 1.8 trace description barectf emits from
the same input; it carries the same MIT header and is the decode ABI shipped with
every trace.

Planned (later tracks):
- `third_party/verilog-axi` — `axi_dma`, `axi_crossbar`, `axil_crossbar`, `axil_cdc` (host / T2).
- `mdio_master`, `ptp_clock_cdc` (T1.4 / T2). *(The Ethernet MAC is now supplied by the `external`
  `fpga-avb-ethernet` submodule above — vendored, not assumed present at synth time.)*

## Working with submodules
```sh
git clone --recurse-submodules <repo>       # fresh clone
git submodule update --init --recursive     # existing clone
```
Bump a core by checking out a new commit inside the submodule and committing the new
gitlink. Do not copy files in — keep upstream fixes flowing via submodule bumps.
