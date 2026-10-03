[R451] NEGATIVE - exact head 4eee41a558a56024e57b27a956fdaf7910ca69dc

Round R451-1, external independent review of issue #629 / PR #644 (bench lane B7, docs only).
Head `4eee41a558a56024e57b27a956fdaf7910ca69dc`, tree `c90f26fbb419062935cae9a0a490b3368688b6e6`,
one commit on dev `bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352`. Diff: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`
(+477/-1, the dated section "Dev bbf704ec, 2026-10-03: lane B7") and its row in `docs/findings/README.md`.
PR body says `Refs #629`, not `Closes`: correct, because not every #629 item is met.

Verdict basis: two open MINOR findings (F1 under Tests and Docs, F2 under Docs). Conformance, RTL and
Robustness are covered clean. Every case verdict (A0, A1, A2, B0, B-CRF, B-AAF) re-derives from the
published run artifacts. The controls are byte-equal to lane B6's and still detect slips. The privacy
sweep is clean. The open findings concern the record's accuracy and traceability, not the measurements.

## What was examined

Context, in this order: AGENTS.md, CONTRIBUTING.md (section 6, wording and privacy), docs/README.md, and the #629 issue body.
Then the [A10] lane B7 assignment (issuecomment-5969106115), [A519] TAKEN and REVIEW READY, the D4 = A2-a and
known-risk decisions, and `docs/design/MEDIA_CLOCK_FOLLOWING.md` (Lock loss, `mr`, CLOCK_DOMAIN C1, Test plan Bench).
Also `docs/reference/REGISTER_MAP.md` (0x738, 0x748, 0x8D4/0x8D8, 0x8E0/0x8E4, 0x8F8), `docs/reference/FR_NFR.md`,
`hdl/ieee1722/avtp/KL_talker_diag_ctx.sv` and `hdl/ieee1722/crf/KL_crf_tx.sv`, and the diff `bbf704ecc..4eee41a5`.
Evidence: branch `629-b7-review-evidence` at `95448218b342c084efa28ac266ae9415bff4ecce`, path `review-evidence/629-b7-r1`
(376 files, every `published_sha256` re-verified, no unlisted file). Lane B6's packet `422dcf91` was used for the controls and A0-criterion comparison.
Hosted check runs were inspected read-only. Prior public review findings on PR #644: none. The PR holds only the two
review-start notices, and no [R]-prefixed finding exists on #629 for lane B7, so nothing is carried or resolved.

## Independent re-derivation (receipts/rederive_b7.json, from `rederive_b7.py`)

The script decodes the raw console CSR words itself from the register map's field layout. It decodes the raw
GET_COUNTERS payloads itself. It recounts `events.csv` and `blocks.csv` and re-applies the 48 n + 12 test to every
capture-path cluster in each `grade.json`.

| Case | Window start (CEST) | Audio s | Listener events (csv) | Net non-capture steps / frames, ppm | Clean blocks, THD+N 997 / 9,973 dB | Servo at 21 reads; trim ppm | Timed ppm (half-width) | Re-derived verdict |
|---|---|---|---|---|---|---|---|---|
| A0 | 14:42:08 | 630.31 | 470 skip-1, 291 insert-1 | 179 / 30,254,880 = +5.916 | 444 of 630, -146.065 / -145.993 | IDLE; 0 | +5.71 (0.55) | control shows the mismatch |
| A1 | 14:53:19 | 629.88 | 0 | 0 / 30,234,240 | 597 of 629, at floor; offset <= 2.3e-7 | IDLE; 0 | -0.28 (1.40) | PASS |
| A2 | 15:04:29 | 628.04 | 0 | 0 / 30,145,920 | 578 of 628, at floor; offset <= 2.1e-7 | IDLE; 0 | +2.15 (4.42) | PASS (see attribution) |
| B0 | 15:15:42 | 629.55 | 457 skip-1, 278 insert-1 | 179 / 30,218,400 = +5.924 | 434 of 629 | IDLE; 0; CRF sink locked +11.025..+11.057 | +5.62 (0.44) | control shows the mismatch |
| B-CRF | 15:26:55 | 628.53 | 0 | 0 / 30,169,440 | 559 of 628 | LOCKED all 21; -6.0..-5.9375; CLOCK_DOMAIN 4/3 throughout | +1.98 (6.52) | PASS |
| B-AAF | 15:38:07 | 627.74 | 0 | 0 / 30,131,520 | 564 of 627 | LOCKED all 21; -6.0..-5.9375; meter locked+valid every read, +11.018..+11.043 ppm, restarts 0 to 0, max dev 29 ns; CLOCK_DOMAIN 5/4 throughout | -1.49 (11.64) | PASS (see attribution) |

