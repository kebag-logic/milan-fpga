# [A711b] R1 register reference (#797): handoff, round 2

Status: REVIEW READY at the head below. Local branch; the manager pushes.
Every docs-workflow step that can run here is rc 0 on a clean clone of the head.

- Branch `797-r1-regref`. Head `96bfa8513978ebc8c2f2e73bd98914b56e84bf12`, tree `816e6324dd4f2f38240faca3e85f547a85a32168` (`receipts/gates/HEAD.txt`).
- Base: live dev `1f29f189279f9fc0132f4918e47342b87d22f33a`, merged in `b01661c8`, and still the dev tip when the gates ended. `git merge-base --all origin/dev HEAD` gives that one base.
- Origin verified: `https://github.com/kebag-logic/milan-fpga.git`. Round 1 branched from dev `1e80128f`.
- Submodules at their pins: `gptp-processor` `135afd04`, `protocol-processor` `a9e84b66`, `third_party/tsn-c-stack` `70936b77`, `third_party/verilog-axis` `48ff7a7e`. The merge moved the first two; nothing else in them was touched.
- Receipts: `receipts/INDEX.md`, generated from the files present, with host paths replaced. Tools: `tools/`.

## Assignment as read

Round 2 of lane R1 of #797. Both reviews of `a8bcfba9` were NEGATIVE: R753-1 (issuecomment-6562673865) and R754-1 (issuecomment-6562982241). Both confirmed offsets, access codes and numeric resets. The faults were in the generator's cells, the gates and carried prose. The manager's rulings are applied as written. No RTL changed.

TAKEN: issuecomment-6563029259 (`taken_posted.md`). REVIEW READY: issuecomment-6565091854 (`review_ready_posted.md`).

## Changes (file:line, reason)

Line numbers are at the head. Round 1's table in `../797-a711/HANDOFF.md` still describes the pieces this round did not touch: the workflow step, the `ci_events.py` pin, builder gate 18a and `REGISTER_MAP_CLASSES.md`.

| File:line | Change | Reason |
|---|---|---|
| `scripts/register_sv.py` | New: expression and statement parser, three-valued evaluator, block interpreter | A form outside the grammar must refuse, and a reset must be computed, not guessed |
| `scripts/register_decode.py:191` | New: what a read of each address returns, and the census, range and flop checks | R753 F1 to F3, R754 F1, F3 |
| `scripts/register_rtl.py:410`, `:537` | Bus-site list, and decodes parsed to trees with labels checked | R753 F2, R754 F1 |
| `scripts/register_fields.py:476`, `:574` | Write decode walked as a tree; any other form refused | R753 F4, R754 F1 |
| `scripts/register_fields.py:837` | CBS window read from `is_plain_rw` and `csr_default`, not hard-coded | R754 F1 row 37 |
| `scripts/register_page.py` | Plain-word conditions, side effects in rows, paragraphs for notes, read-value tables, lane-split diagrams | R753 F5, F6, S1; R754 F2, F6, S1 |
| `scripts/register_diagrams.py` | New: ten checked Mermaid diagrams | R754 F7 |
| `scripts/gen_register_reference.py` | Field `rename` and `split`, name and purpose required, RTL digest, cell cap, design-note anchors checked | R753 F3, F6; R754 F1, F2, S2 |
| `scripts/register_selftest.py` | 58 controls through the workflow's `--check` entry | Each class needs a control that can fail |
| `scripts/register_descriptions.json` | Field rows, short notes, condition wording; long notes gone | R753 F5 to F7; R754 F2, F4, F6, F8 |
| `scripts/register_map_soc.json` | Re-extracted from a builder export of the merged tree. `csr.csv` and `aem_desc.json` are in `receipts/export/` | Manager ruling on dev. Two parameters added; no CSR moved |
| `docs/reference/REGISTER_MAP.md`, `docs/diagrams/regmap/**` | Regenerated | Generated outputs |
| `docs/design/CSR_REGISTER_NOTES.md` | New record: carried rationale and history, corrected | R753 F6, R754 F2 |
| `docs/diagrams/memory_map.gen.py:55`, `:69` | Plain labels and a width check | R753 F8, R754 F5 |
| `docs/DOC_GENERATION.md`, `docs/diagrams/README.md`, `docs/README.md` | Generators named, mechanisms listed, design notes linked | R6, R754 F7 |
| `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:247` | The CRF closure link now targets the design notes | The heading moved |
| `ci/image/command-table.json` | The two entry scripts' hashes | Scripts changed |

