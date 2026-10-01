[R423] NEGATIVE - exact head 35a60c8d6ee742216f98232c85926b435ab01b91

Round R423-1, external independent review of PR #627 (Refs #451, bench lane B4, evidence only). Head `35a60c8d6ee742216f98232c85926b435ab01b91`, tree `6b1aaa3b2867c5cd826d663a22042da0cd1b9dff`, on dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`. Diff: `docs/findings/451_TDM8_TIMING_SOC_BOARD.md` (new, 373 lines) and one row in `docs/findings/README.md`.

The verdict is NEGATIVE because one MINOR finding is open. Every measured figure on the page re-derives from the public packet, and the framing, fs, BCLK, limit, restore and bench-event statements are supported. The one exception is a single summary sentence: it overstates what a one-bit framing offset would do to the checks, and a fault probe falsifies it for one of the two directions. Correcting that sentence is the only change needed for a clean Docs and Tests result at the next head. The three SUGGESTIONs are optional.

## Reconstruction

The context was reconstructed in this order:
1. AGENTS.md and CONTRIBUTING.md (by reference).
2. The #451 issue body and its PocketBeagle 2 amendment (5729936674).
3. The owner decisions 5916029287 and 5924157808.
4. The B4 assignment 5924192573, the TAKEN 5924249315, the two STOPs 5924386279 and 5924930868, the manager ruling 5924950994 and REVIEW READY 5925003925.
5. #626, the oscilloscope version.
6. The PR body.
7. `git diff e4b771f9..35a60c8d` and its three one-line commits.
8. The public packet `review-evidence/b4-r1` at `3247bf45c8e388911153303a0fee74621f93ed45`.

No private author material, lane scratchpad or other reviewer report was read. At the time of reading, the PR had no review objects, no review comments and no prior findings. Its only comments were the two review-start notices. So no earlier finding needs resolving or retaining.

## Findings

### R423-F1 - MINOR - lenses: Docs, Tests

