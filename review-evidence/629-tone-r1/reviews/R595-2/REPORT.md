[R595] POSITIVE - exact head 1df3ac18a85c59626491ccb6c0955f834cb1d31f

# R595-2: external independent review of PR #712 (issue #629, bench lane B15), round 2

- Head `1df3ac18a85c59626491ccb6c0955f834cb1d31f`, tree `94830be1d4efecf402b0866e18edfc2fb85e186d`. Two commits on dev `e8454e2751d05b02ee8e5a571857589ab358ab86` (`70cd90a4`, then `1df3ac18`). Each commit message is one line with no trailers.
- Diff `e8454e27..1df3ac18`: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (+395/-1: the title, the introduction pointer, the Contents line, and the section "Dev 5603c353, 2026-10-10: lane B15" at `:1875-2262`), plus one row in `docs/findings/README.md`. No code, RTL, firmware, test or generated artifact changed.
- Reconstructed in this order: AGENTS.md; CONTRIBUTING.md (section 6, privacy and the em-dash rule); docs/README.md; the #629 body; the B15 assignment (issuecomment-6097827871), TAKEN (6097896607), STOP (6098146914), the round-2 assignment (6098395010) and REVIEW READY (6098501387); the manager's earlier privacy rulings on #629 (instrument identity and capture layout are private); the authorities `docs/reference/REGISTER_MAP.md` (STREAM_INPUT counters, `SLIP_LB` at `0x8D4`) and `avdecc/aem_descriptors.py:96-103` (IEEE 1722.1 Table 7.1 codes); the diff and its history; the published packet `review-evidence/629-tone-r1` at evidence commit `06148614c910d3986991dd130f95d073b4bbe491`.
- The independent pass and a draft verdict were written to `receipts/independent-pass-notes.txt` before I read the prior findings on PR #712 (R594-1, R595-1). No other material was read.

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR is open at this head. Two RESIDUE items (wording only) and three SUGGESTIONs are recorded below. Every prior public finding on this PR is resolved at this head (see "Prior public review findings").

I checked the measurement record against the published evidence:
- every figure, range, share, count, hash and size;
- the counters, census, restore state and peer survey.

All of it matches. The decoders' controls reproduce byte-for-byte, and the Markdown gates pass at this head. The lane took the assignment's "tone absent at (a)" branch, and the evidence supports that branch.

## Findings

### R595-2-R1 - RESIDUE - Docs - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2036-2038` - "by exact match" overstates what the alignment tool compares

- Evidence: `author/tools/align_b15.py:33-38` keys each frame on each sample's low eight bits (`(a[:, c] + 128) & 0xFF`). Probes P3 and P4 (`receipts/probe_tools.txt`) plant a +256 LSB difference, once on one sample and once on a whole channel. The tool reports SAMPLE-EXACT both times.
- Why it is only wording: at this head every compared value is in -2..+1 at (b) and -2..0 at (c). The page's own range columns at `:2004-2011` show this, as do `summary/pts{1,2}/{b-dut-tap,c-mcasp}.json` (`receipts/summary_dump.txt`). On that range the 8-bit key is one-to-one, so "480,000 of 480,000 frames equal" and both SAMPLE-EXACT verdicts stand. No figure, verdict, test or claim changes.
- Exact fix: replace "It locates the recording's first 256-frame window in the stream by exact match, then walks every frame." with "It locates the recording's first 256-frame window in the stream by matching each sample's low eight bits, then walks every frame. That comparison is exact here, because every compared value lies between -2 and +1."

### R595-2-R2 - RESIDUE - Docs - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2247-2250` - three more cited files were already masked in the lane packet

- Evidence: `author/redaction.json` at `06148614` records lane-packet masking with as-run hashes for these files, besides `tools/tone_points_b15.py`:
  - `runs/pts1/events.jsonl` (as run `d80ffde4...`);
  - `runs/pts2/events.jsonl` (as run `5d4acd1c...`);
  - `restore/census-compare.txt` (as run `f3a32e9e...`).
  
  The page annotates only `tone_points_b15.py`. Every cited hash is correct: it equals both `published_sha256` and `original_sha256` (`receipts/check_hashes.txt`).
- Why it is only wording: it is provenance prose. No hash, figure, verdict or privacy treatment changes.
- Exact fix: replace "The lane packet already held `tone_points_b15.py` masked, and `redaction.json` alone holds its as-run hash." with "The lane packet already held `tone_points_b15.py`, both `events.jsonl` files and `census-compare.txt` masked, and `redaction.json` alone holds their as-run hashes."

