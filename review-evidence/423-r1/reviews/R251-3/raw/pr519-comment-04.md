https://github.com/kebag-logic/milan-fpga/pull/519#issuecomment-5780238890
[R243] POSITIVE - exact head df53dfa116b34816db0193230ad9833e67bf46dd

R243-1, cleared-context internal Codex source review of kebag-logic/milan-fpga Issue #423 / PR #519. Tree: `fb7bbe66e6326d9d55b4ad13170446dff12a133a`. All five lenses applied. No open BLOCKER, MAJOR, MINOR, or SUGGESTION finding in this review. This is a source-review verdict; the pending manager gates below remain required.

## Contract and scope

Authorities examined: `AGENTS.md` sections 6-8; `CONTRIBUTING.md` sections 2.1, 2.2, 3; `docs/README.md`; `REQUIREMENTS.md:222` (REQ-VER-04); `docs/overview/ARCHITECTURE.md:39`; `docs/reference/SUBMODULES.md`; [Issue #423](https://github.com/kebag-logic/milan-fpga/issues/423), especially [settled decision 5777210218](https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5777210218); and the [public assignment](https://github.com/kebag-logic/milan-fpga/pull/519#issuecomment-5779895594). Public fixture construction and raw expected OIDs were retrieved separately from the immutable design evidence. No private implementation-lane material or final report of another reviewer was used.

The source integration commit has ordered parents `52711029f374650dc93830d5ea28e81cb5c8f410` and `fed4f63f33e6185e5c7e4735a27234db99651d24`. The latter is the author change over `88e9276b2a220c716f64a843f7e1eb8f9265e896`. The seven-file issue diff is recorded in `source.diff`; history is in `source-history.raw`. It changes the checker, its helpers/tests, and CONTRIBUTING. It contains no production RTL, firmware, pin, workflow scheduling, or older-arm policy change.

The decision preserves refusal of lost work for the new arm. The positive requires a non-overlapping later extension. Adjacent extension and actual gPTP PR62 remain unresolved. The existing linear historical policy is deliberately preserved and remains separately owned by #514; this review does not declare that issue resolved.

## Conformance

[R243] PASS Conformance - `scripts/check_merge_containment.py:523`, `scripts/merge_containment_replay.py:36`, `scripts/merge_containment_replay.py:97` - selected G1 + H + T and existing arm order match the settled decision.

Requirement/evidence: inspection, real public Git reconstruction in `public-history-data.json`, raw retention measurements in `public-retention-data.json`, full CLI matrix/arm traces in `matrix-review-data.json`, and independent histories in `independent-history-data.json` support the following results.

- G1 enumerates only `base..branch` merges. It requires one row, exactly two ordered parents, the second parent's entire parent list equal to `[first]`, and equal merge/second-parent trees. Multiple merges, octopus, distant or reversed parents, and resolution changes cannot satisfy this arm. An ancestor-only shortcut is absent.
- H uses the existing `_linear_patches_contained` helper (`check_merge_containment.py:198`). Every source-only non-merge commit requires a whitespace-preserving patch ID and exact touched-path postimages. Matching replay candidates are consumed, so a replay cannot certify two source commits. Missing work, different whitespace, and a repeated-location patch with a different postimage fail H.
- T requires one merge base and enumerates the source's net-changed paths with NUL delimiters and renames unfolded. It compares literal raw mode/kind/OID entries, including absence. Different entries may proceed only when tip/source and any present ancestor are regular blobs and the documented mode rule holds. Blob contents come from `cat-file`; temporary files are written as bytes. `merge-file` must return 0 AND produce the exact tip bytes. No resolution option, custom driver, textconv, or normalization supplies this proof.
- Failure of G1 or a measured negative H falls through to the original result. Unmeasurable proof or successful H with unproved retention yields UNKNOWN/nonzero. Path-level T failures retain literal path attribution. Conflict and command-error outcomes cannot become a positive.

The real call order is ancestry, touched-path equivalence, linear patch equivalence, then retained redundant replay. Matrix rows 4/5 stop at the earlier path arm; rows 30/31 stop at the historical linear arm. Rows 1/2 traverse the new fallback. The trace wrapper only recorded results and delegated to the unchanged functions; every matrix outcome was also checked through a separate real CLI process.

Public-history result: source `3db86812096830fada2f5f276fa5f4d9f37d1d14` has exactly the source-only merge `f27b45500cb02a5277b5cb32cef408658c1f914e`, whose parents are `7fa64e99490b4648797374d3fdb1fedf08145e91` and `9790ac736e6d10301ad814ffdf73dbe37b59768b`. The latter has only the former as parent; its tree equals the merge tree. Both tested targets have that same unique merge base.

| Original / distinct replay | Raw diff SHA-256 | Exact postimages |
|---|---|---|
| `9790ac736e6d10301ad814ffdf73dbe37b59768b` / `20927af74752620b2ad0f973e8be3203994b5547` | `d3d164b309e376ea06a3734e8452dd5668c4721d0462dc0656af05d6b3c155b3` | All five touched paths |
| `3db86812096830fada2f5f276fa5f4d9f37d1d14` / `5602e70bb4cf70c2e0e39e846e26925e27659e32` | `fa20a2516a4d866a859506c5396779fb98bbafe943e4de2651e9ec252bca996f` | All three touched paths |

Both hashes were independently reproduced with `git diff --no-ext-diff --no-textconv --no-renames <parent> <commit>`, hashing the exact stdout bytes. Original/replay patch files are retained in this packet.

At both `f0f1c055ee5226f08e656c27cb1bf4c355be11ae` and pinned/current `c1b617435824929a790739ea8585c3fe1a328cc0`, the CLI returns UNKNOWN/1, naming `tb/tsngen/mutants.py` and `tb/verilator/gaskets/mutants.py`. Independent raw merges of each of those paths return 4, with output differing from tip. The two Makefile paths merge with return 0 and exact tip output; `tb/mutation_verdict.py` has exact entry identity. Live donor `main` was independently observed as `c1b61743...` in `gptp-live-main.raw`. This is no blanket containment PASS for gPTP, PP/protocol-processor, or any other donor history.

Impact/outcome: the selected positive is admitted without turning historical replay alone into current-retention evidence. Verification: all named positive and refusal cases passed; no conformance change is required.

## RTL and architecture

[R243] PASS RTL - `source.diff`, `scripts/check_merge_containment.py:69`, `scripts/merge_containment_replay.py:14`, `scripts/run_all_suites.sh:237` - tooling/module boundaries and existing product contracts remain intact.

Requirement/evidence: the issue's explicit source-only scope, architecture/submodule ownership documents, the complete seven-file diff, `old-definitions-comparison.json`, and final source integrity. The checker supplies Git and replay callbacks to the bounded helper; the helper's result remains the existing `(is_contained, ahead, note)` contract. UNKNOWN retains `None`, and the report path returns the existing finding status 1. Startup/cannot-run status 2 and self-test cleanup status 3 remain separate.

The historical helper and every pre-existing arm implementation remain unchanged apart from the shared transport and the new final call/report wording. The default self-test calls the appended suites through its existing owner. The normal full-suite preflight invokes that owner and aborts on a failing test; cleanup-only status 3 retains its existing treatment.

Impact/outcome: no clock/reset/CDC/FSM/firmware or pin contract is changed by this tooling patch. All root entries and registered required submodules were checked directly against committed blobs and index records, independent of status/index flags. Verification: 855 root blobs, 222 protocol-processor blobs, 103 gPTP blobs, and 214 verilog-axis blobs match their recorded kinds, bytes and executable modes. No architecture change is required.

## Robustness and shared Git transport

[R243] PASS Robustness - `scripts/check_merge_containment.py:92`, `scripts/check_merge_containment.py:152`, `scripts/merge_containment_replay.py:59`, `scripts/merge_containment_replay.py:113`, `scripts/merge_containment_selftest_retention.py` - byte handling and measured failure boundaries remain conservative.

Requirement/evidence: the settled boundary controls; the 326-assertion default run; `git-caller-census.json`; independent raw-path/CRLF/reversal cases; public mutation runs; and the helper's complete exception/exit handling.

All 21 pre-existing direct `_git` callers were examined, grouped below. Exact lines and call locations are retained in the census.

| Callers | Transport and error effect checked |
|---|---|
| `verbatim_patch_id_error`, `active_graft_error`, `main` | Version/graft-path/shallow checks still inspect status and expected output. Git capability probing remains separate. Captured stderr is not decoded by `_git`. |
| `exact_ref_syntax`, `configured_remote_name`, `offline_ref`, `fetched_branch_refs`, `non_origin_remote_ref`, `_unreadable_ref_error`, `_branch_targets`, `_fetch_origin`, `continuous_merged_pr_tip` | OIDs and line-oriented Git protocol output retain existing parsing; namespace, remote, continuity and refresh rules are unchanged. Existing refusal tests remain green. |
| `_linear_patches_contained`, `_commits_ahead`, `_patch_id_verdict`, `contained` | ASCII graph/count output and return-code checks are preserved. Neither empty/malformed output nor a failed command is treated as successful zero work. |
| `_commit_paths`, `_same_patch_postimage`, `_path_scoped_verdict`, `_differing_paths` | NUL-delimited filenames now preserve CRLF and undecodable bytes; literal comparison arguments round-trip through surrogateescape. Return-code decisions remain before acceptance. |
| `_verbatim_patch_id` | Git patch stdout is decoded with surrogateescape and re-encoded to bytes before patch-id input. Patch-id's OID output is parsed as ASCII. No universal-newline translation remains in the patch transport. |

The existing `_git` terminal-LF stripping remains; it is not a general arbitrary-blob byte API. NUL path terminators keep trailing filename newlines intact. The new T path uses `_git_bytes` instead, preserving complete blob/output bytes without trimming. The independent 0..255-byte round-trip explicitly checked this distinction. CRLF/raw-path controls separately exercised the old path arm, old linear historical arm after reversal, and final differing-path reporting.

Boundary controls passed for literal/exclude-shaped paths, tabs/newlines/CRLF/non-UTF-8 paths and blob bytes, no final LF, absent/add/delete entries, symlinks, gitlinks, file/type changes, executable-bit loss, retained mode changes, binary merge refusal, SHA-1 and SHA-256. Command/storage/missing-object/malformed-entry and ambiguous/failed merge-base controls remain UNKNOWN. The binary error mutant demonstrates that a merge error is not a retention proof. Hostile driver/filter/textconv/configuration controls remain raw and do not execute the planted helper commands. Invalid configuration is an unmeasurable result.

Impact/outcome: no raw-byte or mode-loss false containment was observed in the scoped controls; no robustness change is required. Verification limits: Git 2.55.0 on this Linux environment was tested. Large-file/resource behavior, all Git/platform combinations, and arbitrary semantic rewrites are not established by this review.

## Tests and proof sensitivity

[R243] PASS Tests - `scripts/merge_containment_selftest.py:103`, `scripts/merge_containment_selftest_replay.py:502`, `scripts/merge_containment_selftest_mutations.py:16`, `scripts/merge_containment_selftest_retention.py:232`, `matrix-review-data.json` - tests exercise the actual branch-selection/CLI behavior and detect the intended guard defects.

Requirement/evidence: unchanged assertion policy and the issue's explicit matrix, guard-mutation, positive, negative and boundary acceptance. The focused candidate self-test exits 0 with 326 assertions: the original 145 plus 44 public replay assertions, 25 mutation assertions and 112 retention assertions. A separate execution of the four original baseline modules exits 0 with 145 assertions. All 145 complete result rows are byte-identical to the first 145 candidate rows (`assertion-preservation.json`); the content and scratch modules are byte-unchanged.

The immutable public fixture builder was used independently of the production fixture adaptation. All 31 original branch-head/base-tip OID pairs reproduced. The original CLI plus ten single-guard replicas produced 341 measured CLI results. Exact expected changed-case sets were asserted across the entire matrix, including unaffected cases. No mutant was credited merely for crashing or refusing an unrelated operand.

| Guard mutation | Public cases changed | Actual change detecting the rule |
|---|---|---|
| One-merge count | 3 | STRANDED/1 to contained/0 |
| Two-parent count | 25 | STRANDED/1 to contained/0 |
| Direct ordered parent | 28 | STRANDED/1 to contained/0 |
| Merge-tree equality | 21, 22 | Missing resolution becomes UNKNOWN/1; independently present resolution becomes contained/0 |
| Historical proof | 17-20 | STRANDED/1 to UNKNOWN/1; verdict text detects bypass although T still refuses |
| Current-retention proof | 6-16 | UNKNOWN/1 to contained/0 |
| Exact entries only, removing allowed raw merge | 1, 2 | Required positives become UNKNOWN/1 |
| Mode rule | 10 | UNKNOWN/1 to contained/0 |
| Tip-byte equality | 14 | UNKNOWN/1 to contained/0 despite a clean merge changing output |
| Merge-error rejection | 11 | UNKNOWN/1 to contained/0 on binary merge failure |

Additional independently constructed commit-tree fixtures cover 22 CLI histories plus one complete-byte transport control. Four partial reversals (LF, CRLF, no-final-LF and undecodable bytes) each produce raw merge status 0 but non-tip output and therefore UNKNOWN/1. Ten edit positions distinguish non-overlap, adjacency and exact restoration. A separate history with source edits A / reverse-A / A and only one exact replay of A remains STRANDED. Removing only `candidates.remove(match)` changes it to contained with the retention marker, isolating the distinct-witness requirement.

A further 1,920 raw three-way probes enumerated all five-line binary-alphabet originals, position pairs, replacement/deletion/insertion edits, and either one-edit reversal plus a suffix. None returned both status 0 and exact tip output. This population, the 31 histories, and the author's separately reported 11,256 alignment combinations are bounded evidence, not a general alignment or semantic-preservation proof. Git's [merge-file documentation](https://git-scm.com/docs/git-merge-file) defines the clean-merge status and discusses alignment-related mismerges; a clean result alone is insufficient for this implementation and this verdict.

Impact/outcome: the positive branch is reachable, the refusals are observable, and critical weakened guards are detected for their intended rules. Verification: all recorded reviewer tests passed. No test change is required.

## Documentation and public evidence

[R243] PASS Docs - `CONTRIBUTING.md:208`, `scripts/check_merge_containment.py:44`, PR #519 body, `public-candidate1/manager-builder-final/results.json`, `public-evidence-MANIFEST.json` - contract, reproducibility and evidence limits agree with the examined source.

Requirement/evidence: REQ-VER-04, the settled wording requirement, documentation routing, the diff, focused docs/idiom/whitespace checks, and public manager records. CONTRIBUTING distinguishes historical landing, current retention and unresolved overlap; names the exact topology/mode rule; preserves #514 ownership; and supplies the raw patch reproduction command. The PR's source-only and pending-gate claims match the evidence examined.

The reviewer independently downloaded 72 manager evidence files from immutable object `e637950b796e5a01bdbd37c6e5bd663ccd867ec4`. Their Git blob hashes and published manifest SHA-256 values match. Every composed builder row equals its selected published source receipt. Original/correction hash fields match the manifest's pre-path-neutralization identities; they are not misrepresented as hashes of the path-neutralized bytes.

The original 46-row builder run retains aggregate exit 1: 45 successes and the stale-endpoint whitespace command at row 45 (zero-based 44), exit 128. The separate actual correction uses base `52711029...` and candidate `df53dfa...`, exits 0, and has empty output. The final 46-row ledger selects that correction and the 45 original successes. It is explicitly a composition, not another execution. The independent reviewer diff check on those same endpoints also exits 0.

The five manager native groups are recorded at this exact source/base with exit 0: parent Verilator, Yosys, protocol-processor suites, gPTP suites and behave. The parent log records four declared field-campaign skips contributing zero checks. Builder calibration gate 11 is NOT RUN and supplies no physical proof. The native and builder integrity receipts bind the root tree and all three required pins. The reviewer inspected this evidence; did not rerun the prohibited full native/builder bank or relabel manager results as reviewer executions.

Impact/outcome: a cold reader can reconstruct the decision, source, measurements, correction, and remaining scope. Verification: `docs_check.py`, `check_py_idiom.py`, and the exact-base `git diff --check` all exit 0. No documentation change is required.

## Reproduction and receipts

Reviewer tool: Git 2.55.0. Focused work stayed within the eight-job cap; the largest independent probe/download pools used four workers. Source bytes were preserved. No source fix/commit/push, public comment/metadata mutation, merge, author/agent contact, hardware, install, privilege change, Docker/act, candidate host-side act_ci, or hosted inspection was performed.

Each named run has its exact command, cwd, status, elapsed time and output hashes in `<run>.json`, with raw stdout/stderr beside it. Principal runs: `selftest`, `baseline-selftest`, `matrix-review`, `independent-history`, `alignment-review`, `public-history`, `public-retention`, `docs-check`, `idiom-check`, `diff-check`, `evidence-download`, `evidence-composition`, and `final-source-integrity`. Scripts and the original public fixture inputs are retained. Disposable matrix Git stores can be reconstructed from the fixture builder; they are not evidence dependencies.

From the exact source checkout, the focused source command is:

```sh
rtk proxy python3 -B scripts/check_merge_containment.py --selftest
```

The packet's `REPRODUCE.md` gives the reviewer-script commands and fresh-output-directory requirement. `MANIFEST.sha256` inventories the delivered report/scripts/receipts, excluding disposable Git stores and itself.

## Reviewer-owned coverage ledger

| Lens | Covering round | Exact head |
|---|---|---|
| Conformance: CLEAN | R243-1 | df53dfa116b34816db0193230ad9833e67bf46dd |
| RTL: CLEAN | R243-1 | df53dfa116b34816db0193230ad9833e67bf46dd |
| Robustness: CLEAN | R243-1 | df53dfa116b34816db0193230ad9833e67bf46dd |
| Tests: CLEAN | R243-1 | df53dfa116b34816db0193230ad9833e67bf46dd |
| Docs: CLEAN | R243-1 | df53dfa116b34816db0193230ad9833e67bf46dd |

This ledger is authored by R243. No finding was deferred to another issue to obtain coverage. It covers the exact reviewed source and must be reconsidered if an artifact within a lens's scope changes.

## Pending manager gates and final integrity

This source verdict does not complete AC4 or authorize merge. The other independent review, actual trusted local-replica invocation/results, required hosted contexts, final validation against the live queue base, authorized merge, post-merge containment/checks, and Issue/Project completion remain manager duties. Hosted inspection was DEFERRED and was not queried through run/check APIs, rollups or CLI checks. Pending hosted evidence does not alter this source-code verdict.

The published full local source evidence was constructed against `52711029f374650dc93830d5ea28e81cb5c8f410`. The public record already identifies later dev advancement. It cannot serve as validation of an unconstructed later candidate. Final queue validation must identify its own base/head/tree; no earlier result is relabeled here.

Final reviewer integrity is recorded in `final-integrity-data.json`: exact source HEAD/tree, stage-0 index entries, every root blob/kind/mode, and registered required-submodule heads/index/blob/kind/mode match. The unused optional `external` gitlink remains unchanged and uninitialized, as allowed by CONTRIBUTING. Required pins: protocol-processor `424c688fa2205b934a7689a58f2aa766420f2326`; gPTP `c1b617435824929a790739ea8585c3fe1a328cc0`; verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. Final PR metadata is stored separately using only authorized fields.

R243-1 FINISHED
