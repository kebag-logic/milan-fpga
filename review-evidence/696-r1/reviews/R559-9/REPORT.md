[R559] POSITIVE - exact head 26e2748f47b0d8fa533f53203264d9f31fc13c48

External independent delta review R559-9 of issue #696 / PR #706. All five lenses are CLEAN. No open BLOCKER, MAJOR or MINOR remains. R558-11-F1 and R558-11-R1 are resolved by the exact requested wording. Earlier prose residues and optional suggestions are explicitly retained in [RECONCILIATION.md](RECONCILIATION.md), which is part of this verdict.

Reviewed tree: `b93fd1d39c06c069c01aa8ceeeb74fbb6083472e`. Source base and recorded live dev: `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`. Previous reviewed source: `aa980479aafd1d72c72015707fa6618b5aa47cb1`.

The independent verdict and artifact-specific ledger were written before prior review reports were opened; [independent-pass.json](receipts/independent-pass.json) records that checkpoint. Public findings were read and reconciled afterwards. No private author material or other checkout was read or changed.

Public reconstruction followed the requested order: AGENTS.md/CONTRIBUTING.md, docs/README, [issue #696](https://github.com/kebag-logic/milan-fpga/issues/696) and its public assignment/rulings, requirements and interface authorities, the complete diff against `c6bd08c6` and history, then public source evidence. Authorities examined include `REQUIREMENTS.md`, `FR_NFR.md` FR-MAAP-01, `MAAP_FABRIC.md`'s Annex B contract, `REGISTER_MAP.md:1259-1261`, architecture clock ownership, and the area budget/measurement recipe. The [M8 ruling](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6076940309), [shared-buffer area ruling](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6079087547), [unchanged timing floor](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6089712293), and [narrowed first-draw criterion](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6102832618) remain binding. Bench acceptance remains assigned to the post-merge bench lane.

The delta is exactly the stated composition and wording repair:

- `b075a994f6daae3b406bce415a837b7c401712d5` has parents `aa980479` and `c6bd08c6`. Recomputing their automatic merge gives tree `4650fd5d9d5c940bc6788491229dc808cf866962`, exactly that commit's tree, without conflicts.
- `26e2748f` changes one file, with exactly three removed and three added lines: `docs/design/MARK_II_AREA_PLAN.md:1095-1096,1111`. No additional manual merge resolution or source change is present.
- All other sixteen paths in this PR's seventeen-file delta against `c6bd08c6` have identical blobs and modes to `aa980479`. This includes MAAP RTL, its datapath integration, all MAAP tests, firmware differential changes, resource records and previously reviewed MAAP documentation. Imported CSR/gPTP changes are dev's changes; the fresh integration run below exercises their composition with MAAP.

[Audit receipts](receipts/audit-final.log) and the two raw diffs, [PR delta](receipts/pr-delta.patch) and [since aa980479](receipts/since-aa980479.patch), make those boundaries reproducible.

The M2 section at plan `:696-697`, M5 at `:1095-1096`, and M6 at `:948` each name #645/#647's historical comparison and #696's current record. M2/M5 also explicitly date the former to dev `e8454e27`. Their no-re-record sentences at `:707,969,1111` name the individual lane. No remaining unqualified comparison sentence identifies the current route-1x1 record as 50,267. The plan deliberately retains 50,267 as its historical planning baseline; the already classified baseline wording residues remain listed in the reconciliation.

The requested unmodified [R558-9 script](scripts/R558-9/record_vs_lane_routes.py) confirms that all three historical base rows equal the old record and differ from the current one, with M2/M6 passing against both. The unmodified [R558-11 script](scripts/R558-11/check_plan_composition.py) confirms 66/66 current-inventory figures, the partial-central arithmetic `37,957 + 166 + 479 + 182 = 38,784` (744 over 38,040), and M5 passing the stated comparisons against the 50,013-LUT record. M5 moves -436 LUT, -80 FF and +38 slices; WNS falls 0.136 ns to +0.097, within both floor and fall limit. These scripts check stated historical measurements; they do not perform a new route. The separate [wording control](scripts/check_record_wording.py) passes this head and exits 1 on `b075a994`, naming the missing M5 qualifications.

Local execution evidence:

| Check | Result | Receipt |
|---|---|---|
| MAAP unit target | 186 checks, zero failures; includes every-word/carry-run assertions | [unit.log](receipts/unit.log) |
| Real CSR/datapath MAAP target | Build rc 0; 5 checks, zero failures: programmed-MAC intervals, link return, first block separation, PHC intervals and first offsets | [integration-build.log](receipts/integration-build.log), [integration-run.log](receipts/integration-run.log) |
| Documentation and resource checks | 13/13 final results rc 0: wording/links, style, cited paths, feature status, contents, anchors, added em-dash, module matrix, archive, solution docs, submodule docs, imported documentation, baseline | [checks.json](receipts/checks.json), [checks-retry.json](receipts/checks-retry.json) |
| Resource baseline consistency | PASS, three endpoints; unchanged tolerances, floors and ceilings | [baseline.log](receipts/baseline.log) |
| R558-9 / R558-11 scripts | Both rc 0; historical/current record distinction and stated numerical comparisons verified | [record-vs-lane-routes.log](receipts/record-vs-lane-routes.log), [plan-composition.log](receipts/plan-composition.log) |
| Wording sensitivity | Current head rc 0; pre-fix merge expected rc 1 | [wording-controls.json](receipts/wording-controls.json) |
| Checkout integrity | Exact parent blobs/modes/index and required submodule pins/bytes; clean status | [audit-final.log](receipts/audit-final.log), [final-status.log](receipts/final-status.log) |

Three documentation checks initially refused the missing pinned Markdown renderer. A hash-locked installation in `scratch/venv` resolved that prerequisite; only those three were retried. Initial refusals remain published. Compiler identity was verified before use. All build outputs stayed under `scratch/`; no shared installation changed. [REPRODUCE.md](REPRODUCE.md) gives commands, provenance and the limited compiler-path substitutions in build receipts.

Reviewer-owned ledger:

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue body/rulings; `MAAP_FABRIC.md:43-190`; `KL_maap.sv:142-495`; plan `:696,948,1095`; identical prior fixes and passing unit/datapath evidence against the frozen scope | R559-9 | `26e2748f47b0d8fa533f53203264d9f31fc13c48` |
| RTL | CLEAN | `KL_maap.sv:142-203,313-495`; `milan_datapath.sv:7181-7201`; `integration.mk:11-36`; automatic merge equality and unchanged blobs; current CSR/link/PHC integration build and run | R559-9 | `26e2748f47b0d8fa533f53203264d9f31fc13c48` |
| Robustness | CLEAN | `sim_main.cpp:428-470,780-940,1188-1275`; pending/active-response preservation, allocation cancellation, long link outage, supplied-seed bounds, truncated-PDU no-effect and first-draw boundaries; current 186/0 unit and 5/0 integration | R559-9 | `26e2748f47b0d8fa533f53203264d9f31fc13c48` |
| Tests | CLEAN | `Makefile:29-37`, `integration.mk`, `mutants.py:48-127`, `sim_integration.cpp`, `sim_main.cpp:1188-1275`; unchanged named plants and assertions; current clean targets and failing pre-fix wording control | R559-9 | `26e2748f47b0d8fa533f53203264d9f31fc13c48` |
| Docs | CLEAN | Plan `:56,64-147,656-707,925-969,1076-1111`; `AREA_BUDGET.md:104-160,396-420`; `234_PP_SHADOW_AREA_BASELINE.md:34-106`; resource JSON; 66-cell comparison, historical/current qualifiers, thirteen focused checks and prior-finding reconciliation | R559-9 | `26e2748f47b0d8fa533f53203264d9f31fc13c48` |

All five lenses were applied independently to this delta. This ledger does not approve future changes or replace a full fresh review of dev's separate lanes. RESIDUE and SUGGESTION affect neither the verdict nor lens cleanliness under the supplied owner rule. No code defect has been treated as resolved by moving its paperwork elsewhere.

Evidence limits and remaining manager duties:

- The [requested public source snapshot](https://github.com/kebag-logic/milan-fpga/tree/97f433d668907446e83c074b21e81d03a34988af/review-evidence/696-r1) was inspected, including raw historical suite and endpoint gate receipts. Its earlier route is 50,230/+0.114, not the current 50,013/+0.233 record. The [author's later source evidence](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6103504186) names `32582421`; the current record's measured input is `bee1b0d7`. These retain their stated revisions. No manager source bank ran at `26e2748f`, and none is inferred.
- This reviewer ran focused clean targets and documentation checks only. No full parent, processor, portability or builder bank, full mutation campaign, synthesis/route, local workflow replica, or hardware run was performed. Existing pool-fold bias, one-response capacity and omitted discard accounting remain explicit ruled limitations; full Annex B conformance is not claimed. First-draw universal checks rely on the RTL's reviewed linear structure plus sampled linearity checks, not exhaustive nonlinear-function verification.
- [Hosted snapshot](receipts/hosted-checks.json) is exact-head but incomplete when read: several jobs succeeded while documentation, elaboration and long shards were still running. Physical gPTP was **skipped**. No pending or skipped context is counted as an executed pass. Hosted/local-replica acceptance remains the manager's duty.
- Physical calibration **NOT RUN**. Field-campaign skips and desk simulation provide no hardware proof. Acceptance 4 remains with the post-merge bench lane.
- The manager must construct and validate the final candidate against then-current live dev, run its required builder/native banks and publish their receipts on the PR. Source validation is distinct from that merge-turn candidate. The source includes the recorded `c6bd08c6` base, but tree ancestry alone does not discharge candidate validation.
- The manager must finish independent review and the merge ledger, retain the exact residue fixes/suggestions, accept hosted/local-replica evidence, obtain the required merge authorization, and complete post-merge containment and issue/project updates. This positive review is not merge authorization.

Final integrity verification rehashed 1,297 parent blobs and all blobs of the three required registered submodules: processor `2ad2f845dd583f8310075fa2380cb60a04fd091a` (562), gPTP `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9` (104), and axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce` (214). All parent gitlinks, modes and stage-zero index entries match the reviewed commit. No source edit, commit, push, GitHub write, merge, author contact or delegation occurred. Every launched process has completed; no restoration was needed.

`MANIFEST.sha256` is the publication allowlist. Scratch material is excluded. Only listed files and this report are for publication.

R559-9 FINISHED
