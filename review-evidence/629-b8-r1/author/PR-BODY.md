[A521] Bench lane B8: #629's remaining bench items on dev `bbf704ec`: the source switch, the CRF lock loss and the saved selection across a power cycle; Direction B's THD+N not run

Refs #629

Adds and completes the dated section "Dev bbf704ec, 2026-10-03: lane B8" in `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, with its Contents line and the page introduction's pointer, and updates the page's row in `docs/findings/README.md`. No other file changes.

Head: `4fb5125a2e43997384839deeb1fe4742a5b2dca8`, two commits on PR #644's head `40714c1bd166c2a05f9607a861e8550c705d183a` (lane B7): `c17997fb` (the first session's STOP) and `4fb5125a` (the second session's items 2 to 4). The branch carries lane B7's three commits too.

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
| B-CRF repeated (the window before item 3) | PASS: LOCKED at all 797 polls; 0 net steps in 19,261,920 frames. Three host capture stalls (4.1, 4.4 and 9.8 s) hid 19.0 s of the 420 s window |
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

The lane packet `629-b8-a521` holds the evidence and the tools. The page lists the raw files' and every cited evidence file's SHA-256. Repeated redaction passes masked private identifiers in 78 packet files, `redaction.json` records each file's original and retained SHA-256, and three tools are masked (two where they describe the tone source, one at a line that would state the capture's layout). The packet is not yet published.

## Validation

At `4fb5125a`, every command rc 0:

- `scripts/docs_check.py`, `scripts/check_doc_style.py`, `scripts/gen_toc.py --check`, `scripts/gen_toc.py --verify-anchors`, `scripts/check_em_dash.py --base 40714c1b`, `scripts/check_doc_paths.py` (the pinned Markdown environment)
- `scripts/ci_scope.py --selftest`
- `scripts/check_baremetal_only.py --check` and `--selftest` (the bare invocation is a usage error, rc 2, as lanes B6 and B7 recorded)
- `scripts/check_feature_status.py --self-test`
- `git diff --check 40714c1b HEAD`, and `git diff --check 40714c1b` on the worktree before the commit
