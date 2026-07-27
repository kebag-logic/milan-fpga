# Troubleshooting  -  every problem hit bringing up the full-FPGA solution, and its fix

This is the field log of every real problem encountered building and simulating the
fully-FPGA Milan softcore solution, with the **symptom**, the **cause**, and the
**fix**. It is meant to save the next developer the debugging time.

Grouped as:

- toolchain/environment ([Sections 1–2](#section-1-import-litex-resolves-to-a-namespace-package)),
- LiteX/SoC build ([Sections 3–6](#section-3-identifier-string-must-not-contain-commas)),
- Verilator simulation ([Sections 7–8](#section-7-verilator-cannot-find-include-file)),
- shell/process ([Section 9](#section-9-pkill--f-self-matches-the-running-shell)),
- synthesis ([Section 10](#section-10-yosys--sv2v-cannot-find-axis_mux_rr_2in_1out)),
- RTL/testbench ([Sections 11–14](#section-11-milan_dp-axi-write-bfm-did-not-commit-writes)),
- P&R timing closure ([Sections 15–16](#section-15---full-fails-100-mhz-timing-in-the-cbs-credit-shaper):
  CBS pipelining + running the dense datapath in its own CDC clock domain for a clean 100 MHz),
- and on-hardware NIC bring-up ([Section 17](#section-17-on-hardware-nic-bring-up--dma-works-but-no-packet-on-the-wire-its-gmii-not-rgmii):
  the AX7101 PHY is GMII, not RGMII).

Companion: [`SIMULATION.md`](../testing/SIMULATION.md) (how the sim works) and
[`FULL_FPGA_SOLUTION.md`](../overview/FULL_FPGA_SOLUTION.md) (the architecture).

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
[`REGISTER_MAP.md`](../reference/REGISTER_MAP.md)). The device-tree `reg` base must match the host.

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
for inc in ("hdl/common", "hdl/ieee8021q/ts", "hdl/ieee8021as/ptp_timestamp",
            "hdl/ieee17221/adp", "hdl/common/csr", "hdl/common/eth_event_counter"):
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
[Section 3.3](../testing/SIMULATION.md#section-33-the-scripted-path-used-to-capture-the-evidence)
of [`SIMULATION.md`](../testing/SIMULATION.md).

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

**Symptom.** The Yosys device-portability check passes the other tops then fails
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

**Cause.** The classifier's *reset* PCP→TC→queue map did not fan distinct PCPs out to
distinct queues. (With the four-queue map of the day it clustered PCP 0–3 into one class;
the five-queue reset map `0x004898C0` spreads PCP 0…7 over q0/q0/q3/q4/q1/q1/q2/q2, so it
still is not an identity — the harness fix below is unchanged in kind.)

**Fix.** Program an **identity** classifier config in the harness so PCP `p` → prio
`p` → TC `p` → queue `p` (`cls_prio_regen=0x00FAC688`, `cls_pcp_tc_map=0x00FAC688`,
`cls_tc_queue_map=0x00004688` — 3 bits per entry at `NUMBER_OF_QUEUES = 5`, which is
what `tb/verilator/datapath/sim_main.cpp` computes), then assert `tdest == pcp`. The
identity only holds for `p < 5`: TC5…TC7 name queues ≥ N and `traffic_class_map` clamps
them to q0. This is also why the `milan_dp` harness programs the identity map over the
CSR before the TX test.

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
config->slope cone left to constrain.

The Verilator `cbs` harness now mirrors the engine cadence state-for-state
(`SlopeEngineRef` in `cbs_ref_model.h`) and compares the slope registers every
cycle including warm-up and reconfiguration (87233 checks, 0 mismatches). Do
not change the engine timing without updating that model.

Background: the cross-boundary attribution trap this exposed (the cones showed
up as `milan_csr` LUTs in hierarchical utilization because the `cbs_idle`
source registers live there) is a standing area-report trap — OOC-synth a
module standalone before believing its hierarchical LUT count (the same rule
carried as build gate 2 in [`../integration/BUILDING.md`](../integration/BUILDING.md) §5).

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
UDP-flood pps ceiling  -  see [`LATENCY_INVESTIGATION.md`](../findings/LATENCY_INVESTIGATION.md) §8.)

The S7PLL also rejects intermediate frequencies (115 MHz → `No PLL config found`,
since `sys4x=4·sys` plus the 50/200 MHz clocks force no valid VCO between 100 and 125).
Faster DDR3 (DDR3-1000 @ a 125 MHz `dram` domain) would need the controller+PHY
decoupled onto their own clock with a memory-bus FIFO
(LiteDRAM `crossbar.get_port(clock_domain=…)`), a bigger change for a mostly-latency
gain  -  not pursued (3.2 GB/s already exceeds a 100 MHz core's bandwidth demand).

## Section 17: on-hardware NIC bring-up  -  DMA works, but no packet on the wire (it's GMII, not RGMII)

**Symptom.** With the live rig (ProfiTap ProfiShark 1G+ taps between the FPGA eth ports and
Intel i210 traffic generators), the copper link comes up at **1000/Full**, and the FPGA's
whole internal path is verified on silicon (DDR3 → DMA → AXIS-CDC → datapath, `done=1`).
But **no frame crosses the wire either direction**: the i210 receives nothing from an FPGA
DMA-TX, and an FPGA RX-DMA captures nothing from i210 broadcasts.

**Diagnosis (the useful part).** The LiteEth MAC exposes RX error counters (`milan_mac` @
`0xf0003800`: `rx_datapath_preamble_errors` @ `0xf0003808`, `rx_datapath_crc_errors` @
`0xf000380c`). Blasting a known count of frames from the i210 and reading these gives a
precise signal. (At the time the milan RMON at `0x90000200` was useless here — `MilanMAC`
tied `i_mac_events=0`. Since VERSION `0x0013` those very counters feed it: `preamble_errors`
drives `STAT_RX_ERROR_BAD_FRAME` `0x220` and `crc_errors` drives `STAT_RX_ERROR_BAD_FCS`
`0x224`, so this diagnosis is now available from the datapath CSR window too — check
`STATS_CAP` `0x204` first to confirm the build has them.)

The result: a **20000-frame blast → `preamble_errors` +20000, `crc` +0,
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
[`REGISTER_MAP.md`](../reference/REGISTER_MAP.md), so `length=8` sent one word).

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
`boot.json` (kernel-over-serial).

A **stale `litex_term` process from earlier QSPI-boot work
was still holding the serial port and serving `boot_flashkernel.json`**; `tmux send-keys C-c`
plus a fresh `litex_term …–images boot.json` command did **not** replace it (the C-c reached
the tmux pane but the old process kept the port, and the new command couldn't open the busy
device). Every board reset  -  triggered by each `openFPGALoader` reload  -  was answered by the
old process.

And because the QSPI had been `--bulk-erase`d for the FPU work, linux_flashboot
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

## Section 20: host plane dead, CSR readbacks perfect  -  a stale device tree maps every DMA window onto the wrong registers

**Symptom (2026-07-25, chmap bring-up).** After a boot-image reflash, the kernel counts
`rx_packets=0` absolute, yet the driver's `bd probe` line shows the RX ring base written *and
read back correctly*. `ptp4l` times out polling for TX timestamps. The driver counts outgoing
ARP requests as sent, but **zero of them appear at the inline capture tap** - while the fabric
plane (AAF talker, CRF, MSRP) streams flawlessly out of the same connector.

It reproduced identically across three bitstreams (two fresh seeds *and* the previous
known-good build) and survived a full board power-cycle.

**Root cause.** The flashed `.dtb` was a three-week-old prebuilt artifact with an obsolete
5-window `reg` list (no ts window, no pcm node). The `kl-eth` driver maps its `kl,dma-ether`
`reg` windows **by index**, so every host-DMA register access landed on a
*wrong-but-writable* CSR. A `CSRStorage` stores whatever it is given, so every readback
matched perfectly - while the real ring engine sat unprogrammed and the host lane stayed dead
in both directions at the wire.

**False leads burned** (hours each):

- *Placement lottery* - a second seed was identically dead: the fault was deterministic.
- *PHY RX wedge* - a power-cycle changed nothing, and the PHY honestly reported
  1000 Mb/s full-duplex over MDIO the whole time.
- *Inline-tap egress wedge* - a USB bus reset never touches the tap's line side (the board
  logged no link bounce), so that test was void, not negative.
- *"Fabric RX is dead too"* - the STREAM_INPUT counters only count a **bound** stream's
  frames; reading 0 while unbound means nothing.

**Diagnosis that cracked it.**

1. **Ping out from the board while capturing at the tap.** The driver counted 54 TX frames;
   zero reached the wire. One experiment, and the "TX works" claim collapsed - every earlier
   TX proof had been *fabric* TX, which shares nothing with the host lane above the MAC mux.
2. **`devmem` the real ring-base CSR** (address from the build's `csr.csv`) - it read 0 while
   the driver believed the ring was armed. The writes were landing somewhere else.
3. **Diff the dtb `reg` windows against `csr.csv`** - mis-split from window 1 onward, ts
   window absent. Case closed.

**Fix - and the twist that made round one of the fix a no-op.** Compiling the device tree
fresh from the committed dts source and flashing it is **not enough**: on this boot path the
LiteX BIOS jumps to OpenSBI with `a1 = 0`, so the kernel only ever sees the fdt **embedded in
the opensbi image** (`FW_FDT_PATH`). Flashing a corrected `.dtb` into its slot changed nothing;
the fix is to **rebuild opensbi around the corrected tree** (`build_opensbi.sh` in the private
test repo) and flash *that*.

[`deploy.sh`](../../sw/litex/deploy.sh) `flash-images` now refuses the mismatch outright:
[`check_dtb_csr.py`](../../sw/litex/check_dtb_csr.py) validates the `kl,dma-ether` windows
against the build's `csr.csv` for **both** `$DTB` and `$OPENSBI` - it carves the embedded FDT
out of any binary, so the image that actually boots is the image that gets checked.

**Lessons.**

- A matching readback proves only that *something* stored the write. Verify the **engine**
  (live counters ticking, pointers advancing), never the register echo - the same class as
  the CSR-shadow-lies trap in [KNOWN_ISSUES_AND_LIMITATIONS](KNOWN_ISSUES_AND_LIMITATIONS.md).
- "TX works" must name the lane. Fabric TX flowing proves nothing about host TX.
- A capture tap proves frames reached the *tap*; it never proves they exited toward the DUT.
- Boot artifacts are part of the ABI. dtb ↔ `csr.csv` drift is the same failure class as
  driver ↔ gateware pairing - gate it mechanically, don't trust discipline.

## Section 21: ACMP says SUCCESS, the listener declares itself bound - and not one frame is accepted (ROOT-CAUSED and FIXED, `VERSION 0x000F`; mechanism confirmed on silicon 2026-07-26)

> **ROOT CAUSE FOUND 2026-07-26 — reproduced in simulation, fixed in RTL, and
> the mechanism then confirmed on silicon by causation** (see the confirmation
> block below and [`../findings/STRESS_0726.md`](../findings/STRESS_0726.md) §D).
> The verdict does not die in the *parse*; it dies in the
> stream **table** that tells the parser what to match. Two RTL layers combined:
>
> 1. `hdl/milan/milan_datapath.sv` `win_commit_glue` staged the window's
>    `SID_LO`/`SID_HI` in **one global register pair shared by every index**. Its
>    commit guard asked *"is some sid staged?"*, never *"was a sid staged for THIS
>    index?"* — so a route-flags-only `CTRL` write at idx 0 armed entry 0 with
>    **whatever other listener staged a sid earlier**. A second term
>    (`| ~csr_lctx_wr_data_w[0]`) let an `en=0` write through unconditionally.
> 2. `hdl/ieee1722/avtp/KL_stream_table.sv` set `ovr_armed_r[idx]` on **any** write
>    and cleared it **only on reset**. Once idx 0 was armed, entry 0 permanently
>    stopped aliasing the ACMP bound record — **there was no runtime path back**.
>
> Net effect: one stray window `CTRL` write at index 0 detaches the ACMP alias for
> good, so every later `CONNECT_RX` binds cleanly and changes nothing — exactly the
> **PARSED climbs / MATCHED static / listener reports bound** signature below. It
> also explains why reaching `RSV_OK` changed nothing, and it supplies the missing
> *reason* behind the 2026-07-23 operational rule "stage SID before CTRL".
>
> **Fix (`VERSION 0x0001_000F`):** staging is tagged with the index it was staged
> for, and `{en=0, sid=0}` became **RELEASE-TO-ALIAS**, disarming the override so
> entry 0 returns to the ACMP record at runtime. Regression guards:
> `tb/verilator/milan_dp/sim_nxn.cpp` TRAP-1 (N=4 and N=8, through the real CSR
> window) and `tb/verilator/avtp_parser/sim_tbl.cpp` T6 (table level, from reset),
> both including negative legs.
>
> **CONFIRMED ON SILICON 2026-07-26**, on the AX 8x8 board still running the
> pre-fix `VERSION 0x0001_000B`, with the peer talker live
> (`AAF_STAT 0x694 = 0x37E`, `AAF_FRAMES` advancing ~12.9 k/s).
>
> *The defect, read off the board.* A SNAP'd read of the window at idx 0 showed
> the **correct** stream_id staged — `SID_LO 0x00020000` / `SID_HI 0x02000000` =
> `0x0200000000020000`, the sid both ends agree on — but `A_STRMW_CTRL 0x810`
> read **`0x00000000`**, i.e. `en = 0`. Since
> `tbl_en_o[0] = ovr_armed_r[0] ? ovr_en_r[0] : bound0_i`, an earlier `en=0` CTRL
> write had armed the entry-0 override with en=0 and pinned entry 0 **disabled**,
> regardless of what ACMP reported. `ACMPL_STATE 0x6A4 = 0x0002E07F` (bound,
> stream active, Listener declared, TalkerAdvertise registered) with
> `AVTPRX_FRX = 0`. That is the mechanism, observed directly rather than inferred.
>
> *The workaround, and the proof.* Re-staging the sid at idx 0 and committing
> `CTRL = 0x3` (en + DMA route):
>
> ```sh
> devmem 0x90000800 32 0x000        # SEL: dir=0 idx=0
> devmem 0x90000814 32 0x00020000   # SID_LO
> devmem 0x90000818 32 0x02000000   # SID_HI
> devmem 0x90000810 32 0x3          # CTRL: en + DMA
> ```
>
> | | before | +2 s | +4 s | sustained 5 s |
> |---|---|---|---|---|
> | `AVTPRX_FRX 0x6BC` | **0** | 24 971 | 58 222 | 223 673 → 271 646 |
> | `AVTPRX_STAT 0x6B8` | 0 | 0x101 | 0x101 | 0x101 |
> | `AVTPRX_ERR 0x6C0` | — | — | — | **0** |
>
> ~9.6 k frames/s sustained, zero format rejects. **The listener accepts.**
>
> *RX latency chain, finally readable* (AX datapath = 100 MHz, 1 cyc = 10 ns):
> `MAC_RX→ACCEPT` min 49 cyc / last 50 = **~0.49 µs**; `ACCEPT→DEPKT` min 29 /
> last 30 = **~0.30 µs**; `DEPKT→PCM_RING` min 10 378 / last 12 541 =
> **~104-125 µs**. Total ≈ **105-126 µs**, dominated by the ring-fill stage
> sitting at the 125 µs class-A interval — the expected shape.
> **Caveat:** the `max` fields and `LTAP_RX_INFO 0x898` are saturated
> (`0xFFFF`), polluted by the long blocked period when every frame timed out at
> the tap. Only `min`/`last` are trustworthy above; a clean set needs a counter
> reset, and the `0x000F` flash for the fixed provisioning path.
>
> On any board still carrying pre-`0x000F` gateware, the four `devmem` writes
> above are the standing workaround.

**Symptom (2026-07-26, 8x8 AX gateware `VERSION 0x0001_000B`).** A controller binds the
board's listener 0 to the peer board's talker 0. Every control-plane indication is healthy:

```
ACMP CONNECT_RX_RESPONSE   status = SUCCESS
ACMPL_STATE  0x6A4 = 0x0002E07E
             -> [2:0]=6 SETTLED_NO_RSV | [3] bound | [4] stream active
                [5] Listener declared | [6] TalkerAdvertise registered
                [14:13]=3 probing completed | [12:8]=0 status SUCCESS | VLAN 2
talker board: AAF_STAT 0x694 = 0x37E   (reservation ACTIVE, paced, frames leaving)
```

And the media plane is dead: `AVTPRX_STAT` / `AVTPRX_FRX` / `AVTPRX_ERR` all **0**, the PCM ring
never advances, and the RX latency-tap chain reports `samples = 0` with `timeouts` saturated
(`LTAP_RX_INFO 0x898`).

**What that combination already proves.** The `MAC_RX` tap sits on the datapath's RX input
port (`s_axis_mac_rx_*`), *upstream* of the PTP stamper and the parser tap - so the chain
arming on every frame is hard evidence that **AVTP frames do enter the datapath**. The chain
then aborts at its first hop, which means `avtprx_accept_p` never fires. The failure is
inside the window **parser match → monitor accept**, not on the wire, not in the bridge, and
not in ACMP.

**Narrowed further, from two facts that cost nothing to check.**

- *The monitor is innocent.* `KL_avtp_rx_monitor` acts only under
  `match_valid_i && bound_i`, and a matched PDU with a wrong format increments
  UNSUPPORTED_FORMAT instead of accepting. `AVTPRX_ERR` reads **0**, so no PDU ever
  arrived at the monitor with a match - the verdict is being made (or not made) in the
  **parser**.
- *The parser's input bus is alive.* The parser tap (`rx_axis_ptp_to_filt`) is a passive
  fan-out of the same stream that feeds the host RX filter, and the board's own host network
  lane is working normally over that path. Frames reach the parser; the parser does not
  match them.

**What is ruled out.**

- *The RTL accept path.* `tb/verilator/milan_dp` builds the N=8 shape and proves streams 3..7
  provisioned simultaneously, each landing on the PCM ring with byte-exact payload and
  isolated counters. Sim accepts; silicon does not.
- *A source regression.* No RX-path source change separates the built commit from the current
  trunk.
- *The missing reservation.* `SETTLED_NO_RSV` is suspicious but it is **not** the gate: the
  stream table is written from the ACMP listener context (`bound0_i`/`sid0_i` on
  `KL_stream_table`), and the parser's match is gated by that table alone - no lwSRP
  reservation term stands between a matched frame and the monitor. Confirmed on the bench
  the same day: the SM later reached **`SETTLED_RSV_OK`** (`ACMPL_STATE = 0x0002E07F`) on
  its own and **nothing changed** - `AVTPRX_FRX` still 0. Reservation state is not the cause.
- *The bind record itself, checked against the talker.* Read through the `0x800` window at
  listener index 0, the context holds `SID = 0x0200_0000_0002_0000` with `DMAC` = the peer
  talker's MAAP-claimed group address. Read on the **peer board's own talker window**
  (6 consecutive SEL-bracketed samples, all identical) its stream_id is
  `0x0200_0000_0002_0000` — **the same 64-bit value**. Listener and talker agree on what
  the stream is called; the compare still fails.

> **SUPERSEDED — all three suspects below were REFUTED.** They are kept as the
> record of how the fault was worked, not as live guidance. The fault was not in
> the parser and not in the placement: it was **entry-0 provisioning**, two
> layers up, in `win_commit_glue` + `KL_stream_table.ovr_armed_r` — see the
> root-cause block at the top of this section. Do **not** spend a build cycle on
> suspect 1's "re-test on a fresh netlist"; the mechanism is reproduced in
> simulation and was then triggered deliberately on silicon.

**Suspect list (refuted), in the order it was tested.** All three lived in the parser or in
what the parser is told to compare against:

1. ~~**Stream-ID compare in this placement.**~~ **REFUTED.** The parser compares each
   frame's 64-bit stream_id against `strtbl_sid_w` at width N=8. This bitstream placed at
   **99.93 % slice occupancy**, the same build generation whose placer overflowed on
   `crf_rx` - "correct in sim, wrong in this placement" was the live hypothesis at the time.
   The defect reproduces in simulation, so placement was never the cause.
2. **The path from the bind record to the compare.** The record is right (above), so what
   is left on this axis is the wiring between them: the flat `acmpl_sid`/`acmpl_bound` pair
   that `KL_stream_table` entry 0 is built from, versus the per-context RAM the window
   reads. At N=8 those are two different readers of the same bind - a divergence there
   would present exactly as "record correct, nothing matches".
3. **What the parser extracts from a tagged frame.** Both endpoints agree on the stream_id
   *as a register value*; the compare happens against the value the parser lifts **off the
   wire**. A C-TAG offset - or a byte order - handled differently than in the harness
   stimulus lands a different 64 bits in the comparator and produces exactly this
   signature. The harness generates its own stimulus with the same convention it checks,
   so it cannot catch this class; only a parser-level counter or a wire capture can.

**The instrument this needs — now built (`VERSION 0x0001_000D`).** Every counter that
existed when this was written is *downstream* of the match (`AVTPRX_*` only counts accepted
frames), which is exactly why the fault was invisible from software. The parser's own
frame/match counters turned out to exist in RTL and be left **unconnected** in
`milan_datapath`; they are now wired out, with the wire-side stream_id beside them, as the
**`0x8B4` parser-probe group** ([register map](../reference/REGISTER_MAP.md) §0x8B4):

```sh
# on the board, after binding the listener
for a in 8B4 8B8 8BC 8C0 8C4; do
  printf '0x%s = %s\n' $a "$(devmem 0x90000$a 32)"; done
#   0x8B4 PARSED   0x8B8 MATCHED   0x8BC/0x8C0 last wire stream_id   0x8C4 INFO
```

- `PARSED` static → frames never reach the parser (look upstream: MAC, filter, classify).
- `PARSED` climbing, `MATCHED` static → **the compare is the fault**; diff `0x8BC`/`0x8C0`
  (the stream_id lifted off the wire) against the bind record at `0x814`/`0x818`, and check
  `INFO[23:16]` — a table with zero armed entries matches nothing.
- both climbing → the match is fine and the loss is downstream (format, depacketizer, ring).

That read settles suspects 1 and 3 in one shot, and it is only readable on silicon: it
needs the next flash.

**Trap that will bite you while investigating this: a `0x800` window read of 0 does not mean
"empty".** The listener `SID`/`DMAC` words are served from a snapshot that a `SEL` write
**invalidates** - until the re-poll lands, `milan_csr` returns literal `0` for them
(`acmp_fresh_r` guards the read mux). On a running board a persistence daemon is also
selecting contexts in its own loop, so a bench `devmem` sequence "write SEL, then read"
races with it and can return zeros, half-updated pairs (`SID_HI` right, `SID_LO` 0), or
another context's record entirely. During this investigation that artifact briefly looked
like the root cause. Read it three times and believe the value that repeats - or stop the
daemon for the duration.

**Re-test recipe (do this on the next flash, before anything else).**

1. Bind the board listener to the peer talker (one controller `CONNECT_RX`, §6 of the
   [PipeWire peer guide](../integration/PIPEWIRE_AVB_PEER.md)).
2. Read `AVTPRX_FRX` twice, a second apart. Non-zero and climbing = blocker gone.
3. If still 0, read the `0x8B4` probe group above - that is what it is for, and its three
   readings map 1:1 onto the suspect list. Record the numbers here either way: a *negative*
   ("`PARSED` climbing, `MATCHED` climbing, still no accept") is as informative as a hit.

## Section 22: arming a second talker takes the peer board off the network (and the arm that never happened)

**Symptom (2026-07-26).** With the lwSRP engine disabled (`LWSRP_CTRL 0x680[0] = 0`) an extra
talker context (`t > 0`) is armed for a per-stream experiment. The peer board immediately
stops answering pings and its console floods; the talker sends **~56 000 frames/s** from one
context - roughly 5x the paced class-A rate - and 626 807 frames landed in a single
observation window. Disarming the context restores the peer instantly.

**Root cause - the pacer is the reservation.** Class-A pacing on the extra-talker path comes
from the lwSRP **bandwidth gate**, not from a free-running timer. `~LWSRP_CTRL[0]` is a
deliberate escape hatch (it lets a stream run with no reservation), and with it engaged the
context transmits as fast as the packetizer can build frames. A 50 MHz peer core cannot
survive that interrupt load.

**Rule.** Never leave the engine off with an armed `t > 0` context. Arm extras **only** with
`LWSRP_CTRL[0] = 1`; the escape hatch is for deliberate, watched experiments on a link whose
other end can take it.

**The companion trap - the arm that silently did not happen.** With the engine **off**, `TCTX`
window writes to word 0 (`CTRL`) are **dropped**: the provisioning-commit coupling holds
`wr_rdy` low, and the CSR write completes on the bus with nothing stored. So the sequence
"disable engine → arm context → enable engine" produces a context that was never armed, and a
readback of the window can agree with you. Two rules follow:

- Do the `t > 0` arm/disarm **with the engine on**.
- Take the arm truth from a snapshot, not from the write: `A_STRM_SNAP 0x804[0] = 1`, poll
  busy, then read `A_STRMW_STATE 0x82C[3]` (composed admission). The
  [register map](../reference/REGISTER_MAP.md) `0x800` window rows carry the field layout.

**Related bench fact worth knowing before blaming the board.** An unregistered VLAN-2 stream
DMAC is **flooded** by the bridge - a stream nobody registered still reaches every port at
full rate, while a *registered but listener-less* stream is pruned. A peer board drowning in
frames it never asked for is a switch-forwarding behaviour, not a fabric fault.
