# [A814] REVIEW READY: PR #966 round 3, the corrections to R884-1 and R883-1 (#884, #665 F6)

Branch `opt-gptp-sw-1`, head `8167b70d`: this round's nine commits on PR #966's `f15b3a7d`. Local commits only;
nothing pushed, no PR edit, no comment. The handoff is HANDOFF-r3.md; the PR body draft is PR-BODY.md (no footer).

## What each finding became

| Finding | Severity | Fix at its cause | Regression test that fails at `f15b3a7d` | Plants |
|---|---|---|---|---|
| R884-1-F1 publication tear | MAJOR | `KL_mbx_cdc` crosses a bank committed the cycle after `GEN` moves, never the live words (`8121e098`) | `tb/verilator/mbx/tb_cdc_pub.sv`: 53 checks, 12 fail on the old crossing, the reviewed ordering among them; `split-sw`'s end-to-end check (the old crossing holds `0x2222222233333333`) | 5 of 5 (`cdc_pub_mutants.py`) |
| R884-1-F2 Sync without Follow_Up | MAJOR | the sync receipt deadline restarts only on a consumed pair (802.1AS-2020 10.2.8.2.1 c), `7b74d5ea` | three GoogleTests: priority1 248 and 255, and Sync with Announce | 3, and the Announce-timeout test now keeps complete pairs |
| R884-1-F3 late second responder | MAJOR | a request counts toward the cease once, when a second clock identity answers it, whenever in its interval; a request answered by one clock or none ends the run (`7b74d5ea`) | late second responder, a clean or unanswered request between, one clock answering twice | 4 |
| R884-1-F4 Follow_Up without its TLV | MAJOR | the information TLV is required (11.4.4.1, 11.4.4.3), `7b74d5ea` | absent, cut short, and four malformed fields; a further TLV still accepted | 2 |
| R884-1-F5 xvlog skip reported as PASS | MINOR | the xvlog gate ran, through `$XVLOG` (Vivado 2026.1) and `vivado-slot.sh`: PASS, 0 findings over 142 files, at `09c5934a`; at `8167b70d` its gate run timed out waiting for a slot, and its re-run alone there executed and passed; the PR body names each | | |
| R883-1-F1 a PHC step | MAJOR | the own step voids the exchange in flight, restarts the rate window and drops a response owed; a ratio outside 2^-12 restarts the window; an impossible turnaround is no measurement; overflow-free spans (`7b74d5ea`) | five `Net` cases (TAI scale, 100 ms and 1 s both ways; 1 ms and 10 ms turnarounds) and three `Scripted` ones; the suite under UBSan | 6, one on the new `gptp_ubsan` arm |
| R883-1-F2 split-sw in no gate | MINOR | `milan_dp`'s last case, hosted leg 2, 22 s (`db8e0b99`) | `ci-list` names it; the sweep runs it | |
| R883-1-F3 stale routes on the design page | MINOR | the page states this head's routes with the head they ran at (`9d753fa0`) and the plane comparison's own (`40bd7738`), `333dc7c5` | | |
| R883-1-F4 four-call HAL | RESIDUE | three calls, page and PR body (`333dc7c5`) | | |

The reviewers' own probes at the fix: R884-1's `probe_protocol.c`, 0 failed assertions; its `probe_publication.sv`,
the control and the overlapping update both torn 0; R883-1's outage table, every case 0 ms out of asCapable.

The second-hart lane's three findings (#872 issuecomment-7075152882 section 9) were against `c1e3055c`, a commit no
ref of this branch holds; at `f15b3a7d` and at this head the ledger pins `ctrl_plat` at 19,008 B (`plat_ledger.py`
PASS), `docs_inventory --check` is fresh, and `gptp_sw` and `gptp_tsu` have their durations.

## Measured at this head

Round 2b's conditions still hold with the corrected port:

| Condition | 8x8/1if (burst 7) | 8x8/2if (burst 14) |
|---|---|---|
| `backlog-owed.service.acmp.last.if0` at or under 62.62 ms | 62.411 ms; `egress_ledger.py --point 8x8-1if` PASS, all seven held rows within | 62.460 ms (no 2if ledger) |
| Pdelay turnaround at or under 10 ms | 0.223 ms | 0.309 ms |
| The flood plant, no delivered stamp lost and lock kept | | 48 of 48: 490 stamped, 0 unstamped, 0 egress records lost, lock by 2.9 s |

- The composed maximum is 1.634 ms at 1if and 1.655 ms at 2if, inside THE SHARE of 2.0 ms, and no work pass exceeds
  it (0 of 5,142; 0 of 5,197). The burst's last gptp record lands by 5.998 ms and 7.853 ms.
- gPTP takes 0.238 % of the CPU after link-up at 1if and 0.311 % at 2if (round 2b: 0.264 % and 0.308 %).
- Memory: the platform's gPTP image at 8x8/1if is 151,872 B of rom (80 B less), still 62 RAMB36; all five ledger
  points pass.
- Routed at `9d753fa0` (the head's RTL and firmware), all three directives meet #818's floor: ExtraTimingOpt
  +0.220 / +0.056 ns, AltSpreadLogic_high +0.174 / +0.056 ns, ExtraPostPlacementOpt +0.154 / +0.026 ns; 38.2k LUT,
  45,890 FF (75 more than round 2b's 45,815: the committed bank's 96 bits, less the generation register it replaced), 95.5 tiles, 5 DSP.

## Gate table

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

REVIEW READY 8167b70d89d2a913a07c3b1187f4f2469109eebc
