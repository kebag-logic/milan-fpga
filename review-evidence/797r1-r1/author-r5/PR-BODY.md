[A711e]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Round 5](#round-5)** -- How R753-4 F1 was fixed: the SRP-served clause states every case that clears the word.
- **[Round 4](#round-4)** -- How R753-3 F1 and R754-3 F1 were fixed, and what the 17-table sweep found.
- **[Round 3](#round-3)** -- How each finding of R753-2 and R754-2 was fixed.
- **[Round 2](#round-2)** -- How each finding of R753-1 and R754-1 was fixed.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

GREEN locally at the head: every docs-workflow step that can run outside GitHub is rc 0 on a clean clone, 61 of 61 generator controls pass, and the read-table sweep gives 0 disagreements over all 17 read tables on the shipping and a 2x2 build, 48,007 reads each. Branch `797-r1-regref` -> `dev`, with dev `1f29f189` merged and one merge base.

## Linked Issue / roles

Relates to #797

Executor: `[A711e]`
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
| `scripts/register_read_sweep.py` | Not a gate. Builds `milan_csr` with Verilator at the shipping parameters and at 2x2, drives selection and state, and checks every read against the page's 17 read tables, each clause read as printed from the harness's record of what it did. |
| `scripts/register_descriptions.json` | The hand-kept prose, keyed by RTL register and field. A key the RTL lacks is refused, and a register with no name or purpose is refused. |
| `scripts/register_map_soc.json` | The SoC facts of the shipping AX7101 builder export, written by `--soc-from`. |
| `docs/reference/REGISTER_MAP.md` | Generated: memory map, module summaries, one section per register with a WaveDrom `reg` diagram and a field table, access legend, build parameters, LiteX banks, feature rows. |
| `docs/design/CSR_REGISTER_NOTES.md` | The rationale, dated findings and version log the old page carried. A record, not generated, linked from each module and register. |
| `docs/diagrams/regmap/`, `docs/diagrams/memory_map.gen.py` | One generated WaveDrom source per module and one SVG per register, a digest of the CSR sources, and the memory-map block diagram. |
| docs workflow | Step "Register reference freshness gate": `--check`, `--selftest`, the memory-map `--check`. |
| `scripts/check_doc_style.py` | `docs/reference/REGISTER_MAP.md` is in `DOCUMENTS`. |

Fixed on `REGISTER_MAP.md` and `REGISTER_MAP_CLASSES.md`: D0-006 to -009, -014 to -018, -040 to -044, -057 to -060, and all six bullets of the ETH_GUARD and link-control addition. The page states the code: nothing in the SoC consumes the guard.

## Round 5

R754-4 was POSITIVE. R753-4 was NEGATIVE with one MINOR, F1: the SRP-served clause omitted two cases that clear the word. This round fixes that clause and the sweep that read it. It changes no other row, adds no gate and merges no dev. No RTL changed.

| Commit | Finding | Fix | Check |
|---|---|---|---|
| `f24695e4` | R753-4 F1 | `srp_fresh_r`'s wording pair now states every clearing case of `milan_csr.sv:3108-3133`. The clause reads "the SRP table's latest answer to the window was a poll, after the last `STRM_SEL`/`STRMW_CTRL` write, with no other master using the table since", with its negation. It is regenerated in `STRMW_SID_LO`, `STRMW_SID_HI` and both `STRMW_SRP` rows | `--write` leaves the tree clean, then `--check` is fresh |
| `ef7dc985` | R753-4 F1 | The sweep records the table's answers, the `STRM_SEL`/`STRMW_CTRL` writes and other masters' beats by clock edge. The clause is read from that record in the page's words. Four new states: a poll answered after the write then its write answered, the same with the write unanswered, a poll then another master's beat, and that beat then a poll | 0 disagreements on both builds, 48,007 reads each. The old wording planted back exits 1 with 288 disagreements |

The reviewer's probe, rerun on the head with its sequences unchanged, agrees with the new rows in all 25 states, including the four it marked. The `f7f6ea7d` row of round 4 names the weaker clause; it is kept as that round's record. The suggestions of R753-4 were not taken.

## Round 4

Both reviews of `e90284bd` were NEGATIVE with one MINOR each, on read-table rows false as printed. Both had one cause: the published sweep read a clause by the flop the generator worded, not by the words on the page, and it left five tables out. This round fixes that sweep first, then every row it finds false. It moves no text between pages and adds no gate and no diagram. No RTL changed.

| Commit | Finding | Fix | Check |
|---|---|---|---|
| `fd12faf9` | The class behind both | `scripts/register_read_sweep.py` reads all 17 tables on both builds. Each clause maps to what the harness did or read back through a register. An unknown clause refuses, and a new table is read without an edit | On the `e90284bd` page: 64 disagreements on shipping, 256 on 2x2. Planted wrong rows exit 1 |
| `7c508db4` | R753-3 F1 | `STRMW_SRP`'s field row and read rows state `STRM_SEL[9]` by its value, with the finding's wording | `SEL` `0x300` agrees on both builds |
| `dbe2b143` | R754-3 F1 | The generator reads `RENDER_STAT`'s listener loop as one selection. The row is the finding's: "the selected stream exists and `STRM_SEL[8]` selects a listener" | 0 disagreements on 2x2, where `e90284bd` gave 96 |
| `f7f6ea7d` | Found by the sweep | Three tables said "the SRP table answered since the last selection". An answer to a provisioning write leaves the word 0 (`milan_csr.sv:3113-3115`, `:3120-3128`). The clause now names a poll answer since the last `STRM_SEL` or `STRMW_CTRL` write | `STRMW_SID_LO`, `STRMW_SID_HI` and `STRMW_SRP` at 0 |
| `79fdea05` | Found by the sweep | `CHMAP_LOOP` said "a channel-map readback has completed". A re-arm clears the valid bit (`milan_csr.sv:2773`), and a timeout leaves it 0. The rows now state `CHMAP_SNAP[1]` by its value | `CHMAP_LOOP` at 0 on both builds |

Per table, the sweep's disagreements at `e90284bd`, then at the head:

| Table | Shipping | 2x2 |
|---|---|---|
| `STRMW_SID_LO`, `STRMW_SID_HI` | 0, 0 | 24 each, 0 |
| `STRMW_SRP` | 60, 0 | 108, 0 |
| `RENDER_STAT` | 0, 0 | 96, 0 |
| `CHMAP_LOOP` | 4, 0 | 4, 0 |
| The other 12 | 0, 0 | 0, 0 |

The suggestions of both reports, and the carried ones, were not taken.

## Round 3

Both reviews of `96bfa851` were NEGATIVE with MINOR findings on what the page states. Their generator, gate and simulation results stood. This round fixes statements. It moves no text to other pages, and adds no gate and no diagram. No RTL changed.

| Finding | Fix | Check |
|---|---|---|
| Read conditions lose their grouping (R753 F4, R754 F4) | `read_rows` prints each read value's shortest conjunctions, one per row, drops a row no state reaches, and prints "any other case" for the constant taking the most rows | A sweep of 12 of the 17 tables over `milan_csr`: 1,152 reads, 0 disagreements, with each clause read as the flop it names. The same compare on the previous page: 360. A selftest arm, killed by 4 generator mutants. Round 4 extends the sweep to all 17 tables and reads each clause as printed |
| `MAC_STATUS` publication (R753 F1, R754 F1) | Firmware publishes on each boot path reaching `nvm_boot()`; nothing writes it after a CSR identity mismatch | `milan_baremetal.c:950-953`, `:1099-1102`, `:1671` |
| Entity enable (R753 F2, R754 F6) | Either bit requests the enable. The fabric holds it until the restore releases it, and CLOSED holds it until reset | `protocol_processor_top.sv:2027`, `milan_datapath.sv:9586`, `milan_baremetal.c:1846-1849` |
| REBOOT hold (R753 F3, R754 F7) | `milan_mac_phy_crg_reset` states the set, the hold and the one-cycle CPU clear, and links the design page | `milan_soc.py:2115-2132`, `docs/design/REBOOT_RESET.md:163-164` |
| `ADP_CMD` rows (R753 F5, R754 F3) | Inert strobes that self-clear and read 0 | `milan_csr.sv:1799-1802`; simulated read of 0x640 |
| `PP_NVM_STAT` strobes (R754 F2) | Each strobe named in the row of its own bit, and `[1:0]` named. A reserved writable field on a word whose write leaves the block refuses | `KL_nvm_backend.sv:455-462`, `:593-599`; a control and a mutant |
| `STRM_SEL[9]` (R754 F5) | It also moves `STRMW_SRP` off the alias on the talker side at index 0 | `milan_csr.sv:2528`, `:2574-2576`; simulated reads at `SEL` `0x100` and `0x300` |
| Residue (R753 R1 to R3, R754 R1 to R5) | The reports' exact wording. A note holding a Markdown table refuses | Read at each line; a control and a mutant |

The suggestions were not taken: they are optional, and two would change diagrams.

## Round 2

Both reviews of `a8bcfba9` were NEGATIVE. Both confirmed offsets, access codes and numeric resets. Every finding below was fixed by round 2's head, except S4.

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

- #797: owner scope additions (section 1 short paragraphs, section 2 register reference), the 13:40 diagram rule, the ETH_GUARD and link-control addition, D0's REGISTER_MAP findings on PR #815, R753-1 to R753-4 and R754-1 to R754-4.
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

The read-table sweep needs Verilator and a C++ compiler, and is not a gate:

```sh
python3 scripts/register_read_sweep.py
```

Expected result: every command exits 0. `--selftest` prints 61/61 controls. The sweep prints each table's reads and disagreements, then `0 disagreement(s)`. Planting a new register window, a flop reset change or a field rename in `milan_csr.sv` makes `--check` exit 1 or 2 naming it.

A plant driver that copies part of the tree needs `docs/design/CSR_REGISTER_NOTES.md`, `hdl/common/KL_link_guard.sv` and `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv`, which the generator now reads.

## Known limitations / out of scope

- **ETH_GUARD:** the RTL comments say the guard gates `milan_mac_phy_crg_reset`, but the SoC consumes nothing. The page states the code. The gating and the comments are not in this PR, and that decision stays open.
- **The design notes are not held to the concise-prose rule.** The page is a record, its banner says so, and it is not in `DOCUMENTS`. Rewriting it would be new work.
- **Mermaid is parsed by both reviewers, not rendered.** Read the page once on the PR.
- **`RANGE_ARRAYS` and `KNOWN_BUS_SITES` list RTL structure in the generator.** A new item refuses until the generator is taught it.
- **Any code change to `milan_csr.sv` needs `--write`,** because the digest asks a human to reread the prose it touches. A comment-only edit does not.
- **CI cannot run a LiteX export,** so SoC drift is caught by `--check --soc-from <export>`, not by the docs job alone.
- **Lane conflict with PR #815:** both add a docs-check step. Whichever lands second renumbers it, and D0's inventory must list the new design-notes page.
- **The read-table sweep is `milan_csr` alone,** with the engines replaced by answers on their ports. It deposits the counter kinds and the latched snapshot words. The datapath ties the SRP grant to 0, so SRP-answered states exist only in the harness. On the shipping build, 6 rows above index 0 are never reached.
- **Dev moved to `503bc97c` (PR #828) during round 4.** It touches none of this PR's files, the merge base is still `1f29f189`, and dev was not merged in rounds 4 or 5.
- **The statements about firmware, the SoC and the processor were read, not simulated.**
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
