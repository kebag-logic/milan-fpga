# HANDOFF r3: [A814] correction round for PR #966 (#884, #665 F6)

Status: **REVIEW READY** at `8167b70d` (2026-11-22; REVIEW-READY.md). Base of the round: `f15b3a7d` (PR #966's head, pushed by the manager as
`884-gptp-firmware`). Lane `/data-2/milan/lanes/opt-gptp-sw`, branch `opt-gptp-sw-1`; local commits only, no push.
Reviews answered: R884-1 (#966 issuecomment-7074604747), R883-1 (#966 issuecomment-7075220700), and the second-hart
lane's section 9 on #872 (issuecomment-7075152882).

## Findings and their state

| Finding | Severity | State | Fix commit | Regression test (fails at `f15b3a7d`) | Plants |
|---|---|---|---|---|---|
| R884-1-F1 publication tear (KL_mbx_cdc) | MAJOR | fixed | `8121e098` | `tb/verilator/mbx/tb_cdc_pub.sv` (53 checks; 12 fail on the old crossing, the reviewed ordering among them); `split-sw` `[GPTP] a commit while one crosses...` (old crossing: `0x2222222233333333`) | `cdc_pub_mutants.py`, 5 of 5 |
| R884-1-F2 Sync without Follow_Up renews the deadline | MAJOR | fixed | `7b74d5ea` | `Scripted.SyncWithoutItsFollowUpLetsTheGrandmasterAge`, `...ClearsTheVerdictOfAPortThatIsNeverGrandmaster`, `SyncAndAnnounceWithoutFollowUpNeverHoldTheVerdict` | `sync-alone-renews-deadline`, `pair-renews-no-deadline`; `follow-up-timeout-500` (`64a473be`) |
| R884-1-F3 late second responder never ceases | MAJOR | fixed | `7b74d5ea` | `ASecondResponderAfterTheFirstsFollowUpStillCeases`, `ARequestAnsweredByOneClockEndsTheRun`, `OneClockAnsweringTwiceIsNotAsCapableButDoesNotCease` | `late-second-responder-ignored`, `run-survives-a-clean-request`, `one-clock-twice-ceases`, `cease-never-ends` |
| R884-1-F4 Follow_Up without its information TLV | MAJOR | fixed | `7b74d5ea` | `FollowUpWithoutItsInformationTlvIsNoPair` (absent, cut short, type, length, organization, subtype) | `follow-up-without-tlv-used`, `follow-up-tlv-fields-unchecked` |
| R884-1-F5 xvlog skip reported as PASS | MINOR | fixed: the gate EXECUTED at `09c5934a` and at `8167b70d`; every gate row names a skip or a timeout as one | | the xvlog gate executed at the head through `$XVLOG` (Vivado 2026.1's), its result in the gate table | |
| R883-1-F1 PHC step corrupts neighborRateRatio | MAJOR | fixed | `7b74d5ea` | `Net.AStepAtTaiScaleKeepsAsCapableAt1msTurnaround`, `...At10msTurnaround`, `AStepOf100msKeepsAsCapableAt1msTurnaround`, `AStepOf1sKeepsAsCapableAt10msTurnaround`, `ABackwardStepOf100msKeepsAsCapableAt10msTurnaround`; `Scripted.AnOwnStepVoidsTheExchangeInFlightAndRestartsTheRateWindow`, `AnOwnStepCompletesNoResponseOwed`, `ATurnaroundLongerThanTheRoundTripIsNoMeasurement`; the suite under UBSan (the new `gptp_ubsan` arm) | `rate-envelope-dropped`, `turnaround-unbounded`, `own-step-keeps-the-exchange`, `own-step-keeps-the-window`, `own-step-completes-the-response`, `null-path-compared` (UBSan) |
| R883-1-F2 split-sw in no gate | MINOR | fixed | `db8e0b99` | `make -C tb/verilator/milan_dp ci-list` names `split-sw` (its last case, hosted leg 2) | |
| R883-1-F3 design page's routes are an earlier head's | MINOR | fixed: the page names `9d753fa0` and the plane's `40bd7738` | `333dc7c5` | | |
| R883-1-F4 the HAL is three calls | RESIDUE | fixed, page and PR body | `333dc7c5` | | |
| R883-1-S1 null to memcmp/memcpy | SUGGESTION | taken (UBSan needs it) | `7b74d5ea` | the UBSan arm | `null-path-compared` |
| R883-1-S2 to S5 | SUGGESTION | not taken | | | |
| #872 s9: ctrl_plat 18,944 vs 19,008 | | fixed before `f15b3a7d` (`c1e3055c` is an orphaned pre-rebase commit; the ledger reads 19,008 since round 2); `plat_ledger.py` PASS at `9d753fa0` | | | |
| #872 s9: docs_inventory stale | | fresh at `f15b3a7d`, `9d753fa0` and `09c5934a` with the pinned venv and with the system Python (543 lines) | | | |
| #872 s9: gptp_sw, gptp_tsu durations | | registered since `ee0d920c` (860 s, 120 s, provisional, `scripts/suite_shards.py`); the sharded sweep's preflight self-test passed at `333dc7c5`, and both suites ran in it | | | |

The regression tests and probes in detail are under `receipts/gptp/` and `receipts/publication/`:
- the suite's 52 tests run on `f15b3a7d`'s port: the 15 regression tests fail, the other 37 pass (the 34 it had, and three new
  ones the old port already met: the five-minute cease, a further TLV, the follow-up receipt timeout);
- the suite under UBSan at the fix: all 52 pass with no runtime error, in the gate's `gptp_ubsan` arm (at `f15b3a7d` it aborts
  on the null `memcmp`);
- R884-1's own probes at the fix: `probe_protocol.c` 0 failed assertions; `probe_publication.sv`, the control and the overlapping update, torn 0;
- R883-1's outage table at the fix (its include adapted to the fixture's `turn_ns`): every case 0 ms out of asCapable on both ports.

