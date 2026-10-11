Run from the packet directory against a detached clone at
`a70e38804cb16435c089d024c58e8c3fb4d39ff6`:

```sh
python3 scripts/run_review.py --source /path/to/clone --jobs 3 --compiler /path/to/pinned-5.050/verilator
python3 scripts/run_edges.py
python3 scripts/run_padding_control.py
python3 scripts/audit_checkout.py /path/to/clone
```

The first command exports committed files to `scratch/head`. It runs the
parser suite, documentation/contract/lint checks, and a clean control plus
the eight committed mutation definitions concurrently. It uses a foreground
coordinator that waits for every child; nothing is detached. Three mutation
workers and the parser build each use four compiler jobs, with a maximum of
sixteen. The committed mutation driver has no `--jobs` option; this runner
provides one and saves each build/run log, return code and required check
verdict separately. The source mutation definitions and verdict function are
loaded without changing them. Each make invocation uses `-j16`; the local
compiler wrapper translates an internal unlimited `-j 0` into `-j 4`.

Expected outcomes: parser 337 PASS; clean mutation control rc 0; each
defective parser rc 1 with every assigned failure name; campaign summary
rc 0; documentation/contract/lint rc 0. Mutation failure exits are expected
test outcomes, not failures of the campaign. Build failures never count as
caught defects. `receipts/local/mutations.json` records each interpretation.

The second command appends `edge_probe.cpp` to a disposable copy of the
existing harness after exposing its test helpers and renaming its entry
point. Frame builders are reused, while stimulus sequencing, expanded cases,
and comparisons are reviewer-owned. Production RTL remains exact-head.
It checks all seven supported types, both Announce layouts, padded Sync,
per-position pulsed and held flags with zero/one/three invalid cycles between
bytes, flags on those invalid cycles, clean recovery, all sixteen ordered
pairs of the four required types at every refused-frame byte position,
reset, an adjacent error runt and 16-bit counter wrap. Expected result:
36129 PASS, 0 FAIL, rc 0. This is parser-level evidence, not an engine or
hardware campaign.

The third command independently checks the padding-coverage suggestion
published during final reconciliation. It plants the padding-only defect
in a new scratch RTL copy, then concurrently builds the committed suite and
expanded probe against it. Expected outcomes: committed suite survives with
337 PASS and rc 0; expanded probe reports named refusal failures and rc 1;
the coordinator returns zero only when both expected results occur. This
does not modify source RTL or the completed independent verdict.

The fourth command independently hashes every tracked working-tree blob,
checks executable modes and all index entries against the HEAD tree, checks
any gitlinks, checks status, compares comment-free parser code with round
one, and verifies the four tracked hexadecimal images are unchanged.
This repository has no nested submodules. Expected result: PASS, 105 entries,
no gitlinks, clean status.

All build trees, mutation sources and compiler wrappers remain in `scratch/`,
which is excluded from publication. Raw runtime receipts and their `.rc`
files are published. Build logs contain environment-specific compiler paths
and remain unlisted; their exit-code receipts are published. The parser's
complete runtime stdout is extracted unchanged to `parser-runtime.log`;
the combined build/run log remains unlisted.

Public evidence provenance is recorded in REPORT.md and the downloaded
`receipts/public-r1/MANIFEST.json`. The 57 downloaded executable-evidence
files match their published hashes. The pinned bundle is round-one evidence,
not newly executed round-two full-gate evidence. The exact-head author gate
statement is saved separately. No private author handoff was read.
