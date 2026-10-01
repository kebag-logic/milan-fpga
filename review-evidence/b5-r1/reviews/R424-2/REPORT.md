[R424] NEGATIVE - exact head e29d12b1d5ee858eaf4684aaa8dc6647f6309857

Round R424-2, internal independent review of PR #628 (Refs #117, acceptance box 4, the audio continuity row; bench lane B5, evidence only).

- Head `e29d12b1d5ee858eaf4684aaa8dc6647f6309857`, tree `7d56900c21c8ddefb7f95e9830b598201caf4231`.
- Round 1 head `bf9e5d82a401d167a8ffc786677a19dc7aac0cf2`; base dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`.
- The round 2 commit touches `docs/findings/117_AUDIO_CONTINUITY.md` and its index row in `docs/findings/README.md`. Nothing else.
- Assignment: #117 comment 5926598386.
- Evidence: the published archive branch `b5-review-evidence` at `1116f856f881190471e5320de869b9095a1a0537`, under `review-evidence/b5-r1/`:
  - `author/`, unchanged since `ef3a7091`;
  - `author-r2/`, the round 2 packet;
  - the archive's `MANIFEST.json`.

**Verdict basis.** One MINOR is open, F1, so Tests and Docs are UNCLEAN. F1 is a defect in the public archive, not in the head:

- The archive's copy of the round 2 read record is not the record the page cites.
- A redaction pass during publication masked three of its bytes.
- The head needs no change. F1 closes when the archive carries the cited bytes, and a re-check at this same head can then bank the two lenses.

**Round 1 findings.** All five are resolved at this head (table below), and every attribution figure re-derives independently once the record's three bytes are restored. Conformance, RTL and Robustness are CLEAN.

## Round 1 findings, resolved or retained at this head

| Finding | Status at e29d12b1 | Evidence |
|---|---|---|
| R424-1 F1 and R425-1-F1: the attributions | RESOLVED | See the breakdown below. |
| R425-1-F2: reproducible figures | RESOLVED at the head; public reproduction blocked by F1 | See the breakdown below. |
| R425-1-F3: the Direction B reason | RESOLVED | See the breakdown below. |
| R424-1 F2: the controller tool revision | RESOLVED | See the breakdown below. |
| R424-1 S1, S2 and S3 | RETAINED as SUGGESTION, see S4 below | Not in the round 2 assignment's scope. Part of S3 is now met: a published tool computes the content-frame spacings. |

**R424-1 F1 and R425-1-F1, the attributions.**

- *Skips of 60 frames or more.* The page calls them "stall-aligned capture-path loss" at `:22`, `:222-231` and `README.md:20`. With a stall defined as a read interval over 15 ms, 236 of the 239 fall 1 or 2 reads after a stall and none fall 0 reads after. Each of the 220 stalls is followed by exactly one skip of 240 frames or more. The other three (72, 78 and 108 frames) sit in intervals of 11.76 and 12.11 ms.
- *Skips of 2 to 59 frames.* The page splits them at `:233-248` and `:384-387`:
  - 284 skips, 5,386 frames, lie in the 222 clusters that hold a skip of 60 or more. Across those clusters the deficit steps by 116,137.6 frames against 115,314 skipped.
  - The other 237, 1,790 frames, lie in 121 clusters with no stall. Of those, 95 stay within 2.59 frames, 22 step by 1 ms, 4 match neither, and none steps by the frames skipped.
  - The 237 are left unattributed, with both alternatives named.
- *Does the floor test have power where it is applied?* `receipts/plant_probe.txt` plants a capture loss of each cluster's own size at all 121 of those clusters. The test sees it at 121 of 121, so "no capture-path loss of their size" rests on a test that could have failed.
- *One-frame drops.* The page attributes them "by inference" at `:22`, `:25`, `:250-266`, `:379-383` and in the index row, and names a drop at the capture's input as the alternative.
- *The summary table and the index row* carry the same three strengths as the body.
- *Strength of the wording.* The page states each class no more strongly than the published analysis supports. It understates nothing material, apart from S1, which is optional.

**R425-1-F2, reproducible figures.** Each figure was re-derived by `scripts/rederive.py`, which is independent of the author's tool (`receipts/rederive.txt`):

- 236 of 239 under the stated stall definition;
- the stall excess, 109,069.3 frames;
- the recurrence, 3.001 s (2.990 to 3.020);
- 117,653 frames from `window_time`, which is 117,652.9;
- 16.46 ppm, one frame in 60,768 (60,546 to 60,923, one doubled spacing);
- 520 slip events, 514 single and 6 paired;
- 507 of the 521 skips of 2 to 59 frames are multiples of six, and 354 are exactly six;
- 0.370% and 0.347% of the frames.

Neither 115,614 nor 0.8 or 17.3 ppm appears on the page or in the index row. They appear only in the PR body's round 2 notes, as figures it corrected or dropped. On the restored record, the author's `b5_attrib.py figures` reproduces the published `attribution.txt` byte for byte. On the published record its hash check refuses (F1).

**R425-1-F3, the Direction B reason** (`:337-351`).

- The text states only what was observed: four own clusters, a dynamic map within them, and an AUDIO_UNIT with zero external ports, zero internal ports and no routing element.
- I decoded `author/restore/peer-descs-2.jsonl` myself:
  - all 20 walk reads went out as type 0x0010 and answered NO_SUCH_DESCRIPTOR;
  - no 0x0014 read was sent;
  - the audio-unit record shows 0 external input ports and 0 external output ports.
- The walk's codes in `author/tools/b5_ctl.py:153-162` are 0x0011, 0x0012, 0x0010 and 0x0014. `avdecc/aem_descriptors.py:103` gives AUDIO_CLUSTER 0x0014 and AUDIO_MAP 0x0017.
- The walk is marked defective for reuse, as required. The published `b5_records.py` reproduces `records.txt` byte for byte at this head.

**R424-1 F2, the controller tool revision** (`:432-439`).

- The page says the revision that ran the binds and format sets cannot be established. The packet bears this out:
  - `author/restore/controller-start.txt` records `24208ef2…` at 8,642 bytes;
  - `controller-end.txt` records `47b7387a…` at 9,842 bytes, a copy staged at 06:44, after the runs;
  - `author/tools/run_a.py:185-189` starts the staged copy and records no hash of it.
- The second survey carries the audio-unit walk and the first does not, 70.26 s apart (`records.txt`).
- The table row is qualified in the text beneath it.

**Tables.** `scripts/table_diff.py` compares `bf9e5d82` with `e29d12b1` (`receipts/table_diff.txt`):

- 14 of the 15 tables are byte-identical.
- In the summary verdict table only two cells changed: the Evidence cell of the continuity row and the Evidence cell of the "#117 audio continuity row" row.
- Every Item and Verdict cell is unchanged, as is every figure: 334, 520, 1.266 s and 117,104.

**PR and commits.**

- The PR body references #117 only, as "Refs #117", with no closing keyword. GitHub lists no closing issue references.
- There are two commits, each with a one-line message and no trailers.
- Two files changed.

**Public text.** I scanned the page, the index row, both commit messages and the PR body:

- I used a reviewer-side list of 85 host, vendor, product, interface, wiring, connector, channel-map and clock-topology tokens, plus MAC and IPv4 patterns. The list is not published, so that it names nothing.
- There were 0 real hits. The only two matches were inside the word "dynamic".
- No capture channel number, wiring or clock distribution is stated.
- The peer's and the DUT's INTERNAL clock-source selections are device state. The assignment's item 1 names that state as the basis of the inference.

**Docs gates** (`receipts/gates.txt`). All rc 0 at the head:

- `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base e4b771f9` (447 added lines, 0 findings), `check_doc_paths.py` and `gen_toc.py --verify-anchors`, in a disposable environment built from the hash-pinned Markdown lock;
- `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `check_feature_status.py --self-test`;
- `git diff --check`, both forms.

