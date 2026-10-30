# [A711] R1 register reference (#797): handoff

Status: REVIEW READY at the head below (local branch, not pushed; the manager pushes and opens the PR).
All 45 runnable docs-workflow steps rc 0 at the head.

- Branch `797-r1-regref`, eight commits on dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141` (still the dev tip at the time of writing).
- Head: `a8bcfba9426db350018c9cee95f4905fb364d8f0` (`receipts/gates/HEAD.txt`: the commit every gate receipt was produced on).
- Origin verified: `https://github.com/kebag-logic/milan-fpga.git`. No submodule was touched; `receipts/submodules.txt`
  records every submodule at its pin (no `+`, `-` or `U` prefix).

## Assignment as read

- Section 2 of the owner scope addition (issuecomment-6522974767): the TRM-style register reference, generated from
  `hdl/common/csr/milan_csr.sv` and the SoC's `csr.csv`, with a freshness gate; plus section 1's rule (the page joins
  `check_doc_style.py` `DOCUMENTS`).
- The R1 rule of the 13:40 addition (issuecomment-6523093123): each register's bit-field diagram rendered by WaveDrom
  `reg` from the generator, one generated source per module, listed in `docs/diagrams/README.md`; a generated memory-map
  block diagram.
- The [A10] scope addition (issuecomment-6489587365): ETH_GUARD and the link controls.
- D0's REGISTER_MAP findings (PR #815 head `3e6d92c1`, `scripts/docs_inventory.json`; findings file `reference.md`).
- The newest [A10] comment (issuecomment-6523632193) is lane G1 for [A712]; not this lane's work (stated in TAKEN).
- TAKEN: issuecomment-6523912851. REVIEW READY: issuecomment-6529024576.

## Commits