## Commits since round 1

| Commit | Subject | Closes |
|---|---|---|
| `b01661c8` | Merge live dev into the register reference lane | Manager ruling: dev `1f29f189`, one merge base |
| `db98975e` | Refresh the SoC extract from a builder export of the merged tree | Same ruling: the page describes the merged tree |
| `64093bfe` | Compute resets and reads by running the CSR decodes, refuse any window, reset mismatch or form the parser cannot read, state side effects in the field's row, and move prose the concise gate refuses to a design record | R753 F1, F2, F3, F4, F5; R754 F1, F3, F6; S1, S3, R3 |
| `01ec3198` | State bit meanings in field rows, hold every generated paragraph to the concise-prose gate, cap table cells, and keep the carried rationale on a design-notes page | R753 F6; R754 F2; S2, R2 |
| `ddf8cc6a` | Correct the carried statements the RTL and the export contradict | R753 F7; R754 F4 |
| `17c53378` | Remove private device labels and a bench address from the carried prose, and fix the leftover wording | R754 F8; R1, R4, R5 |
| `a0edd518` | Generate a Mermaid diagram for each mechanism the register reference explains | R754 F7 |
| `ec50b8da` | Shorten memory-map labels, refuse one that would overprint its address or carry markup, and name the register generators in the generation guide | R753 F8; R754 F5; R6 |
| `410714ea` | Print the plain module name in the diagram catalog's mechanism rows | `docs_check.py` finding on the prior commit |
| `b3b42200` | Pin the reviewed register generator and memory-map generator in the CI command table | Command table hashes |
| `eee3c65f` | Drop a trailing blank line from register_rtl.py | `git diff --check` |
| `12b53703` | Point the audit's CRF closure link at the design notes, name the design notes on the page, hold the memory-map label check with a control, and document the new sources | `gen_toc.py --verify-anchors` |
| `5b5486e6` | Shorten the diagram catalog's new sentence and link the design notes from the docs map | Docs map |
| `ae846366` | Hold the diagram catalog's new sentence to the prose rule's ten words | `check_doc_style.py` |
| `426fe78d` | State the W1S strobes' readback exactly, drop a store condition another path implies, mark the deleted discover counter a structural zero, and define the see-table reset code | Own review of the page against the RTL |
| `96bfa851` | Restate MAC_STATUS's link facts on the page, name the MAAP status bits, drop a hand-kept CBS table the generator prints, and lead each carried table with a line | Own check of the ETH_GUARD and link-control addition against the page |

`64093bfe` is wider than one finding group: the reader, the reset evaluator, the census and the row text are one change to one derivation, and splitting them would leave commits that do not build. The later groups are one commit each. Every commit subject is one line, with no body and no trailer.

## Findings closed

Both reviews number independently. Each row gives the fix and how it was checked. Receipts are under `receipts/`.

### Reset and Type cells: R753 F1, R754 F3

- **Fix:** `scripts/register_decode.py:191` `tree` runs the block's own read decodes with the address known. `:233` `reset` evaluates that tree in the state `:90` `ResetScope` defines: a flop holds its reset clause. An input, an unreset flop, or a flop the read itself loads from an input stays X (`scripts/register_rtl.py:525`). `scripts/register_fields.py:37` is the legend.
- **`X` that remains:** input-driven bits and `RST_EPOCH`, which has no reset clause and counts resets.
- **`PTP_PPS_CTRL[0]`:** `scripts/register_rtl.py:449` blanks a term a zero parameter disables. At `PPS_P` = 0 the bit is `R-0`, and two notes state both build shapes.
- **Verification:** `sim/r753_oracle_compare.txt` has one "page reset X, but no input moves it" row, `RST_EPOCH`. `sim/r754_compare_page.txt` has no `X-NOT-INPUT` row and no `PPS_ENABLE` row. `CHMAP_LOOP` reads `0xDEADDEAD`; every other word R753 F1 listed reads its table value.

### A window or word added: R753 F2, R754 F1