## Findings

**F1 - MINOR - Tests, Docs - the published round 2 read record does not match the record the page cites.**

- *Artifacts.*
  - Published copy: `b5-review-evidence@1116f856:review-evidence/b5-r1/author-r2/receipts/a-long-reads.u16`, blob `0fbea6ef`.
  - The page: `docs/findings/117_AUDIO_CONTINUITY.md:401-405` and `:216-220`.
- *Evidence.* Reproducible with `scripts/published_record_check.py`; output in `receipts/published_record_check.txt`.
  - **Hash.** The published file is 131,540 bytes with SHA-256 `8897abce…`. The page and the packet's own `a-long-reads.json` cite `2183d57f…`.
  - **Manifest.** The archive's `MANIFEST.json` lists the file with `original_sha256` `2183d57f…`, `published_sha256` `8897abce…` and `path_redacted: true`.
  - **The masked bytes.** Byte offsets 114032 to 114034 (read intervals 57016 to 57017) are three `0x23` bytes. The file's gaps sum to 896 µs less than its own `elapsed_us_record`.
  - **The tool refuses it.** The published `b5_attrib.py figures` stops with an AssertionError on the published inputs.
  - **Figures on the published bytes.** With the hash pin moved, the tool's output differs from the published `attribution.txt` in the clear-position control. It finds 10 groups, not 9, and an unexplained −43.3-frame group at reads 57005 to 57021. So the page's "at 9 places" (`:219`) does not re-derive from the archive as published.
  - **What does re-derive.** The 236 of 239, the stall figures and the whole 284/237 split do re-derive from the published bytes (`receipts/rederive.txt`, second block).
  - **Local restoration.** A single three-byte restoration satisfies both the record's own sum and the cited SHA-256. On it, the author's tool reproduces `attribution.txt` byte for byte. The restored bytes are withheld here and were not published, because the publication's redaction matched them.
