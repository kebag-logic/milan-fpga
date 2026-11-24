# Receipts: [A834] milan-fpga pin bump to lwSRP d1bb4f4e, round 1

Parent: lane `20-lwsrp-pin-d1bb4f4`, head `dbba60e6` (pushed), base `dev-soft-core` `aa30d77f`. lwSRP `d1bb4f4e`
(tree `ba42b837`, the reviewed `25b5a740`'s). Host paths in logs are this lane's scratch and are not published.
Tools: pinned Verilator 5.050, the pinned RV32 SDK, the LiteX tree's interpreter (`tools/penv.sh`).
`402834ac` -> `dbba60e6` changes only docstrings in `tb/verilator/milan_dp/twin_mrp.py`, which only the twin reads.
So the gates that read none of the twin's files (firmware shards, harness arm A and answering-every-port, ledger,
OOC, srptx) ran at `402834ac` and hold at `dbba60e6`. The twin and docs gates ran at both heads.

- `own-leaveall/`: `srp_own_leaveall.cpp`'s two arms run alone (`tools/own_la.py`): at `08ee86e8` (the reproduction
  commit `3fb8cc76`), at `d1bb4f4e` (`002a195b`) and at `402834ac`; `summary.txt` grades every `OWN-LA` line
  (`tools/ola_sum.py`).
- `firmware/`: `test_ctrl_firmware.py --require-rv32 --self-test --shard k/4`, k = 0-3; `summary.txt` (rc, times,
  counts, the SRP host arms).
- `twin/`: `make twin` and `make twin-plants` twice, at `402834ac` and `dbba60e6` (`*-times.txt` rc, times, Verilator);
  `selftest-mutants.txt` (each planted grade fault against `twin_mrp.py --selftest`; the mutants are in
  `tools/twin-mut/`); `leaveall-room.txt` (LeaveAll frames, omissions, full frames and least spare room per half).
- `srptx/`: `make -k srptx` and `make srptx-mutants` at the base `aa30d77f` and the head `402834ac`; `summary.txt` and
  the per-scenario finding lines; for ISSUE-srptx.md.
- `budget-model/`: `load_grade.py --check`, `flip_grade.py --check --point 1x1/1if` and `--point 8x8/1if`, at the head
  and at the base (`base-*`, byte-identical).
- `harness/`: the CPU budget harness: arm A (`run-1x1`, `run-8x8-1if`), `answering-every-port` (`-every`),
  `answering-later` (`-later`), with `grade-*.txt` (`tools/harness_grade.py`), tables, results, build plans; the egress
  ledger at 8x8/1if and its self-test; `la-window-8x8-1if.txt` (`tools/la_window.py`, the own LeaveAll in the save
  groups); the harness self-test; `times.txt`.
- `ledger/`: `plat_ledger.py --self-test` at the head and `plat_ledger.py` at the base; `image-deltas.txt` (every
  image's sections and every changed object, `tools/img_delta.py`); `margins.md` (ROM and SRAM against their banks,
  base and head); `test_ctrl_memory.py`.
- `ooc/`: `syn/ooc/ctrl_memory_ooc.py` mapped at the base and the head (twice, `head2`), each through
  `vivado-slot.sh` (2 slots): RAMB36, RAMB18, LUT, FF per region; the plans.
- `docs/`: `pin-docs.log` (diagram generator `--check` and `--selftest`, PNG and submodule documentation gates);
  `docs.yml`'s steps (`tools/docs_gates.py`) at `402834ac` and at `dbba60e6`, with the two renderer steps re-run with
  the pinned Markdown renderer (`*-md.log`) and builder leg 0 re-run with the SDK at `$HOME/br-milan-rv32`
  (`dbba60e6/leg0-rerun.txt`, `docs-gates-1__14-rerun.log`). At `402834ac` the idiom gate's two findings led to
  `dbba60e6`, and both builder legs were refused for the untracked `dispatch-build/`.
