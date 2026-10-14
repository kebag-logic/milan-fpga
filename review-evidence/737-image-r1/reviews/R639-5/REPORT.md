[R639] NEGATIVE - exact head 4391f353690972f4844cb641b1e77fa94f38cdf4

External independent review of issue #737 / PR #738, round R639-5. Two MAJOR findings remain. All five lenses were applied. RTL is CLEAN; Conformance, Robustness, Tests and Docs are UNCLEAN. This verdict does not authorize publication or merge.

Tree: `f2882c85eb46b66b35cdec6e69861849af690f4b`. Full review range: `fa7347fc59173f90e4feec2df207692e6e6e72ec..4391f353690972f4844cb641b1e77fa94f38cdf4`; round-five delta: `e355f789..4391f353` (eight commits). The complete diff, not only the last delta, was reviewed. It changes no workflow, RTL, firmware or submodule gitlink.

The contract was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, issue #737 and its public decisions, linked requirements/interface authorities, then the diff/history and public executable evidence. The independent findings and ledger were written in `independent-pass.md` before prior public review findings were read. The reconciliation below was performed afterwards. No private author material or unpublished reviewer report was used.

Authority: [frozen lane assignment](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160953880), [round-five assignment](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6173370560), [standing census rule](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6170640746), [privacy scope](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6162652582), [patched-upstream rule](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6163057631), and [author ready evidence](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6175914084). The source review does not substitute for the manager's current-dev merge-candidate validation.

[R639] R639-5-F1 MAJOR Conformance, Robustness, Tests, Docs — `scripts/ci_make_walk.py:387`; `docs/testing/CI_IMAGE.md:88`, `:99`, `:129` — Target-specific assignments incorrectly defeat command-line assignments.

Authority/evidence: supported Make constructs must have Make's real semantics, and every reached command must be classified or refused. With the committed census and command table copied without modification, use this workflow command and Makefile:

```sh
make SCRIPT=hidden.sh
```

```make
all: SCRIPT=benign.sh
all: ; bash $(SCRIPT)
```

`benign.sh` contains `echo okay`; `hidden.sh` contains the unclassified sentinel `brand_new_command`. Both inventory `--write` and `--check` return 0 with no tools. The walker unconditionally overlays target-specific variables onto the command-line values and visits `benign.sh`. The image's extracted GNU Make 4.3 instead executes `bash hidden.sh` and reaches the sentinel (Make exits 2 after shell status 127). This is fully literal input using accepted syntax. It is not runtime-assembled residue. The passing shipped suites do not cover this precedence composition. Receipts: `independent-probes.json`, case `make_target_override`; portable driver `probe-independent.py`.

Impact: an accepted Make recipe can install a tool which the generated inventory never examines. Regenerating and then checking the inventory does not detect the omission. The guide's supported-semantics guarantee is false for this case; this is a behavioral/conformance claim, not wording residue.

Required outcome: preserve command-line precedence for supported target-specific assignments, including their propagation to prerequisites, or explicitly refuse combinations the walker cannot resolve. Do not bank coverage by changing the guide alone.

Verification: both generation and comparison must refuse `brand_new_command` by name in this fixture, or refuse the unsupported construct before generation. Add positive and negative precedence controls, comparing the resolved command with GNU Make 4.3. Re-run the current inventory, missing/orphan controls, structural suites and required source gates.

[R639] R639-5-F2 MAJOR Conformance, Robustness, Tests, Docs — `scripts/ci_make_walk.py:405`; `scripts/ci_command_table.py:140`; `docs/testing/CI_IMAGE.md:73`, `:84`, `:129` — Traversal caches discard the incoming environment and skip a different command population.

Authority/evidence: literal command/environment values must be resolved and every reached invocation classified. These two independent fixtures retain the committed census/table:

```sh
TOOL=echo make; TOOL=brand_new_command make
```

```make
TOOL ?= echo
all: ; $(TOOL) okay
```

and:

```sh
TOOL=echo bash bootstrap.sh; TOOL=brand_new_command bash bootstrap.sh
```

where `bootstrap.sh` contains `"$TOOL" okay`. For each fixture, both inventory modes return 0 with no tools. Real Make 4.3 / Bash reaches the unclassified sentinel on the second invocation. The Make traversal key includes file/directory/targets/command-line overrides but omits exported values; the script key includes only relative path and working directory. The second walk is therefore skipped despite a different, fully literal input environment. Receipts: `independent-probes.json`, cases `make_environment_memo` and `shell_script_environment_memo`.

