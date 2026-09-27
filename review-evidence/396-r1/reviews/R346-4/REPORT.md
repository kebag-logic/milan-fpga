[R346] POSITIVE - exact head 10a5bf59a6a73e9b6487d9ea6f42669ce142ae25

# R346-4 composition review: issue #396 / PR #586 merge-train candidate

- **Role:** the lane's internal independent reviewer, cleared context, round R346-4, composition acceptance.
- **Exact candidate head:** `10a5bf59a6a73e9b6487d9ea6f42669ce142ae25`, tree `747d5ea4b35f449454034d190257b2a67c7a9ab4`. This is the merge commit "Validate issue 396 merge-train candidate".
  - First parent: `a054172abc5c1b6bce5d4c3f06830b603f37b157`, the #587 train candidate.
  - Second parent: PR #586 source head `07f72ad640f99c43bc1354642ad4d7ed8ba410cc`, source base `ac18b50968b12efe4d15c0a06301264b35656b31`.
- **Order of reading:**
  1. AGENTS.md, CONTRIBUTING.md sections 2.1 (steps 5-7) and 3, and docs/README.md.
  2. The #396 issue body, the owner decision (5789765788) and the manager decisions 5854692245, 5854930205, 5855515133, 5855792297 and 5856062292.
  3. REQ-VER-06, TESTING.md 6b/6d, and the saved-state design pages that #502 changed.
  4. `git diff a054172a..10a5bf59` and the history.
  5. The public evidence tree at `4949b127` and the hosted check runs.
- **Prior public review findings on this PR** were read only after the pass, the verdict and the ledger below were drafted. Nothing in them changed the verdict.

## Verdict basis

The composed tree adds no defect beyond the reviewed sources. Each of the manager's four decisive questions was answered by execution on the candidate.

**Composition shape: a clean additive merge on both sides** (`receipts/patch_equivalence.txt`).
- The PR delta `ac18b509..07f72ad6` and the candidate delta `a054172a..10a5bf59` are identical, apart from hunk offsets and index lines. Both cover the same 8 files, +1746/-9.
- The predecessor delta `ac18b509..a054172a` and `07f72ad6..10a5bf59` are also identical in the same sense. Both cover 44 files, +4886/-353.
- Neither side altered the other's patch.

**Shared files: one.** It is `docs/testing/TESTING.md`.
- Of the files the PR changes, only this one is also in the predecessor delta. That delta covers 44 files; the PR covers 8.
- The predecessor change to this file is exactly one added table row: #502's `pending-mutant` row at `docs/testing/TESTING.md:268`. It came in through `220c9d56` and the `f80525e6` / `de4862cb` candidate merges.
- The PR's change to this file is one hunk that inserts 216 lines at `:839`. It starts with **Standing release campaigns** at `:842`, inside `## 6d` at `:824`.
- Between the source head and the candidate, TESTING.md differs by that single #502 row and nothing else (`receipts/testing_md_source_vs_candidate.diff`).
- These PR files are blob-identical at the source head and the candidate: `REQUIREMENTS.md`, `CONTRIBUTING.md`, `tb/tools/torture_campaign.py`, `tb/tools/torture_release_mutants.py`, `tests/features/torture_campaign_plan.feature`, `tests/steps/torture_plan_steps.py` and `tests/steps/torture_release_steps.py` (`receipts/probes/SUMMARY.txt`).
- The predecessors do not touch `REQUIREMENTS.md`, `CONTRIBUTING.md`, `tb/tools/` or `tests/`.

**(1) The composed TESTING.md is internally consistent.**
- The #502 row appears exactly once (`:268`). The #396 **Standing release campaigns** block appears exactly once (`:842`).
- `gen_toc.py --check` returns rc 0. `gen_toc.py --verify-anchors` returns rc 0, with 184 cross-page fragment links reproduced.
- `check_doc_paths.py` returns rc 0: 849 cited paths resolve, 1 is allowlisted, and there are 0 line anchors. The PR adds no `file:line` citation that a predecessor's line shift could make stale.
- **Anchor probes: the gates are live on this tree** (`receipts/probes/A*`). Renaming any of these three headings was caught by both `--verify-anchors` and `--check`, which each returned rc 1:
  - the `6d` heading, which the PR links from CONTRIBUTING.md and REQUIREMENTS.md;
  - the `6b` heading;
  - REQUIREMENTS `## 8.`, which is also linked from `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md`.
- `docs_check.py` alone does not catch these renames (rc 0). It is not the anchor gate.