- **Fix:** `scripts/register_rtl.py:537` refuses a case label that is not an `A_*` name. `scripts/register_decode.py:319` refuses a live range term the generator does not document, and refuses a documented array whose term is gone. `:301` refuses any other test of the address. `:397` scans 0x000 to 0xFFC and refuses a decoded word with no register. `scripts/register_fields.py:916` names literal-address words only from the descriptions, and refuses one the RTL lacks or does not name. `scripts/register_rtl.py:410` refuses a CSR-bus site outside the known list, which is what catches a new write block and a clear-on-read block.
- **New on the page:** `STRMW_RSVD_86C` at 0x86C, the one decoded word round 1 had no section for.
- **Reachability:** `scripts/register_decode.py:191` refuses a read arm `rd_in_window` makes read 0.
- **Verification:** selftest controls "new range window", "literal-address read arm", "literal-address write arm", "read arm whose label lacks the A_ prefix", "literal-address test", "new address nothing decodes", "new register whose label ends in _END", "read arm removed from rd_in_window's reach", "write decoded in a new block" and "clear on read". `plants/r753_plant_probes.txt`: 45 plants, 0 misses. `plants/r754_mutants.tsv`: rows 22, 23, 25 to 27, 31, 35 and 36 now fail.

### Reset or behaviour change: R753 F3, F4; R754 F1

- **Fix:** `scripts/register_decode.py:335` compares each shadow-served or ROM-named word's flop reset with the ROM, and refuses a difference. `scripts/register_page.py:656` prints every value a multi-view word can return, by condition, so a changed branch changes the page. `scripts/gen_register_reference.py:360` keeps a digest of the comment-stripped CSR sources, so a code change no page text shows still fails the gate. A comment-only edit stays fresh.
- **Reserved bits:** `scripts/register_fields.py:369` refuses "drives nothing" on a stored bit logic reads.
- **CBS geometry:** `scripts/register_fields.py:837` reads the window from `is_plain_rw` and `csr_default`, and refuses a disagreement.
- **Verification:** controls for `mac_ifg`, `mac_ctrl`, `scratch` and `tcam_ctrl` flops, `LWSRP_LATENCY_RST_C`, the snapshot store, the poison constant, `PPS_WIDTH`, the 0x86C value, the `STRMW_SRP` alias, the masked read, `mac_ctrl[9]` in `o_irq`, the CBS word move, and "code change no page text shows".

### A word the parser cannot read: R753 F4, R754 F1

- **Fix:** `scripts/register_sv.py` is a parser of the block's SystemVerilog subset; anything else is a `Refusal`. `scripts/register_fields.py:476` and `:574` accept the listed write forms and refuse the rest, so a field is never published as read-only because its arm could not be read. `scripts/gen_register_reference.py:175` refuses a register with no name or purpose. `CHMAP_LOOP` fields now come from the RTL (`docs/reference/REGISTER_MAP.md:4265`).
- **Verification:** `plants/r753_write_probe.txt`: both write forms exit 2 on `--write`. Controls "write arm stores through a mask", "stores part of a register", "increments the written value", "read expression outside the grammar", "register without a purpose" and "CHMAP_LOOP subfield order swapped".

### Side effects and conditions: R753 F5, R754 F6

- **Fix:** `scripts/register_page.py:302` and `:338` state a write's further actions in the row of the bit that fires them. `:352` words strobes, write-1-to-clear and any-bit clears. `:85` `Wording` prints conditions by the register field software reads, or by the descriptions' wording, and refuses one it cannot word. `:279` gives a row with no prose its input, output or storage from the RTL.
- **Verification:** `plants/r753_row_audit.txt`: 0 empty rows of 498, 203 registers with a purpose. Control "doorbell added to a write arm" and "condition without wording".

### The concise-prose gate: R753 F6, R754 F2

- **Fix:** `scripts/register_page.py:476` renders notes as paragraphs. `:505` refuses a one-column table. `scripts/gen_register_reference.py:289` caps a table cell at 200 words. Bit meanings moved to field rows, with `split` naming the bits of a word read whole from an input (`scripts/gen_register_reference.py:118`).
- **The carried prose:** rationale, dated findings and the VERSION log moved verbatim to `docs/design/CSR_REGISTER_NOTES.md`. Each module and register links to its section. That page is a record, not generated, not current reference, and not in `DOCUMENTS`; its banner says so. This is the disclosed route R753 and R754 both allow, "history moves to its own page". Open risk 2 records it.
- **Numbers:** the page holds about 32,700 words against 55,197 in round 1: about 21,100 in field and summary tables, and 786 prose blocks of about 4,600 words, every one read by the gate. The rest is headings and code. No row is a `| Note |` row.
- **Verification:** `plants/r753_note_as_paragraph.txt`: 0 findings, 0 Note tables. Controls "note breaking the prose rules", "prose wrapped in a one-column table", "prose wrapped in a field's table cell".

