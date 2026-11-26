[A850] #1013 / PR #1016, round 2. Branch `1013-pins`, head `e5d8a71b6fa90352eca72314c7bd2275a1b20285`: one commit on `a6864a49`. Local, not pushed, nothing posted. Pins unchanged: gPTP `3ce71b76`, tsn-c-stack `a795471c`.

| Finding | Outcome at `e5d8a71b` |
|---|---|
| R937-F1, R938-F1: phase 22's Follow_Up check passes with a stale offset or no pair | The graded pair is built 400 ns off, where the background pairs are built at 0. Two checks replace the old one: `the graded Follow_Up is used: its offset is fresh` (it moved by more than 200 ns) and `its offset uses the delay floored at -800 ns` (within 64 ns of the previous offset less 400). Two controls in `mutants.py` are each caught by the first check at -263 ns: `public_bank_keeps_a_stale_offset` (the bank holds `pub_offset_o`) and `graded_follow_up_not_sent` (the harness omits the graded pair, as both reviewers' probe did). At the 1213ac5b generator, `#109 -81 ns: the graded Follow_Up is used: its offset is fresh` fails (R937's verification). README row 22 states what is graded |
| R937-F2: "phase 6 grades every row" | `GPTP_PLANE.md`: phase 6 grades asCapable and the used delay, reading the engine's signed word; `gptp_shadow` phase 22 and the `milan_dp` legs grade the public word |
| R938-F2: the old-generator claim includes an unrun datapath comparison | Run now: `milan_dp` `gptp` with the 1213ac5b generator fails 3 of 242 (`[#109] delay -81 ns: asCapable kept`, -263, -5,000,000). The PR states which legs ran (`gptp`, not `gptp-lat`) |
| R938-F3: route equality beyond the pairs | `SUBMODULES.md`, the change log and the PR state equality for the three paired routes only. The 8x8 AltSpreadLogic_high row is marked "no base pair". The PR no longer says placements are identical |
| R937-R1, R938-R1: blank line splits phase 6 from the table | removed |
| R937-R2: "then" without antecedent | "The Sync path uses the delay signed. So two over-stated latency constants cancel in the offset." |
| R937-R3: two `[A850]` lines | the PR body has one |
| R937-S1: harness-model check | renamed `harness precondition: the peer presents a negative delay` |

| Check at `e5d8a71b` | Result |
|---|---|
| `make -C tb/verilator/gptp_shadow` | 490 checks; 16/16 controls, the two new ones by their named check; lifecycle PASS ("sixteen named defects") |
| `make -C tb/verilator/gptp_plane` | 102 checks; phc-step 8/8; link_delay 9/9 |
| `milan_dp` `gptp`, `gptp-lat` | 242/242 each |
| 1213ac5b generator: `gptp_plane` run, `gptp_shadow` run, `milan_dp` `gptp` | 32 of 102, 25 of 490, 3 of 242 FAIL |
| `check_py_idiom.py`, `measure_test_evidence.py` (in the docs run) | rc 0 each; both budget files byte-identical to the base |
| Docs workflow `run:` steps | 56 rc 0, 24 skipped, 3 failed: the RV32 SDK install-verify in three jobs, which refuses on this host as on the base |
| Image inputs | no file under `hdl`, `syn`, `sw`, `configs`, `constraints`, `avdecc` or any gitlink changes since `a6864a49`; tree hashes equal (`receipts/image-inputs.txt`). The routes and image-level gates stand |

Not re-run this round, as unchanged by it: the firmware gate, the boundary gate, `gptp_tables`, `gptp_txts`, `tsn_fuzz`, `milan_dp_gm_steps`, the physical leg, the ledgers and the routes. Their inputs are unchanged since `d0483d08`, save the test-runner-only gitlink move of round 1.
