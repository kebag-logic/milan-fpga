[R474] draft written before reading any prior review findings on PR #672 (R474-5, R475-6, R475-7 report bodies were not opened; only their probe scripts/inputs named in the assignment were run).

Exact head 7426045c94c317363e5589856e6f3f9fde1a2d21, delta 1e79ebdc..7426045c (rounds 2h and 2i).

Independent draft verdict: POSITIVE. No open BLOCKER/MAJOR/MINOR found.

- Conformance: rulings 6075072415 items 1-5 and 6076487047 items 1-2 are implemented. CLEAN.
- RTL: no hdl/ change in the delta. The follow_ring run target is a bounded -j4 sub-make with one obj_dir build, verified under serial outer make (MAKEFLAGS unset) and outer make -j16 --trace. CLEAN.
- Robustness: a leg failure propagates (incidental missing-include run returned rc 2). 126/126 integer-oracle boundary cases agree at 1e-30 s resolution. Real dup, skip and recentre traces agree with the harness's own window counts. CLEAN.
- Tests: 8/8 unit tests pass at head and 22 subtests fail against the 8e4b1e53 reader. 14/14 planted trace_table defects are caught, R475-7 decimal 9/9 passes, and the parent gets 0/9. CLEAN.
- Docs: every hosted, replica, ratio and margin figure was recomputed from the raw hosted logs and author receipts, and all match. CLEAN apart from residue.

Candidate residue (wording only): the trace_table.py docstring says the servo snapshot is taken "before the step's end", but the code and test take the last window at or before the end (<= te).
Candidate suggestions:
- -O/--output-sync, or line-buffered stdout, for the -j4 legs (b8 writes 4484 bytes, so one line can straddle the 4 KiB flush).
- The unit-test docs say "genuine duplicate and skip frames" for fixture counter records.
- Event, PDU, servo and origin timestamps are printed at different precisions (1 ns, 100 ns, 1 us, 1 us).
