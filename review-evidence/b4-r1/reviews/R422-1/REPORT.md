[R422] NEGATIVE - exact head 35a60c8d6ee742216f98232c85926b435ab01b91

Round R422-1. Internal independent review of PR #627 (Refs #451, bench lane B4, evidence only), tree `6b1aaa3b2867c5cd826d663a22042da0cd1b9dff`, on dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`. The diff is two documentation files: `docs/findings/451_TDM8_TIMING_SOC_BOARD.md` (new, 373 lines) and one row in `docs/findings/README.md`. All five lenses were applied. Two MINOR findings are open, so Conformance and Docs are not covered clean, and the verdict is NEGATIVE. RTL, Robustness and Tests are clean at this head.

The measurement holds up. I re-derived every figure the #451 timing item rests on from the published packet, and each one matches the page: identity, framing, the bit-exact decode, fs, the inferred BCLK, the limits and the restore. Both findings are about wording. Each needs a one-line page edit, and neither changes a measured figure.

## Reconstruction

These are the authorities, read in this order:

- AGENTS.md and CONTRIBUTING.md (sections 4 and 6).
- docs/README and the findings index.
- The #451 issue body, the PocketBeagle 2 amendment (issue comment 5729936674) and the owner decisions 5916029287 and 5924157808.
- The B4 assignment 5924192573, which sets the frozen scope: identity gate; framing from the SoC board's DT and `hw_params`; a bit-exact decode as the data-delay evidence; fs and BCLK = 256 x fs with the uncertainty stated; naming what cannot be shown, pointing to #626; restore; read-only, with no devmem or register writes.
- The STOP comments 5924386279 and 5924930868, the manager ruling 5924950994 (475.6 s accepted; the 10 minutes were the manager's margin; the USB loss is a bench event) and REVIEW READY 5925003925.
- #626.
- `docs/litex/CLOCK_DOMAINS.md` Audio variants, and the RTL contract in `hdl/ieee1722/aaf/KL_tdm_capture_master.sv` and `hdl/milan/milan_datapath.sv`.
- `docs/reference/REGISTER_MAP.md` `SLIP_TDM`.

The diff is `e4b771f9..35a60c8d`: three commits, all docs-only. The evidence is the published packet at `3247bf45c8e388911153303a0fee74621f93ed45:review-evidence/b4-r1`.

## Findings

### F1: MINOR (Docs): `docs/findings/451_TDM8_TIMING_SOC_BOARD.md:114`, the full-length recording size is wrong

- **Authority/evidence:** The capture was set to `-d 630` (`runs/timing-long/soc-capture.log`, command line). The page's own rate is 1.536 MB/s (line 285; 8 x 4 B x 48,000). At full length that gives 630 s x 1.536 MB/s = 967.68 MB. The page says "The recording, 921.6 MB at full length". 921.6 MB is 600 s, the 10-minute figure from the first STOP comment, not the 630 s capture the sentence describes. See `receipts/page-arith.txt` (`full_630s_MB: 967.68`).
- **Impact:** A durable findings page states a wrong figure. The conclusion that the recording exceeds the 209,564 KiB `/tmp` still holds.
- **Required outcome:** The stated size matches the 630 s capture (about 967.7 MB), or the sentence names the duration its figure is for.
- **Verification:** Re-run `scripts/page_arith.py` and compare it with the page line. Re-run the docs gates.

### F2: MINOR (Conformance, Docs): `docs/findings/451_TDM8_TIMING_SOC_BOARD.md:35` and `:300`, the "48 kHz within the SoC board's clock accuracy" verdict is not supported

- **Authority/evidence:** The B4 assignment asks for fs "with the uncertainty stated (the board's crystal tolerance and the timing granularity)". The page measures fs = 47,997.947 Hz, -42.8 ppm from 48 kHz. I reproduced this in `receipts/fs-recompute.json`.
  - The page gives the SoC board crystal only as "tens of ppm" (from #626). It states that this tolerance "is not included above" (lines 232-234).
  - It also states that the -32.1 ppm against the plan "is the sum of both boards' clock errors. This lane has no reference that splits it" (lines 239-241).
  - Yet the verdict cell at line 35 reads "48 kHz within the SoC board's clock accuracy", and line 300 reads "It is 48 kHz at the board's accuracy".
  - 48,000 Hz lies inside 47,997.947 Hz x (1 +- tol) only if tol >= 42.8 ppm. Neither the page nor the packet establishes that figure for the SoC board's clock. The page's own analysis also puts part of the offset on the DUT side, not on the SoC board alone.
  - The index row (`docs/findings/README.md:12`) and the PR body's verdict make no such claim. They read "fs 47,997.947 Hz on the SoC board's clock". The manager ruling 5924950994 likewise keeps "fs 47,997.947 Hz on the board clock".
- **Impact:** The manager closes #451 on this page. Its FSYNC-at-48-kHz verdict reads as established to the SoC board's clock accuracy. In fact it rests on an unquantified bound and contradicts the page's own two-board attribution.
- **Required outcome:** The verdict cell and the fs bullet under "What the SoC board can and cannot show" claim only what the evidence carries. One option: fs is -42.8 ppm from 48 kHz on an uncalibrated clock. -10.64 ppm of that is the plan, and the remaining -32.1 ppm is the two boards' combined, unsplit clock error. That is the planned 48 kHz-family rate and divider, since a wrong divider, slot count or rate family would sit hundreds of ppm away. The other option is to cite an authority giving the SoC board clock a tolerance of at least 42.8 ppm. Either way, absolute ppm stays with #626.
- **Verification:** Re-read lines 35 and 299-301 against the Frequencies section and the ruling. Re-run the docs gates.

### S1: SUGGESTION (Docs): `docs/findings/451_TDM8_TIMING_SOC_BOARD.md:58-60`

"Every value equals that page's" is not literally true. The #617 page's identity readback includes NVM "Slot B seq 230 authoritative", and this run reads seq 236. Every value in this page's identity table does equal its #617 counterpart. "Every identity value" would be exact.

### S2: SUGGESTION (Docs): `docs/findings/451_TDM8_TIMING_SOC_BOARD.md:330-331`

"The talker also ended about 55 s before the unbind" does not match the packet. The talker's own `end` record (`runs/timing-long/controller-logs.txt`, t = 1790828918.128) is 58.7 s before the `unbind` event (`events.jsonl`, t = 1790828976.783). This is a residual narrative only.

No prior public review findings exist on PR #627 (no reviews, no review comments; the one PR comment is the round-start notice), and none on #451 for this lane. There is nothing to resolve or retain.

## Per-lens results, with evidence

[R422] UNCLEAN Conformance - `docs/findings/451_TDM8_TIMING_SOC_BOARD.md` at 35a60c8d against assignment 5924192573, ruling 5924950994, #451 recipe item, PocketBeagle 2 amendment, #626 - F2 open. Everything else was checked and holds:

- **(1) Identity gate.** `identity/console-identity.txt`, `identity-aecp-comparison.txt` and `grader-identity.txt` give VERSION 00020060, AEM CRC 93742dd2 over 7,352 B, ROM acad92b9, QSPI d178f19a, ENTITY 312 B and CONFIGURATION 106 B byte-equal, entity 020000fffe000001, grader 10/10. These equal the #617 page's identity rows.
  - The second session ran on the same DUT boot. `restore/dut-end.txt` against `dut-r2-start.txt` shows only TAI, live counters and the propagation delay moving. The census matches 32 of 33 (`r2-census-compare.txt`).
- **(2) Framing.** `soc/r2-framing-dt.log` shows `simple-audio-card`, format `dsp_a`, and `bitclock-master` and `frame-master` = phandle 0x41. That is the `codec` subnode, whose `sound-dai` 0x43 is `tdm8-codec`. The CPU DAI 0x42 is McASP0. Slots are 8 x 32 on both DAIs, and there is no inversion property. `op-mode` is 0, `tdm-slots` 8, `serial-dir` AXR0 = 1 (TX) and AXR1 = 2 (RX), `rx-num-evt` and `tx-num-evt` 32. McASP1 and McASP2 are disabled.
  - `hw_params`, `sw_params` and `arecord -v` in `soc-capture.log` and `r2-after-stall.log` give S32_LE, 8 channels, 48000/1, period 2,048, buffer 16,384, tstamp ENABLE and MONOTONIC.
  - `decode.json` covers 22,831,104 frames (730,595,328 B = frames x 32; SHA equals the page's raw hash). Each channel c carries only tag c+1 on every frame, with 0 invalid, 0 zero, 0 torn and 0 silent words or frames. The ordinal steps sum to frames - 1 (`receipts/decode-check.json`).
  - This supports "data one BCLK after the frame-sync edge" as far as McASP shows it. The `shift_probe.py` probe shows the decode refuses a one-bit offset either way and a slot rotation.
  - The page explicitly does not claim the FSYNC pulse width (lines 38, 306).
- **(3) fs.** I re-derived fs independently from the 95 RUNNING status samples, which share one trigger: 22,677,480 frames over 472.46770409 s gives 47,997.9474 Hz (endpoints) and 47,997.9464 Hz (least squares). That is -42.763 ppm against 48 kHz and -32.124 ppm against the plan's 47,999.4893 Hz. The plan figure is 24,575,738.53 / 2 / 256, per `CLOCK_DOMAINS.md:119`.
  - Granularity: the endpoint residuals of -1.64 and -1.17 frames give +-0.006 Hz (+-0.124 ppm). One 4-frame step at each end gives +-0.353 ppm.
  - The uptime cross-check gives 47,997.714 Hz, inside its +-42 ppm resolution.
  - The exclusion of the crystal tolerance is stated (lines 232-234). Nothing steers CLOCK_MONOTONIC: the boot-started clock-synchronization process is still only waiting for a gPTP daemon in the retained log, with 0 other lines, and no gPTP or NTP daemon is in the process list (`r2-framing-dt.log`, `r2-framing-discover.log`).
  - All of this matches `fit-fs.json` exactly. The only open point is the 48 kHz verdict wording (F2).
- **(4) BCLK.** It is stated as inferred and not measured: 256 x fs = 12,287,474 Hz (lines 36, 244-247, 302). The probe confirms that an idle bit clock per frame still decodes bit-exact, so the decode bounds BCLK only from below, as the page says.
- **(5) Length row.** It reads "475.6 s (ruled sufficient by the manager, 5924930868 and 5924950994)", worded as the ruling's item 1 requires, and the intro carries the ruling's reason.
- **(6) Limits.** FSYNC width, edge timing (setup and hold, duty, rise and fall), levels and integrity, and absolute frequency are all pointed to #626 (lines 304-310). This matches #626's own list.
- **(8) Closing #451.** Apart from F2's wording, the page meets the #451 timing item to the extent the owner accepted, measured on the SoC board with the oscilloscope version left to #626.

[R422] PASS RTL - `hdl/ieee1722/aaf/KL_tdm_capture_master.sv:46-50,138-145` and `hdl/milan/milan_datapath.sv:1012,1057,1092` at 35a60c8d, against the page's lines 151-156 and 244-247 - The diff touches no RTL, so I checked the page's RTL premises against the shipping RTL:

- BCLK = SLOTS_P x WORD_BITS_P x fs, and the frame position wraps modulo SLOTS_P*WORD_BITS_P, so there are no idle bit clocks. This is the premise of "256 x fs".
- FSYNC is a one-BCLK pulse at slot 0, launched on the BCLK fall.
- DATA_DELAY_P = 1'b1 on every shipping instantiation, which is the `dsp_a` shape.
- `docs/litex/CLOCK_DOMAINS.md:117-135` gives the plan figure and the TDM8 geometry the page links.

All of this is consistent with the page, and I found no module or interface contract change.

[R422] PASS Robustness - `runs/timing-long/soc-capture.log`, `events.jsonl`, `soc/r2-after-stall.log`, `soc/r2-arecord-stop.log`, `soc/r2-arecord-stop2.log`, `soc/r2-end-health.log`, `soc/r2-start-health.log`, the `restore/*` files and `tools/decode_capture.py` at packet 3247bf45 - I checked the failure and boundary paths the page relies on:

- **Truncated capture.** The decode covers every received byte. TCP gives an in-order prefix, `bytes % 32 == 0` is asserted by the decoder, there are 0 gaps of 100 ms or more, and the maximum gap is 50.4 ms.
- **No loss before the event.** All 95 RUNNING samples share one trigger. `avail_max` is at most 2,048 of 16,384 in every 5 s interval, and the status read resets `avail_max`, so this covers the whole run. `arecord`'s stderr has no overrun line.
- **XRUN after the event.** XRUN arrives 0.420 s after the event at uptime 68,514.390, with hw_ptr 22,853,632 and appl_ptr 22,837,248, both past the 22,831,104 frames received.
- **fs window.** It ends 0.238 s before the event. The last residual is -1.17 frames against 1.234 frames rms.
- **Recorder stop.** The blocked recorder was ended by PID only after an exact command-line check (first SIGTERM caught, second ended it).
- **Bridge legs.** They were stopped by PID after a command-line and status check, and restarted with the recorded lines.
- **End state.** PCM states equal the start (card0 capture RUNNING, card0 playback XRUN, card1 both RUNNING). `/tmp` lists the same entries, UDC is configured, BAD=0 and taint is 0.
- **Read-only SoC board.** Every console command line was enumerated. There is no devmem, i2c write, sysfs or procfs write, reboot or module change. The only writes are the recorder's stderr file (removed), the bridge script's pid files on restart, the TCP stream and one TCP test line.
- **Root shell.** It was confirmed by `id` (uid 0, `r2-shell-check.log`), with no credential in any log.
- **Controller.** NIC clock at 0 ppb, back on its recorded trajectory with a 4,547 ns residual. Timestamping is back to tx_type 0 and rx_filter 0, and staging was removed (`restore/r2-controller-restore.txt`, `r2-controller-cleanup.txt`).
- **Residuals.** NVM persistence and `SLIP_LB` saturation are disclosed.
- **Bench events.** The USB loss timeline matches `soc/r2-end-host-view.txt`: host controller warning at 04:25:01.084Z, disconnect at .085, mapped wake line at about .924. The bench host's absent USB function is recorded as an owner item.
- **Privacy.** No private host, peer, switch or instrument name, and no wiring or instrument topology, appears in the page or the index row.

[R422] PASS Tests - `review-evidence/b4-r1/author/tools/decode_capture.py`, `tools/fit_fs.py` output `runs/timing-long/fit-fs.json`, and this round's `scripts/shift_probe.py`, `scripts/recompute_fs.py`, `scripts/check_decode.py` and `scripts/verify_packet.py` - The PR adds no executable test. Its evidence rests on the packet's decoder and fs fit, so I checked that each can fail:

- **Decoder mutation probe** (`receipts/shift-probe.txt`, PROBE AS_EXPECTED). A synthesized TDM8 line run through the packet's own decoder gives:

  | Case | Result |
  |---|---|
  | Correct one-BCLK delay | PASS |
  | Data one bit early | REFUSED: 16,384 invalid words; channels 0 to 3 read tags 2, 4, 6, 8 |
  | Data one bit late | REFUSED: 4,096 torn frames, 18,432 invalid words, the odd-frame low byte as the page predicts |
  | One-slot rotation | REFUSED: tags shifted |
  | One idle BCLK per frame | PASS, which confirms the page's statement that BCLK is inferred |

- **fs.** My parser, written without the packet's fit tool, reproduces every `fit-fs.json` field (`receipts/fs-recompute.json`).
- **Decode and attribution records** are internally consistent, including the partition 189 + 16 + 1,016 = 1,221 clusters, 838 at 22,000 to 26,000 frames, and 816 with jumps of 5, 5 and 8 to 12 (`receipts/decode-check.json`).
- **Hashes.** The archive manifest has 124/124 published hashes equal. The author manifest has 121 equal, plus the 2 that differ only by the archive's recorded redaction (original hash equal). All 11 page evidence-file rows match bytes and SHA-256 (`receipts/packet-verify.txt`).

[R422] UNCLEAN Docs - `docs/findings/451_TDM8_TIMING_SOC_BOARD.md` and `docs/findings/README.md:12` at 35a60c8d - F1 and F2 are open, and S1 and S2 are optional. The focused docs gates all returned rc 0 at the exact head in the pinned Markdown environment (`receipts/gates.txt`):

- `docs_check.py`: 0 findings.
- `check_doc_style.py`: OK.
- `gen_toc.py --check` and `--verify-anchors`: 283 links.
- `check_em_dash.py --base e4b771f9`: 0 over 374 added lines.
- `check_doc_paths.py`: 861 paths.
- `git diff --check e4b771f9 HEAD`: clean.

The index row follows the page and the ruling, and it carries the owning issue, candidate, boundary and raw artifact identity that the findings README asks for. The page's links to the ruling, the STOP comment and #626, and its `CLOCK_DOMAINS.md#audio-variants` anchors, resolve.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | Page lines 1-373 against assignment 5924192573, ruling 5924950994, #451 body and amendment, #626; packet identity, soc, runs and restore files | R422-1 | 35a60c8d6ee742216f98232c85926b435ab01b91 |
| RTL | CLEAN | `KL_tdm_capture_master.sv:46-50,138-145`; `milan_datapath.sv:1012,1057,1092`; `CLOCK_DOMAINS.md:110-140`; diff has no RTL | R422-1 | 35a60c8d6ee742216f98232c85926b435ab01b91 |
| Robustness | CLEAN | `soc-capture.log`, `events.jsonl`, `soc/r2-*.log`, `restore/*`, `decode_capture.py` frame assertion, SoC command enumeration | R422-1 | 35a60c8d6ee742216f98232c85926b435ab01b91 |
| Tests | CLEAN | Packet decoder under `shift_probe.py`; independent fs re-derivation; decode and attribution cross-check; manifest and page-hash verification | R422-1 | 35a60c8d6ee742216f98232c85926b435ab01b91 |
| Docs | UNCLEAN (F1, F2) | Page and index row; focused docs gates at head | R422-1 | 35a60c8d6ee742216f98232c85926b435ab01b91 |

Every lens examined the new findings page, so any later commit that edits the page un-covers all five lenses under AGENTS section 7. That includes a fix for F1 or F2. They must be covered again at the new head, at least as a confirmation that only the wording changed.

## Real limits

- The 730,595,328 B raw capture is held off the packet, so I did not re-decode it. The decode figures come from the packet's `decode.json`, whose recorded SHA-256 equals the page's raw hash, plus its internal consistency and the decoder mutation probe.
- The 8,330 late-PDU count and the median of 18 repeats per unexplained cluster cannot be re-derived from the published packet: per-cluster detail is in the raw `attribution.json`, outside the packet. Both are outside the timing item.
- The McASP data delay is shown from the DT format, the driver's `dsp_a` semantics and the bit-exact decode. No register read was allowed or made.
- I had no bench, instrument or hardware access. Physical calibration was NOT RUN, and nothing here is pin-level proof. FSYNC width, edges, levels and absolute ppm remain #626.
- I ran no full parent, PP, gPTP, Yosys or builder bank. RTL simulation was not needed for this docs-only diff, and none was run.

## Pending manager duties

- Hosted snapshot (`receipts/hosted-checks-snapshot.txt`): `rtl-fast` passed and `docs-check` was pending. The long Verilator and Yosys contexts were skipping, which is not executed evidence. Hosted and act acceptance stays with the manager.
- Candidate-merge validation against the live dev tip at the merge turn.
- The second independent review.
- After F1 and F2 are fixed, a re-review at the new head covering all five lenses.
- Owner items carried by the PR:
  - re-attaching the SoC board's USB function on the bench host;
  - whether the 1,016 unexplained whole-frame discontinuity clusters (against 59 in the #617 run, with `SLIP_LB` about 340/s against about 70/s) get their own issue;
  - closing #451 once the page is clean, with #626 holding the oscilloscope version.

R422-1 FINISHED
