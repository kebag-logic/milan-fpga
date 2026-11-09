[R809] POSITIVE - exact head 794f8442c3d9da158c99d358d825c7b277516bba

# R809-2: independent review of processor issue #217 / PR #219, section 6 and the evidence census

- Head `794f8442c3d9da158c99d358d825c7b277516bba`, tree `9b60c7bbf6b35e34c4c1c2aae306d7477d1eda5d`. This is the same head as R809-1, so there is no source delta since the last reviewed head.
- Base `044cb25f4ed2187bd238490650e73d5d189855d1`.
- Evidence: kebag-logic/milan-fpga `ea450d8d30779e24e9dc8588957623e57dbccf48` (tree `f1efd0715116325ae5070571f7d8bf96f1406219`), `review-evidence/pp217-r1/`.
- Scope, per the manager's ruling (PR #219 issuecomment-6749487294):
  - re-run the census on a complete recursive listing;
  - read the named rc files and log tails, and twin/head against twin/base;
  - judge issue #217 acceptance bullet 4 and the twin claim;
  - confirm F-2.
- Sections 1 to 5 and 7 of R809-1 stand and were not re-done here. The source is unchanged, so their lens verdicts carry over.

## Verdict basis in one paragraph

The evidence commit is complete. Its full recursive listing has 2,020 blob lines in the whole tree and 542 under `review-evidence/pp217-r1/` (541 manifest files plus `MANIFEST.json`). The tree API agrees and reports `truncated: false`. Re-run on that listing, `evidence_census.py` finds 522 entries named by the 29 INDEX files, 0 missing and 0 size mismatches. Every one of the 541 MANIFEST rows hashes to its published file, and no file goes unlisted. R809-1-F-1 came from a listing cut short at 293 blobs. It is withdrawn: refuted at its cause.

Every scratch-parent gate ended rc 0 with a PASS tail. That includes the six the ruling names. The gate commands match the parent's `rtl-fast.yml` at the scratch base `ac0a01e3` one for one. All of them ran after the ROM digests were recorded at pin `794f844`. The twin's rc 2 is its designed outcome. At base the twin already makes 3 findings, all MVRP. The head adds exactly one: the owed row `entity-available-index` "has gone". That is the fix itself, and the twin's own documentation requires the consumer to delete that row. The split capture is unchanged, and the fabric capture differs in one byte of one frame, available_index 0 → 1. Acceptance bullet 4 is met. F-2 is fixed in the PR body. No MINOR or worse finding is open.

## 1. Census of the evidence commit (scope item 1)

How it was run (`scripts/listing.sh`, re-run end to end into a scratch directory with byte-identical listings):
- partial clone of `ea450d8d` with a sparse checkout of `review-evidence/pp217-r1/`;
- `git ls-tree -r` to files, never through a pager or a truncating wrapper.

| Receipt | Lines |
|---|---|
| `receipts/ea450d8d_ls-tree-r_full.txt` (whole tree, blobs) | 2020 |
| `receipts/ea450d8d_ls-tree-r_pp217-r1.txt` (blobs under `pp217-r1/`) | 542 |
| `receipts/ea450d8d_ls-tree-r-t-l_pp217-r1.txt` (blobs and trees, with sizes) | 577 (542 blobs, 35 trees) |
| `receipts/ea450d8d_listing_census_format.txt` (census input) | 577 |

- **Tree API cross-check** (`receipts/tree_api_summary.txt`): `truncated False`, 2,293 entries, 542 blobs and 33 sub-trees under `pp217-r1/`. That count excludes `review-evidence` and `pp217-r1` themselves, so it agrees with the 35 above.
- **Census** (`scripts/evidence_census.py`, unchanged from R809-1): "522 entries named by INDEX files, 0 missing from the tree", rc 0, and no SIZE line (`receipts/evidence_census.txt`, `.rc`).
- **Manifest** (`scripts/manifest_check.py`): "541 manifest rows, 0 absent, 0 hash mismatches, 0 unlisted files, 5 path_redacted, 542 files on disk", rc 0 (`receipts/manifest_check.txt`). The 5 redacted rows are author tool scripts under `author/tools/`. None is a receipt.
- Every path R809-1-F-1 named as absent is present: `proc/`, `twin/`, `repro-base/`, `parent/superseded-piped/`, all 48 `parent/` files, and `author/tools/`.

## 2. Parent consumer gates (scope item 2)

