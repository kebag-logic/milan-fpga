# Virtual end-to-end tier — verified environment inventory

Status: **VERIFIED 2026-08-01** on the development host, repo
`milan-fpga-hermes` (worktree of `milan-fpga`, HEAD `e028662a`).

Every version and path below was read off this box on 2026-08-01 by running the
command in the *check* column. Nothing here is copied from older
notes; where an artifact is **absent**, the row says so rather than omitting it.
Paths are written `~/…` — they are literal, relative to the operator's home.

Read with [`../testing/VIRTUAL_E2E_HOWTO.md`](../testing/VIRTUAL_E2E_HOWTO.md)
(the runnable operator guide) and
[`../testing/VIRTUAL_E2E_QEMU.md`](../testing/VIRTUAL_E2E_QEMU.md) (the T0–T6
roadmap this inventory closes **T0** for).

## Contents

- **[1. The one gotcha that costs an hour](#1-the-one-gotcha-that-costs-an-hour)** — The LiteX venv must be *activated*, not merely referenced, because the build shells out to `python3 -m litex…`.
- **[2. Host and simulation toolchain](#2-host-and-simulation-toolchain)** — Verilator, the venv, the JDK/sbt path that generates the softcore netlist.
- **[3. RISC-V targets: RV32 primary, RV64 secondary](#3-risc-v-targets-rv32-primary-rv64-secondary)** — Two buildroot trees; which one is the default focus and which is kept behind a flag.
- **[4. QEMU](#4-qemu)** — Present, both widths; supersedes the "missing on the box" line in earlier roadmap text.
- **[5. Cached build artifacts](#5-cached-build-artifacts)** — What already exists so a re-run is ~100 s, not a cold build.
- **[6. Firmware (RESOLVED) + remaining T2/T3 blockers](#6-firmware-resolved--remaining-t2t3-blockers)** — The RV32 OpenSBI firmware was found in `milan-tests-avb`; what is still missing is the RAM sim model + wire attachment.
- **[7. Reproducing this inventory](#7-reproducing-this-inventory)** — `scripts/virtual-e2e.sh env-check`.

## 1. The one gotcha that costs an hour

The LiteX venv must be **activated**, not merely referenced:

```sh
. ~/litex-milan/venv/bin/activate
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
```

Invoking `~/litex-milan/venv/bin/python sw/litex/milan_sim.py` *looks*
equivalent and is not. The build shells out to `python3 -m litex…` and to
`make` for the BIOS; those subprocesses resolve `python3` from `PATH`, which
without activation is the **system** python — same version (3.14.6), no
`migen`, no `litex`. The two failures this produces are:

- `ModuleNotFoundError: No module named 'migen'`
- a BIOS build `subprocess.CalledProcessError` at the `crcfbigen` step

Both are the same root cause and neither says so. [`scripts/virtual-e2e.sh`](../../scripts/virtual-e2e.sh)
activates the venv for you; the manual path must do it by hand.

## 2. Host and simulation toolchain

| item | verified value | check |
|---|---|---|
| host cores | 128 | `nproc` |
| Verilator | **5.050** (2026-07-01, rev `v5.050`) | `verilator --version` |
| LiteX venv | `~/litex-milan/venv`, Python **3.14.6** | `~/litex-milan/venv/bin/python --version` |
| system python3 | 3.14.6 -- **lacks `migen`/`litex`** (see Section 1) | `python3 -c "import migen"` fails |
| LiteX source tree | `~/litex-milan/litex` (sim backend: `litex/build/sim/verilator.py`, core Makefile `litex/build/sim/core/Makefile`) | path exists |
| LiteX git sha1 | `a1e1c36` (printed by the booted BIOS) | BIOS banner |
| JDK | OpenJDK **17.0.20** (2026-07-21) at `/usr/lib/jvm/java-17-openjdk` | `$JAVA_HOME/bin/java -version` |
| sbt | `/usr/bin/sbt` | `command -v sbt` |
| softcore netlist cache | `~/litex-milan/pythondata-cpu-naxriscv/pythondata_cpu_naxriscv/verilog/NaxRiscvLitex_<config-hash>.v` — populated; the sim build consumes `NaxRiscvLitex_1b9c524d4409d43204e25d4404d6c364.v` (4.6 MB) | file exists |
| tsn-gen (field generator) | `~/tsn-gen` — present; the [`tb/verilator/tsn_fuzz`](../../tb/verilator/tsn_fuzz) campaigns SKIP cleanly without it | dir exists |

Verilator 5.050 supports `--threads N` and `--threads-dpi <mode>`; the
multithreading policy that uses them is
[Section 5 of `../testing/VIRTUAL_E2E_QEMU.md`](../testing/VIRTUAL_E2E_QEMU.md#5-refinement-for-easily-changeable--runnable--provable).

JDK/sbt only matter when the softcore netlist must be **re**generated. The
cache above is populated, so the M-A2 boot does not shell out to sbt — but
`JAVA_HOME` is still exported on every documented invocation, because the
failure mode when the cache misses is a confusing sbt error deep in the build.

## 3. RISC-V targets: RV32 primary, RV64 secondary

**RV32 is the default focus** for the whole virtual tier: the board shape is
fixed at RV32 VexiiRiscv for area (the RV64 shape does not fit the xc7a100t;
decision recorded 2026-08-01), and the sim SoC's
`--xlen` has always defaulted to 32. RV64 stays *supported*, behind an explicit
`--xlen=64`, and is not the primary path.

### RV32 — primary

| item | verified value |
|---|---|
| buildroot tree | `~/br-milan-rv32/` |
| toolchain prefix | `~/br-milan-rv32/host/bin/riscv32-buildroot-linux-gnu-` |
| compiler | gcc **14.3.0** (`…-gcc-14.3.0` → `toolchain-wrapper`); `g++`, `as`, `ar`, `objcopy`, `addr2line` all present |
| kernel | `~/br-milan-rv32/images/Image` — **7,383,080 B** |
| kernel (compressed) | `~/br-milan-rv32/images/Image.xz` — **2,409,444 B** |
| rootfs | `rootfs.cpio` 29,784,064 B · `rootfs.cpio.gz` 12,815,843 B · `rootfs.cpio.xz` **7,715,920 B** · `rootfs.tar` 31,293,440 B |
| firmware (OpenSBI RV32) | **PRESENT in `milan-tests-avb`** -- `opensbi_ax_vexii_rv32.bin`, see Section 6 |

The two `.xz` sizes are the flash-slot-verified pair, recorded 2026-08-01
(`Image.xz` into a 3 MiB slot; `rootfs.cpio.xz` into a 7,733,248 B slot, 17 KB
slack). They are named here so a virtual run and a flash run demonstrably use
the *same* bytes — the generated-versus-flashed artifact seam that
[Section 1 of `../testing/VIRTUAL_E2E_PLAN.md`](../testing/VIRTUAL_E2E_PLAN.md#1-the-escape-class-this-tier-targets) lists as
an escape class.

### RV64 — secondary, kept behind `--xlen=64`

| item | verified value |
|---|---|
| buildroot tree | `~/br-milan-output/` |
| toolchain prefix | `~/br-milan-output/host/bin/riscv64-buildroot-linux-gnu-` (185 entries in `host/bin`) |
| kernel | `~/br-milan-output/images/Image` (7.9 M), `Image.xz` (2.5 M) |
| rootfs | `rootfs.cpio` (28.3 M), `.gz` (11.3 M), `.xz` (7.0 M), `rootfs.fbi` (8.5 M), `rootfs.tar` (29.6 M) |
| firmware (OpenSBI 1.7) | `fw_dynamic.bin` (266.7 K) · `fw_dynamic.elf` · `fw_jump.bin` (266.6 K) · `fw_jump.elf`; build tree `~/br-milan-output/build/opensbi-1.7` |

Note the naming trap: the RV64 tree's prefix is `riscv64-…` **and so is the
tree's own name**, while the RV32 tree carries a `riscv32-…` prefix. The
xlen of a *simulation* is not set by either — it is set by `--xlen` on the sim
CPU ([`sw/litex/milan_sim.py`](../../sw/litex/milan_sim.py), default 32) and, for T2, by which of the two
image sets is booted.

## 4. QEMU

| item | verified value |
|---|---|
| `qemu-system-riscv32` | **QEMU 11.0.3** — present on `PATH` |
| `qemu-system-riscv64` | **QEMU 11.0.3** — present on `PATH` |

This **supersedes** the "Missing on the box: `qemu-system-riscv*`" line carried
by earlier revisions of the roadmap. Both binaries are installed; T3 is not
blocked on a QEMU install.

## 5. Cached build artifacts

| artifact | path | size |
|---|---|---|
| verilated sim model | `sw/litex/build_milan_sim/gateware/obj_dir/Vsim` | 27.3 MB |
| generated SoC verilog | `sw/litex/build_milan_sim/gateware/sim.v` | 104.7 KB |
| BIOS | `sw/litex/build_milan_sim/software/bios/bios.bin` | (CRC `ec052c87`, printed at boot) |
| build script LiteX regenerates | `sw/litex/build_milan_sim/gateware/build_sim.sh` | 7.0 KB |

`build_sim.sh` begins with `rm -rf obj_dir/`, so **every** `milan_sim.py` run
re-verilates from scratch. On this 128-core host that costs ~15 s at `OPT_LEVEL=O0`
with an unbounded `make -j`, which is why a full M-A2 cycle is ~100 s and not the
several minutes the word "rebuild" suggests. Consequence worth knowing: changing
Verilator flags does not *invalidate* a cache here, because there is no
cross-run object cache to invalidate.

## 6. Firmware (RESOLVED) + remaining T2/T3 blockers

- **RV32 OpenSBI firmware: PRESENT (found 2026-08-01).** It is not in either
  repo tree, but it exists in the `milan-tests-avb` tree:
  `$HOME/milan-tests-avb/fpga/boot/opensbi_ax_vexii_rv32.bin`
  (265,004 B, 2026-07-31 20:24). Embedded-DTB strings verified present:
  `litex,alinx_ax7101`, `audio@f0003120`, `kl,milan-pcm` — the correct RV32 tree
  with the PCM node, so the stale-DTB foot-gun does not apply. Rebuilt
  deterministically by `$HOME/milan-tests-avb/fpga/boot/build_opensbi.sh`
  (OpenSBI 1.7 `litex_nax` platform; XLEN derived from `$CROSS`; an explicit
  XLEN/DTB-agreement gate refuses an sv39 tree under an RV32 build).
- **Caveat (do not overclaim):** that firmware is a *custom LiteX* OpenSBI with
  hard-coded LiteX UART/CLINT/PLIC memory map and an embedded DTB. It will
  **likely not** boot stock `qemu-system-riscv32 -machine virt` (different
  device map) — a custom QEMU machine model is the probable cost. Distinguish:
  the **exact-hardware lane** (VexiiRiscv RV32 + real LiteX SoC, Verilator) is
  authoritative for T2; the **QEMU lane** is fast orchestration and must be
  labelled as such. This is architecture-spike work, not a given.
- **Still genuinely BLOCKED (T2/T3):** (a) `milan_sim.py` has only 64 KiB
  integrated RAM — Linux needs a RAM/SDRAM sim model; (b) no wire attachment on
  the datapath MAC port (SimConfig has only `serial2console`); (c) no
  independent AVDECC oracle wired in. These are engineering tasks R3/R5, not
  artifacts that already exist.
- **No `import "DPI-C"` exists anywhere in `hdl/` or `tb/`.** The co-simulation
  bridges ([`tb/verilator/tsn_fuzz/cosim_axis.h`](../../tb/verilator/tsn_fuzz/cosim_axis.h); and, until 2026-08-13, scripts/run-dut-sim.sh, deleted with the AECP simulation harness it launched) are
  Verilator `--exe` C++ harnesses over UNIX sockets, not DPI. `--threads-dpi`
  therefore has nothing to act on today; it becomes relevant only if T3's bridge
  introduces DPI imports. See the policy in
  [Section 5 of `../testing/VIRTUAL_E2E_QEMU.md`](../testing/VIRTUAL_E2E_QEMU.md#5-refinement-for-easily-changeable--runnable--provable).

## 7. Reproducing this inventory

```sh
cd <repo>
./scripts/virtual-e2e.sh env-check
```

It re-reads every row above and writes a dated report under
[`docs/testing/evidence/`](../testing/evidence). It exits non-zero only on a **required** item
(Verilator, the venv, the RV32 image set); optional items report `SKIP` with the
reason, never a silent pass.
