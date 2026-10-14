[R639] NEGATIVE - exact head e6b86814e6844ef61ba46a867a0fdbfbb925cceb

External independent review, round R639-3, issue #737 / PR #738. Tree: `7e566e139576b082580ab07e334a62ffa1b881f7`. Full source range: `fa7347fc59173f90e4feec2df207692e6e6e72ec..e6b86814e6844ef61ba46a867a0fdbfbb925cceb`; round-three delta: `18f2df92..e6b86814`, three commits. All five lenses were applied. Three MAJOR findings remain; this is not approval for publication or merge.

Authorities were reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue body and public manager decisions, REQUIREMENTS.md REQ-VER-03/04, workflow installation steps and their scripts. Principal decisions: [image assignment](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160953880), [version and mask ruling](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6162190578), [privacy](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6162652582), [patch provenance](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6163057631), [round-three class ruling](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6167899804), and [script-declaration amendment](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6167966247). Workflow adoption and the later signature/trigger scope belong to the separate switch lane.

The independent diff-pass verdict and ledger were written to `independent-pass.md` before reading prior public review findings. No private author reasoning, lane handoff, management checkout, or current-round reviewer report was used. Execution records came from the [public evidence commit](https://github.com/kebag-logic/milan-fpga/tree/d7f2e7f19fb1fbe66d81635ae09eb30c61aee89e/review-evidence/737-image-r1), verified against their Git blob identities. The locally available image exports and their checksum-bound public source archives were read solely as build artifacts.

**Open findings**

[R639] R639-3-F1 MAJOR Conformance, Robustness, Tests, Docs - `scripts/ci_command_table.py:398`, `:475`, `:482`; `docs/testing/CI_IMAGE.md:24` - Makefile traversal accepts a different command population from the one make executes.

Authority/evidence: The class ruling requires every followed Makefile target's commands to be classified, with unresolved paths refused. `probe_inventory.py` produces these independently verified outcomes under CPython 3.12.3:

| Literal input | Actually selected recipe | Deriver result |
|---|---|---|
| `make --file=install.mk` | `install.mk`, containing an unclassified command | Reads benign `Makefile`; accepts |
| `make -finstall.mk` | Same alternate file | Reads benign `Makefile`; accepts |
| `make`, with `.DEFAULT_GOAL := install` after a benign first target | `install` | Reads the first target; accepts |
| `make install`, with a `%:` rule | Pattern recipe containing the unclassified command | Silently ignores the unmatched target; accepts |

Every fixture regenerates `tools: []`, records no residue, returns zero from `--write`, and then returns zero from `--check`. Independent `make -n` output names `brand_new_command install tool` in each case; no planted installation was executed. Raw evidence: `inventory-probes.json`, `reference-probe_inventory.log`. The supplied inventory self-test remains green.

Impact: A literal build recipe can install an unrecorded tool while generation and comparison both pass. This is a missing-command guard, not a claim that current workflows already use the planted form. Literal option/default/rule selection does not assemble a command at runtime and is not the accepted residue class.

Required outcome: Follow the selected file and effective target semantics, or explicitly refuse unsupported selection/rule forms before generating an inventory. Do not silently substitute another file or discard a target. Add generation-then-comparison controls that fail on these cases; preserve current inventory controls and the documented closed-table guarantee.

Verification: Rerun `probe_inventory.py <checkout>` under the reference interpreter. Each unclassified command must be refused by name, or reached and classified through an explicit installer declaration. The four currently empty passing inventories must disappear.

[R639] R639-3-F2 MAJOR Conformance, Robustness, Tests, Docs - `scripts/ci_command_table.py:160`, `:163`, `:171`; `docs/testing/CI_IMAGE.md:30` - Literal keyword unpacking bypasses the executing-script declaration requirement.

Authority/evidence: The amendment requires any followed Python script running subprocesses to have a content-pinned declaration. An undeclared root `bootstrap.py` containing `import subprocess` followed by `subprocess.run(**{"args": ["brand_new_command", "install"]})` passes generation and comparison with no tool and no residue. The equivalent positional list is refused. The walker recognizes the executor but records it only when a positional argument or an explicit `args=` keyword exists; a literal `**` dictionary leaves `calls` empty, bypassing declaration enforcement entirely. Evidence: `reference-probe_inventory.log`, case `python-literal-kwargs`.

Impact: An ordinary argument-binding change removes both command classification and script hash protection. No string building, lookup, eval, or indirect shell is involved. Even an unresolved argument must not erase the separately required executing-script declaration check.

Required outcome: Require the declaration for every detected subprocess call independently of argument decoding. Classify the literal unpacked command or refuse its unsupported form. Add an undeclared-script control and a declared-script command-classification control for this path.

Verification: The undeclared fixture must refuse; after a valid content-pinned declaration, its literal unclassified executable must still refuse. Keep positional, explicit-keyword, network-import, and changed-declaration controls passing.

[R639] R639-3-F3 MAJOR Conformance, Robustness, Tests, Docs - `scripts/ci_tool_inventory.py:193`, `scripts/ci_command_table.py:228`; `docs/testing/CI_IMAGE.md:24` - Working-directory handling follows the wrong script.

Authority/evidence: The ruling requires every executed script to be followed. Two literal fixtures pass both CLI modes with empty tools and no residue:

- A step specifies `working-directory: subdir` and runs `bash bootstrap.sh`. The deriver reads the benign root script instead of `subdir/bootstrap.sh`, which contains the unclassified command.
- `(cd subdir); bash bootstrap.sh` executes the root script, but the flattened shell traversal leaks the subshell's directory into the parent and reads the benign subdirectory script instead.

Both files exist, so these are incorrect positive resolutions, not missing-path refusals. `reference-probe_inventory.log` records the selected inputs. Commands and paths are literal and within the fixture tree.

Impact: The inventory hashes and classifies a script that the workflow does not execute; the actual installer can remain unrecorded. The docs' followed-script guarantee and corresponding self-test coverage are incomplete.

Required outcome: Respect workflow/job/step working-directory selection and shell directory scope, or refuse unsupported cases before generation. Follow the actual script; fail by name when resolution cannot be established. Cover both cases with generation/comparison controls.

Verification: Each planted executable must be reached and refused, with no successful empty inventory. A clean counterpart using the actual selected script must remain accepted.

**Verified acceptance evidence**

| Area | Reviewer result and artifacts |
|---|---|
| Prior reported inventory forms | All ten R638-2 forms and all four R639-2 forms are now refused or digest-recorded. Unknown-command, new classification/subcommand, undeclared-network, changed-script, missing-script, missing-entry and orphan-entry controls pass. `prior-form-controls.json`, `reference-verify_controls.log`, supplied `reference-inventory-selftest.log`. The broader cause remains open as F1-F3. |
| Recipe and architecture | Multi-stage, digest-pinned base; allowlisted build context, checked sources, no-network build command; one base plus 13 tool-group layers. Python and LiteX are separate. `ci/image/Dockerfile`, `install.py`, `build.py`, `image-inspection.json`. No workflow or product RTL/interface change. |
| Reproducibility | Both public metadata records request `no-cache` and network `none`; manifest, config and all 14 compressed/uncompressed layer identities agree with the lock. Both locally present cold export files independently hash to `5cca62849d40392fd3e24c0383d3888c2a0454c13e112c2f63f2a6162a91c53e`. `evidence-verification.json`, `image-inspection.json`, `second-export.json`. No new reviewer cold build is claimed. |
| Lock authentication | Independently read and authenticated the actual export's manifest, configuration and every layer/diff-id against the current recipe/lock. Supplied corruption/schema/source/version controls pass. `image-authentication.json`, `reference-lock-check.log`, `reference-integrity-selftest.log`. |
| Privacy | Inspected all 45,119 layer members, including 37,763 regular files, all 27 untruncated configuration history entries, member metadata, labels and environment. No prohibited context/source-build leftovers; 38 oracle regular files. All 526 allowances authenticated against pinned public archives; patch provenance and added-identity controls pass. `image-history.json`, `image-authentication.json`, `image-inspection.json`, `reference-privacy-selftest.log`, `reference-patch-selftest.log`. This was direct archive inspection, not a daemon history command. |
| CPU source tree | Independently reproduced the six public recursive archives and applied the committed CPU patch with Git. All 4,550 files/links and execute bits equal the installed tree. `cpu-tree-verification.json`, `cpu-tree.log`. |
| Tool versions and offline smoke | Published final-image smoke returns zero with network disabled; its manifest equals the authenticated export, and the exported smoke program/source lock equal this head byte-for-byte. The log records CPython 3.12.3, version checks and all functional smoke families. Accepted runner deviations are documented. `evidence-verification.json`, `public-fetch.json`, public `round3-smoke-0.log`. Full smoke execution was not repeated by this reviewer. |
| Reference interpreter | Extracted only authenticated interpreter/library regular files into disposable scratch, without links/devices or privilege. Reviewer controls and independent probes were repeated with actual CPython 3.12.3. This is an extracted interpreter using host system libraries, not a container-runtime equivalence claim. `reference-python-extraction.json`, `reference-checks.json`, `reference-runs.json`. |
| Minor portability fixes | All 185 published snapshot download records match locked URL/size/hash. Primary-404 fallback and corrupt fallback controls pass. Both public builds completed with buildx v0.38.0 while omitting the old config metadata key; config identity now comes from the authenticated manifest. The patch self-test passes with global/system Git identity disabled. `evidence-verification.json`, `reference-build-selftest.log`, `reference-patch-selftest.log`. |
| Bare-metal masks | File-pinned literal masks preserve wrong-file/appended-term refusals. Zero findings over 1,315 tracked first-party files; all 738 controls pass. `baremetal-scan.log`, `baremetal-controls.log`, `reference-baremetal-check.log`. |
| Docs and adoption | Rebuild, digest consumption, normalization, privacy, snapshot refresh, builder setup and SDK HOME-link instructions checked. Actual `MILAN_RV32_CC` consumers match the guide. The inventory claims remain unclean under F1-F3. `docs/testing/CI_IMAGE.md`, `fw_rv32.py:31`, `test_builder.py:4768`. |

Authenticated manifest: `sha256:86d7aa16e7d2464baf8e0d246434982838c8174de8c8fa610608cce5b23b5e6c`. Configuration: `sha256:62b56e1ab52dce1a1914e8469429c014e69a465e74e0bdb9a7d8bf4a626b2776`. Recipe: `08fe0f5bdedde8382351617017df7af89055b106af11e3946966845dc0ca906e`. Published image size: 3,931,071,698 bytes; build times: 434.933 and 398.716 seconds. These are author timing measurements. Cross-host reproducibility is not proved.

**Builder evidence and skips**

`verify_evidence.py` derives the 103 invocation names from the exact source's main-loop AST. Nine groups contain every invocation exactly once, with matching returned names and source SHA-256 `997e8528ba47199a25376256f1614430586ae574e56db3470c0feeaa706a5c47`. Each accepted group receipt has rc 0 and `--require-rv32`. Group 1 uses the corrected completed background receipt, not its earlier timeout or setup failure. Its wall time is 1,014.708 seconds. These are historical grouped author executions on the round-two image; unchanged builder source does not turn them into a new source-head bank or current-dev candidate verdict.

The assigned [hosted docs-check job](https://github.com/kebag-logic/milan-fpga/actions/runs/38516575606/job/115696619496) at `fa8209889411e8ca95757174c981f720dbcd95a2` explicitly takes the same `MAKEFLAGS += -e` skip. Its pinned runner manifest and the image smoke log both identify make `4.3-4.1build2` / GNU Make 4.3. `evidence-verification.json` retains the relevant raw hosted excerpts and version comparison. No image-induced loss is demonstrated. The mf48 calibration skip is accepted under the manager ruling; neither it nor field/physical skips supplies hardware proof.

The public final-image source receipts include successful inventory, privacy, patch, package-closure and documentation checks. The earlier non-root smoke failure is superseded by the published successful offline smoke; the host package-closure failure is superseded by the image package-closure pass. These failed attempts are not counted as successes. The reviewer's initial bare-metal invocation omitted its required mode and returned usage status 2; the corrected `--check` and reference-interpreter repeat both pass.

**Disposition of prior public findings at this head**

| Prior IDs | Disposition | Cause-level evidence |
|---|---|---|
| R639-1-F1 / R638-1-F2 | Resolved for same-host reproduction | Normalized epoch/revision/ownership/trust-store; cold metadata and two directly hashed identical exports. |
| R639-1-F2 / R638-1-F3 / R639-2-F1 / R638-2-F1 | RETAINED as R639-3-F1-F3 | Prior examples pass their required controls, but the closed-command requirement still fails on literal paths/arguments/targets. |
| R639-1-F3 | Resolved | Full schema and per-layer recipes recomputed; actual export separately authenticated. |
| R639-1-F4 / R638-1-F1 | Resolved source defect | Literal masks, zero scan findings, 738 passing controls; manager acceptance duties remain separate. |
| R639-1-F5 / R638-1-F6 | Resolved | Separate Python/LiteX layers and actual compressed/uncompressed layer bindings. |
| R638-1-F4 | Resolved under public version ruling | Explicit accepted deviations and reference CPython; published binary checks. Full workflow adoption still belongs to switch lane. |
| R638-1-F5 | Resolved under privacy rulings | Direct complete archive/config/history inspection, authenticated upstream/patch allowances and refusal controls. |
| R638-1-F7 | Resolved | Worker override absent; actual environment matches documented consumers. |
| R638-1-F8 | Resolved | Direct 4,550-member CPU-tree equality, recursive archives, committed patch; adoption location instructions present. |
| R638-1-F9 | Resolved | Unique temporary downloads; ten concurrent duplicate-download controls pass. |
| R638-1-F10 | Resolved | Consumer-checked roots and checksum-verified package/Scala closure generators; published final-image package closure passes. |
| R638-1-R1 | Resolved | Guide pins buildx, parser and supporting host prerequisites and names the supported builder setup. |
| R638-2-F2 | Resolved | Ordered timestamped fallback, 185 matching retained downloads, 404/corruption controls, regeneration/mask instructions. |
| R638-2-F3 | Resolved | Authenticated exported config identity; two completed v0.38.0 builds without the removed metadata key. |
| R638-2-F4 | Resolved | Disposable identity supplied by both commits; reviewer identity-free controls pass; public image control also passes. |
| R638-2-F5 | Resolved | Documented job-user SDK link and correct override consumers; published link preflight passes. |

Optional prior suggestions remain optional. No new RESIDUE is used to downgrade these defects; they affect generated inventory and test/verdict behavior. Runtime-built command names, eval/getattr and indirect shells retain the expressly accepted analysis limit documented in the guide.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Assignment/rulings; workflow installs; recipe/lock/export; `reference-probe_inventory.log`; F1-F3 | R639-3 | e6b86814e6844ef61ba46a867a0fdbfbb925cceb |
| RTL | CLEAN | Full diff/gitlinks; `Dockerfile`; `install.py`; authenticated layers; `cpu-tree-verification.json`; no product interface or compile-setting change | R639-3 | e6b86814e6844ef61ba46a867a0fdbfbb925cceb |
| Robustness | UNCLEAN | Literal traversal probes; corrupt-source, concurrent-download, privacy, patch and schema controls; F1-F3 | R639-3 | e6b86814e6844ef61ba46a867a0fdbfbb925cceb |
| Tests | UNCLEAN | Supplied and independent controls; exact-cover builder audit; public offline smoke and hosted skip; F1-F3 | R639-3 | e6b86814e6844ef61ba46a867a0fdbfbb925cceb |
| Docs | UNCLEAN | `CI_IMAGE.md:24-39`; rebuild/privacy/environment/adoption sections; public receipts and prior findings; F1-F3 | R639-3 | e6b86814e6844ef61ba46a867a0fdbfbb925cceb |

[R639] PASS RTL - `ci/image/Dockerfile`, `ci/image/install.py`, `image-inspection.json`, `cpu-tree-verification.json`, `final-tree.json` - Tool-stage architecture, installed CPU sources and workflow compilation settings were checked against the authorized image contract. No RTL, firmware, interface, workflow or gitlink change occurs. This is bounded source/artifact review, not a full product regression or hardware verdict.

**Limits, integrity and pending duties**

The assignment both required Docker inspection and later prohibited Docker/privilege. The prohibition was honored: no Docker, act, privilege, host runner self-test, shared install, hardware, full parent/processor/gPTP/Yosys/builder bank, source fix, commit, push, login, merge, GitHub write, author contact or delegated review occurred. Archive inspection supplies the image/history/privacy evidence without daemon access. Published execution receipts supply full offline smoke; extracted CPython supplies reviewer reference-interpreter controls. No independent full-container execution or new cold build is claimed. All processes were foreground-owned and completed; concurrency stayed below 16 jobs. Disposable data is confined to this packet's `scratch/`.

`final-tree.json` verifies all 1,341 tracked superproject blob bytes and modes, exact index equality, all six gitlinks and the complete tracked bytes/modes/index of the four initialized required submodules. The two initially uninitialized submodules remain so. Worktree status is clean. Full diff SHA-256: `7ee7283243679026138356b9879236654ca7534cb562123c17ff66ac6c831f8b`.

No manager source bank exists at this head and none is inferred. The manager still owns final hosted/act acceptance, current-dev merge-candidate builder/native validation and linked receipts, switch-lane full workflow adoption, independent review completion, registry publication/digest verification, authorized merge and containment. No completed exact-head hosted verdict is claimed by this review. The three open MAJOR findings require fixes and re-review before acceptance.

Portable scripts accept the checkout and, where relevant, an exported-image work directory. `fetch_public.py` and `fetch_hosted.py` retrieve the named public evidence; `verify_evidence.py` checks it without executing the bank. `inspect_export.py` and `verify_cpu_tree.py` inspect an existing export/cache read-only. `extract_reference_python.py` and `run_reference.py` reproduce the focused reference-interpreter probes. `verify_tree.py` performs the final integrity check. Publish only REPORT.md and files listed in MANIFEST.sha256; scratch exports, downloads and temporary trees are excluded.

R639-3 FINISHED
