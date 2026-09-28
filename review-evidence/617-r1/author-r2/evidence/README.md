# Evidence, [A428] round 2 of PR #618 (issue #617)

Head: `377d1ac3658feb8d544e6ed1005b186b67127f35` (local, not pushed). Verilator 5.050, Yosys 0.66, sv2v v0.0.13.

| File | What |
|---|---|
| `gate-summary-377d1ac3.txt` | every gate: rc, name, exact command, seconds (79 entries, all rc 0) |
| `suite-tally-377d1ac3.txt` | `scripts/suite_tally.py` over the eight suite logs: 19,600 checks, 0 failures |
| `suite_*-377d1ac3.log`, `builder_bank-377d1ac3.log`, `lint-*`, `xvlog-*`, `yosys_*`, `ooc_*` | the gate logs at the head (home prefix redacted to `$HOME`) |
| `large-logs-sha256.txt` | sha256 and size of the two gate logs over 200 KB, not copied |
| `base-ce550952-junction.log`, `base-ce550952-dp.log` | the committed round-2 harness against the `ce550952` crossbar and datapath (scratch tree; wrapper aligner binding set to `ce550952`'s; datapath placement tap on the base's `tdm_hold_r[3]`): 386/5240 and 7/311 fail |
| `r1-5546b976-junction.log`, `r1-5546b976-dp.log` | the same harness against the round-1 head's crossbar, datapath and aligner binding: the CRF band reproduced, 414/5240 and 25/311 fail |
| `render-t30-round1-binding.log` | `milan_dp_render` tdm8render with the round-1 aligner binding (for the T30 CRF walk comparison) |
