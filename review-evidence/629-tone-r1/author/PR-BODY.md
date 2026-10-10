[A588] Bench lane B15 for #629: where Direction B's tone is lost

Refs #629.

Adds the dated section "Dev 5603c353, 2026-10-10: lane B15" to `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (with its Contents line, the introduction's pointer and the title's image list) and updates its row in `docs/findings/README.md`. No code, RTL or firmware changes.

## Result

The known tone was played through the authorised tone source and four points of its path were captured at the same time, twice, on the dev `5603c353` image:

- (a) the reference peer's own talker stream, on the peer's link tap: tone absent, one or two LSB of 24 bits on channels 0 to 3 (-141 dBFS), 0 sequence gaps;
- (b) the same stream on the DUT's link tap: identical;
- (c) the DUT's TDM output on McASP0: identical, and equal to (b) sample for sample, 480,000 of 480,000 frames in both runs;
- (d) the external capture: in the second run a positive control, lane B6's loop on the DUT's own talker, found sample-exact there and on both taps.

So the loss is upstream of the peer's talker, an instrument-side item for the owner. Under the assignment that is a STOP: the playback and routing state was read only, no instrument setting was changed, and no DUT stage, fix or THD+N case was run.

## Validation

At the head, every gate rc 0: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base e8454e27`, `check_doc_paths.py` (pinned Markdown environment), `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`, `git diff --check` and `git diff --check e8454e27 HEAD`.

## #629

Direction B's bench quality metric stays NOT met and #645 stays open, so #629 stays open.
