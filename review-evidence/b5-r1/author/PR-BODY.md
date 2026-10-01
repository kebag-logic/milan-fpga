[A472] Record #117 audio continuity end to end against the reference peer on dev ec0cc0c1

Refs #117 (acceptance box 4, the audio continuity row), under the bench lane B5 assignment: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5925737609

Head `bf9e5d82a401d167a8ffc786677a19dc7aac0cf2` on dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`. One commit.

## Change

- `docs/findings/117_AUDIO_CONTINUITY.md` (new): the bench record of the audio continuity row.
- `docs/findings/README.md`: its index row.

No other documentation, code or configuration changes.

## Result (operator measurements, not review verdicts)

The first-light pattern enters the DUT's TDM input from the SoC board's McASP0. The DUT's AAF talker carries it to the reference peer's listener, and an external, hardware-clocked audio capture records the peer's digital output. Image: dev `ec0cc0c1`, as installed; identity gate PASS.

| Item | Verdict |
|---|---|
| Integrity: stream channels 0 and 1 bit-exact at 24 bits, in order, over 660 s | PASS: 31,569,594 of 31,569,600 frames; 0 torn, 0 invalid; 6 single zero frames |
| Continuity over 660 s | FAIL: 334 repeats at the DUT's documented INTERNAL beat; 520 one-frame drops at the peer's output, one every 1.266 s; the capture path lost 117,104 more frames |
| Restarts: 30 unbind and rebind cycles, rebind response to first valid sample | PASS, 30 of 30 under 1 s: median 0.0279 s, maximum 0.1358 s, no growth |
| Direction B, the peer's talker to the DUT's listener | NOT RUN: no known signal drives the peer's talker channels without an instrument or wiring change |
| #117 audio continuity row | FAIL as measured |

Binding rule: the listener's stream format was set to the talker's before each run's first bind, and set back after each run; the talker's format was never set. The bench was restored and the restore proven; the one residual is the SoC board bridge legs' new process IDs.

## Open items

- The capture path loses 0.37% of the frames, so a clean continuity window was not recorded. A capture path that loses no frames is an owner item.
- The one-frame drops are attributed to the peer's INTERNAL media clock running 16.4 ppm slower than the stream. Testing that needs the peer's media clock to follow the stream, a clock-source change on the peer outside this lane. It needs a decision.

## Validation

All rc 0 at the head, from the physical lane path: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base e4b771f9`, `check_doc_paths.py` in the pinned Markdown environment; `scripts/ci_scope.py --selftest`; `scripts/check_baremetal_only.py --check`; `scripts/check_feature_status.py --self-test`; `git diff --check` and `git diff --check e4b771f9 HEAD`; `gen_toc.py --verify-anchors`.

Evidence: lane packet `b5-a472` (tools, per-action evidence, summaries, raw-artifact index by size and SHA-256, redaction record, manifest). Raw captures stay outside the packet and the repository.
