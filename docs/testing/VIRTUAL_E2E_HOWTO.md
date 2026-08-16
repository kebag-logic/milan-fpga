# VIRTUAL E2E HOWTO — simulate the Milan SoC end-to-end, no board required

Status: **2026-08-01.** The copy-paste-runnable operator guide for the boardless
validation tier. Companion docs: [`VIRTUAL_E2E_QEMU.md`](VIRTUAL_E2E_QEMU.md) (roadmap T0–T6),
[historical TRUE E2E requirements](TRUE_E2E_REQUIREMENTS.md) (retired requirement IDs),
[`../tooling/virtual-e2e-env.md`](../tooling/virtual-e2e-env.md) (verified environment inventory),
[`VIRTUAL_E2E_PLAN.md`](VIRTUAL_E2E_PLAN.md) (original scope + honest boundaries).

Read this once before running anything: **a green run here is a simulation
result, never a hardware claim.** Hardware-only properties (PHY timing, analog
audio, Vivado-vs-Verilator differences) report `BLOCKED`, never `PASS`.

## Contents

- **[0. One-time setup](#0-one-time-setup)** — the package install line, where the LiteX venv and both buildroot trees already live, and `env-check` as the one-command environment gate.
- **[1. T1 — the boot proof you can run today (RV32, ~2 min)](#1-t1--the-boot-proof-you-can-run-today-rv32-2-min)** — the runner call and the underlying driver command, the expected PASS output, cache behavior, and the venv-activation gotcha that costs an hour.
- **[2. What T1 does and does not prove](#2-what-t1-does-and-does-not-prove)** — the plane-by-plane honesty table: silicon proven, software BIOS-only, protocol and oracle not yet.
- **[3. T2 — boot the real RV32 Linux image (next tier)](#3-t2--boot-the-real-rv32-linux-image-next-tier)** — the artifact tuple and the two lanes that must not be conflated: exact VexiiRiscv/Verilator (authoritative) vs QEMU orchestration (different CPU fidelity, likely needs a custom machine model).
- **[4. T3 — machine-to-machine verification](#4-t3--machine-to-machine-verification)** — two fully distinct virtual nodes over a deterministic bridge, a foreign AVDECC controller, and the acceptance list including the stale-AEM negative control.
- **[5. Verilator multithreading](#5-verilator-multithreading)** — the three separate knobs (build jobs, sim threads, node count), the per-node cap formula, and the determinism bar threaded runs must clear.
- **[6. Interpreting results](#6-interpreting-results)** — what PASS/FAIL/SKIP/BLOCKED each mean here, and why `t2-prep`/`t3-prep` are never tier passes.
- **[7. Troubleshooting](#7-troubleshooting)** — the symptom→cause→fix table, headed by the migen/venv trap and the stale-build-dir hang.
- **[8. Quick reference card](#8-quick-reference-card)** — every runner command on one screen, including the RV64 lane behind its flag.

## 0. One-time setup

```sh
# Toolchain (already installed on the dev box): verilator >= 5.050,
# qemu-system-riscv32/64, java-17-openjdk, docker.
sudo pacman -S --needed verilator qemu-system-riscv jdk17-openjdk

# LiteX venv (already exists): ~/litex-milan/venv
# Buildroot image trees (already exist): ~/br-milan-rv32 (RV32, DEFAULT),
# ~/br-milan-output (RV64, kept behind a flag).

# Sanity: the whole environment gate in one command.
cd <worktree>
./scripts/virtual-e2e.sh env-check
```

`env-check` exits non-zero only if a **required** item is missing; optional
items print `SKIP` with the reason. Its output lands in
`docs/testing/evidence/virtual-e2e-env-check-<date>.md`.

## 1. T1 — the boot proof you can run today (RV32, ~2 min)

This is the proven, repeatable M-A2 check: the real softcore boots the real
BIOS against the real `milan_datapath` RTL and reads `ID='MILN'`.

```sh
cd <worktree>
./scripts/virtual-e2e.sh t1
```

Or the underlying command directly (the runner wraps exactly this):

```sh
source <litex-work>/litex-milan/venv/bin/activate        # REQUIRED — see gotcha below
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
python scripts/ma2_sim_driver.py --repo <worktree> \
  --log /tmp/ma2_run.log
echo "exit=$?"                                          # 0 = PASS
```

Expected PASS output (last driver line):

```
M-A2: PASS prompt_reached=True dump_seen=True
```

And in the log, the ID dump proving the CPU reached the real RTL CSRs:

```
0x90000000  4e 4c 49 4d 21 00 01 00 ...   NLIM!.....      <- 'MILN' little-endian
```

A cached Verilator build lives in `sw/litex/build_milan_sim/`, so a rerun is
~100 s. To force a cold rebuild, delete that directory and re-run (a few
minutes).

**The one gotcha that costs an hour:** the venv must be *activated*, not merely
referenced on the command line — the BIOS build shells out to
`python3 -m litex...`, which resolves to the system python (no migen/litex) if
the venv isn't active. Symptom: `ModuleNotFoundError: No module named 'migen'`
or a `crcfbigen` `CalledProcessError`.

## 2. What T1 does and does not prove

| plane | status after T1 |
|---|---|
| Silicon (real RTL in Verilator) | proven |
| Software | BIOS only — Linux image boot is T2 |
| Protocol (frames on a wire) | not yet — wire attachment is R3/T2 |
| Oracle (independent validator) | not yet — T3 |

T1 is the foundation, not the goal. **True E2E begins at T2.**

## 3. T2 — boot the real RV32 Linux image (next tier)

Prerequisites (present on this box; `env-check` hashes them):

| artifact | path |
|---|---|
| RV32 OpenSBI firmware | `$HOME/milan-tests-avb/fpga/boot/opensbi_ax_vexii_rv32.bin` (verified DTB strings: `audio@f0003120`, `kl,milan-pcm`) |
| RV32 kernel | `~/br-milan-rv32/images/Image` (or `Image.xz`) |
| RV32 rootfs | `~/br-milan-rv32/images/rootfs.cpio*` |

**Two lanes, and the difference matters (do not conflate them):**

1. **Exact-production-hardware lane (authoritative for T2).** VexiiRiscv RV32 +
   the real LiteX SoC + the real `milan_datapath`, all under Verilator. This is
   the strongest CPU/RTL fidelity. It needs the sim SoC switched from the
   historical NaxRiscv core to VexiiRiscv **and** a Linux-sized simulated RAM
   (`milan_sim.py` currently uses only 64 KiB integrated RAM — Linux needs a
   RAM/SDRAM sim model). This is an open spike, not a given.
2. **Fast QEMU orchestration lane.** QEMU RV32 CPU + a custom LiteX-compatible
   machine model, with `milan_datapath` still as real verilated RTL over a
   socket. Faster Linux/timers/reboot/multi-machine. **Labelled QEMU-CPU
   fidelity, not exact VexiiRiscv execution.** The custom LiteX OpenSBI
   (hard-coded LiteX UART/CLINT/PLIC map, embedded DTB) will **likely not boot
   stock `qemu-system-riscv32 -machine virt`** — this must be *demonstrated*, not
   assumed; a custom machine model is the probable cost.

```sh
./scripts/virtual-e2e.sh t2-prep   # prerequisite gate (today; not a tier pass)
```

Remaining engineering for a full T2 (roadmap R3/R4): wire attachment (LiteX sim
ethernet on the datapath MAC port), guest boot of the RV32 tuple with real
`S50milan`, then assertions (CSR end-state, one ADPDU on the wire, the 1x1
`entity_model_id` negative control must go red).

At the sim's 1 MHz clock the wire is ~1000x slower than line rate — assert on
**cycles and events**, never wall-clock throughput.

## 4. T3 — machine-to-machine verification

Two virtual nodes (each: RV32 guest + own verilated datapath, distinct MAC /
entity-id / stream-id / image / log / seed), bridged at L2 by a deterministic
userspace Ethernet bridge + PCAP recorder (defer TAP/host networking until
replay works). One node runs an **independent AVDECC controller** (candidate:
the `la_avdecc` golden decoder trusted by the live harness) and must enumerate
the other.

```sh
./scripts/virtual-e2e.sh t3-prep   # prerequisite gate (today; not a tier pass)
```

Acceptance: foreign controller discovers the virtual entity, reads its AEM,
GET_COUNTERS answers; serving a stale AEM ROM against a new model id must FAIL;
duplicate entity ids rejected before launch; reboot of one node produces
departure then re-advertisement.

## 5. Verilator multithreading

Separate three knobs (they are not the same thing):

```
VERILATOR_BUILD_JOBS   # make -j, accelerates compilation. Default: nproc
VERILATOR_THREADS      # --threads N, accelerates runtime IF enough mtasks. Default: nproc (min 2)
ACTIVE_NODES           # for multi-node T3
```

For multi-node: `VERILATOR_THREADS = max(2, floor(host_cores / ACTIVE_NODES))`
— never `nproc` per node (oversubscription). Caveats: a single-clock SoC may
see limited `--threads` speedup; `--threads-dpi all` is **deferred** (no
`import "DPI-C"` exists in `hdl/` or `tb/`; bridges are C++ `--exe` over
sockets). Benchmark threads = 1/2/4/8 and pick the fastest *deterministic*
value; threaded results count as evidence only after same-seed normalized JSONL
matches across thread counts (E2E-PERF-3).

## 6. Interpreting results

| verdict | meaning | action |
|---|---|---|
| `PASS` | assertion observed to hold, with an independent observation where required | proceed |
| `FAIL` | something that should work did not | run is red on purpose — read the event log |
| `SKIP` | optional item absent | no action |
| `BLOCKED` | a genuine prerequisite is absent (e.g. a hardware-only property) | expected for hardware-only checks; never a pass |

`t2-prep` / `t3-prep` are **prerequisite gates, not tier passes.** A tier is
`PASS` only when its own acceptance criteria (with a working negative control)
have run.

## 7. Troubleshooting

| symptom | cause | fix |
|---|---|---|
| `ModuleNotFoundError: migen` / `litex` | venv not activated | `source ~/litex-milan/venv/bin/activate` |
| BIOS build fails at `crcfbigen` | system python ran the BIOS build | same as above |
| Sim hangs before `litex>` prompt | stale/partial build dir | remove `sw/litex/build_milan_sim/`, cold rebuild |
| Boot reaches BIOS but dump is wrong | CSR window moved | check banner `milan_csr` base == `0x9000_0000` |
| QEMU RV32 boots nothing | missing `-bios` / stock-machine mismatch | use `opensbi_ax_vexii_rv32.bin`; a custom QEMU machine model may be required (see §3 lane 2) |
| `env-check` FAIL on RV32 artifacts | `~/br-milan-rv32` absent | restore/rebuild the RV32 buildroot output tree |
| Threaded Verilator run shows drift | determinism gate violated | run single-threaded for evidence; treat drift as a bug |

## 8. Quick reference card

```sh
cd <worktree>
./scripts/virtual-e2e.sh env-check   # environment gate (T0)
./scripts/virtual-e2e.sh t1          # boot proof, RV32 (PROVEN)
./scripts/virtual-e2e.sh t2-prep     # RV32 image-boot prerequisites
./scripts/virtual-e2e.sh t3-prep     # machine-to-machine prerequisites
./scripts/virtual-e2e.sh all         # full dependency graph
RISCV_XLEN=64 ./scripts/virtual-e2e.sh t1   # RV64 lane (secondary, behind flag)
```
