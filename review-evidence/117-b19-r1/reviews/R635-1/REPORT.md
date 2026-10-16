[R635] NEGATIVE - exact head 18b98bbcecf478b903610a07667f232d944d6feb

R635-1, external independent review of issue #117 / PR #751. Tree `b9e4e014079cc9497a51ccfc3870e086143b8816`. Three open findings prevent clean coverage. This verdict concerns the findings-only delta and its evidence; it does not establish a hardware defect.

## Scope and authorities

Reconstructed from the operating contract, CONTRIBUTING and documentation index, then frozen acceptance/public scope decisions, requirements/interfaces, diff/history and public evidence. The range `734eb780dc93896a5961cd95180f79475a401650..18b98bbcecf478b903610a07667f232d944d6feb` contains one commit, two Markdown files and 425 added lines. No implementation, configuration, test or submodule pin changes.

The [assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6207451080) governs this round. The [recovery decision](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5795898094) supplies the five-second bound and one further stream restart. The [enumeration decision](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5858063707) permits headless enumeration. The #387 public decisions define the offset stimulus; the [PHC-only restart exclusion](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859297355) supersedes the old step-only restart rule. The assignment explicitly assigns the render re-base count to simulation.

Authorities examined: `REQUIREMENTS.md` REQ-CSR-02 and REQ-PTP-05/07/08/09; `docs/design/GM_LOSS_RECOVERY.md` detection, ordering, recovery bound and media re-base; `docs/design/TIME_SYNC.md` step policy; `docs/testing/726_STREAM_COUNTERS.md` counter contract; `docs/testing/TESTING.md` sections 6b/6c; `sw/firmware/milan_baremetal/milan_baremetal.c:1896` status-read interface.

