[R837] POSITIVE - exact head 7398ec0aeea468d92ff642a03a06e291a0cd58d1

# R837-5: internal independent review of PR #902 (issue #894), round 10 delta

- **Head:** `7398ec0aeea468d92ff642a03a06e291a0cd58d1`, tree `2787f9fae40e581584d454e6cb476e68d1850487`. PR #902 is `894-tiers` into `dev-soft-core`, not a draft, and its head matches.
- **Delta reviewed:** `5b264bf2..7398ec0a`, three one-line commits (`55b8e621`, `947bd389`, `7398ec0a`) touching six files.
- **Authority:** the round-10 assignment, #894 issuecomment-6873298790. Acceptance is issue #894's frozen criteria. The author's claims are in REVIEW READY, #894 issuecomment-6874537343.
- **Evidence:** the author packet `review-evidence/894-r1/author-r10` at archive `56e8f05b`.
- **Verdict:** every lens was applied and every lens is clean. No BLOCKER, MAJOR or MINOR finding is open. There is one RESIDUE item and there are two suggestions.
- **Order of work:** my own pass over the delta came first, then the prior findings. Those were R837-4 (PR #902 issuecomment-6873294087) and R838-4 (issuecomment-6873195590). I read them after my verdict on the delta was formed, and they are resolved below.

## What I checked, and how

All probes ran on this clean detached clone or in disposable scratch. Raw receipts are under `receipts/` and the probe scripts under `scripts/`.

1. **The new assertion** (`sw/firmware/ctrl/aecp/aecp_maps.c:157-162,190-191`).
   - `place()` (`:207-214`) returns `first * MAP_CHANNELS + channel` only when `first < MAP_FIRSTS` and `channel < MAP_CHANNELS`. Its largest index is therefore `MAP_DOMAIN - 1`, and its sentinel is `MAP_SLOTS`.
   - The new `_Static_assert` compares the declared length of `struct edit`'s `slot` array with `MAP_DOMAIN`. That is exactly the range `place()` forms. It is a valid integer constant expression, because the operand of `sizeof` is not evaluated.
   - The sentinel stays outside the domain, because `MAP_SLOTS` is at least `MAP_DOMAIN`. The array is declared `[MAP_SLOTS]`, and the `memset` (`:370`) still clears it to the end of the struct.
   - Round 9's per-direction assertion is removed. `MAP_FLOOR` and `MAP_DOMAIN` are separate macros, as the assignment asks.
2. **The compile-time control** (`aecp_map_mutants.py:17-19,58-64`; `aecp_mutants.py:885-889,898,909-914,948`).
   - `receipts/row-head.txt`: at the head, `--shard 257 274` runs only `DEFECTS[257]`, which is `map-table-each-direction-alone`. The row prints `[ok]`, and its log is `aecp_maps.c does not compile: ... static assertion failed: "the table holds every position place() forms"`.
   - `receipts/row-r9-assertion.txt`: I temporarily put round 9's assertion back in this clone, keeping the same words, then restored it. The same row now prints `[ESCAPED]` and exits 1, and its log shows `[  PASSED  ] 0 tests.` So the control can fail for the defect it names.
   - Other rows are graded as before. `refused()` is false for any row that is not a build row, so their compile failures remain escapes. `controls()` holds the reader to three negative cases.
   - At the head, all 274 planting sites match exactly once and `controls()` passes. I checked this by importing the table.
   - Every row except the new one plants into code whose objects are unchanged (point 4), so their grading cannot move. I did not rerun the full 274-row campaign for that reason. The author's 274/274 receipt stands.
3. **Geometries and planted tables** (`receipts/probe-maps-identity.txt`, from my own script).
   - I covered all five checked-in configurations plus the 16x4 and 16x32 key geometries.
   - The campaign's plant is refused exactly where each direction's own product is below the domain: `arty_8ch`, `arty_current` and `ax7101_1x1_tdm8`.
   - The floor alone is refused only at 16x32, which has 544 positions.
   - The plant with round 9's assertion compiles at all seven.
   - These results match the author's `probe-table-assert.txt` row for row.
   - At 1x1/1if the domain is 8 x 8 = 64. The direction products are 16 and 8, and an input key's index reaches 7 x 8 + 0 = 56. That is the "16 slots ... reaches 56" the documents state.
4. **No code change, so the skip is supported.**
   - My probe: `aecp_maps.c` at `5b264bf2` and at the head, compiled with the arms' C flags and no debug info. The host objects are byte-identical at all seven geometries. The preprocessed text is equal once assertions, whitespace and the parentheses `MAP_DOMAIN` adds are set aside.
   - `aecp_arms.py` is the only other changed file that an image builder imports, transitively through `ctrl_srp_image.py` and `ctrl_plat_image.py`. Its change is three comment lines, and `KEY_GEOMETRIES` is unchanged.
   - The author's cross-build: 332 of 332 files are identical. I confirmed that the two sha256 lists are identical. A rebuild of the base reproduces them, and a planted `MAP_FLOOR` of 264 changes 24 files, so the hashing can detect a change.
   - So round 9's measured rows stand: txL 48.09/49, R4L 188.39/238, last queued notice 126.46/130, load 0.513. Skipping the four-shard sweep and the harness legs is consistent with the assignment's rule.
5. **R838-4-F1, the current table** (`receipts/flip-1x1-1if.txt`, `flip-8x8-2if.txt`, `table-vs-flip.txt`).
   - I ran `flip_grade.py --check` at both points myself. It gives RESULT PASS at 1x1/1if, and the 8x8/2if FAIL is the reported point.
   - `SPLIT_CONTROL_MEMORY.md:2346-2347` and the summary R4 at `:2481` equal it cell for cell.
     - 1x1/1if: 12.85, 72.91, 68.80, 14.51, 126.46.
     - 8x8/2if: 42.09, 189.14, 177.28, 20.24, 626.87.
     - Summary R4: 12.85.
   - Superseded values (12.82 and the rest) now appear only in the progression table (`:2362-2366`) and in sentences that name their state.
6. **R838-4-F2, the core filter** (`receipts/core-wide-filter.txt`, `core-r9-filter.txt`).
   - `--core --filter 'Core.*Map*:Core.Every*'` passes 13 tests, including the definition test `Core.MapEditsAreTheirDefinitionRowForRow`.
   - Round 9's `'Core.Map*:Core.Every*'` passes 8.
   - The PR body (`How to validate`, its line 167) now carries the 13-test command.
7. **Gates I ran at the head:**
   - `fw_coverage.py --check --jobs 16`: PASS over 39 files, including its embedded suites; `aecp_maps.c` 267/267 lines and 336/336 branches.
   - `flip_grade.py --selftest`: 555 of 555.
   - `load_grade.py --check`: 0.513 and 0.509, PASS.
   - `docs_check.py`: 0 findings.
   - `check_py_idiom.py`: exit 0.
   - The added lines contain no em or en dash. The pinned Markdown renderer for `check_em_dash.py` is not installed here, so I scanned the bytes instead.
   - `git diff --check` is clean.
8. **The author packet** (`receipts/packet-index-verify.txt`, `root-manifest-author-r10.txt`).
   - All 66 published files match the archive root `MANIFEST.json`.
   - 64 of 65 `INDEX.md` rows match the bytes. The exception is `scripts/index.py`: its row carries the original's hash, and the root manifest declares that file path-redacted. See S1.
   - The archive commit is unsigned, so content integrity was verified but not authorship.
   - The packet was committed at 08:30:16Z, after REVIEW READY at 08:28:14Z and before this review started.
   - The hosted-step table tallies 139 run, 226 not run with a reason and 0 bad. The sweep's not-run reasons cite the identity rule.
9. **The comment rule over the delta:** no lane label, round, reviewer ID or comment ID appears in any added source comment. `aecp_maps.c` cites #909 and #894. The new `aecp_arms.py` comment is true: under the former hash (stream plus nine times channel), 16x4 keys such as stream 9 channel 0 and stream 0 channel 1 shared slot 9. #909 is open and concerns data-cache placement, which matches "a layout choice".

## Prior findings at this head

| Finding | Status at `7398ec0a` | Evidence |
|---|---|---|
| R837-4-1 MINOR (Conformance, RTL, Tests, Docs): the assertion was vacuous and did not bound `place()`'s range | **Resolved at cause.** All four required outcomes are met. The declared array is asserted against `MAP_FIRSTS x MAP_CHANNELS`. A compile-time control plants an undersized table where it overflows, at 1x1/1if, and the build refuses it with the assertion's words. Both documents say what the assertion holds, and separately that the floor is a layout choice (#909): `SPLIT_CONTROL_MEMORY.md:2461-2462`, `aecp/README.md:213-221,240-241`. There is no image or behaviour change. | Points 1-4; `row-head.txt`, `row-r9-assertion.txt`, `probe-maps-identity.txt` |
| R837-4-R1 RESIDUE | **Fixed** with the exact text, `aecp_arms.py:17-19`. | diff |
| R837-4-R2 RESIDUE | **Fixed** with the exact text at `:2314` and `:2322`. `:2330` was also changed, from "at this head" to "there". Every figure is unchanged. A same-pattern heading the fix did not reach is R837-5-R1. | diff |
| R838-4-F1 MINOR (Docs) | **Resolved.** Cell for cell, at both points, including the refreshed 8x8/2if row. | Point 5 |
| R838-4-F2 MINOR (Tests, Docs) | **Resolved.** The filter runs 13 tests. | Point 6 |
| R838-4-R1 RESIDUE | **Fixed.** The PR body now reads "the first REMOVE is 1,165 visits against 2,078". | PR body line 95 |
| R838-4-S10 (suggestion) | **Taken and verified.** The share bullet states 149,490 of 200,000 cycles. Round 9's final-pass receipt (`author-r9/receipts/model/measured-inputs-final-pass.txt`, H-L1L) lists the heaviest passes as 93,346, 95,503, 138,064 and 149,490. The 200,000-cycle share is in round 9's `harness-head-builds.txt`. | archive `56e8f05b` |

The other round-9 suggestions the author did not take are unchanged and stay optional. Those are R838-4-S1 to S9, apart from S7 (see S1 below), and R837-4 S2 to S4.

## Findings at this head

### R837-5-R1 RESIDUE - Docs - "at this head" heads a bullet of round 30's margins

- **Artifact:** `docs/design/SPLIT_CONTROL_MEMORY.md:2479`. It reads "**The margins at this head** (round 30's legs, every group of arm A and of the `answering-every-port` arm, on the image that merged `dev-soft-core` `0fb66211`)". This PR introduced the heading: at the base `66f71326` it read "round 28's legs ... on this head's image".
- **Evidence:** this is the pattern R837-4-R2 corrected at `:2314` and `:2322`. The bullet's figures name their own source, round 30's legs on an earlier image, which is not this head's image: rom moved in rounds 8 and 9, and round 9 re-ran the harness legs. Only the heading word is wrong, and every figure is attributed correctly.
- **Impact:** wording only. A reader may take round-30 margins for this head's. No measurement, figure, verdict, test or code changes.
- **Exact fix:** at `:2479`, replace "**The margins at this head** (round 30's legs," with "**The margins at round 30's legs** (". Every figure stays as written.

### R837-5-S1 SUGGESTION - Docs - the packet INDEX row of the redacted indexer

- **Artifact:** `author-r10/INDEX.md`, the row `scripts/index.py`. It gives 1,212 B and `96a791f1...`. The published file is 1,225 B, `4af1a900...`.
- **Evidence:** REVIEW READY says the index is "generated from the published bytes", which takes up R838-4-S7. That holds for 64 of 65 rows. The remaining row carries the pre-redaction hash, and the root `MANIFEST.json` declares that hash as `original_sha256` with `path_redacted: true`. So the packet is consistent through the root manifest, which is S7's own alternative.
- **Suggested outcome:** generate `INDEX.md` after redaction, or have it name the root manifest as authoritative for redacted files.

### R837-5-S2 SUGGESTION - Tests - the compile-time row runs at one geometry

- **Artifact:** `aecp_map_mutants.py:58-64`. The campaign runs at `endstation_ax7101_1x1_tdm8` only, and the author lists this as an open risk.
- **Evidence:** the each-direction plant cannot overflow where one direction's product is the domain: `ax7101_8x8`, 16x4 and 16x32. Only the probe receipts, the author's and mine, show the assertion refusing at 16x32 (the floor alone).
- **Suggested outcome:** optionally, add a build row that compiles the floor-alone plant at the 16x32 key geometry the work arm already builds. Then the case where the 256-slot floor would overflow is held by a gate, not by a receipt.

## Lens coverage at this head

| Lens | Result | Artifact | What was checked, and against what |
|---|---|---|---|
| Conformance | PASS | `aecp_maps.c:157-162,190-191,207-214`; `flip-1x1-1if.txt`; `load-check.txt`; `flip-selftest.txt` | Assignment items 1-4 against the diff and probes. #894 acceptance at 1x1/1if: the flip check exits 0 with every row by every source, the self-test refuses 555/555, and the load is 0.513/0.509 within 0.70. The 8x8/2if rows are reported under the standing rulings, unchanged by the delta. |
| RTL | PASS | `aecp_maps.c:157-214,370-390`; `probe-maps-identity.txt` | Firmware architecture, since the delta contains no HDL. Index range against the declared array; sentinel distinct from every index; `size_t` widths and casts; the `memset` extent; objects identical at seven geometries. |
| Robustness | PASS | `aecp_maps.c:207-224,383-386`; `probe-maps-identity.txt` | Out-of-domain keys still take the `MAP_SLOTS` sentinel and are refused at their turn. An undersized table is refused at build at every geometry where it would overflow, and compiles only where it does not. Behaviour is unchanged, shown by identical objects. |
| Tests | PASS | `aecp_mutants.py:885-914,948`; `aecp_map_mutants.py:17-19,58-64`; `row-head.txt`; `row-r9-assertion.txt`; `core-wide-filter.txt`; `fw-coverage-check.txt` | The new control can fail: it escapes with round 9's assertion. Non-build compile failures remain escapes. 274 unique sites and `controls()` hold. The 13-test filter passes. Coverage passes over 39 files. S2 is optional. |
| Docs | PASS | `SPLIT_CONTROL_MEMORY.md:2314,2322,2330,2346-2347,2461-2462,2481`; `aecp/README.md:210-241`; PR body; `table-vs-flip.txt`; `docs-check.txt` | The current rows and summary equal the tool. The assertion and floor sentences are true. The 16/56 figures were derived. The #909 citation was checked. The docs gate reports 0 findings. R837-5-R1 is RESIDUE and S1 is a suggestion. |

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment 6873298790 items 1-4; #894 acceptance; `aecp_maps.c:157-214`; own flip, self-test and load receipts | R837-5 | 7398ec0aeea468d92ff642a03a06e291a0cd58d1 |
| RTL | CLEAN | `aecp_maps.c:157-214,370-390`; host-object identity at seven geometries | R837-5 | 7398ec0aeea468d92ff642a03a06e291a0cd58d1 |
| Robustness | CLEAN | `aecp_maps.c:207-224,383-386`; planted-table probe at seven geometries | R837-5 | 7398ec0aeea468d92ff642a03a06e291a0cd58d1 |
| Tests | CLEAN | `aecp_mutants.py:885-948`; `aecp_map_mutants.py:17-64`; build row at the head and with round 9's assertion; 13/8 filters; `fw_coverage --check` | R837-5 | 7398ec0aeea468d92ff642a03a06e291a0cd58d1 |
| Docs | CLEAN (RESIDUE R837-5-R1 carried) | `SPLIT_CONTROL_MEMORY.md` section 13; `aecp/README.md:210-241`; PR body; `docs_check` | R837-5 | 7398ec0aeea468d92ff642a03a06e291a0cd58d1 |

Code outside the delta keeps its round-9 lens verdict, because nothing it depends on changed: the images and the objects are identical. The lenses R837-4 left unclean (Conformance, RTL, Tests, Docs) are covered again at this head by this round, and so is Robustness.

## Real limits

- I did not rebuild the cross-compiled images, because no cross toolchain is on this host's path. Image identity rests on two things: the author's 332-file receipts, which reference unpublished scratch environment scripts, and my host-compiler object identity for the one changed C file.
- I did not rerun the full 274-row AECP campaign, the firmware suite outside the coverage gate, the control, SRP and boundary campaigns, the Verilator job, the twin, boot, builder or NVM gates, or the hosted-step replay. For those I relied on the author's published receipts. The gate logs themselves are published only as hashes.
- I could not run `check_em_dash.py`, because its pinned renderer is not installed here. A byte scan of the added lines found no dash.
- The packet archive commit is unsigned.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- No manager source bank ran at this head, and none is inferred.

## Pending manager duties

- Validate the current-dev merge candidate (source base `66f71326`, live dev `b7d69295`) with the builder and native banks, and link the receipts.
- Hosted/act acceptance. Hosted CI does not run on split PRs.
- Obtain the second, external positive review.
- Carry R837-5-R1, and any other residue, to the residue checklist.
- Unchanged duties: 8x8/1if (lane 894b), 8x8/2if reported (#910), #908 and #909 open, and the owed S12b wire capture.
- An explicit maintainer authorization before any merge.

R837-5 FINISHED
