# A182 source handoff for parent issue 523

Source is clean, committed and unpublished. This is implementation/evidence handoff, not review approval. Stop source: `b5ce20eca8b59709ec5bc6115e5e15bfc312f283`.

| Identity | Value |
|---|---|
| Branch | `523-isolate-mutation-cancellation` |
| Head | `b5ce20eca8b59709ec5bc6115e5e15bfc312f283` |
| Tree | `bfde1313250ae84105754af4b150325f55f5ef33` |
| Exact dev base | `483a133ed08867ea0d300d2b4a027b5b48a4282f` |
| Executor | A182 |
| Reserved independent reviewers | internal R256 Codex; external R257 Opus |

`unpublished-source.json` records the four one-line local commits and confirms the remote branch still names the exact base.

## Implemented behavior

The shadow mutation driver verifies the copied population against HEAD, the index and actual bytes/modes, then builds in fresh private regular files. First-party inputs are `hdl`, `tb/common` and the shadow suite. Required pinned dependencies are the gPTP `hdl` subtree and axis `rtl` subtree. Caller input files are never restored or written. Dirty/staged/index-hidden, unknown, linked, off-pin and Git-identity override controls refuse before make. `GIT_PAGER` is presentation-only and is positively controlled.

The sweep retains its selector, lock, suite deadlines, ordinary-red continuation, masked-verdict rejection and timeout UNKNOWN semantics. An owner latches INT/TERM, stops the root, terminates owned descendants through pidfds, escalates stubborn leaves, reaps adopted children and resumes terminal shell cleanup. A cancellation returns 130/143 with no later suite or completed summary. Prerequisite output is retained, old logs are removed only after locking, and relative outdirs keep their caller location. Cleanup attempts are bounded; failures cannot earn success.

The normal shadow Makefile owns `python3 test_mutant_lifecycle.py` and the full original mutant campaign. Normal sweep preflight owns `python3 scripts/test_suite_cancellation.py`. Executable forced-red ownership controls prove both calls propagate failure.

Only exact process-inventory declarations received file/context masks in the bare-metal gate, with 12 added positive/refusal controls and no broad mask or budget change. The evidence gate gained one exact-file source-reader disposition for lifecycle/input-identity inspection. No discovery or ratchet changed.

## Completed author evidence

- Complete real shadow make: exit 0, exact Verilator 5.050, eight build jobs, 309/309 baseline checks, all nine original mutations detected, six original reasons retained.
- All 24 focused bank commands passed on this head. Detailed command/status rows are in `VALIDATION.md` and `receipts/final-*`.
- Standalone lifecycle controls cover normal/repeat, every synthetic named defect, surviving mutants, compilation failure, dirty/index/path/pin refusals, INT/TERM/KILL, unsafe in-place controls and actual nested sweep/mutation cancellation.
- Sweep controls cover normal/ordinary-red/masked/timeout, selection/preflight/command/transition INT/TERM, next-suite sentinels, attributable partial logs, normal orphan cleanup, foreign sibling preservation and original unsafe continuation.
- Separate actual-process budget probes completed in about 2.17 seconds after handshake signals. Recorded child start identities became absent, not zombies; no next suite and no completed summary occurred.
- Full tracked-source snapshots before and after the real run are identical, including three complete pins. `populations.json` records nine mutations, six reasons, 55 default suites, one physical suite, exact shard partition and unchanged source harness/tally bytes.

The real campaign preserves existing fallback reporting: observer_latency_off_by_one and crossing_latency_off_by_one fail `every measured result reconstructs its own launch`; credit_never_withheld reports its existing aged-head failures. Six controls match their stored named expectation literally; all nine are detected under the unchanged campaign rule. No named expectation or fallback policy was altered.

## Acceptance and remaining bar

| Acceptance | Author evidence / remaining owner |
|---|---|
| 1: deterministic original-defect fixture | Met by production-driver handshake tests and unsafe negative controls; original public raw evidence retained. |
| 2: input isolation and lifecycle | Met by normal/failure/refusal/INT/TERM/KILL controls and exact tracked/pin integrity receipts. Hard KILL may leave private scratch/children; it cannot change caller source or produce a completed driver verdict. |
| 3: terminal sweep cancellation | Met across selection, preflight, active command and transitions, including stubborn detached descendants, next-suite sentinel, partial logs and reaped identities. |
| 4: original controls and full acceptance | All nine real detections and author-focused gates pass. Full manager banks, independent review and merge/containment remain pending. |

Manager owns all full parent/processor/Yosys/builder banks, trusted serial act, hosted required contexts, source/PR publication, final current-dev composition, candidate validation, reviewer completion ledger and post-merge containment. None was run or claimed here. No Docker/act/candidate orchestrator/selftest, privilege operation, hardware action, shared install, source push, PR or merge was performed.

Public PR524 was inspected only for changed-file collision information. Its ordinary pool files were neither edited nor consumed. The common bare-metal policy file has independent additive entries; manager composition must preserve both sets and re-run affected gates. Product RTL/firmware and all three pins are unchanged.

The published readiness evidence's SHA256SUMS mismatches six public JSON/script/stdout files. All 22 downloaded bundle objects match exact public Git blob IDs. The original checksum failure, fresh transport verification and a public issue note are retained; no original evidence was rewritten. This is an evidence-provenance caveat for the manager, not a passing checksum claim.

Public REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/523#issuecomment-5783934682

## Artifacts and reproduction

- `VALIDATION.md`: exact command/status table and real tool environment.
- `receipts/`: original command logs, environment/exit receipts and fixture records.
- `final-before.json`, `final-after.json`: complete tracked bytes/kinds/modes/index/flags and all pin files.
- `tool-identity.json`, `populations.json`, `unpublished-source.json`: identities and population preservation.
- `original-public/`, `failed-probes/`: original public evidence and failed author probes, retained without replacing failures.
- `run_receipt.py`, `focused_gates.py`, `integrity.py`, `populations.py`, `probe_log_edges.py`, `process_budget_receipt.py`, `verify_public_evidence.py`: reproducible collection/probes.
- `PR-BODY.md`: factual proposed PR text for manager publication.
- `SHA256SUMS`: this handoff directory's file checksums, separate from the original published manifest.
