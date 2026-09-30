[A453] Bench lane B3 on the dev `ec0cc0c1` image: the #617 DIN torn-frame re-run and the #451 capture through the USB Audio device.

Refs #617 (acceptance 4). Refs #451 (capture through the USB Audio device; continuity check). This PR records measurements only; both issues keep their other items.

Commit `6dfa64a7506a8660a70d77eaa7c96c5de2886f5d` on `b3-bench-0930`, one commit on dev `ec0cc0c1`, documentation only:

- `docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md` (new): #617 acceptance 4.
- `docs/findings/451_USB_AUDIO_CAPTURE.md` (new): #451 capture through the USB Audio device, and the continuity check.

No other file changes. The findings index row is not added, because the assignment allowed no other doc edit.

## Verdicts (operator measurements, not review verdicts)

| Item | Verdict | Evidence |
|---|---|---|
| Identity gate | PASS | VERSION `00020060`, AEM CRC `93742dd2`, entity `020000fffe000001`; ENTITY and CONFIGURATION byte-equal to the QSPI AEM bytes; grader 10/10 |
| #617 acceptance 4: 0 torn AAF frames in the #451 DIN capture | PASS | 0 of 3,360,036 playback frames, 0 of 4,551,624 recorded frames (first light: 67.5%) |
| DIN and DOUT slot and channel order | PASS, identity | Every frame, both directions |
| Render path unchanged (DOUT) | PASS | 0 torn, 0 invalid in 3,360,000 frames; first-light discontinuity classes |
| #451 capture through the USB Audio device, order and continuity | FAIL | 0 of 3,600,000 frames pass the pattern rule in each of two 75 s runs; rotating channel order; silent stretches |
| #451 continuity check | NOT RUN | Needs a meter on the unpowered boards |

## Per-run results

| Run | Direction and capture point | Frames | Torn | Invalid words | Order | Discontinuities | Result |
|---|---|---|---|---|---|---|---|
| `din-long` | DIN, DUT talker stream, 70 s playback | 3,360,036 in the region, 4,551,624 recorded | 0 | 0 | Identity | 36 whole-frame repeats, the same frames in all 8 channels, 93,990-93,993 apart; `SLIP_TDM` +36, skips 0 | PASS |
| `dout-long` | DOUT, McASP0 direct, 70 s | 3,360,000 | 0 | 0 | Identity | 36 beat clusters (net one drop each); 23 underrun clusters, 12 after logged talker lateness | PASS |
| `usb-long` | DOUT, USB Audio card through the bridge, 75 s | 3,600,000 | not gradable | 97.4% of words have a non-zero low byte | In order in 9.6% of frames; 2,833 rotation changes | 327,339 silent frames in 2,420 stretches | FAIL |
| `usb-long2` | Same, repeated | 3,600,000 | not gradable | 97.7% | In order in 11.9%; 238 rotation changes | 3,244 silent frames in 4 stretches | FAIL |

The direct McASP0 path is bit-exact on the same image. So the USB-path loss arises between McASP0 receive and the bench host's capture buffer: in the bridge leg, the USB Audio function or the bench host's USB path. The bridge was not changed, and none of the assignment's STOP conditions occurred.

## Restore

Bridge legs running with the recorded command lines (new process IDs). All 18 stream states unbound and both DUT maps empty; the census equals the start in 33 of 33 entries; DUT control words equal. The controller clock frequency reads back as found and is back on its recorded trajectory. The bench lock is free.

Residual: the method's map and bind edits made the DUT persist its saved state. NVM commits went from 0 to 6 (slots 229/230 to 235/236), with `pend=1` and `PP_STAT` bit 11 left set, as first light also recorded.

## Validation at `6dfa64a7`

All rc 0, unpiped, from the physical `/data` lane path; the Markdown gates with the pinned Markdown environment:

- `scripts/docs_check.py`: 0 findings.
- `scripts/check_doc_style.py`.
- `scripts/gen_toc.py --check`.
- `scripts/check_em_dash.py --base ec0cc0c1`: 0 findings over 474 added lines in 2 pages.
- `scripts/check_doc_paths.py`: 860 paths.
- `scripts/ci_scope.py --selftest`.
- `scripts/check_baremetal_only.py --check`.
- `scripts/check_feature_status.py --self-test`: 46/46.
- `git diff --check`, and `git diff --check ec0cc0c1 HEAD`.

Every table in both pages has a constant cell count, rendered and in the source.

## Open questions

1. The findings index (`docs/findings/README.md`) has no row for the two pages; adding them needs a doc edit this lane was not allowed.
2. #451's capture through the USB Audio device fails. Locating the loss needs a change on the SoC board or the bench host, for example a capture with the bridge's rate conversion off. That is outside this lane.
3. #451's playback direction through the USB Audio device was not assigned, and remains NOT RUN.

The lane packet `b3-a453` holds the tools, the redacted per-action evidence, the gate outputs and the raw-artifact index.
