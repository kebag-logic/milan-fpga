[A607]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

Local gates green: 507/507 self-test arms, all required checks rc 0.
`730-act-cpusets` -> `dev`, head `ede700b00ef4d79566a6f108b11ce9bd4ad6beaa`.
Round 5 awaits independent re-review. These commits have not been pushed by this lane.

## Linked Issue / roles

Relates to #730

Acceptance 1 and 2 are proven offline. Acceptance 3's same-head verdict comparison,
acceptance 4's measurement and optional acceptance 5 remain manager duties after merge,
under the [no-replay ruling](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131815815).
The Issue must remain open for those obligations.

Executor: `[A607]`
Internal cleared-context reviewer: `[R632]`
External reviewer: `[R633]`

## Description

Each concurrent replay container now receives its own four-CPU range. Previously all matrix
legs shared four CPUs. The runner derives the number of ranges from the replayed workflows'
`max-parallel` and `CONCURRENT_JOB_LIMIT`; it refuses unsupported concurrency or insufficient
host CPUs, including on slot 0.

| Piece | Result |
| --- | --- |
| Layout | Slot N owns `20N..20N+19`: staging at `20N..20N+3`, followed by four job ranges. Each run uses its derived number of ranges. |
| Placement | An ownership-filtered event stream moves each created container to a reserved range. Reservations survive `die` and uncertain updates; only removal releases them. `docker inspect` determines placement. |
| Verdict | Containers left on staging produce warnings. The workflow verdict continues to follow act's exit alone. |
| Bounds | Each container retains four CPUs, 16 GB memory and no extra swap. The isolated-slot cap remains 24G. No workflow, step, job, suite, testbench, RTL or firmware changes. |
| Cleanup | The event stream is contained, the reader joined and proven ended, and its pipe finalized before outer teardown. Failed cleanup steps do not skip later obligations. First-failure precedence and conventional signal status are preserved. |

| Slot | Before: every concurrent container | After: staging | After: separate concurrent containers |
| --- | --- | --- | --- |
| 0 | `0-3` | `0-3` | `4-7`, `8-11`, `12-15`, `16-19` |
| 3 | `12-15` | `60-63` | `64-67`, `68-71`, `72-75`, `76-79` |
| N | `4N..4N+3` | `20N..20N+3` | Container j, numbered 1-4: `20N+4j..20N+4j+3` |

The standing disjointness proof covers all 64 slots at maximum concurrency: 320 four-CPU
ranges, including staging. Planted cross-slot and within-slot overlaps fail the proof;
staging planted on a job range is refused. The offline dry-run harness prints each slot-0
and slot-3 container range through the real planning path with inert external boundaries.

### Round 5

