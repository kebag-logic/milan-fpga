[R384] POSITIVE - exact head be6b48c140db1692caedbdf997495b43ff1a56a2

# [R384] Review round R384-2: PR #612 / issue #577 (delta a53682ed..be6b48c1, deployed-image enforcement and completed L6/L10 refusals)

- Role: internal independent reviewer, cleared context. Round-2 executor: [A413].
- Exact head reviewed: `be6b48c140db1692caedbdf997495b43ff1a56a2`, tree `cc7578edeefdba3f871e6924de2477dc513420e5`. Source base `54ce877371ee6e8878cf67294e86c2a8481b62f6`; round-1 head `a53682ed38720de758006602a19f78c8e40d69da`.
- Delta under review (one commit, one-line message, no trailers): `sw/builder/aem_image_checks.py` +22/-1, `sw/litex/milan_soc.py` +6, `sw/builder/test_builder.py` +102/-6, `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` +32/-7, `docs/ENDSTATION_BUILDER.md` +16/-12. `sw/builder/endstation_builder.py` is unchanged since round 1 (`receipts/scope.txt`).
- Authorities read: AGENTS.md; issue #577 body, the round-1 assignment (5865331676, decisions 1-6), the F1 decision (5866340517, option (a)), the round-2 assignment (5866376116), and the [A413] TAKEN and REVIEW READY comments; PR #612 body at this head; `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` (L6, L10, source table, probe section, F6); `docs/ENDSTATION_BUILDER.md:130-145,212-214,574-596`; the pinned consumer `protocol-processor/hdl/aecp/ucode/gen_ucode.py:1253-1430` and the AEMI v1 layout `protocol-processor/hdl/aecp/desc/gen_desc_image.py:53-80` at gitlink `16be6768f710e79450aace277abacd6c2c3336e5`; `sw/litex/milan_soc.py:69-83,3331-3373,3950-3970,4014-4038`.
- Clauses checked: IEEE 1722.1-2021 7.2.3 / Table 7-5 (136 current_sampling_rate, 140 offset "144 for this version", 142 count), 7.2.32 / Table 7-61 (72 clock_sources_offset "76 for this version", 74 count, 76 list), 7.4.21.1, 7.4.23.1; Milan v1.2 5.3.3.3 (current_sampling_rate shall be one of the listed rates).
- Public evidence read: `review-evidence/577-r1` at `d13de9c5f2f03f8c4cb7327f46ae9e508e94b29e` (round-1 author packet). No round-2 author packet or manager bank receipt was published on the evidence branch or in the issue/PR threads at report time (last observed 09:22 UTC; see Pending manager duties).

## Verdict

POSITIVE. My round-1 F1 (MAJOR) and F2 (MINOR) are resolved at this head, and the three taken suggestions are implemented. All five lenses are CLEAN. The three findings below are SUGGESTION only.

## Round-1 findings and the round-2 assignment, re-verified at this head

