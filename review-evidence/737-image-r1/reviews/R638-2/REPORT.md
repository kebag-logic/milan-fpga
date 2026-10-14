[R638] NEGATIVE - exact head 18f2df92b13cb3f4036b073ed76940187bf10487

# R638-2: internal cleared-context review of PR #738 (issue #737, image lane), round 2

- Reviewer: [R638], internal independent reviewer, round R638-2 (re-queued after the voided run; nothing from the voided run was read or reused).
- Exact head `18f2df92b13cb3f4036b073ed76940187bf10487`, tree `21c293548a85cfb4a9bd7dfd7c1e990c103d18bd`, source base `fa7347fc59173f90e4feec2df207692e6e6e72ec`, live dev `fa8209889411e8ca95757174c981f720dbcd95a2`.
- Diff: `fa7347fc..18f2df92`, 28 files, 11 one-line commits; round-2 delta `2b2e4d2c..18f2df92`, 26 files. Zero paths under `.github/` (ruling d holds).
- Authorities read: AGENTS.md, CONTRIBUTING.md, docs/README.md; issue #737 body and the A10 comments (registry 6160859632, assignment 6160953880, scope change 6166823105); PR #738 round-2 assignment 6162190578 and rulings 6162652582, 6163057631, 6165220472, 6166238176; the author's TAKEN/STOP/REVIEW READY comments; the four workflows and the scripts they call; the public evidence tree at `faf4ddda`.
- Independence: my findings were recorded (`receipts/independent-findings-before-prior.txt`) before I read R638-1 and R639-1. I did not read any other round-2 review.
- No manager source bank ran at this head and none is claimed. Physical calibration NOT RUN.

## Verdict summary

Round 2 closed almost every round-1 finding at its cause, and I reproduced the central claims independently:

- **Reproducible.** My own no-cache rebuild of the exact-head recipe, about 11 hours after the author's builds and with a different buildx client, exported manifest `sha256:8cc05a5c…1d19` and config `sha256:1eac3b02…0b9b`. Both equal the lock. The only cached step was the base-image resolve (`receipts/reviewer-cold-rebuild.txt`).
- **Lock bound to bytes.** `build.py --check-lock --verify-archive` on the daemon's final image passes. It used my own independently downloaded and verified sources, and it bound all 14 layer digests and diff-ids plus the manifest and config (`receipts/verify-archive.log`).
- **Privacy.** The recipe's scan passes, with 526 provenance allowances, one of them a reproduced patched `Soc.scala`. My separate scan found zero hits for every build-host, author, manager, registry-owner and owner-associated identifier, in contents, member metadata, history, labels and Env (`receipts/reviewer-image-scan-summary.json`).
- **Offline smoke and versions.** The offline smoke passes (rc 0, `--network none`). Binary versions equal the workflow pins, and the deviation table equals the runner manifest 20261004.327.1.
- **Grouped builder evidence.** It covers all 103 functions exactly once at the head source hash `997e8528…`, with `--require-rv32`.
- **MAKEFLAGS skip.** The image's skip of the `MAKEFLAGS += -e` arm is the same skip the hosted docs-check takes at live dev.

Five defects remain open, one MAJOR and four MINOR, so the verdict is NEGATIVE:

- **R638-2-F1 (MAJOR).** Inventory regeneration still drops ten ordinary installation forms silently. These include job `container:`/`services:` images, the mechanism the switch lane will use.
- **R638-2-F2 (MINOR).** 93 of the 185 locked Ubuntu URLs point at update-pocket versions. The archive deletes those once superseded, so the recipe stops rebuilding from its own lock.
- **R638-2-F3 (MINOR).** `build.py` depends on a buildx metadata key that the current buildx release (v0.38.0) no longer emits. The build then crashes with an uncaught `KeyError` after a successful build. The doc does not pin buildx.
- **R638-2-F4 (MINOR).** `privacy_patch_selftest.py` fails (rc 1) wherever no git identity is configured, including inside the image itself.
- **R638-2-F5 (MINOR).** The guide omits the RV32 SDK location that the existing census and workflows require. The author's own campaign needed an undocumented HOME mapping and symlink. The guide also names the wrong consumer for `MILAN_RV32_CC`.

## Findings

### R638-2-F1 MAJOR: regenerating the inventory still drops installation forms silently

