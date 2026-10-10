[R594] NEGATIVE - exact head 70cd90a42fdc8c9b5059383e657a8b5a26f1da8e

# R594-1: internal independent review of PR #712 (issue #629, bench lane B15)

- Head `70cd90a42fdc8c9b5059383e657a8b5a26f1da8e`, tree `c11996e4d13a5c7d1b1c658dbf140d3f1726d87f`, one commit on dev `e8454e2751d05b02ee8e5a571857589ab358ab86` (live dev at review start). The commit message is one line with no trailers.
- Diff: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (+330/-1: title, introduction pointer, Contents line, and the new section "Dev 5603c353, 2026-10-10: lane B15" at `:1875-2197`) and `docs/findings/README.md` (one row). No code, RTL, firmware, test or generated artifact.
- Reconstructed from: AGENTS.md, CONTRIBUTING.md (section 6, privacy and the em-dash rule), docs/README.md, the #629 body, the B15 assignment (issuecomment-6097827871), TAKEN (6097896607), STOP (6098146914), the lane B8/B9/B10 assignments and STOPs on #629, PR #712's body and comments, the diff, and the published packet `review-evidence/629-tone-r1` at evidence commit `06148614c910d3986991dd130f95d073b4bbe491` (branch `629-tone-review-evidence`).
- Prior public review findings on PR #712: none. The PR carries no review, review comment or finding, only the two review-start notices. Nothing is carried forward to resolve or retain.

## Verdict

NEGATIVE. Two MINOR findings are open, both under Docs. The measurement record itself holds. Every figure, verdict, hash and count I could check against the published packet matches it, the decoders' controls reproduce, and the privacy rules hold. What fails is the page's record of where its evidence lives and of the decoders the verdicts rest on (F1), plus one wrong incident time (F2). Conformance, RTL, Robustness and Tests are covered clean at this head.

## Findings

### F1: MINOR, Docs. The B15 section does not say where its packet is published, and does not pin the evidence files or the new decoders its verdicts rest on

- Where: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1905-1906` ("Paths such as `runs/pts1/events.jsonl` are in the lane packet, `629-b15-a588`") and `:2179-2197` ("B15: artifact hashes", which hashes raw files only).
- Authority and evidence:
  - AGENTS.md section 2 says a future cold reviewer must be able to reconstruct the task from GitHub and the repository alone.
  - The section 6 Docs lens asks for "enough evidence for another cold reviewer".
  - The same page sets the pattern three times. B6 (`:630`), B7 (`:1218`) and B8 (`:1816`) each carry a "Where the packet is" paragraph that names the branch, the pinned commit and the label-to-path mapping. B8 also hashes its evidence files and every tool (`:1840-1872`).
  - In B15 the label `629-b15-a588` resolves to nothing in the repository, on the issue or on the PR.
  - The packet is in fact published at `629-tone-review-evidence` `06148614` under `review-evidence/629-tone-r1/author/`.
  - None of these is hashed on the page:
    - `tools/tone_points_b15.py`, which makes every per-point presence verdict (published masked: 16,207 bytes, `a899f2e7a746265338606f1cfd7f41543d6e2f540b02e1c8022d05d13766f608`; as-run hash in `redaction.json`);
    - `tools/align_b15.py`, which makes the SAMPLE-EXACT verdicts (6,399 bytes, `701554820de6dcb532caf90052116226d7d80e858daa012ef540b87e07e497a3`);
    - the control JSONs, the alignment JSONs and the run event logs.
  - The tone source's state and meter figures (`:2108-2112`) are backed only by records the packet keeps private ("meter rows private"). The page does not say so, though it does say so for the external capture's sizes (`:2181-2183`).
- Impact: a cold reader cannot find the evidence behind the B15 verdicts or tie them to a specific decoder. The page's own durable record does not pin "decode 5 of 5" and "alignment 5 of 5" to any code.
- Required outcome: the B15 section, like B6 to B8:
  - says where the packet is published (branch, pinned commit, and `629-b15-a588` mapped to `review-evidence/629-tone-r1/author/`), with the `MANIFEST.json` original/published convention and the three files masked at publication;
  - hashes at least `tools/tone_points_b15.py` (masked, with its as-run hash), `tools/align_b15.py`, `controls/b15-tap-controls.json`, `controls/b15-align-controls.json`, `summary/pts1/align-b-c.json`, `summary/pts2/align-b-c.json`, `runs/pts1/events.jsonl`, `runs/pts2/events.jsonl` and `restore/census-compare.txt`;
  - states that the tone source's state read and meter rows are held privately.
- Verification:
  - each cited hash equals that file's `published_sha256` in `MANIFEST.json` at the pinned commit (`scripts/verify_packet_manifest.py`);
  - the pinned commit carries the mapped path;
  - the Markdown gates still pass.

### F2: MINOR, Docs. The incident's outage start time is not the one the board log records

- Where: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2148`, "It was down from 15:27:23 to 15:28:23 CEST".
- Evidence (`author/soc/pts1-legs.log` in the packet):
  - The stop command was issued at 13:27:19.667Z (15:27:19.7 CEST) and printed `KILLED`. Its record closed at 13:27:25.264Z, after the command's own 2 s and 3 s sleeps.
  - The board's uptime puts the kill 63.5 s before the restart that printed `STARTED` (stop record uptime 350018.34 after a 3 s sleep; restart record 350079.80 after a 3 s sleep). The restart was issued at 13:28:23.070Z.
  - No record carries 15:27:23. The leg was down from about 15:27:20 to 15:28:23, about 63 s, not 60 s.
