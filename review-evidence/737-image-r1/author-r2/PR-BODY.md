[A615]

## Contents

- **[Status](#status)** - Implementation and validation state.
- **[Linked Issue / roles](#linked-issue--roles)** - Task and independent reviewers.
- **[Description](#description)** - Image recipe and verification changes.
- **[Authoritative references](#authoritative-references)** - Public decisions and repository contracts.
- **[How to get into the same state](#how-to-get-into-the-same-state)** - Checkout and prerequisites.
- **[How to validate](#how-to-validate)** - Reproduction and checks.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** - Adoption and review boundaries.
- **[Definition of Done](#definition-of-done)** - Remaining merge conditions.

## Status

REVIEW READY: the corrected `test_baremetal_profile_contract --require-rv32` campaign completed in the final image with rc 0 after 1,014,708 ms (1014.708 seconds), without a timeout. The home-relative compiler preflight passed with GCC 14.3.0. All 103 builder function invocations returned across nine groups; the existing `mf48` resource-calibration and inert `MAKEFLAGS += -e` mutation arms remain NOT RUN. The two identical cold builds stand. `737-ci-image` -> `dev`.

Head: `18f2df92b13cb3f4036b073ed76940187bf10487`.

## Linked Issue / roles

Relates to #737. This is the image implementation for PR #738.

Executor: `[A615]`
Internal cleared-context reviewer: `[R638]`
External reviewer: `[R639]`

## Description

The workflows currently reinstall their toolchains. This adds a pinned prebuilt tool image with a derived installation inventory, independently bound layers and an authenticated image lock. It preserves the existing firmware, linked images and product-test assertions.

The round-2 changes make cold builds reproducible, refuse ambiguous installation forms and distinguish recipe consistency from verification of the exported image. The privacy check authenticates each public upstream allowance, reproduces committed patch postimages and rejects protected identities added by a patch. The oracle contains its runtime libraries and protocol data; removing comment-only prose requires identical parsed data.

The package closure is generated from actual workflow requests and explicit consumers. Binary versions and offline functional smoke checks pass. The accepted runner version differences and every runtime environment setting are documented in the image guide.

## Authoritative references

- Issue #737 assignment, comment 6160953880.
- PR #738 round-2 ruling, comment 6162190578.
- PR #738 privacy ruling and patched-file refinement, comments 6162652582 and 6163057631.
- PR #738 background-run authorization and failure STOP condition, comment 6165220472.
- PR #738 setup correction and rerun ruling, comment 6166238176.
- [Contribution contract](CONTRIBUTING.md), [requirements](REQUIREMENTS.md) and [CI workflow policy](docs/testing/CI_WORKFLOWS.md).
- [Image guide](docs/testing/CI_IMAGE.md), including the independent runner-version comparison and generator commands.

## How to get into the same state

Checkout this head and initialize only the dependencies needed by the selected gates. Set `IMAGE_WORK` to persistent writable storage outside the checkout. Follow the image guide for Python, buildx and the pinned base export prerequisites.

```sh
git switch --detach 18f2df92b13cb3f4036b073ed76940187bf10487
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis third_party/tsn-c-stack
export IMAGE_WORK
python3 scripts/ci_tool_inventory.py --check
```

## How to validate

```sh
python3 ci/image/build_selftest.py
python3 ci/image/integrity_selftest.py
python3 ci/image/privacy_selftest.py
python3 ci/image/privacy_patch_selftest.py
python3 scripts/ci_tool_inventory_selftest.py
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest
python3 ci/image/build.py --work "$IMAGE_WORK" --no-cache --defer-lock
python3 ci/image/build.py --work "$IMAGE_WORK" --record-lock
python3 ci/image/build.py --work "$IMAGE_WORK" --check-lock --verify-archive "$IMAGE_WORK/image.tar"
IMAGE_REFERENCE=$(python3 -c 'import json,os; print(json.load(open(os.environ["IMAGE_WORK"]+"/validation-tools.receipt.json"))["tag"])')
docker run --rm --network none --mount "type=bind,src=$IMAGE_WORK,dst=/scratch" "$IMAGE_REFERENCE" python3 /opt/ci-image/smoke.py --work /scratch/smoke
```

Run a second cold build in a separate work directory as described in the guide. Expected result: all checks exit zero; the manifest, configuration and all 14 layer identities match. The current image is 3,931,041,388 bytes. Cold builds took 456,784 ms and 404,539 ms. Manifest: `sha256:8cc05a5c51aa04a23063c5d0593065912845a4ba4ce5a5dfd3ff53b12ccd1d19`.

The corrected compiler-backed campaign used the unchanged round-2 group driver with `--require-rv32`, the same environment and mounts, networking disabled and no timeout. `builder-home-preflight.json` records compiler availability; `builder-home-background.receipt.json` records the exact invocation, immutable image, rc 0, 1,014,708 ms wall time, and raw-log size/SHA-256. `builder-functions-1.json` records the returned function and its explicit inert-mutation skip. The evidence packet contains the full grouped coverage ledger.

## Known limitations / out of scope

- Builder evidence is grouped execution, not a monolithic builder invocation. The compiler-backed census and identity checks ran; the existing `MAKEFLAGS += -e` mutation was NOT RUN because it is inert with this make. The separate existing `mf48` resource-calibration arm remains NOT RUN because its Vivado build tree is absent; hosted CI takes the same skip.
- The earlier prerequisite failure is superseded by the authorized rerun with the exact round-2 HOME mapping, SDK symlink and mounts. No source change or new commit was made in this continuation.
- Reproducibility is demonstrated on the same host; cross-host identity is not claimed.
- Full workflow adoption acceptance belongs to lane 737-ci30's switch round, as assigned publicly.
- Publication, workflow switching, hosted checks, independent approval and merge remain outstanding. Nothing was pushed.
- Product firmware, linked images, existing patch contents and product-test assertions are unchanged.

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
