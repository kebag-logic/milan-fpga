# Issue #123 / PR #124 — round 2 handoff

Role: author. Status: Complete locally: all required verification passed at the exact head; ready for independent review.

- Repository origin confirmed: `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git`.
- Branch: `123-body-key-check`.
- Base: `870ff88ad35bbd532244e4c7e6d7661b9f6e1366`.
- Round-1 starting head: `eb734969154d5a75ff84b2779ff6088a2f4311a5`.
- Round-2 head: `11dd3e903685183250e7cd8ecc391b04fe7fd494`.
- Subject: `Align descriptor body-key tests with consumer conventions`.
- Exactly one new commit above round 1; one-line subject, no body or trailers.
- Round-2 diff: three files, 26 insertions and 12 deletions.

## Assignment and source review

Read the [round-2 assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/123#issuecomment-5847977272),
[internal review](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/123#issuecomment-5847976048),
[external review](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/123#issuecomment-5847930248),
and [manager disposition](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/123#issuecomment-5847888234).
Both full public reports were read from the fetched evidence and verified to match their issue comments, apart from trailing whitespace.

Also read `tb/desc_store/test_gen_desc_image.py`, the documented and annotated unittest idiom in `tb/pp_top/test_fixture_guards.py`, the full generator, F07.4 in `docs/architecture/07_memory_maps.md`, and parent Rule 12 via `git show HEAD:docs/development/CODE_QUALITY.md`. Rule 12 has a 0/0 signature/docstring budget. The parent checkout at `309f9e3e6aedac8e664808c21f59163c643253d5` was used read-only; no parent checkout, build or edit occurred. The parent scan imports ran with bytecode writing disabled.

## Four requested changes

| Item | Change | Location |
| --- | --- | --- |
| F1 | All four helpers and six tests have complete signatures and docstrings describing what they build or prove. | `tb/desc_store/test_gen_desc_image.py:26` through the six test methods at line 109 onward |
| F2 | Removed `timeout=60` from the CLI invocation; hang bounding remains with the runner. | `tb/desc_store/test_gen_desc_image.py:57` |
| Shared sketch suggestion | Added the two-byte, zero-valued `descriptor_index` immediately after `descriptor_type`. | `hdl/aecp/desc/gen_desc_image.py:31` |
| F07.4 suggestion | Added one sentence stating bytes 0–3 equal the index-map type/index key and disagreement is refused by the generator. | `docs/architecture/07_memory_maps.md:246` |

[behavior-audit.json](behavior-audit.json) records that the generator's executable syntax is unchanged from round 1. All test statements and assertions are also unchanged except removal of the CLI deadline; the remaining edits are annotations, docstrings and their type import. No HDL, port, parameter, image format or test wiring changed. Issue #60's published acceptance is untouched.

## Unchanged review scans

Fetched `pp123-review-evidence` from `https://github.com/kebag-logic/milan-fpga.git` into a scratch repository under `/tmp`; evidence commit `b4a249b6c089e9c195c631b665e371ab48e02040`.
The two original scripts in `review-evidence/pp123-r1/reviews/R336-1/scripts/` ran without modification. [reproduction-sources.json](reproduction-sources.json) records their hashes and the unchanged round-1 mutant driver.

Arguments were `GATE_DIR=$LANES/pp123-parent-consumer/scripts`, `BASE=/tmp/pp123-round2.nEMWg5/base`, and `HEAD=/tmp/pp123-round2.nEMWg5/head`. BASE and HEAD were exported with `git archive` from `870ff88a` and `11dd3e903685183250e7cd8ecc391b04fe7fd494`, respectively, before scanning. No checkout was substituted for those exports.

- Idiom: base and head both have **0 unannotated and 0 undocumented** public functions. The unchanged pre-existing long `gen_ucode.py` module is the only non-zero scan row. [Receipt](parent-idiom-scan.log).
- Wall clock: base **0** flagged files, head **0**, added **[]**. [Receipt](parent-wallclock-scan.log).

These are the parent's per-file detectors, not a claim that the entire parent consumer bank ran here.

## Tests and round-1 mutant

Six tests / 24 cases pass at the new head through both `build()` and the CLI. Four key spellings are exercised for each body form and probe. The target remains cfg 1 / index 1, and each mismatch changes only a high byte. The unchanged exact-message, no-output and byte-preservation assertions remain active.

The [round-1 mutant driver](mutant.py) was copied byte-for-byte from the public evidence and run in a separate archive export under `/tmp`. It removes only the body/key check and restores the source byte-for-byte. [mutant.patch](mutant.patch) contains the exact deletion at the new head. Its own [gate result](mutant-proof.log) is rc 0, requiring all expected outcomes below.

| Probe | New head | Check removed | Evidence |
| --- | --- | --- | --- |
| Legal fields and literal bytes | 8 accepted | 8 accepted; rc 0 | [mutant-legal.log](mutant-legal.log) |
| Type-only mismatch, both forms | 8 refused | 8 refusal failures; rc 1 | [mutant-type.log](mutant-type.log) |
| Index-only mismatch, both forms | 8 refused | 8 refusal failures; rc 1 | [mutant-index.log](mutant-index.log) |
| `make generator-check` | all 24 cases pass; rc 0 | 16 refusal failures, legal controls pass; rc 2 | [mutant-entry.log](mutant-entry.log) |

The expected nonzero mutant subprocess statuses are discrimination evidence, separate from the required green gates.

## Re-recorded image digests

[compare_images.py](compare_images.py) rebuilds all nine round-1 image paths from three archive exports: base, round 1 and round 2. It also builds all eight legal probe images with each revision's generator. Every artifact was compared byte-for-byte as well as by digest and size; each matches the published round-1 table. The direct example map, store map and all legal probe maps also agree.

The new records are [image-digests.json](image-digests.json) and [probe-image-digests.json](probe-image-digests.json). Build commands are in `images-base-build.log`, `images-round1-build.log`, and `images-head-build.log`; [image-comparison.log](image-comparison.log) is the rc 0 receipt. Generated image files and source exports stay in scratch storage.

| Image | Bytes | Base SHA-256 | Round-1 SHA-256 | Round-2 SHA-256 | Byte-identical |
| --- | --- | --- | --- | --- | --- |
| `example_milan_8.bin` | 1880 | `20356f5967e45a9eafcf8a63c5c933dca75fccb5d6bbc16941dc91dc2483b62c` | `20356f5967e45a9eafcf8a63c5c933dca75fccb5d6bbc16941dc91dc2483b62c` | `20356f5967e45a9eafcf8a63c5c933dca75fccb5d6bbc16941dc91dc2483b62c` | Yes |
| `yosys_ucode.hex` | 26624 | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` | Yes |
| `yosys_ltn_rom.hex` | 6138 | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | Yes |
| `tb/desc_store/image.bin` | 1880 | `20356f5967e45a9eafcf8a63c5c933dca75fccb5d6bbc16941dc91dc2483b62c` | `20356f5967e45a9eafcf8a63c5c933dca75fccb5d6bbc16941dc91dc2483b62c` | `20356f5967e45a9eafcf8a63c5c933dca75fccb5d6bbc16941dc91dc2483b62c` | Yes |
| `tb/acmp_listener/ltn_rom.hex` | 6138 | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | Yes |
| `tb/acmp_nvm/ltn_rom.hex` | 6138 | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | Yes |
| `tb/pp_top/ltn_rom.hex` | 6138 | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | Yes |
| `tb/pp_top/ucode.hex` | 26624 | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` | Yes |
| `tb/ucpu/ucode.hex` | 26624 | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` | Yes |
| Probe `fields-str-AUDIO_CLUSTER.bin` | 88 | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | Yes |
| Probe `fields-int-20.bin` | 88 | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | Yes |
| Probe `fields-str-0x0014.bin` | 88 | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | Yes |
| Probe `fields-int-4660.bin` | 88 | `a0483ef462002afaece023610f8fb2297c5b451c21e6e59befc9a7b610740c04` | `a0483ef462002afaece023610f8fb2297c5b451c21e6e59befc9a7b610740c04` | `a0483ef462002afaece023610f8fb2297c5b451c21e6e59befc9a7b610740c04` | Yes |
| Probe `bytes-str-AUDIO_CLUSTER.bin` | 88 | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | Yes |
| Probe `bytes-int-20.bin` | 88 | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | Yes |
| Probe `bytes-str-0x0014.bin` | 88 | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | Yes |
| Probe `bytes-int-4660.bin` | 88 | `a0483ef462002afaece023610f8fb2297c5b451c21e6e59befc9a7b610740c04` | `a0483ef462002afaece023610f8fb2297c5b451c21e6e59befc9a7b610740c04` | `a0483ef462002afaece023610f8fb2297c5b451c21e6e59befc9a7b610740c04` | Yes |

## Gates

All commands run in the foreground, without piping gate output; output is written directly to logs and exact return codes are retained. The runner provides a generous 7,200-second bound per gate. [run_evidence.py](run_evidence.py) is the unchanged round-1 foreground runner.

The HDL runs use the installed pinned Verilator 5.050, rather than round 1's host 5.052. A scratch wrapper caps Makefile requests for `-j 0` at eight jobs without changing repository files or other arguments. Python 3.14.7, Yosys 0.66 and sv2v 0.0.13 are the local versions. [environment.json](environment.json) records provenance and paths. Dependencies and scratch trees are outside this output directory.

| Gate | rc | Seconds | Evidence |
| --- | --- | --- | --- |
| `tests-head` | 0 | 1.22 | [tests-head.log](tests-head.log) |
| `parent-idiom-scan` | 0 | 0.21 | [parent-idiom-scan.log](parent-idiom-scan.log) |
| `parent-wallclock-scan` | 0 | 0.92 | [parent-wallclock-scan.log](parent-wallclock-scan.log) |
| `image-comparison` | 0 | 1.77 | [image-comparison.log](image-comparison.log) |
| `mutant-proof` | 0 | 1.22 | [mutant-proof.log](mutant-proof.log) |
| `make-check` | 0 | 27.0 | [make-check.log](make-check.log) |
| `lint-hdl` | 0 | 8.59 | [lint-hdl.log](lint-hdl.log) |
| `suites` | 0 | 408.32 | [suites.log](suites.log) |
| `yosys` | 0 | 70.5 | [yosys.log](yosys.log) |
| `matrix` | 0 | 0.06 | [matrix.log](matrix.log) |
| `params` | 0 | 0.06 | [params.log](params.log) |
| `docs-matrix` | 0 | 0.03 | [docs-matrix.log](docs-matrix.log) |
| `docs-wavedrom` | 0 | 0.46 | [docs-wavedrom.log](docs-wavedrom.log) |
| `docs-stale` | 0 | 0.06 | [docs-stale.log](docs-stale.log) |
| `fetch-figure-history` | 0 | 0.56 | [fetch-figure-history.log](fetch-figure-history.log) |
| `nvm-figures` | 0 | 236.27 | [nvm-figures.log](nvm-figures.log) |
| `links` | 0 | 0.11 | [links.log](links.log) |
| `diff-check` | 0 | 0.0 | [diff-check.log](diff-check.log) |
| `final-diff-check` | 0 | 0.02 | [final-diff-check.log](final-diff-check.log) |

Each JSON receipt records the exact command. `make-check` is `make check`; `suites` is the full `scripts/run_suites.sh`; `lint-hdl` is `scripts/lint_hdl.sh`; `yosys` is `syn/yosys/run.sh`. `matrix` runs `gen_matrix.py --check`; `params` runs the parameter inventory; `docs-matrix`, `docs-wavedrom`, `docs-stale`, and `links` are the exact documentation workflow commands. `nvm-figures` runs `make -C tb/nvm_port figures`, after fetching the historical pull ref required by the workflow. Diff checks cover both the worktree and the complete base-to-head change.

Completed documentation results: 41 Mermaid and 18 WaveDrom blocks, 915 links, 115 requirement rows and 17 recorded gap findings, 92 module rows with zero untested, and all 24 parameters consistent. HDL lint passes all 40 modules.

The full sweep passes all 33 suites and 1,014,722 checks; desc_store remains 584/584.

The portability gate passes all 35 tops and the Xilinx stage-memory and six-RAMB36 assertions.

The independent nvm_port figure gate completes its 46 builds with all measured README figures agreeing.

## Delivery and remaining ownership

[PR-BODY.md](PR-BODY.md) is replacement PR text: the updated round-1 description followed by a Round 2 section and `Closes #123`. It has no attribution footer or absolute home paths.

Final integrity checks pass: the worktree and index match the committed tree, the commit message has only its one-line subject, and exactly three files changed in the single round-2 commit. The parent head and clean status are unchanged. Suite-generated images still match the recorded digests. See [final-integrity.json](final-integrity.json), [round2.patch](round2.patch), and [archive-provenance.json](archive-provenance.json). The final worktree, index and base-to-head diff checks all return 0 in `final-worktree-diff-check.log`, `final-index-diff-check.log` and `final-commit-diff-check.log`.

The authorized [review-ready issue comment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/123#issuecomment-5848100735) was posted with the full new head. Its exact text is [REVIEW-READY.txt](REVIEW-READY.txt); [review-ready-post.log](review-ready-post.log) records successful posting (rc 0). No push, PR creation/edit, merge or hardware run occurred. The commit remains local.

The parent pin-update patch still owns the DUT-source reader disposition, the earlier port wiring and the parent consumer-bank rerun. The full parent bank and five-configuration shipping-image comparison at this new pin are not claimed here. Independent re-review and final integration acceptance remain with the reviewers and manager.

Only this assigned output directory was accessed under the dated management directory; no private transcripts were read. The parent repository remained read-only.
