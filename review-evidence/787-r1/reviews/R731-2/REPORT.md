[R731] POSITIVE - exact head 4aa5666e730ae877766ed88c48bc8001e7a7b7b3

# R731-2: internal cleared-context delta review of PR #822 (#787)

- PR: kebag-logic/milan-fpga #822, `787-reboot-reset` -> `dev`, 15 commits, not draft.
- Head `4aa5666e730ae877766ed88c48bc8001e7a7b7b3`, tree `979c622ae9195527f4c637767658b3af59f2f069`.
- Previously reviewed head: `667b9bbc02b99a08d71efab750f95e8702cbbe57` (R731-1, `[R731] POSITIVE`).
- Source base `1e80128f`; the manager's live dev is `71d6ed07`.
- Scope: the one commit `667b9bbc..4aa5666e`. R731-1 stands for everything the delta does not touch.

## Verdict

POSITIVE. The delta is exactly as stated.

- It deletes one line, the blank line at the end of `tests/steps/torture_release_steps.py`.
- It changes no other path, mode or gitlink.
- `git diff --check 1e80128f 4aa5666e` exits 0. At `667b9bbc` it exits 2 on that file's new blank line at EOF, which is the refusal the merge candidate reported.
- The file at the head is the same blob as at the base (`07dd9680`). The PR's net diff no longer touches it.
- behave collects the file as before, and the feature that uses it passes.

No BLOCKER, MAJOR or MINOR finding is open.

## What was checked (receipts under `receipts/`)

| Check | Result | Receipt |
|---|---|---|
| `git diff 667b9bbc 4aa5666e` | 1 file, 0 insertions, 1 deletion: the trailing empty line after `assert actual == verdict, detail`. Raw: `100644 -> 100644`, blob `5ed3db84 -> 07dd9680`. No gitlink in the delta. | `delta.txt` |
| Byte check | The head blob is the parent blob minus its last byte, a `\n` (`cmp` identical). Sizes are 51,884 and 51,883 bytes. The file ends in one `\n`. | `file-check.txt` |
| Net PR effect on the file | The blob at `1e80128f` is also `07dd9680`. `git diff --stat 1e80128f 4aa5666e` on the file is empty. The PR's file list (59 files) no longer lists it. | `pr-range-file.txt`, `pr-metadata.txt` |
| `git diff --check 1e80128f 4aa5666e` | rc 0, no output | `diff-check-1e80128f-4aa5666e.txt` |
| `git diff --check 1e80128f 667b9bbc` (control) | rc 2: `tests/steps/torture_release_steps.py:961: new blank line at EOF.` | `diff-check-1e80128f-667b9bbc.txt` |
| `py_compile` | ok. The byte-code was written under `scratch/`, not into the tree. | `file-check.txt` |
| `cd tests && behave --dry-run` at the head, and with the parent blob planted in the clone | Identical, rc 0 both: 12 untested features, 2 "failed", 508 scenarios and 2,330 steps untested. Both "failed" entries, `aecp_response_contract.feature:5` and `milan_base_formats.feature:44`, are behave's dry-run status for files this delta does not touch, and they are the same with the parent blob. JSON check: 0 undefined steps. 382 step matches resolve into `torture_release_steps.py`. | `behave-dry-run-4aa5666e-inclone.txt`, `behave-dry-run-667b9bbc-inclone.txt` |
| `behave features/torture_campaign_plan.feature` at the head | 1 feature, 189 scenarios and 708 steps passed, rc 0 | `behave-torture_campaign_plan-4aa5666e.txt` |
| Comment-rule scan of the delta | 0 added lines, so no new instance | `retained-findings.txt` |
| Clone integrity after the parent-blob probe | HEAD and the index tree are both `979c622a`, with 0 status lines. The file's blob is `07dd9680`, mode 644. No flagged index entries. All six gitlinks are unchanged, and the delta changes none of them. | `clone_integrity.txt` |

## Findings

No new finding. The delta adds no line and changes no code, test, figure or document.

The open items from round 1 at `667b9bbc` are not touched by the delta. They are retained at this head unchanged:

