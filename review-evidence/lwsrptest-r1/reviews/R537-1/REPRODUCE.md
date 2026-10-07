<!-- SPDX-License-Identifier: Apache-2.0 -->

Reproduce in a fresh packet directory containing `review.py` and `binding_probe.py`. Set `REPOSITORY` to a readable checkout containing the reviewed commit and base. Requirements: Python 3.12 or later, C11 compiler, CMake 3.20 or later, make, Git, binutils, and behave. Network access retrieves a checksum-pinned cgreen 1.7.0 archive; nothing is installed outside scratch. The reviewed run used Python 3.14.7, behave 1.3.3, CMake 4.4.3 and compiler 16.2.1.

Run these foreground commands in order:

```sh
python3 review.py "$REPOSITORY" prepare
python3 review.py "$REPOSITORY" baseline
python3 review.py "$REPOSITORY" reversals
python3 review.py "$REPOSITORY" integration
python3 review.py "$REPOSITORY" bindings
python3 review.py "$REPOSITORY" reconcile
python3 review.py "$REPOSITORY" audit
```

Expected failures are checked inside the script; the campaign exits zero only when its command return codes and required output match. All mutations operate on archive copies, leaving the supplied repository unchanged. Each compilation uses at most 16 jobs, and builds run sequentially. The final audit compares actual repository bytes, file modes and the index with the exact tree, and also checks the copied head sources used for tests.

Raw command streams are in `scratch/raw/`, which is never published. `receipts/` has the same streams with absolute paths normalized and command/license headers added. Each `.rc` records the actual command return code after its license comment. Fresh reruns refuse to overwrite existing probe copies; use a fresh packet directory.

The embedded integration check supplies minimal build API stubs to compile the unchanged source list. It does not replace a real embedded SDK build. `reconcile` contains two optional scenario-blind-spot probes and strict-prototype diagnostics used to assess the prior public findings.

`MANIFEST.sha256` is the publication allowlist. Verify it from the packet root with `sha256sum -c MANIFEST.sha256`. It excludes every scratch artifact.
