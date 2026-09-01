# Generate documentation

Edit every authoritative source first.

Then regenerate every committed output.

## Contents

- **[Source rules](#source-rules)** — Identify authoritative inputs.
- **[Module documentation](#module-documentation)** — Regenerate traceability outputs.
- **[Headless HDL reference](#headless-hdl-reference)** — Generate validated module pages.
- **[Drawio diagrams](#drawio-diagrams)** — Export and inspect editable masters.
- **[Wavedrom timing](#wavedrom-timing)** — Render verified HDL timing.
- **[Historical pages](#historical-pages)** — Preserve obsolete documentation safely.
- **[Required gates](#required-gates)** — Reject stale documentation automatically.
- **[Change checklist](#change-checklist)** — Match changes with commands.

## Source rules

- RTL comments own module interface facts.
- Generator scripts own derived diagrams.
- Draw.io files own editable manual diagrams.
- WaveDrom JSON owns timing diagrams.
- Markdown owns reader guidance.
- Rendered files never own source facts.

Never hand-edit generated renders.

## Module documentation

The matrix derives relationships from repository sources.

```sh
python3 docs/traceability/gen_module_matrix.py
python3 docs/traceability/gen_module_matrix.py --check
```

Run both after relevant tree changes.

## Headless HDL reference

TerosHDL builds detailed module pages.

- Tool: [`gen_teroshdl.py`](../scripts/gen_teroshdl.py).
- Sources: first-party `hdl/` files.
- Output: one self-contained HTML file.
- Default: `/tmp/milan-teroshdl-doc/index.html`.
- Runtime: Node `22.23.2`.
- Version: TerosHDL `2.0.3`.
- CI verifies the official runtime archive checksum.

Install locked dependencies beneath `/tmp`:

```sh
tool_dir=/tmp/milan-teroshdl-tool
mkdir -p "$tool_dir"
cp tools/teroshdl/package.json tools/teroshdl/package-lock.json "$tool_dir/"
npm ci --ignore-scripts --audit=false --fund=false --prefix "$tool_dir"
```

Run from the repository root.

```sh
python3 scripts/gen_teroshdl.py \
  --documenter "$tool_dir/node_modules/.bin/teroshdl-hdl-documenter"
```

- Choose an empty output directory.
- Nonempty destinations remain unchanged.
- Failed generations publish nothing.
- Generated HTML remains untracked.
- CI uploads validated HTML artifacts.
- Inspect browsers before sharing.

The wrapper validates source coverage:

- Expectations derive from current sources.
- Every supported module receives one validated SVG.
- Validators inspect SVG structure and graphical content.
- Source-specific fallbacks must name a current tracked declaration.
- Unrecorded diagram gaps stop generation.
- Interfaces lack standalone TerosHDL sections.
- Only first declarations receive file sections.
- Known exceptions remain exact.
- New exceptions stop generation.
- Absolute build paths stop generation.
- Active HTML content stops generation.

Two unreliable views remain disabled:

- Dependency graphs exceed readable widths.
- Their nodes expose temporary paths.
- FSM extraction drops additional module pages.
- WaveDrom remains timing authority.
- Draw.io remains architecture authority.

## Drawio diagrams

Prefer generators for source-derived facts.

```sh
python3 docs/DOC_MAP.gen.py
python3 docs/DOC_MAP.gen.py --check
python3 docs/DOC_MAP.gen.py --selftest
python3 docs/diagrams/submodule_boundaries.gen.py
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 docs/diagrams/submodule_boundaries.gen.py --selftest
```

The generators also write source-bound PNG renders.

They require `rsvg-convert`.

`PNG_MANIFEST.json` pins decompressed raster bytes.

- PNG compression changes remain acceptable.
- Local renderer pixels are never compared.
- Renderer changes may alter the pinned raster.
- Regenerate and visually approve those changes.

Directly export changed Draw.io masters.

```sh
render_dir=$(mktemp -d)
xvfb-run -a drawio --disable-gpu --export --format png \
  --crop --scale 2 --output "$render_dir/direct.png" \
  docs/diagrams/submodule_boundaries.drawio
xvfb-run -a drawio --disable-gpu --export --format pdf \
  --crop --output "$render_dir/native.pdf" \
  docs/diagrams/submodule_boundaries.drawio
```

Simulate an A4 landscape print.

```sh
pdftocairo -svg "$render_dir/native.pdf" "$render_dir/native.svg"
rsvg-convert -f pdf \
  --page-width 297mm --page-height 210mm \
  -w 277mm -h 160.73mm --left 10mm --top 24.635mm -a \
  "$render_dir/native.svg" -o "$render_dir/a4.pdf"
pdftoppm -png -r 150 -singlefile \
  "$render_dir/a4.pdf" "$render_dir/a4"
```

Inspect every direct export.

- Confirm all labels appear.
- Confirm all connectors remain visible.
- Confirm colors retain strong contrast.
- Confirm text survives A4 printing.
- Confirm no clipping occurs.
- Confirm source facts independently.

Keep temporary inspection files under `/tmp`.

Commit generators, masters, and requested renders together.

## Wavedrom timing

Use the pinned rendering package.

```sh
python3 -m venv /tmp/milan-wavedrom
/tmp/milan-wavedrom/bin/pip install wavedrom==2.0.3.post3
```

Install `rsvg-convert` separately.

Generate current timing diagrams.

```sh
/tmp/milan-wavedrom/bin/python3 scripts/gen_wavedrom.py \
  docs/diagrams/wd_axis_backpressure.json --background=white
/tmp/milan-wavedrom/bin/python3 scripts/gen_wavedrom.py \
  docs/diagrams/wd_cdc_handshake.json --background=white
```

Check committed sources and reviewed raster evidence.

```sh
/tmp/milan-wavedrom/bin/python3 scripts/gen_wavedrom.py \
  docs/diagrams/wd_axis_backpressure.json --background=white --check
/tmp/milan-wavedrom/bin/python3 scripts/gen_wavedrom.py \
  docs/diagrams/wd_cdc_handshake.json --background=white --check
```

- WaveDrom SVG output remains deterministic.
- PNG raster evidence uses the shared manifest.
- Different renderer versions may change raster output.
- Such changes require regeneration and visual approval.

White backgrounds protect dark-theme readability.

Legacy diagrams retain their existing background behavior.

- Limit diagrams to essential signals.
- Label only important edges.
- Verify timing against RTL.
- Inspect every generated PNG.
- Check readability at reduced width.

## Historical pages

Move obsolete pages into versioned history.

Use [`history/v1/README.md`](history/v1/README.md) as the ledger.

Every historical page needs these fields.

> Status: Historical
>
> Original path: repository-relative path
>
> Archived: YYYY-MM-DD
>
> Relocated: YYYY-MM-DD
>
> Current successor: repository-relative link

- Preserve the obsolete first-line marker.
- Preserve original content afterward.
- Update current inbound links.
- Label every historical link visibly.
- Never delete non-#259 historical evidence.

Issue #259 is the deliberate exception.

Superseded target-only material is absent from this checkout.

It remains available only in Git history.

Never move that material under `docs/history/`.

Preserve the archive for unrelated obsolete evidence.

## Required gates

Run focused documentation checks first.

```sh
python3 scripts/docs_check.py
python3 scripts/docs_check.py --selftest
python3 scripts/check_doc_style.py
python3 scripts/check_doc_style.py --selftest
python3 scripts/check_solution_docs.py
python3 scripts/check_solution_docs.py --selftest
python3 scripts/check_submodule_docs.py
python3 scripts/check_submodule_docs.py --selftest
python3 scripts/check_diagram_pngs.py
python3 scripts/check_diagram_pngs.py --selftest
python3 scripts/check_archive.py
python3 scripts/check_archive.py --selftest
python3 scripts/gen_teroshdl.py --selftest
python3 scripts/check_doc_paths.py
python3 scripts/check_feature_status.py --self-test
python3 docs/traceability/gen_module_matrix.py --check
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --check
```

Run generator checks for changed diagrams.

Hosted documentation CI repeats these checks.

## Change checklist

| Changed source | Required action |
|---|---|
| RTL or test structure | Regenerate the module matrix |
| HDL documentation comments | Regenerate and inspect TerosHDL HTML |
| Draw.io generator | Regenerate master, SVG, and PNG |
| Manual Draw.io master | Export and inspect PNG and PDF |
| WaveDrom JSON | Regenerate and inspect SVG and PNG |
| Current guide | Run concise-style checks |
| Archived page | Update metadata and history ledger |
| Submodule pin | Regenerate verified boundary documentation |
| Any Markdown | Run link and path checks |
| Any tracked text | Run the privacy scrub |