- `patches/`: `git format-patch --no-binary aa30d77f..dbba60e6`.
- `push/`: the privacy check and the remote branch head after the push.
- `tools/`: this lane's scripts and its tool environment.

## Files

| File | Bytes | sha256 (16) |
|---|---:|---|
| `budget-model/base-flip_1x1.log` | 1,784 | `1402ddc68c0914d2` |
| `budget-model/base-flip_8x8_1if.log` | 1,364 | `e38ea5785c40a017` |
| `budget-model/base-load_check.log` | 1,793 | `5ee7e910c2aa8d71` |
| `budget-model/flip_1x1.log` | 1,784 | `1402ddc68c0914d2` |
| `budget-model/flip_8x8_1if.log` | 1,364 | `e38ea5785c40a017` |
| `budget-model/load_check.log` | 1,793 | `5ee7e910c2aa8d71` |
| `docs/402834ac/ci-cancel-tail__2.log` | 471 | `6455ef8ed100e017` |
| `docs/402834ac/ci-fail-fast__2.log` | 471 | `6455ef8ed100e017` |
| `docs/402834ac/ci-fail-fast__3.log` | 471 | `6455ef8ed100e017` |
| `docs/402834ac/ci-manifest__6.log` | 208 | `c242827f00159daf` |
| `docs/402834ac/docs-check-no-git__3.log` | 225 | `e3d1651e59e9d771` |
| `docs/402834ac/docs-gates-0__11.log` | 128 | `0483501771f7edf2` |
| `docs/402834ac/docs-gates-0__12-md.log` | 191 | `3136d20961477d25` |
| `docs/402834ac/docs-gates-0__12.log` | 163 | `06541123d43c489a` |
| `docs/402834ac/docs-gates-0__13.log` | 167 | `06dde9a3bc8e4ad9` |
| `docs/402834ac/docs-gates-0__14.log` | 242 | `79dce4dc64e4d578` |
| `docs/402834ac/docs-gates-0__15.log` | 146 | `1f719750a8609052` |
| `docs/402834ac/docs-gates-0__16.log` | 227 | `88d83848aecf8145` |
| `docs/402834ac/docs-gates-0__17.log` | 241 | `af9493d0e4acd65e` |
| `docs/402834ac/docs-gates-0__18.log` | 125 | `17d1d2360a98e818` |
| `docs/402834ac/docs-gates-0__19.log` | 1,568 | `b703a4a6f525637d` |
| `docs/402834ac/docs-gates-0__20.log` | 118 | `99cb09ed317195a6` |
| `docs/402834ac/docs-gates-0__22.log` | 2,752 | `8f8bce793ec90c04` |
| `docs/402834ac/docs-gates-0__23.log` | 3,293 | `862838344ece59e4` |
| `docs/402834ac/docs-gates-0__26.log` | 115 | `621eed75d781be28` |
| `docs/402834ac/docs-gates-0__29.log` | 51,487 | `9fc56e3e0dffb313` |
| `docs/402834ac/docs-gates-0__3.log` | 958 | `c7f461ab3a2a7544` |
| `docs/402834ac/docs-gates-0__30.log` | 20,246 | `8dc5ba0d3ea8973a` |
| `docs/402834ac/docs-gates-0__31.log` | 1,192 | `644dbaf9db7fc996` |
| `docs/402834ac/docs-gates-0__32.log` | 52,049 | `61d09b7007b3f90a` |
| `docs/402834ac/docs-gates-0__33.log` | 4,794 | `d3e9263bebd26fb0` |
| `docs/402834ac/docs-gates-0__34.log` | 3,453 | `f978e53937335528` |
| `docs/402834ac/docs-gates-0__35.log` | 40,599 | `417ab22513910597` |
| `docs/402834ac/docs-gates-0__36.log` | 5,040 | `cd027477f9fdbe55` |
| `docs/402834ac/docs-gates-0__37.log` | 12,531 | `5fb874bb636730c9` |
| `docs/402834ac/docs-gates-0__38.log` | 2,745 | `d2f50d329a7d5ca6` |
| `docs/402834ac/docs-gates-0__39.log` | 29,814 | `fd66f6d74af5c261` |
| `docs/402834ac/docs-gates-0__40.log` | 3,972 | `7c1d8db5986b41c4` |
| `docs/402834ac/docs-gates-0__41.log` | 3,173 | `cf68b72f86b70cef` |
| `docs/402834ac/docs-gates-0__42.log` | 4,735 | `df9f1e6d666f4b4b` |
| `docs/402834ac/docs-gates-0__43.log` | 250 | `97d7872d2a593c1e` |
| `docs/402834ac/docs-gates-0__44.log` | 2,696 | `a57f331056f1f93e` |
| `docs/402834ac/docs-gates-0__45.log` | 101 | `52adb085ac53b3a3` |
| `docs/402834ac/docs-gates-0__46.log` | 128 | `1a15e66a07892f54` |
| `docs/402834ac/docs-gates-0__47-md.log` | 201 | `ca29cf3b7fc6241d` |
| `docs/402834ac/docs-gates-0__47.log` | 165 | `73ae4c76fba1c3c9` |
| `docs/402834ac/docs-gates-0__48.log` | 129 | `185c9f506448e385` |
| `docs/402834ac/docs-gates-0__49.log` | 3,596 | `9f126bf9dfc7cb55` |
| `docs/402834ac/docs-gates-0__50.log` | 26,735 | `c67bc1b46cdc8542` |
| `docs/402834ac/docs-gates-0__51.log` | 10,344 | `fbcfaeb03c29f8dd` |
| `docs/402834ac/docs-gates-0__52.log` | 29,010 | `264ce848510fc61f` |
| `docs/402834ac/docs-gates-0__53.log` | 3,749 | `be979dd5dcdee951` |
| `docs/402834ac/docs-gates-0__55.log` | 139,623 | `d6e9dc0b8542ab4c` |
| `docs/402834ac/docs-gates-1__14.log` | 183 | `eae1e363c7bd2fec` |
| `docs/402834ac/docs-gates-2__14.log` | 183 | `eae1e363c7bd2fec` |
| `docs/402834ac/docs-gates-2__15.log.gz` | 27,145 | `2d8fd710a8d1bc05` |
| `docs/402834ac/docs-gates-2__16.log` | 131,281 | `f2bebd6b0fd752dc` |
| `docs/402834ac/not_run.txt` | 2,347 | `6629702b458b5d28` |
| `docs/402834ac/run.log` | 2,602 | `d23b72e401478d08` |
| `docs/402834ac/wire-accountability__4.log` | 5,076 | `de066064fa209d5a` |
| `docs/dbba60e6/ci-cancel-tail__2.log` | 471 | `6455ef8ed100e017` |
| `docs/dbba60e6/ci-fail-fast__2.log` | 471 | `6455ef8ed100e017` |
| `docs/dbba60e6/ci-fail-fast__3.log` | 471 | `6455ef8ed100e017` |
| `docs/dbba60e6/ci-manifest__6.log` | 208 | `c242827f00159daf` |
| `docs/dbba60e6/docs-check-no-git__3.log` | 225 | `00c4cd62094de1fd` |
| `docs/dbba60e6/docs-gates-0__11.log` | 128 | `0483501771f7edf2` |
| `docs/dbba60e6/docs-gates-0__12-md.log` | 232 | `b78bd1a0f6e57740` |
| `docs/dbba60e6/docs-gates-0__12.log` | 163 | `06541123d43c489a` |
| `docs/dbba60e6/docs-gates-0__13.log` | 167 | `06dde9a3bc8e4ad9` |
| `docs/dbba60e6/docs-gates-0__14.log` | 242 | `79dce4dc64e4d578` |
| `docs/dbba60e6/docs-gates-0__15.log` | 146 | `1f719750a8609052` |
| `docs/dbba60e6/docs-gates-0__16.log` | 227 | `88d83848aecf8145` |
| `docs/dbba60e6/docs-gates-0__17.log` | 241 | `af9493d0e4acd65e` |
| `docs/dbba60e6/docs-gates-0__18.log` | 125 | `17d1d2360a98e818` |
| `docs/dbba60e6/docs-gates-0__19.log` | 1,568 | `b703a4a6f525637d` |
| `docs/dbba60e6/docs-gates-0__20.log` | 118 | `99cb09ed317195a6` |
| `docs/dbba60e6/docs-gates-0__22.log` | 2,752 | `8f8bce793ec90c04` |
| `docs/dbba60e6/docs-gates-0__23.log` | 3,293 | `862838344ece59e4` |
| `docs/dbba60e6/docs-gates-0__26.log` | 115 | `621eed75d781be28` |
| `docs/dbba60e6/docs-gates-0__29.log` | 51,487 | `9fc56e3e0dffb313` |
| `docs/dbba60e6/docs-gates-0__3.log` | 958 | `4e1e18f4618ca992` |
| `docs/dbba60e6/docs-gates-0__30.log` | 20,246 | `8dc5ba0d3ea8973a` |
| `docs/dbba60e6/docs-gates-0__31.log` | 1,192 | `644dbaf9db7fc996` |
| `docs/dbba60e6/docs-gates-0__32.log` | 52,045 | `826f9b2f1e74b604` |
| `docs/dbba60e6/docs-gates-0__33.log` | 4,794 | `d3e9263bebd26fb0` |
| `docs/dbba60e6/docs-gates-0__34.log` | 3,453 | `f978e53937335528` |
| `docs/dbba60e6/docs-gates-0__35.log` | 40,599 | `417ab22513910597` |
| `docs/dbba60e6/docs-gates-0__36.log` | 5,040 | `cd027477f9fdbe55` |
| `docs/dbba60e6/docs-gates-0__37.log` | 12,531 | `5fb874bb636730c9` |
| `docs/dbba60e6/docs-gates-0__38.log` | 2,745 | `d2f50d329a7d5ca6` |
| `docs/dbba60e6/docs-gates-0__39.log` | 29,814 | `fd66f6d74af5c261` |
| `docs/dbba60e6/docs-gates-0__40.log` | 3,972 | `7c1d8db5986b41c4` |
| `docs/dbba60e6/docs-gates-0__41.log` | 3,173 | `cf68b72f86b70cef` |
| `docs/dbba60e6/docs-gates-0__42.log` | 4,735 | `df9f1e6d666f4b4b` |
| `docs/dbba60e6/docs-gates-0__43.log` | 2,992 | `e2f52c452a64ce47` |
| `docs/dbba60e6/docs-gates-0__44.log` | 2,696 | `a57f331056f1f93e` |
| `docs/dbba60e6/docs-gates-0__45.log` | 101 | `52adb085ac53b3a3` |
| `docs/dbba60e6/docs-gates-0__46.log` | 128 | `1a15e66a07892f54` |
| `docs/dbba60e6/docs-gates-0__47-md.log` | 201 | `ca29cf3b7fc6241d` |
| `docs/dbba60e6/docs-gates-0__47.log` | 165 | `73ae4c76fba1c3c9` |
| `docs/dbba60e6/docs-gates-0__48.log` | 129 | `185c9f506448e385` |
| `docs/dbba60e6/docs-gates-0__49.log` | 3,596 | `9f126bf9dfc7cb55` |
| `docs/dbba60e6/docs-gates-0__50.log` | 26,735 | `b0933ef10586bda1` |
| `docs/dbba60e6/docs-gates-0__51.log` | 10,344 | `fbcfaeb03c29f8dd` |
| `docs/dbba60e6/docs-gates-0__52.log` | 29,010 | `264ce848510fc61f` |
| `docs/dbba60e6/docs-gates-0__53.log` | 3,749 | `be979dd5dcdee951` |
| `docs/dbba60e6/docs-gates-0__55.log` | 139,623 | `bd9296b465d4c743` |
| `docs/dbba60e6/docs-gates-1__14-rerun.log` | 50,364 | `260215ca0fb301c2` |
| `docs/dbba60e6/docs-gates-1__14.log` | 661 | `e6188ab4829651d9` |
| `docs/dbba60e6/docs-gates-2__14.log` | 110,350 | `074b6518ede0e85f` |
| `docs/dbba60e6/docs-gates-2__15.log.gz` | 27,145 | `89ff9c7369300d58` |
| `docs/dbba60e6/docs-gates-2__16.log` | 131,281 | `f2bebd6b0fd752dc` |
| `docs/dbba60e6/leg0-rerun.txt` | 198 | `715143391e632136` |
| `docs/dbba60e6/not_run.txt` | 2,347 | `6629702b458b5d28` |
| `docs/dbba60e6/run.log` | 2,602 | `3628938eb21c039f` |
| `docs/dbba60e6/wire-accountability__4.log` | 5,076 | `de066064fa209d5a` |
| `docs/pin-docs.log` | 247 | `2d5190139fe4c6e0` |
| `firmware/gate-0.log.gz` | 7,744 | `d5bc5a397593b5c7` |
| `firmware/gate-1.log.gz` | 33,396 | `41156c70d56c8152` |
| `firmware/gate-2.log.gz` | 12,203 | `f278d6ddf2736e5d` |
| `firmware/gate-3.log.gz` | 19,673 | `a51421bca2a113a8` |
| `firmware/summary.txt` | 1,110 | `231c42a2a99b6feb` |
| `harness/build-1x1-every.json` | 7,813 | `909a814f4fa7ceaa` |
| `harness/build-1x1-later.json` | 7,808 | `988b8d0980994108` |
| `harness/build-1x1.json` | 7,746 | `58bb40bd303b78e6` |
| `harness/build-8x8-1if-every.json` | 7,436 | `914f551a62c819c4` |
| `harness/build-8x8-1if-later.json` | 7,431 | `562dac7a30f9d64f` |
| `harness/build-8x8-1if.json` | 7,369 | `09d8ce6599ab9702` |
| `harness/egress-ledger-8x8-1if.log` | 782 | `9c2ff0b4a1c5dff6` |
| `harness/egress-ledger-selftest.log.gz` | 1,529 | `f67549e4cdea335d` |
| `harness/grade-1x1-every.txt` | 406 | `21e21b7034432abb` |
| `harness/grade-1x1-later.txt` | 403 | `f49dbc63f2889382` |
| `harness/grade-1x1.txt` | 1,175 | `d24324d813dd2d8d` |
| `harness/grade-8x8-1if-every.txt` | 411 | `fa68a199a0b5eabc` |
| `harness/grade-8x8-1if-later.txt` | 406 | `b916554b4f6993e6` |
| `harness/grade-8x8-1if.txt` | 1,446 | `b2018f3f4378011e` |
| `harness/la-window-8x8-1if.txt` | 1,794 | `2876e0dd8e0e9757` |
| `harness/results-1x1-every.json.gz` | 44,919 | `eb1ddda466aefe92` |
| `harness/results-1x1-later.json.gz` | 10,667 | `39d9d319ce938dec` |
| `harness/results-1x1.json.gz` | 129,002 | `3fa1c9b18751ce98` |
| `harness/results-8x8-1if-every.json.gz` | 122,323 | `d224554640d3873c` |
| `harness/results-8x8-1if-later.json.gz` | 10,458 | `86b5926ee6f6b0a1` |
| `harness/results-8x8-1if.json.gz` | 130,463 | `118e7cff0a2eed7f` |
| `harness/run-1x1-every.log.gz` | 5,800 | `f05624d65df8fb67` |
| `harness/run-1x1-later.log.gz` | 4,562 | `2cca8bed4f7b255f` |
| `harness/run-1x1.log.gz` | 5,944 | `bf2bacb84083511a` |
| `harness/run-8x8-1if-every.log.gz` | 8,191 | `0e2ca5f5ae4cbd27` |
| `harness/run-8x8-1if-later.log.gz` | 4,537 | `b4cbefa86bb250f5` |
| `harness/run-8x8-1if.log.gz` | 5,947 | `63424f3e570dab44` |
| `harness/selftest.log.gz` | 44,044 | `8bc0ffe2ef340c49` |
| `harness/table-1x1-every.md.gz` | 7,754 | `2914363e1300ca65` |
| `harness/table-1x1-later.md.gz` | 2,427 | `c72dbaf7aef0f4b2` |
| `harness/table-1x1.md.gz` | 25,725 | `ceb54b1e3d3ff774` |
| `harness/table-8x8-1if-every.md.gz` | 16,927 | `1dfda84bb6e56927` |
| `harness/table-8x8-1if-later.md.gz` | 2,391 | `b8928f877d968164` |
| `harness/table-8x8-1if.md.gz` | 25,508 | `409d29d817f0afbd` |
| `harness/times.txt` | 974 | `a850db02d28008aa` |
| `ledger/image-deltas.txt` | 4,404 | `ca616986859b6b9e` |
| `ledger/margins.md` | 1,603 | `260e036dc1709a04` |
| `ledger/plat_ledger-base.log` | 13,988 | `631a97d5b79251ed` |
| `ledger/plat_ledger-head-selftest.log` | 17,226 | `8457bc4b58233543` |
| `ledger/test_ctrl_memory.log.gz` | 8,022 | `e4e6ac34590d2a12` |
| `ledger/times.txt` | 212 | `3b60566599cdd26d` |
| `ooc/base.tsv` | 239 | `59a634ffaf4bd9bf` |
| `ooc/head.tsv` | 239 | `2fbcfa62677053f0` |
| `ooc/head2.tsv` | 239 | `2fbcfa62677053f0` |
| `ooc/plan-base.json` | 1,688 | `00d04b5547c834ed` |
| `ooc/plan-head.json` | 1,688 | `9a33ea82d7cc23d8` |
| `ooc/times.txt` | 196 | `96a8e9d6930b56b1` |
| `ooc/vivado-head.log.gz` | 17,089 | `e2db28e4bbc59e06` |
| `own-leaveall/base-08ee86e8.log.gz` | 15,470 | `e6b16dd3498348e8` |
| `own-leaveall/head-402834ac.log.gz` | 4,712 | `41e77610adff1a8f` |
| `own-leaveall/head-d1bb4f4e.log.gz` | 4,684 | `f2ec72183a3827b6` |
| `own-leaveall/ola_sum.py` | 849 | `fcbad81ab78d4838` |
| `own-leaveall/own_la.py` | 866 | `a5fa5dae2f55ea69` |
| `own-leaveall/summary.txt` | 1,388 | `98db84d00b7b8cbb` |
| `patches/0001-Reproduce-lwSRP-20-at-the-board-Lv-within-240-ms-of-.patch` | 17,501 | `f843bfd67c5ea455` |
| `patches/0002-Pin-lwSRP-d1bb4f4e-lwSRP-PR-21-an-Applicant-takes-on.patch` | 23,863 | `d00ec5c489bbaa98` |
| `patches/0003-Grade-the-twin-s-own-LeaveAll-as-one-Applicant-event.patch` | 24,244 | `50776bf6219d0bab` |
| `patches/0004-Wrap-the-twin-grade-s-docstring-at-120-columns-and-d.patch` | 1,894 | `35ec385499e427ed` |
| `push/push.txt` | 155 | `66943de08f3d0cc4` |
| `srptx/aa30-base.lines.gz` | 5,101 | `97f2d8c91b1f0109` |
| `srptx/base-srptx-mutants.log` | 1,285 | `e1455efafd371b58` |
| `srptx/base-srptx.log.gz` | 17,211 | `e7123f8ce8d369fb` |
| `srptx/head-srptx-mutants.log` | 1,285 | `600129986003201f` |
| `srptx/head-srptx.log.gz` | 9,283 | `d39c6331f3381661` |
| `srptx/head.lines.gz` | 5,381 | `9e61d4d7874016b0` |
| `srptx/summary.txt` | 502 | `a87073eac078f650` |
| `srptx/times.txt` | 680 | `c799a35887f3d1a2` |
| `tools/docs.sh` | 361 | `a4fe7be91b3b82e1` |
| `tools/docs_gates.py` | 2,377 | `eae504e1e0f101a0` |
| `tools/harness.sh` | 599 | `506f545d03110dff` |
| `tools/harness_grade.py` | 2,630 | `92c7ea8e07412d00` |
| `tools/hself.sh` | 365 | `23d36775abe4ab55` |
| `tools/img_delta.py` | 2,033 | `57a54c9e7c825009` |
| `tools/index.py` | 567 | `5ca9836ec2021f33` |
| `tools/la_room.py` | 1,050 | `d47b7681bb3eab2e` |
| `tools/la_window.py` | 2,682 | `4f0a93f9bcf11dad` |
| `tools/ledger.sh` | 431 | `16cfa855d2fe9d96` |
| `tools/ola_sum.py` | 849 | `fcbad81ab78d4838` |
| `tools/ooc.sh` | 471 | `4cf66917eed58d6e` |
| `tools/own_la.py` | 866 | `a5fa5dae2f55ea69` |
| `tools/penv.sh` | 663 | `89fda3a71eaf2c84` |
| `tools/plants.sh` | 483 | `ce2f61353ca7fab9` |
| `tools/shard.sh` | 465 | `38488e580750d1eb` |
| `tools/srptx.sh` | 498 | `d222c4ea66b420b7` |
| `tools/srptx_lines.py` | 591 | `6c37a77bf9a216e4` |
| `tools/srptx_sum.py` | 817 | `c3591be5ec8959e6` |
| `tools/twin-mut/mutants.txt` | 298 | `5007023df9669fd6` |
| `tools/twin-mut/mvrp-walk-off.py` | 23,546 | `9057f7796c283b39` |
| `tools/twin-mut/no-fourpacked.py` | 23,502 | `f24ccc13f34a30ea` |
| `tools/twin-mut/no-txlaf.py` | 23,537 | `43705623a7bc0e34` |
| `tools/twin-mut/old-rla-before-after.py` | 23,713 | `6f6fa199dc4ba69f` |
| `tools/twin-mut/room-1499.py` | 23,550 | `342cbfaaa3c8f0c8` |
| `tools/twin-mut/run.py` | 324 | `378108e0a6b09f0e` |
| `twin/402834ac-plants-1.log.gz` | 6,012 | `1ce5e1548f2b74fa` |
| `twin/402834ac-plants-2.log.gz` | 6,014 | `96660596f09d6030` |
| `twin/402834ac-times.txt` | 241 | `16e71e9d10f18ed3` |
| `twin/402834ac-twin.log.gz` | 20,225 | `947e59be3f14c920` |
| `twin/dbba60e6-plants-1.log.gz` | 6,013 | `cef711303a9abb40` |
| `twin/dbba60e6-plants-2.log.gz` | 6,017 | `a4c6b4d33236dde3` |
| `twin/dbba60e6-times.txt` | 379 | `8cc3f78162b23c83` |
| `twin/dbba60e6-twin.log.gz` | 4,099 | `644a30072de40486` |
| `twin/leaveall-room.txt` | 504 | `cebff616d74b1bbd` |
| `twin/selftest-mutants.txt` | 298 | `5007023df9669fd6` |
