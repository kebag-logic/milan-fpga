# HANDOFF: issue #848, [A739]

Status: REVIEW READY. Nothing pushed; no PR opened. The manager pushes.

| | |
|---|---|
| Branch | `848-audit-drop-line-counts`, lane `$LANES/848-audit-no-lines` |
| Base | dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`, still the live tip at the last check |
| Head | `212b7d6ec506489a4c371e1f214b89a58a60b21e` |
| Commits | `f5ccb318` (the change), `212b7d6e` (fits the module limit, re-pins) |
| Digest | `f502dac7633ecd95fa9f1f9fd05848774f58481cabfbc0d88e393df46d232080`, matches the table |
| Files | `scripts/docs_inventory.py`, `docs/DOCUMENTATION_AUDIT.md`, `ci/image/command-table.json`, `.github/ci-templates/docs.yml` (one comment line) |

## Gates at the head

Clean clone; output in `receipts/clean-clone-gates.txt`.

| Gate | Result |
|---|---|
| `docs_inventory.py --check` | rc 0 |
| `docs_inventory.py --selftest` | rc 0, 53 controls |
| every `run:` step of docs.yml | verifier rc 0: 72 ran, 24 not run with a reason, 0 bad (`receipts/docsyml/docs-yml-table.md`) |
| every job's tree after | clean (`*__tree-after.txt`; the no-git job strips its metadata, so it has none) |
| `git diff --check` dev..head | rc 0 |
| `push-privacy-check.py . origin/dev` | rc 0, 0 private lines |
| `check_py_idiom.py` | rc 0 |

Also: 13 mutants, 13 killed (`receipts/mutants.txt`, script in `receipts/tools/mut848.py`). Real-tree probes are in `receipts/acceptance-probes.txt`: added lines rc 0; page added, page removed and status change each rc 1.

## Where this departs from the assignment

1. **One job did not run in the foreground.** `gate_25_0` is a single gate that cannot be split, and it took 918 s against the roughly 600 s foreground limit. I ran the rest of `docs-gates-1` from that step in a user unit (`RuntimeMaxSec=3000`, `MemoryMax=12G`) and stayed in the session until it finished: rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN`. That one skipped arm is the gate's own `[gate 1b]` MAKEFLAGS arm, and an earlier lane recorded the same verdict.
2. **The runner is a changed copy.** `receipts/tools/` holds the 829 runner and verifier with these changes:
   - lane and virtualenv paths;
   - a clean per-job HOME, so the SDK step installs fresh;
   - job and step `env:` applied, as the later 845 copy does;
   - `not_run.json` taken from the 845 copy, because step ids moved;
   - resuming on the same clone between steps, plus a per-step timeout, so calls fit the foreground limit.

   So each job ran on one fresh clone, but across several calls.
3. **A step was interrupted and rerun.** My own 280 s wrapper killed the runner during `docs-gates-0/gate_28`. No rc was recorded. The orphan exited by itself, the tree was clean, and the step reran on the same clone with rc 0.
4. **One edit outside the script.** `.github/ci-templates/docs.yml` had a comment stating the removed behaviour. `ci_gate_workflows.py --check` stayed rc 0.
5. **Line numbers beyond the issue's literal list.** The Findings `Line` column and the banner line number are not counts, but a line added above them moved them, which fails the acceptance. Declared in TAKEN.
6. **Re-pin method.** No script writes the table's digest; earlier lanes changed that one line. I used `ci_command_table.sha256` and `ci_tool_inventory.serialized`, and the diff is that one line.
7. **Not done, because the assignment barred it or it needs a push.** No Project move, no reviewer set, no `act_ci.py` replica.

## Failed attempt

`f5ccb318` failed `docs-gates-0/gate_39`: `FAIL: long module 11 > ratchet 10`, because the arms took the script to 1044 lines. Logs are in `receipts/attempt1-long-module/`. I folded the finding-line arms into `control()` and dropped four arms I had added:

- an unterminated-line arm, whose count no longer exists;
- a row-shape arm;
- an own-row arm, because the added-line arms already fail if any row carries a count;
- a finding-added arm, because "planted edited quote" and the status arms already cover a finding change.

The script is at 999 lines, and the full docs.yml run was repeated on `212b7d6e`. The ratchet was not raised.

## Open items

1. **Decision needed:** Audience, Purpose and Describes stay, so a title, audience-line or cited-path edit still refreshes the page. That is narrower than a literal "only" in acceptance item 1. It is flagged on #848 and in the PR body, and these rows can still conflict between PRs.
2. **New Issue needed (I may only post on #848):** `ci/image/tool-inventory.json` records command-table digest `c9bd5d35`, while the table at dev is `c20764fa`. No docs.yml step reads it. `ci_tool_inventory.py --check` refuses here without the pinned shell parser, so I did not verify it, and I left the file alone.
3. **Module headroom:** one line. The next change to `docs_inventory.py` will need to cut lines first.
4. **Open docs PRs:** any PR carrying the old page needs one more `--write` after this lands.
5. **`--check`'s success message** still prints the audit page's own line count. That is stdout only and nothing depends on it.
6. **Scratch:** `$VALIDATION_STORAGE/848-a739` keeps the venv and tools; clones and job homes are removed. `$VALIDATION_STORAGE/845-a738/tools` vanished during this run, so an outside cleanup may be active.

## Outputs

- `PR-BODY.md`: PR description.
- `review-ready.md`, `taken.md`: the posted comments.
- `receipts/`: gates, docs.yml logs and table, mutants, probes, tools.
