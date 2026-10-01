[A477] Record #629's bench acceptance: media-clock following graded by THD+N

Refs #629

Bench lane B6, operator [A477], on dev `ec0cc0c1` as installed; one commit, `b5e9242e2e1911bb2bac11221527f8965a4ccaef`, on dev `ea3fb38877842f223afea97e3bd72a10500455c9`.

## What changes

- `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (new): the bench acceptance of #629. It holds the method, the tool controls, the binding rule and clock-source record, the per-case tables of THD+N, SNR, frequency offset and discontinuities, the frame-rate ratio, the capture-path losses, the bench as left, the limits and the artifact hashes.
- `docs/findings/README.md`: its index row.

No other file changes.

## Results

| Case | Blocks at the floor | Listener discontinuities | DUT beat repeats | McASP0 to peer ratio, counted, ppm | Timed, ppm | Result |
|---|---|---|---|---|---|---|
| Tool controls (synthetic) | - | every planted defect found at its frame and size | - | - | - | PASS |
| A0, the reference peer as found (control) | 54 of 629 | 519 drops, 1 silent insert | 321 | +6.519 | +6.44 +-0.72 | PASS as a control |
| A1, the peer follows the DUT's AAF stream | 291 of 617 | 0 | 315 | -10.631 | -12.19 +-2.44 | PASS |
| A2, the peer follows the DUT's CRF stream | 1 of 616 | 494 drops, 180 silent inserts | 316 | -0.068 | -0.59 +-1.24 | FAIL |
| B INTERNAL, the DUT on INTERNAL (control) | 57 of 629 | 506 drops, 1 silent insert | 322 | +6.052 | +6.85 +-1.46 | PASS as a control |
| B CRF, the DUT follows the peer's CRF stream | 611 of 629 | 0 | 0 | 0.000 | -0.01 +-0.65 | PASS |

- Blocks at the floor read THD+N -146.06 dB and SNR 146.07 dB at 997 Hz, and -145.99 dB and 145.99 dB at 9,973 Hz, in every case.
- A2 fails because at INTERNAL the DUT's AAF stream runs on the free-running 48 kHz packet grid, 10.64 ppm off the physical audio clock its CRF talker publishes. A listener that follows the DUT's CRF drops one frame per beat.
- Direction B's THD+N is NOT RUN: the reference peer's talker channels carry 0 to 2 LSB, not a known signal.
- The DUT's AAF following is not in this image.

## Validation

Every gate rc 0 at `b5e9242e`, none piped. The Markdown gates ran in the pinned environment:

- `scripts/docs_check.py`
- `scripts/check_doc_style.py`
- `scripts/gen_toc.py --check`
- `scripts/check_em_dash.py --base ea3fb388`
- `scripts/check_doc_paths.py`
- `scripts/gen_toc.py --verify-anchors`

The others:

- `scripts/ci_scope.py --selftest`
- `scripts/check_baremetal_only.py --check` (the bare invocation is a usage error, as the script needs a mode)
- `scripts/check_baremetal_only.py --selftest`
- `scripts/check_feature_status.py --self-test`
- `git diff --check`
- `git diff --check ea3fb388 HEAD`

## Review notes

- The figures come from the lane packet `b6-a477`: `summary/<case>/grade.json`, `events.csv` and `blocks.csv`, rendered by `tools/b6_tables.py`. The raw captures stay on the bench host, indexed by size and SHA-256.
- The attribution of each discontinuity to the capture path, the DUT's beat or the listener is defined on the page. Each case's `events.csv` holds every event with its evidence.
- The attribution was refined while grading, and each change was applied to every case. Under the rule as first written, A1 and B CRF would fail on 4 and 3 multi-frame events. Each of those lies in a capture-path cluster whose read-time rise matches its loss. The page's Method states the history ("How the attribution was refined").
- The A2 diagnosis rests on the measured rates and on `hdl/milan/milan_datapath.sv:445` and `docs/design/TIME_SYNC.md`. No CRF timestamp was captured on the wire.
- Residuals: DUT NVM commits went from 2 to 8. Two of the reference peer's talker states keep stream parameters with connection count 0.
