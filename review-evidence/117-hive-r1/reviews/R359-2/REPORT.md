[R359] POSITIVE - exact head ecd36018a29f605efe790d33dd50382aec9c1201

# R359-2: external delta review of PR #598 (issue #117, acceptance box 4, Hive row)

- **Head:** `ecd36018a29f605efe790d33dd50382aec9c1201`, tree `505fb4868a1b7a8808ca813e4b668582fe72cf11`.
- **Delta under review:** `bcba79a5..ecd36018`, one commit by the round-2 executor. It touches one file, `docs/findings/117_GPTP_SILICON_EVIDENCE.md`, +53/-15. The base-to-head diff `2a2a7bb6..ecd36018` touches the same single file.
- **Scope authority:**
  - the issue #117 body and acceptance;
  - the owner decisions of 2026-09-23 (issue comments 5789767491 and 5795898094) and 2026-09-27 (5858063707);
  - the round-2 assignment (5858871629), which extends the edit scope to the header, the Contents lines, `:53/:462/:467` and B4;
  - the round-2 TAKEN, STOP and coordinator resolution (5858883277, 5858985706, 5858999219).
- **Evidence read:**
  - `review-evidence/117-hive-r1` on branch `117-hive-review-evidence`, at the page's pin `557087b3` and at `89aa9f94`;
  - the round-2 packet `author-r2/` at the branch head `34c3b1d6`.
- **Order of reading:** I wrote my independent draft (`receipts/independent_draft_before_prior_reviews.txt`) before I read either round-1 review report.

## Verdict summary

All four round-2 items are met at this head, and both round-1 MINOR findings (R359-1 F1 = R358-1 F1, and R359-1 F2) are resolved.

- Every B4-cited hash resolves at the pinned public locator. Seven match the published bytes. The three entity dumps are listed as redacted, and `MANIFEST.json` maps each one to its published copy.
- The Milan FAIL is presented as the dated 2026-09-23 `ede8d48e` record, superseded by the `9e9954e9` PASS. The `#534` link is stated as an observation. Box 4's remaining rows are listed correctly.
- The build sentence equals both the published build flags and the library's upstream default options. It also conditions "no warnings" on that option set.
- The packet addendum is consistent with the recorded include order.

All eight documentation and scope gates return rc 0 at this head.

Two SUGGESTIONs remain. They are optional and do not affect lens coverage.

## Findings

### S1: SUGGESTION, Docs: `docs/findings/117_GPTP_SILICON_EVIDENCE.md:469` and `:543-544` say "#534 closed #529"

**Evidence** (`receipts/pr534_issue529.txt`):
- PR #534 has no closing reference. Its body says "Relates to #529 (it stays open until the manager's silicon re-flash and la_avdecc Milan confirmation)".
- #529 was closed by hand on 2026-09-24T03:38Z. The closing comment cites #534's merge `50e78097`, and a silicon re-run on that image that classified the DUT as Milan.

**Why this is only a SUGGESTION:** the facts the page relies on are true.
- The fix merged as `50e78097`, which is an ancestor of `9e9954e9` and not of `ede8d48e`.
- #529 is closed on the basis of that fix.
- The published dumps show Stream Input 1 serving ten counters, the register map's `0x00000F3F` set.

Only the closure mechanism is loosely worded. The wording comes from the round-2 assignment.

**Optional outcome:** "#534 (merge `50e78097`) fixed the gap; #529 was closed on 2026-09-24 after a silicon Milan PASS on that image". This also gives the page a second, earlier datum for the observational link.

### S2: SUGGESTION, Docs: `review-evidence/117-hive-r1/author-r2/PACKET-ADDENDUM.md` (at `34c3b1d6`) does not name every file omitted from the include directory

**Evidence** (`receipts/upstream_include_tree.txt`):
- Upstream `6d61a92e` has 52 `la/avdecc` `.h/.hpp` headers. The addendum's 48 equals exactly the library and controller header-install lists.
- The addendum names two `la/avdecc` omissions: the umbrella `avdecc.h` and one virtual-entity header.
- The counts also imply three omissions that are not named:
  - `la/avdecc/internals/exports.h`
  - `la/avdecc/internals/typedefs.h`
  - `la/networkInterfaceHelper/internals/exports.h`