- *Impact.*
  - A cold reviewer working from GitHub alone cannot reproduce the record the page cites.
  - The published tool refuses the published input.
  - One page figure, and the meaning of the read-time record at one position, differ from the archive.
  - This is exactly the reproducibility that R425-1-F2 required.
- *Required outcome.* The archive must let a cold reviewer re-derive every page figure from published bytes. Either:
  - the archived record hashes to `2183d57f…`, because binary receipts are kept out of text redaction; or
  - the archive states the masked range and gives a way to recover the cited record that the manager accepts as consistent with the redaction's purpose.
  
  No change to the head is needed.
- *Verification:*
  1. `scripts/published_record_check.py` on the re-archived `b5-r1` shows the published hash equal to the cited one.
  2. The unmodified author tool then reproduces `attribution.txt`.

**S1 - SUGGESTION - Conformance, Docs - `:242-248`, `:384-390` - say where the 1 ms steps fall.**

The page says that in 22 of the 121 stall-free clusters the deficit steps by 1 ms, and that the 1 ms steps are unexplained. It does not say how much more often they occur at those clusters than elsewhere:

| Where | 1 ms steps | Steps over 4 frames |
|---|---|---|
| The 121 stall-free clusters | 22 (18%) | 26 |
| 3,240 non-overlapping clear spans | 6 (0.19%) | 7 |

That is about a hundred times the background rate (`receipts/rederive.txt`). So a capture-side delivery event coincides with about a fifth of those clusters, even though no step equals their size. Stating this would stop "the record shows no capture-path loss of their size" from being read as evidence against the capture path. The page's conclusion, that these skips are not attributed, stands either way.

**S2 - SUGGESTION - Docs - `:345-351` - the survey walk's map reads.**

"It read … the maps with 0x0014" describes the tool's code. No map read was sent, because both stream ports declare 0 static maps, and all 20 walk reads are type 0x0010. Saying so, as the next sentence already does for the external-port reads, would match the record exactly.

**S3 - SUGGESTION - Docs - `:227-228` - what "those skips" covers.**

"109,069 frames, against 109,928 in those skips" counts all 239 skips of 60 frames or more, which includes the three skips not aligned with a stall (258 frames). The 236 aligned skips hold 109,670.

**S4 - SUGGESTION, retained from round 1 - R424-1 S1, S2 and the rest of S3.**