- **Lenses:** Conformance, Robustness, Tests, Docs.
- **Where:**
  - `scripts/ci_tool_inventory.py:27-29`: `INSTALL_WORD` lists only pip/pipx/npm/pnpm/yarn/apt/apt-get/dnf/apk/cargo/gem/brew/conda.
  - `:106-158`: `shell_installs` recognises nothing else.
  - `:265-309`: `derive` reads only `steps`, never a job's `container:` or `services:`.
  - `docs/testing/CI_IMAGE.md:25-27`: "Unknown installers and unsupported installation actions refuse generation."
- **Authority:**
  - Assignment 6160953880 item 1: "A check fails when a workflow installs a tool the inventory lacks".
  - Round-2 required outcome 2 (6162190578): "refuse any unresolved installation form, so regenerating the inventory can never drop an installation silently".
- **Evidence:** `scripts/inventory_probes.py` produced `receipts/inventory-probes.json`. Each form was planted in a disposable `git archive` copy of the head, and the deriver ran with `--root`. The controls behave correctly:
  - a planted `apt-get install` is LISTED;
  - an orphan inventory entry is DETECTED;
  - all seven round-1 forms are now REFUSED (`receipts/prior-findings-probes.json`).

  These ten forms pass `--write` with rc 0, and the planted tool is absent from `tools` (SILENT):
  - `sudo dpkg -i …deb`;
  - `npx --yes tool@1.2.3`;
  - `go install …@v1.0.0`;
  - `sudo snap install`;
  - `uv tool install`;
  - `docker run image:tag`;
  - `git -C … fetch https://…`;
  - a followed Python script that downloads with `urllib.request.urlretrieve`;
  - a job-level `container:` image;
  - a job-level `services:` image.

  At this head the derived inventory is still complete: no workflow uses any of these forms, and the followed scripts' `curl`/`urlopen` hits are data or the named SDK installer.
- **Impact:**
  - After a workflow edit, `--check` fails because the input digests change. The documented remedy, `--write`, then blesses an inventory without the new tool, and `--check` passes.
  - The `container:` gap matters most: the switch lane will add exactly that construct, and the inventory will not see the image the jobs run in.
  - The guide's refusal claim is false for these forms.
- **Required outcome:** regeneration either records or refuses each of the ten forms. It must at least handle job `container:`/`services:` images, non-allowlisted package managers and package-file installers, and non-subprocess downloads in followed scripts. Add self-test controls for container/services and for at least one unlisted installer. Alternatively, a public decision narrows the guarantee, and the guide lists the accepted unrecognised forms.
- **Verification:** `python3 -I scripts/inventory_probes.py <checkout> <pristine-tree> <scratch>` reports no SILENT outcome, and the repository self-test includes the new controls.

### R638-2-F2 MINOR: the source lock's Ubuntu URLs expire, so the recipe stops rebuilding from its own lock

- **Lenses:** Conformance, Robustness, Docs.
- **Where:**
  - `ci/image/sources.lock.json` `packages`: 185 `archive.ubuntu.com` URLs.
  - `ci/image/build.py:113-131`: `verified_download` fetches only the row URL.
  - `docs/testing/CI_IMAGE.md:93-116` and `:209-217`.
- **Authority:**
  - Assignment item 2 requires a build script that "builds the image reproducibly".
  - Focus item 3: a rebuild from the recipe gives the same bytes.
  - The guide's Rebuild section.
- **Evidence** (`receipts/ubuntu-archive-retention.txt`):
  - 93 of the 186 locked packages are update-pocket versions, for example `python3.12=3.12.3-1ubuntu0.17`, `git=1:2.43.0-1ubuntu7.3`, `curl=8.5.0-2ubuntu10.15` and `libc6-dev=2.39-0ubuntu8.9`.
  - The archive already returns 404 for the superseded `git` 7.1 and 7.2 and `python3.12` 0.1 and 0.16. It returns 200 only for the current version.
  - The timestamped `snapshot.ubuntu.com` pool serves the locked `python3.12` deb with an identical SHA-256.
  - Today every URL resolves: my `--prepare-only` from an empty work directory passed.
- **Impact:**
  - The next security update to any of the 93 packages turns `--prepare-only` into a download failure. It fails closed, but the published digest can no longer be rebuilt or re-verified by a second person, and the manager's merge-turn build can fail for reasons unrelated to the change.
  - The guide presents the rebuild as durable and says nothing about this.
