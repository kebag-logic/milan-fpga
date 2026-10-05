The scripts take explicit repository, scratch, and receipt paths. Use a fresh disposable clone for mutations; the reviewer source checkout is never a mutation target. All disposable repositories, environments, browser downloads and builds belong below this packet's `scratch/`. Commands run in the foreground.

Example, from a fresh copy of this packet:

```sh
rtk proxy python3 scripts/verify_tree.py /path/to/exact-head-checkout
rtk proxy git clone --shared /path/to/exact-head-checkout scratch/probe-tree
rtk proxy env TMPDIR="$PWD/scratch" python3 scripts/probe_gates.py scratch/probe-tree receipts
rtk proxy env TMPDIR="$PWD/scratch" python3 scripts/reproduce_findings.py scratch/probe-tree
rtk proxy env TMPDIR="$PWD/scratch" python3 scripts/prior_controls.py scratch/probe-tree
rtk proxy python3 scripts/authority_checks.py /path/to/exact-head-checkout
rtk proxy python3 scripts/prove_comment_scope.py /path/to/exact-head-checkout scratch /path/to/pinned-simulator
rtk proxy python3 scripts/focused_suites.py /path/to/exact-head-checkout scratch receipts /path/to/pinned-simulator
rtk proxy python3 scripts/verify_tree.py /path/to/exact-head-checkout --final
rtk proxy python3 scripts/verify_tree.py scratch/probe-tree --final
```

The probe orchestrator returns zero after completing and recording its observations, including unexpected survivors. Its `gate-probes.json` contains per-case expectations and actual results. The minimal reproduction script asserts the observed bad behavior at the reviewed head; its zero exit is successful reproduction, not a gate pass. Individual `.rc` files are the gate's exit status. `run_logged.py` can wrap each command with a log and return-code receipt.

For the documentation gate, create `scratch/docs-env` with `python3 -m venv`, install `wavedrom==2.0.3.post3` in it, and install the workflow's three packages with a local prefix: `@mermaid-js/mermaid-cli@11.16.0 mermaid@11.17.2 puppeteer@25.12.0`. Set the package cache and `PUPPETEER_CACHE_DIR` below `scratch/`. Prepend the environment's `bin` and the prefix's `node_modules/.bin` to the existing PATH, retaining the installed JavaScript runtime. From the exact-head checkout run `make -j16 check`. No shared installation is required.

`measure_waveforms.mjs` takes the installed browser driver's entry module, the source checkout, and an optional directory for disposable screenshots. In the pinned installation the entry module is `scratch/mermaid-cli/node_modules/puppeteer/lib/puppeteer/puppeteer.js`. It opens the committed SVGs directly, waits for fonts, and reports text bounding boxes outside each SVG viewport. Screenshots were inspected in `scratch/` and are not published. Font-dependent dimensions are reported explicitly.

`focused_suites.py` verifies simulator version 5.050 before use and runs `side_port`, `tx_arbiter`, and `rx_validator` concurrently in a separate disposable clone. Each invokes `make -j16`, with each nested compiler build limited to four workers. No full suite bank, parent build, hardware operation, or external write is performed.

Only REPORT.md and the files listed in MANIFEST.sha256 are intended for publication. Do not publish scratch/.