- `SLIP_TDM` is (0,0) at the first and last window read in all six cases, and no DUT-beat repeat occurs.
  `SLIP_LB` grows 20 to 362 in B0: 342 dups, 2 fed pairs per slipped frame, 171 frames, +5.94 ppm. In B-AAF it reads 380 before the bind, 386 at window-0 and 388 from window-1 to the window's end, then 390 after the lock loss.
- Set to LOCKED, bracketed by the raw 0.5 s polls (`poll-lock-wait.jsonl`): B-CRF 3.057 to 3.560 s; B-AAF 6.550 to 7.052 s,
  with the meter locked by 0.53 s and its rate valid by 4.04 to 4.54 s. The page's figures (3.1-3.6, 6.6-7.1) differ only by the poll stamp used.
- Capture path: every cluster's basis is `read-time rise`. No cluster's rise departs from its loss by more than 1 ms + 2 %.
  No cluster is non-capture. The smallest loss is 60 frames, and the smallest capture-path step is 59 frames, so no one-frame event is hidden as capture path.
  Reads, stalls over 15 ms, clusters, lost frames and longest stall equal the page's table in all six cases.
  The 47 clusters under 98 frames have rises of 0.97 to 2.01 ms after read gaps of 10.68 ms or more.
- Off-signature clusters, re-applied: A0 cluster 1 (2,586 frames, 18 short, control); A2 cluster 0 (100,810 frames, 2.10 s, 2 short) and cluster 9 (215 frames, 1 short);
  B-AAF cluster 4 (57,395 frames, 1.20 s), 17 (155 frames) and 24 (4,331 frames), each 1 short. That is exactly the page's five plus A0's one.
- Lock loss, from the raw polls and payloads: the followed talker was held unbound 11.09 s. HOLDOVER is bracketed 0.025 to 0.527 s after the unbind, with trim -5.9375 ppm
  frozen and every poll after it HOLDOVER. GET_CLOCK_SOURCE reads 2 before, during and after. After the rebind: ACQUIRE with the meter locked by 0.52 s, rate valid
  by 4.04 to 4.55 s, LOCKED by 5.55 to 6.05 s. DUT AAF output MEDIA_RESET 1 to 2 to 2; peer STREAM_INPUT 0 MEDIA_RESET 1 to 2 to 2. CLOCK_DOMAIN
  5/4 to 5/5 to 6/5 (LOCKED = UNLOCKED or UNLOCKED + 1 throughout). DUT STREAM_INPUT 0 MEDIA_UNLOCKED 0 to 1, then bank reset at the bind. The 29.98 s tone segment has 0 events, 0 invalid frames and 0 net steps.
  This is the design's Lock loss steps 1 to 4 and its `mr` section, and FR-CLK-04's toggle-on-disruption, observed through counters, as the page states.
- Fabric gating: the meter's enable bit is 0 at every read of A0, A1, A2, B0 and B-CRF. The DUT AAF output's MEDIA_RESET is 1 at every window mark of B-CRF and B-AAF and 0 in the four cases without a DUT set.
- Restore: in all six cases both clock sources end as found, all four listener formats equal as found, every RX connection count is 0 and the map reads back empty.
  Every format check took the talker's format, and only on the listener. The census shows 45 of 46 equal, the other being the DUT's live propagation delay (0x17F to 0x179).
- INTERNAL observation: A0 +5.916 and B0 +5.924 counted. The peer's media clock against gPTP is +11.02 to +11.06 (slow) from both the CRF sink and the meter, so the DUT is about -5.1 ppm against gPTP. Arithmetic checked.

## Identity, independently

