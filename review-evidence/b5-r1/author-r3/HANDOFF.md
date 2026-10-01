# [A474] B5 round 3 handoff (PR #628, #117 box 4)

Refs #117. Round 3 assignment: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5927406852
Reviews answered: R424-2 (https://github.com/kebag-logic/milan-fpga/pull/628#issuecomment-5927400045) and R425-2 (https://github.com/kebag-logic/milan-fpga/pull/628#issuecomment-5927386225). F1 note: https://github.com/kebag-logic/milan-fpga/pull/628#issuecomment-5927406516

## State

- Head `cf38633ad9a5bdb05517bedba73ce50965af967b` on branch `b5-bench-1001`, parent `e29d12b1d5ee858eaf4684aaa8dc6647f6309857` (the round 2 head), base dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`.
- One new commit: a one-line subject with no body and no trailers, touching `docs/findings/117_AUDIO_CONTINUITY.md` (+93 -35) and its index row in `docs/findings/README.md`. It is local only: nothing was pushed, and no PR was created or edited.
- Worktree clean. The only ignored path is `scripts/__pycache__/`, present before this round and left as found.
- No bench access: no console, JTAG, power strip, tap, controller host or DUT, and no bench lock. Nothing was written to the NAS. No existing comment was edited or deleted. No other checkout was made.
  - The public archive's files were fetched read-only through the API, at `b5-review-evidence@2a40015e`, into a scratch directory outside this packet.
  - The local raw graded pair (`a-long/cap-lr.raw`, sha256-checked) was read for the zero-frame ordinals. It stays local.
- TAKEN posted 08:08:46Z: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5927421686 (`TAKEN.md`, `taken-url.txt`, readback `TAKEN.readback.md`). The readback equals the posted file but for one trailing newline.
- REVIEW READY posted 08:25:23Z with head `cf38633a`: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5927651571 (`REVIEW-READY.md`, `review-ready-url.txt`, readback `REVIEW-READY.readback.md`). The readback equals the posted file but for one trailing newline. The lane stops here.

## The change (file:line at `cf38633a`)

`docs/findings/117_AUDIO_CONTINUITY.md`:

- `:11-13`: round 3 provenance line.
- `:25`: the summary's continuity Evidence cell (item 3). It now reads "236 of the 239 of 60 or more are stall-aligned capture-path loss, and the other three, of 72, 78 and 108 frames, are not stall-aligned". The Item and Verdict cells are unchanged, and every old figure is kept.
- `:27`: the summary's Direction B Evidence cell (item 1). It now says it was not established whether a known signal can reach the peer's talker channels without a wiring change, because the descriptors naming each cluster's signal source were not read, the survey walk being defective. The verdict stays NOT RUN.
- `:36-39`: the free-run acceptance citation, R424-1 S2 under R424-2 S4. It links to the register map's slip counters (`REGISTER_MAP.md` 0x8D4), which record the 1.958 s beat as "the standing free-run rule, slips accepted".
- `:126-128`, `:181`: the order criterion, R424-1 S3 under R424-2 S4. Steps are modulo 65,536, and 32,768 or more is backward. "In order" means 0 backward steps, and the window has 0 (`summary.json` `backward: 0`).
- `:203-207`: F1. Round 3's packet and tool, and the `gunzip -kf` step before either tool runs.
- `:231-233`: R425-2 S3. The planted control is linear by construction, so it checks where the floor windows sit, not the test's power.
- `:238-250`: item 3. The heading reads "236 of the 239". The 236 hold 109,670 frames, and the other three are named, 258 frames: 72 frames at 34.0 s into the window, and 78 and 108 frames on consecutive reads at 634.0 s. The stall excess, 109,069 frames, is compared with the 109,670, and all 239 hold 109,928.
- `:268-272`: item 4. The 1 ms steps concentrate at the 121 off-stall clusters, 22 against about 0.26 by chance. That rate is 7 steps over 51,828 clear positions, 3,239.25 windows of 16 reads. It is stated as an observation, not attributed.
- `:283-287`: the ordinals around the six skip, zero, skip events, R424-1 S3 under R424-2 S4. Each zero frame sits between consecutive ordinals, so each event drops two frames and inserts one: one frame fewer.
- `:369-379`: item 1. The Direction B reason. The lane rule; what was observed; the AUDIO_CLUSTER `signal_type`, `signal_index` and `signal_output` fields (IEEE 1722.1 7.2.16) not read because the walk is defective; so the question is open. "Not visible over AEM" and "would therefore need an instrument or wiring change" are gone.
- `:381-391`: item 2. What the walk's code reads, and what it sent: 20 reads of type 0x0010 at indices 0 to 19, each NO_SUCH_DESCRIPTOR. It sent no map read (both ports declare 0 static maps) and no external port read. The dynamic maps came from GET_AUDIO_MAP.
- `:415-416`: Limits. The 0.35% share names "the 236 stall-aligned skips": 109,670 frames, 0.346%. The share of all 239 is 0.347%, so the printed figure is unchanged.
- `:430-431`: Limits, item 4. The 1 ms steps concentrate at the 121 off-stall clusters.
- `:446-456`: F1. The reproduction steps: `gunzip -kf`, the hash check, `b5_attrib.py figures`, then `b5_round3.py figures`.
- `:498-504`: the round 3 tool and its SHA-256.

`docs/findings/README.md:20`: the index row now says "236 of the 239 skips of 60 frames or more are stall-aligned capture-path loss" (item 3, R425-2 S2).

## Items

- **F1 (R424-2 F1, R425-2 F1).** Resolved by the manager's republication. The page now carries the `gunzip` step. `receipts/f1_reproduction.txt` shows the whole path from the public archive alone:
  - `gunzip -kf` restores 131,540 bytes with SHA-256 `2183d57f…`;
  - the published `b5_attrib.py` (`f1d9b2ba…`) then reproduces the archive's `attribution.txt` byte for byte;
  - `b5_round3.py figures` reproduces `receipts/round3_figures.txt`.
- **Item 1, R425-2 F2.** Done at `:27` and `:369-379`, worded as the assignment gives it. NOT RUN stays.
- **Item 2, R424-2 S2.** Done at `:381-391`. `receipts/round3_figures.txt` section D tallies the 57 exchanges by command and type: 55 READ_DESCRIPTOR and 2 GET_AUDIO_MAP. Types 0x0011, 0x0012, 0x0014 and 0x0017: 0 each. Both ports have `number_of_maps` 0, and the audio unit has 0 external ports.
- **Item 3, R424-2 S3, R425-2 S2.** Done at `:25`, `:238-250`, `:415-416` and `README.md:20`. Section A gives the 236 (109,670 frames, lags 1: 130, 2: 106), and the three others with position, read interval and the nearest stall (125, 127 and 128 reads).
- **Item 4, R424-2 S1, R425-2 S1.** Done at `:268-272` and `:430-431`. Section B: 22 of 121; 7 one-millisecond groups over 51,828 clear positions; 51,828 / 16 = 3,239.25 windows; expected 0.26.
- **Item 5.**
  - R425-2 S3, taken (`:231-233`). Section C: a plant at the same 300 positions reads back as the unplanted step plus the plant, with the largest difference 0.00 frames for 6, 12 and 24.
  - R424-2 S4, the round 1 suggestions it retained:
    - R424-1 S2, the free-run rule, taken (`:36-39`). Only the register map is cited. `CHANNEL_MAP_64.md:229`, which R424-1 also named, describes the render-side pins, not this capture path.
    - R424-1 S3, the order criterion, taken (`:126-128`, `:181`).
    - R424-1 S3, the ordinals, taken (`:283-287`; `receipts/zero_frame_ordinals.txt`). The receipt also checks that the window's 31,569,599 transitions equal in order, repeats, skips, backward and the 12 next to a zero frame.
    - R424-1 S1, the forward pointers from `117_GPTP_SILICON_EVIDENCE.md:59` and `README.md:14`, retained. Those are other pages' rows. The B5 assignment fixed the output as this page and its index row, and round 3 did not extend it, so this stays the manager's call.
    - R424-1 S3's third bullet, the content-frame spacings, was already met in round 2, as R424-2 records.

## For the manager: the archive note's command

`author-r2/receipts/a-long-reads.NOTE.md` (archive `2a40015e`) says to restore the record with `gunzip -k a-long-reads.u16.gz`. The masked `a-long-reads.u16` (`8897abce…`) still sits beside the `.gz` there. With it present, `gunzip -k` prints "already exists; not overwritten", exits rc 2 and leaves the masked copy (`receipts/f1_reproduction.txt`).

The page therefore says `gunzip -kf`, and says why. Either the note's command or the masked copy needs changing, and the archive is the manager's. Nothing here edited it.

## Table byte-identity proof

`receipts/table_identity.txt` runs the round 2 packet's unchanged `b5_table_proof.py` (`5eb78c7f…`) on `e29d12b1` against `cf38633a`. It adds three literal `diff`s:

- every table line of the page, `e29d12b1` against `cf38633a`;
- table lines 9 onward against round 1's `bf9e5d82`;
- the index table.

Results:

- 14 of the page's 15 tables are byte-identical, with 119 table lines at both heads.
- The one changed table is the summary verdict table. It changes in two Evidence cells: the continuity row (item 3) and the Direction B row (item 1). In both rows the Item and Verdict cells are identical, and no figure of the old cell is missing from the new one.
- Every table after the summary verdict table, all the measurement tables, is byte-identical to round 1 as well (`diff` rc 0).
- In the index, one row changes: the 117_AUDIO_CONTINUITY.md row's result cell, with no old figure missing.

## Public-text token scan

`receipts/token_scan.txt` runs the round 2 packet's unchanged `b5_token_scan.py` (`baf199fd…`) twice: over the round 3 range `e29d12b1..cf38633a` and over the whole PR range `e4b771f9..cf38633a`. Both runs cover every file in this directory and the range's added lines and commit messages. The patterns are:

- the round 1 private redaction map (26 literal and 6 regular-expression entries: hosts, interfaces, MACs, clock and entity identities, instruments and the peer);
- MAC addresses and home directories;
- a private list, kept out of this packet, of capture channel numbers, clock-topology words, agent tool and model names, the peer's decoded name, and the local account, the commit account, the posting account and the host name.

Result: 0 hits in both runs. They covered every file in this directory as finally written (the posted texts and their readbacks included, but not `MANIFEST.sha256`, which holds only paths and hashes). They also covered 94 added lines and the commit message of round 3, and 505 added lines and 7 commit-message lines of the whole PR.

- A positive control in scratch planted the host name, a home path, the commit, posting and local account names and a MAC address. It drew 9 hits. A check in memory confirmed the agent tool and model name patterns.
- No capture channel number, wiring, instrument identity, channel map or clock topology is stated in the diff or here. The peer's INTERNAL clock-source selection and the SoC board's McASP0 are round 1 text that both round 2 reviews accepted.

## Gates

`receipts/gates/gates.txt`, at `cf38633a` from the physical lane path. Each command's output is in `gate-<n>.txt`. All 12 are rc 0, none piped:

- `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base e4b771f9` (0 findings over 505 added lines) and `check_doc_paths.py`, in the pinned Markdown environment;
- `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py --check` and `scripts/check_feature_status.py --self-test`;
- `git diff --check`, `git diff --check e4b771f9 HEAD` and `git diff --check e29d12b1 HEAD`;
- `gen_toc.py --verify-anchors`, which covers the new `REGISTER_MAP.md` fragment link.

## Open risks and questions

- Direction B is now explicitly open. A read-only AUDIO_CLUSTER read with type 0x0014 would show each cluster's named source. That needs a lane with bench access and a decision.
- The three skips of 60 frames or more that no stall precedes are named and not attributed. Each sits in a read interval stretched by about its own duration (1.76 to 2.11 ms against 1.50 to 2.25 ms). That is an observation only.
- The 1 ms steps' concentration is stated without attribution, as item 4 requires. Their cause is open.
- The archive note's `gunzip -k` (above) is the manager's to fix.
- Hosted CI, act, the PR body edit and the push are the manager's: nothing was pushed.

## Output layout

| Path | What |
|---|---|
| `TAKEN.md`, `taken-url.txt`, `REVIEW-READY.md`, `review-ready-url.txt`, `*.readback.md` | posted texts, their URLs and the API readbacks |
| `PR-BODY.md` | proposed PR body: the [A472] first line and the "Refs #117" line kept, the result rows matched to the head, and a Round 3 section |
| `tools/b5_round3.py` | round 3 figures (published inputs only) and the zero-frame ordinals (local raw pair) |
| `receipts/round3_figures.txt` | sections A to D: the 236/3 split, the 1 ms concentration, the planted control's linearity, the walk's reads |
| `receipts/zero_frame_ordinals.txt` | ordinals around the six window zero frames, and the transition identity |
| `receipts/f1_reproduction.txt` | the reproduction from the public archive, with `gunzip -k` and `gunzip -kf` |
| `receipts/table_identity.txt` | the table byte-identity proof |
| `receipts/token_scan.txt` | the label-only private-name scan |
| `receipts/gates/` | `gates.txt` and each gate's output |
| `MANIFEST.sha256` | SHA-256 of every file here but itself, written last, with relative paths only |

Nothing here is over 200 KB, and there is no toolchain, virtual environment or tree export. The record itself is not copied here: it is the round 2 packet's, identified by its SHA-256.
