Status: PASS for the round-8 desk scope at `701f294405d47a81eed1079d32b54e1eea4a4f31`. No native rerun, implementation change, push, posting or bench operation.

## Decision and qualification

- [ruling.json](ruling.json): exact public ruling and link.
- [DERIVATION.md](DERIVATION.md), [ledger-derivation.json](ledger-derivation.json): all seven original and injected measurements, maxima, figures and margins; both existing ledgers preserved.
- [qualification.json](qualification.json), [qualification-commands.json](qualification-commands.json), [qualification-run.log](qualification-run.log): final-head ledger leg and complete census checks with the unchanged owner model and #969 disposition.
- [egress-ledger.log](egress-ledger.log): all regraded probe instances against the new point.
- [original-arty-negative.log](original-arty-negative.log): expected exit 1 for the retained 62.03635 ms measurement against 61.99 ms, with exactly one finding.
- [usb-at-figure.log](usb-at-figure.log), [usb-one-cycle-over.log](usb-one-cycle-over.log), [boundary-controls.json](boundary-controls.json), [controls/](controls/): exact-limit pass and one-cycle excess rejection using a copy of the retained grade. Production grades are untouched.
- [owner-model.json](owner-model.json): current model equals the retained fixed point; all unchanged owner bounds pass.

## Retained trace regrade

- [retained-trace-identity.json](retained-trace-identity.json): all 159 raw trace hashes and lengths verified against the round-7 archive and completion records; stimuli/status bytes also checked.
- [regraded-identity.json](regraded-identity.json): every regenerated grade matches its retained SHA-256.
- [regrade-commands.json](regrade-commands.json), [regrade-run.log](regrade-run.log), `regrade-<variant>.log`: eight complete regrades, no native execution. The measurement geometry remains `arty-1x1`; only the separate ledger leg selects `arty-usbnet-1x1`.
- [census/](census/): fresh grade files, scripts, status files, journals and per-image summaries. Full raw traces remain in the [round-7 archive](../../round7/receipts/census/ARCHIVE.json), with the original raw and compressed digests; no trace was overwritten.
- [record-classes.log](record-classes.log): cross-image class coverage after regrading.
- [qualification-setup-correction.json](qualification-setup-correction.json), [staged-build-metadata.json](staged-build-metadata.json), [initial-qualification/](initial-qualification/): the first class-check invocation refused missing staged metadata before grading. The unchanged build records were copied beside the results and qualification rerun; no source or trace changed.
- [egress-evidence-identity.json](egress-evidence-identity.json), [egress-evidence-identity.log](egress-evidence-identity.log): all 159 retained wire replay receipts checked against unchanged traces, source bytes and parameters; aggregate verdict rerun. This is evidence carry, not a new wire replay.

## Final-head gates and identity

- [final-gates.json](final-gates.json), [final-gates-run.log](final-gates-run.log): fourteen passing gates and exact CI arguments, interpreter, removal-audit wrapper, head and output digests.
- [ledger-selftest.log](ledger-selftest.log): 218 control executions, all 25 mutations caught. Includes both documentation tables and all three ledger points.
- [inventory-generate.log](inventory-generate.log), [inventory-check.log](inventory-check.log), [inventory-selftest.log](inventory-selftest.log): own-generator regeneration and final freshness; 60 controls pass.
- [contents-selftest.log](contents-selftest.log), [contents-anchors.log](contents-anchors.log), [contents-check.log](contents-check.log), [docs-check.log](docs-check.log), [doc-paths.log](doc-paths.log): final documentation gates, including 1501 contents controls.
- [identity.json](identity.json), [firmware/](firmware/): thirteen unchanged dependency files, unchanged implementation inputs and same pins; six retained ELF/header pairs rehashed and preserved. Arty ELF SHA-256 is `f17d1a9da8ba6e50a1e8cf0af9b77ed434288a1d0a689a357a0c6a57ecda92cf`. No new build is claimed.
- [round8.patch](round8.patch), [local-history.txt](local-history.txt), [final-git-checks.json](final-git-checks.json), [final-head.json](final-head.json): two local commits, separate inventory commit and clean worktree.
- [resources-final.json](resources-final.json): unit weight, CPU affinity, scratch cap and free-space checks. [source/audited-python.py](source/audited-python.py) logs removal paths before deletion by gate fixtures.

## Reproduction

- [source/regrade-retained.py](source/regrade-retained.py) uses unchanged per-group grading and full per-image cross-checks, verifies the retained data and requires exact output hashes. It runs only the regrade path.
- [source/qualify-retained.py](source/qualify-retained.py) runs the new ledger leg, original-point negative control, exact-limit and one-cycle plants, class gate and current owner model.
- [source/verify-egress-carry.py](source/verify-egress-carry.py) checks every retained wire binding and reruns the aggregate verdict.
- [source/final-gates.py](source/final-gates.py) records CI arguments and results at the final head; the wrapper only audits deletions.
- [source/finish-packet.py](source/finish-packet.py) refuses an incomplete or mismatched packet before writing the handoff.

The [round-7 index](../../round7/receipts/INDEX.md) retains native build provenance, full census and fixed-point derivation, injection-chain measurements, filter/LED plants, shaping regressions and their original limitations. Those checks were not rerun here. [MANIFEST.sha256](MANIFEST.sha256) binds this receipt set. Prior root packet entry points are preserved under `prior-root/` before their current links are refreshed.
