# README-parameters — endstation builder (`sw/builder/`)

<!-- gaps attack item 4: the software-defined End-Station generator.
     Documents the config schema knobs the builder owns, the hash-derived
     entity_model_id recipe, and the sweep.sh single-source contract.
     Companion of the per-module README-parameters.md files
     (docs/templates/README-parameters.template.md). -->

- Module(s): `sw/builder/endstation_builder.py` (generator),
  `avdecc/gen_aemi_image.py` plus the processor descriptor-image packer,
  `sw/litex/sweep.sh` (sweep-opts consumer),
  `hdl/ieee8021q/srp/` + `hdl/common/csr/milan_csr.sv` (lwSRP-table
  gate-comparison targets), `kl-eth` / `snd-kl-milan` (DT consumers).
- Configs: `configs/endstation_*.yaml`
  (schema `kebag-logic/milan-endstation-config` 1.1.x; the annotated
  normative form is `configs/endstation_arty_current.yaml`).
- Gate: `python3 sw/builder/test_builder.py` (17 numbered gates + the 18/19
  emitter families, incl. the ROM byte-identity no-regression gate, the
  Milan 7.2.3 CRF-output rule, the lwSRP↔RTL constant cross-check and the
  CSR-rot `boot_chain_pin` refusal).

The dynamic-map command and persistence claims are checked against the
[Milan feature status ledger](../../docs/reference/MILAN_FEATURE_STATUS.md):

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `aem.served-command-set` | `implemented` | - |
| `soc.baremetal-profile` | `implemented` | - |
| `host.sound-card-option` | `implemented` | - |
| `state.nonvolatile-persistence` | `missing` | - |
<!-- milan-feature-status:end -->

## Contents

