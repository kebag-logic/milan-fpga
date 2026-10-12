[A603] REVIEW READY (B16c)

Commit: `e20fd2820a9c6b9effabc529a742e732263fafa8` on `629-b16-tone`, one new commit on `0d4ff919` (no rebase, no amend). Local, not pushed, no PR. Refs #629.

Changed: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` gains eleven `B16c:` subsections at the end of lane B16's section, plus pointers in the introduction, the Contents line and the B16 introduction. Its row in `docs/findings/README.md` is updated. No other file changed, and no DUT change was made.

Validation: all 14 gates rc 0 at the head, each to its own log, unpiped, on the physical /data path, with the Markdown gates in the pinned environment:
- `docs_check.py`, `check_doc_style.py`;
- `gen_toc.py --check` and `--verify-anchors`;
- `check_em_dash.py --base e8454e27`, 0 findings over 3,015 added lines;
- `check_doc_paths.py`, `ci_scope.py --selftest`;
- `check_baremetal_only.py --check` and `--selftest` (the bare form is a usage error, as lanes B6 to B16b recorded);
- `check_feature_status.py --self-test`;
- `git diff --check`, and `git diff --check c20c85bd HEAD`.

Before any bench action, the new run mode was dry-run offline against stand-ins and passed 8 of 8 scenarios. Its wrapper's deadline path passed too.

**What ran** under the [ruling](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6118365090), bench work 07:47 to 08:04 CEST:
- The identity gate passed again at 07:48 CEST, every fact as in B16. The bench was as B16b left it: census 45 of 46 equal, the other the DUT's live propagation delay.
- The SoC board's McASP playback was closed at every check: no music.
- Each case is one locked action, in this order:
  1. the peer's CLOCK_DOMAIN set to CLOCK_SOURCE 0, INTERNAL, and read back;
  2. the peer's CRF talker bound to the DUT's STREAM_INPUT 1 and its AAF talker to STREAM_INPUT 0, under the binding rule (the formats were already equal; nothing set);
  3. the DUT's CLOCK_DOMAIN set to 1 (B-CRF) or 2 (B-AAF) and read back;
  4. from 20 s after the set: 300 s at McASP0 while it plays lane B6's loop, the external capture, and 40 s of each tap;
  5. the DUT back to 0 and read back, the binds undone, then the peer back to 1, its CRF input, as found, and read back.

| Clock-source record | Peer to INTERNAL | DUT set | DUT restore | Peer restore |
|---|---|---|---|---|
| `bcrf` | 0: SUCCESS, read back 0 | 1: SUCCESS, read back 1 | 0: SUCCESS, read back 0 | 1: SUCCESS, read back 1 |
| `baaf` | 0: SUCCESS, read back 0 | 2: SUCCESS, read back 2 | 0: SUCCESS, read back 0 | 1: SUCCESS, read back 1 |

**Per-run table.** THD+N is the median over one-second blocks, with the worst block in brackets. SNR equals minus THD+N within 0.01 dB.

| Run | Window, CEST | Servo | (a) The peer's talker, its link | (b) The DUT's link | (c) The DUT's TDM output, McASP0, 300 s | (c) against (a) and (b) | (d) The positive control |
|---|---|---|---|---|---|---|---|
| `bcrf`, B-CRF | 07:50:56 to 07:55:56 | LOCKED 2.66 to 3.16 s after the set; at 596 of 596 window polls; trim -6.0 to -6.1 ppm | PRESENT at -14.1035 dBFS, 0.000 ppm; -123.98 (-123.93) / -123.97 (-123.93) dB; 0 gaps | PRESENT; -123.99 (-123.93) / -123.97 (-123.93) dB | -123.98 (-123.93) / -123.97 (-123.90) dB; 300 of 300 blocks at the path's floor; 0 discontinuities; 0.0000 ppm | SAMPLE-EXACT over 34.3 s and 34.3 s, 0 differing | Lane B6's loop: 0 discontinuities, 0 net steps in 14,583,391 frames; 305 of 306 blocks at the loop's floor, the other the playback's start |
| `baaf`, B-AAF | 07:57:47 to 08:02:47 | LOCKED 6.68 to 7.18 s after the set; at 596 of 596; AAF meter locked, rate valid, 0 history restarts, largest deviation 30 ns | PRESENT at -14.1035 dBFS, 0.000 ppm; -123.98 (-123.93) / -123.98 (-123.93) dB; 0 gaps | PRESENT; -123.98 (-123.92) / -123.98 (-123.93) dB | -123.98 (-123.92) / -123.97 (-123.91) dB; 300 of 300 at the floor; 0 discontinuities; 0.0000 ppm | SAMPLE-EXACT over 34.2 s and 34.3 s, 0 differing | 0 discontinuities, 0 net steps in 14,585,924 frames; 305 of 306 at the floor |

Each pair of THD+N values is 997 Hz / 9,973 Hz.

- **`SLIP_TDM`** was 0 throughout.
- **`SLIP_LB`** went 162 to 188 dups, all before LOCKED. In each case, five steps fell in the 12 s between the binds and the DUT's set, while the DUT was still on INTERNAL against the peer's own clock. B-CRF then had one step in ACQUIRE and B-AAF two. None fell after LOCKED. Lane B8's slip after LOCKED (#645) did not repeat.
- **The DUT's CLOCK_DOMAIN counters** moved once per case, before the window, and not in it.
- **The DUT's talkers' MEDIA_RESET** went 0 to 4, as many as its clock-source sets. The peer's listener counted them one per set: none in either window.
- **The tone monitor** read the playback RUNNING at every 0.2 s read of both cases: no restart, no underrun.

**Attribution.** No stage loses the tone:
- (a), (b) and (c) all sit at the path's floor, -124 dB;
- (c) equals the received stream in every one of the 3,289,015 frames compared with (a);
- (d) holds no discontinuity.

In B16b's B0, with the peer following the DUT's CRF, (a) held 131 degraded blocks. With the peer on its internal source, it holds none. That is one run each, and the cause is not shown.

**Acceptance criteria:**
- Met: the ruling's B-CRF and B-AAF, graded by THD+N and SNR at McASP0 with the four-point attribution, and the full restore.
- #629 item "bench quality metric": Direction B is now met for both followed sources, against lane B9's synthetic controls.
- NOT met: the INTERNAL mismatch control. B0 ran with the peer following the DUT, and the exception covers B-CRF and B-AAF only.
- #645 stays open.

So not every #629 item is met: Refs #629.

**State as left** (verified by census and counters at 08:04 CEST):
- the DUT unbound on INTERNAL, its formats and maps as found;
- the peer's STREAM_INPUT 0 bound to the DUT's STREAM_OUTPUT 0 and its STREAM_INPUT 8 to the DUT's STREAM_OUTPUT 1;
- the peer's CLOCK_DOMAIN on CLOCK_SOURCE 1, its CRF input, as found and read back;
- census 45 of 46 equal to the B16c start, the other the DUT's live propagation delay;
- the tone stopped by its process ID;
- the SoC board's McASP playback free, the to-host leg running with its recorded line, the from-host leg dead as found;
- the controller staging removed; no file or capture on the tap host; the bench lock free; nothing left running.

Residuals:
- the peer's talkers counted two more stream starts and stops each;
- the CLOCK_DOMAIN counters went 22/21 to 24/23 on the DUT and 6/5 to 8/7 on the peer;
- `SLIP_LB` went 162 to 188;
- DUT NVM went seq 286 to 292.

Open risks/questions: Direction B's INTERNAL control would need the same exception for B0, with the peer on its internal source. That is a decision for the manager.

