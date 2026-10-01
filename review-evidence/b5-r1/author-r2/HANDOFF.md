# [A473] B5 round 2 handoff (PR #628, #117 box 4)

Refs #117. Round 2 assignment: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5926598386
Reviews answered: R424-1 (https://github.com/kebag-logic/milan-fpga/pull/628#issuecomment-5926590622) and R425-1 (https://github.com/kebag-logic/milan-fpga/pull/628#issuecomment-5926558221).

## State

- Head `e29d12b1d5ee858eaf4684aaa8dc6647f6309857` on branch `b5-bench-1001`, parent `bf9e5d82a401d167a8ffc786677a19dc7aac0cf2` (the round 1 head), base dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`.
- One new commit with a one-line subject, no body and no trailers. It is local only: not pushed, and the PR is not edited. An earlier local version of the same commit, `12ffaca1`, was amended before anything was published.
- Worktree clean. The only ignored path is `scripts/__pycache__/`, written by round 1's gate runs (08:49 to 08:51 CEST) and left as found.
- No bench access: no console, JTAG, power strip, tap, controller host or DUT, and no bench lock. Nothing was written to the NAS. No existing comment was edited or deleted.
- TAKEN posted 07:17Z: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5926614985 (`TAKEN.md`, `taken-url.txt`, readback `TAKEN.readback.md`).
- REVIEW READY posted with head `e29d12b1`: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5927093074 (`REVIEW-READY.md`, `review-ready-url.txt`, readback `REVIEW-READY.readback.md`). Each readback equals the posted file but for one trailing newline. The lane stops here.

## The change (file:line at `e29d12b1`)

`docs/findings/117_AUDIO_CONTINUITY.md`:

- `:8-10`: round 2 provenance line.
- `:22`, `:25`: the summary verdict table's Evidence cells for the continuity row and the row verdict. The causes are now stated at the assignment's strength. The Item and Verdict cells and every figure are unchanged.
- `:176-177`: whole-run zero frames include the window's six; the counts are derived by the round 2 packet.
- `:190-194`: the window deficit corrected to 117,653 frames, from `summary.json`'s `window_time`; it replaces 2.4 s "lost by the capture path". Pointer to the analysis.
- `:203-220`: how the read-time record places a loss. The stall definition (read interval over 15 ms), the recurrence (3.00 s, 2.99 to 3.02 s), the floor test and its controls.
- `:222-231`: skips of 60 frames or more, stall-aligned capture-path loss. 236 of 239 now carries a stated definition, and 109,069 against 109,928 is reproduced. The irreproducible 115,614 drift and the examples are gone.
- `:233-248`: skips of 2 to 59 frames, not separated (item 1, and see the finding below).
- `:250-266`: one-frame skips, attributed to the peer's output rate by inference. 16.46 ppm (one frame in 60,768); the capture-input alternative is named. The absolute 0.8 and 17.3 ppm figures are dropped.
- `:337-351`: Direction B states only what was observed (item 3), and the survey walk is marked defective for reuse.
- `:375-390`: Limits. The loss share is split (0.37% in all, 0.35% stall-aligned); the inference and its alternative; the unattributed off-stall skips; the floor test's assumption and resolution.
- `:401-405`: the round 2 packet and the derived read record's identity.
- `:432-446`: the controller tool revision cannot be established (item 4), and the round 2 tools' hashes.

`docs/findings/README.md:20`: the index row now carries the three causes at the assignment's wording.

## Items

1. **Attributions (R424-1 F1, R425-1 F1).**
   - Skips of 60 frames or more: stall-aligned capture-path loss.
   - Skips of 2 to 59 frames: not separated from a packet-sized drop downstream of the peer's receive counters.
   - One-frame drops: attributed to the peer's output rate by inference, from the period and the INTERNAL clock source. A drop at the capture's input is named as the alternative.
   - The index row and summary rows match. The page states no wiring, channel map or clock topology; the INTERNAL clock-source selections were already on the page, and both reviews accepted them as device state.
2. **Reproducible figures (R425-1 F2).** `tools/b5_attrib.py` has two parts.
   - `derive` reads the local raw read-time file (sha256-checked) and writes `receipts/a-long-reads.u16` (131,540 bytes) and `receipts/a-long-reads.json`: per-read times in whole microseconds, with no accumulated rounding error.
   - `figures` computes every attribution figure from published inputs only: the round 1 packet's `summary.json`, `continuity-events.csv` and `events.jsonl`, plus the derived record. Output: `receipts/attribution.txt`.
   - `wholerun` derives the whole-run integrity counts from the raw pair (`receipts/a-long-wholerun.json`).
   - Reconciliation: 115,614 is not reproduced. The deficit is 117,652.9 frames on `window_time`, and 117,652.1 from the boundary reads. The page now says 117,653.
3. **Direction B (R425-1 F3).** `tools/b5_records.py` writes `receipts/records.txt`, which shows:
   - the peer's AUDIO_UNIT 0 declares no external or internal port and no routing element;
   - STREAM_PORT_OUTPUT 0 owns 4 clusters, and its dynamic map draws only from them;
   - the configuration's one CONTROL is IDENTIFY;
   - the walk's four type codes (`b5_ctl.py:153` external ports, `:160` clusters, `:162` maps) are wrong against IEEE 1722.1 Table 7.1 as `avdecc/aem_descriptors.py:103` encodes it.

   The walk is marked defective for reuse; the round 1 tool is not altered.
4. **Controller revision (R424-1 F2).** `receipts/records.txt` shows the sequence:
   - the start snapshot staged and hashed `24208ef2` (8,642 bytes), and its survey (06:14:57Z) had no audio-unit walk;
   - the survey at 06:16:07Z carries the walk, so the controller copy changed with no hash recorded;
   - the run tool records none;
   - the end snapshot re-staged and hashed `47b7387a`.

   So the executed revision cannot be established, and the page says so. The binding rule audit rests on the logged exchanges.

## Finding beyond the wording (needs owner attention)

The read record separates the 2-to-59 class in part, and in the direction that weakens the capture-path attribution. A frame lost inside the capture path after sampling delays every later read, so the capture's delivery deficit steps by the frames lost.

- **Stall clusters.** 284 smaller skips (5,386 frames) sit in the 222 clusters that hold a skip of 60 or more. There the deficit steps by 116,138 frames against 115,314 skipped. That is consistent with capture-path loss in aggregate.
- **Away from stalls.** 237 smaller skips (1,790 frames) sit in 121 clusters away from any stall. None comes with a deficit step of its size:
  - 95 clusters (skips of 12 to 36 frames each) stay within 3 frames;
  - 22 step by 1 ms;
  - 4 match neither.
- **Controls.**
  - 267 beat repeats and 419 one-frame skips stay within 3.2 frames.
  - Planted 6, 12 and 24-frame losses are recovered within 5.
  - Over 51,828 clear positions there are 9 steps over 4 frames, 7 of them 1 ms steps with no frame missing.
- **Robustness.** Unchanged over 7 parameter sets (`receipts/attribution_sensitivity.txt`).

So the off-stall skips are not attributed. Whether a lossless capture path removes them is open, and the page's Limits and the PR body say so.

## Table byte-identity proof

`tools/b5_table_proof.py` writes `receipts/table_identity.txt`, which also carries a literal `diff` of every table line at `bf9e5d82` against `e29d12b1`. 14 of the page's 15 tables are byte-identical, and 119 table lines remain 119.

The only changed table is the summary verdict table, in two Evidence cells: the continuity row and the row verdict. Their Item and Verdict cells are identical, and no figure of the old cells is missing from the new ones. Item 1 requires this change, as does R425-1 F1's required outcome for lines 19 and 22. No measurement table changed.

## Public-text token scan

`tools/b5_token_scan.py` writes `receipts/token_scan.txt`. It scans every file in this directory, the lines added in `e4b771f9..e29d12b1` and the commit messages. The patterns are:

- the round 1 private redaction map's 26 literal and 6 regular-expression entries;
- MAC addresses and home directories;
- a private list, kept out of the published tool, of capture channel numbers, clock-topology words, agent tool and model names, and the peer's decoded name.

Result: 0 hits over 34 files (this directory as finally written), 447 added diff lines and 5 commit-message lines. The posted TAKEN and REVIEW READY texts and their readbacks are files here, so they are covered. A direct check for the bare account, posting-account and host names also found none, in this directory and in the diff.

## Gates

`receipts/gates/gates.txt`, at `e29d12b1` from the physical lane path; each command's output is in `gate-<n>.txt`. All 11 are rc 0 and none was piped:

- `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base e4b771f9` and `check_doc_paths.py` (pinned Markdown environment);
- `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py --check` and `scripts/check_feature_status.py --self-test`;
- `git diff --check` and `git diff --check e4b771f9 HEAD`;
- `gen_toc.py --verify-anchors`.

## Open risks and questions

- The off-stall 2-to-59 finding changes the follow-up: placing those skips, between the peer's receive counters and the capture's input, needs a decision.
- The floor test assumes a capture whose sampling runs continuously. It resolves about 4 frames, and the 1 ms steps are not explained.
- Hosted CI, act and the PR body edit are the manager's: nothing was pushed.
- The raw read-time file and the raw pair stay local; only the derived record and counts are here.

## Output layout

| Path | What |
|---|---|
| `TAKEN.md`, `taken-url.txt`, `REVIEW-READY.md`, `review-ready-url.txt`, `*.readback.md` | posted texts, their URLs and the API readbacks |
| `PR-BODY.md` | proposed PR body: the [A472] first line and the "Refs #117" line kept, plus a Round 2 section |
| `tools/b5_attrib.py` | derive, figures and wholerun |
| `tools/b5_records.py` | controller revision and descriptor records |
| `tools/b5_table_proof.py` | table byte-identity proof |
| `tools/b5_token_scan.py` | label-only private-name scan |
| `receipts/` | derived read record and its JSON, `attribution.txt`, `attribution_sensitivity.txt`, `a-long-wholerun.json`, `records.txt`, `table_identity.txt`, `token_scan.txt`, `derive.txt`, `gates/` |
| `MANIFEST.sha256` | SHA-256 of every file here but itself, written last; it holds only relative paths and hashes |

Nothing here is over 200 KB. The largest file is the derived read record at 131,540 bytes.
