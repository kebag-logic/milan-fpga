This packet reviews published head `d8060d87f892239ac4e598d0a8556cbfcd4a52ec` against round 6, `13e715136b0b7c8d9763e0b730d9709f2c9f5932`.

Use an isolated detached checkout with its three required submodules initialized at their gitlinks. Pass its absolute path as `<checkout>` below. Keep this packet outside the checkout; the scripts locate their packet directory from their own location. The host needs the repository's normal C/C++, unit-test, coverage, Python and configuration dependencies. No shared installation is performed.

Run these commands in the foreground:

```sh
python3 -B verify_tree.py <checkout>
python3 -B run_checks.py <checkout> --phase sdk --archive <pinned-sdk-archive>
python3 -B run_checks.py <checkout>
python3 -B audit_results.py <checkout>
python3 -B verify_campaign.py <checkout>
python3 -B verify_tree.py <checkout>
```

Without `--archive`, the SDK phase downloads the pinned archive. The repository installer verifies its SHA-256 and installs only under this packet's `scratch/sdk`. All build trees, fault copies, generated headers and temporary directories are under `scratch/`.

`run_checks.py` waits for all children in one foreground invocation. It runs the complete ctrl suite, firmware coverage, four focused probes, two-shape image comparison and three complete/disjoint campaign slices concurrently. The default aggregate compilation allowance is 16 jobs. `--phase campaign` runs only the three slices, with five jobs each. Each task retains its complete log, return code and command receipt.

The original execution ran the independent suite, coverage, probes and images concurrently with an interleaved campaign attempt. That attempt was stopped because `--mutation-shard` truncates the catalog before the complete test-to-defect mapping audit. Its `interleaved-attempt-*` files are retained as superseded evidence, including the deliberately killed return codes. The accepted campaign uses the repository's documented `--slice K/3` interface; it retains the complete catalog for the audit. No repository code or test was changed to make either invocation pass.

Additional focused commands, run from the exact-head checkout with `TMPDIR` pointing to this packet's `scratch/tmp`:

```sh
python3 -B sw/firmware/gtest/fw_coverage.py --selftest
python3 -B scripts/docs_check.py
git diff --check 13e715136b0b7c8d9763e0b730d9709f2c9f5932 d8060d87f892239ac4e598d0a8556cbfcd4a52ec
```

`focused_probes.py` runs both entire ACMP arms for each defect. A required kill must have exit status 1 and exactly one failure line, naming the required test and assertion. The unaffected one-interface controls must return 0. Its summary and each complete arm log are retained separately.

`verify_campaign.py` compares every earlier review fixture with round 6, counts the current catalog, rejects unnamed tests, and matches the executed mutant names to each expected slice. It refuses an escape, a failed process, a missing mutant or an overlapping partition.

`verify_tree.py` hashes every tracked blob directly, checks executable and symlink modes, compares the full stage-zero index against the commit tree, and repeats those checks for the three required registered submodules with replacement objects disabled. It does not depend on status alone.

Only files listed in `MANIFEST.sha256` and `REPORT.md` are publishable. `scratch/` is excluded. Verify the packet from its root with `sha256sum -c MANIFEST.sha256`.