Addresses [R633-4-F1](https://github.com/kebag-logic/milan-fpga/pull/731#issuecomment-6134026466)
under the [Round 5 assignment](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6134111240).
A first signal at the body-to-cleanup transition could previously bypass containment and
reader completion.

- `scripts/act_ci.py:5650`: the CPU monitor blocks `CLEANUP_SIGNALS` before yielding.
  The reader inherits the mask. It remains held through containment, reader completion,
  dead-thread proof and pipe finalization.
- `scripts/act_ci.py:278`: only after cleanup does the incoming mask return and a held
  signal get delivered. Earlier body failures retain precedence. Otherwise the signal
  keeps status `128 + signal`, with secondary cleanup errors reported beside it.
- `scripts/act_ci.py:5313` and `:15565`: normal act and the live interrupt probe temporarily
  unblock signals while act runs, restoring the mask before monitor cleanup. A pending
  signal at the normal boundary's opening cannot bypass mask restoration.
- `scripts/act_ci.py:8309`: standing controls deliver INT/TERM/HUP at the exact cleanup
  entry and inject a signal at each of 198 executed line steps through mask release,
  both to the main thread and process-wide. All 396 injections require complete cleanup
  before teardown, conventional status and diagnostic, and no residual signal mask/pending
  signal. Failure stops the sweep at its first counterexample.
- `scripts/act_ci.py:12390` and `:12443`: offline controls pin both act signal windows.
- `docs/testing/CI_WORKFLOWS.md:1813`: the authoritative guarantee now describes the mask,
  thread inheritance, temporary windows and delivery/precedence rule.

The unchanged R633-4 cleanup-entry probe passes all six cases. Earlier published shutdown,
lifecycle, allocation and derivation probes pass. R632's unchanged campaigns retain their outcomes: 36/36 killed in Round 2; 24/30 in
Round 3, Q24 killed, with the same six prior survivors. All eight new signal controls fail
when their targeted protection is removed. Receipts are recorded in the handoff and issue evidence. The earlier cleanup-entry caveat is superseded by this fix;
independent review of this head remains required.

### Measurement status

No replay ran in Round 5. The retained partial before run is not a completed comparison.

| Run | Job | Per-job wall clock | Slot memory peak | Verdict |
| --- | --- | --- | --- | --- |
| Partial before, dev `dc4d06cb`, PR #728 `2c2f3369`, slot 3 | full-ci-gate | 15 s | 15.1 GiB sampled before stop | succeeded |
| Same partial before | Verilator shards 0-3 | 20:02:57-20:10:36 UTC, interrupted | same sample | interrupted; replay rc 130 |
| Same partial before | Verilator 4, Yosys 0-3 | no completed timing | same sample | interrupted |
| After, this head | all | not run per ruling | not measured | not measured |

The manager compares the recorded slot-0 before runs (#721 at `42678ae2`, #715 at `c7d0ad63`)
with the first replay on merged code. After merge, from the clean candidate and using the
trusted runner, the measurement command is:

```sh
python3 -I <trusted-dev>/scripts/act_ci.py --pr <number> --sudo --workflow rtl-full
```

Read timestamped per-job setup-to-finish intervals, the CPU plan, the workflow verdict,
and the CPU summary. For a complete full run, expect all 12 containers confirmed by inspect,
none removed before placement or left unconfirmed, at most four reserved ranges, and no
CPU-range warning. For an isolated slot also record `memory peak` and cap-hit count.
Slot 0 has no aggregate slot-memory cap or corresponding peak line.

## Authoritative references

- #730 acceptance 1-5 and its public round decisions.
- `REQUIREMENTS.md`, section 8; `CONTRIBUTING.md`, workflow and verification rules.
- `docs/testing/CI_WORKFLOWS.md`: act-first replication and parallel replay slots.
- #532 slot ownership, lease, cleanup, resource and refusal contracts.

## How to get into the same state

Use CPython 3.12.3 in a disposable validation environment with the pinned Markdown renderer.
The final local source is the head above; publication belongs to the manager.

```sh
git switch 730-act-cpusets
git rev-parse HEAD
python3 --version
python3 -m pip install pyyaml==6.0.3
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

## How to validate

Run candidate self-tests only inside a disposable offline job boundary. No live replay or
live self-test is authorized for this lane. Commands are plain shell:

```sh
python3 -I scripts/act_ci.py --selftest
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
scripts/act_slot_proof.sh --selftest
python3 scripts/check_py_idiom.py
python3 scripts/check_py_idiom.py --selftest
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/check_em_dash.py --base dc4d06cb
python3 scripts/check_doc_paths.py
git diff --check dc4d06cb HEAD
```

Expected: every command rc 0; runner self-test 507 ok, 0 FAIL; CI contract 2016 items/2828
arms; slot proof 44 cases; Python idiom 54 controls with unchanged ratchets; bare-metal
700 controls; zero documentation or whitespace findings.

## Known limitations / out of scope

- Live Docker placement, wall-clock effects, memory effects and verdict comparison remain
  unmeasured under the no-replay ruling. The live interrupt window is pinned offline only.
- `--dry-run` enters the existing daemon boundary; only the offline harness was used.
- A container temporarily runs on staging. Failed or uncertain placement retains its
  reservation and prints a warning; it never changes the candidate verdict.
- Every concurrent slot must use the same runner version, because old and new layouts overlap.
- Unrelated optional review suggestions remain outside Round 5.
- Hosted acceptance, current-dev candidate validation and post-merge containment remain pending.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required focused local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive at this head
- [ ] External review is positive at this head
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
