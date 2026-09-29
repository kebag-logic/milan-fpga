[A403] Relates to #451.

Records TDM8 first light in both directions in
`docs/findings/451_TDM8_FIRST_LIGHT.md` and lists the page in the
`docs/findings/README.md` index. Against the base, the net change is that one
added page and one index row. Five commits: `fba793c0` (the 2026-09-27
attempt record), `361d1f47` (first session, replacing the attempt record),
`4f06bfc7` (second session), `6339479d` (one line reworded for the bare-metal
gate) and `335e55c4` (round 2, below).

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

One DUT defect is recorded and tracked by #617: the talker can assemble one
AAF frame from two adjacent TDM frames split between channel pairs. Pairs 1
to 3 lag pair 0 by one frame in 67.5% of frames, cycling once per beat. The
cause is per-pair holds in the capture crossbar read at the media tick, not
the link.

The page records the method, both decode tables, the continuity
classification, the frame-rate offset (10.64 ppm from the DUT slip counter,
matching the divider plan), what changed since the attempt and between the
sessions, the restoration and its residuals, and two disclosed operator
errors. The recorded continuity check, scope measurements, the capture
through the USB Audio device, #386 acceptance 4 and the calibrated #117
listener-audio sequence stay NOT RUN.

Round 1 validation at `6339479d69830614d4267bd3170113737afbf8f4`, all return
code 0: `scripts/docs_check.py`, `scripts/check_doc_style.py`,
`scripts/gen_toc.py --check`, `scripts/check_em_dash.py --base 6d5ebd73`,
`scripts/check_doc_paths.py`, `scripts/ci_scope.py --selftest`,
`scripts/check_baremetal_only.py --check` and `git diff --check`. The
evidence packet `451-a403` is in the public evidence archive, commit
`851f835c` on the `451-review-evidence` branch, under
`review-evidence/451-r1/author`.

## Round 2

[A423] answers the round-1 reviews R392-1 and R393-1 in one documentation
commit, `335e55c4135979a554dc0281d6980ac1e2158aee`. It changes only the page
and the index.

- **DIN outside playback (R392-1 F1, R393-1 S1).** The idle-high claim and
  the conclusion that a zero word could not have come from the pin are
  removed. The page now states what the routed recording holds outside
  playback:
  - `0xffffff00` in every word before playback and after the stop tail;
  - the transition frame 150,489;
  - the 777 frames of zero words at the stop (3,510,525 to 3,511,301), the
    first torn like the pattern frames.

  The root cause now rests on the narrower argument. The unrouted recordings
  are also zero over the roughly 25 s without playback, where the routed
  recording reads `0xffffff00`. The map edit was the only change between the
  second session's two runs.
- **Frame coherence (R392-1 F2, R393-1 F1).** #617 is linked in the summary,
  in the section that names the defect, and in the owner-items row.
- **Findings index (R393-1 F2).** The page has a row at the top of "Current
  entries", because the index lists issue-numbered findings newest first.
- **Owner's wiring check (R393-1 F3).** The check is cited to the owner report
  on #451. The page gives the report's items (BCLK, FSYNC, DOUT, DIN and
  ground) against the amendment's seven conductors: four signals and three
  grounds.
- **Suggestions taken (R393-1 S2 to S6):**
  - the status token is gone from the page head;
  - a NOT RUN owner-items row covers the "through the USB Audio device"
    checklist item;
  - this body's commit count is corrected;
  - the DOUT beat row is labelled as the 34 crossings clear of any underrun.
    The two other crossings, inside the underrun clusters at frames 129,825
    and 411,321, are stated, and the TDM hold read is cited at lines 959 to
    960;
  - the packet is linked to the public evidence archive.

The measurement tables are unchanged apart from the beat-row label. Every new
number was re-derived from the archived evidence: the author's routed-DIN
decode and DOUT cluster attribution, and both reviewers' archived receipts.
The raw captures were not re-read.

Round 2 validation at `335e55c4`, all return code 0, unpiped, with the pinned
Markdown environment: `scripts/docs_check.py`, `scripts/check_doc_style.py`,
`scripts/check_doc_paths.py`, `scripts/gen_toc.py --check` and
`scripts/check_em_dash.py --base 6d5ebd73`. Also `git diff --check 6d5ebd73
HEAD`. The page's eleven tables and the index table pass rendered and source
cell-count checks.

