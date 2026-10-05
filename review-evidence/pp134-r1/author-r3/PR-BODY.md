[A538]

Closes #134

An Lv decoded on an LV registrar's expiry clock could mask the expiry and
leave registration and the stream licence open indefinitely. Both registrar
planes now produce the result of expiry followed by reception, per
802.1Q-2014 Table 10-4. Lv and LeaveAll finish MT; New and Join finish IN
and cancel the obsolete timer while retaining renewal indications.

The tests cover own and peer LeaveAll, 128 simultaneous-event combinations,
6416 byte-stream offsets, and sixteen collision-coverage checks. The retained
LeaveTime arm measures 5000 ms against Milan Table 4.3. Planted faults cover
every added check. The two D3 restore diagnostics now receive their missing
record-count arguments. Processor main 21c6f709 is merged with a merge commit.

Validation at 9050c4bb:

- Every processor suite, HDL lint, documentation checks, matrix check and
  synthesis gate passes at corrected merged base and head.
- The suite banks pass 1,021,664 and 1,028,224 checks respectively. All 33
  suite receipt sets match after the authorized collision additions.
- All twelve campaigns pass. All 579 existing campaign runtime receipts
  match, with only the five authorized SRP collision receipt files added.
  All 282 structured campaign results match.
- All eleven receipts affected by the format defect match the corrected
  pre-merge base at both merged base and head. No undefined field is filtered.
- The complete head SRP run passes 8656/8656 and measures 210547557 clocks.
  Restored branch order fails sixteen collision cases; dropped expiry fails
  all 6416 sweep checks. Planted faults cover every added check.
- All 446 patch and exact-edit audit entries still apply.
- The parent notification gate passes 421 checks with all five adoption
  patches. All seventeen parent consumer commands and both supplemental checks pass
  at both pins, with matching runtime records. The inherited missing mf48 calibration
  fixture remains explicitly reported as not run.

The fresh shipping 1x1 OOC measurement passes the 40-LUT/40-FF gate:
23,161 to 23,145 LUTs and 19,783 to 19,780 FFs, a delta of **-16 LUT,
-3 FF**. RAM and DSP counts are unchanged. Both measurements use identical
bound parameters, a 50 MHz clock, and six identical initialization images.
Both parent compiler gates pass. The final source audit confirms the clean
processor checkout and the scratch parent's processor gitlink at 9050c4bb.
