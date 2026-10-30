# Diagram catalog

Every diagram has one editable source.

Every current render needs visual inspection.

## Contents

- **[Diagram rules](#diagram-rules)** -- Keep facts and renders synchronized.
- **[Audience and architecture](#audience-and-architecture)** -- Navigate major system relationships.
- **[HDL timing](#hdl-timing)** -- Read important signal behavior.
- **[Register bit fields](#register-bit-fields)** -- Find the generated register diagrams.
- **[Measured figures](#measured-figures)** -- Understand dated performance evidence.
- **[Historical diagrams](#historical-diagrams)** -- Find preserved obsolete visuals.
- **[Feature status](#feature-status)** -- Preserve checked cross-document claims.
- **[Regeneration](#regeneration)** -- Rebuild and inspect outputs.

## Diagram rules

- Use Mermaid for simple documentation flows.
- Use WaveDrom for HDL timing.
- Use Draw.io for editable architecture diagrams.
- Use generators for source-derived facts.
- Never edit rendered outputs directly.
- Keep inspection files under `/tmp`.
- Verify every label against implementation.
- Print changed Draw.io masters before review.
- Bind every published PNG to its editable source.
- Decode every published PNG before review.
- Pin decompressed rasters inside `PNG_MANIFEST.json`.
- Permit PNG compression differences.
- Review every changed manifest digest visually.

## Audience and architecture

| Diagram | Purpose | Editable source | Committed renders | Main reader |
|---|---|---|---|---|
| `DOC_MAP` | Four ordered audience paths | [`../DOC_MAP.gen.py`](../DOC_MAP.gen.py), `../DOC_MAP.drawio` | `../DOC_MAP.svg`, `../DOC_MAP.png` | Every reader |
| `SYSTEM_DOMAIN_MAP` | System ownership by domain | [`../SYSTEM_DOMAIN_MAP.gen.py`](../SYSTEM_DOMAIN_MAP.gen.py), `../SYSTEM_DOMAIN_MAP.drawio` | `../SYSTEM_DOMAIN_MAP.svg`, `../SYSTEM_DOMAIN_MAP.png` | Developers and integrators |
| `BUILD_FLASH_BOOT` | Build through deployment | [`../BUILD_FLASH_BOOT.gen.py`](../BUILD_FLASH_BOOT.gen.py), `../BUILD_FLASH_BOOT.drawio` | `../BUILD_FLASH_BOOT.svg`, `../BUILD_FLASH_BOOT.png` | Integrators and managers |
| `submodule_boundaries` | Four exact Git boundaries | [`submodule_boundaries.gen.py`](submodule_boundaries.gen.py), `submodule_boundaries.drawio` | `submodule_boundaries.svg`, `submodule_boundaries.png` | Developers and managers |
| `cdc_census` | Derived clock crossings | [`cdc_census.gen.py`](cdc_census.gen.py), `cdc_census.drawio` | `cdc_census.svg`, `cdc_census.png` | Implementation developers |
| `egress_queue_map` | Derived queue ownership | [`egress_queue_map.gen.py`](egress_queue_map.gen.py), `egress_queue_map.drawio` | `egress_queue_map.svg`, `egress_queue_map.png` | Developers and integrators |
| `flash_layout` | Derived QSPI layout | [`flash_layout.gen.py`](flash_layout.gen.py), `flash_layout.drawio` | `flash_layout.svg`, `flash_layout.png` | Integrators |
| `timesync_chain` | Clock ownership chain | [`timesync_chain.gen.py`](timesync_chain.gen.py), `timesync_chain.drawio` | `timesync_chain.svg`, `timesync_chain.png` | Developers and integrators |
| `memory_map` | Derived SoC memory map | [`memory_map.gen.py`](memory_map.gen.py), `memory_map.drawio` | `memory_map.svg` | Firmware developers and integrators |
| `milan_tx_rx_datapath` | Datapath block map | `../milan_tx_rx_datapath.drawio` | Editable master only | Implementation developers |

The [submodule reference](../reference/SUBMODULES.md) embeds its verified map.

## HDL timing

| Diagram | Verified behavior | Editable source | Main reader |
|---|---|---|---|
| `wd_axis_backpressure` | Accepted AXI-Stream transfers | `wd_axis_backpressure.json` | Both developer roles |
| `wd_cdc_handshake` | Multi-bit clock crossing | `wd_cdc_handshake.json` | Both developer roles |
| `wd_gptp_pdelay` | Parent pdelay timestamp ownership | `wd_gptp_pdelay.json` | Time-sync developers |
| `wd_cbs_credit` | Credit shaping behavior | `wd_cbs_credit.json` | Datapath developers |
| `wd_ring_pointers` | DMA pointer commits | `wd_ring_pointers.json` | DMA developers |
| `wd_linkguard_reset` | Sequenced reset release | `wd_linkguard_reset.json` | Integrators |
| `wd_ts_wrap_alias` | Timestamp wrap behavior | `wd_ts_wrap_alias.json` | Timing developers |
| `wd_i2s_philips` | I2S framing | `wd_i2s_philips.json` | Historical media readers |
| `wd_tdm8_frame` | TDM8 framing | `wd_tdm8_frame.json` | Historical media readers |
| `wd_aaf_pacing` | AAF pacing | `wd_aaf_pacing.json` | Historical media readers |

Every WaveDrom has SVG and PNG renders.

New WaveDrom renders use white backgrounds.

## Register bit fields

Each CSR module has one generated WaveDrom source.

Every register's SVG is rendered from it.

<!-- register-diagrams:start -->
| Module source | Module | Registers | Renders |
|---|---|---|---|
| [`regmap/ident.json`](regmap/ident.json) | Identification / IRQ | 7 | `regmap/ident/*.svg` |
| [`regmap/mac.json`](regmap/mac.json) | MAC control / status | 8 | `regmap/mac/*.svg` |
| [`regmap/stats.json`](regmap/stats.json) | Statistics (RMON) | 3 | `regmap/stats/*.svg` |
| [`regmap/cls.json`](regmap/cls.json) | 802.1Q classifier | 5 | `regmap/cls/*.svg` |
| [`regmap/cbs.json`](regmap/cbs.json) | 802.1Qav CBS (per queue) | 4 | `regmap/cbs/*.svg` |
| [`regmap/ptp.json`](regmap/ptp.json) | PTP hardware clock | 18 | `regmap/ptp/*.svg` |
| [`regmap/adp.json`](regmap/adp.json) | ADP advertiser | 18 | `regmap/adp/*.svg` |
| [`regmap/aecp.json`](regmap/aecp.json) | AECP/ACMP status + AAF talker | 12 | `regmap/aecp/*.svg` |
| [`regmap/lwsrp.json`](regmap/lwsrp.json) | lwSRP engine | 9 | `regmap/lwsrp/*.svg` |
| [`regmap/acmpl.json`](regmap/acmpl.json) | ACMP listener SM | 21 | `regmap/acmpl/*.svg` |
| [`regmap/tcam.json`](regmap/tcam.json) | RX destination-MAC TCAM filter | 7 | `regmap/tcam/*.svg` |
| [`regmap/link.json`](regmap/link.json) | Link guard / MAC recovery | 2 | `regmap/link/*.svg` |
| [`regmap/overlay.json`](regmap/overlay.json) | identity / playback / 802.1AS overlay | 5 | `regmap/overlay/*.svg` |
| [`regmap/crf.json`](regmap/crf.json) | CRF media-clock sink | 6 | `regmap/crf/*.svg` |
| [`regmap/crft.json`](regmap/crft.json) | CRF media-clock talker | 6 | `regmap/crft/*.svg` |
| [`regmap/bdbg.json`](regmap/bdbg.json) | AECP scan forensics (BDBG) and link-guard status | 4 | `regmap/bdbg/*.svg` |
| [`regmap/clkv.json`](regmap/clkv.json) | Clock validity, TX arbiter and SRP domain | 5 | `regmap/clkv/*.svg` |
| [`regmap/rest.json`](regmap/rest.json) | ACMP bind-restore | 6 | `regmap/rest/*.svg` |
| [`regmap/jnl.json`](regmap/jnl.json) | Persistence-journal ingest | 4 | `regmap/jnl/*.svg` |
| [`regmap/aemp.json`](regmap/aemp.json) | AEM dynamic-state patch port | 4 | `regmap/aemp/*.svg` |
| [`regmap/guard.json`](regmap/guard.json) | Ethernet guard | 1 | `regmap/guard/*.svg` |
| [`regmap/asp.json`](regmap/asp.json) | retired AS_PATH compatibility addresses | 3 | `regmap/asp/*.svg` |
| [`regmap/gptpd.json`](regmap/gptpd.json) | gPTP plane drop diagnostics | 2 | `regmap/gptpd/*.svg` |
| [`regmap/gptpl.json`](regmap/gptpl.json) | applied gPTP timestamp latency corrections | 1 | `regmap/gptpl/*.svg` |
| [`regmap/strm.json`](regmap/strm.json) | Indexed per-stream window | 16 | `regmap/strm/*.svg` |
| [`regmap/ltap.json`](regmap/ltap.json) | AAF per-stage latency taps | 2 | `regmap/ltap/*.svg` |
| [`regmap/aprb.json`](regmap/aprb.json) | RX stream-parser probe | 1 | `regmap/aprb/*.svg` |
| [`regmap/gap.json`](regmap/gap.json) | reserved target-media compatibility words | 1 | `regmap/gap/*.svg` |
| [`regmap/slip.json`](regmap/slip.json) | media-boundary slip counters | 2 | `regmap/slip/*.svg` |
| [`regmap/render.json`](regmap/render.json) | render presentation state | 1 | `regmap/render/*.svg` |
| [`regmap/aafm.json`](regmap/aafm.json) | AAF clock meter | 2 | `regmap/aafm/*.svg` |
| [`regmap/mcsrv.json`](regmap/mcsrv.json) | MMCM-DRP media-clock servo | 2 | `regmap/mcsrv/*.svg` |
| [`regmap/chmap.json`](regmap/chmap.json) | channel-map fabric | 6 | `regmap/chmap/*.svg` |
| [`regmap/pp.json`](regmap/pp.json) | protocol-processor control plane | 8 | `regmap/pp/*.svg` |
<!-- register-diagrams:end -->

## Measured figures

| Figure | Purpose | Generator | Embedded by |
|---|---|---|---|
| `ts_modular_ring.svg` | Modular timestamp ring | `diag_ts_modular_ring.py` | [Presentation timing](../design/PRESENTATION_TIME_WRAP.md) |
| `ts_wrap_walk.svg` | Measured wrap progression | `diag_ts_wrap_walk.py` | [Presentation timing](../design/PRESENTATION_TIME_WRAP.md) |

These figures describe dated measurements.

They never guarantee other hardware results.

## Historical diagrams

| Diagram | Historical context | Current successor |
|---|---|---|
| `audio_stream_path` | Retired audio topology | [Dataplane walkthrough](../fpga/DATAPLANE_WALKTHROUGH.md) |
| `nxn_window_map` | Shipped row-map defect | [Architecture](../overview/ARCHITECTURE.md) |
| `../history/v1/diagrams/ROOT_DOC_MAP.*` | Superseded audience map | [Documentation index](../README.md) |
| `../history/v1/diagrams/perf_campaign.*` | Closed throughput-campaign chart | [Full FPGA solution](../overview/FULL_FPGA_SOLUTION.md) |
| `../history/v1/diagrams/timesync_chain.*` | Frozen pre-rework clock-chain render | [Time synchronization](../design/TIME_SYNC.md) |
| `../history/v1/diagrams/wd_gptp_pdelay.*` | Frozen pre-rework peer-delay chronogram | [Fabric gPTP plane](../design/GPTP_PLANE.md) |

Historical diagrams remain evidence only.

They never define current behavior.

## Feature status

These claims remain machine-checked.

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `aem.served-command-set` | `implemented` | - |
| `notifications.change-events` | `implemented` | - |
<!-- milan-feature-status:end -->

## Regeneration

Use the [generation guide](../DOC_GENERATION.md).

Run focused generator checks first.

```sh
python3 scripts/gen_register_reference.py --check
python3 docs/diagrams/memory_map.gen.py --check
python3 docs/DOC_MAP.gen.py --check
python3 docs/DOC_MAP.gen.py --selftest
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 docs/diagrams/submodule_boundaries.gen.py --selftest
python3 docs/diagrams/timesync_chain.gen.py --check
python3 docs/diagrams/timesync_chain.gen.py --selftest
python3 scripts/check_submodule_docs.py
python3 scripts/check_diagram_pngs.py
python3 scripts/check_diagram_pngs.py --selftest
```

Run WaveDrom checks with pinned tooling.

```sh
python3 scripts/gen_wavedrom.py \
  docs/diagrams/wd_axis_backpressure.json --background=white --check
python3 scripts/gen_wavedrom.py \
  docs/diagrams/wd_cdc_handshake.json --background=white --check
python3 scripts/gen_wavedrom.py \
  docs/diagrams/wd_gptp_pdelay.json --background=white --check
```

- Generator checks tolerate local renderer differences.
- Reviewed committed rasters remain cryptographically pinned.
- Changed raster digests require visual approval.

- Regenerate the editable master.
- Regenerate every committed render.
- Export Draw.io directly.
- Simulate A4 printing.
- Inspect PNG readability.
- Verify embedded data independently.
- Update this catalog.
