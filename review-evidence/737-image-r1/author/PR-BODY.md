[A615]

## Contents

- **[Status](#status)** -- Candidate and validation state.
- **[Linked Issue / roles](#linked-issue--roles)** -- Assignment and reviewers.
- **[Description](#description)** -- Image inputs, recipe and proof.
- **[Authoritative references](#authoritative-references)** -- Workflow and dependency contracts.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Rebuild commands.
- **[How to validate](#how-to-validate)** -- Checks and expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Pending integration work.
- **[Definition of Done](#definition-of-done)** -- Review and merge status.

## Status

REVIEW READY for the image lane: scoped image and documentation checks pass.
`737-ci-image` -> `dev`.
Head: `2b2e4d2c5b7f43cfc9df5347d99f9fee2c1fb895`.

## Linked Issue / roles

Relates to #737
Assignment: comment 6160953880.

Executor: `[A615]`
Internal cleared-context reviewer: `[R638]`
External reviewer: `[R639]`

## Description

CI currently repeats dependency installation and native compilation. This change supplies a prebuilt validation environment with a derived workflow inventory, checked public sources, separate tool layers and a generated image lock. The builder refuses pin mismatches and corrupted downloads, builds offline, and tags the result with the recipe digest.

The image occupies 3,989,528,152 bytes. The uncached native build took 393.856 seconds; the final recipe verification rebuild reused the same image bytes in 2.896 seconds. Every tool-family smoke check passed without networking. The pinned CPU generator also compiled offline in 72 seconds.

Image manifest: `sha256:94128cff4711ebfe6d3c5ac10bf88cdc9bac5caff4f4b28fc873fc83897d8427`.
Recipe: `aa3be31ce1924fac59d15ba2992f96561c5d8fb4c307c34b28568eae95b1a5fe`.

## Authoritative references

- #737, assignment comment 6160953880.
- `.github/workflows/` and their existing dependency pins.
- `tools/markdown/requirements.txt`, `tools/hdl_reference/requirements.txt` and `sw/litex/litex_pins.txt`.
- `scripts/ci_rv32_sdk.py` and `scripts/ci_litex_env.py`.
- `CONTRIBUTING.md` and `docs/testing/CI_IMAGE.md`.

## How to get into the same state

Provide `IMAGE_WORK` as writable disk storage outside the checkout. Use the documented build prerequisites.

```sh
git switch 737-ci-image
python3 scripts/ci_tool_inventory.py --check
python3 ci/image/build.py --work "$IMAGE_WORK" --prepare-only
python3 ci/image/build.py --work "$IMAGE_WORK"
```

## How to validate

Set `IMAGE_REFERENCE` to the produced image tag or manifest reference.

```sh
python3 scripts/ci_tool_inventory_selftest.py
python3 ci/image/build_selftest.py
python3 ci/image/build.py --work "$IMAGE_WORK" --check-lock
docker run --rm --network none   --mount "type=bind,src=$IMAGE_WORK,dst=/scratch"   "$IMAGE_REFERENCE" python3 /opt/ci-image/smoke.py --work /scratch/smoke
python3 scripts/docs_check.py
python3 scripts/check_doc_paths.py
python3 scripts/check_doc_style.py
python3 scripts/check_py_idiom.py
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --selftest
python3 scripts/check_em_dash.py --base fa7347fc
```

Expected result: every command exits 0; all image smoke families pass; changed or missing pins and corrupted inputs are refused. The documentation navigation controls passed 1,501/1,501 cases. Diagram and HDL-reference checks also passed inside the image.

## Known limitations / out of scope

- Publication and workflow adoption belong to the manager and integration lane.
- Hosted CI, independent reviews and merge validation remain pending.
- Unversioned workflow requests resolve to the explicit source lock. Independent cold-build byte identity across hosts was not tested.
- Full product regression campaigns were not rerun for this image-only change.

## Definition of Done

- [x] Image-lane acceptance criteria are satisfied
- [x] New behavior has self-checking tests
- [ ] Required integration verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
