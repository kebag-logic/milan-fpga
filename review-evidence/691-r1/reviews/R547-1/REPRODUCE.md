# R547-1 focused review reproduction

Use a disposable packet directory and the exact source checkout.
`REPO` names head `35fb2a95007ce6dd1ec4f51c2dcb793800623cfd`.
Initialize the three required submodules at their gitlinks.
`PACKET` names the directory containing these scripts.
`SIMULATOR` names the verified 5.050 executable.
The recorded executable SHA-256 is in `environment.json`.

Run from the source checkout, with each command awaited:

```sh
python3 "$PACKET/fetch_public.py"
python3 "$PACKET/bootstrap.py" "$REPO"
"$PACKET/scratch/venv/bin/python" "$PACKET/focused_capture.py" "$REPO"
"$PACKET/scratch/venv/bin/python" "$PACKET/build_oracle.py" "$REPO"
python3 "$PACKET/run_focused.py" "$REPO" "$SIMULATOR"
TMPDIR="$PACKET/scratch" python3 "$REPO/sw/litex/iob_pack_selftest.py"
git fetch --no-tags origin 2525eae9567865a8bc741901914bdf5a1caf2c26
python3 "$PACKET/audit_evidence.py" "$REPO"
python3 "$PACKET/verify_tree.py" "$REPO"
python3 "$PACKET/normalize_receipts.py"
```

The bootstrap expects a fresh `scratch/deps` directory.
It installs dependencies only beneath `scratch/venv`.
The focused patch check supplies only the pinned CPU patch target.
It neither generates a CPU nor elaborates full shipping images.

The focused runner awaits two independent tasks concurrently.
Its wrapper replaces inherited unlimited compiler parallelism with `-j 4`.
Outer make commands use `-j16` on individual suite targets.
Every task records its process status and log before returning.
Its disposable checkout initializes actual pinned submodules.
No source fixes or implementation runs are part of this procedure.

The evidence audit reconstructs the overlay using a temporary index.
It checks 112 recorded source files independently for each tree.
Four generated input hashes per tree are reconciled against receipts.
Their original bytes and the full timing reports are not downloaded.
The compact good and defective fixture bytes are independently regenerated.
Both match the public artifact hashes exactly.

`environment-corrections.txt` records the superseded initial setup attempt.
The final logs and return codes are the completed execution evidence.
