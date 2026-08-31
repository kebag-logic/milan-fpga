# Documentation audit

This audit records verified documentation findings.

It covers current root documentation and pinned imports.

## Contents

- **[Method](#method)** — Explain each evidence source.
- **[Audience paths](#audience-paths)** — Separate reader responsibilities.
- **[Measured baseline](#measured-baseline)** — Record dated repository facts.
- **[Authority conflicts](#authority-conflicts)** — Keep contradictions visible.
- **[History policy](#history-policy)** — Separate obsolete material safely.
- **[Device wording](#device-wording)** — Preserve neutral public examples.
- **[Diagram verification](#diagram-verification)** — Check data and readability.
- **[Follow-up work](#follow-up-work)** — Link discovered work publicly.

## Method

- Git supplied every recorded submodule revision.
- RTL supplied interface and timing facts.
- Executable tests supplied verification ownership.
- Generated renders received visual inspection.
- Current authorities excluded historical claims.

## Audience paths

| Reader | New path | Primary decision |
|---|---|---|
| Implementation developer | [`guides/IMPLEMENTATION_DEVELOPER.md`](guides/IMPLEMENTATION_DEVELOPER.md) | Change product code safely |
| Verification developer | [`guides/VERIFICATION_DEVELOPER.md`](guides/VERIFICATION_DEVELOPER.md) | Produce defect-detecting evidence |
| System integrator | [`guides/SYSTEM_INTEGRATOR.md`](guides/SYSTEM_INTEGRATOR.md) | Wire every product boundary |
| Project manager | [`guides/PROJECT_MANAGER.md`](guides/PROJECT_MANAGER.md) | Judge readiness from evidence |

The developer views remain intentionally separate.

Code providers follow implementation ownership.

Test providers follow verification ownership.

## Measured baseline

Measurements describe the 2026-08-31 baseline.

Volatile counts never define future coverage.

| Evidence | Observed result | Documentation consequence |
|---|---|---|
| `scripts/run_all_suites.sh --list` | 54 root Verilator suites | Avoid copied suite inventories |
| `cd tests && behave -f plain` | 14 features, 312 scenarios, 1,467 steps | Existing published counts are stale |
| `sw/litex/test_*.py` | 12 standalone scripts | Missing aggregate ownership needs follow-up |
| Root Verilator sweep | Donor suites excluded | Donor and root evidence stay separate |
| C++ harnesses | Clocks, stimulus, assertions, reference models | Verification guide assigns cycle checking |
| Python tests | Models, orchestration, gates, decoding | Verification guide assigns control flow |
| C sources | Firmware, research microbenchmarks, and trace tooling | Keep target and host roles separate |

## Authority conflicts

These conflicts cannot be resolved through summaries.

Each conflict keeps its original authority.

| Conflict | Implementation evidence | Current treatment |
|---|---|---|
| Donor gPTP README says default-off | `hdl/milan/milan_datapath.sv` defaults `GPTP_PLANE_EN_P` on | Track donor Issue [#48](https://github.com/Mister-M-alt/FPGA-gPTP/issues/48) |
| Donor gPTP README retains retired host services | Full solution specifies bare-metal firmware | Treat donor runtime prose as historical |
| Donor protocol page retains word-wide RX | `protocol_processor_top.sv` exposes byte RX without ready | Track donor Issue [#27](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/27) |
| Archived v1 integration guide omits response memory | `milan_datapath.sv` exposes `resp_mem_*` | Current contract classifies every port group |
| Existing Behave counts are stale | Executed baseline reports 14/312/1,467 | New guide avoids volatile counts |
| Current Milan audit says gPTP is unintegrated | Root RTL defaults fabric gPTP on | Managers use the feature ledger |

## History policy

Obsolete evidence belongs under `docs/history/v1/`.

Moves preserve filenames whenever practical.

Every moved page needs status metadata.

Every moved page names its current successor.

Current indexes must exclude archived authorities.

Normative requirements remain outside this migration.

Mixed pages need factual extraction before movement.

## Device wording

Tracked documentation contains no forbidden peer name.

New examples use `test device`.

The privacy gate remains mandatory.

The full solution names only bare-metal firmware.

A product-document guard rejects retired platform substrings.

Historical runtime profiling remains under `docs/history/v1/`.

Host tooling names remain outside product descriptions.

## Diagram verification

Diagram facts come from Git and verified root paths.

Audience paths come from validated repository files.

Submodule generation rejects missing integration evidence.

Audience generation rejects missing reader paths.

Path-derived node identities prevent edge rebinding.

The PNG manifest pins every reviewed decompressed raster.

Valid blank-raster mutations fail every generator.

Renderer changes require regeneration and visual review.

### Draw.io print review

Draw.io desktop produced the inspected PNG and PDF.

Temporary render files stayed under `/tmp`.

Desktop export requires an available display.

| Diagram | Direct PNG | Native PDF | A4 PNG | Result |
|---|---:|---:|---:|---|
| Audience paths | 3,526 × 2,030 | 1,270.08 × 731.04 points | 1,754 × 1,241 | PASS |
| Submodule boundaries | 2,866 × 1,664 | 1,032 × 599.04 points | 1,754 × 1,241 | PASS |

| Check | Inspected evidence | Result |
|---|---|---|
| Editable structure | Parsed Draw.io XML | PASS |
| A4 print simulation | 841.89 × 595.276 points | PASS |
| Text extraction | Every native PDF label appeared | PASS |
| Visual inspection | No clipping or overlaps | PASS |
| Audience data | Twenty-four repository paths exist | PASS |
| Git data | Four exact Gitlinks matched | PASS |
| Raster provenance | Four manifest digests matched | PASS |
| Wrong-raster controls | Seven independent mutations failed | PASS |

All labels remained readable at page scale.

Light fills preserve monochrome contrast.

Connector captions remained distinguishable.

Reproduce the print review locally.

```sh
render_dir=$(mktemp -d)
python3 docs/DOC_MAP.gen.py --check
python3 docs/diagrams/submodule_boundaries.gen.py --check
drawio --export --format pdf --crop \
  --output "$render_dir/native.pdf" \
  docs/diagrams/submodule_boundaries.drawio
drawio --export --format png --crop --scale 2 \
  --output "$render_dir/direct.png" \
  docs/diagrams/submodule_boundaries.drawio
drawio --export --format png --crop --scale 2 \
  --output "$render_dir/audiences.png" \
  docs/DOC_MAP.drawio
pdftocairo -svg "$render_dir/native.pdf" "$render_dir/native.svg"
rsvg-convert -f pdf \
  --page-width 297mm --page-height 210mm \
  -w 277mm -h 160.73mm --left 10mm --top 24.635mm -a \
  "$render_dir/native.svg" -o "$render_dir/a4.pdf"
pdftoppm -png -r 150 -singlefile \
  "$render_dir/a4.pdf" "$render_dir/a4"
```

### WaveDrom review

WaveDrom timing matches inspected RTL edges.

White backgrounds preserve dark-theme visibility.

| Diagram | Verified behavior | RTL authority |
|---|---|---|
| AXI-Stream backpressure | Acceptance equals `tvalid && tready` | `hdl/common/axi_stream_if.sv` |
| CDC handshake | Capture occurs on destination rising edges | `hdl/common/cdc_handshake.sv` |
| CDC handshake | Separate resets remain visible | `hdl/common/cdc_handshake.sv` |
| CDC handshake | Default synchronizer depths drive shown latency | `hdl/common/cdc_handshake.sv` |

Committed PNG renders received direct inspection.

Reproduce both current timing diagrams.

Create a temporary WaveDrom environment.

```sh
python3 -m venv /tmp/milan-wavedrom
/tmp/milan-wavedrom/bin/pip install wavedrom==2.0.3.post3
```

Install `rsvg-convert` through your system package manager.

```sh
/tmp/milan-wavedrom/bin/python3 scripts/gen_wavedrom.py \
  docs/diagrams/wd_axis_backpressure.json --background=white
/tmp/milan-wavedrom/bin/python3 scripts/gen_wavedrom.py \
  docs/diagrams/wd_cdc_handshake.json --background=white
/tmp/milan-wavedrom/bin/python3 scripts/gen_wavedrom.py \
  docs/diagrams/wd_axis_backpressure.json --background=white --check
/tmp/milan-wavedrom/bin/python3 scripts/gen_wavedrom.py \
  docs/diagrams/wd_cdc_handshake.json --background=white --check
```

## Follow-up work

- Donor gPTP wording uses [Issue #48](https://github.com/Mister-M-alt/FPGA-gPTP/issues/48).
- Donor protocol history uses [Issue #27](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/27).
- LiteX aggregation uses [root Issue #297](https://github.com/kebag-logic/milan-fpga/issues/297).
