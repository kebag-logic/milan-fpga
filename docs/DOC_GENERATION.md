<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->
# Generating the documentation — every generator in one page

A large part of this doc set is **generated, not written**: the module↔spec↔test
matrix, the per-module HDL pages, every diagram render, and the waveform
chronograms. This page says which tool produces what, the exact command, and
when you must re-run it.

The one rule behind all of them: **edit the master, never the render.** Masters
are the RTL `//!` comments, the `*.gen.py` scripts, the `.drawio` files and the
WaveDrom `.json` files. Rendered `.svg`/`.png` and generated `.md` are outputs;
hand-edits there are lost on the next run and fail review.

## Contents

- **[1. Module ↔ spec ↔ test matrix](#1-module--spec--test-matrix)** — The generator behind [`MODULE_MATRIX.md`](traceability/MODULE_MATRIX.md) and the `README-tests.md` in every `hdl/` leaf. Run it after *any* RTL or TB tree change; the `--check` form is what fails CI when the committed output has gone stale.
- **[2. Per-module HDL pages (hdl/**/doc/*.md)](#2-per-module-hdl-pages-hdldocmd)** — Driven from the editor via TerosHDL, because there is no headless path on this box. The honest coverage number is here: ~22 of 84 modules have pages while 82 of 84 already carry the `//!` comments, so the backlog is an editor session, not a writing task.
- **[3. Block diagrams (.gen.py → .drawio + .svg → .png)](#3-block-diagrams-genpy--drawio--svg--png)** — The render chain, the four artifacts that must be committed together, and the catalog entry that goes with them. Two headless caveats: the drawio CLI hangs, and the repo's fallback renderer mangles HTML-formatted labels.
- **[4. Waveform chronograms (WaveDrom)](#4-waveform-chronograms-wavedrom)** — `gen_wavedrom.py` over a `wd_*.json`, with the `wavedrom` package living in the LiteX venv. Includes the style rules learned the hard way: cap at ~10 lanes, write explicit `010` pulses instead of `H`, and look at the rendered `.png` before embedding it.
- **[5. The gate and CI](#5-the-gate-and-ci)** — The five rules `docs_check.py` enforces, spelled out. Rule 4 is the one to know — a dead reference left behind by a deletion used to pass silently, so retiring a document now means adding its basename to `RETIRED`. Also covers the no-git fallback and the single opt-out token.
- **[6. Cheat sheet — you changed X, run Y](#6-cheat-sheet--you-changed-x-run-y)** — Seven rows mapping what you touched to the one command that has to follow. The fastest way to use this page if you are already mid-change.

## 1. Module ↔ spec ↔ test matrix

**Tool:** [`traceability/gen_module_matrix.py`](traceability/gen_module_matrix.py)
**Masters:** the RTL tree (`hdl/`), the TB tree ([`tb/verilator/`](../tb/verilator)), the
per-standard clause tables in [`traceability/`](traceability/MODULE_MATRIX.md).
**Outputs:** [`traceability/MODULE_MATRIX.md`](traceability/MODULE_MATRIX.md)
(the generator prints the live total — 82 modules on 2026-07-26) plus a generated `README-tests.md` in every `hdl/` leaf.

```sh
python3 docs/traceability/gen_module_matrix.py           # regenerate
python3 docs/traceability/gen_module_matrix.py --check   # no-drift gate (CI runs this)
# same, via make (from tb/verilator/tsn_fuzz/): make matrix / make matrix-check
```

Run it after **any** RTL or TB tree change — adding a module, renaming a
harness, touching a clause row. The `--check` form fails CI when the committed
outputs are stale.

## 2. Per-module HDL pages (`hdl/**/doc/*.md`)

**Tool:** the TerosHDL documenter (VS Code extension).
**Masters:** the `//!` documentation comments the house style requires on every
generic, port and signal (see [Section 1 of `../CONTRIBUTING.md`](../CONTRIBUTING.md#1-hdl-house-style-cemal-dogan--oguz-kahraman-school)).

How to generate a page: open the module's `.sv` in VS Code with the TerosHDL
extension installed, run its **"Save documentation"** action, and save the
markdown (plus the schematic SVG it draws) into the module's `doc/` directory.
The page-header convention is the one
[`hdl/common/csr/doc/milan_csr.md`](../hdl/common/csr/doc/milan_csr.md) uses.

Two honest caveats:

- There is **no headless CLI path on this box today** — the documenter is
  Node-based and Node is not installed here; generation goes through the
  editor.
- Coverage is partial: roughly 22 of 84 modules have pages. The `//!` source
  coverage is 82 of 84, so the regeneration backlog is an editor session, not
  a writing task. Newly generated pages must use repo-relative links at the
  right depth — [`../scripts/docs_check.py`](../scripts/docs_check.py) catches
  the classic `../../../`-off-by-one.

## 3. Block diagrams (`.gen.py` → `.drawio` + `.svg` → `.png`)

**Masters:** a checked-in generator script (`*.gen.py`, e.g.
[`DOC_MAP.gen.py`](DOC_MAP.gen.py)) or, for the two hand-drawn ones, the
`.drawio` file itself. The perf diagrams use the tiny shared builder
[`diagrams/svglib.py`](diagrams/svglib.py).

```sh
# the common shape (each script prints its own usage line):
python3 docs/DOC_MAP.gen.py docs/DOC_MAP
rsvg-convert -w 2400 docs/DOC_MAP.svg -o docs/DOC_MAP.png
```

Commit all of: the `.gen.py`, the `.drawio`, the `.svg`, the `.png` — and
register the diagram in the catalog,
[`diagrams/README.md`](diagrams/README.md) (what it shows, editable source,
renders, embed sites). Caveat: the drawio desktop CLI hangs headless on this
box, and the repo's own minimal drawio renderer was **deleted on 2026-08-13**
with the AECP doc tree it lived in. Render with `rsvg-convert`, which is what
every catalog entry in `diagrams/README.md` now names.

## 4. Waveform chronograms (WaveDrom)

**Tool:** [`../scripts/gen_wavedrom.py`](../scripts/gen_wavedrom.py).
**Master:** the WaveDrom `.json` under [`diagrams/`](diagrams/README.md)
(`wd_*.json`) — the standard, easily-modifiable timing-diagram format.

```sh
~/litex-milan/venv/bin/python3 scripts/gen_wavedrom.py docs/diagrams/wd_cbs_credit.json
# emits wd_cbs_credit.svg + wd_cbs_credit.png next to the json
```

The `wavedrom` package lives in the LiteX venv (`pip install wavedrom`
elsewhere). Style rules learned the hard way: at most ~10 lanes, annotate only
the load-bearing edges, prefer explicit `010` pulses over the `H` wave
character (it renders oddly in this renderer), and **look at the rendered
`.png` before embedding it** — a mangled render does not ship. Every timing
edge must be derived from the RTL or a named doc, never invented.

## 5. The gate and CI

```sh
python3 scripts/docs_check.py                            # exit 0 or it lists findings
python3 docs/traceability/gen_module_matrix.py --check   # matrix no-drift
python3 sw/builder/test_builder.py                       # end-station builder gates
```

[`../scripts/docs_check.py`](../scripts/docs_check.py) enforces five rules
over every `*.md` in the tree (plus diagram sources for the last one):

1. relative links must resolve;
2. the wording deny-list;
3. a mentioned doc that **exists** must be a real link (generated files and
   [`../historical_now_obsolete/`](../historical_now_obsolete/README.md) are exempt);
4. a mentioned doc that **does not exist** is a *dead reference* — either a path
   inside this repo that is not there, or a document listed as retired in the
   script's `RETIRED` set. Rule 3 cannot see these, so a reference left behind by
   a deletion used to survive the gate silently; it no longer does. Sibling-repo
   paths are left alone (the rule only fires when the reference's parent
   directory is a real directory of this repo). One document opts out — the
   archive ledger, whose job *is* to name retired
   files — via an HTML-comment line carrying the token
   `docs-check: allow-dead-refs`;
5. no bench/host-identifying information (hostnames, home paths, serials, bench IPs).

The exact allowlist and the `RETIRED` set are in the script header. **The gate
does not need git**: inside a git working tree it takes the file list from
`git ls-files`, and otherwise falls back to a `.gitignore`-aware filesystem walk,
printing which source it used — so it runs identically in an extracted tarball or
a downloaded zip. When you retire a document, add its basename to `RETIRED` and
the gate will find every reference left pointing at it.

All three commands run in CI on every push to `main` and every PR
([`../.github/workflows/docs.yml`](../.github/workflows/docs.yml)), which also
re-runs the docs gate a second time with `.git` deleted to keep the no-git path
honest — run them locally first, exit-checked, never piped through `tail`.

## 6. Cheat sheet — you changed X, run Y

| You changed… | Run |
|---|---|
| RTL module / TB dir / clause table | `gen_module_matrix.py` (then `--check`) |
| A module's `//!` comments | TerosHDL "Save documentation" on that `.sv` |
| A `.gen.py` or `.drawio` diagram master | the `.gen.py` (or draw.io export) + `rsvg-convert`; update the catalog |
| A `wd_*.json` chronogram | [`scripts/gen_wavedrom.py`](../scripts/gen_wavedrom.py) on it; inspect the png |
| Deleted or archived a doc | add its basename to `RETIRED` in [`scripts/docs_check.py`](../scripts/docs_check.py), then run the gate — it lists every reference now pointing at nothing |
| A config schema / builder emission | [`sw/builder/test_builder.py`](../sw/builder/test_builder.py); an explicit `--write-fragment` or `--write-rtl` transfer generates paired `aem_desc.bin`, `aem_desc.json`, and `aem_desc.map` artifacts beside the bitstream. The board-side `aemi-load` verifies and writes the image before entity enable |
| Any `*.md` at all | [`scripts/docs_check.py`](../scripts/docs_check.py) before pushing |
