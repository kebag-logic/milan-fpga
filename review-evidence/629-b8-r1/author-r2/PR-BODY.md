[A521] Bench lane B8: #629's remaining bench items on dev `bbf704ec`: the source switch, the CRF lock loss and the saved selection across a power cycle; Direction B's THD+N not run

Refs #629

Adds and completes the dated section "Dev bbf704ec, 2026-10-03: lane B8" in `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, with its Contents line and the page introduction's pointer, and updates the page's row in `docs/findings/README.md`. No other file changes.

Head: `77299b4fca1ec3268f0997c55a51d84955bbfeca`, three commits on PR #644's head `40714c1bd166c2a05f9607a861e8550c705d183a` (lane B7): `c17997fb` (the first session's STOP), `4fb5125a` (the second session's items 2 to 4) and `77299b4f` (round 2, docs only: the answers to R454-1 and R455-1). The branch carries lane B7's three commits too.

## What happened

The lane was to run #629's remaining bench items on the image lane B7 measured:

1. Direction B graded by the THD+N and SNR of a known tone fed into the reference peer's talker inputs;
2. a source switch between the peer's AAF and CRF streams, the DUT as listener;
3. a followed CRF stream's lock loss;
4. the saved clock-source selection across one cold power cycle.

The first session stopped at item 1's precondition: the known tone did not reach the peer's talker. The manager ruled that item 1 waits for the owner's check of the tone's path and that items 2 to 4 run (https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5970994127). The second session ran them, the one authorised power cycle included, and restored everything.

| Item | Result |
|---|---|
| Identity gate | PASS three times: at the start, at the resume and after the power cycle, each verdict byte-equal to lane B7's |
| Tool controls | PASS, byte-equal to lanes B6 and B7 (run after the cases) |
| 1. Direction B by THD+N and SNR | NOT RUN: the tone does not reach the peer's talker (the DUT's TDM output carried the idle floor while it received the peer's stream) |
| 2. Switch AAF to CRF | PASS: LOCKED 2.62 to 3.12 s after the set; one MEDIA_RESET on the DUT's talker and one as received; CLOCK_DOMAIN LOCKED and UNLOCKED +1 each; GET_CLOCK_SOURCE 1 throughout; `SLIP_LB`, `SLIP_TDM` and the render rails static; the DUT's listeners undisturbed |
| 2. Switch CRF to AAF | PASS: LOCKED 5.96 to 6.48 s after the set, the meter's rate valid 3.9 to 4.4 s after it; otherwise as above |
| Tone path over the whole switch span | 417.3 s: 0 listener discontinuities, 0 net steps in 20,030,400 frames, 416 of 417 blocks at the floor (the other holds a 108-frame capture-path loss) |
| The INTERNAL-to-AAF set that started item 2 | #645 repeated: `SLIP_LB` +2, one frame, 2.0 to 3.0 s after the servo first read LOCKED; +2 in ACQUIRE and +4 on INTERNAL after the binds. The ring then held 428 s through both stream-to-stream switches |
| B-CRF repeated (the window before item 3) | PASS: LOCKED at all 797 polls; 0 net steps in 19,261,920 frames. Three host capture stalls (read gaps of 4.12, 4.37 and 9.77 s) hid 18.7 s of the 420 s window: 899,009 frames lost on the capture path, 18.69 s of them in the three stall clusters |
| 3. CRF lock loss | As declared: HOLDOVER within 0.56 s with the trim frozen at -6.0 ppm for 11 s, GET_CLOCK_SOURCE 1 throughout, one `mr` toggle at the loss and none at the return, CLOCK_DOMAIN UNLOCKED +1 then LOCKED +1, STREAM_INPUT 1 MEDIA_UNLOCKED +1, LOCKED 2.66 to 3.16 s after the rebind; tone path clean |
| 4. Saved selection across a power cycle | PASS: CLOCK_SOURCE 2 set, read back and committed (NVM 30 to 31 commits, image seq 31); one cold power cycle of the DUT's outlet; boot PASS (prompt 8.4 s after the first console byte, the UART grader 10/10 at its first run, NVM slot seq 31 restored); after the boot GET_CLOCK_SOURCE read 2 at the first command and the servo read LOCKED with no command sent; restored to CLOCK_SOURCE 0 and read back |
| Restore | Done: every clock source, format, binding and map read back as found; census 43 of 46 equal, the other three the boot's (MAAP addresses, propagation delay); the bench lock free |

## #629 acceptance

Not every item is met, so this PR refers to #629:

- Bench quality metric, Direction B: NOT met (item 1 not run).
- Fabric, "a switch re-locks with no undeclared discontinuity": met for the switches between the AAF and CRF streams; not met for the switch from INTERNAL to AAF, whose ring slip after LOCKED repeated (#645). The data for #645 is in the section; this lane posted nothing on #645.
- Lock loss: met for both sources (AAF by lane B7, CRF here).
- Protocol processor, "the selection kept as saved state": met at the bench.

## Evidence

The lane packet `629-b8-a521` holds the evidence and the tools. The page lists the raw files' and every cited evidence file's SHA-256. Redaction passes masked private identifiers in 79 packet files, and `redaction.json` records each file's original and retained SHA-256. Four tools are masked: two where they describe the tone source, `run_b8.py` at an assertion on the capture's sample-format name, and `grade_b8.py` at a docstring line that stated the capture's channel count. The format name and the channel count are masked; the code that decodes the capture's samples stays readable, as in lanes B6 and B7 (the manager's ruling, https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5971696657).

The packet is published on branch `629-b8-review-evidence`, pinned at `36ee6d8adca255ad5228c4258a3186a5f0cbc574`, under `review-evidence/629-b8-r1/author/` (the label `629-b8-a521` maps there). `review-evidence/629-b8-r1/MANIFEST.json` gives each file's `original_sha256` beside its `published_sha256`. It was first published at `5bad6a43`; `36ee6d8a` masked the one `grade_b8.py` line on top, with no force-push. Every evidence row on the page equals its published file at `36ee6d8a`, and every raw row its record in `RAW-ARTIFACTS.json` there.

## Validation

At `77299b4f`, every command rc 0, as at `4fb5125a` in round 1:

- `scripts/docs_check.py`, `scripts/check_doc_style.py`, `scripts/gen_toc.py --check`, `scripts/gen_toc.py --verify-anchors`, `scripts/check_em_dash.py --base 40714c1b`, `scripts/check_doc_paths.py` (the pinned Markdown environment)
- `scripts/ci_scope.py --selftest`
- `scripts/check_baremetal_only.py --check` and `--selftest` (the bare invocation is a usage error, rc 2, as lanes B6 and B7 recorded)
- `scripts/check_feature_status.py --self-test`
- `git diff --check 40714c1b HEAD` and `git diff --check 4fb5125a HEAD`, and `git diff --check 40714c1b` on the worktree before the commit

## Round 2

Docs only, with no bench access, from the existing run artifacts. It answers R454-1 and R455-1, both NEGATIVE at `4fb5125a`, under the round-2 assignment (https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5971696657). One commit, `77299b4f`, changes only the lane B8 section of the findings page. No verdict on the page changed.

| Finding | Change |
|---|---|
| R454-1 F1 = R455-1 F4: the capture's channel count in `grade_b8.py` | The manager masked the docstring line top-only at `36ee6d8a`. The page's `tools/grade_b8.py` row now carries the retained file, 27,959 bytes, `77949fd1...`, marked "masked; as run `330c14cd...`". The lane packet's `redaction.json` records both hashes, 79 files in all |
| R454-1 F2: the decode | Per the ruling, the page says the format name and the channel count are masked and the decode, byte width and byte order, stays readable. It no longer says the layout is hidden |
| R454-1 F4 = R455-1 F2: where the evidence lives | A "Where the packet is" paragraph: the branch, the pin `36ee6d8a`, the label-to-path mapping, `MANIFEST.json`'s two hashes, the first publication at `5bad6a43`, the eight path-masked restore records, and where each hash row is recorded. The section's opening pointer names the branch and the pin |
| R454-1 F3 = R455-1 F1: the CRF window's loss | 18.7 s, 899,009 frames, from the grade's `capture_lost_frames`. 401.29 s captured plus 18.73 s lost closes on the events' 420.03 s. The three stall clusters lost 18.69 s; their starts are given on the captured-audio basis and counting the frames lost before each. Two of the three are off the 48 n + 12 signature; the third is on it and holds a 23,776-frame capture-path repeat. The limits and this body carry the same figure |
| R455-1 F3: #645's data, not a cause | The two slips before the set: their intervals, within 1.94 s of the binds and at most 1.33 s apart, with no skip; and the 3.52 s period of a steady 5.92 ppm offset. They are recorded, not analysed, and no cause is given |
| R455-1 S1 | The saved row records `dirty=0`, `commit_busy=0` and `pend=1` (`nvm_pend`), which read 1 at every NVM read before the cycle; the read of 2 after the cold boot is the evidence |
| R454-1 R1 to R3 | Applied as given: `SLIP_TDM` at `0x8D8`; the raw-record sentence; "no state-changing command sent" at both places |
| Suggestions taken | R454-1 S1 ("consistent with the declared recentre"; an underrun leaves the same trace and `RENDER_STAT` does not expose it), S2 (the six post-boot dups offered to #645 as untimed data), S4 (poll 618); R455-1 S2 (the mapped channels' floor against the exactly-zero unmapped ones), S3 (`mr` counted at both ends, not captured on the wire) |
| Not taken | R454-1 S3: a random container interface name in two published restore records. It is on the evidence branch, which the manager publishes |

Left for the manager, as both reports list: carrying the INTERNAL-to-AAF data to #645 (this lane posts nothing there); lane B7's published `grade_b7.py`, which states the same channel count and is outside this diff; the merge order after PR #644; and the hosted and current-dev candidate checks.
