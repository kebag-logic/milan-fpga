# Receipts: round 5, the held-egress ledger restated at 8x8/1if (the ruling on PR #992)

Head `67838b379f9e9ecb6cf6fbd0f162a5bb852ca570`, one commit on `507bce7f`, local and not pushed. Every file is text
and under 200 KB, and there is no .gz. A log over 190,000 B is kept as its first and last 90,000 B, with its full
size and sha256 noted at the cut (`tools/rcopy.py`). Scratch is under `/data-2/milan/tmp/lwsrppin-a834/r5/`. The
measurements graded here are round 4's results directories, under `/data-2/milan/tmp/lwsrppin-a834/r4/harness/`.
Raw logs carry local paths.

| File | Bytes | sha256 (16) | What it is |
|---|---:|---|---|
| `commit/67838b37.patch` | 23,403 | `1c7eab65d4233b10` | git show --stat --patch of the round's commit |
| `docs/docs-check-no-git__3.log` | 225 | `da13269812c948a9` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__11.log` | 128 | `244e5894820987e2` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__12-md.log` | 139 | `fae96bc5fc31e276` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__13.log` | 167 | `06dde9a3bc8e4ad9` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__14.log` | 242 | `79dce4dc64e4d578` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__15.log` | 146 | `1f719750a8609052` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__16.log` | 227 | `88d83848aecf8145` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__17.log` | 241 | `af9493d0e4acd65e` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__18.log` | 125 | `17d1d2360a98e818` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__19.log` | 1,568 | `b703a4a6f525637d` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__20.log` | 118 | `99cb09ed317195a6` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__22.log` | 2,752 | `8f8bce793ec90c04` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__23.log` | 3,293 | `862838344ece59e4` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__26.log` | 115 | `8cf5b60ee259205c` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__29.log` | 51,491 | `793e350cf87f1b9d` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__3.log` | 962 | `f2128b6da22b2651` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__30.log` | 20,246 | `7ada1451a0dbbd66` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__31.log` | 1,192 | `644dbaf9db7fc996` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__32.log` | 51,997 | `55b478563810a384` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__33.log` | 4,794 | `d3e9263bebd26fb0` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__34.log` | 3,453 | `f978e53937335528` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__35.log` | 40,599 | `69b6457c9b2090f6` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__36.log` | 5,040 | `3ffbecba0b2b203e` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__37.log` | 12,532 | `8b0909f387914a18` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__38.log` | 2,745 | `7a5a66dab5f5c22a` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__39.log` | 32,470 | `d9724c8fed8178ed` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__40.log` | 3,972 | `e6843f0327c32454` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__41.log` | 3,173 | `cf68b72f86b70cef` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__42.log` | 4,735 | `a96df99e553213a1` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__43.log` | 2,992 | `81d3b65e11fc556d` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__44.log` | 2,696 | `a57f331056f1f93e` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__45.log` | 101 | `f72e8b9a50f47881` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__46.log` | 128 | `1a15e66a07892f54` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__47-md.log` | 196 | `b3b5fb658a3edc1f` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__48.log` | 129 | `185c9f506448e385` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__49.log` | 3,596 | `9f126bf9dfc7cb55` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__50.log` | 26,881 | `3a447f4574f4a806` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__51.log` | 10,344 | `fbcfaeb03c29f8dd` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__52.log` | 29,010 | `264ce848510fc61f` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__53.log` | 3,749 | `be979dd5dcdee951` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-0__55.log` | 139,623 | `95585aa3f272bafa` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-1__14.log` | 50,475 | `1d069a0a79e79ec7` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-2__14.log` | 110,772 | `d8e0a3eb4cfec46a` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/docs-gates-2__15.log` | 180,201 | `7542e13080df50cc` | a docs.yml step's log (cut head and tail, over 190,000 B) |
| `docs/docs-gates-2__16.log` | 131,281 | `f2bebd6b0fd752dc` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/end` | 26 | `0843dcf721e08635` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/head` | 41 | `36c07c72ec74ce39` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/rc-main` | 2 | `9a271f2a916b0b6e` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/rc-md` | 2 | `9a271f2a916b0b6e` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/run.log` | 2,423 | `40db658f3154f28c` | docs.yml steps at 67838b37: one line per step with its rc |
| `docs/start` | 26 | `aa668fec260647d4` | a docs.yml step's log, or the run's head/start/end/rc |
| `docs/wire-accountability__4.log` | 5,076 | `de066064fa209d5a` | a docs.yml step's log, or the run's head/start/end/rc |
| `identity/identity.txt` | 1,736 | `043888eed1c47934` | image identity: the changed paths, the harness build inputs, the 28-file rebuild comparison |
| `identity/plat-ledger-67838b37.log` | 14,065 | `a4c6338f6eed4f25` | plat_ledger.py --build-dir at 67838b37, its log |
| `identity/sha-507bce7f.txt` | 3,796 | `43a714649ee03535` | the same at 507bce7f (round 3's build) |
| `identity/sha-67838b37.txt` | 3,796 | `43a714649ee03535` | sha256 of every ELF/bin/hex plat_ledger.py --build-dir writes at 67838b37 |
| `ledger/derivation.txt` | 924 | `5b29776e3b9c932d` | each figure: the tool's LEDGER, the rule computed apart in Decimal, the ruling's expected figure, the image that sets it |
| `ledger/egress-ledger-8x8-1if-from-log.log` | 844 | `bb2896e44fd4e23e` | egress_ledger.py --point 8x8-1if at 67838b37 on round 4's arm A 8x8/1if run log |
| `ledger/egress-ledger-8x8-1if.log` | 802 | `9b121f67076e2bf8` | egress_ledger.py --point 8x8-1if at 67838b37 on round 4's arm A 8x8/1if results (merge head image) |
| `ledger/egress-ledger-selftest.log` | 13,409 | `72ff12c6aa584eb6` | egress_ledger.py --selftest at 67838b37 (72 controls, 18 mutants) |
| `ledger/egress-ledger-train-8x8-1if.log` | 800 | `f5174a88a7aaeed9` | egress_ledger.py --point 8x8-1if at 67838b37 on round 4's backlog-owed results on the train's image 2509db68 |
| `ledger/measurements.txt` | 650 | `19e881e85e0ed7a6` | TRAIN and PINNED against round 4's backlog-owed.json (10 ns), and the results' image and file sha256 |
| `pr-body-before-r5.md` | 11,751 | `c1a0520666451331` | the live PR body as it read at the start of this round (updated 2026-11-24T22:48Z) |
| `tools/derive.py` | 1,556 | `606d0a09f45bea0b` | a script this round ran |
| `tools/docs5.sh` | 1,599 | `3eff0d734af051e7` | a script this round ran |
| `tools/docs_gates_r2.py` | 2,830 | `72fbe3f73ae40e28` | a script this round ran |
| `tools/index.py` | 2,950 | `809cbe24d07d00ac` | a script this round ran |
| `tools/poll.sh` | 397 | `7898288a11885780` | a script this round ran |
| `tools/rcopy.py` | 1,452 | `da02e309e1ce258c` | a script this round ran |