**(2) No stale saved-state statement after #502.**
- The PR states the persisted inventory is "today the stream binding" in three places:
  - REQUIREMENTS.md:283 "Currently that list contains stream binding";
  - TESTING.md:871-872;
  - the planner default `persisted_items = ("stream_binding",)` at `tb/tools/torture_campaign.py:3336`.
- On the composed tree, #502's pages still say only binding records reach the store and no other group has a record writer (`receipts/saved_state_inventory_candidate.txt`):
  - `docs/design/SAVED_STATE_FASTCONNECT.md:1376`, `:1393-1396`;
  - `SAVED_STATE_MATERIALIZATION.md:127`, `:240`;
  - `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:992`, `:1750`.
- #502 changed when pending is raised (on accepted name writes and actual map writes). It did not add a persisted item, and it did not change what a journal commit contains.
- The PR's persistence, journal and snapshot statements (`receipts/persistence_mentions.txt`) do not refer to the pending bit or to commit marks. The `KNOWN-PENDING` it names is a verdict class, not the saved-state pending bit.
- No statement is stale.

**(3) The planner self-test and plan feature pass on the candidate** (`receipts/gates/`).
- `torture_campaign.py --self-test`: 54 tests OK.
- `torture_release_mutants.py`: 25/25 killed by named tests; source unchanged.
- Plan feature: 86 scenarios / 353 steps, 0 skipped.
- The `@torture` tier: 231 scenarios / 898 steps.
- The exact 6d `--plan` command with explicit descriptor-shaped topologies emits `release_eligible: true`, `topology_explicit: true`, `persisted_items: ["stream_binding"]` and `restore_bound_s: 30` in every repeat.
- `--coverage-by-area` reports no missing coverage, both with the explicit topologies and with the defaults.
- The source head and the candidate give the same self-test count and scenario count. They also emit a byte-identical default plan JSON (`receipts/probes/cmp_*`).

**(4) Documentation and CI-contract gates pass on the candidate.** Every row returned rc 0:

| Gate | Result on the candidate |
|---|---|
| `docs_check.py` | 0 findings |
| `docs_check.py --selftest` | Passed |
| `check_doc_paths.py` | Passed |
| `gen_toc.py --check` and `--verify-anchors` | Passed |
| `check_em_dash.py --base a054172a` (the parent) | 0 findings over 308 added lines, 339/339 arms |
| `check_em_dash.py --base ac18b509` | Passed |
| `check_em_dash.py --selftest` | Passed |
| `check_doc_style.py` | Passed |
| `check_py_idiom.py` | No ratchet increase |
| `check_feature_status.py` and its `--self-test` | 46/46 |
| `ci_events.py --check` | 1655 items |
| `ci_events.py --selftest` | 2206 arms |
| `git diff --check` against the parent and against the source base | Clean |

- The pinned Markdown renderer was installed with `--require-hashes` from `tools/markdown/requirements.txt` into a disposable environment.

**Other semantic interactions checked.**
- #573 (builder refusals) and #587 (baseline docs) share no file, registry, table, anchor or pin with #396.
- Live dev `9e9954e9` has tree `34b561f9`, equal to the #573 train step `329c86ed`. The candidate is therefore exactly live dev plus #587 plus #396.
- The one HDL file the PR cites, `hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv`, is untouched by every predecessor.
- The planner reads no repository file, so predecessor data changes cannot reach it. Its only imports are the standard library.
- No gitlink changes in the PR.

**Delta since the lane's last internal positive.** R346-3 was POSITIVE at `8153576a`. `54d9beea` and `07f72ad6` then changed the `tu` oracle, its texts and its tests. Because coverage is banked per commit, this round applied all five lenses to `8153576a..07f72ad6` at this head:
- `check_release_tu` (`tb/tools/torture_campaign.py:3536-3563`) matches decisions 5855792297 and 5856062292:
  - the containment window is `[observed_start - resolution, clear)`, with an inclusive start and an exclusive clear;
  - the anchor is `max` of the contained events;
  - the deadline is last + 0.5 s + resolution.
- Incomplete, non-finite, bool, negative or unordered input returns SKIP, never PASS.
- REQUIREMENTS.md:262-277, the TESTING 6d row and prose, the assertion text and the emitted `tu_*` arguments state the same rule.
- Four independent disposable mutants of the oracle were each killed by the planner self-test (`receipts/probes/M*`):
  - capture completeness ignored;
  - strict `<` at the deadline;
  - non-finite accepted;
  - bool accepted via `isinstance`.
