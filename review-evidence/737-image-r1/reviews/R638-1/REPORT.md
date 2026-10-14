[R638] NEGATIVE - exact head 2b2e4d2c5b7f43cfc9df5347d99f9fee2c1fb895

# R638-1: internal cleared-context review of PR #738 (issue #737, image lane)

- Reviewer: [R638], internal independent reviewer, round R638-1.
- Exact head `2b2e4d2c5b7f43cfc9df5347d99f9fee2c1fb895`, tree `7c1b712df4047c428615db348ffbb59a05f51282`, source base `fa7347fc59173f90e4feec2df207692e6e6e72ec`.
- Diff reviewed: `fa7347fc..2b2e4d2c`, which is 13 files and 3 one-line commits with no trailers. No file under `.github/` changes (focus item 7 holds).
- Authorities: AGENTS.md, CONTRIBUTING.md and docs/README.md. The issue #737 body plus these A10 comments: the registry comment, the image-lane assignment 6160953880 and the signature design. The executor's TAKEN and REVIEW READY. The workflows `.github/workflows/{docs,elaborate,rtl-fast,rtl}.yml` and the scripts they call.
- Evidence read: the author's public gate receipts under `review-evidence/737-image-r1` at `efbda0ff` (MANIFEST plus build receipt and rebuild log), and the exact-head hosted check runs (read-only).
- Execution: I ran every probe myself on this host. The image was built twice from the exact-head recipe using a group-switched docker. I installed a checksum-verified buildx v0.38.0 plugin into a private client config inside this packet's scratch directory, because the host has no buildx plugin. Nothing was pushed, and there was no login, no registry pull and no act.
- No manager source bank ran at this head, and none is claimed. Physical calibration was NOT RUN.

## Verdict summary

The tool inventory derivation, the checksum pinning, the offline build and the offline smoke all work at this head. Every repository gate I ran inside the locked image passes, with one exception.

Five properties the assignment requires do not hold:

- **F1 (BLOCKER).** A required gate is red at this exact head. The Bare-metal scope gate fails, both hosted and locally.
- **F2 (MAJOR).** The image is not reproducible. A no-cache rebuild of the same recipe gives a different digest, and all 14 recipe layers differ.
- **F3 (MAJOR).** Regenerating the inventory silently omits several common installation forms, and the docs say such forms are refused.
- **F4 (MAJOR).** Several tool versions differ from what the hosted workflows get today, and the smoke proof only compares the image with its own lock.
- **F5 (MINOR).** A published layer carries a developer home-directory path and an account name.

Five further MINOR findings, one RESIDUE and three SUGGESTIONs follow.

## Findings

### F1 BLOCKER: the Bare-metal scope gate fails at this exact head

- **Lenses:** Conformance, Tests, Docs.
- **Where:**
  - `ci/image/sources.lock.json` (30 hits, e.g. `:125`, `:1365`, `:1717`, `:6759`);
  - `ci/image/image.lock.json` (9 hits, e.g. `:33`, `:88`);
  - `docs/testing/CI_IMAGE.md:46`.
- **Authority/evidence:**
  - Hosted `docs-check` at the exact head concluded `failure`. Step 23, "Bare-metal scope gate", failed and steps 24-51 were skipped. See `receipts/exact-head-check-runs.txt` and `receipts/exact-head-docs-check-steps.txt`, job 115702279596.
  - Locally, `python3 scripts/check_baremetal_only.py --check` at this head returns rc 1 with `baremetal-only: FAIL (40 finding(s) across 1298 scanned file(s))`. All 40 hits are retired-stack term `linux` in the three new files (`receipts/baremetal-check.log`).
  - The same gate on the base tree returns rc 0 with 0 findings (`receipts/baremetal-check-base.log`).
  - REVIEW READY reports "All 13 repository gate commands passed" but did not run this gate.
- **Impact:**
  - A protected required context is red, so the PR cannot merge.
  - The lane's validation evidence omits a gate that the docs workflow runs on every change.
