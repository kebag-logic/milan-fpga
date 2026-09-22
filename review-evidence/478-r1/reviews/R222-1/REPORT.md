[R222] NEGATIVE - exact head d81a302760b84f32d2aa019643f57682bb6e052c

# R222-1: external cleared-context review of issue #478 / PR #512

- Reviewer and round: R222 (external, Opus), round R222-1, cleared context. No author scratchpad, private author reasoning or other reviewer's output was read. The `[R221]` verdict comment (5776222482) and the manager's R221-1 relay (5776222772) on PR #512 were deliberately not opened.
- Exact head: `d81a302760b84f32d2aa019643f57682bb6e052c`, tree `4903a00f30752bc86a99e9bf112ff5ad01827c5d`. The review clone matched both at the start and at the end (receipts/00, receipts/18).
- History: parent 1 is `099e191137dd2797407fb8345a452bcc7a965608` (A156's author commit on `b17580b91deb11f3441dfc5d7f9fafe539d929b8`). Parent 2 is `ec34fcdee0ca9ffa63564a9af8ad70a3a618de29` (dev after #505). Both commit messages are one line with no trailers.
- Pins at the head: protocol-processor `424c688fa2205b934a7689a58f2aa766420f2326` (unchanged; this is the parent pin, not the newer donor main), gptp-processor `c1b617435824929a790739ea8585c3fe1a328cc0`, verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The external submodule `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5` is not initialized and is not a dependency.
- Verdict: NEGATIVE. There is one open BLOCKER (F1), recorded under Conformance, Tests and Docs. RTL and Robustness are covered clean at this head. Two SUGGESTIONs are optional. The code for the frozen acceptance is correct and independently verified. The blocker is a documentation link added by this head, which fails two required hosted contexts.

## 1. Public sources reconstructed

Read in this order:

1. CONTRIBUTING.md and AGENTS.md at the head, docs/README.md, and REQUIREMENTS.md REQ-VER-03/04.
2. Issue #478: the body and all 12 comments. These include the readiness decision (5770832729), the assignment (5770949009), the PP89 scope link (5772948293), the integration (5774956261), the manager static completion (5775131861), the native completion (5775843006) and the current-dev candidate start (5775889448).
3. PR #512: the body and the `[A10]`/`[A169]` comments up to 2026-09-22T12:08:26Z.
4. The pinned processor authority at 424c688:
   - `docs/architecture/07_memory_maps.md` section 3.1, L10 (blob `5be7a4c49c34c6f5638d2a461eedc65dc4dc28a6`);
   - `06_aecp_engine.md` section 6.4;
   - `hdl/aecp/ucode/gen_ucode.py:1330-1398`, the SET_SAMPLING_RATE walk.
5. Milan v1.2 sections 5.3.3.3 and 5.3.5.1, and IEEE 1722.1-2021 7.2.3 (Table 7-5) and 7.4.21, from local copies.
6. The diff and both commits.
7. The public evidence archives `00ffa6bd`, `b671cc62` and `9c882d58`. Only executable evidence, logs and records were used.
8. The hosted check runs and job logs for the head.

The frozen task contract as reconstructed:

1. `_load_clocking` raises `ConfigError` for more than 8 entries, naming the walk bound and L10, and for a duplicate entry.
2. Gate 36a has a negative case for each refusal, and the five tracked configs still build.
3. The bound is one named constant beside `BASE_RATE_HZ`, with a comment pointing at the processor rule.

The readiness decision adds these items:

- a legal eight-entry boundary, and a nine-entry refusal with distinct entries;
- a focused gate that compares pp_shadow's `AU_RATES_C` values and declared length with `configs/endstation_arty_current.yaml`, where drift is refused and the pristine comparison passes;
- the hand-built image is kept;
- list order and all shipping rates are preserved;
- no donor or shipping-rate change;
- authority includes REQ-VER-03/04;
- the standard local, hosted, candidate and review bar applies.

Out of scope: the #399 marks, shipping-rate changes, PP89 packer enforcement and the #509 design. No requirement from those was applied here.

## 2. Findings

[R222] BLOCKER Conformance, Tests, Docs - docs/ENDSTATION_BUILDER.md:963 - the new relative link into the protocol-processor submodule is broken in both required documentation contexts
Requirement/evidence:
- What changed: row 8 adds `[processor section 3.1, L10](../protocol-processor/docs/architecture/07_memory_maps.md#31-descriptor-tree)`. It is the only Markdown link into that submodule anywhere in the tree.
- The gate: `scripts/docs_check.py` `_link_findings` (lines 642-654) reports every relative link whose target does not exist on disk.
- Where the gate runs:
  - `docs-check` runs it at `.github/workflows/docs.yml:51-52`. That is before its submodule step (`docs.yml:124-129`); the job comment at `docs.yml:12` says the documentation-only gates run before any submodule checkout.
  - `docs-check-no-git` (`docs.yml:444-452`) deletes `.git` and never initializes submodules.
  - Both contexts are among the seven that the `dev merge bar` ruleset requires (CONTRIBUTING.md section 2.1).
- The requirement: REQ-VER-04 (MUST), which the #478 readiness decision cites, requires the documentation gates to be green with zero policy findings.
- Independent reproduction:
  - In a git clone with uninitialized submodules, `docs_check.py` exits 1 at the head with `docs/ENDSTATION_BUILDER.md:963: broken link -> ../protocol-processor/docs/architecture/07_memory_maps.md`. It exits 0 at ec34fcde (receipts/11).
  - A `git archive` extraction without `.git` gives the same result (receipts/12).
- Hosted results: check runs 106731058055 (`docs-check`) and 106731058157 (`docs-check-no-git`) concluded failure with that exact line (receipts/13, receipts/14). They ran on GitHub's merge commit 9fea8a3c, whose tree 5aa23f2c is the same tree as the manager's candidate.
- Reader view: GitHub resolves the link from the rendered page to an HTTP 404. The same document at the pinned PP commit returns 200 (receipts/15).
- The manager's static command 12 (`docs_check.py`) passed only because its clones had initialized submodules.
Impact:
- Two required status contexts are red at the exact head and on the merge candidate, so the merge bar cannot be met.
- The hosted `docs-check` job stops at that step. Its later gates did not run for this head, including the End-station builder step (`docs.yml:172-175`), which runs gate 36a.
- A reader of the GitHub page, a tarball or a zip gets a dead link at the one place row 8 names its authority.
Required change:
- Row 8's L10 reference resolves in every configuration the required documentation jobs use: git and no-git, and before any submodule is initialized. It also resolves for a reader on GitHub.
- It still identifies the L10 rule at the parent pin 424c688.
- Row 8's behavioural content, gate 36a, the builder and all shipping bytes are unchanged, and no gate or workflow is weakened.
- For reference, the repository's existing convention for pinned submodule documentation is an absolute URL at the gitlink commit (for example `docs/design/GPTP_PLANE.md:32-35`).
Verification (at the corrected head):
- `python3 scripts/docs_check.py` exits 0 with 0 findings in (a) a git clone whose submodules are uninitialized and (b) a `git archive` extraction without `.git`. Restoring only the old link makes both exit 1 on this line.
- `check_doc_paths.py`, `check_doc_style.py`, `gen_toc.py --check`, `gen_toc.py --verify-anchors`, `check_em_dash.py --base <merge-base>` and `git diff --check` pass.
- Hosted `docs-check` and `docs-check-no-git` succeed; `docs-check` runs through its builder step.
- `receipts/probe_artifacts.py` still produces a manifest byte-identical to receipts/06.
- An independent re-review covers Conformance, Tests and Docs.

[R222] SUGGESTION Tests - tb/verilator/pp_shadow/sim_main.cpp:829,850,879-880 - four hand spellings of the AUDIO_UNIT rate list sit outside the settled AU_RATES_C comparison
Requirement/evidence:
- What the gate covers: the readiness decision settled a comparison of `AU_RATES_C` values and declared length (sim_main.cpp:827-828). Gate 36a implements it, and every value, order, length, initializer, declaration and YAML-drift control is refused (receipts/05).
- What it does not cover. The bench spells the list's shape in four more places:
  - `AU_CUR_RATE_C = 48000u` (829), the YAML `sampling_rate_hz`;
  - `AU_LEN_C = 144 + 4 * 3` (850);
  - the image's `sampling_rates_count` literal `put16be_v(d, 142, 3)` (879);
  - the fill loop bound `k < 3` (880).
- Each can drift while the gate stays green (the receipts/05 RESIDUAL rows). One such case: the YAML and `AU_RATES_C` both shrink to two entries while the count and loop stay at 3, so the loop would read `AU_RATES_C[2]` past its end.
- The `must contain literal rate words` arm (test_builder.py:23602-23603) has no control either, though it fails closed.
Impact: none today, because every spelling agrees with the YAML. A later partial edit of the bench could pass the gate while the hand-built image disagrees with its own array.
Required change: optional and outside the frozen contract. A follow-up issue could derive the count, loop bound and length from `AU_RATES_C` in the bench, or extend the comparison to the current rate and the count.
Verification: the RESIDUAL rows of `receipts/probe_mutants.py` would change from PASS to refused.

[R222] SUGGESTION Docs - docs/ENDSTATION_BUILDER.md:963 - say that eight is a loader bound; the packed-image path accepts only 48, 96 and 192 kHz
Requirement/evidence:
- Row 8 says lists over eight entries raise `ConfigError` and that gate 36a covers "the eight-entry boundary". It does not state the image consumer's own rule: `avdecc/aem_specs.py:219-221` (`spec_from_overlay`) refuses any rate outside 48000/96000/192000.
- An eight-entry list passes `_load_clocking` and `load_config`, but the image path raises `ValueError` (receipts/16). Because duplicates are refused, at most three distinct base rates can reach an image.
- The gate's in-code comment (test_builder.py:23529-23531) and the PR body ("a legal eight-entry loader boundary") already say this. The authoritative row does not.
- Pre-existing, not introduced here: the row's line citations (`_marks_media_clock` line 4171, now at 4480; `aem_specs.py` line 198) come under the page's "at the time of writing" rule.
Impact: a reader could take eight advertised rates as an end-to-end capability of the builder.
Required change: optional. Name the image path's base-rate restriction next to the bound.
Verification: read row 8 against `avdecc/aem_specs.py:219-221` and receipts/16.

## 3. Clean lenses

[R222] PASS RTL - diff ec34fcde..d81a3027 (3 files, none under hdl/ or tb/); gitlinks; receipts/06; protocol-processor@424c688 hdl/aecp/ucode/gen_ucode.py:1330-1398; avdecc/aem_descriptors.py:259-265 - checked no RTL, bench or pin change; RTL-facing headers, gptp_ucode.hex and tracked generated files byte-identical for all five configs; bound 8 = pinned SSR_WALK_MAX (walk at offset 144, refuses past the eighth); 16-bit count field cannot overflow; no CDC, reset, FSM or timing change

[R222] PASS Robustness - sw/builder/endstation_builder.py:3786-3810; receipts/05; receipts/16 - checked 8 accepted, 9 distinct and 9 duplicates refused by count, empty list by membership; duplicates after integer conversion refused; order preserved; omitted list defaults to [sampling_rate_hz]; check order decides no case; loading deterministic; malformed-type handling unchanged; reset/backpressure/timeout inapplicable to a build-time loader

Detail behind the two clean lenses:

RTL:
- The generated headers compared were `adp_shape_defaults.svh`, `aecp_aem_rom.svh`, `lwsrp_csr_defaults.svh` and `lwsrp_table.svh`, plus the tracked generated files that `build()` rewrites. Every one is byte-identical at ec34fcde and d81a3027 for all five configs.
- The pinned microprogram walks entries 0..count-1 at `SSR_LIST_OFF` 144. `SSR_WALK_MAX` is 8, and it refuses any entry past the eighth. The builder bound equals it.
- `sampling_rates_count` is written as a 16-bit field (`avdecc/aem_descriptors.py:261`), which cannot overflow at a maximum of 8.

Robustness:
- Boundaries: eight entries are accepted. Nine distinct entries and nine duplicates are both refused by the count cause. An empty list is refused by the membership cause.
- Duplicates are refused after integer conversion (`[48000, "48000"]`).
- Order is preserved: the unsorted eight at the loader, and three base rates in a new order all the way to the packed image.
- An omitted list defaults to `[sampling_rate_hz]` for each base rate.
- The order of the checks decides no gate case: the swapped-order mutant still passes.
- Loading is deterministic: the manifests are identical across base and head (receipts/06).
- This change closes the only L10 violation that could reach an image before it: nine copies of 48000 packed with count 9 at ec34fcde. The head refuses that list (receipts/16).
- Malformed-type handling is unchanged. A scalar or null still raises `TypeError` at both commits. A string is refused at both commits, by a different cause.

## 4. Lenses applied but not clean at this head

Conformance was applied. Every acceptance criterion and readiness-decision item is met. The lens stays open only because F1 breaks REQ-VER-04 at this head.

| Item | Result | Evidence |
|---|---|---|
| AC1: count refusal names the walk bound and L10 | met | endstation_builder.py:3801-3806; message in receipts/16 |
| AC1: duplicate refusal | met | endstation_builder.py:3807-3808; receipts/05 |
| AC2: a negative case per refusal, and the five configs build | met | test_builder.py:23543-23570 and 23572-23587; receipts/03, receipts/06; manager builder log 40.log |
| AC3: one named bound beside `BASE_RATE_HZ` with a rule comment | met | endstation_builder.py:1197-1200; no second parent-side bound (git grep over the tree) |
| Legal eight and a distinct nine | met | test_builder.py:23532-23535 and 23544; mutants 8->9, 8->7 and `>` to `>=` are caught |
| pp_shadow values and declared-length drift gate | met | test_builder.py:23590-23636; receipts/05 |
| Order, defaults and shipping rates kept; no donor or shipping change | met | receipts/05, receipts/06; gitlinks and configs/ unchanged |
| L10 and the IEEE/Milan reading | correct | 07_memory_maps.md:92 and gen_ucode.py:1330-1331; 1722.1-2021 Table 7-5 fixes offset 144 and allows S up to 91, so the processor's 8 is stricter; Milan v1.2 5.3.3.3 requires the list to report the supported rates and the current rate to be one of them |
| REQ-VER-03 | met | builder tests build all five shipping configs (receipts/03, receipts/06, hosted elaborate) |
| REQ-VER-04 | not met at this head | F1 |

Tests was applied.

- Gate 36a is wired into the normal run: test_builder.py:23957-23959, docs.yml:172-175 and elaborate.yml:247. It ran in the manager's builder log and in the hosted `elaborate` job on the merge commit (receipts/14 elaborate log).
- Each of its three functions fails on its own defect. At ec34fcde with head's test file, only the loader contract fails ("distinct ninth entry accepted"); the image and pp_shadow parts pass (receipts/04). All 29 mutation rows matched their expectations (receipts/05).
- The shipping-image check reads the packed image, not the overlay: a reversed overlay is caught.
- The test hardcodes L10's eight instead of importing the builder constant.
- The lens stays open because F1 leaves two required regressions red.

Docs was applied.

- Row 8 and the gate 36a docstring entry describe the implemented contract accurately.
- Gate 32's key map passes.
- The fast documentation gates pass locally once submodules are initialized (receipts/10).
- The lens stays open because of F1.

## 5. Specific assessments requested

- **Frozen acceptance.** AC1-AC3 and every readiness-decision item are met (section 4). Nothing was widened: there is no donor code, no shipping-rate change, no pp_shadow source or Makefile change, and no generated header.
- **Loader-only eight-entry boundary.** The legal eight uses deliberately non-base rates and calls `_load_clocking` directly (test_builder.py:23532-23535). The test comment says these are loader inputs, not a claim of format or runtime support. This matches the settled scope.
- **Distinct causes.** The ninth-entry fixture has nine distinct values and must name `8`, `walk` and `L10`. The duplicate fixtures must name `duplicate`. Removing either refusal, or moving the duplicate check onto raw pre-conversion values, fails the gate for that arm alone (receipts/05).
- **Order and defaults.** A sorting mutant and a changed default are both caught. Order also survives into the packed image (receipts/16).
- **Named single bound.** `MAX_AUDIO_UNIT_RATES = 8` sits at endstation_builder.py:1200, right after `BASE_RATE_HZ` (1197), with a comment naming the PP file, section 3.1, L10 and offset 144. No other parent-side bound exists: the generated `AEM_RATES_N_C` and `AEM_RATES_C` tables are derived from the list.
- **Gate 36a wiring and independent failure.** See the Tests paragraph in section 4. One caveat: at this head the hosted `docs-check` builder step did not run, because of F1.
- **pp_shadow comparison and controls.** The comparator strips comments and requires exactly one literal declaration. It checks the declared length and the literal words, and compares against the raw YAML list. The five fixture controls and my mutations of the real `sim_main.cpp` and YAML are all refused. `tb/verilator/pp_shadow/Makefile:34` elaborates the `endstation_arty_current` shape, so the gate compares against the right config. The residual spellings are SUGGESTION S1.
- **The five shipping images and the scope of the unchanged-byte evidence.**
  - Author scope (099e191 against b17580b9, `author/check-rate-images.py`): per config, the YAML SHA-256, the packed `aem_desc.bin` SHA-256 and the AUDIO_UNIT offset, count and rates. The PR body's claim is worded to that scope.
  - My scope (d81a3027 against ec34fcde): the YAML bytes, the normalized `load_config` result, the overlay, `aem_desc.bin`, `aem_desc.json`, `aem_desc.map`, the AUDIO_UNIT words read back from the image, all ten `build()` outputs per config, and the tracked generated files `build()` rewrites. The manifest `2304061affaf693ce4767a90d2464a93bf0548f0063d267a8a295d5c13c944d5` is identical on both sides (receipts/06). The author's five image and config hashes reproduce exactly (receipts/08).
  - Neither scope covers LiteX or Vivado outputs, bitstreams or firmware binaries. The normalized configuration handed to them is byte-identical, and hosted `elaborate` passed on the merge commit.
  - Advertised lists: arty_current is [48000, 96000, 192000]; the other four are [48000]. All five use offset 144.
- **Loader acceptance versus downstream support.**
  - `_load_clocking` and `load_config` accept up to eight distinct entries (receipts/16).
  - The packed-image path (`aem_specs.spec_from_overlay`) accepts only 48, 96 and 192 kHz.
  - The render path runs at 48 kHz, with one plan mark per unrunnable rate (#399, out of scope).
  - The processor accepts SET_SAMPLING_RATE only for a rate within the first eight listed entries.
  - The issue body's statement that the builder bounds neither the length nor the content of the list holds for the loader. At image time the content was already restricted to the base rates, so before this change a duplicate-padded list was the only over-length list that could reach an image. SUGGESTION S2 covers the documentation of this.
- **PP pin.** The head and the candidate tree both carry protocol-processor 424c688 (receipts/09). All authority was read at that pin.
- **#505 integration and attribution.** The head merges ec34fcde (#505) into 099e191. `git merge-tree` of those parents writes exactly tree 4903a00f. The dev side touched only `docs/testing/CI_WORKFLOWS.md` and `scripts/ci_events.py`. The author evidence in the archives is tagged to 099e191 and base b17580b9 (`author/git-final.txt`).
- **Unchanged issue delta.** The full-index patch SHA-256 is `f072ec203633281a03ef10331e934a50bf0713091cd2b54bc28cd48391906ad6` for all three of: b17580b9..099e191, ec34fcde..d81a3027, and 88e9276b..5aa23f2c. The per-file blob IDs are identical (receipts/01, receipts/09).
- **Current manager evidence identity.**
  - Archive b671cc62: all 195 manifest entries verify (receipts/07). Its manager records name head d81a3027, tree 4903a00f, base ec34fcde, gitlinks equal to mine, and submodule trees 1b073c8b, 25909c4d and 54432ffb, which match the review clone.
  - Every file in archive 00ffa6bd is carried unaltered into b671cc62; only `MANIFEST.json` was updated (receipts/07b). Archive 9c882d58 (291 entries, all verified) adds 96 files to b671cc62, again changing only `MANIFEST.json` among existing files (receipts/07c).
  - The claimed candidate tree 5aa23f2c equals my `git merge-tree` of d81a3027 with 88e9276b and GitHub's merge commit 9fea8a3c. #507's paths are disjoint from the issue delta.
  - Candidate 443c46ac is recorded as superseded, not a pass.
- **Later validation comments.**
  - The trusted act replica for this head was interrupted: exit 130 after SIGINT, wrapper exit 1. No local replica passed.
  - The current-dev candidate units were stopped and do not count.
  - The hosted docs failure is acknowledged publicly. A169 has taken a one-line correction. No corrected head existed at 2026-09-22T12:10:22Z.
- **Non-evidence.** Builder gate 11 (calibration report absent) is NOT RUN. The four `tsn_fuzz` field-campaign skips contribute zero checks. Neither is hardware evidence, and this round claims none.

## 6. Ledger (published by reviewer R222)

| Lens | Covering round | Exact head | State |
|---|---|---|---|
| Conformance | R222-1 | d81a302760b84f32d2aa019643f57682bb6e052c | applied, not clean: F1 open |
| RTL | R222-1 | d81a302760b84f32d2aa019643f57682bb6e052c | covered clean |
| Robustness | R222-1 | d81a302760b84f32d2aa019643f57682bb6e052c | covered clean |
| Tests | R222-1 | d81a302760b84f32d2aa019643f57682bb6e052c | applied, not clean: F1 open |
| Docs | R222-1 | d81a302760b84f32d2aa019643f57682bb6e052c | applied, not clean: F1 open |

Coverage is banked against d81a3027 only. A correction commit that touches `docs/ENDSTATION_BUILDER.md` un-covers Docs. Any later integration of dev brings artifacts that the next round must place in or out of each lens's scope. This round approves no later head.

## 7. Open findings

- F1, BLOCKER (Conformance, Tests, Docs): the broken submodule link at docs/ENDSTATION_BUILDER.md:963. Open.
- S1 (Tests) and S2 (Docs) are SUGGESTIONs. They are optional and do not affect coverage.

## 8. Limits

- By instruction, there were no full native RTL, Yosys, processor or behave reruns, no act or Docker, and no hardware, installs or privilege. The native results come from manager archive b671cc62, after verifying its manifest and its head, tree and gitlink identity. I did not re-execute them.
- Focused probes ran in isolated scratch clones built only from the review clone's object stores (`receipts/setup_scratch.sh`). They used Python 3.14.7 and PyYAML 6.0.3. No HDL, C or C++ build was run.
- The current-dev candidate commit 443c46ac is not published (the fetch was refused). Its identity was checked through its tree only.
- Milan and IEEE clause text was read from local copies of Milan v1.2 (Consolidated, 2023-11-30) and IEEE Std 1722.1-2021, limited to the clauses listed in section 1.
- Not read:
  - `author/DECISIONS.md` and `author/HANDOFF.md` in the archives;
  - the archive's `link-proposal/*` and `hosted-failure/diagnosis.md` (F1 was reproduced independently);
  - the `[R221]` comment and the manager's R221-1 relay;
  - any author or other-reviewer local directory.
- The hosted state is a snapshot at 2026-09-22T12:10:22Z (receipts/13-hosted-final-snapshot.txt).
- The review checkout's final HEAD, tree, index file, index entries, worktree blobs, file kinds, modes and submodule states equal the baseline (receipts/00, receipts/18).
- Observation outside the frozen scope, not a finding: a scalar or null `audio_unit_rates_hz` raises `TypeError` rather than `ConfigError`. This is identical before and after this PR. It could become a separate issue if wanted.

## 9. Outstanding manager obligations

1. Correct F1 through the sole-author lane (A169 has taken it) and publish the result as a new head. Independent reviewers must then re-review that head, covering at least Conformance, Tests and Docs. A reviewer must publish or accept a five-lens ledger at the final head. RTL and Robustness coverage from this round carries forward only if that ledger shows nothing in their scope changed.
2. Hosted: all seven required contexts on the final head.
   - `docs-check` and `docs-check-no-git` fail at d81a3027.
   - `rtl-fast` succeeded at d81a3027 and must be earned again on the new head.
   - At d81a3027 there is no exact-head exhaustive evidence. The ready-state `rtl-full` run 35723340811 was cancelled: Verilator shards 1/5 and 4/5 were cancelled, and the `verilator-suites` check run 106734761918 failed. Run 35724442058 then ran with `PR_DRAFT: true`, so both aggregates were skipped.
3. The trusted act-first replica must pass on the final head, invoked from a clean trusted dev worktree. The ready replica for d81a3027 was interrupted, so no local replica has passed.
4. The full native bar must pass on the final head. Candidate validation must pass against the live dev tip at that time; the 443c46ac candidate against 88e9276b is superseded and does not count. Repeat both if dev moves again.
5. Before merge: two independent positives at the final head (R221 internal, R222 external), no review round in flight, and explicit maintainer authorization. After merge: containment and the integrity audit (`check_merge_containment.py`, `check_merge_review_integrity.py`), then Issue closure and Project Done.
6. Keep gate 11 NOT RUN and the four field-campaign skips labelled as non-evidence, and make no hardware claim.

## 10. Receipts (receipts/)

| File | Content |
|---|---|
| 00-baseline-integrity.txt / 18-final-integrity.txt | review-clone integrity before and after |
| 01-issue-delta-identity.txt | patch and blob identity across 099e191 and d81a3027; merge-tree of the head's parents |
| 02-scratch-*-setup.txt, setup_scratch.sh | scratch clone construction |
| 03-head-gate36a-focused.txt, probe_run_gates.py | gate 36a (three functions) and gate 32 at the head |
| 04-base-builder-head-gate.txt | head's gate 36a against the ec34fcde builder |
| 05-mutation-probes.txt, probe_mutants.py | 29 builder, image and pp_shadow mutation and residual rows |
| 06-artifacts-{base,head}.json/.log, 06-artifact-compare.txt, probe_artifacts.py | full builder artifact manifests, base against head |
| 07-evidence-manifest-verify.txt, 07b-archive-relation.txt, 07c-archive-9c882d58.txt | manager and author archive identity |
| 08-author-image-evidence-crosscheck.txt | the author's hashes reproduced |
| 09-current-candidate-identity.txt | candidate tree, #507 disjointness, GitHub merge commit |
| 10-head-static-gates.txt | 14 fast documentation, idiom and ratchet gates at the head, submodules initialized |
| 11-docs-check-uninitialized-submodules.txt, 12-docs-check-no-git-repro.txt | F1 reproduction, head against base |
| 13-hosted-*.json/.txt, 14-hosted-job-*.log | hosted check runs, workflow runs and job logs |
| 15-github-link-resolution.txt | HTTP status of the row 8 link as GitHub resolves it |
| 16-downstream-{head,base}.txt, probe_downstream.py | loader versus image path, and malformed input |
| 17-pinned-authority.txt | L10 and microcode blobs and lines at 424c688 |
| issue478*.json, pr512*.json | public issue and PR records as fetched |

R222-1 FINISHED
