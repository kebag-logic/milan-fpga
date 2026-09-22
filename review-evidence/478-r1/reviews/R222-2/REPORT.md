[R222] POSITIVE - exact head 1496558d82cf35fc98dda0e781b2a1be643c301a

# R222-2: external cleared-context re-review of issue #478 / PR #512 (corrected head)

- Reviewer and round: R222 (external, Opus), round R222-2, cleared context. This round started from the public review-start comment 5778185837.
- Not opened: any author scratchpad or private reasoning, any local lane directory (author, link-author or reviewer), the `[R221]` comment 5776222482 (its body is replaced by its SHA-256 in `receipts/pr512-issue-comments.json`, see `receipts/15-redaction.txt`), the archive's `reviews/R221-1/`, `author*`, `link-proposal/` and `hosted-failure/` contents (these blobs were hashed for manifest verification only). My own round-1 report was reconstructed from its public PR comment 5776361061 only.
- Exact head: `1496558d82cf35fc98dda0e781b2a1be643c301a`, tree `e8d797554a935c5514e25be9e1dda119f4f8c999`. The review clone matched both at start and end. Blob, mode, kind, index and submodule states are identical (`receipts/integrity-start.txt`, `receipts/integrity-final.txt`, `receipts/integrity-final-refs.txt`).
- History (`receipts/01-history-identity.txt`):
  - The head is the merge of `2b2009488351f04f4cc4d2d316ad6d5f6f1e8ba7` (A169's one-line link correction on `d81a302760b84f32d2aa019643f57682bb6e052c`) with dev `88e9276b2a220c716f64a843f7e1eb8f9265e896` (#507).
  - `git merge-tree` of those parents writes exactly tree `e8d79755`.
  - Every branch commit is one line with no trailers.
- Pins at the head: protocol-processor `424c688fa2205b934a7689a58f2aa766420f2326`, gptp-processor `c1b617435824929a790739ea8585c3fe1a328cc0`, verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. `.gitmodules` is unchanged. The external submodule `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5` is uninitialized and is not a dependency.
- Verdict: POSITIVE. My round-1 finding F1 (BLOCKER; Conformance, Tests, Docs) is resolved at this head. No new BLOCKER, MAJOR or MINOR was found. All five lenses are covered clean by this round at this head. No coverage is carried over from R222-1. The two optional round-1 SUGGESTIONs are unchanged, not adopted, and recorded on #495. They do not affect coverage.
- This verdict is a review verdict only. Act, hosted, current-dev candidate and post-merge duties are still pending with the manager (section 9).

## 1. Public sources reconstructed

Read in this order:

1. AGENTS.md, CONTRIBUTING.md, docs/README.md, and REQUIREMENTS.md REQ-VER-03/04 at the head.
2. Issue #478: the body and all 13 comments (`receipts/issue478*.json`). These include:
   - the readiness decision 5770832729;
   - the assignment 5770949009;
   - the PP89 scope link 5772948293;
   - the round-2 manager completion 5777273263.
3. PR #512:
   - metadata fetched with explicit `--json` fields only, with no status rollup (`receipts/pr512.json`);
   - every `[A10]` and `[A169]` comment, and my own `[R222]` round-1 comment.
4. Issue #495, reading only the lines that route R222-1 S1/S2 (`receipts/issue495*.json`).
5. The pinned protocol-processor authority at `424c688`:
   - `docs/architecture/07_memory_maps.md` (blob `5be7a4c4`): heading 3.1 at line 54, L10 at line 92;
   - `docs/architecture/06_aecp_engine.md` (blob `f8ccc9a7`), the SET_SAMPLING_RATE row;
   - `hdl/aecp/ucode/gen_ucode.py` (blob `0057cb17`), lines 1312-1397.
6. Milan v1.2 (Consolidated, 2023-11-30) Sections 5.3.3.3 and 5.3.5.1, and IEEE Std 1722.1-2021 Table 7-5 (7.2.3), from local copies (`receipts/11-clauses-and-pp-authority.txt`).
7. The diff and all four branch commits.
8. The immutable evidence archive `3811227e` (`review-evidence/478-r1`). I verified the manifest and read only `round2/manager` and `round2/candidate.json` (`receipts/06`, `receipts/07`).

Frozen contract used (unchanged from round 1):

- AC1: `_load_clocking` refuses more than 8 entries, naming the walk bound and L10, and refuses a duplicate.
- AC2: gate 36a has a negative case per refusal, and the five configs still build.
- AC3: the bound is one named constant beside `BASE_RATE_HZ`, with a comment naming the processor rule.
- Readiness additions:
  - a legal eight-entry boundary, and a distinct nine-entry refusal;
  - a pp_shadow `AU_RATES_C` value and declared-length drift gate against `configs/endstation_arty_current.yaml`;
  - the hand-built image kept;
  - order and shipping rates preserved;
  - no donor or shipping-rate change;
  - REQ-VER-03/04 apply.
- Out of scope, and not applied as acceptance: the #399 marks, PP89 packer enforcement, and #509 descriptor ownership.

## 2. F1 from R222-1: reconstructed, then resolved at this head

The header line below is deliberately not `[R222]`-led. That keeps `check_merge_review_integrity.py` from counting a resolved finding as a new open blocker. Severity and lenses are exactly as published in comment 5776361061.

F1 - BLOCKER - Conformance, Tests, Docs - docs/ENDSTATION_BUILDER.md:963 - the relative link into the protocol-processor submodule was broken in both required documentation contexts - STATUS AT 1496558d: RESOLVED

Requirement/evidence (as published at `d81a3027`):
- Row 8 linked `../protocol-processor/docs/architecture/07_memory_maps.md#31-descriptor-tree`.
- `scripts/docs_check.py` reports a relative target that is missing on disk.
- `docs-check` runs that step before its submodule fetch (`docs.yml:52` against `:129`). `docs-check-no-git` never initializes submodules (`docs.yml:444-452`).
- Both contexts are required. REQ-VER-04 requires the documentation gates to be green with zero findings.

Impact (as published):
- Two required contexts were red.
- `docs-check` stopped before its builder step, which runs gate 36a.
- Readers got a dead link at the row's authority.

Required outcome (as published):
- The L10 reference resolves in the Git and no-Git contexts before any submodule is initialized, and for a GitHub reader.
- It still identifies L10 at the parent pin `424c688`.
- Behaviour, gate 36a, the builder, the shipping bytes, the gates and the workflows are unchanged.

Verification performed at `1496558d`, one item per required outcome:

| Required outcome | Result at 1496558d | Evidence |
|---|---|---|
| Git checkout before any submodule is initialized | `docs_check.py` exit 0, 0 findings, 23/23 scrub and 4/4 routing arms | receipts/03 (all four submodule dirs empty) |
| No `.git` at all (a `git archive` extraction) | `docs_check.py` exit 0, 0 findings, 22/22 scrub and 4/4 routing arms, parity arm skipped by design; `check_feature_status.py` exit 0 | receipts/03; every archived regular file was hashed against its head blob and mode, with no mismatch reported (receipts/02) |
| Negative control, restoring only the old link | exit 1 in both contexts, exactly `docs/ENDSTATION_BUILDER.md:963: broken link -> ../protocol-processor/docs/architecture/07_memory_maps.md`; the control's blob is `7f167a12`, the round-1 blob; after restoring, blob `b66600c8` and exit 0 again | receipts/03 |
| The rest of the docs-check pre-submodule steps | all 20 runnable steps exit 0 in the uninitialized Git clone, so the job no longer stops before its builder step | receipts/04 |
| Target names the pinned PP commit and keeps the fragment | owner/repo equals the protocol-processor `.gitmodules` URL; the commit equals the gitlink `424c688`; the path is `docs/architecture/07_memory_maps.md`; the fragment `31-descriptor-tree` is the only heading anchor with that slug (the repository's own `gen_toc.anchor`), at line 54; L10 (line 92) sits inside that section, which ends at line 94 | receipts/05 |
| GitHub reader | unauthenticated GET returns HTTP 200; the served raw file hashes to blob `5be7a4c4`, the pinned blob; the page carries the anchor. Control: the old relative target resolved from the rendered parent page returns HTTP 404 | receipts/05 |
| Nothing else changed | the correction diff is one line, the link target only (receipts/01 word diff). The builder and test patch hash `7495cb1d` is identical at author, round-1 and head. Configs, tb/, hdl/, avdecc/, .github/ and gitlinks are unchanged against the base. Shipping bytes are identical (receipts/09) | receipts/01, receipts/09 |
| Focused documentation gates | `check_doc_paths`, `check_doc_style`, `gen_toc --selftest/--verify-anchors/--check`, `check_archive`, `check_em_dash --base 88e9276b` (1 added line, 57/57 arms) and `git diff --check` all pass | receipts/10 |

Resolution by lens:
- Docs: the link resolves in every context the required jobs use, and for a GitHub reader.
- Conformance: REQ-VER-04's documentation gates are green with zero findings in both required configurations, reproduced locally.
- Tests: the regression is caught. The old link fails both contexts, so the gate would catch a reintroduction. The job's pre-submodule chain is clear through to the builder step.

F1 is closed at this head. The hosted `docs-check`/`docs-check-no-git` success at this exact head was part of the published verification list. Under this round's CI boundary it is not inferred here. It moves to the manager duties in section 9. The manager's comment 5778134318 reports that docs, elaborate and rtl-fast passed at `1496558d`. That is manager-published evidence and was not inspected by this round.

## 3. Findings of this round

No new BLOCKER, MAJOR or MINOR.

Carried SUGGESTIONs from R222-1 are unchanged at this head. They are optional, not adopted in this frozen correction, and routed to #495. Both checklist lines exist there, with the original review link (`receipts/issue495.json`, comment 5776405000). They do not affect coverage.

[R222] SUGGESTION Tests - tb/verilator/pp_shadow/sim_main.cpp:829,850,879-880 - S1 (carried): four hand spellings of the AUDIO_UNIT list sit outside the settled `AU_RATES_C` comparison
Requirement/evidence:
- The readiness decision settled only the values and the declared length of the array (sim_main.cpp:827-828). Gate 36a enforces exactly that.
- Four more spellings are not compared:
  - `AU_CUR_RATE_C` (829);
  - `AU_LEN_C` (850);
  - the count literal (879);
  - the loop bound (880).
- Rows R1-R4 of receipts/08 each still pass the gate. This is recorded, not graded.
Impact: none today, because every spelling agrees with the YAML. A partial bench edit could pass the gate.
Required outcome: optional, and outside #478. #495 carries it.
Verification: the R rows in receipts/08 would turn into refusals.

[R222] SUGGESTION Docs - docs/ENDSTATION_BUILDER.md:963 - S2 (carried): say that eight is a loader bound, because the packed-image path accepts only 48, 96 and 192 kHz
Requirement/evidence:
- `avdecc/aem_specs.py:219-221` refuses non-base rates.
- The legal eight passes `load_config`, but the image raises `ValueError` (receipts/08 row F1). At most three distinct base rates can reach an image.
Impact: a reader could take eight rates as an end-to-end capability.
Required outcome: optional. #495 carries it, and #509 ownership stays separate.
Verification: read row 8 against aem_specs.py:219-221.

Observations outside the frozen scope. These are not findings and are identical at base and head (receipts/08 F9, F10):
- A scalar or null `audio_unit_rates_hz` raises `TypeError` rather than `ConfigError`.
- `int()` truncates a non-integer float such as `48000.5` to `48000`. A lone float is therefore accepted as a base rate. When it collides with an existing entry, the new duplicate refusal now catches it (F5).

## 4. Lens results (previously unclean lenses first)

Every lens below was applied at `1496558d`. None relies on the round-1 coverage at `d81a3027`.

[R222] PASS Conformance - sw/builder/endstation_builder.py:1197-1200,3788-3810; sw/builder/test_builder.py:23524-23636; docs/ENDSTATION_BUILDER.md:963; PP@424c688 07_memory_maps.md:92, gen_ucode.py:1330-1331,1384-1397; receipts/03,04,05,08,09,11 - AC1-AC3 and every readiness-decision item met; the builder bound equals the pinned L10 and SSR_WALK_MAX of 8; REQ-VER-04 documentation gates are green with zero findings in both required no-submodule contexts (F1 resolved); REQ-VER-03: all five configs build, with outputs identical to the base; Milan v1.2 5.3.3.3 and 1722.1-2021 Table 7-5 (offset 144, S at most 91) are read correctly

[R222] PASS Tests - sw/builder/test_builder.py:249-254,23524-23636,23957-23959; .github/workflows/docs.yml:52,175; .github/workflows/elaborate.yml:247; receipts/04,08; archive 3811227e round2/manager 40.log - gate 36a fails against the base builder for the distinct-ninth defect alone (B1); 11 of 11 non-equivalent builder mutants caught, and the equivalent check-order mutant passes; 8 of 8 real sim_main.cpp drift mutants and 6 of 6 real-YAML drift rows refused; legal C++ spellings (trailing comma, `U` suffix) accepted; gate wired into the builder main list and the docs and elaborate jobs; the docs-check pre-submodule chain passes, so the builder step is reachable; the manager's full builder and native runs at this head are verified by manifest and identity

[R222] PASS Docs - docs/ENDSTATION_BUILDER.md:963 (blob b66600c8); sw/builder/test_builder.py:249-254; PP@424c688 07_memory_maps.md:54,92 (blob 5be7a4c4); receipts/03,04,05,10 - the one link now names the parent gitlink's repository and commit and keeps the unique `#31-descriptor-tree` anchor of the section holding L10; GitHub serves the pinned bytes (HTTP 200); row 8 and the gate 36a docstring match the implementation; docs_check passes with and without .git before submodule initialization and fails on line 963 when only the old link is restored; 15 focused documentation, idiom and hygiene gates pass

[R222] PASS RTL - PR delta 88e9276b..1496558d (3 files, none under hdl/, tb/, syn/, sw/litex/, constraints/ or a submodule); gitlinks; avdecc/aem_descriptors.py:260-261; PP@424c688 gen_ucode.py:1330-1397; receipts/01,09,11,14 - no RTL, bench, synthesis or pin change since the base or since d81a3027; all 50 build outputs (including aecp_aem_rom.svh, adp_shape_defaults.svh, lwsrp_csr_defaults.svh, lwsrp_table.svh and gptp_ucode.hex) and the tracked generated headers are byte-identical base against head; the processor walks entries 0..count-1 at offset 144 and refuses past the eighth, so the builder's 8 closes exactly that gap; the count is a 16-bit field; the emitted AEM_RATES_* tables have no RTL consumer in parent hdl/ or processor hdl/; no clock, reset, CDC, FSM, width or timing effect

[R222] PASS Robustness - sw/builder/endstation_builder.py:3754-3810; avdecc/aem_specs.py:219-221; receipts/08 rows C8 and F1-F11, receipts/09 - 8 distinct accepted; 9 distinct and 9 copies refused by count; 8 copies refused as duplicates; empty and missing-current refused by membership; duplicates after integer conversion (`"48000"`, `48000.5`) refused; declared order survives into the packed image; an omitted list defaults to the current rate; the order of the checks decides no case; builds are deterministic across base and head; the malformed-type behaviour is unchanged from base; the loader is a pure build-time function, so reset, backpressure and timeout do not apply

Detail behind the lens lines:

| Item | Result | Evidence |
|---|---|---|
| AC1 count refusal names the walk bound and L10 | met: "has N entries; processor walk bound is 8 (L10, ... section 3.1)" | endstation_builder.py:3802-3806; receipts/08 F2 |
| AC1 duplicate refusal, after conversion | met | endstation_builder.py:3807-3808; receipts/08 C4, C5, F4, F5 |
| AC2 negative case per refusal; five configs build | met | test_builder.py:23542-23566; receipts/09 (all five built, 50 outputs); manager 40.log `ALL GATES PASS EXCEPT 1 NOT RUN` at 1496558d |
| AC3 one named bound beside `BASE_RATE_HZ`, with the rule comment | met | endstation_builder.py:1197-1200 |
| Legal eight; distinct nine | met; mutants 8->9, 8->7 and `>` to `>=` caught | receipts/08 A1, C1-C3 |
| pp_shadow values and declared length against YAML | met; value, order, length, zero-fill, comment, second declaration, hex and expression drift refused on the real file | receipts/08 D1-D8, E1-E2 |
| Order, defaults and shipping rates kept; no donor or shipping change | met | receipts/08 C6, C7, F6, F7; receipts/09; receipts/01 |
| Gate can fail for its defect | the head's gate against the base builder fails only the loader arm, with "distinct ninth entry accepted" | receipts/08 B1-B3 |

## 5. Specific confirmations requested

- **The PP eight-rate bound.** At `424c688`:
  - L10 (07_memory_maps.md:92) states offset 144 and a count of at most 8;
  - `SSR_LIST_OFF = 144` and `SSR_WALK_MAX = 8` (gen_ucode.py:1330-1331);
  - the walk covers k = 0, 2, 4, 6, with entries k and k+1, then refuses (1384-1397);
  - the builder's `MAX_AUDIO_UNIT_RATES = 8` is equal to it (receipts/11).
- **Duplicate refusal after conversion.** `[48000, "48000"]` and `[48000, 48000.5]` are refused at the head and accepted at the base, which packs count 2. A mutant that tests duplicates on the raw pre-`int()` values is caught (receipts/08 F4, F5, C5).
- **Positive eight-entry loader behaviour.** Eight distinct unsorted entries load in declared order through `_load_clocking` and `load_config` (A1, F1). The sorting mutant is caught (C6).
- **Gate 36a image versus loader limits.**
  - The eight-entry case is a loader boundary. The packed-image path refuses non-base rates with `ValueError`, at both base and head (F1).
  - Base rates in a new order reach the image in that order at offset 144, count 3 (F6).
  - Before this change, nine copies of 48000 packed count 9, an L10 violation. The head refuses them (F3).
  - The gate's in-code comment already says this is loader-only. S2 is the carried documentation suggestion.
- **pp_shadow literal drift controls.**
  - All of these are refused against the real `sim_main.cpp`: a value, the order, the declared length, a shortened initializer (implicit zero fill), a block-commented declaration, a second declaration, a hex word and an expression length (D1-D8).
  - YAML drift is refused too: shortened and reordered lists (E1, E2).
  - A duplicate in the shipping YAML is refused at load (E3). A second rate on a one-rate config is refused (E4).
  - Legal spellings still pass (D9, D10). The remaining residue is S1.
  - `tb/verilator/pp_shadow/Makefile:34` elaborates `endstation_arty_current`, so the comparison targets the right config.
- **Shipping bytes.** For each of the five configs, the base `88e9276b` and head manifests are byte-identical (manifest SHA-256 `7d47bd67...`). Each manifest covers:
  - the YAML bytes;
  - the normalized `load_config` result;
  - the overlay;
  - `aem_desc.bin`, `aem_desc.json` and `aem_desc.map`;
  - the AUDIO_UNIT words read back from the image;
  - the ten `build()` outputs.

  The tracked tree is clean after the builds in both clones (receipts/09). Advertised lists: arty_current is [48000, 96000, 192000]; the other four are [48000]. All five use offset 144.
- **Unchanged pins.** All four gitlinks and `.gitmodules` are identical at the base, at `d81a3027` and at the head (receipts/01). The manager's integrity records name the same submodule heads, trees and file counts as this review clone (receipts/07).
- **Documentation with Git and without Git, before submodules are initialized.** See section 2 and receipts/03-05.

## 6. Evidence identity and attribution

- Archive `3811227e`: all 672 manifest entries are tracked and SHA-256 verified. Every tracked file under `review-evidence/478-r1` is listed (receipts/06).
- Round-2 manager records, all with head `1496558d`, tree `e8d79755` and base `88e9276b` (receipts/07):
  - 40 static and builder commands, all exit 0;
  - the five native groups, all exit 0: the parent sweep (2,118,264 checks, 0 in-suite failures), Yosys, the pinned PP suites, the pinned gPTP suites and behave;
  - the builder and native integrity records verify 851 parent files and three required submodules, matching this clone.
- Attribution preserved:
  - author A156 evidence: `099e191` on `b17580b9`;
  - first-round manager evidence: `d81a3027` on `ec34fcde`;
  - A169 correction: `2b200948`;
  - superseded candidate `443c46ac`: not a pass;
  - round-2 manager bar: `1496558d` on `88e9276b`.
- Tool versions: the native Verilator logs report 5.052. Hosted and trusted act use the workflow-pinned 5.050. No native result is attributed to 5.050.
- Builder calibration gate 11 is NOT RUN (report not on disk). The four `tsn_fuzz` field-campaign skips contribute zero checks. Neither is physical or hardware evidence, and none is claimed.

## 7. Ledger (published by reviewer R222)

| Lens | Covering round | Exact head | State | Basis |
|---|---|---|---|---|
| Conformance | R222-2 | 1496558d82cf35fc98dda0e781b2a1be643c301a | covered clean | applied fresh at this head; F1 resolved |
| RTL | R222-2 | 1496558d82cf35fc98dda0e781b2a1be643c301a | covered clean | applied fresh at this head |
| Robustness | R222-2 | 1496558d82cf35fc98dda0e781b2a1be643c301a | covered clean | applied fresh at this head |
| Tests | R222-2 | 1496558d82cf35fc98dda0e781b2a1be643c301a | covered clean | applied fresh at this head; F1 resolved |
| Docs | R222-2 | 1496558d82cf35fc98dda0e781b2a1be643c301a | covered clean | applied fresh at this head; F1 resolved |

- Coverage is banked against `1496558d` only. No R222-1 coverage at `d81a3027` is relied on.
- A later commit that touches a lens's scope un-covers that lens.
- If the merge result is not `1496558d` itself, this head is an ancestor of the candidate, and AGENTS section 7 applies. Live dev `52711029` (#513) changes six paths that are disjoint from the issue delta. Two of them, `avdecc/gen_aem_store.py` and `avdecc/aem_maps.py`, lie on the packed-image path that gate 36a's shipping arm reads (`endstation_builder.py:2217`).
- An informative run of gate 36a and gate 32 on the computed candidate tree `93be2b57` passed (receipts/12, receipts/13). That is not candidate validation or coverage.

## 8. Open findings

- F1 (BLOCKER; Conformance, Tests, Docs) is resolved at `1496558d`.
- None open at BLOCKER, MAJOR or MINOR.
- S1 (Tests) and S2 (Docs) are optional SUGGESTIONs, unchanged, routed to #495, and do not affect coverage.

## 9. Outstanding manager duties (not inferred here)

1. **Trusted act replica.** It started for `1496558d` from clean live dev `88e9276b`, per the manager comment 5778014438. Its completion and result are pending, and a start is not a pass.
2. **Hosted checks.** All seven required contexts must conclude on the exact head:
   - including hosted `docs-check` and `docs-check-no-git`, the hosted half of F1's published verification;
   - including exhaustive `verilator-suites` and `yosys-portability`. Per comment 5778134318, the first rtl-full run on this commit evaluated `draft=true` and skipped them, so a recovery run was dispatched.
   - This round did not call any Actions, check-run or status API.
3. **Current-dev candidate.** Dev moved to `52711029`. The manager's candidate `72e16c61` has tree `93be2b57`, which I reproduced independently. Its 41+5 bar is pending. The manager must also settle whether #513's avdecc image-path change touches any lens scope under AGENTS section 7 (see section 7).
4. **R221's corrected-head re-review.** The merge bar needs two independent positives at the final head, no review round in flight, and the maintainer's merge authorization.
5. **After merge.** Run `check_merge_containment.py` and `check_merge_review_integrity.py`. Then close the Issue through `Closes #478` and move the Project item to Done.
6. **Labels stay as they are.** Keep gate 11 NOT RUN and the four field-campaign skips labelled as non-evidence. No hardware claim is made.

## 10. Limits

- By instruction, this round ran none of the following:
  - full native RTL, Yosys, processor or behave runs;
  - the full builder;
  - act or Docker;
  - the candidate's `act_ci.py` or its self-test on the host;
  - hosted-CI inspection;
  - installs, privileged commands or hardware;
  - source edits, commits, pushes, public comments or metadata changes.
- Native and full-builder results come from the verified manager archive at their original head.
- Focused controls ran only in isolated scratch copies (`$SCRATCH` = `/tmp/r222-478-r2-scratch`). They were built from the review clone's object stores with no hardlinks (receipts/02). Parallelism never exceeded 2 jobs.
- Tools: Python 3.14.7, PyYAML 6.0.3, Git 2.55.0.
- Two docs-check steps were not run locally, because their dependencies are not installed. Neither step reads the changed files:
  - the HDL-reference build, which needs the pinned `pyslang` wheel;
  - `gen_wavedrom`, which needs the `wavedrom` module.
- Network reads: `git fetch` of the public evidence commit and of live dev into scratch, and unauthenticated GETs of the GitHub blob and raw pages for the link target.
- Clause text was read from local copies of Milan v1.2 (Consolidated, 2023-11-30) and IEEE Std 1722.1-2021, limited to the clauses cited.
- Hosted state, act state and candidate state are as the manager published them at the times cited. They were not observed by this round.

## 11. Receipts (receipts/) and scripts (scripts/)

| Receipt | Script | Content |
|---|---|---|
| integrity-start.txt, integrity-final.txt, integrity-final-refs.txt, integrity-compare.txt | 00_integrity.sh | review-clone HEAD, tree, index, 855 entries' blob, mode and kind, submodules, refs; start equals final (taken after every other command) |
| 01-history-identity.txt | 01_history_identity.sh | parents, merge-tree, patch identity across author, round 1 and head, gitlinks, trailers |
| 02-scratch-setup.txt | 02_setup_scratch.sh | the four scratch copies and their identities |
| 03-f1-docs-nosub.txt | 03_f1_docs_nosub.sh | F1: docs_check in Git and no-Git without submodules, old-link controls |
| 04-docs-presub-steps.txt | 04_docs_presub_steps.sh | 20 docs-check pre-submodule steps in the uninitialized clone |
| 05-link-target.txt | 05_link_target.sh | URL, pin, anchor, L10 section, HTTP and raw-blob identity |
| 06-evidence-manifest.txt | 06_evidence_manifest.py | archive 3811227e manifest verification |
| 07-manager-evidence-facts.txt | 07_manager_evidence_facts.sh | round-2 manager identities, exits, versions, integrity |
| 08-gate36a-probes.txt | 08_gate36a_probes.py | gate 36a sections A-F: base cross-run, mutants, real-file drift, loader against image |
| 09-artifacts-{base,head}.json/.log, 09-artifact-compare.txt | 09_artifacts.py | shipping-byte manifests, base against head |
| 10-focused-static-gates.txt | 10_focused_static_gates.sh | 15 focused documentation, idiom and hygiene gates, submodules initialized |
| 11-clauses-and-pp-authority.txt | 11_clauses_and_pp_authority.sh | Milan and IEEE clause text, pinned PP L10 and microcode |
| 12-live-dev-identity.txt | 12_live_dev_identity.sh | live dev 52711029: disjointness and merge-tree identity (observation only) |
| 13-candidate-gate36a-info.txt | 13_candidate_gate36a_info.sh | informative gate 36a and gate 32 run on candidate tree 93be2b57 (not validation) |
| 14-rtl-scope-facts.txt | 14_rtl_scope_facts.sh | RTL-scope paths, AEM_RATES consumers, pp_shadow spellings |
| 15-redaction.txt | 15_redact_other_reviewer.py | the R221 body in the saved PR receipt replaced by its hash |
| issue478*.json, pr512*.json, issue495*.json | (gh, explicit fields) | public records as fetched |
| MANIFEST.sha256 | (sha256sum) | hashes of REPORT.md, scripts/ and receipts/ |

R222-r2 FINISHED
