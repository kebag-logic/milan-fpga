[R747] NEGATIVE - exact head ffe3a631ed1e717ea77e2faae11cd2740edde36a

# R747-3: composition review of PR #820 (#818) on the merge-train candidate

Candidate `ffe3a631ed1e717ea77e2faae11cd2740edde36a`, tree `0761e4747b37842755934727a42af9e940736436`.
Parents: `683e59712b93b2ef9fc81d22cc21c7d96e4c3909` (the #806 candidate) and PR head `50e5d08dda6e89cf010a740cea5cf4539807db01`.
Scope: composition acceptance only. The source head has two POSITIVE source reviews, R747-2 and R748-2, both at `50e5d08d`.

Verdict basis: the composition creates one defect that neither source had (F1, MINOR, Docs and Conformance).
The #806 predecessor states three times, in present tense, that the resource gate refuses the shipping route's 0.408 ns WNS fall.
#818's gate in the same tree prints such a fall as a WARNING and passes it, and the same page that carries the #806 sentence says so.
Every other check of the composition is clean: the merge is textual-clean, the signed packet verifies, and 27 gates pass on the candidate.

## Composition identity

| Check | Result | Receipt |
|---|---|---|
| `git merge-tree --write-tree 683e59712 50e5d08dd` | `0761e474...`, the candidate tree; no conflict | this report |
| Live dev `02ca829a` tree vs candidate parent `683e5971` tree | identical, `556e7906...` | this report |
| `git merge-tree --write-tree 02ca829ad 50e5d08dd` | `0761e474...`: the candidate is exactly what merging the PR into live dev produces | this report |
| PR-only files (`MARK_II_AREA_PLAN.md`, `PP_SHADOW_BASELINE_RECIPE.md`, `syn/ooc/*`) at candidate vs PR head | byte-identical | this report |
| Shared files at candidate minus PR head | exactly the predecessor's own delta on them (8 changed lines) | `receipts/pr_head_to_candidate_overlap.diff` |

Files changed both by this PR and by a predecessor (merge base `1e80128f`):
- `docs/design/AREA_BUDGET.md`: #806 rewrote the slice-headroom paragraph (`:142-145`); #818 rewrote "The resource gate" (`:437-456`). The two hunks are textually apart. They conflict semantically: F1.
- `docs/integration/BUILDING.md`: #806 added the servo reset synchronizer cut (`:618-621`, in the clock-constraint subsection); #818 changed section 5 (`:570-579`, `:636-637`, `:726-729`). No textual or semantic interaction.

Semantic interactions checked beyond shared files:
- **Gate inputs.** `pp_resource_gate.py` reads `docs/design/AREA_BUDGET.md`'s policy table (`:87`) and `syn/ooc/pp_resource_baseline.json`. #806 changed that page outside the table and did not touch the baseline. `check-baseline` passes on the candidate.
- **CI command table / workflow pins.** #806 re-pinned only `sw/firmware/nvm_hosttest/*` entries in `ci/image/command-table.json`; #818 changes no workflow and no table entry. `ci_events.py --check/--selftest`, `ci_gate_workflows.py --check` and `generate_ci_evidence_pins.py --check` pass. A stale-pin observation inherited from the source head is OBS-1.
- **Docs registries, TOC and anchors.** `gen_toc.py --check/--verify-anchors/--selftest`, `docs_check.py`, `check_doc_paths.py` and `DOC_MAP.gen.py --check` pass. The section-5 anchor `#5-gates-before-a-build-is-good` that #818 cites still resolves.
- **Shared ratchets.** The hygiene, naming, test-evidence and fail-fast ratchets pass on the composed population.
- **Old gate command forms in predecessor pages.** No page #806 changed invokes `pp_resource_gate.py check` or `record`; the only invocations are in PR-only pages or historical findings pages, all reviewed at source.

## Findings

### F1 MINOR Docs, Conformance - docs/design/AREA_BUDGET.md:144, docs/reference/SUBMODULES.md:421-425, CHANGELOG.md:75 - the composed tree says the gate refuses a fall that the composed gate passes with a WARNING

Authority/evidence:
- #818's frozen rule: "The fall from the record is computed and printed as `WARNING`, with no failure." The composed `docs/design/AREA_BUDGET.md:444` says the same: "A WNS or WHS fall from the record by more than the timing fall prints a WARNING, also beside a floor failure, and never fails."
- The composed gate does it: `syn/ooc/pp_resource_gate.py:577` (the WARNING note) and `:547` (the summary). The arm "a large fall passes with a WARNING" (`syn/ooc/pp_resource_gate_set_selftest.py:146-148`: WNS 0.500 to 0.100, above the floor, exit 0, `RESULT: PASS`) passes on the candidate (`receipts/gates/gate_selftest.log:234`).
- Same tree, from #806 (`0c45ebf2` and `f99405af`, both in the candidate parent):
  - `AREA_BUDGET.md:144`: "That route meets the build floor at every corner, at +0.032 / +0.034 ns, but its WNS is 0.408 ns under the record's, beyond the gate's 0.25 ns tolerance, so the gate refuses it."
  - `SUBMODULES.md:425`: "The tolerance is 0.25 ns, so the gate refuses."
  - `CHANGELOG.md:75`: "The gate refuses that 0.408 ns fall."
- That route is exactly the shape of the arm: +0.032 ns is above the +0.030 ns floor, and the fall is 0.408 ns. Under the composed gate it prints a WARNING and does not fail on timing. `AREA_BUDGET.md:452` (#818) correctly puts the old binding in the past tense ("Before #818, the 0.25 ns fall limit bound first"). The #806 sentence 300 lines earlier on the same page still states it as the present verdict.
- Neither source has this defect. At `683e5971` the gate did refuse; at `50e5d08d` the #806 sentences are absent. The merge creates it.

Not RESIDUE: the sentence states a gate verdict on the shipping route, and the owner rule excludes verdict claims from RESIDUE.

Impact: the authoritative area-budget page and the pin page tell an adopter the current shipping route fails the resource gate. The gate in the same tree passes it with a WARNING on timing. A reader cannot tell which is true without running the gate. The next adoption's timing argument would also start from a false premise (that recovery of 0.408 ns is needed to pass).

Required outcome: in the tree that lands, no present-tense statement says the resource gate refuses the `135afd04` route's fall. `AREA_BUDGET.md:144` and `SUBMODULES.md:425` state the #818 rule for that route: the route meets the floor at every corner, and its 0.408 ns fall from the record prints a WARNING and does not fail. Alternatively, they mark the refusal explicitly as the gate's verdict before #818. `CHANGELOG.md:75` is the #806 entry's own record. Either qualify it the same way, or have #818 add an entry that states the change of verdict. Do not change the figures (+0.032 / +0.034 ns, 0.408 ns, +0.440 ns, 0.25 ns).

Verification: `git grep -n "gate refuses\|0\.408"` on the new head shows no present-tense refusal of that fall. `check_doc_style.py`, `gen_toc.py --check`, `docs_check.py` and `check_em_dash.py --base <parent>` pass. `pp_resource_gate.py check-baseline` passes, because the page edited is the one whose policy table the gate reads.

### OBS-1 SUGGESTION Tests, Docs - ci/image/command-table.json:13944-13957 - three declared resource-gate scripts keep their pre-#818 content pins (inherited from the source head, not composition-introduced)

Evidence: `receipts/command_table_pins.txt`. The declarations of `syn/ooc/pp_placement_selftest.py`, `syn/ooc/pp_resource_gate_mutants.py` and `syn/ooc/pp_resource_gate_selftest.py` match their content at `1e80128f` and `683e5971`, and are STALE at `50e5d08d` and at this candidate. `docs/testing/CI_IMAGE.md:41-42` says "Non-installing declarations include a reason and content SHA-256" and "Changed declared scripts refuse generation until reviewed again". Other lanes re-pin when they change a declared script (for example `ac0da94e`, #70).

Why it is not a finding against this composition:
- The composition does not create it. The bytes are the source head's, which the source reviews accepted.
- It changes no gate result. `scripts/ci_tool_inventory.py --check` was run with the checksum-pinned shell parser (sha256 `1904ec6b...`, from `ci/image/sources.lock.json`). It already refuses on the candidate parent, at `sw/builder/endstation_builder.py` (`receipts/ci_tool_inventory_parent683e597.log`). It refuses identically on the candidate (`receipts/ci_tool_inventory_candidate.log`). No PR workflow runs it; `ci/image/build.py:211` does, at image build.

Required outcome (manager routing): re-pin the three declarations at their #818 content, after re-reviewing each one's classification, in this lane or a tracked follow-up. Also decide whether the new `pp_resource_gate_set_selftest.py` needs a declaration. The source reviews or the manager may judge this a MINOR at source level; this round does not, because it is outside the composition scope.

Verification: `command_table_pins.sh` reports `match` for all three at the new head. Once dev's own stale pin is cleared, `ci_tool_inventory.py --check` advances past them.

## Prior public review findings (read after the independent pass above)

| Finding | Status at this head | Basis |
|---|---|---|
| R748-1 F1 MINOR Docs, RTL: Mark II `record` exits 2 | RESOLVED, unchanged by composition | `MARK_II_AREA_PLAN.md` is byte-identical to `50e5d08d`; no predecessor touched it |
| R748-1 F2 MINOR Conformance, Docs, Tests: no WARNING beside a floor miss | RESOLVED, unchanged | `pp_resource_gate.py` byte-identical; the four arms pass on the candidate (`gate_selftest` rc 0) |
| R748-1 F3 MINOR Tests: corner-agreement guard safety direction | RESOLVED, unchanged | arms pass; the mutant run kills all 236 mutants (`gate_mutants` rc 0) |
| R748-1 R1 RESIDUE: PR-body mutant claim | RESOLVED (per R747-2 and R748-2) | PR body not changed by composition |
| R748-1 S1 SUGGESTION: `bound()` sub-conditions | ceiling part RESOLVED; `bound()` part RETAINED, optional | gate bytes unchanged |
| R747-1 three SUGGESTIONs (fuzz on marked routes only; selection by WNS only; stale comparison directory) | RETAINED, optional | gate, selftest and recipe bytes unchanged |
| R747-2 RS1 RESIDUE: PR body "Round 2 mutants, each killed by the arm written for it" | RETAINED as RESIDUE | the sentence is still in the PR body (`receipts/pr820_body_at_review.md:89`) |
| R748-2 R2 RESIDUE: PR body file table, stale arm and mutant counts | RETAINED as RESIDUE | PR body unchanged; composition does not affect it |

Comment rule: the composition adds no bytes of its own (a clean merge), so it introduces no source comment and no new RESIDUE.

## Lens results (clean lenses in findings format)

- `[R747] UNCLEAN Docs - docs/design/AREA_BUDGET.md:144 vs :444, docs/reference/SUBMODULES.md:425, CHANGELOG.md:75 - F1 open.` Also checked clean: BUILDING.md section 5 and the servo-reset hunk compose without overlap (`receipts/pr_head_to_candidate_overlap.diff`). The Markdown, TOC, anchor, style, path, map and em-dash gates pass (`receipts/gates/SUMMARY.txt`).
- `[R747] UNCLEAN Conformance - docs/design/AREA_BUDGET.md:144 against #818's frozen "printed as WARNING, with no failure" - F1 open.` The gate behaviour itself conforms on the candidate. The four issue cases (`gate_selftest.log:232-235`) and `check-baseline` pass.
- `[R747] PASS RTL - git diff 683e59712..ffe3a631e (9 files, docs and syn/ooc Python only) and the predecessor's RTL (KL_gptp_shadow.sv, milan_datapath.sv, KL_mmcm_drp_servo.sv) - the composition joins no RTL to #818's files, and #818 reads no RTL.` Covered by R747-2 and R748-2 at `50e5d08d`. Composition-untouched.
- `[R747] PASS Robustness - syn/ooc/pp_resource_gate.py and its two selftests, byte-identical to 50e5d08d; its inputs, AREA_BUDGET.md's policy table and pp_resource_baseline.json, are unchanged by the predecessor - check-baseline rc 0.` Covered by R747-2 and R748-2 at `50e5d08d`.
- `[R747] PASS Tests - receipts/gates/{gate_selftest,gate_mutants,gate_check_baseline,placement_selftest}.log on the candidate - selftest PASS, all 236 mutants fail, baseline PASS on 3 endpoints, placement PASS.` The shared ratchets (hygiene, naming, test-evidence, fail-fast, py-idiom) pass on the composed population. OBS-1 is a SUGGESTION and outside the composition.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #818 body; `AREA_BUDGET.md:144,437-456`; `pp_resource_gate.py:547,577`; `gate_selftest.log:232-235` | R747-3 | `ffe3a631ed1e717ea77e2faae11cd2740edde36a` |
| RTL | CLEAN; composition does not touch its scope | composed diff vs parent (no RTL); the predecessor's RTL list | R747-2 and R748-2 (source); R747-3 confirms no interaction | `50e5d08dda6e89cf010a740cea5cf4539807db01`; confirmed at `ffe3a631...` |
| Robustness | CLEAN; composition does not touch its scope | gate bytes identical; inputs unchanged; `check-baseline` | R747-2 and R748-2 (source); R747-3 re-ran on the candidate | `50e5d08d...`; confirmed at `ffe3a631...` |
| Tests | CLEAN | `receipts/gates/*` (27 gates rc 0) | R747-3 | `ffe3a631ed1e717ea77e2faae11cd2740edde36a` |
| Docs | UNCLEAN (F1) | `AREA_BUDGET.md`, `BUILDING.md`, `SUBMODULES.md:405-432`, `CHANGELOG.md:52-80`; docs gates | R747-3 | `ffe3a631ed1e717ea77e2faae11cd2740edde36a` |

## Signed local CI packet

Packet at `review-evidence/818-r1/local-ci/50e5d08d` @ `c0270352f3eb5dc1c2b849749c7d0efeebf79bf9`, copied to `receipts/signed/`.
1. `allowed_signers` holds one line, principal `milan-local-ci`, namespace `milan-local-ci`, ED25519 key `SHA256:dRI12tvJkhueTEGqsRutn2L+dT/5qqOCsCVzBU5CI7k`. This is the required key; no other key is present.
2. `manifest.json` sha256 is `71357d82288ce5fd9e837a986f57384589496e79d813b8729176c9af6cf5d2aa`, as stated. `ssh-keygen -Y verify -f allowed_signers -I milan-local-ci -n milan-local-ci -s manifest.json.sig < manifest.json` exits 0: `Good "milan-local-ci" signature ... SHA256:dRI12tvJ...`.
3. The subject names PR 820, candidate `ffe3a631...` with tree `0761e474...` and parent `683e5971...`, and head `50e5d08d...` with tree `3a555c98...`; `result` is `success`. Of the 47 coverage entries, all are `ok: true`: 46 by act, and 1 not run (`rtl/physical-gptp`, schedule and dispatch only; act shows it skipped; stated as not hardware evidence). Banks: `manager-builder` 48 commands and `full-native` 5 commands, all exit 0.
4. The act replay ran on the PR head. The banks ran on the candidate. This round's own docs-gate runs on the candidate fill the gap between them for the Markdown gates.

## Executed evidence (this round, at the candidate)

`scripts/composition_gates.sh` runs every gate below; `receipts/gates/SUMMARY.txt` records each one's rc and last line. All are rc 0:
- `docs_check`, `check_em_dash --base 683e5971`, and `gen_toc --selftest/--verify-anchors/--check`. The Markdown gates ran with the renderer pinned by `tools/markdown/requirements.txt`; versions are in `receipts/gates/md_venv_freeze.txt`.
- `ci_events --check/--selftest`, `ci_gate_workflows --check`, `generate_ci_evidence_pins --check`.
- `check_doc_style` and its `--selftest`, `check_doc_paths`, `check_submodule_docs`, `check_gptp_docs`, `DOC_MAP.gen --check`, `check_feature_status`, `check_todo_ownership`, `check_solution_docs`.
- `check_py_idiom`, plus the hygiene, naming, test-evidence and fail-fast ratchets.
- `pp_resource_gate --selftest`, `pp_resource_gate_mutants` (236 of 236 killed), `check-baseline`, `pp_placement_selftest`.

Also run: `ci_tool_inventory.py --check` on the candidate and on the parent. Both refuse on the same dev-side pin (OBS-1).

Clone integrity after the probes: HEAD, tree and `git write-tree` are all `0761e474...`. Status is empty, and the worktree and index match HEAD. The gitlinks are `external efeb541a`, `gptp-processor 135afd04` and `protocol-processor f65c8ff7` (`receipts/integrity_after.txt`).

## Real limits

- No Vivado run. The claim that the `135afd04` route passes the #818 gate rests on its recorded figures (+0.032 / +0.034 ns at every corner) and on the arm of the same shape. This round did not run the gate on that route's reports, because they are not in the tree.
- The act replay is of the PR head, not the candidate. Hosted exact-head contexts were not inspected by this round.
- Physical calibration was NOT RUN, and field skips are not hardware proof.
- OBS-1 was judged against the inventory gate's current state on dev. The source-level severity is left to the manager.

## Pending manager duties

- Route F1 to a fix on the lane that lands after #806. Dev `02ca829a` already carries #806, so the fix goes on PR #820 rebased or merged onto dev. Re-run this composition check on the new candidate.
- Route OBS-1: re-pin in this lane, or open a tracked issue for it and dev's `endstation_builder.py` pin.
- Carry RS1 and R2 (PR-body RESIDUE) to the residue checklist.
- Build and validate the final current-dev candidate at the merge turn, and publish its builder and native receipts. Own hosted and act acceptance.

R747-3 FINISHED
