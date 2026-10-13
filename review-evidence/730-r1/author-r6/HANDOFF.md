[A607]

## Round 6

Head: `73b8dcd667aa5bf1254e828dd1dd7217c8a103ce` on `730-act-cpusets`, clean and two commits ahead of its remote.
Starting head: `ede700b00ef4d79566a6f108b11ce9bd4ad6beaa`.
Source base: `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`.
Origin was confirmed as the assigned repository. No identity or configuration changed.

Assignment: [Round 6](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6137869227).
Reviews: [R633-5-F1](https://github.com/kebag-logic/milan-fpga/pull/731#issuecomment-6137685765)
and [R632-5](https://github.com/kebag-logic/milan-fpga/pull/731#issuecomment-6137864130).
Executor `[A607]`; internal reviewer `[R632]`; external reviewer `[R633]`.
The assignment settles the reviewers' disagreement: the active failure wins at closing.
Independent review of this new head is still required.

New commits, with one-line subjects and no trailers:

- `9be1bc44480109086e77a03ca33b36d7e980c81c`: preserve active failures when the act signal window closes.
- `73b8dcd667aa5bf1254e828dd1dd7217c8a103ce`: document closing-signal precedence and exact diagnostics.

No push, PR edit, replay, live dry-run, daemon operation, hardware access, or Vivado lock.
No workflow, suite, testbench, RTL, firmware, gitlink or generated file changed.
The unused lwSRP submodule remains uninitialized.

### Changes and evidence

| File:line | Change | Evidence |
| --- | --- | --- |
| `scripts/act_ci.py:5313` | The normal boundary records an escaping failure before closing its signal window. A first signal interrupting restoration cannot replace it. Restoration is retried before the secondary diagnostic, with a final restore on every exit. Act remains interruptible, pending signals arrive before act starts, and signal-only outcomes retain conventional status. | R633-5's unchanged probe; standing window and closing controls. |
| `scripts/act_ci.py:12415` | Existing interruptibility and pending-signal controls invoke the new closing controls. | Full self-test, 525 ok / 0 FAIL. |
| `scripts/act_ci.py:12469` | Real monitor and real normal boundary, with inert process collaborators and a real reader. It checks the mask during act, at the boundary-to-monitor handoff and at containment; reader completion and pipe closure precede outer teardown. | 18 cases: INT/TERM/HUP at both closing restores, with no earlier failure, a Refusal or a RuntimeError. |
| `scripts/act_ci.py:12570` | Standing injection points come from both boundary `finally` entries, including the first restore where signals remain open. The earlier exception's identity and diagnostic survive; later signals are reported beside it. | Restoring the original boundary fails nine cases; the guarded restore itself is exercised. |
| `docs/testing/CI_WORKFLOWS.md:1819` | States closing-window precedence, restored hold and the actual secondary-signal message. | Documentation gates pass. |
| `docs/testing/CI_WORKFLOWS.md:1833` | Applies R632-5-R1's exact monitor message. | Documentation gates pass. |
| `docs/testing/CI_WORKFLOWS.md:1838` | Applies R632-5-R2: "Throughout, the first failure wins." | Documentation gates pass. |

The unchanged public probe has sha256
`de6247850b64d9ece52b08e896427c254cd912b6bc8c7e55ceae076a1e468700`.
It was fetched from public evidence commit `44ed94470ffa0598be81bc8916c2d21f026b3fd8`.
At the starting head it exits 1: three closing cases replace the Refusal.
At the corrected runtime all nine cases exit with the original Refusal (status 2),
and every case contains the stream, ends the reader and closes the pipe.
The later signal is printed beside the failure, never substituted for it.
Receipts: `receipts/r6/boundary-precedence-before.log` and `boundary-precedence-after.log`.

### Validation

All normal gates ran in foreground disposable offline namespaces on CPython 3.12.3,
with PyYAML 6.0.3 and the pinned Markdown renderer. No candidate host orchestration ran.
Commands below are the commands inside that disposable boundary; no gate was piped.
Both final gate groups used the committed head above. Full logs, individual statuses,
commands and elapsed times are in `receipts/r6/head-code/` and `head-docs/`.

| Command | Result |
| --- | --- |
| `python3 -I scripts/act_ci.py --selftest` | rc 0; 525 ok, 0 FAIL; all previous 507 arms retained. This is the workflow's local act runner contract gate. |
| `python3 scripts/ci_events.py --check` | rc 0; 2016 contract items. |
| `python3 scripts/ci_events.py --selftest` | rc 0; 2828 arms. |
| `scripts/act_slot_proof.sh --selftest` | rc 0; 44 cases. |
| `python3 scripts/check_py_idiom.py` and `--selftest` | rc 0; unchanged ratchets, 54 controls. |
| `python3 scripts/check_baremetal_only.py --check` and `--selftest` | rc 0; 700 controls. |
| `python3 scripts/docs_check.py` | rc 0. |
| `python3 scripts/check_doc_style.py` | rc 0. |
| `python3 scripts/gen_toc.py --check` and `--verify-anchors` | rc 0; no regeneration required. |
| `python3 scripts/check_em_dash.py --base dc4d06cb` | rc 0; 0 findings over 167 added lines, 339/339 controls. |
| `python3 scripts/check_doc_paths.py` | rc 0. |
| `git diff --check dc4d06cb` | rc 0. |

Published cleanup-entry, shutdown, lifecycle, monitor, compatibility and derivation
probes retain rc 0. Their unchanged inputs and prior receipt history remain under
`receipts/r5/`; this round's results are in `receipts/r6/probes/`.
The cleanup-entry probe passes all six cases. The lifecycle probes cover 76,800 and
120,000 transitions. The derivation probe uses 300 seeds.

Eight Round 5 fault controls are rejected by their targeted controls (all rc 1).
E06/E07 anchors were adjusted for the nested normal boundary; their defects are unchanged.
Seven additional Round 6 faults are rejected: original boundary restored, original failure
replaced by signal, only Refusal protected, missing secondary diagnostic, signal swallowed,
original exception replaced with a copy, and all closing restores removed.
The last exits 129 in the existing window control; the other six produce named failures.
These nonzero mutation statuses are expected negative evidence, not failing normal gates.

Final-head unchanged mutation campaigns retain their outcomes: R632-2 kills 36/36;
R632-3 kills 24/30, including Q24. Survivors remain Q06/Q11/Q13/Q15/Q28/Q29;
Q15 is the previously recorded equivalent control. Neither campaign has a bad anchor.
The campaign drivers exit 0; the mutant nonzero statuses are expected.
Receipts: `receipts/r6/head-mutants-r2.log` and `head-mutants-r3.log`.
Both public driver files match their published sha256. The final runs use an export of
`73b8dcd667aa5bf1254e828dd1dd7217c8a103ce`, with no subsequent source edits.

### CPU layout and disjointness

Round 6 changes no CPU arithmetic or resource limit.
With `CONCURRENT_JOB_LIMIT = 1` and default matrix width 4, each slot owns 20 CPUs:
one staging range and four job ranges, each `CONTAINER_CPU_LIMIT = 4` wide.
The replayed workflows derive the number used; unsupported concurrency or capacity refuses.
`rtl-full` derives four; each other shipping workflow derives one.

| Slot | Before: every concurrent container | After: staging | After: separate concurrent containers |
| --- | --- | --- | --- |
| 0 | `0-3` | `0-3` | `4-7`, `8-11`, `12-15`, `16-19` |
| 1 | `4-7` | `20-23` | `24-27`, `28-31`, `32-35`, `36-39` |
| 3 | `12-15` | `60-63` | `64-67`, `68-71`, `72-75`, `76-79` |
| N | `4N..4N+3` | `20N..20N+3` | Container j, numbered 1-4: `20N+4j..20N+4j+3` |

The standing proof enumerates slots 0-63 at maximum concurrency: 320 four-CPU ranges,
including staging. Every CPU has one owner. Planted old `slot*4` spacing fails across slots;
placing every concurrent container on one range fails within a slot. Planting staging on
a job range triggers the runtime refusal. Per-container memory remains 16 GB without extra
swap; isolated-slot memory remains 24G. Slot 0 has no aggregate slot cap.
Reservations survive `die` and uncertain updates until removal; inspect confirms placement.
Mixed old/new runner versions overlap, so concurrent slots must use one version.

`receipts/r6/offline-dryrun.log` records the actual dry-run planning path with inert external
boundaries for slots 0 and 3, both rc 0. Its plan lines list exactly the ranges above.
A live `--dry-run` still enters the daemon boundary, so none was run.

### Before/after replay table

The [no-replay ruling](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131815815)
remains binding. No replay ran in Round 6. The retained partial before run is not a completed
comparison and supplies no claimed speedup.

| Run | Job | Per-job wall clock | Slot memory peak | Verdict |
| --- | --- | --- | --- | --- |
| Partial before, dev `dc4d06cb`, PR #728 `2c2f3369`, slot 3 | full-ci-gate | 15 s | 15.1 GiB sampled before stop | succeeded |
| Same partial before | Verilator shards 0-3 | 20:02:57-20:10:36 UTC, interrupted | same sample | interrupted; replay rc 130 |
| Same partial before | Verilator 4, Yosys 0-3 | no completed timing | same sample | interrupted |
| After, this head | all | not run per ruling | not measured | not measured |

The original replay log exceeds the output size limit: 424948 bytes, sha256
`d6c756d0a992fd09f951d82b7c0c34b00c777db5eb743b22ae487f1a268333aa`.
It remains in scratch; only its small sampled receipt is retained in the output.
The partial sample observed four containers sharing CPUs `12-15`.

The manager owns post-merge measurement. The before records are slot-0 replays #721 at
`42678ae2` and #715 at `c7d0ad63`; the after is the first replay on merged code.
From a clean candidate, using a separate trusted runner, the deferred command is:

```sh
python3 -I <trusted-dev>/scripts/act_ci.py --pr <number> --sudo --workflow rtl-full
```

Read timestamped `[rtl-full/<job>]` setup-to-finish intervals, the CPU plan, and the verdict.
Read the CPU summary: for a complete full run, expect all 12 containers confirmed by inspect,
none removed before placement or left unconfirmed, at most four reserved ranges, and no
`WARNING ... CPU ranges:` line. Isolated slots also print `memory peak` and cap-hit count;
slot 0 requires separate memory sampling. Compare verdicts at the same PR head.
Optional `CONCURRENT_JOB_LIMIT = 2` remains deferred and requires a separate cap measurement.

### Acceptance and handoff

| Acceptance | Current evidence |
| --- | --- |
| 1 | Allocation, lifetime, uncertainty and capacity boundaries proved offline; live placement remains unmeasured. |
| 2 | Workflow-derived ranges; maximum-concurrency disjointness proof and planted overlaps. |
| 3 | No workflow, step or job changes; each mask remains four wide. Live `nproc` and same-head verdict comparison remain deferred. |
| 4 | Deferred by ruling; no measured speed claim. |
| 5 | Optional and deferred by ruling. |

The PR body uses `Relates to #730`. The Issue remains open.
Manager duties: publish the two commits and evidence, obtain independent re-review,
complete hosted acceptance and current-dev candidate validation, obtain merge authorization,
then perform deferred measurements and post-merge containment.
This executor supplies no review verdict or reviewer-owned completion ledger.

Receipt paths are normalized to neutral placeholders; `receipts/r6/MANIFEST.json` records
raw and published sizes and sha256. `source-manifest.json` records the exact head and source
blob identities. No source-tree export, environment, installed package or file over 200 KB
is placed in the output directory.
