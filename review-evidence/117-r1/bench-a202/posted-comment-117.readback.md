[A202] REVIEW READY: #117 step 3 (GM loss and return) and the GM-change half of step 4, on the dev `ede8d48e` image, under the [owner decisions of 2026-09-23](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5795898094).

**Commit:** `0abf147f726721f4a323ee6a32095a02363fe2dc`, branch `117-silicon-evidence`, one commit on the PR #531 head `c3eb95fa`. Not pushed; the manager publishes. PR #531 is to be reviewed at this head.

**Changed:**
- `docs/findings/117_GPTP_SILICON_EVIDENCE.md` (SHA-256 `f55810c3...`). Step 3 is rewritten from NOT RUN to the six measured cycles, and step 4 gains the grandmaster-change correlation. Also updated: box 2 and box 3's transition row, observations 7 to 12, bench state after step 3, blockers B1 and B2 marked resolved, and the step 3 artifact hashes.
- `docs/design/GM_LOSS_RECOVERY.md` (`ab43f73e...`): a new "Recovery bound" section with the owner's 5 s bound and its derivation. The page's Contents separator is switched to `--`, which is the em-dash gate's prescribed remedy for adding an entry.
- `docs/findings/README.md`: the row status.

**Validation** at `0abf147f`:
- `scripts/docs_check.py`: 0 findings across 165 md files.
- `scripts/check_doc_style.py`: OK.
- `scripts/gen_toc.py --check`: OK, and `--verify-anchors` OK.
- `scripts/check_em_dash.py --base ede8d48e`: 0 findings over 630 added lines.

## Gates before any power action

- **Identity: PASS**, 13:44:58 to 13:45:22 UTC under the bench lock, read-only. ROM `f6afa4ec`, QSPI payload `02036e95` (seed `asl`), AEM `93742dd2`, `VERSION=00020060`, and the grader passed 10 of 10. The reference CRC table, recomputed from the build directories, is byte-identical to the earlier one. `origin/dev` was still `ede8d48e`.
- **OUT4 is the switch: PASS**, proved by cycle 1 before any other cycle ran.
  - At start the strip read OUT0, 1, 2, 4, 5 and 6 on and OUT3 off.
  - With OUT4 off, the switch's last frame on the DUT link came at 0.73 s, and the controller host's switch port lost carrier at 1.12 s. The DUT lost sync at 1.16 s and replaced the switch with itself as grandmaster at 3.56 s.
  - The DUT stayed up: 1,600 console samples, largest gap 0.106 s, `RST_EPOCH` 1 throughout.
  - The reference peer stayed up: its ADP available_index and GPTP_GM_CHANGED counted on.
  - No other outlet changed.

## Per-cycle result

Each cycle switched OUT4 off for 20 s and then on. Times are seconds after the off command. Recovery runs from the switch's first post-boot Announce on the DUT link (the Sync came 0 to 18 ms later) to the first 0.1 s console sample from which GM = switch, `SYNC=1`, `ASCAPABLE=1` and `TU=0` hold. Bound: 5 s.

| Cycle | CRF bound | DUT sync 0, `tu` 1 | DUT GM = itself | DUT asCapable 0 | Switch first Announce | DUT all-good | Recovery | Result |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | no | 1.16 | 3.56 | 5.66 | 39.95 | 40.46 | 0.51 s | PASS |
| 2 | no | 1.08 | 3.48 | 4.78 | 39.06 | 39.58 | 0.52 s | PASS |
| 3 | no | 1.08 | 2.88 | 5.48 | 39.07 | 40.58 | 1.51 s | PASS |
| 4 | yes | 1.17 | 3.66 | 4.91 | 40.00 | 40.42 | 0.43 s | PASS |
| 5 | yes | 1.09 | 2.96 | 5.75 | 39.07 | 40.54 | 1.46 s | PASS |
| 6 | yes | 1.06 | 3.24 | 5.62 | 39.12 | 40.72 | 1.60 s | PASS |

- **Loss declaration (DUT).**
  - Sync and `tu` went 0.40 to 0.46 s after the switch's last Sync, which is the 375 ms receipt timeout within one console sample.
  - The grandmaster went 3.01 to 3.08 s after the last Announce.
  - asCapable went 5.0 to 5.1 s after the last Pdelay response the DUT received.
- **While absent.** The DUT becomes its own grandmaster (priority1 248, alone). GM and parent read `020000fffe000001` with path count 1, `SYNC=0`, `ASCAPABLE=0` and `TU=1`. `RST_EPOCH` stays 1, and the link is silent.
- **Return.**
  - When the link came back, the DUT acted as master for 0.1 to 0.6 s, between becoming asCapable and adopting the switch: 1 to 4 Syncs in every cycle, and one self-naming Announce in cycles 3 and 5. It became slave on the switch's Announce (priority1 246).
  - In cycles 1, 2 and 4 it was asCapable before the first Announce and took the switch 9 to 20 ms after it.
  - In cycles 3, 5 and 6 the first Announce came before asCapable, and the DUT took the next one, 1.007 s later. That one announce interval is the whole difference between the 0.43 to 0.52 s cycles and the 1.46 to 1.60 s cycles.
  - `tu` cleared 0.41 to 0.52 s after adoption, which is the holdover.
