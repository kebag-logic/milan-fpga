# Evidence, [A431] round 3 of PR #618 (issue #617)

Head: `ddb0774779d10a9b0bd90a4822f4e5df9fdedb1b` (local, not pushed). Verilator 5.050, Yosys 0.66, sv2v v0.0.13. Home prefix redacted to `$HOME` in copied logs.

| File | What |
|---|---|
| `gate-summary-ddb0774.txt` | every gate: rc, name, exact command, seconds (85 entries, all rc 0) |
| `suite-tally-ddb0774.txt` | `scripts/suite_tally.py` over the 13 suite logs: 52,285 checks, 0 failures |
| `<gate>-ddb0774.log` | the gate logs at the head under 200 KB |
| `large-logs-sha256.txt` | sha256 and size of every log over 200 KB (gate logs and recorded probe runs), not copied |
| `explore-nco-head.log`, `explore-nco-fix.log` | `media_nco` built against `377d1ac3`'s NCO (10 failures, check 10) and the round-3 NCO (410 / 0) |
| `explore-j-fine-head.log`, `explore-j-fine-fix.log` | the committed `--fine` sweep against `377d1ac3`'s NCO (27 failures, 9 engagements) and the round-3 NCO (0) |
| `explore-ch-clean.log`, `explore-ch-rm7.log`, `explore-ch-rm8.log` | `chmap_capture` clean (371 / 0), RM7 (9 failures) and RM8 (12 failures) |
| `ooc-KL_media_nco-*.txt` | Yosys `stat` of `KL_media_nco` at 50 and 100 MHz, `377d1ac3` and head, with and without `-nodsp` |
| `recorded-settle-and-transient-summary.txt` | the recorded 60,000-column settled-lock runs (52, 0 tail slips) and the transient-limit runs (84-90 ppm) |
