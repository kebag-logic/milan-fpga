Run from the exact reviewed checkout. Let `PACKET` name this packet's directory.
All disposable output goes under `scratch/`.

```sh
export TMPDIR="$PACKET/scratch" PYTHONDONTWRITEBYTECODE=1
python3 -B "$PACKET/run_checks.py" "$PWD"
python3 -B sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --config configs/endstation_ax7101_1x1_tdm8.yaml --jobs 16
python3 -B "$PACKET/probe_map.py" "$PWD"
python3 -B "$PACKET/fetch_public.py"
python3 -B "$PACKET/probe_evidence.py" "$PWD" "$PACKET/scratch/public"
python3 -B "$PACKET/verify_checkout.py" "$PWD"
```

The five `run_checks.py` checks run concurrently and each receives a log and exit-status file. The separate compiled suite uses at most 16 jobs. The probes require no full target build. `probe_map.py` loads the exact comparison function through its syntax tree, avoiding SoC dependencies; it does not elaborate a SoC. `probe_evidence.py` rechecks published target traces, generates the report demonstrating R738-F1, and imports a disposable copy of the current writer's grader with the D5 check removed. The unchanged gate must exit 1 in that planted case; the enclosing probe exits 0 when this expected rejection occurs. The source checkout is never modified.

The immutable receipt URLs and hashes are in `public-inputs.json`. Downloaded copies are scratch inputs, not new reviewer executions. The generated table is the unmodified generator's output and intentionally lacks the clock; its required context for this probe is CPU 50 MHz, bus 100 MHz.
