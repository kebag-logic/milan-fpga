[A850] #1013, branch `1013-pins`, head `a6864a49293ba3d0df37029abfa581468ef78dce` on `dev-soft-core` `c34e7d8b` (merged as `d0483d08`, no conflict). Local, not pushed, nothing posted.

**Review ready.** The gPTP pin is FPGA-gPTP `3ce71b768a2f6f6a5274c127080146e755d02275` (the merge of its PR #110), by the ruling on #1013. The issue first named `3009f9a2`, whose PR #112 test runner exceeds two of this repository's ratchets. `a6864a49` moves the gitlink and regenerates by their generators everything that names it: the pin sites, both diagrams and the ROM ledger row. It also updates the adoption record and the change log.

**Image inputs.** `hdl/` (the microcode generator included) and `syn/` have identical tree hashes at `3ce71b76` and `3009f9a2`. The ledger row's image digest is the same, `52293128...` (`receipts/pin/image-inputs.txt`). So the routes, and the image-level gates run at `d0483d08`, stand.

| Check | Commit | Result |
|---|---|---|
| `check_py_idiom.py`, `measure_test_evidence.py` | `a6864a49` | rc 0 each, budgets unchanged |
| `make -C tb/verilator/gptp_plane` | `a6864a49` | 102 checks; phc-step 8/8; link_delay 9/9 |
| `make -C tb/verilator/gptp_shadow` | `a6864a49` | 483 checks; 14/14 controls; lifecycle PASS |
| `milan_dp` `gptp`, `gptp-lat` | `a6864a49` | 242/242 each |
| Docs workflow `run:` steps | `a6864a49` | 56 rc 0, 24 skipped, 3 failed: the RV32 SDK install-verify in three jobs, which refuses on this host as on the base |
| Firmware gate, four shards `--require-rv32 --self-test` | `d0483d08` | rc 0 each; 847 of 847 plants caught |
| Stack boundary gate, both CI legs | `d0483d08` | PASS, PASS |
| `gptp_tables`, `gptp_txts`, `tsn_fuzz`, `milan_dp_gm_steps`, `milan_dp_gptp` (physical) | `d0483d08` | all pass |
| Egress ledger 8x8-1if, head and base | `d0483d08` | PASS; rows equal |
| `plat_ledger`, head and base | `d0483d08` | PASS; points equal |
| Old generator (1213ac5b) under the new phases | — | `gptp_plane` 32 FAIL, `gptp_shadow` 15 FAIL |
| Routes 1x1/1if, 8x8/1if against the base `c34e7d8b` | `d0483d08` | identical at every directive; #818 floor met at every corner; 8x8 on ExtraTimingOpt |

LUT / FF / RAMB36 against the base: 1x1/1if 0 / 0 / 0 (32,582 / 42,803 / 63); 8x8/1if 0 / 0 / 0 (45,810 / 53,378 / 82). No growth to declare.

Delta since the previous packet (`37a98e17`): one commit, `a6864a49`. It changes the gitlink, the pin sites and permalinks, both diagrams, one ledger row, `SUBMODULES.md`'s record, the change log, and one comment in `tb/verilator/gptp_plane/link_delay.py`.