### Carried prose: R753 F7, R754 F4

| Statement | Now | Against |
|---|---|---|
| `STRMW_SRP` "STRUCTURAL ZERO at every index" | Index 0 is the live `LWSRP_STATUS`, unless `STRM_SEL[9]` selects the listener row | `milan_csr.sv:2574-2576` |
| `STRM_SEL` "`[8]`/`[3:0]` are ignored while set" | `[9]` acts only while `[8]` is 0, and `[3:0]` still gates the window | `:1109-1110`, `:3086-3090` |
| `STRM_SEL` "Only these bits are stored/read back" | These are stored; a read returns `[8]` and `[3:0]` | `:2535` |
| "Unused bits read 0" | Reserved read-only bits read 0, reserved R/W bits store | Sim: `MAC_CTRL` |
| Second legend `RO`, `RW`, `ROc` | Dropped; the page's legend stands | The legend |
| "Every one defaults to PRESENT, so a shipping build's map..." | Defaults stand, but the export sets `I2SPB_P` and `LPF_P` to 0; the page states what that means, generated from the extract | `scripts/register_map_soc.json` |

### Device labels: R754 F8

The two device labels the review named are gone from the page, the design notes and the descriptions. A grep of both for hosts, addresses and serials found a bench MAC and a capture tool's name in the design notes; both are removed. Multicast group addresses remain. They are protocol constants. `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv` still carries one of those labels in comments: outside this diff, reported below.

### Mechanism diagrams: R754 F7

`scripts/register_diagrams.py` generates ten Mermaid diagrams, each after its explaining text: how a read is served, the statistics snapshot, a TCAM write, the link guard, the Ethernet guard, a stream snapshot, the latency-tap chains, the media-clock servo, a channel-map readback, and the posted side-port read. `Labels` (`:34`) reads each register, offset, bit, key and constant from the model, and checks state names against the source. `docs/diagrams/README.md` lists them in the generated block. Controls "mechanism diagram's state gone from its source", "bit no longer a strobe" and "reset change the ETH_GUARD diagram draws". The servo's transitions were read against `KL_mmcm_drp_servo.sv:946-998` and `:1201-1272`.

### Memory map: R753 F8, R754 F5

`docs/diagrams/memory_map.gen.py:55` reduces a heading to its plain name, and `:69` refuses a label that would reach its address, or carries markup. `receipts/renders/memory_map.png` shows every address legible. `plants/memory_map_plants.txt`: a long label exits 2.

### Suggestions and residue

| Item | State |
|---|---|
| S1 (R753, R754) | Closed: `scripts/register_page.py:383` splits a field at each lane. `receipts/renders/MAC_CTRL.png` |
| S2 (R753, R754) | Closed: `CAP` fields are named through `rename` |
| S3 (R754) | Closed: the dead expression went with the rewrite |
| S4 (R754) | Not closed: `KL_pp_shadow.sv:688` and `milan_datapath.sv:8651` are RTL comments, outside this PR |
| R1 | Closed in the row and in the design notes |
| R2 | Closed: the `Group summary` rows are deleted |
| R3 | Closed: legend reads "Reserved read-only fields read as `R-0`" |
| R4, R5 | Closed |
| R6 | Closed: `docs/DOC_GENERATION.md` names both generators |

## Findings count per area

| Area | R753 | R754 | Closed |
|---|---|---|---|
| Freshness gate and parser | 3 (F2, F3, F4) | 1 (F1) | 4 |
| Reset and Type cells | 1 (F1) | 1 (F3) | 2 |
| Concise-prose gate | 1 (F6) | 1 (F2) | 2 |
| Side effects and conditions | 1 (F5) | 1 (F6) | 2 |
| Carried prose | 1 (F7) | 1 (F4) | 2 |
| Memory-map labels | 1 (F8) | 1 (F5) | 2 |
| Mechanism diagrams | 0 | 1 (F7) | 1 |
| Device labels | 0 | 1 (F8) | 1 |
| Suggestions | 2 | 4 | 3 distinct, S4 stays |
| Residue | 3 | 6 | 6 distinct |

