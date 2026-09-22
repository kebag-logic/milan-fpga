R221-1 reproduction and receipt index

The report is [REPORT.md](REPORT.md). Scripts and receipts contain factual inputs, checks, and results. `scratch/` contains disposable exported source trees and generated files; it is not evidence of a new implementation commit and need not be published. `public-archive/` contains only the fetched public author/manager evidence. No private standards extracts or other reviewers' reports are included.

Use a fresh output directory and an initialized review clone at the recorded head. The following are example commands; replace `<package>`, `<review-clone>` and `<fresh-output>` with local absolute paths. Every command is prefixed by `rtk`. No command below needs Docker, act, hardware, installations, privilege, or compilation.

```sh
rtk proxy python3 <package>/prepare.py <review-clone> <fresh-output>
rtk proxy python3 -B <package>/probes.py focused <fresh-output>/scratch/candidate <fresh-output>/receipts/focused
rtk proxy python3 -B <package>/probes.py images <fresh-output>/scratch/candidate <fresh-output>/receipts/current-images
rtk proxy python3 -B <package>/probes.py images <fresh-output>/scratch/original-base <fresh-output>/receipts/base-images
rtk proxy python3 -B <package>/probes.py shipping-builds <fresh-output>/scratch/candidate <fresh-output>/receipts/shipping-builds
rtk proxy python3 -B <package>/docs_probe.py <review-clone> <fresh-output>
```

Expected results: focused and image/build commands exit 0. `docs_probe.py` exits 0 only if its current-head Git/no-Git no-submodule cases each exit 1 for the exact new link, its integrated-base control exits 0, and both current-head populated-processor controls exit 0. Its source is unchanged throughout; it only populates the pinned submodule files for the positive controls. Use a new output directory for another docs-probe run because those populations remain after the first run.

`probes.py` loads only scratch candidate builder/test modules. Loader mutations exist only in Python memory. C++ source mutations affect only the scratch copy and are restored after each probe. Its normal-dispatch probe executes the candidate's actual loop with unrelated functions stubbed, and does not claim a full-suite rerun. The shipping-builds mode invokes existing gates 1 and 32; generation writes only in scratch. Original and current image generation use separate Python processes to prevent module-cache mixing.

The review's first three scratch invocations lacked the gPTP export and failed setup. `receipts/setup-attempt-*.log` preserve those failures; `prepare.py` includes all three required pinned exports. Final successful focused, image, and shipping-build results use the complete population. One hosted-log download was initially refused by the CLI because its response contained terminal escape sequences. Retried downloads explicitly permitted capture, stripped ANSI sequences before storage, and retain raw/normalized hashes in `receipts/hosted-docs-download.json`.

| Receipt | Meaning |
|---|---|
| `receipts/issue478.json`, `receipts/pr512.json` | Public issue and initial PR identity/body |
| `receipts/public-*-author-manager-comments.json` | Initial public author/manager discussion snapshot, reviewer bodies excluded |
| `receipts/public-*-updates.json`, `receipts/public-*-final-updates.json` | Later public author/manager results, including failure and cleanup, reviewer bodies excluded |
| `receipts/public-state-final.json` | Last observed source head, draft state, dev, and observation timestamp |
| `receipts/context-89.json`, `context-509.json`, `context-399.json` | Public neighboring scope/ownership boundaries; not additional acceptance |
| `receipts/standards.json` | Local standards document hashes and clause conclusions |
| `receipts/diff-identity.json`, `issue-delta.patch` | Full binary-diff equality and commit/history identities |
| `receipts/focused.log`, `focused/focused-results.json` | Three pristine gates, 115 independent loader cases, seven loader mutations, five actual scratch C++ mutations, normal dispatch, downstream boundary |
| `receipts/shipping-builds.log` | All five builder gate-1 builds and gate-32 schema map |
| `receipts/current-images/`, `base-images/` | Independently generated packed bytes and decoded field/hash records |
| `receipts/image-and-archive-comparison.json` | Five full-image/config comparisons and manifest verification result |
| `receipts/docs-probe/`, `docs-probe.log` | Independent F1 reproduction and positive controls |
| `receipts/hosted-check-runs.json` | Hosted metadata associated with the reviewed source head, at observation time |
| `receipts/hosted-docs-*.log`, `hosted-docs-actual-commit.json` | Failing hosted logs and actual merge checkout/tree identity |
| `receipts/archive-tree.json`, `archive-download.json` | Immutable public evidence tree and downloaded blob/hash identities |
| `receipts/original-public-archive-manifest.json` | Earlier `00ffa6bd` manifest; all 73 entries match the later archive |
| `public-archive/MANIFEST.json` | Later `b671cc6` manifest; all 195 published hashes verified |
| `receipts/integrity-initial.json`, `integrity-final.json` | Equal initial/final index, tracked blobs, filesystem kinds/modes, and submodule identities |

The image comparison is reproducible by comparing the two `images.json` files and each same-named `.aem_desc.bin` byte sequence. The historical author hashes are in `public-archive/author/after-rates.json`. The patch comparison uses these exact commands, whose outputs must be byte-identical:

```sh
rtk proxy git -C <review-clone> diff --binary --full-index b17580b91deb11f3441dfc5d7f9fafe539d929b8 099e191137dd2797407fb8345a452bcc7a965608
rtk proxy git -C <review-clone> diff --binary --full-index ec34fcdee0ca9ffa63564a9af8ad70a3a618de29 d81a302760b84f32d2aa019643f57682bb6e052c
```

The public archive can be reconstructed from the paths and immutable revision in `receipts/archive-download.json`, using the repository's raw-content endpoint. Verify each downloaded file's Git blob ID against `receipts/archive-tree.json`, then SHA-256 against its `published_sha256` entry. No private original file was used to validate a pre-neutralization hash.

`integrity.py` is the original review-specific integrity checker. Its root is deliberately fixed to the reviewed checkout; adapt only that local root to reproduce elsewhere. It disables Git replacement objects and optional locks, compares the index with the commit tree, and hashes the actual tracked file or symlink bytes while checking executable modes. It separately verifies the three required submodules. It does not execute candidate validation orchestration.

Publication: manager may neutralize local paths consistently and preserve the substantive text and results. Publish the factual report, reproducer scripts and relevant receipts. Do not treat scratch mutations or generated output as candidate changes. `FILE_HASHES.json` covers the report/scripts/receipt files at handoff and excludes scratch and the already separately verified public archive.