**Scratch parent** (`author/receipts/IDENTITY.txt`): milan-fpga dev `ac0a01e3` plus four local commits, never pushed. The last two commits pin `794f844` and record its ROM digests. Its changed paths against dev are exactly `protocol-processor` and `syn/yosys/rom_digests.tsv` (`parent/ci_changed_files.log`). The scope classifier answers `true`, which means a full rtl-fast scope.

| Gate (`parent/`) | Command | rc | Tail |
|---|---|---|---|
| `rom_digests` | `./syn/yosys/ooc.sh --record-rom-digests` | 0 | "recorded ROM content digests for protocol-processor pin 794f8442c3d9da158c99d358d825c7b277516bba and gptp-processor pin 1616fc8f… in syn/yosys/rom_digests.tsv" |
| `yosys_elaborate` | `syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow` | 0 | 3 tops PASS (cells 79622 / 70363 / 3717), "tops: 3 pass: 3 fail: 0", RESULT: PASS |
| `publication_census` | `python3 sw/mailbox/publication_census.py --check --selftest --jobs 4` | 0 | "6 shape(s), checks: 246 failures: 0"; "mutations: 0 of 31 rule(s) no arm proves" |
| `pp_shadow` | `make -C tb/verilator/pp_shadow` | 0 | "pp_shadow: 317 checks, 0 failures", RESULT: PASS. The published tail's full-log digest is `a2efb697…`, 350,348 B. |
| `nvm_cosim` | `make -C tb/verilator/nvm_cosim` | 0 | "39 of 39 mutant(s) killed by their named check"; "465 checks: 465 PASS, 0 FAIL", RESULT: PASS |
| `milan_dp_render` | `make -C tb/verilator/milan_dp_render` | 0 | tdm8_render 79 and 263 checks, 0 failures, RESULT: PASS (twice); leg defects "5 checks: 5 PASS, 0 FAIL". The only "fail" words in the log are these zero counts. |
| `milan_dp`, `milan_dp_mclk`, `capture_coherence` | `make -C tb/verilator/…` | 0, 0, 0 | 6/6, 34/34, 42/42 PASS tails |
| `behave` | `cd tests && behave --no-capture -f plain` | 0 | 14 features, 508 scenarios, 2330 steps passed, 0 failed, 0 skipped |

**Match against the parent's `rtl-fast.yml` at `ac0a01e3`** (fetched read-only; `receipts/rtl-fast_ac0a01e3_jobs.txt`). Each job's run step has a receipt with the same command, every one rc 0:

| Job | Receipts |
|---|---|
| changes | `ci_scope_selftest` |
| verilator-lint | `lint_rtl`, `pp_srcs` |
| bdd-conformance | `behave` |
| yosys-elaboration | `yosys_elaborate` with the same three tops; `ooc_read_sets` with the ten `syn/ooc` commands in the workflow's order; `ooc_selftest`, `guard_selftest`, `cache_selftest` |
| publication-census | `publication_census` |
| firmware-unit | `fw_tally_selftest`, `fw_rv32_sdk_selftest`, `fw_rv32_selftest`, `fw_shard0`, `fw_ctrl_nvm`, `fw_coverage_selftest`, `fw_coverage` |
| control, AECP and SRP mutation campaigns | `fw_shard1`, `fw_shard2`, `fw_shard3_srp`, the workflow's `--shard 1/4`, `2/4`, `3/4` |
| firmware-boundary | `fw_boundary` |
| firmware-verilator | `fw_verilator` |

- The jobs without a receipt build tools (`yosys-tool`) or run CI plumbing (`rtl-fast`, `ci-manifest`, `ci-fail-fast`, `ci-cancel-tail`). They exercise no processor behaviour.
- **Ordering** (`receipts/parent_gate_timeline.txt`): every gate started after `rom_digests` ended (epoch 1794208142, 2026-11-09 07:09 UTC). So none of them ran at the scratch parent's earlier `43149fb` pin.
- **Process receipts.** `interrupted-1034/fw_shard0` has a start and no rc. It was re-run to rc 0 (`parent/fw_shard0`). `superseded-piped/ci_scope_classify` was a tee-piped run, replaced by the unpiped pair `ci_changed_files` and `ci_scope_classify`, which agree with it. Neither is a defect.
- **F-2 check** (`proc/run_suites.log`, the head sweep): 36 `PASS <suite>` lines, 0 `FAIL` lines, and the per-suite checks sum to 1,032,052. The log prints "suites: 1032052 checks total, 0 failing", rc 0. The PR body now reads "1,032,052 checks, 0 failing (36 suites)". **F-2 is fixed.**

