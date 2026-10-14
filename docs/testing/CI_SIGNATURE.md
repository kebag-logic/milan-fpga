# CI execution signatures

Issue #737 defines independently collected execution manifests.
Their canonical payloads must agree before claiming equivalent runs.
Equal documents alone do not authenticate their collectors.

## Contents

- **[Payload](#payload)** -- Identify the seven compared evidence sections.
- **[Excluded observations](#excluded-observations)** -- Keep timing and runner observations outside the signature.
- **[Collection and authentication](#collection-and-authentication)** -- Require independent collectors and a separate signing key.
- **[Source plan](#source-plan)** -- Recompute the expected jobs and steps from committed workflow bytes.
- **[Comparison](#comparison)** -- Refuse changed or incomplete execution evidence.
- **[Implementation boundary](#implementation-boundary)** -- State the collected evidence and remaining authentication work.

## Payload

JSON uses UTF-8, sorted keys, and integer numeric values.
Duplicate keys and non-finite values are refused.
SHA-256 identifies the canonical payload bytes.

| Section | Bound evidence |
|---|---|
| `subject` | Repository, head, tree, event, and PR ancestry |
| `definitions` | Every workflow file's SHA-256 |
| `environment` | Image digest, measured tool provenance, and action commits |
| `plan` | Resolved jobs, matrix coordinates, dependencies, conditions, and steps |
| `execution` | Each planned step's actual outcome and skip explanation |
| `inventories` | Suite inventory, actual leg membership, union, and verdict digest |
| `results` | Every job and leg's outcome |

Each step binds its name, kind, condition, and command digest.
Action steps hash their complete action reference.
Shell steps hash their complete `run` text.
Array ordering remains significant during comparison.
Tool records include version, source, recipe, and binary digests.

## Excluded observations

The outer envelope also holds operational observations.
Their allowed fields are deliberately enumerated:

- `wall_clock`
- `runner`
- `cpu_count`
- `logs`
- `cache`

These observations never change the payload signature.
They cannot replace a required execution or inventory record.

## Collection and authentication

Hosted collection reads job and step outcomes through GitHub's API.
Leg artifacts provide case receipts and measured environment provenance.
Local collection reads the replay's actual execution telemetry.
Neither collector may manufacture success from the static plan.
Both must recompute that plan from the bound source tree.
Both must verify inventories against their owning drivers.

The coordinating role supplies the signing key separately.
The private key never enters a job container.
Only the corresponding public key belongs in the repository.
Signature verification authenticates the local collector's payload digest.
The source, plan, environment, outcomes, and unions remain independently checked.

## Source plan

The planner reads workflow blobs from the specified commit.
Working-tree edits cannot redefine those inputs.
It expands literal matrix axes and every dependency leg.
It binds each step's complete command or action reference and condition.
Duplicate keys, aliases, dynamic matrices, ambiguous names, and cycles fail closed.

```sh
python3 scripts/ci_workflow_plan.py --head <full-commit>
python3 scripts/ci_workflow_plan.py --manifest collected.json
python3 scripts/ci_workflow_plan_selftest.py
```

The manifest check verifies its tree, definitions, and plan against Git objects.
It is a source-binding check, not an execution or authentication verdict.
Both collectors must call the same verification before comparison.
Controls remove a definition or job, replace the tree, and alter commands.
Each changed collection is refused against its original committed inputs.

## Comparison

The transport-independent comparison command is:

```sh
python3 scripts/ci_manifest.py compare local.json github.json
```

It names differing sections and fields.
It refuses missing steps, extra legs, and changed environments.
It refuses omitted cases, duplicate cases, and changed verdict digests.
It refuses unsuccessful or cancelled collections, including identical ones.
It recomputes payload digests and recorded completeness.
An outer `complete` flag cannot override failed evidence.

Controls exercise the production comparator:

```sh
python3 scripts/ci_manifest_selftest.py
```

## Implementation boundary

The source plan, both collectors, and comparison controls are implemented.
`scripts/ci_runtime_evidence.py` records actual per-job step contexts and tool
versions, then reads hosted job and step outcomes through the API. The final
job of each workflow uploads its manifest. The collector accepts repeated
`--run` arguments for a completed readback of all four workflows. Missing
results remain unknown; the final job cannot claim its own future success.

The trusted local runner collects structured scheduler start, step and job
observations. It retains the first failure and distinguishes admitted jobs
cancelled by that failure from jobs never admitted. It stops the execution
process group and cleans its owned containers and volumes before collection.
`--evidence-directory` selects a fresh durable directory outside the candidate;
without it the runner creates one and prints its path. It saves
`act-execution.jsonl` and `ci-manifest.json` there.

The host reader is a separate isolated process. The trusted runner pins
`ci_local_manifest.py`, `ci_manifest.py`, and `ci_workflow_plan.py` by digest,
copies their verified bytes into a private directory and rechecks them there.
Candidate workflow blobs and bounded JSON artifact members are data only.
The audited flat-install bootstrap must install these pinned helpers beside
the runner. Their identities are generated by
`scripts/generate_ci_evidence_pins.py`; changed helper bytes require regenerated
pins and a newly audited runner checksum. Controls reject changed helpers,
symlinks, candidate import paths and reused or in-tree output directories.

Round one emits deliberately incomplete manifests where proof is unavailable.
The image and layer lock, immutable action pins, signing key and conditional-skip
evaluation proof remain round-two work. Tool versions and executable hashes
are measured; missing source or recipe provenance stays null. A hosted PR
checkout can name the synthetic merge while local replay names the PR head;
that difference is recorded and refused, never normalized away. A final API
readback is also necessary to conclude collection jobs themselves.

The comparator independently recomputes each manifest's plan from its source
commit, then checks the seven canonical sections. Identical incomplete or
cancelled records are refused. These base collectors establish no authenticated
build verdict until the remaining proofs exist. Existing hosted checks and
local gates remain mandatory.
