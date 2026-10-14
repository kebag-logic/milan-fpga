[R639] NEGATIVE - exact head 18f2df92b13cb3f4036b073ed76940187bf10487

External independent review of issue #737 / PR #738, round R639-2. All five lenses were applied. One MAJOR finding remains: inventory regeneration still accepts ordinary installation forms while omitting their tools. RTL is CLEAN; Conformance, Robustness, Tests and Docs are UNCLEAN. This is a source-head verdict, not merge or publication authorization.

Tree: `21c293548a85cfb4a9bd7dfd7c1e990c103d18bd`. Full range: `fa7347fc59173f90e4feec2df207692e6e6e72ec..18f2df92b13cb3f4036b073ed76940187bf10487`, 28 paths. The round-two delta from `2b2e4d2c` has 26 paths. No workflow, RTL, firmware, existing patch or submodule gitlink changed.

The review reconstructed repository rules, documentation map, frozen public scope and decisions, requirements/workflow interfaces, implementation/history, then published executable evidence. `independent-pass.md` recorded an independent verdict and ledger before consultation of the prior public findings. No private author material or another current-round report was used.

Authorities: [image assignment](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160953880), [round-two assignment and version/mask rulings](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6162190578), [privacy ruling](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6162652582), [patch refinement](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6163057631), [corrected campaign environment](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6166238176), [author readiness](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6166569995), and [public evidence at faf4ddda](https://github.com/kebag-logic/milan-fpga/tree/faf4ddda73e3a9ce91e1e6f35021af316ec6bdf6/review-evidence/737-image-r1). REQUIREMENTS.md REQ-VER-03/04 and CONTRIBUTING.md remain applicable.

**Open finding**

[R639] R639-2-F1 MAJOR Conformance, Robustness, Tests, Docs - `scripts/ci_tool_inventory.py:26`, `scripts/ci_tool_inventory.py:226`, `scripts/ci_tool_inventory.py:261`, `scripts/ci_tool_inventory_selftest.py:25`, `docs/testing/CI_IMAGE.md:23` - Regeneration still silently drops installations.

Authority/evidence: Assignment item 1 requires deriving tools from workflows and their called scripts. The round-two ruling requires resolving or refusing installation forms so regeneration cannot silently drop an installation. `probe_inventory.py`, executed in the final image under CPython 3.12.3 without networking, demonstrates:

| Disposable workflow input | `--write` | Generated tools | Subsequent `--check` |
|---|---|---|---|
| Called `scripts/bootstrap.py`: `subprocess.run("python3 -m pip install fixture-package==1.0", shell=True)` | Refused, rc 2 | None generated | Refused, rc 2 |
| Same script using `subprocess.run(args="python3 -m pip install fixture-package==1.0", shell=True)` | Accepted, rc 0 | `[]` | Accepted, rc 0 |
| Workflow calls root-level `bootstrap.py` containing a literal-list pip installation | Accepted, rc 0 | `[]` | Accepted, rc 0 |
| Workflow calls a Makefile that downloads a tool with `curl`, extracts it and invokes its install target | Accepted, rc 0 | `[]` | Accepted, rc 0 |

Command inspection requires positional `node.args`; the path recognizer excludes root-level scripts; Makefile scanning catches package-manager words but misses the download/build form. Input hashes are recorded for the followed-script and Makefile cases, but regenerated tool records remain empty. Independent missing-entry and orphan-entry controls both correctly fail with rc 2. Raw receipts: `inventory-probes.json`, `reference-inventory-probes.log`, `reference-inventory-probes.rc`.

Impact: A routine installer refactor or bootstrap step can produce a fresh, passing inventory that omits a required tool. The documented refusal guarantee and installation-drift acceptance remain false. This demonstrates a guard defect; it does not assert that the current unchanged workflows already use those omitted forms.

Required outcome: Derive these ordinary command/path/build forms or explicitly refuse them before writing an inventory. Add generation-then-comparison controls for each while preserving the positional-string, missing-entry and orphan-entry controls. Document the supported boundary accurately; weakening prose alone does not meet the frozen acceptance criterion.

Verification: Run `probe_inventory.py <checkout>` with the corrected parser under CPython 3.12.3. Every installing fixture must be explicitly refused or represented with the tool and pin. An empty passing inventory is unacceptable. Re-run the committed inventory comparison and controls at the corrected head.

This retains the underlying R639-1-F2 / R638-1-F3 finding. Their specific examples are fixed; the required cause-level outcome is not. No RESIDUE or SUGGESTION is used to downgrade it.

**Acceptance evidence**

The reviewer exported, inspected and executed the locally present final image. No image was pulled, rebuilt or published. The pinned base was exported locally. Empty-cache preparation independently authenticated all 186 distribution and 479 source declarations. The image's smoke program and source lock match this head byte-for-byte.

| Area | Result and evidence |
|---|---|
| Inventory | Baseline and supplied controls pass; independent missing/orphan controls refuse drift. F1 remains open after regeneration. |
| Recipe and layer architecture | Digest-pinned base, checked artifacts, offline build command; 13 recipe layers plus one base layer, with Python and LiteX separate. `Dockerfile`, `install.py`, `prepare.log`, `layer-audit.json`. |
| Cold reproducibility | Both published build metadata files explicitly request `no-cache` and network `none`. Both cold records agree on manifest, config and all 14 compressed/uncompressed layer identities. Every identity equals the independently exported final image. `image-verification.json`; public `cold-comparison.json` and candidate metadata. |
| Lock | Complete schema/recipe checks and actual archive authentication pass. Corrupted schema, versions, source identities, platform/base and unverified image-identity controls refuse. `integrity-controls.log`, `lock-consistency.log`, `image-authentication.log`. |
| Versions and smoke | All supplied tool-family checks pass with networking disabled, on CPython 3.12.3. Binary outputs include Verilator `rev v5.050`, synthesis/conversion, RV32, rendering, GoogleTest, Scala and a real oracle packet. `offline-smoke.log`, `version-excerpts.json`. Runner deviations are explicitly authorized and documented. |
| Privacy | Full `docker history --no-trunc` and configuration examined. Every layer scanned against the identity table and runtime builder identity, with authenticated upstream allowances. Independent enumeration covers 45,119 members, including 37,763 regular files; no forbidden context/build leftovers. `image-history.txt`, `image-inspect.json`, `image-authentication.log`, `layer-audit.json`. |
| Patch provenance | 526 upstream allowances authenticated on this reviewer host. The patched CPU member is reproduced from the pinned source and committed patch; each matching line retains upstream origin. Added-identity, changed-input and unknown-postimage controls refuse. `image-verification.json`, `patch-controls.log`, `privacy-controls.log`. |
| Recursive CPU sources | Independent archive/member comparison and actual patch application match all 4,550 files/links and executable modes, with no missing/extra/changed entries. `cpu-tree-verification.json`; offline placement `--check` also passes. |
| Dependency regeneration | 30 checked roots resolve to exactly 186 locked packages; the image cache reproduces 423 Scala artifacts and 88 bootstrap placements. `package-closure.log`, `reference-maven-closure.log`; unused-root control passes. |
| Bare-metal masks | File-pinned literal masks preserve wrong-file and appended-term refusals. Zero findings over 1,312 tracked first-party files; all 738 controls pass. `reference-baremetal.log`, `baremetal-controls.log`. |
| Documentation | Rebuild prerequisites, cold-build limits, recipe identity, layer authentication, privacy, environment and digest consumption checked. Documentation privacy gate passes. F1 prevents accepting the inventory guarantee. |
| Workflow boundary | No workflow changed; complete workflow/image adoption belongs to the separate switch lane. `final-tree.json`. |

Measured manifest: `sha256:8cc05a5c51aa04a23063c5d0593065912845a4ba4ce5a5dfd3ff53b12ccd1d19`. Configuration: `sha256:1eac3b02d4109a09c63bbf68893a2695c6380f1ce6d444168a3828c9a83e0b9b`. Recipe: `a6fd01e6bf2ced24f6a68a33c899199dfda2eb46fe4a0def569542d5c5240b7f`. Published size: 3,931,041,388 bytes; cold-build times: 456.784 and 404.539 seconds. These timings are author measurements, not a third reviewer cold build. Cross-host reproducibility remains unproved.

History has 27 entries and the documented environment, without `VERILATOR_JOBS`. All recipe-layer members, including the SDK, have root ownership; the immutable base retains distribution accounts. The oracle layer has 38 regular files and six symlinks, without bytecode, CMake logs, source checkout or context leftovers. Privacy allowances follow the two public decisions; third-party examples may retain identity-like text only with authenticated provenance.

**Grouped builder and make-skip ruling**

`builder-coverage.json` independently derives 103 invocation names from the exact source's main-loop AST and checks every group's declared and returned population. Every name appears exactly once at source SHA-256 `997e8528ba47199a25376256f1614430586ae574e56db3470c0feeaa706a5c47`. All nine accepted group receipts have rc 0 and `--require-rv32`. Group 1 uses the completed corrected campaign, not the timeouts or failed compiler prerequisite. Its published elapsed time is 1,014.708 seconds. This is grouped author evidence; the reviewer did not run the builder bank.

All 373 retrieved non-prose round-two public receipts/data/scripts match the publication manifest. `public-evidence-verification.json` records published hashes and path-redaction flags. Pre-publication hashes are not confused with the redacted public bytes.

The assigned make question produces no finding. Current-dev docs-check [job 115696619496](https://github.com/kebag-logic/milan-fpga/actions/runs/38516575606/job/115696619496), at `fa8209889411e8ca95757174c981f720dbcd95a2`, explicitly takes the same `MAKEFLAGS += -e` skip. Its logged runner image `20261004.327.1` has make `4.3-4.1build2` in the [runner manifest](https://github.com/actions/runner-images/blob/ubuntu24/20261004.327/images/ubuntu/Ubuntu2404-Readme.md). The reviewed image reports that identical package version and GNU Make 4.3. `hosted-make-excerpts.txt` and `version-excerpts.json` retain the comparison. No image-induced coverage loss is demonstrated.

The mf48 calibration arm stays NOT RUN under the explicit ruling. Neither that skip nor field/physical skips provide hardware proof. The published documentation ledger covers 76 commands with earlier-image runs and replacements; it is not a complete final-image workflow verdict.

**Disposition of prior findings**

| Prior finding | Disposition at this head | Cause-level evidence |
|---|---|---|
| R639-1-F1 / R638-1-F2: reproducibility | Resolved for the required same-host property | Fixed epoch; timestamp, ownership, trust-store and revision normalization; two no-cache records and measured manifest/config/14-layer equality. |
| R639-1-F2 / R638-1-F3: inventory | RETAINED as R639-2-F1 | Reported forms now refuse, but ordinary keyword/path/build forms still regenerate empty passing inventories. |
| R639-1-F3: lock check | Resolved | Full schema/recomputed layer records; actual archive authentication remains separate; controls pass. |
| R639-1-F4 / R638-1-F1: bare-metal gate | Source defect resolved | Public literal masks; zero findings and 738 passing controls. Final hosted/act acceptance remains a manager duty. |
| R639-1-F5 / R638-1-F6: layer mapping | Resolved | Separate Python/LiteX layers, one Scala layer, actual compressed/uncompressed digests and per-group recipe records. |
| R638-1-F4: version differences | Resolved under public decision | Accepted deviation table, independent runner manifest and binary outputs; CPython 3.12.3 reference. Full switch-lane acceptance remains pending. |
| R638-1-F5: privacy | Resolved under privacy rulings | Complete export/history/config scan, upstream and patch-line proofs, controls and independent oracle/member inspection. |
| R638-1-F7: environment | Resolved | Worker override removed; remaining ENV entries documented and matched to configuration. |
| R638-1-F8: CPU tree/placement | Resolved | Six recursive repositories and 4,550 matching files/links; offline `--check` passes; adoption replacement documented. |
| R638-1-F9: download race | Resolved | Unique temporary files; ten simultaneous duplicate-download controls pass; empty-cache preparation succeeds. |
| R638-1-F10: roots/closures | Resolved | Consumer-checked roots, distribution/Scala generators and complete candidate-pool procedure; closure checks pass. |
| R638-1-R1: prerequisites | Resolved | Guide explicitly names buildx and containerd/docker-container cache export. |

R638-1-S2 ownership and S3 per-layer recipe suggestions are implemented and verified. S1 separating input provenance from inventory comparison remains optional. No new RESIDUE is recorded.

**Reviewer-owned coverage ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Public assignment/rulings; workflow installs; locks; Dockerfile; measured image; `inventory-probes.json`; open F1 | R639-2 | 18f2df92b13cb3f4036b073ed76940187bf10487 |
| RTL | CLEAN | Full diff/gitlinks; `install.py:49` and `:59` against workflow compile settings; `layer-audit.json`; offline HDL/RV32 smoke and CPU-tree comparison | R639-2 | 18f2df92b13cb3f4036b073ed76940187bf10487 |
| Robustness | UNCLEAN | Inventory forms/drift; concurrent-download, corrupt-source, schema, privacy and patch controls; archive authentication; open F1 | R639-2 | 18f2df92b13cb3f4036b073ed76940187bf10487 |
| Tests | UNCLEAN | Image/inventory selftests; 738 scope controls; smoke; independent parser/CPU/layer probes; grouped builder and hosted skip evidence; open F1 | R639-2 | 18f2df92b13cb3f4036b073ed76940187bf10487 |
| Docs | UNCLEAN | `CI_IMAGE.md:23` and rebuild/privacy/environment/adoption sections; `docs/README.md:88`; public evidence and prior findings; open F1 | R639-2 | 18f2df92b13cb3f4036b073ed76940187bf10487 |

[R639] PASS RTL - `ci/image/Dockerfile`, `ci/image/install.py`, `layer-audit.json`, `offline-smoke.log`, `cpu-tree-verification.json`, `final-tree.json` - Tool-stage architecture and compilation settings match authorized workflow contracts; layers are separately authenticated. No product RTL/interface change exists. Bounded HDL smoke and exact CPU-tree comparison pass; full product regression coverage is not claimed.

**Limits, integrity and pending duties**

No full parent, processor, gPTP, Yosys or builder bank was run. No act, host runner selftest, hardware, shared install, source fix/commit, push, login, merge, GitHub write, author contact or delegated review occurred. Docker use was confined to the explicitly requested local image export/inspection and disposable offline checks. No other image was pulled. Independent operations used foreground processes and bounded concurrency.

Initial host checks used the host interpreter; controls and parser probes were repeated on CPython 3.12.3. An initial root-container scope check failed Git ownership access; the same read-only clone passed as caller UID with explicit safe.directory. The host lacked `dpkg-deb`; the package closure passed inside the image. These setup failures are not passes; completed replacements are separately recorded.

`final-tree.json` verifies all 1,338 tracked blob bytes/modes, exact index equality, all six gitlinks, the four initialized submodule heads and empty worktree status. The two initially uninitialized submodules remain so. Full diff SHA-256: `05a1fc20c7290edf72dbacb26d09ed381c6d0d77d4381fbe26dc90870f38e185`.

`hosted-snapshot.json` is one exact-head observation: some jobs succeeded, major jobs remained in progress, and the physical job was skipped. It is not a completed hosted verdict. No manager source bank exists at this head and none is claimed. Source-head author receipts and this review are distinct from future current-dev merge-candidate builder/native validation.

The manager owns final hosted/act acceptance, current-dev candidate validation and linked receipts, switch-lane full workflow/version adoption, publication and registry digest verification, independent review completion, authorized merge and containment. The image must not be published on this NEGATIVE review. No registry round trip or cross-host rebuild was tested.

Publish only REPORT.md and files listed in MANIFEST.sha256. Disposable trees, downloads, exports and preliminary setup logs stay under `scratch/`. Portable probes accept the checkout path; receipts distinguish reviewer execution from public author evidence. All review processes have completed.

R639-2 FINISHED
