[A476] REVIEW READY

Round 4 addendum for PR #628 (bench lane B5, #117 acceptance box 4, the audio continuity row). It applies the [A10] ruling on the stream-count question (https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5929406675) on top of the round 4 REVIEW READY (https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5929389267). Docs only, with no bench access. Refs #117.

Commit: `e216dfe4f0cab7b0c7352d7973acb4d33c157f70`
Branch: `b5-bench-1001`, parent `c5804007630b4ef39b93f725807019f46e700ecd` (the round 4 head, kept as is), base dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`. One added commit with a one-line subject. It is local only: not pushed, and the PR is not edited.
Changed: `docs/findings/117_AUDIO_CONTINUITY.md` (+11 -10). No other file. The index row is unchanged.

**Ruling item 1.** The page now states the peer's streams, stream ports, stream states and clusters without counts, and the reasoning is kept:
- `:76-77`, as found: every reference-peer stream state was unbound. The DUT's own stream state count is kept.
- `:375-376`, Direction B: the peer's dynamic audio map on its STREAM_PORT_OUTPUT 0 takes the talker's stream channels only from the audio clusters that port owns.
- `:395-397`, the survey walk: it sent one read of type 0x0010 at the index of each cluster the peer's stream ports own, each answered NO_SUCH_DESCRIPTOR. It sent no map read, because the peer's stream ports declare no static map.
- `:410`, the Restore table: "All unbound; the end census equals the start in every entry but one, the DUT's live propagation delay". The census total is dropped too. The census holds a fixed number of entries per stream, so its total gives the peer's stream count.
- PR body: the Round 2 and Round 3 sections are restated the same way, and Round 4 gains a "Stream counts" bullet. It is to be applied when the PR is next edited.

**Ruling item 2.** The peer's media clock source selection stays, at `:80` and `:297`.

**Not changed (a reading, for review).** The stream-format channel counts at `:94` (the Stream format table) and `:403` count channels within a stream format. They are not counts of streams, stream ports, stream states or clusters, and the frozen Binding rule record's format values encode them. Whether the rule reaches them is the manager's call.

**Tables.** Proof of `c5804007` against `e216dfe4`, with the unchanged round 2 `b5_table_proof.py` and a literal `diff` of every table line:
- 14 of the 15 tables are byte-identical, including every measurement table, with 119 table lines at both heads.
- One line changed: the Restore table's stream-state cell, for these counts only. Its Item cell is unchanged.
- Against `cf38633a`, 13 of 15 tables are byte-identical. The two changed lines are that cell and the R424-3 S1 cell.

**Public text.**
- **Stream-count scan.** The peer's counts and the totals that contain them are derived in memory from the local lane packet and never written. The scan covered the added lines and commit messages of `c5804007..e216dfe4`, `cf38633a..e216dfe4` and `e4b771f9..e216dfe4` (the whole page), and the packet. No hit is a peer count: the hits are the DUT's own stream state count at `:76`, and a phrase about the capture's reads at `:243` and in the PR body. As a power check at `c5804007`, it hit every line the ruling names on the page and in the round 3 PR body.
- **Label scan.** As in round 4, with the pattern lists rebuilt in memory and every pattern first hitting a planted line. It found 0 hits in the addendum and round 4 ranges and in the packet. The whole-PR range keeps its one hit: round 1 text in the frozen Restore table, the DUT's own gPTP state, now at `:415`.

Validation, all rc 0 at `e216dfe4` from the physical lane path, none piped:
- `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base e4b771f9` (0 findings over 542 added lines) and `check_doc_paths.py`, in the pinned Markdown environment;
- `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py --check` and `scripts/check_feature_status.py --self-test`;
- `git diff --check`, `git diff --check e4b771f9 HEAD`, `git diff --check cf38633a HEAD` and `git diff --check c5804007 HEAD`;
- `gen_toc.py --verify-anchors`.

Acceptance criteria (the ruling's items 1 to 3): met, with the evidence above. The round 4 assignment's items 1 to 4 stand as in the earlier REVIEW READY. Round 4 packet `b5-a476` adds:
- the gate outputs at `e216dfe4`;
- the table proof, the label scan and the stream-count scan at `e216dfe4`;
- the updated `HANDOFF.md`, `PR-BODY.md` and `MANIFEST.sha256`.

Open risks/questions:
- The removed counts remain in the earlier commits of this PR, which are already pushed, and in the PR body as last applied. The ruling chose an added or amended commit, so history is not rewritten.
- The format channel counts, as above.
- Direction B stays open, and a read of the AUDIO_CLUSTER descriptors might not settle it.
- The head is not pushed, so the hosted checks and the act replica have not run on it.
