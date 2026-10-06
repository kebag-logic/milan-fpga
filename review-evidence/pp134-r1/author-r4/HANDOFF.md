# [A538] Processor #134 round-4 handoff

Status: **REVIEW READY**. Branch `pp134-lv-leave`, head `a596c7626864ae10026994ca777a8ccfdb53a9f6`,
tree `3c8b892c98694479945f471a55aaea9ab442294a`. The one-line correction commit is
`Correct full-suite LV mutation records (#134)`, with no body or trailers.
The canonical checkout is clean. Nothing pushed; no PR creation or edit.

## Round-4 authority and scope

Read [the round-4 assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/134#issuecomment-6001384633),
the complete internal review 6001378167, issue #134 and its earlier rulings,
the original assignment, the prior collision review, and parent #608 comment
5885808887. Re-read the repository guides, the SRP architecture and registrar/timer
paths, relevant suite/campaign code, the local standards extracts and parent
measurement recipe. TAKEN is comment 6001399905.

Origin is the required processor repository. This resume started clean at
`9050c4bbd25556929a0f24fb98258bc98e3bcfbe`, as the latest assignment requires;
original base `ead8036035affd53ef4b29979190f2f4f67084c0` remains an ancestor.
Main is still `21c6f7096ac80007f723de59c6f717f55bd34cfc`, already merged by
`9050c4bb` with two parents. The final remote check is in `integrity-final.json`.
No new main merge was needed. The entire round-4 source diff is the README
correction at `tb/srp_top/README.md:539`; no executable source, port, parameter,
register map, timer contract, test or assertion changed.

## Full default mutation runs: F1

Both checked-in patches were applied separately to exports of 9050c4bb. Each
ran the complete default `make -j16 -l8 -C tb/srp_top`, without RUN_ARGS. The
corrected README states the measured current result:

| Fault | Exact planted tree | Complete default result | Named failures | Receipt |
|---|---|---|---|---|
| lv-second-lv-ends | `c30c5dd9ab065003b158f1c4120709cf3a71f5b0` | rc 2; 8640 pass, 16 fail of 8656 | S1 8, S2 8; no other failure | `second/run.log`, `second/run.rc` |
| lv-never-ends | `48311c27d88e685e9e07ee195d56a0e263aea004` | rc 2; 5624 pass, 3032 fail of 8656 | S2 8, S3 8, SC2 3016; no other failure | `never/run.log`, `never/run.rc` |

Every 15-check storage run at 1/1, 2/2, 3/5 and 9/9 passes under both faults.
`mutant-results.json` checks the exact failure histograms and all five tallies.
The compiled inputs at the final head equal 9050c4bb. There is no new check
requiring an additional fault. The documentation gate at the corrected checkout
returns 0 (`check.log`, `check.rc`).

Large logs remain outside the output directory:

| Receipt | Bytes | SHA-256 |
|---|---:|---|
| second/run.log | 639960 | `1234bca8be0321c81d8c5ad1b11fd31cc713f8f16b2939bb67b1913356f405ec` |
| never/run.log | 966242 | `2ea854aa529f245604df63ef5c8c9f114bf4a7f0420b52a813502d554d2d7a3a` |

## Suite arithmetic and record equality: F2

Fresh main baseline: `21c6f7096ac80007f723de59c6f717f55bd34cfc` plus only the
same two missing D3 diagnostic arguments, exact tree `579e3c599dcd013647a7a7e5fa0418fe4f4b4c18`.
Fresh head: `a596c7626864ae10026994ca777a8ccfdb53a9f6`, exact tree `3c8b892c98694479945f471a55aaea9ab442294a`.
Both `scripts/run_suites.sh` banks return 0. `suite_capture.sh` preserves every
suite log before the unmodified runner removes its temporary file. `audit.py`
parses its 33 PASS rows and independently sums each bank and every delta.

| Suite | Main with diagnostic fix | Head | Delta |
|---|---:|---:|---:|
| acmp_listener | 3,111 | 3,111 | +0 |
| acmp_nvm | 388 | 388 | +0 |
| acmp_talker | 1,342 | 1,342 | +0 |
| adp_engine | 1,348 | 1,348 | +0 |
| aecp_notify | 34 | 34 | +0 |
| ca_originator | 16 | 16 | +0 |
| desc_mem_guard | 78 | 78 | +0 |
| desc_store | 586 | 586 | +0 |
| dispatch | 211 | 211 | +0 |
| dyn_state | 118 | 118 | +0 |
| event_router | 81 | 81 | +0 |
| lsn_admit | 18 | 18 | +0 |
| maap | 196 | 196 | +0 |
| nvm_port | 1,219 | 1,219 | +0 |
| originator | 107 | 107 | +0 |
| pp_top | 10,444 | 10,444 | +0 |
| prng | 76 | 76 | +0 |
| release_merge | 18 | 18 | +0 |
| resp_buf | 64 | 64 | +0 |
| rx_slots | 130 | 130 | +0 |
| rx_validator | 555 | 555 | +0 |
| scoreboard | 3,705 | 3,705 | +0 |
| side_port | 368 | 368 | +0 |
| srp_admission | 991,231 | 991,231 | +0 |
| srp_decoder | 190 | 190 | +0 |
| srp_encoder | 581 | 581 | +0 |
| srp_stream_fsms | 1,219 | 1,347 | +128 |
| srp_top | 2,200 | 8,656 | +6,456 |
| timer_map | 1,360 | 1,360 | +0 |
| timer_service | 48 | 48 | +0 |
| tx_arbiter | 66 | 66 | +0 |
| tx_slots | 95 | 95 | +0 |
| ucpu | 437 | 437 | +0 |
| **Total** | **1,021,640** | **1,028,224** | **+6,584** |

**1,028,224 − 1,021,640 = 6,584 = 24 S1–S3 + 128 SC1 + 6416 SC2 + 16 SC3.**
The bank follows the runner’s final per-suite tallies; supplementary shape runs
are recorded separately within the same suite logs.

The prior 1,021,664 total is valid for the earlier comparison base, exact tree
`ad2af42ecc394c06d1b443959e1acc435e7a4f0e`, formed from 5ab43bd9 and main 21c6f709 plus
the diagnostic fix. It already includes S1–S3: srp_top is 2224 instead of 2200.
Every other per-suite tally is identical to the main column above. Its comparison
with prior head tree `3bcc8532549ea69139323a863049022d10f799c1` correctly gives
1,028,224 − 1,021,664 = 6,560. The defect was the imprecise base label. The PR body
now names all exact trees and uses the main baseline’s 1,021,640 headline total.
The pre-repair merge-tree was 96e49906; `ad2af42ecc394c06d1b443959e1acc435e7a4f0e` is its actual
measured tree after the two diagnostic arguments were added.

`suite-tallies.json` binds every count to its tree and hashed bank log.
`suite-record-equality.json` compares all 33 runtime receipt sets in each of three
pairs: fresh main/head after the authorized S/SC additions and run-length record; fresh/prior head
literally; fresh main/prior comparison base after only S1–S3. All 99 receipt-set
comparisons match. The new `TOTAL_CLOCKS 210547557` record is retained separately
in that JSON and checked against the round-2 run-length requirement and the prior
head measurement. No undefined diagnostic value or existing DUT field is removed
or normalized. Compilation commands, compiler banners, build durations and build
paths are excluded from runtime records. The raw comparison before excluding
three inter-run compiler banners and accounting for the added clock record is
preserved in `comparison-before-metadata-filter.json`.

## Retained validation and parent pin

The twelve campaigns and remaining processor gates below are retained from
round 3b at the exact comparison trees named above. The complete round-4 diff is
one README, so all compiled and synthesized inputs remain identical. No campaign
builds the changed file; no merged file needs remeasurement because main did not
move. `retained-evidence-audit.json` checks every retained return code and the
thirteen patched parent source hashes. The five patches remain applied in the
required c8, p2-p1, c10, 232, 148 order on scratch parent fa450d30, as verified in
round 3b; no parent commit or push was made.

`retained-area-record.json` was read again from the retained OOC reports at the
final staged pin (rc 0). Its complete record, including the current source-input
digest, is identical to the round-3b head record. No synthesis was rerun.

The scratch parent’s processor gitlink is now staged at `a596c7626864ae10026994ca777a8ccfdb53a9f6`.
Every direct submodule Git action first checks its exact top-level directory.
Thirteen parent checks ran again at that staged pin and returned 0:

| Fresh consumer | Receipt under pc-head/ | rc |
|---|---|---:|
| C++ conventions | 01_check_cpp_idiom | 0 |
| Python conventions | 02_check_py_idiom | 0 |
| RTL source lists | 03_check_rtl_source_lists | 0 |
| RTL source-list self-test | 03b_check_rtl_source_lists_selftest | 0 |
| Processor source contract | 04_pp_srcs | 0 |
| Port contracts | 05_check_port_contracts | 0 |
| Naming | 06_measure_naming | 0 |
| Test evidence | 07_measure_test_evidence | 0 |
| Documentation | 08_docs_check | 0 |
| RTL lint | 11_lint_rtl | 0 |
| NVM cosimulation lint | 13_nvm_cosim_lint | 0 |
| NVM quick check | 14_nvm_cosim_quick | 0 |
| Shell conventions | 17_check_sh_idiom | 0 |

All thirteen fresh consumer receipt sets equal the retained head records, as
`parent-light-equality.json` records; only compiler timing summaries are excluded.

The complete retained parent table, including the heavier consumers and compiler
gate, follows. The retained OOC input set is identical: −16 LUT, −3 FF, unchanged
RAM/DSP, inside the 40/40 threshold. No new vendor run was warranted by a README
correction. This round makes no new area or hardware claim. The inherited mf48
calibration fixture remains NOT RUN.

All fresh work ran concurrently with separate logs and return-code files, using
the pinned simulation executable and make -j16. Every foreground wait was under
ten minutes. No new campaign driver was required. Memory event counts and final
source/parent integrity are retained in `integrity-final.json`; generated parent
products were moved outside its tree. The canonical tree has no generated files.

Evidence root: `$VALIDATION_STORAGE/pp134-a538/r4`. The artifact ledger is
`artifact-ledger.json`, 209629 bytes, SHA-256 `299c7e98a5e0d9aabc1a447546ceb3e5ba5bea80e8f321c3be6efece8fdb041e`.
All logs, binaries, environments and source exports remain outside the output
directory. Final integrity and the ledger identify the evidence. No hardware or
bench access, flashing, push, PR action, rebase, amend, additional checkout, or
existing comment edit/deletion was performed.

## Retained round-3b evidence (historical snapshot at 9050c4bb)

The remainder records the prior completed measurements and their original pins.
Its “base” is the group-S-bearing comparison tree `ad2af42ecc394c06d1b443959e1acc435e7a4f0e`;
its “head” is 9050c4bb, tree `3bcc8532549ea69139323a863049022d10f799c1`.
These pins are historical; the current clean checkout and staged parent pin are
recorded above. Fresh round-4 measurements take precedence for F1 and F2.

## Source and authority

Origin is the processor repository. Round 3b started clean at `9050c4bb`.
Original main `ead8036035affd53ef4b29979190f2f4f67084c0` and round-2 head
`ed727d4d` remain ancestors. The required no-fast-forward merge is already present:
`9050c4bb` has parents `9d265988` and exactly `21c6f7096ac80007f723de59c6f717f55bd34cfc`.
The preceding commit supplies the two missing diagnostic arguments. Both commits have
one-line subjects, no bodies or trailers. Round 3b adds no processor source change
or new commit.

Read issue #134 in full, assignment 5988316116, review 5990539778, rulings 5990549074,
5994864535 and [5995957938](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/134#issuecomment-5995957938),
and parent issue #608 comment 5885808887. TAKEN was posted at the start of round 3b.

## Fifth parent patch

The scratch parent is `fa450d301805881ad713b67521477bf042ddadfd`, advanced from the
originally required e6172750 under the round-2 ruling. Round 3b reversed the verified
four-patch application to pristine parent files, then applied c8, p2-p1, c10, 232 and 148
in order, checking each application. Thirteen patched files are bound by a size/hash
manifest. No parent commit or push.

The fifth patch makes `tb/verilator/milan_dp/sim_nxn.cpp` finish reading a frame still
on the trunk at the observation-window end, bounded by 2048 additional cycles.
The existing NOTIFY-CRF assertion now receives both notifications. The isolated head
notification command returns 0: **421 checks, zero failures**. The four-patch failures
at main and head remain historical receipts in r3. No notification RTL or assertion
expectation changed in round 3b.

## Diagnostic repair and record comparison

`tb/pp_top/d3_phases.hpp:2964` and `:2994` now supply `D3_RECORDS`, the integer named by the final `%d` in D3C3/D3C4. Before editing, exact `git grep -F` searches covered both full format lines and both argument lines across `tb/**/*.patch`, `d3_mutants.py` and `notify_mutants.py`. None carried those lines. All 283 patches applied with `git apply --check`; all 110 D3 and 47 notification exact-edit entries matched once before the merge. After the merge all 283 patches, 110 D3 and 53 notification entries still apply: 446 entries, zero refusals. No context refresh was needed and no new check was introduced by this repair.

Three external source exports were used, without another source checkout:

| Export | Source | Repair |
|---|---|---|
| prebase | `5ab43bd9`, tree `fbe1f7b8e626e707333bd5f2f00b4fed02bd0ce0` | Identical two argument additions |
| base | clean merge-tree of `5ab43bd9` and `21c6f709`, tree `96e4990690c1a0b0e8f97933b2a890b1bcb341a9` | Identical two argument additions |
| head | final tree `3bcc8532549ea69139323a863049022d10f799c1` | Committed repair |

This gives the base the same main changes and diagnostic fix, while the original pre-merge base separately remeasures the previously affected receipts.

All three retained source exports were verified against their manifests before this
resume. The base carries the same main merge and diagnostic repair. The original
corrected pre-merge base supplies the third comparison for the eleven affected receipts.
No undefined diagnostic field is removed or normalized. Compilation chatter, temporary
paths and wall-clock build durations are infrastructure metadata, not DUT records.

## Arm, clause and leave timer

The retained S1-S3 arm is `tb/srp_top/sim_main.cpp:802`. Own/peer LeaveAll moves the Listener registrar to LV; repeated Lv in LV preserves registration and ACTIVE until expiry, then one STREAM_STOP is counted. SC1 is `tb/srp_stream_fsms/sim_main.cpp:1072`; SC2/SC3 are `tb/srp_top/sim_main.cpp:923`. The latter drive real MRPDUs at k=0..400 across both registrar planes, own/peer LeaveAll, Ready/ReadyFailed and indices 0/7. Sink 0 holds Advertise and sink 7 Failed. Each case grades both registrations absent, ACTIVE low, one STREAM_STOP and one TK_UNREGISTERED. Sixteen checks prove that a decoded Lv actually meets the calibrated expiry clock.

802.1Q-2014 Table 10-4: rLv/rLA/txLA in LV changes nothing; LV/leavetimer! produces Lv and MT. Milan v1.2 section 4.2.7.2.2 changes only IN/rLv to immediate Lv, MT. LeaveAll starts aging; a registering event stops it. Table 4.3 LeaveTime defaults to 5000 ms, with minimum 4500 and maximum 7500. Both local standards were read through their PDF text extracts.

`hdl/srp/KL_srp_top.sv:106` binds LEAVE_MS_P=5000. Registering-event priority begins at `hdl/srp/KL_srp_talker_fsm.sv:725` and `hdl/srp/KL_srp_listener_fsm.sv:752`; the expiry arms are at `:732` and `:769`. The clause comments are at `:720` and `:747`. `hdl/common/KL_pp_timer_service.sv:192` computes expiry, and `:200` disarms the slot. The expiry is a single-clock strobe; the pending-ARM exclusion and timer queue contract remain unchanged. No port, parameter or register-map change was made.

| LV expiry plus event | Composed Table 10-4 result | Publication / timer |
|---|---|---|
| rNew, rJoinIn, rJoinMt | MT then IN | Retain registration, cancel obsolete timer, preserve renewal indications |
| rLv | MT then MT | Withdraw once; no re-arm |
| rLA, own txLA | MT then MT | Withdraw once; no re-arm |
| rIn, rMt | MT then MT | Withdraw once; no re-arm |

Retained complete default run at this merged head: **8656/8656**, rc 0, **210547557 clocks**, equal to `sim_main.cpp:368`. All 6416 offsets close once; every one of the sixteen groups contains each k=0..400. All eight retained S cases measure 5000 ms, one STREAM_STOP and no STREAM_START. `clock.log/.rc` and `../r3/final-sweep-summary.json` retain this evidence.

## Planted faults

The full round-3b head campaign returns 0: 137/137 checks, assertion coverage 86/86. All new standing trials are killed by their named assertions. Separate round-3 full-sweep receipts retain the original-order and dropped-expiry failures at this exact unchanged head.

| Fault | Failing receipt | Result |
|---|---|---|
| lv-second-lv-ends, lvleave only | `head/srp_top/lv-second-lv-ends.log` | rc 2; 16 S1/S2 failures |
| lv-never-ends, lvleave only | `head/srp_top/lv-never-ends.log` | rc 2; 16 S2/S3 failures |
| lv-expiry-masked, original RTL restored | `../r3/original.log/.rc` | rc 2; exactly 16 SC2 failures, talker k=19 and listener k=35/44; no other failure |
| lv-expiry-masked, unit matrix | `head/srp_top/lv-expiry-masked.log` | rc 2; 16 SC1 failures |
| lv-expiry-last | `head/srp_top/lv-expiry-last.log` | rc 2; 48 SC1 registering-event failures |
| lv-expiry-dropped | `../r3/drop.log/.rc` | rc 2; all 6416 distinct SC2 checks fail; 16 SC3 checks pass |
| lv-expiry-dropped, unit matrix | `head/srp_top/lv-expiry-dropped.log` | rc 2; 80 SC1 and six older failures |
| lv-sweep-misses-collision | `head/srp_top/lv-sweep-misses-collision.log` | rc 2; 16 SC3 failures, SC2 green |

The fresh union (`sc1-current-coverage.json`) covers all 128 SC1 cases; dropped expiry covers all 6416 SC2 cases; missed collision covers all sixteen SC3 checks. Original-order and dropped-expiry full sweeps were repeated at the merged head, with separate logs to avoid the campaign's reuse of the restoration mutant's filename. `../r3/original-summary.json` and `../r3/drop-summary.json` retain the fresh failing case sets.

Standards source identities (the PDF files remain outside the output directory):

| Source | Bytes | SHA-256 |
|---|---:|---|
| 802.1Q-2014 | 19163920 | `0538d48ca469f7983d7261f090e93277503ede30dc8eaf61764f8fbdfa9ac9ab` |
| Milan consolidated specification v1.2 | 1684588 | `6bb902be1c1de8c44f4c4c583a645b0b37e0b2dac27870486ce229e68ce3bba8` |

The prior merged-head clock and complete original-order/dropped-expiry sweeps remain
valid: the processor head is unchanged. Round-3b full campaigns provide fresh standing
mutant receipts under `head/srp_top/`; the restoration mutant's separate full sweep is
retained because the campaign reuses its filename for the later unit run.

## Processor gates and campaigns

Base and head export the pinned simulation executable. Independent work runs concurrently,
with make -j16 and campaign --jobs 3. Completed round-3 documentation, matrix and lint
receipts are retained for the unchanged exports; the interrupted banks are rerun here.
All 33 suite logs are captured before the suite runner removes its temporary logs.
Their runtime records match after the authorized new cases: total checks increase from
1,021,664 to 1,028,224, exactly 128 SC1 plus 6432 SC2/SC3 checks.

| Gate | Corrected merged base | Merged head |
|---|---|---|
| `scripts/run_suites.sh` | rc 0 | rc 0 |
| `scripts/lint_hdl.sh` | rc 0 | rc 0 |
| `make -j16 check` | rc 0 | rc 0 |
| `scripts/gen_matrix.py --check` | rc 0 | rc 0 |
| `syn/yosys/run.sh` | rc 0 | rc 0 |

| Campaign | Corrected merged base | Merged head |
|---|---|---|
| srp_top | rc 0; assertion coverage: 83/83; missing=[]; 131 checks: 131 PASS, 0 FAIL | rc 0; assertion coverage: 86/86; missing=[]; 137 checks: 137 PASS, 0 FAIL |
| srp_admission | rc 0; 12 checks: 12 PASS, 0 FAIL | rc 0; 12 checks: 12 PASS, 0 FAIL |
| d3 | rc 0; D3 mutations: 110 of 110 KILLED by their named checks; goldens PASS | rc 0; D3 mutations: 110 of 110 KILLED by their named checks; goldens PASS |
| notify | rc 0; C6 notification mutations: 53 of 53 KILLED by their named checks; goldens PASS | rc 0; C6 notification mutations: 53 of 53 KILLED by their named checks; goldens PASS |
| aecp_dispatch | rc 0; 44 checks: 44 PASS, 0 FAIL | rc 0; 44 checks: 44 PASS, 0 FAIL |
| acmp | rc 0; ACMP mutations: 33 of 33 KILLED by their named checks; goldens PASS | rc 0; ACMP mutations: 33 of 33 KILLED by their named checks; goldens PASS |
| aecp | rc 0; 67 checks: 67 PASS, 0 FAIL | rc 0; 67 checks: 67 PASS, 0 FAIL |
| gsi | rc 0; GSI mutations: 20 detected by named checks; golden and restored PASS | rc 0; GSI mutations: 20 detected by named checks; golden and restored PASS |
| ctr | rc 0; 18 checks: 18 PASS, 0 FAIL | rc 0; 18 checks: 18 PASS, 0 FAIL |
| name_wr | rc 0; Name-write mutation: decode killed; golden and restored PASS | rc 0; Name-write mutation: decode killed; golden and restored PASS |
| adp | rc 0; 43 checks: 43 PASS, 0 FAIL | rc 0; 43 checks: 43 PASS, 0 FAIL |
| maap | rc 0; 32 checks: 32 PASS, 0 FAIL | rc 0; 32 checks: 32 PASS, 0 FAIL |

These twelve campaigns build files changed by the lane or required main merge. The retry
campaign builds only unchanged ACMP talker sources. The documentation gate's retained
export runs use a read-only Git inventory adapter; fixture initialization uses ordinary
Git. The actual Git checkout also passed make check in round 3. No source was changed
for that environment accommodation.

| Suite | Base checks | Head checks |
|---|---:|---:|
| acmp_listener | 3111 | 3111 |
| acmp_nvm | 388 | 388 |
| acmp_talker | 1342 | 1342 |
| adp_engine | 1348 | 1348 |
| aecp_notify | 34 | 34 |
| ca_originator | 16 | 16 |
| desc_mem_guard | 78 | 78 |
| desc_store | 586 | 586 |
| dispatch | 211 | 211 |
| dyn_state | 118 | 118 |
| event_router | 81 | 81 |
| lsn_admit | 18 | 18 |
| maap | 196 | 196 |
| nvm_port | 1219 | 1219 |
| originator | 107 | 107 |
| pp_top | 10444 | 10444 |
| prng | 76 | 76 |
| release_merge | 18 | 18 |
| resp_buf | 64 | 64 |
| rx_slots | 130 | 130 |
| rx_validator | 555 | 555 |
| scoreboard | 3705 | 3705 |
| side_port | 368 | 368 |
| srp_admission | 991231 | 991231 |
| srp_decoder | 190 | 190 |
| srp_encoder | 581 | 581 |
| srp_stream_fsms | 1219 | 1347 |
| srp_top | 2224 | 8656 |
| timer_map | 1360 | 1360 |
| timer_service | 48 | 48 |
| tx_arbiter | 66 | 66 |
| tx_slots | 95 | 95 |
| ucpu | 437 | 437 |

## Parent consumers

Each bank stages its processor gitlink before running: main 21c6f709 at base, 9050c4bb
at head, with the same five patches. Direct submodule Git commands are preceded by a
top-level identity check. The final staged gitlink must be the final head.

| Consumer | Command from the parent root | Main baseline | Head |
|---|---|---|---|
| 01_check_cpp_idiom | `python3 scripts/check_cpp_idiom.py` | rc 0 | rc 0 |
| 02_check_py_idiom | `python3 scripts/check_py_idiom.py` | rc 0 | rc 0 |
| 03_check_rtl_source_lists | `python3 scripts/check_rtl_source_lists.py` | rc 0 | rc 0 |
| 04_pp_srcs | `python3 scripts/pp_srcs.py --check --selftest` | rc 0 | rc 0 |
| 05_check_port_contracts | `python3 scripts/check_port_contracts.py` | rc 0 | rc 0 |
| 06_measure_naming | `python3 scripts/measure_naming.py --check` | rc 0 | rc 0 |
| 07_measure_test_evidence | `python3 scripts/measure_test_evidence.py --check` | rc 0 | rc 0 |
| 08_docs_check | `python3 scripts/docs_check.py` | rc 0 | rc 0 |
| 09_xvlog_gate | `python3 scripts/xvlog_gate.py --check` (under the synthesis lock) | rc 0 | rc 0 |
| 10_builder | `python3 sw/builder/test_builder.py` | rc 0 | rc 0 |
| 11_lint_rtl | `python3 scripts/lint_rtl.py --check` | rc 0 | rc 0 |
| 12_pp_shadow | `make -j16 -l8 -C tb/verilator/pp_shadow` | rc 0 | rc 0 |
| 13_nvm_cosim_lint | `make -j16 -C tb/verilator/nvm_cosim lint` | rc 0 | rc 0 |
| 14_nvm_cosim_quick | `make -j16 -C tb/verilator/nvm_cosim quick` | rc 0 | rc 0 |
| 15_milan_dp | `make -j16 -l8 -C tb/verilator/milan_dp VERILATOR_JOBS=3` | rc 0 | rc 0 |
| 16_milan_dp_render | `make -j16 -l8 -C tb/verilator/milan_dp_render` | rc 0 | rc 0 |
| 17_check_sh_idiom | `python3 scripts/check_sh_idiom.py` | rc 0 | rc 0 |
| 03b_check_rtl_source_lists_selftest | `python3 scripts/check_rtl_source_lists.py --selftest` | rc 0 | rc 0 |
| 16b_render_mutants | `python3 tdm8_render_mutants.py --leg-defects` (cwd `tb/verilator/milan_dp_render`) | rc 0 | rc 0 |

The builder retains its inherited missing mf48 fixture NOT RUN. No hardware result is
claimed. The default render command includes five leg-defect checks, and the separate
supplementary invocation retains their own receipt. That mode does not accept --jobs.

## Comparisons, area and final integrity

The parent Python gate reports 200087 lines at main and 200095 at head, with the
same 317 modules and identical findings and verdicts. The eight-line inventory
increase is exactly the nine additions minus one removal in
`tb/srp_top/mutants.py`, for the authorized new trials. The raw difference and
source accounting are retained in `parent-metadata-differences.json`.
That file also preserves the builder gate 17's clipped temporary fixture owner
names. The gate prints the first 100 characters of an expected exception;
only that random name differs. Temporary paths and names are normalized in
the consumer comparison, with the DUT and assertion fields retained.

- `comparison-suites.json`: recorded
- `comparison-runtime.json`: recorded
- `comparison-verdicts.json`: recorded
- `comparison-eleven.json`: recorded
- `comparison-parent.json`: recorded
- `comparison-parent-all.json`: recorded
- `meas/delta.json`: recorded
- `integrity-final.json`: recorded

| Campaign record comparison | Identical existing receipts | Different existing receipts | Added receipts |
|---|---:|---:|---:|
| srp_top | 125 | 0 | 5 |
| srp_admission | 12 | 0 | 0 |
| acmp | 37 | 0 | 0 |
| notify | 60 | 0 | 0 |
| d3 | 116 | 0 | 0 |
| aecp_dispatch | 44 | 0 | 0 |
| aecp | 67 | 0 | 0 |
| gsi | 22 | 0 | 0 |
| ctr | 18 | 0 | 0 |
| name_wr | 3 | 0 | 0 |
| adp | 43 | 0 | 0 |
| maap | 32 | 0 | 0 |

All 579 existing campaign runtime receipts and all 33 suite receipt sets match after only the authorized collision additions. The only added campaign receipt files are the five new SRP collision trials/control. There are no remaining unexplained DUT-record differences. Build-only logs remain separate from runtime records.

All 282 structured result entries in the 6 campaigns that emit them are identical when keyed by trial identity; concurrent completion order is not a DUT record.

| Parent runtime comparison | Base records | Head records | Result |
|---|---:|---:|---|
| 10_builder | 506 | 506 | identical |
| 12_pp_shadow | 2336 | 2336 | identical |
| 15_milan_dp | 12530 | 12530 | identical |
| 16_milan_dp_render | 203 | 203 | identical |
| 16b_render_mutants | 6 | 6 | identical |

The eleven previously affected receipts compare literally with the corrected pre-merge base:

| Receipt | Corrected merged base | Merged head |
|---|---|---|
| d3/RPL_clks.log | identical | identical |
| d3/TRG_clks.log | identical | identical |
| d3/blank_applies_zero.log | identical | identical |
| d3/clks_restore_count_narrowed.log | identical | identical |
| d3/clks_restore_index_narrowed.log | identical | identical |
| d3/clks_row_two_bits.log | identical | identical |
| d3/done_without_d3.log | identical | identical |
| d3/rule_ignored.log | identical | identical |
| d3/unframed_reads_as_device_error.log | identical | identical |
| aecp_dispatch/sclks-bound-inclusive.log | identical | identical |
| aecp_dispatch/sclks-bound-three.log | identical | identical |

| OOC 1x1 resource | Main baseline | Merged head | Delta |
|---|---:|---:|---:|
| LUT | 23161 | 23145 | -16 |
| FF | 19783 | 19780 | -3 |
| BRAM_TILE | 17.5 | 17.5 | +0.0 |
| RAMB36 | 16 | 16 | +0 |
| RAMB18 | 3 | 3 | +0 |
| DSP | 8 | 8 | +0 |
| CARRY4 | 1494 | 1494 | +0 |
| WNS_ns | -2.685 | -2.578 | +0.107 |
| WHS_ns | 0.159 | 0.159 | +0.000 |

The area scope is the synthesized `KL_pp_shadow` wrapper on `xc7a100tfgg484-2`, with a 20 ns standalone clock and the recipe's area optimization directive. Timing figures are synthesized estimates; this measurement does not claim implementation timing closure.

The measurement identity, all bound parameters and all six image manifests match. The source-input digest changes with the RTL. The resource gate returns 0 with the required 40-LUT/40-FF tolerance; the wrapper and processor-core deltas are both **-16 LUT, -3 FF**. RAM and DSP counts are unchanged. The ungated SRP subtotal is +40 LUT, 0 FF; the full hierarchy movements remain in `meas/resource-gate.stdout`. Both compiler gates return 0 at the same inherited two-finding ratchet. All six measured images are frozen with matching sizes and hashes in `meas/frozen-images.json`.

Final integrity confirms the clean processor checkout, the required merge parents, all three source exports, thirteen patched parent files, and four clean pinned submodules. The staged parent processor gitlink is the final head. Generated parent products were moved outside the scratch tree.

All validation and measurement processes have exited. The canonical checkout has no ignored/generated files, and the service records zero out-of-memory events or kills. File-cache reclaim events are retained in `integrity-processes.json`.

Artifact ledger: `$VALIDATION_STORAGE/pp134-a538/r3b/artifact-ledger.json`, 332134 bytes, SHA-256 `673dbede374e502c2370786f018abfe2611a387f53fa1b1ed63f08045df4d472`. It records sizes and hashes for the retained evidence; larger artifacts are not copied to the output directory.

The fresh area workflow uses the parent #638 recipe, generated shipping images and
bound parameters, 1x1 at the integrated 50 MHz clock. The extracted parameters
bind two input and two output streams, 576-byte descriptor lines, and the same
six initialization images (165732 bytes total). Vendor runs hold
`flock $VIVADO_LOCK` and start only after all heavy validation. The STOP
threshold is more than 40 LUT or 40 FF. Historical pre-merge area is not substituted.

Evidence root: `$VALIDATION_STORAGE/pp134-a538/r3b`; prior roots r2 and r3 remain intact.
Large logs, source exports, binaries, environments and products remain outside the
output directory. Initial lower-concurrency suite/builder attempts were interrupted
and retained under `attempts/initial-concurrency`; no pass is claimed from those attempts.
No hardware/bench access, flashing, push, PR creation/edit, rebase, amend, parent commit,
or existing issue/PR comment edit/deletion was performed.
