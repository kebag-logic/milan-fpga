# Troubleshooting  -  every problem hit bringing up the full-FPGA solution, and its fix

This is the field log of every real problem encountered building and simulating the
fully-FPGA Milan softcore solution, with the **symptom**, the **cause**, and the
**fix**. It is meant to save the next developer the debugging time. Grouped as:
toolchain/environment ([Sections 1–2](#section-1-import-litex-resolves-to-a-namespace-package)),
LiteX/SoC build ([Sections 3–6](#section-3-identifier-string-must-not-contain-commas)),
Verilator simulation ([Sections 7–8](#section-7-verilator-cannot-find-include-file)),
shell/process ([Section 9](#section-9-pkill--f-self-matches-the-running-shell)),
synthesis ([Section 10](#section-10-yosys--sv2v-cannot-find-axis_mux_rr_2in_1out)),
RTL/testbench ([Sections 11–14](#section-11-milan_dp-axi-write-bfm-did-not-commit-writes)),
P&R timing closure ([Sections 15–16](#section-15---full-fails-100-mhz-timing-in-the-cbs-credit-shaper):
CBS pipelining + running the dense datapath in its own CDC clock domain for a clean 100 MHz),
and on-hardware NIC bring-up ([Section 17](#section-17-on-hardware-nic-bring-up--dma-works-but-no-packet-on-the-wire-its-gmii-not-rgmii):
the AX7101 PHY is GMII, not RGMII).

Companion: [`SIMULATION.md`](SIMULATION.md) (how the sim works) and
[`FULL_FPGA_SOLUTION.md`](FULL_FPGA_SOLUTION.md) (the architecture).

---

## Section 1: import litex resolves to a namespace package

**Symptom.** All CPU imports fail with
`ImportError: cannot import name 'get_data_mod' from 'litex'`, and
`litex.__file__` is `None`.

**Cause.** The LiteX repos are installed *editable* into the venv, but they live under
`~/litex-milan/`, and that directory *also* contains a subdir literally named
`litex/`. When Python is started with `~/litex-milan` as the working directory (or on
`sys.path`), `import litex` resolves to that **repo-root directory**  -  a namespace
package with no `__init__.py`  -  instead of the editable-installed inner package that
defines `get_data_mod`. Hence `__file__ is None` and the symbol is missing.

**Fix.** Run every build/sim command from a directory that is **not** the litex-repos
parent  -  e.g. `~/litex-milan/work/`:
```sh
cd ~/litex-milan/work         # anywhere except ~/litex-milan itself
python .../milan_soc.py ...
```
Verify: `python -c "import litex; print(litex.__file__)"` must print a real path
ending `…/litex/litex/__init__.py`, not `None`.

## Section 2: NaxRiscv generation needs JAVA_HOME

**Symptom.** The SoC build dies during "NaxRiscv netlist generation", or `sbt` fails
to launch, or the AMD/Xilinx installer's bundled JRE is reported missing.

**Cause.** The NaxRiscv core is generated on demand from **SpinalHDL (Scala)**: LiteX
clones `SpinalHDL/NaxRiscv` and runs `sbt "runMain naxriscv.platform.litex.NaxGen …"`.
That needs a JDK on `PATH`/`JAVA_HOME`. It is not installed by default.

**Fix.** Install JDK 17 + sbt and export `JAVA_HOME`:
```sh
sudo pacman -S --needed jdk17-openjdk sbt
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
export PATH="$JAVA_HOME/bin:$PATH"
```
First generation also downloads Scala/SpinalHDL (network needed once); subsequent
builds reuse the cached netlist (`NaxRiscvLitex_<hash>.v`).

## Section 3: Identifier string must not contain commas

**Symptom.** `ValueError: Identifier string must not contain commas` from
`litex/soc/cores/identifier.py` during SoC construction.

**Cause.** `SoCCore(ident=…)` writes the identifier into a hardware string ROM and
forbids commas. The first draft used `ident=f"Milan TSN SoC (NaxRiscv RV{xlen}, …)"`.

**Fix.** Remove commas from the ident string:
```python
ident=f"Milan TSN SoC - NaxRiscv RV{xlen} {cpu_count}-core"
```

## Section 4: SoCError at _finalize_cpu_reset_address (no ROM)

**Symptom.** The build reaches `builder.build(...)` then raises a bare
`litex.soc.integration.soc.SoCError` from `_finalize_cpu_reset_address`. The bus
slave list shows only `sram`, `main_ram`, `csr`  -  no `rom`.

**Cause.** The CPU's reset vector points at the integrated ROM, but no integrated ROM
was added, so LiteX cannot place the reset address.

**Fix.** Give the SoC an integrated ROM (the BIOS lives there and holds the reset
vector):
```python
kwargs.setdefault("integrated_rom_size", 0x20000)
```

## Section 5: NaxRiscv has no attribute no_netlist_cache

**Symptom.** `AttributeError: type object 'NaxRiscv' has no attribute
'no_netlist_cache'` in `naxriscv/core.py:add_sources`.

**Cause.** NaxRiscv keeps its configuration in **class attributes** that are normally
populated by its own argparse flow (`args_fill()` + `args_read(args)`). The first
draft hand-set only `xlen`/`data_width`, so other required attributes
(`no_netlist_cache`, `update_repo`, `with_fpu`, `l2_bytes`, …) were never set.

**Fix.** Drive the CPU's own arg pipeline  -  fill a parser with its args, take the
defaults, override just xlen/cpu-count, then `args_read`:
```python
_p = argparse.ArgumentParser(); NaxRiscv.args_fill(_p)
_na, _ = _p.parse_known_args([]); _na.xlen = xlen; _na.cpu_count = cpu_count
NaxRiscv.args_read(_na)
```

## Section 6: Region not in IO region, it must be cached

**Symptom.**
`ERROR:SoCBusHandler:milan_csr Region not in IO region, it must be cached: Origin:
0x43c00000 … Cached: False` and the build aborts with `SoCError`.

**Cause.** On NaxRiscv the address map marks `0x8000_0000–0xFFFF_FFFF` as the uncached
**IO region**; any uncached MMIO slave must live there. The Zynq build put `milan_csr`
at `0x43C0_0000`, which is below the IO region, so it is rejected as uncached.

**Fix.** Map the CSR window inside the IO region  -  the design uses **`0x9000_0000`**.
The register *offsets* are unchanged; only the base is host-specific (documented in
[`REGISTER_MAP.md`](REGISTER_MAP.md)). The device-tree `reg` base must match the host.

## Section 7: Verilator cannot find include file

**Symptom.** The softcore sim build fails with
`%Error: … Cannot find include file: 'ethernet_packet_pkg.sv'` (and `ethernet_events.svh`),
even though those files are added as sources.

**Cause.** ``include "ethernet_packet_pkg.sv"`` is a bare include with no path.
**Vivado auto-searches the directories of all added source files; Verilator does
not**  -  it only searches `-I`/`+incdir` paths. The RTL sources were added, but their
directories were never added as include paths, so the sim (Verilator backend)
couldn't resolve the includes. (The board Vivado build worked, masking the problem.)

**Fix.** Add the include directories explicitly. In the shared datapath helper:
```python
for inc in ("hdl/common", "hdl/802_1q_traffic_shaper", "hdl/ptp_timestamp",
            "hdl/adp", "hdl/csr", "hdl/eth_event_counter"):
    platform.add_verilog_include_path(os.path.join(base, inc))
```
The RTL harness Makefiles do the same with `+incdir+<dir>`.

## Section 8: The interactive and non-interactive sim both block

**Symptom.** Driving the softcore sim to run a `mem_read` was flaky: a pty driver got
`OSError: Subprocess failed` from `_run_sim`; fixed sleep-then-command timing sent the
command *during* the multi-minute Verilator compile; and `milan_sim.py
--non-interactive` never returned so a chained piped run never started.

**Cause (three-part).**
1. LiteX **couples build and run**  -  `builder.build(sim_config, interactive=…)` builds
   the `Vsim` binary *and* runs it in the same call.
2. `--non-interactive` still **runs** the sim; with no stdin it just sits at the
   `litex>` prompt forever, so any command chained after it never executes.
3. The `OSError` from `_run_sim` was simply the sim exiting non-zero because the
   driver **SIGKILL'd** it  -  expected, not the real failure. The real failure was the
   command being consumed before the prompt existed (compile still running).

**Fix.** Separate build from run: build once, then run the **cached `Vsim` binary
directly** with the command on a plain stdin pipe (`serial2console` bridges the sim
UART to stdio). Verilator caches the compile, so the direct run boots in seconds:
```sh
# build once (Ctrl-C at the first "litex>"), then:
cd build_milan_sim/gateware
{ sleep 4; printf 'mem_read 0x90000000 16\n'; sleep 5; } | ./obj_dir/Vsim
```
Also set `BIOS_NO_DELAYS` + `BIOS_NO_MEMTEST` so the prompt appears in seconds (the
memtest/memspeed are very slow at the simulated 1 MHz), guaranteeing the piped command
lands *after* the prompt. See
[Section 3.3](SIMULATION.md#section-33-the-scripted-path-used-to-capture-the-evidence)
of [`SIMULATION.md`](SIMULATION.md).

## Section 9: pkill -f self-matches the running shell

**Symptom.** Commands that tried to clean up the sim exited with `144`/`143` and no
output; the shell appeared to be killed mid-command.

**Cause.** `pkill -f "milan_sim.py …"` matches against **full command lines**  -  and the
very shell running the `pkill` has that pattern in *its own* argv, so `pkill` kills its
own parent shell.

**Fix.** Kill by the exact process name, never the pattern:
```sh
pkill -x Vsim           # exact binary name  -  cannot match the shell
```

## Section 10: Yosys / sv2v cannot find axis_mux_rr_2in_1out

**Symptom.** The Yosys device-portability check passes 17 tops then fails
`milan_datapath` with
`ERROR: Module '\axis_mux_rr_2in_1out' referenced in module '\ptp_ts_top' … is not
part of the design`. The Verilator build of the same module had *not* complained.

**Cause.** `ptp_ts_top` instantiates `axis_mux_rr_2in_1out` (in `hdl/common/`), which
was missing from the explicit source list. **Verilator auto-resolves undefined modules
from the directories of the input files** (so it silently found it), but **sv2v/Yosys
only compile the files you list**  -  so the module was undefined there.

**Fix.** Add the file explicitly to both flows (`syn/yosys/run.sh` top entry and the
`tb/verilator/milan_dp` Makefile source list):
```
hdl/common/axis_mux_rr_2in_1out.sv
```
General rule: never rely on Verilator's directory auto-resolution  -  list every source
explicitly so sv2v/Yosys and Verilator agree.

## Section 11: milan_dp AXI-write BFM did not commit writes

**Symptom.** In the `milan_dp` harness, a CSR written over AXI-Lite read back as `0`
(`CLS_REGEN` read `0x0` instead of the written `0x00FAC688`), while reads of reset
values worked.

**Cause.** The first AXI-write BFM sampled `awready`/`wready` *after* the rising clock
edge and deasserted `awvalid`/`wvalid` independently. `milan_csr` is a
**single-outstanding** slave that accepts AW and W together; that timing let the write
address/data desynchronize so the write never committed.

**Fix.** Copy the proven pattern from the `csr` harness: sample `*ready` while the
clock is **low** (combinationally), then pulse the rising edge to commit, holding AW
and W valid together until both readys assert:
```cpp
for (int g = 0; g < 64; g++) { lo(); bool acc = awready && wready; hi(); if (acc) break; }
```
All 11 `milan_dp` checks pass after this. (This same class of bug  -  sampling on the
wrong clock phase  -  is worth checking first whenever a write "silently does nothing".)

## Section 12: Benign Verilator warnings (PINMISSING and SELRANGE)

**Symptom.** Verilator prints `%Warning-PINMISSING` and `%Warning-SELRANGE` during
harness builds.

**Cause / why safe.**
- `PINMISSING` on `axi_stream_if`: the interface declares optional `clk`/`rst_n` pins
  that the datapath instances legitimately leave unconnected (unused in those blocks).
- `SELRANGE` inside Forencich `axis_fifo.v`: `m_axis[ID_OFFSET +: ID_WIDTH]` and the
  DEST/USER equivalents select out-of-range bits, but only inside ternary branches
  that are **dead** because `ID_ENABLE`/`DEST_ENABLE`/`USER_ENABLE` are 0.

**Fix.** Suppress them in the harness `VFLAGS` (they are noise, not defects):
```
-Wno-PINMISSING -Wno-SELRANGE
```

## Section 13: traffic_queues silently dropped a frame

**Symptom.** (Earlier, `queues` harness.) A frame routed into a queue was lost  -  the
`queue_has_data`/output collapsed as if the frame were discarded.

**Cause.** Only the arbiter's `tvalid` was gated by the per-queue grant, while the FIFO
read (`m_axis_tready`) was left ungated. The `axis_arb_mux` prefetches
(`s_axis_tready = ~s_axis_tvalid_reg | …`), so it *drained and dropped* the frame from
the FIFO even when it had no grant to forward it.

**Fix.** Gate **both** sides by the grant  -  the arbiter `tvalid` **and** the FIFO
`m_axis_tready`  -  so a queue without a grant neither presents nor drains data. Caught
directly by the `queues` harness (`has_data` collapsing to one queue).

## Section 14: datapath harness "≥2 queues" assertion failed

**Symptom.** (Earlier, `datapath` harness.) A check expecting frames to land in ≥2
distinct queues failed  -  everything clustered into one queue.

**Cause.** The classifier's *reset* PCP→TC→queue map clusters PCP 0–3 into the same
class, so distinct PCPs did not fan out to distinct queues.

**Fix.** Program an **identity** classifier config in the harness so PCP `p` → prio
`p` → TC `p` → queue `p` (`cls_prio_regen=0x00FAC688`, `cls_pcp_tc_map=0x00FAC688`,
`cls_tc_queue_map=0x000000E4`), then assert `tdest == pcp`. This is also why the
`milan_dp` harness programs the identity map over the CSR before the TX test.

## Section 15: `--full` fails 100 MHz timing in the CBS credit-shaper

**Symptom.** The first `--full` Artix-7 bitstream (100 MHz `sys`) synthesised and
routed but missed timing badly  -  `WNS = -19.25 ns`, `TNS = -78626 ns` on the
`main_clkout0` (sys) group. Every worst path was in the 802.1Qav credit-based shaper:
`…/gen_cbs[N].u_cbs/send_delta…`, `send_slope_per_byte`, `credit…`. Lowering `sys` was
not an option  -  DDR3 needs `sys4x ≈ 400 MHz`, i.e. `sys = 100 MHz`.

**Cause.** `credit_based_shaper.sv` computed the Q16 per-byte slope with a wide
**constant-divide** (`(send_slope << 16) / port_rate`) and then multiplied it by
`bytes_sent` **in the same clock period**  -  `report_timing` showed a single 21 ns cone
of **36 logic levels / 22 CARRY4** from `is_1g` (`mac_ctrl_reg[4]`) to the `send_delta`
DSP. The divide is the killer, but the slope terms are **quasi-static** (they change
only when `tc cbs` reprograms idleSlope or the link rate flips  -  held for millions of
cycles), so the divide never needs a single-cycle result.

**Fix (two parts).**
1. **Pipeline + multicycle the divide.** Register the divide outputs
   (`idle_slope_per_cycle_r` / `send_slope_per_byte_r`, stage-0 `slope_pipe`) so the
   multiply no longer shares the period, and declare `config → slope_r` a **multicycle
   path** in the SoC XDC (`milan_soc.py add_milan_datapath`, `set_multicycle_path 4
   -setup / 3 -hold`). Two gotchas: (a) synthesis **absorbs** the slope register into
   the credit/`send_delta` DSP unless it is marked `(* dont_touch = "true" *)`  -  without
   it the multicycle target cell does not exist (`[Vivado 12-180] No cells matched`);
   (b) synthesis pulls the CBS slope cone toward the `csr` module (where its config
   sources live), so the constraint must match by **leaf** register name
   (`*send_slope_per_byte_r_reg*`), not a `*u_cbs*` hierarchy path. The Verilator CBS
   ref model mirrors the one extra stage in both `FixedPointRef` and `IdealRef`, so the
   `cbs` harness stays **bit-exact** (87233 checks, 0 mismatches). This alone took the
   CBS off the critical path: `WNS -19.25 → -2.18 ns`.
2. **`sys = 80 MHz` for the residual.** With the CBS fixed, the worst path becomes the
   dense **`milan_csr` read-data mux** (`rx_filter/mac_cam` + DMA base regs → the
   `r_data` register, ~15 levels), marginally failing 100 MHz (`WNS ≈ -1.06 ns` even
   with aggressive `--timing-opt` directives). Running `sys` at **80 MHz** closes it
   with margin while keeping DDR3 valid: `sys4x = 320 MHz` is still above the DDR3 DLL
   lock floor (~303 MHz). 80 MHz is a valid Linux-capable bring-up clock, but the clean
   fix is Section 16 (run the datapath in its own clock). `--timing-opt` (aggressive
   place/route/phys-opt directives) is the no-RTL lever for the last ns of setup slack.

**Superseded (2026-07-11, AREA-70 campaign).** Fix part 1 is history: the divide
cones are GONE, not multicycle-hidden. The slope terms are now produced by a
**sequential slope engine** in `credit_based_shaper.sv` (`slope_engine`): one
31-bit serial restoring divider per queue on a fixed 100-cycle cadence, results
committed atomically into `idle_slope_per_cycle_r`/`send_slope_per_byte_r`.
Steady-state values are bit-identical to the old `/` operator; a config write
takes effect at most 200 cycles later (2 us at 100 MHz, irrelevant vs `tc cbs`
reprogramming rates). This deleted ~9.3K LUTs of combinational divide cones
(~2.3K per queue, measured: the per-queue OOC synth went 1265+leaked to 362
LUTs) and with them BOTH gotchas: the `dont_touch` attributes and the
`set_multicycle_path` XDC in `milan_soc.py` are removed  -  there is no wide
config->slope cone left to constrain. The Verilator `cbs` harness now mirrors
the engine cadence state-for-state (`SlopeEngineRef` in `cbs_ref_model.h`) and
compares the slope registers every cycle including warm-up and reconfiguration
(87233 checks, 0 mismatches). Do not change the engine timing without updating
that model. Background: the cross-boundary attribution trap this exposed (the
cones showed up as `milan_csr` LUTs in hierarchical utilization because the
`cbs_idle` source registers live there) is written up in SESSION_HANDOFF.md;
OOC-synth a module standalone before believing its hierarchical LUT count.

## Section 16: clean 100 MHz  -  run the dense datapath in its own clock domain

**Symptom.** Even after the CBS fix (Section 15), the full DDR3 SoC would not close a
clean **100 MHz** `sys`: the worst path kept landing in the dense TSN datapath
(`rx_filter/mac_cam` TCAM readback, CSR read mux), `WNS ≈ -1 to -2 ns`.

**Cause.** `report_timing` showed the offenders were **routing-dominated** (~72% route,
high-fanout nets from a BRAM in `rx_filter`), not logic depth  -  a *congestion* problem
in a datapath that is simply too dense to route at 100 MHz on this Artix-7 (-2). A
`milan_csr` read-mux pipeline made it **worse** (added 256 registers of congestion,
`WNS -1.06 → -1.92`)  -  the wrong lever, reverted.

**Fix.** The datapath does not need 100 MHz  -  it only has to service 1 GbE (a 64-bit
datapath at 50 MHz is 3.2 Gb/s). And `milan_datapath` was built with a **separate
`axis_clk`/`gtx_clk`** for exactly this. So run the whole datapath in its own slower
clock domain and cross the CPU boundary with a FIFO:
- `milan_soc.py --milan-clk-freq 50e6` adds `cd_milan` (50 MHz) in `_CRG`, drives the
  datapath's `i_axis_clk`/`i_gtx_clk` from it (`add_milan_datapath(..., milan_cd)`), and
  crosses the CPU's AXI-Lite CSR bus with **`axi.AXILiteClockDomainCrossing`** (async
  FIFOs per channel) + a **`MultiReg`** for the level IRQ into the sys EventManager.
- `sys` (100 MHz) now carries only CPU + DDR3 + bus + the CSR async-FIFO  -  the dense
  logic is off its budget. Result: **"All user specified timing constraints are met"** at
  100 MHz; on the AX7101, NaxRiscv @100 MHz + **DDR3-800** (up from 640 @80 MHz), memtest
  OK, `MILN` reads correctly across the CDC (`evidence/hw_ddr3_800_cdc_100mhz.log`).
- `milan_cd="sys"` (the default) keeps the single-clock direct wiring for the sim. The
  DMA/MAC AXIS boundary needs its own stream CDC before `--milan-clk-freq` combines with
  `--with-dma/--with-mac` (guarded with `NotImplementedError`).

**DDR3 ceiling.** DDR3 rate = `8×sys`, and the CPU shares `sys`; the **NaxRiscv** core
capped `sys` at **~102 MHz** (register-file path), so DDR3-800 was the max with a shared
clock  -  the MT41J256M16 part is rated 1600, i.e. the CPU was the limit, not the DRAM.
(**Update, current VexiiRiscv core:** the ~102 MHz cap was NaxRiscv-specific  -  a VexiiRiscv
build closed and ran **112.5 MHz / DDR3-900** on silicon, memtest OK. It was nonetheless
reverted to 100 MHz / DDR3-800 because the higher clock *worsened* memory latency and the
UDP-flood pps ceiling  -  see `LATENCY_INVESTIGATION.md` §8.) The S7PLL also
rejects intermediate frequencies (115 MHz → `No PLL config found`, since `sys4x=4·sys`
plus the 50/200 MHz clocks force no valid VCO between 100 and 125). Faster DDR3
(DDR3-1000 @ a 125 MHz `dram` domain) would need the controller+PHY decoupled onto their
own clock with a memory-bus FIFO (LiteDRAM `crossbar.get_port(clock_domain=…)`), a
bigger change for a mostly-latency gain  -  not pursued (3.2 GB/s already exceeds a 100 MHz
core's bandwidth demand).

## Section 17: on-hardware NIC bring-up  -  DMA works, but no packet on the wire (it's GMII, not RGMII)

**Symptom.** With the live rig (ProfiTap ProfiShark 1G+ taps between the FPGA eth ports and
Intel i210 traffic generators), the copper link comes up at **1000/Full**, and the FPGA's
whole internal path is verified on silicon (DDR3 → DMA → AXIS-CDC → datapath, `done=1`).
But **no frame crosses the wire either direction**: the i210 receives nothing from an FPGA
DMA-TX, and an FPGA RX-DMA captures nothing from i210 broadcasts.

**Diagnosis (the useful part).** The LiteEth MAC exposes RX error counters (`milan_mac` @
`0xf0003800`: `rx_datapath_preamble_errors` @ `0xf0003808`, `rx_datapath_crc_errors` @
`0xf000380c`). Blasting a known count of frames from the i210 and reading these gives a
precise signal (the milan RMON at `0x90000200` is useless here  -  `MilanMAC` ties
`i_mac_events=0`). The result: a **20000-frame blast → `preamble_errors` +20000, `crc` +0,
0 captured**. *Exactly one preamble error per frame* ⇒ every frame reaches the MAC (RX_DV
sampled fine) but the **data is structurally corrupted**  -  not a timing margin (that would
give a *fraction* of errors), and not the datapath (frames never get past the preamble).

**False trails (all the wrong interface).** Assuming RGMII, we chased: the s7rgmii IDELAY
value (0 vs 2 ns), inverting the RX clock (the Alinx `util_gmii_to_rgmii` does
`BUFG(~rgmii_rxc)`), removing the IDELAY entirely, swapping the IDDR nibbles. Each was a
~25-min rebuild; none moved the 100% error rate. Lesson: a **100%-deterministic** data
error is structural  -  stop tuning timing and question the interface/pinout.

**Root cause.** The AX7101's RTL8211E is strapped for **GMII (8-bit SDR)**, *not* RGMII
(4-bit DDR). The Alinx vendor top (`SRC/15_ethernet_test/.../ethernet_test.v`) makes it
explicit: `input [7:0] e_rxd`, **separate** `e_rxdv`/`e_rxer`, and `assign e_gtxc=e_rxc`.
A 4-bit-DDR RGMII read of an 8-bit-SDR bus corrupts every byte (and RX_DV, a level, still
reads fine → the tell-tale one-preamble-error-per-frame).

**Fix.** Platform `eth0` → 8-bit GMII pinout (`rx_data[0:7]`, separate `rx_dv`/`rx_er`,
`gtx`/`rx`/`tx` clocks  -  all from the Alinx `top.xdc`), and `MilanMAC` → **`LiteEthPHYGMII`**
(the RGMII `milan_rgmii.py` path is retired for this board). See
`evidence/hw_ma3_dma_datapath_100mhz.md` for the full sequence and the exact `mem_write`/
`mem_read` console recipe used to drive DMA-TX/RX and read the MAC counters over the BIOS
console (no toolchain needed).

**Meta-lesson.** Confirm the PHY interface (GMII vs RGMII) from the board vendor's *working*
example before writing the PHY  -  the LiteEth default for a "1G Artix + RTL8211" is RGMII,
which was simply wrong for this board.

## Section 18: TX frames egress truncated / not at all  -  AXIS `tkeep` vs LiteEth `last_be`

**Symptom.** With the GMII bitstream, GMII RX proven, and the TX-DMA reading memory
correctly (`milan_dma_tx_done=1`, `_offset`=word-count for both ROM and DRAM), driving
DMA-TX still put **no correct frame on the wire**: a single-word (8-byte) transfer egressed
as `ff:00:00:00:00:00` (only byte 0 survived, rest zero), and a full 64-byte frame
**never egressed at all** (i210 `rx_packets` delta = 0 over 300 frames).

**Not the cause (each eliminated).** DMA read (proven via `done`/`offset` on ROM+DRAM and an
isolated Migen sim of the 64→32 converter); the datapath TX (byte-exact in
`tb/verilator/datapath`, tkeep-preserving `traffic_queues.sv`); CBS (`CBS_CTRL[0]=0` is
*unshaped*, not starved); DMA `length` units (a separate bug  -  it's **bytes**, see
`REGISTER_MAP.md`, so `length=8` sent one word).

**Root cause.** `MilanMAC` mapped AXIS `tkeep` straight onto LiteEth `core.sink.last_be`.
LiteEth's `last_be` is a **one-hot pointer to the last valid byte** (`liteeth/mac/padding.py`
Case: `0x01`→1 B, `0x02`→2 … `0x80`→8 B), *not* a keep mask. The 64→8 TX `StrideConverter`
reads `0xFF`'s **lowest** set bit → 1 valid byte, truncating a full word to one byte and
breaking multi-beat frame termination. RX had the mirror defect (one-hot fed where the
datapath expects a mask).

**Fix.** Convert in both directions in `MilanMAC` (`milan_soc.py`):
`last_be = keep & ~(keep>>1)` (mask→one-hot of the highest byte), and
`keep = last ? (last_be<<1)-1 : 0xFF` (one-hot→mask). `keep=0xFF ↔ last_be=0x80`.

**Meta-lesson.** AXIS `tkeep` (contiguous mask) and LiteEth `last_be` (one-hot last-byte
pointer) are different encodings  -  never wire one onto the other. And the Verilator datapath
harness checks egress `m_tdata` but **not `m_tkeep`**; a keep/last_be bug in the LiteX glue
(`milan_soc.py`) is covered by no RTL harness. See `evidence/hw_ma3_dma_datapath_100mhz.md`.

## Section 19: kernel hangs after OpenSBI (no `Linux version`)  -  a STALE `litex_term` served the wrong boot manifest

**Symptom (2026-07-05, FPU bring-up).** After loading a bitstream, the console showed the
LiteX BIOS, then OpenSBI's full banner ending at `Boot HART MEDELEG …`, and then **nothing**  - 
no `Linux version`, no panic, a silent hang at the OpenSBI→kernel handoff. It reproduced
across *every* combination tried: FPU kernel and no-FPU kernel, FPU gateware and the known-good
`ring10` gateware, corrected `riscv,isa` strings, both `--with-fpu` netlists. Hours were spent
suspecting the FPU (timing at +0.004 ns), then the kernel `CONFIG_FPU`, then a rebuild config
regression  -  **all red herrings.**

**Root cause  -  the kernel was never loaded to `0x40000000`.** The boot console showed
serialboot uploading only `milan.dtb`, `rootfs.cpio.gz`, `opensbi.bin`  -  **the `Image` was
never uploaded.** That file set is exactly `boot_flashkernel.json` (kernel-from-QSPI), *not*
`boot.json` (kernel-over-serial). A **stale `litex_term` process from earlier QSPI-boot work
was still holding the serial port and serving `boot_flashkernel.json`**; `tmux send-keys C-c`
plus a fresh `litex_term …–images boot.json` command did **not** replace it (the C-c reached
the tmux pane but the old process kept the port, and the new command couldn't open the busy
device). Every board reset  -  triggered by each `openFPGALoader` reload  -  was answered by the
old process. And because the QSPI had been `--bulk-erase`d for the FPU work, linux_flashboot
printed `Error: invalid image length 0xffffffff` and fell through, so **no kernel came from
QSPI either.** OpenSBI dutifully jumped to `0x40000000`, which held only memtest patterns →
silent hang.

**Diagnosis method that finally worked.** Read the *upload lines* in the boot log, not just
the hang point: `Uploading …/milan.dtb`, `…/rootfs.cpio.gz`, `…/opensbi.bin`  -  and the
conspicuous **absence of `Uploading …/Image to 0x40000000`**. Then `pgrep -af litex_term`
revealed the live process still pointed at `boot_flashkernel.json`.

**Fix.** Kill the stale term by its exact PID (`pgrep -af litex_term` → `kill <pid>`; confirm
`sudo fuser <by-id-dev>` shows the port free), start a fresh `litex_term … --images boot.json`,
then reload the bitstream. The log now shows `Uploading …/Image to 0x40000000 (11900984
bytes)…` and the kernel boots.

**Lessons.**
- When a Linux boot hangs right after OpenSBI, **first confirm the kernel was actually loaded**
  (look for the `Image` upload line, or `Copying …to 0x40000000` for the QSPI path) *before*
  suspecting the CPU/kernel. OpenSBI running proves the CPU executes; a jump into an unloaded
  address hangs identically to a broken CPU.
- `tmux send-keys C-c` is **not** a reliable way to replace a serial-holding process  -  verify
  with `pgrep -af litex_term` that the *intended* manifest is being served. Prefer killing the
  old PID and starting fresh.
- Don't `--bulk-erase` the QSPI and then boot expecting the resident kernel  -  pair an erase with
  either a re-flash *or* a full-serial `boot.json` (kernel included), and make sure the term
  actually serves that manifest. (See also the QSPI pre-erase rule in the milan-fpga-nic skill.)
- This masqueraded perfectly as an FPU/timing bug. The FPU hardware was fine the whole time
  (misa `rv64imafd`, fits at 58 % BRAM / 77 % LUT, timing met)  -  see the FPU notes in
  `board-session-state`.
