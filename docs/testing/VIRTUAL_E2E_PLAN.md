# Virtual end-to-end tier — boot the real image against the real fabric, per commit

Status: **PROPOSED 2026-07-28 (USER: "add it to the roadmap")** — roadmap
item 13 in [`../MILAN_COMPLIANCE_GAPS.md`](../MILAN_COMPLIANCE_GAPS.md).
Nothing below exists yet except the scaffolding named in §3; this page is the
plan, its acceptance criteria, and the honest boundary of what it can never
replace.

## Contents

- **[1. The escape class this tier targets](#1-the-escape-class-this-tier-targets)** — Five defects found by hand in one session, every one invisible to all 57 Verilator suites and to behave, every one living in the software/boot-chain/artifact seam that only a booted image exercises. The tier exists to make that review mechanical, per commit.
- **[2. What it structurally cannot catch](#2-what-it-structurally-cannot-catch)** — The bench stays. The Vivado-vs-Verilator gap, wall-clock/PHY timing, and analog properties have no fidelity in virtual time; this repo's own defect history names one silicon-only saga per category.
- **[3. Tooling options, assessed against this tree](#3-tooling-options-assessed-against-this-tree)** — Extend the existing Verilator sim SoC (cheapest start, already boots the real BIOS to `ID='MILN'`), Renode with a verilated `milan_datapath` (the multi-machine virtual bench), or raw QEMU cosimulation (most glue, last resort). The recommendation is A-then-B, and why.
- **[4. Phases V0-V3, each with its oracle and its negative control](#4-phases-v0-v3-each-with-its-oracle-and-its-negative-control)** — From the M-A2 boot check that already passes, through boot-the-image-and-assert-the-provisioned-state, to a two-machine virtual bench an independent controller stack enumerates, to the fast-connect reboot drill as CI. Each phase's negative control is a real defect from the 2026-07-28 session, replayed.
- **[5. Timers, and where each tool wins](#5-timers-and-where-each-tool-wins)** — RTL timers already shrink with the `-G` discipline; the Linux daemons' timers are the awkward half, and virtual-time simulators are the only clean answer for them.
- **[6. Where it sits in the methodology](#6-where-it-sits-in-the-methodology)** — A new rung between L3 and L5: the wire, on virtual hardware, with the L4 independent-controller oracle kept honest through a TAP. The normative levels table gains the row when the tier lands, not before.

## 1. The escape class this tier targets

The 2026-07-28 session found, **by manual review alone**, five defects that
no desk gate could see and that would otherwise have cost a build+flash+bench
trip each:

| defect | where it lived |
|---|---|
| both boards' boot script wrote the 1x1 `entity_model_id` onto every flash shape (controllers cache AEM **by model id**) | `S50milan` |
| the CRF identity override recomputed *claim base + 1* = **AAF talker 1's DMAC** on the 8x8 — a colliding multicast | `S50milan` |
| the MAAP claim was sized 8 for 9 streams, leaving the CRF's `base+N` slot undefended | `S50milan` |
| the DTB DMA windows needed a hand-migrated `+0x74` for `rx_queues: 2`, guarded only by review | deployed `.dts` |
| `CRFT_CTRL` was provisioned `0x1` (the untagged-flood posture) after the class-A bit existed | `S50milan` |

The pattern is the one
[`methodology.md`](methodology.md) §1 already names (escapes 4 and 6: absent
platform backing, generated-versus-flashed artifacts): **the seam between the
fabric and the software that provisions it is tested by nothing**. L0-L3 test
modules and models; L5 tests silicon hours later. Every defect above is a
deterministic function of `(image, init script, gateware CSR map)` — a booted
virtual system with the *real* rootfs and the *real* `S50milan` against the
*real* `milan_datapath` RTL catches all five mechanically, on every commit.

The same tier is the only realistic way the saved-state fast-connect **reboot
drill** (the saved-state fast-connect design record was deleted 2026-08-13 with the persistence engine; **nothing in this device restores a binding across a power cycle** now — gates G0-G2: partition
appears, journal restores, binds survive a power cycle) ever becomes CI
instead of a bench ritual.

## 2. What it structurally cannot catch

Named per category from this repo's own defect ledger, so nobody retires the
bench on the strength of a green virtual run:

- **The Vivado-vs-Verilator gap.** The four silicon-only `GET_DYNAMIC_INFO`
  defects (LUTRAM read-port replication, the Synth 8-4767 RAM-inference
  fallback) passed every Verilator build ever run. A verilated virtual tier
  shares exactly that blind spot.
- **Wall-clock, PHY and load properties.** The D7 grandmaster depose under a
  950M flood, ingressLatency calibration, servo step polarity, GMII edge
  inversion, the MAC-TX wedge on link bounce — none has meaning in virtual
  time.
- **Analog.** The DAC loop, THD+N, the media-clock ppm chain.

The tier **reduces bench trips**; it never replaces the bench tier. R6 stands:
a hardware claim still requires a hardware run.

## 3. Tooling options, assessed against this tree

**A. Extend the in-tree Verilator sim SoC — the recommended start.**
[`../../sw/litex/milan_sim.py`](../../sw/litex/milan_sim.py) already boots the
**real LiteX BIOS** on the softcore with `milan_datapath` attached at its real
CSR base and reads `ID='MILN'` — migration milestone M-A2, proven. What V1
adds on top of it: boot the buildroot **image** instead of stopping at the
BIOS, a virtual ethernet (LiteX sim ethernet / TAP), and assertions over the
CSR end-state after `S50milan` runs. Known fight: Linux-boot wall-clock in a
cycle-accurate simulation; if it lands under ~15 min it can gate per-PR,
otherwise nightly. Zero new toolchain, and the module-level socket-bridge
pattern (scripts/run-dut-sim.sh and Containerfile.dut-sim, both deleted
2026-08-13 with the AECP simulation harness they launched) showed the
container discipline to reuse.

**B. Renode with a verilated `milan_datapath` — the multi-machine end game.**
First-class LiteX/RISC-V platform support, co-simulation of exactly one
verilated peripheral (our whole custom fabric is a single AXI-Lite + AXIS
block), **deterministic virtual time** (the answer to §5's daemon-timer
problem), and multi-machine simulations wired into one virtual network — a
two-board bench plus a TAP into the host, so a real controller stack
enumerates a virtual board and the L4 oracle stays independent. The cost is
the platform description and the verilated-block bridge; the payoff is V2/V3.

**C. Raw QEMU with a cosimulation bridge — last resort.** A custom machine
model, an AXI transactor, and lockstep time synchronization are all
hand-built glue for this stack. Only worth revisiting if Renode's CPU support
lags the VexiiRiscv the boards actually run.

## 4. Phases V0-V3, each with its oracle and its negative control

Per [`methodology.md`](methodology.md) §4: every phase names its oracle, and
R2 demands each new check be shown able to fail — the negative controls below
are **real defects from the 2026-07-28 session, replayed**, not invented
mutations.

| phase | what runs | oracle | negative control (must FAIL) |
|---|---|---|---|
| **V0** (exists) | BIOS boots, CPU reads `ID='MILN'` | the CSR read | tie off the AXI bridge |
| **V1** | the buildroot image boots, the real `S50milan` runs, then assert the provisioned CSR end-state (`entity_model_id` == the flashed config's hash, `CRFT_CTRL` = `0x3`, MAAP claim count = N+1, `AAF_CTRL` bypass clear) and the first ADPDU on the virtual wire carries the shape's counts | the config's generated constants — the same single source `check_entity_shape.py` uses | re-introduce the 1x1 model-id write; the run must go red on the exact defect shipped until 2026-07-28 |
| **V2** | two virtual boards + a TAP; an independent controller stack enumerates both, binds a stream, `hive_compliance.py` runs against a virtual entity | a foreign implementation (L4) | serve a stale AEM ROM against a new model id |
| **V3** | the fast-connect reboot drill: bind, let the journald half write the slots, power-cycle the virtual machine, assert the bind restored (`PRB_W_AVAIL`, E2 read-back) with **zero** controller traffic | Milan v1.2 5.3.8.2 + the persist suite's image taxonomy | corrupt one slot word; the restore count must be ZERO, not partial |

Estimated V1 effort on scaffolding A: **3-5 days**; it buys more
escape-coverage per day than anything else on the tooling column.

## 5. Timers, and where each tool wins

RTL-side protocol timers already scale with the `-G` override discipline
(`CLKV_QTICK_CYC_P`, `DIAG_TICK_CYC_P`, the lwSRP timer bases) — a Verilator
V1 reuses it unchanged. The awkward half is the **Linux daemons**: `ptp4l`
announce intervals, the MRP cadences the kernel side sees, `sleep`-paced init
scripts. Those cannot be `-G`-shrunk, which is exactly where a virtual-time
simulator (option B) wins: the guest's clock is the simulator's, so a 10 s
`valid_time` costs 10 *virtual* seconds. A Verilator-only V1 lives with
wall-clock init (acceptable: `S50milan` is seconds, not minutes) and defers
daemon-timescale scenarios to V2.

## 6. Where it sits in the methodology

A new rung between L3 and L5 — call it **VL5: the wire, on virtual
hardware** — observing the same things L5 observes (frames on a wire, a
booted software stack, flashed-artifact agreement) with the same preference
for an independent oracle, minus everything §2 lists. The normative levels
table in [`methodology.md`](methodology.md) gains the row **when V1 lands and
its negative control has been shown to bite**, not before: a tier that exists
only as a plan must not appear in the table a lane cites when declaring its
coverage.
