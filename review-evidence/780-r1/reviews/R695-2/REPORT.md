[R695] POSITIVE - exact head 91bf51e4ef246900c35a1f469392d15c3a22e1b4

# R695-2: internal cleared-context review of PR #783 (issue #780), round 2 (merge delta)

Head `91bf51e4ef246900c35a1f469392d15c3a22e1b4`, tree `050bef8e5355a3102fe760531c7a3e717216494b`. Parents: PR head `25f05752` (R695-1 and R696-2 POSITIVE) and dev `d385b38e5282b395ca55d49d135e46a93f56a340`. Gitlinks at this head: protocol-processor `ed2118035e4cec76fb1b59cfbf8a053aeacc8af8`, gptp-processor `55680bff3b287b9a7b0c759f51471fa617c17335`. Both are unchanged from `25f05752`.

## Summary

The merge composes cleanly, and every record this PR pins still matches the merged tree.

- **PR-owned content is unchanged.** Six of the eight files this PR changes have the same blob at `25f05752` and at this head: the gitlink, the ROM ledger, and the diagram drawio, svg, png and manifest. Dev did not touch any of them. The other two, `CHANGELOG.md` and `docs/reference/SUBMODULES.md`, are the files dev also changed. In both, the PR's added and removed lines are identical before and after the merge.
- **Nothing was lost in CHANGELOG.** Every dev line and every PR-branch line survives at this head.
- **No interaction with dev's four changes.** None of them touches GET_AVB_INFO or any record this PR pins. The #774 TSpec port binds to a processor port that is byte-identical across the two pins.
- **Status 11 at the composed head.** A pp_shadow probe on the merged tree, which builds the full `milan_datapath` including #774's TSpec wiring, answers a wrong-type GET_AVB_INFO with status 11 at cdl 16. The same tree with only the processor moved back to `93fb0b2d` answers status 1.

There are no BLOCKER, MAJOR or MINOR findings. There is one RESIDUE: the PR body does not record the merge commit. The three suggestions from R695-1 are retained.

## Reconstruction

Read in this order:

