[R635] POSITIVE - exact head c2243f791ced37dd2288dbf870758d93c5aa5325

External independent review R635-2 of issue #117 / PR #751. Tree `ece348805565c8c0b12bd6c90eccf512ef46c222`. All five lenses are CLEAN for the assigned delta. The named source findings are resolved against the round-2 assignment's required outcomes. No new BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION is raised.

This accepts the corrected findings and offline derivations, not a merge candidate, issue closure or new hardware proof.

## Scope and reconstruction

Read the operating contract, CONTRIBUTING and documentation index; issue #117's frozen acceptance and public scope decisions; linked requirements and interfaces; then diff/history and public executable evidence. The full range `734eb780dc93896a5961cd95180f79475a401650..c2243f791ced37dd2288dbf870758d93c5aa5325` changes only two findings pages, adding 509 lines. This round assesses the six correction commits after `d812a604`, the privacy amend of `18b98bbc`. No RTL, firmware, configuration, test or gitlink changes. Unchanged first-round content retains its assessment except where corrected derivations affect its dependencies.

Authorities: the [original assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6207451080), [round-2 assignment](https://github.com/kebag-logic/milan-fpga/pull/751#issuecomment-6208623939), #621 item 3, #387 item 4, REQ-PTP-05/07/08/09, `docs/design/GM_LOSS_RECOVERY.md:93-118`, `docs/design/GPTP_PLANE.md:96-163`, `docs/design/TIME_SYNC.md:76`, and `docs/testing/726_STREAM_COUNTERS.md`'s counter contract.

The [published author packet](https://github.com/kebag-logic/milan-fpga/tree/633b6e33244545b0dd5a1ef9a01fb96a0209d35e/review-evidence/117-b19-r1/author-r2) was extracted without opening review directories. The independent verdict and five-lens ledger were written before reading the two prior public review comments. No private author narrative, other checkout or current-round peer review was read. Prior findings were then reconciled below. There were no formal or inline PR reviews at reconciliation.

## Independent results

**Box 3:** `117_GPTP_SILICON_EVIDENCE.md:867-873,984-1016` now states the model and falsifiable criterion. The status handler reads publication words, prints two lines, then reads the PHC. The 271/272-byte output, 115200 baud and UART buffering justify separating those instants. Firmware and baud-configuration bytes equal the installed-image source. Pinned UART sources at `a1e1c3652ec2f1346ebaea7663d2867f393ae2c4` were checked for newline expansion, software-ring capacity, hardware buffering and transmit acknowledgement behavior.

Regeneration gives the published bounds and placement allowances exactly. All 27 assessed edges pass: six each of sync loss, GM loss, asCapable return and GM return, plus three first uncertain CRF PDUs. All eleven near-boundary entries match. The three former counterexamples are explicitly accounted for; the narrowest margin is cycle 1 GM loss, 0.66 ms, followed by cycle 3 GM return, 1.76 ms. The verdict follows the grader. asCapable loss and `tu` clear are distinguished as range observations rather than independently timed wire causes.

The 13 published box-3 controls pass. An independent probe moved each assessed cause/effect outside each boundary: all 54 cases fail, including the special 2 ms effect allowance.

**GM-step timing and poll grading:** `387_SOFTWARE_GM_STEP.md:425-461,484` uses console command-send timestamps consistently, with observation intervals, and distinguishes wire episodes. Independent full-history reconstruction agrees with all ten assertion and clear times. The four late assertions are corrected; all ten clear times move earlier by 31/32 ms. Steady-after-set is 0.25-0.75 s. Wire first-to-last asserted-PDU spans are 0.376-0.684 s, supporting the minimum-holdover observation independently of console sampling.

All ten edges pass. The nine published controls pass. Independent mutations of real controller records in takeover and release windows make the complete grading process return 1 and fail only the intended edge. Observed totals are 2,399 console samples and 600 answered DUT polls, zero asCapable-clear observations, and 373-392 ns peer delay in both sources. Edge windows contain 2,379 samples and 595 polls; five polls precede the takeover windows, as the page records. Aggregate observations and edge-window grading are distinct.

**Counter figures:** reproduction gives peer CRF input FRAMES_RX 149,513 over 300 polls. The 26 endpoint reads give lag 167-7,925; all 1,495 polls give 0-7,925, none negative. These figures now have executable derivations over retained raws.

**Integrity and provenance:** all 281 public author-r2 entries match publisher hashes, including 42 marked redacted. All 151 cold-archive raws match size and SHA-256, totaling 108,011,178 bytes. The retention comment contains all 54 large-artifact hashes. Both pages' bitstream and AEM hashes match pinned `provenance.json`. Continuity is explicitly supported by assignment item 8; VERSION/CRC are correctly described as non-distinguishing.

## Prior-finding disposition

Read [R635-1](https://github.com/kebag-logic/milan-fpga/pull/751#issuecomment-6208467023) and [R634-1](https://github.com/kebag-logic/milan-fpga/pull/751#issuecomment-6208603345) after the independent pass. Original finding lens ownership is preserved.

| Prior item | Original severity and lenses | Disposition and verification at this head |
|---|---|---|
| R635-1-F2 / R634-1-F2 | MAJOR / MINOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED. `117_GPTP_SILICON_EVIDENCE.md:867-873,984-1016`: model, 27 mechanically graded edges, eleven margins, corrected verdict. `box3-model.json`, `box3-grade.json`, `box3-controls.log`, `edge-boundary-probes.json`. |
| R635-1-F3 | MINOR; Conformance, Tests, Docs | RESOLVED. `387_SOFTWARE_GM_STEP.md:425-461,484`: full-history timestamps and uncertainty. `independent-tu.json`, `gm-steps-r2.json`, `gm-controls.log`. |
| R634-1-F1 | MINOR; Conformance, Docs | RESOLVED. `117_GPTP_SILICON_EVIDENCE.md:835-838`, `387_SOFTWARE_GM_STEP.md:374-381`: resolving provenance link, exact bitstream/AEM hashes, non-distinguishing reads and continuity receipt. `support-checks.json`. |
| R634-1-F3 | MINOR; Conformance, Tests, Docs | RESOLVED. `387_SOFTWARE_GM_STEP.md:386,415,461,482`, `117_GPTP_SILICON_EVIDENCE.md:1024,1029`: poll arm and published figures. `poll-process-probes.json`, `gm-steps-r2.json`, `box4-derivations.json`. |
| R634-1-F4 | MINOR; Conformance, Docs | RESOLVED. `117_GPTP_SILICON_EVIDENCE.md:1071-1077`, `387_SOFTWARE_GM_STEP.md:503-507`; [retention receipt](https://github.com/kebag-logic/milan-fpga/pull/751#issuecomment-6208612856), independently checked 151/151 raws and 54/54 large-entry hashes. `raw-verification.json`. |
| R635-1-F1 / R634-1-F5 | Originally MAJOR / MINOR; Docs | RESOLVED for explicit round-2 item 1. `387_SOFTWARE_GM_STEP.md:474` uses a role label. Five equivalent identity forms have zero matches under `docs/` and in the PR body. `privacy-check.json`. Existing archived exposure is addressed below under the accepted-exposure/no-history-rewrite decision. |
| R635-1-R1 / R634-1-R1 | RESIDUE; Docs | RESOLVED. Live PR body names the published exact head, open PR and assigned reviewers. |
| R635-1-R2 | RESIDUE; Docs | RESOLVED. `117_GPTP_SILICON_EVIDENCE.md:822,1023` and PR body distinguish identical result lines from the target-identity line. |
| R634-1-R2 | RESIDUE; Docs | RESOLVED. `387_SOFTWARE_GM_STEP.md:391-392` says the earlier +3 rise occurred at nine of ten edges. |
| R634-1-S1 | SUGGESTION; Docs | APPLIED. `387_SOFTWARE_GM_STEP.md:400` states that the current-image servo observable was not exercised; INTERNAL kept it IDLE and the earlier locked observation predates the correction. |

No new source-comment instance exists: the entire source delta is findings Markdown. Packet analysis scripts fall under the assignment's explicit exception allowing lane names there.

## Reviewer-owned ledger

Each PASS applies the lens to the correction and its affected dependencies.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | REQ-PTP-07/08; assignment 6208623939; `117_GPTP_SILICON_EVIDENCE.md:867-1029`; `387_SOFTWARE_GM_STEP.md:374-484`; regenerated edge/counter outputs | R635-2 | c2243f791ced37dd2288dbf870758d93c5aa5325 |
| RTL | CLEAN | Two-file delta; unchanged `milan_baremetal.c:1896-1938`; baud configuration; pinned UART buffering/newline implementation; `box3-model.json` | R635-2 | c2243f791ced37dd2288dbf870758d93c5aa5325 |
| Robustness | CLEAN | Six loss/return correlations; `box3-controls.log`; 54 boundary probes; `gm-controls.log`; two process-level poll faults; disclosed dark-link limits | R635-2 | c2243f791ced37dd2288dbf870758d93c5aa5325 |
| Tests | CLEAN | Four published analysis scripts; byte-identical outputs in `reproduction.json`; independent transition reconstruction; negative controls; raw/manifest audits | R635-2 | c2243f791ced37dd2288dbf870758d93c5aa5325 |
| Docs | CLEAN | Both changed sections and live PR body; provenance/continuity/retention receipts; source privacy check; author gate logs; prior-item reconciliation | R635-2 | c2243f791ced37dd2288dbf870758d93c5aa5325 |

## Reproduction and execution

Extract the pinned `author-r2` packet and parent `MANIFEST.json` into a disposable directory. Supply read-only access to the indexed raw archive. Portable scripts take explicit paths:

```sh
python3 reproduce.py "$AUTHOR_PACKET" "$RAW_ROOT" "$OUTPUT_PACKET"
python3 probes.py "$AUTHOR_PACKET" "$RAW_ROOT" "$OUTPUT_PACKET"
python3 audit.py "$REPOSITORY" "$AUTHOR_PACKET" "$PUBLIC_MANIFEST" "$OUTPUT_PACKET"
python3 privacy.py "$REPOSITORY" "$AUTHOR_PACKET" "$PR_JSON" "$OUTPUT_PACKET"
```

All six reproduction commands returned 0; four outputs match published bytes. Independent controls passed. The driver runs three independent small campaigns concurrently and waits for every result; dependent model/grade steps remain ordered. Disposable copies and mutations stay under `scratch/`, excluded from publication.

Source-head execution evidence is `author-r2/gates/round2/gates.txt` and eleven logs, all recording this head and rc 0. Logs confirm documentation/privacy, style, TOC, links/anchors and the 509-added-line check. The reviewer additionally ran the documentation/privacy and full-range whitespace checks successfully. No manager source bank is claimed. Hosted execution/skipping was not used as evidence.

Final integrity: all 1,377 tracked entries, blob bytes, modes and index records agree with the assigned tree. All six gitlinks match; submodule checkouts remain uninitialized and unexecuted. No tracked file needed restoration. `integrity.json` records the pins and audit. The evidence commit has no Git signature (`N`); verification is by object identity and SHA-256 manifests, not a cryptographic-signature claim.

## Real limits and pending manager duties

- The timing model is an engineering bound, not an instrument measurement. Its upper bound includes 1 ms formatting allowance; the narrow lower-bound result depends on UART capacity. Calibrated dark-link placement uses the measured within-action spread. Assumptions and sensitivity are explicit. Physical calibration was NOT RUN. Field skips are not hardware proof.
- No new hardware work occurred. Sampled no-loss observations cannot exclude every shorter inter-sample event. The current-image CRF servo remained IDLE; render re-base counting remains simulation-owned. First-reach precision, peer-link recovery, latency, audio and other acceptance rows retain their limits.
- Existing publication duty from R634-1 remains recorded: ten archived `author-r2/bench/gm01..gm05/ptp4l-{gm,slave}.log` files still contain the dotted host clock identity. `privacy-check.json` names files without printing the value. Round-2 item 1 expressly accepts earlier exposure, requires absence under `docs/`, and says no history rewrite and nothing further for that author item. This is retained as the existing manager publication matter, not relabelled RESIDUE or a newly introduced source defect. The manager should reconcile comment 6208484697's claim that the packet never carried it and preserve role-only wording in future publication.
- The manager owns completion of independent review, publication, hosted/local workflow acceptance, and validation of the final merge candidate against then-current `dev`. Source base is `734eb780dc93896a5961cd95180f79475a401650`; assigned live dev is `8eacc40839d95ff0e8cb26d0169cc1638800a44d`. Required builder/native receipts belong to that merge turn, not this source head. Any authorized merge still requires containment checks and remaining issue/release decisions.

Only `REPORT.md` and files listed in `MANIFEST.sha256` are publishable. No GitHub write, source edit, commit, push or bench operation was performed.

R635-2 FINISHED
