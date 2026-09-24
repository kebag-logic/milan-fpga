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

`gen_toc.py` owns Contents provenance, not Markdown parsing.

GitHub's own renderer decides every heading and block.
It is cmark-gfm, read through the `cmarkgfm` binding.

html5lib then parses the HTML that cmark-gfm emits.
A heading counts only when both stages keep it.

- Lock: [`requirements.txt`](../tools/markdown/requirements.txt), hash-checked.
- Binding: `cmarkgfm` `2025.10.22`.
- Renderer: cmark-gfm `0.29.0.gfm.13`, inside that binding.
- HTML parser: `html5lib` `1.1`.
- Another release stops both gates by name.

Install the lock into the interpreter running documentation gates:

```sh
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

Hosted documentation CI installs the same lock first.

Its wheels cover CPython 3.12 and 3.14.
Other hosts add their wheel hashes from PyPI.

Setext headings and container headings now appear in Contents.

An ATX label still comes from its own line.
A setext label is its rendered text.

Raw HTML headings are never listed.
GitHub's hidden footnote label is never listed either.

A page able to forge the position attribute lists nothing.
Letter case, character references and backslash escapes all count.

A page nesting elements over 200 deep lists nothing.
GitHub drops everything from an element 256 deep.

Each limit withholds a heading and grants no exemption.

GitHub's file view reads some raw HTML differently.
[CONTRIBUTING.md](../CONTRIBUTING.md) 6.1 measures that difference and its direction.

The refusal policy names 26 characters.
It also names the position attribute in any letter case.

Refusal binds both provenance and the base heading's authority.

[`gen_toc_shapes.json`](../scripts/gen_toc_shapes.json) records GitHub renderings.
The self-test compares every shape with the renderer.

Its file-view pages keep GitHub's anchors for withheld cases.

Synthetic inputs and renderer receipts stay outside tracked Markdown.

## Module documentation

The matrix derives relationships from repository sources.

```sh
python3 docs/traceability/gen_module_matrix.py
python3 docs/traceability/gen_module_matrix.py --check
```

Run both after relevant tree changes.

## Headless HDL reference

A first-party generator builds detailed module pages.

- Tool: [`gen_hdl_reference.py`](../scripts/gen_hdl_reference.py).
- Sources: first-party `hdl/` files.
- Output: one self-contained HTML file.
- Default: `/tmp/milan-hdl-reference/index.html`.
- Parser: `pyslang` `11.0.0`, hash-locked.
- Lock: [`requirements.txt`](../tools/hdl_reference/requirements.txt).

Install the locked parser beneath `/tmp`:

```sh
python3 -m venv /tmp/milan-hdl-reference-tool
/tmp/milan-hdl-reference-tool/bin/pip install --require-hashes \
  -r tools/hdl_reference/requirements.txt
```

Run from the repository root.

```sh
/tmp/milan-hdl-reference-tool/bin/python3 scripts/gen_hdl_reference.py
```

- Choose an empty output directory.
- Nonempty destinations remain unchanged.
- Failed generations publish nothing.
- Generated HTML remains untracked.
- CI uploads validated HTML artifacts.
- Inspect browsers before sharing.

The generator validates source coverage:

- Expectations derive from current sources.
- Two independent source front ends must agree.
- Every supported module receives one validated SVG.
- Validators inspect SVG structure and graphical content.
- Interfaces lack standalone sections.
- Only first declarations receive file sections.
- Known exceptions remain exact.
- New exceptions stop generation.
- A drifted parser release stops generation.
- Absolute build paths stop generation.
- Active HTML content stops generation.

### Dependency posture

Issue #300 replaced the legacy documenter graph.

- The retired node graph carried thirteen advisories.
- One retired advisory was critical.
- The pinned parser has zero known advisories.
- Audit evidence: `pip-audit`, 2026-09-02.
- Re-evaluate on each parser release.
- Re-evaluate on any new parser advisory.

Two legacy documenter views stay retired:

- Dependency graphs exceeded readable widths.
- Their nodes exposed temporary paths.
- FSM extraction dropped additional module pages.
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
python3 docs/diagrams/timesync_chain.gen.py
python3 docs/diagrams/timesync_chain.gen.py --check
python3 docs/diagrams/timesync_chain.gen.py --selftest
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
/tmp/milan-wavedrom/bin/python3 scripts/gen_wavedrom.py \
  docs/diagrams/wd_gptp_pdelay.json --background=white
```

Check committed sources and reviewed raster evidence.

```sh
/tmp/milan-wavedrom/bin/python3 scripts/gen_wavedrom.py \
  docs/diagrams/wd_axis_backpressure.json --background=white --check
/tmp/milan-wavedrom/bin/python3 scripts/gen_wavedrom.py \
  docs/diagrams/wd_cdc_handshake.json --background=white --check
/tmp/milan-wavedrom/bin/python3 scripts/gen_wavedrom.py \
  docs/diagrams/wd_gptp_pdelay.json --background=white --check
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

Install the locked Markdown renderer before these checks.

```sh
python3 scripts/docs_check.py
python3 scripts/docs_check.py --selftest
python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
python3 scripts/check_em_dash.py --selftest
python3 scripts/check_doc_style.py
python3 scripts/check_doc_style.py --selftest
python3 scripts/check_gptp_docs.py
python3 scripts/check_gptp_docs.py --selftest
python3 scripts/check_solution_docs.py
python3 scripts/check_solution_docs.py --selftest
python3 scripts/check_submodule_docs.py
python3 scripts/check_submodule_docs.py --selftest
python3 docs/diagrams/timesync_chain.gen.py --check
python3 docs/diagrams/timesync_chain.gen.py --selftest
python3 scripts/check_diagram_pngs.py
python3 scripts/check_diagram_pngs.py --selftest
python3 scripts/check_archive.py
python3 scripts/check_archive.py --selftest
/tmp/milan-hdl-reference-tool/bin/python3 scripts/gen_hdl_reference.py --selftest
python3 scripts/check_doc_paths.py
python3 scripts/check_feature_status.py --self-test
python3 docs/traceability/gen_module_matrix.py --check
python3 scripts/gen_toc.py --selftest
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --check
```

Run generator checks for changed diagrams.

Hosted documentation CI repeats these checks.

## Change checklist

| Changed source | Required action |
|---|---|
| RTL or test structure | Regenerate the module matrix |
| HDL documentation comments | Regenerate and inspect the HDL reference |
| Draw.io generator | Regenerate master, SVG, and PNG |
| Manual Draw.io master | Export and inspect PNG and PDF |
| WaveDrom JSON | Regenerate and inspect SVG and PNG |
| Current guide | Run concise-style checks |
| Archived page | Update metadata and history ledger |
| Submodule pin | Regenerate verified boundary documentation |
| Any Markdown | Run link and path checks |
| Any tracked text | Run the privacy scrub |
