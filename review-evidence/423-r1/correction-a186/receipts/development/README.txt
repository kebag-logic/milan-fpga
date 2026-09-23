Development runs on uncommitted working trees or intermediate commits.
selftest-before-injection-retarget.out: first run after the transport change, before the two
original path-arm fault injections were retargeted from _git to _git_raw; its 4 FAIL lines
show the old injection no longer reached the measurement (verdict became contained/0).
None of these files is final-head evidence.
