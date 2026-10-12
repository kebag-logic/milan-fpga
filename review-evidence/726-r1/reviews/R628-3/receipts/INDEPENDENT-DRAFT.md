[R628] independent draft, written before any prior review report or probe was opened (2026-10-12T20:47Z)

Head e893e4d13d99eb5ba00745f0f5cf74ee847972c2, tree 0e94807ebc9c4978bfb173c8d3076f9ddfefc4cf.

Draft verdict: NEGATIVE (one MAJOR open).

Draft findings
- F1 MAJOR, Conformance + Tests + Docs: the window grading passes only by the alignment of the
  fixed one-second grid. In the PR's own clean runs the input-0 rows have an empty window 1 between
  two steady-cadence notifications (shipping 0.999742 -> 2.000742 s; largest 0.999115 -> 2.000115 s and
  0.999896 -> 2.000878 s). The evidence excludes windows 0-1 as "registration and startup
  transient". Shifting the grid 0.2 ms (largest) or 0.8 ms (shipping) later makes the PR's own
  [726 CADENCE] check fail on the corrected RTL. With the unchanged scheduler period of
  1000 ms + service, ruling 6126028604's first bullet cannot hold on a fixed grid indefinitely.
  The conflict needs a public maintainer decision, and the evidence and texts must stop presenting
  the selected windows as proof of that bullet.
- S1 SUGGESTION, Robustness + RTL: KL_crf_rx drops an AVTPDU accepted in the bind-rise cycle
  (wipe overrides the increment); talker and AAF keep the coincident event.
- R1 RESIDUE, Docs: PR body Status still says "Local source head" and "The new commits remain local
  pending authorized publication"; e893e4d1 is the published PR head.

Draft ledger
| lens | state | key artifacts |
|---|---|---|
| Conformance | UNCLEAN (F1) | RTL counters, resets, dirty sources; window evidence |
| RTL | CLEAN | four HDL files, datapath arbiter, area/timing evidence (author-reported) |
| Robustness | CLEAN | bind/unbind/start/wrap/batch boundary plants; S1 only |
| Tests | UNCLEAN (F1) | 9+2 plants, 4 reviewer plants, grader guard probes, window-shift probe |
| Docs | UNCLEAN (F1) | 726_STREAM_COUNTERS.md, REGISTER_MAP, audit, AECP README, dated notes; R1 residue |