## Contract changes (2.5 stays additive)

The contract's interface is unchanged this round: no register, field, offset, channel, event, table entry or
version moved, and the minor is still 5. Exactly this changed:

- `sw/mailbox/mailbox.yaml`, `GPTP_STATE`'s `doc` only (`8121e098`): after "...publishes every GPTP_* word as one
  snapshot" it now reads ", which the datapath takes whole: a word written after it reaches no snapshot, however
  long the crossing before is in flight, and a snapshot a later one overtakes before it crosses is not taken."
- Its generated outputs, the same sentence only: `docs/reference/MAILBOX_CONTRACT.md`, the doc comment in
  `hdl/milan/mailbox/KL_mbx_pkg.sv` and in `sw/firmware/ctrl/mbx/mbx_contract.h`. 2.6 regenerates them from its
  own yaml; taking this `doc` text keeps them equal.
- Not generated, and where 2.6 will merge with this lane:
  - `hdl/milan/mailbox/KL_mbx_cdc.sv`'s `gptp_pub_send` block: the committed bank (`gptp_bank_r`, `gptp_dirty_r`,
    `gptp_send_d_r`), `cdc_handshake`'s `src_in` from the bank. Interface 0's three words, 96 bits; the routed design
    gains 75 FF against round 2b.
  - `sw/firmware/ctrl/host/mbx_model.c` and `mbx_model.h`: two comments; the model's behaviour is as it was.
  - `tb/verilator/mbx/Makefile` (`all:` gains `cdc-pub-mutants`, three targets added) and `README.md` (item 6, the
    `make` count); new `tb_cdc_pub.sv`, `cdc_pub_mutants.py`. The second-hart lane edits the same Makefile and
    README: a textual conflict on `all:` and the item list, whose union is both.
  - `sw/firmware/ctrl/test/model_suite.cpp`: one test appended (`MbxModelGptp`).

## R883-1's suggestions not taken (optional, no lens)

- S2, an elaboration `$error` for `GPTP_SW_EN_P` with `GPTP_PLANE_EN_P`: `milan_soc.py` refuses the pair today; the
  assertion is RTL with a negative elaboration test of its own, so it is left for a change of its own.
- S3, `g_gptp_sw`'s `GPTP_STATE` decode from `KL_mbx_pkg`'s constants: a refactor with no change of behaviour.
- S4, `d_ts_take_p_o` gated on `!ts_send_r` too: the reviewer shows the credit holds today; a defensive RTL change.
- S5, one gptp bucket an interface: worth weighing with #962, as the reviewer says; the existing channels share
  theirs the same way.

## Gates

Final head `8167b70d`. Receipts are under `receipts/`, indexed in `receipts/INDEX.md`.

