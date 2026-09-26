# Issue #123 handoff

Role: author [A342]
Status: complete locally; all required gates pass; ready for review.
Repository: `Mister-M-alt/protocol-processor-control-plane-avb-milan`
Origin confirmed: `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git`
Branch: `123-body-key-check`
Base: `870ff88ad35bbd532244e4c7e6d7661b9f6e1366`
Head: `eb734969154d5a75ff84b2779ff6088a2f4311a5`
Commit subject: `Refuse descriptor bodies that disagree with their directory keys`
One commit, one-line subject, no body or trailers. Working tree clean.

Assignment: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/123#issuecomment-5847636202

## Scope and source review

One new `ImageError` compares the assembled body's big-endian type at offset 0
and index at offset 2 with the normalized directory key. Both `fields` and
literal `bytes` converge before this check. The diagnostic names the cfg, key
type/index and body type/index. Existing body assembly, padding, image layout,
name binding and rendering code are unchanged.

Read the issue and assignment; the full generator and its existing refusals;
the full worked example; `tb/desc_store`; all generator references from
`git grep -n gen_desc_image`; the repository README, integrator and HDL engineer
guides, `hdl/README.md`, `docs/README.md`, and `.github/workflows/hdl.yml`.
There is no separate tracked contribution or style file; the repository and
guide conventions above supply those rules. The sole pre-existing build caller
of the descriptor generator is `tb/desc_store/Makefile`.

## Change list

| File:line | Change |
| --- | --- |
| `hdl/aecp/desc/gen_desc_image.py:40` | Document body/key agreement for both input forms. |
| `hdl/aecp/desc/gen_desc_image.py:215` | Decode the two body u16 fields and add one contextual `ImageError` refusal. |
| `tb/desc_store/test_gen_desc_image.py:20` | Six tests / 24 cases, using independent legal and type-only/index-only probes through `build()` and the CLI. |
| `tb/desc_store/test_gen_desc_image.py:64` | Legal controls assert exact descriptor bytes and CLI output files. |
| `tb/desc_store/test_gen_desc_image.py:82` | Refusals require the named exception and exact context; CLI exit 1 and no image/map. |
| `tb/desc_store/Makefile:21` | Existing default run depends on `generator-check`; the repository suite sweep therefore runs these tests. |
| `tb/desc_store/Makefile:31` | Dedicated generator-only target. |
| `tb/desc_store/README.md:59` | Explain probes, input coverage, and the measured mutation result. |

## Test and mutant results

Each row contains four key variants: named, integer, hex string, and numeric
type outside the name table. Configurations and directory indices stay dense.
The target is cfg 1, index 1. A refusal probe changes only the high byte of its
body type or index, preventing a comparison of low bytes alone from passing.

| Probe | With check | Base / check removed |
| --- | --- | --- |
| Legal `fields` | 4 accepted; library and CLI pass | 4 accepted; legal test passes |
| Legal `bytes` | 4 accepted; library and CLI pass | 4 accepted; legal test passes |
| Type mismatch only, `fields` | 4 refused; `ImageError`, CLI rc 1, no outputs | 4 refusal assertions fail: `ImageError` not raised |
| Type mismatch only, `bytes` | 4 refused; `ImageError`, CLI rc 1, no outputs | 4 refusal assertions fail: `ImageError` not raised |
| Index mismatch only, `fields` | 4 refused; `ImageError`, CLI rc 1, no outputs | 4 refusal assertions fail: `ImageError` not raised |
| Index mismatch only, `bytes` | 4 refused; `ImageError`, CLI rc 1, no outputs | 4 refusal assertions fail: `ImageError` not raised |

Example type refusal: `cfg 1 directory key type 0x0014 index 1 disagrees with body type 0x0114 index 1`.
Example index refusal: `cfg 1 directory key type 0x0014 index 1 disagrees with body type 0x0014 index 257`.

