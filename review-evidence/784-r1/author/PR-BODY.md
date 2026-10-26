[A673]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN (offline) -- `act_ci.py --selftest` PASS (622 arm lines, 610 at dev plus 12 new), runner contract gate rc 0, `ci_events.py --check`/`--selftest` rc 0, every touched docs and Python gate rc 0, five planted mutants each killed by named checks -- `784-act-runner-ubuntu-2404` -> `dev`, head `42dbe6bd42c950a7acedce56fcf29b82543123c6`, one commit on dev `d385b38e`.

## Linked Issue / roles

Relates to #784

This is step 1 of #784 (the act runner). The Issue's acceptance also covers step 2 (the workflows pin `ubuntu-24.04`, no `ubuntu-latest` remains, a hosted run shows `Image: ubuntu-24.04` on every job), which this PR does not do, so it must not close the Issue.

Executor: `[A673]`
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Description

GitHub moved hosted `ubuntu-latest` to the `ubuntu-26.04` image, where the pinned Python tools fail pip resolution (run 40187576861, job 121179871493: `Image: ubuntu-26.04`, `ResolutionImpossible` on `PyYAML==6.0.2`; dev's push run 40187422760 at `d385b38e` ran on `Image: ubuntu-24.04` and passed). #784 decides to pin `ubuntu-24.04`. The act runner refused every label but the literal `ubuntu-latest` and mapped only that label, so a PR that moves the workflows would fail its own replay on the trusted runner. This PR teaches the runner the second label first.

| Piece | Change |
|---|---|
| `scripts/act_ci.py` `RUNS_ON_LABELS` | New constant: the literal `runs-on` labels a candidate job may name, `("ubuntu-latest", "ubuntu-24.04")`, with the reason (#784). |
| `validate_workflow_sandbox` | Accepts a job whose `runs-on` is one of `RUNS_ON_LABELS`, exactly as `ubuntu-latest` was accepted. Every other value is refused before act, and the refusal now names it: `runs on 'ubuntu-26.04'; only the literal labels ubuntu-latest, ubuntu-24.04 are replayed`. |
| `build_act_command` | Passes act one `--platform <label>=catthehacker/ubuntu:full-latest` entry per accepted label, so both labels run on the same runner image. |
| Hosted memory model (beside the `CONTAINER_MEMORY` self-test) | States the 16 GB hosted runner for both labels; a new arm proves a `ubuntu-24.04` replay carries the same 8g memory and swap bound. |
| Self-tests | `selftest_runner_labels`, `selftest_runner_platforms`, `selftest_runner_label_replay` and their helpers (12 new arms). |
| `docs/testing/CI_WORKFLOWS.md` | The runner contract paragraph says both labels are accepted, that others are refused by name, why (hosted `ubuntu-latest` moved to 26.04; step 2 of #784 pins `ubuntu-24.04`), and why every accepted label needs a platform entry. |

Why the platform list matters: the pinned act skips a job whose label has no `--platform` entry as an "unsupported platform" and can still exit 0. A no-daemon dry run of the pinned binary shows it: with dev's single entry, a lone `ubuntu-24.04` job prints `Skipping unsupported platform -- Try running with -P ubuntu-24.04=...` and act exits 0; with both entries the job starts on `catthehacker/ubuntu:full-latest`. An accepted label without an entry would therefore be a green replay of a job that never ran, and the self-test requires the accepted set and the mapped set to be equal.

No STOP: act's `--platform` is a repeatable flag mapping each `label=image` entry, so a second label needs no change to act, the dispatcher patch or the runner image. The workflows are byte-identical to dev (`git diff --exit-code d385b38e -- .github` is empty).

New arms and the mutants they kill (each mutant planted in a scratch copy and run as `python3 -I <copy> --selftest --worktree <checkout>`):

| Mutant | Self-test result | Failing checks |
|---|---|---|
| Platform list drops `ubuntu-24.04` (dev's form) | rc 1, 3 failures | `act's platform list maps ubuntu-latest and ubuntu-24.04 to the runner image, once each`; `every runs-on label the sandbox accepts has a platform entry, and nothing else does`; `a job on ubuntu-24.04 passes the sandbox and dry-run replays to an act command that maps ubuntu-24.04 to the runner image` |
| `ubuntu-24.04` mapped to act's default `node:16-bullseye-slim` | rc 1, 3 failures | the same three |
| `RUNS_ON_LABELS` back to `("ubuntu-latest",)` | rc 1, 4 failures | `a job on ubuntu-24.04 is accepted by the sandbox`; the dry-run replay check; `a ubuntu-24.04 replay holds its job containers to the same 8g memory and swap bound as ubuntu-latest`; the platform list check |
| Sandbox accepts any `ubuntu-` label | rc 1, 5 failures | `a job on ubuntu-26.04 is refused before act, and the refusal names ubuntu-26.04`; the same for `ubuntu-22.04`; `the arm image of an accepted label is refused: only the exact literal is replayed`; `a job on ubuntu-26.04 is refused naming ubuntu-26.04, before any Docker boundary or act command`; the accepted-equals-mapped check |
| Refusal text back to dev's `must use literal ubuntu-latest` | rc 1, 3 failures | both `refusal names` checks and the `ubuntu-26.04` replay refusal check |

## Authoritative references

- #784, Decision (step 1) and Acceptance (step 1); the step 1 assignment comment on #784.
- [AGENTS.md section 5](../AGENTS.md#5-executor-procedure) and [Act-first local replication](../docs/testing/CI_WORKFLOWS.md#act-first-local-replication): the bootstrap rule. The trusted runner on dev replays this PR; the candidate runner was tested offline only.
- [docs/testing/CI_WORKFLOWS.md](../docs/testing/CI_WORKFLOWS.md), the runner contract paragraph beginning "Candidate jobs must name one of two literal runner labels".
- Pinned act 0.2.89 source: `cmd/root.go` (`--platform` is a string array), `cmd/platforms.go` (`newPlatforms` maps each entry over act's defaults), `pkg/runner/run_context.go` (`isEnabled` skips an unmapped label; `Executor` returns nil for it).

## How to get into the same state

```sh
git fetch origin
git switch --detach 42dbe6bd42c950a7acedce56fcf29b82543123c6
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

The CI tooling gates need PyYAML (the hosted pin is `PyYAML==6.0.2` in `ci/constraints-ci.txt`). The evidence below was taken on CPython 3.12.3 with PyYAML 6.0.2, the hosted pair, and again on CPython 3.14 with PyYAML 6.0.3.

## How to validate

```sh
python3 scripts/act_ci.py --selftest
install_dir="$(mktemp -d)"
install -m 0555 scripts/act_ci.py "$install_dir/act_ci.py"
python3 -I "$install_dir/act_ci.py" --selftest --worktree "$PWD"
rm -rf "$install_dir"
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
git diff --exit-code d385b38e5282b395ca55d49d135e46a93f56a340 -- .github
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base d385b38e5282b395ca55d49d135e46a93f56a340
python3 scripts/gen_toc.py --check
python3 scripts/check_doc_paths.py
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_py_idiom.py
python3 scripts/generate_ci_evidence_pins.py --check
python3 scripts/ci_runtime_evidence_selftest.py
```

Expected result / pass criteria: every command exits 0. Both self-test runs end `selftest: PASS` and print these new arms as `ok`:

```text
a job on ubuntu-latest is accepted by the sandbox
a job on ubuntu-24.04 is accepted by the sandbox
a job on ubuntu-26.04 is refused before act, and the refusal names ubuntu-26.04
a job on ubuntu-22.04 is refused before act, and the refusal names ubuntu-22.04
an upper-case spelling of an accepted label is refused: only the exact literal is replayed
the arm image of an accepted label is refused: only the exact literal is replayed
a one-label list of an accepted label is refused: only the exact literal is replayed
a job on ubuntu-24.04 passes the sandbox and dry-run replays to an act command that maps ubuntu-24.04 to the runner image
a ubuntu-24.04 replay holds its job containers to the same 8g memory and swap bound as ubuntu-latest
a job on ubuntu-26.04 is refused naming ubuntu-26.04, before any Docker boundary or act command
act's platform list maps ubuntu-latest and ubuntu-24.04 to the runner image, once each
every runs-on label the sandbox accepts has a platform entry, and nothing else does
```

The `git diff` prints nothing: no workflow, template or generator changed.

## Known limitations / out of scope

- Step 2 of #784 (generators and workflows say `runs-on: ubuntu-24.04`, then the runner refuses `ubuntu-latest`, and `TESTING.md` names the image) is a separate PR after this one merges. Until then the workflows still name `ubuntu-latest` and hosted jobs still land on `ubuntu-26.04`, so hosted required checks on this PR can fail at pip resolution for the reason #784 records, not because of this change.
- "Replays" in the self-test is an offline dry run through `run_validation` with the real sandbox and act command builder, Git, GitHub, Docker and act faked; per the bootstrap rule the candidate runner was not run with `--sudo`, against a real PR, or through a replay slot. The act-first replica of this PR is the trusted dev runner's.
- act sets `ImageOS` per label (`ubuntu20` for `ubuntu-latest`, `ubuntu24` for `ubuntu-24.04`). Nothing in `.github/` or `scripts/` reads it, and the audited `actions/setup-python@v5` bundle does not either, so the step 2 label change does not reach any step through it.
- act lower-cases a label before looking up its image; the sandbox matches the exact literal, so an upper-case spelling is refused rather than replayed.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (step 1 items met; step 2 is a later PR)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
