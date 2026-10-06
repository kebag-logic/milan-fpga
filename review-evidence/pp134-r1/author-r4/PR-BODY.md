[A538]

Closes #134

An Lv decoded on an LV registrar’s expiry clock could mask the expiry and leave
registration and the stream licence open indefinitely. Both registrar planes now
produce the result of expiry followed by reception, per 802.1Q-2014 Table 10-4.
Lv and LeaveAll finish MT; New and Join finish IN and cancel the obsolete timer
while retaining renewal indications.

The tests cover own and peer LeaveAll, 128 simultaneous-event combinations,
6416 byte-stream offsets, and sixteen collision-coverage checks. The retained
LeaveTime arm measures 5000 ms against Milan Table 4.3. Planted faults cover
every added check. Both D3 restore diagnostics receive their missing record-count
arguments. Main 21c6f709 is merged with a merge commit; main has not advanced.

Round 4 corrects the suite README’s full-run mutation record. Each checked-in
patch was planted separately and run through the complete default suite:

| Fault | Result out of 8656 checks | Failing assertions | Exit |
|---|---|---|---:|
| lv-second-lv-ends | 8640 pass, 16 fail | S1: 8; S2: 8 | 2 |
| lv-never-ends | 5624 pass, 3032 fail | S2: 8; S3: 8; SC2: 3016 | 2 |

All four storage shapes pass 15 checks under each fault. The documentation gate
passes after the correction. Round 4 adds no executable source or check.

Suite-bank identities, measured by `scripts/run_suites.sh`:

- Main baseline: commit `21c6f7096ac80007f723de59c6f717f55bd34cfc` with only the
  same two diagnostic argument additions; exact tree `579e3c599dcd013647a7a7e5fa0418fe4f4b4c18`.
- Head: commit `a596c7626864ae10026994ca777a8ccfdb53a9f6`, exact tree `3c8b892c98694479945f471a55aaea9ab442294a`.

Both complete banks return 0. Their per-suite tallies are:

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

The difference is **6,584 = 24 S1–S3 + 128 SC1 + 6416 SC2 + 16 SC3**.
All 33 runtime receipt sets match after those authorized additions and the added
run-length record, independently checked as 210547557 clocks. The runner
uses each suite’s final tally; supplementary shape checks remain in its receipt.

The earlier total **1,021,664** belonged to exact tree `ad2af42ecc394c06d1b443959e1acc435e7a4f0e`:
round-1 head 5ab43bd9 merged with main 21c6f709, with the same diagnostic repair.
That tree already contains the 24 S1–S3 checks, so srp_top is 2224 there, versus
2200 at the main baseline above; every other suite tally is identical. Its
comparison with head tree `3bcc8532549ea69139323a863049022d10f799c1`
(total 1,028,224) correctly differs by 6,560. The former description did not name
that intermediate base. The main-to-head baseline total is **1,021,640**.

Other validation remains bound to the retained comparison tree `ad2af42ecc394c06d1b443959e1acc435e7a4f0e`
and head tree `3bcc8532549ea69139323a863049022d10f799c1`. Round 4 changes
only `tb/srp_top/README.md`; final-head compiled and measured inputs are identical
to those at 9050c4bb:

- Every processor suite, HDL lint, documentation checks, matrix check and
  synthesis gate passed at both retained trees. The fresh head bank also matches
  the retained head bank’s runtime records exactly.
- All twelve campaigns passed: 579 existing runtime receipts match, with only
  five authorized collision receipt files added; all 282 structured results match.
- All eleven receipts affected by the diagnostic repair match the corrected
  pre-merge base. No undefined field is filtered. All 446 planting audit entries apply.
- The complete head SRP run passes 8656/8656. The measured run length is
  210547557. Restored branch order fails sixteen collision cases; dropped expiry
  fails all 6416 sweep checks.
- All seventeen parent consumer commands and both supplemental checks passed at
  main 21c6f709 and head 9050c4bb, using all five adoption patches. Runtime records
  match. The notification gate passes 421 checks. The inherited missing mf48
  calibration fixture is explicitly recorded as not run.
- Thirteen parent checks were repeated successfully with the gitlink staged at
  `a596c7626864ae10026994ca777a8ccfdb53a9f6`, including documentation, source-list contracts, naming,
  test evidence, RTL lint and the NVM quick check. Their records match the retained
  head receipts.

The retained shipping 1x1 OOC measurement passes the 40-LUT/40-FF gate:
23,161 → 23,145 LUTs and 19,783 → 19,780 FFs, a delta of **−16 LUT, −3 FF**.
RAM and DSP counts are unchanged. Both measurements use identical bound parameters,
a 50 MHz clock, and six identical initialization images; both compiler gates pass.
The README-only correction changes no measurement input, so this is retained
round-3b evidence, not a new area run. The complete measurement record and source
input digest were read again at the final pin and match exactly. The checkout is clean, and the
scratch parent remains uncommitted with its processor gitlink at the final head.
