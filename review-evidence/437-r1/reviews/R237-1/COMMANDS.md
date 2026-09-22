[R237] Reproduction and receipt index

Source checkout: `$VALIDATION_STORAGE/reviews/r237-437-r1`, exact head `65df1df50a80cd5f540a93d8f0cfabc97da3da75`, tree `da06c8609b7a574e3df121fbcb8a1fc8f207dcb7`. These scripts write only to this evidence directory or temporary scratch. No script invokes act, Docker, hosted checks, installs, or full native gates. Python subprocess invocations are argument arrays; shell commands below all begin with rtk.

Run from this directory. Each command stands alone. The scripts use at most four workers; do not launch enough simultaneously to exceed eight total jobs. Renderer calls submit only the saved synthetic text to GitHub's Markdown API.

```sh
rtk proxy python3 -B prepare_snapshots.py
rtk proxy python3 -B focused_gates.py
rtk proxy python3 -B preservation_controls.py
rtk proxy python3 -B renderer_controls.py
rtk proxy python3 -B consumer_controls.py
rtk proxy python3 -B mutation_controls.py
rtk proxy python3 -B block_marker_mutation.py
rtk proxy python3 -B marker_consumer_controls.py
rtk proxy python3 -B replay_published.py
rtk proxy python3 -B integrity.py
```

`mutation_controls.py` extracts only the public mutation literals using `ast.literal_eval`; it does not execute the downloaded author script. `block_marker_mutation.py` defines the independently narrowed mutant. Its two passing self-tests are the observed coverage defect, not a successful negative control. The scripts preserve their complete outputs in JSON and log receipts. The original intended-arm assertion in the first mutation run correctly rejected `markers-in-blocks`; the final script records that false intended-arm attribution explicitly rather than aborting before receipt publication.

- `focused-gates.json` and associated logs: seven independently rerun focused commands, arguments, exits and outputs.
- `preservation-summary.json`, `original-corpus-*`, `updated-corpus-*`, `prior-arms-*`: identical-input comparisons on both committed 163-page populations and all 707 prior arm inputs.
- `renderer-inputs.json`, `renderer-responses.json`, `renderer-summary.json`: 42 independent synthetic inputs with exact GitHub request/response bytes and base/head classifications; six F1 regressions.
- `consumer-summary.json`: 15 base/head real-Git provenance cases and generated navigation, including all six F1 regressions and outside-item/four-space controls.
- `mutation-results.json`, `scratch/mutants/*/*.log`: 17 reproduced public mutations, required intended arm, actual failing arms and exits.
- `block-marker-summary.json`, `block-marker-*.json`, `block-marker-only-*.log`: narrower F3 mutant, both unchanged shipped-suite PASS outputs and three controls exposing its defect.
- `marker-consumer-summary.json`: the same three F3 controls through real-Git provenance, with no unrelated finding.
- `published-replay-responses.json`, `published-replay-summary.json`: replay of all 47 newly published author fixtures and three independent F3 fixtures. This does not assert historical byte or row identity.
- `final-integrity.json`: committed blob/mode/kind/index and registered-submodule verification. `integrity.py` disables replace-object lookup and optional Git locks and hashes disk bytes directly rather than trusting status alone.
- `issue437.json`, `pr515.json`, `comments*-author-manager.json`: read-only public contract/decisions and manager evidence; PR metadata excludes check rollup. Comment indexes contain only metadata and first lines, not reviewer reports.
- `public-packet/`: selected factual evidence from immutable commit `e6013980ef12e558b633c0d18faecc59f1939e8a`. `packet-downloads.json` records verified Git blobs and SHA-256. `public-packet/MANIFEST.json` retains original versus published hash attribution. `fetch_packet.py` can retrieve this selected factual subset again; it does not retrieve reviewer reports or private handoffs.
- `scratch/base` and `scratch/head`: direct committed parser/gate source snapshots; `prepare_snapshots.py` regenerates them. Synthetic Git repositories are temporary; their full page bytes and commit identities are retained in consumer receipts.

The final evidence manifest records SHA-256 for report, scripts and receipts. No source acceptance decision depends on private reasoning.
