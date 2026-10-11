[R599] NEGATIVE - exact head 2bef9e50489a60f216a8073a9f5ea0645752b33f

R599-4, external independent delta review of issue #640 / PR #722.
Tree: `9777e890c07850052a0d9134cdb22388a651c5f1`.
Reviewed predecessor: `c0cba330fd485e52fcb90d5ccc69169edf9f0c2b`.
Source base and observed live dev: `6bfeeb132fa0b1ad8a5b957446c66a498e633af7`.
[Public review start](https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6108156582).

All five lenses were applied. One MINOR remains in the current PR body,
leaving Docs UNCLEAN. Conformance, RTL, Robustness and Tests are CLEAN for
this delta. The automatic merge and the in-tree arithmetic repair are correct.
No new RTL or test defect was found. This is not merge authorization or
completion of umbrella issue #640.

I reconstructed AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue body
and public decisions, requirements/interfaces, then the source-base diff and
history, followed by public author evidence. The independent verdict and
ledger were written in `receipts/independent-verdict.md` before reading prior
public review bodies. No private author material, management checkout,
other reviewer's local report or sub-agent was used. No source edit or GitHub
write was made.

**R599-4-F1: MINOR; all attributable lenses: Docs.**

- **Artifact:** [PR #722](https://github.com/kebag-logic/milan-fpga/pull/722),
  Known limitations / out of scope, first bullet; captured at
  `receipts/pr-body.md:140`. Compare Status and Composition repair,
  especially `receipts/pr-body.md:163`.
- **Authority/evidence:** AGENTS.md section 6 requires sufficient, accurate
  public review evidence. The current body identifies head `2bef9e50` and
  correctly states the three-lane result in Composition repair, but Known
  limitations still says the partial-central scenario is 38,436 LUTs,
  396 over 38,040. The current plan's own rows give
  `37,957 + (200 - 34) + (600 - 121) + (600 - 418) = 38,784`, or 744 over.
  The older pair includes M5 alone and omits 166 + 182 = 348 LUTs of
  measured shortfall. `receipts/delta.log` reproduces both observations;
  `receipts/pr-final-check.log` confirms the body was unchanged on the
  final read.
- **Impact:** the current PR presents two budget consequences without
  explicitly identifying the older one as a scenario in which every other
  lane retains its planning figure. Reading its limitations understates the
  all-measured gap by 348 LUTs. This concerns a figure's scope and value,
  so it is not wording-only RESIDUE. The credited M5 saving remains correct;
  no register or protocol requirement is violated by this PR-body defect.
- **Required outcome:** replace the obsolete sentence with the three-lane
  result, or explicitly scope it to M5 alone with all other lanes at their
  planning figures and direct readers to the combined result. Suggested
  replacement: “Using measured M2, M5 and M6 savings, partial central becomes
  about 38,784 LUTs, 744 above 38,040, pending D8's week-4 re-measure.”
- **Verification:** re-read the complete updated PR body against plan
  `:699`, `:960`, `:1048` and `:1106`; no competing unqualified current
  figure may remain. No RTL edit is needed.

R598-3-F1 treated the PR-body update as optional. That disposition is recorded,
not silently relabelled: its required in-tree repair is resolved below.
R599-4-F1 is this review's independent finding about the inconsistent current
PR body, first recorded before reading R598-3.

**What the delta proves.**

`git merge-tree --write-tree c0cba330 6bfeeb13` produces
`0fc0841bebece392d6facb87cd209d2f5e96e565`, exactly `da341a15`'s tree and
the stated composition tree. The merge has the expected two ordered parents.
The only following change is one removed and one added line in
`docs/design/MARK_II_AREA_PLAN.md:1106`.

The common base is `e8454e27`. Only the plan and
`scripts/measure_test_evidence_readers.py` were changed on both sides.
All eight other M5 files, including the CSR RTL, module page, harness,
generator, reference, campaign and Makefile, have identical blobs at
`c0cba330` and this head. The registry retains both lanes' entries and its
focused evidence gate passes. M6's datapath changes are on its counter-reader
face, away from the unchanged CSR instance at `hdl/milan/milan_datapath.sv:2445`.
M2's CSR crossing at `sw/litex/milan_soc.py:773` preserves its bus boundary.
No M5 port or parameter was changed by composition.

The plan's reproducible figures are M2 34, M5 121 and M6 418 LUTs, on their
stated measurement bases. Their central shortfalls total 827; the repaired
38,784/744 sentence recomputes exactly. Every cumulative planning row and
all nine placement rows, including both headroom columns, recompute.
They explicitly remain planning estimates until the week-4 re-measure.
The RAM ledger arithmetic also holds: 120.5 tiles before conditional release,
109.5 after, 115.5 with six further firmware tiles, and 126.5 for the partial
pre-release estimate. M2's maximum +2 is an explicitly unused allowance;
M5 and M6 add no tiles. No further stale plan-watch or ledger figure was
identified against the three measured lanes. D7 still leaves the resource
record unchanged. The PR states the repair and has no closing reference.

**Prior public findings, resolved or retained at this head.**

The findings were read from the public
[R598-1](https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6105288411),
[R599-1](https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6105370578),
[R598-2](https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6105610437),
[R599-2](https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6105856251)
and [R598-3](https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6108060229)
comments. The captured review and inline-comment lists were empty.

| ID and original classification | Disposition and verification |
|---|---|
| R599-1-F1; MINOR; Conformance, Docs | RESOLVED. Plan `:1102` labels the in-datapath 211 slope separately from standalone/proxy slopes. `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:623` and `:647` distinguish its N=1,2,4 fit from the 8x8 shape. Public author tables recompute base slopes 83/7 and 436/7, and M5 slopes 344/7 and 392/7, supporting the rounded 12/62/49/56. No non-reproduction claim remains. |
| R598-1-F1 = R599-1-F2; MINOR; Docs | RESOLVED in current attribution. PR Description states disjoint CSR -121, wrapper -342 and other -227, totaling -690; nested `u_pp` -344 is explicitly not added. The immutable round-one HANDOFF remains historical. The public round-two correction supersedes its attribution prose; no unpublished replacement was inspected or certified. |
| R599-1-RES-1; RESIDUE; Docs | RESOLVED. `hdl/common/csr/milan_csr.sv:1066` describes the OR stage and matches `:2660`. |
| R599-1-RES-2; RESIDUE; Docs | RESOLVED. Plan `:539` says M5 saved 121 routed and 127 post-synthesis. |
| R599-1-RES-3; RESIDUE; Docs | RESOLVED. PR CSR-test row says “apart from the module name”. Normalizing only that name reproduces the original base blob exactly. |
| R598-1-S1; SUGGESTION; Docs; subsequently required by the manager | RESOLVED and superseded by the combined sentence at plan `:1106`. |
| R598-2-S1; SUGGESTION; Conformance, Docs; escalated to R598-3-F1 | RESOLVED in the combined plan calculation. The current PR-body discrepancy is separately R599-4-F1. |
| R598-3-F1; MINOR; Conformance, Docs | RESOLVED in both original lenses. Plan `:1106` includes all three measured lanes and states 38,784/744. The six requested docs checks pass. |
| R598-2-RES-1 and R598-2-RES-2; RESIDUE; Docs | RETAINED as wording residues, with exact fixes below. |
| R599-1-S1; SUGGESTION; RTL, Docs | RETAINED, optional; details below. |
| R598-3-S1; SUGGESTION; Docs | RETAINED, optional; details below. |

**Retained R598-2-RES-1: RESIDUE; Docs.** Artifact: PR Round 2, first
attribution bullet. It calls all three values the gate's sub-block figures,
although `syn/ooc/pp_resource_gate.py:255` names scopes within the wrapper;
CSR is a sibling and -227 is the remainder. Impact: a reader looks in the
wrong receipt; the numbers stay unchanged. Exact fix: “The wrapper and
`u_pp` figures are the route gate's sub-block figures for the M5 route;
`csr` -121 is the routed hierarchy report's `milan_datapath/csr` scope,
and about -227 is the remainder.” Verification: re-read the body against
the named hierarchy and gate scopes. This does not leave Docs unclean.

**Retained R598-2-RES-2: RESIDUE; Docs.** Artifact: PR Description,
Saving against the plan. “Nearly all” describes nested -344 within -342,
where the other wrapper movement is +2. Impact: wording only; all values
are correct. Exact fix: “the processor wrapper -342, which nests `u_pp`
(-344; the rest of the wrapper moved +2; not added)”. Verification:
re-read that phrase and confirm the disjoint sum remains -690.

**Retained R599-1-S1: SUGGESTION; RTL, Docs.** Artifact:
`docs/testing/PP_SHADOW_BASELINE_RECIPE.md:142` and public route evidence.
The reported WNS fall is 0.202 ns, within the 0.25 tolerance and above
the 0.03 floor. Optional alternate-directive runs would characterize
placement sensitivity before later lanes inherit the margin. Required
outcome: none for this review; the optional outcome is comparative timing
evidence under the same recipe. Verification would compare complete timing
receipts and flow identities. No such run occurred here.

**Retained R598-3-S1: SUGGESTION; Docs.** Artifact:
`docs/design/AREA_BUDGET.md:197` and `:208` record M2/M6, without a similar
M5 measurement note. No existing claim is false; D7's required M5 ledger
entry is present. Optional outcome: add a link to the M5 intermediate
measurement naming its 121 routed/127 post-synthesis saving and zero RAM
growth. Verification: check the linked ledger and documentation gates.

**Executed evidence and reproducibility.**

| Check | Result | Receipt |
|---|---|---|
| Automatic merge, M5 blob preservation, frozen oracle and all plan arithmetic | PASS; PR-body check detects F1 and deliberately returns 1 | `scripts/check_delta.py`; `receipts/delta.log`, `.rc` |
| `docs_check.py` | rc 0; zero findings, scrub controls 23/23 | `receipts/docs/docs-check.*` |
| `check_em_dash.py --base 6bfeeb13` | rc 0; zero findings over 68 added lines; controls 339/339 | `receipts/docs/em-dash.*` |
| `gen_toc.py --check` and `--verify-anchors` | both rc 0; 143 contents pages and 471 cross-page anchors checked | `receipts/docs/toc-check.*`, `toc-anchors.*` |
| `check_doc_style.py`, `check_doc_paths.py` | both rc 0; 961 cited paths resolve | `receipts/docs/doc-style.*`, `doc-paths.*` |
| `measure_test_evidence.py --check` | rc 0; 67 <= 77; zero unexplained source readers | `receipts/test-evidence.*` |
| `git diff --check 6bfeeb13 HEAD` | rc 0 | `receipts/diff-check.*` |
| Supplied public author packet | Both blob IDs and published SHA-256 values verified | `scripts/check_public_evidence.py`; `receipts/public-evidence.*` |
| Root and three required submodules | All tracked bytes, modes, stage-zero index and pins verified; no hidden flags or checkout leftovers | `scripts/check_identity.py`; `receipts/identity-final.*`, `worktree-final.txt` |

The initial em-dash and two TOC attempts refused to judge because the pinned
renderer dependencies were absent (rc 2). Those raw receipts remain in
`receipts/docs-initial/`; they are not passes. Hash-locked dependencies were
installed only under `scratch/`, and all six checks then passed concurrently.
`scripts/REPRODUCE.md` gives portable commands. No source mutation or
simulation build was needed for this one-line repair and automatic-merge delta.

**Reviewer-owned completion ledger.** Every row covers this exact delta;
it does not certify the final merge candidate or release.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #640 assignment 6098404907 and D1/D3/D7/D8; REQUIREMENTS.md:129; docs/reference/REGISTER_MAP.md; docs/design/MARK_II_AREA_PLAN.md:539,1102,1106; receipts/delta.log. ABI/snapshot obligations and correctly scoped area claims checked against those authorities. | R599-4 | 2bef9e50489a60f216a8073a9f5ea0645752b33f |
| RTL | CLEAN | hdl/common/csr/milan_csr.sv:2630,2643,2923; hdl/milan/milan_datapath.sv:2445,3502; sw/litex/milan_soc.py:773; delta.log. Read precedence, shadow zeroing, SNAP capture, unchanged handshake and merge boundaries checked. | R599-4 | 2bef9e50489a60f216a8073a9f5ea0645752b33f |
| Robustness | CLEAN | tb/verilator/csr/sim_lock.cpp:435,459,485,603,647; hdl/common/csr/milan_csr.sv:2935; delta.log. Reset during read, invalid/unaligned addresses, snapshot ordering, stale/poison transitions and backpressure coverage examined; corresponding M5 logic and tests unchanged. | R599-4 | 2bef9e50489a60f216a8073a9f5ea0645752b33f |
| Tests | CLEAN | tb/verilator/csr/gen_lockstep.py:89; tb/verilator/csr/lock_mutants.py:113; tb/verilator/csr/sim_lock.cpp:703; scripts/measure_test_evidence_readers.py; docs and test-evidence receipts. Frozen oracle identity, named failure grading, nonzero-read requirement and merged registry checked. | R599-4 | 2bef9e50489a60f216a8073a9f5ea0645752b33f |
| Docs | UNCLEAN: R599-4-F1 | docs/design/MARK_II_AREA_PLAN.md:674,921,967,1071; hdl/common/csr/doc/milan_csr.md:156; current PR body:140,163. Plan, module description and gates pass; current PR budget figures conflict. | R599-4 | 2bef9e50489a60f216a8073a9f5ea0645752b33f |

**Real limits and pending manager duties.**

The [public author packet](https://github.com/kebag-logic/milan-fpga/tree/648503cfeee36d03d7baf2a7b8608e1310caae49/review-evidence/640-m5-r1)
and [round-two source receipts](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6105430562)
supply broader execution evidence at their stated revisions. They report
the two lockstep shapes, seven named mutation catches, broader source gates
and individual-lane measurements. Their tests were not re-executed here;
unchanged M5 artifacts were proved by blob identity. No combined M2+M5+M6
route is inferred from individual routes or from planning arithmetic.
The selected-split route remains at the M0s prerequisite STOP; the author's
8x8 integrated synthesis was not completed. No full parent, processor,
gPTP, synthesis or builder bank, implementation run, workflow replica,
hardware operation or merge was performed by this review.

There is no manager source bank at this exact head; none is claimed or
inferred. The manager's final current-dev candidate is a separate validation
object, built at the merge turn, with builder/native receipts to be linked
on the PR. Both the supplied source base and observed remote dev are
`6bfeeb132fa0b1ad8a5b957446c66a498e633af7`; any later dev movement must
be accounted for in that candidate.

The exact-head hosted snapshot at 2026-10-11 10:47 UTC
(`receipts/hosted-jobs.json` and `.tsv`) shows executed successes for the
selector, change detection, BDD, documentation without Git, wire
accountability and one synthesis shard. Other jobs were queued or running,
including documentation, elaboration, firmware, lint and remaining shards.
Physical gPTP was skipped with zero steps. No completed required aggregate
is inferred from partial jobs. Physical calibration was NOT RUN; field and
physical skips are not hardware proof. Hosted and local workflow-replica
acceptance remain manager duties.

Before merge: repair F1 and obtain its re-review, carry both retained residues
to the residue checklist, finish independent review coverage with no round
in flight, validate the current-dev candidate and publish its receipts,
and obtain maintainer merge authorization. Afterwards, run containment and
the plan's boot readback. D8's measured planning update, M9's target and
re-record, selected-placement qualification and physical release obligations
remain outstanding. M5 must not close #640.

Only REPORT.md and files named in MANIFEST.sha256 are publishable.
The dependency environment, public-input downloads and disposable material
under `scratch/` are excluded.

R599-4 FINISHED