Impact: a repeated supported script or Make target can execute an unclassified installer after an earlier harmless invocation, without changing the census or command table and without causing either inventory mode to fail. The current control suites pass despite the omission. The scope/environment claims in the guide do not hold across repeated invocations.

Required outcome: traversal deduplication must preserve every semantically distinct incoming state, or a repeated invocation with unresolved/distinct state must refuse explicitly. Recursion prevention must not silently drop reachable command populations.

Verification: both fixtures must refuse the sentinel by name, or refuse the unsupported state combination before generation. Exercise repeated file/target visits under different literal environments and an unchanged-environment repeat. Preserve the existing source/cwd/function and recursive-Make controls.

Both findings retain the earlier inventory cause class. No actual defect has been reclassified as RESIDUE, and moving either finding to another issue would not clean its lenses.

| Acceptance area | Result and examined evidence |
|---|---|
| Derived inventory / closed census | Baseline passes under extracted CPython 3.12.3. All 45 tool/pin/installation-provenance records equal `e6b86814`. Actual missing, orphan and changed-pin controls refuse drift. All three shipped inventory suites pass. Independent uncensused shell `CoprocClause`, Make `.ONESHELL`, Python `AsyncFunctionDef`, nested trap, startup-variable and sourced-file controls refuse. Nevertheless F1/F2 silently accept misresolved literal commands, so the required closure property is not met. `reference-focused-results.json`, `drift-controls.json`, `independent-probes.json`, `inventory-and-builder-proof.json`. |
| Former blocking source gates | Entity shape self-test: 228 checks, zero failures. Protocol-processor source-list check/self-test: 46-source derived population, pass. The command table now uses typed HDL data operands instead of frozen source copies; the population/data-operand controls pass. `entity-shape.log`, `pp-sources.log`, `reference-ci_inventory_nodes_selftest.log`, workflow-step receipts. |
| Pinned recipe and tool layers | Dockerfile multi-stage boundaries, digest-pinned base, exact artifact version/digest/size checks and installer checksum enforcement examined. Final export has 14 authenticated layers, including separate Python and LiteX layers and the Scala group. Lock records bind source/recipe identities and compressed layer digest plus uncompressed diff-id. `independent-exports.json`, `independent-image-audit.json`, `reference-integrity_selftest.log`. |
| Cold reproducibility | The two supplied final cold OCI exports were independently hashed: both 1,135,213,568 bytes, SHA-256 `725ba52e874f840e66272eae9ba0cbbbee872d407d389b2b463dd6e76e734c47`. Manifest `sha256:86d7aa16e7d2464baf8e0d246434982838c8174de8c8fa610608cce5b23b5e6c`; config `sha256:62b56e1ab52dce1a1914e8469429c014e69a465e74e0bdb9a7d8bf4a626b2776`. All 14 compressed and uncompressed layer identities agree. Public records identify sequential no-cache builds. This independently verifies the delivered bytes, not a third reviewer rebuild or cross-host reproducibility. |
| Recipe / census authentication | Recomputed recipe `214fefe3bd807c3403558de25d553d5a5a10f682a6bb5a824257f2a27ef192be` includes the current census, command table and walkers. Full lock/schema/layer reconstruction and tampering controls pass. A pin change changes recipe identity. `independent-image-audit.json`, `reference-integrity_selftest.log`, `reference-build_selftest.log`. Authentication binds these bytes; it does not establish correct traversal semantics. |
| Offline versions and smoke | Read the complete smoke implementation and authenticated public final-image receipt: 131 records, rc 0, network `none`, log SHA-256 `60fb30609a5949eb90af29c3f435ff2d1bb62aefd88af4a634901d23cf0a9206`. Independently extracted and executed CPython 3.12.3 and GNU Make 4.3 from authenticated layers. Documented runner/reference-version deviations follow the public ruling; the switch lane must adopt those pins. No new full container execution is claimed. |
| Privacy | Independently inspected full configuration/history and every layer, rather than only the flattened final filesystem: 27 history entries, eight environment entries and 45,119 layer members. The project identity scan authenticated 526 public-upstream allowances, including one reproduced patched postimage. No added patch line carried an allowed identity. Modified-source, first-party placement, embedded-wheel, metadata-surface, oracle-leftover and patch-added-identity controls pass. Member contents, links/metadata, labels and history were included. `image-config-history.json`, `independent-image-audit.json`, `image-population.json`, reference privacy logs. |
| Recursive CPU source population | Independently reconstructed six pinned public repositories and applied the committed patch. All 4,550 expected files/links and modes match the installed image population; zero mismatches. Embedded smoke/lock bytes match this head and recipe/build-context roots and oracle build leftovers are absent. `image-population.json`, `audit-population.py`. |
| Documentation and unchanged workflows | Rebuild prerequisites, digest pinning/consumption, source generators, privacy provenance, documented environment, `$HOME/br-milan-rv32/host` to `/opt/rv32-sdk` link and actual `MILAN_RV32_CC` consumers checked. Inventory semantics remain inaccurate through F1/F2. No workflow changed; image adoption remains the separate lane. |