- **Automatic.** No operator action reached the DUT beyond read-only AECP queries.
- **Reference peer: recovery time NOT RUN.** Its link is not tapped, and the controller host is inside the partition. Its GPTP_GM_CHANGED rose by 2 in every cycle. At the first reachable poll it already named the switch in cycles 1, 4, 5 and 6. In cycles 2 and 3 it named itself until 46.6 s, which is 7.6 s after the switch's first Announce on the DUT link. It never restarted.
- **Stream, cycles 4 to 6: PASS against "media within one further stream restart".** The peer's primary CRF input was bound to the DUT's CRF output through each outage.
  - At the loss, the first `tu=1` PDU on the wire (1.08, 1.07 and 1.00 s) fell inside the console interval where `CLKV_STAT[0]` rose. Emission ended with the link.
  - The binding survived.
  - After the return the DUT relicensed 0.72 to 2.38 s after all-good, with every PDU `tu=0`. That was exactly one stream restart per return, and the listener reported MEDIA_LOCKED by the next poll.
  - Each unbind succeeded on its first attempt.

## Step 4, GM-change half: PASS

Across the six losses and returns, every edge in the publication words matched its wire cause within one 0.1 s console sample. The causes are the receipt timeouts after the switch's last Sync and Announce at the loss, and the accepted Announce at the return. The words are:
- GM, parent, path generation and count, `CLKV_STAT` sync/asCapable/holdover/`tu`.
- The return edge came 0 to 74 ms after the accepted Announce.
- GET_AVB_INFO and GET_AS_PATH agreed at the next poll, and GPTP_GM_CHANGED rose by 2 per cycle, one per CSR identity edge.
- `CLKV_TUCNT` rose by 39 to 41, the 1 s intervals of each 38.5 to 39.7 s span with `tu=1`.
- Limit: the wire shows `tu=1` only at the loss edge, because the stream restarts after `tu` has cleared.

## Not counted: attempt 1

At 13:51:43 UTC a first attempt switched OUT4 off with no console record: my console poller was missing from the packet and exited at once. The guard saw no transcript and switched OUT4 back on after 5.95 s. The DUT and the peer recovered on their own (controller view in the packet).

Since then a pre-flight check refuses any power action until the console transcript is growing, and a 5 s poll check passed before cycle 1.

## Bench state

Restored, and shown:
- The strip read identically at 13:45 and 14:12 UTC. Only OUT4 was switched: seven times off and seven times on.
- 18 of 18 ACMP states and 15 of 15 settings reads match the start census. The only difference is the peer's varying reserved half-word, as before.
- The grader passed 10 of 10 at 14:13 UTC. `CRFT_CTRL` read `0x3`, drops 0, `CTLR_DIAG` 0, and a 22 s capture shows no AVTP stream.
- Scripts were removed from the controller host and the power-strip host. Captures were copied, hash-checked against the remote copy and removed. No process remains, and the lock is free.
- Flash, JTAG, wiring, instruments and every other outlet were not touched.

## New observations (numbered as on the page; no cause assigned)

- **Need their own issue (DUT):**
  - 8: AVB_INTERFACE LINK_UP/LINK_DOWN did not move over seven outages. The reference peer's didn't either.
  - 9: Stream Output 1 TIMESTAMP_UNCERTAIN and FRAMES_TX restart at each STREAM_START. This extends the earlier FRAMES_TX 16.
  - 10: The DUT never put its own identity on the wire in an ADPDU. It re-advertised 0.54 to 2.56 s after adopting the switch.
- **Bench facts:**
  - 7: The switch's gPTP time restarts from one origin at every power-on. Each return stepped the DUT PHC by minus the switch's previous uptime (-128 to -356 s).
  - 11: The peer's slower return in cycles 2 and 3.
  - 12: The peer resets its stream-input counters when bound and on each restart.

**Open risks/questions:**
1. The owner's bound ends at "asCapable and sync". These figures also wait for `tu` to clear, which is the stricter end point.
2. The reference peer's own recovery time cannot be timed on this bench without a tap on its link. Reviewers judge whether box 2 needs it.

Raw artifacts are in the private bench packet `117-a202-packet`, with a per-file SHA-256 manifest. The findings page lists the primary hashes, for example cycle 6 tap `6b4f090a...`, console `5a16a9bf...` and watcher `9ca7e270...`.