- The executor's 25 controls are all killed (above).

## Findings

No BLOCKER, MAJOR, MINOR or SUGGESTION is raised by this round.

## Prior public findings on this PR at this head

I read these after the verdict and ledger were drafted. The #396 files are blob-identical to `07f72ad6`, except TESTING.md, which differs only by the #502 row. So each state below carries onto the candidate.

**Closed findings (R346-1 to R347-4):**
- R346-1 F1 (MAJOR) and F2-F4: closed at R346-2/R346-3.
- R346-2 R2-F1 and R2-F2: closed at R346-3.
  - The restore-eligibility mutants and `test_release_eligibility_boundaries` are killed or green here.
  - `test_release_topology_each_key` is green here.
- R347-1 F1-F4, R347-2 F1-F4 and R347-3 F1: closed.
- R347-4 F1: closed at R347-5. The start-edge mutants are killed here (`receipts/gates/torture_release_mutants.log`).

**Retained suggestions (all optional; the composition changes none of them):**
- R347-5 S1: pre-first-event `tu` duration unbounded, by decision, and disclosed at TESTING 6d.
- R347-5 S2: float knife-edge at exactly 1x lag.
- R346-3 S1: no numeric resolution ceiling.
- R346-3 S4: boot-time figures.
- R346-3 S5: stale round labels.
- R346-1 S3: a malformed `--dut` still raises a traceback with rc 1 (`receipts/malformed_dut.log`).

**No public finding at MINOR or above is open on this PR at this head.**

## Clean results per lens (reviewer-applied, exact head 10a5bf59)

