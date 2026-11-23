Run from the exact review checkout. All commands run in the foreground.
`PACKET` denotes this packet directory; disposable outputs stay in its `scratch/`.

```sh
git fetch --no-recurse-submodules origin 7bd1b85460690e53a860c53d92c44816667e8be2
mkdir -p "$PACKET/scratch"
git archive 7bd1b85460690e53a860c53d92c44816667e8be2 review-evidence/963-r1/author review-evidence/963-r1/author-r2 review-evidence/963-r1/MANIFEST.json | tar -x -C "$PACKET/scratch"
python3 -B "$PACKET/audit.py" "$PWD" "$PACKET"
python3 -B "$PACKET/probe.py" "$PWD" "$PACKET"
python3 -B "$PACKET/integrity.py" "$PWD"
```

The probe uses the repository's host test build API with 16 compile jobs. It checks the normal two mapping tests,
plants the new order mutation, substitutes the previous test blob against that same mutation, then raises only
the disposable tally-reporting floors to expose the generated counts. Expected child statuses: 0, 1, 0, 1;
the probe driver must exit 0. Neither a mutation's expected failure nor the tally probe's expected failure is a
production regression. Source tests and production copies are restored in a finally block.

An initial probe attempt changed the disposable test but left the build API's test-directory global pointing
at the original checkout. It therefore ran the head test twice and failed the old-test escape assertion.
That setup result is not evidence about the old test. The corrected script explicitly redirects the test source,
and the final receipts are from that corrected run. The original checkout was never edited.

The initial evidence fetch retrieved the requested commit but returned 1 because automatic recursive fetches
requested unavailable unrelated submodule objects. The requested evidence object was present and extracted
successfully. Required submodule checkouts remained at their pins; integrity.json verifies their bytes and indexes.
Use the nonrecursive fetch above to avoid that incidental failure.

Public author evidence is hash-verified against the manifest, not cryptographically signed: the evidence commit
has no signature header and the selected packet supplies no detached signature. The audit does not call this a
signature verification. Round-1 oversized logs are excerpts; their original-log hash headers match the new tally.
Current complete partition logs are recounted against the live mutation table, one name per partition.

Public test logs replace only checkout/packet path prefixes with role placeholders. No assertion, result or count
is removed. Scratch builds, extracted packets and failed setup artifacts are excluded from publication.
