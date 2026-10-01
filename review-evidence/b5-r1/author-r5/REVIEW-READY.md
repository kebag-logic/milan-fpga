[A478] REVIEW READY

Round 5 for PR #628 (bench lane B5, #117 acceptance box 4, the audio continuity row), under the [A10] round 5 assignment (https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5929901339). It answers R424-4 and R425-4. Docs only, with no bench access. Refs #117.

Commit: `e5ad118783c2ff96e13f1d794f10bf2b63741282`
Branch: `b5-bench-1001`, parent `e216dfe4f0cab7b0c7352d7973acb4d33c157f70`, base dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`. One commit with a one-line subject. It is local only: not pushed, and the PR is not edited.
Changed: `docs/findings/117_AUDIO_CONTINUITY.md` (+23 -12). No other file. The index row is unchanged.

**1. The every-channel capture sizes (R425-4 F1).**
- The Artifact hashes table's Bytes cells of the three every-channel rows now read `withheld` (`:493`, `:495`, `:498`), and their SHA-256 values stay. These are the only table cells changed.
- Two sentences that claimed every raw size now match: `:471-472` and `:524-526`. At `9006c78e` the masked `RAW-ARTIFACTS.json` keeps every SHA-256, and every size but the every-channel captures'.
- A check derives the capture's channel count in memory from the old page, and never prints it. It tests every byte size against each stated duration, exactly and as a whole multiple.
  - On the old page it flags exactly the three rows.
  - At the head it finds no unexplained hit on the page, the index row or the PR body. The one whole-multiple match is the `cap-test1` graded pair, a two-channel file whose size is a multiple of its own 6 bytes per frame.

**2. The masked input the reproduction reads (R424-4 F1 = R425-4 F3).**
- `:521-523`: of the lane packet's label-masked files, `b5_attrib.py` and `b5_round3.py` read only the `a-long` `summary.json`. The PR body's Round 4 item 1 says the same.
- An open trace of both `figures` commands at `9006c78e` agrees.
  - The only `path_redacted` file either tool opens is `summary.json`, besides the read-record copy that step 1 replaces.
  - Neither opens `events.jsonl`.

**3. Re-pin and reproduction.** `:461-463` pin `9006c78e354d5a2f244fd606c55790a825304bd3`. From `author/`, `author-r2/` and `author-r3/` at that commit alone:
- all 207 files equal their manifest `published_sha256`;
- step 1 restores `2183d57f…` (131,540 bytes);
- steps 2 and 3 reproduce `attribution.txt` (`18ebbfc1…`) and `round3_figures.txt` (`9fa0f027…`) byte for byte, with rc 0 and empty stderr.

Other checks at the new pin:
- All 20 SHA-256 values on the page resolve against the manifest at `9006c78e`, with 0 problems.
- Every artifact row's size equals its raw-index entry, or both are withheld.
- The masked file set is unchanged from `8e6be432`.

**4. PR body (R425-4 F4).** `PR-BODY.md` is rewritten in the repository's template: Status, Linked Issue / roles, Description, Authoritative references, How to get into the same state, How to validate, Known limitations / out of scope and Definition of Done.
- It keeps the `[A472]` first line and "Refs #117", with no closing keyword.
- It keeps the Round 2 to Round 4 sections and adds a Round 5 section.
- It is to be applied when the PR is next edited.

**5. Page header (R424-4 S1).** `:14-22` list round 4 ([A476], its assignment and the stream-count ruling) and round 5 ([A478], its assignment).

**Rulings.**
- The format channel counts stay (`:103`, `:412`).
- No count of the peer's streams, stream ports, stream states or clusters is on the page or in the body.
- No history is rewritten.

**Tables.** The proof prints no old table text.
- `e216dfe4` to `e5ad1187`: 14 of 15 tables are byte-identical (literal `diff` rc 0), with 119 table lines at both heads. That covers every measurement table.
- The Artifact hashes table changes only the three Bytes cells. With that column cut out, its `diff` is empty.
- Tables 2 to 12 and 15 are byte-identical to round 1 `bf9e5d82`.

**Public text.** Three scans covered the added lines and commit messages of `e216dfe4..e5ad1187` and `e4b771f9..e5ad1187`, and the round 5 packet. Each prints labels and places only, and each first hits a planted control in memory.
- The round 4 label scan (private mask literals, host names, and vendor, link, clock, tool, account, channel, SoC, bus, MAC, path and interface patterns) found 0 hits in round 5. The whole-PR range keeps its one known hit: round 1 text in the frozen Restore table, the DUT's own gPTP state, now at `:424`.
- The round 4 stream-count scan found no peer count. The hits are the DUT's own stream state count at `:85`, and the round 2 and 3 phrase about the capture's reads around a stall.
- A withheld-value scan covered the four withheld sizes and the capture's channel count, all derived in memory. It found 0 hits, and its power check hits the three old rows.

Validation, all rc 0 at `e5ad1187` from the physical lane path, none piped:
- `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base e4b771f9` (0 findings over 553 added lines) and `check_doc_paths.py`, in the pinned Markdown environment;
- `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py --check` and `scripts/check_feature_status.py --self-test`;
- `git diff --check`, `git diff --check e4b771f9 HEAD` and `git diff --check e216dfe4 HEAD`;
- `gen_toc.py --verify-anchors`.

Acceptance criteria (the assignment's items 1 to 5, under rulings 1 to 4): met, with the evidence above. Round 5 packet `b5-a478` holds:
- the reproduction at `9006c78e` with its open trace;
- the hash, raw-index and size-derivation checks;
- the table proof, the three scans and the gate outputs;
- `HANDOFF.md`, `PR-BODY.md` and `MANIFEST.sha256`.

Open risks/questions:
- **Archive (manager).** At `9006c78e`, two archive receipts still carry the `diag1` every-channel size: `author-r4/receipts/raw_index_check.txt:9` and `reviews/R424-4/receipts/hash_check.txt:7`. No other archive file there holds a withheld size. The page's steps do not read either file.
- **Not taken.** R425-4 S2 (naming `author-r2/` and `author-r3/` `gates/gates.txt` as masked) is not among the round 5 items, and the page cites no hash of either.
- The head is not pushed, so the hosted checks and the act replica have not run on it.
