# Diagram catalog

Every diagram has one editable source.

Every current render needs visual inspection.

## Contents

- **[Diagram rules](#diagram-rules)** — Keep facts and renders synchronized.
- **[Audience and architecture](#audience-and-architecture)** — Navigate major system relationships.
- **[HDL timing](#hdl-timing)** — Read important signal behavior.
- **[Measured figures](#measured-figures)** — Understand dated performance evidence.
- **[Historical diagrams](#historical-diagrams)** — Find preserved obsolete visuals.
- **[Feature status](#feature-status)** — Preserve checked cross-document claims.
- **[Regeneration](#regeneration)** — Rebuild and inspect outputs.

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
| `milan_tx_rx_datapath` | Datapath block map | `../milan_tx_rx_datapath.drawio` | Editable master only | Implementation developers |

The [submodule reference](../reference/SUBMODULES.md) embeds its verified map.

## HDL timing

| Diagram | Verified behavior | Editable source | Main reader |
|---|---|---|---|
| `wd_axis_backpressure` | Accepted AXI-Stream transfers | `wd_axis_backpressure.json` | Both developer roles |
| `wd_cdc_handshake` | Multi-bit clock crossing | `wd_cdc_handshake.json` | Both developer roles |
| `wd_gptp_pdelay` | Peer-delay timestamps | `wd_gptp_pdelay.json` | Time-sync developers |
| `wd_cbs_credit` | Credit shaping behavior | `wd_cbs_credit.json` | Datapath developers |
| `wd_ring_pointers` | DMA pointer commits | `wd_ring_pointers.json` | DMA developers |
| `wd_linkguard_reset` | Sequenced reset release | `wd_linkguard_reset.json` | Integrators |
| `wd_ts_wrap_alias` | Timestamp wrap behavior | `wd_ts_wrap_alias.json` | Timing developers |
| `wd_i2s_philips` | I2S framing | `wd_i2s_philips.json` | Historical media readers |
| `wd_tdm8_frame` | TDM8 framing | `wd_tdm8_frame.json` | Historical media readers |
| `wd_aaf_pacing` | AAF pacing | `wd_aaf_pacing.json` | Historical media readers |

Every WaveDrom has SVG and PNG renders.

New WaveDrom renders use white backgrounds.

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
python3 docs/DOC_MAP.gen.py --check
python3 docs/DOC_MAP.gen.py --selftest
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 docs/diagrams/submodule_boundaries.gen.py --selftest
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
