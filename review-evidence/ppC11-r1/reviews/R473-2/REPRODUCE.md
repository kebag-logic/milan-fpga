The scripts derive the packet root from their own path. Start with an isolated repository at the exact reviewed head and the required compiler/diagram dependencies on PATH. All copies and builds go in scratch/.

Run in the foreground:

```sh
python3 scripts/setup.py /path/to/isolated/exact-head-clone
python3 scripts/run-focused.py
python3 scripts/provenance.py
python3 scripts/id-probes.py
python3 scripts/id-selftest-strength.py
python3 scripts/figure-probes.py
python3 scripts/artifact-checks.py
python3 scripts/integrity.py /path/to/isolated/exact-head-clone
```

The setup script creates the scratch clone and a private renderer environment. Use a fresh scratch directory for a fresh replay. The focused-build coordinator caps each simulator build at four workers; its three independent commands run concurrently and each records its own log and rc. The default simulator path is the scoped path supplied in the review assignment. Public API/package receipts are snapshots, not executable pass claims. A probe driver returns zero when observed success/failure outcomes match its assertions; expected negative gate return codes remain in its log. No probe edits the supplied original clone. Scratch is never published.
