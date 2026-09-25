[A302]

Round 2 for PR #119 / issue #99 is ready for delta review.

Branch: `99-integrator-params`  
Base: `663d50d65ff49c33b153107b2f79d6f3c5725799`  
Head: `9cde1c19dbfd859257be8e012d4455856fcfce3b`  
Commit: `Fix parameter owner anchors and document the inventory gate`

The commit contains only the assigned changes:

- `docs/guides/integrator.md`: four descriptor rows now use `#sec-desc-memory`; the response-buffer row uses `#sec-resp-memory`.
- `docs/architecture/07_memory_maps.md`: added `<a id="sec-resp-memory"></a>` immediately before section 3.3.2, matching the existing anchor style.
- `docs/architecture/09_verification.md`: section 7 now lists `params` and `scripts/check-integrator-params.py`. It states that the guide section 2 table and diagram 21's `integration-parameters` group each equal the top's overridable parameter set, with no missing, extra or duplicate names; empty or unparseable inputs fail.

This addresses R288-1 F1/F2 and R289-1 F1. The final delta is three files, seven insertions and five deletions. No other repository content changed.

Validation completed in the foreground; every final gate returned 0:

| Gate | Result | Receipt |
|---|---|---|
| `make check` | 41 diagram blocks and 18 waveform blocks; all sub-gates pass | `make-check.log` |
| `python3 scripts/check-links.py` | 916 links, OK | `links.log` |
| `python3 scripts/check-matrix.py` | 115 requirement rows, 17 gap findings, OK | `matrix.log` |
| `python3 scripts/check-integrator-params.py` | top 24, guide 24, diagram 24, OK | `params.log` |
| `python3 scripts/render-wavedrom.py --check` | 18 blocks, OK | `wavedrom-check.log` |
| `make stale` | pass | `stale.log` |
| `git diff --check` | pass | `diff-check.log` |
| Reviewer-equivalent anchor check | 59 checked, 0 dead | `github-anchors.log` |

The documentation commands match the `docs-gates` job in `.github/workflows/hdl.yml`; the existing repository renderer environment supplied its dependency. The `make check` result also includes the generated module matrix: 92 rows, zero untested. Committed file hashes match the tested bytes, and the working tree is clean.

The anchor check retained the reviewer's link extraction and ID matching. It covered `docs/guides/integrator.md`, `docs/architecture/07_memory_maps.md`, `docs/architecture/09_verification.md`, and `docs/diagrams/README.md`. Because this commit remains local, unchanged headings were verified against the base and checked using GitHub's published rendering. The sole new explicit ID was independently confirmed by submitting the edited memory-map file to GitHub's Markdown renderer. The memory-map delta was verified to be exactly that anchor insertion. No publication was required.

The preliminary standalone-renderer probe is retained as `github-anchors-api-probe.log`: that endpoint omits automatic heading IDs, producing 12 false misses. The final check uses the published IDs for unchanged headings and reports zero dead links.

Public review sources: [R288-1](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/119#issuecomment-5827016237) and [R289-1](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/119#issuecomment-5827043730). Their scripts were fetched read-only from `kebag-logic/milan-fpga` archives `e101da3bd5d668dbeb2b6f400189315d06d1448d` and `7ede3850fc64d1d12e0143167f4018d6b559d850`. The anchor script matched its manifest SHA-256 `f94cf26cd3314a155b3eff8ec60657cc5faccb6226ba18cf0c939acf89c97027`; the documentation-gate script also matched its manifest. The fetched archives and scratch scripts were deleted after use.

`PR-BODY.md` contains the full current PR body with the new role marker and Round 2 update, retaining `Closes #99`. `round2.patch` contains the complete delta; `validation.json` records the final return codes. The commit has one subject line, no body and no trailers. No push, PR edit, merge, other checkout, sub-agent, or hardware action was performed. The next step is the assigned delta reviews.
