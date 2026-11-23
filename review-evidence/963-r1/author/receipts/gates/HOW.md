# The gates at the intermediate heads (superseded)

These ran at the intermediate heads: `b63c4179` for the firmware shards, the firmware-unit steps, the twin and the
harness self-test, and `e54e064a` for the portable and docs gates. That code observed through the cold `aecp_running`,
which `e9627b31` replaced. So `gates-final/` supersedes every one of them, at `e9627b31` (firmware, twin) and
`1b3e27ce` (portable, docs). The exception is the harness self-test: this lane changes no file under `tb/`, so its run
at `b63c4179` (`twin-selftest/harness-selftest.log`, `self-test: 0 failures`) covers the final head's harness too.