| Commit | Subject |
|---|---|
| `60e8e62c` | Generate the Milan CSR register reference from milan_csr.sv and a builder export, with WaveDrom reg diagrams and a memory-map diagram (#797) |
| `ee682570` | Regenerate REGISTER_MAP.md in the TRM layout from the RTL and list its diagram sources; builder gate 18a reads the generated reset column (#797) |
| `bf5be176` | Gate the register reference in the docs workflow and hold REGISTER_MAP.md to the concise-prose rule (#797) |
| `67bd0722` | Carry the old register-group summaries into their modules, name undriven stored words after their register, and correct D0's REGISTER_MAP_CLASSES findings with the ETH_GUARD row (#797) |
| `462a0732` | Write the edited REGISTER_MAP_CLASSES row's separator as -- under the added-line em-dash rule (#797) |
| `dc6ec69b` | Split load_rtl's decode and table parsing into helpers and pass an array's geometry as one pair, under the Python idiom ratchets (#797) |
| `b6fd7631` | Explain the R/W1C and R/W1S codes and stored reserved bits in the legend, and state what preamble_crc reports (#797) |
| `a8bcfba9` | Spell description links from the repository root and resolve the shape include from the RTL's own include lines, so the entity-shape consumer inventory sees no unresolved header path (#797) |

## Changes (file:line, reason)

| File:line | Change | Reason |
|---|---|---|
| `scripts/gen_register_reference.py:78` `build_model` | entry point: reads the RTL facts, the SoC extract, the descriptions and the feature ledger | the generator #797 section 2 asks for |
| `scripts/gen_register_reference.py:127` `validate` | refuses a description of a register, field, CSR, bank or region the RTL or the export lacks (exit 2) | "a descriptions file ... the generator refuses to accept for a register or field the RTL lacks" |
| `scripts/gen_register_reference.py:161` `build_modules` | every register must sit in exactly one module range, else exit 2 | the A10 bullet "fail on any register the map is missing" |
| `scripts/gen_register_reference.py:202` `outputs` | renders page, per-module WaveDrom sources, SVGs and the catalog block; runs `check_doc_style.analyze`, the em-dash check and an anchor-uniqueness check on the page before writing | the generator never writes a page the docs gates refuse |
| `scripts/gen_register_reference.py:249` `stale`, `:313` `main` | `--check` (any byte difference, missing or extra diagram = exit 1), `--write`, `--selftest`, `--soc-from DIR` | the freshness gate |
| `scripts/register_rtl.py:664` `load_rtl` (helpers `decodes` :613, `tables`) | parses `milan_csr.sv`: `A_*` offsets, `csr_default`, `is_plain_rw`, every `if (!aresetn)` reset block, the write decodes (`register_write`, `pp_regs`), the read decodes (`read_mux`, `pp_read`, `strm_read_mux`), output assigns, declarations; a small SV constant evaluator | the RTL is the source of truth |
| `scripts/register_rtl.py:726` `extract_soc`, `:791` `csr_parameters` | reads a builder export (`csr.csv`, `aem_desc.json`, the datapath parameters in the generated top Verilog) and resolves `milan_csr`'s parameters through `milan_datapath`'s instance | the shipping build's reset values (PTP_INCR at 50 MHz, CHMAP_RDBK 3, gPTP plane on) |
| `scripts/register_fields.py:107` `Deriver` | per-bit derivation: read source, write effect (store, W1C, W1S strobe, key compare, guarded or masked store), name (output port, setter event, storage, constant), reset (defaults ROM, reset block, X for a live input) | field names and access are RTL facts, not hand-kept data |
| `scripts/register_fields.py:670` `array_registers` | STATn, the CBS queue words, LTAP/APRB words, the reserved gap, the window counters; refused when the RTL range term is gone | arrays have no case label |
| `scripts/register_page.py:445` `render_page` | owner layout: memory map, module summaries, `ACRONYM register (offset 0xNNN) [reset = 0xNNNNNNNN]`, diagram, field table, notes, access legend, build parameters, LiteX banks, feature block from the ledger | issuecomment-6522974767 section 2 |
| `scripts/register_page.py:135` `side_effect_text` | generates the ETH_GUARD unlock-key sentence (`0x554E4C4B`, ASCII `UNLK`) and "while it is 1, writes to PHY_RESET are dropped; LINK_CTRL[1] is stored as 0" from the decodes | A10 addition: the ETH_GUARD row with its unlock word and masks, generated |
| `scripts/register_page.py:376` `cbs_table` | the per-queue CBS reset table from `CBS_*_RST` | builder gate 22 reads it |
| `scripts/register_selftest.py:72` | 16 planted controls on the workflow's own `--check` entry | evidence the gate can fail |
| `scripts/register_map_soc.json` | SoC extract (generated by `--soc-from` from the shipping AX7101 export at this head) | CI cannot run LiteX |
| `scripts/register_descriptions.json:1529,1560,2816` | prose keyed by RTL register/field: names, purposes, field texts, notes; MAC_STATUS, PHY_RST, ETH_GUARD texts at these lines. Link targets are written from the repository root; the renderer makes them page-relative | the only hand-kept input; `check_entity_shape.py` resolves every shape-header path a tracked file names |
| `docs/diagrams/memory_map.gen.py` | Draw.io + SVG block diagram of regions, windows, modules, LiteX banks; `--check` | owner 13:40 addition |
| `docs/diagrams/regmap/*.json` (34), `regmap/<module>/*.svg` (202) | one generated WaveDrom source per module and one SVG per register | owner 13:40 addition |
| `docs/reference/REGISTER_MAP.md` | regenerated (generated banner, Contents table, 34 modules, 202 registers) | replaces the hand-written page |
| `docs/diagrams/README.md:46,76` | `memory_map` catalog row; generated "Register bit fields" block; Contents separators written `--`; regeneration commands | catalog rule; em-dash rule for re-rendered entries |
| `docs/reference/REGISTER_MAP_CLASSES.md:83,84,100,102,110,131` | D0-042, D0-041, D0-040, D0-018 (new ETH_GUARD row, links the generated section), D0-043, D0-044 | D0 findings; no rewrite, page not added to `DOCUMENTS` |
| `.github/ci-templates/docs.yml:457`, `.github/workflows/docs.yml:430` | new step "Register reference freshness gate" after "Entity shape gate" (workflow regenerated by `ci_gate_workflows.py`) | the gate runs on every PR |
| `scripts/ci_events.py:1168` | the step pinned in docs-check's list; seven step counts 51 -> 52 | the contract gate pins every step |
| `ci/image/command-table.json:5801` | three `python3` argv patterns; `scripts/gen_register_reference.py` and `docs/diagrams/memory_map.gen.py` pinned as reviewed non-installing (sha256) | the closed command table |
| `scripts/check_doc_style.py:37` | `docs/reference/REGISTER_MAP.md` joins `DOCUMENTS` | owner section 1 |
| `sw/builder/test_builder.py:20546` | gate 18a reads the generated summary row (`| 0x680 | LWSRP_CTRL | name | 0x00000010 |`) and the 8-digit reset; the RTL comparison is unchanged | the page format changed; the gate keeps its strength |

## Generator and freshness gate

- Inputs: `hdl/common/csr/milan_csr.sv`, `hdl/common/csr/gen/lwsrp_csr_defaults.svh`,
  `configs/generated/endstation_ax7101_1x1_tdm8/gen/adp_shape_defaults.svh`, `hdl/milan/milan_datapath.sv` (the
  `milan_csr` instance), `hdl/common/ethernet_packet_pkg.sv`, `scripts/register_map_soc.json`,
  `scripts/register_descriptions.json`, `docs/reference/milan_feature_status.json`.
- Outputs: `docs/reference/REGISTER_MAP.md`, `docs/diagrams/regmap/**`, the catalog block in `docs/diagrams/README.md`;
  `docs/diagrams/memory_map.{svg,drawio}` from `memory_map.gen.py`.
- Gate (docs workflow step "Register reference freshness gate"):
  `python3 scripts/gen_register_reference.py --check`, `--selftest`, `python3 docs/diagrams/memory_map.gen.py --check`.
- Self-test: 16 controls, each a temporary copy of the inputs with one planted defect, run through the same `--check`
  entry (receipt `receipts/gates/46-register-reference-freshness-gate.txt`):
  fresh copy (rc 0); RTL field rename of an undescribed field (rc 1 STALE page); RTL field rename of a described
  field (rc 2, refused description); reset-value change in `csr_default` (rc 1); reset-value change in the reset block
  (rc 1); ETH_GUARD unlock-key change in the write decode (rc 1); new address inside a module (rc 1); new address
  outside every module (rc 2); hand edit of the page (rc 1); deleted diagram (rc 1); extra diagram (rc 1); edited
  WaveDrom source (rc 1); edited SoC extract (rc 1); description of an unknown register (rc 2); of an unknown field
  (rc 2); description breaking the prose rules (rc 2).
- In-tree planted stale-page mutants on the committed head (receipts `receipts/mutants/`): an RTL field rename and a
  `csr_default` reset change each make `--check` exit 1 naming the stale page; each restore returns 0 with a clean tree.
- The SoC half: CI cannot run a LiteX export, so the extract is committed and generated, never hand-written.
  `--check --soc-from <export>` re-extracts and fails on any difference; run it whenever the SoC build changes
  (receipt `receipts/mutants/soc-from-check.txt`).

## Findings closed, per area (reference)

| Finding | Page:line (base) | Closed by |
|---|---|---|
| D0-006 | REGISTER_MAP.md:1226 | "802.1Q 35.2.2.7.2 (Table 35-3)" in the LWSRP_STATUS text |
| D0-007 | REGISTER_MAP.md:1286 | "IEEE 1722.1-2021 Table 7-156, Milan v1.2 Table 5.6" |
| D0-008 | REGISTER_MAP.md:199 | the old Contents block is not carried; the statement no longer exists |
| D0-009 | REGISTER_MAP.md:423 | publication only while the saved-state writer runs, else the reset value |
| D0-014 | REGISTER_MAP.md:1427 | ETH_GUARD 0x7D8 generated: reset 1, unlock key, PHY_RESET drop, LINK_CTRL[1] mask, link guard not gated |
| D0-015 | REGISTER_MAP.md:419 | PHY_RESET documented inert; `milan_mac_phy_crg_reset` documented as the real PHY reset |
| D0-016 | REGISTER_MAP.md:752 | LINK_CTRL[1] masked while ETH_GUARD[0] = 1 (generated from the decode) |
| D0-017 | REGISTER_MAP.md:416 | MAC_STATUS: mirror of `milan_mac_link_status`, reset link up/1000/FD, pointers to LINKG_STAT, counters, BMSR |
| D0-057 | REGISTER_MAP.md:137 | 2 ms is the default; SET_STREAM_INFO sets each Stream Output's offset |
| D0-058 | REGISTER_MAP.md:1327 | bindings persist through the processor's restore walk and `KL_nvm_backend` (#70) |
| D0-059 | REGISTER_MAP.md:1374 | this retired face no longer serves 5.3.8.2; the saved-state store does |
| D0-060 | REGISTER_MAP.md:1578 | the shipping AX7101 is the one-stream shape; the 8x8 yaml declares 8 |
| D0-018, D0-040, D0-041, D0-042, D0-043, D0-044 | REGISTER_MAP_CLASSES.md | see the change table |
| A10 ETH_GUARD / PHY_RESET / LINK_CTRL[1] / milan_mac_phy_crg_reset / MAC_STATUS / gate | issuecomment-6489587365 | all six bullets; the gate is `build_modules` + the self-test's address controls |

Count: 12 REGISTER_MAP.md findings and 6 REGISTER_MAP_CLASSES.md findings closed; 6 of 6 A10 bullets.
After this PR and #815 both land, D0's `scripts/docs_inventory.json` must drop these 18 entries and the audit page be
regenerated (an area lane that fixes a statement removes its entry; this branch does not carry D0's data file).

## Dropped statements from the old page

The survival check (`tools/survival.py`, receipt `receipts/survival.txt`) splits the old page (minus Contents and the
regenerated feature block) into 1,612 fragments: 1,600 are on the new page verbatim. The 12 that are not, and why:

| Old statement (base line) | Why dropped |
|---|---|
| `# Milan TSN CSR - register map (ABI)` (1) | title of the generated page is "Milan CSR register reference"; the ABI statement survives in the notes |
| "VERSION `0x0002_0055` adds lane 4 for `gptp_ctl_mux` ..." (139) | reworded "minor `0x0055` adds lane 4"; the feature-status gate refuses a non-canonical `0x0002_00xx` claim |
| "presentation-time offset is pinned at the Milan 2 ms default" (137) | D0-057: contradicted by the 0x0053 entry (SET_STREAM_INFO served) |
| "`[0]` phy_reset_n (0 = hold PHY in reset)" (419) | D0-015: `o_phy_reset_n` (milan_csr.sv:2692) is unconnected in `sw/litex/milan_soc.py` |
| "Bare-metal firmware publishes PHY state into LiteX `milan_mac.link_status`." (423) | D0-009: kept with the condition `milan_baremetal.c` imposes (`phy_link_tick()` inside `nvm_heartbeat_tick()`) |
| "Physical switch-cycle acceptance remains on #599." (428) | #599 is closed; the sentence links the #599 link-cycle finding |
| "802.1Q 35.2.2.7.4 FourPackedEvents" (1227) | D0-006: no such clause |
| "(STREAM_INPUT[0], Milan Table 7-156)" (1286) | D0-007: the table is IEEE 1722.1-2021's |
| "Nothing in this device persists a binding across a power cycle." (1327) | D0-058: `KL_pp_shadow.sv:1123` instantiates `KL_nvm_backend`; the paragraph after it is kept as the dated record |
| "Milan v1.2 5.3.8.2 ... is not met by this build." (1374) | D0-059 |
| "and the shipping AX7101 shape is 8" (1578) | D0-060: `sw/litex/build.sh:378` ships `endstation_ax7101_1x1_tdm8` |
| "[`../limitations/TROUBLESHOOTING.md`] Section 21" (1856) | rewritten as an anchored link (docs_check's un-anchored section-pointer rule fires once the line break that hid it is gone) |

The old Acc/Reset columns are replaced by generated values. `tools/compare_old.py` (receipt `receipts/compare-old.txt`)
compares all 227 rows: 222 agree. The five that do not, with the RTL line, plus MAC_STATUS, whose old reset was
not a value at all:

| Register | Old | RTL | Line |
|---|---|---|---|
| CLKV_CTRL | RW inert | R: no write arm; the read arm returns 0 | milan_csr.sv:1732, 2434 |
| ASP_LO, ASP_HI | RW inert | R: read arm returns 0, no write arm | milan_csr.sv:2362 |
| I2SPB_STAT | RO/W1C | R/W1C (the same thing) | milan_csr.sv:1775, 2409 |
| CHMAP_SNAP | reset `0xC500_0000` | `0xC5000300`: `CHMAP_RDBK_C` sits at [9:8] and the shipping datapath passes `CHMAP_RDBK_P(3)` | milan_csr.sv:1283, milan_datapath.sv:2656 |
| MAC_STATUS | reset `–` | `0x0000000X` from this block; the SoC's CSR resets it to 0xD on the AX7101 | milan_soc.py `link_status` |

## Gate table

Every step of `.github/ci-templates/docs.yml` (jobs docs-check, wire-accountability, docs-check-no-git) run on
the committed head `a8bcfba9`, one `bash -e` script per step, output captured to a file (never piped). Setup steps
(pip/apt installs, the sv2v download, submodule fetches) are not rerun: the scratch environment provides them and
every submodule is at its pin. The RV32 SDK steps use the pinned SDK installed by `scripts/ci_rv32_sdk.py` under a
scratch HOME (the host's copy has no provenance receipt). The em-dash base is `1e80128f` (the merge base); the
git-free job runs in a `git archive` export. Runner: `tools/run_gates.py`.

| Step | Job | Name | Result | Time | Receipt |
|---|---|---|---|---|---|
| 0 | docs-check | Build the validated HDL reference | rc=0 | 2s | `gates/00-build-the-validated-hdl-reference.txt` |
| 1 | docs-check | Install the python gate dependencies | not rerun (setup step) | - | - |
| 2 | docs-check | Install the pinned Markdown renderer | not rerun (setup step) | - | - |
| 3 | docs-check | Install diagram gate dependencies | not rerun (setup step) | - | - |
| 4 | docs-check | Link health, wording, dead-reference and local-info gate | rc=0 | 8s | `gates/04-link-health-wording-dead-reference-and-local-info-gate.txt` |
| 5 | docs-check | Added-line em-dash gate | rc=0 | 6s | `gates/05-added-line-em-dash-gate.txt` |
| 6 | docs-check | Concise audience documentation gate | rc=0 | 1s | `gates/06-concise-audience-documentation-gate.txt` |
| 7 | docs-check | Audience diagram no-drift gate | rc=0 | 2s | `gates/07-audience-diagram-no-drift-gate.txt` |
| 8 | docs-check | Product solution source-fact gate | rc=0 | 3s | `gates/08-product-solution-source-fact-gate.txt` |
| 9 | docs-check | Verified submodule documentation gate | rc=0 | 2s | `gates/09-verified-submodule-documentation-gate.txt` |
| 10 | docs-check | HDL timing diagram no-drift gate | rc=0 | 2s | `gates/10-hdl-timing-diagram-no-drift-gate.txt` |
| 11 | docs-check | Published diagram PNG gate | rc=0 | 8s | `gates/11-published-diagram-png-gate.txt` |
| 12 | docs-check | Milan feature-status consistency gate | rc=0 | 1s | `gates/12-milan-feature-status-consistency-gate.txt` |
| 13 | docs-check | Traceability matrix no-drift gate | rc=0 | 1s | `gates/13-traceability-matrix-no-drift-gate.txt` |
| 14 | docs-check | Fetch the builder source dependencies | not rerun (setup step) | - | - |
| 15 | docs-check | Imported gPTP documentation gate | rc=0 | 1s | `gates/15-imported-gptp-documentation-gate.txt` |
| 16 | docs-check | Code-quality measurement self-tests | rc=0 | 0s | `gates/16-code-quality-measurement-self-tests.txt` |
| 17 | docs-check | Install the pinned sv2v release | not rerun (setup step) | - | - |
| 18 | docs-check | Bare-metal scope gate | rc=0 | 33s | `gates/18-bare-metal-scope-gate.txt` |
| 19 | docs-check | Install and verify the pinned RV32 SDK | rc=0 | 2s | `gates/19-install-and-verify-the-pinned-rv32-sdk.txt` |
| 20 | docs-check | Compiler-absent firmware controls | rc=0 | 740s | `gates/20-compiler-absent-firmware-controls.txt` |
| 21 | docs-check | End-station builder gates | rc=0 | 1465s | `gates/21-end-station-builder-gates.txt` |
| 22 | docs-check | NVM record-space gate | rc=0 | 50s | `gates/22-nvm-record-space-gate.txt` |
| 23 | docs-check | Capture measurement census and clock gate | rc=0 | 1s | `gates/23-capture-measurement-census-and-clock-gate.txt` |
| 24 | docs-check | Saved-state writer gate | rc=0 | 172s | `gates/24-saved-state-writer-gate.txt` |
| 25 | docs-check | SoC source-list gate (Vivado would fail 40 min in without this) | rc=0 | 2s | `gates/25-soc-source-list-gate-vivado-would-fail-40-min-in-without-thi.txt` |
| 26 | docs-check | RTL source-list drift gate | rc=0 | 5s | `gates/26-rtl-source-list-drift-gate.txt` |
| 27 | docs-check | Boundary-unit naming ratchet | rc=0 | 1s | `gates/27-boundary-unit-naming-ratchet.txt` |
| 28 | docs-check | Port contract gate | rc=0 | 6s | `gates/28-port-contract-gate.txt` |
| 29 | docs-check | Fail-fast ratchet | rc=0 | 4s | `gates/29-fail-fast-ratchet.txt` |
| 30 | docs-check | TODO ownership gate | rc=0 | 4s | `gates/30-todo-ownership-gate.txt` |
| 31 | docs-check | Test-evidence ratchet | rc=0 | 17s | `gates/31-test-evidence-ratchet.txt` |
| 32 | docs-check | Mechanical hygiene ratchet | rc=0 | 1s | `gates/32-mechanical-hygiene-ratchet.txt` |
| 33 | docs-check | SystemVerilog idiom gate | rc=0 | 1s | `gates/33-systemverilog-idiom-gate.txt` |
| 34 | docs-check | C and C++ idiom gate | rc=0 | 4s | `gates/34-c-and-c-idiom-gate.txt` |
| 35 | docs-check | Python idiom gate | rc=0 | 10s | `gates/35-python-idiom-gate.txt` |
| 36 | docs-check | Shell idiom gate | rc=0 | 0s | `gates/36-shell-idiom-gate.txt` |
| 37 | docs-check | CI event and SHA contract gate | rc=0 | 178s | `gates/37-ci-event-and-sha-contract-gate.txt` |
| 38 | docs-check | Local act runner contract gate | rc=0 | 96s | `gates/38-local-act-runner-contract-gate.txt` |
| 39 | docs-check | Doc cited-path gate | rc=0 | 0s | `gates/39-doc-cited-path-gate.txt` |
| 40 | docs-check | Archive integrity gate | rc=0 | 1s | `gates/40-archive-integrity-gate.txt` |
| 41 | docs-check | Per-page contents gate | rc=0 | 10s | `gates/41-per-page-contents-gate.txt` |
| 42 | docs-check | AEM store generator self-test | rc=0 | 0s | `gates/42-aem-store-generator-self-test.txt` |
| 43 | docs-check | Sweep/build shape gate | rc=0 | 12s | `gates/43-sweep-build-shape-gate.txt` |
| 44 | docs-check | Deploy shape gate | rc=0 | 0s | `gates/44-deploy-shape-gate.txt` |
| 45 | docs-check | Entity shape gate | rc=0 | 67s | `gates/45-entity-shape-gate.txt` |
| 46 | docs-check | Register reference freshness gate | rc=0 | 5s | `gates/46-register-reference-freshness-gate.txt` |
| 47 | docs-check | CI scheduling and evidence controls | rc=0 | 29s | `gates/47-ci-scheduling-and-evidence-controls.txt` |
| 48 | wire-accountability | Fetch the engine authority the builder derives from | not rerun (setup step) | - | - |
| 49 | wire-accountability | Advertised-vs-emitted gate (green since 2026-07-28, item 00) | rc=0 | 1s | `gates/49-advertised-vs-emitted-gate-green-since-2026-07-28-item-00.txt` |
| 50 | docs-check-no-git | Strip git metadata, then run the docs gate | rc=0 | 9s | `gates/50-strip-git-metadata-then-run-the-docs-gate.txt` |

45 steps rc 0, 0 not rc 0, 6 setup steps not rerun.


Also on this head:

| Check | Result | Receipt |
|---|---|---|
| full behave suite (`cd tests && behave --no-capture -f plain`, rtl-fast bdd-conformance) | rc 0, 495 scenarios | `behave/full-suite.txt` |
| `behave tests/features/counters_contract_milan.feature` (reads the page) | rc 0, 88 scenarios | `behave/counters_contract_milan.txt` |
| command-table walk of the new step (`tools/walk_regref_step.py`) | rc 0, no residue | `command-table/walk-step-final-head.txt` |
| walk negative control: a planted unlisted subprocess form in `register_page.py` | refused (on `bf5be176`, same scripts' walk path) | `command-table/walk-step-negative-control.txt` |
| in-tree mutant: RTL field rename (`o_tcam_wr_action`) | planted rc 1, restored rc 0 | `mutants/rtl-field-rename.txt` |
| in-tree mutant: `csr_default` reset change (MAC_IFG 0x0C to 0x0D) | planted rc 1, restored rc 0 | `mutants/reset-value-change.txt` |
| in-tree mutant: hand edit of the page | planted rc 1, restored rc 0 | `mutants/page-hand-edit.txt` |
| in-tree mutant: description of a field the RTL lacks | planted rc 2, restored rc 0 | `mutants/unknown-field-description.txt` |
| `--check --soc-from` the shipping export / an export copy with one bank moved | rc 0 / rc 1 | `mutants/soc-from-check.txt` |
| survival of the old page's statements | 1,600 of 1,612 fragments verbatim | `survival.txt` |
| old Acc/Reset columns against the RTL | 222 of 227 agree | `compare-old.txt` |

## Open risks and decisions

1. ETH_GUARD and the LiteX PHY reset: the A10 bullet and the RTL comments (`o_eth_guard` port, `A_ETH_GUARD` banner)
   say the guard gates `milan_mac_phy_crg_reset`; `sw/litex/milan_soc.py` exports the level and consumes nothing. The page
   states the code. Decision needed: implement the gating (an RTL/SoC issue) or correct the two comments.
2. Lane conflict with PR #815: both add a docs-check step (51 -> 52). Whichever lands second renumbers to 53 in
   `scripts/ci_events.py` and regenerates `.github/workflows/docs.yml`; it also drops the 18 closed entries from
   `scripts/docs_inventory.json` and reruns `python3 scripts/docs_inventory.py --write`.
3. Any change to `milan_csr.sv` that moves a documented fact now needs `python3 scripts/gen_register_reference.py
   --write` in the same PR (that is the gate's purpose). A change to the SoC build needs a builder export and
   `--soc-from`; CI cannot see SoC drift by itself.
4. `scripts/register_descriptions.json` is ~300 KB, not small: it carries the old page's still-true facts verbatim
   (every row and paragraph, the VERSION changelog split by minor). A later lane can move history to the design pages.
5. Live-input fields show reset `X` (set by the producing block); the page does not claim the producers' resets except
   where the old page did (kept as notes or the LTAP "Producer reset" column).
6. `ci_scope.py` lists `docs/reference/REGISTER_MAP.md` among gate-read docs, so the hosted RTL aggregates run on this
   PR; the full Verilator sweep and Yosys were not run locally (documentation lane, no full sweep by instruction).
7. `REGISTER_MAP_CLASSES.md` was corrected, not rewritten, and is not added to `DOCUMENTS` (its prose would need a
   rewrite to pass the 10-word rule).
