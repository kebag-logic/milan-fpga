Portable replay uses an exact-head processor checkout and this packet. All downloaded or generated source inputs remain under `scratch/`. The commands run in the foreground; no synthesis, simulation bank, shared install or external write is needed.

```sh
python3 scripts/fetch_measurement.py
python3 scripts/recover_public_inputs.py
python3 scripts/audit_measurement.py --repo "$PROCESSOR"
python3 scripts/recompute_inputs.py --measurement receipts/public-measurement/measurement-m3final/ooc-m3final --record receipts/public-measurement/measurement-m3final/record-m3final.stdout --map scratch/input-map.json
python3 scripts/audit_source_scope.py --repo "$PROCESSOR" --output receipts/source-scope-audit.json
python3 scripts/verify_checkout.py --repo "$PROCESSOR" --output receipts/checkout-integrity.json
```

`audit_measurement.py` and `recompute_inputs.py` currently return 2 for the documented missing input bytes. Do not use an `&&` chain if the later audits should still run. A complete digest replay accepts a JSON map of recipe references to local files/directories and, where generated files still carry original roots, the three source-root strings in the gate's documented order. No original home path needs publication: a generated source can instead be published after the gate's own comment/root normalization. The digest script returns 0 for a complete match, 1 for a complete mismatch, and 2 for absent inputs. The record's digest is never substituted for missing components.

The source and integrity audits are static checks. The round-2 functional suites and fault executions are carried forward at the identical commit, not repeated by these scripts.
