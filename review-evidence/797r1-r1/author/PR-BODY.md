[A711]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

GREEN locally: every docs-workflow gate command passes at the head (rc 0, outputs not piped), plus the full
behave suite (495 scenarios). Branch `797-r1-regref` -> `dev`, eight commits on `1e80128f`.

## Linked Issue / roles

Relates to #797

Executor: `[A711]`
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Description

The register reference is now generated from the RTL, in the layout of a technical reference manual
(lane R1 of #797, owner scope addition section 2 and the 13:40 diagram rule).

| Piece | What it does |
|---|---|
| `scripts/gen_register_reference.py` (+ `register_rtl.py`, `register_fields.py`, `register_page.py`, `register_selftest.py`) | Reads `hdl/common/csr/milan_csr.sv` (offsets, defaults ROM, reset blocks, write and read decodes, output assigns), its generated includes and the `milan_csr` instance in `milan_datapath`, and derives every field per bit: name (the RTL output port, setter event or storage), access (R, W, R/W, W1C, W1S, key-compared, guarded or masked writes), reset (defaults ROM, reset block, or X for a live input). |
| `scripts/register_map_soc.json` | The SoC facts from the shipping AX7101 builder export at this head (`csr.csv`, `aem_desc.json`, datapath parameters), written by `--soc-from`, never by hand. |
| `scripts/register_descriptions.json` | The only hand-kept input: prose keyed by RTL register and field name. The generator refuses a key the RTL lacks. It carries every still-true statement of the old page (1,600 of its 1,612 fragments verbatim). |
| `docs/reference/REGISTER_MAP.md` | Regenerated: memory map, module summaries, one section per register (`ACRONYM register (offset 0xNNN) [reset = 0xNNNNNNNN]`, purpose, WaveDrom `reg` diagram, field table, notes), access legend, build parameters, LiteX banks, feature-status rows from the ledger. Inbound anchors are kept. |
| `docs/diagrams/regmap/` | One generated WaveDrom source per CSR module (34) and one SVG per register (202), listed in `docs/diagrams/README.md` by a generated block. |
| `docs/diagrams/memory_map.gen.py` | Generated Draw.io and SVG block diagram of the regions, windows, CSR modules and LiteX banks. |
| docs workflow | New step "Register reference freshness gate": `--check` fails on any difference (page, sources, SVGs, catalog block); `--selftest` runs 16 planted controls; the memory-map `--check`. Step pinned in `scripts/ci_events.py`, commands registered in `ci/image/command-table.json`. |
| `scripts/check_doc_style.py` | `docs/reference/REGISTER_MAP.md` joins `DOCUMENTS`. |
| `sw/builder/test_builder.py` | Gate 18a reads the generated summary row and 8-digit reset; its RTL comparison is unchanged. |
| `docs/reference/REGISTER_MAP_CLASSES.md` | D0-018 (ETH_GUARD row), D0-040 to D0-044 corrected; not rewritten. |

Closed: D0-006, -007, -008, -009, -014, -015, -016, -017, -057, -058, -059, -060 on `REGISTER_MAP.md`; D0-018,
-040, -041, -042, -043, -044 on `REGISTER_MAP_CLASSES.md`; all six bullets of the ETH_GUARD and link-control
addition. The ETH_GUARD row's unlock word (`0x554E4C4B`) and its masks (PHY_RESET writes dropped, LINK_CTRL[1]
stored as 0) are generated from the write decode.

Planted controls (run by `--selftest` through the workflow's own `--check` entry): an RTL field rename, a
renamed described field, reset-value changes in the defaults ROM and in the reset block, an unlock-key change, a
new address inside and outside every module, a hand edit, deleted, extra and edited diagrams, an edited SoC
extract, and descriptions of an unknown register, an unknown field and over-long prose. Each fails with the
expected verdict; the fresh copy passes.

## Authoritative references

- #797: owner scope additions (section 1 short paragraphs, section 2 register reference), the 13:40 diagram rule,
  the ETH_GUARD and link-control addition, D0's REGISTER_MAP findings on PR #815.
- `hdl/common/csr/milan_csr.sv`, `hdl/milan/milan_datapath.sv` (the `milan_csr` instance),
  `sw/litex/milan_soc.py` (`link_status`, the exported guard), `sw/firmware/milan_baremetal/milan_baremetal.c`.
- IEEE 1722.1-2021 Table 7-156; Milan v1.2 Table 5.6, 5.3.8.2; IEEE 802.1Q 35.2.2.7.2 (Table 35-3).
- `docs/diagrams/README.md` (diagram rules), CONTRIBUTING.md section 6 and 6.1.

## How to get into the same state

```sh
git fetch origin
git checkout 797-r1-regref
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack
python3 -m pip install wavedrom==2.0.3.post3 pyyaml
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

To refresh the SoC extract after a SoC change, export the shipping build without Vivado and re-extract:

```sh
python3 sw/builder/endstation_builder.py configs/endstation_ax7101_1x1_tdm8.yaml
sw/litex/deploy.sh build --dry-run
# run the printed milan_soc.py line without --build, with --output-dir <export>
python3 scripts/gen_register_reference.py --write --soc-from <export>
```

## How to validate

```sh
python3 scripts/gen_register_reference.py --check
python3 scripts/gen_register_reference.py --selftest
python3 docs/diagrams/memory_map.gen.py --check
python3 scripts/check_doc_style.py
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
python3 scripts/check_doc_paths.py
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --check
python3 scripts/check_feature_status.py --self-test
python3 sw/builder/test_builder.py --require-rv32
python3 scripts/ci_events.py --check
cd tests && behave --no-capture -f plain
```

Expected result / pass criteria: every command exits 0. `--selftest` prints 16/16 controls. Planting an RTL
field rename or a reset-value change in `milan_csr.sv` makes `--check` exit 1 naming the stale page.

## Known limitations / out of scope

- ETH_GUARD and the LiteX PHY reset: the RTL comments say the guard gates `milan_mac_phy_crg_reset`, but the SoC
  consumes nothing at this head. The page states the code; the gating or the comment fix needs a decision.
- CI cannot run a LiteX export, so the SoC extract is committed. `--check --soc-from <export>` proves it against a
  fresh export; SoC drift is caught when someone runs that, not by CI alone.
- Live inputs show reset `X`: the producing block sets them, not the register file.
- The descriptions file is large because it carries the old page's still-true facts; moving history out is later
  work.
- Lane conflict with PR #815: both add a docs-check step. Whichever lands second renumbers the step count and
  drops the closed REGISTER_MAP entries from D0's data file.
- `REGISTER_MAP_CLASSES.md` is corrected, not rewritten, so it does not join the concise-prose gate.
- The full Verilator sweep and Yosys were not run locally (documentation lane).

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