- **[Pipeline](#pipeline)** -- One diagram: one YAML config in, and every artifact it fans out to -- SoC argv, AEM overlay, lwSRP table, platform shape, the DT fragment and the sweep-opts shell fragment. Start here to see which generated file you actually care about.
- **[SoC software profile (soc:)](#soc-software-profile-soc)** -- Selects Linux bring-up or the shipping cacheless RV32I bare-metal contract; invalid CPU, cache and flash combinations are refused before SoC generation.
- **[lwSRP reservation table (srp:, CSR 0x680)](#lwsrp-reservation-table-srp-csr-0x680)** -- Every `srp:` knob with its default chosen so a config *without* the section emits the deployed gateware bit-for-bit. Two things worth the read: the TSpec derivation showing `MaxFrameSize + 42` is exactly the wire slot (so the deployed pinned 224 over-reserves ~2.3× for a stereo talker), and the attribute-context shortfall this emitter surfaced -- an 8×8 shape needs 15 lwSRP rows and gets 8.
- **[Platform shape (platform:) -- device tree + driver-visible layout](#platform-shape-platform----device-tree--driver-visible-layout)** -- Explains how RX queues determine the DMA window map, how the generated device tree and driver ABI stay paired, and how the boot-chain pin rejects address drift.
- **[Optional blocks (board.features:) -- product options and tier-1 prunes](#optional-blocks-boardfeatures----product-options-and-tier-1-prunes)** -- The sound-card and fabric-gPTP product switches, six elaboration-time area levers, their emitted flags and the measurements each prune invalidates.
- **[Schema 1.1 deltas (vs the 1.0 scaffold)](#schema-11-deltas-vs-the-10-scaffold)** -- The nine fields 1.1 added or changed, including `model_id_pin` (which wins over everything and is what protects already-flashed silicon), the two cluster-mapping policies, and the enforced Milan 7.2.3 rule: ≥2 AAF listener streams without a CRF output is a hard rejection.
- **[entity_model_id: hash-derived recipe (normative)](#entity_model_id-hash-derived-recipe-normative)** -- The exact recipe -- which fields enter the shape, the canonical JSON encoding, and the sha256 fold under the OUI. The design point is at the end: two boards with the same audio shape share one model id, because names and serials are deliberately excluded.
- **[Per-stream STREAM_PORT layout (overlay 2.x)](#per-stream-stream_port-layout-overlay-2x)** -- The rule that determines every descriptor count in an NxN overlay: one stream port per stream, one contiguous cluster block, exactly one audio map with port-relative rows -- unless the port is `map_mode: dynamic`, which carries none.
- **[sweep.sh single-source contract](#sweepsh-single-source-contract)** -- What the generated `sweep_opts_<board>.sh` fragment contains, that `sweep.sh` falls back to inline tables only when it is absent, and the gate that asserts the two agree byte-for-byte.
- **[gen_aem_store consumption + current limits](#gen_aem_store-consumption--current-limits)** -- How overlay descriptor bytes are packed into the processor's `aem_desc.bin` image, paired with its manifest and map, loaded into DRAM, and consumed for NxN enumeration. Also records the open nonvolatile replay gap.
- **[Resource estimator (approximate, pre-Vivado)](#resource-estimator-approximate-pre-vivado)** -- How the pre-Vivado area estimate is built and how much to trust it: costs calibrated from a real place report, four confidence labels (config-scaling rows are explicitly UPPER BOUND because the NxN engines do not exist yet), and a ±15 % calibration gate currently landing within 0.21 %. The payoff line: 4×4 comes out ~108 % and 8×8 ~142 % of the xc7a100t -- known before burning a sweep.

## Pipeline

```
configs/endstation_<x>.yaml
   └─ endstation_builder.py
        ├─ out/<x>/soc_params.json      milan_soc.py DESIGN argv
        ├─ out/<x>/aem_overlay.json     kebag-logic/aem-overlay 2.x
        │     └─ gen_aemi_image.py + processor descriptor-image packer
        │            └─ aem_desc.bin / aem_desc.json / aem_desc.map
        ├─ out/<x>/lwsrp_table.{json,svh}   kebag-logic/lwsrp-table 1.x
        │     └─ gate-compared against lwsrp_pkg.sv + milan_csr.sv
        ├─ out/<x>/platform_shape.json      kebag-logic/platform-shape 1.x
        ├─ out/<x>/milan-nic.dtsi           kl,dma-ether + kl,milan-pcm nodes
        ├─ out/<x>/gptp_ucode.hex       option-on MAC/P1/clock-specific ROM
        ├─ out/<x>/build_plan.md        human-readable, "planned" marks
        ├─ out/<x>/milan-entity.conf        board-software IDENTITY fragment
        ├─ configs/generated/sweep_opts_<board>.sh   (board-level)
        │     └─ sourced by sw/litex/sweep.sh (inline tables = fallback)
        ├─ <rootfs overlay>/etc/milan-entity.<board>.conf   (board-level)
        │     └─ sourced by the flashed /etc/init.d/S50milan, which programs
        │        entity_id 0x604/0x608 + entity_model_id 0x60C/0x610 from it
        └─ hdl/ieee8021q/srp/gen/lwsrp_table.svh  (the srp.rtl_table config)
```

The identity fragment and the sweep fragment move at the same moment
(`--write-rtl`, or `--write-fragment` for the board that does not own the
tracked RTL tree) because they answer the same question: **what is this
board**. The fabric serves the AEM ENTITY descriptor's `entity_model_id` from
CSR `0x60C/0x610`, not from a ROM constant, so a literal in the boot script is
the entity's model id - and on 2026-08-02 silicon it was a *stale* one, an
8x8 AEM with dynamic output maps advertised under `0x001BC52ED611DB08`, the
id of a model that no longer existed. Gate 25 asserts that no identity CSR in
the shipped `S50milan` is written from a literal and that the shipped fragment
is byte-for-byte what the builder emits for the config `sweep.sh` builds that
board from.

## SoC software profile (`soc:`)

| Field | Values | Default | Bare-metal contract |
|---|---|---|---|
| `soc.software_profile` | `linux` \| `baremetal` | `linux` | Selects the firmware/CPU contract. |
| `soc.cpu` | `vexiiriscv` \| `naxriscv` | `vexiiriscv` | Must be `vexiiriscv`. |
| `soc.xlen` | `32` \| `64` | `32` | Must be `32`. |
| `soc.cpu_count` | positive int | `1` | Must be `1`. |
| `soc.scala_args` | Vexii argument list | proven Linux cache arguments | Must be empty. |
| `board.constraints.l2_bytes` | zero or power of two | board/config value | Must be zero. |
| `board.constraints.flashboot` | `none` \| `baremetal` \| `kernel` \| `full` | board/config value | Must be `baremetal` or `none`. |

The bare-metal selection emits `--software-profile baremetal --xlen 32
--l2-bytes 0`. LiteX then selects the RV32I machine-mode Vexii variant and
removes its bus-side SDRAM cache. Linux configurations retain the existing
cached/MMU-capable bring-up flow. The full firmware and UART contract is in
[`docs/integration/BAREMETAL_FIRMWARE.md`](../../docs/integration/BAREMETAL_FIRMWARE.md).

## lwSRP reservation table (`srp:`, CSR 0x680)

The lwSRP contract is hand-written in three places today —
`hdl/ieee8021q/srp/lwsrp_pkg.sv` (SR class, MRP timers, bandwidth math),
`hdl/common/csr/milan_csr.sv` (the 0x680 reset words, plus a *literal
duplicate* of the class-A `PriorityAndRank` byte because that file
deliberately does not import the package), and
[`REGISTER_MAP.md`](../../docs/reference/REGISTER_MAP.md) (the documented
Reset column). The config
owns all three: **every default in `SRP_DEFAULTS` is exactly today's reset
word**, so a config with no `srp:` section emits the deployed gateware
bit-for-bit, and gates 18a/18b parse all three RTL/doc sources and fail on
any disagreement.

| Field | Type / values | Default | Notes |
|-------|---------------|---------|-------|
| `srp.sr_class` | `A` | `A` | Milan v1.2 Section 5.6 defines class A only for a Milan end station; class B is rejected. |
| `srp.vid` | int 1..4094 | `2` | The SR VID. `0` is rejected — a stream on VID 0 floods **unshaped**. |
| `srp.stream_dmac_base` | MAC-48 hex | `0x91E0F000FE01` | Must be multicast (MAAP range). Stream `t` declares `base + t` (the MAAP-base+uid rule). |
| `srp.class_queue` | int, `< num_queues` | `4` | `LWSRP_CTRL[4:2]`, the class-A queue the granted slope muxes into (reset PCP3→TC3→q4 — q4 is the top of the 802.1Q-ordered 5-queue egress map). |
| `srp.enable_at_reset` / `talker_declare_at_reset` | bool | `false` | `LWSRP_CTRL[0]` / `[1]`. |
| `srp.accumulated_latency_ns` | uint32 | `0` | `LWSRP_LATENCY` (0x6A0). |
| `srp.bandwidth_limit_pct` | int 1..100 | `75` | Milan Section 5.6 / 802.1Q Section 34.3.1. Gate 18b checks the `KL_lwsrp_bw_gate` 750e6/75e6 ceiling literals against it. |
| `srp.timers_ms.{join,leave,leaveall}` | int ms | `200/600/10000` | 802.1Q Table 10-7. |
| `srp.tspec.policy` | `pinned` \| `derived` | `pinned` | `pinned` keeps `max_frame_bytes` verbatim (the deployed 0x690 reset). `derived` computes MaxFrameSize per talker from its AAF format. |
| `srp.tspec.max_frame_bytes` | uint16 | `224` | `pinned` only. |
| `srp.tspec.interval_frames` | uint16 | `1` | `LWSRP_TSPEC[31:16]`. |
| `srp.rtl_table` | bool | `false` | The one config that owns the tracked `hdl/ieee8021q/srp/gen/lwsrp_table.svh` (the DEPLOYED shape). |

**TSpec derivation (`policy: derived`).** Anchored in the
`KL_aaf_packetizer` contract, which states its own frame identity: payload =
`SAMPLES_PER_FRAME_C × C × 4` octets, so the L2 frame is `42 + 24·C` bytes at
48 kHz (`C = 2` is the golden 90-byte shape its byte-compare gate pins).
MSRP `MaxFrameSize` is the **MSDU**, not the L2 frame — the 802.1Q idleSlope
overhead of 42 already carries the Ethernet header + VLAN tag, so

```
samples_per_frame = sampling_rate_hz / 8000          (48 k → 6)
MaxFrameSize      = 24 + samples_per_frame × C × 4   (AVTPDU; 8ch → 216)
idleSlope[bps]    = MaxIntervalFrames × (MaxFrameSize + 42) × 8 × 8000
MaxFrameSize + 42 == preamble 8 + eth 14 + VLAN 4 + AVTPDU + FCS 4 + IPG 12
```

i.e. `MaxFrameSize + 42` is the exact wire slot — the identity gate 18c
checks for every `C` in 1..32. The deployed `pinned` 224 is a hand-picked
conservative value with no derivation behind it; for the shipping 2-channel
talker the derived MaxFrameSize is 72, so the deployed reservation
over-reserves ~2.3×. It stays pinned because changing it needs a reflash.

Σ-slope over `bandwidth_limit_pct` of the port rate is a **ConfigError**
citing 802.1Q Section 34.3.1 -- `KL_lwsrp_bw_gate` would refuse the excess streams
anyway, and finding that out at config-load beats finding it out on silicon.

**Attribute-context capacity (a real NxN shortfall this emitter surfaced).**
The 0x800 window row map is `listener k → row k`, `talker t → row (L-1)+t`,
row 0 = the legacy pair, so a shape needs **L+T-1** rows; but
`milan_datapath` ties `KL_lwsrp_top.N_CTX_P` to `N_STREAMS = max(L, T)`.
Every shape beyond 1x1 is therefore short: 4x4 needs 7 rows in 4, 8x8 needs
15 in 8. It rides in the build plan as a `planned (item 5)` mark, never
silently. Per-stream TSpec is a second mark: the ctx provisioning port
carries `max_frame`/`interval` per row, but the window sources both from the
shared `LWSRP_TSPEC` until per-stream TSpec words exist.

## Platform shape (`platform:`) -- device tree + driver-visible layout

`sw/litex/milan_soc.py`'s `MilanDMA` registers its submodules in a fixed
order and LiteX allocates CSR addresses in that order, so the driver-visible
DMA window map is a pure **function of `board.constraints.rx_queues`**:

```
+0x000  dma-tx        RingDMAReader                     0x24
+0x024  dma-rx  (q0)  RingDMAWriter incl. rsc + hs      0x68  (DT window 0x40)
+0x08C  steer         RxSteer               rx_queues≥2 0x0C  ┐ 0x74
+0x098  dma-rx1 (q1)  RingDMAWriter         rx_queues≥2 0x68  ┘ shift
   …    dma-ts        WishboneDMAWriter                 0x1C
   …    hs-pgsz-cap   CSRStatus                         0x04
   …    pcm-dma       PCM ring (sound_card=true only)   0x1C
```

1 queue gives `dma-ts 0xf000308c`, `hs-pgsz-cap 0xf00030a8`, and, when the
sound card is enabled, `pcm-dma 0xf00030ac`. Two queues give
`0xf0003100 / 0xf000311c / 0xf0003120` respectively. With the sound card off,
the PCM block consumes no CSR address and no PCM window appears in the DT.
Both are byte-verified against the real LiteX `csr.csv` of the shipping
builds and against the deployed `.dts` files by gate 19b (which SKIPs when
those trees are absent).

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `platform.csr_base` | address | `0x90000000` | The AXI-Lite Milan CSR window. Rejected below `0x80000000` (an MMIO peripheral must live in the CPU IO region). |
| `platform.mac_address` | MAC-48 | **required** | Must be unicast and non-zero. Two boards on one AVB switch must not share it. |
| `platform.interrupt` | int 0..31 | `3` | The PLIC line (`constant,milan_interrupt` in `csr.csv`). |
| `platform.pcm_ring_phys` / `_bytes` / `_stride` | address / pow2 / pow2 | `0x4ff00000` / `0x100000` / `0x100000` | With `sound_card: true`, the `no-map` region `snd-kl-milan` DMAs into. With it false, no PCM reservation is emitted; `pcm_ring_phys` still anchors the adjacent protocol-processor window below it. `stride × capture streams > bytes` is a ConfigError. |
| `platform.dma_coherent` | bool | `true` | Emits `dma-coherent;`. |
| `platform.boot_chain_pin` | map `window → address` | absent | **The CSR-rot guard.** The flashed DTB/opensbi/`kl-eth` address these windows *by address*; if `rx_queues` would move a pinned one, the build is REFUSED. |

`board.constraints.num_queues` (default `5`) joins the schema here: it is
`ethernet_packet_pkg::NUMBER_OF_QUEUES`, sizes the CBS tables and bounds
`srp.class_queue`; gate 18c parses the package and compares. It is **not**
required to be a power of two - the shipping egress map is five queues
(q4 SR class A down to q0 best effort, see
[EGRESS_QUEUE_MAP.md](../../docs/reference/EGRESS_QUEUE_MAP.md)).

Derived DT properties: `phy-mode` from `board.constraints.phy`
(`mii-100 → mii`, `gmii-1g → gmii`), and `kl,rsc-clk-mhz` from
`milan_clk_hz` — **the only `of_property_read_u32` `kl-eth` makes.** Omit it
and the AX7101 runs its PHC at 2× rate from a clean boot, so a
non-integer-MHz datapath clock is a ConfigError rather than a silent
truncation.

The shape also emits the physical addresses `kl-eth.c` **hardcodes** and the
DT does not carry — `MILAN_EV_PHYS`, `MILAN_PHY_CSR_PHYS`,
`MILAN_DMA_RX1_PHYS`, `MILAN_HS_PGSZ_CAP_PHYS`. Two of those move with
`rx_queues`; that is the largest remaining un-modelled coupling and the
reason the table exists.

## Optional blocks (`board.features:`) -- product options and tier-1 prunes

`sound_card` controls the Linux host audio surface and defaults to `false`.
`fabric_gptp` controls the #114 time-sync plane and defaults to `true` since
#116; `false` is the explicit legacy software bring-up comparison. The
remaining keys are the
[`docs/design/AREA_BUDGET.md`](../../docs/design/AREA_BUDGET.md) tier-1
datapath blocks; they default to `true`.

When `sound_card` is false, the builder rejects host role-pools and playback
rings, and emits no `--sound-card`, PCM DMA window, PCM device-tree node or
reserved ring. Physical capture/render, AAF, CRF and loopback fabric remain.

When `fabric_gptp` is true, the builder requires a `gptp:` section, emits
`--fabric-gptp`, and writes `gptp_ucode.hex` into the per-config output. The
ROM's station MAC, priority1 and clock come from the same YAML as the AEM and
SoC arguments and omits the legacy ptp4l config artifact. The shipping AX7101
config states the default explicitly; existing Arty Linux profiles state
`false` because they have no fabric microcode facts and remain the A/B arm.

The tier-1 set contains six
`milan_datapath` blocks that a given deployment may not be able to use, each
behind an **elaboration-time** parameter so synthesis drops the instance. The
whole section is optional.

```yaml
board:
  features:                    # optional; omit the block to keep everything
    sound_card: false          # default: no Linux PCM DMA/DT/AEM host surface
    fabric_gptp: true          # default; false retains ptp4l/statd comparison
    media_clock_servo: true
    latency_taps: true
    maap: true
    i2s_playback: true
    rx_mac_filter: true
    render_lpf: true
```

| Key | `milan_soc.py` flag | `milan_datapath` | Buys (yosys ESTIMATE) | Refused when the config still asks for it |
|-----|---------------------|------------------|-----------------------|-------------------------------------------|
| `media_clock_servo` | `--no-media-clock-servo` | `MCSERVO_P=0` | 814 LUT / 789 FF / 1 DSP | `clocking.media_clock_sources` offers anything but `internal` |
| `latency_taps` | `--no-latency-taps` | `LTAP_P=0` | 948 LUT / 614 FF | `board.constraints.strip_probes: false` (this build keeps its probes) |
| `maap` | `--no-maap` | `MAAP_P=0` | 634 LUT / 269 FF | `srp.stream_dmac_base: maap` (addresses claimed at run time) |
| `i2s_playback` | `--no-i2s-playback` | `I2SPB_P=0` | 454 LUT / 631 FF / 1 BRAM36 | `audio_interface.kind: i2s_philips` (its render half IS this block) |
| `rx_mac_filter` | `--no-rx-mac-filter` | `RXFILT_P=0` | 801 LUT / 1691 FF | `platform.rx_address_filter: hardware` (the default) |
| `render_lpf` | `--no-render-lpf` | `LPF_P=0` | 864 LUT / 756 FF / 1 DSP | `i2s_playback` is pruned but this is kept — its only consumer would be gone |

Every figure above is a **yosys estimate** from `syn/yosys/ooc.sh`'s toolchain
on the 8×8 ship shape, **not a placement result**; on the one block where both
numbers exist, Vivado places it at roughly half the LUTs. The last column is the
gate (`validate_features()`): a config that prunes a block *and* keeps the
element that needs it raises `ConfigError` naming both. A pruned block also
prints into `build_plan.md` with its parameter, its flag and the
**re-measurement it forces** — the obligation travels with the artefact.

Two supporting fields land with it:

| Field | Type / values | Default | Notes |
|-------|---------------|---------|-------|
| `platform.rx_address_filter` | `hardware` \| `software` \| `promiscuous` | `hardware` | Declares **where** the RX destination-address decision is taken. `hardware` (what both boards ship) requires `rx_mac_filter`; the other two are the honest statements that let it be pruned, because a pruned filter makes the port promiscuous. |
| `srp.stream_dmac_base` | MAC-48 hex \| `maap` | `0x91E0F000FE01` | `maap` = the DMACs are claimed at run time by `KL_maap` rather than provisioned here. The tables still model the default base; the allocation POLICY is what the MAAP prune gate keys on. |

## Schema 1.1 deltas (vs the 1.0 scaffold)

| Field | Type / values | Default | Consumed by | Notes |
|-------|---------------|---------|-------------|-------|
| `audio_interface.cluster_mapping.policy` | `cap-at-interface` \| `cluster-per-stream-channel` \| `role-pools` | `cluster-per-stream-channel` | overlay emitter (`cluster_layout`) | Replaces 1.0 `rule` (now rejected). `cluster-per-stream-channel`: the stream's `clusters` field verbatim (legacy/pipewire-reference). `cap-at-interface`: per stream `min(clusters, interface channels/direction)` — clusters model real endpoints only. `role-pools` (**D8**, 2026-07-28): the port's cluster block is the sum of its declared ROLE POOLS and `clusters` is unused for that port. All three generators implemented; `arty_current` keeps the deployed legacy layout, `arty_4x4` uses `cap-at-interface`, `ax7101_8x8` uses `role-pools`. |
| `audio_interface.physical_channels` | mapping: `capture` / `render`, each int `0..interface channels` | both = the interface family width | `cluster_layout` role assignment + `role-pools` `physical` width | Channels the **board actually routes**, per direction. Under the legacy policies it only decides which clusters are `physical` and which are `virtual` (the per-direction wire-truth rule — it does NOT change any count, so every pre-D8 config is byte-unchanged). Under `role-pools` it IS the `physical` pool width. **0 is legal and load-bearing**: `ax7101` ships `_connectors = []`, so `milan_soc.py` leaves `i2s_pads = None` / `i_i2s_sdout_i = 0` and ties the TDM pins off — that board routes no audio at all, and saying so is what keeps the model from advertising a pool the fabric cannot back. |
| `audio_interface.cluster_mapping.pools` | mapping: `host` int, `pilot` bool, `loopback` int | `{}` | `cluster_layout` (`role-pools` only) | **D8 role pools.** `host` = the ALSA/PipeWire lane channels for this port's stream (both directions); `pilot` = one `KL_tone_gen` cluster, **talker ports only**; `loopback` = received stream channels offered back as talker sources, **talker ports only**, talker *t* starting at rx stream *t* channel 0. Declaring `pools` under any other policy is a `ConfigError` (they would be silently ignored). The static AUDIO_MAP is written against the first non-empty of `physical`, `loopback`, `host`, `pilot`. **Planned RTL**: the pilot fan-out needs D7 (target-keyed store); the loopback lane needs a new `KL_chan_map_capture` source bucket (`src[6:4]` has `5..7` reserved today). Changes the model hash (conditional key: pre-D8 configs keep their ids). |
| `streams.talkers[].clusters` | int 1..32 | `channels` | overlay emitter | SINGLE AUTHORITY for the talker's cluster count (pre-policy). Example configs ship the wire-truth 2 (today's framer RTL is stereo); `arty_current` expresses the deployed legacy-8. |
| `streams.listeners[].clusters` | int 1..32 | `channels` | overlay emitter | Same authority, listener side. |
| `streams.listeners[].map_mode` | `dynamic` | `dynamic` | overlay emitter + gen_aem_store `AEM_DYNMAP` | Every Stream Port Input is dynamic. Milan v1.2 5.3.3.9 forbids an input AUDIO_MAP descriptor, so an explicit `static` value is rejected. The processor serves GET/ADD/REMOVE_AUDIO_MAPPINGS and the map RAM resets empty until restored or edited. |
| `streams.talkers[].map_mode` | `static` \| `dynamic` | `static` | overlay emitter + gen_aem_store `AEM_ODYNMAP` | A dynamic Stream Port Output drops its AUDIO_MAP and uses the live capture map. The capture crossbar currently selects one mapping mode for the complete image, so all talkers must use the same mode. A mixed static/dynamic output set is rejected. |
| `streams.listeners[].map_page` | int 1..11 | `min(max clusters over dynamic ports, 8)` | gen_aem_store `AEM_DYNMAP | GET_AUDIO_MAP fixed partition size in cluster keys (Milan 5.4.2.26; per port `number_of_maps = ceil(clusters/map_page)`, last partition short). ONE value shared by every dynamic port (the RTL page origin is a constant multiply) — declaring two different values is a ConfigError; leaving it unset resolves one default. Only valid with `map_mode: dynamic`; 11 = the RTL const-scratch bound. |
| `board.constraints.eth_port` | board's `eth_ports` (`ax7101`: `e1`\|`e2`) | absent | soc argv + sweep opts | Multi-PHY boards only (arty rejects it). `ax7101` ships `e2` (e1 GMII-RX hardware fault, 2026-07-22). |
| `entity.entity_model_id` | `hash-derived` \| EUI-64 hex | required | model-id resolution | `hash-derived` = the default path (recipe below); a hex literal stays expressible. |
| `entity.model_id_pin` | EUI-64 hex | absent | model-id resolution | WINS over everything: pins already-flashed silicon to its deployed identity (`arty_current` → `0x001BC50AC1000001`). Remove only with a model-changing reflash. |
| `clocking.crf_output` | mapping: `enabled` bool + `format` EUI-64 hex | `{enabled: false, format: 0x041060010000BB80}` | overlay emitter → `gen_aem_store` | CRF Media Clock OUTPUT (Milan 7.2.3). **RULE ENFORCED:** a config with >=2 AAF listener streams is rejected without `enabled: true` (error cites 7.2.3). Emits a CRF STREAM_OUTPUT appended after the AAF talkers — Milan 7.3.2 format word, `clock_domain_index` 0, CLOCK_SYNC_SOURCE\|CLASS_A flags, NO STREAM_PORT/cluster/map (mirrors the CRF sink), ADP talker count +1. Model half only: S50 provisioning + the ACMP talker context for the CRF stream ride with item-5 NxN (the `KL_crf_tx` fabric talker already exists, CSRs 0x750-0x764). |

## entity_model_id: hash-derived recipe (normative)

Resolution order: `model_id_pin` > `entity_model_id: hash-derived` >
`entity_model_id: <hex literal>`.

1. **shape** = `model_shape(cfg)`: the model-shaping fields ONLY —
   - cluster policy; interface kind/channels/word length; sampling rates +
     current rate; CRF sink + format;
   - CRF output (enabled + format, since the Milan-7.2.3 round — extended
     deliberately: a CRF output IS a model-shape change, so pre-existing
     hash-derived 4x4/8x8 ids changed with it; the deployed identity is
     pinned and unaffected);
   - per-listener channels/formats/clusters/buffer; per-talker
     channels/formats/clusters;
   - the derived per-stream port layout (`[base_cluster, clusters,
     base_map]` per port, both directions).
   - NO board flags, names or serials: two boards with the same audio
     shape share one model id (AEM semantics — same model, different
     instances).
2. **canon** = `json.dumps(shape, sort_keys=True, separators=(",", ":"))`
   (UTF-8).
3. **id** = `(MODEL_ID_OUI << 40) | (int.from_bytes(sha256(canon).digest()[:8], "big") & (2**40 - 1))`
   — top 8 bytes of the sha256, folded under the base EUI-64 prefix
   `MODEL_ID_OUI = 0x001BC5` (Kebag Logic OUI, 24 bits; 40 hash bits).
   Constants live in `endstation_builder.py` and are schema-level: changing
   them (or `model_shape`'s key set) re-identifies every hash-derived model
   — that is exactly what `model_id_pin` protects deployed silicon from.

Properties (test-gated): deterministic (same config → same id),
shape-sensitive (any `model_shape` field change → new id),
instance-insensitive (name/serial/board flags don't change it).

## Per-stream STREAM_PORT layout (overlay 2.x)

USER decision: ONE `STREAM_PORT_INPUT` per listener stream, ONE
`STREAM_PORT_OUTPUT` per talker stream (the CRF sink is a `STREAM_INPUT`
without an audio port). Every port owns

- a contiguous `AUDIO_CLUSTER` block (`base_cluster`, mono MBLA clusters;
  all input blocks precede all output blocks; the physical interface
  channels bind in order to the first clusters per direction — wire-truth
  1-to-1 rule), and
- exactly ONE `AUDIO_MAP` (`base_map`; static input ports first, then
  output ports, numbered contiguously) whose rows carry cluster offsets
  RELATIVE to the port's `base_cluster` (IEEE 1722.1-2021 Section 7.2.19) --
  UNLESS the port is `map_mode: dynamic`: it then carries NO map,
  advertises `number_of_maps=0`/`base_map=0` (Section 7.2.13) and its mappings
  are read through `GET_AUDIO_MAP`. They are currently writable only through
  the CSR `0x900` window; the required AECP ADD and REMOVE writers remain an
  open compliance gap.

Descriptor counts follow: `STREAM_PORT_INPUT = L`, `STREAM_PORT_OUTPUT = T`,
`AUDIO_MAP = static ports only (L + T minus dynamic)`,
`AUDIO_CLUSTER = Σ per-port clusters`.

## sweep.sh single-source contract

`endstation_builder.py` emits `configs/generated/sweep_opts_<board>.sh` — a
sh fragment defining exactly `OPTS` (the board design-flag prefix:
`--board`, non-default `--sys-clk-freq`, `--milan-clk-freq`,
`--gtx-tx-invert`, `--floorplan`, `--eth-port`) and `L2`.

`sw/litex/sweep.sh` sources the fragment when present and only falls back
to its inline case tables (loudly commented as FALLBACK) when it is absent.

The test gate asserts fragment `OPTS`/`L2` == the inline tables
byte-for-byte for both boards, and `sh -n` on sweep.sh + fragments.

The fragment is board-level: every config of a board emits the same
content as long as its `board.constraints` agree.

## gen_aem_store consumption + current limits

The builder still uses `gen_aem_store.py` to construct descriptor bytes from
the overlay, then `gen_aemi_image.py` and the pinned processor's descriptor
packer turn that model into `aem_desc.bin`. The paired `aem_desc.json` manifest
records the memory window and gateware pairing, while `aem_desc.map` is the
human-readable layout. An explicit `--write-fragment` or `--write-rtl`
ownership transfer writes the three files into the board rootfs overlay, and
`aemi-load` verifies and loads them into DRAM before entity enable.

The processor consumes the generated NxN descriptor image through the root
descriptor-memory master. Dynamic audio-map writes update the live root stores.
Nonvolatile replay remains absent, so software must restore dynamic state after
each power cycle.

## Resource estimator (approximate, pre-Vivado)

Every build plan carries a `## Resource estimate` section: per-module
LUT/FF/BRAM36/DSP costs x instance counts from the config, summed against
the xc7a100t budget (63400 LUT / 126800 FF / 135 BRAM36 / 240 DSP;
BRAM36 = RAMB36 + RAMB18/2 equivalents).

The cost table (`RESOURCE_COSTS` in `endstation_builder.py`) is calibrated
2026-07-22 from the REAL hierarchical place report of the shipping Arty
build (`build_arty_eto_milanfinal48`, cross-checked
`build_ax7101_eppo_milanfinal38`, totals within 2.4%); every entry states
its provenance row.

Confidence labels, per the area-70 house rule (hierarchical figures
mislead for small modules):

- `measured` - large blocks read straight from the report (cpu subtree,
  soc_infra top leaf incl MAC/DMA/DDR, milan_datapath major children);
- `low` - small-module hierarchical rows, aggregated into `datapath_misc`;
- `UPPER BOUND` - config-scaling rows (per AAF listener/talker engine,
  MAAP claim, ACMP listener context, lwSRP attribute context) charge
  TODAY's single-instance module cost per instance because the NxN
  engines do not exist yet (item 5) - full replication, no sharing;
- `model` - derived, not measured: L2 BRAM = 1 RAMB36 per 4 KB vs the
  64 KB calibration build (32 KB cross-check exact), AEM ROM growth =
  128 B per cluster beyond 16 (tracked ROM = 3675 B / 34 descriptors).

Verdict = worst category vs the part: **OK** (<70%), **TIGHT** (70-80%,
area-70 directive: keep slice headroom), **OVER** (>80%).

Calibration gate (test_builder gate 11): the `arty_current` estimate must
land within +/-15% of the real mf48 place totals, parsed from the report
at test time (SKIPs when the build tree is absent); current deltas are
+0.21% LUT / -0.13% FF / 0% BRAM36 / 0% DSP.

The NxN shapes come out OVER on xc7a100t (4x4 ~108% LUT, 8x8 ~142% LUT,
upper bounds) - that is the point: sizing before burning sweeps.
