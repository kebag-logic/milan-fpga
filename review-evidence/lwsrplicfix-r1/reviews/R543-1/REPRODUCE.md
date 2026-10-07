# R543-1 reproduction

Use an isolated checkout at head `f800a2bb920c543934d6286a47fe20dde3efa2c5`, with parent `a4cbe41de1c80d43f26e0d348cbdb45075273a4f` available. Supply absolute paths in REPO and PACKET. Keep disposable content under PACKET/scratch. The scripts require Python 3, a C compiler, CMake, make, the scenario runner, the read-only GitHub CLI, and network access for public downloads. They perform no GitHub writes.

The supplied canonical bytes and exact-head license API receipt support offline replay of the audit:

```sh
python3 "$PACKET/scripts/audit.py" "$REPO" "$PACKET"
python3 "$PACKET/scripts/bootstrap_dependency.py" "$PACKET"
python3 "$PACKET/scripts/run_checks.py" docs "$REPO" "$PACKET"
python3 "$PACKET/scripts/run_checks.py" build "$REPO" "$PACKET" \
  --prefix "$PACKET/scratch/cgreen-prefix"
```

Run independent documentation and dependency preparation commands concurrently through separate foreground command sessions if supported. Build profiles compile sequentially with make -j16, limiting aggregate compiler jobs to 16. Every command returns normally; no detached job or notification is needed. Each checker/build stage writes its own log and rc. No full parent bank is invoked. The dependency is installed only inside scratch.

For fresh public snapshots, use a new packet rather than overwriting published receipts:

```sh
python3 "$PACKET/scripts/capture_public.py" source "$PACKET"
```

Only after recording an independent verdict and ledger at receipts/independent-verdict.md, reconcile public findings:

```sh
python3 "$PACKET/scripts/capture_public.py" reconcile "$PACKET"
```

The source phase pins evidence to public commit `f15a271b1211a566ff3b163b5a8195280e8bac9e` and validates both author-artifact hashes. Live issue/PR metadata can change; capture times identify the observed state. No private author material or another local checkout is used.

Run the audit again after execution. It verifies all raw tracked blob bytes, modes, index entries, the complete header inventory, and any submodule gitlinks. At this head there are zero gitlinks. The audit also creates three disposable canonical-text negative controls in scratch.

Check publication integrity from the packet root:

```sh
sha256sum --check MANIFEST.sha256
```

Only manifest-listed files and REPORT.md are publishable. Scratch contains dependencies, binaries, probes, and original local-path logs, and is never published.
