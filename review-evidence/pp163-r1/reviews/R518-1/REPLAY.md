The scripts operate on the assigned exact head and put all generated source copies, build products and mutations under `scratch/`. No script changes the reviewed checkout. Supply absolute paths for `--repo`, `--packet` and `--verilator`; the latter must identify the assigned 5.050 executable. The two proof utilities must already be available on PATH.

Run these commands from any working directory, replacing the three shell variables with those paths:

```sh
python3 "$PACKET/scripts/static_audit.py" --repo "$REPO" --packet "$PACKET"
python3 "$PACKET/scripts/run_focused.py" --repo "$REPO" --packet "$PACKET" --verilator "$PINNED_COMPILER"
python3 "$PACKET/scripts/run_equivalence.py" --repo "$REPO" --packet "$PACKET"
python3 "$PACKET/scripts/run_top_checks.py" --packet "$PACKET" --verilator "$PINNED_COMPILER"
python3 "$PACKET/scripts/cone_audit.py" --packet "$PACKET"
python3 "$PACKET/scripts/verify_state.py" --repo "$REPO" --output "$PACKET/receipts/final-state.json"
```

`run_focused.py` creates the source copy and compiler/build shims used by `run_top_checks.py`, so it must finish before the latter starts. Each supervisor stays in the foreground and waits for all children. Independent units use a bounded worker pool. The mutation campaign receives `--jobs 3`; make receives `-j16`, and each compilation is capped at two workers. The review ran no vendor synthesis job. The packet's source comparison is confined to the arbiter and is not a full synthesis bank.

The clean proofs must return 0. The tie-fault proof must return nonzero with three unproven points. The three changed-feature mutants must be KILLED by their named WD/CX checks; their nonzero simulation return codes are expected. Clean simulations and patch audits return 0.

The published evidence copies retain their original bytes and can be checked against `receipts/public-evidence/MANIFEST.json`. The original public evidence root is `https://github.com/kebag-logic/milan-fpga/tree/fc0046724b1416d5f87451c52eaac1a2668ae4ad/review-evidence/pp163-r1`. The independent cone audit verifies summary arithmetic and the register-family inventory; it cannot rerun the unpublished integrated cone script or inspect its unpublished checkpoint.

Only files listed in `MANIFEST.sha256` and `REPORT.md` are publication inputs. `scratch/` is excluded.