- **Required outcome:**
  - Locked package rows resolve durably, for example through a timestamped snapshot URL carrying the same size and SHA-256, or a documented ordered fallback that `verified_download` uses.
  - The guide states the retention property, and the regeneration steps note that a lock refresh also updates the file-pinned literals in `scripts/check_baremetal_only.py` (`CI_IMAGE_LOCK_LITERALS`).
- **Verification:** a `--prepare-only` in an empty work directory succeeds when the primary archive URL of a locked update-pocket package returns 404, by substituting the superseded-archive form in a disposable copy. The fetched bytes match the lock.

### R638-2-F3 MINOR: the build script crashes with the current buildx release; the prerequisite is unpinned

- **Lenses:** Robustness, Docs.
- **Where:**
  - `ci/image/build.py:314-318`: `produced["containerimage.config.digest"]`.
  - `:345`: the `except` tuple has no `KeyError`.
  - `docs/testing/CI_IMAGE.md:72-75`: "Install the Docker buildx plugin", with no version; "Alternatively, use a docker-container builder."
- **Evidence** (`receipts/buildx-metadata-keys.txt`, `receipts/reviewer-cold-rebuild.txt`):
  - With buildx v0.38.0, the latest release (2026-10-07; checksum-verified), the full `--no-cache --defer-lock` build completed and exported the locked manifest.
  - `build.py` then exited 1 with an uncaught `KeyError: 'containerimage.config.digest'`, so no receipt, `image.tar` or lock step followed.
  - A fresh tiny-image build with the same client shows that the key is never emitted. The author's metadata, from an older client, contains it.
  - Separately, by buildx's documented semantics, a docker-container builder keeps `--output type=image` results inside the builder. The script's following `docker image inspect` and `docker image save` would therefore fail. This was not executed (pulling the builder image was out of bounds).
- **Impact:** a rebuilder who follows the guide with today's buildx gets a traceback after the long build, with no image export or lock. The documented alternative builder cannot complete the script.
- **Required outcome:** `build.py` takes the config digest from a source that every supported client provides, such as the exported manifest it already authenticates or `docker image inspect`. Otherwise it pins and checks the supported buildx version and refuses others with a `REFUSED:` message. The guide names a builder setup that completes the script.
- **Verification:** `build.py --no-cache --defer-lock` followed by `--record-lock` completes with buildx v0.38.0, and the receipt equals `image.lock.json`.

### R638-2-F4 MINOR: the patch-provenance self-test needs a configured git identity

- **Lenses:** Tests, Robustness.
- **Where:** `ci/image/privacy_patch_selftest.py:28-30` and `:49-50` (`git commit` with no identity).
- **Evidence** (`receipts/selftests/patch-selftest-identity.txt`, `receipts/selftests/summary.txt`):
  - Inside the final image, offline, with `HOME=/tmp`, the self-test exits 1 at `git commit` ("unable to auto-detect email address").
  - With `GIT_AUTHOR_*`/`GIT_COMMITTER_*` set, all five controls pass.
  - Hosted runners and the image configure no git identity.
- **Impact:** a documented validation command (PR body; `CI_IMAGE.md:92`) fails for a reason unrelated to the property it tests. Once adopted in CI it would be red, or would invite an environment workaround.
- **Required outcome:** the self-test supplies its own disposable identity, for example `git -c user.name=… -c user.email=…` or a subprocess environment, and passes on a clean runner and in the image.
- **Verification:** run it in the image with `HOME=/tmp` and no identity: rc 0 with all five PASS lines.

### R638-2-F5 MINOR: the guide omits the SDK location the existing census needs, and misattributes `MILAN_RV32_CC`

- **Lenses:** Docs, Robustness.
- **Where:**
  - `docs/testing/CI_IMAGE.md:247` ("`MILAN_RV32_CC` … Existing SDK installer's compiler selection").
  - `:279-298` (CI and act adoption).
  - `sw/builder/test_builder.py:4767-4768`, where the census compiler is `Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc"`.
  - The workflows' `~/br-milan-rv32/host` (for example `docs.yml:190-196`).