- **Required outcome:** the gate passes at the head. Do this either by changing the new files' wording, or through a public, gate-owned exemption decision for generated lock data. The author's validation list must include the docs-check gate set.
- **Verification:** `python3 scripts/check_baremetal_only.py --check` and `--selftest` exit 0 at the new head, and hosted `docs-check` succeeds.

### F2 MAJOR: the build is not reproducible

- **Finding:** a rebuild from the same recipe yields different image bytes.
- **Lenses:** Conformance, Robustness, Tests, Docs.
- **Where:**
  - `ci/image/build.py:215-218`: no `SOURCE_DATE_EPOCH`, no timestamp rewriting and no normalisation step;
  - `ci/image/Dockerfile:1-8` and `:10-15`: package logs and caches stay in the layer;
  - `ci/image/install.py:94-118`: bytecode is compiled at install time;
  - `ci/image/install.py:121-131`: the build tree and its configure log are kept;
  - the REVIEW READY and PR body claim the "same image bytes".
- **Authority:** focus item 3 and assignment item 2: "a build script that builds the image reproducibly".
- **Evidence:**
  - The normal `build.py` run on this host reproduced the lock digest `sha256:94128cff…8427`, but only from BuildKit cache (`receipts/build-cached.log`, 8.7 s).
  - The same recipe built with `--no-cache` produced `sha256:81b035e8…75ab`, size 3,989,549,585 instead of 3,989,528,152 bytes (`receipts/build-nocache.log`, `receipts/layer-compare.txt`). The recipe digest `aa3be31c…5fe` is identical in both runs.
  - The base layer is identical; all 14 recipe layers differ.
  - Member-level diff (`receipts/layer-member-diff.jsonl`):
    - every layer has file mtime differences, including the `COPY` of `smoke.py` and `WORKDIR`;
    - the content differs in `var/log/{dpkg,alternatives}.log`, `var/log/apt/*`, `var/cache/fontconfig/*`, `var/cache/ldconfig/aux-cache` and `etc/ssl/certs/java/cacerts`;
    - 2,300 `.pyc` files differ;
    - `opt/yosys/bin/yosys-abc` and `opt/tsn-gen/build/CMakeFiles/CMakeConfigureLog.yaml` differ.
  - Verilator's version string embeds the build date (`rev vUNKNOWN-built20261014`, `receipts/smoke-locked-versions.txt`), so a rebuild on another day differs again.
  - The author's "final recipe verification rebuild producing the same image bytes" (2.896 s) was a cache hit, not a rebuild.
- **Impact:**
  - Nobody can rebuild the published digest from the committed recipe.
  - The signature design's "the same image ran" therefore rests only on trusting the one build that was pushed.
  - A rebuild after a cache loss silently produces a new digest that the lock does not record.
- **Required outcome:** one of two.
  - A no-cache rebuild from the committed recipe reproduces the locked image digest, at least on the same host, with cross-host status stated.
  - Or a public owner decision replaces bit-reproducibility with a weaker documented property, and the docs and PR claims say exactly what is reproduced.
- **Verification:** run `build.py` with BuildKit cache disabled (e.g. `scripts/docker-nocache.sh` in this packet as `--docker-command`) and get `image_digest` equal to `ci/image/image.lock.json`. `scripts/oci_layers.py diff` reports no difference.

### F3 MAJOR: regenerating the inventory silently omits real installation forms

- **Lenses:** Conformance, Robustness, Tests, Docs.
- **Where:**
  - `scripts/ci_tool_inventory.py:26`: `PATH_WORD` never follows Makefiles;
  - `:156-157`: the refusal regex lacks `pipx`;
  - `:196-207`: only list-literal subprocess calls are inspected;
  - `:238-245`: of the `uses:` actions, only `actions/setup-python` yields a tool pin;
  - `docs/testing/CI_IMAGE.md:21`: "Unsupported installation commands refuse generation."
