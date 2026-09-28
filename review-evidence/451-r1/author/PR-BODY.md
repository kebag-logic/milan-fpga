[A403] Relates to #451.

Replaces the 2026-09-27 attempt record with the first-light result in
`docs/findings/451_TDM8_FIRST_LIGHT.md`, removing
`docs/findings/451_TDM8_FIRST_LIGHT_ATTEMPT.md`. No other file changes.
Three commits: `361d1f47` (first session), `4f06bfc7` (second session) and
`6339479d` (one line reworded for the bare-metal gate).

Both directions carry identifiable audio in all eight slots, in order, over
70 s each.

- **DOUT.** Over a 70 s capture on the SoC board, each capture channel carried
  the expected DUT listener channel in the expected TDM slot, with 0 torn
  frames and 0 invalid words. Every discontinuity is a whole frame: the
  documented INTERNAL-source beat, or render-queue underruns from the software
  talker. A 3 s capture in the second session showed no regression.
- **DIN.** Over 70 s of SoC playback, every word of the DUT's talker stream
  carried its own channel's tag, in order. Each channel is continuous apart
  from the INTERNAL-source beat.

The first session recorded DIN as all zero and attributed it to the wiring.
That was wrong. In this image STREAM_PORT_OUTPUT 0 has a dynamic audio map,
so the capture crossbar feeds the talker, and the first session left that map
empty. The second session repeated the DIN leg unchanged, again all zero,
then repeated it with eight identity mappings on that port. Those mappings
were removed afterwards.

One DUT property is recorded for triage as a separate issue: the talker can
assemble one AAF frame from two adjacent TDM frames split between channel
pairs. Pairs 1 to 3 lag pair 0 by one frame in 67.5% of frames, cycling once
per beat. The cause is per-pair holds in the capture crossbar read at the
media tick, not the link.

The page records the method, both decode tables, the continuity
classification, the frame-rate offset (10.64 ppm from the DUT slip counter,
matching the divider plan), what changed since the attempt and between the
sessions, the restoration and its residuals, and two disclosed operator
errors. The recorded continuity check, scope measurements, #386 acceptance 4
and the calibrated #117 listener-audio sequence stay NOT RUN owner items.

Validation at the local head `6339479d69830614d4267bd3170113737afbf8f4`, all
return code 0: `scripts/docs_check.py`, `scripts/check_doc_style.py`,
`scripts/gen_toc.py --check`, `scripts/check_em_dash.py --base 6d5ebd73`,
`scripts/check_doc_paths.py`, `scripts/ci_scope.py --selftest`,
`scripts/check_baremetal_only.py --check` and `git diff --check`. Eleven
tables pass rendered and source cell-count checks. Evidence is retained in
packet `451-a403`.

This record does not close #451, #448, #386 or #117.
