[R425] POSITIVE - exact head e5ad118783c2ff96e13f1d794f10bf2b63741282

Round R425-5, external independent review of PR #628: issue #117, bench lane
B5, acceptance box 4, the audio continuity row.

- **Head:** `e5ad118783c2ff96e13f1d794f10bf2b63741282`, tree
  `d79bb19b5e635b1f8bbc458e5c05c1e7e19afa9b`. One docs-only commit on the
  round-4 head `e216dfe4`, `docs/findings/117_AUDIO_CONTINUITY.md` only
  (+23 -12).
- **Source base:** dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`. Live dev is
  `ea3fb38877842f223afea97e3bd72a10500455c9`; the candidate merge is the
  manager's.
- **Order:** context was rebuilt from AGENTS.md, CONTRIBUTING.md, the issue
  body, the B5 assignment, the round 2 to 5 assignments and rulings
  (#117 5925737609, 5926598386, 5927406852, 5928569912, 5929406675,
  5929901339), the diff, the history and the public archive. The independent
  pass over the diff and evidence was finished before any prior review
  finding was read.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR is open at this head. Three
SUGGESTIONs follow; they affect no lens.

- R425-4 F1 (the capture's channel count followed from the page's byte sizes)
  is resolved on the page, in the PR body, the index row and the commit
  message, and at the archive tip.
- R425-4 F3 = R424-4 F1 (which masked input the reproduction reads) is
  resolved, and the trace agrees with the page.
- R425-4 F4 (PR template) is resolved.
- R424-4 S1 (rounds 4 and 5 in the header) is taken.
- R425-4 F2 and R424-4 S2 are answered by the round 5 archive ruling. The page
  and the PR text comply with it.
- 14 of 15 tables are byte-identical to round 4. The 15th, the Artifact hashes
  table, differs only in three Bytes cells. Every measurement table is
  unchanged since round 1.
- The twelve docs gates are rc 0 at the head.

## Findings

### S1 SUGGESTION: the page's archive link lands on a tree that still carries one withheld size

- **Lenses:** Docs, Conformance.
- **Where:** `docs/findings/117_AUDIO_CONTINUITY.md:461-463`, the pin
  `9006c78e354d5a2f244fd606c55790a825304bd3` and its tree link to
  `review-evidence/b5-r1`.
- **Authority:** round 5 ruling 4 (#117 5929901339) masks the every-channel
  capture sizes in the archive. The manager's later archive commit `2be652c3`
  ("Mask the remaining diag1 capture size in two receipts") shows that intent
  reaches the two receipts below.
- **Evidence:** `receipts/archive_scan.txt`.
  - At `9006c78e`, two lines carry the `diag1` every-channel size literally:
    `author-r4/receipts/raw_index_check.txt:9` and
    `reviews/R424-4/receipts/hash_check.txt:7`. Neither is in the three
    directories the page's steps use.
  - At `2be652c3` and at the tip `6e6a08fa` there are 0 such lines, and 0
    lines from which the channel count follows by exact division.
  - At `2be652c3`, steps 1 to 3 give the same result as at `9006c78e`: 207
    files with 0 manifest mismatches, `2183d57f…` restored, and both receipts
    byte-identical (`receipts/repro_steps1-3.txt`).
- **Why it is only a SUGGESTION:**
  - The page text and the PR text comply with the ruling.
  - Under the owner's top-only decision (ruling 3), older archive commits keep
    what they had, so the value stays public in history whatever the pin.
  - The manager fixed `9006c78e` as the item 3 pin.
  - That `diag1` size does not give the channel count by exact division at the
    page's stated 25 s.
- **Optional outcome:** at the next edit of the page, re-pin to `2be652c3` or
  a later tip. The reproduction is unchanged there.
- **Verification:** `r425_5_archive_scan.py` shows A1 = 0 at the new pin, and
  `r425_5_repro.sh` reproduces both receipts there.

### S2 SUGGESTION: the PR body counts 12 gates but its validation block lists 10

- **Lenses:** Docs.
- **Where:** PR #628 body, Status ("Local gates: 12 of 12 rc 0") and the
  Definition of Done ("12 documentation gates"), against How to validate.
- **Evidence:** How to validate lists nine scripts and
  `git diff --check e4b771f9 HEAD`. The other two gates are `git diff --check`
  and `git diff --check e216dfe4 HEAD`. They appear only in the #117 REVIEW
  READY comment (5930172204). All twelve are rc 0 at the head
  (`receipts/gates.txt`).
- **Optional outcome:** list the two other commands, or state the count the
  block shows.

### S3 SUGGESTION (R425-4 S2, retained): two masked gate outputs are not named

- **Lenses:** Docs.
- **Where:** `docs/findings/117_AUDIO_CONTINUITY.md:517-521`.
- **Evidence:** `author-r2/receipts/gates/gates.txt` and
  `author-r3/receipts/gates/gates.txt` are `path_redacted` at `9006c78e`
  (`receipts/hashcheck_9006c78e.txt`). The page's list covers the lane packet,
  and it does that exactly. The page cites no hash of either file, so only
  completeness is affected. Round 5 recorded it as not taken.

## Round 4 findings and round 5 items at this head

| Finding / item | State at `e5ad1187` | Evidence |
|---|---|---|
| R425-4 F1 (MINOR, Conformance, Docs): capture channel count follows from byte sizes | RESOLVED | `:493`, `:495` and `:498` read `withheld`, and their SHA-256 values are kept. `:471-472` and `:524-526` match. `receipts/withheld_sizes.txt`: the power check on `e216dfe4` flags the three old sizes (W1 3, W2 4). The new page, PR body, index row, commit message and the A478 REVIEW READY give W1 0 and W2 0, testing every integer against every stated duration at 3 and 4 bytes per sample. Archive: `receipts/archive_scan.txt` shows 0 exact derivations at `9006c78e`, `2be652c3` and `6e6a08fa`, and 0 literal sizes from `2be652c3` on (S1). `receipts/raw_index_9006c78e.txt`: 19 of 19 entries keep SHA-256. The 4 withheld sizes are every-channel captures; 3 are the page's withheld rows, and every page size cell that is not withheld matches |
| R425-4 F3 = R424-4 F1 (MINOR, Docs, Tests): masked inputs the reproduction reads | RESOLVED | `:521-523` and the PR body's Round 4 item 1 name only the `a-long` `summary.json`. `receipts/open_trace_9006c78e.txt` (audit-hook trace): `b5_attrib.py figures` opens `a-long-reads.json`, the restored `a-long-reads.u16`, `summary/a-long/summary.json` and `continuity-events.csv`. `b5_round3.py figures` opens those and `restore/peer-descs-2.jsonl`. Of the `path_redacted` files, only `summary.json` is opened, besides the record copy that step 1 replaces. `receipts/probes.txt`: perturbing `summary.json`'s `window_time` changes `attribution.txt` (cmp 1). Appending to `events.jsonl` changes neither receipt (cmp 0) |
| Re-pin to `9006c78e` (item 3) | RESOLVED | `:461-463`. `receipts/repro_steps1-3.txt`, from the three directories at `9006c78e` alone: 207 files, 0 `published_sha256` mismatches. Step 1 restores `2183d57f…`, 131,540 bytes. Steps 2 and 3 give rc 0, empty stderr, and `attribution.txt` `18ebbfc1…` and `round3_figures.txt` `9fa0f027…` byte for byte. `receipts/hashcheck_9006c78e.txt`: all 20 distinct SHA-256 values on the page resolve, 0 unresolved. 3 are `original_sha256` of `path_redacted` files (`run_a.py`, `grade_a.py`, the read record), 7 are unmasked files whose published bytes match, and 10 are quoted in published files |
| R425-4 F4 (MINOR, Docs): PR template | RESOLVED | `receipts/pr_body_checks.txt`: the template's H2 sequence is identical, with the Round 2 to 5 sections inserted. The 12 DoD items are in template order, with honest ticks. The first line is `[A472]`. There are Executor, internal and external reviewer roles. The body says "Refs #117" and "Relates to #117" and carries no closing keyword. `closingIssuesReferences` is empty |
| R424-4 S1: rounds 4 and 5 in the header | TAKEN | `:14-22` |
| R425-4 F2 (MINOR) and R424-4 S2: peer counts in the archive | ANSWERED by ruling 2 (#117 5929901339); the page and PR text comply | `receipts/pubscan.txt`: no count of the peer's streams, stream ports, stream states or clusters on the page, the index row, the PR body or the commit message. The "clusters" hits are skip-analysis clusters, and "All 4 DUT stream states" (`:85`) is the DUT's own. The format channel counts (`:103`, `:412`) stay under ruling 1. The peer's clock-source selection (`:89-90`, `:306`) stays under ruling 5929406675 item 2 |
| R425-4 S2 | RETAINED as S3 | See S3 |
| Earlier rounds (R425-1 F1 to F3, R424-1 F1 and F2, R425-2 F1 and F2, R424-2 F1, R424-3 F1, R425-3 F1, and their suggestions) | RESOLVED or retained as before; nothing reopened | The text they concern is unchanged in round 5: the diff touches only `:14-22`, `:461-463`, `:471-472`, `:493-498` and `:518-526`. Rounds 3 and 4 confirmed them. R425-3 F1's derivation class, carried as R425-4 F1, is now resolved. The forward pointers (R424-1 S1 and successors) stay retained by the manager |

## Assigned checks

| Check | Result | Evidence |
|---|---|---|
| Table identity | 14 of 15 byte-identical to `e216dfe4`. The Artifact hashes table differs in rows 4, 6 and 9, column Bytes only. Tables 2 to 12 and 15 are identical to round 1 `bf9e5d82`. Table 14 was unchanged from round 1 to round 4. 119 table lines at every head | `receipts/tables.txt`, `receipts/tables_round1_vs_round4.txt` |
| Public text | No host, peer, switch or instrument name. No wiring, channel map, stream count, capture layout or clock topology. 12 generic pattern classes, each first hitting a planted line. All 7 hits are false positives | `receipts/pubscan.txt` |
| Docs gates | 12 of 12 rc 0, in a private environment holding the hash-pinned Markdown lock. `check_em_dash`: 0 findings over 553 added lines in 2 pages, as the PR body expects. The worktree stayed clean | `receipts/gates.txt` |
| Commit | One commit, one-line message, no trailers. Author and committer are the lane identity | `git log -1 --format=%B e5ad1187` |
| Round-5 author packet | `author-r5` at `6e6a08fa`: 35 files equal the archive `MANIFEST.json` `published_sha256`. `HANDOFF.md` and `gates/gates.txt` are `path_redacted`, which is why the packet's own `MANIFEST.sha256` differs for those two | `receipts/author_r5_manifest.txt` |
| Hosted, exact head (read only) | At 2026-10-01T11:24:10Z, 7 contexts had executed with success: `bdd-conformance`, `changes`, `docs-check-no-git`, `elaborate`, `full-ci-gate`, `rtl-fast` and `wire-accountability`. `docs-check` was in progress. 7 were skipped by scope: physical gPTP, `verilator-lint`, `verilator-suites` and its shards, `yosys-elaboration`, `yosys-portability` and its shards. Skipped contexts are not evidence | `receipts/hosted_checks.tsv` |

## Lens results

```text
[R425] PASS Conformance - docs/findings/117_AUDIO_CONTINUITY.md:14-22,461-463,471-472,489-499,511-526 at e5ad1187; PR #628 body - checked against #117 acceptance box 4, the B5 assignment and rulings 5929406675 and 5929901339 items 1-5 (withheld sizes, summary.json only, re-pin, template, header, Refs only, no peer counts)
[R425] PASS RTL - git diff --raw e4b771f9..e5ad1187 (two .md files, mode 100644; 4 gitlinks identical to base); docs/design/TIME_SYNC.md:169,463,478; docs/reference/REGISTER_MAP.md:203; avdecc/aem_descriptors.py:97-103,590; avdecc/aem_assemble.py:289-294 - the page's beat, slip-counter and 7.2.16 encoding claims hold, and no RTL, CDC or interface contract changed
[R425] PASS Robustness - receipts/robustness.txt, receipts/probes.txt at archive 9006c78e - the masked record copy is refused by both tools (rc 1), gunzip -k without -f refuses (rc 2) and keeps the masked copy, steps 2-3 are cwd-independent, and a one-bit flip in the restored record changes both receipts
[R425] PASS Tests - receipts/repro_steps1-3.txt, open_trace_9006c78e.txt, probes.txt, hashcheck_9006c78e.txt - steps 1-3 reproduce both receipts byte for byte at 9006c78e and 2be652c3, the trace matches :521-523, and each cmp can fail for the input it claims to depend on
[R425] PASS Docs - the whole page, the docs/findings/README.md row, the PR body and the commit message at e5ad1187 - tables, withheld sizes, header, archive paragraph, template and public text checked; receipts/tables.txt, withheld_sizes.txt, pubscan.txt, pr_body_checks.txt, gates.txt; S1-S3 are SUGGESTION only
```

## Lens ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #117 body (acceptance box 4). B5 assignment 5925737609. Round assignments 5926598386, 5927406852, 5928569912 and 5929901339. Ruling 5929406675. Page `:6-48`, `:83-103`, `:380-413` and `:459-552`. PR body. Archive `9006c78e`, `2be652c3` and `6e6a08fa` `MANIFEST.json` and `RAW-ARTIFACTS.json` | R425-5 | `e5ad118783c2ff96e13f1d794f10bf2b63741282` |
| RTL | CLEAN | `git diff --raw e4b771f9..e5ad1187`: two Markdown files, no RTL, gitlinks unchanged. `docs/design/TIME_SYNC.md:169,463,478`, `docs/reference/REGISTER_MAP.md:203`, `avdecc/aem_descriptors.py:97-103,590` and `avdecc/aem_assemble.py:289-294` against page `:41-48`, `:118-120`, `:220-225` and `:384-409` | R425-5 | `e5ad118783c2ff96e13f1d794f10bf2b63741282` |
| Robustness | CLEAN | `r425_5_robust.sh` and `r425_5_probes.sh` on fresh extractions of `author/`, `author-r2/` and `author-r3/` at `9006c78e`: `receipts/robustness.txt`, `receipts/probes.txt` | R425-5 | `e5ad118783c2ff96e13f1d794f10bf2b63741282` |
| Tests | CLEAN | `b5_attrib.py` and `b5_round3.py` at `9006c78e` and `2be652c3`: `receipts/repro_steps1-3.txt`, `receipts/open_trace_9006c78e.txt`, `receipts/hashcheck_9006c78e.txt`, `receipts/raw_index_9006c78e.txt` and `receipts/probes.txt` | R425-5 | `e5ad118783c2ff96e13f1d794f10bf2b63741282` |
| Docs | CLEAN (S1, S2, S3 are SUGGESTION) | The whole page, the `docs/findings/README.md:20` row, the PR body, the commit message, `.github/PULL_REQUEST_TEMPLATE.md` and CONTRIBUTING. `receipts/tables.txt`, `withheld_sizes.txt`, `pubscan.txt`, `pr_body_checks.txt` and `gates.txt` | R425-5 | `e5ad118783c2ff96e13f1d794f10bf2b63741282` |

## Limits

- **No bench access.** No measurement was re-taken. Physical calibration was
  NOT RUN, and field skips are not hardware proof. The figures that need the
  private raw captures (the whole-run counts, the zero-frame ordinals, and the
  `derive` and `wholerun` modes) rest on the raw files' SHA-256 values in the
  published index, and were not re-derived.
- **Withheld values were derived in memory only.** The old sizes and the
  channel-count candidates were derived from `e216dfe4` and are written
  nowhere in this packet. The scan covers stated durations at 3 and 4 bytes
  per sample, not every possible arithmetic route.
- **The public-text scan uses generic lists only.** No private name map was
  available, so a bench-specific name outside those classes would not be
  caught by it.
- **Not run (not allowed or not applicable):** the full parent, processor,
  gPTP, Yosys and builder banks; Docker or the act replica; any GitHub write.
  No RTL probe was needed, so the scoped simulator was not used.
- **Hosted evidence was read only.** `docs-check` was still in progress at
  the snapshot.
- **Archive observation, not a page finding.** The `b5_attrib.py` docstring
  (lines 11-13) still lists `runs/a-long/events.jsonl` among its inputs. Only
  its private-input modes read that file. The page pins that tool's hash, so
  the docstring is not the page's to change.
- **Clone integrity** (`receipts/clone_integrity.txt`):
  - HEAD, the HEAD tree and the index tree are the exact head, and the
    worktree equals the index in content and mode.
  - There are 0 untracked files.
  - The two changed files re-hash to their HEAD blobs.
  - The gitlinks are `external` `efeb541a`, `gptp-processor` `5dce647a`,
    `protocol-processor` `b2db3a97` and `third_party/verilog-axis`
    `48ff7a7e`, unchanged from the base.

## Pending manager duties

- Hosted acceptance at the exact head, including `docs-check`, which was in
  progress at the snapshot, and the act replica.
- The round-5 PR body is already live at this head. Keep it in step with any
  later commit.
- Optionally act on S1 (re-pin to `2be652c3` or later) at the next page edit.
- The final current-dev candidate at the merge turn: source base `e4b771f9`,
  live dev `ea3fb38877842f223afea97e3bd72a10500455c9`. Source validation is
  distinct from it.
- The merge needs explicit maintainer authorization and the second, internal
  positive review at this head.

## Receipts

Scripts: `r425_5_repro.sh`, `r425_5_hashcheck.py`, `r425_5_trace.py`,
`r425_5_probes.sh`, `r425_5_robust.sh`, `r425_5_withheld.py`,
`r425_5_archive_scan.py`, `r425_5_rawindex.py`, `r425_5_tables.py` and
`r425_5_pubscan.py`. Receipts are under `receipts/`. Every published file is
listed in `MANIFEST.sha256`.

R425-5 FINISHED
