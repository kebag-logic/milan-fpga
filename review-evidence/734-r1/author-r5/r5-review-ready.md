[A613] REVIEW READY - Round 5

Head: `7c862ad980dfe829ef4d85ff8f4fb4fab451984f`. One local merge commit, with parents `59354ffe75697e17a16fd117d9ba853e104394bc` and the fetched dev `0136de16291a127e0a34627c77ac09cd41efc08b`. No push, PR edit, rebase or amend.

Only `scripts/ci_events.py:598` conflicted. The resolution preserves the lane's live-base PR scope inputs and dev's two firmware-boundary aggregate result inputs. `act_ci.py` and `CI_WORKFLOWS.md` merged automatically: the stack trust entry, six-entry manifest and five public pins coexist with composed live-base replay, inline histories and the complete isolated flat-install check. Both policy texts survive.

Merged-tree validation, all rc 0:

- The exact runner contract CI step passes in a disposable isolated job: `act_ci.py --selftest` passes 570 assertions; the documented mode-0555 single-file installation under isolated Python passes 568. All four stack-manifest refusal controls pass in both forms.
- `ci_scope.py --selftest`: 198 assertions and 48 killing history mutations. All 30 before/after selector rows agree, including REV, REV+E and historical B16.
- `ci_events.py --check` and `--selftest`: 2174 contract items and 3096 arms.
- Documentation, source-list, evidence-reader, idiom and linked-image audit checks pass. All five freshly rebuilt linked images are byte-identical to the pre-merge images.

The tested tree is `622e79ae2a21917a49426c675d417307104112a1`, verified equal to the committed tree. The worktree is clean. Product inputs and gitlinks equal dev exactly; only the required stack submodule was newly initialized at its pin.

HANDOFF.md and PR-BODY.md contain Round 5 changes, conflict disposition, scope, coverage, mutation, gate/control and image-hash tables. The prepared body retains one Closes #734. Independent review of this head, manager publication, trusted replay, hosted acceptance and current-dev candidate banks remain pending.