### Suggestions (optional; no effect on coverage)

- **S1 - Tests - `author/tools/align_b15.py:33-38`, `controls/b15-align-controls.json`.** None of the five planted controls changes a sample by more than 127 LSB, so the 8-bit key (R1) is never graded. Before the alignment is reused on a tone at (a), where it will see full-scale values, key on the full 24-bit sample and add a +256 LSB control. R595-1-S3 made the same point and it is still open.
- **S2 - Tests - `author/tools/tone_points_b15.py:240`.** Every synthetic PDU in the tap-decode controls carries `mr` 0 and `tv` 1. A decoder that never counted `tv` clears or `mr` toggles would therefore still pass 5 of 5. Here, independent evidence backs the page's `tv`/`mr` columns at (b): the DUT's TIMESTAMP_NOT_VALID and MEDIA_RESET deltas are both 0 (`receipts/counters.txt`). (a) is the same stream. A control that toggles `mr` and clears `tv` would close the gap.
- **S3 - Conformance, Tests (for the resume) - `author/tools/tone_points_b15.py:152`.** The presence rule requires the channel's RMS to be above -40 dBFS. The page puts the tone source's output at -38.5 dBFS on its meters. Probe: a tone pair at -41.5 dBFS RMS with share 1.000 is graded TONE ABSENT. At this head the absence does not depend on that threshold: every share is 0.03 to 0.05 % and every level is -141 dBFS. When a tone reaches (a), report the share result separately from the level gate. R594-1-S1 and R595-1-S4 point the same way.

## Prior public review findings (read after the independent pass)