`tests-before.log` records the probes against the unchanged base generator:
16 negative cases fail, both legal tests pass. `tests-after.log` records all
six tests / 24 cases passing after the fix. The existing desc_store RTL suite
still reports 584 checks, all passing; its tally is separate from the Python
cases. The full sweep passes 33 suites, 1,014,722 checks, zero failing.

The reproducible [mutant script](mutant.py) removes only the new comparison,
its two decoding assignments and its `ImageError`; the exact removed block is
[mutant.patch](mutant.patch). It restores the source byte-for-byte in `finally`.
Run it from this repository root using `python3 <evidence-directory>/mutant.py`.
Its own rc 0 requires these measured subprocess results:

| Mutant run | Expected and observed rc | Evidence |
| --- | --- | --- |
| Legal controls, both forms | 0; 2 tests / 8 cases pass | [mutant-legal.log](mutant-legal.log) |
| Type-only refusal probes, both forms | 1; 8 failures, all `ImageError` not raised | [mutant-type.log](mutant-type.log) |
| Index-only refusal probes, both forms | 1; 8 failures, all `ImageError` not raised | [mutant-index.log](mutant-index.log) |
| `make generator-check` | 2; 16 refusal failures, legal controls pass | [mutant-entry.log](mutant-entry.log) |

These intentional nonzero mutant results are the discrimination proof. They
are separate from the required green repository gates below.

## Image digests

The original nine image destinations were built and saved before the generator
edit, then rebuilt after it. `example_milan_8.bin` is the direct CLI build of
`hdl/aecp/desc/example_milan_8.json`; `tb/desc_store/image.bin` is the repository
Makefile build of that same example. The ROM paths are included for completeness;
`yosys_*.hex` are the two temporary ROM inputs built by the Yosys script.

The eight additional legal probe images were generated using the exact base
revision's generator loaded in memory, then the changed generator. No extra
checkout or source-tree export was used. Every image was compared byte-for-byte
as well as by SHA-256. The direct example map and all legal probe maps agree too.
Saved bytes are under `images-before/` and `images-after/`; repository path
separators in saved filenames are replaced by `__`. Inventory and exact build
commands are in `images-before-build.log` and `images-after-build.log`.

