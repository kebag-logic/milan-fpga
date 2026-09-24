# [A228] Commands and receipts (PR #538 correction round 1)

- Head: `26a0cc3042300d5213edf7b1c0037a3ae2612ecd`.
- Reviewed head: `196cb7d99cb06631df514715979a5f82fbb1f7aa`.
- Base: `759da623072358afdb0e9d570a7b4b6a788492c9`.
- `<packet>` is this directory. Its resolved path matters for the RV32 installer, which refuses a symlinked destination.

## Interpreters

```sh
python3 -m venv --system-site-packages <packet>/venv            # CPython 3.14.7
<packet>/venv/bin/python -m pip install --require-hashes -r tools/markdown/requirements.txt
<packet>/venv/bin/python -m pip install wavedrom==2.0.3.post3
<packet>/venv/bin/python -m pip install --require-hashes -r tools/hdl_reference/requirements.txt
python3.12 -m venv <packet>/venv312                             # CPython 3.12.13, lock only
<packet>/venv312/bin/python -m pip install --require-hashes -r tools/markdown/requirements.txt
```

## Gates (`gates/`)

- `gates/run_gates.sh <list>` runs each line from the lane with the venv's `python3` first on PATH. It appends `rc, seconds, command` to `gates/EXITS.txt` and keeps each output in `gates/logs/NNN.log`.
- The lists come from `.github/workflows/docs.yml`, read step by step: `commands-1.txt`, `commands-2.txt`, `commands-A.txt`, `commands-B.txt`, `commands-4b.txt`, `commands-5.txt` (no-git export) and `commands-6-py312.txt`.
- The RV32 SDK, compiler and builder steps run with `HOME=<packet>/scratch/home`, where the pinned SDK is installed and verified, as CI does on its runner.
- Result at the head: 96 runs, all rc 0.
- Earlier heads of the same commit are recorded, not reused:
  - `gates-attempt-6903f6f7/`: `docs_check` refused a bare reference.
  - `gates-attempt-edbe7f31/`: a rerun into a non-empty HDL-reference scratch directory and a symlinked SDK destination were refused, and a builder run was cut by the batch time limit. Each was rerun cleanly.

## Probes (`probes/`) and receipts (`receipts/`, all at `26a0cc30` unless named)

| Script | What it shows | Receipt |
|---|---|---|
| `forge_probe.py <repo>` | `headings()` for each forged spelling | (inline, superseded by the e2e below) |
| `emdash_e2e_spellings.py <py> <repo> <work> [rev]` | shipped em-dash gate, real commits, control plus four spellings | `emdash-e2e-spellings-at-26a0cc30.txt`, `...-at-196cb7d9.txt` |
| R238-4 `scripts/emdash_spoof_e2e.sh <py> <repo> <work>` | reviewer's own spoof probe | `r238-emdash-spoof-e2e-at-26a0cc30.txt` |
| R237-5 `scripts/probe_emdash_gate.py <export> <work> <py312>` | reviewer's own forged-position probe | `r237-probe-forged-position-emdash-at-26a0cc30.txt` |
| `deep_pages_gates.py <py> <repo> <work> <rev>` | both shipped gates on 1200-deep pages | `deep-pages-gates-196cb7d9-and-26a0cc30.txt` |
| `file_view_compare.py <old tree> <repo>` | each file-view page against GitHub at both heads | `file-view-196cb7d9-vs-26a0cc30.txt` |
| `tracked_compare.py <old tree> <repo>` | all 164 tracked pages under both heads | `tracked-pages-196cb7d9-vs-26a0cc30.txt` |
| `tracked_depth.py <repo>` | deepest tracked element, and what `--write` would touch | `tracked-depth-and-write-at-26a0cc30.txt` |
| `position_only_diff.py <repo> <pages.json>...` | positions are the only rendering difference | `position-only-difference-at-26a0cc30.txt` (shapes, fuzz and tracked) |
| `own_element_scan.py <repo> <pages.json>...` | which own-element drops change labels | `own-element-scan-at-26a0cc30.txt`, `partial-swallow-containers-at-26a0cc30.txt` |
| `mutate_a228.py <py> <repo> <work> <out.json>` | 23 mutants of this round's properties | `mutations-a228-at-26a0cc30.{txt,json}` |
| R238-4 `scripts/mutate.py <py> <repo> <work> <out>` | reviewer's campaign | `r238-mutations-at-26a0cc30.{txt,json}` |
| R237-5 `scripts/mutate.py`, `scripts/mutate_own_element.py <export> <work> <py312>` | reviewer's campaigns | `r237-mutations-at-26a0cc30.txt`, `r237-own-element-at-26a0cc30.txt` |

The `<old tree>` is `git archive 196cb7d9 scripts tools/markdown`. The `<export>` is `git archive HEAD`, which has no `.git` and no submodule content.

## GitHub renderings

- `probes/record.py <pages.json> <out.json>` sends each page with `gh api --method POST markdown --input -`. The exact JSON is kept in `request_bytes`: keys `context`, `mode` and `text`, context `kebag-logic/milan-fpga`, sorted keys, ASCII. The exact body returned is kept too.
- `render-cache/<request sha256>.{req,resp,meta}` holds all 40, so a rerun sends nothing already cached.
- `probes/pages_a228.py` builds the 21 fixture pages from the arm tables.
- `probes/write_fixture_a228.py` adds them to `scripts/gen_toc_shapes.json`: the gfm pages to `shapes` and the `markdown`-mode pages to `file_view`.
- `pages-depth*.json` hold the 19 depth probes.