| Finding | At `1df3ac18` | Evidence |
|---|---|---|
| R594-1-F1 (MINOR, Docs): packet location and evidence hashes | Resolved | `:2235-2262` names the branch, the pinned commit `06148614`, the label-to-path mapping, the MANIFEST convention and the three files masked at publication. The 9 required files are hashed, and 9 of 9 equal their published bytes and sizes (`receipts/check_hashes.txt`). The tone source's private records are stated at `:2118-2119` |
| R594-1-F2 (MINOR, Docs): outage start | Resolved | `:2179-2186`: stopped on purpose at 15:27:19.7, `LEG_PRESENT_NOT_STARTED` at 15:27:55, restarted at 15:28:23, about 63 s down. This matches `author/soc/pts1-legs.log`: record headers 13:27:19.667Z, 13:27:55.459Z and 13:28:23.070Z |
| R594-1-R1 (RESIDUE) | Applied | `:1946-1949` carries the exact text |
| R595-1-F1 (MINOR, Conformance, Docs): AUDIO_CLUSTER claim | Resolved, per the manager's round-2 conditions | `:2126-2148` states the 20 NO_SUCH_DESCRIPTOR answers in configuration 1. Their requests carry type `0x0010`: `receipts/peer_survey.txt` decodes the payload heads as `0001 0000 0010 xxxx`. Table 7.1 gives `0x0010` to EXTERNAL_PORT_INPUT, and `avdecc/aem_descriptors.py:103` gives `0x0014` to AUDIO_CLUSTER. The linked PR #628 comment records the inherited survey's wrong code. The private 15:35:10 read is stated as private, in configuration 1, with type `0x0014`. The page says the conclusion rests on the tap decode and on the published CONFIGURATION and AUDIO_UNIT fields, and I verified those fields: no jack, no external or internal port, one CONTROL, base cluster 16 with identity maps |
| R595-1-F2 (RESIDUE) | Applied | `:1900` and the README row read "with THD+N at the loop's 24-bit floor" |
| R595-1-F3 (RESIDUE) | Applied | Superseded by the R594-1-F1 paragraph above |
| R594-1-S2 / R595-1-S1, R594-1-S3, R595-1-S5 | Applied | `:2055-2056` (FRAMES_RX per committed interval), `:2172-2177` (`SLIP_LB` unexplained, linked to `0x8D4` and #645), `:2118-2119` (private records) |
| R595-1-S3, S4; R594-1-S1 | Still open as suggestions | Carried as S1 and S3 above |
| R595-1-O1, O2; R594-1-S4, S5 | Not findings against this head | O1 is carried to #495 by the manager. O2/S4 (extra host virtual interfaces) and S5 (no as-run hash for `align_b15.py`) remain observations |

## Lens results (round R595-2, head `1df3ac18a85c59626491ccb6c0955f834cb1d31f`)

[R595] PASS Conformance - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1875-2199` against the B15 assignment (6097827871) and #629's acceptance:
- Identity: `author/identity/identity-verdict.txt` matches `:1911-1920` (entity_id, name, firmware 2.96.0, serial, ID/VERSION, AEM CRC `5ba355eb`, ENTITY 312 B and CONFIGURATION 106 B byte-equal, CLOCK_SOURCE 0/1/2 with 3 NO_SUCH_DESCRIPTOR, CLOCK_DOMAIN list 0/1/2 reading 0).
- Binding rule: `receipts/events_binds.txt` matches `:1982-1994` (one listener format set and echoed, then restored; every bind count 1 and unbind count 0; the pts1 rx flags `0x0082` to `0x0002`).
- Captures: both runs fall inside the playback window (13:26:59Z to 13:35:31Z). pts1 captures from 13:27:28.7Z and pts2 from 13:31:13.1Z.
- Per-point tables at `:2002-2022`: levels, ranges, shares, PDU counts, gaps, `tv`, `mr` and format all match the summary JSONs (`receipts/summary_dump.txt`). AAF header fields were checked against the IEEE 1722-2016 AAF layout:
  - `mr` is bit 3 of byte 1 and `tv` is bit 0;
  - format INT_32BIT is `0x02`, nsr 5 is 48 kHz, cpf is 4, depth 32, and stream_data_length is 96.
- Counters at `:2050-2053`: `receipts/counters.txt` shows MEDIA_LOCKED 1, MEDIA_UNLOCKED 0, every error counter delta 0, and FRAMES_RX +191,998 and +199,998.
- Branch taken: the absent-at-(a) branch led to a STOP with evidence, read-only peer and instrument reads, and no instrument write (`author/runs/tone-start.txt`, `tone-stop.txt`).
- #629 judgement at `:2190-2199`: consistent with B8's at `:1737-1755`. Direction B stays NOT met, #645 stays open, and the PR is Refs only.

[R595] PASS RTL - `:2034-2060`, `:2166-2177` against `docs/reference/REGISTER_MAP.md` and the receipts:
- The diff touches no `hdl/`, firmware or tooling.
- The page's DUT-path claims hold. (c) equals (b) on the four identity-mapped channels. The DUT's maps read 4 and 8 identity mappings, equal at start and end (`receipts/dut_maps.txt`).
- The STREAM_INPUT counter layout matches REGISTER_MAP `:1551` and `tb/tools/avdecc_ctl.py:67-73`.
- `SLIP_LB` 146 to 152 is consistent with REGISTER_MAP `:1870`: one dup per fed pair per slipped beat, and the 4-channel stream feeds two pairs, so 3 frames. The raw words are `0x92` and `0x98` in `author/restore/dut-{start,end}.txt`.
- The page reports the slip as unexplained, with #645 linked, rather than claiming a cause.

[R595] PASS Robustness - `author/runs/pts{1,2}/events.jsonl`, `author/soc/pts1-legs.log`, `author/restore/census-compare.txt`, `author/restore/dut-{start,end}.txt` against `:2152-2186`:
- The pts1 (d) mistake is recorded as run.
- The leg incident's timeline matches the log.
- Census: 45 of 46 entries are equal. The one exception is GET_AVB_INFO propagation delay, `0x17d` to `0x183`, which is 381 to 387 ns.
- NVM went from seq 272 to 276 and from 38 to 42 commits, with `pend=0`.
- Restore read-backs equal the start state.
- Probes P1-P5 (`receipts/probe_tools.txt`): the alignment catches a channel swap and a frame drop. Its blind spot above 8 bits (R1, S1) does not reach the recorded data.

[R595] PASS Tests - `author/controls/*`, `author/tools/{tone_points_b15,align_b15,b6_thdn,b9_thdn}.py`, re-run on scratch copies with placeholder stream IDs:
- `b6_thdn.py controls` reproduces `7bbefc71...`, `b9_thdn.py controls` reproduces `728a4f0e...`, and `tone_points_b15.py control` reproduces `f69bf5cf...`. All three are byte-equal to the published files (`receipts/repro/`).
- The `align_b15.py` controls pass 5 of 5 on a synthetic floor stream (`receipts/repro/probe-align-controls.json`).
- The positive control's block counts at `:2100-2102` match the per-block data: 15 of 23, 15 of 23 and 13 of 16 blocks at -146 dB. The rest are silent or edge blocks.
- Gaps in the controls are recorded as S1 and S2. They are optional, because no claim at this head depends on them.

[R595] PASS Docs - the diff, `docs/findings/README.md:15`, and `receipts/gates/gates.txt`:
- Gates, all rc 0 at this head, using the pinned Markdown environment where applicable: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base e8454e27` and `--selftest`, `check_doc_paths.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check`, `check_feature_status.py --self-test`, and `git diff --check e8454e27 HEAD`.
- Hash tables: 9 of 9 evidence rows and 11 of 11 raw rows match (`receipts/check_hashes.txt`, `receipts/check_raw.txt`).
- Privacy: a scan of the added lines finds no host, path, address, MAC, interface or vendor. The identity strings it uses are already public at dev (`653_DISCONNECT_ORDER_BENCH.md:62`). The external capture's sizes stay withheld.
- The open Docs items are R1 and R2. Both are RESIDUE, so the lens stays clean.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | B15 section `:1875-2199`; identity, events, summary and counter receipts; B15 assignment; #629 acceptance; B8 acceptance `:1737-1755` | R595-2 | `1df3ac18a85c59626491ccb6c0955f834cb1d31f` |
| RTL | CLEAN | Diff scope (docs only); `:2034-2060`, `:2166-2177` against REGISTER_MAP `:1551`, `:1870`; DUT maps; `SLIP_LB` raw words | R595-2 | `1df3ac18a85c59626491ccb6c0955f834cb1d31f` |
| Robustness | CLEAN | events.jsonl ×2, pts1-legs.log, census-compare, dut-start/end, probes P1-P5 | R595-2 | `1df3ac18a85c59626491ccb6c0955f834cb1d31f` |
| Tests | CLEAN (S1, S2 optional) | tap/align/B6/B9 controls reproduced; align controls on synthetic floor; positive-control per-block data | R595-2 | `1df3ac18a85c59626491ccb6c0955f834cb1d31f` |
| Docs | CLEAN (R1, R2 RESIDUE) | Diff; README row; hash tables vs `06148614`; 11 gates; privacy scan | R595-2 | `1df3ac18a85c59626491ccb6c0955f834cb1d31f` |

## Real limits

- The raw captures (pcap, McASP, external capture) are not published, so I did not re-run the decode or the alignment on the real captures. I verified their outputs against the published summaries, hashes and controls, and I re-ran the tools on synthetic inputs.
- The tone source's state read and meter rows are private, and so is the 15:35:10 peer AUDIO_CLUSTER read, under the bench privacy rule. The page's -38.5 dBFS, -20.0 dB and -18.5 dB figures, and its cluster sourcing, are therefore not publicly verifiable. The conclusion does not rest on them.
- No manager source bank was run at this head, and I claim none. No hardware, flash or calibration evidence was produced or reviewed. Physical calibration was NOT RUN.
- Hosted checks at the exact head, as queried (`receipts/hosted-checks.txt`):
  - executed and successful: `rtl-fast`, `changes`, `elaborate`, `bdd-conformance`, `docs-check-no-git`, `wire-accountability`, `full-ci-gate`;
  - still in progress: `docs-check`;
  - skipped by scope: `verilator-suites`, `yosys-portability`, `verilator-lint`, `yosys-elaboration`, `firmware-unit`, the shard jobs and physical gPTP.
  
  These are skipped contexts, not executed evidence.

## Pending manager duties

- Hosted and act acceptance at the exact head, including `docs-check`, which was still in progress when queried.
- The current-dev merge-candidate validation (builder and native banks) at the merge turn, with source base and live dev both `e8454e27` at review time.
- Carry R595-2-R1 and R595-2-R2 to the residue checklist with their exact texts.
- R595-1-O1 to #495 at merge, as already ruled.
- #629 stays open: Direction B's quality metric is NOT met, and resuming it needs an owner instrument decision.

## Receipts (paths relative to this packet)

`receipts/independent-pass-notes.txt`, `receipts/check_hashes.txt`, `receipts/check_raw.txt`, `receipts/summary_dump.txt`, `receipts/counters.txt`, `receipts/events_binds.txt`, `receipts/peer_survey.txt`, `receipts/dut_maps.txt`, `receipts/probe_tools.txt`, `receipts/repro/*.json`, `receipts/gates/*`, `receipts/hosted-checks.txt`, `receipts/clone-integrity.txt`; scripts `scripts/check_hashes.py`, `scripts/check_raw.py`, `scripts/decode_counters.py`, `scripts/parse_peer_survey.py`, `scripts/probe_tools.py`. The clone was left at the exact head with a clean worktree and index (index tree `94830be1...`), and its five submodule gitlinks were unchanged (`receipts/clone-integrity.txt`).

R595-2 FINISHED
