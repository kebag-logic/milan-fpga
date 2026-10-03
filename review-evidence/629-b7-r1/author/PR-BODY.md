[A519] Bench lane B7: #629's bench acceptance on dev `bbf704ec`, after PR #634

Refs #629

Adds a dated section, "Dev bbf704ec, 2026-10-03: lane B7", to `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and updates its row in `docs/findings/README.md`. No other file changes.

Head: `4eee41a558a56024e57b27a956fdaf7910ca69dc`, one commit on dev `bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352`.

## What was measured

Lane B6's method, tools and grading rules on the image with #634, with every change stated on the page and fixed before any graded case ran. Each window is 630 s, untouched. The listener's format was adapted before every bind and the talker's never set. Clock sources were set only on the listener's CLOCK_DOMAIN, read back, and restored.

| Case | Talker to listener, the listener follows | Result |
|---|---|---|
| Identity | VERSION `00020060`; AEM image, BIOS ROM and QSPI bitstream payload CRCs equal the build's; every live descriptor byte-equal to the build's AEM image; CLOCK_SOURCE 0 INTERNAL, 1 CRF, 2 the AAF input's INPUT_STREAM source | PASS |
| Tool controls | Synthetic slips and drift | PASS, byte-equal to lane B6's |
| A0 | DUT to peer, the peer on INTERNAL | PASS as a control: net +5.92 ppm of listener drops; the DUT's INTERNAL beat is gone |
| A1 | DUT to peer, the peer follows the DUT's AAF | PASS: 0 listener discontinuities, 0 net steps |
| A2 | DUT to peer, the peer follows the DUT's CRF | PASS: 0 listener discontinuities (lane B6: 494 drops, 180 inserts) |
| B0 | Peer to DUT, the DUT on INTERNAL | PASS as a control: +5.92 ppm counted |
| B-CRF | Peer to DUT, the DUT follows the peer's CRF | PASS: LOCKED 3.1 to 3.6 s after the set and at every read; 0 net steps in 30,169,440 frames |
| B-AAF | Peer to DUT, the DUT follows the peer's AAF (CLOCK_SOURCE 2) | PASS: LOCKED 6.6 to 7.1 s after the set and at every read; 0 net steps in 30,131,520 frames; meter history never restarted, largest deviation 29 ns |
| Lock loss (observation) | Unbind of the followed AAF talker for 11.1 s | As declared: HOLDOVER within 0.56 s, the index kept, one `mr` toggle at the loss and none at the return, LOCKED 6.1 s after the return |
| INTERNAL clock (observation) | Frame-rate ratio against the peer | +5.92 ppm from the peer, about -5.1 ppm against gPTP time; the oscillator grade stays the owner's known risk |
| Direction B THD+N | Known-signal probe repeated | NOT RUN: no known signal on the peer's talker channels |

## #629 acceptance

Judged item by item on the page. Not every item is met, so this PR refers to #629. What stays open:

- the bench quality metric for Direction B: no known signal reaches the peer's talker without a wiring change;
- no bench evidence for a switch between the AAF and CRF streams, a followed CRF stream's lock loss, or the saved selection across a power cycle; simulation covers them.

A2 and B-AAF rest on lane B6's capture-path attribution. Five capture-path clusters are one or two frames off its size signature, and the page states the conservative reading.

## Validation

At `4eee41a5`, every command rc 0:

- `scripts/docs_check.py`, `scripts/check_doc_style.py`, `scripts/gen_toc.py --check`, `scripts/check_em_dash.py --base bbf704ec`, `scripts/check_doc_paths.py` (the pinned Markdown environment)
- `scripts/ci_scope.py --selftest`
- `scripts/check_baremetal_only.py --check` and `--selftest` (the bare invocation is a usage error, rc 2)
- `scripts/check_feature_status.py --self-test`
- `git diff --check`, and `git diff --check bbf704ec HEAD`
- `scripts/gen_toc.py --verify-anchors`

The evidence packet is `629-b7-a519`; the page lists its hashes and the raw files' hashes.