- **Location:** `docs/findings/451_TDM8_TIMING_SOC_BOARD.md:297-298`, the sentence "A one-bit offset either way would break every class of word check."
- **Evidence:** I wrote `probe_bit_offset.py` (receipt `receipts/probe_bit_offset.txt`). It builds the first-light pattern as a TDM8 serial bit stream and models a receiver framing one bit off in each direction, plus a slot rotation, a torn frame and a repeated frame. Each case runs through the packet's own `tools/decode_capture.py` (sha256 `cfb7121b…`).
  - **Data one BCLK late:** every check fires. Channel 0 is invalid in all frames, the other channels are invalid on odd frames, all 4,096 frames are torn, and the tags are wrong.
  - **Data one BCLK early:** the tags double (channels 0 to 3 read 2t), and channels 4 to 7 are invalid in every frame. But **torn = 0**, the low-byte check never fires (channels 0 to 3 have 0 invalid words), and there are 0 zero words.
  - So under data-early, the torn-frame check (the #617 page's headline metric), the low-byte rule and the zero-word count all stay clean. The sentence is false for that direction.
  - The page's precise per-direction statement at lines 151-156 is correct, and the probe confirms it.
  - The PASS itself stands. "0 invalid" alone excludes both offsets (data-early leaves channels 4 to 7 invalid, data-late leaves odd frames invalid), and the tag identity in the channel table excludes a rotation.
- **Impact:** This sentence sits in the section that defines what the SoC board shows, and the manager may close #451 on this page. A later reader could take it to mean that 0 torn or a clean low byte rules out a framing offset by itself. It does not.
- **Required outcome:** The sentence states only what holds. For example: either offset breaks the tag or validity checks, as lines 151-156 detail. Or it names which checks each direction trips. No figure or verdict changes.
- **Verification:** Re-read the corrected lines against `receipts/probe_bit_offset.txt`, then re-run the docs gates at the new head.

### R423-S1 - SUGGESTION - lens: Docs

- **Location:** `docs/findings/451_TDM8_TIMING_SOC_BOARD.md:35`, `:241` and `:300-301`.
- **Issue 1:** The verdict row reads "48 kHz within the SoC board's clock accuracy", and line 300 reads "48 kHz at the board's accuracy". Both attribute the whole -42.8 ppm to the SoC board. That -42.8 ppm includes the plan's designed -10.64 ppm and the DUT oscillator's own error. Line 241 handles this correctly.
- **Issue 2:** Line 241 calls the -32.1 ppm "the sum of both boards' clock errors". In signed terms it is approximately the DUT oscillator error minus the SoC board clock error: a fast SoC clock lowers the measured fs.
- **Note:** #626's "tens of ppm" is unquantified, so neither wording is falsifiable. Tightening is optional.

### R423-S2 - SUGGESTION - lens: Docs

- **Location:** `docs/findings/451_TDM8_TIMING_SOC_BOARD.md:151` and `:296`, "The receiver is set for one bit of data delay".
- **Issue:** The one-bit data delay is the McASP driver's mapping of the device tree's `dsp_a` format. It was not read back from the receive format register, and the assignment forbade that readback. The DT format is recorded in `soc/r2-framing-dt.log`; the delay itself is not observed.
- **Suggestion:** Saying so would make the inference chain explicit. The bit-exact decode corroborates it.

### R423-S3 - SUGGESTION - lens: Docs

- **Location:** `docs/findings/451_TDM8_TIMING_SOC_BOARD.md:15-16` and `:94-97`.
- **Issue:** The page says the owner logged the console in, and that SoC actions other than the capture, bridge legs and TCP test were reads. It does not record two facts that only the public STOP comment 5924930868 states:
  - the root shell was confirmed with `id` (uid 0), as `soc/r2-shell-check.log` shows;
  - no credential was typed or stored.
- **Suggestion:** One sentence would make the page self-contained for a cold reader.

## Focus items, judged against the packet

1. **Identity gate: supported.**
   - `identity/console-identity.txt` shows VERSION `00020060`, CRC32 `93742dd2` (7,352 B), `acad92b9` (53,344 B) and `d178f19a` (3,825,788 B).
   - `grader-identity.txt` shows 10 of 10 PASS, and `summary.json` shows ENTITY (312 B) and CONFIGURATION (106 B) byte-equal to QSPI, entity `020000fffe000001`.
   - These equal the #617 page's identity table. NVM seq differs naturally, and the page's identity table does not list it.
   - The second session's same-boot claim matches `restore/r2-census-compare.txt`: 32 of 33 entries equal, the difference being GET_AVB_INFO propagation delay.
2. **Framing: supported.**
   - `soc/r2-framing-dt.log` shows `simple-audio-card,format` = `dsp_a`, and `bitclock-master` and `frame-master` = phandle 0x41. That is the `simple-audio-card,codec` subnode, whose `sound-dai` 0x43 is `tdm8-codec`; the CPU DAI 0x42 is McASP0.
   - Both DAIs show slot-num 8 and slot-width 0x20. There are no inversion properties.
   - McASP0 shows `op-mode` 0, `tdm-slots` 8, `serial-dir` [1,2,0…] (AXR0 transmits, AXR1 receives, matching the amendment's P2.03 = AXR1 receive) and `rx-num-evt` 32. McASP1 and McASP2 are disabled.
   - `runs/timing-long/soc-capture.log` hw_params show `S32_LE`, 8 channels, 48000 (48000/1), period 2,048, buffer 16,384 and `tstamp_mode` ENABLE. The arecord setup shows `tstamp_type` MONOTONIC.
   - The `decode.json` figures re-checked: 22,831,104 frames = 730,595,328 B / 32, torn 0, silent 0, channel c carries only tag c+1 in every frame, 0 non-pattern words and 0 zero words. The step table sums to frames - 1, with no backward step (`receipts/claims_crosscheck.txt`, 16/16 OK).
   - This supports "data starting one BCLK after the frame-sync edge" as far as the board shows. The probe confirms that either one-bit offset or a slot rotation would fail this decode; see R423-F1 for the one overstated sentence.
   - The page correctly does not claim the FSYNC pulse width (lines 38 and 306). The receiver detects the edge only, which #626 also states.
3. **fs: re-derived exactly** by my own parser (`rederive_fs.py`, `receipts/rederive_fs.json`), not the packet's tool.
   - The log holds 143 status blocks: 95 RUNNING and 48 XRUN. All 95 RUNNING samples share trigger 68,038.252028915.
   - The window is 472.467704 s and 22,677,480 frames. Endpoint fs is 47,997.9474 Hz and least-squares fs is 47,997.9464 Hz.
   - That is -42.763 ppm against 48 kHz. The plan's fs is 24,575,738.529 / 512 = 47,999.4893 Hz (-10.639 ppm), and the measurement sits -32.124 ppm from it.
   - The hw_ptr step GCD is 4. Residuals are 25.71 us rms and 52.87 us max. The endpoint residuals (-1.645 and -1.171 frames) give ±0.124 ppm, and one step at each end gives ±0.353 ppm. My own bound of twice the maximum residual gives ±0.224 ppm, inside the stated worst case.
   - The uptime cross-check gives 47,997.714 Hz against a ±42.3 ppm resolution.
   - The clocksource is `arch_sys_counter` at 200 MHz (`soc/r2-tcp-test.log`). phc2sys logged only "Waiting for ptp4l" (`soc/r2-framing-dt.log`, count of other lines 0). The system clock was never set ("Jan 1").
   - The crystal tolerance is explicitly excluded (lines 232-234). The comparisons with 48 kHz and with the plan are stated with their limits (lines 239-242 and 300-301; see S1 for wording).
   - The DUT-side SLIP_TDM figure (395 duplicates in 774.27 s, 0.5102 per second, 10.63 ppm) is correct, and the page correctly labels it a DUT comparison.
4. **BCLK: supported as inferred, not measured** (lines 36, 244-247 and 302-303). 256 × 47,997.946 Hz gives 12,287,474 Hz.
   - At this head and at `ec0cc0c1` (an ancestor; `KL_tdm_capture_master.sv` is unchanged between them), the RTL basis is `hdl/ieee1722/aaf/KL_tdm_capture_master.sv:203` and `:298`. There, `FRAME_C = SLOTS_P*WORD_BITS_P` and `fpos_r` wraps at `FRAME_C-1` with no idle bit clocks.
   - FSYNC is a one-BCLK pulse at `fpos_r == 0` (`:299`), with `DATA_DELAY_P (1'b1)` at both shipping instantiations (`hdl/milan/milan_datapath.sv:1012` and `:1057`).
   - This shape is graded by the existing suite `tb/verilator/tdm` (cap M3, SLOTS_P=8, BCLK_HALF_P=1, FSYNC gap and width checks in `sim_main.cpp:91-138`).
5. **Capture length: matches the ruling.** Line 37 reads "475.6 s (ruled sufficient by the manager, 5924930868 and 5924950994)", as ruling item 1 requires. Received: 730,595,328 B, 475.648 s at 48 kHz, sha256 `dd201b3a…` equal in `decode.json`, `events.jsonl` and `summary.json`. The largest arrival gap is 50.4 ms, with 0 gaps of 100 ms or more.
6. **Limits: present and pointed to #626.** Lines 38 and 304-310 name the FSYNC width, edge timing (setup, hold, duty, rise and fall), levels, overshoot and ringing, and absolute frequency. This matches #626's own list and acceptance.
7. **Restore, bench events and read-only: supported.**
   - **Timeline.** Trigger at uptime 68,038.252 s. The last RUNNING sample is 475.480 s after the trigger and 0.238 s before the dwc3 "remote wakeup not configured" line at 68,513.970 s, which is 475.718 s after the trigger. XRUN follows 0.420 s later, at 68,514.390 s. The "remote wakeup" line also appears at 667 s and 26,028 s of uptime.
   - **Arrival times.** First bytes arrived at 04:17:05.207Z and last bytes at 04:25:00.820Z. Mapped through the trigger, the wakeup line falls at about 04:25:00.92Z, ahead of the bench host's xHCI line at 04:25:01.084Z and the disconnect at 04:25:01.085Z (`soc/r2-end-host-view.txt`).
   - **Contiguous prefix.** The received frames (22,831,104) lie between the last RUNNING hw_ptr (22,822,044) and the final appl_ptr (22,837,248). One trigger and avail_max ≤ 2,048 show no overrun before the event, so the received bytes are a contiguous prefix.
   - **Commands sent.** Every command line in the `soc/r2-*.log` files and the capture log is a read, the capture, the TCP test, the bridge-leg stop and restart by checked PID, or the recorder's termination by checked command line. The doubled characters in the echoed commands are console echo; the outputs (for example `STARTED`) confirm the commands as sent.
   - **No devmem, no writes.** The only `devmem` string in the packet is busybox's applet list (`soc/r2-framing-discover.log`). There are no `/sys` or `/proc` writes. `soc/r2-shell-check.log` sent only `id` and `tty` (uid 0, /dev/ttyS3), and no credential appears.
   - **Restore.** Bridge legs 1265 and 1266 run with the recorded lines. card0 capture is RUNNING and playback is XRUN, as at the start. UDC is configured, BAD=0 and taint 0.
   - **Controller restore** (`restore/r2-controller-restore.txt`): frequency offset 0 ppb, residual 4,547 ns from the recorded trajectory, tx_type 0 and rx_filter 0.
   - **DUT restore.** Maps were removed and unbound. The census matches 31 of 33, and the DUT and peer differences are disclosed. The `ctl-*.jsonl` files show bind, map and unbind commands addressed to the DUT only.
   - **Residuals.** NVM commits 0 to 2, seq 237 and 238, `pend=1` and `PP_STAT` bit 11 (`restore/r2-dut-compare.txt`). SLIP_LB reads `ffffffff`, and the render rail count is 0x1878 = 6,264.
8. **Meets the #451 timing item to the extent the owner accepted: yes in substance.**
   - Every element the assignment and the ruling require is present: identity, framing record and decode, fs with uncertainty, BCLK inferred, the ruled length, the limits handed to #626, restore and hashes.
   - Once R423-F1 is corrected, the page supports the manager closing #451's timing item.
   - The PR says `Refs #451`, so a merge will not close #451. Closing it by hand is the manager's act.

**Publication safety.** The page and the index row use neutral roles (DUT, SoC board, controller host, bench host, reference peer). They contain no host, peer, switch or instrument names, no addresses, and no wiring or instrument topology. The packet's own placeholders (`<ecm-host>`, `<bench-host>`) are redactions. The packet `MANIFEST.sha256` matches every file except `gates/gates.txt` and `identity/controller-preflight.txt`, which the archive's `MANIFEST.json` discloses as path-redacted. All 124 published hashes verify, and all 11 evidence hashes the page cites match (`receipts/page-evidence-hashes.txt`).

## Clean-lens evidence (format: lens, artifact, what was checked)

- `[R423] PASS Conformance` — `docs/findings/451_TDM8_TIMING_SOC_BOARD.md:30-38` and the per-run tables at `:163-219`, against the assignment 5924192573 steps 1-5, the ruling 5924950994 items 1-3, #626 and the packet files named in items 1-8. Every required element is present, and every figure re-derives (`receipts/rederive_fs.json`, `receipts/claims_crosscheck.txt`).
- `[R423] PASS RTL` — `hdl/ieee1722/aaf/KL_tdm_capture_master.sv:203,289-302`, `hdl/milan/milan_datapath.sv:1008-1012,1053-1057`, `docs/litex/CLOCK_DOMAINS.md` Audio variants (Plan A 24,575,738.529 Hz, TDM8 32-bit slots) and `tb/verilator/tdm/tdm_wrap.sv` cap M3. The page's RTL-dependent statements (256 BCLK per frame with no idle bits, one-BCLK FSYNC by design, data delay 1, plan -10.64 ppm) match the HDL unchanged since `ec0cc0c1`. The page does not claim more than inference. No RTL is in the diff.
- `[R423] PASS Robustness` — `soc-capture.log` (143 blocks, XRUN tail, single trigger), `soc/r2-after-stall.log`, `events.jsonl` (rc 124, upload gaps) and `decode_capture.py:24` (truncated input fails closed). The capture's partial-end and failure path is handled correctly: a contiguous TCP prefix, an fs window ending before the event, the last residual inside the fit's rms, and XRUN samples excluded. The recorder's termination was guarded by its command line. The STOP was taken rather than any USB action.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Page `:4-38,125-310`; issue body and 5729936674, 5924192573, 5924950994, #626; packet identity, soc, runs and restore files; `receipts/rederive_fs.json`, `receipts/claims_crosscheck.txt` | R423-1 | `35a60c8d6ee742216f98232c85926b435ab01b91` |
| RTL | CLEAN | `KL_tdm_capture_master.sv:203,289-302`; `milan_datapath.sv:1008-1057`; `CLOCK_DOMAINS.md` Audio variants; `tb/verilator/tdm` cap M3 (static) | R423-1 | `35a60c8d6ee742216f98232c85926b435ab01b91` |
| Robustness | CLEAN | `soc-capture.log` XRUN tail and trigger; `r2-after-stall.log`; `r2-arecord-stop*.log`; `events.jsonl`; `decode_capture.py`; `fit_fs.py` | R423-1 | `35a60c8d6ee742216f98232c85926b435ab01b91` |
| Tests | UNCLEAN (R423-F1) | `tools/decode_capture.py`, `tools/fit_fs.py`; `receipts/probe_bit_offset.txt` (offset, rotation, torn and repeat probes); independent `rederive_fs.py` | R423-1 | `35a60c8d6ee742216f98232c85926b435ab01b91` |
| Docs | UNCLEAN (R423-F1) | Page (all 373 lines), README index row; docs gates with the pinned renderer (`receipts/docs-gates-pinned.txt`: docs_check, doc_style, gen_toc `--check` and `--verify-anchors`, em_dash `--base e4b771f9`, doc_paths, all rc 0); `receipts/table_cells.txt` (13 tables, constant cells); privacy scan | R423-1 | `35a60c8d6ee742216f98232c85926b435ab01b91` |

## Real limits

- The 730.6 MB raw capture is not public. The decode could not be re-run on the raw bytes. It was verified through `decode.json`, the decoder's logic and the synthetic fault probe, and the raw sha256 is consistent across three packet files.
- The designated pinned simulator path (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host. No unverified substitute was used, so no simulation ran. The RTL lens rests on static reading of the HDL and the existing `tb/verilator/tdm` checks, which the manager's native bank runs.
- The one-bit receive data delay is the driver's `dsp_a` mapping. No register readback exists, by design of the assignment.
- The crystal tolerance ("tens of ppm") is unquantified anywhere in public material.
- Lane B3's "SLIP_LB about 70 per second" (line 330) was not verified. The #617 page does not state it.
- No bench, hardware, or hosted or act runs were made by this reviewer. Docs gates ran in a disposable environment with the repository's hash-pinned Markdown renderer (`tools/markdown/requirements.txt`).
- The clone was restored and verified byte-exact (`receipts/clone-integrity.txt`):
  - HEAD, tree and write-tree all equal `6b1aaa3b…`;
  - the index is identical to the tree, with 0 status lines;
  - the gitlinks for gptp-processor, protocol-processor and verilog-axis are checked out at their recorded commits, and `external` is uninitialized at its recorded gitlink.

## Pending manager duties

- Hosted state at snapshot (`receipts/hosted-checks-snapshot.txt`):
  - `docs-check` IN_PROGRESS;
  - `rtl-fast`, `elaborate`, `changes`, `full-ci-gate`, `wire-accountability`, `bdd-conformance` and `docs-check-no-git` SUCCESS;
  - `verilator-suites`, `verilator-lint`, the Verilator and Yosys shards, `yosys-elaboration`, `yosys-portability` and physical gPTP SKIPPED. Skipped contexts are not executed evidence.
  - Hosted and act acceptance are the manager's.
- Build and validate the final current-dev candidate at the merge turn.
- The second independent review (R422-1) is in flight. The completion ledger needs both reviews' lens coverage at the merge-candidate head, after R423-F1 is fixed and re-reviewed.
- #451 is `Refs` only, so closing the timing item and moving #451 to Done is a manual manager act after merge.
- Owner items outside this PR:
  - re-attach the SoC board's USB function;
  - decide whether the 1,016 unmatched discontinuity clusters get their own issue.

R423-1 FINISHED
