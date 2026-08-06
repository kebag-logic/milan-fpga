# Virtual E2E run - `t2-prep` - 2026-08-01

Produced by `scripts/virtual-e2e.sh t2-prep`. Verdict: **BLOCKED**.
Simulation result only - not a hardware claim.

Tally: 28 PASS / 0 FAIL / 0 SKIP / 1 BLOCKED.

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
| `sim.cached-model` | **PASS** | 28609720 B |
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

