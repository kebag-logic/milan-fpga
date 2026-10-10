[R595] NEGATIVE - exact head 70cd90a42fdc8c9b5059383e657a8b5a26f1da8e

# R595-1: external independent review of PR #712 (issue #629, bench lane B15)

- Head `70cd90a42fdc8c9b5059383e657a8b5a26f1da8e`, tree `c11996e4d13a5c7d1b1c658dbf140d3f1726d87f`, one commit on dev `e8454e2751d05b02ee8e5a571857589ab358ab86` (source base = live dev at review time).
- Diff: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (+329/-1: title, introduction pointer, Contents line, the dated section "Dev 5603c353, 2026-10-10: lane B15", lines 1875-2197) and its row in `docs/findings/README.md` (1/1). No code, RTL, firmware, test or generated artifact changes.
- Evidence judged: the public packet at `629-tone-review-evidence` = `06148614c910d3986991dd130f95d073b4bbe491`, `review-evidence/629-tone-r1/` (182 files; `MANIFEST.json` verified: 182 of 182 published hashes match, and the 3 files that differ from the author manifest are the path-redacted ones it lists).
- Authority reconstructed from: AGENTS.md, CONTRIBUTING.md (sections 6, 6.1), docs/README.md, issue #629's frozen body, the [A10] B15 assignment (issuecomment-6097827871), [A588] TAKEN (6097896607) and STOP (6098146914), the earlier lanes B6 to B8 on the same page, `docs/reference/REGISTER_MAP.md` (STREAM_INPUT counters, `SLIP_LB`), and `hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv`.

**Verdict reason.** One MINOR is open (F1, Conformance and Docs), so the verdict is NEGATIVE. Everything else checks out at this head:
- Every lane B15 figure on the page reproduces from the archived decoder summaries: 77 of 77 checks (`receipts/crosscheck_b15.txt`).
- The tool controls re-run byte-equal.
- The decoders behave under 22 planted probes.
- All ten documentation and scope gates are rc 0.
- The page carries no new instrument, peer-product, host, address, wiring or clock-topology identifier.

RTL, Robustness and Tests are CLEAN. Two RESIDUE items and six SUGGESTIONs are listed below.

## Findings

### F1 - MINOR - Conformance, Docs - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2113-2118` - the peer's AUDIO_CLUSTER read result contradicts the only published read and rests on an unpublished one

**Authority and evidence.**
- The B15 assignment, step 3, branch "Tone absent at (a)": "Read the playback and routing state read-only (... the peer's input routing over ATDECC reads only) ... STOP with the evidence".
- AGENTS.md section 6, Docs: "The PR and Issue contain enough evidence for another cold reviewer".
- The page states: "Each of those AUDIO_CLUSTER descriptors takes its signal from the peer's AUDIO_UNIT 0."
- The packet's published start survey, `author/restore/peer-descs.jsonl` (15:19 CEST), read the peer's current configuration. The census GET_CONFIGURATION answers `00000001` and every read carries cfg=1. In that survey:
  - STREAM_PORT_OUTPUT 0 names 4 clusters from index 16, and STREAM_PORT_INPUT 0 names 16 from index 0.
  - All 20 READ_DESCRIPTOR AUDIO_CLUSTER reads, indices 0 to 19 (16 to 19 included), answered **NO_SUCH_DESCRIPTOR**. See `receipts/peer_cluster_reads.txt`.
- The author's published handoff, step 11, cites a second read at 15:35:10 that found clusters 0 to 19 with 16 to 19 sourced from AUDIO_UNIT 0. Its evidence column reads "private (descriptor payloads)". Its requests, including the configuration index, are not in the packet.
- The page does not say a second read exists, that it is private, or why the same descriptors answered NO_SUCH_DESCRIPTOR sixteen minutes earlier.

**Impact.**
- A read result of the assignment's required read-only routing check cannot be verified, and the only public receipt for it says the opposite.
- If the later read addressed another configuration index, the statement describes a configuration the peer is not running.
- The lane's conclusion does not depend on this sentence, so the lane's verdict is unaffected; the defect is in the claim. The conclusion is that the loss is upstream of the peer's talker and the input path is not described over ATDECC. It rests on two things: (a)'s tap decode, and the published CONFIGURATION counts and AUDIO_UNIT 0 port fields (no jack; external and internal ports all 0).

