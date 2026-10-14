# CI execution signatures

Issue #737 defines independently collected execution manifests.
Their canonical payloads must agree before claiming equivalent runs.
Equal documents alone do not authenticate their collectors.

## Contents

- **[Payload](#payload)** -- Identify the seven compared evidence sections.
- **[Excluded observations](#excluded-observations)** -- Keep timing and runner observations outside the signature.
- **[Collection and authentication](#collection-and-authentication)** -- Require independent collectors and a separate signing key.
- **[Comparison](#comparison)** -- Refuse changed or incomplete execution evidence.
- **[Implementation boundary](#implementation-boundary)** -- State the remaining collection and authentication work.

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

The current module defines the envelope and comparison boundary.
Its `emit` command packages supplied collector records.
It preserves incomplete evidence and returns failure for it.
It refuses conditional skips until their evaluation evidence is integrated.

Hosted API collection and replay telemetry integration remain required.
Source-derived plan verification and signing also remain required.
The digest-pinned image and measured tool lock remain required.
The comparator alone establishes no authenticated build verdict.
Existing hosted checks and local gates remain mandatory.
