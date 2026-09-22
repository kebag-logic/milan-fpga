# R241 design evidence reproduction

Run these from this artifact directory. Every shell command uses RTK. The scripts read the unchanged checker from `$VALIDATION_STORAGE/reviews/r241-423-design/scripts/check_merge_containment.py`, trusted head `88e9276b2a220c716f64a843f7e1eb8f9265e896`. If reproducing elsewhere, adjust that explicit path in the scratch scripts to an isolated checkout of exactly that public commit. Never edit the trusted checkout to run these probes.

Offline, with the preserved public Git clone and fixture data:

```sh
rtk proxy python3 -B scripts/verify_public.py
rtk proxy python3 -B scripts/fixtures.py
rtk proxy python3 -B scripts/inspect_donor.py
```

The fixture runner creates only Git objects and refs in `fixtures/counterexamples.git`, with fixed author/committer identity/date and no working checkout. Repeated runs reproduce its object IDs. It runs child processes sequentially. Expected final exit is 0, with 25 cases and 75 recorded predicate exits. Individual logs include argv, exit, stdout and stderr. The historical mode is an intentional unsafe comparison, never a containment approval.

Unchanged checker self-test, from the trusted checkout (it needs a Git repository with a commit):

```sh
rtk proxy python3 -B scripts/check_merge_containment.py --selftest
```

Expected exit 0. Saved original run: `logs/trusted-selftest.log`. The initial attempt from an uninitialized scratch directory refused with exit 2 before tests; the valid run above completed. No long gates are part of this design review.

The original public minimal fixture can be rerun from scratch:

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/fixtures" python3 -B public/readiness-evidence/423/probe/probe_ff_merge.py $VALIDATION_STORAGE/reviews/r241-423-design/scripts/check_merge_containment.py
```

Expected exit 0 and both reported unchanged-checker predicates false; the historical helper reports true for both extension and revert. Its object IDs vary with execution time; the R241 fixtures above are deterministic. `prepare.py` verifies the prior manifest, runs the unchanged self-test/public fixture, and clones public donor history if absent. `fetch_public.py` fetches issue/public evidence; it excludes later R242 report-bearing comments before display/storage and is not needed for offline reproduction. No new issue-comment refresh was performed after the initial filtered snapshot.

`logs/donor-evidence.json` records fixed tested donor OIDs, replay pairs, topology and all six donor process exits. `inspect_donor.py` uses the preserved clone's recorded main ref; it does not refresh it. `logs/issue-patch-hashes-verified.json` reproduces the two exact issue hashes. The separate full-index patch rendering naturally has different hashes, while each original/replay pair is byte-identical.

`logs/fixture-initial-results.json` preserves the first run: two guessed baseline expectations were wrong because the existing path arm accepts exact current endpoints independent of topology. The later matrix corrects only those baseline expectations and adds differing-endpoint cases. The prototype's negative expectations were not weakened. See `logs/fixture-expectation-correction.txt`.

`integrity.py` records trusted HEAD, index bytes/stage entries, clean status, and tracked/untracked enumerated entries' kind/mode/SHA-256. Initial/final JSON files match exactly. They are records of this run; do not overwrite them when reproducing elsewhere. All local absolute paths are publication-neutralization candidates. These artifacts contain evidence and executable probes, not private reasoning.