- **Authority:** focus item 1 and assignment item 1: "A check fails when a workflow installs a tool the inventory lacks".
- **Evidence:**
  - At this head the derived inventory is complete. A repository-wide search found no installation outside the parsed forms.
  - All 10 planted refusal controls on the real tree exit 2 (`receipts/inventory-controls.jsonl`): added apt tool, removed tool leaving an orphan, changed pip pin, changed archive sha, changed Verilator pin, changed requirement hash, changed LiteX pin, list-form pip in a called script, pip in a called shell script, and an orphan inventory entry.
  - `--check` compares the whole text, input digests included, so any edit to a followed file trips it. The meaningful test is what `--write` records.
  - Five planted forms are accepted by `--write` (rc 0), absent from `tools`, then pass `--check` and `validate_pins` (`receipts/inventory-write-gaps.jsonl`):
    - `actions/setup-java@v4` with `java-version: '21'`;
    - `pipx install` in a workflow `run`;
    - `pip install` in a Makefile recipe of a suite that the workflows run;
    - `subprocess.run("pip install …", shell=True)` in a followed script;
    - `os.system("apt-get install …")`.
  - The setup-java case is the standard GitHub install mechanism. The image keeps OpenJDK 17 while that workflow would get 21, and nothing fails.
- **Impact:**
  - The guard fails open on drift it claims to refuse.
  - After the switch to the image, such a workflow change would run on a tool the image lacks or pins differently.
- **Required outcome:**
  - Every `uses:` action that installs a toolchain (`actions/setup-*`, or any non-checkout/cache/artifact action) either yields an inventory entry with its version or is refused.
  - Installation-shaped strings in followed scripts, and Makefiles reached from workflow steps, are either parsed or refused.
  - The docs claim matches the behaviour.
- **Verification:** `scripts/inventory_write_gaps.py <tree> <scratch>` reports REFUSED or RECORDED for all six probes. The repository self-test includes at least the setup-action and Makefile controls.

### F4 MAJOR: image tool versions differ from what the hosted workflows get today

- **Finding:** several image tool versions differ from the hosted ones, and the proof is circular.
- **Lenses:** Conformance, Tests, Docs.
- **Where:**
  - `ci/image/sources.lock.json` (packages `git`, `cmake`, `ninja-build`, `openjdk-17-*`, `python3.12`);
  - `ci/image/build.py:59-61`: `"3.12"` is accepted as equal to `3.12.3`;
  - `ci/image/smoke.py:25-48`: versions are checked against the lock only;
  - `docs/testing/CI_IMAGE.md:31`.
- **Authority:** assignment item 3, "The tool versions must match exactly what the workflows install today", and focus item 4.
- **Evidence** (`receipts/hosted-tool-versions.txt`, `receipts/runner-ubuntu2404-20261004.327-readme.md`, `receipts/smoke-locked-versions.txt`). The hosted values come from the runner image ubuntu-24.04 20261004.327.1 used by the #737 baseline runs. The table compares what the hosted runner provides today with what the image provides.

| Tool | Hosted today | Image |
|---|---|---|
| `git` (an inventory tool; the workflows `apt-get install git`) | 2.55.0 | 2.43.0 |
| elaborate's `actions/setup-python` `python-version: '3.12'` | CPython 3.12.15 | 3.12.3 |
| CMake (builds the tsn-gen oracle) | 3.31.6 | 3.28.3 |
| Ninja | 1.13.2 | 1.11.1 |
| Java | Temurin 17.0.20+1 | Ubuntu OpenJDK 17.0.20.1 |
| Verilator version string | `rev v5.050` | `rev vUNKNOWN-built20261014` |

  - Node 22.23.3, gh 2.102.0, Clang 18.1.3 and the system Python 3.12.3 do match the runner.
  - The smoke `versions()` asserts only that installed packages equal the source lock, so it cannot detect any of these differences.
  - The owner's registry comment names "Python 3.12.3", which conflicts with elaborate's `3.12`, which resolves to 3.12.15. That conflict is encoded in `build.py:60` but not published for a decision. AGENTS section 2 requires publishing it.
