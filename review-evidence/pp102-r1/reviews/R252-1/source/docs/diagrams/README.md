<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Diagram Sources & Toolchain

Three figures are rich enough to warrant free-form drawing; they are draw.io sources
with committed SVG exports. **Everything else** (Mermaid, WaveDrom) lives as editable
text inside the host Markdown documents — see `docs/README.md` §3.

Rendering support differs per format, which drives the storage pattern:

| Format | GitHub renders it? | Pattern |
|---|---|---|
| Mermaid | yes, natively | fenced source only |
| WaveDrom | **no** | committed SVG in `wavedrom/` + fenced source collapsed in `<details>` under the image; `make wavedrom` keeps them in sync (bootstraps `.venv-wavedrom/` with the Python `wavedrom` package on first run) |
| draw.io | no | committed SVG here + `.drawio` source in `src/` |
| hand-authored SVG | yes | the SVG **is** the source; validate a change by rendering it to PNG and looking at it (below) |

`wavedrom/*.svg` files are named after the figure anchor of their source block
(`fig-04-adpdu.svg` ← `<a id="fig-04-adpdu">`); the render script derives this
automatically — never hand-edit those SVGs.

## Inventory (draw.io)

| Source (`src/`) | Export | Figure | Host document |
|---|---|---|---|
| `01-system-context.drawio` | `01-system-context.svg` | F01.1 — PAAD system context | `architecture/01_overview.md` §2 |
| `01-top-level.drawio` | `01-top-level.svg` | F01.2 — processor top level | `architecture/01_overview.md` §4 |
| `03-shared-datapath.drawio` | `03-shared-datapath.svg` | F03.1 — shared datapath & memory interconnect | `architecture/03_packet_engine.md` §2 |

Rule: **source and export are committed together**; `make stale` fails the tree if an
SVG is older than its `.drawio`.

## Inventory (hand-authored SVG)

These five are written directly as SVG and have **no `.drawio` source**. They are drawn
against the landed RTL rather than against the specification, and they are the entry
figures of the [persona guides](../guides/README.md).

| File | Figure | Host document |
|---|---|---|
| `20-rtl-dataflow.svg` | every module in `protocol_processor_top`, and how a frame moves through them | [HDL engineer guide](../guides/hdl-engineer.md), [integrator guide](../guides/integrator.md) |
| `21-integration-faces.svg` | the complete external contract, with tie-off behaviour | [integrator guide](../guides/integrator.md) |
| `22-aecp-descriptor-fetch.svg` | READ_DESCRIPTOR through the integrator's main memory | [HDL engineer guide](../guides/hdl-engineer.md), [integrator guide](../guides/integrator.md) |
| `23-bringup-decision.svg` | the bring-up ladder and the counter to read at each failure | [operator guide](../guides/operator.md) |
| `24-adp-acmp-states.svg` | the advertise and listener-binding machines, as an operator sees them | [operator guide](../guides/operator.md) |

**Why no draw.io source for these:** the draw.io CLI does not complete headless on the
development machine used here — it hangs rather than exporting, including under
`xvfb-run`, and ignores a shell timeout. A `.drawio` file that cannot be rendered is not a
diagram anyone can see, so these are authored as clean, hand-written SVG instead, which is
both the editable source and the published artifact. If draw.io export is ever fixed on
your machine, the three files in `src/` still export normally with `make diagrams`.

**Editing rule for these five:** after any change, render to PNG and *look at the result*.
Overlap, clipped text and lines running through boxes are invisible in the XML.

```sh
rsvg-convert -w 1500 -o /tmp/check.png docs/diagrams/20-rtl-dataflow.svg
```

Check for overlapping text, labels escaping their box, arrows landing on the wrong block,
and legibility at normal size. Every one of these carries an opaque light background so it
reads on both light and dark page themes.

## Commands

```sh
# regenerate all exports: drawio -> svg AND every wavedrom block -> svg (from repo root)
make diagrams

# wavedrom only (after editing a ```wavedrom block in any doc)
make wavedrom

# one file, manually
drawio -x -f svg --crop -o docs/diagrams/01-top-level.svg docs/diagrams/src/01-top-level.drawio
# headless fallback (no display):
xvfb-run -a drawio --no-sandbox -x -f svg --crop -o <out.svg> <in.drawio>

# full documentation gate: mermaid/wavedrom lint + links + compliance matrix + SVG freshness
make check
```

## Style guide

- **draw.io**: snap to a 10 px grid; sans-serif 11–12 pt labels; clock/reset domains as
  tinted container groups; no embedded bitmaps.

  **Routing discipline — follow this or edges will overlap boxes.** draw.io's automatic
  routing sends edges *through* shapes and drops labels at the geometric midpoint of an
  edge, which lands them on unrelated blocks. Therefore:

  1. **Every edge declares `exitX/exitY/entryX/entryY`.** Never leave a connection
     floating; pick the side deliberately, and give parallel edges distinct fractions
     (`exitX=0.3`, `0.5`, `0.7`) so they fan out instead of stacking.
  2. **Every edge that leaves its row or column carries explicit waypoints**
     (`<Array as="points">`) routed through a **gutter** — a deliberate empty lane
     between blocks. The current layouts reserve horizontal gutters between block rows
     and vertical gutters between block columns; keep them empty.
  3. **Two edges never share a lane.** Parallel runs are spaced ≥ 20 px
     (e.g. one vertical at x=1120, the next at x=1170).
  4. **Labels are short and opaque**: `labelBackgroundColor=#ffffff;fontSize=10`, one or
     two words. Anything longer belongs in the host document's prose or in the
     figure's legend box.
  5. Interface-class tags (A–F per `architecture/02_interfaces.md`) go on short external
     edges or in the legend — never on long internal edges.

  After any edit, re-export and **look at the result** (`drawio -x -f png --scale 1.1 -o
  /tmp/check.png <src>`); overlap is invisible in the XML.
- **Mermaid**: theme-neutral (no `%%{init}%%`), stable lower-kebab node IDs, no HTML
  labels; FSM arcs labeled with `T-…`/`A…` IDs, not literal values.
- **WaveDrom**: strict JSON (double-quoted keys); MSB left; in `reg` figures, field
  names carry byte offsets (`seq_id@48`) or masks (`REGISTERING_FAILED (0x40)`) where
  misreading is dangerous.
