[A331] Author handoff for issue #532

Branch: `532-pasta-invoked-name`
Base: `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`
Head: `ad4a5ff6ba15502ed60d58b3ca91830b50fa9e1c`
Commit: `Preserve pasta invoked name in slot uplink lookup`

[Assignment and decision](https://github.com/kebag-logic/milan-fpga/issues/532#issuecomment-5845269093).
Items 1-2 are implemented. Item 3 remains the post-merge live proof.
Reviewers: [R266] and [R267]. This packet is validation evidence, not a review verdict.
The origin URL was confirmed as `https://github.com/kebag-logic/milan-fpga.git`.

## Change list

| File:line | Change |
|---|---|
| `scripts/act_ci.py:701` | Keep `shutil.which(name, path=SAFE_PATH)`. Only `pasta` returns an absolute path without resolving its final symlink. Every other name still uses `resolve()`. |
| `scripts/act_ci.py:11428` | Add seven offline checks using executable fixtures and real symlinks. Execute only the fake uplink suffix of the production command. |
| `scripts/act_ci.py:12480` | Include the new checks in the existing slot self-test stages. |
| `docs/testing/CI_WORKFLOWS.md:1855` | Document the invoked-name rule and unchanged resolution for other tools. |

Only those two tracked files changed. No workflow, identity check, isolation,
cleanup, command option, or budget changed.
The commit has one subject line, no body, and no trailers.

## Test and mutant table

| Check or mutation | Expected observation | Result |
|---|---|---|
| Executable `pasta` symlink to fake `passt` | Absolute SAFE_PATH spelling retained | PASS |
| Resolve selected path for identity | Same fake `passt` target | PASS |
| Other slot host tools through symlinks | Every tool resolves to its target | PASS |
| Execute the uplink suffix from `slot_uplink_command` | Fake executable observes `pasta` through its invoked name | PASS |
| Remove SAFE_PATH `pasta`, leaving ambient impostor | Refusal | PASS |
| Dangling `pasta` symlink | Refusal | PASS |
| Non-executable `pasta` target | Refusal | PASS |
| Original behavior before the fix | Spelling and execution checks fail | Exactly 2 failures |
| Resolve the pasta lookup again | Same two regression checks fail | KILLED; full offline self-test exits 1 |
| Resolve the uplink path at launch | Execution check fails | KILLED; 1 focused failure |
| Preserve every tool name | Other-tools check fails | KILLED; 1 focused failure |

The focused control passes all seven arms.
The full resolving-path mutant exits 1 on exactly the two new regression arms;
all other arms pass. Expected mutant failures are evidence, not gate failures.
See [mutation_checks.py](mutation_checks.py), [path-mutations.log](path-mutations.log),
[full_mutant_check.py](full_mutant_check.py), and [full-mutant.log](full-mutant.log).
The mutation scripts operate on in-memory source or one temporary file;
they never change the committed runner or start a live replay.

## Gate table

All commands ran in the foreground without pipelines, through the command proxy.
Every gate ran against the head above and returned 0.
The repository embeds its runner unit tests in `act_ci.py --selftest`;
there is no separate act_ci unit-test file or CI invocation in this checkout.
The local runner contract gate is exactly the command from docs.yml.

| Command | RC | Evidence | Log |
|---|---|---|---|
| `python3 -I scripts/act_ci.py --selftest` | 0 | 432 arms, zero failures; includes the repository runner unit and slot checks | [runner-isolated.log](runner-isolated.log) |
| `python3 -B mutation_checks.py` | 0 | 7 control arms pass; 3/3 path mutants killed | [path-mutations.log](path-mutations.log) |
| `bash scripts/act_slot_proof.sh --selftest` | 0 | 44 offline cases pass | [slot-proof.log](slot-proof.log) |
| `python3 scripts/ci_events.py --check` | 0 | 1655 contract items pass | [ci-events-check.log](ci-events-check.log) |
| `python3 scripts/ci_events.py --selftest` | 0 | 2197 arms pass | [ci-events-selftest.log](ci-events-selftest.log) |
| `python3 scripts/act_ci.py --selftest` | 0 | Exact docs.yml command; 432 arms pass | [runner-contract.log](runner-contract.log) |
| `python3 -B scripts/docs_check.py` | 0 | 0 findings; 166 Markdown files, 884 scrubbed text files | [docs-git.log](docs-git.log) |
| `python3 scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` | 0 | 0 findings over 4 added lines; 339/339 arms | [em-dash.log](em-dash.log) |
| `python3 scripts/check_doc_style.py` | 0 | 22 current documents pass | [doc-style.log](doc-style.log) |
| `python3 scripts/gen_toc.py --check` | 0 | 108 Contents pages pass; 17 below threshold | [contents.log](contents.log) |
| `python3 scripts/check_py_idiom.py` | 0 | Ratchet passes without budget changes | [python-idiom.log](python-idiom.log) |
| `python3 scripts/check_sh_idiom.py` | 0 | Existing check_sh_idiom.py passes | [shell-idiom.log](shell-idiom.log) |
| `git diff --check` | 0 | Clean working-tree diff | [diff-working.log](diff-working.log) |
| `git diff --check 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a HEAD` | 0 | Clean complete branch diff | [diff-base.log](diff-base.log) |
| `python3 -B scripts/docs_check.py` (metadata-free export) | 0 | 0 findings; same file counts; expected Git-only parity arm skipped | [docs-no-git.log](docs-no-git.log) |

The metadata-free docs check used a temporary Git archive of the exact head,
without `.git`, matching the second CI mode. The export was deleted afterward;
the lane's Git metadata was never removed. No second checkout was created.
The pinned Markdown requirements were installed into a temporary Python
environment outside this packet. No toolchain or tree export is in this directory.
[run_gates.py](run_gates.py) records the commands and foreground execution;
[gate-results.json](gate-results.json) records the head, exits, durations, and logs.

## Scope and remaining work

Items 1-2 satisfy the assignment. Independent review remains pending.
The manager must rerun the live slot proof from the trusted merged runner
before closing #532. This offline evidence does not claim live connectivity.
There was no push, PR creation/edit, merge, hardware use, privilege escalation,
Docker invocation, or network-namespace creation in this session.
The proposed PR body uses `Relates to #532` so the issue remains open.