The grouped builder evidence was checked as a set, not accepted merely because all group receipts say pass. The current main-loop source SHA-256 is `997e8528ba47199a25376256f1614430586ae574e56db3470c0feeaa706a5c47`; its 103 function invocations occur exactly once across nine groups at that same hash. The background completion receipt and recorded skips were examined. `inventory-and-builder-proof.json` records the exact-cover check. The grouped/background receipts use the round-two image/head with that unchanged source hash; they are not a full bank execution on the final image. This is the author's public source evidence, not a manager source-bank run.

The current-dev docs-check job [115980812751, run 38601263556](https://github.com/kebag-logic/milan-fpga/actions/runs/38601263556/job/115980812751), at `f62602531d415d6c1cae1374a3cc2938faf54049`, explicitly takes the same `MAKEFLAGS += -e` mutation skip. Its runner image `20261004.327.1` lists package `make 4.3-4.1build2`, the image's package version; the extracted executable reports GNU Make 4.3. This is not a new coverage loss. Receipts: `hosted-docs-log-proof.json`, `hosted-docs-excerpts.log`, `runner-make-proof.json`, `reference-make.json`. The mf48 resource-calibration skip needs the physical-tool build tree and is not a finding under the ruling. Neither skip establishes hardware correctness.

Reviewer workflow-step execution: the complete published docs-check (79 commands) and RTL-fast (36 commands) step plans were examined against `.github/workflows/docs.yml` and `.github/workflows/rtl-fast.yml`. The local run executed every available, permitted command in those plans, rather than selecting a passing sample. **76 docs commands and 21 RTL-fast commands passed.** Docs step 34 initially exhausted the review driver's 540-second limit; the unchanged compiler-absent command passed in 606.407 seconds with a 1,800-second limit. The initial timeout remains in the raw record and is superseded only by `compiler-absent-retry.json`. The retry used reference Python/Make with the inherited host tool path; it did not inject the scoped Verilator directory. Deliberate compiler absence and any listed elaboration stand-downs are not compiler or RTL coverage.

**18 commands were NOT RUN locally**, with per-command reasons retained: three docs commands (full builder and two prohibited orchestration self-tests); 15 RTL commands (four synthesis-bank commands and 11 native/RV32 commands requiring unavailable reference compiler/test dependencies or the full publication bank). Installation/setup actions requiring privilege or shared destinations were not replayed. Thus this is not a claim of a complete local workflow run. Published receipts for those commands were examined, and final candidate execution remains the manager's duty. The scoped Verilator executable was verified as 5.050 before the permitted checks. Local commands used the extracted CPython 3.12.3, GNU Make 4.3, packet-local temporary storage, and bounded job settings. See `docs-gate-results.json`, `rtl-gate-results.json`, `gate-logs/`, `reference-versions.json` and the retry receipt. The previously omitted public docs step 66 has a successful local raw log in this packet.

Public source receipts are separately identified in `public-gates-verification.json`: all 115 docs/RTL step records were examined; 114 public raw logs authenticate directly or through the publisher's explicit path-redaction map. The omitted docs step 66 log is identified by its published receipt and not represented as independently downloaded. Its reviewer execution appears separately in the local results. The published full docs run was at `605e312d`; RTL receipts span `8882ce17`, `605e312d` and `4d192b5d`. They are ancestor evidence, not an exact-head manager bank. Exact-head author blocker/final-control receipts are separate. The final-head scoped executions in this packet avoid borrowing ancestor review coverage.

| Prior public finding | Disposition at this head | Cause / evidence |
|---|---|---|
| R638-4-F1, blocking shape/source-list gates | Source defect resolved | Typed HDL operands replace frozen populations; both actual gates and data-population controls pass. Hosted/act acceptance remains separate. |
| R638-4-F2, interpreter/startup/path constructs | Listed escape causes resolved | Shell selection, startup variables, PATH/GITHUB_PATH/GITHUB_ENV and Make interpreter/flag overrides have exact census boundaries or refuse; all listed controls pass. |
| R638-4-F3, installer behind xargs | Resolved | Positive wrapper-child classification and exact-use boundaries refuse the installer fixtures; inventory node controls pass. |
| R638-4-F4, real-tool semantics | Listed examples resolved; cause retained as F1/F2 | Source side effects, read/printf-v, environment `?=`, automatic-directory modifiers, recursive overrides and literal markers now resolve or refuse. Target precedence and repeated incoming state still misresolve. |
| R638-4-F5, substring normalization | Resolved at the source/control level | Component-boundary normalization replaces substring root removal; `/src` and `/include` collision controls pass. No privileged alternate-root mount was performed. |
| R638-4-F6, Python execution/import gaps | Resolved for listed causes | Foreign-function capability detection and local member/initializer traversal controls pass, including undeclared capabilities and a declared importer with undeclared initializer. |
| R639-4-F1, source/background/conditional-function scope | Listed causes resolved; scope guarantee retained through F2 | Censused source effects apply in caller scope; background refuses; function alternatives are walked. Repeated-script incoming state remains omitted. |
| R639-4-F2, selected Make interpreter | Resolved | File/command-line SHELL and interpreter-selection overrides refuse before generation. This does not resolve F1's different precedence defect. |
| R639-4-F3, literal marker bypass | Resolved | Typed runtime values and exact inline hashes replace literal marker authorization; both listed controls refuse. |
| R639-4-F4, local package imports | Resolved | Local shadow packages, initializers and selected members receive traversal/capability checks; controls pass. |
| R639-1-F2 / R638-1-F3 / R639-2-F1 / R638-2-F1 / R638-3-F1 | RETAINED as F1/F2 | Prior individual forms refuse or record pinned image tools, but the closed-traversal cause is not eliminated. |
| R639-3-F1 | Listed forms resolved; broader Make selection cause retained as F1 | Alternate file/default-goal/pattern controls pass; target-specific precedence remains wrong. |
| R639-3-F2 | Resolved | Detection precedes decoding; unpacked-keyword declaration controls pass. |
| R639-3-F3 | Listed forms resolved; broader context cause retained as F2 | Step working directory and subshell directory controls pass; repeated incoming environment remains omitted. |
| R638-3-F2 | Resolved | Location heuristic removed; controls execute in packet scratch. No `/tmp` exemption remains. |
| R639-1-F1 / R638-1-F2 | Resolved for required same-host property | Independently identical final cold archives, manifest/config and 14 layers; deterministic normalization examined. |
| R639-1-F3 | Resolved | Full lock/schema/per-layer recomputation, archive authentication and tampering controls. |
| R639-1-F4 / R638-1-F1 | Source defect resolved | Narrow file-pinned TERM_MASKS; bare-metal gate and 738 controls pass. No gate weakened. |
| R639-1-F5 / R638-1-F6 | Resolved | Final Python/LiteX separation and measured per-group layer bindings. |
| R638-1-F4 | Resolved under public version decision | Documented accepted deviations, reference interpreter and runner/version evidence; adoption remains separate. |
| R638-1-F5 | Resolved under privacy rulings | Full layer/metadata scan and authenticated upstream/patch provenance controls. |
| R638-1-F7 | Resolved | Image-level worker override removed; remaining eight environment entries document their consumers. |
| R638-1-F8 | Resolved | Six-repository CPU reconstruction and 4,550 exact installed entries; placement/check instructions reviewed. |
| R638-1-F9 | Resolved | Unique temporary downloads and ten concurrent duplicate-download controls pass. |
| R638-1-F10 | Resolved | Consumer-derived package roots and authenticated distribution/Scala closure generators; missing-consumer control. Shared package tooling was not installed. |
| R638-1-R1 | Resolved | Guide includes buildx/storage/parser prerequisites. |
| R638-2-F2 | Resolved | Ordered timestamped snapshot fallback retains size/hash authentication; 404-primary and corrupt-payload controls pass. Not every remote endpoint was downloaded again. |
| R638-2-F3 | Resolved | Config digest comes from authenticated exported manifest; completed public buildx v0.38.0 records and final archive agree. |
| R638-2-F4 | Resolved | Patch controls supply disposable git identity; repeated with global/system identity configuration disabled, rc 0 (`patch-no-identity.json`). |
| R638-2-F5 | Resolved | SDK home link and real compiler-override consumers documented. |

Optional earlier suggestions remain optional. There are no new RESIDUE items. Refusal of unsupported forms is not a finding; only the accepted, incorrectly resolved fixtures above make this verdict negative.

[R639] PASS RTL — `git diff fa7347fc..4391f353`, `ci/image/Dockerfile`, `ci/image/install.py`, `scripts/pp_srcs.py`, `scripts/check_entity_shape.py`, `independent-exports.json` — No RTL/interface/workflow/gitlink change; tool build configuration and separated layer architecture checked against workflow/install contracts; both former blocking integration gates pass. This is scoped image/architecture coverage, not a claim that prohibited simulation/synthesis banks or hardware were executed.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN, F1/F2 | Public scope/census rules; workflows and reached installers; all three walkers; census/table; locks and authenticated exports; independent literal probes | R639-5 | 4391f353690972f4844cb641b1e77fa94f38cdf4 |
| RTL | CLEAN | Full diff and unchanged gitlinks; Dockerfile/install build configuration; measured layer architecture; Entity shape and protocol-processor source-list gates; `final-tree.json` | R639-5 | 4391f353690972f4844cb641b1e77fa94f38cdf4 |
| Robustness | UNCLEAN, F1/F2 | Unsupported shell/Make/Python and nested/startup/source probes; missing/orphan controls; download/schema/archive/privacy/patch controls; context-sensitive invocation fixtures | R639-5 | 4391f353690972f4844cb641b1e77fa94f38cdf4 |
| Tests | UNCLEAN, F1/F2 | All three inventory suites; GNU Make/Bash oracle fixtures; scoped workflow execution/logs; smoke source/public receipt; builder exact-cover and hosted skip evidence | R639-5 | 4391f353690972f4844cb641b1e77fa94f38cdf4 |
| Docs | UNCLEAN, F1/F2 | CI_IMAGE.md census and semantics claims; source closure/rebuild/privacy/environment/adoption instructions; docs/README diff; public evidence provenance | R639-5 | 4391f353690972f4844cb641b1e77fa94f38cdf4 |

Real limits and pending manager duties: this was a source-head review plus offline inspection of the delivered image exports. No Docker, act, registry login/push/pull, privilege, shared install, hardware run or prohibited full bank was used. Full image smoke is authenticated author evidence; extracted interpreter/Make execution is narrower. The two cold exports prove their equality, not a new rebuild on another host. Physical calibration and field skips are not hardware proof. No manager source bank at this head is claimed. The manager owns the eventual current-dev candidate build, builder/native banks and published receipts, hosted/act acceptance and exact candidate containment. The hosted snapshot distinguishes executed and skipped checks and is not an aggregate acceptance verdict. Image adoption remains the separate workflow-switch lane. F1/F2 need a corrected head and independent re-review before merge or publication acceptance; changed recipe inputs require refreshed lock/export evidence.

Final containment: `verify-tree.py` read every tracked blob directly and recomputed its Git object identity and executable/symlink mode, then compared index entries with the committed trees. All 1,347 parent blobs and 1,023 blobs across the five required submodules match. The required gitlinks are `gptp-processor` = `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`, `protocol-processor` = `2ad2f845dd583f8310075fa2380cb60a04fd091a`, `third_party/lwSRP` = `08ee86e812a0eb5e1dc6cd61b494d8baf3491348`, `third_party/tsn-c-stack` = `405dc68310a18f669049ffc10cc23eef7300dcff`, and `third_party/verilog-axis` = `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The optional `external` gitlink remains uninitialized with its committed index identity. Worktree status is empty, the index is exact, the head/tree match the assignment, and the workflow diff is empty. `final-tree.json` is the receipt.

Only REPORT.md and MANIFEST.sha256-listed receipts/scripts are publishable; scratch is excluded. No GitHub write or source commit was made. No review work remains running when this packet is handed off.

R639-5 FINISHED
