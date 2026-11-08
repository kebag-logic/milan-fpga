# Reviewer probes (exact head c687810b74b53b69c1fbdff7bfd0ec9da94eaa78)

Set `TOOLS`, `CLONE` and `PACKET`, then run each from any directory. Disposable trees go under `$PACKET/scratch`.
The hosted CI artifacts were downloaded read-only with `gh run download` (runs 42465293588, 42465283076, base 38295188787).
The author receipts were fetched read-only by blob id from milan-fpga commit d40afd2b2a9b03d685e1e97fb25680461db18a7c. Each blob id was rechecked with `git hash-object`.

| Script | Receipt |
|---|---|
| `equivalence.sh` (+ `equivalence.c`) | `receipts/equivalence.txt` |
| `rv32_symbols.sh` | `receipts/rv32-symbols.txt` |
| `variant.py` (one call per variant, see REPORT.md) | `receipts/variants/*.json` |
| `w1_strength.py` | `receipts/w1-strength.json` |
| `errpath.py` | `receipts/errpath.json`, `receipts/errpath/*` |
| `ratchet.sh` | `receipts/ratchet.txt` |
| `python3 $CLONE/scripts/mutation.py --work $PACKET/scratch/mut-wire --jobs 2 --select wire-put-be` | `receipts/mutation-select-wire*.{txt,rc,json}` |
| `python3 $CLONE/scripts/baremetal.py --work $PACKET/scratch/rv32 --jobs 3` (head) and the same from a base `git archive` | `receipts/baremetal*.txt` |
