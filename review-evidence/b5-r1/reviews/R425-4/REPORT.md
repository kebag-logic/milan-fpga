[R425] NEGATIVE - exact head e216dfe4f0cab7b0c7352d7973acb4d33c157f70

Round R425-4, external independent review of PR #628: issue #117, bench lane
B5, acceptance box 4, the audio continuity row.

- **Head:** `e216dfe4f0cab7b0c7352d7973acb4d33c157f70`, tree
  `15e18903484842dcb6302159b9f9f1f27d8fc3ed`.
- **Source base:** dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`.
- **Scope:** docs and evidence only. Round 4 is `c5804007` and `e216dfe4` on
  the round-3 head `cf38633a`.
- **Order:** context was rebuilt from the issue, the assignments, the ruling,
  the diff and the public archive. The verdict and ledger were written before
  any prior review finding was read.

## Verdict

**NEGATIVE, on four MINOR findings.**

**Resolved at this head:**
- R424-3 F1 and every round-4 suggestion.
- The literal classes of the R425-3 F1 mask.
- The stream-count ruling, on the page, the index row, the PR body and the
  commit messages.

**Unchanged and confirmed:**
- The measurements, every measurement table and the "FAIL as measured"
  reading.
- The docs gates, rc 0.

**What keeps it NEGATIVE:**
- **F1:** the masked capture channel count still follows from the page's own
  byte sizes.
- **F2:** the pinned archive the page names still states the peer's stream
  and cluster counts, and the page's step 3 regenerates one such receipt.
- **F3:** the page misstates which masked inputs the reproduction reads.
- **F4:** the PR body does not use the repository's PR template.

## Findings

### F1 MINOR: the capture's channel count follows from the page's byte sizes

- **Lenses:** Conformance, Docs.
- **Where:**
  - `docs/findings/117_AUDIO_CONTINUITY.md:483` and `:488`, the Artifact
    table's "every channel" rows (`:485` is consistent with them).
  - Archive `8e6be432` (and tip `cae94a6b`), in
    `review-evidence/b5-r1/author/`:
    - `RAW-ARTIFACTS.json`;
    - the capture-file records in `runs/{a-long,diag1,cap-test1}/console.txt`
      and `events.jsonl`.
- **Authority:**
  - The R425-3 F1 resolution (PR #628 comment 5928569576) masks the capture
    channel count as `<capture-channel-count>`. It masks it even inside a raw
    file's name: `cap-all-<n>ch.raw`.
  - CONTRIBUTING section 6 forbids bench-identifying information.
  - Ruling #117 5929406675 applies the derivation standard: the census total
    was dropped because "its total gives the peer's stream count".
- **Evidence:**
  - The page states the capture at 48 kHz and 24 bits.
  - The graded-pair row is 6 bytes per frame for two channels: 236,137,116
    bytes for 39,356,186 frames. So the samples are 3 bytes.
  - The "every channel, 10 s" and "as found, every channel, 3 s" byte sizes
    each divide exactly by seconds x 48,000 x 3. The quotient is the masked
    count.
  - The archive keeps every raw size, and its capture-file records carry the
    same sizes.
  - Probe: `scripts/public_scan.py`, DERIVE lines in
    `receipts/public_scan.txt`. They print YES or no and never the value.
  - A literal scan of the page has 0 hits, so the mask holds only against
    literal text.
  - R425-3 F1 recorded "the page needs no change". That round missed this
    derivation, so this round retains the class.
- **Impact:** the masked class is public by one division. The mask, and the
  "0 hits" result for the class, hold only literally.
- **Required outcome:** one of these two.
  - No public text from which the capture's channel count follows by
    arithmetic, on the page and in the archive. For example, the
    every-channel rows keep their SHA-256 and drop or mask their byte size.
    The page's tables are frozen, so this needs a manager ruling.
  - A public manager ruling that the capture's channel count is outside the
    rule, with the archive mask withdrawn to match.
- **Verification:** rerun `scripts/public_scan.py` against the corrected page
  and archive tip. Every capture-channel-count DERIVE line reads `no`.

### F2 MINOR: the pinned archive states the peer's stream and cluster counts, and the page's step 3 regenerates one such receipt

- **Lenses:** Conformance, Docs.
- **Owner:** the manager (archive).
- **Where:** archive `8e6be432` (and tip `cae94a6b`), under
  `review-evidence/b5-r1/`:
  - `author-r2/receipts/records.txt`:
    - the peer configuration's STREAM_INPUT and STREAM_OUTPUT descriptor
      counts;
    - the AUDIO_UNIT's stream port counts;
    - each stream port's cluster count.
  - `author-r3/receipts/round3_figures.txt`: each stream port's cluster
    count, and the walk's read index range and read count.
  - `author/restore/census-start.jsonl`, `census-end.jsonl` and
    `author/runs/agent-dryrun.txt`: one label per peer stream index.
  - `author/restore/peer-descs-2.jsonl`: the raw `descriptor_counts` of the
    peer CONFIGURATION descriptor.
  - The archived review reports `reviews/R425-1/REPORT.md:35`,
    `reviews/R424-2/REPORT.md:61,143` and `reviews/R425-2/REPORT.md:42`:
    walk-read counts, one read per peer cluster.
- **Authority:**
  - Ruling #117 5929406675: the public-text rule reaches the reference peer's
    stream counts.
  - The round-4 constraint (#117 5928569912): no stream counts in public
    text.
  - The R425-3 F1 resolution comment states that the peer's stream counts
    are masked in `author/`.
- **Evidence:**
  - The page pins this archive as its evidence (`:452-459`).
  - Its step 3 regenerates `round3_figures.txt` byte for byte
    (`receipts/repro_pinned.txt`), so a reader who follows the page prints
    the counts.
  - None of these files is `path_redacted` in `MANIFEST.json`
    (`receipts/hash_check_8e6be432.txt`).
  - Probe: DERIVE lines in `receipts/public_scan.txt`, and the field names
    above.
  - This report states no count.
- **Impact:**
  - The ruling holds on the page and the PR body. It does not hold in the
    public evidence the page tells a reader to regenerate.
  - The same counts also stand in the PR's earlier commits, in round 1 to 3
    review comments on PR #628 and in earlier lane comments on #117
    (`receipts/comment_count_scan.txt`). Under the "do not edit or delete"
    rule those stay; see Pending manager duties.
- **Required outcome:** a public manager decision, either way.
  - Mask the counts at the archive top as the R425-3 F1 resolution did. This
    touches the published receipts of `b5_records.py` and `b5_round3.py`, so
    state how the page's byte-for-byte reproduction of `round3_figures.txt`
    is then checked.
  - Or rule publicly that the stream-count rule does not reach the evidence
    archive.
- **Verification:** after the decision, rerun `scripts/public_scan.py` over
  the archive tip and read the count fields of the receipts named above.

### F3 MINOR: the page says both tools read the masked `events.jsonl`; neither does in the reproduction

- **Lenses:** Docs, Tests.
- **Where:** `docs/findings/117_AUDIO_CONTINUITY.md:511-513`: "`b5_attrib.py`
  and `b5_round3.py` read the masked `a-long` `summary.json` and
  `events.jsonl`, and still reproduce both receipts byte for byte".
- **Evidence:** the page's steps 2 and 3 were run under an open-audit hook
  (`scripts/trace_opens.py`, `receipts/tool_inputs.txt`).
  - `b5_attrib.py figures` opens `a-long-reads.json`, `a-long-reads.u16`,
    `summary/a-long/summary.json` and
    `summary/a-long/continuity-events.csv`.
  - `b5_round3.py figures` opens the same files plus
    `restore/peer-descs-2.jsonl`.
  - Neither opens `runs/a-long/events.jsonl`.
  - In `b5_attrib.py`, only `derive` and `wholerun` read that file
    (`window()`, lines 67-80 and 112-113). Both need raw files that stay
    private.
  - `b5_round3.py` has no reader of it.
  - The `b5_attrib.py` docstring (lines 11-13) also lists `events.jsonl`
    among the `figures` inputs.
- **Impact:**
  - The paragraph exists to tell a reader which masked inputs the published
    reproduction exercises. It claims coverage of the masked `events.jsonl`
    that the reproduction does not give.
  - The byte-for-byte result therefore says nothing about the mask's effect
    on that file.
  - That both receipts reproduce is true.
- **Required outcome:** the page names exactly the masked inputs the
  reproduction reads: the masked `summary.json`, with the read record
  restored from the `.gz`. Either the page drops `events.jsonl` from that
  sentence, or it says that only the private-input `derive` and `wholerun`
  modes read it.
- **Verification:** `scripts/trace_opens.py` on both `figures` commands
  matches the page's list.

### F4 MINOR: the PR body does not use the repository's PR template

- **Lenses:** Docs.
- **Where:** the PR #628 body.
- **Authority:**
  - CONTRIBUTING section 2.2: "PRs use the template: Status / Description /
    how-to-reproduce / how-to-validate / DoD".
  - `.github/PULL_REQUEST_TEMPLATE.md` also has Linked Issue / roles,
    Authoritative references and Known limitations.
- **Evidence:**
  - The body's sections are Change, Result, Round 2 to Round 4, Open items
    and Validation.
  - It has no Status line, no executor and reviewer roles, no authoritative
    references section, no "How to get into the same state" commands and no
    Definition of Done.
  - The sibling #117 evidence PR #598 uses the template headings.
  - Earlier rounds did not record this.
- **Impact:** a cold reviewer cannot read the lane's status, roles or DoD
  tally from the PR. The evidence content is otherwise complete.
- **Required outcome:** the body carries the template's sections, with
  "Refs #117" (under Relates to) and no Closes keyword, as the B5 assignment
  requires.
- **Verification:** read the body's headings against the template.

### Suggestions

- **S1 (Docs):** the page header (`:6-13`) credits rounds 1 to 3 but not
  round 4. A round-4 line (packet location, mask statement, stream-count
  ruling) would keep the provenance self-contained.
- **S2 (Docs):** `:507-511` lists the lane packet's masked files. The
  `path_redacted` `gates/gates.txt` of `author-r2/` and `author-r3/` is not
  named. The page cites no hash of either, so only completeness is affected.

## Round-4 items and the assigned checks

| Item | Result | Evidence |
|---|---|---|
| R424-3 F1: where the packets are | Resolved | `:452-459` name branch `b5-review-evidence`, pin `8e6be4329008137a152f9171638e48a43e549fb7` and map `b5-a472`, `b5-a473` and `b5-a474` to `author/`, `author-r2/` and `author-r3/`. From those three directories alone at that commit, in a fresh extraction, steps 1 to 3 restore `2183d57f...`. They reproduce `attribution.txt` (`18ebbfc1...`) and `round3_figures.txt` (`9fa0f027...`) byte for byte: `receipts/repro_pinned.txt`. The form follows `117_GPTP_SILICON_EVIDENCE.md:652-656` |
| Item 2: hashes of the masked files | Resolved, except one sentence (F3) | Each of the page's 20 SHA-256 values resolves: `receipts/hash_check_8e6be432.txt`. `run_a.py`, `grade_a.py` and the read record give the `original_sha256` of `path_redacted` files. 7 tool hashes equal the published bytes. The other 10 are quoted in published files. All 355 manifest entries' `published_sha256` equal the bytes, and no file lies outside the manifest. The page's list of masked files equals the `author/` `path_redacted` set |
| R425-3 F1: the mask at `8e6be432` | Literal classes resolved; derivation retained as F1 | Capture-channel-index, capture-channel-count, link-type, interface-name, soc-product and usb-bus-position give 0 direct hits on the page, index row, added lines, PR body and commit messages. 24 patterns, each first hitting a planted line: `receipts/public_scan.txt`. `summary.json` `channel_identification` reads `<capture-channel-layout>`. In the archive's author packets, the one direct hit is a false positive: an "All <n> SHA-256 values" sentence in `author-r4/REVIEW-READY*.md:20`. The hits in archived review reports are walk-read counts (F2) and one generic word-list regex, which does not single out the masked word: `receipts/hit_classification.txt` |
| Stream-count ruling | Met on page, index row, PR body and commits | `receipts/count_scan.txt`: no count of the peer's streams, stream ports, stream states or clusters. "All 4 DUT stream states" is the DUT's own. The peer's clock-source selection is kept (`:80-81`, `:297`). The stream-format channel counts stay (`:94`, `:403`): they are format fields, not a channel map, per the manager's reading in this review's assignment |
| R424-3 S1: name the three unaligned skips | Taken | `:28` and `:437-439` name the skips of 72, 78 and 108 frames (258 frames) |
| R425-3 S1: 7.2.16 qualification | Taken; verified | `avdecc/aem_descriptors.py:590` writes `signal_type` as passed. `avdecc/aem_assemble.py:289-294` passes 0xFFFF for input-port clusters and AUDIO_UNIT for output-port clusters. The Table 7.1 codes are at `aem_descriptors.py:103` |
| R425-3 S2: p95 method | Taken; verified | `grade_a.py:266` uses the nearest rank. From the page's cycle table, rank 29 of 30 is 0.0389 s, cycle 20's, and linear interpolation gives 0.0344 s: `receipts/p95_check.txt` |
| Table identity | Verified | `receipts/table_identity.txt`. Against `cf38633a`, 13 of 15 tables are identical; the two changed lines are the final summary row's Evidence cell and the Restore stream-state cell, and both rows' first cells are unchanged. Against `c5804007`, 14 of 15 are identical; only the Restore cell changed. Against round 1, `bf9e5d82`, every measurement table (2 to 12, 14 and 15) is identical. Every head has 119 table lines |
| Refs only | Verified | Page `:6` and the PR body say Refs #117. Neither carries a Closes keyword |
| Commits | Verified | Five commits, each with a one-line message and no trailers |
| Public names and topology | Verified, except F1 and F2 | The page, index row, PR body and commit messages name no host, peer, switch or instrument. They state no wiring, channel map or clock topology, and no peer stream count. The scan classes and `receipts/count_scan.txt` cover this |
| Docs gates | rc 0 | `receipts/gates.txt`, run in a private environment holding the hash-pinned Markdown lock: `docs_check.py`; `check_em_dash.py --base e4b771f9` and `--selftest`; `check_doc_style.py`; `gen_toc.py --check` and `--verify-anchors`; `check_doc_paths.py`; `check_feature_status.py` and its `--self-test`; `git diff --check e4b771f9 HEAD`. The worktree stayed clean |
| Hosted, exact head (read only) | Executed and skipped contexts recorded | `receipts/hosted_checks.txt`: 8 succeeded, including `docs-check` (completed 2026-10-01T10:52:16Z), `docs-check-no-git` and `rtl-fast`. 7 were skipped by scope (Verilator, Yosys, physical); skipped contexts are not evidence. The manager owns hosted and act acceptance |

## Prior review findings at this head

| Finding | State at `e216dfe4` | Evidence |
|---|---|---|
| R425-1 F1, R424-1 F1 (MINOR): attributions stated beyond the evidence | Resolved | `:25`, `:28`, `:240-300` and `:428-443` and the index row state each cause only as strongly as the receipts carry it |
| R425-1 F2 (MINOR): figures not reproducible | Resolved | `receipts/repro_pinned.txt` |
| R425-1 F3, R425-2 F2 (MINOR): the Direction B reason | Resolved | `:27` and `:373-388` say that whether a known signal can reach the peer's talker channels was not established |
| R424-1 F2 (MINOR): controller tool revision | Resolved | `:520-527` |
| R425-2 F1, R424-2 F1 (MINOR): published read record | Resolved | Step 1 restores `2183d57f...`: `receipts/repro_pinned.txt` |
| R424-1 S2, S3; R424-2 S1, S2, S3 | Taken | `:36-38`, `:129`, `:270-274`, `:285-289`, `:394-400`, `:243-252` |
| R424-1 S1, R424-2 S4, R424-3 S2: forward pointers | Retained by the manager (round-4 item 4) | SUGGESTION; it affects no lens |
| R424-3 F1 (MINOR) | Resolved | See above |
| R424-3 S1; R425-3 S1, S2 | Taken | See above |
| R425-3 F1 (MINOR) | Partly resolved | The literal classes are resolved at the archive top. The capture-channel-count class is retained by derivation as F1. The unmasked originals remain in the archive's history (`ef3a7091` to `227a6541`), pending the owner decision the manager named |

## Lens ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | Issue #117 acceptance box 4. Assignments 5925737609, 5926598386, 5927406852 and 5928569912; ruling 5929406675; manager comments 5927406516 and 5928569576. Page `:15-39`, `:371-404` and `:450-542`. Archive `8e6be432` and tip `cae94a6b` | R425-4 | `e216dfe4f0cab7b0c7352d7973acb4d33c157f70` |
| RTL | CLEAN | `git diff --name-only e4b771f9..e216dfe4` lists only `docs/findings/117_AUDIO_CONTINUITY.md` and `docs/findings/README.md`, so no RTL changed. The page's RTL-facing claims were checked against `docs/design/TIME_SYNC.md:169,463-478` (the 1.958 s beat, counted once on `SLIP_TDM`) and `docs/reference/REGISTER_MAP.md:1837-1861` (slip counters, the free-run rule). Also checked: the AAF decode of `0205022002006000`, `0205022001006000` and `0215022002006000` (48 kHz, INT32, 8, 4 and up to 8 channels, 6 frames per packet, 8,000 packets per second); `avdecc/aem_descriptors.py:103,590` and `avdecc/aem_assemble.py:245-294`; and the arithmetic of `:200-201`, `:211-216` and `:290-294` | R425-4 | `e216dfe4f0cab7b0c7352d7973acb4d33c157f70` |
| Robustness | CLEAN | `receipts/robustness_probes.txt` (`scripts/robustness_probes.sh`). Beside the masked copy, `gunzip -k` without `-f` refuses (rc 2), as `:470-473` says. Both tools refuse the masked record copy (assertion, rc 1). Steps 1 to 3 do not depend on the working directory. A one-bit flip in the restored record changes `attribution.txt`. Every run starts from a fresh extraction | R425-4 | `e216dfe4f0cab7b0c7352d7973acb4d33c157f70` |
| Tests | UNCLEAN (F3) | `receipts/repro_pinned.txt`, `receipts/tool_inputs.txt`, `receipts/hash_check_8e6be432.txt`, `receipts/p95_check.txt` and `receipts/table_identity.txt`. `b5_attrib.py` and `b5_round3.py` at `8e6be432`; `grade_a.py:266` | R425-4 | `e216dfe4f0cab7b0c7352d7973acb4d33c157f70` |
| Docs | UNCLEAN (F1, F2, F3, F4) | The whole page at the head; the `docs/findings/README.md` row; the PR body; the commit messages; CONTRIBUTING sections 2.2, 6 and 6.1; `.github/PULL_REQUEST_TEMPLATE.md`. `receipts/public_scan.txt`, `receipts/count_scan.txt` and `receipts/gates.txt` | R425-4 | `e216dfe4f0cab7b0c7352d7973acb4d33c157f70` |

## Limits

- **How the private values were derived:**
  - Derived in memory only, from the difference between the round-1 packet
    in archive history (`ef3a7091`) and the masked packet (`8e6be432`).
  - No private value and no peer count is written anywhere in this packet.
  - A class the mask did not label is covered only by the generic lists.
  - The self-scan of this packet has 2 direct hits. Both are the generic word
    lists in `scripts/public_scan.py`, which single out no word.
- **Bench and calibration:**
  - No bench access. Physical calibration was NOT RUN, and field skips are
    not hardware proof.
  - No measurement was re-taken. Figures were re-derived only from published
    inputs.
- **Not run (not allowed):** the full parent, processor, gPTP, Yosys and
  builder banks.
- **Hosted evidence:** read only.
- **Clone integrity:** the clone remains at exact head bytes
  (`receipts/clone_integrity.txt`).
  - The index tree is `15e18903...`, with no modified or untracked file.
  - The worktree bytes and modes equal the index.
  - The gitlinks are `external` `efeb541a`, `gptp-processor` `5dce647a`,
    `protocol-processor` `b2db3a97` and `third_party/verilog-axis`
    `48ff7a7e`, unchanged from the base.

## Pending manager duties

- Decide F1 and F2 publicly. Both concern the manager's archive, and F1 also
  concerns a frozen page table.
- Publish the reading that stream-format channel counts are format fields and
  stay. The executor asked for it (#117 5929592804), and it is not yet in a
  public comment.
- The owner decision on history:
  - the unmasked round-1 packet (`ef3a7091` to `227a6541`);
  - the PR's earlier commits (`bf9e5d82` to `c5804007`), which carry the
    removed counts;
  - the round 1 to 3 review comments on PR #628 and the earlier lane comments
    on #117, which state peer cluster counts and stay under the do-not-edit
    rule.
- Hosted acceptance at the exact head (the contexts are recorded in
  `receipts/hosted_checks.txt`) and the act replica.
- The final current-dev candidate at the merge turn: source base `e4b771f9`,
  live dev `ea3fb38877842f223afea97e3bd72a10500455c9`. Source validation is
  distinct from it.

R425-4 FINISHED
