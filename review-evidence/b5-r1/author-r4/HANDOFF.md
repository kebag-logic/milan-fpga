# [A476] Round 4 handoff: PR #628, bench lane B5 (#117 audio continuity)

Status: REVIEW READY at `e216dfe4f0cab7b0c7352d7973acb4d33c157f70` (local only, not pushed). This is the addendum head. The earlier REVIEW READY was at `c5804007630b4ef39b93f725807019f46e700ecd`.

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5928569912
- Reviews answered: R424-3 (PR #628 comment 5928525413), R425-3 (PR #628 comment 5928526687). Manager F1 note: 5928569576 (R425-3 F1 resolved by the manager at archive `8e6be432`).
- Addendum: the [A10] ruling on the stream-count question, https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5929406675. See [Addendum](#addendum-the-stream-count-ruling-e216dfe4).
- Branch `b5-bench-1001`: start head `cf38633ad9a5bdb05517bedba73ce50965af967b`, round 4 head `c5804007630b4ef39b93f725807019f46e700ecd`, then one added commit, addendum head `e216dfe4f0cab7b0c7352d7973acb4d33c157f70`. Each is one commit with a one-line subject, no body and no trailers. Base dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`.
- Archive: branch `b5-review-evidence` at `8e6be4329008137a152f9171638e48a43e549fb7`, read with `git show` only.
- No bench access, no NAS write, no push, no PR edit, no comment edited or deleted.
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5929194470. Its readback equals `TAKEN.md` except for the trailing newline.
- REVIEW READY at `c5804007`: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5929389267. Its readback equals `REVIEW-READY.md` except for the trailing newline.
- REVIEW READY at `e216dfe4`: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5929592804. Its readback equals `REVIEW-READY-2.md` except for the trailing newline: the first 5,072 bytes are equal, and the readback has one more. No second TAKEN was posted.
- Resume note: the session was cut by a host restart. At resume the worktree was clean at `cf38633a`, nothing was committed, and no TAKEN was posted. So TAKEN was posted once, and the work was done from the start.

## Addendum: the stream-count ruling (`e216dfe4`)

The ruling: the public-text rule reaches the reference peer's stream counts.

1. Replace every count of the peer's streams, stream ports, stream states or clusters, on the page and in the PR body, with count-free wording that keeps the reasoning.
2. The peer's media-clock-source selection stays.
3. Amend, or add one commit, then re-run the gates and the scan.

One commit was added rather than amended, so the announced `c5804007` stays an ancestor and the delta reads on its own. Subject: "State the #117 B5 reference peer's stream states, stream ports and clusters without counts, under the round 4 stream-count ruling". `docs/findings/117_AUDIO_CONTINUITY.md` only, +11 -10.

| Where (at `e216dfe4`) | Was (at `c5804007`) | Now |
|---|---|---|
| `:76-77`, As found | `:76`, a count of DUT and of peer stream states | every reference-peer stream state was unbound; the DUT's own stream state count is kept |
| `:375-376`, Direction B | `:374-375`, a count of the clusters STREAM_PORT_OUTPUT 0 owns | the peer's dynamic audio map on its STREAM_PORT_OUTPUT 0 takes the talker's stream channels only from the audio clusters that port owns |
| `:395-397`, the survey walk | `:394-396`, the read count, the index range, the stream port count and the cluster count | one read of type 0x0010 at the index of each cluster the peer's stream ports own; no map read, because the peer's stream ports declare no static map |
| `:410`, Restore table | `:409`, the stream-state total and the census total | "All unbound; the end census equals the start in every entry but one, the DUT's live propagation delay" |

- **The census total.** It is dropped with the stream-state total. The start census holds a fixed number of entries per stream, one state entry and one format entry, plus fixed others, so its total gives the peer's stream count (`restore/census-start.jsonl` in the local lane packet).
- **Item 2.** The peer's clock-source lines stay: `:80` (As found) and `:297` (one-frame skips).
- **Not changed: the format channel counts.** `:94` (the Stream format table) and `:403` count channels within a stream format. They are not counts of streams, stream ports, stream states or clusters, and the frozen Binding rule record's format values encode them. This reading is published in REVIEW READY for the manager.
- **PR body.** Round 2 (`:46`) and Round 3 (`:57`, `:60`) are restated count-free. Round 4 gains a "Stream counts" bullet and the two-head table statement. The head, Validation and Evidence lines move to `e216dfe4`.
- **History.** The removed counts remain in the PR's earlier commits, which are already pushed, and in the PR body as last applied. The ruling chose an added or amended commit, so history is not rewritten.

### Addendum table proof

`receipts/table_identity-e216dfe4.txt` uses the same unchanged `b5_table_proof.py` (`5eb78c7f…`) and a literal `diff` of every table line.

- **`c5804007` to `e216dfe4`.** 15 tables at both heads, and 119 table lines at both. 14 of 15 are byte-identical, including every measurement table. The diff has one hunk: the Restore table's stream-state cell, Item cell unchanged.
- **`cf38633a` to `e216dfe4`.** 13 of 15 are byte-identical. The diff has two hunks: the R424-3 S1 cell and that Restore cell.
- **`docs/findings/README.md`.** 0 lines changed against both.
- **Masking.** In the receipt, the removed cell's counts are masked as `<stream-count>` and `<census-count>` (4 places, stated in its first line). Every other byte is raw tool output.

### Addendum scans

- **Stream-count scan.** `receipts/count_scan.txt`, written by `tools/b5_count_scan.py`.
  - The peer's stream input, output and state counts, its stream port and cluster counts, the highest cluster index and the totals that contain them are derived in memory from the local lane packet. They are never written.
  - The positive control is 12 of 12 planted lines.
  - Hits at `e216dfe4`, over the three ranges and this directory: the DUT's own stream state count at `:76`, and a phrase about the capture's reads at `:243` and `PR-BODY.md:34`. None is a peer count. The places in this directory that quote the DUT's count or that phrase were reworded before the final run.
  - Power check at `c5804007` (range `e4b771f9..c5804007`, with the round 3 PR body): it hits every line the ruling names, page `:76`, `:374`, `:394-396` and `:409`, and PR body `:46`, `:57` and `:60`, plus the same two capture-read phrases.
- **Label scan.** `receipts/token_scan-e216dfe4.txt`, written by the unchanged `tools/b5_scan.py`.
  - The labelled pattern lists were rebuilt in memory and passed on standard input. They cover vendor, link-type, clock-topology, capture-channel, account and tool or model names.
  - Each listed spelling first hit a labelled pattern in memory, and the tool's own control passed: 17 of 17 private literals and 9 of 9 labelled patterns.
  - Ranges `c5804007..e216dfe4` and `cf38633a..e216dfe4`, and this directory as finally written: 0 hits.
  - `e4b771f9..e216dfe4`: 1 hit, the same round 1 clock-topology word in the frozen Restore table, the DUT's own gPTP state, now at `:415`.
- **EUI-64 identifiers.** The stream-count scan also flags any 16-hex identifier other than the page's DUT entity, DUT stream and three format values, on lines that carry no `sha256`: 0 at `e216dfe4`.
- **Scope of "as finally written".** Both receipts were written after the REVIEW READY was posted and read back, so they cover every file here except themselves and `MANIFEST.sha256`. Both scans were then run once more over the whole directory, receipts and this final `HANDOFF.md` included, with the same results.
- **Scratch.** The masked archive files the label scan reads were extracted with `git show` into a temporary directory outside this one, which was removed afterwards.

### Addendum gates

`receipts/gates-e216dfe4/gates.txt`, run at `e216dfe4` from the physical lane path. Each command's output is in `gate-<n>.txt`. The same 12 gates are all rc 0, none piped, plus gate 13, `git diff --check c5804007 HEAD`, also rc 0.

- `docs_check.py`: 0 findings, 182 pages.
- `check_em_dash.py --base e4b771f9`: 0 findings over 542 added lines.
- `check_doc_paths.py`: 861 paths.
- `gen_toc.py --verify-anchors`: 283 links.
- `check_feature_status.py --self-test`: 46/46, 0 findings.

The worktree is clean before and after. The only ignored entry is a pre-existing `scripts/__pycache__/`.

## Round 4 change (file:line at `c5804007`)

`docs/findings/117_AUDIO_CONTINUITY.md` only, +47 -11. `docs/findings/README.md` is unchanged.

| Item | Where | What |
|---|---|---|
| 1, R424-3 F1 | `:451-458` | New first paragraph of Artifact hashes, in the form of `117_GPTP_SILICON_EVIDENCE.md:652-654`. It gives branch `b5-review-evidence`, the pinned commit `8e6be4329008137a152f9171638e48a43e549fb7` and a tree link, and maps `b5-a472` to `review-evidence/b5-r1/author/`, `b5-a473` to `author-r2/` and `b5-a474` to `author-r3/`. It also names `MANIFEST.json` (`original_sha256`, `published_sha256`, `path_redacted`). |
| 1 | `:206-208`, `:52` | The Continuity paragraph and the Contents entry now point to where the packets are published. |
| 2 | `:500-514` | After the tool table: the `run_a.py` and `grade_a.py` hashes are the unmasked originals' (`original_sha256`). The published copies are label-masked (`path_redacted`), so they are checked against `published_sha256`. The mask replaced code constants, so those copies do not run as published. The read record's hash is stated the same way. The other masked lane-packet files are named, and the page cites no hash of them. Both analysis tools still reproduce at the pinned commit. The masked `RAW-ARTIFACTS.json` keeps every raw size and hash. |
| 3, R424-3 S1 | `:28` (final row, Evidence cell), `:436-438` (Limits) | Names the three skips of 72, 78 and 108 frames that are not stall-aligned as not attributed. These are the continuity row's own figures. |
| 3, R425-3 S1 | `:377-387` | "names" becomes "records". The source need not be a physical input: the repository's encoding writes INVALID for a stream input port's cluster and AUDIO_UNIT for a stream output port's cluster (`avdecc/aem_descriptors.py:590`, `avdecc/aem_assemble.py:289-294`, both read at the head). So a read might not settle the question. The PR body's open item says the same. |
| 3, R425-3 S2 | `:319-321` | The p95 is the nearest-rank 95th percentile as `grade_a.py` computes it (`srt[ceil(0.95 n) - 1]`, published `author/tools/grade_a.py:266`): the 29th of 30, which is cycle 20's restart. Linear interpolation gives 0.0344 s (`receipts/p95_rule.txt`). This is prose below the table, and the table is unchanged. |
| 4 | none | The forward pointers are retained by the manager. |

## Reproduction at the pinned commit

`receipts/repro_at_8e6be432.txt`. The inputs are the three directories at `8e6be432`, extracted with `git show` into a scratch directory outside this one.

1. `gunzip -kf a-long-reads.u16.gz` takes the masked copy (`8897abce…`) to `2183d57f0646cf94405b95aea5547b83f5ff0b9190ac0bd1bdcc87760c919961`, 131,540 bytes.
2. `b5_attrib.py figures author author-r2/receipts` gives rc 0 with empty stderr. The output equals `attribution.txt` (`18ebbfc1…`) byte for byte.
3. `b5_round3.py figures author author-r2/receipts` gives rc 0. The output equals `round3_figures.txt` (`9fa0f027…`) byte for byte.

This matters at `8e6be432` because both tools read the lane packet's `summary/a-long/summary.json` and `runs/a-long/events.jsonl`. The mask changed both files after the round 3 reviews ran at `227a6541`.

## Hash check against MANIFEST.json

`receipts/hash_check.txt`, written by `tools/b5_hash_check.py` over the page at `c5804007`. Result: PASS, with 0 problems across 20 cited SHA-256 values. It stands at `e216dfe4`: no line the addendum adds or removes holds a hex identifier or hash. The line numbers below are at `c5804007`, and from `:77` on they are one higher at `e216dfe4`.

- **Manifest file hashes (10).**
  - 3 are `original_sha256` of `path_redacted` files: `run_a.py` (`:492`), `grade_a.py` (`:493`) and the read record (`:465`).
  - 7 are unmasked files whose published blob equals `published_sha256` equals `original_sha256`: `b5_tables.py`, `b5_ctl.py`, `avdecc_ro.py`, `console_read.py`, `b5_attrib.py`, `b5_records.py` and `b5_round3.py`.
- **Quoted in published files (10).**
  - 8 raw files are in the published `RAW-ARTIFACTS.json`, with sizes equal to the page's (`receipts/raw_index_check.txt`: 19 of 19 entries keep bytes and SHA-256, and 3 paths are label-masked).
  - The SoC-built pattern period is quoted in the published run logs.
  - The start snapshot `24208ef2…` is quoted in `restore/controller-start.txt` and `author-r2/receipts/records.txt`.
- **Local originals.** All 15 `path_redacted` files in `author/` hash, as the local lane packet holds them, to their `original_sha256`.
- **Published masked tools.** The published `author/tools/run_a.py` and `grade_a.py` fail to parse (rc 1). The mask replaced code constants, which is why the page says they do not run as published.

## Round 4 table identity proof (`cf38633a` to `c5804007`)

`receipts/table_identity.txt`. It uses the round 2 packet's unchanged `b5_table_proof.py` (`5eb78c7f…`, as published at `8e6be432`) and a plain `diff` of every table line, `cf38633a` against `c5804007`.

- 15 tables and 119 table lines at both heads.
- Tables 2 to 15 are byte-identical, and they include every measurement table.
- Table 1, the summary verdict table, differs in one line only: the "#117 audio continuity row" row. Its Item and Verdict cells are identical. The old cell's only figure (1.266) is kept, and the new figures (2, 59, 72, 78, 108) are the continuity row's own.
- `docs/findings/README.md`: 0 lines changed.

## Round 4 token scan (at `c5804007`)

`receipts/token_scan.txt`, written by `tools/b5_scan.py`.

The private literals are built in memory and never written:

- every value the `8e6be432` mask replaced, recovered by matching each masked line against the local original;
- the local host names.

The labelled patterns (vendors of instruments, switches and peers, link types, clock-topology words, capture channel numbers, tool and model names, account names) are passed on standard input, so their spellings are in no file. MAC addresses, home directories and interface-name forms are built in.

The positive control runs in memory before the scan: 17 of 17 private literals and 9 of 9 labelled patterns hit their planted line.

Result:

- **Round 4 range `cf38633a..c5804007`** (added lines and the commit message): 0 hits.
- **This directory as finally written**: 0 hits, for every file except `MANIFEST.sha256`, which holds only paths and hashes.
- **Whole PR range `e4b771f9..c5804007`**: 1 hit, a clock-topology word at `:414`. It is round 1 text (`bf9e5d82`, by `git blame`) in the Restore table's "DUT synchronization" row, the DUT's own gPTP state. Round 4 does not touch it, because that measurement table is frozen. Neither round 3 review raised it.

## Round 4 decision (ruled)

At `c5804007` this was published as a decision: whether the public-text rule's "stream counts" reaches the round 1 to 3 text at `:76`, `:374`, `:395` and `:409` (Restore table), and the clock-source lines `:79` and `:296`. The manager ruled yes for the counts and no for the clock-source selection. `e216dfe4` applies the ruling (see [Addendum](#addendum-the-stream-count-ruling-e216dfe4)). This handoff does not restate the removed values.

## Round 4 gates (at `c5804007`)

`receipts/gates/gates.txt`, run at `c5804007` from the physical lane path. Each command's output is in `gate-<n>.txt`. All 12 are rc 0, and none is piped.

- In the pinned Markdown environment:
  - `docs_check.py`: 0 findings, 182 pages;
  - `check_doc_style.py`;
  - `gen_toc.py --check`;
  - `check_em_dash.py --base e4b771f9`: 0 findings over 541 added lines;
  - `check_doc_paths.py`: 861 paths;
  - `gen_toc.py --verify-anchors`: 283 links.
- `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py --check` and `scripts/check_feature_status.py --self-test` (46/46, 0 findings).
- `git diff --check`, `git diff --check e4b771f9 HEAD` and `git diff --check cf38633a HEAD`.

The worktree is clean before and after. The only ignored entry is a pre-existing `scripts/__pycache__/`.

## PR body

`PR-BODY.md` keeps the `[A472]` first line and the `Refs #117` line, with no closing keyword. It updates the head line, adds "Round 4", and qualifies the Direction B open item (R425-3 S1). For the addendum, it restates the Round 2 and Round 3 sections count-free, adds the "Stream counts" bullet and the two-head table statement to Round 4, and moves the head, Validation and Evidence to `e216dfe4`. It has no absolute home path and no attribution footer.

## Limits

- No bench access. The raw captures are identified by hash only.
- The reproduction and the hash check read the archive at `8e6be432` only. The archive tip was not re-read for later commits.
- The scan's labelled patterns are finite lists, so a clean result covers those classes only. The private literals cover the `8e6be432` mask and the local host names. The round 1 redaction record (`redaction.json` in the local lane packet) holds labels and hashes only; its literal values are kept outside every local packet, so they were not available. Its classes (entity, clock and MAC identities, the gPTP time-source identity, capture identities, operator names) are covered by the MAC, EUI-64 and account patterns only.
- The labelled lists were rebuilt in memory for the addendum, because round 4 did not write them. They are not guaranteed to equal round 4's lists, so the two scans are comparable in result, not in pattern set.
- The stream-count scan derives the peer's counts from the round 1 census and the survey's descriptor reads. A count the packet does not record (for example, clusters per port) is matched only where it equals one of the derived counts.
- The removed counts remain in the PR's pushed history and in the PR body as last applied, until the PR body is next edited.
- Hosted checks and the act replica were not run: the head is not pushed.

## Files

| File | What |
|---|---|
| `TAKEN.md`, `TAKEN.readback.md`, `taken-url.txt` | the posted TAKEN |
| `REVIEW-READY.md`, `REVIEW-READY.readback.md`, `review-ready-url.txt` | the REVIEW READY posted at `c5804007` |
| `REVIEW-READY-2.md`, `REVIEW-READY-2.readback.md`, `review-ready-2-url.txt` | the REVIEW READY posted at `e216dfe4` |
| `PR-BODY.md` | the PR body to apply |
| `tools/b5_hash_check.py` | page hashes against the archive manifest |
| `tools/b5_scan.py` | label-only private-name scan |
| `tools/b5_count_scan.py` | the peer's stream-count scan, with counts derived in memory |
| `receipts/repro_at_8e6be432.txt` | steps 1 to 3 at the pinned commit |
| `receipts/hash_check.txt` | the hash check, the local originals and the parse check |
| `receipts/raw_index_check.txt` | the raw-artifact index, original against published |
| `receipts/p95_rule.txt` | p95 by nearest rank and by interpolation |
| `receipts/table_identity.txt` | the table proof and the plain table diff |
| `receipts/token_scan.txt` | the scan |
| `receipts/gates/` | the gate outputs at `c5804007` |
| `receipts/table_identity-e216dfe4.txt` | the addendum table proof, against `c5804007` and `cf38633a` |
| `receipts/token_scan-e216dfe4.txt` | the label scan at `e216dfe4` |
| `receipts/count_scan.txt` | the stream-count scan at `e216dfe4`, and its power check at `c5804007` |
| `receipts/gates-e216dfe4/` | the gate outputs at `e216dfe4` |
| `MANIFEST.sha256` | the sha256 of every other file here |
