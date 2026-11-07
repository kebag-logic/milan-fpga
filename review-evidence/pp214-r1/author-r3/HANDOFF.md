# [A736d] HANDOFF: processor issue #214, round 3 (the test gaps of R779-1 and R780-1)

**Status: REVIEW READY (posted on the issue) at `1c8b485f5eebfa8efaba6f5facbade7e5aa4caaa`.** Every item of the [A10] ruling is closed, every
acceptance item of the issue is met (§8), and every gate below is rc 0 at this head. No RTL change: no new check found
a defect, so no STOP.

- Repository: the processor repository (`git remote get-url origin` checked), branch `214-one-vector-per-value`, local,
  not pushed. Base of this round `cc92e90a95376151a9ebd484c429bc53feb8573c`, main `9210065` (unchanged at the last
  check), original base `a9e84b66`.
- Head `1c8b485`. Two commits on `cc92e90`, history not rewritten:
  - `d9bdb0d` Grade the read-port isolation, the whole value identity, the newer FirstValue, the MVRP merges and the
    push face in PV13 to PV20, each with a planted arm (issue #214)
  - `1c8b485` Record PV13 to PV20, their arms, the measured counts and the newer-FirstValue rule in the encoder README,
    09 8.14 and 10 3 (issue #214)
- `git rev-parse HEAD:hdl` equals `cc92e90:hdl`, `6f29f7158dc4` (`receipts/IDENTITY.txt`), so every file under `hdl/` is
  byte-identical to the reviewed head. No port, parameter, register-map or MRP timer change exists, the area figures
  of round 2 stand (2x2 and 8x8, in `PR-BODY.md`), and `KL_srp_listener_fsm.sv` is untouched.

## 1. The ruling, item by item

| Ruling item | Finding | Row | Arm | Result |
|---|---|---|---|---|
| 1. Application isolation, both directions | R779-1 F-1, R780-1-F3 | PV13 | `msrp-read-taken-by-any-search`, `mvrp-read-taken-by-any-search` | closed |
| 2. Identity width: StreamID top octet | R779-1 F-2, R780-1-F4 | PV14 | `identity-drops-top-octet` | closed |
| 2. Identity width: VIDs above bit 7 | R780-1-F1 | PV15 | `identity-vid-low-octet-only` | closed |
| 3. Newer FirstValue | R779-1 F-2, R780-1-F2 row 1 | PV16 | `merge-keeps-older-value` | closed |
| 4. MVRP JoinIn then Lv, New then Lv, Lv then New | R780-1-F1 | PV17 | one arm per row, and `mvrp-merge-never-written` under all three | closed |
| 5. `rv-fp-s-replaces-kept` | R780-1-F2 row 2 | PV18 | `listener-type-s-over-s-kept` | closed |
| 5. `rv-invalid-type-searches` | R780-1-F2 row 3 | PV19 | `unknown-type-held-while-pending` | closed |
| 5. `rv-push-on-drain-start` | R780-1-F2 row 4 | PV20 | `push-on-drain-start` | closed with a check and an arm, so no tracking reference is needed |

## 2. Changes (file:line at `1c8b485`, clause)

| File:line | Change | Clause |
|---|---|---|
| `tb/srp_encoder/sim_main.cpp:345` | `H::offer()`, split out of `push_enc()`: an event stays offered until valid drops | harness only |
| `tb/srp_encoder/sim_main.cpp:1751`, `:1774` | `offer_through_a_drain()`; PV13 | 10 §3; issue #214 acceptance 1 |
| `tb/srp_encoder/sim_main.cpp:1803` | PV14 | 802.1Q-2022 35.2.2.8.1, 35.2.2.8.2, 10.7.7 |
| `tb/srp_encoder/sim_main.cpp:1821` | PV15 | 11.2.3.1.7 |
| `tb/srp_encoder/sim_main.cpp:1838` | PV16 | 35.2.2.8 |
| `tb/srp_encoder/sim_main.cpp:1855` | PV17 | Table 10-3 Lv!, New! |
| `tb/srp_encoder/sim_main.cpp:1869` | PV18 | 10 §3; 35.2.2.7.2 |
| `tb/srp_encoder/sim_main.cpp:1887` | PV19 | 10 §3 |
| `tb/srp_encoder/sim_main.cpp:1909`, `:1935` | `offer_on_the_start_clock()`; PV20 | 10 §3 |
| `tb/srp_top/mutants.py:389` | 19 rows for 13 arms | acceptance 2 |
| `tb/srp_top/mutations/*.patch` | 13 new patches, each one exact edit of `KL_srp_encoder.sv`, written by `tools/make_arm_patches.py` | acceptance 2 |
| `docs/architecture/10_srp_engine.md:150`, `:163` | the newer-FirstValue rule, which only the PR body stated before; PV1 to PV20 | 35.2.2.8 |
| `docs/architecture/09_verification.md:841` | five rows of the §8.14 table; the PV1 to PV12 row now says "MVRP re-joins", re-read as R780-1 asked | same clauses |
| `tb/srp_encoder/README.md:6`, `:137`, `:274`, `:288` | the count, the rows, the arm table, the base count | same clauses |

The expected messages come from Table 10-3 and 802.1Q-2022 text, read again this round (`receipts/STANDARDS.txt`): Lv!
takes VN, AN, AA and QA to LA, and New! takes LA to VN.

## 3. New checks, planted arm, failing words (measured at `1c8b485`)

`tb/srp_encoder` reads `888 checks: 888 PASS, 0 FAIL`, 196 more than the 692 of `cc92e90`. All of them passed on first
run against the unchanged RTL, so no row found a defect; each row's power comes from the arm under it.

| Check (failing words) | What it requires | Planted arm | Failing |
|---|---|---|---:|
| `PV13 an MVRP search beside an MSRP drain: the drain reads its own entries` | an MVRP offer held from the join tick to the end of the MSRP frame, with VIDs pending, leaves that frame byte-exact | `msrp-read-taken-by-any-search` | 3 |
| `PV13 an MSRP search beside an MVRP drain: the drain reads its own entries` | the same in the other direction | `mvrp-read-taken-by-any-search` | 2 |
| `PV13 an absent VID offered beside an MSRP drain` | an offer repeated back to back appends once, then merges | `search-survives-accept` | 8 |
| `PV14 two type 1 StreamIDs that differ only in octet 0`, and type 3 (type 2 fails too) | each of the eight octets, each of the three types: two values | `identity-drops-top-octet` | 6 |
| `PV15 VID 2 and the VID that differs only in bit 8` (bits 9 to 11 fail too) | VID 2 and VID 258, 514, 1026, 2050: two values | `identity-vid-low-octet-only` | 8 |
| `PV16 two Talker Advertise values of one StreamID`, `PV16 two Talker Failed values of one StreamID` | every field after the StreamID changed: the frame carries the newer | `merge-keeps-older-value` | 2 |
| `PV17 VID JoinIn then Lv`, `PV17 VID New then Lv`, `PV17 VID Lv then New` | each frame carries what Table 10-3 leaves owed | `mvrp-merge-never-written` | 3 |
| `PV17 VID JoinIn then Lv` | Lv | `mvrp-lv-keeps-joinin` | 1 |
| `PV17 VID New then Lv` | Lv | `mvrp-lv-keeps-new` | 1 |
| `PV17 VID Lv then New` | New | `mvrp-new-keeps-lv` | 1 |
| `PV18 Listener In Ready then Mt AskingFailed` | the replacing Mt's declaration type, and the mirror row | `listener-type-s-over-s-kept` | 2 |
| `PV19 an unknown MSRP type taken at once`, `PV19 an unknown MVRP type taken at once` | taken on its first clock beside a pending value, with its strobe, nothing pended | `unknown-type-held-while-pending` | 3 |
| `PV20 a Domain value on the MSRP drain's start clock: the offer waits`, `PV20 a VID on the MVRP drain's start clock: the offer rides the next MRPDU` | the offer waits on the start clock, and the next frame carries it; under the arm it is lost | `push-on-drain-start` | 6 |

Each single-rule MVRP arm fails only its own PV17 row, so the three rows are independent. Full failing lines:
`receipts/arms/new-arm-failing-words.txt`. Counts of older arms the new rows moved: `second-queueing` 46 to 72,
`leave-does-not-replace` 2 to 4, `listener-type-oldest` 2 to 4, all in the README. No other `srp_encoder` arm moved
(`receipts/arms/encoder-arm-counts.tsv`).

**The base.** `tb/srp_encoder` on main's encoder reads `888 checks: 810 PASS, 78 FAIL` (`receipts/arms/base-encoder.txt`):
every PV row except PV8, PV14, PV15 and PV19, and O8. PV20 fails there because the base takes the offer one clock
before the start clock, which is the stimulus's timing rather than a second defect.

## 4. Both reviews' own arms against the new suite

Every arm of both packets ran at this head (`receipts/arms/reviewer-arms.tsv`): 51 of 52 fail the suite, and each arm
named in a Verification line fails the row it asked for: `rv-search-steals-other-read`, `rv-search-steals-other-read-mvrp`,
`rv-msrp-port-taken-by-any-search` and `rv-mvrp-port-taken-by-any-search` on PV13; `rv-key-low-mac-ignored` and
`rv-key-top-mac-octet-ignored` on PV14; `rv-mvrp-key-low-byte` on PV15; `rv-merge-keeps-old-value` and
`rv-value-keeps-oldest` on PV16; `rv-mvrp-hit-appends-addr` on PV17; `rv-fp-s-replaces-kept` on PV18;
`rv-invalid-type-searches` on PV19; `rv-push-on-drain-start` on PV20.

Two rows of that table need a word:

- **`rv-search-ignores-start` survives, and it is equivalent.** It drops `!start_tgt_w` from `sr_engage_w` only. `ev_ready_o`
  still has it through `base_ok_w`, so nothing is accepted on the start clock. The arm only moves the search's own
  registers and the read address for that clock; the drain's first read comes after `E_ALLOC` and `E_HDR`, and the
  next clock `busy_app_w` ends the search. At most a push in the `E_COLLECT` corner is taken a clock sooner. That is my
  reading; R779-1 recorded the arm as behaving like the head, and neither review lists it as a finding.
- **`rv-empty-table-searches` reads rc 2 with no tally.** The suite segfaults on an older row when no push to an empty
  table is ever taken, and buffered stdout is lost. R780-1's receipt shows the same at `cc92e90`, not caused by these rows.

## 5. Processor gates (clean clones of `1c8b485`)

| Gate | rc | s | Last tally or verdict line |
|---|---|---|---|
| diff_check | 0 | 1 | (no output) |
| gen_matrix_check | 0 | 0 | matrix: OK (94 rows, 0 untested) |
| lint_hdl_5050 | 0 | 70 | LINT OK  protocol_processor_top |
| make_check | 0 | 30 | lint: 41 mermaid + 18 wavedrom blocks checked, OK |
| srp_encoder | 0 | 5 | 888 checks: 888 PASS, 0 FAIL |
| srp_top | 0 | 548 | 8683 checks: 8683 PASS, 0 FAIL |

`make_check` ran every target of `make check` with CI's pins: wavedrom 2.0.3.post3, Mermaid CLI 11.16.0. Its last line
is whichever target ended last, because it ran with `-j8`; the log shows links, matrices, parameters, the AECP command
model, IDs, figures and staleness each OK. `diff_check` is `git diff --check` against main: no output.

| Gate | rc | s | Last tally or verdict line |
|---|---|---|---|
| camp-srp | 0 | 4055 | 310 checks: 310 PASS, 0 FAIL |

The campaign reads `310 checks: 310 PASS, 0 FAIL`: 20 controls, 289 arm verdicts all KILLED by name, 0 UNPROVEN, assertion
coverage 174 of 174, 256 arm names, with `--jobs 8`. Against `cc92e90` (`receipts/campaigns/cc92e90-vs-head.campdiff.txt`):
267 verdicts identical, 3 moved, 19 new. The three are `second-queueing`, `leave-does-not-replace` and
`listener-type-oldest`, which the new rows also catch; each is still KILLED, and each count is in the README.

## 6. Scratch-parent consumer gate table

Parent `604899c0` plus two local commits, never pushed: `e2d1f141fe` (gitlink to `1c8b485`) and `53ebba1348`
(`./syn/yosys/ooc.sh --record-rom-digests`, rc 0, two rows for the new pin). Branch `pp214-1c8b485-consumer-gate`.

| Gate | rc | s | Last tally or verdict line |
|---|---|---|---|
| rom_digests | 0 | 1 | ooc.sh: recorded ROM content digests for protocol-processor pin 1c8b485f5eebfa8efaba6f5facbade7e5aa4caaa and g |
| behave | 0 | 13 | 2330 steps passed, 0 failed, 0 skipped |
| cache_selftest | 0 | 169 | cache selftest: OK (unit self-test + 5 original live arms on cdc_pulse + ROM controls) |
| check_cpp_idiom | 0 | 2 | build without warnings: 0 <= 0 |
| check_cpp_idiom_selftest | 0 | 2 | 75 checks: 75 PASS, 0 FAIL |
| check_doc_paths | 0 | 0 | doc path gate: OK (1092 cited paths all resolve, 2 allowlisted; 10 line anchor(s) within their file) |
| check_hygiene | 0 | 1 | HYGIENE RATCHET: PASS (3 population(s), 1308 file(s)) |
| check_port_contracts | 0 | 4 | port contract gate: OK (4081 first-party port(s): hdl 2182, gptp-processor 127, protocol-processor 1772; 347 u |
| check_py_idiom | 0 | 8 | over-long line: 0 <= 0 |
| check_py_idiom_selftest | 0 | 7 | 54 checks: 54 PASS, 0 FAIL |
| check_rtl_source_lists | 0 | 2 | RTL source-list gate: OK (112 files in the milan_datapath closure, 4 of 4 consumer list(s) carry all of them;  |
| check_sh_idiom | 0 | 0 | top-heavy long script: 0 <= 0 |
| check_sh_idiom_selftest | 0 | 1 | 48 checks: 48 PASS, 0 FAIL |
| check_sv_idiom | 0 | 1 | SystemVerilog idiom gate: OK (141 first-party HDL file(s) across the superproject and both processor submodule |
| check_sv_idiom_selftest | 0 | 0 | 55 checks: 55 PASS, 0 FAIL |
| ci_scope_classify | 0 | 0 | syn/yosys/rom_digests.tsv |
| ci_scope_selftest | 0 | 34 | selftest: PASS |
| docs_check | 0 | 6 | docs_check: 0 finding(s) across 213 md files + 1440 scrubbed text files, scrub self-test 23/23, routing arms 4 |
| fw_boundary | 0 | 1151 | ctrl_boundary: PASS |
| fw_coverage | 0 | 241 | firmware coverage: PASS (30 files) |
| fw_coverage_selftest | 0 | 1 | coverage self-test: 29 of 29 planted cases read as planted |
| fw_ctrl_nvm | 0 | 94 | saved-state store gate (#665 F1): OK across 5 shape(s), 435 tests |
| fw_rv32_sdk_selftest | 0 | 1 | OK |
| fw_rv32_selftest | 0 | 6 | RV32 build self-test: 17 checks PASS |
| fw_shard0 | 0 | 300 | test_ctrl_firmware: PASS |
| fw_shard1 | 0 | 1169 | test_ctrl_firmware: PASS |
| fw_shard2 | 0 | 280 | test_ctrl_firmware: PASS |
| fw_shard3_srp | 0 | 844 | test_ctrl_firmware: PASS |
| fw_tally_selftest | 0 | 4 | tally self-test: 18 of 18 planted cases read as planted |
| fw_verilator | 0 | 674 | ctrl_boundary: PASS |
| guard_selftest | 0 | 100 | elaboration guard self-test: 36 controls passed |
| lint_rtl | 0 | 14 | LINT GATE: PASS (89 violation(s) <= ratchet 89; 19 waived, 0 justified lint_off) |
| measure_fail_fast | 0 | 2 | FAIL-FAST RATCHET: PASS (78 <= 84 modules without an elaboration contract, 3 <= 4 masked pipeline(s), 0 <= 0 d |
| measure_naming | 0 | 1 | NAMING RATCHET: PASS (95 candidate(s), all recorded by identity; 95 recorded) |
| measure_test_evidence | 0 | 12 | TEST-EVIDENCE RATCHET: PASS (67 <= 77 suite(s) without a mutation arm, 10 <= 10 unseeded draw site(s), 0 <= 0  |
| milan_dp | 0 | 3763 | 6 checks: 6 PASS, 0 FAIL |
| milan_dp_mclk | 0 | 1332 | 34 checks: 34 PASS, 0 FAIL |
| milan_dp_render | 0 | 852 | 5 checks: 5 PASS, 0 FAIL (--leg-defects: the arms that need no elaboration; the gateware and shape mutants are |
| ooc_read_sets | 0 | 1579 | baseline PASS: 3 endpoints |
| ooc_selftest | 0 | 104 | ooc.sh refusal self-test: 75 arm(s) passed |
| pp_shadow | 0 | 360 | RESULT: PASS |
| pp_srcs | 0 | 0 | pp source list: 46 tracked source(s) derived; no build input carries a literal copy (self-test passed) |
| publication_census | 0 | 1062 | 26 class-D net(s) from the wrapper cell's ports, 4 unread; 41 read(s) of 22 class-D net(s) in each shape; RESU |
| yosys_elaborate | 0 | 521 | RESULT: PASS |

43 gates and the ROM recorder, every one rc 0, the same 44 names as round 2 (compared by name). The firmware gates ran
on a copy of the parent at the same commit, to run beside `milan_dp`; head, gitlink and clean state were checked on
both trees first and again at the end. These are the workflow's `run` steps executed locally on the pinned tools,
job by job, not a run of the workflow itself, so the aggregate `rtl-fast` job, which only collects the others, did not
execute. `check_cpp_idiom.py` and `check_py_idiom.py` are rc 0 with the new rows.

**Interpreter.** Every gate of this round, processor and parent, asserted `python3` before and after it and would read
rc 97 on a mismatch. All 43 parent gates, the campaign and the processor gates read this lane's own venv at 3.12.3 on
both sides (`<gate>.python`), `make_check` the docs venv. Both venvs were built this round in this lane's scratch, and
their full package lists are now published (`receipts/venv-ci.freeze.txt`, `receipts/venv-docs.freeze.txt`), which
answers the limit R780-1 recorded on round 2.

## 7. Residue and suggestions

| Item | Disposition |
|---|---|
| R779-1 R-1 = R780-1-R1, PR body byte identity | Fixed in `PR-BODY.md`, with R779-1's exact wording |
| R779-1 R-2 = R780-1-R2, banner "the only reader" | **Left open.** It is an edit to an RTL file, and the ruling says no RTL change. Both reviews carry it to the manager's residue checklist |
| R779-1 R-3 = R780-1-R3, "(Run B, 10 §6.5)" at `tb/srp_top/sim_main.cpp:3422` | **Left open.** The ruling does not name it, and this round does not otherwise touch that file. Same checklist |
| R779-1 S-1 = R780-1-S3, back-to-back search row | Covered by the same edit, so kept, as the ruling allows: PV13's held offer repeats back to back, and `search-survives-accept` fails it by name |
| R779-1 S-2 = R780-1-S2, area in the tree | Out, by the ruling: no edit here reaches 10 §5.1 |
| R780-1-S1, post-synthesis timing | Out, by the ruling. The RTL is unchanged, and no timing is claimed here; builder timing stays a manager duty |

## 8. Acceptance items

1. **Met.** Each value at most once per MRPDU, for MSRP Domain, Talker and Listener and MVRP, through a received LeaveAll, an
   own LeaveAll, `periodic!` and a join in one window: OV0 reads every MRPDU of the run, OV1 to OV10 place each case, PV1
   to PV20 grade each merge, the identity and the read port. `tb/srp_top` 8683 of 8683, `tb/srp_encoder` 888 of 888.
2. **Met.** OV0 to OV7 and the PV rows fail without the fix and pass at the head. `second-queueing` re-enables the second
   queueing and fails `OV1:` and `PV1 two re-joins of one Domain value` by name.
3. **Met.** `tb/srp_top/mutants.py` 310 of 310 at this head. The other campaigns were green at `cc92e90` (§9). Area at 2x2
   and 8x8 stands, `hdl/` being byte-identical (`PR-BODY.md`; receipts in `pp214-a736b`).
4. **Met on the scratch parent.** 43 gates rc 0 with `1c8b485` as the gitlink and the ROM digests re-recorded. The real
   parent bump is still to be done.

## 9. What this round did not do

- **Not re-run at this head:** the full sweep, the other sixteen campaign gates, and the area. The ruling's gate list does
  not name them, and no input of theirs changed: 18 files differ from `cc92e90`, none under `hdl/` or `tb/common/`, and
  the only suite source among them is `tb/srp_encoder/sim_main.cpp`. Their figures in `PR-BODY.md` are labelled as
  `cc92e90`'s. The executed traceability check needs the sweep, so it did not run; the static half in `make check` did,
  and these rows add no requirement tag.
- **The consumer gates ran on parent `604899c0`,** the parent this lane's brief names, not live dev `87e9d03a`. Both reviews
  list that merge candidate as a manager duty.
- **Memory went over the target once.** `memory.peak` read 11,101 MB against the 10 GB target, under the 12 GB cap, with 0
  throttle events and 0 OOM kills. It was reached in the first hour, while the campaign, the parent chain and my
  eight-way run of the reviewers' arms overlapped, and I started no further chain until the campaign ended. The
  governor's samples read at most 9,476 MB in total and 8,141 MB of anon, so the peak fell between samples and was
  brief, but its exact moment and cause are not recorded. No gate was lost to it.
- No hardware or bench access, and no timing result.

## 10. Notes for review

1. **No new row found a defect.** All 196 new checks passed first run on the unchanged RTL, so the ruling's STOP did not
   apply.
2. **PV20 fails at the base for a timing reason.** The base has no search, so it takes the offer a clock early, before
   the start clock. The base's guard itself is intact, and this says nothing against it.
3. **The issue stands with the STOP comment of round 2.** It cannot be edited, and later REVIEW READY posts supersede it.
