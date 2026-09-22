# [A155] AC5 isolated real-act experiment

Status: recipe and fixture prepared, syntax checked only. No real-act receipt
is claimed. Manager execution and publication remain required.

## Trust boundary and input

Use the final SHA in HANDOFF.md. Start from a clean, exact checkout with the
three normal pinned submodules. Keep the implementation lane untouched.
Use a clean live-dev trusted runner for all host-side resource handling.
Neither candidate `act_ci.py` nor AC5_FIXTURE.py runs on the host.

Generate fixture YAML by running AC5_FIXTURE.py in a disposable uncredentialed
setup job container. Copy the candidate and fixture into its disposable
filesystem; give it no host mount, Docker socket, credential, SSH agent, or
persistent cache. Install PyYAML there. Copy generated YAML/JSON out as data.
The generator explicitly refuses an ordinary host invocation. All subsequent
candidate Python and injection code executes only in act job containers.

Inside that setup container, use the exact candidate SHA and these commands
(the container paths are examples, not host paths):

```sh
python3 /probe/AC5_FIXTURE.py --root /candidate --output /output --sha "$candidate_sha" --mode clean
python3 /probe/AC5_FIXTURE.py --root /candidate --output /output --sha "$candidate_sha" --mode defect
python3 /probe/AC5_FIXTURE.py --root /candidate --output /output --sha "$candidate_sha" --mode swallow
```

The source workflows remain untouched during generation. Each execution copy
keeps every original job, original job property, dependency, condition, action,
and original step in order. Its workflow name is unique to the experiment.
It inserts one explicitly named experiment step immediately before the Python
idiom step in docs-check, or before the contract step in full-ci-gate. Only
the swallow docs execution copy also appends `|| true` to the first idiom call.

Keep these YAML files OUTSIDE `.github/workflows/` in the staged checkout.
The checker must read the original four candidate workflows, modified only
inside each disposable job by the intended single docs-script mutation.
The execution-only injection is not an extra production step being exempted.

## Real-act invocations

Use real act 0.2.89 or the trusted runner's supported version. Create a fresh
boundary per invocation using the trusted runner's sanitized environment,
empty input/secret files, preseeded owned toolcache, isolated network, action
cache, artifact/cache servers, volume leases, and verified cleanup. Retain
the no-socket argument, explicit empty token, 4-core/16-GB limit, and single
concurrent-job limit. Serialize the runs to avoid the global toolcache name.

The manager's experiment driver can use trusted `build_act_command` and
`run_act_process` with the usual boundary helpers. Change only the generated
command's `--workflows` argument to the generated execution-copy path and add
`--job docs-check` for each docs run. Lease the generated workflow name using
trusted `act_job_volume_prefix`, rather than leasing `docs` or `rtl-full`.
Resolve/cache the remote actions using the original candidate workflows;
the execution copies introduce no new action. Keep `--directory` at the
clean exact candidate checkout. This is a mutation experiment, not an
`act_ci.py --pr` success receipt; do not suppress its integrity checks or
publish a manufactured required status.

Use a `pull_request` event with the candidate head, live validation base,
base ref `dev`, repository `kebag-logic/milan-fpga`, and `draft: false`.
The target step must establish `git rev-parse HEAD == GITHUB_SHA`.
No authenticated default-branch read is needed: its existing PR behavior
accepts `unreadable`; scheduled/dispatch semantics are outside this probe.

Execute these four experiments, with fresh checkouts and boundaries:

| Execution copy | Job selection | Required observation |
|---|---|---|
| `carrier-script-407-docs-clean.yml` | `docs-check` | Complete original docs-check succeeds, including idiom and contract steps. An earlier dependency/setup failure invalidates the experiment. |
| `carrier-script-407-docs-defect.yml` | `docs-check` | Unmasked idiom control returns 1 for a planted bare except; actual idiom step fails; contract step is skipped by normal failure propagation. |
| `carrier-script-407-docs-swallow.yml` | `docs-check` | The same unmasked control returns 1; actual tampered idiom step succeeds; actual contract step fails naming the idiom step; complete docs-check fails. |
| `carrier-script-407-rtl-swallow.yml` | Whole workflow, no `--job` filter | full-ci-gate's actual contract step fails naming the idiom step; both exhaustive aggregate jobs run and fail closed. Worker matrices skip because their existing selector condition is false. |

Do not run the generated clean/defect RTL copies: they are unnecessary for
AC5 and would launch the complete RTL sweep. The manager owns normal complete
validation separately. Run the complete RTL swallow graph so act, rather than
a Python model, evaluates `needs`, outputs, job conditions, and failure status.

## What the injection proves

Each injection first requires the exact candidate HEAD and a green pristine
`ci_events --check`. In swallow mode it changes only this line in the
job-local `.github/workflows/docs.yml`:

```diff
-          python3 scripts/check_py_idiom.py
+          python3 scripts/check_py_idiom.py || true
```

The docs defect/swallow experiments also append an unused function with a
bare `except` to the already tracked `scripts/ci_scope.py`, immediately before
the idiom step. The function is never called. The real idiom scanner reads
it and must return exactly 1 with `bare except: 1`; exit 2 or a different
failure invalidates the control. The actual workflow selftest call remains
unchanged. The RTL injection needs only the workflow mutation, since it is
proving the independent runner and downstream fail-closed propagation.

The expected contract diagnostic is:

```text
.github/workflows/docs.yml: job `docs-check` step 34 (`Python idiom gate`) script is not the canonical form: line 1 must be 'python3 scripts/check_py_idiom.py' (found 'python3 scripts/check_py_idiom.py || true'); 2 line(s) expected, 2 found
```

The docs contract step may stop before its following selftest command because
the existing shell correctly propagates `--check`'s nonzero exit. The RTL
decision step must not publish a successful no-op after the failed contract.
Both aggregate fail-closed conditions must therefore select execution; record
their own failed verifier/evidence/worker-result steps, not merely act's global
exit code. Neither aggregate may count as successful or skipped.

## Receipts to publish

Record the candidate SHA, trusted runner SHA/path, fixture hashes, source
workflow hashes from `inputs-*.json`, act version, event JSON, exact sanitized
argv, per-step outcomes, job outcomes, and verified cleanup. Preserve the
unmasked idiom output, successful tampered idiom step, both named contract
refusals, failed docs job, and both failed aggregates. Publish these measured
receipts in the Issue/PR; this recipe is not a substitute for them.

Stop on any missing prerequisite or unrelated earlier failure. Do not skip
an original step, stub a scanner, loosen a guard, alter a required aggregate,
or claim a green docs-check job to manufacture the requested outcome.
