[A615]

## Contents

- **[Status](#status)** - Local implementation and validation.
- **[Linked Issue / roles](#linked-issue--roles)** - Public task and reviewers.
- **[Description](#description)** - Image recipe and verification behavior.
- **[Authoritative references](#authoritative-references)** - Public scope decisions.
- **[How to get into the same state](#how-to-get-into-the-same-state)** - Checkout and prerequisites.
- **[How to validate](#how-to-validate)** - Reproduction and expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** - Adoption and evidence boundaries.
- **[Definition of Done](#definition-of-done)** - Remaining merge conditions.
- **[Round 3](#round-3)** - Closed command table and rebuild portability.
- **[Round 4](#round-4)** - Positive forms and scope-correct traversal.

## Status

Local validation GREEN; independent reviews pending. `737-ci-image` -> `dev`.
The round-four changes are committed locally at `e355f789b4f59b86083809299134557ca47bbcfb`. Nothing was pushed.

## Linked Issue / roles

Relates to #737. Image implementation for PR #738.

Executor: `[A615]`
Internal cleared-context reviewer: `[R638]`
External reviewer: `[R639]`

## Description

The workflows currently reinstall their toolchains. This adds a pinned prebuilt tool image with a generated installation inventory, separate tool layers, reproducible cold builds and an authenticated image lock.

The inventory now classifies literal commands through a closed table. It follows executed scripts and Makefile targets, refuses unknown commands and changed script declarations, and records digest-pinned job containers and services. Retained package URLs preserve the locked downloads after archive updates. Export authentication binds the manifest, config and every layer, and privacy allowances require exact public-source provenance.

## Authoritative references

- Issue #737 assignment, comment 6160953880.
- Round-four assignment 6170435035 and amendments 6170543242 and 6170640746.
- Reviews R638-3 (6170421890) and R639-3 (6169543700).
- PR #738 round-three assignment 6167899804 and amendment 6167966247.
- Reviews R638-2 (6167893456) and R639-2 (6166908258).
- Round-two scope/version/literal-mask ruling 6162190578; privacy rulings 6162652582 and 6163057631.
- [Contribution contract](CONTRIBUTING.md), [requirements](REQUIREMENTS.md), [CI workflow policy](docs/testing/CI_WORKFLOWS.md) and [image guide](docs/testing/CI_IMAGE.md).

## How to get into the same state

Use Linux x86-64, Python 3.12 with PyYAML, buildx v0.38.0, the Docker driver with containerd image storage, and the remaining host prerequisites in the image guide. Set `IMAGE_WORK` to persistent writable storage outside the checkout.

```sh
git switch --detach e355f789b4f59b86083809299134557ca47bbcfb
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis third_party/tsn-c-stack
mkdir -p "$IMAGE_WORK/first" "$IMAGE_WORK/second"
export CI_IMAGE_SHFMT="$IMAGE_WORK/shfmt"
python3 ci/image/prepare_parser.py --output "$CI_IMAGE_SHFMT"
base=$(python3 -c 'import json; print(json.load(open("ci/image/sources.lock.json"))["base"])')
docker pull "$base"
docker image save --output "$IMAGE_WORK/first/base-locked.tar" "$base"
cp "$IMAGE_WORK/first/base-locked.tar" "$IMAGE_WORK/second/base-locked.tar"
```

## How to validate

```sh
python3 scripts/ci_tool_inventory.py --check
python3 scripts/ci_tool_inventory_selftest.py
python3 scripts/ci_inventory_patterns_selftest.py
python3 ci/image/build_selftest.py
python3 ci/image/integrity_selftest.py
python3 ci/image/privacy_selftest.py
python3 ci/image/privacy_patch_selftest.py
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest
python3 scripts/check_py_idiom.py
python3 scripts/check_py_idiom.py --selftest
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/check_doc_paths.py
python3 scripts/check_em_dash.py --base fa7347fc
python3 scripts/gen_toc.py --check
python3 ci/image/build.py --work "$IMAGE_WORK/first" --no-cache --defer-lock
python3 ci/image/build.py --work "$IMAGE_WORK/first" --check-lock --verify-archive "$IMAGE_WORK/first/image.tar"
python3 ci/image/build.py --work "$IMAGE_WORK/second" --no-cache --defer-lock
python3 ci/image/build.py --work "$IMAGE_WORK/second" --check-lock --verify-archive "$IMAGE_WORK/second/image.tar"
python3 ci/image/resolve_packages.py --cache "$IMAGE_WORK/first/context/debs"
docker run --rm --network none --mount "type=bind,src=$IMAGE_WORK,dst=/scratch" sha256:86d7aa16e7d2464baf8e0d246434982838c8174de8c8fa610608cce5b23b5e6c python3 /opt/ci-image/smoke.py --work /scratch/smoke
```

Expected: every command exits zero; both exports match the committed manifest, config and all 14 layer identities. The image smoke uses the image's default user. Package regeneration requires `dpkg` and `dpkg-deb`; it was verified inside the image with the repository and package cache mounted read-only.

Manifest: `sha256:86d7aa16e7d2464baf8e0d246434982838c8174de8c8fa610608cce5b23b5e6c`. Config: `sha256:62b56e1ab52dce1a1914e8469429c014e69a465e74e0bdb9a7d8bf4a626b2776`. Size: 3,931,071,698 bytes. Cold Docker builds: 400,411 ms and 436,056 ms. Offline smoke: rc 0, 37.021 seconds.

The final packet receipts are `round4-cold-comparison.json`, `round4-lock.json`, `round4-second-archive.json`, `round4-rebuilt-image.json` and `round4-final-gates.json`. Intermediate failures and preliminary builds are retained and explicitly superseded in `HANDOFF.md`.

## Known limitations / out of scope

- Declared runtime-assembled commands remain a located manual residue checklist. Literal evaluation and unsupported interpreter forms are refused.
- Reproducibility is measured on one host. Registry publication and round-trip verification are pending.
- The previously accepted grouped builder campaign covered all 103 functions exactly once. It remains round-two evidence; this round did not rerun that campaign. The inert `MAKEFLAGS += -e` arm and unavailable `mf48` calibration arm remain explicitly NOT RUN.
- Workflow adoption and full hosted/act acceptance belong to the switch lane. Independent approval, publication and merge remain outstanding.
- No workflow, HDL, firmware, linked-image patch or product-test assertion changed.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

## Round 3

The amended assignment resolves STOP 6167951082. The table declares 214 command names and 109 content-pinned scripts, including reviewed non-installing scripts with network imports or subprocess calls. Controls cover the reported installation forms, keyword `args=`, a newly introduced command, root scripts, Makefile recipes, changed declarations, missing/orphan entries and job image digests.

All 185 timestamped Ubuntu fallback URLs were fetched and matched their original size and SHA-256. The HTTP-404 fallback and corrupt-download controls pass. Configuration identity is read from the exported manifest, and cold builds run with buildx v0.38.0. Patch self-tests pass without a configured global/system commit identity. A fresh-HOME SDK-link preflight resolves GCC 14.3.0 at the documented census location.

The reviewer-owned coverage ledger and verdicts must be refreshed for this head.

## Round 4

The reached-construct census was committed before implementation.
Positive command forms now include subcommands, arguments and executable paths.
Shell directory scope and Make file/default/pattern selection are explicit.
Python capability detection precedes keyword or alias decoding.
Unsupported forms refuse generation and comparison by name.

All 45 tool records, pins and workflow provenance remain identical.
The traversal now binds 328 inputs and locates all 269 residue entries.
Alternate Makefiles retain the invocation directory; shell functions retain local/global scope.
Literal dollar text cannot match a runtime argument allowance.
The original controls and new generation/comparison controls pass.
All 13 source gates and three Markdown checks pass.
Two cold builds match in manifest, configuration and all 14 layers.
Both exports authenticate against the generated lock.
All ten rebuilt-image checks and the final source gates pass.
The reviewer-owned coverage ledger and verdicts must be refreshed for this head.