| Gate | Head | Result | Receipt |
|---|---|---|---|
| Full Verilator sweep, 4 parallel shards (`native-shards.py`, the CI-pinned Verilator 5.050) | `333dc7c5` | 66 of 67 suites PASS, 0 in-suite failures; `tsn_fuzz` failed there on its traceability-matrix check alone (the matrix stale for the new bench), regenerated in `09c5934a` and passing there (next row). `mbx` ran the crossing bench (53 checks) and its 5 plants; `milan_dp` ran `split-sw` (152 checks) | `sweep/` |
| `tsn_fuzz`, with the tsn-gen field campaigns (`TSN_GEN_ROOT` set) and without | `09c5934a` | PASS both; the AAF/AVTP and 802.1AS field campaigns 164 and 675 pass, 0 skipped; the traceability matrix check passes | `sweep/tsn_fuzz-*.log` |
| Docs, idiom and light rtl-fast gates (73) | `8167b70d` | 72 of 73 PASS in the run; its xvlog TIMED OUT (rc 124) waiting for a Vivado slot other lanes held, not a pass. Re-run alone at this head once slot 1 freed (13:49): EXECUTED, 90 files under hdl/ and 52 in the pinned processors, 0 findings, PASS. So 73 of 73 | `gates-8167b70d/` |
| The same 73 gates | `09c5934a` | 73 of 73 PASS, none skipped: xvlog EXECUTED (`$XVLOG` = Vivado 2026.1's, through `vivado-slot.sh`), 90 files under hdl/ and 52 in the pinned processors, 0 findings; no HDL changed after `8121e098` | `gates-09c5934a/` |
| The same gates one head back | `a8c7a8d6` | 72 of 73: `module_matrix` found the matrix stale for the new bench, regenerated in `09c5934a` | `gates/` |
| Firmware gate, four shards (`test_ctrl_firmware.py --require-rv32 --self-test --shard k/4`), a clone each | `64a473be` | 4 of 4 PASS; the control campaign 826 of 826 caught; arms `gptp` (52 tests), `gptp_ubsan` (52, clean), `gptp_rv32` (4 checks), `model` with `MbxModelGptp` | `fwgate/` |
| gPTP planted defects, `gptp_mutants.py` | `8167b70d` | 40 of 40 killed (25 earlier, 15 this round); the rate-envelope plant fails all five step cases | `gptp/gptp_mutants-final.log` |
| The new GoogleTests on `f15b3a7d`'s port; the suite under UBSan | `7b74d5ea` | 15 of the 52 fail there, 37 pass; UBSan clean at the fix, the old port aborts on its null `memcmp` | `gptp/` |
| Closed loop, `make -C tb/verilator/gptp_sw` (slave, master, flood) | `64a473be` | 48 of 48; the flood: 490 stamped, 0 unstamped, 0 egress lost, lock 2.9 s | `closedloop/` |
| Closed-loop campaign, `gptp_sw_mutants.py` | `64a473be` | 14 of 14 killed | `closedloop/` |
| `gptp_tsu` and `tsu_mutants.py` | `64a473be` | 36 checks PASS; 24 of 24 killed | `tsu/` |
| The publication crossing, `run-cdc-pub` and `cdc_pub_mutants.py` | `8121e098` (unchanged since); in the sweep's `mbx` at `333dc7c5` | 53 checks PASS; on `f15b3a7d`'s crossing 12 fail; 5 of 5 killed | `publication/` |
| `milan_dp` `split-sw` | `8121e098`; in the sweep's `milan_dp` at `333dc7c5` | 152 checks PASS; on `f15b3a7d`'s crossing the new check fails (`0x2222222233333333`) | `publication/` |
| `milan_dp` `split-cdc` | `64a473be` | 13 checks PASS | `milan_dp/` |
| `plat_ledger.py --self-test`, `test_ctrl_memory.py` | `9d753fa0` | 5 points PASS, 9 of 9 controls; PASS (the gPTP image 151,872 B of rom, 62 RAMB36) | `memory/` |
| Harness legs, 8x8 and 8x8-1if `--with-gptp` (six groups each) | `64a473be` | rc 0, 0 refusals; 0 of 5,197 and 0 of 5,142 passes over the share | `harness/` |
| `egress_ledger.py --point 8x8-1if` on the 8x8-1if run | `64a473be` | PASS, all seven held rows within; `acmp.last.if0` 62.411 ms against 62.62 | `harness/` |
| `egress_ledger.py` on the 8x8 (2if) run | `64a473be` | FAIL as at round 2b, from the 1if ledger's `if0` naming (no 2if ledger); its held row 62.460 ms | `harness/` |
| Yosys portability, 4 shards (64 tops; tied-input and tap-purity gates) | `64a473be` | PASS | `yosys/` |
| Publication census, `--check --selftest --jobs 4` | `64a473be` | 246 checks PASS; 164 self-test arms, 57 of 57 rules proved | `census/` |
| Routes, 8x8/1if `--sw-gptp`, all three directives | `9d753fa0` | all meet #818's floor: ExtraTimingOpt +0.220 / +0.056 ns, AltSpreadLogic_high +0.174 / +0.056, ExtraPostPlacementOpt +0.154 / +0.026 | `route/` |
| The reviewers' probes, at the fix | `7b74d5ea`, `8121e098` | R884-1 `probe_protocol.c` 0 failed assertions; `probe_publication.sv` torn 0 in both cases; R883-1's outage table 0 ms out of asCapable in every case | `gptp/`, `publication/` |

What moved after each head:
- `8121e098`: nothing of the crossing, its bench or the split bench since;
- `9d753fa0` to `64a473be`: tests only (one GoogleTest, one plant);
- `64a473be` to `333dc7c5`: the design page and the documentation audit;
- `333dc7c5` to `a8c7a8d6`: a comment in `scripts/suite_shards.py`;
- `a8c7a8d6` to `09c5934a`: the generated traceability matrix;
- `09c5934a` to `8167b70d`: `gptp_mutants.py` alone (the envelope plant names all five step cases).

Not re-run this round, and out of the changes' scope: the harness self-test (no harness source moved since round 2b's
`62fcd154`, 298 of 298 there) and S3 synthesis (superseded by the routes).

Scheduling, for the CI owner: `mbx` ran about 40 s longer in this sweep than in round 2b's (130 to 172 s here,
under load), the new crossing bench and its five plant builds. `scripts/suite_shards.py` keeps its hosted 73 s
until a measured hosted run; `milan_dp`'s leg 2 and serial figure take the measured 22 s of `split-sw`.