| ID | Severity | Lenses | Artifact | Status at `4aa5666e` |
|---|---|---|---|---|
| R731-1 F1 (= R732-1 R2) | RESIDUE | Docs | `tb/verilator/reboot_ctrl/mutants.py:113-114`, a comment with a lane label and an issue-comment ID | **Retained**, still in the tree. Exact fix as in R731-1: `# the egress arms of the REBOOT silicon defect (#787): the PHY hold on the request alone, an egress wait that ignores the MAC FIFO, an egress wait with no bound`. |
| R732-1 R1 | RESIDUE | Docs | `tb/tools/torture_campaign.py:3136-3138`, a link-down comment that omits the egress wait | **Retained**, still in the tree. Its exact fix is in R732-1. |
| R731-1 S1 | SUGGESTION | Tests, Robustness | `hdl/milan/milan_datapath.sv:9760, 9763` beat and flush wirings | Retained, optional; `hdl/` is unchanged since `667b9bbc` |
| R731-1 S2 | SUGGESTION | Tests | `hdl/milan/KL_reboot_ctrl.sv:290, 296` quiet-window edges | Retained, optional |
| R732-1 S1, S2 | SUGGESTION | RTL, Robustness; Tests | `KL_reboot_ctrl.sv:257-262`; `mutants.py` saturation control | Retained, optional |

## Reviewer-owned ledger

Each lens was applied to the delta at this head. R731-1's coverage carries to this head because nothing in that lens's scope changed. The delta only removes trailing whitespace from a step file, and the file's steps match, compile and pass the same.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Delta: no requirement, wire or clause artifact touched (`delta.txt`). Rest: R731-1 at `667b9bbc`, unaffected. | R731-2 (delta), R731-1 (rest) | `4aa5666e730ae877766ed88c48bc8001e7a7b7b3` |
| RTL | CLEAN | Delta: no `hdl/`, constraint, SoC or gitlink change (`delta.txt`, `retained-findings.txt`). Rest: R731-1, unaffected. | R731-2, R731-1 | `4aa5666e730ae877766ed88c48bc8001e7a7b7b3` |
| Robustness | CLEAN | Delta: no behaviour path changed. Rest: R731-1, unaffected (S1 is optional). | R731-2, R731-1 | `4aa5666e730ae877766ed88c48bc8001e7a7b7b3` |
| Tests | CLEAN | `tests/steps/torture_release_steps.py`: byte check, `py_compile`, behave dry-run identical to the parent, `torture_campaign_plan.feature` 189 of 189. Rest: R731-1, unaffected. | R731-2, R731-1 | `4aa5666e730ae877766ed88c48bc8001e7a7b7b3` |
| Docs | CLEAN (RESIDUE F1 and R1 carried) | Delta: 0 added lines, no new comment-rule instance, `git diff --check` clean. Rest: R731-1, unaffected. | R731-2, R731-1 | `4aa5666e730ae877766ed88c48bc8001e7a7b7b3` |

## Real limits

- I re-ran no Verilator, builder, Yosys or route work for this delta. The delta cannot affect them, and R731-1's limits stand.
- The behave runs were the dry-run collection and the one feature that uses the file, not the whole behave suite.
- No manager source bank ran at this head, and none is claimed.
- The current-dev candidate on `71d6ed07` was not built here.
- Physical calibration was NOT RUN. Desk results are not hardware proof.

## Pending manager duties

- Rebuild and validate the current-dev merge candidate on `71d6ed07`: `git diff --check`, then the builder and native banks. Link its receipts, and own hosted and act acceptance at the exact head.
- Carry RESIDUE F1 and R1 to the residue checklist.
- Re-record the area and route records on dev under the record rule (R731-1 limits).
- Run the bench: DEPARTING on the wire, then the #396 power area's 50 soft resets. #787 stays open until then.
- The external review of this head is still owed.

## Prior public findings at this head

(Written after the verdict and the ledger above were on disk.)

I read PR #822's issue comments (7), reviews (0) and review comments (0), and issue #787's comments.

- **Reviews since `667b9bbc`.** The only reviews of this PR are R731-1 and R732-1, both `POSITIVE` at `667b9bbc`. Their findings are all accounted for in the Findings table above. Two RESIDUE items are retained (R731-1 F1 / R732-1 R2, and R732-1 R1). Four SUGGESTIONs are retained as optional. None was resolved by this delta, and none is under a lens the delta could clear or dirty.
- **The manager's refusal** (`issuecomment-6537798578`) names exactly the defect this delta removes: `tests/steps/torture_release_steps.py:961: new blank line at EOF` on candidate dev `71d6ed07`, with the full-native bank passing (rc 0). My `diff-check-1e80128f-667b9bbc.txt` reproduces the refusal, and `diff-check-1e80128f-4aa5666e.txt` shows it gone. **Resolved at this head.**
- **Other entries since round 1** are the R731-2 and R732-2 start notices. Neither carries a finding.
- **Verdict:** nothing here changes the verdict or the ledger.

R731-2 FINISHED
