[R639] NEGATIVE - exact head 2b2e4d2c5b7f43cfc9df5347d99f9fee2c1fb895

Round R639-1, external independent review of issue #737 / PR #738. Three MAJOR findings and two MINOR findings remain open. All five lenses were applied. This is a source-head review, not approval to publish the image or merge the PR.

Tree: `7c1b712df4047c428615db348ffbb59a05f51282`.
Reviewed range: `fa7347fc59173f90e4feec2df207692e6e6e72ec..2b2e4d2c5b7f43cfc9df5347d99f9fee2c1fb895`.

The public contract was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue body and manager decisions, REQUIREMENTS.md, CI_WORKFLOWS.md, workflow installation steps and their installer/pin files. The complete 13-path diff and three-commit history were examined. Executable author receipts were then read from the pinned public evidence commit. No private author material, management scratchpad, or another reviewer's report was read. An independent verdict and ledger were written before checking prior public findings.

Authorities: [image-lane assignment](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160953880), [public-image rule](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160859632), [issue contract](https://github.com/kebag-logic/milan-fpga/issues/737), [public review start](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6161843572), and [published executable evidence](https://github.com/kebag-logic/milan-fpga/tree/efbda0ff15e1e9606fa59019b6957383bda3b720/review-evidence/737-image-r1).

**Findings**

[R639] F1 MAJOR Conformance, Robustness, Tests, Docs - `ci/image/build.py:215`, `ci/image/install.py:54`, `ci/image/install.py:148`, PR #738 Description / Definition of Done - Cold builds are not byte-reproducible.

Authority/evidence: The assignment requires a reproducible build; this review explicitly requires identical image bytes. The build command supplies neither a fixed build epoch nor timestamp normalization. The archived simulator source lacks Git metadata, and its exact checked `src/config_rev` function uses the current date. `probe_revision.py` verified the archive SHA-256 and executed that function with two dates: the same source produced `vUNKNOWN-built20261014` and `vUNKNOWN-built20261015`. The published smoke receipt actually contains the first string. This is embedded version content, not just an external receipt timestamp. Separately, the exact `sbt()` installer, with only destinations relocated and a fixed fixture artifact, produced identical file payloads with different mtimes and different tar hashes. `probe-controls.json` records that bounded experiment. The published image receipt compares a 393.856-second uncached build with a 2.896-second cached rebuild; cache reuse does not exercise reconstruction. BuildKit documents separate handling for image/config timestamps and timestamps within layers: [build reproducibility](https://github.com/moby/buildkit/blob/master/docs/build-repro.md#source_date_epoch).

Impact: An unchanged recipe can yield different tool contents and image digests on another build date. The checked image-lane acceptance box is premature. The published limitation about untested cross-host cold builds does not establish the required same-byte property.

Required outcome: Make all image-affecting inputs deterministic, including generated tool revision strings and file/image metadata. Demonstrate two genuinely uncached builds of the same recipe with matching image manifests, configuration and layer bytes. Preserve honest disclosure until that evidence exists.

Verification: `probe-revision.json`, `probe-controls.json`, `public-receipts/smoke-version-excerpts.jsonl`, and `public-receipts/image-build-receipt.json`; then an independent two-cold-build comparison. No full image comparison was executed in this round.

[R639] F2 MAJOR Conformance, Robustness, Tests, Docs - `scripts/ci_tool_inventory.py:196`, `scripts/ci_tool_inventory_selftest.py:56`, `docs/testing/CI_IMAGE.md:21` - Called-script installations can disappear from the derived inventory.

Authority/evidence: Assignment item 1 requires deriving installations from workflow steps and their called scripts. The parser inspects only calls whose first argument is a literal list or tuple. In disposable fixtures, a workflow called `scripts/bootstrap.py`. Both of these script bodies were accepted by `--write`, produced `tools: []`, and subsequently passed `--check`:

```python
cmd = ["pip", "install", "review-fixture==1.0"]
subprocess.run(cmd, check=True)
```

```python
subprocess.run("python3 -m pip install review-fixture==1.0", shell=True, check=True)
```

The otherwise equivalent literal-list call was refused. These probes do not execute an installation. Ordinary missing-entry and orphan-entry mutations of the committed inventory were correctly refused; the defect is incomplete derivation after regeneration, not failure to notice a changed workflow hash.

Impact: A normal installer refactor or new installation can produce a current, passing inventory that omits a required tool. The documented unconditional refusal of unsupported installations is false, and the existing negative control covers only the literal-list spelling.

Required outcome: Derive supported command/data-flow forms or refuse unresolved installation behavior. Regeneration must not bless an omitted installation. Add controls for command variables and shell-string calls while keeping the missing/orphan controls effective.

Verification: `probe-controls.json`, `inventory-selftest.log`, and `inventory-check.log`; rerun both fixture forms through generation and comparison after correction.

[R639] F3 MINOR Conformance, Robustness, Tests, Docs - `ci/image/build.py:201`, `docs/testing/CI_IMAGE.md:92` - The lock check validates only the recipe digest field.

Authority/evidence: The lock is the downstream record of tool versions, source digests, platform, base and final image identity. The documented consistency command returned exit 0 and `PASS: image lock describes the current recipe` for each separate mutation: empty layers, an invalid layer tool version, an all-zero final image digest, a different platform, and `ubuntu:latest` as its recorded base. Only `recipe_digest` was retained. The current committed lock's source rows do match the source declarations; this finding concerns the advertised checker accepting contradictory records.

Impact: A stale, truncated or edited lock can pass its supplied consistency check while exposing incorrect inputs to later consumers. A valid recipe hash is not validation of the rest of the record.

Required outcome: Validate schema and required fields, recompute/compare the layer tool/version/source/recipe data, and check platform/base consistency. Clearly distinguish recipe consistency from verification of the actual image digest against a build artifact. Reject malformed image identities; do not imply that a syntactically valid arbitrary digest has been authenticated offline.

Verification: The five separate lock mutations in `probe-controls.json` must be refused or explicitly classified as unverified image identity. Preserve the clean-lock pass.

[R639] F4 MAJOR Conformance, Tests, Docs - `ci/image/image.lock.json:33`, `ci/image/sources.lock.json:37`, `docs/testing/CI_IMAGE.md:46`, `.github/workflows/docs.yml:183` - The new image artifacts fail a mandatory repository gate.

Authority/evidence: REQUIREMENTS.md REQ-VER-04 requires the repository-wide bare-metal-only gate to pass with zero policy findings. On this exact checkout, `python3 scripts/check_baremetal_only.py --check` exits 1 with 40 findings, all in the new locks and image guide. The one exact-head hosted snapshot independently reports `docs-check` failed at `Bare-metal scope gate` in [run 38518396662](https://github.com/kebag-logic/milan-fpga/actions/runs/38518396662). The author's 13 scoped gate receipts omit this mandatory gate.

Impact: The required docs context is red, so this head cannot meet the existing merge bar. These are host package names, platform strings and source URLs; the finding does not claim that the product acquired a hosted operating-system dependency.

Required outcome: Resolve the host-tooling allowance publicly and narrowly, preserving real package/source identities and the gate's protection of product surfaces. Do not erase provenance or add a broad exemption simply to obtain a pass. The exact corrected head must pass the gate and its negative controls.

Verification: `baremetal-check.log`, `baremetal-check.rc`, `hosted-state.json`; then rerun the scope gate and its selftest, with controls proving the allowance cannot hide product claims or unrelated terms.

[R639] F5 MINOR Conformance, RTL, Docs - `ci/image/Dockerfile:82`, `ci/image/Dockerfile:87`, `ci/image/build.py:233`, `docs/testing/CI_IMAGE.md:73` - The final image does not preserve one layer per declared tool group.

Authority/evidence: Assignment item 2 requires one layer per tool. `python-tools` creates `/opt/python`; `litex-tools` inherits and adds to that same prefix. The final stage inherits `gtest-tools` and copies the complete Python-plus-LiteX prefix once from `litex-tools`. It therefore has a combined output layer while the lock declares separate `python` and `litex` layer records. Conversely, the single `sbt` record corresponds to two final COPY instructions. `layer-layout.json` records the stage and COPY instructions; this is a static architecture finding, not a claim to have exported the image's layers.

Impact: Intermediate build stages are being described as separately preserved final tool layers. A LiteX-only change also replaces the copied Python package layer, and the lock's layer grouping does not describe the requested one-tool/one-layer layout.

Required outcome: Preserve the requested tool-layer boundaries in the final image and align the lock/docs with those actual boundaries, or obtain an explicit public scope decision changing that requirement. Merely renaming the records does not satisfy the existing assignment.

Verification: Inspect the final exported layer contents/digests, map each tool group to its layer, and verify that changing one group's pin leaves unrelated group layers reusable.

No RESIDUE or SUGGESTION findings are used to downgrade these defects. All five findings remain open at this head.

**Acceptance and evidence**

| Assignment item | Result at the reviewed head |
|---|---|
| Derived inventory and controls | Baseline comparison and supplied controls pass. Actual missing/orphan entries are refused. Called-script omission remains F2. |
| Pinned multi-stage recipe | The base is digest-pinned. All 214 package and 476 other artifact declarations have versions, sizes and SHA-256 values; all 690 appear exactly once in the lock's tool records. Final tool-layer separation remains F5. |
| Reproducible build and generated lock | The current recipe/lock declarations agree, but cold reproducibility remains F1 and the lock checker remains F3. |
| Matching versions and offline smoke | Author receipts report successful offline smoke checks and CPU-source compilation. The supplied smoke code and outputs were reviewed. No independent image execution occurred, and unversioned workflow packages are only resolved to the lock's choices, not compared against a fresh hosted installation. |
| Public image privacy | Source declarations use public HTTPS origins without URL userinfo. Context construction, mounts, COPYs, ENV and cleanup were examined. No independent history or layer-content audit occurred; publication privacy is NOT VERIFIED. |
| Accurate rebuild/digest documentation | Rebuild and pull-by-digest commands exist. F1-F3 and F5 prevent accepting all associated claims. |
| No workflow changes | PASS: the complete source diff changes no workflow, RTL, firmware or submodule gitlink. F4 still prevents the unchanged required workflow from passing. |

The supplied inventory selftest, image-builder selftest, inventory check, and clean-lock check each exited 0. They ran concurrently as four small foreground commands, with separate logs and return-code receipts. The independent probes ran only in disposable copies under `scratch/`; no source fix was made. `source-audit.json` records the exact diff digest, all changed paths, commit history, 294 matching inventory input hashes and declared source/lock consistency. Only the simulator archive was independently downloaded and checksum-verified; the full dependency closure was not redownloaded.

The published evidence manifest was verified for 31 selected executable receipts/data files, without opening the public handoff or private author material. `public-evidence-verification.json` records each checked digest. The public inventory and image lock are byte-identical to the reviewed files. `public-receipts/` retains selected unchanged receipts plus explicitly named smoke-version excerpts. Their origin remains the author, not this reviewer or a manager source bank.

**Reviewer-owned coverage ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Issue assignment and public-image rule; workflow install steps; `ci_tool_inventory.py`; source/image locks; Dockerfile; F1-F5 | R639-1 | 2b2e4d2c5b7f43cfc9df5347d99f9fee2c1fb895 |
| RTL | UNCLEAN | Complete 13-path diff proves no HDL/interface/gitlink changes; installer compiler options match workflow options; Dockerfile final-stage architecture and lock layer grouping have F5 | R639-1 | 2b2e4d2c5b7f43cfc9df5347d99f9fee2c1fb895 |
| Robustness | UNCLEAN | Parser command forms; download/path/hash controls; `build.py --check-lock`; timestamp-sensitive installers; independent fixtures; F1-F3 | R639-1 | 2b2e4d2c5b7f43cfc9df5347d99f9fee2c1fb895 |
| Tests | UNCLEAN | Both new selftests; `smoke.py`; public executable receipts; missing/orphan, called-script, lock-corruption and timestamp probes; exact-head scope gate; F1-F4 | R639-1 | 2b2e4d2c5b7f43cfc9df5347d99f9fee2c1fb895 |
| Docs | UNCLEAN | `docs/README.md` diff; `CI_IMAGE.md`; PR acceptance/evidence claims; generated locks and public receipts; F1-F5 | R639-1 | 2b2e4d2c5b7f43cfc9df5347d99f9fee2c1fb895 |

All lenses were applied; no clean coverage is banked by this round. There are no product CDC, reset or wire-interface changes in the reviewed delta. That observation does not assert product regressions were executed inside this image.

**Prior findings and hosted evidence**

After writing the independent assessment, the public PR reviews, inline comments and issue comments were queried. At the recorded query time there were zero submitted reviews, zero inline findings and zero reviewer-led finding comments. There was therefore no prior public finding to resolve or retain. The two review-start comments are not verdicts. See `prior-review-state.json`.

The single hosted snapshot, taken at 2026-10-14T05:57:52Z, shows docs failed while elaborate, rtl-fast and rtl-full remained in progress. The physical gPTP job was explicitly skipped. `hosted-state.json` records job and step outcomes separately, including skips. It is not a green hosted verdict and was not used as proof of locally executed tests. No further hosted acceptance was inferred.

**Reproduction**

From this exact source checkout, with this packet at `$PACKET`:

```sh
export TMPDIR="$PACKET/scratch"
export PYTHONDONTWRITEBYTECODE=1
python3 scripts/ci_tool_inventory.py --check
python3 scripts/ci_tool_inventory_selftest.py
python3 ci/image/build_selftest.py
python3 ci/image/build.py --work "$PACKET/scratch/build" --check-lock
python3 "$PACKET/probe_controls.py" "$PWD" "$PACKET"
python3 "$PACKET/probe_revision.py" "$PWD" "$PACKET"
python3 "$PACKET/audit_sources.py" "$PWD"
python3 scripts/check_baremetal_only.py --check
python3 "$PACKET/verify_tree.py" "$PWD"
```

The scope gate currently exits 1. The probe scripts exit 0 when they reproduce the recorded defects and controls; that is not a product PASS. They may download the one public pinned source archive but never execute an installation, invoke Docker, or write to the candidate. `collect_public.py` is a separate read-only public-state collector; its snapshot is time-dependent. The foreground commands must be captured independently so the expected scope-gate failure does not prevent the final byte verification.

**Limits and pending manager duties**

The assignment requires Docker build/history/layer inspection but later explicitly prohibits Docker and privilege use. Clarification was requested and no answer was received. No Docker, act, privileged command, image rebuild or independent offline image smoke was run. In particular, no `docker history --no-trunc`, layer archive, label/environment inspection, or independent privacy proof is claimed. `runtime-limits.json` records these as NOT RUN. The static HTTPS/context checks and author smoke receipts cannot clear public-image privacy.

No full parent, processor, gPTP, synthesis or builder bank was run. No manager source bank exists at this exact head, and none is claimed. The source base above is distinct from live dev `fa8209889411e8ca95757174c981f720dbcd95a2`. The manager still owns source/hosted/act acceptance and the final current-dev candidate's builder and native bank execution, with receipts linked on the PR at the merge turn. This source review supplies none of that candidate evidence.

Physical calibration was NOT RUN. Skipped field/physical jobs and desk checks provide no hardware proof. No hardware was accessed. No comments, reviews, labels, metadata, commits, pushes, registry logins, image pushes or merges were made. No sub-agents were used.

Initial and final verification directly hashes tracked blob bytes, checks file kinds/modes, compares the entire index with the exact commit, and checks the required gitlinks. The initialized protocol, gPTP and public stack submodules were also verified against their pinned bytes and indexes. `third_party/verilog-axis` is uninitialized; its required gitlink was verified, but no checkout-byte or axis-dependent execution claim is made. All probes used disposable copies, so no candidate restoration was necessary.

Before publication or merge, the manager must obtain corrected-head re-review of the open findings, actual uncached reproducibility evidence, independent image history/layer privacy inspection and offline smoke/version proof; resolve the mandatory scope-gate failure; complete the remaining independent review and current-dev validation; and apply the repository's merge/containment rules. Workflow adoption remains the separate integration lane. This report does not close issue #737 or authorize a merge.

Only REPORT.md and the files listed in MANIFEST.sha256 are publishable. `scratch/` is excluded.

R639-1 FINISHED
