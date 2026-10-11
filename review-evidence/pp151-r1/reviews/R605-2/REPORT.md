[R605] NEGATIVE - exact head 02063dc1b593d422406991bf0bc60e5cc47828ff

External independent review, issue #151 / PR #175, round R605-2. Tree: `2fd23c4ce9d7f23f73d6b4440b494e62d88a2682`. Source base: `2cbed0a987c1e68402658d69459ab7e5aa571adc`. Live parent dev identified by the brief: `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`. [Public review start](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/175#issuecomment-6106551240).

The implementation corrections withstand the focused checks. One MINOR remains: the available public evidence does not close the expanded Round 2 proof obligations. This is an evidence-publication finding, not an observed RTL failure. Conformance, Tests and Docs remain UNCLEAN. No BLOCKER or MAJOR was found.

**Scope and reconstruction**

The checkout has no repository `AGENTS.md` or `CONTRIBUTING.md`. I read the supplied workspace instruction, repository README, `docs/README.md`, and the HDL coding rules. The governing scope comes from the [issue acceptance](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/151), [frozen scope decision](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/151#issuecomment-6098621173), and [Round 2 decision](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/151#issuecomment-6105580039):

- Inventory every parameter guard; preserve its predicate; enforce elaboration rejection in each required front end.
- Grade the diagnostic severity and guard identity, the violating boundary and nearest passing boundary, and named weaker-severity and tightened/loosened mutants.
- Preserve passing production elaborations, ROMs and shipping shapes; retain the required source-gate proof.
- Correct the integration contract and severity explanation; satisfy the parent's Python rules without moving ratchets; provide the parent evidence-disposition patch and scratch-parent verification. The Python authority is [parent Rule 12 at the specified dev](https://github.com/kebag-logic/milan-fpga/blob/ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5/docs/development/CODE_QUALITY.md#rule-12-prefer-idiomatic-python).

I read `hdl/README.md`, the HDL engineer guide §2/§2.1, overview F01.5, interfaces §1/§2, verification §7/§8, the integrator contract and figure 21, then all 32 changed files and the five-commit history. The public executable archive was examined afterward. The Round 2 comment's summary of prior findings was read only after the independent diff pass. My independent verdict and five-lens ledger were written to `receipts/independent-verdict.txt` before opening either prior findings report. No current-round peer report or private author material was used.

**R605-2-F1 — MINOR — Conformance, Tests, Docs — current public proof is incomplete**

- **Artifacts:** PR #175 body, validation and scratch-parent paragraphs (`public/pr-body.txt`, lines 24–38); issue comment 6106223714; the supplied immutable evidence archive at [`bda25e67…/review-evidence/pp151-r1`](https://github.com/kebag-logic/milan-fpga/tree/bda25e67cb4df99a837ccb21383917c90b81a1ad/review-evidence/pp151-r1).
- **Authority:** the frozen per-guard/per-front-end proof requirement and Round 2 decision items 1, 4 and 5. Round 2 expressly requires each tightened and loosened boundary defect to fail by name in each front end, and the parent disposition patch plus a successful scratch-parent check.
- **Evidence:** all 340 downloaded executable receipts match the archive's published SHA-256 manifest. That archive was committed at 03:31:05 UTC, before Round 2; its source-head environment records identify `ef86ea848dbfb0d869108a1987accb203a17474d`. It has the old boundary cases, portable campaigns ending **98/98**, and a vendor campaign ending **14/14**. It does not carry the new **160/160** campaigns, the **62** vendor boundary arms, the changed boundary fixtures, or `parent-guard-evidence.patch`. Its parent receipts identify `e8454e27…`, not the newly required patched parent at `ac2c5e77…`. The current issue provides a private patch location only; neither current issue nor PR comments links an updated public receipt packet. The PR asserts the new results and refers to an accompanying handoff, without an accessible public source for those receipts.
- **Distinction:** the production HDL is byte-identical between the previous head and this head. Earlier production netlist/ROM and unchanged-campaign evidence therefore remains useful, as the PR correctly says. It cannot establish execution of newly changed test fixtures or an unpublished parent patch. Current independent lint and native checks, and successful exact-source hosted documentation/portability jobs, close part of the gap; they do not supply the missing vendor and parent proof. This finding does **not** require a manager source bank.
- **Impact:** the expanded acceptance cannot be independently closed from the permitted evidence. In particular, the old vendor log's passing value for the response-size guard is 24, and the deadline passing values are 2; they do not verify the new 17-byte and 1-cycle cases. This affects a verification claim, so it is not wording-only RESIDUE. No claim is made that the unpublished runs failed or did not occur.
- **Required outcome:** publish and link the existing Round 2 author receipts, bound to this exact source head and their tool identities: updated boundary runs in the required front ends, the portable 160-arm and vendor 62-boundary-arm results, relevant exact-head source-gate receipts, and the actual parent disposition patch with the required patched-parent checks and gitlink identity. Distinguish carried production evidence from fresh runs. Publication of already completed evidence can resolve this without changing source.
- **Verification:** hash-check the new public manifest; inspect named GUARD/ELAB results for all 31 guards, 62 named vendor boundary failures and the portable campaigns; review the patch; match the parent head, source gitlink, both applied dispositions and zero-exit Python/evidence checks to the claimed configuration. Reconcile those records with the PR body. Supporting receipts here: `receipts/public-evidence-fetch.json`, `receipts/public-evidence-analysis.json`, `public/retained-r1/`, and the exact-source hosted logs.

**R605-1-S2 — retained SUGGESTION — Robustness, Tests — inventory extension coverage**

- **Location:** `tb/elab_guards/guards.py:207`, particularly the `hdl/**/*.sv` glob and line-comment stripping.
- **Authority/evidence:** the inventory is intended to cover every HDL parameter guard. It currently sees all 31; there are no tracked `.svh` or `.vh` files. A future included header would be outside its scan; block-comment severity text can produce a false inventory failure.
- **Impact:** no current guard escapes. This remains optional and leaves both lenses clean except for unrelated F1 in Tests.
- **Suggested outcome:** include supported HDL header extensions and handle block comments consistently if the tree begins using them.
- **Verification:** fixtures should detect an included-header guard and ignore a severity task appearing only in a block comment, while preserving the current 31-site inventory.

**Independent evidence and lens assessment**

| Examination | Result and artifact |
|---|---|
| Production RTL and guard inventory | All 46 production `.sv` files compared to base. Exactly 31 fatal sites in 13 guard-bearing files. The 29 severity substitutions and listener scope move leave predicates, messages and the remaining production RTL unchanged. `scripts/source_audit.py`, `receipts/source-audit.json`, `receipts/exact-head.diff`. |
| Current lint bench | **93/93**, rc 0: 31 inventory checks and both sides of each guard. `receipts/guards-lint.log`. |
| Current portable conversion/elaboration bench | **93/93**, rc 0 using sv2v 0.0.13 and the available Yosys 0.66 distribution build. `receipts/guards-yosys013.log`. This is a scoped guard check, not the full synthesis bank. |
| Current mutation campaign | Control PASS; **160/160 KILLED** in the lint leg. All 31 error, warning, initial, tightened and loosened arms plus five bench arms. Individual raw logs in `receipts/mutants-lint/`; summary `receipts/mutants-lint.log`. No claim of a fresh 160-arm second-front-end run here. |
| Independent boundary probes | Four separately written literal mutations: size guard `<= 23`, shadow timeout `< 2`, writer timeout `< 2`, writer aggregate `< 2`. All fail with the named passing-side USERFATAL at 17 bytes or 1 cycle. `scripts/reviewer_probes.py`, `receipts/reviewer-probes/`. |
| Diagnostic robustness | Reviewed exit-status, severity, exact-site and message matching (`guards.py:273` onward), fixed context edits and boundary mutant attribution (`mutants.py:106`, `:244`). Deadline allowance requires only recorded UNSIGNED source comparisons, rc 1 and the exact warning-count exit; planted USER and other-warning defects are killed. No production predicates are edited by fixtures. |
| Independent severity measurement | **20/20 expected statuses**, five forms × two parameter sides × two available front ends. A violating module-scope `$info` emits an info note and exits 0; module-scope `$fatal` refuses in both. `scripts/probe_forms.py`, `receipts/forms/`. |
| Existing adjacent guard benches | Top interface **4/4**, descriptor-line **6/6**; NVM four legal and six refusing lint cases plus both native guard pairs pass. `receipts/adjacent-top-guards.log`, `receipts/adjacent-nvm-guards.log`. |
| Documentation | Focused links, requirement/module matrices, parameters, IDs, figures and staleness gates pass; figure 21 rendered and visually inspected, including the `$fatal` sentence. `receipts/docs-focused.log`, `receipts/docs-figure-inspection.txt`. Full exact-source hosted documentation job also succeeded. |
| Python obligations | Forty public function definitions in the two new modules have complete annotations and docstrings; manual review found none of Rule 12's six prohibited constructs. `receipts/python-contract-audit.json`. This does not claim a full patched-parent gate run. An initial reviewer scan incorrectly included constructors; that reviewer-script error was corrected and both receipts are retained. |
| Retained production evidence | The 57-line base/head canonical digest records are identical: 55 netlists plus two ROMs. Public vendor OOC summaries match at default and 9×9; all 15 retained campaign pairs have rc 0. The old suite records preserve every existing suite tally; head adds the 155-check guard suite, taking 1,029,620 to 1,029,775. These are carried Round 1 records, not new source-bank runs. |

The verified scoped lint executable reports version 5.050; wrapper hash and available native versions are in `receipts/tool-identity.txt`. Campaigns ran concurrently with foreground child processes and explicit worker counts, at most 16 workers; Make invocations used `-j16`. No vendor run or heavy build was launched. Every disposable tree and render is under this packet's `scratch/`.

The exact-source **push** run [38120459547](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/38120459547) checked out the requested head. Its documentation job 114413930614 and portability job 114413930410 completed successfully; the latter actually executed the new guard command and printed 93 PASS. The corresponding PR-context jobs also reported success, but those are kept distinct from the source checkout. Both suite jobs were still in progress at the final snapshot. The cached compiler-build step was skipped; that is not a skipped test job. No pending suite or skipped step is credited as executed proof. See `public/hosted-source-*.log`, `public/hosted-*-jobs.json` and `public/hosted-checks-final.json`.

**Disposition of every prior public finding**

The [prior external findings](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/175#issuecomment-6105535610) and [prior internal findings](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/175#issuecomment-6105577986) were opened only after the independent verdict and ledger were written.

| Prior ID | Disposition at this head | Current evidence |
|---|---|---|
| R604-1-F1, nearest response-size boundary | Implementation defect resolved; required vendor verification retained under R605-2-F1 | `guards.py:142` uses 16/17; current lint/native runs pass; the independently planted `<=23` defect fails by name at 17. New vendor receipt remains unavailable. |
| R604-1-F2 = R605-1-F1, integration contract | RESOLVED | `docs/guides/integrator.md:114` and figure 21 line 53 say `$fatal`; figure rendered and inspected; documentation checks pass. |
| R605-1-F2 = R604-1-R1, `$info` explanation | RESOLVED; no residue remains | Guide §2.1, bench README and module docstring correctly distinguish the three warnings from `$info`; the independent form probe reproduces its rc 0 info note. |
| R605-1-S1, deadline value 1; made mandatory by Round 2 | Implementation resolved; expanded vendor proof retained under R605-2-F1 | Cases at `guards.py:93`, `:134`, `:137`; strict diagnostic exception; all three independently tightened guards fail by name at 1. |
| R605-1-S2, inventory scope | RETAINED SUGGESTION | Described above; no current header guard is missed. |
| R604-1-S1, hosted portability coverage | RESOLVED | `.github/workflows/hdl.yml:114`; exact-source job executes the new command successfully, 93 checks. |

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — F1 | Frozen acceptance, Round 2 scope, F01.5 and interface/coding authorities; complete production inventory; retained versus missing current proof | R605-2 | 02063dc1b593d422406991bf0bc60e5cc47828ff |
| RTL | CLEAN | Full diff/history; all 46 production SV files; 31 predicates/messages; listener scope move; carried netlist/ROM records and unchanged Round 2 HDL | R605-2 | 02063dc1b593d422406991bf0bc60e5cc47828ff |
| Robustness | CLEAN — S2 optional | Diagnostic class/site/status matching; strict deadline exception; fixed fixtures; 160 named mutants; four independent boundary faults; standalone severity forms | R605-2 | 02063dc1b593d422406991bf0bc60e5cc47828ff |
| Tests | UNCLEAN — F1 | Both current 93-check benches; 160-arm lint campaign; adjacent guard benches; annotation audit; missing current vendor/parent receipts | R605-2 | 02063dc1b593d422406991bf0bc60e5cc47828ff |
| Docs | UNCLEAN — F1 | Coding rule, bench docs, integrator contract, rendered figure 21, passing local/hosted docs gates; PR proof claims without current public receipts | R605-2 | 02063dc1b593d422406991bf0bc60e5cc47828ff |

**Real limits and pending manager duties**

No full parent, processor, gPTP, synthesis or builder bank was run. No fresh vendor execution, pinned sv2v 0.0.12 execution, or full patched-parent check was performed. The available native synthesis executable is the distribution build of version 0.66, not the parent SDK build. Canonical digest receipts were compared; full original netlists were not independently regenerated. No physical calibration was run: **physical calibration NOT RUN**, and field skips are not hardware proof.

No manager source bank exists at this exact head, and none is claimed or inferred. The earlier consumer-bank result mentioned in the manager's Round 2 scope comment concerns the earlier state. Source-head author evidence and final current-dev candidate validation are distinct.

The manager must arrange publication of the missing source proof and disposition patch, obtain closure of F1 and the required independent review results, then build and validate the final current-dev merge candidate at the merge turn, including builder/native and required donor/consumer banks with the relevant disposition patches. The manager must link those receipts on the PR and own hosted/act acceptance, including the still-running hosted suites. The previously reported parent lint-filter issue remains a separate parent follow-up; this review neither fixes it nor claims that a manager bank validated it. Residue checklist: none from this round.

**Integrity and packet**

The review checkout remains detached at the exact head and tree. All **592 tracked file blobs and executable modes** match HEAD, the index tree matches, and status is clean. There are **no submodule gitlinks** in this repository, so no required nested gitlink was omitted. `receipts/integrity-before.json` and `receipts/integrity-final.json` record the checks. No source fix, commit, push, GitHub write, merge, author contact, shared install, privileged action or hardware action occurred.

Portable review scripts and raw receipts are listed in `MANIFEST.sha256`, with relative paths. Scratch trees, downloaded working copies and raster previews are excluded. `scripts/run_focused.py` takes the source root, a fresh packet directory and the scoped executable path; create its `scratch/` and `receipts/` directories before replay. The submitted campaign intentionally refuses an existing mutation-output directory. Source integrity is independently reproducible with `scripts/integrity.py SOURCE_ROOT`.

R605-2 FINISHED
