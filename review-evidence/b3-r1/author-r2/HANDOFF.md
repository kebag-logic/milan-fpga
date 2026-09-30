# [A456] Bench lane B3, round 2 handoff (PR #624)

Refs #617 (acceptance 4). Refs #451 (capture through the USB Audio device; continuity check).

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5904487454
- Round-1 reviews: R414-1 (PR #624 comment 5904469593, three MINOR) and R415-1 (PR #624 comment 5904480629, one MINOR, four suggestions). Both are NEGATIVE on documentation only.
- Branch: `b3-bench-0930`, lane worktree on the physical `/data` path. Base head `6dfa64a7506a8660a70d77eaa7c96c5de2886f5d`, new head `a66996aae46bc4a3eb2d8a4822d12d5186aa04eb` (tree `e45645cd5599cbfad06d0dc44e11c2a35caee56e`).
- Documentation only. No bench, console, JTAG, power, tap, controller-host or DUT access; the bench lock was not taken. No NAS write. No push, PR creation, PR edit or merge.

## State

- TAKEN posted: https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5904494199. `TAKEN.md` is the posted text; `TAKEN.readback.md` is the API readback, identical but for one trailing newline.
- Commit `a66996aae46bc4a3eb2d8a4822d12d5186aa04eb`: one commit on `6dfa64a7`, one-line subject, no body, no trailers. Local only, not pushed. The worktree is clean. The ignored `scripts/__pycache__/` was already there from the round-1 gate run, and is left as found.
- REVIEW READY posted for `a66996aa`: see [Posting](#posting). DONE; the lane stops.

## Items (file:line at `a66996aa`)

| Item | Source | Change | State |
|---|---|---|---|
| 1. Index | Ruling on R414-1 F1 and R415-1 F1 | `docs/findings/README.md:12` adds a row for `451_USB_AUDIO_CAPTURE.md`, and `:13` one for `617_DIN_FRAME_COHERENCE_BENCH.md`. They sit directly after the first-light row they follow up, in file-name order, the placement PR #622 used for its 606 and 608 rows after the 75 row. `:11`: the first-light row keeps its text and its State now points at the `ec0cc0c1` DIN re-run (0 torn) and the USB Audio capture FAIL, as PR #622 did for its row | DONE |
| 2. McASP0 rate | R414-1 F2 | `docs/findings/451_USB_AUDIO_CAPTURE.md:126-127`: 250.7 becomes 250.0 periods/s. `:129-133` state the bracket: 18,942 and 18,957 periods in 75.78 s and 75.83 s, between the same uptime read of the before and after status logs, 47,992 and 47,999 frames/s. Packet `packet/HANDOFF.md:30` (step 5) is corrected, and `:62` records the correction | DONE |
| 3. Packet locator | R414-1 F3 | `docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md:275-278` and `docs/findings/451_USB_AUDIO_CAPTURE.md:216-219` name `review-evidence/b3-r1/author/` on branch `b3-review-evidence`. The lane-private packet name is dropped | DONE |
| 4. Torn-count scope | R415-1 S1 | `docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md:107-112`: the rule reads only pattern words, so the whole-recording count covers the frames that carry them, which are the region's. `:158-161`: frame 45,587 and the 777 transition frames after the region are graded by inspection | DONE |
| 5. Identity chain | R415-1 S2 | `docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md:54-58`: VERSION, AEM CRC32, entity ID and ROM CRC32 are unchanged from `13eda870` (the #606 page's readback); only the QSPI payload CRC32 differs. `:61-63`: the lane packet does not hold the `ec0cc0c1` build's own payload CRC32, so `d178f19a` stays recorded as read | DONE; the build CRC is not in the packet |
| 6. `nvm_pend` | R415-1 S3 | `docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md:239-243`: commits, slots, `VD_OK`, `dirty=0`. `:244-252`: `pend=1` and `PP_STAT` bit 11 are one wire (`PP_NVM_STAT[22]`, `PP_STAT[11]`, REGISTER_MAP `0x920`). A channel-map write holds it until reset (SAVED_STATE_SNAPSHOT_OWNERSHIP section 11, records `0x60` to `0x7F`), so a next lane that needs the durable reading must reset the DUT first | DONE |
| 7. Frame 1,632 | R415-1 S4 | `packet/summary/usb-long-frame-1632.json` and `packet/summary/summary.json` (`usb[0].first_non_silent_frame`): `016ec820 026ec838 036ec850 046ec868 056ec878 066ec890 076ec8a8 086ec8c0`. That is one ordinal, `0x6ec8`, in slot order, with low bytes `0x20` to `0xc0`, as the page states. Read by `packet/tools/usb_frame_words.py` from the raw `usb-long` capture, whose SHA-256 is checked against the page, `7995b44a…d7ca`, 115,200,000 B. Frame 1,632 is the grader's `first_non_silent_frame`, zero-based, byte offset 52,224 | DONE |

Not assigned, so not done: R414-1's suggestions S1 to S3. S1 and S2 overlap items 5 and 6, and S3 is the attribution wording at `451_USB_AUDIO_CAPTURE.md:154-161`.

## Byte-identical table proof

- `receipts/table-diff.txt` comes from `scripts/table_diff.py` over `6dfa64a7` and `a66996aa`, pairing every table by order.
  - `617_DIN_FRAME_COHERENCE_BENCH.md`: 12 of 12 tables IDENTICAL. Each is listed with its bytes and SHA-256, including the generated `din-run`, `din-channels`, `dout-run` and `dout-channels` tables.
  - `451_USB_AUDIO_CAPTURE.md`: 7 of 8 IDENTICAL, including the generated `usb-runs` and `usb-detail` tables. Table 5, the bridge-side table at `:124-127`, is CHANGED only in the two rate cells that item 2 corrects.
  - `README.md`: the index table changes by item 1.
- `receipts/table-lines-diff.txt` runs `diff <(git show 6dfa64a7:<page> | grep '^|') <(git show a66996aa:<page> | grep '^|')`.
  - #617 page: diff rc 0. 85 table lines, SHA-256 `a2f63c3a…7b48` at both heads.
  - #451 page: only the two `usb-long` and `usb-long2` bridge-side lines differ. `cmp -l` shows exactly 2 bytes (offsets 2656 and 2849, `7` to `0`), at 3,994 bytes on both sides.
- Why one table cell moves: the assignment keeps the measurement tables byte-identical and also requires the McASP0 rate correction, which sits in that table. The change is the smallest that meets both. It is disclosed in the PR body and in REVIEW READY.

## Token scan

- `scripts/private_scan.py` scans for private names and never prints one; each hit reports only file, line and label. Its token sources are read at run time:
  - the round-1 lane's private redaction map (20 literals, 3 patterns, 14 check strings);
  - the private endpoint file's values;
  - this host's name, the account name, every interface name and hardware address, and the EUI-64 clock identity of each address;
  - 16 run-time patterns for agent tool, model and vendor names and absolute home paths, passed in the environment so that no written file names them.
- Positive controls: a host name, a home path and a hardware address fed on standard input give 3 hits and rc 1. Every redaction-map literal fed the same way is detected, rc 1.
- Result: `receipts/private-scan.txt`, from the final run after this file's last edit. It covers this whole directory, the round-2 commit diff `6dfa64a7..a66996aa` and the commit subject, with 0 hits.

## Gates (at `a66996aa`, rc 0 each, unpiped, physical `/data` path)

`receipts/gates/gates.txt` lists all 11 invocations, and `gate-<n>.txt` holds each output.

- Pinned Markdown environment:
  - `docs_check.py`: 0 findings across 181 md files.
  - `check_doc_style.py`: OK.
  - `gen_toc.py --check`: OK.
  - `check_em_dash.py --base ec0cc0c1`: 0 findings over 512 added lines in 3 pages.
  - `check_doc_paths.py`: 860 paths.
- `ci_scope.py --selftest`: PASS.
- `check_baremetal_only.py --check`: 0 findings.
- `check_feature_status.py --self-test`: 46/46.
- `git diff --check`: plain, `ec0cc0c1 HEAD` and `6dfa64a7 HEAD`.

Further checks:

- `receipts/table-cells.txt`: every table in `README.md` (1), the #617 page (12) and the #451 page (8) has a constant cell count, rendered and in the source. It uses `scripts/table_cells.py` with the pinned environment's `cmarkgfm` and the standard HTML parser, and has a negative control.
  - The round-1 `table_render_check.py` needs `html5lib`, which cannot import in the pinned environment (no `six`). Nothing was installed.
- `receipts/anchor-check.txt`: the 9 relative links in the added lines, anchors included, reach their targets.
- `packet/receipts/mcasp-rx-rate.txt`: the reviewer's `mcasp_rx_rate.py` (SHA-256 `8e242c67…d173`) over the four published status logs gives 249.96 and 249.99 periods/s, with restart deltas of 5 and 5.

## Corrected packet files (`packet/`)

These overlay the round-1 packet, which is published as `review-evidence/b3-r1/author/` on branch `b3-review-evidence`. The local copies of `HANDOFF.md`, `summary/summary.json` and `MANIFEST.sha256` were checked equal to the published ones before editing.

| File | Change |
|---|---|
| `packet/HANDOFF.md` | Step 5 rate: 250.7 becomes 250.0 periods/s, with the bracket. One deviation line records the round-2 correction. The layout table names the round-2 files |
| `packet/summary/summary.json` | Adds `mcasp0_rx` to each USB run (interval, periods, rate, frames/s, restarts, bracket rule) and `first_non_silent_frame` to `usb-long`. Every original key and value is unchanged; the diff only adds lines |
| `packet/summary/usb-long-frame-1632.json` | New: frame 1,632's eight words, split into tag, ordinal and low byte |
| `packet/tools/usb_frame_words.py` | New: the read-only extraction tool, which refuses a capture whose SHA-256 differs |
| `packet/receipts/mcasp-rx-rate.txt` | New: the rate re-derivation with input hashes |
| `packet/MANIFEST.sha256` | The round-1 manifest, 166 entries, with `HANDOFF.md` and `summary/summary.json` re-hashed and the three new files added: 169 entries |

## Posting

- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5904494199 (2026-09-30T05:08:14Z).
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5904649003 (2026-09-30T05:21:58Z), for head `a66996aae46bc4a3eb2d8a4822d12d5186aa04eb`. `REVIEW-READY.md` is the posted text; `REVIEW-READY.readback.md` is the API readback, identical but for one trailing newline.
- Nothing else was posted, and no existing issue or PR comment was edited or deleted. The lane stops here.

## Directory layout

| Path | What |
|---|---|
| `HANDOFF.md` | This file |
| `PR-BODY.md` | Proposed PR body. It keeps the [A453] first line and the `Refs #617` and `Refs #451` line, has no closing keyword, updates the stale statements and adds a Round 2 section |
| `TAKEN.md`, `TAKEN.readback.md` | Posted TAKEN and its readback |
| `REVIEW-READY.md`, `REVIEW-READY.readback.md` | Posted REVIEW READY and its readback |
| `packet/` | Corrected packet files, above |
| `receipts/` | `gates/`, `table-diff.txt`, `table-lines-diff.txt`, `table-cells.txt`, `anchor-check.txt`, `private-scan.txt` |
| `scripts/` | `table_diff.py`, `table_cells.py`, `private_scan.py` |

Inputs read, never written:

- the round-1 packet;
- the two review packets (only `scripts/mcasp_rx_rate.py` was executed);
- the raw `usb-long` capture and its full grade file in the round-1 lane's raw directory (SHA-256 checked);
- the round-1 lane's private redaction map and endpoint file, used only as scan token sources.

No file here exceeds 200 KB. No toolchain, environment or tree export is here.