The index row conflicts textually with the #75 and #397 rows that live `dev`
(`ce550952`) added at the same place. The resolution keeps all rows, with the
#451 row first.

This record does not close #451, #448, #386 or #117.

## Merge with dev

[A426] merged live `dev` `7390b436` into the branch as `f4bb2bd7`, with the
subject "Merge dev into 451-tdm8-first-light". The only conflict was
`docs/findings/README.md`: dev's #75, #395 and #397 rows against this PR's #451
row, all at the top of "Current entries". The resolution keeps all ten rows,
with the #451 row first and dev's rows after it in dev's order. No row is lost
or duplicated. The gitlinks are dev's, unchanged, because the branch never
touched them.

A separate commit, `0e5ae9c8`, rewords two statements that the DOUT result
contradicts. Both said the shipping AX7101 1x1 TDM8 configuration has no
physical TDM render:

- `docs/reference/MILAN_COMPLIANCE_MATRIX.md`, row 4.4.4.5 / .9. "The TDM render
  lane is not clocked on any shipping build" now says the lane is clocked on
  that shape (#447) and that first light decoded its eight slots in order. Its
  silicon figure still rides #117.
- `docs/litex/CLOCK_DOMAINS.md`. "The example configuration exposes capture,
  not physical TDM rendering" now says it exposes both, and cites first light.

The search for other such statements covered the whole merged tree outside
`docs/history` and the submodules. It looked for first light, #451, the SoC
board, J11, render and capture status, and #386, #448 and #117 silicon claims.
Nothing else is contradicted by the page. Against `dev`, the net change is now
the page, its index row and these two lines.

Validation at `0e5ae9c82bbdb5abc3feba84f07d0e6481254906`, all return code 0,
unpiped, with the pinned Markdown environment:

- `scripts/docs_check.py`;
- `scripts/check_doc_style.py`, plus `--selftest`;
- `scripts/check_doc_paths.py`;
- `scripts/gen_toc.py --check`;
- `scripts/check_em_dash.py --base 7390b436`, the merge base, plus `--selftest`;
- `scripts/check_baremetal_only.py --check`;
- `git diff --check 7390b436 HEAD`.

The same gates pass at the merge commit. The index table and the edited matrix
table have three cells in every row, in the source and when rendered.

## Merge with dev, round 2

[A436] merged live `dev` `13eda870` into the branch as `caa1df66`, with the
subject "Merge dev into 451-tdm8-first-light". Dev had gained PR #614, PR #603
(#602), PR #615 (#607) and PR #609 (#590, #592, #599).

The only conflict was `docs/reference/MILAN_COMPLIANCE_MATRIX.md`, in two
adjacent rows. Dev's #602 rewrote 4.4.4.3 (`mr` and the PHC-only re-base), and
this PR rewrote 4.4.4.5 / .9. The resolution keeps dev's 4.4.4.3 and this PR's
4.4.4.5 / .9, each with its link. Dev's other matrix rows merged unchanged:
5.4.2.15 / .16 and 5.3.11.1 from #602, and 7.4.42.2 from #609. The resolved
matrix differs from `dev` by this PR's one line only.

`docs/findings/README.md` merged cleanly. It holds the #451 row first, then
dev's nine rows in dev's order, including #609's reworded #397 row.
`docs/litex/CLOCK_DOMAINS.md` also merged cleanly. The gitlinks are dev's,
with `protocol-processor` at `c951a9ff`.

Against `dev`, the net change is still the page, its index row and the two
reworded lines. The merge brings exactly dev's changes.

The stale-statement search found nothing to reword, so there is no new
rewording commit. It covered:

- dev's added lines;
- the whole merged tree outside `docs/history` and the submodules, compared
  with the search at `0e5ae9c8`;
- the page, for the topics dev changed.

Validation at `caa1df666de17ba38ae402c52e1ae219dbd01d8b`, all return code 0,
unpiped, with the pinned Markdown environment:

- `scripts/docs_check.py`;
- `scripts/check_doc_style.py`, plus `--selftest`;
- `scripts/check_doc_paths.py`;
- `scripts/gen_toc.py --check`, plus `--selftest` and `--verify-anchors`;
- `scripts/check_em_dash.py --base 13eda870`, plus `--selftest`;
- `scripts/check_baremetal_only.py --check`, plus `--selftest`;
- `git diff --check`, and `git diff --check 13eda870 HEAD`.

All 14 matrix tables and the index table have a constant cell count in every
row, in the source and when rendered.

