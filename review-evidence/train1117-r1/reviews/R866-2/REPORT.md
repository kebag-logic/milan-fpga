[R866] POSITIVE - exact head b1f1161b0f72e6066f60c7e0fa5ba399e185493d

External independent delta review, R866-2, PR #945. Tree: `c84aa1e1d12890b82c806a370416a3b9aecbe902`. Previous reviewed head: `732726660a88cd79a568d650d955d535fe79c720`. Source base: `cb96336d7aaacbaec76990ab07ef64148808d4ac`.

No open BLOCKER, MAJOR or MINOR in the reviewed delta. All five lenses are CLEAN. Two prior wording residues remain; one PR narrative residue is added below. This verdict does not discharge merge-candidate or hardware acceptance.

Scope and independence

The governing sources were AGENTS.md sections 6-7, CONTRIBUTING.md, docs/README.md, the thirteen named issue bodies and public decisions, REQUIREMENTS.md, the linked ownership/service-budget/interface authorities, and docs/DOC_GENERATION.md. The composition contract is [#665 comment 6939574513](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6939574513); its later step-11 and release-record decisions remain unchanged.

The `cb96336d..b1f1161b` diff and first-parent history were acquired; the independent technical pass concentrated on `73272666..b1f1161b`, as directed. Untouched composition logic retains [R866-1's public coverage](https://github.com/kebag-logic/milan-fpga/pull/945#issuecomment-6982365106). The independent delta verdict and ledger were written before reading that prior report. No other review report was read. The PR discussion contained that one prior verdict, two earlier start notices and this round's start notice; the separate review-submission and inline-comment endpoints were empty.

Delta and historical cause

- Exactly one commit and one path change: `docs/DOCUMENTATION_AUDIT.md`, mode `100644` unchanged, 13 additions and 12 deletions. Old/new blob IDs are `383f13f35065c105fb64e1a9d924a533710a7004` and `cc616ab94dc80c37347a1188656526000cc012b8` (`scope.json`, `delta.patch`).
- The new audit lists 223 documents: 186 current, 16 stale, zero superseded and 21 obsolete. The added page is `tb/verilator/ctrl_reboot/README.md`; module README and test-tree counts rise by one. Six existing page rows refresh their cited paths or standards. Existing semantic findings and their statuses remain visible.
- The generator and its JSON data are byte-identical to the previous reviewed head. Two consecutive `docs_inventory.py --write` invocations reproduce the committed bytes exactly; `--check` returns zero. SHA256 of the audit is recorded in `audit-probe.json`.
- A negative control temporarily restores the exact previous audit. `--check` returns 1 with STALE, including current 185 versus generated 186. `--write` then restores the exact new bytes and `--check` returns zero. A finally block restores the original head bytes independently.
- Historical snapshots prove the commit's cause. At #934's frozen head `544fd72c`, the same generator says the audit is fresh; that tree has no REBOOT README. Step 9, merge `8f6fbb84`, imports exactly that audit blob into a tree containing the earlier train's REBOOT README and changed page references: the check becomes stale. The identical stale blob persists through `73272666`. The regenerated row delta is already present at step 9. Thus the cause is composition around #934, including #881's README, not the later release-resource record. See `inventory-history.json` and `inventory_history.py`.

The audit describes documentation. It is not a build or protocol input. The entire delta contains no RTL, firmware, constraints, test implementation, generator, requirement, interface or gitlink change. Source comments gain no new bench labels or review identifiers.

Executed evidence at this head

Every command below returned zero. Full stdout/stderr and exit-code files are under `gates/`; `gates/results.json` records commands and elapsed times.

| Command | Result |
|---|---|
| `python3 scripts/docs_inventory.py --check` | Fresh, 541 lines |
| `python3 scripts/docs_inventory.py --selftest` | 60 controls pass |
| `python3 scripts/docs_check.py` | Zero findings |
| `python3 scripts/gen_toc.py --check` | 160 annotated pages; 18 below threshold |
| `python3 scripts/gen_toc.py --verify-anchors` | 755 cross-page fragment links reproduced |
| `python3 scripts/check_em_dash.py --base 73272666` | Zero findings; 13 added lines; 339/339 controls |
| `python3 scripts/check_em_dash.py --base cb96336d` | Zero findings across the composed train |
| `python3 scripts/check_doc_style.py` | 25 current documents pass |
| `python3 scripts/check_doc_paths.py` | 1,755 cited paths resolve; two allowlisted; ten line anchors valid |
| `python3 scripts/check_hygiene.py --check` | PASS |
| `python3 scripts/check_py_idiom.py` | PASS |
| `git diff --check cb96336d..b1f1161b` | Empty output |

No other generated documentation table is stale. The generated-page census identified the audit, module matrix, register reference, mailbox contract and trace catalogue. Their checks all pass: `docs/traceability/gen_module_matrix.py --check` (84 modules, 7/7 controls), `scripts/gen_register_reference.py --check` (203 registers, 34 modules, 240 files), `sw/mailbox/gen_mailbox.py --check --crosscheck`, and `sw/trace/gen_trace_events.py --check` (23 events). `scripts/check_feature_status.py` also reports zero findings in the status projections. Contents checks cover generated navigation separately. This is freshness evidence, not a new assertion that the audit's sixteen semantically stale pages have been corrected.

The initial environment lacked the documented Markdown renderer and waveform package. Five checks correctly refused setup; their original rc=2 receipts remain under `setup-refusals/`. The documented package versions were installed only in `scratch/venv`, with the Markdown lock hash-checked. Only the refused checks were rerun; their final results are zero. No shared installation changed.

Published evidence

The [public author archive](https://github.com/kebag-logic/milan-fpga/tree/66fea879135dec78ecfb2410d5dc2115c1a29077/review-evidence/train1117-r1) is fixed at `66fea879135dec78ecfb2410d5dc2115c1a29077`. All 3,651 published SHA256 entries match, totaling 21,434,428 bytes (`evidence-verification.json`). The archive commit has no embedded signature and the evidence directory has no detached signature; signer authenticity cannot be verified from the supplied publication. The verified claim is manifest consistency and commit identity.

Spot-checks of `author-r5/receipts/step11/gates/q-73272666/` match the published successful docs, contents, anchors, em-dash, paths, style, hygiene and idiom receipts. They are ancestor source-head evidence, not executions at `b1f1161b`. This round's own receipts supply the requested exact-head documentation checks. No manager source bank is claimed. The reported earlier builder inventory failure was independently reproduced with the parent audit; no unpublished manager log was accessed.

Reviewer-owned coverage ledger

Each result applies to the delta and preserves prior coverage only for unchanged dependencies.

| Lens | CLEAN/UNCLEAN | Examined artifacts and result | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `docs/DOCUMENTATION_AUDIT.md:3`; `docs/DOC_GENERATION.md`; `audit-probe.json`; `inventory-history.json`: exact generated output and historical cause satisfy the regeneration contract; no normative behavior changes | R866-2; R866-1 untouched composition carried | b1f1161b0f72e6066f60c7e0fa5ba399e185493d |
| RTL | CLEAN | `delta.patch`, `scope.json`, `final-integrity.json`: sole Markdown change; build sources, interfaces, constraints and five required gitlinks identical | R866-2; R866-1 untouched RTL carried | b1f1161b0f72e6066f60c7e0fa5ba399e185493d |
| Robustness | CLEAN | `audit-probe.json`; `gates/inventory-selftest.log`: old output rejected, regeneration heals, repeated writes stable; malformed/missing/copy/status controls pass | R866-2; R866-1 untouched runtime paths carried | b1f1161b0f72e6066f60c7e0fa5ba399e185493d |
| Tests | CLEAN | `gates/results.json`, `audit_probe.py`, `scripts/docs_inventory.py`: actual stale-parent negative control is sensitive; all requested checks and generated-table checks pass without weakening tests | R866-2; R866-1 untouched campaigns carried | b1f1161b0f72e6066f60c7e0fa5ba399e185493d |
| Docs | CLEAN | `docs/DOCUMENTATION_AUDIT.md:27`, `:306`, `:428`; `inventory-history.json`; generated-table receipts: counts, page population, source citations and freshness agree; prior findings explicitly retained below | R866-2 | b1f1161b0f72e6066f60c7e0fa5ba399e185493d |

Findings and residue reconciliation

[R866] R866-1-R1 | RESIDUE | Docs | `sw/firmware/ctrl/test/test_plat_boot.cpp:91,95,116,119` | RETAINED

- Authority/evidence: owner source-comment rule, 2026-10-15. The B24 prefix, parenthetical Phy test-label list and L5/L6 prefixes remain. The entire source blob is unchanged (`carry-identity.json`).
- Impact: wording-only source-comment convention violation; no behavior, measurement, verdict, clause or privacy change.
- Required outcome / exact fix: remove B24 on line 91, the parenthetical label list on line 95 and the L5/L6 prefixes on lines 116/119. Keep behavioral descriptions and issue/requirement references; do not rename executable tests.
- Verification: comment-only diff and unchanged executable test contents. Carry to the residue checklist; this is not resolved by this commit.

[R866] R866-1-R2 | RESIDUE | Docs | `sw/firmware/ctrl/plat/ctrl_split_hot.txt:14,19` | RETAINED

- Authority/evidence: the same rule forbids issue-comment IDs in source comments. Both IDs remain in the unchanged blob (`carry-identity.json`).
- Impact: wording only; ordered entries, trace hashes, costs and acceptance rules are unaffected.
- Required outcome / exact fix: delete `issuecomment-6959600243` and `issuecomment-6967930396`, adjusting adjacent commas. Keep #665, ruling dates, item numbers and NFR-SCOUT-01.
- Verification: header-prose-only diff; all 266 ordered entries and three trace hashes unchanged. Carry to the residue checklist.

[R866] R866-2-R1 | RESIDUE | Docs | PR #945 body, Status and Composition commits | OPEN

- Authority/evidence: the current body still calls `73272666` the final review head and omits this regeneration commit. Public metadata and `scope.json` identify `b1f1161b`; the new commit changes only the audit.
- Impact: reader-facing narrative is stale. The measurements and their actual execution heads remain correct and must not be relabelled.
- Required outcome / exact fix: replace the opening status with “Ready for the delta review at head `b1f1161b`; measured source evidence remains at `73272666` and carries across the documentation-only regeneration.” Add the composition row “`b1f1161b` | Regenerate `docs/DOCUMENTATION_AUDIT.md` with `docs_inventory.py --write` | Step 9 retained #934's audit while earlier train steps added the REBOOT README and changed cited metadata.”
- Verification: PR prose update only; preserve every measured figure, measurement-head label, verdict and acceptance claim. Carry to the residue checklist.

Limits and pending manager duties

This is a documentation-delta review, not a repeated full composition review. Full source banks, implementation routes and hardware tests were not run. Hosted job execution/skipping was not audited in this round. Physical calibration remains NOT RUN; field skips are not hardware proof. Historical receipt stubs and previously recorded limitations retain R866-1's limits. No source fixes, commits, pushes, GitHub writes, hardware operations or other-checkout edits were performed.

The manager still owns validation of the current-dev merge candidate against live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`, the builder/native banks and publication of their receipts, acceptance of hosted and local-replication evidence with executed/skipped contexts distinguished, remaining independent-review requirements, merge authorization, containment and gating hardware qualification. Source validation is distinct from that final candidate. Preserve the existing resource/ROM debts and qualification limits; this verdict does not waive them.

Reproduction and integrity

The portable scripts accept `CHECKOUT PACKET`: `run_gates.py`, `audit_probe.py`, `inventory_history.py`, `verify_evidence.py`, and `verify_integrity.py`. Use the documented dependencies from the disposable environment for documentation gates. The evidence verifier requires the published archive commit fetched into the local object database. The history probe materializes only inventory inputs under `scratch/`; the audit probe restores head bytes in a finally block.

`final-integrity.json` proves raw tracked blob bytes, executable modes, symlink contents and exact index entries against the requested commit, then repeats that proof for the five required initialized submodules. Their heads match the gitlinks: protocol processor `801ef2283ec793e35a2590fc6593c90313a64041`, gPTP processor `1616fc8f062fbf58c35ad31674b5b233207bbdb8`, axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, protocol stack `715589c1db7cf67e2f3259fd7083ebc7f0923376`, and SRP library `08ee86e812a0eb5e1dc6cd61b494d8baf3491348`. The unrelated external submodule is uninitialized and was not used. Checkout status is clean.

MANIFEST.sha256 lists every publishable receipt and script with relative paths. Scratch inputs, extracts and environments are excluded. All foreground processes have completed.

R866-2 FINISHED
