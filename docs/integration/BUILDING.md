# Building bitstreams  -  the two-board build flow

*2026-07-11. Canonical entry point: **`sw/litex/build.sh`**. This page is the
maintainer reference for it: what the named configurations are, the parallel
launch discipline the script encodes (and why each rule exists), how to add a
configuration, and the per-board load/console facts you need after a build
lands. Test layers around a build: ../testing/RUNNING_TESTS.md. Live lab
state: ../findings/SESSION_HANDOFF.md.*

## 1. Usage

```sh
cd sw/litex
./build.sh <config> [<config> ...] [--sweep] [--dry-run] [-- <milan_soc.py args>]
```

| Invocation | Effect |
|---|---|
| `./build.sh ax7101` | one build of the AX7101 ship shape |
| `./build.sh arty` | one build of the Arty A7-100 bring-up shape |
| `./build.sh ax7101 arty` | BOTH boards in parallel (90 s stagger) |
| `./build.sh ax7101 --sweep` | 3 builds: the config x the place-directive sweep |
| `TAG=fold2 ./build.sh arty` | output dir `work/build_arty_fold2` (default TAG = mmddHHMM) |
| `./build.sh arty -- --sys-clk-freq 90e6` | append/override milan_soc.py arguments |
| `./build.sh ... --dry-run` | print the exact launch commands, start nothing |

Outputs land in `/home/alex/litex-milan/work/build_<config>[_<directive>]_<TAG>/`
with a `*.launch.log` next to each. Builds run detached; check progress with
`grep -oE "Phase [0-9.]+ .*" <outdir>/gateware/vivado.log | tail -1` and gate on
the timing/utilization reports (see section 5).

## 2. The named configurations

A configuration is a bash function `cfg_<name>()` in `build.sh` that echoes the
full `milan_soc.py` argument list. One place to edit a board's canonical shape;
call-time deviations go through `-- <args>` (appended last, so argparse lets
them override).

### `ax7101`  -  Alinx AX7101, the perf/ship platform

xc7a100t**fgg484-2**, 1 GbE (RTL8211E strapped GMII), 512 MB DDR3
(MT41J256M16), 16 MB N25Q128 QSPI. Shape: 2x VexiiRiscv @100 MHz, datapath in
its own 100 MHz domain, 2 RX queues, header-split 16K pages (STRICT driver
pairing, kl-eth `hs_pgsz=16384`), `--strip-probes` (ship diet), QSPI flashboot
(hands-free Linux boot), `--gtx-tx-invert`, `--timing-opt --floorplan`, place
directive ExtraPostPlacementOpt (the measured density winner, 91.0 pct slices
vs 94.9 for the spread directives at identical RTL).

### `arty`  -  Digilent Arty A7-100, the second Milan node

xc7a100t**csg324-1** (SAME die, SLOWER speedgrade  -  expect tighter WNS at
100 MHz), 10/100 Ethernet (DP83848, **MII**; the SoC drives its 25 MHz
`eth_ref_clk`), 256 MB DDR3 (MT41K128M16), serial boot only (`--with-spiflash`
asserts on arty until the S25FL128S flashboot increment lands). Probes KEPT
(bring-up forensics). Role: AVDECC/Milan interop peer and the 100 Mbit CBS
test point (`is_1g=0` slope branch); not a throughput peer.

### Adding a configuration

1. Add `cfg_<name>() { echo "--board ... --cpu ..."; }` next to the others.
2. If it is a new BOARD (not just a shape), first port `milan_soc.py`:
   `--board` choice, platform import, `_CRG` clocking arm, DRAM module,
   `MilanMAC` phy_model, and the speed wiring  -  the arty arm (commit e32feaf)
   is the template. Elaborate WITHOUT `--build` before burning P&R time
   (RUNNING_TESTS layer 1).
3. Keep the pairing notes in the function comment: hs page size, flashboot,
   probe policy. A configuration IS the pairing contract for its board.

## 3. The launch discipline (why the script is not just a for-loop)

Every rule below was paid for on silicon or in lost build hours; the script
exists so they cannot be forgotten:

* **`--vivado-max-threads 32` always.** Vivado hard-caps at 32 threads and
  ERRORS above it (96 aborts P&R). Saturating the 96-core box = 3 parallel
  builds of 32, never one build of 96.
* **At most 3 concurrent builds.** The script refuses more; split the call.
* **90 s stagger between launches.** Two LiteX elaborations share the
  pythondata git checkout; concurrent first-touches race on `.git/index.lock`
  and one elaboration dies with CalledProcessError. The stagger serializes the
  checkout window only  -  P&R still overlaps fully.
* **`setsid nohup` + a launch log per build.** A harness/session bulk
  task-kill once reaped 4 running Vivado instances mid-route. Detached
  process groups survive anything short of a reboot.
* **`--sweep` = the 3-directive place sweep** (ExtraPostPlacementOpt,
  AltSpreadLogic_high, ExtraTimingOpt): placement is noise-dominated, so
  single important configs are built as sweeps and the best WNS/slices build
  is kept (the standing 96-core rule).

## 4. After the build: load + console, per board

ttyUSB numbers RENUMBER whenever a USB device is replugged. Always select
cables by serial and consoles by `/dev/serial/by-id/` path:

| Board | JTAG load | Console |
|---|---|---|
| AX7101 | `openFPGALoader --ftdi-serial 210512180081 -c ft232 <bit>` | CP2102N adapter (by-id path appears when attached to the VM), 115200; tmux session `milan_qspi_boot` |
| Arty A7-100 | `openFPGALoader --ftdi-serial 210319AFEED0 -c digilent <bit>` | same FT2232, channel B: `/dev/serial/by-id/usb-Digilent_Digilent_USB_Device_210319AFEED0-if01-port0`, 115200; tmux session `arty_console` |

AX7101 traps (details in SESSION_HANDOFF/QSPI_FLASHBOOT): the bitstream goes
to SRAM over JTAG (flash holds NO bitstream); NEVER `openFPGALoader -f` (it
clobbers the Linux kernel at flash offset 0); power-cycle blanks the FPGA.
The Arty has no flash images yet: after JTAG load, boot over serial
(`litex_term --kernel ...`) or run the BIOS interactively.

## 5. Gates before a build is "good"

1. **WNS >= 0** in `<outdir>/gateware/*_timing.rpt` (Design Timing Summary
   row). On the AX7101 keep comfortable margin  -  QSPI flashboot corrupted
   below +0.03 at 112.5 MHz; the -1 arty die will run tighter at 100 MHz.
2. **Utilization** vs the AREA-70 scoreboard (`*_utilization_place.rpt`:
   Slice LUTs / Slice / Block RAM Tile rows; hierarchical variants for
   attribution  -  but OOC-synth a module before believing its hierarchical
   line, see TROUBLESHOOTING (../limitations/) section 15).
3. **Silicon section V checklist** (RUNNING_TESTS): boot, ID=MILN, driver
   pairing probe, ghost-peer ARP check, TX gate, RX cells. A build that
   passes 1-2 but regresses the TX gate is NOT ship-cleared (see the open
   cbsf_epo TX investigation in SESSION_HANDOFF).
