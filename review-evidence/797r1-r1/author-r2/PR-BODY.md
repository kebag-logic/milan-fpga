[A711b]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Round 2](#round-2)** -- How each finding of R753-1 and R754-1 closed.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

GREEN locally at the head: every docs-workflow step that can run outside GitHub is rc 0 on a clean clone, 58 of 58 generator controls pass, and both reviewers' plants have 0 misses. Branch `797-r1-regref` -> `dev`, with live dev `1f29f189` merged and one merge base.

## Linked Issue / roles

Relates to #797

Executor: `[A711b]`
Internal cleared-context reviewer: `[R753]`
External reviewer: `[R754]`

## Description

The register reference is generated from the RTL, in the layout of a technical reference manual (lane R1 of #797, owner scope addition section 2 and the 13:40 diagram rule).

| Piece | What it does |
|---|---|
| `scripts/register_sv.py` | Reads the block's SystemVerilog subset. Anything outside it is a refusal. Computes values in three-valued logic, and runs a decode with the address known. |
| `scripts/register_decode.py` | Runs the block's own read decodes per address. Gives the reset value of every word, every value a read can return and under which condition, the address census, the range terms and the flop-against-ROM check. |
| `scripts/register_fields.py`, `scripts/register_rtl.py` | Read the RTL's facts and derive every field per bit: name, access, reset, side effects. A write or read form outside the grammar is refused. |
| `scripts/register_page.py`, `scripts/register_diagrams.py` | Render the page and ten generated mechanism diagrams, with every label checked against the RTL. |
| `scripts/gen_register_reference.py` | The entry point: `--write`, `--check`, `--selftest`, `--soc-from DIR`. |
| `scripts/register_descriptions.json` | The hand-kept prose, keyed by RTL register and field. A key the RTL lacks is refused, and a register with no name or purpose is refused. |
| `scripts/register_map_soc.json` | The SoC facts of the shipping AX7101 builder export, written by `--soc-from`. |
| `docs/reference/REGISTER_MAP.md` | Generated: memory map, module summaries, one section per register with a WaveDrom `reg` diagram and a field table, access legend, build parameters, LiteX banks, feature rows. |
| `docs/design/CSR_REGISTER_NOTES.md` | The rationale, dated findings and version log the old page carried. A record, not generated, linked from each module and register. |
| `docs/diagrams/regmap/`, `docs/diagrams/memory_map.gen.py` | One generated WaveDrom source per module and one SVG per register, a digest of the CSR sources, and the memory-map block diagram. |
| docs workflow | Step "Register reference freshness gate": `--check`, `--selftest`, the memory-map `--check`. |
| `scripts/check_doc_style.py` | `docs/reference/REGISTER_MAP.md` is in `DOCUMENTS`. |

Closed on `REGISTER_MAP.md` and `REGISTER_MAP_CLASSES.md`: D0-006 to -009, -014 to -018, -040 to -044, -057 to -060, and all six bullets of the ETH_GUARD and link-control addition. The page states the code: nothing in the SoC consumes the guard.

## Round 2

Both reviews of `a8bcfba9` were NEGATIVE. Both confirmed offsets, access codes and numeric resets. Every finding below is closed at this head, except S4.

| Finding | Fix | Check |
|---|---|---|
| Reset says X on words the RTL fixes (R753 F1, R754 F3) | Reset is computed by running the read decode in the reset state. `X` only on a bit an input or an unreset flop sets. `CHMAP_LOOP` reads `0xDEADDEAD`. `PTP_PPS_CTRL[0]` is `R-0` at `PPS_P` = 0 | Both reviewers' simulations rerun: the only such row is `RST_EPOCH`, which has no reset clause |
| A window can be added under a green gate (R753 F2, R754 F1) | Case labels, range terms, address tests and CSR-bus sites are all checked; a scan of 0x000 to 0xFFC refuses a decoded word with no register. 0x86C now has a section | 45 and 39 reviewer plants: 0 misses; the comment-only control stays fresh |
| A flop reset can drift from the ROM (R753 F3, R754 F1) | Each shadow-served or ROM-named word's flop is compared with the ROM, and a difference refuses | `mac_ifg`, `mac_ctrl`, `scratch`, `tcam_ctrl`, `LWSRP_LATENCY_RST_C` controls |
| An unread form publishes a wrong page (R753 F4, R754 F1) | A write or read outside the grammar refuses. `CHMAP_LOOP` fields come from the RTL | Both write forms exit 2 on `--write` |
| Behaviour changes stay fresh (R754 F1) | Multi-value words print every value by condition. A digest of the comment-stripped sources fails on a code change no text shows | Controls for the poison, the 0x86C value, `PPS_WIDTH`, the snapshot store, the SRP alias, `mac_ctrl[9]` |
| Side effects outside the row, conditions as pseudo-code (R753 F5, R754 F6) | Each side effect is in its field's row, each condition in plain words, refused when unworded. No row is empty | Row audit: 0 empty of 498 |
| The prose gate skips 55 % (R753 F6, R754 F2) | Notes render as paragraphs the gate reads. A one-column table refuses, and a cell over 200 words refuses. Rationale moved to the design notes | Reviewer probe: 0 findings, 0 Note tables |
| Carried prose false (R753 F7, R754 F4) | `STRMW_SRP`, `STRM_SEL`, unused bits, legacy legend, prune defaults corrected | Re-read against the cited lines |
| Memory-map overprint (R753 F8, R754 F5) | Plain labels; `--check` refuses one that would reach its address | Render inspected; a long label exits 2 |
| Mechanisms without diagrams (R754 F7) | Ten generated Mermaid diagrams, listed in the catalog | Controls: a label the RTL no longer backs refuses |
| Device labels (R754 F8) | Removed, with a bench MAC and a capture tool's name found by grep | Grep of the page, the notes and the descriptions |
| S1, S2, S3, residue R1 to R6 | Closed | S4 is RTL comments, outside this PR |

## Authoritative references

- #797: owner scope additions (section 1 short paragraphs, section 2 register reference), the 13:40 diagram rule, the ETH_GUARD and link-control addition, D0's REGISTER_MAP findings on PR #815, R753-1 and R754-1.
- `hdl/common/csr/milan_csr.sv`, `hdl/milan/milan_datapath.sv` (the `milan_csr` instance), `sw/litex/milan_soc.py` (`link_status`, the exported guard).
- IEEE 1722.1-2021 Table 7-156; Milan v1.2 Table 5.6, 5.3.8.2, 7.3.2; IEEE 802.1Q 35.2.2.7.2 (Table 35-3).
- `docs/diagrams/README.md` (diagram rules), CONTRIBUTING.md section 6 and 6.1.

## How to get into the same state

```sh
git fetch origin
git checkout 797-r1-regref
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack
python3 -m pip install wavedrom==2.0.3.post3 pyyaml
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

To refresh the SoC extract after a SoC change, export the shipping build without a place-and-route run and re-extract:

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
python3 scripts/ci_events.py --check
git diff --check "$(git merge-base origin/dev HEAD)" HEAD
cd tests && behave --no-capture -f plain features/counters_contract_milan.feature
```

Expected result: every command exits 0. `--selftest` prints 58/58 controls. Planting a new register window, a flop reset change or a field rename in `milan_csr.sv` makes `--check` exit 1 or 2 naming it.

A plant driver that copies part of the tree needs `docs/design/CSR_REGISTER_NOTES.md`, `hdl/common/KL_link_guard.sv` and `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv`, which the generator now reads.

## Known limitations / out of scope

- **ETH_GUARD:** the RTL comments say the guard gates `milan_mac_phy_crg_reset`, but the SoC consumes nothing. The page states the code. The gating and the comments are not in this PR, and that decision stays open.
- **The design notes are not held to the concise-prose rule.** The page is a record, its banner says so, and it is not in `DOCUMENTS`. Rewriting it would be new work.
- **Mermaid is not rendered locally.** No renderer is available without publishing the source. Read the page once on the PR.
- **`RANGE_ARRAYS` and `KNOWN_BUS_SITES` list RTL structure in the generator.** A new item refuses until the generator is taught it.
- **Any code change to `milan_csr.sv` needs `--write`,** because the digest asks a human to reread the prose it touches. A comment-only edit does not.
- **CI cannot run a LiteX export,** so SoC drift is caught by `--check --soc-from <export>`, not by the docs job alone.
- **Lane conflict with PR #815:** both add a docs-check step. Whichever lands second renumbers it, and D0's inventory must list the new design-notes page.
- **The full Verilator sweep and Yosys were not run locally** (documentation lane). No RTL changed.

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