```text
[R346] PASS Conformance - REQUIREMENTS.md:250-334, docs/testing/TESTING.md:842-872, tb/tools/torture_campaign.py:3325,3336,3536-3563, docs/design/SAVED_STATE_FASTCONNECT.md:1376-1396 at 10a5bf59 - REQ-VER-06 binding-only inventory still true after #502 (no new persisted item, no new record writer); tu oracle matches decisions 5855792297/5856062292; 6d plan command emits release_eligible true with explicit topology (receipts/gates/torture_plan_6d.log, receipts/saved_state_inventory_candidate.txt)
[R346] PASS RTL - PR diff a054172a..10a5bf59 (8 files, no hdl/, firmware, builder or gitlink path) and hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv untouched by ac18b509..a054172a at 10a5bf59 - composition adds no RTL; predecessor RTL (#502 KL_pp_shadow/milan_datapath) is not read by or cited in the #396 artifacts (receipts/patch_equivalence.txt)
[R346] PASS Robustness - tb/tools/torture_campaign.py:3536-3563 SKIP/boundary arms and mutants M1-M4 at 10a5bf59 - incomplete, non-finite, bool, negative and unordered input cannot PASS; deadline equality is inclusive; planner is stdlib-only and reads no repository file, so predecessor data cannot perturb it (receipts/probes/SUMMARY.txt)
[R346] PASS Tests - tb/tools/torture_campaign.py self-test (54), tb/tools/torture_release_mutants.py (25/25), tests/features/torture_campaign_plan.feature (86/353), @torture tier (231/898) at 10a5bf59 - identical counts and byte-identical default plan to source head 07f72ad6; four independent oracle mutants killed by named tests (receipts/gates/, receipts/probes/)
[R346] PASS Docs - docs/testing/TESTING.md:268,824,842 (#502 row and #396 block each exactly once), CONTRIBUTING.md:418, REQUIREMENTS.md:250,333 at 10a5bf59 - docs_check, check_doc_paths, gen_toc --check/--verify-anchors (184), check_em_dash --base parent (0/308, 339/339 arms), doc_style, ci_events --check/--selftest all rc 0; anchor-rename probes A1-A3 caught (receipts/gates/, receipts/probes/A*)
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Composition touches scope? | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|---|
| Conformance | CLEAN | Yes, question (2): the saved-state inventory after #502 | REQ-VER-06 (REQUIREMENTS.md:250-334); TESTING.md:842-872; planner:3325, :3336, :3536-3563; saved-state pages as composed | R346-4 | `10a5bf59a6a73e9b6487d9ea6f42669ce142ae25` |
| RTL | CLEAN | No: no RTL in the PR; no predecessor RTL read or cited | patch equivalence; PR path scope; `KL_ptp_clock_validity.sv` unchanged | R346-4, with source cover from R347-5 | `10a5bf59a6a73e9b6487d9ea6f42669ce142ae25` (R347-5: `07f72ad6`) |
| Robustness | CLEAN | No: planner blobs are identical to the source | `check_release_tu` arms; mutants M1-M4 | R346-4, with source cover from R347-5 | `10a5bf59a6a73e9b6487d9ea6f42669ce142ae25` (R347-5: `07f72ad6`) |
| Tests | CLEAN | No: test blobs are identical; results rerun on the candidate | self-test; release mutants; plan feature; `@torture` tier; source-versus-candidate comparison | R346-4, with source cover from R347-5 | `10a5bf59a6a73e9b6487d9ea6f42669ce142ae25` (R347-5: `07f72ad6`) |
| Docs | CLEAN | Yes: TESTING.md is shared with #502 | composed TESTING.md; the anchors; the docs, TOC, em-dash, path, style and CI-contract gates; probes A1-A3 | R346-4 | `10a5bf59a6a73e9b6487d9ea6f42669ce142ae25` |

- All five lenses are banked at the candidate head itself.
- For the three lenses the composition does not touch, the source review R347-5 is POSITIVE at `07f72ad6`, and every artifact in those lenses' scope is blob-identical between `07f72ad6` and this head.
- The earlier internal positive, R346-3 at `8153576a`, is superseded for every lens by this round. `54d9beea..07f72ad6` changed Conformance, Robustness, Tests and Docs artifacts after it.

## Real limits

- **Desk review only.** Physical calibration NOT RUN. Acceptance items 3 and 4 remain open: the seven-day soak, the 200 cold cuts, the #366 or persistence-disabled negative control, and the retained bench evidence. Field skips are not hardware proof.
- **Banks not run.** I did not run the full parent, PP, gPTP, Yosys or builder banks, and did not use Docker, act or the host replica, because none of these was allowed.
  - Verilator was not used, because nothing in #396 is RTL. The composition's RTL changes belong to the predecessors and are covered by their banks.
- **Public evidence tree.** The tree linked for this round (`4949b127`, `review-evidence/396-r1`) contains only round-1 author gate logs at `b7b74b8b`. It holds no receipts for the manager's source or candidate banks at this head, so this round could not inspect them.
- **Hosted evidence.** The candidate commit is not on the remote; the API reports no commit for `10a5bf59`, so it has no hosted runs. For the source head `07f72ad6`, every executed context completed with success:
  - `rtl-fast`, `verilator-suites`, `yosys-portability` and `full-ci-gate`;
  - docs, BDD, lint and elaboration;
  - Verilator shards 0-4 and Yosys shards 0-3.
  - `Physical gPTP (nightly and manual)` was **skipped**, not executed.
- **Oracle only.** The bench runner that feeds `check_release_tu` lives outside this repository and was not reviewed.
- **Provisional bound.** `RELEASE_RESTORE_BOUND_S = 30` remains provisional.

## Pending manager duties

- **Final candidate.** Build and validate the final current-dev candidate at the merge turn: source base `a054172a`, live dev `9e9954e9`. Rerun the composition gates above if dev moves.
- **Candidate banks.** Run the candidate banks, and publish their receipts where a cold reviewer can open them.
- **Hosted and act acceptance.** The manager owns this.
- **Provisional values.** Ratify `RELEASE_RESTORE_BOUND_S` from the #397 and #75 measurements. Decide whether to take any retained suggestion.
- **Bench items.** Keep acceptance items 3 and 4 open until bench evidence exists.
- **Merge.** Obtain explicit maintainer authorization before merging, then run post-merge containment.

## Reproduction

The scripts are in this packet.

- `run_gates.sh <clone> <python-with-pinned-markdown-deps> <receipt-dir>` runs every gate above.
- `probes.sh <clone> <python> <scratch> <receipt-dir>` makes a throwaway local clone and runs:
  - anchor probes A1-A3;
  - oracle mutants M1-M4;
  - the source-versus-candidate comparison and the blob-identity checks.
- `clone_integrity.sh <clone>` checked the review clone after all probes (`receipts/clone_integrity.log`):
  - HEAD and tree are exact.
  - Status is clean, with untracked and ignored files included.
  - The index equals HEAD's tree.
  - All 930 tracked blobs and symlinks rehash to their recorded ids and modes.
  - The gitlinks `gptp-processor` `5dce647a`, `protocol-processor` `870ff88a` and `third_party/verilog-axis` `48ff7a7e` are checked out at their recorded commits. `external` `efeb541a` is recorded but not initialized.

R346-4 FINISHED