## Generator and freshness gate

- **Inputs:** `hdl/common/csr/milan_csr.sv`, its two generated includes, the `milan_csr` instance in `hdl/milan/milan_datapath.sv`, `hdl/common/ethernet_packet_pkg.sv`, `scripts/register_map_soc.json`, `scripts/register_descriptions.json`, `docs/reference/milan_feature_status.json`, the anchors of `docs/design/CSR_REGISTER_NOTES.md`, and the state names of `hdl/common/KL_link_guard.sv` and `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv`.
- **Outputs:** `docs/reference/REGISTER_MAP.md`, `docs/diagrams/regmap/**` with `rtl_fingerprint.txt`, the catalog block in `docs/diagrams/README.md`; `docs/diagrams/memory_map.{svg,drawio}` from `memory_map.gen.py`.
- **Gate:** step "Register reference freshness gate" of `.github/workflows/docs.yml`, `id: gate_50`.
- **Planted stale-page mutants:** 58 controls through the workflow's own `--check` entry, in `gates/docs-gates-0__gate_50.log`. A flop change with a matching ROM change exits 1 naming the page. A field rename exits 2 while its description names the old field, and 1 naming the page once the description follows. A flop change alone exits 2.
- **Both reviewers' plants, rerun at this head:** `plants/r753_plant_probes.txt` 45 plants, 0 misses. `plants/r754_mutants.tsv` 39 rows: rc 2 on 24, rc 1 on 14, rc 0 on the comment-only control.
- **The reviewer's `mutants.py` needs three more paths.** The generator now reads the design notes and two state-machine sources. `tools/r754_mutants_paths.py` is that script with those three added and nothing else changed.

## The simulation

Both reviewers' harnesses ran unchanged, at the shipping parameters, against the committed page.

- `sim/r753_oracle_compare.txt`: 203 registers, 498 fields, 0 undocumented addresses with a nonzero observation. Of 38 field findings, one is the justified `RST_EPOCH`. The rest are the classes R753 explained: guarded and refused writes, window words that write a different store, and `CHMAP_SNAP[4]`, `[2]` moving after an arm. `PP_NVM_STAT` now accounts for 21 of them, one per split field, with the same cause: writes there go to the strobe word.
- `sim/r754_compare_page.txt`: 203 registers, 257 words, 8,224 bit checks. No `X-NOT-INPUT`, no `W-NO-EFFECT` on `PPS_ENABLE`. `R-BUT-OUTPUT` on `PP_SPADDR` and `LTAP_CTRL`, and `W-NO-EFFECT` on `TCAM_CMD` and `REST_CMD`, are the rows R754 read and explained.
- `sim/r754_attribution.txt`: its `DIFF` rows are `RST_EPOCH` and the words `split` names, where the page's field name is no longer the input port's.

## Dropped statements

`tools/survival.py` splits the old page into 1,610 fragments and looks for each on the page, the design notes or the descriptions, ignoring link targets. 1,554 are present verbatim. `receipts/survival.txt` lists the other 56.

| Fragments | Why |
|---|---|
| 12 from round 1 | Unchanged from round 1's table: false, obsolete, or kept in other words |
| 28 `Group summary` rows | R2: deleted. Each module's heading and purpose state the same |
| `STRMW_SRP` and `STRMW_BIND` cells | Contradicted: `milan_csr.sv:2574-2576`. Rows rewritten |
| `STRM_SEL` note, unused-bit rule, legacy legend, "defaults to PRESENT" | Contradicted: table above |
| TCAM residue, lane-K, `#617 round 3`, device labels, bench MAC, tool name | Rewritten as the rulings and residue order |
| The quoted instruction in the control-plane note | Provenance only; the statement stands without it |

## Open risks and decisions

