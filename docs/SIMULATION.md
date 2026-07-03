# Simulation — how the Milan design is simulated and verified

Everything in this design is verified **without vendor tools and without hardware**,
using three layers of simulation (plus a synthesis-portability check). This document
explains each layer: what it is, how it is wired, how to run it, and what it proves.

| Layer | Tool | Top | Proves | Where |
|-------|------|-----|--------|-------|
| **1. RTL unit/integration** | Verilator + C++ | one RTL module (flat-port) | the block behaves per spec, cycle-accurate | `tb/verilator/` (15 harnesses) |
| **2. Softcore boot** | Verilator (via LiteX) | the whole SoC | the NaxRiscv core boots the LiteX BIOS | `litex_sim` / `sw/litex/evidence/naxriscv_sim_boot.log` |
| **3. Softcore + NIC (M-A2)** | Verilator (via LiteX) | SoC + `milan_datapath` | the **CPU reads the NIC over the real bus** | `sw/litex/milan_sim.py` / `…/naxriscv_reads_MILN.log` |
| (aux) Device portability | Yosys + sv2v | each module | synthesizes on non-Xilinx devices | `syn/yosys/` (18 tops) — not simulation, see its README |

These three layers map to the sections below:
[Section 1](#section-1-verilator-rtl-harnesses),
[Section 2](#section-2-softcore-boot-with-litex_sim), and
[Section 3](#section-3-softcore-plus-nic-milestone-m-a2).

Read alongside [`FULL_FPGA_SOLUTION.md`](FULL_FPGA_SOLUTION.md) (architecture) and
[`PROTOCOL_VALIDATION_MATRIX.md`](PROTOCOL_VALIDATION_MATRIX.md) (which test covers
which protocol). If something goes wrong, see [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md).

---

## Section 0: Prerequisites

- **Layer 1 (RTL harnesses)** needs *only* `verilator >= 5.0` + a C++17 compiler.
  No LiteX, no RISC-V toolchain, no Xilinx. This is the fast inner loop.
- **Layers 2–3 (softcore)** additionally need the LiteX venv + RISC-V toolchain +
  JDK/sbt (NaxRiscv is generated from SpinalHDL). One-time setup is in
  [`../sw/README.md`](../sw/README.md); the essentials:
  ```sh
  . ~/litex-milan/venv/bin/activate
  export JAVA_HOME=/usr/lib/jvm/java-17-openjdk      # sbt/SpinalHDL generates NaxRiscv
  cd ~/litex-milan/work                              # NOT the litex-repos parent
  ```
  The last two lines are load-bearing — see
  [Section 1](TROUBLESHOOTING.md#section-1-import-litex-resolves-to-a-namespace-package)
  and [Section 2](TROUBLESHOOTING.md#section-2-naxriscv-generation-needs-java_home)
  of [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md).

---

## Section 1: Verilator RTL harnesses

Each `hdl/` block has a self-checking Verilator harness. They are the primary
verification: a harness exits `0` on pass / non-zero on failure, so they drop
straight into CI. The full list and what each proves is in
[`../tb/verilator/README.md`](../tb/verilator/README.md).

### Section 1.1: Anatomy of a harness

Every harness is three files (using `milan_dp/`, the whole-`milan_datapath` one, as
the worked example):

```
tb/verilator/milan_dp/
  Makefile        # the verilator invocation + source list
  sim_main.cpp    # the C++ testbench (BFMs + self-checks)
  (milan_datapath is the DUT directly — no wrapper needed here)
```

**The DUT top.** Verilator elaborates one SystemVerilog module as the top and
generates a C++ class `V<top>` (e.g. `Vmilan_datapath`). Verilator *flattens*
SystemVerilog `interface` instances (like `axi_stream_if`) internally, so the C++
sees plain signals. Harnesses that verify an interface-using module through a clean
flat boundary provide a thin **flat-port wrapper** (e.g. `datapath/datapath_wrap.sv`,
`classifier/classifier_wrap.sv`); `milan_dp` drives `milan_datapath` directly because
its ports are already flat.

**The C++ testbench** (`sim_main.cpp`) does four things:

1. **Clock the model** — Verilator has no notion of time; the harness toggles the
   clock and calls `eval()`:
   ```cpp
   static void lo() { dut->axis_clk = 0; dut->gtx_clk = 0; dut->eval(); }
   static void hi() { dut->axis_clk = 1; dut->gtx_clk = 1; dut->eval(); }
   static void step() { lo(); hi(); }          // one full cycle
   ```
2. **Drive the DUT with bus-functional models (BFMs)** — small routines that speak
   the DUT's protocols. `milan_dp` has an **AXI4-Lite BFM** (`axi_read`/`axi_write`)
   and an **AXIS frame BFM** (`run_tx`/`run_rx` push/collect a frame, `vlan_frame`
   builds a byte-exact 802.1Q frame packed big-endian into 64-bit beats). The exact
   AXI-Lite handshake timing matters — see
   [Section 11](TROUBLESHOOTING.md#section-11-milan_dp-axi-write-bfm-did-not-commit-writes)
   of [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md).
3. **Self-check** — compare the DUT's response against the expected value:
   ```cpp
   static void ck(const char* what, unsigned long got, unsigned long exp);  // PASS/FAIL + counts
   ...
   ck("ID == 'MILN'", axi_read(0x000), 0x4D494C4E);   // milan_csr ID register
   ```
   A reference model or an independently-computed expectation is the oracle — a
   DUT/model mismatch fails the run. (Some harnesses, e.g. `cbs`, run a
   cycle-accurate reference model in C++ over 10⁴–10⁵ randomized cycles.)
4. **Return the verdict** — `return fails ? 1 : 0;`.

**The Makefile** turns the SV + C++ into a runnable binary:
```make
VFLAGS = --cc --exe --build -j 0 --top-module milan_datapath \
         +incdir+$(RTL_DIR)/common +incdir+... \        # include search paths
         -Wno-fatal -Wno-PINMISSING -Wno-SELRANGE ...    # benign-warning suppressions
SRCS = <packages first> <axis cores> <rtl in dependency order> milan_datapath.sv
run:
	$(VERILATOR) $(VFLAGS) $(SRCS) sim_main.cpp -o Vmilan_dp_sim
	./obj_dir/Vmilan_dp_sim
```
Source order matters: packages (`ethernet_packet_pkg.sv`, `adp_pkg.sv`) and the
`axi_stream_if.sv` interface come first, then leaf modules, then the DUT. The
`+incdir` paths are required — see
[Section 7](TROUBLESHOOTING.md#section-7-verilator-cannot-find-include-file) of
[`TROUBLESHOOTING.md`](TROUBLESHOOTING.md).

### Section 1.2: What milan_dp proves — the integration harness

`milan_dp` is the most complete harness — it drives the entire `milan_datapath`
(the PS-less wrapper) exactly as the SoC will:

```
[CSR] read ID="MILN" (0x4D494C4E), VERSION, CAP.ADP/TCAM bits     ← M-A2 at RTL level
[CSR] program the classifier over the CSR (identity map, readback)
[TX]  push a VLAN frame into the TX-DMA port → byte-exact on the MAC port
[RX]  push a frame into the MAC port → byte-exact on the RX-DMA port
[IRQ] o_irq_csr is a defined level
=> 11 checks, 0 failures
```

### Section 1.3: Running them

```sh
cd tb/verilator/milan_dp && make          # one harness
# the whole suite:
cd tb/verilator && for d in cbs shaper_core cls ptp ptp_sync csr adp adp_tx \
  classifier queues tcam rx_filter cdc datapath milan_dp; do (cd $d && make) || break; done
# expected: each ends "<name>: N checks, 0 failures"; suite total 15/15 green
```

### Section 1.4: Warning suppressions and why they are safe

Two Verilator warnings are suppressed project-wide and are **not** bugs (details in
[Section 12](TROUBLESHOOTING.md#section-12-benign-verilator-warnings-pinmissing-and-selrange)
of [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md)):
- `PINMISSING` on `axi_stream_if` — optional `clk`/`rst_n` interface pins the
  datapath instances don't connect.
- `SELRANGE` inside Forencich `axis_fifo.v` — dead ternary branches selecting
  disabled ID/DEST/USER fields.

---

## Section 2: Softcore boot with litex_sim

This boots the **bare** NaxRiscv SoC (no NIC) under Verilator, end-to-end from HDL
generation to a running BIOS. It is the proof that the softcore itself works with
the open toolchain.

```sh
litex_sim --cpu-type=naxriscv --non-interactive
```

What happens, in order:
1. **NaxRiscv netlist generation** — LiteX shells out to `sbt` which clones
   `SpinalHDL/NaxRiscv` and runs `NaxGen`, emitting a Verilog netlist
   (`NaxRiscvLitex_<hash>.v`). Needs `JAVA_HOME` (JDK17). First run downloads Scala
   (see [Section 2](TROUBLESHOOTING.md#section-2-naxriscv-generation-needs-java_home)
   of [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md)).
2. **SoC elaboration** — LiteX (Migen) builds the SoC (CPU + wishbone bus + CSR +
   ROM/RAM + UART) and writes the top Verilog + a memory map.
3. **Verilator build** — the SoC Verilog + the sim modules (`serial2console`, a
   clocker, …) are compiled into `build/sim/gateware/obj_dir/Vsim`.
4. **BIOS build** — `riscv64-elf-gcc` compiles the LiteX BIOS to `bios.bin`, loaded
   into the integrated ROM.
5. **Run** — `Vsim` executes: BIOS banner → `Memtest OK` → "Booting from serial…
   Timeout / No boot medium" → the **`litex>`** prompt.

Captured output: [`../sw/litex/evidence/naxriscv_sim_boot.log`](../sw/litex/evidence/naxriscv_sim_boot.log).

---

## Section 3: Softcore plus NIC, milestone M-A2

This is the same softcore sim as [Section 2](#section-2-softcore-boot-with-litex_sim)
**plus the real `milan_datapath`** attached as an AXI4-Lite CSR slave, so the CPU
(running the BIOS) can read the NIC's registers over the actual SoC bus. It proves
migration milestone **M-A2** — "CPU reaches `milan_csr`" — on the softcore, not just
at the RTL level (the [Section 1](#section-1-verilator-rtl-harnesses) `milan_dp` harness).

### Section 3.1: How it is wired

`milan_sim.py` is deliberately thin — it reuses the proven pieces:

```python
from litex.tools.litex_sim import SimSoC              # the Section-2 sim SoC
from milan_soc import add_milan_datapath, MILAN_CSR_BASE, MILAN_CSR_SIZE

class MilanSimSoC(SimSoC):
    def __init__(self, **kw):
        SimSoC.__init__(self, **kw)                    # CPU + bus + ROM/RAM + UART
        axil = axi.AXILiteInterface(data_width=32, address_width=32)
        self.bus.add_slave("milan_csr", axil,          # map the NIC CSR window...
            region=SoCRegion(origin=MILAN_CSR_BASE, size=MILAN_CSR_SIZE, cached=False))
        add_milan_datapath(self, self.platform, axil, Signal())   # ...and instantiate the RTL
        self.add_config("BIOS_NO_DELAYS")              # reach the prompt fast (see Section 3.4)
        self.add_config("BIOS_NO_MEMTEST")
```

- `add_milan_datapath()` is the **same helper the board SoC uses** (`milan_soc.py`) —
  it instantiates `milan_datapath`, ties the DMA/MAC AXIS ports idle (only the CSR
  path matters here), and adds the RTL sources **and the `+incdir` include paths**
  (Verilator needs those explicitly — see
  [Section 7](TROUBLESHOOTING.md#section-7-verilator-cannot-find-include-file) of
  [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md)).
- `MILAN_CSR_BASE = 0x9000_0000` — on NaxRiscv an MMIO peripheral must live in the
  CPU IO region (≥ `0x8000_0000`); the register offsets are unchanged from the Zynq
  build (see [`REGISTER_MAP.md`](REGISTER_MAP.md) and
  [Section 6](TROUBLESHOOTING.md#section-6-region-not-in-io-region-it-must-be-cached)
  of [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md)).
- LiteX auto-bridges the CPU Wishbone bus → AXI-Lite (`Bus adapted from AXI-Lite
  32-bit to Wishbone 32-bit` in the build log).

### Section 3.2: Reading the ID register interactively — the simple path

At a real terminal:
```sh
./sw/litex/milan_sim.py --xlen 32          # build + boot; drops you at litex>
litex> mem_read 0x90000000 16              # read the milan_csr ID + VERSION
```

### Section 3.3: The scripted path used to capture the evidence

For automation there is no TTY, and LiteX couples "build" and "run". The robust
recipe is **build once, then pipe commands into the cached `Vsim` binary directly**
(running via `milan_sim.py` a second time blocks — see
[Section 8](TROUBLESHOOTING.md#section-8-the-interactive-and-non-interactive-sim-both-block)
of [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md)):

```sh
# 1. build (this also runs the sim; once "litex>" appears, Ctrl-C — Vsim is now built)
./sw/litex/milan_sim.py --xlen 32 --non-interactive --output-dir build_milan_sim

# 2. run the cached binary with the command on stdin (serial2console = the sim UART)
cd build_milan_sim/gateware
{ sleep 4; printf 'mem_read 0x90000000 16\n'; sleep 5; } | ./obj_dir/Vsim
```

### Section 3.4: Reading the result

```
litex> mem_read 0x90000000 16
Memory dump:
0x90000000  4e 4c 49 4d 03 00 01 00 04 3f 40 00 ...  NLIM.....?@.....
```
- `mem_read` dumps **memory bytes** in address order, little-endian. The `ID`
  register holds the 32-bit word `0x4D494C4E`, which in memory is the byte sequence
  `4e 4c 49 4d` → the ASCII column reads **`NLIM`** (the little-endian byte order of
  the characters "MILN"). This is the NIC identifying itself — **M-A2 reached**.
- The next word `03 00 01 00` = `0x00010003` = the `VERSION` register.

Captured output: [`../sw/litex/evidence/naxriscv_reads_MILN.log`](../sw/litex/evidence/naxriscv_reads_MILN.log).

`BIOS_NO_MEMTEST`/`BIOS_NO_DELAYS` (set in `MilanSimSoC`) are what let the sim reach
the prompt in seconds instead of grinding the memtest/memspeed at the simulated
1 MHz — important because the piped command must arrive **after** the prompt.

---

## Section 4: Where each layer's result is recorded

| Result | File |
|--------|------|
| 15 RTL harnesses pass | run `tb/verilator/` (self-checking; no stored log) |
| Bare softcore boots to `litex>` | `sw/litex/evidence/naxriscv_sim_boot.log` |
| CPU reads NIC ID = MILN (M-A2) | `sw/litex/evidence/naxriscv_reads_MILN.log` |
| 18 tops synthesize (device-portable) | run `syn/yosys/run.sh` |

## Section 5: Speed notes

- [Section 1](#section-1-verilator-rtl-harnesses) harnesses build+run in seconds each.
- [Section 2](#section-2-softcore-boot-with-litex_sim) and
  [Section 3](#section-3-softcore-plus-nic-milestone-m-a2) are dominated by the
  **Verilator compile of the NaxRiscv core** (a few minutes cold). Verilator caches,
  so re-running the *same* binary is fast — hence the "build once, then run `Vsim`
  directly" pattern in [Section 3.3](#section-33-the-scripted-path-used-to-capture-the-evidence).
  The sim itself runs at ~0.03× realtime (a 1 MHz simulated clock), so keep
  interactions short.
