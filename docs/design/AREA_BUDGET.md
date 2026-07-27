# Area budget — where the LUTs are, and which of them are optional

**Measured 2026-07-27** from the post-synthesis hierarchical utilisation of an
8×8 `xc7a100t` build (`report_utilization -hierarchical`, Vivado 2026.1). Every
number here is a **synthesis** figure from a real Vivado run — not an estimate,
and not a placement result.

This page deliberately **excludes the CPU**. The soft CPU and its caches are a
vendored component with their own configuration surface; everything below is
logic this project owns and can therefore choose not to build.

## The budget

| region | LUTs | share of device |
|---|---|---|
| device capacity (`xc7a100t`) | 63,400 | 100 % |
| **total used** | **61,959** | **97.7 %** |
| soft CPU + caches | 16,799 | 26.5 % |
| **`milan_datapath`** | **35,113** | **55.4 %** |
| SoC glue outside the datapath | 9,993 | 15.8 % |
| **non-CPU total (this page's scope)** | **~45,160** | **71.2 %** |

Flip-flops are **53,217 / 126,800 = 42 %** and block RAM is **91 / 135 = 67 %**.
**The design is LUT-bound.** A change that trades LUTs for FFs is a win; a change
that only removes FFs buys nothing.

## The datapath, by block

Leaf blocks over 400 LUTs. Parent rows are omitted where a single child
dominates them.

| block | module | LUT | FF | BRAM |
|---|---|---|---|---|
| `u_bld` | `KL_aecp_response_builder` | **5,300** | 2,342 | — |
| `csr` | `milan_csr` | **4,066** | 3,763 | R18×2 |
| `walker` | `KL_lwsrp_walker` | **2,938** | 904 | — |
| `u_ctx` | `KL_acmp_lstn_ctx` | **2,650** | 1,984 | — |
| `traffic_shaper` | `traffic_shaping_core` | **2,579** | 1,276 | — |
| `chan_map_render` | `KL_chan_map_render` | **2,547** | 1,625 | — |
| `ctx` | `KL_lwsrp_ctx` | 1,615 | 1,515 | R36×2 |
| `avtp_rx_monitor` | `KL_avtp_rx_monitor_ctx` | 1,268 | 1,113 | R18×1 |
| `aaf_packetizer` | `KL_aaf_packetizer` | 1,226 | 1,473 | R36+R18 |
| `ptp_timestamp` | `ptp_ts_top` | 1,069 | 1,669 | — |
| `mmcm_servo` | `KL_mmcm_drp_servo` | 933 | 807 | — |
| `acmp_responder` | `KL_acmp_tlkr_ctx` | 770 | 797 | — |
| `aaf_latency_taps` | `KL_aaf_latency_taps` | 696 | 614 | — |
| `maap_engine` | `KL_maap` | 621 | 268 | — |
| `rx_filter` | `rx_mac_filter` | 569 | 1,570 | — |
| `bw_gate` | `KL_lwsrp_bw_gate` | 564 | 676 | — |
| `i2s_player` | `KL_i2s_playback` | 552 | 624 | R36×1 |
| `buffer_queues` | `traffic_queues` | 531 | 321 | R36×6 R18×6 |
| `ctx_tx` | `KL_lwsrp_ctx_tx` | 505 | 312 | — |
| `mac_cam` | `tcam` | 504 | 1,568 | — |
| `pcm_lpf` | `KL_pcm_lpf` | 445 | 756 | — |

## What is actually optional

**Only two elaboration prunes exist today** — `AUDIO_IF_SLOTS_P` and
`AAF_PLAYBACK_P` — plus two SoC switches (`--aaf-playback`, `--strip-probes`).
Everything else is built unconditionally, whether or not a given deployment can
use it.

### Tier 1 — genuinely optional blocks

Each is dead weight in a deployment that does not use the feature. All default
to **PRESENT**, so adding the parameter changes no shipping build.

| candidate | LUT | FF | dead when |
|---|---|---|---|
| media-clock servo | 933 | 807 | the media clock is internal — the servo idles unless the clock source is the recovered one |
| latency taps | 696 | 614 | pure instrumentation; nothing in the media path reads them |
| MAAP engine | 621 | 268 | stream destination addresses are statically provisioned |
| I2S playback | 552 | 624 | the board has no DAC |
| RX address filter | 504 | 1,568 | the port is promiscuous, or filtering is done in software |
| PCM low-pass | 445 | 756 | already banked as `LPF_P` — render path only, and every digital acceptance measurement is taken upstream of it |
| **total** | **3,751** | **4,637** | |

**~3.75 k LUTs = 5.9 % of the device**, none of it requiring a functional change
— only the ability to say "this build does not include that".

### Tier 2 — blocks that should scale with the configured shape

These are not prune-or-keep; they are built for the largest shape regardless of
what the config asks for. Parameterising them to the *actual* shape is worth more
than pruning in a small build and costs nothing in a large one.

| candidate | LUT | scales with |
|---|---|---|
| `chan_map_render` | 2,547 | physical channels and slot count — a 2-channel build should not carry a 64-channel crossbar |
| `avtp_rx_monitor` | 1,268 | per-context counter banks |
| `KL_lwsrp_ctx` + `ctx_tx` | 2,120 | the L+T attribute rows |
| `acmp_responder` | 770 | talker contexts — a listener-only entity needs none |

### Tier 3 — core, not reclaimable by parametrisation

`u_bld` (5,300), `csr` (4,066), `walker` (2,938), `u_ctx` (2,650),
`traffic_shaper` (2,579). Together **17,533 LUTs, half the datapath.** These
implement mandatory behaviour; the only route into them is **structural** —
sequentialising wide parallel compares, sharing duplicated decode, replacing
per-index logic with a mux behind a counter. That is a redesign question, not a
parameter question, and it should be costed separately.

## The 9,993 LUTs outside the datapath

Roughly a sixth of the device sits in SoC glue that is neither CPU nor datapath —
DMA writers, the RX steering front end, CSR bridges, the Ethernet MAC core. It
has had **no area review at all**. It is called out here because "exclude the
CPU" makes it in-scope, and because 10 k LUTs is comparable to the entire tier-1
and tier-2 opportunity combined.

## The memory cascade: DDR3 for FIFOs, BRAM as register file

The device has **44 free BRAM tiles** (91 of 135 used). That single fact reorders
the work:

| consumer | tiles | note |
|---|---|---|
| soft CPU + caches | 29 | out of scope |
| SoC glue (DMA rings etc.) | 41 | largest single consumer, never reviewed |
| `traffic_queues` — egress FIFOs | 9 | largest datapath user |
| lwSRP (`top`+`rx`+`ingress`+`mrpdu_fifo`) | ~6.5 | |
| AECP ingress | 1.5 | |
| `milan_csr` | 1.0 | |
| **free** | **44** | |

### Stage 1 — spend the free tiles first: BRAM as the register file

**BRAM is not the constraint; LUTs are.** So the trade that matters is *LUTs into
BRAM*, and there are 44 tiles to spend **before** anything has to be freed.

The prize is not flop arrays — an audit found the big blocks are logic-dominated
(LUTRAM is 784 of 35,113 across the whole datapath, and their declared arrays
total ~5.5 k bits, mostly already in RAM). The prize is **turning combinational
logic into memory lookups**:

* **`milan_csr` — 4,066 LUT / 3,763 FF / 1 tile.** A CSR block is address decode,
  a register file, and a read multiplexer. Held in flops with a LUT mux, that
  read path grows with every register added — and this one has grown a lot
  (`0x200` RMON, `0x400` CBS, the `0x800` window, `0x870` taps, `0x8B4` probes,
  `0x8C8` playback). A **BRAM-backed register file** replaces the flop array *and*
  the read mux with one block memory. The registers that cannot move are the ones
  with side effects — strobes, W1C, snapshot latches, anything a fabric consumer
  reads combinationally — so this is a partition exercise, not a wholesale swap.
* **`u_bld` — 5,300 LUT.** A response builder is largely a wide field mux over
  descriptor data. Whatever part is a pure function of a descriptor index is a
  ROM.
* **`u_ctx` — 2,650 LUT**, `walker` — 2,938 LUT: same question, per block.

Each conversion costs a **read latency** and that is the real risk, not the
memory. `crf_rx` is the in-tree precedent: its `rate_o` moved one clock later and
that shift had to be pinned by a suite check before the change was accepted.

### Stage 2 — DDR3 for the bulk FIFOs, to free more tiles

Once the 44 free tiles are spent, the next tiles come from moving buffering into
the 512 MB DDR3. The candidates are **not equal**:

| FIFO | tiles | move to DDR3? |
|---|---|---|
| DMA / host rings (in the SoC glue's 41) | large | **yes** — already the pattern; the PCM ring already offers `--pcm-ring dram` |
| `mrpdu_fifo`, AECP ingress | ~3 | **yes** — control-plane, elastic, no deadline |
| `traffic_queues` egress buffers | 9 | **NO, or only with proof** |

**The egress queue buffers are the dangerous one.** They feed the MAC at line
rate, and the CBS shaper makes credit decisions against them cycle by cycle. DDR3
latency is variable — refresh, bank conflicts, arbitration against the CPU and
the DMA engines — and a late return mid-frame is an underrun on the wire, not a
retry. Anything isochronous stays on-chip unless someone measures worst-case
latency under contention and shows the headroom. Elastic, deadline-free buffering
is what belongs in DRAM.

## Rules for adding a prune parameter

1. **Default PRESENT.** A parameter that changes a shipping build by existing is
   a behaviour change wearing a costume.
2. **Elaboration-time, not runtime.** A runtime enable still builds the logic.
   The point is for synthesis to drop the instance.
3. **Tie the outputs to their inert values**, so a pruned block leaves a defined
   interface rather than a floating one.
4. **State what re-measurement it forces.** `LPF_P` is the worked example: the
   analog loop record was measured *through* that filter, so removing it invalidates
   that measurement even though it changes no digital acceptance surface.
5. **Gate it.** The builder must refuse a config that asks for a feature the
   parameter pruned — a silently absent feature is the decorative-ABI failure in
   reverse.

## Honest limits

* These are **synthesis** numbers. Placement can differ, and slice occupancy —
  not LUT count — is what actually failed on this design.
* The tier-1 total is what synthesis reports for those instances **today**; it is
  not a promise that removing them frees exactly that many slices, because
  packing and control-set effects dominate at this occupancy.
* Tier 2 is un-costed: the savings depend on the configured shape, and nobody has
  measured a small-shape build.
* The CPU is excluded by scope, not because it is optimal. It is 26.5 % of the
  device and has its own configuration surface.