Evidence paths below are relative to [the pinned public packet](https://github.com/kebag-logic/milan-fpga/tree/2c4ca68a1d0b63651942ce2510f4fa5d19e944ab/review-evidence/117-b19-r1). All 249 published manifest entries match their published SHA-256 values. Original and scrubbed hashes are distinguished. Author narrative handoff material and other reviewers' reports were not used to derive this verdict.

## Findings

### R635-1-F1 - MAJOR - Docs

Artifact: `docs/findings/387_SOFTWARE_GM_STEP.md:445`.

Authority/evidence: CONTRIBUTING section 6 and the public-text rule prohibit identifying private bench hosts. This added line publishes the controller host's literal clock identity. The corresponding `author/bench/gm02/analysis.json` and `author/summary/gm-steps.json` use a neutral controller-host placeholder in the public packet. The reviewer receipt prints only the location and presence, never the identifying value.

Impact: the new public findings disclose a private host identifier. This touches the privacy rule and cannot be RESIDUE.

Required outcome: replace the literal with a neutral role label, preserving priority and stepsRemoved measurements. Scrub the reviewed delta and PR text consistently, including equivalent representations.

Verification: rerun the targeted identity-presence check and documentation privacy gate, then inspect all added text. The current gate passes despite this literal; gate success alone is insufficient.

### R635-1-F2 - MAJOR - Conformance, RTL, Robustness, Tests, Docs

Artifacts: `docs/findings/117_GPTP_SILICON_EVIDENCE.md:864`, `:821`, `:968`, `:975`; `author/bench/cycle01/correlation.json`, `cycle03/correlation.json`, `cycle05/correlation.json`; `author/tools/corr_analyze.py`; `sw/firmware/milan_baremetal/milan_baremetal.c:1910` and `:1938`.

Authority/evidence: box 3 and REQ-PTP-07/08 require honest wire/publication correlation. The summary and verdict say every cause or timeout lies inside its console interval. Recomputing that predicate gives these counterexamples:

| Event | Last-before / first-after (s) | Cause or timeout (s) | Result |
|---|---|---|---|
| Cycle 1 GM loss | 3.4836 / 3.7338 | last Announce 0.4734 + 3 = 3.4734 | 10.2 ms before bracket |
| Cycle 3 GM return | 41.2527 / 41.5027 | accepted Announce 41.2436 | 9.1 ms before bracket; 259.1 ms to changed sample |
| Cycle 5 GM return | 40.2519 / 40.5020 | accepted Announce 40.2482 | 3.7 ms before bracket; 253.8 ms to changed sample |

The detail row acknowledges the last two exceptions, while the overall PASS still asserts universal containment. More fundamentally, the placement method treats `TAI_NS` as the instant of the health/identity reads. The firmware reads those registers first, performs two formatted output calls, and only then calls `gettime_ns()`. It does not atomically timestamp those earlier reads. The analyzer supplies no bound or correction for that separation. Cross-host calibration spread does not measure this internal sampling skew.

Impact: an architectural observation-interface assumption and unchecked interval exceptions undermine the claimed one-sample proof for timeout and return paths. This is not evidence that hardware violates the protocol or the five-second recovery bound. All three first wire `tu=1` PDUs are inside their reported loss brackets.

Required outcome: reconstruct register observation intervals with a justified timing/error bound, check every loss and return against that model, and regenerate the table and verdict. If the receipts cannot establish the stated bound, mark that portion unproved and retain the measured limits. Processing time cannot silently justify a universal containment claim that the receipts contradict.

Verification: enumerate every assessed edge, reject an out-of-bound planted event, explicitly account for the separation between register reads and PHC sampling, and reconcile these three counterexamples and the PR summary. This review prescribes neither a source fix nor a new hardware action.

### R635-1-F3 - MINOR - Conformance, Tests, Docs

Artifacts: `docs/findings/387_SOFTWARE_GM_STEP.md:420`, `:423`, `:425`, `:429`, `:431`, `:455`; `author/bench/gm01..gm05/analysis.json`; `author/tools/a624_analyze.py:303`; `author/tools/gm_summary.py`.

Authority/evidence: the page defines `tu set` as the first console sample with `tu` set. Four rows skip that first sample:

| Run / edge | First `tu=1` in health history | Published `tu set` |
|---|---:|---:|
| 1 / takeover | 3.756 | 4.006 |
| 2 / release | 50.523 | 50.773 |
| 3 / release | 50.524 | 50.774 |
| 5 / release | 50.449 | 50.699 |

Each error is one 0.250 s sample. The analyzer selects its search window from a rounded PHC-step bracket instead of directly using the `tu` transition. It also publishes the end of the clear sample's command as `tu_steady_clear`, whereas health transitions use the start: all ten clear times differ by approximately 31-32 ms. Reproducing the summary gives byte-identical published JSON and Markdown, so this is an evidence-derivation discrepancy.

Impact: the table and derived timing comparison do not measure the observables they claim. These figures support the holdover discussion, so this changes measurements and cannot be RESIDUE. Separate wire episodes remain above 0.25 s in the published summaries; no actual short holdover is alleged.

Required outcome: derive assertion/clear times from complete transition history using one stated timestamp convention and observation uncertainty; regenerate affected rows and duration claims. Distinguish wire episodes, sampled console edges and command-completion times.

Verification: compare every generated edge time against health history, including these four cases. A boundary control must ensure rounded step brackets cannot discard the first asserted sample. Recheck the minimum-holdover claim using declared observation bounds.

### R635-1-R1 - RESIDUE - Docs

Artifact: PR #751 body, Status paragraph.

Authority/evidence: the body says the head is local and "Not pushed", although it is the published review head.

Impact: stale workflow wording only; no measurement, conformance, generated artifact or privacy claim changes.

Exact fix: replace "Not pushed. Independent review is pending." with "Published for independent review."

Verification: read back the body after the manager applies the wording change. This item does not leave a lens unclean.

### R635-1-R2 - RESIDUE - Docs

Artifact: `docs/findings/117_GPTP_SILICON_EVIDENCE.md:988` and the corresponding probe-parity wording in the PR body.

Authority/evidence: the two counters-probe logs differ only at line 4, which identifies the target entity. Every result line agrees. Thus "the same transcript line for line" is unnecessarily literal.

Impact: wording only; the measured parity and verdict remain valid.

Exact fix: use "identical result lines; the target-identity line differs" in place of the complete-transcript equality claim.

Verification: compare the two logs, requiring the sole differing line to be the target-identity line. `receipts/support-checks.txt` records this comparison. This item does not leave a lens unclean.

## Assignment evidence

| Item | Examined artifacts and result |
|---|---|
| Image and identity | [Manager provenance](https://github.com/kebag-logic/milan-fpga/tree/bbc53aabb02a1654812ba2eaa1642f5e36e69ce0/review-evidence/645-b18-r1/manager-provenance): source `9ef717727e6fdac11ee7f01672fefae948452343`, selected build, descriptor size/hash, flash verification and cold-boot CRC. Examined provenance, flash layout/log and boot receipt. Current initial/closing identity transcripts and 11-check verdicts agree. Initial identity precedes OUT0. VERSION alone is not source identity. |
| First reach | `author/bench/firstreach/events.jsonl`, boot transcript and `author/firstreach/analysis.json`: one OUT0 cycle, first-frame/Pdelay/Announce sequence and first AECP answer already asCapable. Events show polling immediately returning to passive mode. The precise DUT edge is inferred; AECP provides an upper observation bound. The page discloses this limitation. |
| Retention | `author/bench/retention/retention.json`, turnaround and wire summaries: 1,200 healthy console samples, 300 DUT/peer polls, 372-391 ns delay, cadence counts and DUT turnaround at most 13.432 us. One switch answer exceeds 15 ms and is disclosed. Bare-metal ownership and process checks support no daemon. |
| Switch cycles | Six event logs each contain one OUT4 off/on pair; other outlet reads stay on. Cycle 1 records continued console service and peer availability. Correlation receipts yield recovery 1.4930, 0.6322, 1.7680, 0.7452, 0.5039 and 0.4735 s. Bound-stream cycles show one restart and peer relock. Five-second health recovery and the additional stream restart remain distinct. |
| Publication | All three first CRF `tu=1` loss PDUs fall inside reported console brackets. Compared GM/parent/path and controller transitions. F2 prevents accepting the stronger universal timing claim. No write-based health manufacture is introduced by the diff. |
| Counters / enumeration | `author/box4/` probe transcripts, three run logs/entity trees/inventories: identical probe results, DUT compatibility, 42 descriptors, no DUT complaint/query error; peer complaints disclosed. `author/bench/retention/avtpdu-parity.json`: 149,514 CRF counts versus 149,499 tapped PDUs within stated window uncertainty, not literal equality. AAF receive coalescing matches the counter contract. |
| Ten GM edges | Five analyses and reproduced summary: one signed PHC jump per edge, one console/wire uncertainty episode, one GM_CHANGED, unchanged outgoing CRF `mr`, flat DUT talker and peer CRF listener MEDIA_RESET and listener unlock counts. Peer AAF resets are disclosed. F3 affects timing. DUT INTERNAL/idle CRF servo is explicit; no DUT CRF-servo-lock proof is claimed. Render count is simulation-owned by decision. |
| Restore | Starting/closing censuses and compare receipt: 46 entries, 41 equal, five differences comprising live delay and reallocated multicast destinations in transmit/receive state. Music/CRF bindings, formats/maps, clock sources and outlet reads agree. Controller receipt records zero frequency correction, timestamping off, no daemon and 4.5 us trajectory residual. Saturated slip counter and reclaimed addresses remain disclosed. |
| Public text | Complete two-file addition and PR body examined; F1 remains. No source comment is added in the reviewed delta, so the source-comment lane-label rule has no new in-tree instance. Historical findings remain dated records. |

## Reviewer-owned ledger

Every lens was independently applied. An unchanged implementation does not make the architectural lens clean when the evidence misinterprets its observation interface.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F2, F3 | Assignment; REQ-PTP-07/08; recovery/step authorities; both new sections; cycle/GM receipts | R635-1 | 18b98bbcecf478b903610a07667f232d944d6feb |
| RTL | UNCLEAN: F2 | Two-file diff/unchanged pins; status-handler register/PHC ordering; correlation method's interface assumption | R635-1 | 18b98bbcecf478b903610a07667f232d944d6feb |
| Robustness | UNCLEAN: F2 | Six timeout/return brackets; boot reader failure; ten step edges; outage/restore/reset receipts | R635-1 | 18b98bbcecf478b903610a07667f232d944d6feb |
| Tests | UNCLEAN: F2, F3 | Analyzer/checker sources; manifest audit; interval controls; table reproduction; health-history cross-check; focused gates | R635-1 | 18b98bbcecf478b903610a07667f232d944d6feb |
| Docs | UNCLEAN: F1, F2, F3 | Complete addition, PR body, authority links, provenance, methods, labels and privacy | R635-1 | 18b98bbcecf478b903610a07667f232d944d6feb |

## Execution, limits and manager duties

Reviewer receipts: `receipts/packet-audit.txt`, `receipts/local-checks.txt` and `receipts/support-checks.txt`. Diff whitespace, documentation, style and path checks passed. Both GM summary artifacts reproduce byte-identically. Initial/closing identity verdicts and the census comparison also reproduce byte-identically; both planted CRC mismatches are rejected. The counters-probe comparison found only the target-identity line differs (R2). The interval checker exercises boundary/outside controls. These checks validate published observations; they do not regenerate unavailable captures.

Source-head gate evidence is the author's `author/gates/gates.txt` and eleven logs at this exact head. No manager source bank is claimed. This reviewer ran no exhaustive bank, build, hardware operation or hosted/local workflow replica. Hosted execution versus skipping and workflow acceptance remain the manager's duty; no skipped context is counted as executed evidence.

The public raw index names 151 files and says 54 large files are held separately. Full cycle/retention/GM console records, controller transcripts and captures are absent from this packet. Full raw-to-summary replay and individual packet inspection were therefore unavailable. Hashes identify named artifacts, not their unseen contents. Sampled no-loss observations cannot exclude every shorter inter-sample event. Physical calibration NOT RUN and field skips remain limits, never hardware proof.

Manager duties: resolve findings and publish corrected evidence for re-review; apply residue wording; complete independent review; validate the then-current-dev merge candidate with required builder/native banks and hosted/local acceptance; publish post-merge containment after any authorized merge. Source base `734eb780dc93896a5961cd95180f79475a401650` and stated live dev `4a9b5a2a74fe793a637745fd3ccf51ad2eaf93b4` are distinct. This review approves neither a merge candidate nor closure of remaining #117 rows.

Integrity: all 1,371 tracked blob bytes/modes match HEAD; index equals the exact tree; six required gitlinks match; working tree clean. Submodule contents are uninitialized and were not executed. No tracked source was edited, so no restoration was needed. No GitHub write was performed.

Prior public finding reconciliation: after writing the independent verdict and ledger, queried PR issue comments, formal reviews and inline review comments. There were two review-start notices, zero formal reviews and zero inline comments, and no prior public findings to resolve or retain. See `receipts/prior-findings.txt`. No other review report was read.

R635-1 FINISHED
