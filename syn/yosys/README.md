# Open-toolchain synthesis check (Yosys) — device portability

This proves the Milan RTL is **vendor-neutral**: now that the Xilinx XPM primitives
are gone (see [`docs/OPEN_SOURCE_MIGRATION.md`](../../docs/integration/OPEN_SOURCE_MIGRATION.md)),
every block maps to a **generic, device-independent** cell library with the
open-source [Yosys](https://yosyshq.net/yosys/) synthesizer — so it will build on
non-Xilinx FPGAs (Lattice ECP5/iCE40, Gowin, Efinix, ASIC flows, …), not just Vivado.

It complements the Verilator harnesses (`tb/verilator/`, which prove *behaviour*) by
proving *synthesizability on other devices*.

```sh
git submodule update --init third_party/verilog-axis   # required: several tops
                                                        # elaborate Forencich cores
cd syn/yosys
make            # generic synth (device-independent) of every top -> RESULT: PASS
make ecp5       # map to a real non-Xilinx device: Lattice ECP5 (TRELLIS_FF/LUT4)
```

## How it works
1. **[sv2v](https://github.com/zachjs/sv2v)** converts the SystemVerilog (interfaces,
   packages, assignment patterns) to Verilog-2005 — Yosys's built-in frontend does
   not handle SV interfaces. Interface-port modules (`traffic_classifier`,
   `traffic_queues`) are synthesised through their flat wrappers in `tb/verilator/*`.
2. **Yosys** runs `synth` (generic) then `hierarchy -check`. `hierarchy -check` fails
   if any **undefined / vendor primitive** remains, so a PASS means the module is
   fully mapped to generic logic (`$_AND_`, `$_DFF_`, `$_MUX_`, …) — nothing
   Xilinx-specific left.

## Tooling
- `yosys` (Arch: `pacman -S yosys`).
- `sv2v` on `PATH` — prebuilt static Linux binary from
  [github.com/zachjs/sv2v/releases](https://github.com/zachjs/sv2v/releases)
  (drop into `~/.local/bin`). No Xilinx tools required.

## Coverage
18 tops (the `tops=()` array in `run.sh` is authoritative): the new open blocks (`tcam`, `rx_mac_filter`, `cdc_pulse`, `cdc_handshake`,
`adp_advertiser`, `adp_tx_arbiter`), the CSR (`milan_csr`), the de-Xilinx'd 802.1Q
datapath (`classifier_wrap`→`traffic_classifier`, `queues_wrap`→`traffic_queues`),
the CBS/PTP/RMON leaves, the vendored Forencich cores (`axis_fifo`, `axis_demux`,
`axis_arb_mux` — kept as a portability check even though the queue egress now
uses a plain grant-indexed mux instead of `axis_arb_mux`), and **`milan_datapath`
itself** (the full integration wrapper, which pulls in `ptp_ts_top`/`ptp_ts_core`
hierarchically). Not covered: `milan_top` (RGMII SelectIO + PS block design, T2)
and `avtp_stream_parser` (has a Verilator harness but no yosys top yet — a known
gap, see [`docs/limitations/KNOWN_ISSUES_AND_LIMITATIONS.md`](../../docs/limitations/KNOWN_ISSUES_AND_LIMITATIONS.md)).

## Notes
- `synth_ecp5` (Lattice ECP5) and `synth_ice40` (iCE40) are concrete non-Xilinx
  targets — `make ecp5` maps e.g. `tcam`→~1.7 k `TRELLIS_FF`, `milan_csr`→~2.2 k.
- `axis_fifo`'s large cell count is its default `DEPTH=4096` RAM; instances in the
  design set a small depth.
