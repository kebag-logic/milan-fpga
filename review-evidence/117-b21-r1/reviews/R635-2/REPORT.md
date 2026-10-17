[R635] POSITIVE - exact head 75853d80c22893448936bd1890e782bd0a0ce642

R635-2, external review of issue #117 / PR #758. All five lenses are technically CLEAN for this delta. The four R635-1 findings and three R634-1 findings are resolved at their causes. No BLOCKER, MAJOR or MINOR remains from this review. Three wording residues and the remaining optional suggestions are recorded below. This accepts the measured findings and corrected evidence, not the product release or a merge.

Tree: `02e138dde9cad84cac346fe3d0d0bc35d61be435`. Source base: `4a9b5a2a74fe793a637745fd3ccf51ad2eaf93b4`. The complete PR changes only `docs/findings/117_AUDIO_CONTINUITY.md` (+797 lines); this round is one commit on `867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b`, +232/-57. No RTL, firmware, interface, configuration or gitlink changes.

Review process limitation: after the independent diff pass, I retrieved the authorized prior public findings from comments 6231731098 and 6231778265. The returned full comment bodies also included their supporting report and ledger text, before this round's verdict was written. That exceeded the requested findings-only sequencing. No current-round report from another reviewer, private author material or lane scratchpad was consulted. The manager must decide whether this procedural deviation requires a replacement independent review; the technical verdict rests on the reproduced evidence below.

Scope and evidence

Authorities examined: AGENTS.md; CONTRIBUTING.md; docs/README.md; issue #117's frozen acceptance; the [inherited audio assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5925737609), [current measurement assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6208207821), [round-2 correction assignment](https://github.com/kebag-logic/milan-fpga/pull/758#issuecomment-6231784136), and [direct McASP capture decision](https://github.com/kebag-logic/milan-fpga/issues/625); REQUIREMENTS.md section 8; TIME_SYNC.md:507; REGISTER_MAP.md:149, :1878 and :2028. Scope remains the audio-continuity row on installed image `9ef71772`. The other #117 rows and deferred physical obligations remain open.

