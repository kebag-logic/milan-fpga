[A468] TAKEN
Branch: `b4-bench-1001` from dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`, local only.
Authoritative references: the #451 recipe item "Scope BCLK, FSYNC and DOUT at the AM62x end: 12.288 MHz, a one-BCLK FSYNC pulse at 48 kHz, data starting one BCLK after it"; the PocketBeagle 2 amendment (comment 5729936674); the bench lane B4 assignment (comment 5924192573); the owner decisions in comments 5916029287 and 5924157808; #626, the oscilloscope version; PR #624 and `docs/findings/451_TDM8_FIRST_LIGHT.md` for the method, the pattern and the torn-frame rule.
Interpreted scope:
- Identity gate first, as lane B3 ran it; STOP if it fails.
- Framing from the SoC board, read-only: the live device tree's DAI format, clock-provider roles and slot geometry, and the ALSA `hw_params` of `hw:0,0` during a capture.
- Then the DUT's rendered pattern, using the first-light DOUT method (software AAF talker, DUT STREAM_INPUT 0 bound, eight identity mappings). It is recorded on McASP0 in one capture of at least 10 minutes, streamed off the board and pattern-checked over every frame.
- fs from the frames received against the board's monotonic clock, using the ALSA pointer and timestamp read from `/proc`; BCLK = 256 x fs; the uncertainty from the board's crystal tolerance and the timing granularity.
- The FSYNC pulse width, edge timing, levels and absolute ppm are named as not shown, with a pointer to #626.
- Full restore with proof: maps, binding, the bridge legs by PID with their recorded command lines, and the controller clock.
- One findings page and its index row.
Validation plan: `scripts/docs_check.py`, `scripts/check_doc_style.py`, `scripts/gen_toc.py --check`, `scripts/check_em_dash.py --base e4b771f9` and `scripts/check_doc_paths.py` in the pinned Markdown environment; `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py`, `scripts/check_feature_status.py --self-test` and `git diff --check`. All rc 0, unpiped, from the physical lane path. Local commit only, no push.
Blockers: none known. STOP conditions: the identity gate fails; the USB Audio card leaves the bench host; no bit clock or frame sync reaches McASP0.