- Impact: the incident figure is about 3 s short. It moves no measurement or verdict, but it is a stated figure the evidence does not support. The owner's rule keeps figure errors out of RESIDUE.
- Required outcome: the outage start reads about 15:27:20 CEST (the kill, issued at 15:27:19.7), or the sentence says what 15:27:23 marks. Note that the stop was deliberate; the unintended part began when the first restart attempt at 15:27:55 printed `LEG_PRESENT_NOT_STARTED`.
- Verification: compare against the record headers and uptime lines in `soc/pts1-legs.log`.

### R1: RESIDUE (wording only). The method claims that playback start and stop were "the only instrument actions"

- Where: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1945-1946`.
- Evidence: the same page records a read of the tone source's state and passive reads of its meters (`:2108-2112`), plus the external capture's recordings. The packet's handoff lists all of these as instrument actions. Nothing was written, so the claim "no instrument setting was changed" stands.
- Exact fix: replace "Starting and stopping that playback were the only instrument actions." with "Starting and stopping that playback, one read of the tone source's state, passive reads of its meters and the external capture's recordings were the only instrument actions; no instrument setting was written."

### Suggestions (optional; none affects coverage)

- **S1 (Tests, Robustness; for the lane that resumes Direction B).** Lane B8's presence rule gates on the channel's whole-capture RMS (`level > -40` in `tone_points_b15.py`), not on the tone's level as the page quotes tones (`-1.00 dBFS` for a sine whose RMS is about 3 dB lower).
  - Probe P1 (`receipts/probe-b15-tools.json`) adds a tone at -40 dBFS peak to a floor like the captured one: share 0.998, verdict TONE ABSENT.
  - The tone leaves the source at -38.5 dBFS (`:2109-2111`). If it reaches (a) at about that level, the gate may report a present tone as absent.
  - This does not touch B15's result. The 0.04 % shares at (a), (b) and (c) rule out any tone above about -140 dBFS (P1: a -140 dBFS tone already moves the share to 62 %).
  - Suggest: grade presence on the share, or state the gate in RMS terms, and add a control with a present quiet tone.
- **S2 (Docs).** `:2049-2050`: the DUT publishes FRAMES_RX coalesced at a 1 s interval (`docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md:185`). So +191,998 and +199,998 over 24.5 s (TIMESTAMP_VALID +195,893 and +196,239) are 24 and 25 publications, not rates. A clause saying so would stop a reader from seeing an 8,153 PDU/s stream.
- **S3 (Docs).** `:2141-2144`: `docs/reference/REGISTER_MAP.md` (the `0x8D4` row) reads `SLIP_LB` as static under one media clock. Here the DUT was on INTERNAL and the peer followed the DUT's CRF, yet 3 slipped frames counted. A link to #645, or a note that these are unexplained, would keep the residual from reading as expected.
- **S4 (Docs).** `restore/host-end.txt` lists three more virtual interfaces than `restore/host-start.txt`. The "Bench host" row of "B15: bench as left" (`:2135`) does not say whether the lane caused them; nothing in the lane's commands suggests it did.
- **S5 (Tests).** `:2072-2077` says the alignment control's correction left the comparison code untouched. The packet records only the final `align_b15.py`, not a hash as run at the two alignments, so this rests on the author's word. Recording that hash would close it. My probe P2 exercises the published `compare()` and finds it correct.

## Per-lens results (covering round R594-1, head 70cd90a4)

- **[R594] PASS Conformance.** I checked the B15 section `:1875-2197` against the B15 assignment (6097827871).
  - Step 1, identity gate: `identity/identity-verdict.txt` gives 11/11 PASS, the window is 13:17:48 to 13:17:54Z, and the CRC32 of the 7,512 bytes is `5ba355eb`.
  - Step 2, four simultaneous points: the capture start times are in `runs/pts*/events.jsonl`.
  - Step 3: the "absent at (a)" branch was taken with read-only checks and a STOP (6098146914).
  - Step 4: the dated section, per-point tables, capture hashes and the #629 checklist are all present. The checklist is consistent with B8's table (`:1737-1750`) and #645 is OPEN.
  - Binding rule: the formats `0205022001006000` (4 ch, 6 spf) and `0205022002006000` (8 ch) decode correctly, and the listener adapted.
  - The AAF header parse in `tone_points_b15.py` (sv/mr/tv, sequence_num, nsr, channels_per_frame, bit_depth, stream_data_length) matches IEEE 1722-2016 clause 7.
  - The GET_COUNTERS decode matches the STREAM_INPUT counter order, with valid mask `0xfff`.
  - Refs #629 only: no closing keyword in the PR body or the commit, and `closingIssuesReferences` is empty.
- **[R594] PASS RTL.** The diff touches no RTL, firmware or `hdl/` (`scripts/ci_scope.py` scope; hosted `rtl-fast` success with the RTL jobs skipped). The page's datapath claims at `:2031-2055` are consistent with the interface authorities:
  - AAF 24-bit left-justified in 32-bit big-endian words (`docs/CHANNEL_MAP_64.md:61`);
  - unmapped or disabled render entries give digital silence, matching channels 4 to 7 reading zero (`docs/CHANNEL_MAP_64.md:82-88`);
  - the McASP0 sample in bits 31:8 (`docs/findings/451_TDM8_FIRST_LIGHT.md:162`);
  - `SLIP_LB` at one dup per fed pair per slipped beat, so 6 dups on a 4-channel stream are 3 frames (`docs/reference/REGISTER_MAP.md` `0x8D4` row; page `:1423-1424`).
- **[R594] PASS Robustness.**
  - Robustness of the conclusion: probe P1 shows the observed 0.04 % shares exclude any tone component above about -140 dBFS, and every (a)/(b) PDU has one format, `bad_length` 0, 0 sequence gaps and 0 tv clear (`summary/pts*/{a,b}-*.json`).
  - (a) is direction-selected (port 3), and the peer's stream ID cannot reach the peer's link from the switch.
  - The pts1 control mistake checks out against `runs/pts1/events.jsonl`: the peer's counters all 0, the external capture all zero (`summary/pts1/d-extcap-pair.json`), the rx flag `0x0002` against `0x0082`, then `0x0082` at pts2 start and end. It is recorded honestly.
  - Restore census: 45 of 46 (`restore/census-compare.txt`, the GET_AVB_INFO propagation delay 381 to 387 ns).
  - Residuals: NVM seq 272 to 276 and commits 38 to 42, `SLIP_LB` `0x92` to `0x98` (`restore/dut-start.txt` against `dut-end.txt`).
  - SoC board: same boot, leg PID 1948, UDC configured (`soc/end-health.log`).
  - Tone stopped by PID (`runs/tone-stop.txt`).
  - The incident's mechanism is confirmed in `soc/pts1-legs.log` (its time is F2, under Docs).
- **[R594] PASS Tests.**
  - `b6_thdn.py controls` and `b9_thdn.py controls`, rerun from the published tools, are byte-equal to the packet's `controls.json` (`7bbefc71...`, also the B8 row at `:1852`) and `b9-controls.json` (`728a4f0e...`).
  - `tone_points_b15.py control`, with only its two synthetic placeholders unmasked, passes 5/5 and its JSON equals `b15-tap-controls.json`. Each control can fail: exact recovery, channel placement, gap position, port filter, floor-only.
  - Probe P2 on a synthetic floor stream of pts1's size: 9/9. Exact, drop (+1), repeat (-1) and 1 LSB change are detected and located. A channel 0/1 swap, a channel 2/3 swap, an all-zero recording, a dead channel and another stretch are all NOT SAMPLE-EXACT. The first window matches once.
  - `align_b15.py control` itself cannot be rerun, because the raw pts1 tap capture stays on the bench host.
- **[R594] UNCLEAN Docs.** F1 and F2 are open (MINOR). R1 is RESIDUE.
  - The pinned Markdown environment gates at the exact head all return rc 0: `docs_check`, `check_doc_style`, `gen_toc --check`, `gen_toc --verify-anchors`, `check_em_dash --base e8454e27` and `--selftest`, `check_doc_paths`, plus `ci_scope --selftest`, `check_baremetal_only --check`/`--selftest`, `check_feature_status --self-test` and `git diff --check` (`receipts/gates.txt`).
  - All 85 in-page anchors resolve (`receipts/inpage-anchors.txt`).
  - Every B15 table figure matches the packet (`receipts/page-vs-packet.txt`, 0 mismatches): all 11 raw rows (bytes and SHA-256 against `RAW-ARTIFACTS.json`), per-channel levels, PDUs, alignment rows, counters, the census, and the control block counts 15/23, 15/23, 13/16.
  - Privacy, page and PR body:
    - no instrument, peer product, host, address, interface, USB position or wiring beyond phrasing the base page already uses ("the peer's digital output", "the tone source", the tap's 28-byte record header, "SoC board", McASP0);
    - the DUT identity values were already on the base page;
    - the external capture's sizes and channel count are withheld;
    - a scan of the added lines for addresses, paths and vendor tokens is clean.

## Completion ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Page B15 section `:1875-2197` against assignment 6097827871 steps 1 to 4, #629 body, B8 acceptance `:1737-1750`; `tone_points_b15.py` AAF parse against IEEE 1722-2016 clause 7; GET_COUNTERS payloads in `runs/pts*/events.jsonl`; `identity/identity-verdict.txt`; PR body and commit (no closing keyword) | R594-1 | `70cd90a42fdc8c9b5059383e657a8b5a26f1da8e` |
| RTL | CLEAN | Diff (2 Markdown files, no RTL/firmware); `docs/CHANNEL_MAP_64.md:61,82-88`; `docs/reference/REGISTER_MAP.md` `0x8D4`; `docs/findings/451_TDM8_FIRST_LIGHT.md:162`; page `:2031-2055` against `summary/pts*/c-mcasp.json` and `align-b-c.json` | R594-1 | `70cd90a42fdc8c9b5059383e657a8b5a26f1da8e` |
| Robustness | CLEAN | Probe P1; `summary/pts*/*.json` format and gap fields; `runs/pts*/events.jsonl`; `restore/*` (census, DUT start/end, controller, host); `soc/*-health.log`, `soc/pts1-legs.log`; `runs/tone-*.txt` | R594-1 | `70cd90a42fdc8c9b5059383e657a8b5a26f1da8e` |
| Tests | CLEAN | Reruns of `b6_thdn.py`/`b9_thdn.py controls` (byte-equal), `tone_points_b15.py control` (5/5, equal JSON); probe P2 on `align_b15.compare` (9/9); `controls/b15-*.json` | R594-1 | `70cd90a42fdc8c9b5059383e657a8b5a26f1da8e` |
| Docs | UNCLEAN (F1, F2 open) | Full diff; pinned Markdown gates; in-page anchors; page-vs-packet cross-check; privacy scan; precedent sections B6/B7/B8 | R594-1 | `70cd90a42fdc8c9b5059383e657a8b5a26f1da8e` |

Docs must be re-covered at a head that fixes F1 and F2. A Markdown-only fix to this section also un-covers Conformance for the edited claims, so re-check those lines at that head.

## Real limits

- Raw captures are not public. The pcaps, McASP0 recordings, external capture and tone loop stay on the bench host, so no per-point figure was re-derived from samples. Every figure was checked against the published summaries, controls and logs, and the decoders were checked by their controls and my probes.
- I could not rerun `align_b15.py control`, for the same reason. The claim that its correction left the comparison code untouched rests on the author's statement (S5).
- The tone source's state, meter readings and the peer's descriptor payloads are private. The -38.5 dBFS, -20.0 dB and -18.5 dB figures and the AUDIO_CLUSTER/AUDIO_UNIT description were not verifiable from public material.
- "Byte-equal to lane B10's" cannot be checked publicly, because B10's packet is not published. I instead reproduced both controls byte-equal from the published tool hashes. The b6 hash also equals the merged B8 row.
- No hardware was touched. Physical calibration NOT RUN, and field skips are not hardware proof.
- No source bank was run at this head, and none is claimed or inferred. Source execution evidence is the author's published gate receipts plus my documentation-gate rerun.

## Pending manager duties

- Merge-turn validation of the current-dev merge candidate (builder and native banks) and its receipts on the PR. Hosted and local-replica acceptance is the manager's.
- Hosted contexts at 70cd90a4, observed 2026-10-10T14:06:48Z (`receipts/hosted-checks-observed-at.txt`):
  - `rtl-fast` success; `changes`, `elaborate`, `bdd-conformance`, `docs-check`, `docs-check-no-git`, `wire-accountability` and `full-ci-gate` success;
  - `verilator-lint`, `verilator-suites`, `yosys-elaboration`, `yosys-portability`, `firmware-unit`, the shards and physical gPTP skipped. These are skipped contexts, not executed evidence.
- Packet hygiene, outside the diff:
  - `author/identity/grader-identity.txt` in the published packet carries the grandmaster identity unmasked, while `restore/census-*.jsonl` and `restore/dut-*.txt` mask it as `<gm-id>`.
  - The same value already appears in three files tracked on dev at `e8454e27`, so this is no new exposure, only an inconsistency in the redaction pass.
  - Also, author gate 13 (`check_baremetal_only.py` with no mode) returned rc 2. It was a mis-invocation that gates 8 and 9 supersede, and the PR body does not claim it.
- Carry R1 to the residue checklist.
- #629 stays open.

## Receipts (paths relative to this packet)

- `receipts/gates.txt`, `receipts/gate-1.txt` to `gate-12.txt`: documentation gates at the exact head (pinned Markdown lock installed from `tools/markdown/requirements.txt` with `--require-hashes`).
- `receipts/inpage-anchors.txt`: `scripts/check_inpage_anchors.py` on the page.
- `receipts/page-vs-packet.txt`, `.rc`: `scripts/check_b15_page_vs_packet.py <page> <packet author dir>`.
- `receipts/packet-manifest.txt`: `scripts/verify_packet_manifest.py <review-evidence/629-tone-r1>`, 182/182.
- `receipts/rerun-controls.txt`, `rerun-b6-controls.json`, `rerun-b9-controls.json`, `rerun-b15-tap-controls.json`: control reruns from the published tools (`scripts/unmask_synthetic_ids.py` prepares the tap decode's controls).
- `receipts/probe-b15-tools.json`, `.stdout`, `.rc`: `scripts/probe_b15_tools.py <tools dir> <out>`, probes P1 and P2.
- `receipts/hosted-checks-observed-at.txt`: hosted check-run states at the exact head.
- `receipts/clone-integrity.txt`: the review clone after all probes.
  - HEAD, tree and index tree are exact, with 0 status lines.
  - Index equals HEAD over 1,275 entries.
  - All 1,270 tracked blobs re-hash to HEAD and every mode matches.
  - The five submodule gitlinks are unchanged.
  - No source file was edited.

R594-1 FINISHED