- **Impact:**
  - Adopting the image changes git, CMake, Ninja, Java and elaborate's CPython under every job.
  - The proof that versions "match exactly" is not established by the evidence offered.
- **Required outcome:** one of the following.
  - The image matches the hosted versions for tools the workflows install or rely on.
  - Or each deviation is listed publicly and accepted by a recorded owner decision, with the Python 3.12 vs 3.12.3 conflict decided explicitly.
  - Either way, the proof compares the image against an independent record of the hosted versions, not against its own lock.
- **Verification:** a version table of hosted job log or runner manifest against the image output, with no unexplained difference, and the decision linked on #737.

### F5 MINOR: privacy, a host path and account name in a published layer

- **Finding:** the tsn-gen layer carries a developer home-directory path and account name. It also ships build-tree leftovers, and the recipe has no privacy check.
- **Lenses:** Conformance, Tests.
- **Where:**
  - `ci/image/install.py:121-131`: the whole tsn-gen source and build tree is copied into `/opt/tsn-gen`;
  - image layer 10 (`COPY /opt/tsn-gen`), member `opt/tsn-gen/traffic-gen/tests/aecp_behave/__pycache__/environment.cpython-314.pyc`.
- **Authority:**
  - Focus item 5: no host path, account name or identity in any layer.
  - The registry comment: "no private dependency, host path or identity".
- **Evidence:**
  - The member embeds an absolute developer home-directory source path (`/home/<account>/prjs/…`; the account name is redacted here).
  - It is byte-identical (sha256 `061af518…ea5a`) to a `.pyc` committed in the public upstream `kebag-logic/tsn-gen@deca300c`, so it adds no new exposure. It still violates the rule as written (`receipts/tsn-gen-stray-pyc.txt`, `receipts/privacy-scan-locked.jsonl`).
  - The same layer ships `build/CMakeCache.txt` and `build/CMakeFiles/CMakeConfigureLog.yaml`. These are build leftovers with container paths only.
  - The rest of my scan found no host path, build-host account, credential, token or build-context leftover in any layer, label, history entry or environment variable. Scan inputs: `docker history --no-trunc`, the config and every layer of the locked image. The remaining pattern matches are upstream copyright addresses, documentation examples and binary constants.
  - Neither the recipe nor the smoke runs a privacy scan.
- **Impact:** an image intended for a public registry carries an account-identifying path whose presence nobody chose. Nothing would catch the next one.
- **Required outcome:**
  - The published layers contain no host path or account name: ship only what the oracle needs, or drop stray bytecode and build logs.
  - A recipe-owned check refuses such strings.
- **Verification:** `scripts/oci_layers.py scan <saved image> '/home/(?!ubuntu)[a-z]+' …` reports no match from the tsn-gen layer, and the recipe's own check has a planted-path control.

### F6 MINOR: layer mapping

- **Finding:** Python and LiteX share one image layer, and the lock's layers are not bound to the image's layers.
- **Lenses:** Conformance, Docs.
- **Where:**
  - `ci/image/Dockerfile:82` (`COPY --from=litex-tools /opt/python /opt/python`);
  - `ci/image/build.py:231-237`;
  - `ci/image/image.lock.json` (`layers`);
  - `docs/testing/CI_IMAGE.md:88`.
- **Authority:**
  - Focus item 2 and assignment item 2: "one layer per tool".
  - The registry comment, which lists LiteX and Python as separate layers, each "tagged with its exact version and source/recipe digest".
- **Evidence:**
  - The image has 15 layers (`receipts/locked-image-layers.txt`), and the Python packages and LiteX are one `COPY /opt/python` layer (122 MB).
  - The lock lists `python` and `litex` as two layers.
  - No lock entry records an OCI layer digest.
  - The `system` layer holds 211 distribution packages, among them several workflow tools: the compilers, git, make, Java, CMake and Tcl.
  - Every layer's `recipe_digest` is the single global recipe digest.