1. **ETH_GUARD.** The page states the code: nothing in the SoC consumes the guard. The RTL comments at `milan_csr.sv:708` and `:890` still claim the gating, by ruling. The decision remains open.
2. **The design-notes page is not held to the concise-prose rule.** It holds about 31,000 words of carried prose. The rule covers pages a lane rewrites or marks current; this page is neither, and its banner says so. If the owner wants it rewritten, that is new work.
3. **Mermaid is not rendered here.** The host has no Mermaid renderer, and sending the source to a web renderer would publish it. Syntax follows the forms in `docs/README.md`. The generator checks labels, not rendering, so a reader should open the PR's rendered page once.
4. **Hand-kept structure in the generator.** `RANGE_ARRAYS` and `KNOWN_BUS_SITES` list RTL structure. Each is checked against the RTL: a new item refuses until someone teaches the generator, so it cannot go stale silently.
5. **Every code change to `milan_csr.sv` needs `--write`.** The digest makes that deliberate: the gate asks a human to reread the prose of the registers touched.
6. **Lane conflict with PR #815.** Both add a docs-check step. Whichever lands second renumbers it. D0's inventory must also list the new design-notes page.
7. **A device label remains in RTL comments** (`KL_mmcm_drp_servo.sv:248-251`). This PR changes no RTL; the page and its sources are clean.
8. **CI cannot run a LiteX export**, so SoC drift is caught by `--check --soc-from`, not by the docs job alone (`export/soc_from_check.txt`, rc 0).
9. **`i_i2spb_*` on the shipping build:** the page's structural-zero note rests on the extract's `I2SPB_P` = 0, read with `milan_datapath.sv:8016`. It was not simulated at the datapath level.

## Gate table

Method: as `../640-a720g`. Each step of the head's `.github/workflows/docs.yml` ran as its job runs it, read from the workflow by `tools/run_docs_workflow.py`, one `bash -e` script per step, output to a file, never piped. The clone is a fresh one of the head with the four submodules the jobs fetch, each at its pin. The gate venv and scratch HOME are the ones the assignment names as reusable. After the run the clone's status was empty and its head unchanged. Logs and rc files: `receipts/gates/`.