| Item | Result at be6b48c1 | Receipt |
|---|---|---|
| F1: the check runs on the exact bytes every deployed-image emitter writes | **Resolved.** `build_desc_image` packs once (`milan_soc.py:3364-3365`, the only assignment of `blob`), validates that object (`:3368-3372`), and returns it (`:3373`). `main()` binds `_desc_blob` only to that return value (`:3952-3955`, besides the `None` initialiser). The check precedes `binascii.crc32(_desc_blob)` (`:3965-3966`) and `write_bytes(_desc_blob)` (`:4018`). The builder emitter `_entity_model_image` keeps its round-1 hook (`endstation_builder.py:2308-2312`). A search outside the submodules finds no other writer of the deployed image. `scripts/nvm_shape.py:82` packs a temporary image for analysis only, and `deploy.sh`, `layout_from_soch.py` and `check_gptp_owner_pair.py` consume an image rather than emit one | `receipts/scope.txt` |
| F1: soc_path_probe `[1,0]` plant | **REFUSED `L6_ORDER`** through the SoC emitter (`B SoC verdict: REFUSED L6_ORDER`), and through the builder. A new zero-rate plant through the SoC is refused with `L10_EMPTY`. Unfaulted SoC and builder bytes are identical for all five configurations | `receipts/soc_path_probe.log` |
| F1: the SoC import resolves in the real launch | `from sw.builder import aem_image_checks` (`milan_soc.py:3358`) was replayed under milan_soc's own `sys.path` inserts (lines 72, 76, 83, 3352, 3353) with `sw/litex` as the script directory. It resolves to `sw/builder/aem_image_checks.py` as a namespace package, and no module imported earlier binds `sw` | `receipts/soc_import_probe.log` |
| F1: a committed test fails if the SoC emitter bypasses the check | `test_soc_shipping_image_contract` (`test_builder.py:27406-27423`) executes the repository's `build_desc_image` source (`:27385-27403`) with only `_builder_out` stubbed, and runs all 23 packed-image cases through it. My mutants "SoC hook removed" and "SoC refusal swallowed" are both KILLED, and so is "builder hook removed". The test is registered in the builder runner (`:27878`) | `receipts/mutants.log`, `receipts/gate36b_head.log` |
| F1: the PR body's reproduction command reaches the check | The PR body's heredoc, run verbatim from a farm root, returns rc 0 with 56 gate-36b lines. With the checker forced to raise on every call it returns rc 1 and ends `aem_desc.bin: PROBE_REACHED`. As a control, the builder CLI still emits no image and never reaches the checker, which the document now states (`PP_DESCRIPTOR_OWNERSHIP.md:189`) | `receipts/cli_reach_probe.log` |
| F1: the ownership document names the enforcing emitters | `PP_DESCRIPTOR_OWNERSHIP.md:89,93` (both L6 and L10 rows), `:99` (new source key G = `milan_soc.py`), `:182-189` (links the decision at `:399`), `:341` (F6). `ENDSTATION_BUILDER.md:136-140,213-214,580-587` no longer claims that `--write-rtl`/`--write-fragment` or `_entity_model_image` produce the deployed set, which was the drift noted in round 1 | read at head |
| F2: zero-entry rate list | **Resolved.** `L10_EMPTY` (`aem_image_checks.py:48-49`). The committed fixture is "empty rates" (`test_builder.py:27266`). My removed-check mutant is KILLED (`empty rates: wrong refusal ... L10_CURRENT`: the gate demands the exact name). Edge probe: count 0 is `REFUSED L10_EMPTY`, including with current 0 | `receipts/mutants.log`, `receipts/edge_probe.log` |
| Taken: `clock_sources_offset` pinned at 76 | `L6_OFFSET` for any offset other than 72+4 (`aem_image_checks.py:74-75`). Offsets 70, 74 and 78-with-padding are refused, and 76 is accepted. My mutants "L6_OFFSET removed" and "relaxed to the round-1 lower bound" are both KILLED | `receipts/edge_probe.log`, `receipts/mutants.log` |
| Taken: at least one checked AUDIO_UNIT and CLOCK_DOMAIN row per configuration | The header `n_config` at +0x06 matches the AEMI v1 layout (`gen_desc_image.py:58`). A row counts only when a descriptor was actually checked, so zero-count rows do not count (`aem_image_checks.py:103-131`). Refusals: `L10_MISSING`, `L6_MISSING`, `IMAGE_CONFIGS`. The edge probe refuses AUDIO_UNIT-only, CLOCK_DOMAIN-only, retyped-row and header-count 2/65535/0 images. My mutants for L10_MISSING, L6_MISSING, zero-count rows counted, IMAGE_CONFIGS, CLOCK_DOMAIN rows skipped and configuration 0 only are all KILLED | `receipts/edge_probe.log`, `receipts/mutants.log` |
| Taken: `current_sampling_rate` membership at the image | `L10_CURRENT` (`aem_image_checks.py:61-64`) compares the full 32-bit word, pull bits included. This matches the consumer, which compares "all 32 bits, pull too" (`gen_ucode.py:1324-1325,1389`) and serves byte 136 as the current rate until a controller sets one (`:1272-1280,1340-1345`). The pull-bit-mismatch and absent-rate cases are refused, and last-position and pull-bearing matches are accepted. My mutants "L10_CURRENT removed" and "pull bits masked" are both KILLED | `receipts/edge_probe.log`, `receipts/mutants.log` |
| All five shipping images byte-identical | Both emitters produce identical bytes at base `54ce8773`, round-1 `a53682ed` and head `be6b48c1` for all five configurations, builder bytes equal SoC bytes at each commit, and the head builder hashes equal my round-1 packet's | `receipts/images_{base,r1,head}.txt`, `receipts/images_compare.txt` (RESULT PASS) |
| No processor source or gitlink change | The diff touches no submodule or `avdecc` path. Gitlinks are identical at base and head. `_load_clocking`, `_validate_output_clock_sources`, `load_config` and `emit_aem_overlay` have unchanged source hashes (#478 scope preserved) | `receipts/scope.txt`, `receipts/tree_*.txt` |

Focused gates 36a/36b, all six functions at head: rc 0 (`receipts/gate36b_head.log`). Mutant campaign: 30 of 31 KILLED (`receipts/mutants.log`). The single survivor is a defensive structural refusal outside the frozen refusal list (S1).

## Findings

### S1: SUGGESTION: Tests, Robustness: the new configuration-outside-header refusal has no fixture

- Where: `sw/builder/aem_image_checks.py:112-113` (`IMAGE_STRUCTURE: configuration {cfg} outside header count`), added in this round. `test_shipping_image_contract_presence` (`test_builder.py:27426-27467`) forces the header count to 0 and 3 only.
- Evidence: my mutant that removes the check SURVIVES the focused gate (`receipts/mutants.log`). `receipts/bound_probe.log` shows what the check buys. With it, both cases are refused `IMAGE_STRUCTURE`. Without it, an AUDIO_UNIT or CLOCK_DOMAIN row beyond the header count raises an unnamed `IndexError`, which still fails closed in both emitters because neither catches it. A different row type beyond the count is accepted, but that is generic image integrity, which the ownership matrix allocates to the processor packer.
- Why not MINOR: the frozen acceptance and the round-2 assignment do not name this refusal. The case table does not claim it, and "each removed semantic refusal" (`PP_DESCRIPTOR_OWNERSHIP.md:238`) does not cover `IMAGE_STRUCTURE`. For F6 the behaviour stays fail-closed.
- Optional outcome: a presence fixture with the header count forced below a row's configuration, expecting `IMAGE_STRUCTURE`.

### S2: SUGGESTION: Docs: pre-existing texts outside this diff still attribute `aem_desc.bin` to the end-station builder

- Where (all unchanged by this PR): `docs/fpga/FPGA_DESIGN.md:67-68`, `docs/integration/QSPI_FLASHBOOT.md:176-177`, `docs/reference/FR_NFR.md:119-120,391`, `docs/reference/REGISTER_MAP.md:81`, `docs/limitations/TROUBLESHOOTING.md:972`, and the `emit_aem_rom_svh` docstring (`sw/builder/endstation_builder.py:3133-3135`: "the flat DRAM image emitted by `_entity_model_image()`"). `README.md:116-118` already says "the named SoC build generates".
- Impact: none on the F6 enforcement claim, which the ownership document states correctly. These texts are only less precise about which emitter writes the file. A minor wording point in the same area: "Every fault survives packing before the parent check refuses it" (`PP_DESCRIPTOR_OWNERSHIP.md:206`) describes the planted-fault cases. The presence and header-count fixtures are post-pack byte edits, which the case table already reports correctly.
- Optional outcome: a follow-up issue for the wording. It is out of this lane's scope under AGENTS section 4.

### S3: SUGGESTION: Conformance, Robustness: two image properties remain outside the frozen L6 scope

- `clock_source_index` (byte 70, IEEE Table 7-61) is not checked against `clock_sources_count`. An image with index 5 and list `[0,1]` is accepted (`receipts/edge_probe.log`). This is the L6 analogue of the adopted `L10_CURRENT`: the consumer serves the image's index until a controller sets one.
- Trailing bytes after the CLOCK_DOMAIN list are still accepted. The executor recorded this as unadopted for this round in REVIEW READY.
- Optional outcome: a follow-up issue if the maintainer wants either property.

## Clean-lens evidence

[R384] PASS Conformance - `sw/builder/aem_image_checks.py:39-131`, `sw/litex/milan_soc.py:3358-3373,3952-3966,4016-4018`, `sw/builder/endstation_builder.py:2308-2312`, PR #612 body "How to reproduce" - F1 option (a) per decision 5866340517: both emitters check the exact bytes they return, and the SoC refuses before CRC binding and writing. Checked against IEEE Tables 7-5 and 7-61 (offsets 140/142/144 and 72/74/76), Milan 5.3.3.3 (non-empty list, current rate a member, full word), the round-1 decisions 2 and 3 and the round-2 taken suggestions. Receipts: `soc_path_probe.log`, `generator_plant_probe.log`, `soc_import_probe.log`, `edge_probe.log`, `cli_reach_probe.log`, `scope.txt`. Only SUGGESTION S3 is open.

[R384] PASS RTL - `protocol-processor/hdl/aecp/ucode/gen_ucode.py:1253-1430` and `protocol-processor/hdl/aecp/desc/gen_desc_image.py:53-80` at gitlink 16be6768; `receipts/scope.txt` - The diff has no HDL and no gitlink change. The checker's premises match the unchanged consumer. SET_SAMPLING_RATE refuses unless offset == `SSR_LIST_OFF` (144), walks at most `SSR_WALK_MAX` (8) entries, and compares whole 32-bit words including pull bits, which is the basis for `L10_CURRENT`'s full-word test. GET_SAMPLING_RATE serves image byte 136 until a controller sets a rate. SET_CLOCK_SOURCE range-checks against the count at byte 74 on the identity-list premise that `L6_*` enforces. The header `n_config` sits at +0x06 and the index rows are 16 bytes (`>HHHHIHH`). Both consumer constants are live: the drift mutants to 148 and 10 are KILLED.

[R384] PASS Robustness - `sw/builder/aem_image_checks.py:91-133`; `receipts/edge_probe.log` (27 cases), `receipts/bound_probe.log`, `receipts/mutants.log` - Checked cases: zero-count lists (both), pull-bit mismatch, offsets 70/74/78, missing types per configuration, zero-count rows, header count 0/2/65535, a row configuration beyond the header, index offset beyond the image, a row count beyond the index, layout version 2, and truncation to 14 and 3 bytes. All are refused with named reasons, and the positive controls are accepted. Every exception path out of the checker is `ImageCheckError`, except the fail-closed `IndexError` in the survivor scenario (S1, SUGGESTION).

[R384] PASS Tests - `sw/builder/test_builder.py:27233-27467` (gate 36b: `_image_contract_cases`, `_assert_image_contract_case`, `test_shipping_image_contract`, `_index_walk`, `_soc_image_emitter`, `test_soc_shipping_image_contract`, `test_shipping_image_contract_presence`) and runner registration at `:27875-27878` - The focused gates return rc 0 (`receipts/gate36b_head.log`). 30 of 31 independent mutants are KILLED. They cover every named L10/L6 refusal, both emitter hooks, the SoC refusal path, presence and zero-count rows, IMAGE_CONFIGS, the index walk and consumer drift. The survivor is S1 (SUGGESTION). Six accepted body controls and 17 negative cases run through each emitter. The SoC test executes repository source, not a copy of the checker.

[R384] PASS Docs - `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:89,93,99,182-237,341,399`; `docs/ENDSTATION_BUILDER.md:136-140,213-214,580-587`; PR #612 body - The case table matches the executed outcomes line for line (`receipts/gate36b_head.log`, `receipts/edge_probe.log`). Both enforcing emitters are named, the decision is linked, and the round-1 deployment-path drift in `ENDSTATION_BUILDER.md` is corrected. The CRC-binding sentence holds because `baremetal` is the only accepted software profile (`milan_soc.py:2539-2540`). Focused local gates: `docs_check.py` in Git and no-Git modes, `check_doc_paths.py` and `check_py_idiom.py` all return rc 0. `gen_toc.py --check/--verify-anchors` were NOT RUN locally because the pinned renderer is absent (`receipts/docs_gates.log`). Hosted `docs-check-no-git` succeeded at this head, and hosted `docs-check` was still in progress at 09:22 UTC. Only SUGGESTION S2 is open.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (S3 SUGGESTION only) | issue #577, decisions 5865331676 / 5866340517 / 5866376116; IEEE Tables 7-5, 7-61, 7.4.21.1, 7.4.23.1; Milan 5.3.3.3; `aem_image_checks.py:39-131`; `milan_soc.py:3331-3373,3950-3970,4014-4038`; `endstation_builder.py:2282-2331`; PR body; `soc_path_probe.log`, `generator_plant_probe.log`, `soc_import_probe.log`, `edge_probe.log`, `cli_reach_probe.log`, `scope.txt` | R384-2 | be6b48c140db1692caedbdf997495b43ff1a56a2 |
| RTL | CLEAN | `gen_ucode.py:1253-1430`, `gen_desc_image.py:53-80` at gitlink 16be6768; `aem_image_checks.py`; `scope.txt` (no HDL, no gitlink change); consumer-drift mutants in `mutants.log` | R384-2 | be6b48c140db1692caedbdf997495b43ff1a56a2 |
| Robustness | CLEAN (S1, S3 SUGGESTION only) | `aem_image_checks.py:91-133`; `edge_probe.log`, `bound_probe.log`, `mutants.log`, `soc_path_probe.log`, `generator_plant_probe.log` | R384-2 | be6b48c140db1692caedbdf997495b43ff1a56a2 |
| Tests | CLEAN (S1 SUGGESTION only) | `test_builder.py:27233-27467,27875-27878`; `gate36b_head.log` (rc 0); `mutants.log` (30/31 KILLED, survivor S1); `cli_reach_probe.log`; `images_compare.txt` | R384-2 | be6b48c140db1692caedbdf997495b43ff1a56a2 |
| Docs | CLEAN (S2 SUGGESTION only) | `PP_DESCRIPTOR_OWNERSHIP.md:89,93,99,182-237,341,399`; `ENDSTATION_BUILDER.md:130-145,212-214,574-596`; PR #612 body; `docs_gates.log`; hosted `docs-check-no-git` success | R384-2 | be6b48c140db1692caedbdf997495b43ff1a56a2 |

Every lens is covered at the merge-candidate source head itself. Any later commit that touches a lens's scope un-covers that lens.

## Prior public review findings on PR #612

I read these only after the verdict, findings and ledger above were written. At report time PR #612 has no review objects and no inline review comments. Its thread holds my round-1 review (5866336473), the external round-1 review (5866373356), and manager start notices. I have not read any round-2 review from the other reviewer.

| Prior finding | Status at be6b48c1 | Evidence |
|---|---|---|
| [R384] F1 MAJOR: the check does not run on the deployed-image emitter | RESOLVED under decision option (a) | See the re-verification table. The SoC `[1,0]` plant is REFUSED `L6_ORDER` (`receipts/soc_path_probe.log`). The bypass mutants are KILLED. The reproduction command reaches the check. The emitters are named in the document |
| [R384] F2 MINOR: a zero-entry rate list passes | RESOLVED | `L10_EMPTY`; committed fixture; mutant KILLED; edge probe REFUSED |
| [R384] F3 SUGGESTION: reader hardening | TAKEN in part: offset 76, row presence and current-rate membership are implemented. Trailing CLOCK_DOMAIN bytes are not adopted; this round's S3 retains that as optional | `receipts/edge_probe.log` |
| [R385] F1 MAJOR: the parent check does not guard the image that ships (same defect, including its generator-level plant in `avdecc/aem_descriptors.py` `d_clock_domain`) | RESOLVED under option (a). I re-ran the generator-level variant myself in a farm copy. The loader accepts the planted `[1,0]` list, and then both the builder emitter and the SoC emitter REFUSE it with `L6_ORDER`. The finding's equivalence requirement is gated too: `test_soc_shipping_image_contract` asserts builder bytes equal SoC bytes for all five configurations (`test_builder.py:27414-27416`). The checker docstring's "before shipping the image" now holds for both emitters | `receipts/generator_plant_probe.log`, `receipts/images_compare.txt`, `receipts/gate36b_head.log` |
| [R385] F2 MINOR: a zero-entry rate list passes (retains [R384] F2) | RESOLVED | as [R384] F2 |
| [R385] S1 SUGGESTION: offset 78, trailing bytes, vacuous pass with no rows, current rate unchecked | Offset 78 is now `L6_OFFSET`, the vacuous pass is now `L10_MISSING`/`L6_MISSING`, and the current rate is now `L10_CURRENT`. Trailing bytes are still accepted and remain optional (this round's S3) | `receipts/edge_probe.log` |

## Real limits

- I ran only the focused gates 36a/36b (six functions), the focused docs and idiom gates, and disposable probes. I did not run the full builder, parent, processor, gPTP, Verilator or Yosys banks, per instructions. Scoped Verilator was neither used nor identity-checked, because the diff contains no HDL.
- The SoC emitter was executed from its own function source, not through a LiteX elaboration: LiteX and migen are absent here, so only `_builder_out` is stubbed. That the returned bytes are the ones `main()` CRC-binds and writes rests on code reading (`receipts/scope.txt`), not on execution. The import resolution was replayed from milan_soc's own `sys.path` inserts, not observed in a real LiteX environment. A distribution named `sw` installed in a build environment could in principle shadow the namespace package, and I cannot inspect that from here.
- `gen_toc.py --check/--verify-anchors` were NOT RUN locally (renderer absent). I rely on hosted `docs-check` for them, and it was still in progress when I last checked.
- The brief lists `checker_sweep` among my round-1 probes, but my round-1 packet contains no script by that name. I did not read the other reviewer's script of that name. My round-1 boundary sweep was `edge_probe.py` plus `mutants.py`, and both were re-run and extended here. `generator_plant_probe.py` needs its farm's `avdecc/aem_descriptors.py` as a real copy; I made that copy by hand after `make_farm.sh`, and the script asserts it.
- The mutants are my own condition-removal forms. I did not re-execute the executor's round-2 campaign, whose receipts were not public at report time.
- Physical calibration NOT RUN. No bitstream, deploy, flash or hardware claim is made. The hosted `Physical gPTP (nightly and manual)` context is skipped, which is not an executed pass.

## Pending manager duties

- Hosted exact-head contexts, observed read-only at 09:22 UTC (`receipts/hosted_checks.txt`). Executed and successful: `rtl-fast`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0-3, Verilator shards 0 and 3, `full-ci-gate`, `changes`, `bdd-conformance`, `wire-accountability`, `docs-check-no-git`. In progress: `docs-check`, `elaborate`, Verilator shards 1, 2 and 4. Skipped: `Physical gPTP (nightly and manual)`. Hosted and act acceptance remain with the manager.
- The manager's round-2 builder and native bank receipts, and the [A413] round-2 packet, were not yet public on the evidence branch or in the threads at report time. Publishing them remains with the manager.
- The current-dev candidate build and validation (source base 54ce8773, live dev 1fa2357f), candidate-merge validation and post-merge containment remain with the manager.
- The optional follow-ups S1-S3 are for the maintainer or manager to accept or decline.

## Probe hygiene

All mutation, gate, edge, bound, generator-plant and reproduction runs used symlink farms or `git archive` extractions under `$REVIEWS/577-r384-2-packet/scratch/`, with bytecode writing disabled. The extractions point their submodule paths at the clone's checked-out submodules, whose HEADs equal the gitlinks at all three commits (`receipts/tree_*.txt`). The docs, idiom and scope commands ran read-only in the clone. Disclosure: the first run of `soc_import_probe` used `python3 -I`, which ignores the bytecode setting. Because `nvm_shape.py` resolves its own directory through the farm symlink, that run created one ignored file in the clone, `scripts/__pycache__/nvm_contract.cpython-314.pyc`. I removed it, and the published script and receipt come from a re-run with `-B`. `receipts/restore.txt` records the final checks:
- HEAD and tree are exact.
- The index hash equals the session-start value.
- There is no content or mode difference against HEAD.
- `git status --porcelain --ignored` is empty in the clone and in all three checked-out submodules.
- Gitlinks are unchanged.
- No file in the clone or its submodules has an mtime after 11:08:30; the checkout was at 11:07:40.

R384-2 FINISHED