- **Evidence:**
  - `scripts/ci_rv32_sdk.py` never reads `MILAN_RV32_CC`. Its consumers are `sw/firmware/gtest/fw_rv32.py:31` and the ctrl tests.
  - In the image, `~/br-milan-rv32/host` does not exist, and only `riscv32-linux-gcc` is on PATH, which is not a census candidate (`receipts/sdk-home-probe.txt`).
  - The author's own public receipt (`faf4ddda` `author-r2/builder-background.receipt.json`, STOP 6165278540) shows `--require-rv32` failing in 3.3 s with the default HOME.
  - The passing campaign needed a HOME mapping and a `br-milan-rv32/host -> /opt/rv32-sdk` link (`builder-home-preflight.json`).
  - The guide's adoption section names the `ci_litex_env.py` change but not this one.
- **Impact:**
  - The switch lane, which must "pass every workflow's suites inside it", will hit the same failure, or keep downloading the SDK in each job.
  - The environment table's consumer column is wrong for one of the five variables it documents.
- **Required outcome:** the guide states how the existing census and workflow SDK steps find the compiler in the image. Either the image provides the home-relative link for the job user, or the adoption section names the required link or step change. The `MILAN_RV32_CC` row names its actual consumers.
- **Verification:**
  - Doc check against `test_builder.py:4767`.
  - In the image, with only the documented setup, `test_baremetal_profile_contract --require-rv32` gets past its compiler prerequisite.

### Suggestions (do not affect the verdict)