| Job | Step id | Name | rc | Last line |
|---|---|---|---:|---|
| wire-accountability | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| wire-accountability | ci_step_3 | Fetch the engine authority the builder derives from | 0 |  |
| wire-accountability | ci_step_4 | Advertised-vs-emitted gate (green since 2026-07-28, item 0 | 0 | RESULT: PASS |
| docs-check-no-git | ci_step_2 | Set CPU-derived job budgets | 0 |  |
| docs-check-no-git | ci_step_3 | Strip git metadata, then run the docs gate | 0 | feature_status: 0 finding(s) |
| docs-gates-0 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| docs-gates-0 | gate_1 | Build the validated HDL reference | 0 | Wrote: <runner-temp>/milan-hdl-reference/index |
| docs-gates-0 | gate_7 | Link health, wording, dead-reference and local-info gate | 0 | docs_check: 0 finding(s) across 213 md files + 1687 scrubbed text files, scrub self-test 2 |
| docs-gates-0 | gate_8 | Added-line em-dash gate | 0 | check_em_dash: 0 finding(s) over 5785 added line(s) in 7 changed Markdown page(s), 0 mirro |
| docs-gates-0 | gate_9 | Concise audience documentation gate | 0 | gPTP documentation selftest: OK (30 controls) |
| docs-gates-0 | gate_10 | Audience diagram no-drift gate | 0 | time-sync diagram selftest: OK (source, status, XML, raster) |
| docs-gates-0 | gate_11 | Product solution source-fact gate | 0 | solution documentation selftest: OK (45 mutation controls) |
| docs-gates-0 | gate_12 | Verified submodule documentation gate | 0 | submodule documentation selftest: OK (table and diagram controls) |
| docs-gates-0 | gate_13 | HDL timing diagram no-drift gate | 0 | WaveDrom current: docs/diagrams/wd_gptp_pdelay.json |
| docs-gates-0 | gate_14 | Published diagram PNG gate | 0 | diagram PNG selftest: OK (6 rasters, 28 mutation controls) |
| docs-gates-0 | gate_15 | Milan feature-status consistency gate | 0 | feature_status: 0 finding(s) |
| docs-gates-0 | gate_16 | Traceability matrix no-drift gate | 0 | traceability matrix up to date (80 modules, 0 untested <= ratchet 0, 0 archived) |
| docs-gates-0 | ci_step_21 | Fetch the builder source dependencies | 0 |  |
| docs-gates-0 | gate_18 | Imported gPTP documentation gate | 0 | source evidence selftest: PASS (7 arms) |
| docs-gates-0 | gate_19 | Code-quality measurement self-tests | 0 | 18 checks: 18 PASS, 0 FAIL |
| docs-gates-0 | gate_21 | Bare-metal scope gate | 0 | baremetal-only selftest: PASS (867 arm(s)) |
| docs-gates-0 | ci_step_28 | Install and verify the pinned RV32 SDK | 0 | SDK cache hit: verified |
| docs-gates-0 | gate_24 | Compiler-absent firmware controls | 0 | GATE 1b PASS; 1 NOT RUN; 0 actual firmware compiler invocations |
| docs-gates-0 | gate_26 | NVM record-space gate | 0 | 0 finding(s) across 5 config(s): the inventory's (group, index) key set is exactly the set |
| docs-gates-0 | gate_27 | Capture measurement census and clock gate | 0 | PASS: capture census, clocks, both timing arms and receipt agree |
| docs-gates-0 | gate_28 | Saved-state writer gate | 0 | saved-state writer gate: OK across 5 shape(s), and every planted defect reddened |
| docs-gates-0 | gate_29 | SoC source-list gate (Vivado would fail 40 min in without  | 0 | iob_pack_selftest: 22 arms, 21 mutants, 0 failure(s) |
| docs-gates-0 | gate_30 | RTL source-list drift gate | 0 | 50 checks: 50 PASS, 0 FAIL |
| docs-gates-0 | gate_31 | Boundary-unit naming ratchet | 0 | 66 checks: 66 PASS, 0 FAIL |
| docs-gates-0 | gate_32 | Port contract gate | 0 | 82 checks: 82 PASS, 0 FAIL |
| docs-gates-0 | gate_33 | Fail-fast ratchet | 0 | 106 checks: 106 PASS, 0 FAIL |
| docs-gates-0 | gate_34 | TODO ownership gate | 0 | 45 checks: 45 PASS, 0 FAIL |
| docs-gates-0 | gate_35 | Test-evidence ratchet | 0 | 105 checks: 105 PASS, 0 FAIL |
| docs-gates-0 | gate_36 | Mechanical hygiene ratchet | 0 | 35 checks: 35 PASS, 0 FAIL |
| docs-gates-0 | gate_37 | SystemVerilog idiom gate | 0 | 55 checks: 55 PASS, 0 FAIL |
| docs-gates-0 | gate_38 | C and C++ idiom gate | 0 | 75 checks: 75 PASS, 0 FAIL |
| docs-gates-0 | gate_39 | Python idiom gate | 0 | 54 checks: 54 PASS, 0 FAIL |
| docs-gates-0 | gate_40 | Shell idiom gate | 0 | 48 checks: 48 PASS, 0 FAIL |
| docs-gates-0 | gate_43 | Doc cited-path gate | 0 | doc path gate: OK (1091 cited paths all resolve, 2 allowlisted; 10 line anchor(s) within t |
| docs-gates-0 | gate_44 | Archive integrity gate | 0 | archive selftest: OK (24 controls) |
| docs-gates-0 | gate_45 | Per-page contents gate | 0 | TOC gate: OK (151 page(s) carry an annotated contents list, 18 below the 3-section thresho |
| docs-gates-0 | gate_46 | AEM store generator self-test | 0 | gen_aem_store self-test: PASS |
| docs-gates-0 | gate_47 | Sweep/build shape gate | 0 |   [self-test] OK: 1 drift(s) reported |
| docs-gates-0 | gate_48 | Deploy shape gate | 0 |   [selftest] OK: 1 drift(s) reported |
| docs-gates-0 | gate_49 | Entity shape gate | 0 | RESULT: PASS |
| docs-gates-0 | gate_50 | Register reference freshness gate | 0 | memory map diagram: fresh |
| docs-gates-0 | ci_step_53 | Fetch inventory dependencies | 0 |  |
| docs-gates-0 | gate_51 | CI scheduling and evidence controls | 0 | manifest comparison controls: PASS |
| docs-gates-1 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| docs-gates-1 | ci_step_9 | Fetch the builder source dependencies | 0 |  |
| docs-gates-1 | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | SDK cache hit: verified |
| docs-gates-1 | gate_25_0 | End-station builder gates, leg 0 of 2 | 0 | ALL GATES PASS |
| docs-gates-2 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| docs-gates-2 | ci_step_9 | Fetch the builder source dependencies | 0 |  |
| docs-gates-2 | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | SDK cache hit: verified |
| docs-gates-2 | gate_25_1 | End-station builder gates, leg 1 of 2 | 0 | ALL GATES PASS EXCEPT 16 NOT RUN |
| docs-gates-2 | gate_41 | CI event and SHA contract gate | 0 | selftest: PASS (2207 contract items, 5271 arms) |
| docs-gates-2 | gate_42 | Local act runner contract gate | 0 | selftest: PASS |

58 steps ran, 0 not rc 0, 38 not run.

Not run: wire-accountability: Record actual job execution; docs-check-no-git: Retain checkout identity before removing metadata; docs-check-no-git: Record actual job execution; docs-gates-0: Install the python gate dependencies; docs-gates-0: Install the pinned Markdown renderer; docs-gates-0: Resolve exact package downloads 6; docs-gates-0: Install diagram gate dependencies; docs-gates-0: Install the pinned sv2v release; docs-gates-0: Record executed gate outcomes; docs-gates-0: Record actual job execution; docs-gates-1: Install the python gate dependencies; docs-gates-1: Install the pinned Markdown renderer; docs-gates-1: Resolve exact package downloads 4; docs-gates-1: Install diagram gate dependencies; docs-gates-1: Install the pinned sv2v release; docs-gates-1: Record executed gate outcomes; docs-gates-1: Record actual job execution; docs-gates-2: Install the python gate dependencies; docs-gates-2: Install the pinned Markdown renderer; docs-gates-2: Resolve exact package downloads 4; docs-gates-2: Install diagram gate dependencies; docs-gates-2: Install the pinned sv2v release; docs-gates-2: Record executed gate outcomes; docs-gates-2: Record actual job execution; docs-check: Set CPU-derived job budgets; docs-check: Install the pinned evidence reader; docs-check: Require every gate exactly once; docs-check: Record actual job execution; ci-manifest: Set CPU-derived job budgets; ci-manifest: Fetch inventory dependencies; ci-manifest: Install the pinned evidence reader; ci-manifest: Collect actual runtime evidence; ci-fail-fast: Set CPU-derived job budgets; ci-fail-fast: Observe the first failed job; ci-fail-fast: Cancel this run and sibling workflows; ci-fail-fast: Record actual job execution; ci-cancel-tail: Set CPU-derived job budgets; ci-cancel-tail: Cancel confirmed terminal failures.

Reasons for the steps not run:

- **`Record ...`, `Retain checkout identity`:** GitHub run evidence only.
- **`Install ...`, `Resolve exact package downloads`:** apt, sudo or pip. The host and venv already hold these tools. `ci/constraints-ci.txt` pins CPython 3.12 downloads and cannot resolve in this venv, so the runner also drops the `python3 -m pip install` lines inside gate steps and leaves their other commands intact.
- **Jobs `docs-check`, `ci-manifest`, `ci-fail-fast`, `ci-cancel-tail`:** they verify uploaded CI receipts or cancel runs, so they run only on GitHub.

Builder leg 1 reports `ALL GATES PASS EXCEPT 16 NOT RUN` with rc 0 (`gates/docs-gates-2__gate_25_1.log`). Those arms need an interpreter that imports migen, litex and litex_boards, which the docs workflow never installs, or a local Arty build report. Each leg's rc is 0, and the verdict is judged on the union of the legs.

`docs-gates-2__gate_41.log` is over the size limit: its digest, size and tail are in `gates/docs-gates-2__gate_41.log.tail`.

Also on this head:

| Check | rc | Receipt |
|---|---:|---|
| `git diff --check 1f29f189 HEAD` | 0 | `gates/lane__diff_check.rc` |
| `docs_check.py`, `check_em_dash.py --base 1f29f189`, `check_doc_style.py`, `gen_toc.py` in the pinned Markdown venv | 0 | `gates/lane__md_*.rc` |
| `gen_register_reference.py --selftest` (58/58, in gate_50) | 0 | `gates/docs-gates-0__gate_50.log` |
| `gen_register_reference.py --check --soc-from <export>` | 0 | `export/soc_from_check.txt` |
| `behave features/counters_contract_milan.feature` (reads the page), 88 scenarios | 0 | `behave/counters_contract_milan.txt` |
| Both reviewers' simulations, rerun | 0 | `sim/` |
| Both reviewers' plants and probes, rerun | 0 | `plants/` |

Not run: the Verilator sweep, Yosys and the full behave suite (documentation lane, no RTL changed). No hardware, no Vivado.