- The forward pointers from the #117 ledger and the #75 index row. This stays the manager's call, because the assignment froze the output.
- Citing the standing free-run acceptance rule for the INTERNAL beat at `:29-33`.
- Stating the order criterion as 0 backward steps.
- The ordinals around the six skip, zero, skip events.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Sources: #117 body, boxes 4 and 5; the B5 assignment (5925737609) and the round 2 assignment (5926598386); R424-1 and R425-1 findings, each resolved above. Page: `:18-33`, `:179-268`, `:335-355`, `:373-395`, `:429-446`. Also `README.md:20`. Commands: `scripts/rederive.py` on the restored record and `scripts/plant_probe.py`. Packet inputs: `author/restore/peer-descs-2.jsonl`, `controller-start.txt`, `controller-end.txt`, `author/tools/run_a.py:185-189`. | R424-2 | `e29d12b1d5ee858eaf4684aaa8dc6647f6309857` |
| RTL | CLEAN | No RTL in the diff (`git diff --stat e4b771f9..e29d12b1`: two Markdown files). The page's DUT-behaviour claims still anchor at this head: `hdl/ieee1722/aaf/KL_chan_map_capture.sv:452-453,1024-1033` (dup and skip counters), `docs/reference/REGISTER_MAP.md:134,242` (`SLIP_TDM`), `docs/design/TIME_SYNC.md:463,478` (the 1.958 s beat), `docs/litex/CLOCK_DOMAINS.md:169`. | R424-2 | `e29d12b1d5ee858eaf4684aaa8dc6647f6309857` |
| Robustness | CLEAN | Edge and failure handling of the new analysis: the window-edge clusters (0), the stall-free clusters (0 stalls within), the doubled slip and beat spacings, and the zero frames in content positions (`receipts/rederive.txt`). The tool's hash refusal on altered input. Planted losses at the real cluster positions, 121 of 121 detected (`receipts/plant_probe.txt`). The author's 7-set parameter sweep (`author-r2/receipts/attribution_sensitivity.txt`): the stall-free split keeps the same shape. | R424-2 | `e29d12b1d5ee858eaf4684aaa8dc6647f6309857` |
| Tests | UNCLEAN (F1 open) | `author-r2/tools/b5_attrib.py`, run on the published and on the restored record (`receipts/published_record_check.txt`). `b5_records.py`, rerun with output byte-identical. The independent re-derivation `scripts/rederive.py` and the floor-test power probe `scripts/plant_probe.py`. The table comparison `scripts/table_diff.py`. | R424-2 | `e29d12b1d5ee858eaf4684aaa8dc6647f6309857` |
| Docs | UNCLEAN (F1 open) | `docs/findings/117_AUDIO_CONTINUITY.md` (all 446 lines) and `docs/findings/README.md:20`. Docs gates, all rc 0 (`receipts/gates.txt`). Table identity (`receipts/table_diff.txt`). The public-text scan of the page, the index row, the commits and the PR body. PR references and commits. Archive `MANIFEST.json` and `author-r2/MANIFEST.sha256`: 2 of 34 listed hashes differ in the archive, the record and `receipts/gates/gates.txt`; the latter is a disclosed path redaction of text. | R424-2 | `e29d12b1d5ee858eaf4684aaa8dc6647f6309857` |

## Real limits

- The raw capture, the read-time file and the raw graded pair stay local by design.
  - The derived record, and the whole-run counts in `a-long-wholerun.json`, are taken as the author's receipts of those files, identified by size and SHA-256.
  - The whole-run counts are consistent with each other (3,407,496 zero frames by place) but were not recomputed from bytes.
- The three-byte restoration behind F1's "local restoration" claim was verified only in the reviewer's unpublished working area. It is unique under the record's own sum constraint and the cited hash. It is not in this packet.
- There was no hardware or bench access. Physical calibration was NOT RUN, and every rate is on an uncalibrated host clock.
- The hosted `docs-check` context was still in progress when read.
  - `rtl-fast`, `full-ci-gate`, `docs-check-no-git`, `bdd-conformance`, `elaborate`, `wire-accountability` and `changes` succeeded.
  - The Verilator, Yosys and physical contexts were skipped for this docs-only scope (`receipts/hosted_checks.txt`).
- The pinned Markdown lock was installed in a disposable environment outside the clone. No full bank was run.
- The clone was not modified (`receipts/clone_integrity.txt`):
  - HEAD and the index tree equal `7d56900c…`;
  - 0 changed, untracked or ignored paths;
  - all four gitlinks are at HEAD's pins (`external` is uninitialised, as CONTRIBUTING expects).

## Pending manager duties

- F1: re-archive the round 2 read record so that the public bytes hash to the page's cited value, or publish an accepted recovery note. Then a re-check at this same head.
- Hosted and act acceptance at the exact head, including the in-progress `docs-check`.
- The final current-dev candidate at the merge turn. The source base and live dev were both `e4b771f9` when this review ran.
- The external review's verdict.
- The decisions S4 leaves with the manager.

R424-2 FINISHED
