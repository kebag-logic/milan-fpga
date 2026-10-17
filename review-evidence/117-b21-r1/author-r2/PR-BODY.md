[A625] Bench lane B21: #117 box 4, the audio continuity row, on dev 9ef71772 (round 3: the row passes as measured)

## Contents

- **[Status](#status)** -- Round 3 passes the row as measured, corrected after review in PR round 2; rounds 1 and 2 stopped; gates; `117-b21-bench` -> `dev`.
- **[PR round 2](#pr-round-2)** -- 2026-10-17: what each review finding changed, with the per-cycle restart table and the grader controls.
- **[Linked Issue / roles](#linked-issue--roles)** -- The public task, the executor and the reviewers.
- **[Description](#description)** -- What each round measured, with round 3's per-run tables.
- **[Authoritative references](#authoritative-references)** -- The assignment, the B5 page and the method pages.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- The branch and the pinned documentation environment.
- **[How to validate](#how-to-validate)** -- The gate commands and the reproduction from the lane packet.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this lane does not show.
- **[Definition of Done](#definition-of-done)** -- The merge bar.

## Status

Round 3 passes the audio continuity row as measured on the installed image. PR round 2 corrected the round 3 section after reviews R635-1 and R634-1: each restart is now bounded from the rebind command to the first valid output sample, the McASP grader compares slot words, and every figure the reviews named has a published computation. Rounds 1 and 2 stopped (after step 1, and at the identity gate). Findings docs only: `docs/findings/117_AUDIO_CONTINUITY.md`. Head `75853d80c22893448936bd1890e782bd0a0ce642`, four commits on dev `4a9b5a2a` (PR round 2: one commit on `867fb945`, +232 and -57 lines). Eleven gate invocations, all rc 0 at the head. `117-b21-bench` -> `dev`.

## PR round 2

2026-10-17, under the [PR round 2 assignment](https://github.com/kebag-logic/milan-fpga/pull/758#issuecomment-6231784136), answering reviews R635-1 (NEGATIVE) and R634-1 (NEGATIVE) at `867fb945`. Offline, from the round 3 records and the archived raws read by path; no bench action ran. Commit `75853d80`, findings page only.

| Finding | Change | Evidence in the packet |
|---|---|---|
| R635-1-F1, restart endpoint | Each cycle bounded from the rebind command to the first valid output sample. Upper bound on one clock (the bench host's): the cycle driver's last event before the command to the external capture's read that delivered the first valid frame, so any output latency is inside it. Lower bound on the peer-link tap: the received CONNECT_RX command to the packet carrying the first output frame's counter. Verdict PASS, 20 of 20; planted output latency of 0.5 s passes, 0.903 s fails cycle 19 only, 1.0 s fails all 20. Round 3's output figure assumed the output's last frame was the wire's last; the counters show 486 to 540 more frames on the wire, so it is replaced by the bounds | `pr2/rA/` |
| R635-1-F2, grader proof | The McASP grade accepts alignments and runs only on equal slot words; a final pass checks every matched frame. The collision control now reads 1 foreign frame (as-run: fully matched). Real recording: clean, 30,480,000 matched at offset 148,874, 0 unequal; the exact comparator agrees. The as-run grader is kept unchanged | `pr2/probes/`, `pr2/dB/` |
| R635-1-F3, leading insertion | The first offset is kept at alignment; the isolated control reads 3 foreign zero frames and an insertion of 3 (as-run: exits 1) | `pr2/probes/` |
| R635-1-F4, R634-1-F1, floor groups | Stated as printed: eight positive (+6.3 to +8.4) and one negative (-2.5). The sampler woke every 1.02 to 1.04 s, so no group is a missing cycle; in all nine the sign follows the two windows' deepest sampler dips, a computed association | `pr2/mst-long/floor-groups.txt` |
| R634-1-F2, unpublished figures | Transit fit (-13.070107 ppm, residual -27.681 to +23.894 µs) and CRF per tap; repeated frames 21.1%; the grader controls | `pr2/dA/`, `pr2/dB/dB-exact.json`, `pr2/probes/` |
| R634-1-F3, round 1 losses | Counts as printed: 17 of 20 losses above the control maximum; the other three +7.8, +6.8 and -5.2 | page, round 1 |
| R634-1 R1 to R5 | Applied as written | page |
| S1, S2 | Direction B values -2 to +1 LSB stated; step 1's mechanical verdict CLEAN with 9 planted losses caught | `pr2/mst-long/step1-verdict.json` |

| Cycle | Lower bound, ms | Upper bound, ms | Upper below 1 s |
|---|---|---|---|
| 1 | 41.5 | 51.0 | yes |
| 2 | 23.5 | 28.6 | yes |
| 3 | 23.4 | 33.7 | yes |
| 4 | 24.2 | 28.0 | yes |
| 5 | 23.2 | 32.3 | yes |
| 6 | 23.5 | 36.4 | yes |
| 7 | 23.5 | 32.6 | yes |
| 8 | 26.7 | 39.0 | yes |
| 9 | 23.7 | 33.3 | yes |
| 10 | 23.7 | 27.5 | yes |
| 11 | 23.7 | 31.8 | yes |
| 12 | 23.7 | 36.1 | yes |
| 13 | 23.7 | 32.2 | yes |
| 14 | 23.6 | 36.5 | yes |
| 15 | 23.9 | 30.8 | yes |
| 16 | 23.6 | 35.8 | yes |
| 17 | 23.8 | 30.3 | yes |
| 18 | 23.7 | 34.6 | yes |
| 19 | 96.7 | 100.7 | yes |
| 20 | 23.6 | 34.9 | yes |

New raw and work files (the derived received-frame record and the control inputs) stay outside the packet, by size and SHA-256 in `RAW-ARTIFACTS-pr2.json`.

## Linked Issue / roles

Refs #117

Executor: `[A625]`
Internal cleared-context reviewer: assigned by the manager
External reviewer: assigned by the manager

## Description

The [B21 assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6208207821) localises the losses lane B5 recorded, then passes the row. Every round ran on the installed dev `9ef71772` image: not flashed, reset or power-cycled.

**Round 3** (2026-10-16 17:21 UTC and 2026-10-17 06:49 to 07:52 UTC). A bench host restart cut it after the first identity gate. The controller host restarted too, so the gate ran again before any measurement.

| Item | Verdict | Evidence |
|---|---|---|
| Identity gate | PASS, 11 of 11, three times | 2026-10-16 17:22, 2026-10-17 06:51 and 07:51 UTC |
| Step 1, McASP capture-path self-test, deficit-only | CLEAN | 630 s, 63,000 reads of one period each, 0 overruns, 0 stalls, no permanent floor step |
| Step 2, Direction A, both taps, DUT CSRs, peer counters | PASS | 644.8 s of pattern frames on both taps, all valid and in order; the peer's output 638.0 s with no repeat, skip or silent frame |
| Step 3, Direction B, both taps, DUT CSRs, McASP capture | PASS | 30,480,000 frames (635.0 s) equal to the frames the DUT received, bit for bit and in order |
| Restarts, 20 cycles under the binding rule, rebind to the first valid output sample | PASS, 20 of 20 under 1 s | Upper bound on one clock, including every output latency: median 33.5 ms, maximum 100.7 ms |
| #117 audio continuity row | PASS as measured | Operator measurement, not a review verdict |

| Run | Window, UTC | What | Result |
|---|---|---|---|
| `mst-long` | 07:05:09 to 07:15:39 | McASP0 capture, no DUT, peer, tap or controller action | 30,240,000 frames, 0 overruns, 0 stalls, longest read interval 11.1 ms, 10 s floors within -3.50 to +1.94 frames of the +43.06 ppm line |
| `dA` | 07:17:32 to 07:28:22 | Pattern into McASP0; DUT talker to the peer's listener | DUT-link tap 5,198,452 AAF packets, peer-link tap 5,198,499, 0 sequence breaks; 30,951,504 pattern frames, 0 repeats, 0 skips, 0 torn, 0 invalid; 5,198,372 common packets equal in sequence number, timestamp and payload; `SLIP_TDM` 0 in all 128 samples, `RENDER_STAT` converged with 0 rails; peer FRAMES_RX = DUT FRAMES_TX = 5,245,516, no error counter moved; external cross-check 30,624,574 valid frames, 0 stalls |
| `dB` | 07:31:30 to 07:42:20 | The peer's talker (the noise already at its inputs) to the DUT's listener; McASP0 records the DUT's TDM output | Peer-link tap 5,198,371 packets, all present and equal on the DUT-link tap, 0 sequence breaks; McASP 30,480,000 frames at one constant offset to the received frames: 0 skips, 0 repeats, 0 foreign frames; 0 overruns; `SLIP_TDM` 0, `RENDER_STAT` converged with 0 rails, listener words static |
| `rA` | 07:44:28 to 07:46:28 | 20 unbind and rebind cycles of the as-found Direction A binding | 20 SUCCESS binds, formats equal before each, ended bound as found; rebind to the first valid output sample: upper bound 27.5 / 33.5 / 100.7 ms, lower bound 23.2 / 23.7 / 96.7 ms (min / median / max); wire restart 13.4 / 13.8 / 86.8 ms; no packet in any hold; silences all zero frames |

- No loss occurred in either direction, so none needed placing, and step 5's debug trace is not needed.
- Lane B5's one-frame drops every 1.266 s are absent with the peer following the DUT's CRF, as found.
- Restore: end census equal to the start in 45 of 46 entries (the DUT's live propagation delay). DUT words equal but for live counters; NVM unchanged. Outlets on; taps and controller clean.
- SoC board: its bridge leg restarted with its recorded command line; the board's audio player restarted through its own scripts. Its stop script removes a runtime CA mount the player needs, which its start script does not make. The lane recreated it from the player's own directory, restarted the player, and the player logged in.

**Round 1** stopped after step 1: the external capture's self-test was not clean (336 and 10,945 frames lost in USB stall episodes), and the SoC board's console stood at a login prompt. **Round 2** stopped at the identity gate: the controller host could not be reached.

## Authoritative references

- #117 acceptance box 4; the B21 assignment (above).
- `docs/findings/117_AUDIO_CONTINUITY.md`, lane B5's record and analysis tools (`b5_attrib.py`, `b5_round3.py`).
- `docs/findings/451_TDM8_FIRST_LIGHT.md` (method, pattern, TDM clocking); `docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md` (torn-frame definition).
- `docs/design/TIME_SYNC.md` (talker capture handoff); `docs/reference/REGISTER_MAP.md` (`SLIP_LB`, `SLIP_TDM`, `RENDER_STAT`).

## How to get into the same state

```sh
git fetch origin
git switch -c 117-b21-bench 75853d80c22893448936bd1890e782bd0a0ce642
python3 -m venv md-venv && md-venv/bin/pip install --require-hashes -r tools/markdown/requirements.txt
```

## How to validate

```sh
md-venv/bin/python scripts/docs_check.py
md-venv/bin/python scripts/check_doc_style.py
md-venv/bin/python scripts/gen_toc.py --check
md-venv/bin/python scripts/check_em_dash.py --base e4b771f9
md-venv/bin/python scripts/check_doc_paths.py
python3 scripts/ci_scope.py --selftest
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_feature_status.py --self-test
git diff --check 4a9b5a2a HEAD
# round 3 figures, from the lane packet 117-b21-a625 once published (raw files by hash in RAW-ARTIFACTS-r3.json):
B5_W=110 python3 -B tools/b21_mcasp_ana.py <raw mst-long dir> mst-long <out dir>
python3 -B tools/b21_grade.py wire <DUT-link pcap> <peer-link pcap> 0200000000010000 3 2 8 <out prefix> pattern
python3 -B tools/b21_grade.py wire <DUT-link pcap> <peer-link pcap> 3cc0c60102030000 2 3 4 <out prefix>
python3 -B tools/b21_grade.py mcasp <raw dB dir> dB <out prefix>-dutlink.samples 4 <out prefix>
python3 -B tools/b21_grade.py ext <raw external capture dir> <out prefix>
python3 -B tools/b21_restart.py <peer-link pcap> <DUT-link pcap> <raw external capture dir> <out json>
```

Expected result / pass criteria: every gate rc 0; the analyses reproduce `r3/selftest/mst-long/mst-long-analysis.txt` and the JSON files under `r3/summary/`. PR round 2's commands, inputs and expected outputs are in the packet's `pr2/REPRODUCE.txt`; each exits 0 and reproduces its output under `pr2/`.

## Known limitations / out of scope

- One window per direction, on one morning. Only stream channels 0 and 1 are observed at the peer's output, and 0 to 3 at the McASP.
- Direction B's signal is the noise already at the peer's talker inputs, made known by the wire record; it is not a pattern from the source.
- The restart upper bound needs the bench host's realtime clock to run without a step through the capture (the tool refuses a move over 1 ms against the monotonic clock). Round 3's output figure, which left out the steady latency, is kept as published and replaced by the two bounds.
- Direction B's samples take only the values -2 to +1 LSB, so bit-exactness there is shown for those values; the full-scale listener path is not exercised.
- Step 1's mechanical verdict catches a planted 6-frame loss with 0.58 to 1.82 frames of margin; a smaller loss can pass it.
- The restart driver's format comparison read a field the controller agent does not emit. The format reads ran before every bind and are logged, and all 20 pairs were equal, so no set was due.
- Round 1's external-capture stall source stays unnamed; round 3's external capture had no stall, and it does not grade the row.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (the audio continuity row measured PASS; review pending)
- [ ] New or changed behavior has self-checking tests (findings docs only)
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
