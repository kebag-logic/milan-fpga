# Open-toolchain synthesis check (Yosys) — device portability

This proves the Milan RTL is **vendor-neutral**: now that the Xilinx XPM primitives
are gone (see [`docs/integration/OPEN_SOURCE_MIGRATION.md`](../../historical_now_obsolete/integration/OPEN_SOURCE_MIGRATION.md)),
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
47 tops as of 2026-07-26 (the `tops=()` array in `run.sh` is authoritative — that
array is the count, this prose is not; re-read it rather than trusting a number
here):

- the new open blocks (`tcam`, `rx_mac_filter`, `cdc_pulse`, `cdc_handshake`,
  `adp_advertiser`, `adp_tx_arbiter`),
- the CSR (`milan_csr`),
- the de-Xilinx'd 802.1Q datapath (`classifier_wrap`→`traffic_classifier`,
  `queues_wrap`→`traffic_queues`),
- the CBS/PTP/RMON leaves,
- the vendored Forencich cores (`axis_fifo`, `axis_demux`, `axis_arb_mux` —
  kept as a portability check even though the queue egress now uses a plain
  grant-indexed mux instead of `axis_arb_mux`), and
- **`milan_datapath` itself** (the full integration wrapper, which pulls in
  `ptp_ts_top`/`ptp_ts_core` hierarchically).

Not covered: `milan_top` (RGMII SelectIO + PS block design, T2). The
`avtp_stream_parser` gap noted here previously is **closed** — it is a top in
the array.

## Notes
- `synth_ecp5` (Lattice ECP5) and `synth_ice40` (iCE40) are concrete non-Xilinx
  targets — `make ecp5` maps e.g. `tcam`→~1.7 k `TRELLIS_FF`, `milan_csr`→~2.2 k.
- `axis_fifo`'s large cell count is its default `DEPTH=4096` RAM; instances in the
  design set a small depth.

## `ooc.sh` — AREA measurement (a different question from `run.sh`)

`run.sh` answers *"does this map to generic logic"* and gates on it.
`ooc.sh` answers *"what does it cost"*, which is the only number an area
lever may be judged on:

```sh
./ooc.sh                      # every top in its AREA list
./ooc.sh KL_chan_map_render   # just these
OOC_CHPARAM="N_STREAMS=8 AUDIO_IF_SLOTS_P=16" ./ooc.sh milan_datapath
OOC_TMP=/some/dir ./ooc.sh …  # keep the .v / .log / .json artefacts
```

It runs `sv2v` → `synth_xilinx -family xc7 -flatten` → `stat` and reports
`LUT1..6`, `FD[CPRS]E?`, `RAMB36E1`, `RAMB18E1`, `DSP48E1`.

Two traps this exists to avoid:

- **`-flatten` is not optional.** A hierarchical synth's `stat` counts
  *top-level* cells only, so a lever inside a submodule reads as exactly
  zero — which looks like a clean "no regression" and is not.
- **The SV defaults are not the ship shape.** `milan_datapath` defaults
  `N_STREAMS = 1`, which constant-folds the NxN engines away; measuring
  there reads as a free win. Use `OOC_CHPARAM`, or force the parameter
  defaults in a scratch copy of `hdl/` when `chparam` cannot re-elaborate
  the `sv2v` output (it cannot, for the interface-carrying tops).

**These are estimates, not Artix LUT6 counts.** The yosys→Vivado ratio
measured against this tree's own place report ranges 0.25 (wide muxes,
shared serial arithmetic) to 0.86 (the whole flattened datapath) — see
[NXN_ARCHITECTURE](../../docs/NXN_ARCHITECTURE.md) section 6.3. Quote a band, never a single figure, and
never call an `ooc.sh` number a placement result.

**Control sets are NOT measurable here.** A yosys proxy was tried and
discarded: counting `(clock, enable, set/reset)` triples over the `FD*` cells
of the flattened netlist reports **18 691** sets for `milan_datapath`'s
24 002 flops, against Vivado's **1 612** for the whole 56 k-flop design —
yosys keeps a private enable net per flop and never merges them the way
Vivado's `opt_design` does, so the proxy is ~12x wrong and its *delta* is
meaningless too. Use the build's own `report_control_sets` output
(`<board>_control_sets.rpt`), whose summary line
"Unused register locations in slices containing registers" is the actual
packing loss.
