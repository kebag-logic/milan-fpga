[R424] POSITIVE - exact head e5ad118783c2ff96e13f1d794f10bf2b63741282

Round R424-5, internal cleared-context independent review of PR #628 (issue #117, bench lane B5, acceptance box 4, the audio continuity row).

- **Head:** `e5ad118783c2ff96e13f1d794f10bf2b63741282`, tree `d79bb19b5e635b1f8bbc458e5c05c1e7e19afa9b`.
- **Source base:** dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`.
- **Round 5:** one docs-only commit on the round 4 head `e216dfe4`, touching `docs/findings/117_AUDIO_CONTINUITY.md` only (+23 -12). The PR as a whole changes that page and its index row in `docs/findings/README.md`, and nothing else.

## Verdict basis

No BLOCKER, MAJOR or MINOR is open at this head, and all five lenses are CLEAN. Two SUGGESTIONs are recorded below. Neither affects coverage.

What I confirmed at this head:

- **Round 4 findings.** Every round 4 MINOR from both reviewers is resolved, or its archive side is answered by the round 5 rulings. The page and the PR text comply with those rulings.
- **Reproduction.** I used only the three packet directories at the new pin `9006c78e`. Step 1 restores the read record to `2183d57f…` (131,540 bytes). Steps 2 and 3 reproduce `attribution.txt` and `round3_figures.txt` byte for byte, with rc 0 and empty stderr.
- **Manifest and hashes.** All 207 files match their manifest `published_sha256`. All 20 SHA-256 values on the page resolve, with 0 problems.
- **Tables.** 14 of the 15 tables are byte-identical to round 4. The Artifact table differs only in the three every-channel Bytes cells. Measurement tables 2 to 12 are byte-identical to round 1.
- **Gates.** The documentation gates are rc 0, 15 of 15, in the pinned Markdown environment.

I wrote my provisional verdict and ledger to `receipts/verdict_ledger_before_prior_findings.txt` after my own pass over the diff, and only then read the round 4 review reports.

## Reconstruction

I read the sources in this order:

1. AGENTS.md and CONTRIBUTING.md: section 6 (wording and privacy), section 6.1 (the em-dash gate) and the docs workflow's gate list.
2. `docs/README.md` and `docs/findings/README.md`.
3. Issue #117: its body and acceptance box 4.
4. The manager comments on #117:
   - the B5 assignment, 5925737609;
   - the round 2 to round 5 assignments, 5926598386, 5927406852, 5928569912 and 5929901339;
   - the stream-count ruling, 5929406675;
   - the round 5 REVIEW READY, 5930172204.
5. The manager's archive comments on PR #628, 5927406516 and 5928569576.
6. `.github/PULL_REQUEST_TEMPLATE.md` and the live PR body (head `e5ad1187`, read through the API).
7. `git diff e4b771f9..e5ad1187`, `git diff e216dfe4..e5ad1187` and the six commit messages.
8. The evidence archive branch `b5-review-evidence`:
   - the pin `9006c78e`;
   - `8e6be432`, `2be652c3` and the tip `6e6a08fa`;
   - `ef3a7091`, the starting point the assignment named;
   - the round 5 packet `author-r5/` at the tip, scanned only.
9. The page's own code and design citations in the repository.

## Findings

### R424-5-S1 - SUGGESTION - Docs - `docs/findings/117_AUDIO_CONTINUITY.md:461-463` (archive pin `9006c78e`)

- **What the page says.** It pins `9006c78e` and links that commit's `review-evidence/b5-r1` tree.
- **Evidence** (`receipts/archive_size_scan.txt`):
  - At `9006c78e`, the linked tree still carries the `diag1` every-channel capture size in two receipts outside the three cited directories:
    - `author-r4/receipts/raw_index_check.txt`;
    - `reviews/R424-4/receipts/hash_check.txt`, this reviewer's own round 4 receipt.
  - The archive commit `2be652c3` masks both. At `2be652c3` and at the tip `6e6a08fa` there are 0 hits.
  - The three packet directories are identical at `9006c78e`, `2be652c3` and the tip. `git diff --quiet` gives rc 0, and the subtree ids are equal: `5edd0801`, `aec1d690` and `00cd3bee`.
  - The manifest entries for the three directories are also unchanged. Only the two masked receipts' entries differ.
- **Why it is not a MINOR:**
  - Neither the page nor the PR text carries the value.
  - The round 5 assignment named `9006c78e` as the pin.
  - The owner's top-only decision of 2026-10-01 lets older archive and branch commits keep what they had. The PR's own commits `bf9e5d82` to `e216dfe4` still show all three sizes on the page, so the pinned tree adds no new exposure.
  - The PR body's Round 4 section says that the sizes were kept at `8e6be432`. That is a statement of history and carries no value.
- **Suggested outcome**, either one:
  - Re-pin the page to `2be652c3` or a later tip, changing only the hash and the link. The steps and every cited hash stay valid, because the three directories are byte-identical there.
  - Or the manager records that the `9006c78e` pin is accepted under the top-only decision.
- **Verification.** Re-run `scripts/archive_size_scan.py` on the new pin, expecting 0 hits. Then re-run `scripts/reproduce_pinned.sh` on that pin.

### R424-5-S2 - SUGGESTION - Docs - PR #628 body, Status and Definition of Done ("12 of 12" local gates)

- **What the body says.** The Status line and the third Definition of Done box cite 12 gates, rc 0. The Status line points to How to validate for them.
- **Evidence.** How to validate lists 10 gate commands. The other two are the `git diff --check` runs against `e4b771f9` and `e216dfe4`, which the round 5 REVIEW READY counts. Those two are not in the body.
- **Impact.** A cold reader can reproduce 10 of the 12 gates the body claims. All 12 pass (`receipts/gates.txt` covers them).
- **Suggested outcome.** List the two extra `git diff --check` commands, or state the count as 10.

## Round 4 findings at this head

| Finding | State at `e5ad1187` | Evidence |
|---|---|---|
| R424-4 F1 = R425-4 F3 (MINOR, Docs and Tests): the page said both tools read the masked `events.jsonl` | RESOLVED | `:521-523` now say that, of the lane packet's masked files, the tools read only the `a-long` `summary.json`. The PR body's Round 4 item 1 says the same, marked "(corrected in round 5)". I traced both `figures` commands at `9006c78e` with an openat trace (`receipts/reproduce_pinned_9006c78e.txt`). `b5_attrib.py` opens `a-long-reads.json`, `a-long-reads.u16`, `summary/a-long/summary.json` and `summary/a-long/continuity-events.csv`. `b5_round3.py` opens the same files and `restore/peer-descs-2.jsonl`. Of these, the only `path_redacted` file in the lane packet is `summary.json`; the read-record copy is the one step 1 replaces. Neither tool opens `events.jsonl`, `console.txt`, `HANDOFF.md`, `RAW-ARTIFACTS.json` or `host-*.txt`. |
| R425-4 F1 (MINOR, Conformance and Docs): the capture's channel count follows from the byte sizes | RESOLVED on the page and in the PR text; archive side at tip `2be652c3` | The three Bytes cells read `withheld` (`:493`, `:495`, `:498`), and their SHA-256 values are unchanged. `:470-472` and `:524-526` now match. The withheld-value scan (`receipts/size_scan.txt`) derives the sizes and the channel count in memory and never prints them. Its control hits the three rows of the round 4 page. At the head it finds 0 hits on the page, the index row, the PR body and the six commit messages. There is no unit-form size (`receipts/unit_size_scan.txt`). The one whole-multiple match, `:496`, is the two-channel `cap-test1` pair, and no stated duration divides it to the count. The masked `RAW-ARTIFACTS.json` at the pin keeps 19 of 19 SHA-256 values and withholds exactly the 4 every-channel sizes (`receipts/raw_index_sha_census.txt`, `raw_index_check.txt`). The residual in the pinned tree is S1. |
| R425-4 F2 (MINOR, archive) and R424-4 S2 (archive residuals) | ANSWERED by ruling 5929901339 items 2 and 3; page and PR text comply | `receipts/public_scan.txt` and `public_scan_hit_classification.txt` find no count of the peer's streams, stream ports, stream states or clusters on the page, the index row, the PR body or the commit messages. The count hits are clusters of analysis skips, or the round 4 subject "without counts". The format channel counts stay at `:102-103` and `:411-412`, under ruling item 1. The peer's clock-source selection stays at `:89`, `:306` and `:438`, under ruling 5929406675 item 2. |
| R425-4 F4 (MINOR, Docs): the PR body did not use the template | RESOLVED | The live body has the template's first line form (`[A472] …`), Contents, Status, Linked Issue / roles (Executor, Internal cleared-context reviewer, External reviewer), Description, Authoritative references, How to get into the same state, How to validate with expected results, Known limitations / out of scope, and Definition of Done. The round sections sit in between. It says "Refs #117" and "Relates to #117", and a closing-keyword scan finds nothing. The Contents anchors resolve, 13 of 13 (`receipts/anchor_check_pr_body.txt`). One count mismatch is S2. |
| R424-4 S1 = R425-4 S1 (SUGGESTION): list round 4 in the header | TAKEN | `:14-22` list round 4 ([A476], 5928569912 and the ruling 5929406675) and round 5 ([A478], 5929901339). All six cited comment ids exist on #117, and each is the kind the text says it is. |
| R425-4 S2 (SUGGESTION): name `author-r2/` and `author-r3/` `gates/gates.txt` as masked | RETAINED (not a round 5 item) | `:517-521` is scoped "In the lane packet", and its list equals that packet's `path_redacted` set. The two files are in the round 2 and round 3 packets, and the page cites no hash of either. Completeness only, so no lens is affected. |
| R424-1 S1 and its successors: forward pointers from other pages | RETAINED by the manager | Outside the lane's fixed output. |

The earlier MINORs stay resolved at this head. Their text regions did not change in round 5:

- R424-1 F1 and R425-1 F1, the attribution strength: `:33-37`, `:249-309` and `:433-452`.
- R424-1 F2, the controller revision: `:531-538`.
- R425-1 F2, the reproducibility: reproduced at the pin.
- R425-1 F3 and R425-2 F2, the Direction B reason: `:36` and `:382-397`.
- R424-2 F1 and R425-2 F1, the read record: step 1 restores `2183d57f…`.
- R424-3 F1, where the packets are: `:461-468`, re-pinned.
- R425-3 F1, the round 1 layout: masked at the archive top, and the page and PR text carry none of it.

## Lens results

```text
[R424] PASS Conformance - docs/findings/117_AUDIO_CONTINUITY.md:14-22, :33-37, :461-468, :470-472, :489-499, :511-526; PR #628 body (receipts/pr628_body.md); receipts/reproduce_pinned_9006c78e.txt, hash_check_9006c78e.txt, raw_index_check.txt, size_scan.txt, public_scan.txt - round 5 assignment items 1-5 and rulings 1-4 (#117 5929901339) against #117 box 4's continuity row: sizes withheld with hashes kept; only summary.json named and confirmed by trace; pin 9006c78e reproduces steps 1-3 from the three directories alone; 20/20 hashes resolve; template body with Refs/Relates #117 and no closing keyword; header lists rounds 4 and 5; verdicts (integrity PASS, continuity FAIL as measured, restarts PASS, Direction B NOT RUN, row FAIL as measured) unchanged and not overclaimed.
[R424] PASS RTL - git diff --name-only e4b771f9..e5ad1187 (two docs files; no HDL, firmware, script, config; four gitlinks unchanged, receipts/citation_check.txt, clone_integrity.txt); page :43-47, :220-225 against docs/design/TIME_SYNC.md:463,478 (Talker capture handoff, one whole-frame slip every 1.958 s on SLIP_TDM) and docs/reference/REGISTER_MAP.md:1837 heading (anchor used by :46); page :389-402 against avdecc/aem_descriptors.py:103,590 and avdecc/aem_assemble.py:289-294 - no RTL artifact in scope; the design and encoding facts the page rests on match the authoritative sources.
[R424] PASS Robustness - receipts/reproduce_pinned_9006c78e.txt, mutation_probe.txt, archive_size_scan.txt, raw_index_check.txt - the reproduction fails on a single flipped byte in the restored record and on the archive's masked copy (gunzip without -f), and passes when restored; the pinned packet trees are identical at 9006c78e, 2be652c3 and the tip, so the pin is stable against the later mask; the withheld-value scan catches plain and comma-grouped forms, approximate-duration division, and a planted size; every withheld index entry is an every-channel capture.
[R424] PASS Tests - receipts/size_scan.txt (control hits the three round-4 rows), mutation_probe.txt (P1, P2, P3 cross-page link, P4 planted size), public_scan.txt (7/7 planted controls), table_proof.txt, restart_stats.txt - each check this round relies on was shown able to fail; restart distribution re-derives from the page's cycle table (min 0.0262, median 0.0279, nearest-rank p95 0.0389 at cycle 20, linear 0.0344, max 0.1358, 30/30 under 1 s; slope and interval within rounding of the printed cycle values).
[R424] PASS Docs - docs/findings/117_AUDIO_CONTINUITY.md (all 552 lines), docs/findings/README.md index row, PR body, six commit messages; receipts/gates.txt (15/15 rc 0), table_proof.txt, anchor_check.txt (17/17 intra-page links), public_scan_hit_classification.txt - gates clean in the pinned Markdown environment; 14/15 tables byte-identical to round 4, the Artifact table differing only in three Bytes cells; tables 2-12 and 15 byte-identical to round 1; no host, peer, switch or instrument name, wiring, channel map, peer stream count, capture layout or clock topology; one-line commit, no trailers. S1 and S2 are SUGGESTION only.
```

### Table proof (`receipts/table_proof.txt`)

The page has 15 tables and 119 table lines at both heads.

- **Against `e216dfe4`:** 14 tables are byte-identical. Table 14, Artifact, changes only the Bytes column of the three every-channel rows.
- **Against round 1 `bf9e5d82`:** tables 2 to 12 and table 15 are byte-identical. Three tables differ, each by cells that earlier rounds accounted for:
  - table 1: the Evidence cells changed in rounds 2 to 4;
  - table 13: the Restore stream-state cell, changed under the round 4 ruling;
  - table 14: the three Bytes cells changed in round 5.
- **Every measurement table is unchanged since round 1:** identity, binding, stream format, runs, binding rule record, the two integrity tables, continuity, restart distribution, slope and the per-cycle table.

### Gates (`receipts/gates.txt`)

All ran at the exact head, in the pinned Markdown environment, and all exited rc 0:

- `docs_check.py`, with 0 findings over 182 md files and 953 scrubbed files;
- `check_doc_style.py` and its `--selftest`;
- `gen_toc.py --check`, `--verify-anchors` and `--selftest`;
- `check_em_dash.py --base e4b771f9`, with 0 findings over 553 added lines, and its `--selftest`;
- `check_doc_paths.py`;
- `check_feature_status.py` and its `--self-test`;
- `check_baremetal_only.py --check`;
- `ci_scope.py --selftest`;
- `git diff --check` against `e4b771f9` and against `e216dfe4`.

The worktree was clean afterwards.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Page `:14-37`, `:461-526`; PR body; #117 box 4; round 5 assignment and rulings, stream-count ruling; `reproduce_pinned_9006c78e.txt`, `hash_check_9006c78e.txt`, `raw_index_check.txt`, `size_scan.txt`, `public_scan.txt` | R424-5 | `e5ad118783c2ff96e13f1d794f10bf2b63741282` |
| RTL | CLEAN | Diff name list (docs only), gitlinks; `TIME_SYNC.md:463,478`; `REGISTER_MAP.md:1837`; `aem_descriptors.py:103,590`; `aem_assemble.py:289-294`; `citation_check.txt` | R424-5 | `e5ad118783c2ff96e13f1d794f10bf2b63741282` |
| Robustness | CLEAN | `reproduce_pinned_9006c78e.txt`, `mutation_probe.txt` (P1, P2), `archive_size_scan.txt`, packet subtree identity across `9006c78e`, `2be652c3` and the tip, `raw_index_check.txt` | R424-5 | `e5ad118783c2ff96e13f1d794f10bf2b63741282` |
| Tests | CLEAN | `size_scan.txt` control, `mutation_probe.txt` (P1-P4), `public_scan.txt` controls, `table_proof.txt`, `restart_stats.txt` | R424-5 | `e5ad118783c2ff96e13f1d794f10bf2b63741282` |
| Docs | CLEAN (S1, S2 are SUGGESTION) | Page (552 lines), index row, PR body, commit messages; `gates.txt`, `table_proof.txt`, `anchor_check.txt`, `anchor_check_pr_body.txt`, `public_scan_hit_classification.txt` | R424-5 | `e5ad118783c2ff96e13f1d794f10bf2b63741282` |

## Limits

- **Docs-only head.** No RTL, simulation, Verilator or Yosys was run, and no full bank. The scoped Verilator was not needed and was not used, so its identity was not checked.
- **Raw captures are not public.** I did not re-derive the figures that need them: the whole-run integrity counts, the zero-frame ordinals, and the `derive` and `wholerun` modes. They rest on the raw-artifact hashes at the pin and on the earlier rounds.
- **The scans' coverage.** The public-text scan is pattern-based, and every rule fires on a planted control. Its name lists are stored encoded. The withheld-value scan covers only the values it derives from the round 4 page. No scan proves the absence of private text.
- **A gate limit, not a finding against this head.** Probe P3 shows that `docs_check.py` and `gen_toc.py --verify-anchors` do not reject a broken intra-page anchor: rc 0 with `#artifact-hashes` rewritten to a missing fragment. I checked the page's 17 intra-page links and the PR body's 13 separately, and all resolve. Whether to track the limit is the manager's call.
- **Hosted checks** (`receipts/hosted_check_runs.txt`, read 2026-10-01T11:27:54Z):
  - Succeeded: `rtl-fast`, `changes`, `bdd-conformance`, `docs-check-no-git`, `elaborate`, `full-ci-gate` and `wire-accountability`.
  - Still in progress: `docs-check`.
  - Skipped by scope: the `verilator-*`, `yosys-*` and physical gPTP contexts. A skipped context is not a result.
  - No act replica was run.
