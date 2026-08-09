# Virtual end-to-end validation on real RTL + QEMU — executable roadmap (v2, refined)

Status: **REFINED 2026-08-01 (v2).** Supersedes v1 of this page. It scopes what
"true end-to-end" means for this tree, the refined requirements R1–R8, and the
T0–T6 task list updated for: **RV32 as the default** (RV64 behind a flag),
**T3 = machine-to-machine verification**, and a **Verilator multithreading
policy**. It assumes [`VIRTUAL_E2E_PLAN.md`](VIRTUAL_E2E_PLAN.md) is read; it complements the operator
guide [`VIRTUAL_E2E_HOWTO.md`](VIRTUAL_E2E_HOWTO.md) and the env inventory [`../tooling/virtual-e2e-env.md`](../tooling/virtual-e2e-env.md).

## Contents

- **[1. What "true E2E" means (the bar, stated explicitly)](#1-what-true-e2e-means-the-bar-stated-explicitly)** — the four planes (silicon, software, protocol, oracle) with the falsifier that disqualifies each; T1/M-A2 covers only two, so true E2E begins at T2.
- **[2. Gap analysis (verified this session, not assumed)](#2-gap-analysis-verified-this-session-not-assumed)** — gaps G1–G6 with evidence: Linux never booted in sim, no packet I/O, no oracle; the RV32-firmware gap RESOLVED, both doc gaps closed.
- **[3. Refined requirements (numbered, testable)](#3-refined-requirements-numbered-testable)** — R1–R8 in full, each with an acceptance that must be able to fail: RV32-default, the resolved OpenSBI tuple, wire attachment, T2/T3 negative controls, threading, oracle honesty, evidence.
- **[4. Updated task list T0–T6](#4-updated-task-list-t0t6)** — the status table (T1 DONE, T2–T6 OPEN with what gates each) and the ordering rationale: threading first, wire attachment gates everything after.
- **[5. Refinement for "easily changeable / runnable / provable"](#5-refinement-for-easily-changeable--runnable--provable)** — the five practices: one runner command, versioned contract files as single truth, seeded replay, ratcheted CI, honesty rails.
- **[6. Decisions needed (the remaining forks)](#6-decisions-needed-the-remaining-forks)** — the three open choices: which foreign controller oracle, how to label the three-way CPU-fidelity split, and the virtual wire model.

## 1. What "true E2E" means (the bar, stated explicitly)

A run is **true E2E** iff all four planes are simultaneously real. Anything less
is a partial proof and must be labelled as such.

| plane | requirement | falsifier (disqualifies the claim) |
|---|---|---|
| **Silicon** | The actual `hdl/` SystemVerilog (`milan_datapath` + wrappers) simulated by Verilator | a behavioral stub or Python model standing in for the datapath |
| **Software** | The real firmware/OS stack — BIOS (done), then the real buildroot RV32 Linux image + `S50milan` provisioning, unmodified | a test binary that bypasses the shipped init path |
| **Protocol** | Real frames on a wire: ADP/AECP/ACMP/AVTP-AAF/CRF/gPTP/MRP entering and leaving the RTL MAC, parsed by an independent implementation | loopback-only checks that never serialize an Ethernet frame |
| **Oracle** | An independent implementation validates behaviour (foreign AVDECC stack, decode, or cross-side counter corroboration) — never the DUT grading itself | "PASS" read only from the DUT's own CSRs with no cross-check |

**T1/M-A2 satisfies Silicon + Software(BIOS only). True E2E begins at T2.**
This is the single most important sentence on this page.

## 2. Gap analysis (verified this session, not assumed)

| # | gap | evidence | consequence |
|---|---|---|---|
| G1 | Linux image never booted in sim | only BIOS→`MILN` proven ([`evidence/M-A2-2026-08-01.md`](evidence/M-A2-2026-08-01.md)) | no software-plane provisioning coverage |
| ~~G2~~ | ~~no RV32 OpenSBI firmware~~ | **RESOLVED 2026-08-01** — see R2 below | QEMU RV32 boot is now unblocked |
| G3 | no packet I/O in `milan_sim.py` | SimConfig has only `serial2console`; no ethernet module / TAP | protocol plane untestable in the SoC sim today |
| G4 | no independent oracle attached | `tsn_fuzz` bridges are per-module fuzzers, not an E2E enumerator | oracle plane missing |
| G5 | docs lacked the three directives | now addressed by this v2 + [`VIRTUAL_E2E_HOWTO.md`](VIRTUAL_E2E_HOWTO.md) | closed |
| G6 | HOWTO missing | now written | closed |

## 3. Refined requirements (numbered, testable)

**R1 — RV32 is the default execution path.** Every tier T0–T3 defaults to RV32
(`--xlen=32` on the sim; the RV32 kernel/DTB/rootfs/firmware tuple from
`~/br-milan-rv32/`). RV64 stays *supported* behind an explicit `--xlen=64` /
`RISCV_XLEN=64` and is inventoried but never gates. *Acceptance (must be able to
fail):* `./scripts/virtual-e2e.sh t2` with no flags boots RV32; `RISCV_XLEN=64`
boots RV64. Missing RV32 artifacts → exit 2 (BLOCKED), never a silent RV64
fallback. The RV64 lane must be exercised at least once after the default
lands — an untested flag is a broken flag.

**R2 — RV32 OpenSBI firmware (G2, RESOLVED).** The firmware **exists** at
`$HOME/milan-tests-avb/fpga/boot/opensbi_ax_vexii_rv32.bin` (265,004 B,
2026-07-31 20:24). Verified embedded DTB strings: `litex,alinx_ax7101`,
`audio@f0003120`, `kl,milan-pcm` — the correct RV32 tree with the PCM node, so
the stale-DTB foot-gun does not apply. It is rebuilt deterministically by
`$HOME/milan-tests-avb/fpga/boot/build_opensbi.sh` (OpenSBI 1.7
`litex_nax` platform; XLEN derived from `$CROSS`, with an explicit
XLEN/DTB-agreement gate that refuses an sv39 tree under an RV32 build). For a
QEMU RV32 boot the tuple is: `-bios opensbi_ax_vexii_rv32.bin`, kernel
`~/br-milan-rv32/images/Image` (or `.xz`), `~/br-milan-rv32/images/rootfs.cpio*`.
*Acceptance:* `env-check` records the firmware path + sha256 and reports PASS.

**R3 — Wire attachment (G3).** Add an Ethernet interface to the sim SoC using
LiteX's proven `sim` ethernet mechanism (the same one `litex_sim --with-ethernet`
uses, TAP- or socket-backed), wired to the Milan datapath's MAC port.
*Acceptance (must be able to fail):* from the booted guest, send one ADP
advertise; the frame must appear on the host TAP/socket byte-comparable to a
captured board frame. Note: at 1 MHz `sys_clk` the wire is ~1000× slower than
line rate — fine for control-plane (ADP/AECP); audio-plane streaming assertions
must be cycle-count-based, not wall-clock.

**R4 — T2 acceptance (true single-machine E2E, RV32).** Boot the real buildroot
RV32 image on the sim (or QEMU+verilated pair), let the real `S50milan` run,
then assert: (a) provisioned CSR end-state matches the documented post-provision
register set, (b) one ADPDU observed on the virtual wire, (c) **negative
control:** re-introduce the historical 1x1 `entity_model_id` write defect → the
run must go red on that exact mismatch. Any of the three failing = FAIL. A
final-state CSR snapshot alone is insufficient — the event sequence matters.

**R5 — T3 = machine-to-machine.** Two virtual nodes, each a full instance
(sim SoC or QEMU+verilated-datapath pair), connected at L2 (TAP-to-TAP bridge
or a userspace frame forwarder). One node runs an **independent controller
stack** (a foreign AVDECC implementation — e.g. the `la_avdecc` tooling used as
the golden decoder in the live harness) and must enumerate the other. Do **not**
use two copies of the same internal model as the only oracle. *Acceptance:* the
controller discovers the virtual entity, reads its AEM, and the entity answers
GET_COUNTERS; **negative control:** serve a stale AEM ROM against a new model
id → enumeration must FAIL. Each node gets a distinct MAC/entity-id/stream-id/
persistent image/socket/log/seed.

**R6 — Verilator multithreading policy.** All verilated builds use
`--threads N` (default `nproc`, min 2) with `make -j$(nproc)`.
`--threads-dpi all` is documented but **deferred** — verified: no
`import "DPI-C"` exists in `hdl/` or `tb/` (the co-sim bridges are `--exe` C++
over UNIX sockets), so the flag has nothing to act on until a DPI bridge is
introduced. Implement via a `VERILATOR_THREADS` env var through the LiteX
verilator backend hook (`litex/build/verilator.py`) only if a clean hook
exists; otherwise document as a next step, do not hack the proven boot path.
For multi-node T3, cap per-node threads to avoid oversubscription:
`node_threads = max(2, floor(host_cores / active_nodes))`. Before declaring a
threaded run as evidence, prove determinism: same seed + same inputs →
identical normalized JSONL event log across thread counts. *Acceptance:* a
`--threads 8` Vsim reproduces M-A2 PASS with no output drift.

**R7 — Oracle honesty (cross-cutting).** Every PASS in the runner requires an
independent observation (wire decode, foreign stack, or cross-side counter
corroboration — the same honesty rules as the live torture harness). A green
virtual run is a **simulation result, never a hardware claim**; it does not
retire the bench. Hardware-only properties (Vivado-vs-Verilator gap, PHY/
RGMII timing, analog audio, DDR electricals, real gPTP timestamp quality) are
`BLOCKED` in the virtual tier, never silently skipped or passed.

**R8 — Reproducible evidence.** Every tier emits a dated file under
[`docs/testing/evidence/`](evidence) with: exact command, tool versions, artifact hashes
(RV32/RV64 selection, firmware/kernel/dtb/rootfs, RTL source list), thread
settings, the assertion outputs, and a replayable JSON event log so failures
are reproducible commit-over-commit.

## 4. Updated task list T0–T6

| # | task | engine | acceptance (must be able to FAIL) | status |
|---|---|---|---|---|
| **T0** | env inventory + artifact provenance (hashes) | host | `env-check` records hashes; RV32 tuple complete | **mostly DONE** (env doc + runner); add firmware hash |
| **T1** | reproduce M-A2 (RV32 default) | LiteX Verilator SoC | `ID='MILN'` at `0x90000000`; exit 0 | **DONE** ([`M-A2-2026-08-01.md`](evidence/M-A2-2026-08-01.md)) |
| **T2** | boot real RV32 image, run `S50milan`, assert CSR end-state + first ADPDU | LiteX sim (or QEMU+verilated) | R4 (a)+(b)+(c) | OPEN — needs R2 firmware + R3 wire |
| **T3** | **machine-to-machine** virtual verification | two nodes, virtual L2 | R5 enumerate + stale-AEM negative control | OPEN — needs R3 + independent controller |
| **T4** | harness virtual-bench transport | `harness/transport_virtual.py` | 8-phase campaign board-less; FAILED/BLOCKED intact | OPEN |
| **T5** | independent conformance scenarios (ADP/AECP/ACMP, model consistency) | virtual bench | per-scenario negative control | OPEN |
| **T6** | persistence + virtual power-cycle drill | QEMU | corrupt one slot word → restore count exactly ZERO | OPEN |

Ordering: T1 done; R6 (threading) is the lowest-risk code change next; R3 (wire
attachment) is the largest new code and gates T2/T3; T2/T3 follow only after
their predecessor's negative control has been shown to bite.

## 5. Refinement for "easily changeable / runnable / provable"

1. **One command** — `./scripts/virtual-e2e.sh [env-check|t1|t2-prep|t3-prep|all]`
   (exists, `bash -n` clean). Extend, don't rewrite; reuse `ma2_sim_driver.py`.
2. **Single source of truth for the CSR/packet/event contract** — a versioned
   `csr-contract.yaml` / `packet-contract.yaml` / `event-contract.yaml` that the
   QEMU device, the Verilator bridge, and [`harness/milanharness/csr.py`](../../harness/milanharness/csr.py) all
   consume, so a CSR change touches one file.
3. **Deterministic seeds + replay log** — JSONL event stream; compare event
   sequences, not just final state.
4. **Ratcheted CI** — T1 per-commit (fast); T2/T3 nightly once wired; full T4–T6
   scheduled.
5. **Honesty rails** — green virtual ≠ hardware; the bench stays; unvirtualisable
   properties report `BLOCKED`.

## 6. Decisions needed (the remaining forks)

1. **Independent controller oracle for T3** — pick the foreign AVDECC
   implementation (candidate: the `la_avdecc` golden decoder already trusted by
   the live harness). Required before T3 can be called *independent*.
2. **CPU-fidelity split** — LiteX/NaxRiscv sim proves fabric integration; QEMU
   proves guest artifact + network orchestration; only a VexiiRiscv sim proves
   the exact production core. Use both and label each claim precisely.
3. **Virtual wire model** — start with a deterministic userspace Ethernet bridge
   + PCAP recorder; defer TAP/real host networking until deterministic replay is
   established.
