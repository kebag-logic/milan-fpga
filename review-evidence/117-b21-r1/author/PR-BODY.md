[A625] Bench lane B21: #117 box 4, the audio continuity row, on dev 9ef71772 (round 3: the row passes as measured)

## Contents

- **[Status](#status)** -- Round 3 passes the row as measured; rounds 1 and 2 stopped; gates; `117-b21-bench` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- The public task, the executor and the reviewers.
- **[Description](#description)** -- What each round measured, with round 3's per-run tables.
- **[Authoritative references](#authoritative-references)** -- The assignment, the B5 page and the method pages.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- The branch and the pinned documentation environment.
- **[How to validate](#how-to-validate)** -- The gate commands and the reproduction from the lane packet.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this lane does not show.
- **[Definition of Done](#definition-of-done)** -- The merge bar.

## Status

Round 3 passes the audio continuity row as measured on the installed image. Rounds 1 and 2 stopped (after step 1, and at the identity gate). Findings docs only: three dated sections in `docs/findings/117_AUDIO_CONTINUITY.md` (+224, +64 and +334 lines, their Contents entries included). Head `867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b`, three commits on dev `4a9b5a2a`. Eleven gate invocations, all rc 0 at the head. `117-b21-bench` -> `dev`.

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
| Restarts, 20 cycles under the binding rule | PASS, 20 of 20 under 1 s | Wire median 13.8 ms, maximum 86.8 ms |
| #117 audio continuity row | PASS as measured | Operator measurement, not a review verdict |

| Run | Window, UTC | What | Result |
|---|---|---|---|
| `mst-long` | 07:05:09 to 07:15:39 | McASP0 capture, no DUT, peer, tap or controller action | 30,240,000 frames, 0 overruns, 0 stalls, longest read interval 11.1 ms, 10 s floors within -3.50 to +1.94 frames of the +43.06 ppm line |
| `dA` | 07:17:32 to 07:28:22 | Pattern into McASP0; DUT talker to the peer's listener | DUT-link tap 5,198,452 AAF packets, peer-link tap 5,198,499, 0 sequence breaks; 30,951,504 pattern frames, 0 repeats, 0 skips, 0 torn, 0 invalid; 5,198,372 common packets equal in header and payload; `SLIP_TDM` 0 in all 128 samples, `RENDER_STAT` converged with 0 rails; peer FRAMES_RX = DUT FRAMES_TX = 5,245,516, no error counter moved; external cross-check 30,624,574 valid frames, 0 stalls |
| `dB` | 07:31:30 to 07:42:20 | The peer's talker (the noise already at its inputs) to the DUT's listener; McASP0 records the DUT's TDM output | Peer-link tap 5,198,371 packets, all present and equal on the DUT-link tap, 0 sequence breaks; McASP 30,480,000 frames at one constant offset to the received frames: 0 skips, 0 repeats, 0 foreign frames; 0 overruns; `SLIP_TDM` 0, `RENDER_STAT` converged with 0 rails, listener words static |
| `rA` | 07:44:28 to 07:46:28 | 20 unbind and rebind cycles of the as-found Direction A binding | 20 SUCCESS binds, formats equal before each, ended bound as found; wire restart 13.4 / 13.8 / 86.8 ms (min / median / max); at the peer's output less the steady latency 23.5 / 24.8 / 97.8 ms; no packet in any hold; silences all zero frames |

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
git switch -c 117-b21-bench 867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b
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

Expected result / pass criteria: every gate rc 0; the analyses reproduce `r3/selftest/mst-long/mst-long-analysis.txt` and the JSON files under `r3/summary/`.

## Known limitations / out of scope

- One window per direction, on one morning. Only stream channels 0 and 1 are observed at the peer's output, and 0 to 3 at the McASP.
- Direction B's signal is the noise already at the peer's talker inputs, made known by the wire record; it is not a pattern from the source.
- The output restart figure excludes the steady wire-to-output latency, which was not measured.
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