- **Impact:** a consumer or the signature manifest cannot verify which image layer carries which tool. Changing LiteX re-ships the Python layer.
- **Required outcome:** LiteX has its own layer, or the docs and assignment state the grouping by public decision. The lock binds each logical layer to its OCI layer digest.
- **Verification:** inspect the image's `RootFS.Layers` against `image.lock.json`.

### F7 MINOR: undocumented, non-derived environment defaults change job behaviour

- **Lenses:** Conformance, Docs.
- **Where:** `ci/image/Dockerfile:95` (`ENV VERILATOR_JOBS=2`), with `MILAN_RV32_CC`, `TSN_GEN_ROOT`, `COURSIER_CACHE` and `SBT_OPTS` alongside it at `:92-97`. `docs/testing/CI_IMAGE.md` documents none of them.
- **Authority:** assignment item 1: derived from the workflows, not a hand choice. Fidelity requirement: the image changes no job's behaviour beyond the tool provision.
- **Evidence:**
  - No workflow sets `VERILATOR_JOBS=2`; `rtl.yml:376` sets 4.
  - Nine Makefiles default it with `?= 0` or `?= 16`, and `sw/litex/milan_sim.py:146` reads it.
  - The image value overrides all of these wherever a job does not set it.
- **Impact:** after adoption, Verilator compile fan-out drops to 2 in jobs that rely on the default. That affects the 30-minute budget the parent issue measures. The change is invisible in the docs.
- **Required outcome:** remove `VERILATOR_JOBS` from the image, or derive and document it, and document every image `ENV`.
- **Verification:** `docker image inspect` Env, compared with the CI_IMAGE.md table.

### F8 MINOR: the VexiiRiscv layer is not the workflow's tree

- **Finding:** the image's VexiiRiscv tree is not the one the workflows build, and the workflow's own placement step fails against it.
- **Lenses:** Conformance, Robustness, Docs.
- **Where:**
  - `ci/image/install.py:114-116`, which unpacks only `SpinalHDL` and `rvls` and creates no `.git`;
  - `scripts/ci_litex_env.py:96-105`;
  - `docs/testing/CI_IMAGE.md:29` ("Git toolchains use checked archives at their workflow pins").
- **Evidence:**
  - The workflow runs `git submodule update --init --recursive` at the pin. That also populates `ext/NaxSoftware`, `ext/riscv-isa-sim` and SpinalHDL's `tester/.../cocotblib`, verified from the upstream trees.
  - In the image, `NaxSoftware` and `riscv-isa-sim` are empty.
  - Running `python3 scripts/ci_litex_env.py` in the image, offline, fails: `fatal: destination path … already exists and is not an empty directory`, `place_rc=1`. `--check` passes (`receipts/litex-env-in-image.log`).
- **Impact:** the workflow step "Place the VexiiRiscv source at the revision LiteX pins" cannot run on the image unchanged. The difference from the hosted closure is undocumented.
- **Required outcome:** make the image tree what the step expects, or document the difference and the adoption change it forces.
- **Verification:** `ci_litex_env.py` exits 0 offline in the image, or CI_IMAGE.md records the decision.

### F9 MINOR: the cold `--prepare-only` race fails on duplicate staged filenames

- **Lenses:** Robustness, Tests.
- **Where:**
  - `ci/image/build.py:107-120` (shared `.part` path);
  - `:152-155` (4-thread pool);
  - `ci/image/sources.lock.json`: two pairs of `sbt-assembly` rows share `maven/14622420…-sbt-assembly.jar` and `maven/00d3a88d…-ivy.xml`.
