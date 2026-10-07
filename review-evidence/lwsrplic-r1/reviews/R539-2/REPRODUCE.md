The scripts accept an isolated source checkout and keep disposable work under this packet's `scratch/` directory. Run from the packet directory. Python, Git, a C11 compiler, Make, CMake, the scenario runner, and authenticated read access to the repositories are required. No shared installation is changed.

```sh
mkdir -p scratch receipts
git clone --no-checkout https://github.com/kebag-logic/lwSRP.git scratch/fresh
curl -fsSL https://www.apache.org/licenses/LICENSE-2.0.txt -o scratch/apache-license.txt
curl -fsSL https://github.com/cgreen-devs/cgreen/archive/refs/tags/1.7.0.tar.gz -o scratch/cgreen.tar.gz
tar -xzf scratch/cgreen.tar.gz -C scratch
python3 -m pip install --no-compile --target scratch/pydeps kconfiglib==14.1.0 PyYAML
python3 scripts/audit.py "$REVIEW_SOURCE" scratch/fresh scratch/apache-license.txt
python3 scripts/provenance.py scratch/fresh
python3 scripts/run_checks.py "$REVIEW_SOURCE"
PYTHONPATH=scratch/pydeps python3 scripts/robustness.py
git init --bare scratch/original.git
git -C scratch/original.git fetch https://github.com/kebag-logic/lwSRP.git 86a5f74c028dedec2a0f5bc1c5a258bbd83746b9:refs/heads/published-before-rewrite
python3 scripts/compare_history.py scratch/original.git scratch/fresh
sha256sum -c MANIFEST.sha256
```

Set `REVIEW_SOURCE` to a clean checkout at `4eba61b7b1c49fc9b7260a487240ca86f9d38168`. Use a fresh output directory for a new run; a later branch update changes the all-branch history input. The six observed branch tips are recorded in `receipts/audit.log`.

The original head was obtained from the public PR #12 force-push event, retained in `receipts/force-push.json`. It contains all 35 original commits. Original commit availability depends on the hosting service retaining old objects. Do not fetch it into the fresh publication-history clone: the two histories are intentionally inspected in separate repositories.

The history comparison matches author and committer identities, both timestamps, encoding and message bytes; requires one-to-one pairing; checks mapped parents; and permits only the authorized historical file and architecture-line removals. It also verifies both open PR head trees remain identical. Two signatures disappear because their signed commit objects changed.

The build script runs independent documentation and dependency/build campaigns concurrently under a foreground process. It uses `make -j16`, then joins the unit, CTest and scenario runs. The robustness script joins four bounded workers. No full parent bank or hardware operation is included. Logs have separate exit-code files; negative probes intentionally return nonzero. The external link check retains its HTTP 403 failure.

Published logs preserve process output except that local source and scratch roots become `$SOURCE` and `$SCRATCH`. Unmodified originals, downloads, dependencies, build trees and probe copies remain unpublished in `scratch/`. `receipts/validation-metadata.json` binds the campaign to the exact head and records the dependency archive hash; `receipts/integrity.json` independently binds every source/export file to its Git blob and mode.

The scanner uses encoded restricted-name patterns so its published source does not reproduce those names. Such screening is finite and cannot prove the absence of every possible identifier. It scans paths, full commit objects and all unique blobs reachable from `git rev-list --all` in the fresh six-branch clone. The separate provenance scan checks licence identifiers, competing notice markers, private paths and credential markers.

Merge preservation can be reproduced in the fresh scratch clone with `git merge-tree --write-tree bc6687afb17b0e190cbb9db4b335aeca91e99477 1401654530ce7d9275de9b901e67df47e5bbc536`. Exit 1 is expected. Compare the resulting tree with `e59b21f2ee8cb32ee07b3fc4f0799f0197743d5e`: only README resolution and placeholder deletion differ. The final anchor commit is checked separately by `audit.py`.

Only `REPORT.md` and files listed in `MANIFEST.sha256` are publishable. Never publish `scratch/`.