| Image | Bytes | Before SHA-256 | After SHA-256 | Identical |
| --- | --- | --- | --- | --- |
| `example_milan_8.bin` | 1880 | `20356f5967e45a9eafcf8a63c5c933dca75fccb5d6bbc16941dc91dc2483b62c` | `20356f5967e45a9eafcf8a63c5c933dca75fccb5d6bbc16941dc91dc2483b62c` | Yes |
| `yosys_ucode.hex` | 26624 | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` | Yes |
| `yosys_ltn_rom.hex` | 6138 | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | Yes |
| `tb/desc_store/image.bin` | 1880 | `20356f5967e45a9eafcf8a63c5c933dca75fccb5d6bbc16941dc91dc2483b62c` | `20356f5967e45a9eafcf8a63c5c933dca75fccb5d6bbc16941dc91dc2483b62c` | Yes |
| `tb/acmp_listener/ltn_rom.hex` | 6138 | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | Yes |
| `tb/acmp_nvm/ltn_rom.hex` | 6138 | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | Yes |
| `tb/pp_top/ltn_rom.hex` | 6138 | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | Yes |
| `tb/pp_top/ucode.hex` | 26624 | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` | Yes |
| `tb/ucpu/ucode.hex` | 26624 | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` | Yes |
| Probe `fields-str-AUDIO_CLUSTER.bin` | 88 | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | Yes |
| Probe `fields-int-20.bin` | 88 | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | Yes |
| Probe `fields-str-0x0014.bin` | 88 | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | Yes |
| Probe `fields-int-4660.bin` | 88 | `a0483ef462002afaece023610f8fb2297c5b451c21e6e59befc9a7b610740c04` | `a0483ef462002afaece023610f8fb2297c5b451c21e6e59befc9a7b610740c04` | Yes |
| Probe `bytes-str-AUDIO_CLUSTER.bin` | 88 | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | Yes |
| Probe `bytes-int-20.bin` | 88 | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | Yes |
| Probe `bytes-str-0x0014.bin` | 88 | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | `005bbc19997a4af7454d3083c0e837fed1e791ba502d31a94d36f0d771a8f071` | Yes |
| Probe `bytes-int-4660.bin` | 88 | `a0483ef462002afaece023610f8fb2297c5b451c21e6e59befc9a7b610740c04` | `a0483ef462002afaece023610f8fb2297c5b451c21e6e59befc9a7b610740c04` | Yes |

Machine-readable digest records: `image-digests-before.json`,
`image-digests-after.json`, and `probe-image-digests.json`.
Suite outputs were checked against the saved baseline again after the full run.

## Gates

All commands ran in the foreground, with output directed straight to log files
and exact return codes retained; no gate was piped. Long-running commands used
a 7,200-second timeout. Versions: Verilator 5.052, Yosys 0.66, sv2v 0.0.13.
The documentation workflow also requires the independent nvm_port figure gate;
its historical pull ref was fetched exactly as CI specifies, with no checkout
or branch change. That gate completed 46 builds and all measured figures agree.

| Command | rc | Seconds | Evidence |
| --- | --- | --- | --- |
| `make -C tb/desc_store generator-check` | 0 | 1.17 | [tests-after.log](tests-after.log) |
| `python3 <evidence-directory>/mutant.py` | 0 | 1.22 | [mutant-proof.log](mutant-proof.log) |
| `make check` | 0 | 28.84 | [make-check.log](make-check.log) |
| `scripts/run_suites.sh` | 0 | 459.42 | [suites.log](suites.log) |
| `scripts/lint_hdl.sh` | 0 | 11.49 | [lint-hdl.log](lint-hdl.log) |
| `syn/yosys/run.sh` | 0 | 71.01 | [yosys.log](yosys.log) |
| `python3 scripts/gen_matrix.py --check` | 0 | 0.06 | [matrix.log](matrix.log) |
| `python3 scripts/check-integrator-params.py` | 0 | 0.06 | [params.log](params.log) |
| `python3 scripts/check-matrix.py` | 0 | 0.03 | [docs-matrix.log](docs-matrix.log) |
| `python3 scripts/render-wavedrom.py --check` | 0 | 0.42 | [docs-wavedrom.log](docs-wavedrom.log) |
| `make stale` | 0 | 0.06 | [docs-stale.log](docs-stale.log) |
| `make -C tb/nvm_port figures` | 0 | 244.88 | [nvm-figures.log](nvm-figures.log) |
| `python3 scripts/check-links.py` | 0 | 0.11 | [links.log](links.log) |
| `git diff --check` | 0 | 0.00 | [diff-check.log](diff-check.log) |
| `git diff --cached --check` | 0 | 0.00 | [staged-diff-check.log](staged-diff-check.log) |
| `git diff --check 870ff88ad35bbd532244e4c7e6d7661b9f6e1366 HEAD` | 0 | 0.00 | [final-diff-check.log](final-diff-check.log) |

`make check`: 41 Mermaid and 18 WaveDrom blocks; 915 links; 115 requirement rows
and 17 gap findings; 92 module-matrix rows with zero untested; 24 parameters in
the top, guide and diagram. HDL lint: 40 modules. Yosys: all 35 listed tops plus
the Xilinx stage-memory and total-RAMB36 assertions.

## Review delivery and remaining ownership

`PR-BODY.md` is the prepared PR text. The final delivery action is to post
`[A342] REVIEW READY` with head `eb734969154d5a75ff84b2779ff6088a2f4311a5` on issue #123.
The commit remains local; no push, PR creation/edit, merge, other checkout,
hardware action or parent-repository edit was performed. No RTL, port or
parameter changed; issue #60's published acceptance is untouched.

The parent's shipping descriptor images at the new pin remain the assigned
consumer bar after the PR, outside this lane. No parent files or private
transcripts were read. Only this assigned evidence directory was accessed under
the dated management directory.
