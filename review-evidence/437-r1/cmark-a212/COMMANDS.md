# Commands and receipts (A212, #437 and #516)

Head `196cb7d99cb06631df514715979a5f82fbb1f7aa`, tree `796c734682c7d7dc5c26fd9a92090a3c4a35fc32`, base `759da623072358afdb0e9d570a7b4b6a788492c9`.
Gate interpreter: a CPython 3.14.7 virtual environment with system site packages, the hash-locked
`tools/markdown/requirements.txt` installed (`pip install --require-hashes`), and `wavedrom==2.0.3.post3`
(as `docs.yml` installs it). The runner's CPython 3.12 was reproduced with a 3.12.13 environment carrying the same lock.

## Gates (all at the head)

`gates/EXITS.txt` lists the 72 commands with exit code and seconds; `gates/logs/NNN.log` holds each output.
`gates/commands.txt` and `gates/commands2.txt` are the exact lists; `scripts/gates.sh` runs them.
Every exit is 0.

Constraint checks at the head, in `gates/constraints/`:
- `no-git.log`: `docs_check.py` and `check_feature_status.py` in a `git archive` export with no `.git` (exit 0, 0);
- `no-submodules.log`: a fresh local clone with no submodule initialised runs `gen_toc.py --selftest/--verify-anchors/--check`
  and `check_em_dash.py --selftest/--base 759da623` (all exit 0);
- `python312.log`: the hosted runner's interpreter line, CPython 3.12.13 with the lock, runs the TOC gates and the
  em-dash selftest (all exit 0);
- `missing-renderer.log`: system CPython without the lock: exit 2 with the install command, for `gen_toc.py --check`,
  `--selftest` and `check_em_dash.py --selftest`, `--base`; `gen_toc` still imports without it (`check_hygiene.py` needs that);
- `drifted-release.log`: cmarkgfm 2025.10.20 installed: exit 2, refused by name.

## GitHub renderings

`scripts/record.py pages.json rendered.json` sends each page as
`gh api --method POST markdown --input -` with the exact JSON body kept in `request_bytes`
(`{"context":"kebag-logic/milan-fpga","mode":"gfm","text":...}`, sorted keys, ASCII) and keeps the exact body returned.
`render-cache/<request sha256>.{req,resp,meta}` holds every request and response byte and its UTC time, so a rerun sends
nothing that is cached. `RENDER_MODE=markdown` renders the same pages in the API's `markdown` mode (README-style, with
heading anchors). All renders are synthetic pages; no repository page was submitted.

- `pages.json` (352 shapes), assembled by `scripts/shape_list.py`: the pages of superseded PR #515's three fixtures,
  every page the R237 and R238 reports published (reconstructions marked), family two, every converted arm, the
  corpus-difference reproductions and the pages of the new I437 arms.
- `rendered.json`: their gfm renderings (2026-09-23); `scripts/write_fixture.py` writes `scripts/gen_toc_shapes.json` from it.
- `rendered-markdown-mode.json`: the same pages in `markdown` mode.
- `fuzz-pages-437212.json` (`scripts/fuzz_pages.py 437212 700`), `fuzz-rendered-437212.json` (gfm) and
  `fuzz-rendered-437212-markdown-mode.json`.

## Comparisons

- `scripts/compare.py <repo> rendered.json`: parser headings against gfm headings, per shape.
- `scripts/three_way.py <repo> <base scripts> <rendered>`: the base walk (dev 759da623's `gen_toc.py`), the renderer walk
  and GitHub. `three-way-shapes.json`: 221 agree at both, 131 fixed, 0 regressed, 0 wrong at both.
  `three-way-fuzz-437212.json`: 249, 451, 0, 0.
- `scripts/markdown_mode.py <repo> <markdown-mode renderings>`: headings and GitHub's file-view anchor ids.
  `markdown-mode-shapes.json`, `markdown-mode-fuzz.json`, `family-two-anchors.json`, `gfm-vs-markdown-mode.json`.
- `scripts/ac4_compare.py <repo> <base scripts> <tree>`: refusals, blocks, line kinds, headings with anchors, plan,
  existing block, ownership and generated block for every tracked page under both walks. `ac4-head-tree.*`,
  `ac4-base-tree.*` (dev 759da623) and `ac4-candidate-tree.*` (a scratch merge with live dev 26d855a9).
- `scripts/base_arms_under_new.py`: every base-era arm scored by the renderer walk; `converted-arms.json` lists the 42
  it answers differently, each of whose pages is in the fixture.

## Mutations

`scripts/mutate.py <repo> <python> <out> [ids]` applies each named mutation to a scratch copy of `scripts/` and
`tools/markdown/` and runs both shipped selftests. `mutations-final.json`: 30 of 30 fail the TOC selftest at arms named
for their property; M03-M06, M08, M10, M19-M22 and M26-M28 also fail the em-dash selftest. `mutations-round1.json` and
`mutations-round2.json` are the earlier rounds whose two survivors (M17 source order, M25 hash prefix) and one broken
mutant (M09) led to the footnote-order and non-sha256 hash arms and the corrected M09.

`MANIFEST.sha256` lists every file in this directory.
