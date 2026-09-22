R225-1 receipts for PR #507 at 0d43ff25d38917e77bb5c3d2ddb6473013cea3ba.

Run from the isolated candidate checkout. Bind `R225_RECEIPTS` to this archived directory. Shell commands use the required RTK prefix. The source scripts contain the exact base/head revisions and public archive revision.

```sh
rtk proxy python3 -B "$R225_RECEIPTS/review_probe.py" setup
rtk proxy python3 -B "$R225_RECEIPTS/review_probe.py" observe base
rtk proxy python3 -B "$R225_RECEIPTS/review_probe.py" observe head
rtk proxy python3 -B "$R225_RECEIPTS/review_probe.py" e2e base
rtk proxy python3 -B "$R225_RECEIPTS/review_probe.py" e2e head
rtk proxy python3 -B "$R225_RECEIPTS/review_probe.py" live
rtk proxy python3 -B "$R225_RECEIPTS/reader_cli_probe.py"
rtk proxy python3 -B "$R225_RECEIPTS/mutation_probe.py"
rtk proxy python3 -B "$R225_RECEIPTS/scope_probe.py"
rtk proxy python3 -B "$R225_RECEIPTS/integrity_probe.py"
```

`setup` reads frozen Git objects and downloads the 205 archived HTML responses; it changes only this evidence directory. `live` sends synthetic Markdown to the rendering API and saves fresh responses; it publishes no repository content. Other probes use scratch copies or temporary fixture repositories. No candidate file is edited.

| Receipt | Contents |
|---|---|
| `issue440.json`, `issue440-comments.json`, `decision5771170243.json`, `r86-9.json` | Public task contract, decisions and historical review; compressed bodies omitted from the comments receipt |
| `pr507.json`, `pr507-comments.json`, `ready5772565104.json` | Public implementation and validation/readiness state read for this review |
| `candidate.diff`, `snapshots/` | Exact six-file diff and relevant scripts from both frozen revisions |
| `public-evidence/` | Selected expanded author/manager artifacts downloaded from the frozen public archive; attributed evidence |
| `public-renderer/`, `public-renderer-index.json` | 205 archived responses, independently counted, with source URLs and hashes |
| `live-renderer/`, `live-renderer.json` | 25 fresh synthetic requests/responses, exits, response hashes and normalized-head comparisons |
| `corpus-base.json`, `corpus-head.json` | Same 205 fixtures through both engines, raw and actual Path.read_text input |
| `boundaries-base.json`, `boundaries-head.json` | 3,614 independent grammar probes, exact source, expected and observed heading counts; base has 368 mismatches, head has zero |
| `e2e-base.json`, `e2e-head.json` | 17 actual Git base/head judgments, added lines, findings, exemptions and reader normalization; five base exemption mismatches, zero head mismatches |
| `reader-cli.json` | Eight actual generator CLI controls; all meet the expected success, stale-TOC or named-refusal outcome |
| `controls-base.json`, `controls-head.json` | Existing arm identities and fixture strings by family |
| `pages-base.json`, `pages-head.json` | Both parser engines on both complete tracked Markdown populations |
| `summary.json` | Corpus/page/control comparisons and production AST scope comparison |
| `mutations/`, `mutations.json` | Eleven exact patches and complete selftest outputs: ten issue-property variants detected; one unchanged length-condition variant survives |
| `gates.json`, `gate-*.json` | Local gate commands, exit codes, durations, stdout and stderr; includes the honest idiom setup refusal |
| `initial-integrity.json`, `final-integrity.json`, `tracked-sha256.json` | Frozen checkout identity, index equality, all tracked bytes/modes and uninitialized submodule state |
| `SHA256SUMS` | Final deliverable file hashes, excluding itself |

The mutation runner initially asserted that all eleven exploratory variants must fail. The unchanged length-condition variant survived, so that reviewer assertion failed. The runner now explicitly distinguishes that observed optional-coverage result from the ten issue-property variants; the candidate was unchanged throughout. The final mutation receipts preserve the surviving variant's successful selftest outputs.

The original historical 504-row/106-row campaigns were not recreated in full. The public 205-row reconstruction and its exact expanded inputs were used for the historical closer population. Fresh GFM calls independently spot-check 25 cases; the other renderer results remain attributed archived observations.
