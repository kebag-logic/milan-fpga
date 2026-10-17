[R635] NEGATIVE - exact head 867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b

R635-1, external independent review of issue #117 / PR #758. All five lenses were applied. Two MAJOR and two MINOR findings remain open. The continuity recordings reproduce the reported measurements, including an independent comparison of every Direction B slot word. The release-row PASS still overstates the restart evidence, and the published grader has reproducible defects.

Scope and reconstruction

Tree: `a5f405e02461121570f89d27955e245269ed87d2`. Source base: `4a9b5a2a74fe793a637745fd3ccf51ad2eaf93b4`. Three commits add 622 lines to `docs/findings/117_AUDIO_CONTINUITY.md` only. No RTL, firmware, configuration, source comments or submodule pins change. The source-comment rule has no new repository source-comment instance; lane labels in this findings page are permitted.

I reconstructed the task from AGENTS/CONTRIBUTING, docs/README, [issue #117](https://github.com/kebag-logic/milan-fpga/issues/117) and public scope decisions, then the authorities, diff/history and executable evidence. Authorities include [the B21 assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6208207821), [the inherited restart requirement](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5925737609), REQUIREMENTS.md section 8, TIME_SYNC.md's talker capture handoff, REGISTER_MAP.md's slip/render definitions, and the #451/#617 method pages. The supplied owner decision makes direct SoC McASP capture authoritative and host USB capture a cross-check. The failed USB self-test does not prohibit that authorized capture path.

Evidence is pinned at [a4352980, review-evidence/117-b21-r1](https://github.com/kebag-logic/milan-fpga/tree/a43529800735820f1662690e4457bf9a6ece27e4/review-evidence/117-b21-r1). `author/` paths below are relative to that packet. Public tools, measurements and gate receipts were examined; private handoffs, lane scratchpads and other reviewers' reports were not used. The independent verdict and ledger were written to `REPORT.independent.md` before checking prior public findings. That check found zero submitted reviews, zero inline comments and only two review-start notices. There are no prior PR findings to resolve or retain; `prior-findings-check.json` records this.

Findings

**R635-1-F1 — MAJOR — Conformance, Tests, Docs**

Artifact: `docs/findings/117_AUDIO_CONTINUITY.md:865`, `:866`, `:1057`, `:1065`, `:1071`; `author/tools/b21_restart.py`; `author/r3/summary/rA-restart.json`; PR status/restart table.

Authority/evidence: The inherited assignment requires rebind-to-first-valid-sample timing; B21 requires restarts below one second. The page clears that row using CONNECT_RX_RESPONSE-to-first-AAF times. The output estimate excludes an unmeasured steady wire-to-output latency. Raw replay reproduces 20 wire times of 13.447–86.795 ms and output estimates excluding latency of 23.475–97.794 ms. The equation is `output restart = wire restart + S/48000 - G + L`; `L` was neither measured nor bounded. Starting at the response also excludes the preceding command duration.

Impact: A constant output latency above 902.206 ms makes the slowest cycle exceed one second while leaving every reported relative figure unchanged. This is an observability counterexample, not an allegation that the hardware has that delay. The release-blocking row is not established by this evidence.

Required outcome: Preserve the wire/relative-output results, but withhold the end-to-end restart PASS until the required events share a defensible time basis, including absolute latency or a conservative bound and uncertainty. A different acceptance endpoint requires an explicit public scope decision; listing the omitted latency as a limit does not satisfy the current criterion.

Verification: Publish a mechanically evaluated table for all 20 cycles from rebind to valid output. Deliberately excessive output latency must fail the one-second test. Update the page and PR acceptance claims consistently.

**R635-1-F2 — MAJOR — Conformance, Robustness, Tests, Docs**

Artifact: `author/tools/b21_grade.py:184`, `:215`, `:234`, `:237`; `docs/findings/117_AUDIO_CONTINUITY.md:1021` and `:1024`; `probe-results.json`, case `unequal_words_same_hash`.

Authority/evidence: The criterion and page claim exact equality of all 32 bits in four slots. The grader reduces each 128-bit frame to a 64-bit multiply/XOR key. Alignment confirmation and continuing matches compare keys without comparing original words. The probe changes one frame from `[0, 0, 0, 0]` to `[0, 0, 256, 256000768]`. Both keys are zero and both frames retain zero low padding bytes. The unmodified grader reports all 1,400 frames matched, zero foreign frames and zero offset changes, just as for the clean control.

Impact: Changed words can receive a clean bit-exact result. Hashes can locate candidate alignments but cannot establish exact equality. Independently comparing the retained recording's original words found **zero unequal frames across all 30,480,000 frames**; this finding concerns the published proof method, not observed corruption in that recording.

Required outcome: Compare original slot words before accepting aligned windows and continuing runs. Retain collision rejection beside ordinary skip/repeat/foreign controls, and replay the actual recording with the corrected published grader. Preserve the as-run version separately.

Verification: The clean control must remain clean; the six-frame skip and one-frame repeat must retain their correct counts; the unequal-word collision must cease to be fully matched. Corrected real-record output must agree with the exact comparator in `recompute.py`.

**R635-1-F3 — MINOR — Robustness, Tests**

Artifact: `author/tools/b21_grade.py:253` and `:255`; `probe-results.json`, case `three_zero_insertions`.

Authority/evidence: The grader promises to classify foreign frames and offset changes. Three inserted zero frames as the first discontinuity create foreign events followed by an offset event. Summary generation tests whether any offset event exists, then reads `ev[0]["wire_frame"]`. The first foreign event lacks that key. The published script exits 1 with `KeyError: 'wire_frame'` and emits no grade. Positive, skip and repeat controls complete normally. A combined control beginning with a skip can mask this event-order defect.

Impact: A valid negative input loses its numerical grade. This is a crash, not a false clean verdict, and does not itself invalidate the clean recording.

Required outcome: Compute initial alignment independently of the first event's shape and report foreign counts/offsets for this ordering. Add an isolated insertion control.

Verification: The input must produce a completed non-clean grade with three foreign zero frames and the corresponding insertion offset, preserving all other control results.

**R635-1-F4 — MINOR — Tests, Docs**

Artifact: `docs/findings/117_AUDIO_CONTINUITY.md:937`; `author/r3/selftest/mst-long/mst-long-analysis.txt`; `mst-long-replayed.txt`.

Authority/evidence: The page describes nine groups of positive +6 to +8-frame steps and attributes each to a missing sampler cycle. Replay with `B5_W=110` produces **eight positive groups (+6.3 to +8.4 frames) and one negative group (-2.5 frames)**. The negative group spans reads 57,646–57,845, starting at 576.485 s. Against the +2.304-frame median floor drift, it exceeds the absolute four-frame detection tolerance. It is not a ninth positive step.

Impact: The measurement and universal explanation disagree with the executable receipt. The separate ten-second floors still reproduce -3.50 to +1.94 frames; this finding does not establish capture loss. Because it changes a measured figure, it is not wording-only RESIDUE.

Required outcome: Correct the signed population and qualify or substantiate the sampler explanation for both signs. Keep short floor excursions distinct from the permanent-step check.

Verification: Regenerate the nine signed group entries from the retained timing record and compare them with the corrected prose.

Measured evidence

`records-audit.json` verifies 378 extracted public files against published hashes and 18 selected retained media/timing inputs against raw hashes. Private host inventories were not read. The retention receipt lists 82 files; its complete assertion is not relabelled as my 18-input verification. Round 1's original raws are lost, explicitly acknowledged at page lines 835–838. Its derived intervals remain reproducible; its original interrupt/pressure samples do not.

| Measurement | Re-derived result | Receipt |
|---|---|---|
| Identity, three observations | 11/11 each; changed VERSION rejected, exit 1 | `replay-results.json` |
| McASP self-test | 63,000 × 480 = 30,240,000 frames; zero overrun/drop/>15 ms stall; 630.017 s between first/last reads; +43.06 ppm deficit slope | `mst-long-replayed.txt` |
| Permanent floor check | 63 blocks; residual -3.50 to +1.94 frames; largest adjacent change 2.81 frames | `mst-long-replayed.txt` |
| Direction A, DUT tap | 5,198,452 packets; zero sequence breaks; 124,999–125,020 ns timestamp steps; 30,951,504 valid pattern frames; zero repeat/skip/backward/torn/invalid-in-region | `recomputed.json` |
| Direction A, peer tap | 5,198,499 packets; zero sequence breaks; same timestamp bounds; 30,952,266 valid pattern frames, zero defects | `recomputed.json` |
| Direction A, both taps | 5,198,372 common packets equal in sequence, timestamp and complete payload; 80 DUT-only leading and 127 peer-only trailing packets | `recomputed.json`; published wire summary |
| Tap clock difference/transit | Magnitude 13.070107 ppm; detrended residual -27.681 to +23.894 µs, not absolute latency | `recomputed.json` |
| Direction A, CRF | 324,903 and 324,906 packets; zero sequence breaks; approximately 500 packets/s each | `recomputed.json` |
| Direction A, output cross-check | 30,624,574 valid frames, 638.01196 nominal seconds; zero repeat/skip/zero/torn in-region; 64,005 reads, zero stalls | `dA-ext-replayed.json` |
| Direction B, taps | DUT 5,199,125; peer 5,198,371; zero sequence breaks; 124,953–125,042 ns steps; all 5,198,371 common packets equal | `recomputed.json` |
| Direction B, exact samples | 30,480,000 frames; four complete words each equal at wire offset 148,874; zero unequal frames | `recomputed.json`; `dB-mcasp-replayed.json` |
| Direction B, capture delivery | 63,490 reads: 63,484 × 480, four × 960, two × 1,920 frames; zero overrun/drop; 25 stalls, maximum 87.07 ms | `dB-reads-replayed.txt` |
| DUT, each direction | 128 samples; SLIP_TDM zero; SLIP_LB 0x0000ffff, saturated, no rate evidence; render converged, prefill clear, fill 8–14, rails zero; listener summaries static | `records-audit.json`; replayed CSR JSONs |
| Direction A counters | AAF_FRAMES +5,079,938 and AAF_PAIRS +121,918,506 over 635 s; DUT output FRAMES_TX = peer input FRAMES_RX = +5,245,516 | `dA-counters-replayed.json`; `records-audit.json` |
| Direction B counters | Peer FRAMES_TX +5,207,829; DUT FRAMES_RX +5,207,944 at different read instants; error counters static | `dB-counters-replayed.json` |
| Restart transactions | 20 successful cycles; 40 successful matching format reads, 0205022002006000; no format set due | `records-audit.json` |
| Wire restarts | Min/median/max 13.447 / 13.8165 / 86.795 ms; no packets in graded holds; first 480 frames valid/ordered each time | `rA-restart-replayed.json` |
| Output restart excluding latency | Min/median/max 23.475 / 24.7685 / 97.794 ms; 20 zero-only silences; no in-run step/capture stall | `rA-restart-replayed.json`; F1 applies |
| Historical round-1 intervals | 11/123 stalls; longest 23.191/88.417 ms; no 2.99–3.02 s recurrence; 2/18 large-loss groups and 11/13 one-ms groups | `records-audit.json` |

CSR/counter, external-capture, restart and full McASP alignment outputs reproduce their published JSONs exactly. The independent packet parser verifies hashes while decoding and rejects truncated records. Its sample comparison uses original words. Historical loss sums depend on subtracting the small median floor drift; the receipt records both conventions rather than implying the lost raw files are available.

All 20 restart comparison records contain null fields because the driver reads a nonexistent response field. Decoding the 40 actual successful GET_STREAM_FORMAT payloads proves every pair matched. Thus no set was due in this run; the disclosed driver limitation is not an additional acceptance failure here.

Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | #117 body/assignments; REQUIREMENTS.md section 8; findings page:843–1136; direction/restart media; F1, F2 | R635-1 | 867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b |
| RTL | CLEAN | Entire source.diff; TIME_SYNC.md:507; REGISTER_MAP.md:1878/:2028; CSR polls/decodes; source-integrity.json | R635-1 | 867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b |
| Robustness | UNCLEAN | McASP grader; skip/repeat/foreign/collision probes; buffer/stall evidence; restart holds and transactions; F2, F3 | R635-1 | 867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b |
| Tests | UNCLEAN | Pinned analyses/raw inputs; independent decoder and exact comparator; identity mutation; replay outputs; F1–F4 | R635-1 | 867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b |
| Docs | UNCLEAN | Entire page delta/PR body; task/receipts; hash provenance/limits; local docs checks; F1, F2, F4 | R635-1 | 867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b |

[R635] PASS RTL — `source.diff`, `docs/reference/REGISTER_MAP.md:1878`, `:2028`, `docs/design/TIME_SYNC.md:507`, `records-audit.json` — checked slip saturation, render fields and capture/render clock boundaries against the claims. No implementation/interface change or new RTL/reset/CDC/width/backpressure behavior is present to simulate. This clean result covers the findings delta, not every property of the installed image.

Validation, limits and pending duties

The author's `author/r3/gates-head/gates.txt` identifies this exact source head and eleven successful invocations. I independently ran the five documentation checks and `git diff --check 4a9b5a2a HEAD`; all passed. Focused replay campaigns used at most four workers and one numerical-library thread per process. No full parent/processor/synthesis/builder bank, hardware operation, source fix, commit, push, public write or merge occurred.

`hosted-contexts.json` records successful fast/documentation/elaboration contexts. The long-suite and synthesis aggregates were **skipped**, as were physical and several subordinate contexts. These are not executed long-bank or calibration evidence; no executed work was inferred from aggregate names. Hosted/local workflow acceptance remains the manager's duty.

No manager source bank was run or inferred. Source-head evidence is the author's receipts plus the focused checks listed here. The manager must separately build the merge candidate against live dev `1f6f2f57177f1dd904654c317009461b43423989`, or the updated tip at merge time, run the required builder/native banks and publish receipts. The source base and this review cannot substitute for candidate validation.

The identity gate proves the listed console/descriptor/CRC facts, not a complete configuration SHA-256 readback. There is one window per direction on the installed `9ef71772` image. Direction A checks eight channels on the wire but only channels 0–1 at the peer output. Direction B checks four McASP slots against received wire samples; it does not observe the peer's upstream source. That noise contains 6,437,039 adjacent identical frames and 6,371,968 all-zero frames. Exact equality proves the observed sequence, but cannot reveal substitutions between indistinguishable equal samples or establish unobserved upstream continuity.

McASP read timing uses the SoC monotonic clock; sample delivery uses the DUT's serial-audio clock. The deficit test cannot detect corruption before the reader or establish arbitrary single-frame loss sensitivity. Tap clocks are independent and unwrapped using host capture time; AVTP presentation fields wrap modulo 2^32. Nominal durations divide sample counts by 48,000. Detrending measures relative variation, not calibrated absolute transit. Physical calibration is NOT RUN. Offline controls and field skips are not hardware proof. F1 preserves the missing absolute output latency.

The page acknowledges round-1 raw loss and preserves round-2's incomplete identity STOP. Restoration receipts document bindings/maps/clocks, the live propagation-delay difference, unchanged saved-state line and restarted bridge/player. This review has no live access to verify later bench state.

Final source verification hashed all 1,371 tracked blobs, checked file kinds/modes, matched every index entry and all required gitlinks against the head. Required submodules remain uninitialized as supplied; no submodule-source execution is claimed. No restoration was needed because source bytes were never changed. See `source-integrity.json`.

Portable reproduction, with explicit input directories:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 recompute.py "$EVIDENCE/author" "$RAW_ARCHIVE" "$PACKET/scratch/recomputed"
MD_PYTHON="$PINNED_MARKDOWN_PYTHON" python3 run_evidence.py "$CHECKOUT" "$EVIDENCE/author" "$RAW_ARCHIVE" "$PACKET"
python3 probes.py "$EVIDENCE/author/tools" "$PACKET/scratch/probes"
python3 audit_records.py "$EVIDENCE" "$RAW_ARCHIVE" "$PACKET/records-audit.json"
python3 verify_source.py "$CHECKOUT"
```

Media inputs must match published sizes/hashes. The replay script requires the repository-pinned Markdown environment. Probe success means reproducing the documented observations, including false-clean/crash behavior; it is not a product PASS. Large generated data and probe trees remain under `scratch/`, outside the publication manifest.

Before merge, the manager must obtain corrections and independent re-review of F1–F4, finish the other review, accept a clean updated ledger, complete candidate and hosted/local validation, obtain maintainer merge authorization and perform containment. This PR references #117; its audio row does not close the issue's other physical obligations.

R635-1 FINISHED