- **Evidence:**
  - My first cold `--prepare-only` failed with `FileNotFoundError … sbt-assembly.jar.part` (`receipts/prepare-w1-first-cold.log`), and a retry passed.
  - A deterministic probe fails 10 of 10 times (`receipts/prepare-race-probe.txt`, `scripts/prepare_race_probe.py`).
  - `scripts/dup_filenames.py` lists the pairs.
  - The failure is closed (hashes are verified), but the documented first step fails nondeterministically on a clean machine. No self-test covers duplicate rows.
- **Required outcome:** downloads are deduplicated by target or use unique temporary names, and a self-test covers duplicate rows.
- **Verification:** `prepare_race_probe.py` reports 10 passes. A cold `--prepare-only` in an empty work directory passes repeatedly.

### F10 MINOR: the source lock's distribution roots are a hand list with no generator

- **Lenses:** Conformance, Docs.
- **Where:** `ci/image/sources.lock.json` (`packages`, 214 rows; maven, 423 rows; `sbt_boot`, 88 rows) and `docs/testing/CI_IMAGE.md:98-103`.
- **Authority:** assignment item 1: "no hand list".
- **Evidence:**
  - 68 locked packages lie outside the dependency closure of the 18 derived apt requests (`receipts/lock-hand-roots.txt`).
  - They hang from 20 hand-chosen roots: `automake`, `build-essential`, `clang`, `cmake`, `curl`, `libbz2-dev`, `libffi-dev`, `liblzma-dev`, `libreadline-dev`, `libsqlite3-dev`, `libssl-dev`, `locales`, `ninja-build`, `openjdk-17-jdk-headless`, `python3-dev`, `python3-pip`, `python3-venv`, `time`, `unzip`, `uuid-dev`.
  - Some are used by workflow steps without being installed, for example Java for sbt and CMake for the oracle. Others have no consumer I could find: `automake` and `ninja-build` appear in no workflow, script or Makefile.
  - No committed tool resolves the dependency closure or the maven/boot sets. The documented pin-change procedure ("Record the public URL, exact version, size and SHA-256") is therefore manual for hundreds of rows.
- **Impact:** image content is not derived or checked, so unused tools persist. A pin change cannot be reproduced by a second person.
- **Required outcome:**
  - The runner-provided tool set is derived from the workflow and script usage, or listed with its reason and checked for use.
  - The lock's closure generator is committed, or the manual procedure is documented in full.
- **Verification:** a checker refuses a locked root that has no consumer, with a planted control, and the regeneration reproduces `sources.lock.json`.

### R1 RESIDUE: the rebuild prerequisites are incomplete

- **Where:** `docs/testing/CI_IMAGE.md:46`.
- **Problem:** `build.py` invokes `docker buildx build … --cache-to type=local`, but this host's docker has no buildx plugin (`docker: unknown command: docker buildx`).
- **Exact fix:** after "Use Linux x86-64, Docker, BuildKit and Python 3.12.", add "Install the Docker buildx plugin; local cache export needs the containerd image store or a docker-container builder." Line 46's word "Linux" also needs the F1 change.

### Suggestions (do not affect the verdict)

