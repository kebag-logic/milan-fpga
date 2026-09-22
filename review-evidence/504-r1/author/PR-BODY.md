[A160]

## Status

Local implementation prepared; real-SDK validation is blocked by archive
download timeouts. No author Bootlin-backed or fresh-installation pass is claimed.
504-hosted-rv32-compiler -> dev. Local head `3d90958f3a82ca2a9617112c107a22f332117e17`. Source remains unpublished by the author.
Full native, trusted act, hosted and candidate acceptance remain pending.

## Linked Issue / roles

Closes #504
Relates to #408 and #409

Executor: [A160]
Internal cleared-context reviewer: [R227]
External reviewer: [R228]

## Description

Both direct builder jobs now install and verify the selected checksum-pinned
Bootlin RV32 glibc SDK at the existing selector location. Cache identity binds
the full archive digest, runner OS/architecture and installer contract/source.
Receipts reject stale provenance, incomplete installations and changed files.
Exact SDK metadata masks are confined to the installer and its fixture, with
wrong-file, appended-term and protected-document refusal controls.
Both builder calls require adoption through the settled absolute selector; docs also exercises the
explicitly weaker compiler-absent gate with every retained text refusal.

## Authoritative references

REQ-VER-03/04; issue #504 decision comment5771915061; assignment
comment5778746031; docs/testing/CI_WORKFLOWS.md; docs/integration/BAREMETAL_FIRMWARE.md.

## How to get into the same state

After manager publication, check out this PR head and initialize the three
public source dependencies as CONTRIBUTING.md specifies. The focused gate
needs the normal builder dependencies, make and Verilator for RTL controls.
The SDK command below downloads only the selected official archive.

## How to validate

```sh
rtk proxy bash <<'SH'
set -euo pipefail
sdk_trial=$(mktemp -d)
python3 scripts/ci_rv32_sdk_selftest.py
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 sw/builder/test_firmware_compiler.py --selftest
python3 scripts/ci_rv32_sdk.py --destination "$sdk_trial/host"
python3 scripts/ci_rv32_sdk.py --destination "$sdk_trial/host"
python3 sw/builder/test_firmware_compiler.py --sdk-destination "$sdk_trial/host" --audit "$sdk_trial/compiler.jsonl"
python3 sw/builder/test_firmware_compiler.py --absent --audit "$sdk_trial/absent.jsonl"
SH
```

Each normal command must pass. The absent run must explicitly report NOT RUN
for the compiler instruments while keeping all text refusals active. Adding
--require-rv32 to that absent command must fail for the named requirement.
The mapped-prefix run is local compatibility evidence; the hosted builder
uses its normal absolute selector without mapping. Full local and remote
acceptance follows CONTRIBUTING.md and the trusted act contract.

## Measured author evidence

At final head: 16 synthetic installer tests; 365 bare-metal scope arms and
zero checkout findings; 57 em-dash controls and zero added-prose findings.
At preceding `ab2671c0f12cdd68df8a9260f98960b92f533efc`, with unchanged builder,
harness, workflow and workflow-contract blobs: absent gate 182 hostile refusals,
17 firmware positives, four Makefile positives, 46 RTL variants, one explicit
NOT RUN and zero firmware compiler invocations; workflow 1555 items/1198 arms.
Exact command/exit/head/tree receipts are in the author management handoff.
These results do not establish a fresh real SDK installation or compiled gate.

## Known limitations / out of scope

No text-rule retirement, extra C-library residual, product build setting,
firmware, RTL or processor pin change. Cache receipts detect drift within
GitHub's cache trust boundary; they are not independent signatures.
The author does not claim fresh hosted/act acceptance from a local SDK trial.

## Definition of Done

- [ ] All issue acceptance criteria and full required gates pass
- [x] Focused behavior and workflow controls are included
- [ ] Reproducible exact-head evidence is posted to the PR
- [ ] R227 and R228 independently accept the required review lenses
- [ ] Candidate validation and authorized merge complete
- [ ] Post-merge containment completes before Done
