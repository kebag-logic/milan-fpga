[R639] NEGATIVE - exact head e355f789b4f59b86083809299134557ca47bbcfb

Round R639-4, external independent review of issue #737 / PR #738. Four MAJOR findings remain open. All five lenses were applied. RTL is CLEAN; Conformance, Robustness, Tests and Docs are UNCLEAN. This does not authorize publication or merge.

Tree: `42f0ade89e45e059ac27a477376ec3f289996e54`. Full range: `fa7347fc59173f90e4feec2df207692e6e6e72ec..e355f789b4f59b86083809299134557ca47bbcfb`; round-four range: `e6b86814..e355f789`. The full range changes 34 files; the round-four history has five commits. No workflow, product RTL, firmware, testbench or gitlink changes.

The contract was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue/public decisions, requirements and workflow/installer authorities, then the diff/history and public executable evidence. An independent verdict and five-lens ledger were written in `independent-pass.md` before reading prior public findings. No other round-four review, private author notes or management material was read.

Authorities: [image assignment](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160953880), [round-four assignment](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6170435035), [inline/function amendment](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6170543242), [standing census/semantics ruling](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6170640746), [version/mask ruling](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6162190578), [privacy ruling](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6162652582), [patch refinement](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6163057631), and [public evidence](https://github.com/kebag-logic/milan-fpga/tree/42bb379cf9e8eca0161122b8a1919819455bc84c/review-evidence/737-image-r1).

**Findings**

Every defect fixture below ran under authenticated CPython 3.12.3, returned zero from both `--write` and `--check`, and generated `tools: []`. A harmless local executable named `brand_new_command` prints a marker; real shell, Make or Python execution reaches it. No installer is executed. Complete fixture bytes, selected inputs, CLI outputs and actual execution results are in `probe-traversal.py`, `reference-traversal-probes.json` and its raw log.

[R639] R639-4-F1 MAJOR Conformance, Robustness, Tests, Docs - `scripts/ci_shell_walk.py:99`, `:153`, `:257`; `docs/testing/CI_IMAGE.md:82` - Shell scope selects the wrong command population.

Authority/evidence: The standing ruling requires real shell semantics or an explicit refusal. Four literal cases are accepted without residue:

| Probe | Actual execution | Deriver result |
|---|---|---|
| `source fragment.sh; bash bootstrap.sh`, fragment contains `cd sub` | Executes `sub/bootstrap.sh` | Follows benign root script; omits the subdirectory script |
| `name=bootstrap.sh; source fragment.sh; bash "$name"`, fragment assigns `name=sub/bootstrap.sh` | Executes `sub/bootstrap.sh` | Discards sourced assignment; follows root script |
| `cd sub & bash bootstrap.sh` | Background `cd` leaves the parent unchanged; root script executes | Follows benign subdirectory script |
| `if true; then f() { brand_new_command; }; else f() { echo okay; }; fi; f` | Calls first definition | Other branch overwrites the function map; unknown command is never walked |

`source` uses a separate audit shell and copies back only selected functions. Conditional handling merges variables but not function alternatives. Statement background metadata is ignored. These are literal scope effects, not runtime command assembly. Even if background syntax is outside the census, it must refuse rather than pass silently.

Impact: Generation can bless scripts the workflow does not execute while omitting a literal installer it does execute. Existing scope tests pass despite these omissions; the guide's traversal/refusal guarantee is false.

Required outcome: Preserve sourced state, reachable function alternatives and asynchronous scope, or refuse unsupported variants before generation. Add generation/comparison controls and clean counterparts for all four cases.

Verification: `sourced-directory`, `sourced-variable`, `background-directory` and `branch-functions` must reach/refuse the unknown command or refuse the construct by name. Retain subshell, fallback, local-variable and working-directory controls.

[R639] R639-4-F2 MAJOR Conformance, Robustness, Tests, Docs - `scripts/ci_make_walk.py:55`, `:266`, `:374`; `docs/testing/CI_IMAGE.md:89` - Make's selected recipe interpreter is accepted but not followed.

Authority/evidence: The census ruling requires correctly resolved constructs and refusal of unsupported variants. This fixture passes both CLI modes without residue:

```make
SHELL := ./runner.sh
all: ; echo okay
```

A second fixture omits the assignment and runs `make SHELL=./runner.sh`. In both, executable `runner.sh` contains `brand_new_command`; actual Make invokes it. The walker treats `SHELL` as ordinary data and parses `echo okay` directly, never including `runner.sh` in its inputs.

Impact: A literal interpreter selection can run an unclassified installer behind a harmless-looking recipe. Generic assignment/override acceptance bypasses the claimed command boundary.

Required outcome: Refuse uncensused interpreter-selection variables/overrides, or resolve and classify the selected interpreter with actual Make semantics. Add file-assignment and command-line controls. Arbitrary-shell support is not required.

Verification: `make-selected-shell` and `make-selected-shell-override` must no longer produce passing empty inventories. Preserve ordinary recipes and existing alternate-file/default-goal/pattern controls.

[R639] R639-4-F3 MAJOR Conformance, Robustness, Tests, Docs - `scripts/ci_command_table.py:410`; `docs/testing/CI_IMAGE.md:115` - Literal marker text bypasses pinned inline-program classification.

Authority/evidence: The inline amendment requires a program-digest declaration; the standing ruling refuses unsupported variants. This undeclared workflow command passes:

```sh
bash -c 'echo "<dynamic>"; brand_new_command'
```

The shortcut tests substring membership, not runtime-expression provenance. It returns before digest lookup/body traversal and records `declared runtime shell program`, although the entire program is literal and no enclosing declaration exists. Actual Bash executes the unknown command. The guide explicitly says literal marker text never acquires runtime provenance.

Impact: Literal marker text disables classification of an arbitrary inline shell program. This affects generated evidence and conformance; it is neither authorized runtime-assembly residue nor prose-only RESIDUE.

Required outcome: Bind runtime allowances to expression provenance and required declarations, never a substring. Literal inline programs must match their exact-text entry or refuse. Add this control alongside changed-inline and literal-dollar controls.

Verification: `literal-inline-marker` must refuse the unpinned program. Review-pinned inline programs and legitimate declared runtime values retain their distinct documented behavior.

[R639] R639-4-F4 MAJOR Conformance, Robustness, Tests, Docs - `scripts/ci_command_table.py:171`; `docs/testing/CI_IMAGE.md:29`, `:103` - Literal local package imports escape traversal and capability detection.

Authority/evidence: The guide follows local imports; the ruling requires declarations for executing/network-capable followed Python files. Lookup checks only `<module>.py`, not package initialization. An undeclared `bootstrap.py` containing `import json`, alongside local `json/__init__.py` containing `subprocess.run(["brand_new_command"])`, passes without residue. Actual Python imports the local package and executes the command. The initializer is absent from inputs and needs no declaration.

A second case uses `import localpkg` and a content-pinned declaration for the importing file. `localpkg/__init__.py` is still unvisited/unpinned. Neither case uses dynamic imports, attribute lookup or command construction.

Impact: An allowed external-import name can hide literal local execution. Package edits need not invalidate recorded inputs, and pinning only the importer does not protect the executing file.

Required outcome: Resolve local package initialization/imports within the supported subset or explicitly refuse unsupported package/shadowing forms. The external-import table must not silently override an existing local package. Require declarations for reached executing files.

Verification: `literal-python-package` and `literal-shadow-package` must refuse the unknown execution or unsupported import. Preserve clean external-import and local-module controls.

The ten independent fixtures contain nine demonstrated escapes and one clean Make-selection counterpart. The clean counterpart does not execute its unselected command and is not a finding. No new SUGGESTION or prose-only RESIDUE downgrades these defects.

**Verified evidence**

| Area | Result and examined artifacts |
|---|---|
| Current inventory | Baseline `--check` passes. All 45 tool/pin/installation-provenance records equal `e6b86814`; 328 inputs and 269 located residue entries. `evidence-verification.json`, `reference-ci_tool_inventory.log`. Future literal forms remain blocked by F1-F4. |
| Controls | Both inventory suites pass under 3.12.3: prior command/subcommand, positional/keyword/alias/network, Make selection/pattern, shell-directory, reusable-job, image-digest, unknown-command and changed-declaration forms rerun. Independent actual CLI missing/orphan/new-install controls pass. `reference-ci_inventory_patterns_selftest.log`, `reference-ci_tool_inventory_selftest.log`, `drift-controls.json`. |
| Recipe/pins | Digest-pinned base, multi-stage recipe, allowlisted context, offline build, exact versions/sizes/checksums. All 665 source/package archives used for inspection authenticated before use. `Dockerfile`, `build.py`, `install.py`, `sources.lock.json`, `image-authentication.json`. |
| Layers/lock | One base plus 13 tool-group layers; separate Python/LiteX. Actual member populations inspected; recipe records recomputed and compressed/uncompressed digests bound to export. `export-population.json`, `image-authentication.json`, `reference-integrity_selftest.log`. |
| Cold reproduction | Both published exports directly hash to `612e003a3920e6b70bb48704d9c33e9a9aabca8b15d0697715878cc2a11a2745`; manifest/config/all 14 layers match. Both public metadata records request no-cache and network none; recipe input hashes equal this head. `image-authentication.json`, `evidence-verification.json`. Inspected author builds, not reviewer rebuilds. |
| Privacy | All 45,119 members, including 37,763 regular files, and 27 untruncated history entries examined. Config/labels/environment/member metadata scanned. No forbidden build-context roots. Exactly 526 authenticated upstream allowances, one with reproduced patch provenance. `image-config-history.json`, `image-provenance.json`, `image-authentication.json`, `export-population.json`. |
| Privacy controls | Protected OCI surfaces, unknown/modified/first-party files, corrupt archives, patch-added identity and changed-patch controls pass. Fixture commits supply identity with global/system identity disabled. `reference-privacy_selftest.log`, `reference-privacy_patch_selftest.log`. |
| CPU sources | Six pinned archives reconstructed; committed CPU patch replayed independently with Git. All 4,550 installed files/links and execute-bit states equal expected. `audit-export.py`, `export-population.json`. |
| Versions/smoke | Public final-image smoke uses network none and returns zero in 37.021 seconds; all version/functional families pass. Embedded smoke/source lock equal this head. Accepted runner differences and reference 3.12.3 match ruling/runner manifest. `evidence-verification.json`, public `author-r4/round4-rebuilt-image-smoke.log`. Full image execution was not repeated by reviewer. |
| Portability | Primary-404/corrupt-fallback controls pass; timestamped package fallbacks retained. Config digest comes from authenticated exported manifest. Public v0.38.0 metadata/build receipts agree. SDK HOME link and actual consumers documented. `reference-build_selftest.log`, public `round3-buildx.json`, `build.py:327`, guide Environment/adoption sections. |
| Bare-metal/docs | Zero findings over 1,318 first-party files; 738 controls pass. File-pinned masks retain wrong-file/appended-term refusals. Docs privacy/style/paths pass. `reference-check_baremetal_only.log`, its controls log, other reference gate receipts. |
| Public receipts | 248 selected public blobs authenticated by Git identity; 28 final source/Markdown/image/lock logs checked against recorded hashes and zero statuses. These remain author evidence. `public-evidence-fetch.json`, `evidence-verification.json`. |

Authenticated manifest: `sha256:86d7aa16e7d2464baf8e0d246434982838c8174de8c8fa610608cce5b23b5e6c`. Configuration: `sha256:62b56e1ab52dce1a1914e8469429c014e69a465e74e0bdb9a7d8bf4a626b2776`. Recipe: `e689418be8fe7e7857c291d940d96d1edfedf5958879431bfe3fcece5a3728c7`. Public size: 3,931,071,698 bytes; cold build times: 400.411 and 436.056 seconds. Cross-host and registry-round-trip reproducibility remain unproved.

**Builder evidence and skips**

The exact main-loop AST defines 103 invocations. Nine accepted group records cover each exactly once at SHA-256 `997e8528ba47199a25376256f1614430586ae574e56db3470c0feeaa706a5c47`, equal to this head. Returned names equal assignments; accepted receipts are zero and include `--require-rv32`. Group 1 uses the corrected completed 1,014.708-second receipt, not earlier timeouts/setup failure. All 12 non-validation tool layers remain byte-identical to round two. This is historical grouped author evidence, not a current source-head bank or merge-candidate execution.

The [current-dev hosted docs-check log](https://github.com/kebag-logic/milan-fpga/actions/runs/38584726767/job/115923539474), at `113493920448a8fe6cebd7988408f071b99894c8`, explicitly takes the same `MAKEFLAGS += -e` skip. Its [runner manifest](https://github.com/actions/runner-images/blob/ubuntu24/20261004.327/images/ubuntu/Ubuntu2404-Readme.md) and the image both have make `4.3-4.1build2` / GNU Make 4.3. No image-induced coverage loss is shown. `evidence-verification.json` retains the excerpt/version comparison. The mf48 skip is accepted under the ruling; neither skip is hardware proof.

**Prior finding dispositions**

Prior comments were read after the independent verdict/ledger: R638-1 `6162177267`, R639-1 `6162055584`, R638-2 `6167893456`, R639-2 `6166908258`, R638-3 `6170421890`, R639-3 `6169543700`.

| Prior IDs | Disposition | Cause-level evidence |
|---|---|---|
| R639-1-F1 / R638-1-F2 | Resolved for measured same-host reproduction | Deterministic epoch/revision/ownership/trust-store; directly hashed identical cold exports. |
| R639-1-F2 / R638-1-F3 / R639-2-F1 / R638-2-F1 / R638-3-F1 | RETAINED as F1-F4 | Previously listed forms refuse or record image digests, but literal omissions still violate the closed traversal rule. |
| R639-3-F1 | Listed cases resolved; selection cause retained as F2 | Alternate-file/default/pattern controls pass; selected interpreter omitted. |
| R639-3-F2 | Literal unpacking defect resolved | Detection precedes decoding; undeclared and declared `**args` controls pass. F4 is a separate import gap. |
| R639-3-F3 | Listed cases resolved; scope cause retained as F1 | Step-directory/subshell controls pass; source/background/function controls fail. |
| R638-3-F2 | Location heuristic removed | No `/tmp` exemption remains. Reviewer scratch controls pass; authenticated public default-temp and `/tmp/checkout` receipts pass. Reviewer created no fixtures outside packet scratch. |
| R639-1-F3 | Resolved | Full schema/per-layer recomputation; separately authenticated export and corruption controls. |
| R639-1-F4 / R638-1-F1 | Source defect resolved | Narrow masks, zero findings and 738 controls; hosted/act acceptance separate. |
| R639-1-F5 / R638-1-F6 | Resolved | Actual separated layers and compressed/uncompressed bindings. |
| R638-1-F4 | Resolved under version ruling | Documented deviations, independent runner manifest, public binary checks and reference Python; adoption separate. |
| R638-1-F5 | Resolved under privacy rulings | Direct export/history/config inspection; authenticated upstream/patch allowances and controls. |
| R638-1-F7 | Resolved | Worker override absent; eight ENV entries match documented consumers. |
| R638-1-F8 | Resolved | Reconstructed CPU-tree equality; documented offline `ci_litex_env.py --check` adoption. |
| R638-1-F9 | Resolved | Unique temporary downloads; ten forced concurrent duplicate-download controls pass. |
| R638-1-F10 | Resolved | Consumer-checked roots, authenticated closure generators, missing-consumer control and public final-image closure pass. Host package tooling was not installed. |
| R638-1-R1 | Resolved | Buildx, builder storage and parser/host prerequisites documented. |
| R638-2-F2 | Source defect resolved | Timestamped fallback with original digest/size; 404/corrupt controls. Not every endpoint redownloaded this round. |
| R638-2-F3 | Resolved | Exported manifest config source; public completed v0.38.0 builds without old key. |
| R638-2-F4 | Resolved | Disposable identity supplied; identity-free reference controls pass. |
| R638-2-F5 | Resolved | Job-user SDK link and real override consumers documented. |

Optional suggestions remain optional: working-root privacy rules and registry-digest verification remain recommendations. The table's `installer_forms` field is now consumed. No optional item clears F1-F4.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN, F1-F4 | Public rulings; workflow/installer pins; recipe/locks/export; reference traversal probes | R639-4 | e355f789b4f59b86083809299134557ca47bbcfb |
| RTL | CLEAN | Full diff/gitlinks; Dockerfile/install.py; export-population.json; CPU source/patch equality and compile settings | R639-4 | e355f789b4f59b86083809299134557ca47bbcfb |
| Robustness | UNCLEAN, F1-F4 | Shell/Make/Python probes; source/hash/schema/privacy/patch controls; reference-focused-results.json | R639-4 | e355f789b4f59b86083809299134557ca47bbcfb |
| Tests | UNCLEAN, F1-F4 | Both inventory suites; CLI/real-execution probes; public smoke/exact-cover builder receipts; bare-metal controls | R639-4 | e355f789b4f59b86083809299134557ca47bbcfb |
| Docs | UNCLEAN, F1-F4 | CI_IMAGE.md census/refusal claims; rebuild/privacy/environment/adoption instructions; PR description/public evidence | R639-4 | e355f789b4f59b86083809299134557ca47bbcfb |

[R639] PASS RTL - `ci/image/Dockerfile`, `ci/image/install.py`, `export-population.json`, `final-tree.json` - Checked tool-stage architecture, actual layers, workflow compilation settings and installed CPU source/patch closure. No product RTL/interface, firmware, workflow or gitlink changes. This is bounded source/artifact review, not product regression execution.

**Limits, reproduction and pending duties**

The later Docker/privilege prohibition was honored. Direct archive inspection supplied image/history/layer evidence without daemon access. No reviewer cold build or full-container smoke occurred. Published smoke supplies image execution; extracted authenticated CPython 3.12.3 supplies reviewer controls using host system libraries, not container-runtime equivalence. Initial controls used host 3.14.7; all final focused checks and probes were repeated under 3.12.3.

No full parent/processor/gPTP/synthesis/builder bank, host runner self-test, hardware, shared install, Docker/act command, image pull/push/login, source fix, commit, push, merge, GitHub write, author contact or sub-agent was used. Commands remained foreground-owned, with at most eight fetch workers or four test workers. Disposable trees, exports, pins and interpreter files stay under packet `scratch/`. An initial reviewer population-audit assertion included unrelated source-parent rows and stopped before inspection; the corrected scoped audit completed and is the cited result.

Reproduction scripts are included. `run-focused.py <checkout>` uses the pinned parser at `$PACKET/scratch/shfmt`. `fetch-evidence.py` retrieves pinned public executable evidence. `inspect-image.py <checkout> <published-export-root> <public-source-work>` authenticates exports/pins before inspection. `extract-python.py <checkout>` and `run-reference.sh <checkout>` repeat reference checks. `probe-drift.py`, `probe-traversal.py`, `audit-export.py`, `verify-evidence.py` and `verify-tree.py` each take the checkout path. A probe's zero status means reproduction of the observed defect, not product approval.

`final-tree.json` directly verifies 1,344 superproject tracked blob bytes/modes, exact index equality, all six gitlinks and bytes/modes/indexes of all four initialized submodules. Two uninitialized submodules remain so with gitlinks verified. Status is clean; no tracked restoration was needed. Full diff SHA-256: `1bc8ca623b41b89e1f6c8abdd25fe55ad9e75068e13dd1c81f2c8c2b4f97755b`.

No manager source bank exists at this head and none is inferred. Source base: `fa7347fc59173f90e4feec2df207692e6e6e72ec`; assigned live dev: `113493920448a8fe6cebd7988408f071b99894c8`. The manager still owns current-dev candidate builder/native validation and linked receipts, hosted/act acceptance, full switch-lane adoption, independent review completion, publication/registry-digest verification, authorized merge and containment. No exact-head hosted aggregate verdict is claimed. Physical calibration/field skips supply no hardware proof.

Fix and independently re-review F1-F4 before acceptance. Publish only REPORT.md and MANIFEST.sha256-listed files; scratch is never published.

R639-4 FINISHED