- **S1.** `tool-inventory.json` hashes about 290 followed scripts, so any edit to a mutant or test script fails `--check` until someone runs `--write`. Consider separating the input-digest provenance from the tool list that the drift test protects.
- **S2.** `/opt/rv32-sdk` keeps the archive's owner, uid/gid 1000:1000, on 5,287 files (`receipts/privacy-scan-locked.jsonl`). That uid is the base image's `ubuntu` user. Normalise the owner to root.
- **S3.** Use a per-layer recipe digest (that layer's installer plus its lock slice) instead of one global digest. That gives each layer a real cache key, which is what the registry comment describes.

## Acceptance check against the assignment and focus

| Item | Result | Evidence |
|---|---|---|
| (1) Inventory derived; the check fails on missing or unused entries | Partly. Derivation is complete at this head and 10 of 10 refusal controls pass. Regeneration fails open for 5 forms (F3); the lock's extra roots are hand-listed (F10). | `receipts/inventory-controls.jsonl`, `receipts/inventory-write-gaps.jsonl`, `receipts/lock-hand-roots.txt` |
| (2) Multi-stage, one layer per tool, base pinned by digest, exact versions, verified checksums | Base pinned by digest, and every source and deb is size- and sha256-checked at prepare and again in the build. Submodule pins equal the upstream gitlinks for yosys v0.66, tsn-gen, rapidyaml, c4core and VexiiRiscv. Python and LiteX share a layer (F6). | `ci/image/install.py:29-37`, `ci/image/Dockerfile:3-6` |
| (3) Reproducible build; lock content | Not reproducible (F2). The lock carries the per-layer tool, version and source digest, the recipe digest and the image digest. | `receipts/layer-compare.txt`, `receipts/layer-member-diff.jsonl` |
| (4) Versions equal today's workflow installs; smoke passes offline | Smoke passes offline with `--network none`, rc 0 in 29 s. Several versions differ from hosted (F4). | `receipts/smoke-locked-offline.log`, `receipts/hosted-tool-versions.txt` |
| (5) Privacy | One account path through an upstream file, plus build leftovers (F5). History, labels, Env and layers are otherwise clean. | `receipts/privacy-scan-locked.jsonl`, `receipts/layer-toplevel-locked.jsonl`, `receipts/history-locked-image.txt` |
| (6) CI_IMAGE.md accurate | The refusal claim is wrong (F3), rebuild reproducibility is implied but false (F2), prerequisites are incomplete (R1), image ENV is undocumented (F7), and the VexiiRiscv difference is undocumented (F8). Pin changes do change the recipe digest (self-test passes), and pull-by-digest wording is consistent. | `docs/testing/CI_IMAGE.md` |
| (7) No workflow file changed | Holds: zero paths under `.github/`. | `git diff --name-only fa7347fc..2b2e4d2c -- .github` |

Other executed evidence:

- Inside the locked image, offline, with the clone mounted read-only, these exit 0 (`receipts/repo-gates-in-image.log`):
  - `docs_check.py`, `check_doc_paths.py`, `check_doc_style.py` and `check_py_idiom.py`;
  - `gen_toc.py --check` and `gen_toc.py --verify-anchors`;
  - `check_em_dash.py --base fa7347fc` (146 added lines, 0 findings);
  - `ci_tool_inventory.py --check`, `ci_tool_inventory_selftest.py` and `build_selftest.py`.
- PyYAML, behave and the unpinned dependency wheels equal today's latest PyPI releases. pycparser 3.0 and pyslang 11.0.0 differ from latest but are hash-pinned by the repository, which is correct (`receipts/pypi-latest.txt`).
- Uncached build wall time on this host: 448 s (`build_ms` 445,661); the author reported 393.856 s.

## Clean lens

[R638] PASS RTL — `ci/image/install.py:54-73`, `ci/image/Dockerfile:31-41`, against `.github/workflows/rtl-fast.yml:155-180`, `rtl.yml:240-267` and `elaborate.yml:280-293`, plus the locked image's smoke run.

- No HDL, testbench or synthesis source changed in `fa7347fc..2b2e4d2c`.
- Verilator is built as the workflows build it (`autoconf`, `./configure --prefix=/opt/verilator`, `make`, `make install`).
- Yosys is built as the workflows build it (`config-gcc`, then `ENABLE_TCL/READLINE/PLUGINS := 0`, `PREFIX=/opt/yosys`), with abc `5d51a5e4` and cxxopts `4bf61f08` equal to the yosys v0.66 gitlinks.
- In the image, offline, a `--binary --assert` Verilator model ran, and sv2v → Yosys `synth` + `abc` + `check -assert` passed (`receipts/smoke-locked-offline.log`).
- The Verilator version-string difference is recorded under F4 (Conformance/Tests), not as an RTL defect.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3, F4, F5, F6, F7, F8, F10) | assignment and registry comments; `scripts/ci_tool_inventory.py`; `ci/image/{Dockerfile,build.py,install.py,smoke.py,sources.lock.json,image.lock.json,tool-inventory.json}`; workflows; hosted logs; both built images | R638-1 | 2b2e4d2c5b7f43cfc9df5347d99f9fee2c1fb895 |
| RTL | CLEAN | Verilator and Yosys recipe vs the workflow build steps; submodule gitlinks; offline simulation and synthesis smoke | R638-1 | 2b2e4d2c5b7f43cfc9df5347d99f9fee2c1fb895 |
| Robustness | UNCLEAN (F2, F3, F8, F9) | cold and warm prepare; duplicate-row race probe; regeneration gap probes; no-cache rebuild; in-image workflow placement step | R638-1 | 2b2e4d2c5b7f43cfc9df5347d99f9fee2c1fb895 |
| Tests | UNCLEAN (F1, F2, F3, F4, F5, F9) | `scripts/ci_tool_inventory_selftest.py`; `ci/image/build_selftest.py`; `ci/image/smoke.py`; author gate receipts; my planted controls | R638-1 | 2b2e4d2c5b7f43cfc9df5347d99f9fee2c1fb895 |
| Docs | UNCLEAN (F1, F2, F3, F4, F6, F7, F8, F10; R1 residue) | `docs/testing/CI_IMAGE.md`; `docs/README.md:88`; PR body; REVIEW READY | R638-1 | 2b2e4d2c5b7f43cfc9df5347d99f9fee2c1fb895 |

