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

## 1. Module ↔ spec ↔ test matrix

**Tool:** [`traceability/gen_module_matrix.py`](traceability/gen_module_matrix.py)
**Masters:** the RTL tree (`hdl/`), the TB tree (`tb/verilator/`), the
per-standard clause tables in [`traceability/`](traceability/MODULE_MATRIX.md).
**Outputs:** [`traceability/MODULE_MATRIX.md`](traceability/MODULE_MATRIX.md)
(all 77 modules) plus a generated `README-tests.md` in every `hdl/` leaf.

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
generic, port and signal (see [`../CONTRIBUTING.md`](../CONTRIBUTING.md) §1).

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
box; the repo's minimal renderer
(`hdl/ieee17221/aecp/doc/atdecc_architecture.render.py`) works for
plain-label files but mangles HTML-formatted labels — verify its output.

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
```

[`../scripts/docs_check.py`](../scripts/docs_check.py) enforces four rules
over every tracked `*.md` (plus diagram sources for the last one): relative
links must resolve; the wording deny-list; a mentioned doc must be a real
link (generated files and [`../historical_now_obsolete/`](../historical_now_obsolete/README.md)
are exempt); and no bench/host-identifying information (hostnames, home
paths, serials, bench IPs). The exact allowlist is in the script header.
Both commands run in CI on every push to `main` and every PR
([`../.github/workflows/docs.yml`](../.github/workflows/docs.yml)) — run them
locally first, exit-checked, never piped through `tail`.

## 6. Cheat sheet — you changed X, run Y

| You changed… | Run |
|---|---|
| RTL module / TB dir / clause table | `gen_module_matrix.py` (then `--check`) |
| A module's `//!` comments | TerosHDL "Save documentation" on that `.sv` |
| A `.gen.py` or `.drawio` diagram master | the `.gen.py` (or draw.io export) + `rsvg-convert`; update the catalog |
| A `wd_*.json` chronogram | `scripts/gen_wavedrom.py` on it; inspect the png |
| Any `*.md` at all | `scripts/docs_check.py` before pushing |
