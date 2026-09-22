# R220-2 receipts: PR #505 / issue #407 at ad62493186576144f9fa1568babad012bc9ad8ca

`REPORT.md` is the review. This directory holds its factual receipts.

## Layout

- `logs/00-entry-state.log`, `logs/99-final-integrity.log`: clone state at entry and exit.
- `logs/01-remote-refs.log`: live `dev`, PR branch and `refs/pull/505/head` (read-only `git ls-remote`).
- `logs/02-check-head.log`, `logs/03-selftest-head.log`: the real CLI at the head, run in the review clone.
- `logs/gates/`: documentation and diff gates run in the review clone; the four code-quality scans show their exit-2 refusal (submodules not initialized).
- `logs/p*.json|log`: probe outputs; `logs/p3-cli/` holds every mutant's complete `--check` and `--selftest` output at both heads.
- `probes/`: the probe sources (`common.py` shared loader).
- `receipts/`: public-state snapshots (issue #407, PR #505 thread, hosted check runs at the head, scratch commit 66ba2106 via the commits API, evidence tree listing at b7380181), the base-to-head and round-1-to-head diffs, and `public-evidence/` (AC5 and round-2 manager/builder receipts downloaded from evidence commit b7380181, each checked against its git blob id).

## Reproduce

The probes read git objects from a clone that contains
b17580b91deb11f3441dfc5d7f9fafe539d929b8, 6af65a151663e1301f1983a6c9d22650a0b35da9 and
ad62493186576144f9fa1568babad012bc9ad8ca. They never write to that clone: modules are
imported from temporary copies, and CLI runs use `git archive` scratch roots under the
system temporary directory with `--root`.

```sh
export R220_CLONE=/path/to/clone      # default: the review clone named in probes/common.py
cd probes
python3 -B p1_census.py ../logs/p1-census.json                    # 56 bodies, 173 lines, records equal
python3 -B p2_arms.py ../logs/p2-arms.json                        # arm populations base / r1 / head
python3 -B p3_cli_mutants.py ../logs/p3-cli-mutants.json          # comparator mutants via the real CLI (~4 min)
python3 -B p4_masking.py ../logs/p4-masking.json                  # specialized arms stay reason-pinned
python3 -B p5_maintenance_ac5.py ../logs/p5-maintenance-ac5.json  # maintenance, whitespace, AC5 analogue
python3 -B p6_scope_equality.py ../logs/p6-scope-equality.json    # AST and constant equality, blob ids
python3 -B p7_residue_claim.py ../logs/p7-residue-claim.json      # F3: gate pin step edits, real CLI
python3 -B p8_robustness.py ../logs/p8-robustness.json            # malformed bodies and records
python3 -B p10_records_structure.py ../logs/p10-records-structure.json
python3 -B p11_sibling_residue.py ../logs/p11-sibling-residue.json  # F3: every sibling run step
python3 -B p12_ac5_finding_equality.py ../logs/p12-ac5-finding-equality.json
```

`logs/p9-selftest-on-malformed-pristine.log` records the one-off CLI command for the
SUGGESTION (idiom body replaced by `run: " "` in a scratch root).

Requirements: Python 3 with PyYAML (3.14.7 and PyYAML 6.0.3 here) and git. No network is
needed except for the `receipts/` snapshots, which were read with `gh api` (read-only).
Some logs and `probes/common.py` contain local absolute paths of the review host
(the clone, the receipts directory, temporary scratch roots); they carry no result.
