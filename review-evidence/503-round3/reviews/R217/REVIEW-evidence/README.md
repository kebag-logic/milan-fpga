R217 round-three local review artifacts for PR #503, page head
`ab0fb23fd1a6376213a9d0e5aa61f4751ece00e4`.
These files accompany `REVIEW.md`; they have not been published or committed.

`probe_preload.py` imports the public runner at evidence commit
`fc2e3a6211bdbca3c41718eb6e1b4b4c2a128293`, copies its harness to private scratch,
and changes only that copy. It connects the amended binding manager to the
unchanged pinned `KL_pp_acmp_listener`, using the pinned ACMP NVM suite's
existing droppable-event backpressure lever. It also exercises descriptor
responses around the subordinate timeout and rollback deadline. It leaves
the writer, arbiter, amended binding/port prototypes, descriptor store and
firmware unchanged. The stimulus is an interface-level scheduling probe,
not a claim to have reproduced a particular network packet attack.

Use an independently fetched disposable evidence checkout, initialize the
three required submodules, and set these environment variables before running:

```sh
export EVIDENCE_ROOT=<disposable-evidence-checkout>
export REVIEW_ARTIFACTS=<directory-containing-this-file>
export REVIEW_SCRATCH=<private-scratch-directory-under-/data>
export TMPDIR="$REVIEW_SCRATCH/tmp"
export D3_OUT="$REVIEW_SCRATCH/d3"
export OOC_OUT="$REVIEW_SCRATCH/ooc"
mkdir -p "$TMPDIR" "$D3_OUT" "$OOC_OUT"
cd "$EVIDENCE_ROOT/design-evidence/500-materialization/proposal-evidence"
mapfile -t builds < "$REVIEW_ARTIFACTS/selected-builds.txt"
taskset -c 64-79 python3 -B run.py prep
taskset -c 64-79 python3 -B run.py build "${builds[@]}" --pool 1 --jobs 8
taskset -c 64-79 python3 -B run.py run "${builds[@]}" --pool 8
taskset -c 64-79 python3 -B run.py controls --pool 8
export D3_OUT="$REVIEW_SCRATCH/adjacent"
taskset -c 64-79 python3 -B "$REVIEW_ARTIFACTS/probe_preload.py"
python3 -B "$REVIEW_ARTIFACTS/assert_review_observations.py" "$REVIEW_SCRATCH/adjacent-probes.json"
```

The selected immutable run produced **29 builds, 243 runs, 2,420 checks and
zero verdict failures**. This is FOCUSED evidence, not the published full
69-build campaign. `results-focused.json` and `.txt` retain its check and
mutant verdict details; `selected-builds.txt` records every build selected.

The added probe produced ten completed scenarios in one additional build.
`adjacent-probes.json` contains their observations and events;
`adjacent-summary.json` is a compact extraction. The observation checker
explicitly checks both the counterexample and the adjacent successful safety
controls. Its successful exit means the stated observations were reproduced;
it does **not** mean the proposed contract passed. The held-preload case has
no restore terminal or GET answer. The finite case finishes only after its
chosen release time. The seed slots come from the synthetic ordering case
V1a, as in the immutable failure campaign; output-format product legality is
tested separately by V1s_a/V1s_b/V1s_c in the focused run.

`gates.json` records the 18 sequential docs/interface gate invocations and
exit codes. `input-verification.json` records the 59 immutable digest checks,
the candidate-input comparison and the four integrated documentation blob
comparisons. `tracked-byte-verification.json` records direct Git blob checks
of both checkouts and their initialized submodules. No product sources were
edited. `SHA256SUMS` identifies this accompanying artifact set.
