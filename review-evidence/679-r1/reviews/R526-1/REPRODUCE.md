Run from an exact-head candidate checkout with its required submodules initialized. Use a fresh copy of this packet's scripts with empty scratch directories. The host C/C++ test libraries and PyYAML must already be available.

```sh
sh <packet>/scripts/setup.sh
python3 <packet>/scripts/run-focused.py <checkout>
python3 <packet>/scripts/run-contract-checks.py <checkout>
python3 <packet>/scripts/independent-rv32.py <checkout>
python3 <packet>/scripts/runtime-binding-probe.py <checkout>
python3 <packet>/scripts/verify-tree.py <checkout>
```

The original focused driver uses separate store mutant paths and may rebuild slowly. The completed review instead used the unchanged store driver with physical worker-directory reuse:

```sh
python3 <packet>/scripts/nvm-reuse.py <checkout> --jobs 8
```

Do not overlap the original store campaign with its replacement. Keep total compiler workers at or below 16. The focused driver assigns 3 ctrl, 6 store, 4 coverage workers and one serial RV32 control. It records every exit status; the review's interrupted original store run is retained, not counted as a pass. Setup installs the locked documentation dependencies in scratch; use that environment's Python for the successful em-dash and contents checks.

The runtime-binding probe exits zero when its experiment completes. Its result JSON records each actual firmware-arm result. At the reviewed head, both masked cases return zero even though the partial link retains the disallowed undefined symbol. After correction, both masked cases should return failure while the ordinary positive firmware remains accepted.

Probe copies are never written into the candidate checkout. All generated builds and environments stay under scratch. The publication script normalizes local paths and terminal color only.
