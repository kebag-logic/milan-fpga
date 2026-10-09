# Reproduce the focused review

Use a fresh output directory. Set SOURCE to a clone at the reviewed head,
PACKET to this published packet, OUT to disposable output, and SIMULATOR
to the verified 5.050 launcher. Commands are foreground commands.

```sh
mkdir -p "$OUT/scratch" "$OUT/receipts"
python3 "$PACKET/scripts/source_integrity.py" "$SOURCE" "$OUT/receipts/integrity.json"
python3 "$PACKET/scripts/verify_public.py" "$SOURCE" "$OUT"
python3 "$PACKET/scripts/run_defaults.py" "$SOURCE" "$OUT" "$SIMULATOR"
python3 "$PACKET/scripts/fresh_traces.py" "$SOURCE" "$OUT" "$OUT/scratch/serial/tb/verilator/follow_ring/obj_dir/Vfollow_ring"
python3 "$PACKET/scripts/schedule_probe.py" "$SOURCE" "$OUT"
python3 "$PACKET/scripts/boundary_probes.py" "$SOURCE" "$OUT"
python3 "$PACKET/receipts/public-probe-inputs/R475-7/scripts/decimal_boundaries.py" "$SOURCE" "$OUT"
python3 -B "$SOURCE/tb/verilator/follow_ring/test_trace_table.py"
```

The source clone needs the four required submodules initialized at their
existing gitlinks. Public verification requires the two evidence archive
commits identified in the script, obtainable from `645-review-evidence`.
The defaults driver runs two independent cold invocations concurrently and
joins both. It selects two disjoint four-CPU sets from allowed affinity.
Its simulator wrapper caps every compilation at two workers; inner campaigns
use two jobs. The graph probe replaces workers only in a disposable tree;
its graph is the unchanged reviewed Makefile. It verifies orchestration,
while the cold defaults separately execute actual production checks.

Fresh traces run concurrently after compilation. Full traces remain under
scratch; published CSVs are bounded windows with whole-file raw hashes.
The earlier-reader receipt is an expected negative result, not a failing
current-head test. Public path placeholders preserve measurement values.