## 3. Twin: head against base (scope items 2 and 3)

| Run | Processor pin | rc | Findings | Captures |
|---|---|---|---|---|
| `twin/base` | `044cb25f` | 2 | 3 | fabric `cba463ad…`, split `ee143865…` |
| `twin/head-43149fb` | `43149fb` | 2 | 4 | fabric `72134697…`, split `ee143865…` |
| `twin/head` | `794f844` | 2 | 4 | fabric `72134697…`, split `ee143865…` |

The full comparison is in `receipts/twin_findings_diff.txt`.

- **`report.json`, base → head.** The `counts` and `measured` objects are identical. The only finding the head adds is `[DIFF] owed row entity-available-index: the difference has gone`, and the base has no finding the head lacks. The only note the head lost is base's `[OWED] entity-available-index` row, which at base still held: "the fabric sends the ENTITY descriptor with available_index 0 after the ENTITY_AVAILABLE that carried 1, the split … 1".
- **The 3 findings shared by base and head** are all MVRP VID 0002: two `[MRP]` Applicant-message findings and `[DIFF] owed row fabric-vid2-join-in does not hold` (JoinIn x14 against the row's x15). This matches the PR's "Its other three findings, all from the all-fabric MVRP, are the same at base and head".
- **`twin/head` and `twin/head-43149fb`.** Their `report.json` files are byte-identical, as are the fabric and split capture digests. `43149fb..794f844` changes only `tb/pp_top/aecp_dispatch_mutations/rdc-base-no-overlay.patch` and `tb/pp_top/ctr_mutations/store-link-detector-resets-up.patch`, which the twin never reads. That is also why the head run's Verilator report reads "0 modules": it re-linked the identical 43149fb model in the same scratch copy. This is sound, because every RTL and ROM input is byte-identical.
- **`capture_diff.txt`.** The fabric has 195 frames at base and head. Exactly one differs: frame 59 at 7501 ms, wire byte [81], "all inside descriptor octets 36..39 (available_index): base 0, head 1". The split has 260 frames and 0 differences.
- **The served descriptor in the head finding.** It decodes to `0004` (READ_DESCRIPTOR), configuration 0, ENTITY 0, entity_id `020000fffe000001`, model `001bc5c1935893e1`, capabilities `0000c588`, 2/`4801` talker, 2/`4801` listener, controller `00000000`, and **available_index `00000001`**, followed by entity_name "Milan FPGA 1x1 TDM8". That is the index of the one ENTITY_AVAILABLE before the read, the value IEEE 1722.1-2021 Table 7-2 and 6.2.2.15 require.
- **The published log supports the findings.** All 16 lines of `twin/head/findings.txt` occur verbatim in the published `twin/head/twin.log` at the line numbers they carry. The log ends with "twin: 4 finding(s)" and `make: *** [Makefile:939: twin] Error 1`.

**The author's explanation of rc 2 holds.** The public `tb/verilator/milan_dp/twin_compare.py` at the lane commit `a88772f1` documents three points:
- "a row whose difference has gone is a finding too, so the lane that fixes it deletes the row" (lines 22-24);
- "exit 1 on any" finding (line 35);
- the "vanished-available-index" plant with the words "owed row entity-available-index: the difference has gone" (line 89), and the row itself (line 484).

The twin exits nonzero at base too, and for the same three MVRP findings, so rc 2 is not a regression. The twin lives on the unmerged lane branch `665-s6b-cosim`, not in the parent's rtl-fast. Under its own rules, the one new finding is exactly the expected sign that this defect is fixed.

## 4. Issue #217 acceptance bullet 4 (scope item 3)

"The parent's gates that read AECP and ADP pass on a scratch parent with this head pinned." **Met.**
- The scratch parent pins `794f844`. The ROM digest record and the twin identity name that pin.
- Every rtl-fast job that runs a check has an rc 0 receipt with the workflow's own command.
- So do the five datapath benches that build the processor inside the datapath (`milan_dp`, `pp_shadow`, `nvm_cosim`, `milan_dp_mclk`, `capture_coherence`) and `milan_dp_render`.
- Limits: the scratch parent's local commits were never pushed, so their identity rests on the author's receipts. And the parent's dev has since moved to `123f57a9`. Both are covered by the manager's merge-turn candidate build (below).

Bullets 1 to 3 were judged CLEAN in R809-1 sections 1 to 3, and that judgement stands.

## Findings

### R809-1-F-1 MAJOR (Tests, Docs): WITHDRAWN, refuted at its cause
- **Cause:** R809-1 ran the census on a listing that held only 293 of the commit's 542 blobs. The evidence commit itself was complete all along.
- **Verification at this round:** census 0 missing of 522 named, rc 0; manifest 541/541 hash-exact, 0 unlisted (section 1).
- R809-1's `receipts/evidence_census.txt` (52 missing) is superseded by this round's `receipts/evidence_census.txt`.
- No republish and no author action is needed.

### R809-1-F-2 MINOR (Docs): RESOLVED
- The PR body reads "(36 suites)", and the head sweep log has 36 PASS suite lines (section 2).

### R809-1-R-1 RESIDUE (Docs): RETAINED, carried to the residue checklist
- `hdl/aecp/ucode/gen_ucode.py:387-388` and `docs/architecture/06_aecp_engine.md:322-323` compare `rdent_r` routing with START/STOP's 0xD0.
- The exact fix is in R809-1 and is unchanged at this head.

### R809-1-R-2 RESIDUE (Docs): RETAINED, carried to the residue checklist
- The PR body's area paragraph attributes the 33 flip-flops but not the LUT and MUXF7/8 deltas.
- The exact sentence to append is in R809-1 and is unchanged.

### R809-1-S-1 SUGGESTION (Tests): RETAINED
- An IF9 sample of `last_avail_index_o` between the two ENTITY_DEPARTINGs would pin the per-interface clear.
- Optional.

### S-2 SUGGESTION (Tests, Docs): label the twin log digest as pre-normalisation
- **Artifact:** `review-evidence/pp217-r1/author/receipts/twin/head/sha256.txt` against `twin/head/twin.log`, and the `MANIFEST.json` row for that log.
- **Evidence:**
  - `sha256.txt` records `01d7e4c5…  twin/twin.log` and "twin.log bytes 26024".
  - The published `twin/head/twin.log` is 24,580 B, sha256 `f4dba92f…`. Its paths are replaced by `$TWIN` (50 times) and `$TOOLS` (4 times).
  - MANIFEST marks the file `path_redacted: false`, with `original_sha256` equal to `published_sha256`.
  - So the recorded digest is that of the raw scratch log, not of the file published beside it. The packet cannot tell a reader whether the `*.log.sha256` files beside the `.log.tail.txt` files are likewise digests of un-normalised logs.
- **Impact:** none on any claim. The findings, report and capture digests are self-consistent, and all 16 finding lines match the published log at their line numbers. A reader who checks the sibling digest will see a mismatch with no stated reason.
- **Suggestion:** in later packets, either record the digest of the published, path-normalised bytes as well, or state in the INDEX or MANIFEST that the log digests and sizes are of the un-normalised originals.
- Not required for this PR.

No new MINOR, MAJOR or BLOCKER finding. There is no source delta since R809-1, so there is no new source comment to check against the comment rule; R809-1 section 7's comment-rule scan stands.

### Other prior public review findings at this head

The R810-1 review (PR #219 issuecomment-6749693033, POSITIVE) was read only after this round's verdict and ledger were written.

| R810-1 item | Severity | Status here |
|---|---|---|
| R-1 (the START/STOP 0xD0 comparison) | RESIDUE | RETAINED. Same defect as R809-1-R-1. |
| R-2 (area LUT and MUXF attribution) | RESIDUE | RETAINED. Same defect as R809-1-R-2. |
| S-1 (pin the index's upper octets with an index of 256 or more; its `gather-low-byte` probe survives AI) | SUGGESTION | RETAINED. Outside this round's scope and not re-probed here. It does not change any verdict: the path is 32 bits wide by construction (R809-1 section 1), and byte order is pinned. |
| S-2 (the per-interface clear on DEPARTING) | SUGGESTION | RETAINED. Same as R809-1-S-1. |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | R809-1 sections 1 to 3 (Table 7-2, 6.2.2.15, Milan 5.6.3 against the RTL; bullets 1 to 3), unchanged at this head. Here: bullet 4 judged met; the head twin's served ENTITY descriptor decoded to available_index 1 after one ENTITY_AVAILABLE; the base twin row recorded 0 | R809-1 (sections 1 to 3), R809-2 (bullet 4) | 794f8442c3d9da158c99d358d825c7b277516bba |
| RTL | CLEAN | R809-1 sections 2 and 4 (full `hdl/` delta), unchanged at this head. Here: the parent's `yosys_elaborate` (3 tops) and `lint_rtl` at pin 794f844, rc 0 | R809-1, R809-2 | 794f8442c3d9da158c99d358d825c7b277516bba |
| Robustness | CLEAN | R809-1 probes, unchanged at this head. Here: the twin's other captures unchanged (split 0 differences, fabric 1 byte), and the parent's mutation campaigns and benches rc 0 | R809-1, R809-2 | 794f8442c3d9da158c99d358d825c7b277516bba |
| Tests | CLEAN | Census of `ea450d8d` (2,020 / 542 / 577-line listings; 522 named, 0 missing); manifest 541/541; parent gates mapped one for one to `rtl-fast.yml` at `ac0a01e3`, all rc 0, with the six named tails read; head sweep 36 suites; twin base, 43149fb and head reports, captures and findings compared; R809-1-F-1 withdrawn; S-2 | R809-2 | 794f8442c3d9da158c99d358d825c7b277516bba |
| Docs | CLEAN | PR body "36 suites" (F-2 resolved); the PR's consumer-gate and two-placement paragraphs checked against the receipts (rtl-fast job list, 195/260 frames, one differing response at octets 36..39, the three MVRP findings unchanged); R-1 and R-2 retained as residue; R809-1 section 7 stands | R809-1, R809-2 | 794f8442c3d9da158c99d358d825c7b277516bba |

## Real limits

- This round re-ran no processor, parent or twin gate. Source-head execution evidence is the author's published receipts, and parent and twin runs are outside a reviewer's allowed scope. The R809-1 processor runs at this head stand.
- The scratch parent's four local commits and the twin's scratch copies were never pushed. Their identity (pin `794f844`, superproject commits) rests on the author's `IDENTITY.txt`, `twin/*/identity.txt` and the ROM-digest log line.
- `capture_diff.txt` was computed by the author from the twin's `fabric.json` and `split.json`. Those captures are not published, only their digests. Their agreement with `report.json` (identical counts, one finding changed) supports the result, but this reviewer did not recompute the frame diff.
- The full `pp_shadow`, `milan_dp`, `capture_coherence` and `behave` logs are published only as tails plus a digest of the full log.
- The exact-head hosted `suites` job of the processor (runs 42665288037 and 42665248413) was still `in_progress` when read (`receipts/hosted_check_runs.txt`). `docs-gates` and `portability` succeeded in both. Skipped contexts were not counted as executed.
- Physical calibration NOT RUN. Field skips are not hardware proof. No manager source bank ran at this head, and none is claimed or inferred.
- The standards texts were not re-read this round; R809-1's limit on clause text stands.

## Pending manager duties

- At the merge turn: build and validate the current-dev merge candidate with the builder and native banks, and link the receipts on the PR. The source base is `044cb25f`; the live dev is `123f57a922bf07476cd69f91867f3b6f07080804`, which has moved past the scratch parent's `ac0a01e3`. Also take the hosted `suites` conclusion for this head.
- R809-1-R-1 and R809-1-R-2 go to the residue checklist. Optionally, S-1 and S-2 go to the author.
- When the parent takes this pin, delete the twin's `entity-available-index` owed row (in `twin_compare.py`, lane `665-s6b-cosim`, or wherever that ledger lives when the pin lands). The twin's design requires this; until then the twin keeps reporting "the difference has gone".
- The parent must also re-record the ROM digests at the pin, as the scratch parent did.
- Merge still needs the full completion bar.

## Publishable receipts

Listed in `MANIFEST.sha256`:
- scripts: `scripts/listing.sh`, `scripts/evidence_census.py`, `scripts/manifest_check.py`;
- receipts: the four listing files, `evidence_census.txt` and `.rc`, `manifest_check.txt` and `.rc`, `tree_api_summary.txt`, `listing_line_counts.txt`, `gate_reads.txt`, `parent_gate_timeline.txt`, `rtl-fast_ac0a01e3_jobs.txt`, `twin_findings_diff.txt`, `hosted_check_runs.txt` and `.json`, `IDENTITY.txt`;
- the PR, issue and PR-comment snapshots.

After the review, the exact-head clone has 0 porcelain entries, HEAD and tree are as above, and the repository has no gitlinks (`receipts/IDENTITY.txt`).

R809-2 FINISHED
