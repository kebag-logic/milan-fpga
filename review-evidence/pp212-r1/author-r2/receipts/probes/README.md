# The reviewers' probes, re-run at head a2fce43

- `r770.out`, `r770/`: R770-1's `probe.py` (`scripts/r770_probe.py`, the packet's script byte for
  byte), suite `srp_stream_fsms`, on the head tree. Every probe whose text still exists at the head
  was run. Each of the six that passed every suite at round 1 now fails its named rows: PS16, PS17
  (three probes), PS18, PS19. `presettle-removed` here is the reviewer's form (the seed and the
  one-walk declaration only); PS3 passes under it because the kept registration serves a re-bind
  to the same stream. The campaign's `presettle-removed` also removes the kept registration and
  fails PS3. `seed-declares-ready-only` was not run: the line it edits now also selects the kept
  registration's type, and `keep-declares-seed-type` and `seed-type-advertise` plant that defect.
- `r769.log`, `r769.rc`: R769-1's probe block (`scripts/r769_probe.diff`, the packet's diff),
  inserted at the end of the PS15 function of the head's `tb/srp_stream_fsms/sim_main.cpp`. Its
  hunk context names the old `run()`, which the new rows now follow. Result: rc 0, 1502 of 1502,
  PROBE-R1a and PROBE-R1b included, where both failed at round 1.