- These are C-binding and export headers. The C++ probe does not include them.

**Why this is only a SUGGESTION:**
- The provenance claims hold against what I could check:
  - The include order matches `author/build-provenance.txt`: library `include/`, then `externals/3rdparty/json/include`, then the probe directory.
  - The library's `include/` has no `la/networkInterfaceHelper`, so the probe directory adds only that header.
  - The submodule pins nih `d777db8b` and json `9cca280a` equal the upstream gitlinks at `6d61a92e`.
- The byte-identity claim and the inventory hash `7711cedc...` cannot be recomputed without the controller host (see Limits).

**Optional outcome:** list the omitted files exhaustively, or publish the per-file `sha256sum` list whose hash the addendum gives.

## Assigned items

1. **B4 locator and hashes: met.**
   - `:652-667` names branch `117-hive-review-evidence` at `557087b34479c9ba0f1fc1722b6e577a0ecc3998`, path `review-evidence/117-hive-r1`. "publication is pending" is gone.
   - `check_b4_hashes.py` result (`receipts/b4_hashes_557087b.txt`):
     - 7 of the 10 table hashes equal the published bytes.
     - 3 (`run-1/2/3.entity.json`) are listed as redacted. For each, `MANIFEST.json` `original_sha256` equals the cited hash and `published_sha256` equals the file's `sha256sum`.
     - The published dumps carry `<device-serial>`.
   - The probe source hash `ac552f67...` also equals the published `tools/enum_probe.cpp`.
   - Mutation controls (`receipts/stale_claims_and_mutations.txt`): corrupting one hash, or dropping one redacted listing, makes the checker return rc 1.
   - No line says the public dumps keep their recorded bytes. `grep` for "recorded bytes", "retain their", "keep their", "publication is pending" and "two blockers" finds nothing.
   - `author/` and its `MANIFEST.json` entries are identical at `89aa9f94`, `557087b3` and the branch head, and the pin is an ancestor of the branch head (`receipts/other_b4_hashes_and_pin.txt`).
   - The Raw artifacts section (`:688-689`) now points to the B4 locator. So the box-5 row's "[Raw artifacts] gives the locator" holds for the B4 runs too.
2. **Superseded dated FAIL: met.**
   - `:464` dates the FAIL to 2026-09-23 on `ede8d48e` and marks it superseded. `:469` dates the downgrade explanation the same way.
   - `:540-548` states the supersession and the ancestry, which I verified (`receipts/ancestry_and_counters.txt`). It calls the causal link "likely ... observational".
   - Box 4's Milan row (`:55`) stands on the `9e9954e9` PASS. I confirmed the PASS in all three published run logs (`flags=IEEE17221|Milan`, complaints 0) and in `enumeration-summary.txt`.
   - `:550-552` lists box 4's remaining non-PASS rows as behave hardware tier, latency (#64/#213), and audio continuity deferred to 2026-12-31. That equals the table at `:53-58`.
   - The header (`:6-9`), Contents `:30` and `:33`, and `:469` no longer contradict this (`receipts/page_consistency_grep.txt`).
3. **Build define and option set: met** (`receipts/build_options.txt`, `receipts/runtime_option_selfreport.txt`).
   - The nine probe defines at `:635-639` equal the `-D` set in `BUILD_FLAGS`.
   - The eleven enabled options and the one disabled option at `:639-646` equal the upstream behaviour-option defaults at `6d61a92e`.
   - Every verdict-affecting library option is also self-reported by the library at runtime. The option block is identical in all three run logs. That covers the private-only defines `IGNORE_INVALID_CONTROL_DATA_LENGTH`, `IGNORE_INVALID_NON_SUCCESS_AEM_RESPONSES` and `ALLOW_GET_AUDIO_MAP_UNSOL`.
   - `:647-648` conditions "no warnings" on that default set, including `IGNORE_INVALID_CONTROL_DATA_LENGTH`.
4. **Packet addendum: accurate as provenance, with S2.**
   - The addendum is consistent with the round-1 `build-provenance.txt` include order.
   - Its conclusion is correct: the probe directory contributes only the networkInterfaceHelper header, because its `la/avdecc` copies sit behind the library's own `include/`.

