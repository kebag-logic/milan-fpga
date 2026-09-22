[R222] POSITIVE - exact candidate 72e16c6172db723734317b105cff6c6e9168571a; PR source 1496558d82cf35fc98dda0e781b2a1be643c301a

# R222-3: external cleared-context candidate-integration review of issue #478 / PR #512

- Reviewer and round: R222 (external, Opus), coverage round **R222-3**, cleared context. Started from the public start comment 5778597964.
- Objects under review (both explicitly):
  - candidate `72e16c6172db723734317b105cff6c6e9168571a`, tree `93be2b5788c4b79e88bfe22fbaf985686bbdc8f2`;
  - its parents: live dev `52711029f374650dc93830d5ea28e81cb5c8f410` (tree `31ddc6b5`, #513 merged) and the unchanged PR source `1496558d82cf35fc98dda0e781b2a1be643c301a` (tree `e8d79755`).
- Verdict: POSITIVE. No BLOCKER, MAJOR or MINOR was found at the candidate. All five lenses were applied fresh at the candidate and are covered clean by R222-3 (ledger, section 8).
- What this round settles: my source-head round R222-2 (5778557281) was clean on all five lenses at `1496558d`. It withheld candidate coverage because #513 changed `avdecc/gen_aem_store.py` and `avdecc/aem_maps.py`, which sit on gate 36a's packed-image path. This round examined that dependency, and every other #513 artifact, on the actual combined tree. Disjoint paths were checked but were not treated as proof.
- No coverage is relabelled. R222-2's coverage stays banked against `1496558d` only. Nothing in the ledger rests on it.
- This is a review verdict only. It approves no pending gate (section 9).

## 1. Sources and what was not opened

Read, in order:

1. AGENTS.md, CONTRIBUTING.md, docs/README.md; REQUIREMENTS.md REQ-VER-03/04 at the candidate.
2. Issue #478: the body and all 13 comments (receipts `issue478*.json`), including:
   - readiness decision 5770832729;
   - assignment 5770949009;
   - PP89 scope link 5772948293;
   - round-2 completion 5777273263.
3. PR #512:
   - the public start 5778597964;
   - the manager's candidate/CI receipts 5778014438, 5778076390, 5778134318, 5778289141, 5778469586 and 5778505279;
   - my own public R222-2 report 5778557281.
4. PR #513: metadata and body (merge `52711029`, head `a769d9db`, tree `31ddc6b5`), and the manager validation comments 5776839776, 5777485129, 5778039813 and 5778092076.
5. Pinned protocol-processor authority at `424c688`:
   - `docs/architecture/07_memory_maps.md` (blob `5be7a4c4`): section 3.1 at line 54, L10 at line 92;
   - `hdl/aecp/ucode/gen_ucode.py` (blob `0057cb17`): lines 1330-1331 and 1384.
6. Milan v1.2 (Consolidated, 2023-11-30) section 5.3.3.3 and IEEE Std 1722.1-2021 section 7.2.3 / Table 7-5, from local copies. They are recorded by file SHA-256, section location and boolean layout checks only; no standards text is reproduced (receipt 11).
7. The candidate, source and dev objects, and the six #513 artifacts (section 2).
8. Public evidence archive `2102036d` (`review-evidence/478-r1`): the manifest was verified. I read `candidate2/` and my own `reviews/R222-2/`.

Not opened:
- any author scratchpad, private reasoning or local lane directory;
- `[R221]` comments 5776222482 and 5778469236 on PR #512, and `[R235]`/`[R236]` comments on PR #513. Their bodies are replaced by SHA-256 in the saved receipts (receipt 19);
- the archive's `reviews/R221-*`, `author*`, `link-proposal/`, `hosted-failure/` and `act-ready-interrupted/` contents. These were hashed only, for manifest verification.

Disclosure: the comment-index listing printed the first line, truncated at 170 characters, of every `[A*]` comment. Of those lines:
- two carried another reviewer's published verdict word: 5776222772 (R221-1) and 5777469953 (R236-1);
- one linked an R221 report packet: 5778469566.

Their bodies were not read. Separately, the #513 hosted-check receipt 5777485129, which I did read, names R236-1's verdict in passing. Nothing from any of these is used.

Frozen contract (unchanged from R222-2):
- AC1: `_load_clocking` refuses more than 8 entries, naming the walk bound and L10, and refuses a duplicate.
- AC2: gate 36a has a negative case per refusal; the five configs still build.
- AC3: one named bound beside `BASE_RATE_HZ`, with the rule comment.
- Readiness additions:
  - a legal eight-entry boundary and a distinct nine-entry refusal;
  - the pp_shadow `AU_RATES_C` value and declared-length drift gate;
  - the hand-built image kept;
  - order and shipping rates preserved;
  - no donor or shipping-rate change;
  - REQ-VER-03/04.
- Out of scope: the #399 marks, PP89 packer enforcement and #509 ownership.

## 2. The candidate and every #513 artifact on it

Identity (receipts 01, 03, integrity-start):
- `git merge-tree --write-tree 52711029 1496558d` writes exactly `93be2b57`. The merge base is `88e9276b`.
- **Issue patch unchanged**: `88e9276b..1496558d` and `52711029..72e16c61` are byte-identical (sha256 `aec58c21...`; `patch-id --verbatim` `0301ff6e...`).
  - The three issue files at the candidate are the source blobs: ENDSTATION_BUILDER.md `b66600c8`, endstation_builder.py `95ffb669`, test_builder.py `ea24c58c`.
- **#513 patch unchanged**: `88e9276b..52711029` and `1496558d..72e16c61` are byte-identical (sha256 `bcf40aee...`). The six #513 files at the candidate are the dev blobs.
- The two sides share no path.
- Gitlinks and `.gitmodules` (`39a5c43e`) are identical at `88e9276b`, `52711029`, `1496558d` and `72e16c61`:
  - PP `424c688`;
  - gPTP `c1b61743`;
  - verilog-axis `48ff7a7e`;
  - external `efeb541a`, uninitialized.
- The candidate commit is one line with no trailer.
- Live refs, read at 14:51:55Z and again at 15:15:24Z (end of round), unchanged: dev `52711029`; `validation/478-candidate2` `72e16c61`; branch and `refs/pull/512/head` both `1496558d`.

Each #513 artifact, and what it means for this PR's lens scopes:

| #513 artifact (candidate blob) | Change | Where it meets #478 | Evidence at the candidate |
|---|---|---|---|
| `avdecc/gen_aem_store.py` (`aa884381`) | docstring; `from collections.abc import Callable` (:100); new `_map_fixture` (:157); rewritten `_selftest_map_bounds` (:192); new `_selftest_map_deviations` (:290); `self_test` calls it (:424). `build_model` and `spec_from_overlay` live in unchanged siblings | Imported by gate 36a's loader arm (`load_config` -> `rtl_firmware_version`, endstation_builder.py:3007-3022) and by its shipping arm (`_entity_model_image`, :2201-2221) | Imported on both arms (receipt 13); outputs byte-identical (receipt 09); reverting it leaves gate 36a green, and its own self-test red (08 G5) |
| `avdecc/aem_maps.py` (`25636b2d`) | `KNOWN_MAP_DEVIATIONS` renamed from `AUDIO_MAP[1]` to `AUDIO_MAP[0]` (:107-112), plus a comment | Imported on the same arms. The allowlist is read only by the self-test; no builder code calls `assert_no_map_deviations` | Allowlist equals the builtin model's 6 deviations (receipt 12); revert or widen: gate 36a green, self-test red (08 G4, G6) |
| `.github/workflows/docs.yml` (`6495a125`) | docs-check step 41 `AEM store generator self-test` (:390); the job now has 44 steps | Gate 36a runs in docs-check step 21 (:172-175), after the submodule fetch in step 16 (:124-129) and before step 41 | Order proven; the step passes (08 H1-H2, G1d; 10a) |
| `scripts/ci_events.py` (`b6cc7689`) | `CARRIER_STEP_LISTS` entry (:1065); arms now expect 44 steps | Pins gate 36a's carrier and the new step | `--check` passes; it refuses the builder step removed, the builder call made non-failing, and the self-test step removed (08 H3-H6); `--selftest` 1150 arms PASS (10c) |
| `docs/testing/CI_WORKFLOWS.md` (`2823156c`) | :1059-1067 describe the step | Authoritative CI page | Each statement verified (receipt 12, 08 H6, 10a) |
| `docs/testing/RUNNING_TESTS.md` (`38a276cc`) | :24 adds the self-test beside the builder | Local-bar page | Command runs (10a, 08 G1d, G1g) |

## 3. Independent evidence on the combined tree

**Shipping bytes and wire layout (receipt 09).**
- I reused my published R222-2 `09_artifacts.py` verbatim (blob `b92cab00`). For each of the five configs, it hashes:
  - the YAML;
  - the normalized `load_config` result;
  - the overlay;
  - `aem_desc.bin`, `.json` and `.map`;
  - the AUDIO_UNIT words read back from the image;
  - the ten `build()` outputs (50 in all), including `aecp_aem_rom.svh`, `adp_shape_defaults.svh`, `lwsrp_*.svh` and `gptp_ucode.hex`.
- The manifests for the candidate, the source and dev all hash to `7d47bd673e5802c41d691fb4c833f54c840f5b1199ede883dadbb9623ddcfe60`. That equals my published base (`88e9276b`) and head (`1496558d`) manifests.
- The tracked tree is clean after the builds in every clone.
- Images:
  - arty_current: offset 144, count 3, `[48000, 96000, 192000]`;
  - the other four: offset 144, count 1, `[48000]`;
  - all five: current rate 48000.
- #513 therefore changes no loader result, no packed image and no generated output.

**Gate 36a on the combined tree (receipt 08; 0 graded mismatches).** Every scratch file was restored and blob-verified.
- A1-A4: gate 36a's loader, shipping and pp_shadow arms and gate 32 pass.
- B1: the candidate's gate 36a against the dev `52711029` builder fails only its loader arm, with "distinct ninth entry accepted" (B2 and B3 pass).
- C1-C12: all 11 non-equivalent builder mutants are caught (bound 9 or 7, `>=`, duplicate refusal removed or raw, sorted, forced default, membership removed, L10 not named, count refusal removed or truncating). The equivalent check-order mutant passes both arms.
- E1-E4: four real-YAML drifts are caught by the shipping arm on the combined tree. Three fail its declared-list check and one fails the loader's duplicate refusal.
- G2-G3: image-layout mutants are caught by the shipping arm:
  - the `sampling_rates_offset` field set to 148;
  - the rate words emitted reversed.

  The #513 self-test is blind to both (G2), so the two gates do not overlap.
- G4-G6: reverting either #513 avdecc file to its source blob, or widening the allowlist by one stale entry, keeps all gate 36a arms green and turns the #513 self-test red. #513's change has no semantic path into gate 36a's verdicts.
- F rows: loader against image, candidate against dev builder:
  - 8 distinct entries load, and the image refuses the non-base rates (S2);
  - 9 distinct entries, 9 or 8 copies, and `"48000"` or `48000.5` duplicates are refused at the candidate;
  - on dev, 9 distinct entries load and the image refuses them, while 9 copies, 8 copies and the two duplicates pack counts 9, 8 and 2;
  - reordered base rates reach the image in declared order;
  - an omitted list defaults to the current rate.

**Dependency trace (receipt 13).** Fresh interpreters recorded every repository file opened, with an empty bytecode cache.
- Loader arm: 21 files, including both #513 avdecc files.
- Shipping arm: 30 files, adding `gen_aemi_image.py` and PP `gen_desc_image.py`.
- pp_shadow arm: 16 files, no #513 file.
- Self-test: 7 files (six avdecc modules and `hdl/common/csr/milan_csr.sv`), no issue file.

**Downstream required-context gates (receipts 14, 15, 15b, 17).** All pass on the candidate.

Traced, reading issue and #513 paths together:
- `check_wire_accountability.py --self-test`: 77 checks, 0 findings. It reads endstation_builder.py and both #513 avdecc files.
- `check_entity_shape.py --self-test`: PASS. It reads all nine changed paths.
- `check_deploy_shape.py --self-test`: pristine OK, and 6 planted drifts rejected. It reads endstation_builder.py and both #513 avdecc files.
- `check_gptp_docs.py --with-submodule`: it reads ENDSTATION_BUILDER.md, CI_WORKFLOWS.md and RUNNING_TESTS.md.
- The TODO-ownership, hygiene, Python-idiom and test-evidence self-tests.

Traced, reading only a #513 path: `measure_fail_fast --selftest` (docs.yml).

Traced, reading neither:
- `check_rtl_source_lists.py --selftest`: 49/49.
- `check_soc_sources.py --selftest`: 25/25.
- `iob_pack_selftest.py`: 21/21.
- `check_nvm_record_space --self-test`.
- The naming, port-contract, SystemVerilog-, C++- and shell-idiom, and archive self-tests.

Untraced:
- `check_baremetal_only --check` (0 findings over 825 files) and `--selftest` (342 arms);
- `pp_srcs --check --selftest`;
- `check_rtl_source_lists.py` and `check_soc_sources.py`;
- `make -C gptp-processor docs`.

**Documentation gates in the three contexts the required jobs use (receipt 10).**
- Git clone with no submodule (docs-check's pre-submodule phase): all 20 gate commands exit 0.
  - em-dash at base `52711029`, the merge base a PR event derives: 1 added line, 0 findings, 57/57 arms.
  - The #513 self-test also passes there, which confirms its documented "needs no submodule".
- `git archive` extraction with no `.git` (docs-check-no-git):
  - 851 files match their candidate blobs and modes;
  - `docs_check` reports 0 findings (22/22 scrub, 4/4 routing arms; the parity arm is skipped by design);
  - `check_feature_status` reports 0 findings.
- Clone with submodules: 20 commands exit 0:
  - doc paths (824 cited paths), doc style;
  - `gen_toc` self-test (707/707), anchors, check; archive;
  - em-dash at `52711029`, `1496558d` and `88e9276b` (1, 11 and 12 added lines, 0 findings);
  - Python idiom, hygiene, TODO ownership, feature status;
  - `ci_events --check` and `--selftest` (1513 items, 1150 arms);
  - `git diff --check` from each of the three bases to the candidate.

**#513 statements the combined tree relies on (receipt 12).**
- The docstring counts match the builtin model: STREAM_INPUT 2, CLOCK_SOURCE 2, AUDIO_CLUSTER 16, AUDIO_MAP 1.
- The self-test is step 41, directly before the three shape gates (42-44).
- No tracked file still says "43 steps" or carries an `AUDIO_MAP[1]` allowlist spelling.
- Under Python 3.12.13 (stdlib only), the self-test passes with 20/0 arms (08 G1g).

## 4. Validation attribution (judged, not approved)

| Evidence | Object executed | Owner | Counted here as |
|---|---|---|---|
| Composed 41-command static/builder bank (archive `2102036d` `candidate2/`) | `72e16c61` / `93be2b57` against dev `52711029` | manager | Attributed candidate evidence, verified (receipts 06, 07) |
| Round-2 40 + 5 bar | `1496558d` / `e8d79755` against `88e9276b` | manager | Source head only |
| Trusted act replica (start receipt 5778014438) | Head tree of `1496558d`, validation base `88e9276b` | manager | Source head only; pending |
| Hosted docs, elaborate and rtl-fast (passed per 5778134318) | PR #512 merge ref at trigger time | manager | PR-head evidence; not inspected; not candidate |
| rtl-full 35732769071 | PR head, `draft=true` | manager | Exhaustive jobs SKIPPED; not a success |
| rtl-full recovery 35739098185 | Dispatched on the source branch. A dispatch validates the tip of the chosen ref (CI_WORKFLOWS.md:913-915), here `1496558d` / `e8d79755` | manager | Source tree; pending |
| #513 hosted runs | `a769d9db` / `31ddc6b5` (the dev tree) | manager | #513's own evidence for the dev side only |
| R222-2 | `1496558d` | R222 | Source-head coverage only |
| R222-3 focused controls | `72e16c61` / `93be2b57` | R222 | This round's candidate evidence |

Checks behind the first row:
- The archive manifest verifies 907/907 entries, none unlisted, with one declared omission (my own receipt 11, standards text).
- The spec and results match: 41 commands in order, at head `72e16c61` and base `52711029`, all exit 0.
- The final ledger differs only at command 40. The stale `git diff --check 52711029 1496558d` is replaced by `git diff --check 52711029 72e16c61`, and the entry names its receipt origin.
- I re-ran the corrected command, and the same check from `1496558d` and `88e9276b`: all exit 0.
- Integrity records at 16:24:23 and 16:39:14 carry the candidate head and tree and 851 files. Their submodule trees and file counts match my clone: PP `1b073c8b`/222, gPTP `25909c4d`/103, verilog-axis `54432ffb`/214.

The candidate head is not a PR hosted head: act validates the exact PR head tree, and hosted `pull_request` runs validate the merge ref (CI_WORKFLOWS.md:1281-1286). So no hosted or act run has executed tree `93be2b57`. Candidate evidence is the manager's local bar plus this round.

The public record is accurate after the correction:
- 5778289141 overstated command 40's endpoint.
- 5778469586 and 5778505279 corrected it publicly and kept the original receipts.
- The composition is explicit.

Native 5.052 results will not be pinned 5.050 evidence. Builder gate 11 is NOT RUN, and the field-campaign skips contribute no hardware evidence.

## 5. Findings

No new BLOCKER, MAJOR or MINOR at the candidate. No finding was moved to another Issue.

The carried optional SUGGESTIONs are unchanged at the candidate. `sim_main.cpp` (`98523e1b`), `aem_specs.py` (`7a6378d5`) and `ENDSTATION_BUILDER.md` (`b66600c8`) are identical to the source (receipt 18). Both stay routed to #495 and do not affect coverage.

[R222] SUGGESTION Tests - tb/verilator/pp_shadow/sim_main.cpp:829,850,879-880 - S1 (carried, unchanged): four hand spellings of the AUDIO_UNIT list sit outside the settled `AU_RATES_C` comparison
Requirement/evidence: the readiness decision settled only the values and the declared length (sim_main.cpp:827-828). `AU_CUR_RATE_C` (829), `AU_LEN_C` (850), the count literal (879) and the loop bound (880) are not compared. The trace shows the arm reads no #513 file (receipt 13).
Impact: none today; every spelling agrees with the YAML. A partial bench edit could pass the gate.
Required change: optional, outside #478; carried by #495.
Verification: R222-2 rows R1-R4 would turn into refusals.

[R222] SUGGESTION Docs - docs/ENDSTATION_BUILDER.md:963 - S2 (carried, unchanged): say that eight is a loader bound, because the packed-image path accepts only 48, 96 and 192 kHz
Requirement/evidence: `avdecc/aem_specs.py:219-221` refuses non-base rates. At the candidate, the legal eight load and the image raises `ValueError` (08 F1).
Impact: a reader could take eight rates as an end-to-end capability.
Required change: optional; carried by #495; #509 ownership stays separate.
Verification: read row 8 against aem_specs.py:219-221.

Observations, which are not findings against this PR:
- **Hosted-only gate.** `check_wire_accountability.py --self-test` (the required `wire-accountability` context) appears neither in RUNNING_TESTS.md nor in the manager's 41-command bank.
  - `check_entity_shape.py --self-test` and `check_deploy_shape.py --self-test` (docs-check steps 43-44) are also absent from the bank, although RUNNING_TESTS.md:27 lists the deploy gate.
  - All three read the combined tree's changed paths and pass here (receipts 14, 15).
  - This is a pre-existing question about how the bar is composed, outside #478. It is recorded for the manager.
- **Carried loader observations.** From R222-2 (loader blob unchanged): a scalar or null `audio_unit_rates_hz` raises `TypeError`, and `int()` truncates floats. Both are outside the frozen scope.

## 6. Lens results at the candidate

Each line is this round's own application at `72e16c61`. None rests on R222-2.

[R222] PASS Conformance - sw/builder/endstation_builder.py:1197-1200,3754-3810 (blob 95ffb669); sw/builder/test_builder.py:23524-23636; avdecc/aem_descriptors.py:240-265; PP@424c688 07_memory_maps.md:54,92 and gen_ucode.py:1330-1331,1384; receipts 08 A/B/C/F, 09, 10, 11, 14 - AC1-AC3 and each readiness item hold on the combined tree. The bound equals L10 and `SSR_WALK_MAX` 8. The image carries offset 144 with the count at octet 142, matching Table 7-5 (7.2.3), read without copying standards text. REQ-VER-03: all five configs build with manifest-bound images, byte-identical to source and dev. REQ-VER-04: the documentation and feature-status gates report zero findings in the Git, no-Git and no-submodule contexts, and the traceability, source-list and bare-metal gates pass (receipts 10, 14).

[R222] PASS RTL - diffs 1496558d..72e16c61 and 52711029..72e16c61 (no path under hdl/, tb/, syn/, sw/litex/, constraints/ or a submodule); gitlinks at four commits; the 50 build outputs in receipt 09 (aecp_aem_rom.svh, adp_shape_defaults.svh, lwsrp_csr_defaults.svh, lwsrp_table.svh, gptp_ucode.hex); receipts 01, 08 G2-G3, 11 - no RTL, bench, synthesis or pin change on either side. All generated RTL-facing outputs are byte-identical across source, dev and candidate, and the tracked generated headers are unchanged. The processor walk (entries 0-7 at offset 144) is unchanged at the pin, and wire-layout mutants are caught. No clock, reset, CDC, FSM, width or timing effect.

[R222] PASS Robustness - sw/builder/endstation_builder.py:3786-3810; avdecc/aem_specs.py:219-221; receipts 08 rows A1, C8, E1-E4, F1-F11 and G4-G6, 09 - on the combined tree, with the F rows built through the #513 image path:
- 8 distinct entries are accepted;
- 9 distinct entries, and 9 or 8 copies, are refused by count and by duplicate;
- duplicates after `int()` are refused;
- empty and missing-current lists are refused by membership;
- declared order reaches the image, and an omitted list defaults to the current rate;
- the order of the checks decides no case.

Builds are deterministic across the three trees. #513 adds no input path. The loader is a pure build-time function, so reset, backpressure and timeout do not apply.

[R222] PASS Tests - sw/builder/test_builder.py:249-254,23524-23636; .github/workflows/docs.yml:124-129,172-175,390; scripts/ci_events.py:1065,3326; receipts 08 (B1, C, E, G, H), 13, 14, 15, 17; archive 2102036d candidate2/manager-builder 41.log (attributed) - gate 36a still fails for its defect against the dev builder. All 11 non-equivalent builder mutants, 4 YAML drifts and 2 image-layout mutants are caught on the combined tree, and the equivalent mutant passes. The dependency traces show exactly which arms import the #513 files, and the reverts show those files do not influence the verdicts. Gate 36a's CI carrier stays pinned and ordered: removing it, or making it non-failing, is refused. The existing downstream gates that read both halves pass. The manager's full builder at the candidate reports `ALL GATES PASS EXCEPT 1 NOT RUN`, with every gate 36a line present.

[R222] PASS Docs - docs/ENDSTATION_BUILDER.md:963 (blob b66600c8); docs/testing/CI_WORKFLOWS.md:1059-1067; docs/testing/RUNNING_TESTS.md:24; avdecc/gen_aem_store.py:5-11,67-68; receipts 10a-c, 12, 16, 17 - row 8 and the gate 36a docstring are unchanged and still match the implementation. The #513 statements are true of the combined tree:
- the step sits just before the three shape gates;
- it needs no submodule;
- it is pinned by `CARRIER_STEP_LISTS`;
- the model counts match.

Documentation gates are green with zero findings in all three required contexts. There are no stale step counts or allowlist spellings. The public record (5778076390, 5778289141, 5778469586, 5778505279 and the archive) lets a cold reviewer reconstruct the candidate and its evidence.

## 7. Remaining dependency risk (reported, not moved away)

1. **Python 3.12 on the combined tree.** The hosted docs job uses the runner's system Python.
   - This round ran gate 36a and the builder under 3.14.7 only; there is no PyYAML for the local 3.12, and no installs were allowed. Only the stdlib-only self-test ran under 3.12.13.
   - Both halves ran separately under hosted CI, and the only #513 Python on gate 36a's import path is 3.12-valid (G1g). The residual risk is low. It is retired by hosted merge-context or post-merge push evidence.
2. **Three docs-check steps (7 command lines) not executed on the candidate:**
   - the HDL reference build (pinned `pyslang` wheel not installed);
   - `gen_wavedrom` (module not installed);
   - `act_ci.py --selftest` (the candidate copy must not run on the host).

   All three scripts are byte-identical across the three objects and name no issue or #513 path. The act self-test's four workflow inputs equal dev's (receipt 16).
3. **Candidate native groups pending.** The five groups have not run: parent sweep, Yosys, PP, gPTP and behave. The RTL-facing outputs are byte-identical, but those groups remain mandatory.
4. **Coverage is tied to this candidate.** It is banked against tree `93be2b57`, with parents `52711029` and `1496558d`. A merge result with another tree, or a dev move, needs a new candidate and a re-examination of the changed scope.

## 8. Ledger (published by reviewer R222)

| Lens | Covering round | Exact head | State | Scope basis |
|---|---|---|---|---|
| Conformance | R222-3 | 72e16c6172db723734317b105cff6c6e9168571a | covered clean | Applied fresh at the candidate: AC1-AC3 and readiness items re-run on the combined tree; L10 and SSR constants at the unchanged pin; image offset and count read back; REQ-VER-03/04 gates green |
| RTL | R222-3 | 72e16c6172db723734317b105cff6c6e9168571a | covered clean | Applied fresh: no RTL, bench, synthesis or gitlink change on either side; 50 generated outputs byte-identical to source and dev; layout mutants caught |
| Robustness | R222-3 | 72e16c6172db723734317b105cff6c6e9168571a | covered clean | Applied fresh: A1, C8, E and F rows on the combined tree, with the F rows built through the #513 image path |
| Tests | R222-3 | 72e16c6172db723734317b105cff6c6e9168571a | covered clean | Applied fresh: B1, C, E, G and H rows, dependency traces, and the downstream required-context gates on the combined tree |
| Docs | R222-3 | 72e16c6172db723734317b105cff6c6e9168571a | covered clean | Applied fresh: three-context documentation gates; #513 statements verified; row 8 unchanged |

- No ancestor's coverage is relied on. R222-2 at `1496558d` stays source-head coverage.
- The two carried SUGGESTIONs are optional and do not affect coverage.

## 9. Outstanding manager duties (not approved by this round)

1. The candidate's five native groups.
2. The trusted act result for `1496558d`, which started at dev `88e9276b`.
3. Tying the rtl-full recovery 35739098185 and all seven required contexts to the PR head.
4. R221's corrected review.
5. The merge bar itself:
   - two independent positives;
   - no review round in flight;
   - maintainer authorization;
   - a merge result equal to tree `93be2b57`.
6. After merge:
   - `check_merge_containment.py` and `check_merge_review_integrity.py`;
   - closure through `Closes #478`;
   - the Project item moved to Done.
7. Gate 11 NOT RUN and the field-campaign skips stay labelled as non-evidence.

## 10. Limits

- By instruction, this round did not run:
  - full native RTL, Yosys, processor, behave or builder banks;
  - act, Docker, or the candidate's `act_ci.py`;
  - hosted-job polling;
  - installs, privileged commands or hardware;
  - edits, commits, pushes, public writes or metadata changes.
- Focused controls ran only in scratch clones under `/tmp/r222-478-r3-scratch`, built from the review clone's object stores (`--no-hardlinks`, separate filesystem). Parallelism never exceeded 3 jobs.
- Tools: Python 3.14.7, PyYAML 6.0.3, Git 2.55.0; Python 3.12.13 (stdlib only); tclsh.
- Network reads:
  - `gh api` reads of issue #478, PR #512 and PR #513;
  - `git ls-remote` of four refs;
  - a fetch of the public evidence commits `2102036d`, `1961ad05` and `2cfba1ab` into a scratch bare repository.
- Hosted, act and native states are as the manager published them at the times cited. This round did not observe them.
- Review clone integrity: start and final snapshots are identical (receipts `integrity-start.txt`, `integrity-final.txt`, `integrity-compare.txt`):
  - HEAD `72e16c61`, tree `93be2b57`;
  - index equal to the HEAD tree;
  - 855 entries with blob, mode and kind verified;
  - the three pins match; external uninitialized.

## 11. Receipts and reproduction

| Receipt (receipts/) | Script (reproduction/) | Content |
|---|---|---|
| integrity-start.txt, integrity-final.txt, integrity-compare.txt | 00_integrity.sh | review-clone identity, index, blobs and modes, pins |
| 01-history-identity.txt | 01_history_identity.sh | merge-tree, patch identity, disjointness, blobs, gitlinks |
| 02-scratch-setup.txt | 02_setup_scratch.sh | scratch clones and pins |
| 03-live-refs.txt | (git ls-remote) | live dev, validation, source and PR refs |
| 06-evidence-manifest.txt | 06_evidence_manifest.py | archive `2102036d` manifest |
| 07-manager-evidence-facts.txt | 07_manager_evidence_facts.py | candidate2 bank, composition and integrity |
| 08-candidate-probes.txt | 08_candidate_probes.py | sections A, B, C, E, F, G and H |
| 09-artifacts-{cand,src,dev}.json/.log, 09-artifact-compare.txt | 09_artifacts.py (R222-2 script, verbatim) | shipping-byte manifests |
| 10-setup.txt, 10a-docs-nosub.txt, 10b-docs-nogit.txt, 10c-static-withsub.txt | 10_focused_static_gates.sh | documentation gates in three contexts |
| 11-pp-authority-and-layout.txt | 11_pp_authority_and_layout.sh | PP L10 and SSR constants; standards hashes and locations only |
| 12-pr513-artifact-facts.txt | 12_pr513_artifact_facts.py | #513 statements checked |
| 13-dependency-traces.txt | 13_dependency_traces.py | files opened per gate 36a arm and by the self-test |
| 14-extra-required-gates.txt | 14_extra_required_gates.sh | wire-accountability, bare-metal and source lists |
| 15-shape-gates-traced.txt, 15b-deploy-shape-pristine.txt | 15_shape_gates_traced.sh | deploy, entity, source-list and iob gates |
| 16-docs-workflow-attribution.txt | 16_docs_workflow_attribution.py | per-step evidence map of the docs workflow |
| 17-remaining-docs-gates.txt | 17_remaining_docs_gates.sh | remaining runnable docs-check lines |
| 18-carried-suggestions.txt | (sed) | S1/S2 lines at the candidate |
| 19-redaction.txt | 19_redact_other_reviewers.py | other reviewers' bodies replaced by SHA-256 |
| 20-line-references.txt | (grep) | candidate line references used above |
| issue478*.json, pr512-comments-all.json, pr513*.json | (gh, redacted) | public records as fetched |
| MANIFEST.sha256 | (sha256sum) | hashes of this report, receipts/ and reproduction/ |

R222-3 FINISHED
