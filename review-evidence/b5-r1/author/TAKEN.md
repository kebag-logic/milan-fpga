[A472] TAKEN

Bench lane B5, #117 acceptance box 4, the audio continuity row, under the [A10] assignment (https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5925737609).

Branch: `b5-bench-1001` from dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`, local only. Image under test: dev `ec0cc0c1`, as installed.

Authoritative references: #117 acceptance box 4; the #451 first-light method and pattern (`docs/findings/451_TDM8_FIRST_LIGHT.md`); the #617 torn-frame definition and the frame-atomic capture handoff (PR #618, `docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md`); the reconnect and restart method (`docs/findings/608_75_WITHDRAWAL_AND_RESTART.md`).

Interpreted scope:
1. Identity gate first, as lanes B3 and B4 ran it. STOP if it fails.
2. Before every bind, read the talker's and the listener's stream formats. If they differ, set the listener's to the talker's, then bind. Each read and set is recorded.
3. Direction A: the first-light pattern is played into the DUT's TDM input through the SoC board's McASP0. The DUT's AAF talker carries it to the reference peer's listener, and the peer's digital output is recorded by an external, hardware-clocked audio capture. Channels 0 and 1 are graded bit-exact at the captured word length and in order. At least 10 minutes of continuity are graded for silent stretches, repeats and skips. At least 20 unbind and rebind cycles are timed from the rebind response to the first valid sample.
4. Direction B runs only if a known signal can drive the reference peer's talker channels without a wiring or instrument change; otherwise it is NOT RUN, with the reason.
5. Streams, formats, the SoC board's audio bridge and the bench are restored as found, with proof.

Output: one findings page under `docs/findings/` with its index row; no other doc edit.

Validation plan: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base e4b771f9`, `check_doc_paths.py`, `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py`, `scripts/check_feature_status.py --self-test` and `git diff --check`, all rc 0 at the committed head.

Blockers: none.
