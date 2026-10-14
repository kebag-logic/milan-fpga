# CI tools image

The image supplies public, pinned validation tools.
Issue #737 owns its recipe and workflow adoption.
This lane supplies the image without changing workflows.

## Contents

- **[Inputs](#inputs)** -- Trace workflow requests to checked public sources.
- **[Rebuild](#rebuild)** -- Stage verified inputs and build offline.
- **[Identity](#identity)** -- Distinguish recipe identity from image identity.
- **[Smoke checks](#smoke-checks)** -- Exercise every installed tool family offline.
- **[CI and act adoption](#ci-and-act-adoption)** -- Select the published image by digest.

## Inputs

[`tool-inventory.json`](../../ci/image/tool-inventory.json) derives installation requests.
Each entry names its workflow, job and step.
[`ci_tool_inventory.py`](../../scripts/ci_tool_inventory.py) reads all workflow files.
It follows literal script references and local imports.
Unsupported installation commands refuse generation.
Changed requests and unused inventory entries fail comparison.

[`sources.lock.json`](../../ci/image/sources.lock.json) resolves those requests.
Every downloaded artifact carries its size and SHA-256.
The base image uses an immutable manifest digest.
Distribution packages include their complete resolved dependency closure.
Python wheels retain the repository's existing hash pins.
Git toolchains use checked archives at their workflow pins.
The existing LiteX patch series remains unchanged.
Unpinned package requests resolve to the source lock's versions.
Future repository updates require reviewing those resolved versions.
JavaScript actions require the runner's Node runtime.
The workflow selector also requires its GitHub CLI.
Those runtime tools have separate checked release layers.
The Markdown renderer uses Python packages, without Node modules.

Scala dependencies include the pinned CPU generator's requirements.
The launcher is 1.10.7; that project selects 1.10.0.
Both versions belong to the same installed toolchain.
Downloaded JARs and metadata have independent SHA-256 entries.
The image carries no host cache or credentials.

## Rebuild

Use Linux x86-64, Docker, BuildKit and Python 3.12.
Install PyYAML before invoking the inventory reader.
Choose disk storage outside the source checkout.
Allow eight compilation workers per native tool stage.

```sh
python3 scripts/ci_tool_inventory.py --check
python3 scripts/ci_tool_inventory_selftest.py
python3 ci/image/build_selftest.py
python3 ci/image/build.py --work "$IMAGE_WORK" --prepare-only
python3 ci/image/build.py --work "$IMAGE_WORK"
```

The preparation step downloads and verifies locked artifacts.
Existing downloads undergo the same size and hash checks.
Only explicitly selected recipe files enter the build context.
Docker builds run with networking disabled.
Each compiler invocation uses eight workers or fewer.

Individual stages can build separately when resources require it.

```sh
python3 ci/image/build.py --work "$IMAGE_WORK" --stage verilator-tools
python3 ci/image/build.py --work "$IMAGE_WORK" --stage yosys-tools
python3 ci/image/build.py --work "$IMAGE_WORK"
```

Stages retain their own source manifests and layers.
Build logs, timing receipts and cache exports use `IMAGE_WORK`.
The final receipt records image size and build time.
The build never logs in or pushes an image.
The context is rebuilt from the allowlist each time.
Old downloads cannot add unlisted packages to a layer.

## Identity

The recipe digest covers every installer and source lock.
It also covers the existing patch series and smoke checks.
A changed pin therefore produces a changed recipe digest.
The local image tag contains that recipe digest.

[`image.lock.json`](../../ci/image/image.lock.json) records the build result.
Each layer lists its tools, versions and source digests.
The lock also records the final image manifest digest.
The source lock and recipe remain necessary rebuild inputs.
An image digest identifies bytes; a tag does not.
Check that the lock still matches the current recipe.

```sh
python3 ci/image/build.py --work "$IMAGE_WORK" --check-lock
```

For a pin change, update the source lock first.
Record the public URL, exact version, size and SHA-256.
Preserve hashes required by the workflow's requirement files.
Refresh the derived inventory when workflow requests change.
Rebuild, rerun smoke checks and review the resulting lock.
The build generates `image.lock.json`; never edit its digest manually.

```sh
python3 scripts/ci_tool_inventory.py --write
python3 ci/image/build.py --work "$IMAGE_WORK"
```

## Smoke checks

Run the checks inside the produced image.
Mount writable scratch storage for their temporary builds.
Disable networking to expose missing dependencies.

```sh
mkdir -p "$IMAGE_WORK/smoke"
docker run --rm --network none \
  --mount "type=bind,src=$IMAGE_WORK/smoke,dst=/scratch" \
  "$IMAGE_REFERENCE" python3 /opt/ci-image/smoke.py --work /scratch
```

The checker verifies distribution and Python package versions.
It prints the native tools' version commands too.
Checks compile host programs, RV32 code and a simulation.
They exercise synthesis, conversion, unit tests and coverage.
Rendering, protocol generation and Scala compilation run as well.
These checks establish tool availability and basic operation.
Repository gates still establish product correctness.

## CI and act adoption

The manager publishes the reviewed image separately.
Consumers use its manifest digest from the image lock.
Configure the registry repository through `REGISTRY_IMAGE`.

```sh
digest=$(python3 -c 'import json; print(json.load(open("ci/image/image.lock.json"))["image_digest"])')
docker pull "$REGISTRY_IMAGE@$digest"
```

Hosted job containers and act must select that reference.
Their run manifests must record the same image digest.
Workflow adoption belongs to the separate #737 integration lane.
Existing hosted contexts and review requirements remain mandatory.
