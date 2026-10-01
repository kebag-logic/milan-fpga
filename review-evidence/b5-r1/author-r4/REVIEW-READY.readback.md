[A476] REVIEW READY

Round 4 for PR #628 (bench lane B5, #117 acceptance box 4, the audio continuity row), under the [A10] round 4 assignment (https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5928569912). It answers R424-3 and R425-3. Docs only, with no bench access. Refs #117.

Commit: `c5804007630b4ef39b93f725807019f46e700ecd`
Branch: `b5-bench-1001`, parent `cf38633ad9a5bdb05517bedba73ce50965af967b`, base dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`. One new commit, local only: it is not pushed, and the PR is not edited.
Changed: `docs/findings/117_AUDIO_CONTINUITY.md` (+47 -11). No other file. The index row is unchanged.

**1. Where the packets are published (R424-3 F1)** at `:451-458`, in the form of `117_GPTP_SILICON_EVIDENCE.md:652-654`.
- The paragraph names branch `b5-review-evidence` and pins archive commit `8e6be4329008137a152f9171638e48a43e549fb7` with a tree link.
- It maps `b5-a472` to `review-evidence/b5-r1/author/`, `b5-a473` to `author-r2/` and `b5-a474` to `author-r3/`, and names `MANIFEST.json`.
- `:206-208` and the Contents entry point to it.
- At that commit, from those three directories alone, the page's steps 1 to 3 work as written. The record restores to `2183d57f…`, and `attribution.txt` (`18ebbfc1…`) and `round3_figures.txt` (`9fa0f027…`) reproduce byte for byte. Both tools now read the masked `summary.json` and `events.jsonl`.

**2. The masked files' hashes** at `:500-514`.
- The `run_a.py` and `grade_a.py` hashes are the unmasked originals', recorded as `original_sha256` in `MANIFEST.json`.
- The published copies are label-masked, recorded with `path_redacted`, and are checked against `published_sha256`. The mask replaced code constants, so those two copies do not run as published.
- The read record's hash is stated the same way. The other masked lane-packet files are named, and the page cites no hash of them.

All 20 SHA-256 values on the page were checked against the manifest at `8e6be432`, with 0 problems:
- 3 are `original_sha256` of `path_redacted` files;
- 7 are unmasked files whose published bytes match;
- 10 are quoted in published files: 8 raw files in `RAW-ARTIFACTS.json`, whose 19 entries all keep their size and hash, the pattern period in the run logs, and the controller's start snapshot.

**3. Suggestions, all taken.**
- R424-3 S1: the final row's Evidence cell (`:28`) and Limits (`:436-438`) now name the three skips of 72, 78 and 108 frames that are not stall-aligned as not attributed.
- R425-3 S1 (`:377-387`): each AUDIO_CLUSTER descriptor records its source, but the source need not be a physical input.
  - The repository's encoding writes INVALID for a stream input port's cluster and AUDIO_UNIT for a stream output port's cluster (`avdecc/aem_descriptors.py:590`, `avdecc/aem_assemble.py:289-294`).
  - So a read might not settle the question. The PR body's open item says the same.
- R425-3 S2 (`:319-321`): the p95 is the nearest-rank 95th percentile, as `grade_a.py` computes it: the 29th of 30, cycle 20's. Linear interpolation gives 0.0344 s.

**4. The forward pointers** are retained by the manager, so they are not changed.

**Tables.** 14 of the page's 15 tables are byte-identical to `cf38633a`, including every measurement table, with 119 table lines at both heads. The summary verdict table changes one line: the Evidence cell of the "#117 audio continuity row" row (R424-3 S1). Its Item and Verdict cells are unchanged. The old figure is kept, and the new figures are the continuity row's own. The proof gives SHA-256 per table and a literal `diff`.

**Public text.** A label-only scan covered the packet, and the added lines and commit messages of `cf38633a..c5804007` and of `e4b771f9..c5804007`.
- It used the private values the archive mask replaced, the local host names, MAC, home-directory and interface patterns, and lists of vendor, link-type, clock-topology, channel-number, tool and account names. Every pattern first hit a planted line in memory.
- It found 0 hits in round 4's range and in the packet.
- The whole-PR range has one hit: round 1 text in the frozen Restore table, the DUT's own gPTP state (`:414`).

Validation, all rc 0 at `c5804007` from the physical lane path, none piped:
- `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base e4b771f9` (0 findings over 541 added lines) and `check_doc_paths.py`, in the pinned Markdown environment;
- `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py --check` and `scripts/check_feature_status.py --self-test`;
- `git diff --check`, `git diff --check e4b771f9 HEAD` and `git diff --check cf38633a HEAD`;
- `gen_toc.py --verify-anchors`.

Acceptance criteria (the assignment's items 1 to 4): met, with the evidence above. Round 4 packet `b5-a476` holds:
- the hash check, the reproduction at `8e6be432`, and the raw-index and p95 receipts;
- the table proof, the scan and the gate outputs;
- `HANDOFF.md`, `PR-BODY.md` and `MANIFEST.sha256`.

Open risks/questions:
- **Decision needed.** The round 4 constraint adds "stream counts". Text from rounds 1 to 3 at `:76`, `:409` (Restore table), `:374` and `:395` states counts of the reference peer's stream states and clusters, and `:79` and `:296` state its clock-source selection. Round 4 changes none of it: the tables are frozen, and no item requires it. Whether the rule reaches that text is the manager's call.
- Direction B stays open, and a read of the AUDIO_CLUSTER descriptors might not settle it.
- The head is not pushed, so the hosted checks and the act replica have not run on it.