1. AGENTS.md and CONTRIBUTING.md: roles, lenses, completion bar.
2. docs/README.
3. The #780 issue body and its manager comments: assignment `issuecomment-6386868969` and the correction `issuecomment-6389770127`.
4. The executor's TAKEN and REVIEW READY.
5. The processor change: `93fb0b2d..ed211803`, one commit, PR #201 / #200.
6. `git diff d385b38e..91bf51e4` (the PR net against current dev, 8 files) and `git diff 25f05752..91bf51e4` (dev's 47 files arriving through the merge).
7. The published packet `review-evidence/780-r1` at `3e0d0e08`.

Prior PR review comments were read only after my independent pass over the delta.

## Delta evidence

| Check | Result | Receipt |
|---|---|---|
| PR-owned change lines, PR base `a032c6d6..25f05752` vs this head `d385b38e..91bf51e4`, per file | identical hash for all 8 files; for the 6 files dev did not touch, the blobs are also identical at `25f05752` and at this head | `receipts/delta_equivalence.txt` |
| Gitlinks at `25f05752`, `d385b38e`, `91bf51e4` | protocol-processor is `ed211803` at both PR heads (dev has `93fb0b2d`); the gPTP pin and every third-party gitlink are unchanged | `receipts/clone_restore_check.txt`, ls-tree in session |
| CHANGELOG composition | 0 dev lines and 0 PR-branch lines missing at this head; this PR's entry is on top (contents line 11, section 49-61); 39 headings, 37 in-file links, 0 unresolved, link order matches heading order | `receipts/changelog_composition.txt`, `receipts/anchors_head.txt`, `check_md_anchors.py` |
| SUBMODULES.md auto-merge | dev's `#190` row rewording (line 229, for #774) and this PR's pin row (line 25) and adoption section (lines 260-274) coexist; no contradiction, since the #774 row speaks of the #771 adoption and the new section says no port changes | read at head |
| ROM ledger | regenerated at this head: `ltn_rom.hex` `23cc67ee...`, `ucode.hex` `1f78804e...`, `gptp_ucode.hex` `19ed525d...`; equal to `syn/yosys/rom_digests.tsv:72-73` and to the `55680bff` row | `receipts/rom_regen.txt`, `receipts/rom_digest_check.txt` |
| Processor-side change | the only HDL change is `hdl/aecp/KL_aecp_engine.sv`: one dispatch constant at `:3457` (`UPC_NOTIMPL_C` to `UPC_NSUPPE_C`) plus comments. `aecp_commands.json` feeds HDL only through `gen_ucode.py`, whose output is unchanged. `protocol_processor_top.sv:303` `cfg_tspec_max_frame_i [N_STREAM_OUT_P*16-1:0]` is identical at both pins | session diff |
| #774 shadow interface | `hdl/milan/KL_pp_shadow.sv:303` and `:1284` bind the per-source port 1:1; `milan_datapath.sv:9472` drives it from `pp_src_maxf_w`. Built at this head with Verilator 5.050 (identity verified): 0 warnings | `receipts/probe-head.p780-lines.txt` |
| Dev delta vs GET_AVB_INFO | no added or removed line in `a032c6d6..d385b38e` names GET_AVB_INFO, NOT_IMPLEMENTED, NOT_SUPPORTED, 0x0027 or AVB_INTERFACE. Of the parent's GET_AVB_INFO consumer files, dev changed three: `KL_pp_shadow.sv`, `milan_datapath.sv` and `sim_nxn.cpp`, all only in TSpec or unrelated lines. `sim_nxn.cpp:1721-1723` queries AVB_INTERFACE (0x0009) only | `receipts/avb_info_grep.txt`, `receipts/avb_info_consumers.txt` |
| Composed boundary probe (published author patch, re-applied to copies of this head) | head: `status=11 cdl=16 type=0x0024`, pp_shadow 622 checks 0 failures, rc 0. Same tree with only the processor at `93fb0b2d`: `status=1`, rc 0. The probe tells the two pins apart in the composed tree | `receipts/probe-head.*`, `receipts/probe-oldpin.*`, `receipts/pp_shadow-p780-probe.patch` |
| Docs falsification at head (make 4.3) | `docs_check.py` 0 findings across 210 md; `check_doc_style.py` OK; `check_submodule_docs.py` OK (6 gitlinks); `check_diagram_pngs.py` OK; `submodule_boundaries.gen.py --check` OK; `check_gptp_docs.py --with-submodule` OK; `check_port_contracts.py` OK; processor `check-integrator-params.py` 29/29/29 OK; `measure_test_evidence.py --check` PASS; `measure_naming.py --check` PASS | `receipts/docs_*.log`/`.rc`, `receipts/pinchecks_head.txt`, `receipts/measure_*.log`/`.rc` |
| Published packet `review-evidence/780-r1` @ `3e0d0e08` | 135 manifest entries, 135 blobs, 0 mismatched, 0 unlisted, 16 path-redacted. The commit carries no git signature; integrity rests on the manifest digests | `receipts/evidence_manifest_verify.txt`, `verify_evidence_manifest.py` |
| Hosted checks at this head (inspected 2026-10-25) | 14 check runs, 13 queued and 1 in progress, 0 completed. No hosted verdict exists yet | `receipts/hosted_checks_91bf51e4.tsv` |
| Comment rule | the merge adds no source comments (only CHANGELOG and SUBMODULES.md change on the PR side) | diff |

## Findings

### R695-2-R1 - RESIDUE - Docs - PR #783 body, "Status" and "Description" commit table

- **Evidence:** the PR body still reads "**REVIEW READY** at `25f05752...`". Its commit table lists `e4bd7f5b`, `afdbd99b` and `25f05752`, and its expected-state block names "head `25f05752...`". The PR head is now `91bf51e4`, and the merge commit is not mentioned. Every statement is true of `25f05752`, so no measurement, figure or verdict is wrong. This is wording.
- **Impact:** a cold reader of the PR body cannot see that the head is a merge of dev `d385b38e` or which evidence ran where.
- **Exact fix:**
  - Add a commit-table row: "`91bf51e4` | Merge of dev `d385b38e` (PR #779 for #773, PR #782 for #781, PR #777 for #775, PR #778 for #774); one textual conflict in `CHANGELOG.md`, both Unreleased entries kept with this PR's on top; no PR-owned change differs; the CHANGELOG section is now `CHANGELOG.md:49-61`".
  - Add one sentence under Status: "Head `91bf51e4` merges dev `d385b38e`; the gates above ran at `25f05752`, and the current-dev merge candidate is validated at the merge turn."
- **Verification:** read the PR body.

### Prior findings on this PR, disposition at this head

- **R695-1 F1 / R696-1-F1** (MINOR, Tests and Docs: the behave model scope claim). **RESOLVED and still resolved.** The PR body line 70 and `issuecomment-6389770127` carry the corrected text. The merge does not touch `tests/`: no file under `tests/` is in dev's 47 files.
- **R695-1 R1 / R696-1-R1** (RESIDUE, Docs: the compliance pointer). **RESOLVED and still resolved.** PR body line 113 names processor `docs/00_MILAN_COMPLIANCE_REVIEW.md` section 8 row 14 and `docs/architecture/06_aecp_engine.md` section 6.10. The processor pin is unchanged, so the target is unchanged.
- **R695-1 S1** (SUGGESTION, Tests: builder leg 1 intermittent). **RETAINED.** The merge changes no file under `sw/firmware/nvm_hosttest/`, `ctrl_nvm/` or `common/`; dev changes only `sw/firmware/ctrl/README.md` there. Still worth a public issue if it recurs.
- **R695-1 S2** (SUGGESTION, Tests: no committed parent wire row for the changed status). **RETAINED.** This round's composed probe again shows such a row is cheap and discriminating: 11 at this head, 1 at the old pin.
- **R695-1 S3** (SUGGESTION, Tests: the behave model's target-gate limitation, `tests/steps/aecp_engine_model.py:621-624`). **RETAINED.** The file is unchanged by the merge.

No other prior findings exist on this PR. Its comments contain only the R695-1, R696-1 and R696-2 rounds plus manager start notices; there are no formal reviews or inline threads.

## Lens results (exact head 91bf51e4)

```text
[R695] PASS Conformance - protocol-processor/hdl/aecp/KL_aecp_engine.sv:3455-3460 at ed211803; receipts/probe-head.p780-lines.txt; receipts/avb_info_grep.txt - wrong-type GET_AVB_INFO answers Table 7-141 status 11 echoed at cdl 16 in the composed tree (status 1 at the old pin); cdl<16 BAD_ARGUMENTS precedes the type test; dev adds no status expectation for this command; the issue's Required list stays satisfied after the merge
[R695] PASS RTL - protocol_processor_top.sv:303 (identical at both pins); hdl/milan/KL_pp_shadow.sv:303,1284; hdl/milan/milan_datapath.sv:9472 - the processor delta is one dispatch constant; #774's per-source TSpec port binds 1:1 to an unchanged processor port; the composed milan_datapath elaborates and builds with 0 warnings
[R695] PASS Robustness - KL_aecp_engine.sv:3455-3460; receipts/probe-head.*, receipts/probe-oldpin.* - the wrong-type arm runs no gathers (E_NSUPPE), so the gsi/TSpec paths dev changed are not reached from it; dev's sequence advance (#775) and AAF/CRF stamp changes (#773) are datapath-only, with no processor dependence; the merge adds no state or reset path
[R695] PASS Tests - receipts/probe-head.*, receipts/probe-oldpin.*, receipts/rom_regen.txt, receipts/measure_test_evidence.log, receipts/evidence_manifest_verify.txt - the composed boundary probe discriminates; the ROM ledger regenerates; the test-evidence and naming ratchets pass at head; the PR owns no test change; the published source-head receipts verify against their manifest
[R695] PASS Docs - CHANGELOG.md:11,49-61; docs/reference/SUBMODULES.md:25,229,260-274; receipts/changelog_composition.txt, receipts/anchors_head.txt, receipts/docs_*.log, receipts/pinchecks_head.txt - no line lost in the conflict resolution; all anchors resolve in order; the auto-merged rows are coherent; the docs and pin checks pass at head; only R695-2-R1 (RESIDUE) remains
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | engine arm `KL_aecp_engine.sv:3455-3460` @ `ed211803`; composed probe (11 vs 1); dev-delta grep | R695-2 | `91bf51e4ef246900c35a1f469392d15c3a22e1b4` |
| RTL | CLEAN | processor HDL diff (`KL_aecp_engine.sv` only); `protocol_processor_top.sv:303`; `KL_pp_shadow.sv:303,1284`; `milan_datapath.sv:9472`; 0-warning composed build | R695-2 | `91bf51e4ef246900c35a1f469392d15c3a22e1b4` |
| Robustness | CLEAN | wrong-type arm ordering and no-gather path; dev #773/#775/#774 surfaces vs processor delta; composed probe | R695-2 | `91bf51e4ef246900c35a1f469392d15c3a22e1b4` |
| Tests | CLEAN | composed probe and old-pin control; ROM regeneration; ratchet checks; evidence-manifest verification; S1-S3 retained as suggestions | R695-2 | `91bf51e4ef246900c35a1f469392d15c3a22e1b4` |
| Docs | CLEAN | `CHANGELOG.md` composition and anchors; `SUBMODULES.md` merged rows; docs, diagram and pin checks; PR body (R695-2-R1 RESIDUE) | R695-2 | `91bf51e4ef246900c35a1f469392d15c3a22e1b4` |

My R695-1 ledger at `25f05752` stands for everything outside this delta. Of that content, only `CHANGELOG.md` and `docs/reference/SUBMODULES.md` were changed by the merge, and both are re-covered above.

## Limits

- **Not rerun by me:** the full sweep, milan_dp, the firmware gate set, the rtl-fast replica / behave, Yosys, lint, the builder bank and the three Vivado endpoints. Those author receipts are at `25f05752`, not at this head. The only HDL that differs between `25f05752` and this head is dev's, which its own PRs validated against processor `93fb0b2d`. The composition is argued statically (the processor delta is one constant on a path dev does not touch) and executed only through the pp_shadow leg above.
- **No manager source bank** runs at this head, and none is claimed or inferred.
- **No hosted verdict yet:** at inspection every hosted context at this head was queued or in progress.
- **Resource record not re-measured:** the merged candidate includes dev's #773/#774 RTL, which the author's route-1x1 / ooc-1x1 / ooc-8x8 runs at `25f05752` did not include.
- **No hardware proof:** physical calibration was NOT RUN, and field skips are not hardware proof.
- **An outside observation, not attributable to this PR:** `measure_test_evidence.py --check` prints the advisory "the mutation ratchet can be lowered to 67" (67 <= 77). This PR adds no suite.
- **The `external` submodule** is not checked out in this clone. Its gitlink `efeb541a` is unchanged across all three commits.

## Pending manager duties

- Build and validate the current-dev merge candidate (live dev `d385b38e5282b395ca55d49d135e46a93f56a340`) with the builder and native banks, including the resource gate on the merged RTL, and link the receipts on the PR.
- Own hosted and act acceptance at the exact head: the contexts were still queued at inspection.
- Carry R695-2-R1 to the residue checklist. Decide whether S1-S3 become public issues.
- Obtain the second independent positive at this head, wait until no round is in flight, get explicit merge authorization, check post-merge containment, then close #780 and move it to Done.

## Conduct

- No source fixes, commits, pushes, GitHub writes, author contact, sub-agents, containers/act or hardware.
- Probes ran only on disposable copies under `scratch/`. The review clone was verified afterwards: HEAD and tree exact, index equal to the HEAD tree (modes and blobs), all 1,442 tracked files byte-equal to their blobs, no untracked entries, and every populated gitlink checked out at its recorded commit and clean (`receipts/clone_restore_check.txt`).
- Publishable content is this file and the files listed in `MANIFEST.sha256`. `scratch/` is excluded.

R695-2 FINISHED
