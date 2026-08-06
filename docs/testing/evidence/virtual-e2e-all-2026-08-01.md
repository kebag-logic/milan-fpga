# Virtual E2E run - `all` - 2026-08-01

Produced by `scripts/virtual-e2e.sh all`. Verdict: **BLOCKED**.
Simulation result only - not a hardware claim.

Tally: 35 PASS / 0 FAIL / 1 SKIP / 4 BLOCKED.

### T0 env-check - host, toolchain, images

| check | state | detail |
|---|---|---|
| `host.cores` | **PASS** | 128 cores |
| `verilator` | **PASS** | Verilator 5.050 2026-07-01 rev v5.050 |
| `litex.venv` | **PASS** | <litex-work>/litex-milan/venv (python 3.14.6) |
| `litex.venv.modules` | **PASS** | migen + litex importable |
| `jdk` | **PASS** | openjdk version "17.0.20" 2026-07-21 at /usr/lib/jvm/java-17-openjdk |
| `sbt` | **PASS** | /usr/bin/sbt |
| `rv32.kernel` | **PASS** | 7383080 B |
| `rv32.rootfs.cpio` | **PASS** | 7715920 B |
| `rv32.kernel.xz` | **PASS** | 2409444 B |
| `rv32.toolchain` | **PASS** | 14.3.0 at $HOME/br-milan-rv32/host/bin/riscv32-buildroot-linux-gnu- |
| `rv64.kernel` | **PASS** | 8311504 B |
| `rv64.opensbi` | **PASS** | 273024 B |
| `rv64.toolchain` | **PASS** | <buildroot-output>/host/bin/riscv64-buildroot-linux-gnu- |
| `qemu.riscv32` | **PASS** | QEMU emulator version 11.0.3 |
| `qemu.riscv64` | **PASS** | QEMU emulator version 11.0.3 |
| `tsn-gen` | **PASS** | $HOME/tsn-gen |
| `sim.cached-model` | **PASS** | 28620528 B |
| `ma2.driver` | **PASS** | 3653 B |
| `verilator.threads` | **PASS** | VERILATOR_THREADS=(unset - single-threaded, the proven M-A2 path) |

### T1 - M-A2 boot proof (softcore reads ID='MILN')

| check | state | detail |
|---|---|---|
| `t1.ma2.boot` | **PASS** | M-A2: PASS prompt_reached=True dump_seen=True |
| `t1.ma2.id-magic` | **PASS** | 4e 4c 49 4d 21 00 01 00 05 7f 40 00 00 00 00 00  NLIM!.....@..... (LE 'MILN') |
| `t1.log` | **PASS** | /tmp/virtual-e2e-t1-2026-08-01.log |

### T2-prep - RV32 image-boot prerequisites

| check | state | detail |
|---|---|---|
| `t2.rv32.kernel` | **PASS** | 7383080 B |
| `t2.rv32.rootfs` | **PASS** | 7715920 B |
| `t2.sim.entry` | **PASS** | 6342 B |
| `t2.xlen.default` | **PASS** | milan_sim.py --xlen default 32 (RV32 primary); --xlen=64 supported |
| `t2.oracle.source` | **PASS** | scripts/check_entity_shape.py (same constants source as the CSR oracle) |
| `t2.rv32.opensbi` | **PASS** | 265004 B |
| `t2.boot-the-image` | **BLOCKED** | not implemented yet - this target only proves prerequisites |

### T3-prep - machine-to-machine (two virtual nodes, one enumerates the other)

| check | state | detail |
|---|---|---|
| `t3.qemu.riscv32` | **PASS** | QEMU emulator version 11.0.3 |
| `t3.verilator` | **PASS** | Verilator 5.050 2026-07-01 rev v5.050 |
| `t3.cosim.header` | **PASS** | 5397 B |
| `t3.cosim.driver` | **PASS** | 11362 B |
| `t3.dut-sim` | **PASS** | 1238 B |
| `t3.datapath.rtl` | **PASS** | 231020 B |
| `t3.dpi.present` | **SKIP** | no DPI-C in hdl/ or tb/ (bridges are --exe C++ over UNIX sockets); --threads-dpi is a no-op until T3 adds one |
| `t3.rv32.opensbi` | **PASS** | 265004 B |
| `t3.bridge` | **BLOCKED** | socket/chardev bridge between the two verilated nodes not built yet |
| `t3.virtual-l2` | **BLOCKED** | virtual L2 (QEMU netdev/TAP or userspace bridge) not wired yet |
| `t3.neg-control` | **BLOCKED** | stale-AEM-ROM-vs-new-model-id negative control not implemented yet |