- **S1.** Have `privacy.Policy` add runtime rules for the checkout path and the `--work` path. The absolute-path class covers `/home/` and `/data/X/` but not, for example, `/srv/…`. Today no such path can reach a layer, because all inputs are bind-mounted at fixed targets, and my scan found none.
- **S2.** The guide's pull-by-digest step depends on the registry serving the lock's OCI manifest digest unchanged. State how the manager pushes so that it holds, for example a push from the containerd image store, and check the registry's digest against the lock before announcing it.
- **S3.** `CI_IMAGE_LOCK_LITERALS` pins individual package versions. Mention it in "Regenerating source closures" (see F2's required outcome).

## Manager rulings, checked

- **(a)** The `mf48` resource-calibration arm NOT RUN is the existing hosted skip. It is not a finding.
- **(b)** Grouped builder evidence: `scripts/check_builder_groups.py` produced `receipts/builder-groups-check.json`.
  - Nine `builder-functions-N.json` files (groups 0-8) carry one identical source hash, `997e8528…`, equal to `sha256(HEAD:sw/builder/test_builder.py)`.
  - Every file records the same partition, equal to the 103-entry `__main__` loop at the head. Each file ran exactly its assigned group, all with `require_rv32: true`.
  - Missing, duplicated and extra functions: none.
  - Group 1, `test_baremetal_profile_contract`, is the background campaign: rc 0 in 1,014,708 ms on image `8cc05a5c…`, at this head.
  - Accepted as the completed verdict.
- **(c)** `MAKEFLAGS += -e` (`receipts/makeflags-skip-parity.txt`):
  - The hosted docs-check at live dev (run 38516575606, ubuntu-24.04 20261004.327.1) prints the identical `NOT RUN [gate 1b]` skip, in both the focused pass and `test_baremetal_profile_contract`.
  - The image's make is Ubuntu noble `make 4.3-4.1build2`. The gate's own probe construct prints `good.o` in the image, so the construct is inert there.
  - Same skip, so no coverage loss, and not a finding. The hosted log does not print the runner's make version, so parity is shown by behaviour and the shared release.
- **(d)** No workflow file changed.

## Prior findings at this head

| Finding | Status at 18f2df92 | Evidence |
|---|---|---|
| R638-1-F1 BLOCKER bare-metal gate red | **Closed.** File-pinned literal `TERM_MASKS` bound to the two locks, the guide and three named infrastructure files. Wrong-file, appended-term and unlisted-literal arms included. | `receipts/selftests/` (`--check` 0 findings over 1,312 files; `--selftest` PASS 737 arms plus one LOUD SKIP as root); exact-head hosted `docs-check` success (`receipts/exact-head-check-runs.tsv`) |
| R638-1-F2 MAJOR not reproducible | **Closed.** Verilator reports `rev v5.050`. | `receipts/reviewer-cold-rebuild.txt` (third cold build, identical manifest and config); `receipts/smoke-offline.log` |
| R638-1-F3 MAJOR regeneration fails open | **Five named forms closed (all REFUSED). Retained, narrowed, as R638-2-F1.** The required "docs claim matches the behaviour" still fails for other forms. | `receipts/prior-findings-probes.json`, `receipts/inventory-probes.json` |
| R638-1-F4 MAJOR versions | **Closed** per ruling 6162190578. The guide's table equals runner manifest 20261004.327.1 (Git 2.55.0, CMake 3.31.6, Ninja 1.13.2, Temurin 17.0.20+1, Node 22.23.3, gh 2.102.0, Docker client 28.0.4, Clang 18.1.3, Python 3.12.3). Smoke compares binary output with the lock. | `receipts/smoke-offline.log`; the runner manifest at tag `ubuntu24/20261004.327` |
| R638-1-F5 MINOR privacy | **Closed.** The oracle layer holds 38 files, with no bytecode or build logs. The recipe scan has per-class planted controls. Zero build-host identity found. | `receipts/verify-archive.log`, `receipts/privacy-report.json`, `receipts/reviewer-image-scan-summary.json` |
| R638-1-F6 MINOR layer mapping | **Closed.** Base plus 13 tool layers, with LiteX separate. The lock binds OCI digest and diff-id per record, with per-layer recipe digests. | `ci/image/image.lock.json`; verify run |
| R638-1-F7 MINOR env defaults | **`VERILATOR_JOBS` removed; Env documented. One wrong consumer retained in R638-2-F5.** | config Env in `receipts/reviewer-image-scan-summary.json` |
| R638-1-F8 MINOR VexiiRiscv tree | **Closed.** Five recursive repositories. `resolve_git.py` regeneration leaves `sources.lock.json` byte-identical. `ci_litex_env.py --check` is rc 0 in the image, and the guide records the adoption change. | `receipts/closures/`, `receipts/sdk-home-probe.txt` |
| R638-1-F9 MINOR prepare race | **Closed.** Unique temporary names; self-test with ten simultaneous duplicate downloads. | `receipts/selftests/` |
| R638-1-F10 MINOR hand roots | **Closed.** `package_roots.json` with consumers. The resolver reproduces 186 packages from 30 roots. | `receipts/closures/summary.txt` |
| R638-1-R1 RESIDUE prerequisites | Text added. Its "docker-container builder" alternative and the unpinned buildx are now a functional defect, R638-2-F3. | |
| R639-1-F1 MAJOR reproducibility | **Closed** (as R638-1-F2). | |
| R639-1-F2 MAJOR called-script forms | **Both forms REFUSED, closed.** The general claim is retained in R638-2-F1. | `receipts/prior-findings-probes.json` |
| R639-1-F3 MINOR lock check | **Closed.** All five mutations refused. The clean control passes and reports `UNVERIFIED without --verify-archive`. | `receipts/prior-findings-probes.json` |
| R639-1-F4 MAJOR gate red | **Closed** (as R638-1-F1). | |
| R639-1-F5 MINOR layer boundaries | **Closed.** LiteX has its own COPY layer, and sbt is one COPY. | config history |

## Clean lens

[R638] PASS RTL — the artifacts examined, at this head:

- `ci/image/install.py:55-75` against `.github/workflows/rtl-fast.yml:153-170` and `elaborate.yml:280-293`.
- The upstream yosys `v0.66` tag commit `86f2ddeb…` and its `abc`/`libs/cxxopts` gitlinks `5d51a5e4…`/`4bf61f08…`, which equal the lock.
- The in-image offline smoke: Verilator `--binary --assert` model run; sv2v, then Yosys `synth`, `abc -g AND` and `check -assert`; and `yosys-abc`.

No HDL, testbench or synthesis source changes in `fa7347fc..18f2df92`. The simulator and synthesizer are configured exactly as the workflows configure them. The fixed revision string `rev v5.050` equals what a git checkout of the tag reports.

## Other executed evidence

- **Recipe verification.** `--prepare-only` from an empty work directory passed and reproduced recipe `a6fd01e6…`; the first try hit a network connection reset and the retry passed. `--check-lock` and `--check-lock --verify-archive` both passed.
- **Repository gates in the image** (CPython 3.12.3, offline, clone read-only) all exit 0: `ci_tool_inventory.py --check`, the inventory, build, integrity and privacy self-tests, `check_baremetal_only.py --check/--selftest`, `docs_check.py`, `check_em_dash.py --base fa7347fc`, `check_doc_style.py` and `check_py_idiom.py`. `privacy_patch_selftest.py` is the exception (F4).
- **Closure regeneration.** On a disposable copy, the `resolve_base.py` and `resolve_git.py` regeneration leaves `sources.lock.json` unchanged. `resolve_packages.py` passes against my cache.
- **Exact-head hosted checks** (read-only): 24 success, 1 skipped (physical gPTP), and Verilator shards 1/5 and 2/5 still in progress when read. The manager owns hosted acceptance.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R638-2-F1, R638-2-F2) | Assignment and rulings; `scripts/ci_tool_inventory.py`; `ci/image/{Dockerfile,build.py,install.py,image_lock.py,image_archive.py,privacy.py,privacy.json,patch_provenance.py,sources.lock.json,image.lock.json,tool-inventory.json,package_roots.json}`; my rebuilt and the daemon's final image; runner manifest; hosted logs | R638-2 | 18f2df92b13cb3f4036b073ed76940187bf10487 |
| RTL | CLEAN | Verilator/Yosys recipe vs the workflow build steps; upstream tag and gitlinks; offline simulation and synthesis smoke | R638-2 | 18f2df92b13cb3f4036b073ed76940187bf10487 |
| Robustness | UNCLEAN (R638-2-F1 to F5) | Cold prepare and cold rebuild; archive retention probe; buildx client probe; inventory and lock mutation probes; in-image environment probes | R638-2 | 18f2df92b13cb3f4036b073ed76940187bf10487 |
| Tests | UNCLEAN (R638-2-F1, R638-2-F4) | All six recipe self-tests and the bare-metal self-test run in the image; smoke; my planted controls; grouped builder evidence | R638-2 | 18f2df92b13cb3f4036b073ed76940187bf10487 |
| Docs | UNCLEAN (R638-2-F1, F2, F3, F5) | `docs/testing/CI_IMAGE.md`; `docs/README.md:88`; PR body; REVIEW READY; doc gates | R638-2 | 18f2df92b13cb3f4036b073ed76940187bf10487 |

