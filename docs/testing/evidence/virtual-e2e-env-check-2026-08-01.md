# Virtual E2E run - `env-check` - 2026-08-01

Produced by `scripts/virtual-e2e.sh env-check`. Verdict: **PASS**.
Simulation result only - not a hardware claim.

Tally: 19 PASS / 0 FAIL / 0 SKIP / 0 BLOCKED.

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
| `sim.cached-model` | **PASS** | 29294288 B |
| `ma2.driver` | **PASS** | 3653 B |
| `verilator.threads` | **PASS** | VERILATOR_THREADS=(unset - single-threaded, the proven M-A2 path) |

