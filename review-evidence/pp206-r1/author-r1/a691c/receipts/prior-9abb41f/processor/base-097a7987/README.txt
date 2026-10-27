gsi_internal.*: make -C tb/pp_top gsi-internal at the base 097a7987 (its tests, its RTL):
  rc 0, 6254 checks, 0 failures. The same target at the head 9abb41f: 6373 checks, 0 failures
  (the 119 checks of the settled-gate step; the head's full pp_top run is in sweep-9abb41f).
head-tests-on-base-rtl.*: the head 9abb41f tree with hdl/ replaced by the base's
  (head-tests-base-rtl.hdl-equal.txt is the empty output of diff -rq between that hdl/ and
  the base clone's; head-tests-base-rtl.hdl-diff.txt is git diff --stat 097a7987 9abb41f -- hdl/),
  then make -C tb/pp_top gsi-internal: make rc 2 because the simulation exits 1;
  82 FAIL lines, 32 of them "GI GATE", the same lines as the settled-gate-removed arm.