## Real limits

- **Same-host check only.** Reproducibility was tested on one host and one daemon: a cached build and a no-cache build. A cross-host cold build was not attempted, and F2 already fails on the same host.
- **Different builder plugin.** I used buildx v0.38.0 from a private client config; the author's plugin version is unknown. The member diff attributes every difference to mtimes, logs, caches and bytecode, not to the builder.
- **No registry round-trip.** Nothing was pushed or pulled from a registry, so the claim that the registry serves the lock's `image_digest` after push is unverified.
- **CPU generator not re-run.** I did not re-run the author's offline VexiiRiscv Scala generation (72 s receipt). My sbt coverage is the smoke's offline sbt 1.10.0 project.
- **Hosted versions from older runs.** The hosted versions come from the #737 baseline runs at `7032bca5` on runner image 20261004.327.1, plus the runner manifest at that tag. They are not from a run at this head; the exact-head runs were still in progress for the Verilator shards and elaborate when read.
- **No product regression or hardware.** I ran no product regression, no act, no hardware and no physical calibration.
- **Pre-existing tags.** The image tags `fpga-validation:*` already existed in the shared daemon. I added and then removed only my own tags; the BuildKit cache from my no-cache build remains in the daemon.
- **Clone untouched.** Probes ran on archive copies under this packet's scratch directory and in a disposable build work directory outside the clone. The review clone is byte-identical to the head: worktree and index clean, index hash equals the HEAD tree hash, and the submodule gitlinks are unchanged (`receipts/clone-integrity.txt`).
- **Prior findings.** No prior public review findings existed on PR #738 when this round began.

## Pending manager duties

- Hosted and act acceptance at the eventual head, including `docs-check`, which is red at this head (F1).
- Current-dev merge-candidate validation: source base `fa7347fc`, live dev `fa8209889411e8ca95757174c981f720dbcd95a2`.
- Image publication by digest, but only after F2 is resolved or the reproducibility property is redefined by owner decision.
- Owner decisions requested by F4 (Python 3.12 vs 3.12.3 and the runner-tool deviations) and, if chosen, by F6.
- Carry RESIDUE R1 to the residue checklist.

## Publishable files

Every published receipt and script is listed in `MANIFEST.sha256`. The scripts are portable: the docker wrappers read an optional `DOCKER_PREFIX`, and the probes take the tree and scratch paths as arguments. During this run the wrappers used a local group-switch prefix. In `receipts/privacy-scan-locked.jsonl`, one developer account name and this host's name are redacted, as stated in its first line.

R638-1 FINISHED
