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

Focused local gates pass: 525/525 runner self-test arms and all required checks rc 0.
`730-act-cpusets` -> `dev`, head `73b8dcd667aa5bf1254e828dd1dd7217c8a103ce`.
Round 6 awaits independent re-review. These two new commits have not been pushed.

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

Each concurrent replay container receives its own four-CPU range. Previously all matrix
legs shared four CPUs. The runner derives the ranges used from the replayed workflows'
`max-parallel` and `CONCURRENT_JOB_LIMIT`. Unsupported concurrency and insufficient CPUs
refuse the run, including on slot 0.

| Piece | Result |
| --- | --- |
| Layout | Slot N owns `20N..20N+19`: staging followed by four job ranges. Each run uses its derived number of ranges. |
| Placement | An ownership-filtered event stream moves each container to a reserved range. Reservations survive `die` and uncertain updates until removal. Inspect confirms placement. |
| Verdict | Unconfirmed placement prints a warning; act's exit still determines the workflow verdict. |
| Bounds | Four CPUs per container, 16 GB memory without extra swap, and the isolated-slot 24G cap remain unchanged. |
| Cleanup | Stream containment, reader completion and pipe finalization precede outer teardown, including failure and interruption paths. |

| Slot | Before: every concurrent container | After: staging | After: separate concurrent containers |
| --- | --- | --- | --- |
| 0 | `0-3` | `0-3` | `4-7`, `8-11`, `12-15`, `16-19` |
| 3 | `12-15` | `60-63` | `64-67`, `68-71`, `72-75`, `76-79` |
| N | `4N..4N+3` | `20N..20N+3` | Container j, numbered 1-4: `20N+4j..20N+4j+3` |

The standing proof covers all 64 slots at maximum concurrency: 320 four-CPU ranges,
including staging. Planted cross-slot and within-slot overlaps fail; staging planted on
a job range is refused. Offline dry-run output lists every slot-0 and slot-3 range.

### Round 6

Addresses [R633-5-F1](https://github.com/kebag-logic/milan-fpga/pull/731#issuecomment-6137685765)
under the [Round 6 assignment](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6137869227).
A first signal at the normal boundary's closing restore previously replaced an active
integrity Refusal, hiding its reason and changing status 2 to a signal status.

- `scripts/act_ci.py:5313` records the active failure before closing. If restoration is
  interrupted, it restores the hold, reports the later signal and preserves that failure.
  Act remains interruptible; a pending signal prevents its start. With no earlier failure,
  conventional signal status remains unchanged.
- `scripts/act_ci.py:12469` and `:12570` add 18 standing cases using the real monitor and
  boundary with a real reader. They inject INT/TERM/HUP at both closing restores, with no
  earlier failure, a Refusal and a RuntimeError. They require the earlier exception and
  diagnostic, restored hold before monitor cleanup, contained stream, ended reader and
  closed pipe before teardown.
- `docs/testing/CI_WORKFLOWS.md:1819` states closing precedence and its diagnostic.
  `:1833` and `:1838` apply R632-5-R1 and R632-5-R2 exactly.

The unchanged R633-5 probe fails on the starting head and passes all nine cases with the
fix. Existing cleanup-entry, lifecycle, shutdown and derivation probes pass. The self-test
retains all previous 507 arms. All eight Round 5 fault controls and seven new closing faults
are rejected. Removing all closing restores exits 129; the other new controls name failures.
The earlier per-step sweep remains covered; its step count depends on the interpreter.
Final-head unchanged mutation campaigns retain their outcomes: R632-2 kills 36/36;
R632-3 kills 24/30, including Q24. Survivors remain Q06/Q11/Q13/Q15/Q28/Q29;
Q15 is the previously recorded equivalent control. Neither campaign has a bad anchor.
The campaign drivers exit 0; the mutant nonzero statuses are expected.
Receipts: `receipts/r6/head-mutants-r2.log` and `head-mutants-r3.log`.
Both public driver files match their published sha256. The final runs use an export of
`73b8dcd667aa5bf1254e828dd1dd7217c8a103ce`, with no subsequent source edits.

### Measurement status

No replay ran in Round 6. No speedup is claimed.

| Run | Job | Per-job wall clock | Slot memory peak | Verdict |
| --- | --- | --- | --- | --- |
| Partial before, dev `dc4d06cb`, PR #728 `2c2f3369`, slot 3 | full-ci-gate | 15 s | 15.1 GiB sampled before stop | succeeded |
| Same partial before | Verilator shards 0-3 | 20:02:57-20:10:36 UTC, interrupted | same sample | interrupted; replay rc 130 |
| Same partial before | Verilator 4, Yosys 0-3 | no completed timing | same sample | interrupted |
| After, this head | all | not run per ruling | not measured | not measured |

The manager compares recorded slot-0 before runs (#721 at `42678ae2`, #715 at `c7d0ad63`)
with the first replay on merged code. After merge, from the clean candidate, the command is:

```sh
python3 -I <trusted-dev>/scripts/act_ci.py --pr <number> --sudo --workflow rtl-full
```

Read timestamped per-job setup-to-finish intervals, the CPU plan, verdict and CPU summary.
For a complete full run, expect all 12 containers confirmed, none removed before placement
or left unconfirmed, at most four reserved ranges, and no CPU-range warning. Isolated slots
also report memory peak and cap hits; slot 0 needs separate memory sampling.

## Authoritative references

- #730 acceptance 1-5 and public round decisions, especially Round 6.
- `REQUIREMENTS.md`, section 8; `CONTRIBUTING.md`, workflow and verification rules.
- `docs/testing/CI_WORKFLOWS.md`: act-first replication and parallel replay slots.
- #532 slot ownership, lease, cleanup, resource and refusal contracts.

## How to get into the same state

Use CPython 3.12.3 in a disposable offline validation environment with the pinned renderer.
The final source is the head above; publication belongs to the manager.

```sh
git switch 730-act-cpusets
git rev-parse HEAD
python3 --version
python3 -m pip install pyyaml==6.0.3
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

## How to validate

Run candidate self-tests inside a disposable offline job boundary.
The local act runner contract gate is the runner self-test below.

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

Expected: every command rc 0; runner self-test 525 ok, 0 FAIL; CI contract 2016 items/2828
arms; slot proof 44 cases; Python idiom 54 controls with unchanged ratchets; bare-metal
700 controls; zero documentation or whitespace findings. Re-run both unchanged public
mutation campaigns and the boundary-precedence probe in the same disposable boundary.

## Known limitations / out of scope

- Live placement, `nproc`, wall-clock effects, memory effects and verdict comparison remain
  unmeasured under the no-replay ruling. There are no workflow, suite, testbench, RTL or
  firmware changes.
- Live `--dry-run` enters the daemon boundary; only the offline harness was used.
- A container temporarily runs on staging. Uncertain placement retains its reservation and
  prints a warning without changing the candidate verdict.
- Concurrent slots must use the same runner version because old and new layouts overlap.
- Prior optional test survivors remain disclosed; they are not claimed as kills.
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

