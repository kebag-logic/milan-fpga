# Open-toolchain synthesis check (Yosys) — device portability

This proves the Milan RTL is **vendor-neutral**: now that the Xilinx XPM primitives
are gone (see [`docs/integration/OPEN_SOURCE_MIGRATION.md` (archived)](../../historical_now_obsolete/integration/OPEN_SOURCE_MIGRATION.md)),
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

## Contents

- **[How it works](#how-it-works)** — The two-stage pipeline and why each stage is there: sv2v converts the SystemVerilog Yosys cannot parse (interfaces, packages, assignment patterns), then `hierarchy -check` is what makes a PASS mean something — it fails on any surviving vendor primitive, so green = fully mapped to generic logic with nothing Xilinx-specific left.
- **[Tooling](#tooling)** — The two binaries you need and where to get them. No Xilinx tools are required, which is the point — this flow is the evidence that the RTL is not tied to one vendor's toolchain.
- **[Coverage](#coverage)** — What the tops actually span, and the standing rule that the `tops=()` array is the count while this prose is not. Also names the one deliberate gap: `milan_top`, which pulls in the RGMII SelectIO and PS block design.
- **[Notes](#notes)** — Two facts that stop you misreading the output: the concrete non-Xilinx targets (`synth_ecp5`, `synth_ice40`) with real cell counts, and why `axis_fifo` looks enormous — its 4096-deep default, which no instance in the design uses.
- **[ooc.sh — AREA measurement (a different question from run.sh)](#oocsh--area-measurement-a-different-question-from-runsh)** — `run.sh` asks *does it map*; this asks *what does it cost*, which is the only number an area lever may be judged on. Three traps it exists to avoid, and the third is the sharpest: `-flatten` can read a genuinely deleted block as **−1 LUT / −0 FF**, so a structural lever needs the hierarchy-preserving form as well. Ends with the honest caveat — these are estimates with a yosys→Vivado ratio between 0.25 and 0.86, and control sets are not measurable here at all.

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
44 tops as of 2026-08-13 (the `tops=()` array in `run.sh` is authoritative — that
array is the count, this prose is not; re-read it rather than trusting a number
here):

- the new open blocks (`tcam`, `rx_mac_filter`, `cdc_pulse`, `cdc_handshake`,
  `adp_tx_arbiter`),
- the control plane (`KL_pp_shadow`, `KL_pp_maap_shim`) — the protocol
  processor as this datapath instantiates it. The 1722.1/SRP tops it replaced
  (`adp_advertiser`, `KL_aecp_top`, the two ACMP contexts and their two
  wrappers, `KL_persist_journal`, `KL_lwsrp_top`) are gone with that RTL,
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

**These are estimates, not Artix LUT6 counts.** The yosys→Vivado LUT ratio
measured against this tree's own two Vivado anchors is **0.31 … 0.71** —
see [NXN_ARCHITECTURE](../../docs/NXN_ARCHITECTURE.md) section 6.3. Quote a
band, never a single figure, and never call an `ooc.sh` number a placement
result. **Flip-flops are the exception**: they convert one-for-one (the
`KL_pcm_lpf` row is 756 FF in both toolchains), which makes an FF count the
best available sanity check on an estimate.

**Run the hierarchical instrument too, and say so when they disagree.** The
same sources with **no** `-flatten` and `stat -top <mod>` sum each submodule
into its parent: no cross-boundary optimisation, so absolute numbers are
high, but the hierarchy survives and per-block attribution is possible
(`abc` renames every cell in a flattened netlist, so nothing there can be
traced back). The two instruments agreed within 11 % on the 2026-07-27 logic
levers and disagreed 8× on the LPF prune; the hierarchical one was believed,
because it reproduces the place report's FF and DSP columns exactly. When
they disagree, prefer the instrument that reproduces a known Vivado row.

### `-flatten` has a THIRD trap: it can read a real prune as zero

Measuring the 2026-07-27 optional-block prunes
([AREA_BUDGET](../../docs/design/AREA_BUDGET.md)) found a case where
`-flatten` is not merely noisy but **wrong**. Removing `rx_mac_filter` +
`tcam` from `milan_datapath` reads as **−1 LUT / −0 FF** in a flattened
whole-design `stat`, and removing `KL_pcm_lpf` as **−14 LUT / −0 FF** — while
`yosys hierarchy -top milan_datapath` proves neither module is in the design
any more, and the blocks carry 1 691 and 756 flip-flops respectively. **A
flip-flop total cannot be unchanged by deleting 1 691 flip-flops**, so that
number is an artefact of whole-design flattening, not a measurement.

Rule that follows: `-flatten` is the right instrument for a **logic** lever
(rewrite a cone, keep the block), because both sides contain the same blocks
and the mapping noise is symmetric. For a **structural** lever (delete a
block), also run the hierarchy-preserving form and read the per-module `stat`
of the block you removed:

```sh
yosys -p "read_verilog dp.v; synth_xilinx -family xc7 -top milan_datapath; \
          stat -top milan_datapath"
```

If the two disagree by more than the cross-boundary slack, trust the
hierarchical one and say so. The tier-1 leaf blocks (`KL_mmcm_drp_servo`,
`KL_aaf_latency_taps`, `KL_maap`, `KL_i2s_playback`, `rx_mac_filter`, `tcam`,
`KL_pcm_lpf`) are tops in `ooc.sh`'s array for exactly this cross-check —
a standalone OOC figure is the **upper bound** for a prune, because in
context a block shares decode and constants with its neighbours.

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
