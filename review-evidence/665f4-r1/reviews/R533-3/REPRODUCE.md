Run from the exact reviewed source checkout. Set `SOURCE` to that checkout and
`PACKET` to this packet. All generated files belong under `$PACKET/scratch`.
The four required submodules must match the recorded gitlinks.

```sh
python3 -B "$PACKET/run_srp_review.py" positive --repo "$SOURCE" --packet "$PACKET" --jobs 4
python3 -B "$PACKET/run_srp_review.py" plants --repo "$SOURCE" --packet "$PACKET" --jobs 4
python3 -B "$PACKET/run_probes.py" --repo "$SOURCE" --packet "$PACKET" --jobs 4
python3 -B "$PACKET/run_target.py" --repo "$SOURCE" --packet "$PACKET" --jobs 4
python3 -B "$PACKET/run_docs.py" --repo "$SOURCE" --packet "$PACKET"
python3 -B "$PACKET/probe_docs.py" --repo "$SOURCE" --packet "$PACKET"
```

The documentation checks require the pinned Markdown environment described by
`tools/markdown/requirements.txt`. In this execution the default interpreter
refused the em-dash check because html5lib was absent. Running that same command
with the provisioned, hash-locked Markdown interpreter passed. Both receipts
are retained in `docs/08*`; `docs.rc=1` records the initial composite refusal.
Use the pinned interpreter for `run_docs.py` to avoid that setup refusal.

Independent positive and mutation commands can run concurrently, with four
compiler workers each. Keep every command attached to its foreground caller.
Never exceed sixteen total compilation workers.

The upstream topic source is available at
`kebag-logic/lwSRP` commit `495520f5e02dd077fc9b1451942b25ec95afa1b8`.
Export it under scratch using `git archive`. Its `src` tree must equal the
parent's pinned `23d9a8173b07503a0ee6e8528f922fceab4e67f0`.
The test dependency used here was `cgreen-devs/cgreen` release 1.7.0, commit
`feeb85ed48d163f6b7b0011a6d8e6043951541e4`, built and installed only in scratch:

```sh
cmake -S "$PACKET/scratch/cgreen-src" -B "$PACKET/scratch/cgreen-build" \
  -DCMAKE_INSTALL_PREFIX="$PACKET/scratch/cgreen" \
  -DCGREEN_WITH_UNIT_TESTS=OFF -DCGREEN_WITH_CXX=OFF
make -j16 -C "$PACKET/scratch/cgreen-build" install
python3 -B "$PACKET/run_upstream.py" \
  --source "$PACKET/scratch/lwsrp-topic" \
  --prefix "$PACKET/scratch/cgreen" --packet "$PACKET" --jobs 16
python3 -B "$PACKET/verify_integrity.py" --repo "$SOURCE" \
  --output "$PACKET/integrity.json"
```

The upstream runner compiles both profiles, runs their original unit and
behavior suites, plants three independent guard reversals, checks named
failures, then rebuilds and passes the restored source. Build failures never
count as caught behavioral defects. Its full commands, logs and exit codes
are under `upstream/`. Keep the sixteen-worker build separate from other
compiler runs. Host prerequisites include the ordinary native C/C++ test
libraries, CMake, behave and the repository's pinned RV32 SDK.

Only REPORT.md and files named in MANIFEST.sha256 are publication inputs.
Scratch contains disposable dependencies, exports and binaries, and is excluded.