**Required outcome.** Either:
- the page states only what public evidence supports (the start survey's 20 NO_SUCH_DESCRIPTOR answers in configuration 1); or
- the packet publishes the 15:35:10 requests with their configuration index, plus the decoded signal_type, signal_index and signal_output of clusters 16 to 19 (redacted as the privacy rule needs), and the page reconciles them with the start survey.

**Verification.**
- Re-read the B15 "The peer, over ATDECC reads" bullet at the new head against the packet.
- Run `scripts/peer_cluster_reads.py <author dir>` on the republished packet.

### F2 - RESIDUE - Docs - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1900` and `docs/findings/README.md:15` - "at the 24-bit floor" reads as the tone's level

The positive control's tone is at -1.00 dBFS. The 24-bit floor is its THD+N, as `:2097-2099` says correctly. This is wording only: no figure or verdict changes. Exact fix:
- In the `:1900` cell, replace "...is found on both taps and at the external capture, at the 24-bit floor" with "...is found on both taps and at the external capture, with THD+N at the loop's 24-bit floor".
- In the README row, replace "finds a tone at the 24-bit floor" with "finds the tone with THD+N at the loop's 24-bit floor".

### F3 - RESIDUE - Docs - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1906, 2179-2183` - the section names its lane packet but not where it is published

Lanes B6, B7 and B8 each carry a "**Where the packet is.**" paragraph (`:630`, `:1218`, `:1816`). B15's text says only "in the lane packet, `629-b15-a588`", and the PR and issue do not link it either. This is wording only. Exact fix: add to "B15: artifact hashes", in B8's form:

> **Where the packet is.** It is published on branch `629-tone-review-evidence`, pinned at `06148614c910d3986991dd130f95d073b4bbe491`. `629-b15-a588` maps to `review-evidence/629-tone-r1/author/` there: `runs/pts1/events.jsonl` is `review-evidence/629-tone-r1/author/runs/pts1/events.jsonl`. `review-evidence/629-tone-r1/MANIFEST.json` gives each file's `original_sha256`, the lane packet's file, beside the published file's `published_sha256`.

(Use whatever commit the manager finally pins.)

### Suggestions (optional; no effect on coverage)

- **S1 - RTL, Docs - `:2049-2050`.** FRAMES_RX reads "+191,998 in 24.5 s" and "+199,998 in 24.5 s": the same span, 8,000 apart. Both match the raw GET_COUNTERS (`receipts/counters_decode.txt`). The shipping engine commits FRAMES_RX per observation interval of at most 1 s (Milan Table 5.6; `hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv:18-22`), so two reads see 24 or 25 committed intervals. TIMESTAMP_VALID, +195,893 and +196,239, tracks the PDUs. One sentence would stop a reader taking 8,163 frames/s as an excess.
- **S2 - Robustness, Tests - `author/runs/pts1/tap.txt`, `author/runs/pts2/tap.txt`.** The tap-side `tail -2` was rejected on the tap host ("unexpected argument '-2'"), so the capture tool's own drop summary was never recorded. No claim depends on it: every selected stream has 0 sequence gaps, and 191,843 PDUs span 23.90 s (8,000.1/s). For later lanes, use `tail -n 2`.
- **S3 - Tests - `author/tools/align_b15.py:33-38, 85-87`.** `key()` keeps 8 bits per channel: probe A3 plants a +256 LSB error and the tool misses it. The verdict can also read SAMPLE-EXACT with fewer frames compared than recorded: in probe A7, 300,000 of 480,000 compared still gave SAMPLE-EXACT. Neither affects the recorded runs: every value at (b) and (c) is in -2..+1, compared = recorded = 480,000, covered [0, 480000]. Widen the key, and require compared == recorded for SAMPLE-EXACT.
- **S4 - Conformance, Tests (for the resume).** The tone leaves the source at -38.5 dBFS. Lane B8's presence rule needs a channel level above -40 dBFS. Probe T2 shows a -45 dBFS tone with share 1.0 judged TONE ABSENT. Here the absence is robust: every share is 0.03 to 0.05 %, the flat-floor value, and the RMS is -141 dBFS. When a tone does reach (a), decide presence relative to the floor, or record the expected arrival level first.
- **S5 - Docs - `:2108-2112`.** Say on the page that the tone source's state read and its meter rows are kept privately, as the loop's layout is. Their only public trace is `author/runs/tone-start.txt`, "METERS_RC=0 (rows private)", and the meter reader is not in the packet.
- **S6 - Docs - `:2097-2099`.** "Sample-exact" for the positive control is inferred from THD+N. The inference is sound at the printed resolution:
  - every in-playback block on both taps reads exactly the loop's own floor, -146.0647 / -145.9933 dB;
  - the external capture's -146.0648 is within the floor's own spread across window rotations (-146.0647 to -146.0653, `receipts/rotation_floor.txt`);
  - one 1-LSB error moves a block by +0.0017 dB (probe L4).

  State that, or decode the frames' ordinals with `b6_tone`'s table, which the loop is built for.

### Observations for the manager (not findings against this head)

- **O1.** The published `author/identity/grader-identity.txt` shows the gPTP grandmaster's clock identity unmasked, while every other packet file masks it as `<gm-id>`, and `redaction.json` has no entry for this file. The same identity is already committed in `docs/findings/117_GPTP_SILICON_EVIDENCE.md:129`, so nothing new is disclosed. This is redaction consistency only.
- **O2.** `author/restore/host-end.txt` lists three more virtual interfaces than `host-start.txt`. The page claims no host-network equality, and the packet does not show their origin.
- **O3.** The census's 46 entries include the census tool's start record, so 45 AVDECC reads. This is the same convention as lanes B6, B7 and B8 (`:553`, `:1119`, `:1717`), and the stated single difference is exact: GET_AVB_INFO propagation delay `0x17d` to `0x183`, 381 to 387 ns.

## Prior public review findings

At this head PR #712 has 0 reviews, 0 review comments and two review-start notices. Issue #629 carries no review finding on lane B15. There is nothing to resolve or retain.

## Lens results

### Conformance - UNCLEAN (F1)

- **PASS: identity gate.** `author/identity/identity-verdict.txt` matches the page's identity table: entity_id, name, firmware 2.96.0, serial, ID `4d494c4e`, VERSION `00020060`, AEM CRC `5ba355eb`, ENTITY 312 B and CONFIGURATION 106 B byte-equal, CLOCK_SOURCE 0/1/2 and 3 = NO_SUCH_DESCRIPTOR, domain list 0,1,2 reading 0, grader 10/10, ADP model. The lock window 15:17:48 to 15:17:54 matches `lock-window.txt`.
- **PASS: binding rule (the listener adapts).** `author/runs/pts1/events.jsonl`:
  - format-check: the DUT input is already equal; the peer's STREAM_INPUT 0 is set 8ch to 4ch, SUCCESS and echoed;
  - format-restore to `0205022002006000`, then rebind-as-found;
  - final differs only in rx flags `0x0002` against `0x0082`, as the page says.
  - In `pts2/events.jsonl`, final equal_to_found is true.
- **PASS: per-point results and hashes.** `receipts/crosscheck_b15.txt`, 77 of 77, covers:
  - levels, ranges, shares, PDUs, gaps, `tv`, `mr` and format for (a), (b), (c) in both runs;
  - alignment rows;
  - the control medians and blocks at floor (15 of 23, 13 of 16);
  - every raw hash and size against `author/RAW-ARTIFACTS.json`.
- **PASS: DUT STREAM_INPUT 0 counters.** `receipts/counters_decode.txt`: MEDIA_LOCKED 1 / UNLOCKED 0 at all four reads, every error counter 0, valid mask `0xFFF`, as REGISTER_MAP's AAF row states.
- **PASS: the branch taken.** The assignment's "absent at (a)" branch was taken, and the STOP was posted with evidence (issuecomment-6098146914).
- **PASS: no instrument setting written.** `author/tools/tone_play_b15.sh` only starts and stops the playback, and `tone-start.txt` and `tone-stop.txt` record that.
- **PASS: #629 judgement.** Direction B stays NOT met, #645 stays open, Refs #629 only (PR body and one-line commit), and #629 stays open.
- **PASS: the pts1 (d) control mistake** is recorded as run. A bridge does not forward a frame to its reception port. The peer's counters are 0 and its digital output exact zero (`author/summary/pts1/d-extcap-pair.json`).
- **UNCLEAN:** F1, the peer AUDIO_CLUSTER read claim.

### RTL - CLEAN

- **[R595] PASS RTL** - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2031-2055, 2123-2151` against `hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv:18-40`, `docs/reference/REGISTER_MAP.md:877-884, 1870` and `author/restore/dut-{start,end}.txt`. The DUT-side claims are consistent with the shipping contracts:
  - The sample is bits 31:8, and the low byte is 0 at both taps and McASP0.
  - The four identity mappings (`map-dut-in` in the events) give mapped TDM slots 0-3 equal to stream channels 0-3, and unmapped slots 4-7 are exactly zero.
  - FRAMES_RX is an interval counter (S1).
  - `SLIP_TDM` stayed 0. `SLIP_LB` 146 to 152 is 6 dups, which is 3 slipped frames at 2 fed pairs, the register map's unit and lane B7's `:993` convention.
  - NVM seq 272 to 276 and commits 38 to 42 match the 4 bind/unbind commits.
  - No RTL changed.

### Robustness - CLEAN

- **[R595] PASS Robustness** - the run's failure and restore paths: `author/runs/pts{1,2}/events.jsonl`, `author/soc/pts1-legs.log` and `author/restore/census-compare.txt`.
  - The leg incident matches the page: stop at 15:27:19-25, LEG_PRESENT_NOT_STARTED at 15:27:55, restart at 15:28:23 under pid 1723. The capture had completed by then.
  - The census shows 45 of 46 equal, the one difference being the propagation delay.
  - The tap host and controller staging were cleaned (`ls` misses, PGREP_RC=1).
  - Malformed input handling in `tone_points_b15.py:76-105` skips short records, foreign subtypes and bad lengths.
- **Probes** (`receipts/probes_r595.jsonl`): the alignment flags a 1-LSB change, a channel swap, a 50-frame hold and a drop/repeat slip. The two edge weaknesses (S3) do not touch the recorded data.

### Tests - CLEAN

- **[R595] PASS Tests** - `author/controls/*` and `author/tools/{tone_points_b15,align_b15,b6_thdn,b9_thdn}.py`, re-run in scratch copies (`receipts/controls_rerun.txt`):
  - `b6_thdn.py controls` and `b9_thdn.py controls` are byte-equal to the archived `controls.json` (`7bbefc71...`) and `b9-controls.json` (`728a4f0e...`).
  - `tone_points_b15.py control` is byte-equal to `b15-tap-controls.json` once its two redaction placeholders get neutral ids (as published it stops at `bytes.fromhex("<peer-eid>")`).
  - `align_b15.py`'s planted controls pass 5 of 5 on a synthetic floor of pts1's length.
  - The disclosed one-frame expectation correction is principled: the expected slip index now comes from the content's equal-neighbour runs, and the comparison code is unchanged.
- **Independence from the tools' own assumptions** is shown by real data. The known lane B6 loop is recovered from both real tap captures and the external capture at -1.00 dBFS, 997.0000 and 9,973.0000 Hz, at the loop's own floor, and the loop is regenerated here with SHA-256 `566d3dfa...` (probe L1). The two independent capture paths (b) and (c) also agree sample for sample.
- **SUGGESTIONS** S2, S3 and S4 only.

### Docs - UNCLEAN (F1)

- **PASS: gates.** All rc 0 at the head (`receipts/gates-summary.txt`, `receipts/gate-*.txt`), with the pinned Markdown environment already on the host (cmarkgfm 2025.10.22, html5lib 1.1): `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `gen_toc.py --verify-anchors`, `check_em_dash.py --base e8454e27...`, `check_doc_paths.py`, `git diff --check e8454e27 HEAD`, `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `check_feature_status.py --self-test`.
- **PASS: privacy.** A scan of the 331 added lines finds no host name, address, MAC, interface, serial adapter, vendor or product name. Every role term the section uses (SoC board, McASP0, USB network link, bench host, digital output to the external capture) is already on the base page. The external capture's sizes are withheld. The peer is described only by role and by its AEM shape.
- **PASS: honesty of the record.** The pts1 (d) mistake, the alignment control's first failing run, the leg incident and the residuals are all recorded honestly.
- **UNCLEAN:** F1. RESIDUE F2 and F3, and SUGGESTIONs S1, S5 and S6, are listed above.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 open) | B15 assignment, TAKEN, STOP; page `:1875-2197`; `author/identity/*`, `author/runs/*`, `author/summary/*`, `author/restore/peer-descs.jsonl`, `author/tools/tone_play_b15.sh`; `receipts/crosscheck_b15.txt`, `receipts/peer_cluster_reads.txt`, `receipts/counters_decode.txt` | R595-1 | `70cd90a42fdc8c9b5059383e657a8b5a26f1da8e` |
| RTL | CLEAN | `KL_avtp_rx_monitor.sv:18-40`; `REGISTER_MAP.md:877-884, 1870`; `author/restore/dut-{start,end}.txt`; page `:2031-2055`, `:2123-2151` | R595-1 | `70cd90a42fdc8c9b5059383e657a8b5a26f1da8e` |
| Robustness | CLEAN | `author/runs/pts{1,2}/events.jsonl`, `author/soc/pts1-legs.log`, `author/restore/*`; `receipts/probes_r595.jsonl` (A3-A8) | R595-1 | `70cd90a42fdc8c9b5059383e657a8b5a26f1da8e` |
| Tests | CLEAN | `author/tools/{tone_points_b15,align_b15,b6_thdn,b9_thdn,b6_tone}.py`, `author/controls/*`; `receipts/controls_rerun.txt`, `receipts/probes_r595.jsonl`, `receipts/rotation_floor.txt` | R595-1 | `70cd90a42fdc8c9b5059383e657a8b5a26f1da8e` |
| Docs | UNCLEAN (F1 open) | the page diff and README row; CONTRIBUTING section 6; `receipts/gates-summary.txt`; base-page convention `:630`, `:1218`, `:1816` | R595-1 | `70cd90a42fdc8c9b5059383e657a8b5a26f1da8e` |

## Real limits

- **Raw captures not re-decoded.** The raw captures (both taps, McASP0, the external capture) and the tone loop stay on the bench host. Every page figure was checked against the archived decoder summaries, not re-decoded from raw bytes. The decoders were re-run on their controls and on synthetic stimulus only.
- **Private material.** The tone loop `d9684a8f...` cannot be regenerated here, because its playback layout is private. The tone source's state read, its meter rows and the 15:35:10 peer read are private, so the -38.5 / -20.0 / -18.5 dB figures were not verifiable.
- **No hardware.** No bench access and no hardware was used. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **No source bank.** No manager source bank ran at this head, and none is claimed or inferred. Source-head execution evidence is the author's gate receipts plus the gates re-run here.
- **Hosted contexts.** At the head: `rtl-fast`, `docs-check`, `docs-check-no-git`, `changes`, `elaborate`, `bdd-conformance`, `wire-accountability` and `full-ci-gate` succeeded. `verilator-suites`, `yosys-portability`, the shards and `verilator-lint` were skipped by scope (docs-only). The manager owns hosted and act acceptance.

## Pending manager duties

- Route F1 to a fix round, then re-review Conformance and Docs at the new head.
- Carry F2 and F3 to the residue checklist.
- Validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts.
- Observations O1 to O3.
- The second independent review (R594-1) and the full completion bar before any merge.

## Clone restore

Receipt: `receipts/clone_restore_check.txt`.
- No file in the review clone was edited: probes ran on copies under the packet's `scratch/`.
- At the end: HEAD `70cd90a4...` and `write-tree` = `c11996e4...`.
- Index identical to the tree in modes, blobs and paths. Worktree equals index equals HEAD, with 0 porcelain lines.
- Gitlinks unchanged: `external` `efeb541a`, `gptp-processor` `5dce647a`, `protocol-processor` `2ad2f845`, `third_party/lwSRP` `9197193e`, `third_party/verilog-axis` `48ff7a7e`. Checked-out submodules are at their recorded commits.

## Receipts and scripts

All paths are relative to this packet, with hashes in `MANIFEST.sha256`.
- `scripts/crosscheck_b15.py <author dir> <page>` derives the page figures from the summaries.
- `scripts/peer_cluster_reads.py <author dir>` lists the peer's cluster, port and unit reads.
- `scripts/decode_counters.py <events.jsonl>...` decodes the GET_COUNTERS payloads.
- `scripts/prepare_tools.sh <tools> <scratch>` copies the tools and substitutes neutral ids.
- `scripts/probes_r595.py <tools> <work>` runs the 22 planted probes.
- `scripts/rotation_floor.py <tools> [n]` measures the loop floor across window rotations.
- Their outputs are in `receipts/`.

R595-1 FINISHED
