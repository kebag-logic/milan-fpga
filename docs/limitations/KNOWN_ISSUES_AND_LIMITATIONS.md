[OBSOLETE + 2026-08-17]

# Known issues & limitations

The single page that makes every error, limitation and hazard apparent.
Three kinds of entries, kept separate: **open limitations** (things that do
not work or do not exist yet), **operational hazards** (things that work but
bite you if mispaired), and **refuted approaches** (things measured and
proven not to help - do not re-try without new evidence). Fixed bugs are not
listed here; their post-mortems live in the [findings log](../findings/README.md)
(§5) and field-level symptom→fix recipes in [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

_Last reconciled against the tree: **2026-08-13** — the control-plane
substitution and its capability boundary are §0 below; the 2026-07-27 pass
carried the media-clock servo, the AX42 MAC-TX guard, the on-chip BRAM PCM-ring
option, the ALSA record and playback paths, the `0x0014` flash and its LPF
prune. A page that is three days behind itself is the one failure this page
cannot afford, so the date is a claim: if you land here after changing what
ships, this line is the thing to re-check._

---

## 0. The capability boundary: the AECP surface, and the losses behind the echo

**Stated once, plainly, at the top, because everything else on this page is
smaller than it.** On 2026-08-13 this repository's own IEEE 1722.1 / SRP control
plane — the AECP/AEM engine, the ACMP talker and listener, the ADP advertiser
and parser, the lwSRP applicant — was **deleted**. The control plane is the
`protocol-processor` submodule, wrapped by
[`hdl/milan/KL_pp_shadow.sv`](../../hdl/milan/KL_pp_shadow.sv) and instantiated
**unconditionally** by
[`hdl/milan/milan_datapath.sv`](../../hdl/milan/milan_datapath.sv). No
parameter, no fallback, no shadow arm. Firmware `VERSION` major stepped to 2.

The device discovers over ADP, connects over ACMP and reserves over SRP. On AECP
it serves the processor's declared command inventory, including
`READ_DESCRIPTOR` and `GET_COUNTERS`. Unsupported commands receive a conformant
fallback response. The processor's AECP uCPU has landed, so
the earlier reading of this page, that the entity answered nothing on AECP, is
**withdrawn**. Concretely:

* **`READ_DESCRIPTOR` (`0x0004`) is answered**, so **controller enumeration is
  reachable again — once the descriptor image is in DRAM, which nothing in this
  repository does for you yet** (the paragraph after this list is the whole of
  that gap, and it is the one to read before planning a bench session).
  `SUCCESS` carries `configuration_index`, the reserved field and the descriptor
  itself; a locate miss answers `NO_SUCH_DESCRIPTOR` and a bad configuration
  index answers `BAD_ARGUMENTS`, both carrying the IEEE 1722.1 §7.4.5 4-byte
  `{descriptor_type, descriptor_index}` stub.
* **Every other opcode, and every other message type** — AEM, ADDRESS_ACCESS,
  vendor-unique MVU — gets a **conformant `NOT_IMPLEMENTED` echo**: correct
  `message_type` + 1, correct length, correct `controller_data_length`. Never
  silence, never a malformed frame.
* **`IDENTIFY_NOTIFICATION` (`0x0026`) arriving as a command answers
  `BAD_ARGUMENTS`** — IEEE 1722.1 §7.4.39.2's opcode-specific rule wins over
  §9.3.5.3.3.
* **Silently refused** — freed, counted, no reply — are a command whose
  `target_entity_id` is not ours, and any AECP *response* arriving as input.
* **Known gap, kept visible rather than smoothed over:** Milan Δ7
  `ACQUIRE_ENTITY` (`NOT_SUPPORTED` with `owner_id` = 0) is **not**
  distinguished from the generic echo. The Δ7 microprogram exists in the uCPU's
  microcode; nothing dispatches to it, so opcode `0x0000` falls into the
  `NOT_IMPLEMENTED` path with everything else.

**The entity model lives in DDR3, and nothing in this repository puts it
there — that is an open limitation, not a footnote.** The descriptor store
fetches the model over a read-only master whose base (`PP_DESC_BASE_P`, surfaced
as the `o_desc_mem_*` / `i_desc_mem_*` port group) is **compile-time**: the
processor holds no base register, so there is nothing to point at the wrong
place at runtime, and nothing to fix at runtime either. Software must write the
image at that base, and the supply chain for it is **missing at three links**:

* the image generator lives in the submodule
  (`protocol-processor/hdl/aecp/desc/gen_desc_image.py`, vendor-neutral JSON in,
  flat image out) — this repository has no step that produces that JSON from an
  `endstation_*.yaml`;
* **no** step in [`sw/builder`](../../sw/builder), [`scripts/`](../../scripts),
  the LiteX SoC builder or the boot path writes an image into DRAM;
* [`sw/builder/endstation_builder.py`](../../sw/builder/endstation_builder.py)
  still emits `aecp_aem_rom.svh`, which is the ROM of the **deleted**
  `KL_aecp_aem_store` — an **orphaned artifact**, not the image the processor
  reads. Do not mistake it for one.

So on a stock build the region is unloaded and **every `READ_DESCRIPTOR` answers
`BAD_ARGUMENTS`** — that is today's default state, not an accident of one
bench. `BAD_ARGUMENTS` rather than `NO_SUCH_DESCRIPTOR` because the microprogram
checks `configuration_index` against `configurations_count` *before* it locates,
and an image marked invalid deliberately reports a count of zero, so no
configuration index passes and the locate never runs. That makes the status a
free diagnostic: **every read answering `BAD_ARGUMENTS` means the image was
never loaded or is corrupt, while a read answering `NO_SUCH_DESCRIPTOR` means
the image is loaded and that descriptor is genuinely absent from the model.**
The refusal is clean either way: an all-zero region fails the image header's magic
(`"AEMI"`, `0x41454D49`) before anything else, the layout version and checksum
back it up, and the store's watchdog (4096 cycles, about 41 µs at 100 MHz,
covering the request handshake too) abandons a stalled burst rather than hanging
the AECP path. A **late load heals without a reset** — every locate against an
invalid image re-arms the header probe — so the ordering rule ("load, then
enable") is a discipline, not a trap you cannot escape. Bench walk-through:
[TROUBLESHOOTING §26](TROUBLESHOOTING.md).

**An echo is not an implementation.** This table separates the live command
surface from the remaining gaps. A `NOT_IMPLEMENTED` answer is protocol
conformance, not coverage, and no clause may be graded on an echo:

| Capability | State |
|---|---|
| READ_DESCRIPTOR | **implemented, protocol processor**: served from the validated DRAM descriptor image |
| The §9.3.5 duty to answer an unimplemented command | **implemented, protocol processor**: conformant `NOT_IMPLEMENTED` fallback, plus `BAD_ARGUMENTS` for IDENTIFY_NOTIFICATION as a command |
| ACQUIRE_ENTITY / LOCK_ENTITY | **implemented**: ACQUIRE_ENTITY returns Milan `NOT_SUPPORTED`; LOCK_ENTITY owns and times out the live lock |
| SET/GET_CONFIGURATION and SET/GET_SAMPLING_RATE | **implemented**; persistence remains open |
| SET/GET_NAME | implemented for all generated semantic names; values are not restored after reboot |
| GET_STREAM_FORMAT / GET_STREAM_INFO | **implemented** |
| SET_STREAM_FORMAT / SET_STREAM_INFO | **implemented** (0x0053): the per-row format verdict and the ACC_LAT presentation offset; the framers do not yet re-shape from a stored format |
| SET/GET_MAX_TRANSIT_TIME | **not implemented** |
| GET_AUDIO_MAP / ADD_AUDIO_MAPPINGS / REMOVE_AUDIO_MAPPINGS | **implemented** for dynamic ports, including atomic validation, lock exclusion, live projection, and successful-change notification |
| GET_COUNTERS | **implemented** for the available counter banks; Table 5.22 change notification coverage remains incomplete |
| GET_AVB_INFO / GET_AS_PATH / GET_MILAN_INFO | **implemented** |
| IDENTIFY | **implemented in protocol state**; the root-level external indication remains open |
| SET_CLOCK_SOURCE | **implemented in protocol state**; the selected value does not yet drive the media clock plane |
| saved-state persistence | **not implemented**: nothing restores mappings or bindings across a power cycle; issue #70 owns the backend and replay |

A controller sees the entity, enumerates the loaded DRAM model, and can use the
served control inventory above. Commands outside that inventory receive a
well-formed command-specific refusal or the generic fallback.

### 0.1 Three functional losses that follow, each with its own consequence

1. **The CRF media clock can never be SELECTED.** AECP `SET_CLOCK_SOURCE` is
   the only writer of the live CLOCK_DOMAIN `clock_source_index` and it is not
   implemented — the command gets the echo — so the index is pinned at 0, the
   **INTERNAL** media clock, for the life of a build.
   Consequence: `KL_mmcm_drp_servo` and the `KL_media_nco` packet-grid servo are
   **structurally off**, and `A_MCSRV_STAT` (`0x8F8`) reads its idle. The CRF
   Media Clock Input engine (`KL_crf_rx`) still parses, counts and reports — it
   simply cannot steer anything. This supersedes the "both knobs are
   bench-gated" row in §1: the knobs are moot on a build whose servo is never
   engaged.
2. **Presentation-time offset is pinned at the Milan 2 ms DEFAULT** for every
   Stream Output, because `SET_MAX_TRANSIT_TIME` is not implemented (nor is
   `SET_STREAM_INFO`'s `MSRP_ACC_LAT` leg). That is a **default, not a zero** —
   0 ns would be a presentation time in the past and every listener would drop
   every frame as late. The streams still work; the offset is simply not
   tunable.
3. **The Milan Table 5.4 per-STREAM_OUTPUT diagnostic counters are live for
   solicited reads.** `KL_talker_diag_ctx` is instantiated per declared AAF
   output and for CRF. GET_COUNTERS serves all five counters. The Table 5.22
   unsolicited change producer remains open. **The STREAM_INPUT counters at
   the `0x6B8` `A_STRMW_CNT` window remain live too.**

### 0.2 A whole class of CSR words now reads a structural zero

No register was removed — the register map is an ABI — but a word whose source
is deleted must read a **structural zero**, and is documented as such. That
means **"the counter reads 0" no longer means "nothing happened"**: for a good
number of words it means "there is no longer anything behind this". The
per-word verdicts, word by word, are in
[`docs/reference/REGISTER_MAP.md`](../reference/REGISTER_MAP.md); they are not
restated here. Two shapes to know before reading any of them:

* Some words in a mostly-dead group are **still live**, so the group cannot be
  dismissed wholesale — `A_ADP` `available_index`, ACMP `talker_active`, the
  listener group's `bound`/`active`/CRF-sink bits, and the lwSRP domain word,
  granted slope and over-limit bit are all published by the processor.
* Some words are **write-only scratch**: they read back what software wrote and
  the value **no longer reaches the wire**. Writing them changes nothing
  observable.
* [TROUBLESHOOTING §24](TROUBLESHOOTING.md) is the field entry for diagnosing
  against them, and §25 there carries the `A_TXARB_DIAG` lane renumbering, which
  is the trap most likely to produce a confident wrong reading.

### 0.3 One behaviour that changed and is NOT a limitation — the CBS slope edges

Recorded here so it is not re-discovered as a defect. The deleted
`KL_lwsrp_bw_gate` joined a stream's idleSlope into the running sum **before**
opening its gate, and closed the gate **before** removing the slope. The
processor asserts `srp_active_o` and `srp_granted_slope_bps_o` in the **same**
cycle. On the opening edge that is at worst equal, never worse; on the closing
edge the sum is briefly high for zero traffic — conservative, not permissive.
**Neither edge lets a stream transmit against an un-budgeted slope**, which is
the property that mattered.

---

## Contents

- **[0. The capability boundary: the AECP surface, and the losses behind the echo](#0-the-capability-boundary-the-aecp-surface-and-the-losses-behind-the-echo)** -- The protocol processor owns ADP, ACMP, SRP and the served AECP inventory. The descriptor-image supply chain, Table 5.22 producer and ACQUIRE_ENTITY semantics remain visible gaps. Solicited Stream Output counters are live.
- **[1. Scope limitations (by design, current state)](#1-scope-limitations-by-design-current-state)** -- What is deliberately absent or simply not built yet: one port, MTU pinned at 1500, no descriptor-image supply chain (so the entity model never reaches DRAM and a stock build enumerates nothing), no MDIO master anywhere in fabric (`MAC_STATUS` is software-published and reports its reset default until a driver writes it), and two media-clock servo knobs still gated on a bench answer. §1.1 inside is the open-blocker list: the AX42 MAC-TX wedge, whose *recovery* is explicitly NOT silicon-proven, the playback path that has never been flashed, and the 1-in-24 DRAM-ring read artifact -- plus the fabric-listener blocker, now CLOSED.
- **[2. Build & reproducibility gaps](#2-build--reproducibility-gaps)** -- The ways a correct-looking build is wrong. Includes: CI runs every paper and RTL gate but nothing on hardware; the CPU default is not the shipped config and L2 is per board; omitting `--coherent-dma` builds a NIC that silently drops all RX; and the shipping `0x0014` build prunes the render low-pass, which quietly invalidates the analog loop record measured through it.
- **[3. Timing & clocking constraints](#3-timing--clocking-constraints)** -- Three constraints that survive any port: the CBS slope divide is the 100 MHz critical path (hence the multicycle, or the datapath's own 50 MHz domain), 112.5 MHz was built and reverted on reset fanout, and `--gtx-tx-invert` is mandatory on the AX7101 or 25–40 % of TX frames corrupt.
- **[4. Operational hazards - lethal pairings (gateware ⇄ driver)](#4-operational-hazards---lethal-pairings-gateware--driver)** -- Combinations that work individually and are fatal together, each with its guard: header-split page-size mismatch panics the kernel, RX-queue count is now per board and the wrong one shifts every DMA window under an unchanged DTB, and an armed `t > 0` talker with the lwSRP engine off blasts ~56 k frames/s unpaced because the reservation gate *is* the pacer.
- **[5. Refuted performance levers (measured; do not rebuild without new evidence)](#5-refuted-performance-levers-measured-do-not-rebuild-without-new-evidence)** -- Six levers built or modelled, measured on silicon, and rejected -- TX reader prefetch, a second core, coalescing sweeps, 112.5 MHz, bigger L2/scratchpad/prefetch, and socket zero-copy RX. Read before proposing any of them again.
- **[6. Performance: where the numbers actually live](#6-performance-where-the-numbers-actually-live)** -- The precedence rule for the conflicting throughput figures scattered across the corpus: the ledger and the campaign record win, prose snapshots lose. Audio gets its own rule at the end, and it is the sharper one -- every analog figure names the filter it was measured through, because the shipping build prunes that filter.
- **[7. Legacy collateral that can mislead](#7-legacy-collateral-that-can-mislead)** -- Files still in the tree that describe a system we no longer build: the xsim-era testbenches, an unused RGMII PHY experiment on a GMII board, and the Zynq variant whose `0x43C0_0000`/IRQ_F2P mechanics leak into other docs.

## 1. Scope limitations (by design, current state)

| Limitation | Detail |
|---|---|
| **Single endpoint port** | One MAC/PHY today; the 4-port AVB switch is direction, not implementation ([../overview/AVB_SWITCH_DIRECTION.md](../overview/AVB_SWITCH_DIRECTION.md)) |
| **MTU fixed at 1500** | A deliberate decision of the switch direction doc; no jumbo support |
| **802.1 standards gaps** | The normative gap analysis (~60 items: SRP/MSRP, full gPTP stack, MVRP, …) is [`REQUIREMENTS.md`](../../REQUIREMENTS.md) §3 - read it before claiming Milan conformance. [../reference/MILAN_V12_DEPENDENCY_MATRIX.md](../reference/MILAN_V12_DEPENDENCY_MATRIX.md) traces what is covered |
| **MDIO not fabric-driven — `MAC_STATUS` is SOFTWARE-published** | There is no hardware MDIO master anywhere in the design. LiteEth's `LiteEthPHYGMII`/`LiteEthPHYMII` expose **no** link, speed or duplex output — only `LiteEthPHYMDIO`, a software bit-bang register pair at the DT `phy` window (`0xf000_3800`, 0xc bytes). Since 2026-07-26 `milan_soc.py` no longer hardwires `i_link_up`/`i_full_duplex`/`i_mac_speed`: they come from the `milan_mac_link_status` CSR (`0xf000_381c`, fields `link_up[0] speed[2:1] full_duplex[3]`, reset = the old per-board constants), so software that reads the PHY over MDIO can publish the truth into `MAC_STATUS` 0x110 and into `o_mac_is_1g` (REQ-MAC-03). **Until the driver writes it, the register still reports its reset default** — that half needs `kl-eth` phylib work, and a fabric MDIO poller (new SystemVerilog) would be needed to make it hardware-driven | 
| **The external AEM image handoff is explicit, not automatic for custom flows** | `READ_DESCRIPTOR` serves a flat DRAM image. An explicit builder deployment transfer (`--write-fragment` or `--write-rtl`) now generates `aem_desc.bin`, its paired manifest/map and loader payload in the sibling rootfs overlay; tracked `S50milan` invokes `aemi-load` before identity programming and entity enable. The loader validates the manifest/window pairing, AEMI magic and firmware version and verifies DRAM readback. An ordinary builder inspection deliberately does not mutate the overlay, and a custom boot flow that omits the transfer/load receives `BAD_ARGUMENTS` until a valid image is supplied; a late valid load heals without gateware reset. [ENDSTATION_BUILDER.md](../ENDSTATION_BUILDER.md) owns the current contract and [TROUBLESHOOTING §26](TROUBLESHOOTING.md) owns the bench diagnosis |
| **Open CBS requirements** | REQ-CBS-05/06/07 (credit-skew/pacing refinements) are open in [`REQUIREMENTS.md`](../../REQUIREMENTS.md) |
| **Latent CBS slope truncation** | The CBS slope divide truncates: zero error only while configured slopes divide evenly (today's do). Documented in the CBS math section of [`REQUIREMENTS.md`](../../REQUIREMENTS.md) - re-check before exotic `tc cbs` configs |
| **Media-clock servo: both knobs are BENCH-GATED, not settled** (2026-07-23) — **and since 2026-08-13 the servo is structurally off in every build** (§0.1), so neither knob is reachable: with `SET_CLOCK_SOURCE` unimplemented the clock source index is pinned at 0 and `A_MCSRV_STAT` reads its idle. The row below is the last state of a loop that is no longer engaged | The MMCM-DRP servo (`KL_mmcm_drp_servo`, `MCSRV_STAT`/`MCSRV_CTRL` at `0x8F8`/`0x8FC`) is silicon-proven as a loop — the coherent chain measured **−83.9 dB THD+N, the converter floor** — but neither `MCSRV_CTRL` bit is a settled default. `[0]` **`ps_invert`** exists because mf51 silicon stepped the fine phase shift *opposite* the UG472 reading and the rails went 25× worse under the servo; the winning polarity has not been baked into the RTL. `[1]` **`auto_repair`** defaults **0** = verify-only, so a CLKOUT0 divider mismatch is *reported*, never repaired. Both are open rows in [`../design/TIME_SYNC.md`](../design/TIME_SYNC.md) §5 |
| **Optional datapath blocks can be pruned, and a pruned block's RO words read a STRUCTURAL zero** | Six `milan_datapath` blocks sit behind elaboration-time prune parameters ([`../design/AREA_BUDGET.md`](../design/AREA_BUDGET.md) tier 1). All default to PRESENT, but a build that pulls a lever keeps the *register window* while the block behind it is gone — so at `0x8F8` you cannot distinguish "no servo built" from "servo idle", and at `0x870` "no taps built" from "taps never armed". **There is deliberately no capability bit** (adding one would be a CSR contract change owing a `VERSION` bump). Read the build plan, not the register — [`../reference/REGISTER_MAP.md`](../reference/REGISTER_MAP.md) "A group can be STRUCTURALLY absent". **Since 2026-08-13 the same reading problem applies to a second, larger set of words that is NOT prune-controlled** (§0.2): their source RTL is deleted outright, so they read a structural zero in every build |

### 1.1 Silicon blockers

| Blocker | State | Evidence / next step |
|---|---|---|
| **MAC-TX wedge on link bounce (AX42): recovery is UNPROVEN** | **OPEN.** The *logic fix* landed and is genuinely wired on the deployed board (the guard's `eth_rst` reaches the `eth_tx`/gtx domain — netlist extract in the finding). The *guard FSM* is silicon-proven: detect → `eth_rst` → HOLD → back to RUN in ~2 s, every induced cycle, `RST_EPOCH` never moving, and — not trivial — asserting `eth_rst` does **not** itself break TX. **What is not proven is the thing the fix is for.** | **Do not read this as validated.** [`../findings/STRESS_0726.md`](../findings/STRESS_0726.md) §H carries a **2026-07-27 CORRECTION** retracting an earlier "validated on silicon" claim: the control experiment ran the same drill with the guard *disabled* and TX kept ticking for 24 s, so `LINK_CTRL[3] linkg_freeze` only forces the guard's **liveness indicators** low — it never stops the eth clock, and **no wedge was ever induced**. Closing this needs a **physical cable pull** or a managed switch port. Also: do not quote a drill cycle count from that page (8 vs 9, no raw log kept) |
| **Playback path (`KL_pcm_tx` → DAC) has never been on silicon** | **OPEN — TB-proven only.** The fabric chain is continuous and closed in RTL (`VERSION 0x000E`): host ring → render crossbar → `KL_i2s_feed_mux` picks both the DAC source *and* its 48 kHz pace, so a playback ring reaches the line-out with no inbound stream. [`tb/verilator/pcm_playback`](../../tb/verilator/pcm_playback) decodes the serialized DAC pin back with a spec-derived I2S receiver: 40/40, 41 consecutive ring words bit-exact, plus under-run / over-run / disarmed-map / mid-stream-channel-count negatives | Nothing past the RTL is established: **no board has been flashed with this gateware and no ALSA sink drives it** ([`../design/AUDIO_STREAMING.md`](../design/AUDIO_STREAMING.md) §6). The *record* direction is the one that is silicon-proven — see §6 below |
| **DRAM PCM-ring read artifact (I6)** | **OPEN.** Two silicon failure classes on the DRAM ring path: the real-time writer **sheds a beat under CPU DRAM contention** (mitigated by the CDC depth 16 → 128 fix, not killed at root), and **I6**, a **1-in-24 read artifact that survives CDC-128** — write-posting versus OFFSET-CSR ambiguity, still open ([`../MILAN_COMPLIANCE_GAPS.md`](../MILAN_COMPLIANCE_GAPS.md) §2) | `--pcm-ring bram` (`KL_pcm_ring_bram.sv`) kills **both at the root** — always-ready write port, no DRAM controller or posting between writer and reader — at ~8 RAMB36 for 32 KB, with the driver unchanged. **DRAM remains the default**, so the artifact is live in a shipping build ([`../design/AUDIO_STREAMING.md`](../design/AUDIO_STREAMING.md) §3.4) |
| **Fabric listener never accepts on the 8×8 AX gateware** | **CLOSED 2026-07-26** — root-caused, fixed in RTL (`VERSION 0x0001_000F`, and in every build since), mechanism confirmed on silicon | The cause was **entry-0 provisioning, not the parser and not a placement artifact**: `win_commit_glue` staged the `0x800` window's `SID_LO`/`SID_HI` in one global register pair shared by every index, so a route-flags-only `CTRL` write at index 0 armed entry 0 with another index's sid; `KL_stream_table` then set `ovr_armed_r[idx]` on any write and cleared it only on reset, so entry 0 never returned to the ACMP alias. The fix tags staging with the index it was staged for and makes `{en=0, sid=0}` a **release-to-alias**. Confirmed on silicon by **causation** — the trap was triggered on purpose and the listener went deaf, then recovered by re-staging ([findings/STRESS_0726.md](../findings/STRESS_0726.md) §D, tests D0/D1/D2). Regression guards: [`tb/verilator/milan_dp`](../../tb/verilator/milan_dp) `sim_nxn.cpp` TRAP-1 (N=4 and N=8) and [`tb/verilator/avtp_parser`](../../tb/verilator/avtp_parser) `sim_tbl.cpp` T6, both with negative legs. Full walk: [TROUBLESHOOTING §21](TROUBLESHOOTING.md) |

> The silicon confirmation was obtained on a board still carrying the **pre-fix**
> `VERSION 0x0001_000B` — it proves the *mechanism*, and the *fix* is proven in
> simulation by the two regression guards above. A board that has not been
> reflashed past `0x000F` still needs the workaround (stage the sid at index 0
> before committing `CTRL`).

## 2. Build & reproducibility gaps

| Gap | Impact | Workaround |
|---|---|---|
| **CI runs everything except hardware** (2026-07-26) | GitHub Actions runs the paper gates in [`docs.yml`](../../.github/workflows/docs.yml) (docs gate — links, wording, dead references, local info — twice, the second time with `.git` deleted; the traceability no-drift gate; the end-station builder gates) **and the RTL gates** in [`rtl.yml`](../../.github/workflows/rtl.yml): the full Verilator sweep via [`scripts/run_all_suites.sh`](../../scripts/run_all_suites.sh), the Yosys portability sweep, and the BDD conformance suite. **Nothing on hardware runs automatically** — silicon regressions are still caught by discipline | run the [TESTING.md](../testing/TESTING.md) layers before pushing; [`../../QUICKSTART.md`](../../QUICKSTART.md) §2 has the exact local commands |
| **No version pins** | No requirements.txt / lockfile; [`sw/litex/patches`](../../sw/litex/patches) are diffed against LiteX `master` and can stop applying | known-good LiteX: `a1e1c36` (recorded in [`sw/litex/evidence/hw_naxriscv_reads_MILN.log`](../../sw/litex/evidence/hw_naxriscv_reads_MILN.log)); re-diff per `patches/README.md` |
| **CPU default ≠ published config** | `milan_soc.py --cpu` defaults to `naxriscv` and `deploy.sh` does not override it, while the **shipped config is 1-hart VexiiRiscv** — `sweep.sh` passes `--cpu vexiiriscv` explicitly and [`sw/builder`](../../sw/builder) defaults to it. L2 is **per board**, not one number: `L2=16384` for ax7101 (the 8×8 shape that closed) and `L2=65536` for arty. (The dual-hart `--cpu-count 2` scoreboard was a superseded perf-lineage variant.) NaxRiscv is the *historical* core throughout the corpus — hence the framing banner on [`../integration/AXIS_CORES_ON_NAXRISCV.md`](../integration/AXIS_CORES_ON_NAXRISCV.md), whose filename still names it | see [../litex/LITEX_SOC.md](../litex/LITEX_SOC.md) §2.5 |
| **`--coherent-dma` not implied by `--all-blocks`** | Omitting it builds a NIC that silently drops all RX and TXes garbage (DMA bypasses the snooping bus) | always pass it (deploy.sh does); hardware-confirmed 2026-07-04 |
| **`external` submodule is SSH-only** | anonymous `git clone --recurse-submodules` fails on it | it is **not needed** - init only [`third_party/verilog-axis`](../../third_party/verilog-axis) |
| **Driver out of tree** | the `kl-eth` Linux driver lives in the sibling repo `kl-linux-drivers`; no kernel-version pin is documented | contract in the retired driver record |
| **DT `phy-mode` `rgmii-id` in the retired binding toolkit — RESOLVED by retirement (2026-07-26)** | the retired AX7101 board input + `milan-nic.litex.dtsi` carry `rgmii-id` on a GMII-wired board ([BOARD_PORTING_AX7101 §3](../integration/BOARD_PORTING_AX7101.md)). Those files are now **historical artifacts**: the shipping node comes from [`sw/builder/endstation_builder.py`](../../sw/builder/endstation_builder.py), which emits `phy-mode = "gmii"` / `"mii"` from the config and byte-matches both deployed `.dts` files | nothing to do; do not deploy `sw/dts/milan-nic.*.dtsi` |
| ~~**`build.sh cfg_ax8x8` L2 ≠ the 8x8 config's L2**~~ | **CLOSED 2026-07-27** — the real fix was taken: [`configs/endstation_ax7101_8x8.yaml`](../../configs/endstation_ax7101_8x8.yaml) now declares `l2_bytes: 16384` (the 8-stream shape closed at 16K, not 32K) and `sweep.sh` carries `L2=16384` for ax7101, so config and sweep agree on the combination that was actually placed and routed | nothing to do; `test_builder.py` gate 9 and [`scripts/check_sweep_shape.py`](../../scripts/check_sweep_shape.py) fail if either side moves again |
| **The `0x0014` build PRUNES the render low-pass, which invalidates the analog record** (2026-07-27) | `sweep.sh ax7101` passes `--no-render-lpf` (`LPF_P = 0`) — a banked area lever spent on the board that had missed placement by 282 slices. The pruned datapath behaves exactly as `LPF_CTRL[0] = 0` does today, so this is not a functional regression. **But the −147.99 dBFS loop THD+N figure was measured *through* `KL_pcm_lpf`** and does not carry over to this bitstream | do not quote the analog loop record against a `LPF_P = 0` build until it is re-measured; the digital acceptance measurements are all taken upstream of the filter and are unaffected ([`../findings/FLASH_0x0014_0727.md`](../findings/FLASH_0x0014_0727.md) "Honest limits", [`../design/AREA_BUDGET.md`](../design/AREA_BUDGET.md)) |
| ~~**`avtp_stream_parser` portability unchecked**~~ | **CLOSED** — it is a top in [`syn/yosys/run.sh`](../../syn/yosys/run.sh) `tops=()` and is swept on every portability run | nothing to do |

## 3. Timing & clocking constraints

* **The CBS slope divide is the 100 MHz critical path.** The build only
  closes with the multicycle constraint that `add_milan_datapath()` emits
  (or with the datapath in its own slower domain, `--milan-clk-freq 50e6`,
  which is what `deploy.sh` ships). Porting to another toolchain? Re-express
  it: [../integration/PORTING_GUIDE.md](../integration/PORTING_GUIDE.md) §4.5.
* **112.5 MHz sys was built, measured, and reverted** - reset-fanout timing
  (`sys_rst` replication proved impossible - DONT_TOUCH); see
  [../findings/LATENCY_INVESTIGATION.md](../findings/LATENCY_INVESTIGATION.md).
  DDR3 pins sys at 100 MHz.
* **`--gtx-tx-invert` is required on the AX7101** - edge-aligned GMII TX
  launch is hold-marginal at the RTL8211E (25-40 % corrupt frames without
  it). Other boards must re-evaluate TX clock phase.
* **VERSION `0x0002_0055` defaults to fabric-owned clock validity; no daemon
  lease is required.** The integrated `gptp-processor` publishes sync,
  asCapable, GM identity and discontinuity coherently, and
  `KL_ptp_clock_validity` drives AVTP `tu` from that selected-owner bank.
  Software writes to `CLKV_CTRL` cannot forge live health in this build.
  `CLKV_STAT[1]` is the engine sync verdict, `[16]` is engine asCapable, and
  the compatibility-only no-lease bit `[2]` and lease count `[15:4]` are
  structural zero. Focused `gptp_shadow`, `clkvalid`, `milan_dp` and CSR tests
  cover that wiring and the option-off arm; integrated booted/two-board
  physical acceptance of the default owner remains #117. The talker does not
  stop on uncertainty: Milan v1.2 5.3.7.3 forbids that.

  **Historical VERSION `0x0001_0016` and explicit option-off evidence.** The
  fail-open defect before `0x0016` sent 31 M frames from a PHC 60 h off the
  domain while claiming `tu = 0`
  (the retired reference-listener sweep of 2026-07-27 (#259, in git history)).
  The first fail-closed lease build was also only half a deployment: with both
  boards at `0x0001_0016` and no writer, `CLKV_STAT` was `0x00000005` on the
  ALINX and Arty and `CLKV_TUCNT` climbed at exactly **1.00/s since boot**,
  although the ALINX was a healthy grandmaster and the Arty was `SLAVE` at
  **-93 ns**. Leaving `tu` asserted on a stable clock is itself a conformance
  failure: IEEE 1722-2016 PICS **AAF-10** (`AAF:M`) requires `tu = 0` when
  gPTP time is stable, and Milan v1.2 4.4.2.3 has a Listener PAAD leave
  free-wheel after `tu` resets. The bench repo's `gptp2csr.sh` lease and its
  decision/renewal oracles remain the compatibility solution.

  **Deployment caveat applies only to `fabric_gptp: false`.** That explicit
  comparison build still relies on the board image's `gptp2csr.sh`; an image
  predating the 2026-07-28 lease update can remain at `tu = 1`. In a synced
  option-off deployment, check `devmem 0x9000077C` for bit 1 set and bit 2
  clear, rather than the historical `0x5`. Do not use this historical silicon
  result as acceptance evidence for the `0x0055` default owner.

## 4. Operational hazards - lethal pairings (gateware ⇄ driver)

The header-split / BD-format features couple gateware and driver builds.
These pairings are **known-fatal**:

| Pairing | Consequence | Guard |
|---|---|---|
| driver `--hs-page-bytes` ≠ gateware `hs_page_bytes` | **kernel panic** (Bad page map class) | `milan_dma_hs_pgsz_cap` reads back the elaborated size (`0xf000311c` in the reference build — LiteX assigns CSR offsets at build time, so confirm against your build's `csr.csv`); the hsplit16 driver **refuses to load** on mismatch. Reads 0 on older gateware = warn-and-trust |
| hsplit10+ driver on ≤hsq5 gateware | **silent ring lap** (by construction, no error) | never load it there - see [../findings/RX_PERF_TUNING_MAP.md](../findings/RX_PERF_TUNING_MAP.md) |
| BD-256 ring depth without the hsq6 drain gate | RX wedge under overload | use hsq6+ gateware ([../findings/RX_OVERLOAD_WEDGE.md (archived)](../../historical_now_obsolete/findings/RX_OVERLOAD_WEDGE.md) history) |
| **RX-queue count differs PER BOARD** (2026-07-26) | the queue count sets the DMA window map: the shipping ax7101 gateware is **1 queue** (no `rx1_*`/steer registers in its `csr.csv`), the deployed arty is **2**. Building either with the other's count shifts every DMA window under an unchanged DTB — the CSR-rot failure of [TROUBLESHOOTING §20](TROUBLESHOOTING.md), silent until the host plane is dead | `rx_queues` lives in each board's `configs/endstation_*.yaml` and flows into `sweep.sh` as `RXQ`; builder gate 9 asserts config ⇄ sweep agreement per board. Change it only together with a full boot-chain rebuild for that board |
| **Extra talker (`t > 0`) armed while the SRP engine is OFF** (2026-07-26; **still live 2026-08-13**) | the admitted stream transmits **unpaced** — the reservation gate *is* the pacer. Measured ~56 k frames/s from one context; the peer board's 50 MHz core drowns in the interrupt storm and stops answering the network until the talker is disarmed. The hazard survived the control-plane substitution unchanged in shape: `LWSRP_CTRL[0]` (`cfg_lwsrp_enable`) is still the escape hatch, and `~cfg_lwsrp_enable` still bypasses the gate. What changed is who drives the gate — it is now the processor's class-D admitted vector, not the deleted `KL_lwsrp_bw_gate` | never leave `LWSRP_CTRL[0] = 0` with an armed `t > 0` context; arm extras only with the engine running ([TROUBLESHOOTING §22](TROUBLESHOOTING.md)) |
| **`t > 0` context (`TCTX`) window writes while the engine is OFF** (2026-07-26) | writes are **silently dropped** (provisioning-commit coupling holds `wr_rdy` low) — the arm looks done and is not | arm/disarm `t > 0` with the engine ON, and take the arm truth from a snapped `A_STRMW_STATE 0x82C[3]` (composed admission), never from the write itself |

STRICT-pairing rules and the current compatibility ledger:
[../findings/RX_PERF_TUNING_MAP.md](../findings/RX_PERF_TUNING_MAP.md) and
[../findings/BENCH_TOPOLOGY.md](../findings/BENCH_TOPOLOGY.md) (which gateware/rootfs
pair is on which board).

## 5. Refuted performance levers (measured; do not rebuild without new evidence)

Each was implemented or modeled, **measured on silicon**, and rejected -
the write-ups explain why, so the next person doesn't re-spend the effort:

| Lever | Verdict | Where |
|---|---|---|
| TX reader prefetch | "MEASURED VERDICT: do not build it" | [../findings/TX_READER_PREFETCH_PLAN.md (archived)](../../historical_now_obsolete/findings/TX_READER_PREFETCH_PLAN.md) |
| Second core for single-flow throughput | single flow is latency-bound, not CPU-bound; SMP helps multi-flow TX instead | [../findings/LATENCY_INVESTIGATION.md](../findings/LATENCY_INVESTIGATION.md) §2.1 |
| Interrupt-coalescing sweeps for single-flow RX | `rx-usecs` 5 µs→1 ms flat | [../findings/LATENCY_INVESTIGATION.md](../findings/LATENCY_INVESTIGATION.md) §2/§2.1 |
| 112.5 MHz sys clock | built + measured, reverted (reset fanout) | [../findings/LATENCY_INVESTIGATION.md](../findings/LATENCY_INVESTIGATION.md) |
| L2 > 64 KB, BRAM scratchpad, software prefetch (blocking D$) | no measured gain on this core | campaign ledger: [`CHANGELOG.md`](../../CHANGELOG.md), [../findings/PERFORMANCE_GOAL.md](../findings/PERFORMANCE_GOAL.md) |
| Socket zero-copy RX (TCP_ZEROCOPY_RECEIVE) on this core+kernel | 110-113 Mbit at 87 % zero-copied - equilibrium economics refute the lane; AF_XDP ZC remains the open >500 lane | [../findings/PERFORMANCE_GOAL.md](../findings/PERFORMANCE_GOAL.md), [../findings/RX_PERF_TUNING_MAP.md](../findings/RX_PERF_TUNING_MAP.md) |

## 6. Performance: where the numbers actually live

Historical docs quote different RX/TX figures because each is a **dated
measurement** of a moving system (and several older docs carry superseded
banners). The rules:

* The per-lever measured ledger is [`CHANGELOG.md`](../../CHANGELOG.md).
* The consolidated campaign record is [../findings/PERFORMANCE_GOAL.md](../findings/PERFORMANCE_GOAL.md)
  (it carries the no-copy RX ceiling re-baseline); the newest *board* state — which
  gateware and rootfs each board is actually running — is
  [../findings/BENCH_TOPOLOGY.md](../findings/BENCH_TOPOLOGY.md).
* Any number embedded elsewhere (including the root README) is a snapshot
  with a date - trust the ledger over prose.

**Audio numbers are a separate ledger with a separate rule.** The **record**
direction (listener → ALSA) is the one proven on silicon: end-to-end
capture→render equals the presentation offset (pto 500 µs, 0 LATE), talker wire
output bit-exact against the tone table (900/900), a full board→board→PipeWire→board
loop at −72.7 dB THD+N, and a 5 s capture at −147.99 dBFS THD+N with 0 periodicity
mismatches in 239,952 comparisons. The playback direction is **TB-only** (§1.1).
The rule: **every analog figure names the filter it was measured through.** The
−147.99 dBFS record was taken through `KL_pcm_lpf`, which the shipping `0x0014`
ax7101 build prunes — see the `LPF_P` row in §2 before quoting it. The digital
measurements are taken upstream of the filter and carry over unchanged.
Sources: [../findings/STRESS_0726.md](../findings/STRESS_0726.md) §I,
[../design/AUDIO_STREAMING.md](../design/AUDIO_STREAMING.md) §6.

## 7. Legacy collateral that can mislead

* [`tb/utests/`](../../tb/utests), [`tb/itests/`](../../tb/itests) - Vivado-xsim era, partly stale interfaces
  ([../testing/TESTING.md](../testing/TESTING.md) §5).
* [`sw/litex/milan_rgmii.py`](../../sw/litex/milan_rgmii.py) - unused legacy RGMII PHY experiment; the board
  is GMII.
* `milan_top.sv` + `bd/` + `constraints/*.xdc` - the Zynq-7020 variant,
  maintained but not the primary target; [`REQUIREMENTS.md`](../../REQUIREMENTS.md)/[`TODO.md`](../../TODO.md) still
  describe some Zynq-era mechanics (`0x43C0_0000`, IRQ_F2P) that only apply
  there. It is also **archived and unbuildable**, and it still wires the AECP
  top that no longer exists.
* **Anything in this corpus that describes an in-fabric AECP/AEM engine, an ADP
  advertiser, an ACMP responder or the lwSRP applicant as *ours*.** Those pages
  described a system deleted on 2026-08-13. The design records for them were
  retired with the RTL; git history keeps all of it. Where a page still carries
  such a description, the tree wins — `hdl/milan/KL_pp_shadow.sv`'s banner and
  `hdl/milan/milan_datapath.sv`'s banner are the authoritative RTL statements,
  and §0 above is the authoritative capability statement.