- **Not hardware proof.** Physical calibration was NOT RUN, and Direction B was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- **S1:** re-pin to `2be652c3` or later, or record that `9006c78e` is accepted under the top-only decision.
- **S2:** optional, one line in the PR body.
- **Hosted acceptance:** hosted `docs-check` completion, and the hosted and act acceptance at the exact head.
- **The final current-dev candidate at the merge turn.** A scratch `git merge-tree` of the head into live dev `ea3fb388` merges with no conflict, giving tree `84d57ec2` (`receipts/merge_tree_live_dev.txt`). Since the base, live dev touches `docs/findings/README.md` and adds one findings page. No gate was run on the merged tree.
- **Retained items:** the forward pointers (R424-1 S1 and its successors) and R425-4 S2.
- **Merge:** it still requires the external positive review and the full completion bar.

## Receipts

Every published receipt is listed in `MANIFEST.sha256`. The scripts are under `scripts/`, take their inputs as arguments, and print labels and line numbers, never withheld values:

- `reproduce_pinned.sh`: steps 1 to 3 from the pin, the manifest check and the open trace.
- `hash_check.py`: resolves every SHA-256 on the page.
- `raw_index_check.py`: checks the artifact table against the raw index.
- `size_scan.py` and `archive_size_scan.py`: the withheld-value scans.
- `public_scan.py`: the public-text scan.
- `table_proof.py`: table identity across heads. It never prints old cell text.
- `restart_stats.py`: re-derives the restart statistics.
- `anchor_check.py`: checks intra-page links.
- `mutation_probe.sh`: the probes.
- `run_gates.sh`: the documentation gates.

`receipts/clone_integrity.txt` records the state of the review clone after all probes:

- HEAD is `e5ad1187` with tree `d79bb19b`;
- 0 status entries, and the index tree equals the HEAD tree;
- 977 of 977 tracked blobs are byte-equal to their index entries, and the modes are unchanged;
- all four gitlinks equal HEAD.

All probes ran on scratch copies.

R424-5 FINISHED