**No new claims beyond these:**
- The delta's hunks are the header, Contents `:30/:33`, `:55`, `:464`, `:469`, B4 and a two-line Raw artifacts pointer.
- Every NOT RUN table row is unchanged from `bcba79a5`. The only NOT RUN line that changed is the B4 prose sentence the assignment asked for (`receipts/scope_delta.txt`).

## Prior public findings on PR #598

| Finding | Status at `ecd36018` | Evidence |
|---|---|---|
| R359-1 F1 = R358-1 F1 (MINOR, Docs/Conformance): no B4 locator, "pending", redacted hashes, "recorded bytes" | RESOLVED | item 1 above |
| R359-1 F2 (MINOR, Docs/Conformance): Milan PASS not reconciled with the FAIL; header, Contents `:28/:31`, `:53/:462/:467` | RESOLVED | item 2 above |
| R358-1 S1 (image difference as observation) | Taken | `:543-547` |
| R358-1 S2 (Contents "two blockers that remain") | Taken | `:33` |
| R358-1 S3 = R359-1 S2 (full define and option set; "no warnings" conditioning) | Taken | item 3 above |
| R359-1 S1 (`summarize.py` gating) | Not taken, by coordinator decision; still optional | no lens effect |
| R359-1 S3 (include directory undescribed) | Taken in `author-r2/PACKET-ADDENDUM.md` | item 4; residual S2 |

## Clean lenses

```text
[R359] PASS Conformance - docs/findings/117_GPTP_SILICON_EVIDENCE.md:6-9,30,33,53-58,464,469,540-552,634-667 at ecd36018 against issue #117 boxes 4/5, comments 5858063707 and 5858871629 items 1-4, the pinned packet 557087b3 (receipts/b4_hashes_557087b.txt), git ancestry 50e78097 -> 9e9954e9 (receipts/ancestry_and_counters.txt) and the three run logs - every round-2 item is met, box 4 lists its remaining non-PASS rows exactly, and no other NOT RUN row changed (receipts/scope_delta.txt)
[R359] PASS RTL - git diff --name-only 2a2a7bb6..ecd36018 (one Markdown file); gitlinks external/gptp-processor/protocol-processor/third_party/verilog-axis unchanged (receipts/clone_state_after.txt); 9e9954e9..2a2a7bb6 touches four docs/evidence files (receipts/ancestry_and_counters.txt) - no HDL, builder or generated-RTL artifact is in scope; the measured image's source lineage is unchanged
[R359] PASS Robustness - receipts/b4_hashes_557087b.txt with mutation controls (receipts/stale_claims_and_mutations.txt); pin stability across 89aa9f94/557087b3/34c3b1d6 (receipts/other_b4_hashes_and_pin.txt); redacted-versus-original handling at :658-667; conditioning of "no warnings" at :647-648 - the page's evidence path survives redaction, a moving branch head and a non-default library build without overstating
[R359] PASS Tests - receipts/docs_gates.txt (docs_check, check_doc_style, gen_toc --check, check_em_dash --base 2a2a7bb6, check_doc_paths, ci_scope --selftest, check_baremetal_only --check, git diff --check: all rc 0); receipts/gate_mutation_probes.txt (gen_toc --check fails on a broken Contents anchor; check_em_dash --selftest 339 arms PASS; 0 em dashes in added lines); check_b4_hashes.py kills both planted faults
[R359] PASS Docs - the whole page at ecd36018 for present-tense Milan statements (receipts/page_consistency_grep.txt), the B4 and Raw artifacts locators, and author-r2/PACKET-ADDENDUM.md against upstream 6d61a92e (receipts/upstream_include_tree.txt) - no stale or contradictory statement remains; S1 and S2 are optional SUGGESTIONs
```

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #117 boxes 4 and 5; owner decisions; round-2 assignment items 1-4; page `:6-9`, `:30`, `:33`, `:53-58`, `:464`, `:469`, `:540-552`, `:634-667`; pinned packet `557087b3`; run logs 1-3; `50e78097` ancestry | R359-2 | `ecd36018a29f605efe790d33dd50382aec9c1201` |
| RTL | CLEAN | Diff name list `2a2a7bb6..ecd36018` (one Markdown file); four gitlinks unchanged; `9e9954e9..2a2a7bb6` is docs/evidence only | R359-2 | `ecd36018a29f605efe790d33dd50382aec9c1201` |
| Robustness | CLEAN | B4 hash resolution under redaction, with mutation controls; pin stability across three evidence commits; option-set conditioning | R359-2 | `ecd36018a29f605efe790d33dd50382aec9c1201` |
| Tests | CLEAN | Eight documentation and scope gates at the head, rc 0; gate mutation probes; em-dash self-test; checker mutation controls | R359-2 | `ecd36018a29f605efe790d33dd50382aec9c1201` |
| Docs | CLEAN (S1, S2 are SUGGESTIONs) | Whole findings page at the head; Raw artifacts pointer; `author-r2/PACKET-ADDENDUM.md` against the upstream tree and install lists | R359-2 | `ecd36018a29f605efe790d33dd50382aec9c1201` |

