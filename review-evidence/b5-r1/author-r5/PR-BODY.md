[A472] Record #117 audio continuity end to end against the reference peer on dev ec0cc0c1

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why, and the measured result.
- **[Round 2](#round-2)** -- How R424-1 and R425-1 were answered.
- **[Round 3](#round-3)** -- How R424-2 and R425-2 were answered.
- **[Round 4](#round-4)** -- How R424-3 and R425-3 were answered, and the stream-count ruling.
- **[Round 5](#round-5)** -- How R424-4 and R425-4 were answered, under the round 5 rulings.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

WIP: documentation only, in review. Round 5 answers R424-4 and R425-4, both NEGATIVE at `e216dfe4`. Re-review at the round 5 head is pending.

- `b5-bench-1001` -> `dev`.
- Head: `e5ad118783c2ff96e13f1d794f10bf2b63741282`. Base: dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`.
- Six commits: the round 1 record `bf9e5d82`, the round 2 restatement `e29d12b1`, the round 3 restatement `cf38633a`, the round 4 restatement `c5804007` with its stream-count follow-up `e216dfe4`, and the round 5 restatement `e5ad1187`.
- Local gates: 12 of 12 rc 0 at `e5ad1187` (see [How to validate](#how-to-validate)).
- Hosted checks and the act replica: not run at `e5ad1187` when this body was written.

## Linked Issue / roles

Refs #117 (acceptance box 4, the audio continuity row), under the bench lane B5 assignment: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5925737609

Relates to #117. This PR records one row of acceptance box 4 and must leave the Issue open, so it carries no closing keyword.

Roles:

- Executor: `[A472]` (round 1, the bench operator); rounds 2 to 5: `[A473]`, `[A474]`, `[A476]` and `[A478]`, docs only with no bench access.
- Internal cleared-context reviewer: `[R424]`.
- External reviewer: `[R425]`.
- Assignments and rulings: `[A10]`, the lane manager.

## Description

- `docs/findings/117_AUDIO_CONTINUITY.md` (new): the bench record of the audio continuity row.
- `docs/findings/README.md`: its index row.

No other documentation, code or configuration changes.

**Result (operator measurements, not review verdicts).** The first-light pattern enters the DUT's TDM input from the SoC board's McASP0. The DUT's AAF talker carries it to the reference peer's listener, and an external audio capture records the peer's output. Image: dev `ec0cc0c1`, as installed; identity gate PASS.

| Item | Verdict |
|---|---|
| Integrity: stream channels 0 and 1 bit-exact at 24 bits, in order, over 660 s | PASS: 31,569,594 of 31,569,600 frames; 0 torn, 0 invalid; 6 single zero frames |
| Continuity over 660 s | FAIL: 334 repeats at the DUT's documented INTERNAL beat; 520 one-frame drops, one every 1.266 s, attributed by inference to the peer's output rate; 117,104 more frames in skips of two frames or more: 236 of the 239 of 60 or more stall-aligned capture-path loss, the other three, of 72, 78 and 108 frames, not stall-aligned; those of 2 to 59 not separated from a packet-sized drop downstream of the peer's receive counters |
| Restarts: 30 unbind and rebind cycles, rebind response to first valid sample | PASS, 30 of 30 under 1 s: median 0.0279 s, maximum 0.1358 s, no growth |
| Direction B, the peer's talker to the DUT's listener | NOT RUN: it was not established whether a known signal can reach the peer's talker channels without a wiring change; the descriptors naming each cluster's signal source were not read, because the survey walk is defective |
| #117 audio continuity row | FAIL as measured |

Binding rule: the listener's stream format was set to the talker's before each run's first bind, and set back after each run; the talker's format was never set. The bench was restored and the restore proven; the one residual is the SoC board bridge legs' new process IDs.

Line numbers in the Round 2 to Round 4 sections are at those rounds' heads. Round 5's are at `e5ad1187`.

## Round 2

Under the round 2 assignment (https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5926598386), answering R424-1 and R425-1. Docs and evidence only, with no bench access.

- **Attributions (R424-1 F1, R425-1 F1).** The page, its summary rows and the index row now state each cause only as strongly as the evidence carries it. Skips of 60 frames or more are stall-aligned capture-path loss. Skips of 2 to 59 frames are not separated from a packet-sized drop downstream of the peer's receive counters. The one-frame drops are attributed to the peer's output rate by inference, with a drop at the capture's input named as the alternative.
- **Reproducible figures (R425-1 F2).** A new tool derives the window's read record (131,540 bytes) from the local read-time file and computes every attribution figure from published inputs.
  - 236 of 239 reproduces with the stall defined as a read interval over 15 ms, one or two reads before the skip.
  - The stall excess, 109,069 frames, reproduces. The recurrence is corrected to 3.00 s (2.99 to 3.02 s).
  - The count drift 115,614 does not reproduce. It is corrected to 117,653 frames from `summary.json`'s `window_time`.
  - The slip rate is stated as 16.46 ppm, one frame in 60,768.
  - The absolute host-clock rates (0.8 and 17.3 ppm) are dropped: they held only if every skip of two frames or more was a capture loss.
  - The whole-run integrity counts are now derived from the raw pair; the six window zero frames are named.
  - The Limits share is split: skips of two frames or more removed 0.37% of the frames, 0.35% in the stall-aligned skips.
- **What the read record adds.** A frame lost inside the capture path after sampling delays every later read, so the capture's delivery deficit steps by the frames lost.
  - The 284 smaller skips inside stall clusters are consistent with that, in aggregate.
  - The 237 smaller skips away from any stall, in 121 clusters, never come with a deficit step of their size: 95 clusters stay within 3 frames, 22 step by 1 ms, and 4 match neither.
  - Controls: beat repeats, one-frame skips and planted losses behave as expected, and the result holds across a parameter sweep.
  - So those skips are not attributed, and whether a lossless capture path would remove them is open.
- **Direction B (R425-1 F3).** The reason now states only what was observed. The peer's dynamic map on STREAM_PORT_OUTPUT 0 draws only from the clusters that port owns. Its AUDIO_UNIT declares no external or internal port and no routing element, so the clusters' source is not visible over AEM (round 3 replaces this reason). The survey walk is marked defective for reuse: four descriptor type codes are wrong against IEEE 1722.1 Table 7.1 as `avdecc/aem_descriptors.py` encodes it, so no AUDIO_CLUSTER descriptor was read.
- **Controller tool revision (R424-1 F2).** The revision that ran the binds and format sets cannot be established from the packet's records. The start snapshot hashed `24208ef2` (8,642 bytes). The descriptor survey 70 s later shows that the controller copy had changed, with no hash recorded. The listed `47b7387a` is the end snapshot's re-staged copy.
- **Tables.** 14 of the page's 15 tables are byte-identical. The summary verdict table changes only the Evidence cells of the continuity row and the row verdict. Their Item and Verdict cells and every figure are unchanged.

## Round 3

Under the round 3 assignment (https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5927406852), answering R424-2 and R425-2. Docs only, with no bench access. One commit, `cf38633a`, on `docs/findings/117_AUDIO_CONTINUITY.md` and its index row.

- **F1 (R424-2 F1, R425-2 F1), the published read record.** The manager republished it as `a-long-reads.u16.gz`. The page now gives the reproduction steps: `gunzip -kf a-long-reads.u16.gz`, check the SHA-256, then run `b5_attrib.py figures`.
  - The `-f` is needed. The copy with three bytes masked still sits beside the `.gz`, and `gunzip -k` alone refuses to overwrite it (rc 2).
  - From the public archive alone, `gunzip -kf` restores SHA-256 `2183d57f…`, and the published `b5_attrib.py` reproduces the published `attribution.txt` byte for byte.
- **Direction B reason (R425-2 F2, item 1).** The page no longer says the clusters' source is not visible over AEM. It says what was observed: a dynamic map on STREAM_PORT_OUTPUT 0 that draws only from the clusters that port owns, and no external port, internal port or routing element.
  - Each AUDIO_CLUSTER descriptor names its cluster's signal source (`signal_type`, `signal_index`, `signal_output`, IEEE 1722.1 7.2.16). Those descriptors were not read, because the survey walk is defective.
  - So whether a known signal can reach the peer's talker channels without a wiring change is open. NOT RUN stays. The summary row's Evidence cell says the same.
- **What the walk sent (R424-2 S2, item 2).** It sent one read of type 0x0010 at the index of each cluster the peer's stream ports own, each answered NO_SUCH_DESCRIPTOR. It sent no map read, because the peer's stream ports declare no static map, and no external port read. The dynamic maps came from GET_AUDIO_MAP.
- **Which skips "stall-aligned" covers (R424-2 S3, R425-2 S2, item 3).** 236 of the 239 skips of 60 frames or more are stall-aligned, 109,670 frames. The stall excess, 109,069 frames, is now compared with those 109,670.
  - The other three are named: 72 frames at 34.0 s into the window, and 78 and 108 frames on consecutive reads at 634.0 s. They are not stall-aligned, and the stall attribution does not cover them.
  - The summary row, the index row and the Limits share say "236 of the 239".
- **Where the 1 ms steps fall (R424-2 S1, R425-2 S1, item 4).** Stated as an observation, without attribution: 22 of the 121 off-stall clusters step by 1 ms, against about 0.26 by chance. The chance figure is 7 one-millisecond steps over 51,828 clear read positions, about 3,240 windows of the floor test's 16 reads.
- **Suggestions (item 5).**
  - R425-2 S3, taken: the page now says the planted-loss control is linear by construction, so it checks where the floor windows sit, not the test's power. The round 3 receipt shows a plant reads back as the floor's own step plus the plant, with a largest difference of 0.
  - R424-2 S4, the suggestions retained from round 1:
    - R424-1 S2, the free-run acceptance rule, taken. The page cites the register map's slip counters, which record the 1.958 s beat as "the standing free-run rule, slips accepted".
    - R424-1 S3, the order criterion, taken. "In order" means 0 backward steps, as the grader defines them, and the window has 0.
    - R424-1 S3, the ordinals around the six skip, zero, skip events, taken. They are read from the local graded pair and published as a derived receipt. Each zero frame sits between consecutive ordinals and replaces no pattern frame. So each event drops two frames and inserts one: one frame fewer, like a single skip.
    - R424-1 S1, the forward pointers from the #117 ledger and the #75 index row, retained. Those rows are on other pages. The B5 assignment fixed the output as this page and its index row, and round 3 did not extend it, so adding them stays the manager's call.
- **Tables.** 14 of the page's 15 tables are byte-identical to round 2, and every table after the summary verdict table is byte-identical to round 1. The summary verdict table changes only two Evidence cells: the continuity row (item 3) and the Direction B row (item 1). Their Item and Verdict cells are unchanged, and so is every figure of the old cells.

## Round 4

Under the round 4 assignment (https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5928569912), answering R424-3 and R425-3. Docs only, with no bench access. Two commits on `docs/findings/117_AUDIO_CONTINUITY.md` only: `c5804007`, and `e216dfe4` under the stream-count ruling below. The index row is unchanged. R425-3 F1, the round 1 packet's bench layout, was resolved by the manager at archive commit `8e6be432`.

- **Where the packets are published (R424-3 F1, item 1).** Artifact hashes now opens with one paragraph in the sibling findings pages' form. It names branch `b5-review-evidence`, pins archive commit `8e6be4329008137a152f9171638e48a43e549fb7` with a link (re-pinned to `9006c78e` in round 5), and maps each lane label to its directory: `b5-a472` to `review-evidence/b5-r1/author/`, `b5-a473` to `author-r2/` and `b5-a474` to `author-r3/`. The Continuity paragraph and the Contents entry point to it.
  - At that commit, from those three directories alone, the page's steps 1 to 3 restore the read record to `2183d57f…` and reproduce `attribution.txt` (`18ebbfc1…`) and `round3_figures.txt` (`9fa0f027…`) byte for byte. Of the lane packet's label-masked files, both tools read only the `a-long` `summary.json` (corrected in round 5).
- **The masked files' hashes (item 2).** After the tool table, the page says:
  - the `run_a.py` and `grade_a.py` hashes are the unmasked originals', recorded as `original_sha256` in the archive's `MANIFEST.json`;
  - their published copies are label-masked, recorded with `path_redacted`, and are checked against `published_sha256`;
  - the mask replaced code constants, so those two copies are for reading and do not run as published.

  The read record's hash is stated the same way. The other masked lane-packet files are named, and the page cites no hash of them.
  - Every one of the page's 20 SHA-256 values was checked against the manifest at `8e6be432`. 10 are manifest file hashes: the `original_sha256` of 3 `path_redacted` files, and 7 unmasked files whose published bytes match.
  - The other 10 are quoted in published files: 8 raw files in `RAW-ARTIFACTS.json`, the pattern period in the run logs, and the controller's start snapshot.
  - At `8e6be432` the masked `RAW-ARTIFACTS.json` kept all 19 entries' sizes and hashes. At `9006c78e` it withholds the every-channel captures' sizes (round 5).
- **Suggestions (item 3), all taken.**
  - R424-3 S1: the final row's Evidence cell and Limits now name the three skips of 72, 78 and 108 frames that are not stall-aligned as not attributed. These are the continuity row's own figures.
  - R425-3 S1: the Direction B reason now says that each AUDIO_CLUSTER descriptor records its cluster's source in `signal_type`, `signal_index` and `signal_output`, but that the source need not be a physical input.
    - The repository's own encoding writes INVALID for a stream input port's cluster and AUDIO_UNIT for a stream output port's cluster (`avdecc/aem_descriptors.py:590`, `avdecc/aem_assemble.py:289-294`).
    - So reading those descriptors might not settle the question either. The open item below says the same.
  - R425-3 S2: the restart p95 is the nearest-rank 95th percentile, as `grade_a.py` computes it: the 29th of the 30 sorted restarts, cycle 20's. Linear interpolation gives 0.0344 s. This is stated below the table, and the table is unchanged.
- **Forward pointers (item 4).** Retained by the manager, so they are not changed.
- **Stream counts (`e216dfe4`, under the manager's ruling https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5929406675).** The public-text rule reaches the reference peer's stream counts. The page and this body now name the peer's stream states, stream ports and clusters without counting them, and keep the reasoning.
  - As found (`:76-77`): every reference-peer stream state was unbound. The DUT's own stream state count is kept.
  - Direction B (`:375-376`): the peer's dynamic audio map on its STREAM_PORT_OUTPUT 0 takes the talker's stream channels only from the audio clusters that port owns.
  - The survey walk (`:395-397`): it sent one read of type 0x0010 at the index of each cluster the peer's stream ports own, each answered NO_SUCH_DESCRIPTOR. It sent no map read, because the peer's stream ports declare no static map.
  - Restore table (`:410`): all unbound, and the end census equals the start in every entry but one, the DUT's live propagation delay. The census total is dropped too, because the census holds a fixed number of entries per stream, so its total gives the peer's stream count.
  - The Round 2 and Round 3 sections above are restated the same way.
  - As ruled, the peer's media clock source selection stays (`:80`, `:297`).
  - The stream-format channel counts (`:94`, `:403`) count channels within a stream format, not streams, stream ports, stream states or clusters. The round 5 assignment's ruling 1 keeps them.
- **Tables.** Against `c5804007`, 14 of the page's 15 tables are byte-identical, including every measurement table. The Restore table changes only the stream-state cell, and only for these counts. Against round 3 (`cf38633a`), 13 of 15 are byte-identical. The two changed lines are that Restore cell and the Evidence cell of the "#117 audio continuity row" row (R424-3 S1). That row's Item and Verdict cells are unchanged, and the old cell's figures are all kept.

## Round 5

Under the round 5 assignment (https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5929901339), answering R424-4 and R425-4. Docs only, with no bench access. One commit, `e5ad1187`, on `docs/findings/117_AUDIO_CONTINUITY.md` only (+23 -12). The index row is unchanged.

- **The every-channel capture sizes (R425-4 F1, item 1).** In the Artifact hashes table, the Bytes cells of the three every-channel rows now read "withheld": the `a-long` 10 s, the `diag1` 25 s and the as-found 3 s captures (`:493`, `:495`, `:498`). Their SHA-256 values stay.
  - Two sentences that stated every raw file's size now match. Raw files are identified by SHA-256, and all but the every-channel captures by size too (`:471-472`). The masked `RAW-ARTIFACTS.json` keeps every raw file's SHA-256, and every size but the every-channel captures', which it withholds (`:524-526`).
  - No other byte size on the page, in the index row or in this body gives the capture's channel count by division. A check derives that count in memory from the old page and never prints it. It tests every byte size against each stated duration, exactly and as a whole multiple. It flags exactly the three rows on the old page, and none on the new page, the index row or this body. The one whole-multiple match is the `cap-test1` graded pair. That is a two-channel file, and its size is a whole multiple of its own 6 bytes per frame.
- **Which masked input the reproduction reads (R424-4 F1, R425-4 F3, item 2).** `:521-523` now say that, of the lane packet's label-masked files, `b5_attrib.py` and `b5_round3.py` read only the `a-long` `summary.json`. Round 4 item 1 above is corrected the same way.
  - An open trace of both `figures` commands at `9006c78e` lists the packet files each opens. `b5_attrib.py` opens `a-long-reads.json`, the restored `a-long-reads.u16`, `summary.json` and `continuity-events.csv`. `b5_round3.py` opens the same files and `peer-descs-2.jsonl`.
  - Of those, only `summary.json` is `path_redacted`, apart from the read record copy that step 1 replaces. Neither tool opens `events.jsonl`.
- **Re-pin (item 3).** The archive paragraph (`:461-463`) pins `9006c78e354d5a2f244fd606c55790a825304bd3`, the archive commit that withholds the same sizes. The three packet directories were taken from that commit alone, 207 files, each equal to its manifest `published_sha256`.
  - Step 1 restores `2183d57f…` (131,540 bytes).
  - Steps 2 and 3 reproduce `attribution.txt` (`18ebbfc1…`) and `round3_figures.txt` (`9fa0f027…`) byte for byte, with rc 0 and empty stderr.
  - All 20 SHA-256 values on the page resolve against the manifest at that commit, with 0 problems.
  - The masked file set in the three directories is unchanged from `8e6be432`. The re-pin changes only the published bytes of 7 files that were already masked.
  - Every artifact row's size equals its `RAW-ARTIFACTS.json` entry, or both are withheld. Every entry whose size is withheld is an every-channel capture.
- **This body (R425-4 F4, item 4).** It is rewritten in the repository's pull-request template: Status, Linked Issue / roles, Description, Authoritative references, How to get into the same state, How to validate, Known limitations / out of scope and Definition of Done. The round sections are kept. "Refs #117" stays, with no closing keyword.
- **Page header (R424-4 S1, item 5).** `:14-22` list round 4 ([A476], its assignment and the stream-count ruling) and round 5 ([A478], its assignment).
- **Rulings applied.**
  - The format channel counts stay (`:103`, `:412`).
  - The page and this body carry no count of the peer's streams, stream ports, stream states or clusters.
  - Redaction is top-only, so no history is rewritten.
- **Not taken.**
  - R425-4 S2, naming the `gates/gates.txt` of `author-r2/` and `author-r3/` among the masked files, is not among the round 5 items. The page cites no hash of either.
  - R424-4 S2, the archive residuals, is the manager's. The round 5 rulings 2 to 4 answer it.
- **Tables.** Against `e216dfe4`, 14 of the 15 tables are byte-identical, with 119 table lines at both heads. That covers every measurement table, the summary verdict table and the Restore table. The Artifact hashes table changes only the three Bytes cells, as item 1 requires. With its Bytes column cut out, its literal diff is empty. Tables 2 to 12 and 15 are byte-identical to round 1 `bf9e5d82`.

## Authoritative references

- #117 acceptance box 4, the audio continuity row, and #75's 1 s restart bound.
- The bench lane B5 assignment and the round 2 to round 5 assignments: #117 comments 5925737609, 5926598386, 5927406852, 5928569912 and 5929901339. The stream-count ruling: #117 comment 5929406675.
- IEEE 1722.1 7.2.16 (AUDIO_CLUSTER) and Table 7.1 (descriptor types), as `avdecc/aem_descriptors.py` and `avdecc/aem_assemble.py` encode them.
- `docs/design/TIME_SYNC.md`, "Talker capture handoff": the INTERNAL beat, one whole-frame repeat every 1.958 s.
- `docs/reference/REGISTER_MAP.md`, the media-boundary slip counters: the standing free-run rule, slips accepted.
- `docs/findings/451_TDM8_FIRST_LIGHT.md`, Method: the first-light pattern.
- CONTRIBUTING section 6 (wording and privacy) and section 6.1 (the em-dash rule).
- The evidence archive: branch `b5-review-evidence` at `9006c78e354d5a2f244fd606c55790a825304bd3`, `review-evidence/b5-r1/`, and its `MANIFEST.json`.

## How to get into the same state

The lane packet `b5-a472` holds the tools, per-action evidence, summaries, the raw-artifact index by SHA-256 (and size, but for the every-channel captures), the redaction record and a manifest. The round 2 packet `b5-a473` holds the analysis tools, the derived read record, the attribution, records and table-identity receipts, the gate outputs and a manifest. The round 3 packet `b5-a474` holds `b5_round3.py`, its receipts, the gate outputs and a manifest. They are published at archive commit `9006c78e` as `author/`, `author-r2/` and `author-r3/`, as the page states.

The round 4 packet `b5-a476` holds the hash check, the reproduction at `8e6be432`, the table-identity and scan receipts and the gate outputs. The round 5 packet `b5-a478` holds the reproduction at `9006c78e` with its open trace, the hash and raw-index checks, the capture-size derivation check, the table proof and the gate outputs. Raw captures stay outside the packets and the repository.

```sh
git fetch origin dev b5-bench-1001 b5-review-evidence
git switch --detach e5ad118783c2ff96e13f1d794f10bf2b63741282
# The Markdown gates refuse to run without the hash-pinned lock, so install it in a virtual environment:
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
# The three evidence packets, from the archive commit alone, outside the worktree:
E=$(mktemp -d)
git archive 9006c78e354d5a2f244fd606c55790a825304bd3 review-evidence/b5-r1/author review-evidence/b5-r1/author-r2 review-evidence/b5-r1/author-r3 | tar -x -C "$E"
```

## How to validate

```sh
python3 -B scripts/docs_check.py
python3 -B scripts/check_doc_style.py
python3 -B scripts/gen_toc.py --check
python3 -B scripts/gen_toc.py --verify-anchors
python3 -B scripts/check_em_dash.py --base e4b771f9
python3 -B scripts/check_doc_paths.py
python3 -B scripts/ci_scope.py --selftest
python3 -B scripts/check_baremetal_only.py --check
python3 -B scripts/check_feature_status.py --self-test
git diff --check e4b771f9 HEAD
# The page's reproduction steps 1 to 3, in the extraction above:
cd "$E/review-evidence/b5-r1"
(cd author-r2/receipts && gunzip -kf a-long-reads.u16.gz && sha256sum a-long-reads.u16)
python3 author-r2/tools/b5_attrib.py figures author author-r2/receipts | cmp - author-r2/receipts/attribution.txt
python3 author-r3/tools/b5_round3.py figures author author-r2/receipts | cmp - author-r3/receipts/round3_figures.txt
```

Expected result / pass criteria:

- Every command exits 0.
- `check_em_dash` reports 0 findings over 553 added lines in 2 changed pages.
- `sha256sum` prints `2183d57f0646cf94405b95aea5547b83f5ff0b9190ac0bd1bdcc87760c919961`.
- Both `cmp` commands print nothing.

## Known limitations / out of scope

- **No new measurement.** Rounds 2 to 5 had no bench access. Physical calibration was NOT RUN. Printed precision is not calibrated accuracy.
- **Raw captures are not public.** The whole-run integrity counts, the zero-frame ordinals and the `derive` and `wholerun` modes need them. They rest on the raw files' SHA-256 in the published index.
- **History.** Under the owner decision of 2026-10-01, redaction is top-only. This PR's earlier commits and the archive's earlier commits keep what they had.
- **Open items.** Each needs a decision outside this lane.
  - The 236 stall-aligned skips of 60 frames or more remove 0.35% of the frames, so a clean continuity window was not recorded. A capture path that loses no frames is an owner item.
  - Direction B: whether a known signal can reach the peer's talker channels without a wiring change is open. A read-only read of the peer's AUDIO_CLUSTER descriptors, type 0x0014, would show the source each cluster records. Under the repository's own encoding of IEEE 1722.1 7.2.16, that source may be the audio unit rather than a physical input, so the read might not settle the question. It needs a decision.
  - The 237 skips of 2 to 59 frames away from capture stalls are not attributed. Placing them, between the peer's receive counters and the capture's input, needs a decision. The 1 ms steps that concentrate there are not explained.
  - The one-frame drops are attributed by inference to the peer's INTERNAL media clock, running 16.46 ppm slower than the stream. Testing that needs the peer's media clock to follow the stream, a clock-source change on the peer outside this lane. It needs a decision.
- **Retained by the manager.** The forward pointers from the #117 ledger and the #75 index row (R424-1 S1 and its successors). R425-4 S2 is not among the round 5 items.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (the row is recorded as FAIL as measured; this PR records it and leaves #117 open)
- [ ] New or changed behavior has self-checking tests (not applicable: documentation only, no behavior change)
- [x] Required local verification bar passes (12 documentation gates, rc 0 at `e5ad1187`)
- [ ] Self-test evidence is posted in a PR comment (each round's evidence is in its REVIEW READY comment on #117)
- [x] No undocumented requirement or interface change remains (documentation only)
- [ ] Internal cleared-context review is positive (R424-4 NEGATIVE at `e216dfe4`; re-review at `e5ad1187` pending)
- [ ] External review is positive (R425-4 NEGATIVE at `e216dfe4`; re-review at `e5ad1187` pending)
- [ ] Blocking and major findings are fixed and re-reviewed (no BLOCKER or MAJOR was raised; the round 4 MINORs are answered at `e5ad1187`, re-review pending)
- [ ] No review round remains in flight (round 5 re-review pending)
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md) (the manager, at the merge turn)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done (the manager; this PR leaves #117 open)