`aem_from_source.py` (receipts/aem_from_source.json) runs the builder's own image path (`emit_aem_overlay`, `_entity_model_image`)
on `configs/endstation_ax7101_1x1_tdm8.yaml` at this head. It gives 7,512 B, CRC32 `5ba355eb`, SHA-256 `4fc8d61582a9...` and
entity_model_id `0x001BC5C1935893E1`. That equals the bench's `identity/expected.json` and the live readback, so the
image on the DUT is bound to the dev `bbf704ec` source through the AEM. The builder rewrote two tracked generated files byte-identically.
`identity-verdict.txt` holds 11 AECP descriptors byte-equal, CLOCK_SOURCE 3 NO_SUCH_DESCRIPTOR, and sources 0 INTERNAL, 1 on STREAM_INPUT 1 (CRF) and 2 on STREAM_INPUT 0 (AAF), in D1 = L1 order.

## Controls (receipts/controls_*)

The published `b6_tone.py` and `b6_thdn.py` are byte-equal to lane B6's (`d188a1a9...`, `d4673f55...`). The tone loop reproduces `566d3dfa...`.
`b6_thdn.py controls` exits 0 and its JSON is byte-equal to both lanes' `controls.json` (`7bbefc71...`).
Two disposable mutants show that the controls still bite: repeats made invisible fails `repeat1` (rc 1), and one-frame skips made invisible fails `drop1` and both slip controls (rc 1).
The 16 ppm and 1 ppm resampled controls stay green under both mutants, as expected, since they test the fitted offset.

## Capture-path attribution: the five off-signature clusters

- **Is the conservative reading stated?** Yes: page lines 1014-1018 and the limit at 1088-1089 ("Under the conservative reading of item 1 above, both would fail").
- **Would a verdict change under the strict reading?** Yes: A2 (2 + 1 merged listener repeats) and B-AAF (3) would each FAIL the "0 listener discontinuities" criterion.
  No other verdict changes: A1, B0 and B-CRF have no off-signature cluster, and A0 is a control.