The R359-1 ledger's RTL, Robustness and Tests rows at `bcba79a5` are superseded by this round's rows at `ecd36018`, which re-cover every lens at the merge-candidate head.

## Limits

- **No bench access and no hardware re-measurement.** I judged every bench result from the published raw artifacts.
- **No controller-host access.** The addendum's byte-identity claim, its 49-file count and its inventory hash `7711cedc...` are coordinator statements. I checked them only for consistency with the upstream tree, the install lists and the recorded include order.
- **The library's build configuration** is evidenced by the library's own runtime option self-report in the run logs and by the probe's `-D` set. There is no configure cache. `ENABLE_AVDECC_USE_FMTLIB` is not self-reported, and it has no bearing on the compatibility flags.
- **Original bytes of the three redacted dumps** are not public. They are verified through `MANIFEST.json` only.
- **Hosted checks at the head** (`receipts/hosted_exact_head.txt`, read-only):
  - Succeeded: `rtl-fast`, `changes`, `elaborate`, `bdd-conformance`, `wire-accountability`, `docs-check-no-git`, `full-ci-gate`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0-3, and Verilator shards 0 and 3.
  - Still in progress when read: `docs-check` and Verilator shards 1, 2 and 4.
  - Skipped: physical gPTP. A skipped context is not execution evidence.
- **The scoped Verilator binary was not used**, because the delta has no RTL or test-bench change. Its identity was therefore not checked.
- **Physical calibration is NOT RUN**, and field skips are not hardware proof. Acceptance box 4 keeps its NOT RUN rows, and #117 stays open.
- **Local environment notes:**
  - The documentation gates ran with the pinned Markdown lock installed in a disposable environment under `scratch/`.
  - `check_baremetal_only.py` ran under the system interpreter, because that environment lacked `pyyaml`. The first attempt's rc 2 was environmental and is recorded.

## Pending manager duties

- Hosted and local-replica acceptance at the exact head, including the in-progress contexts above.
- The merge-turn candidate build and validation against live dev `6d5ebd7357c1e468e446f18a61527c5be6118a04`, from source base `2a2a7bb655e528edc3087c88033cd3a47546feb4`.
- Post-merge containment.
- Publishing this packet.
- Merge authorization rests with the maintainer.
- Optional: decide on S1 and S2.

## Receipts and restoration

- **Scripts:**
  - `check_b4_hashes.py <page> <extracted review-evidence/117-hive-r1>`
  - `check_build_options.py <page> <build-provenance.txt> <upstream CMakeLists.txt> <upstream src/CMakeLists.txt>`
  - `receipts/upstream_sources.txt` gives the upstream files by revision and SHA-256. They are not republished.
- **Receipts** are under `receipts/`. `MANIFEST.sha256` lists every published file.
- **Clone state after the probes** (`receipts/clone_state_after.txt`):
  - HEAD `ecd36018`; index tree `505fb486` equals the HEAD tree.
  - The worktree and index are clean, with 0 porcelain entries including ignored files. The two ignored `scripts/__pycache__` files the gate runs wrote were removed.
  - All 928 tracked non-gitlink entries re-hash to their index blob with matching mode.
  - The four gitlinks are unchanged: `external` `efeb541a`, `gptp-processor` `5dce647a`, `protocol-processor` `870ff88a`, `third_party/verilog-axis` `48ff7a7e`.
- **Disposable trees** stayed under `scratch/`. That covers the evidence extractions, the upstream copies, the Markdown environment and the mutation copies.

R359-2 FINISHED
