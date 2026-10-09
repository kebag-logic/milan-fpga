[R493] POSITIVE - exact head 173362fc21c33078b7feed42a24a3636907010f5

# R493-3 external independent review: issue #640 / PR #698

Tree: `fbc807d191d0c98f7fac332502e93f9c65c81138`.
Source base and assigned live dev: `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
Delta base: `7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783`.
[Public review start](https://github.com/kebag-logic/milan-fpga/pull/698#issuecomment-6082458212).

R492-2-F1 and R492-2-F2 / R493-2-R2 are **RESOLVED**.
No BLOCKER, MAJOR or MINOR remains in this review's scope.
All five lenses are CLEAN at the exact head above.
Previously resolved substantive findings remain resolved.
Previously open wording residue and optional suggestions remain explicitly listed below.
This approves the stage-1 documentation change, not the completed redesign or merge.

## Scope and independent reconstruction

Read the operating contract, contribution rules and documentation map first.
Then reconstructed [issue #640](https://github.com/kebag-logic/milan-fpga/issues/640), its stage-1 assignment and subsequent public decisions.
The issue's eventual acceptance remains a routed image at most 38,040 LUTs, passing timing and unchanged functional acceptance, with the reaching lane re-recording the resource gate.
The [stage-1 ruling](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5988586965) and [updated assignment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6080904058) authorize planning only.
The [measurement ruling](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081534590) and [memory assignment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081895732) further define this document's scope.

Checked the linked requirements, placement/mailbox contracts, resource records and source wiring before assessing the full base-to-head diff and history.
The full PR changes only `docs/design/MARK_II_AREA_PLAN.md` and `docs/design/AREA_BUDGET.md`.
The focused delta contains exactly one commit and changes only the plan:

- Remove the command prefix from the Tcl-writing fence.
- Remove that prefix from the lock-held execution fence.
- Insert one blank line after the final M3 basis row.

The byte-exact transformation assertion in `scripts/delta_probe.py` passes.
No other document bytes, measurements, figures, tests, RTL, interfaces, resource records, policy values or gitlinks change in this delta.
See `receipts/delta.patch`, `receipts/full-diff.patch` and `receipts/history.txt`.

`INDEPENDENT_PASS.md` records my verdict and five-lens ledger before reading prior reviewer reports or findings.
Prior public findings were read only after that independent pass.
No private author material or another checkout was used.
No source edit, commit, push, GitHub write, author contact or delegation occurred.

## Corrected findings

| ID | Original severity and attributable lenses | Exact-head disposition and verification |
|---|---|---|
| R492-2-F1 | MINOR; Conformance, Tests, Docs | **RESOLVED.** Plan:1167 and 1211 now begin directly with the required commands. The unchanged published `repro_block_probe.sh` runs the first fence as printed with a clean PATH: rc 0, Tcl written, 1,339 bytes, completeness 1. Both fences parse. Independent execution of both literal fences succeeds with a controlled synthesis-command stub. Failures at each of the three core invocations propagate into the recorded rc and stop the loop. Restoring the removed prefix causes exit 127. Case-insensitive whole-word search finds no prefix token in tracked repository text. |
| R492-2-F2 | MINOR; Docs | **RESOLVED.** Plan:838 is now the table separator. The unchanged published `render_tables.py` reports 30 plan tables and 0 absorbed prose rows. The M3 fragment contains exactly four data rows, followed by a paragraph holding all ten prose lines. The prior-head control contains fourteen data rows and no following paragraph. |
| R493-2-R2 | RESIDUE; Docs | **RESOLVED** by the same separator and render evidence. Every word and numeric statement after the table is preserved. |

Sources: [R492-2 findings](https://github.com/kebag-logic/milan-fpga/pull/698#issuecomment-6082400621) and [R493-2 findings](https://github.com/kebag-logic/milan-fpga/pull/698#issuecomment-6082437272).
The original severity/lens assignments are preserved; resolution removes their open status.

The published probe scripts were retrieved from immutable public revision `227c103a454872378049090b8226ac8203f646c4` and run unchanged.
Their provenance is recorded in `receipts/upstream-provenance.json`.
The older shell probe's prefix-word diagnostic assumes a prefix exists and now prints a misleading six-word count.
Its actual execution result, written Tcl and completeness result establish the requested closure.
The independent probe avoids that diagnostic assumption and also exercises the second fence.
It redirects the lock to a disposable scratch file while retaining real locking; synthesis is stubbed.
Neither probe supplies new area or timing measurements.

## Earlier finding reconciliation

Sources: [R492-1](https://github.com/kebag-logic/milan-fpga/pull/698#issuecomment-6081481326), [R493-1](https://github.com/kebag-logic/milan-fpga/pull/698#issuecomment-6081524243), and the two round-2 findings above.

| Prior ID | Severity / lenses | Disposition at this head |
|---|---|---|
| R492-1-F1 | MINOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED, unchanged: plan:967,984-1028 and budget:336-356 schedule manager-owned M0s tooling and both selected-placement routes before week 4 and the default flip. Missing measurement prevents a pass. |
| R492-1-F2 | MINOR; Conformance, RTL, Docs | RESOLVED, unchanged: plan:573-599 and budget:204-217 correctly name pre-packing cells, the unowned remainder, explicit assumptions and M8a repricing. Checked against the census at `649_RESOURCE_MAP_AND_SENSITIVITY.md:262`. |
| R492-1-F3 | MINOR; Conformance, RTL, Robustness, Docs | RESOLVED, unchanged: plan:876-952 and budget:288-330 price inclusive no-split and partial-flip cases, both LUT bars and the required further redesign. The published arithmetic checker passes 58/58. |
| R492-1-R1; R493-1-R1; R492-2-R1; R493-2-R1 | RESIDUE; Docs | RETAINED as long-prose residue below. The earlier requested replacements remain; the new table's separator defect is resolved. |
| R492-1-R2; R493-1-R2 | RESIDUE; Docs | RESOLVED for the identified references. Issue/file links remain; cited-path and anchor gates pass. |
| R492-1-R3 | RESIDUE; Docs | RESOLVED: plan:153,173-174,1119-1122 label and date historical measurements. Separate stale round wording remains below. |
| R492-1-R4 | RESIDUE; Docs | RESOLVED: the budget's redundant blank line remains removed. |
| R492-1-S1 | SUGGESTION; Docs, Tests | RESOLVED: plan:1137-1233 gives sources, digests and exact commands; the portability correction now passes execution probes. |
| R492-1-S2 | SUGGESTION; RTL, Docs | RESOLVED: plan:450-486 names surviving MAC/CSR FIFOs and exclusions. Checked against `milan_soc.py:805,1612,1672`. |
| R492-2-R2 | RESIDUE; Docs | RETAINED: stale round wording, exact fixes below. |
| R492-2-R3 | RESIDUE; Docs | RETAINED: redundant plan blank line, exact fix below. |
| R492-2-R4 | RESIDUE; Docs | RETAINED: optional command-prefix presentation in the PR's historical gate tables, exact fix below. Repository reproduction commands are fixed. |
| R492-2-S1 | SUGGESTION; Robustness, Docs | RETAINED, optional: cross-reference partial-placement memory pressure beside the LUT scenario row. Plan:797-802 already states 126.5 tiles and withholds full-split reclamation. Verification: compare the scenario and memory sections. |
| R492-2-S2 | SUGGESTION; RTL, Docs | RETAINED, optional: explicitly name the mixed-placement state face in the integration allowance. Plan:892-903 already requires single ownership and arbitration. Verification: inspect the allowance's scope without granting additional savings. |
| R492-2-S3 | SUGGESTION; RTL, Robustness, Docs | RETAINED, optional: price maximum M6/M7 RAM debits. Plan:764-765,791-795 already withholds unpriced capacity and requires repricing or redesign. Verification: reconcile any future debit with the unchanged ceiling. |

## Retained wording residue

These items do not change measurements, figures, verdicts, executable tests/code, generated artifacts, conformance claims or privacy rules.
They remain non-blocking RESIDUE under the assigned owner rule.
The manager carries them to the residue checklist.
No source fix was made here.

**R492-2-R1 / R493-2-R1 (continuing R492-1-R1 / R493-1-R1)**

- Severity: RESIDUE. Lenses: Docs.
- Artifacts: plan:700,812; budget:265; prior public sentence observations.
- Authority/evidence: `docs/README.md` requires current sentences under eleven words. These unchanged sentences exceed that limit; the style gate's selected population excludes these pages.
- Impact: readability only.
- Required outcome / exact fixes: at plan:700 use “The [F5 ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081705916) sets the linked-image limit at 224 KB.” followed by “That includes AECP.” At plan:812 use “The default flip requires firmware in block RAM.” followed by “The reserve must remain intact.” At budget:265 use “Five RX pools, MRP strip and TX slots give way.” followed by “So do timer, trace, RX validator and `ctl_fifo`.” Split remaining confirmed long sentences while retaining every value and qualification.
- Verification: inspect rendered prose and word counts; preserve every ledger and qualification claim.

**R492-2-R2**

- Severity: RESIDUE. Lenses: Docs.
- Artifacts: plan:148 and 1112.
- Authority/evidence: the document itself identifies the current revision as Round 1d at plan:4 and says no new measurement in Rounds 1b-1d at plan:72.
- Impact: stale narrative labels only.
- Required outcome / exact fixes: replace “not the Round 1b baseline” with “not the current baseline”; replace “Rounds 1b and 1c use committed records without new synthesis.” with “Rounds 1b-1d use committed records without new synthesis.”
- Verification: re-read those two sentences against the dated measurement notes.

**R492-2-R3**

- Severity: RESIDUE. Lenses: Docs.
- Artifact: plan:149-150.
- Authority/evidence: two consecutive blank lines remain after the historical-baseline introduction.
- Impact: source presentation only.
- Required outcome / exact fix: delete one of the two blank lines.
- Verification: the same paragraphs/headings and content render afterward.

**R492-2-R4**

- Severity: RESIDUE. Lenses: Docs. Retains the original classification.
- Artifact: PR #698 body, historical Round 1c/1d gate-command tables.
- Authority/evidence: the prior finding names 99 recorded commands with the optional host-local prefix. The body still contains that presentation, while its appended Round 1e section correctly describes the repository fix.
- Impact: avoidable host-specific presentation of historical receipt commands; the historical outcomes and checked-in reproduction are unchanged.
- Required outcome / exact fix: remove the optional prefix from each command cell, preserving arguments, recorded heads and results; alternatively explicitly label the prefix optional.
- Verification: inspect both command tables and keep receipt provenance unchanged.

## Reviewer-owned coverage ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #640 frozen acceptance and public decisions; REQUIREMENTS.md:25-52; FR_NFR.md:464; plan:49-106,697-813,954-1107,1137-1233. Targets, single ownership, conditional placement and exact reproduction checked. | R493-3 | 173362fc21c33078b7feed42a24a3636907010f5 |
| RTL | CLEAN | `receipts/full-diff.patch`, `delta.patch`; `milan_soc.py:805,1612,1672,2548`; `milan_datapath.sv:8003`; plan:406-448,450-486; resource record and #649 census. No RTL/interface/pin change; retained FIFO and idle-mailbox claims checked. | R493-3 | 173362fc21c33078b7feed42a24a3636907010f5 |
| Robustness | CLEAN | Plan:435-448,760-813,876-952,992-1028; `receipts/delta-probe.log`, `recompute.log`. Core rejection, failed reuse, packing, partial qualification, late/missing measurements, reserve enforcement and command failure propagation checked. | R493-3 | 173362fc21c33078b7feed42a24a3636907010f5 |
| Tests | CLEAN | `scripts/delta_probe.py`, published probes and all matching receipts; documentation gates; author receipt identities; `full-diff.patch`. Prefix-restored and old-table controls detect the actual defects. No executable-test delta. | R493-3 | 173362fc21c33078b7feed42a24a3636907010f5 |
| Docs | CLEAN | Both changed documents; plan:828-848,1137-1233; `receipts/m3-head.html`, render logs, path/anchor/privacy/style gates; prior-finding reconciliation. Correct rendering and portable commands; only retained wording residue. | R493-3 | 173362fc21c33078b7feed42a24a3636907010f5 |

CLEAN means applied with no open BLOCKER, MAJOR or MINOR in scope.
Optional suggestions and the explicitly retained wording residue do not unclean a lens.

## Execution and evidence limits

Focused checks pass at this head: documentation/privacy and its controls, feature status, selected-page style, cited paths, contents/anchors, added-line punctuation and its 339 controls, three-endpoint baseline validation, whitespace, independent delta/command/render probes, the two published probes, and the 58-check arithmetic recomputation.
The published table probe also passes on AREA_BUDGET: 9 tables, zero absorbed prose rows.
Every result has its own log and rc file.
The foreground controllers join all children; peak concurrency was eight lightweight checks.
All disposable files, dependencies and probe trees are under `scratch/`.

Reproduction, with `REPO` and `PACKET` set to absolute paths:

```sh
python3 -m venv "$PACKET/scratch/markdown-env"
"$PACKET/scratch/markdown-env/bin/python" -m pip install --require-hashes -r "$REPO/tools/markdown/requirements.txt"
"$PACKET/scratch/markdown-env/bin/python" "$PACKET/scripts/run_focused.py" "$REPO" "$PACKET" --jobs 8
"$PACKET/scratch/markdown-env/bin/python" "$PACKET/scripts/run_published_probes.py" "$REPO" "$PACKET"
python3 "$PACKET/scripts/check_integrity.py" "$REPO"
```

The independent stub probe is shell-behavior evidence only.
No current core netlist was synthesized and no historical area result was remeasured.
The original shared-lock probe was stopped while waiting; the completed stub probe uses a scratch lock.
An initial token search included incidental compressed-image bytes; the completed check searches tracked text, the relevant command population.
Neither setup correction changed repository bytes or relaxed a production gate.

The [specified public evidence tree](https://github.com/kebag-logic/milan-fpga/tree/994453e98aa8cea39e06534115ebebb258136767/review-evidence/640-r1) contains the older Round 1b receipt at `c4b8b7d3`.
The [later published Round 1d receipt](https://github.com/kebag-logic/milan-fpga/blob/227c103a454872378049090b8226ac8203f646c4/review-evidence/640-r1/author-r1d/ROUND1D-GATE-RECEIPTS.txt) names `7387bb6f` and reports 51/51 commands returning zero, consistent with the [author's public readiness comment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6082152872).
Receipt bytes and identities were checked; their underlying unpublished gate logs were not independently rehashed here.
Those attributed source receipts are not relabelled as execution at `173362fc`.
This packet's focused receipts cover the current exact head.
**No manager source bank ran at this head; none is inferred.**

`receipts/hosted-snapshot.json` and `hosted-jobs.json` record a single exact-head inspection.
Several jobs executed successfully, including lint, behavior conformance, wire accountability, documentation without Git, the selector and four synthesis shards.
The job-step records distinguish these executions from skipped contexts.
Documentation, elaboration, firmware and long simulation work remained in progress.
No final aggregate acceptance is claimed.
The physical job was skipped, with no executed steps.
**Physical calibration: NOT RUN. Field skips are not hardware proof.**

No full parent, processor, time-processor, synthesis or builder bank was run by this reviewer.
No local workflow replica, host orchestrator or orchestrator self-test was run.
No shared installation, privilege operation or hardware action occurred.

## Integrity and pending manager duties

Final verification checks tracked blob bytes directly against immutable Git objects, executable modes, complete stage-0 index entries and registered required submodule gitlinks.
It covers 1,233 parent blobs, 562 protocol-processor blobs, 104 gPTP-processor blobs and 214 stream-library blobs.
Required pins:

- `protocol-processor`: `2ad2f845dd583f8310075fa2380cb60a04fd091a`.
- `gptp-processor`: `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`.
- `third_party/verilog-axis`: `48ff7a7e2ef782cf778d47910cf85835c64b1bce`.

Unused external and lwSRP worktrees remain uninitialized.
The clone remains detached at the exact head and clean.
No restoration was needed because all mutations used disposable copies.

The manager still owns publication, residue tracking, the other independent review and ensuring no review remains in flight.
Hosted and local-replica acceptance remain manager duties.
At the merge turn, the manager validates the current-dev candidate with builder/native banks and links its receipts on the PR.
Source validation is distinct from that final candidate validation.
The assigned source base and live dev match; no future candidate receipt is claimed here.
Explicit merge authorization, post-merge containment and workflow updates remain required.

M0s routes, F5 integration, actual memory reuse/packing and replacement costs, service bounds, bench qualification and final routed LUT/timing acceptance remain future implementation work.
This planning stage does not close #640's eventual acceptance.
Publish only REPORT.md and files listed in MANIFEST.sha256; scratch is excluded.

R493-3 FINISHED