- **My judgement: the PASS reading is supported.** The visible ~627 s of each window holds no listener event. With a flat prior, the posterior chance that the
  strict reading holds is at most 7.9e-11 for A2 and 1.4e-12 for B-AAF (receipts/attribution_bound.json). A0's control cluster 1 is 18 frames off the signature
  inside 54 ms, where A0's own measured listener rate predicts 0.065 events, so the capture path alone departs from the signature. Two of the five also sit inside
  losses longer than the loop, where lane B6's rule already excludes any event. The page's own second argument (the capture's drift) is weaker than these; see S1.
  No finding.

## #629 acceptance table on the page (lines 1067-1081), item by item

| Item | Page | Evidence checked | Holds? |
|---|---|---|---|
| Requirements | Met | FR_NFR.md:156 carries "The #389 record, as reversed by #629"; :238 and :239 carry the selectable set, AAF recovery, holdover without fallback and `mr` | Yes |
| Model and builder | Met on this image | Identity verdict; AEM regenerated from source equal; builder gate 33 present (`sw/builder/test_builder.py:19610`) | Yes |
| Fabric | Met for recovery and gating; switch not at bench | B-AAF re-derivation; meter enable 0 in the other five; switch named as sim-only | Yes, qualified |
| Lock loss | Met for the AAF source | Lock-loss re-derivation above; CRF loss named as not run | Yes, qualified |
| Protocol processor | Met in part | SET 1 and 2 SUCCESS with read-back; processor pin `631eeb34` is the merge of processor PR 142; `tb/pp_top` D3C3 grades the AAF-index save and restore | Yes |
| Simulation | Met by PR #634's evidence | PR #634 head `2bc5adc0` (merged as `bbf704ec`): 21 executed check runs SUCCESS including verilator-suites, rtl-fast, yosys-portability; one nightly context skipped (RESIDUE-1) | Yes |
| Bench, both directions | Met | A1/A2 (peer listener set and read back), B-CRF/B-AAF (DUT set and read back), formats, restore | Yes |
| Quality metric | Met for A, NOT met for B | A0 shows the mismatch, A1/A2 at floor, controls byte-equal; probe -2..0 LSB (`runs/probe/soc-record.log`) | Yes |
| A2-a | Met; observed | A2 PASS; INTERNAL +5.92 ppm / about -5.1 ppm, oscillator grade still the owner's known risk | Yes |

## Findings

**F1 - MINOR - lenses: Tests, Docs - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:756` (with :762, :835) - the A0 grading change is said to be fixed before any graded case, but it was fixed while A0 was recording.**
- Authority/evidence: line 756 reads "Each change was fixed at 14:50 CEST, before any graded case ran". Line 835 gives A0's window start as 14:42:08.
  `runs/a0/events.jsonl` has start 14:41:42, window-start 14:42:08 (t 1791031328.9) and window-end 14:52:39.
- The change at line 762 decides A0's verdict. It replaces lane B6's A0 criterion, "about 16 ppm" (B6 packet `HANDOFF.md:94`), with "beyond 2 ppm". A0 measured +5.92 ppm, which passes the new rule and not the old one.
  It was fixed during A0's window, with about 470 s of A0 recorded.
- Impact: the page's pre-registration statement is false for the one case whose criterion it changes. A reader cannot tell from the record whether the A0 threshold was chosen
  before or after A0's data. A0 still shows the mismatch in #629's own terms (186 of 630 blocks off the floor, 761 listener events), so this does not overturn A0. But the
  record that the page offers as the grading's integrity is wrong.
- Required outcome: the page states the true order, with the criteria fixed at 14:50 during A0's window. It gives the A0 threshold's basis independent of A0's data (lane B6's counted +6.52 ppm,
  and A2-a removing the 10.6 ppm beat). It states that A0 meets #629's control wording ("the metric must show the mismatch") whatever the threshold. If 14:50 is itself the wrong time,
  the page corrects it with the evidence that fixes it.
- Verification: compare the corrected text with the A0 run's `events.jsonl` start and window-start stamps.

**F2 - MINOR - lens: Docs - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1100-1140` - a cold reader cannot locate the B7 packet or every hash's record.**
- Authority/evidence: AGENTS.md section 6, Docs lens: "The PR and Issue contain enough evidence for another cold reviewer". Lane B6's section gives its packet's branch, pinned commit and path mapping (lines 620-653).
  The B7 section names the label `629-b7-a519` and no location. The packet is on public branch `629-b7-review-evidence` at `95448218`, but nothing on the page, in the PR body, or in any PR or issue comment points to it.
  Separately, lines 1102-1103 say each run's `events.jsonl` records its raw files' size and SHA-256. The seven `grade-full.json` rows (1126-1132) are not in any `events.jsonl`; they appear only in the packet's `RAW-ARTIFACTS.json`
  (`check_page_hashes.py`: 38 of 45 rows verified against the packet, those 7 found only there).
- Impact: every verdict rests on the packet, but its location is known only from the reviewers' private assignment. From the repository and GitHub alone, the hashes cannot be followed to their files.
- Required outcome: the section names where the packet is published (branch, pinned commit, path mapping, as lane B6 does) and where each hash table's rows are recorded.
- Verification: follow the page's pointer in a fresh clone and run `check_page_hashes.py` with 0 problems.

**RESIDUE-1 - lens: Docs - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1074`.** "all SUCCESS at its head `2bc5adc0`": 21 check runs are SUCCESS and "Physical gPTP (nightly and manual)"
is skipped (receipts/pr634_head_checkruns.tsv). Exact fix: "every executed check SUCCESS at its head `2bc5adc0` (the nightly physical gPTP context skipped)". This is wording only and changes no verdict.

**RESIDUE-2 - lens: Docs - the [A519] REVIEW READY comment on #629 (issuecomment-5969917459).** It says "12 live descriptors byte-equal", but `identity/identity-verdict.txt` grades 11
(plus the CLOCK_SOURCE 3 absence check), and the page names 11 correctly. Exact fix: a later comment reads "11 live descriptors". This is wording only, outside the diff.

**S1 - SUGGESTION - Tests, Docs - :1019-1024.** The capture-drift argument ("its packets are shortened by a frame about once a second") fits the two long losses but predicts about 0.2-0.4 % for the 155-
and 215-frame clusters. Cite instead A0 cluster 1, 18 frames off in 54 ms where the listener rate predicts 0.065 events. Also note that two of the five sit inside losses longer than the loop, and give the bound from zero visible events.

**S2 - SUGGESTION - RTL, Docs - :865-867.** A2's CRF-output MEDIA_RESET of 1 "right after its stream started, with no source change" is the documented counter rule. `KL_talker_diag_ctx.sv:176-181`
counts a first PDU after reset carrying `mr` = 1, and the shared restart level was odd after the shakedown's three source-change toggles. Cite it rather than "not analysed".

**S3 - SUGGESTION - Robustness - :932-938.** B-AAF is the only following case with the DUT's audio listener live, and its ring slipped one frame inside the graded window. Attach this observation, with its data,
to a named issue (#632, #386's recentre, or a new one) so the still-open Direction B metric inherits it.

## Reviewer ledger (R451-1)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #629 acceptance vs page :1067-1081. Lock-loss re-derivation vs design Lock loss and `mr` (IEEE 1722-2016 4.4.4.3 as the design reads it) and FR_NFR.md:238-239. CLOCK_DOMAIN C1 invariant. Milan v1.2 7.4 observation arithmetic. `Refs #629` in the PR body | R451-1 | 4eee41a558a56024e57b27a956fdaf7910ca69dc |
| RTL | CLEAN | No HDL in the diff (`git diff --stat`). Page's register-level claims decoded independently against REGISTER_MAP 0x738/0x748/0x8D4/0x8D8/0x8E0/0x8E4/0x8F8. Counter semantics vs `KL_talker_diag_ctx.sv:176-240` and `KL_crf_tx.sv:147-166`. AEM image regenerated from source equal to the DUT's | R451-1 | 4eee41a558a56024e57b27a956fdaf7910ca69dc |
| Robustness | CLEAN (S3 optional) | Lock loss (holdover, index kept, relock, tone path through it). Restore and read-back in all six cases. Census. The page's stated gaps (switch, CRF loss, power cycle, Direction B) checked as stated in :1079-1081 and :1083-1098 | R451-1 | 4eee41a558a56024e57b27a956fdaf7910ca69dc |
| Tests | UNCLEAN (F1) | Controls reproduced byte-equal plus 2 mutants. All six verdicts re-derived from `grade.json`, `events.csv`, `blocks.csv` and raw polls. Attribution re-applied and bounded. Pre-registration timeline vs `runs/a0/events.jsonl` (F1) | R451-1 | 4eee41a558a56024e57b27a956fdaf7910ca69dc |
| Docs | UNCLEAN (F1, F2) | Page :1-51 and :691-1162, README row. docs gates rc 0 in the pinned Markdown environment (docs_check, check_doc_style, gen_toc --check and --verify-anchors, check_em_dash --base bbf704ec and --selftest, check_doc_paths, check_feature_status --self-test). 45 page hashes checked. Privacy sweep of page and packet (no vendor, host, address, serial, MAC beyond the DUT's public default, channel map or home path; `McASP0` and `AX7101` are established public repository terms) | R451-1 | 4eee41a558a56024e57b27a956fdaf7910ca69dc |

## Real limits

- The raw captures (`cap-lr.raw`, `cap-ts.bin`, `samples.txt`) and `grade-full.json` are not published, so the audio was not re-decoded. The attribution and ratios are re-checked from the
  published grades and CSVs, whose internal consistency was verified, not from the raw samples. `grade_b7.py` and `run_b7.py` are masked, so the grader itself was not re-run.
- The BIOS ROM and QSPI payload CRCs were checked against `identity/expected.json` (the manager's build), not regenerated. Only the AEM image was regenerated from source.
- No hardware, no builder or simulation banks. PR #634's simulation evidence was taken from its hosted check runs.
- Timings are bracketed by 0.5 s console polls.

## Pending manager duties

- Hosted evidence at the exact head was read once: `rtl-fast`, `full-ci-gate`, `docs-check-no-git`, `bdd-conformance`, `wire-accountability`, `elaborate` and `changes` SUCCESS; `docs-check` in progress;
  the Verilator/Yosys contexts skipped by the docs-only scope. Hosted and act acceptance stay with the manager.
- Carry RESIDUE-1 and RESIDUE-2 to the residue checklist. F1 and F2 need a new commit and a re-review of the Tests and Docs lenses at that head.
- The final current-dev candidate validation at the merge turn is distinct from this source review.

## Receipts

Scripts: `rederive_b7.py`, `aem_from_source.py`, `check_page_hashes.py`, `attribution_bound.py`. Raw receipts under `receipts/`, all listed in `MANIFEST.sha256`.
Clone restored and verified: 994 of 994 tracked blobs and all modes equal the index; the index equals the HEAD tree; gitlinks are external `efeb541a`, gptp-processor `5dce647a`,
protocol-processor `631eeb34` and verilog-axis `48ff7a7e`; no untracked or ignored file (`receipts/restore_verification.txt`).

R451-1 FINISHED