Executable evidence is pinned at [68f0200e, review-evidence/117-b21-r1](https://github.com/kebag-logic/milan-fpga/tree/68f0200e64ce3e631cb38a920e62134656d0132d/review-evidence/117-b21-r1). Paths beginning `author-r2/` below are relative to that archive. The public `MANIFEST.json` verified all 447 `author-r2/` files against `published_sha256`, with zero mismatches. Ten selected cold-archive inputs were read-only and matched their published SHA-256 values. The regenerated Direction B received-frame file also matches its published 499,116,000-byte hash. These are hash/provenance checks, not a claim of a separate cryptographic signature or of verifying every retained raw.

The revised computations were replayed with the published scripts. Independent campaigns ran concurrently, with at most three campaign workers and one numerical-library thread per process. The full Direction B grade and exact comparison were both executed. No broad implementation bank was rerun. The unchanged implementation retains its prior RTL result; changed counter and timing interpretations were checked afresh.

Prior finding dispositions

| Prior finding | Disposition at this head | Cause-level evidence |
|---|---|---|
| R635-1-F1, MAJOR; Conformance, Tests, Docs | RESOLVED | Page :1095-1134 and :1210-1245; `author-r2/tools/pr2/b21_restart_bound.py`; timestamp producers `tools/restart_b21.py:34,66-100` and `tools/selftest_b21.py:68-82`; `receipts/bound-as-measured.json`, `restart-controls.json`, `clock-controls.json`, `comparison.json` |
| R635-1-F2, MAJOR; Conformance, Robustness, Tests, Docs | RESOLVED | Corrected `tools/pr2/b21_grade.py:194-298` compares original words for candidate windows and runs, then checks assigned words again. All 30,480,000 captured frames compare exactly at offset 148,874. Collision is rejected. `receipts/direction-b-mcasp.json`, `direction-b-exact.json`, `grader-controls.json` |
| R635-1-F3, MINOR; Robustness, Tests | RESOLVED | Initial offset is saved when alignment succeeds, independent of event order. The isolated insertion control completes with three foreign zero frames, one offset change and three inserted frames. The archived as-run grader still crashes. `receipts/grader-controls.json` |
| R635-1-F4 and R634-1-F1, MINOR; Tests, Docs | RESOLVED | Page :946-960 states eight positive groups and one negative group, with signed values and a qualified association. Replay agrees with all nine printed groups. `receipts/floor-groups.txt` |
| R634-1-F2, MINOR; Tests, Docs | RESOLVED | Transit fit, CRF per tap, repeated-frame statistics and isolated grader controls now have executable public computations and matching outputs. `receipts/transit-crf.json`, `direction-b-exact.json`, `grader-controls.json`, `comparison.json` |
| R634-1-F3, MINOR; Tests, Docs | RESOLVED | Page :659-673 states 17/20 above the respective control maxima; exceptions are +6.8, -5.2 and +7.8. Independently counted from retained public loss lines. `receipts/comparison.json` |
| R634-1-R1, Docs | RESOLVED | Page :869, :946 and :1179 says permanent step and 111-read windows (`B5_W=110`). |
| R634-1-R2, Docs, RTL | RESOLVED | Page :1011-1016 and :1077-1082 uses AVTPDUs, names TIMESTAMP_VALID, and explains the FRAMES_RX commit interval. This agrees with REGISTER_MAP.md and preserved counter receipts. |
| R634-1-R3, Docs | RESOLVED | Page :1051 says sequence number, timestamp and payload, matching the actual comparison. |
| R634-1-R4, Docs | RESOLVED | Page :1346-1349 distinguishes original and published hashes for the three masked shell scripts. |
| R634-1-R5, Docs | RESOLVED | Page :758-762 uses past tense and records the loss of round-1 raws. |
| R634-1-S1, Robustness, Docs | APPLIED | Page :1032-1037 and :1192-1197 limits Direction B to observed -2 through +1 LSB values and excludes full-scale coverage. The +1 value occurs 23 times. |
| R634-1-S2, Tests | APPLIED | Page :962-969; `b21_step1_verdict.py` emits CLEAN only when all four checks hold. Nine planted losses all produce NOT CLEAN. `receipts/step1.json` |

No submitted reviews or inline review comments supplied additional prior findings at inspection. The prior public findings are resolved individually above; their old NEGATIVE verdicts are not approval of the fixes.

Restart endpoint and clock assessment

The upper bound is sound for the recorded cycles. Both timestamp producers run on the bench host: the driver logs `binding-rule` with `time.time()` before writing the bind request to the controller session; the capture reader takes its realtime timestamp after the read returns. The orchestration script launches both locally. Thus the command is sent after the starting timestamp, and the peer emitted the captured valid frame before the ending timestamp. Command service, presentation delay, peer buffering and capture delivery are inside that elapsed interval. There is no unknown steady output latency to add to this upper bound.

The peer-link lower bound is independently conservative: it starts when the command reaches that tap and ends when the packet carrying the first captured frame reaches the tap. Both events precede the corresponding peer actions. The first output frame's counter is in the first post-command AAF packet in all 20 cycles. There are exactly 20 recorded silences, commands, responses and binds, with no retries; the records support the pairing.

All 19,001 read timestamps cover the cycle sequence, have increasing frame counts and increasing realtime, and span 190 seconds. Realtime-minus-monotonic varies by 29.564 microseconds. Independent +2 ms and -2 ms timestamp-step controls are refused before tap access. This supports the recorded common-clock basis; it is not oscillator calibration or proof that an arbitrary unobserved clock disturbance is impossible. The large margin to one second is not sensitive to the reported sub-millisecond clock tolerance.

| Replayed quantity | Result |
|---|---|
| Upper bounds, min / median / max | 27.511 / 33.5025 / 100.725 ms |
| Lower bounds, min / median / max | 23.158 / 23.7205 / 96.727 ms |
| Mechanical table | All 20 lower bounds, upper bounds and widths match the page at printed precision |
| First post-rebind frames | First 480 valid and in order in every cycle |
| Added output latency 0.5 s | PASS; maximum upper bound 600.713 ms |
| Added output latency 0.903 s | FAIL, cycle 19 only; maximum 1,010.719 ms |
| Added output latency 1.0 s | FAIL, all 20; maximum 1,100.714 ms |

The controls shift samples relative to the unchanged read-time record, so the verdict depends on the delayed output endpoint. Read quantization means a planted delay need not add exactly its nominal value to every upper bound. The failing sets match the stated predictions. These controls address the prior excessive-latency counterexample; they do not claim exhaustive arbitrary-delay pairing coverage.

The old wire and relative-output figures remain explicitly historical. The new record also explains why the old formula was incomplete: 486-540 frames remained on the wire after the last frame played before silence. Those figures no longer discharge the restart criterion.

Other reproduced figures

| Measurement | Result | Receipt |
|---|---|---|
| Corrected Direction B grade | 30,480,000 matched; offset 148,874; zero foreign, skipped, inserted, unaligned or unequal frames | `receipts/direction-b-mcasp.json` |
| Exact comparison without hash alignment | Unique 64-frame initial match at 148,874; all 30,480,000 frames compared; zero unequal | `receipts/direction-b-exact.json` |
| Seven grader controls | Clean stays clean; skip 6, repeat 1, insertion 3, bit flip, zero replacement and unequal-word/equal-key collision classified as expected | `receipts/grader-controls.json` |
| Noise statistics | 6,437,039 adjacent equal frames (21.1%); 6,371,968 all-zero frames (20.9%); values -2, -1, 0, +1 LSB | `receipts/direction-b-exact.json` |
| Short floor groups | Eight positive, +6.3 to +8.4; one negative, -2.5 at reads 57,646-57,845; drift +2.304 | `receipts/floor-groups.txt` |
| Sampler association | 610 wakes; longest interval 1.040 s; both signs follow the deepest-dip comparison in all nine groups | `receipts/floor-groups.txt` |
| Step 1 mechanical check | CLEAN; largest adjacent block-floor change 2.81 frames, limit 4; all nine 6/12/48-frame plants caught | `receipts/step1.json` |
| Direction A transit | 5,198,372 aligned pairs; -13.070107 ppm fitted difference; residual -27.681 to +23.894 microseconds | `receipts/transit-crf.json` |
| CRF, DUT / peer taps | 324,903 / 324,906 packets; zero sequence breaks; 499.993 / 500.000 packets/s | `receipts/transit-crf.json` |

All seven replayed JSON results equal the published results after normalizing only input role labels where necessary. The floor text also agrees after label normalization. An initial receipt-comparison assertion caught those label substitutions in the input-description line; the numerical and group lines never differed. `receipts/comparison.json` records the final comparison and all 20 table checks.

New residues and remaining suggestions

**R635-2-R1 - RESIDUE - Docs - `author-r2/tools/pr2/` source docstrings.**

Authority/evidence: the owner requires new source comments to describe behavior and reason with issue/requirement IDs, without lane names or review rounds. Seven new modules start with `Lane B21 PR round 2:`: `b21_restart_bound.py:2`, `b21_restart_controls.py:2`, `b21_probes.py:2`, `b21_exact.py:2`, `b21_transit_crf.py:2`, `b21_floor_groups.py:2`, `b21_step1_verdict.py:2`. The corrected `b21_grade.py:4,7` adds round-specific provenance. New floor/step-1 docstrings also use a predecessor lane label at :9 and :11 respectively.

Impact: source-comment provenance wording only; no measurement, computation or verdict changes. The repository diff itself adds no executable source comments. Existing unchanged decoder/as-run comments are not newly filed here.

Required outcome: replace each of the seven new header prefixes with `Issue #117 audio-continuity evidence:`. In the corrected grader, replace `PR round 2 version. The mcasp grade now accepts` with `For issue #117, the McASP grade accepts`; remove the sentence about the as-run round-3 version. In the two new floor/step-1 docstrings, replace `lane B5's` with `the inherited #117`. Keep historical version provenance in the findings page and packet metadata, and preserve the archived as-run files.

Verification: inspect the new source-comment delta; refresh published hashes if source bytes are republished. No behavioral test change is needed.

**R635-2-R2 - RESIDUE - Docs - `docs/findings/117_AUDIO_CONTINUITY.md:1100,1190`.**

Authority/evidence: the correct computation measures variation of realtime-minus-monotonic, and the table bounds command-to-first-output elapsed time. The prose says realtime “stayed within 0.03 ms of its monotonic clock” and calls the bounded quantity the first frame's “output latency.”

Impact: terminology can be read as equality of clock epochs or as a separately measured wire-to-output delay. The formulas, endpoint definitions, values and PASS remain correct.

Required outcome: replace the first phrase with `whose difference from the monotonic clock varied by less than 0.03 ms over the capture`. Replace the second sentence with `The true command-to-first-output elapsed time lies between the bounds; their separation includes controller-session and capture-delivery delays.` This clarifies the already defined quantity without adding a latency measurement.

Verification: compare wording against `receipts/clock-controls.json` and `bound-as-measured.json`; no figure or verdict changes.

**R635-2-R3 - RESIDUE - Docs - PR #758, Known limitations, final bullet.**

Authority/evidence: the PR still says the external capture “does not grade the row.” The new restart subsection correctly uses that capture to bound the required output endpoint; the statement was intended to distinguish the continuity grading path.

Impact: an overbroad noun obscures the roles already stated correctly in the PR's restart table. It does not alter the executed measurement or its result.

Required outcome: replace that clause with `it is a continuity cross-check; its timestamped output record also supplies the restart upper bound`.

Verification: the limitations and restart sections then describe the same existing evidence.

**R634-1-S3 - SUGGESTION - Docs - page's resume-scope paragraphs and :854-858.** Retained optional. Link the [#625 owner decision](https://github.com/kebag-logic/milan-fpga/issues/625) where the direct-McASP resume terms are stated. The public decision exists and was checked; the missing local link affects navigation only. Verify the link reaches that decision.

**R634-1-S4 - SUGGESTION - Robustness, Docs - page :1198.** Retained optional. Repeat in the limits that the DUT used INTERNAL and the peer followed the DUT's CRF. Those conditions are already in the as-found table. Verify that any added sentence agrees with that table; no broader configuration coverage is implied.

**R634-1-S5 - SUGGESTION - Robustness, Docs - round-3 tap coverage wording.** Retained optional. State explicitly that continuity claims concern written capture windows; packet counts received by the capture filter at shutdown are not identical to written counts. Prior unchanged evidence records this tail distinction and no in-record gap. No new loss is alleged. Verify any added wording against the existing tap shutdown receipts.

Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #117 acceptance and assignments; REQUIREMENTS.md:317; page :866-875, :1095-1134, :1210-1272; timestamp producers; restart and exact-word replay receipts | R635-2 | 75853d80c22893448936bd1890e782bd0a0ce642 |
| RTL | CLEAN | Full/delta file inventory; REGISTER_MAP.md:149, :1878, :2028; TIME_SYNC.md:507; page :1011-1016, :1077-1082; `receipts/head-integrity.json`. No implementation or clock-domain contract changes; prior implementation verdict retained | R635-2 | 75853d80c22893448936bd1890e782bd0a0ce642 |
| Robustness | CLEAN | Corrected McASP grader :194-298; collision/skip/repeat/insertion/foreign controls; restart delayed-output and clock-step controls; noise and measurement limits | R635-2 | 75853d80c22893448936bd1890e782bd0a0ce642 |
| Tests | CLEAN | Eight revised analysis modules; ten hash-checked raw inputs; `receipts/replay-status.json`, `comparison.json`, `clock-controls.json`; seven grader controls and nine floor plants | R635-2 | 75853d80c22893448936bd1890e782bd0a0ce642 |
| Docs | CLEAN | Page delta and current PR body; source-comment delta; assignments; archive manifest; hash explanation; exact-head author gate receipts; all named prior findings | R635-2 | 75853d80c22893448936bd1890e782bd0a0ce642 |

[R635] PASS Conformance - page :1095, :1210; restart producer code and replay receipts - command-to-valid-output criterion and exact-word criterion now have matching evidence.

[R635] PASS RTL - REGISTER_MAP.md:149, :1878, :2028; TIME_SYNC.md:507; head-integrity receipt - counter units, saturation and media-boundary interpretations checked; no changed implementation requiring simulation.

[R635] PASS Robustness - grader-controls, restart-controls and clock-controls receipts - isolated negative inputs and delayed output change the expected verdict; scope limits remain explicit.

[R635] PASS Tests - replay-status and comparison receipts - revised computations reproduce, controls detect their intended defects, and all 20 printed restart rows match.

[R635] PASS Docs - findings delta, PR body, public archive manifest and exact-head source-gate receipts - substantive inaccuracies resolved; only listed residues and optional suggestions remain.

Real limits and pending manager duties

The author's `author-r2/pr2/gates-head/gates.txt` names this exact head and eleven successful invocations. Their individual receipts were examined and hashed; `comparison.json` identifies each. I additionally checked both complete-PR and round-2 diffs for whitespace errors. No manager source bank ran at this head, and none is claimed. No hosted or local workflow acceptance is inferred from these source receipts. Hosted contexts were not re-polled in this round; a skipped context would not constitute executed bank evidence.

There was no bench action, physical calibration, hardware access, source fix, commit, push, GitHub write, container run or merge. Physical calibration is NOT RUN; field skips and offline controls are not hardware proof. This round does not extend the recorded windows to other configurations, full-scale listener samples, upstream peer-source continuity, or all possible clock disturbances. Equal adjacent noise samples cannot reveal substitution between indistinguishable samples. The deficit-only self-test cannot establish arbitrary one-frame loss sensitivity or exclude corruption before the reader. Its 6-frame controls have only 0.58-1.82 frames of margin. Transit detrending is relative variation, not calibrated latency. Round-1 original raws remain lost; the old shortfall correction was checked against retained published computations, not missing raws.

Final integrity checks prove all 1,371 tracked blob bytes and modes, every index entry and all six gitlinks against the exact head. Submodules remain uninitialized as supplied; their source execution is not claimed. No source restoration was necessary because probes and generated data stayed in this packet's `scratch/`. Fetching the public evidence commit added objects and FETCH_HEAD only.

The manager must resolve the review-process qualification above, finish the other review, carry the residues, accept the final ledger, and validate the current-dev merge candidate with required builder/native banks. Source base `4a9b5a2a74fe793a637745fd3ccf51ad2eaf93b4` and stated live dev `1f6f2f57177f1dd904654c317009461b43423989` are distinct; use the actual live tip at the merge turn and publish candidate receipts. Hosted/local workflow acceptance, maintainer merge authorization and post-merge containment remain manager duties. This PR says Refs #117; passing the audio row does not close remaining issue obligations.

Portable replay commands (all remain in the foreground):

```sh
python3 replay.py "$PUBLIC_PACKET_ROOT" "$RAW_ARCHIVE" "$OUTPUT"
python3 clock_controls.py "$PUBLIC_PACKET_ROOT/author-r2" "$RAW_ARCHIVE/rA-ext" "$OUTPUT"
python3 compare_receipts.py "$PUBLIC_PACKET_ROOT/author-r2" "$CHECKOUT" "$OUTPUT"
python3 integrity.py "$CHECKOUT" "$OUTPUT/receipts/head-integrity.json"
```

`MANIFEST.sha256` lists publishable scripts and receipts. Everything under `scratch/` is disposable and excluded from publication.

R635-2 FINISHED
