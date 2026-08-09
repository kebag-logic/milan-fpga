# TRUE E2E requirements — stable IDs for the boardless virtual validation tier

Status: **2026-08-01.** Normative requirement set for the Milan v1.2 AVB/TSN
virtual end-to-end tier. Every requirement has: ID, statement, rationale,
implementation component, observable evidence, positive acceptance, negative
control, and a status of **PROVEN / PLANNED / BLOCKED**. Companion docs:
[`VIRTUAL_E2E_QEMU.md`](VIRTUAL_E2E_QEMU.md) (roadmap T0–T6), [`VIRTUAL_E2E_HOWTO.md`](VIRTUAL_E2E_HOWTO.md) (operator guide),
[`../tooling/virtual-e2e-env.md`](../tooling/virtual-e2e-env.md) (verified inventory).

Definitions: **DUT** = the verilated real `milan_datapath` RTL + its guest.
**Oracle** = an implementation independent of the DUT (foreign AVDECC stack,
independent decoder, or cross-side corroboration). A mock may control faults or
collect evidence; it may **never** generate the behavior being declared valid.

## Contents

- **[E2E-ART — artifact provenance](#e2e-art--artifact-provenance)** — manifest hashes for every run, RV32 as the no-fallback default tuple, and the already-verified OpenSBI binary.
- **[E2E-BOOT — firmware/Linux boot](#e2e-boot--firmwarelinux-boot)** — the boot ladder: the 'MILN' ID read is PROVEN (M-A2 evidence); unmodified-buildroot boot and `S50milan` in-guest are still PLANNED.
- **[E2E-MMIO — CSR bridge](#e2e-mmio--csr-bridge)** — guest accesses must hit real RTL at the real base/width, with a versioned `csr-contract.yaml` as single truth and bounded (never hung) timeouts.
- **[E2E-NET — virtual wire](#e2e-net--virtual-wire)** — a PCAP-captured shared L2 with drop/duplicate/reorder/corrupt injection, plus the cycle-time honesty rule for the 1 MHz sim clock.
- **[E2E-DMA / E2E-IRQ — data + interrupt planes](#e2e-dma--e2e-irq--data--interrupt-planes)** — rings allocated by the production driver and at least one RTL-asserted interrupt actually delivered and acknowledged.
- **[E2E-M2M — machine-to-machine (T3 core)](#e2e-m2m--machine-to-machine-t3-core)** — two fully independent virtual nodes on one L2, a foreign AVDECC controller on Node B, and the reboot departure/re-advertisement sequence.
- **[E2E-ORACLE — independent verdicts](#e2e-oracle--independent-verdicts)** — no PASS without an independent observation, and no scenario admitted until its negative control has been demonstrated to fail.
- **[E2E-RESET — persistence/restart](#e2e-reset--persistencerestart)** — journal restore across a full VM stop/start with zero controller traffic; a corrupted slot must restore exactly zero binds.
- **[E2E-PERF — Verilator threading](#e2e-perf--verilator-threading)** — threading defaults, per-node thread caps for multi-node runs, and the determinism gate a threaded build must pass before it counts as evidence.
- **[E2E-EVID — evidence & replay](#e2e-evid--evidence--replay)** — the artifact set every run emits (manifest, logs, JSONL, PCAP, verdicts) and the seed-replay reproducibility bar.
- **[E2E-HONEST — hardware-only boundaries (BLOCKED, never passed)](#e2e-honest--hardware-only-boundaries-blocked-never-passed)** — what the virtual tier can never prove: P&R timing, PHY/analog, real gPTP quality; a green virtual run is never a hardware claim.

## E2E-ART — artifact provenance

| ID | requirement | acceptance / negative control | status |
|---|---|---|---|
| E2E-ART-1 | Every run records hashes of firmware, kernel, DTB, rootfs, RTL source list, guest config, and tool versions in `manifest.json` | manifest complete → PASS; any missing hash → FAIL | PLANNED |
| E2E-ART-2 | RV32 is the default tuple (`~/br-milan-rv32/` kernel/rootfs + RV32 OpenSBI + RV32 DTB); RV64 only via explicit flag | no-flag run boots RV32; missing RV32 artifact → `BLOCKED`, never silent RV64 fallback | PLANNED |
| E2E-ART-3 | RV32 OpenSBI firmware: `$HOME/milan-tests-avb/fpga/boot/opensbi_ax_vexii_rv32.bin` (265,004 B), rebuilt by `build_opensbi.sh` (OpenSBI 1.7 `litex_nax`, XLEN/DTB-agreement gate) | sha256 recorded in `env-check`; XLEN/DTB mismatch → gate refuses | **PROVEN to exist + verified DTB strings (`audio@f0003120`)**; not yet consumed by a boot |

## E2E-BOOT — firmware/Linux boot

| ID | requirement | acceptance / negative control | status |
|---|---|---|---|
| E2E-BOOT-1 | RV32 softcore boots the real LiteX BIOS and reads `ID='MILN'` at `0x9000_0000` | exit 0 from [`scripts/ma2_sim_driver.py`](../../scripts/ma2_sim_driver.py); corrupt expected ID → FAIL | **PROVEN** ([`evidence/M-A2-2026-08-01.md`](evidence/M-A2-2026-08-01.md)) |
| E2E-BOOT-2 | The exact RV32 buildroot image boots unmodified (firmware→kernel→DTB→rootfs) | guest reports rv32; wrong-DTB/XLEN tuple → BLOCKED, not a boot | PLANNED |
| E2E-BOOT-3 | Production init (`S50milan`) runs in the virtual guest | provisioning writes visible in RTL CSRs; skipping init → no such writes → FAIL | PLANNED |

## E2E-MMIO — CSR bridge

| ID | requirement | acceptance / negative control | status |
|---|---|---|---|
| E2E-MMIO-1 | Guest CSR accesses at the real base/width (`0x9000_0000`, 32-bit) reach real RTL, not a behavioral model | version/ID registers match; wrong base → driver probe FAIL | PLANNED |
| E2E-MMIO-2 | A versioned `csr-contract.yaml` is the single source of truth consumed by QEMU device, Verilator bridge, harness, and decoders | contract↔RTL fingerprint mismatch → FAIL | PLANNED |
| E2E-MMIO-3 | Bounded backpressure/timeout: a dropped bridge response produces a classified timeout, never a hung test | inject dropped response → bounded TIMEOUT verdict | PLANNED |

## E2E-NET — virtual wire

| ID | requirement | acceptance / negative control | status |
|---|---|---|---|
| E2E-NET-1 | Ethernet frames serialize onto a shared virtual L2 from the real RTL MAC (LiteX sim ethernet / socket-backed), captured deterministically (PCAP) | one ADPDU byte-compared to a captured board frame; mismatched bytes → FAIL | PLANNED |
| E2E-NET-2 | Wire supports fault injection: drop, duplicate, reorder, corrupt | injected fault → classified behavior; silent acceptance of corrupt frame → FAIL | PLANNED |
| E2E-NET-3 | Cycle-time honesty: at 1 MHz sim clock, protocol assertions are cycle/event-based, not wall-clock-rate-based | any wall-clock-rate assertion at sim speed → test marked invalid | PLANNED |

## E2E-DMA / E2E-IRQ — data + interrupt planes

| ID | requirement | acceptance / negative control | status |
|---|---|---|---|
| E2E-DMA-1 | Real DMA rings are allocated by the production driver and consumed by the RTL | ring traffic in event log; invalid descriptor → classified error | PLANNED |
| E2E-IRQ-1 | At least one interrupt is asserted by RTL, delivered to the guest, and acknowledged | IRQ event in log; suppressed IRQ → FAIL (not a silent timeout) | PLANNED |

## E2E-M2M — machine-to-machine (T3 core)

| ID | requirement | acceptance / negative control | status |
|---|---|---|---|
| E2E-M2M-1 | Two independent virtual nodes (each: RV32 guest + own verilated datapath + own MAC/entity-id/stream-id/image/log/seed) share one virtual L2 | both enumerate over the wire; identical IDs → config FAIL | PLANNED |
| E2E-M2M-2 | Node B runs an independent AVDECC controller/decoder (candidate: `la_avdecc` golden decoder); it must NOT be the same internal model | controller discovers Node A and reads its AEM | PLANNED |
| E2E-M2M-3 | AECP descriptor reads match Node A's configured model; GET_COUNTERS answers | stale AEM ROM vs new model id → enumeration FAIL | PLANNED |
| E2E-M2M-4 | Reboot of one node produces departure/re-advertisement on the surviving node | missing departure sequence → FAIL | PLANNED |

## E2E-ORACLE — independent verdicts

| ID | requirement | acceptance / negative control | status |
|---|---|---|---|
| E2E-ORACLE-1 | Every PASS requires an independent observation (wire decode, foreign stack, or cross-side counters) | DUT-only self-read PASS → verdict downgraded | PLANNED |
| E2E-ORACLE-2 | Every scenario ships a negative control that has been **demonstrated to fail** | a negative control that cannot go red → scenario not admitted to CI | PLANNED |

## E2E-RESET — persistence/restart

| ID | requirement | acceptance / negative control | status |
|---|---|---|---|
| E2E-RESET-1 | Virtual power-cycle (full VM stop/start, not userspace restart) restores a bind from the journal with zero controller traffic | restore events in log | PLANNED |
| E2E-RESET-2 | Corrupt one journal slot word → restore count is exactly ZERO, never partial | partial restore → FAIL | PLANNED |

## E2E-PERF — Verilator threading

| ID | requirement | acceptance / negative control | status |
|---|---|---|---|
| E2E-PERF-1 | All verilated builds use `--threads N` (default `nproc`, min 2) + `make -j`; build-jobs and sim-threads are separately configurable | `--threads 8` build reproduces M-A2 PASS | PLANNED |
| E2E-PERF-2 | Multi-node runs cap per-node threads: `node_threads = max(2, floor(host_cores / active_nodes))` | oversubscription warning in manifest | PLANNED |
| E2E-PERF-3 | Determinism gate: same seed + inputs → identical normalized JSONL across thread counts before threaded mode is an evidence lane | drift → threaded run disqualified as evidence | PLANNED |
| E2E-PERF-4 | `--threads-dpi all` only when a real `import "DPI-C"` exists (none today) | claiming it active without DPI → docs bug | PLANNED |

## E2E-EVID — evidence & replay

| ID | requirement | acceptance / negative control | status |
|---|---|---|---|
| E2E-EVID-1 | Every run emits `manifest.json`, per-node console logs, RTL event JSONL, wire PCAP, CSR before/after, `verdict.json`, `junit.xml` under a dated evidence dir | missing artifact → report incomplete | PARTIAL (runner emits env-check + t1 evidence) |
| E2E-EVID-2 | Event log carries `{vtime, node, source, event, data}` per entry; replay from seed reproduces the verdict | non-reproducible log → not a CI gate | PLANNED |

## E2E-HONEST — hardware-only boundaries (BLOCKED, never passed)

| ID | requirement | status |
|---|---|---|
| E2E-HONEST-1 | FPGA synth/P&R differences, Vivado-vs-Verilator gap | BLOCKED in virtual tier |
| E2E-HONEST-2 | Board clock/PHY/RGMII timing, DDR electricals, analog audio/I²S quality | BLOCKED in virtual tier |
| E2E-HONEST-3 | Real gPTP timestamp quality, switch-specific multicast/queue/CBS behavior (unless deliberately modeled) | BLOCKED in virtual tier |
| E2E-HONEST-4 | A green virtual run is a simulation result, never a hardware claim; the bench is not retired | permanent rail |