## Real limits

- **One host only.** Reproducibility was checked on one host and one daemon. Mine is a third cold build: a different session, about 11 hours later, with a different buildx client. Cross-host identity was not tested.
- **No registry round-trip.** Nothing was pushed, pulled or logged in, so whether the registry serves the lock digest after push is unverified (S2).
- **Builder campaign not re-executed.** I verified the grouped evidence structurally against the head source and its receipts.
- **Hosted make version.** It is not printed in the hosted log; parity rests on identical skip behaviour and the shared Ubuntu release.
- **Builder alternative not executed.** The docker-container builder claim in F3 follows documented buildx behaviour; it was not run.
- **Tool provisioning.** The host has no buildx plugin. I installed the checksum-verified v0.38.0 binary into a private client configuration under this packet's scratch directory. The shared daemon was used through the group-switch prefix.
- **Daemon state.** I added the temporary tag `r638-2-rebuild:…` and then removed it. The BuildKit cache from my no-cache build remains in the daemon. A pre-existing `r638-2-probe:…` tag on the same image, from the voided session, was left untouched.
- **No product regression.** No product regression, act run, hardware or physical calibration.
- **Clone untouched.** Probes ran on `git archive` copies and in an external work directory, and the clone stayed byte-identical to the head (`receipts/clone-integrity.txt`):
  - worktree equals HEAD;
  - the index tree equals the HEAD tree `21c29354…`;
  - the submodule gitlinks are unchanged.

## Pending manager duties

- Hosted and act acceptance at the eventual head. Verilator shards 1/5 and 2/5 were still in progress at read time.
- Current-dev merge-candidate validation: source base `fa7347fc`, live dev `fa820988`.
- Image publication only after both reviews are POSITIVE. After any push, confirm that the registry digest equals `image.lock.json` (S2).
- Re-review of F1 to F5 at the corrected head.

## Publishable files

`MANIFEST.sha256` lists every published receipt and script. Host-specific paths in receipts are replaced by `<packet>`, `<clone>` and `<home>`. The reviewer's private scan needle list is not published; the scan summary publishes neutral class labels and counts only.

R638-2 FINISHED
