[R900] NEGATIVE - exact head 677d605f37c3a80654df1dd2cde053b57242845b

External independent review R900-1 of issue #983 / PR #986. All five lenses were applied. Two MINOR findings remain open. Under the assigned completion rule they prevent a positive verdict and leave their attributable lenses unclean. One separate RESIDUE concerns stale PR publication wording.

Reviewed tree: `79d523167a95861b8092b64574222db91bce5a07`. Source base: `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`. One commit changes five files. This is a source-head review, not validation of a merge into current dev.

## Authorities and independence

Reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, [issue #983](https://github.com/kebag-logic/milan-fpga/issues/983), its public acceptance/evidence comment, and the [scope ruling on board issue #29](https://github.com/kebag-logic/ti-sitara-am65x-bsp/issues/29#issuecomment-7096504049). Then examined REQUIREMENTS.md sections 1 and 8, docs/overview/ARCHITECTURE.md, docs/reference/PP_DESCRIPTOR_OWNERSHIP.md, ENDSTATION_BUILDER, the exact diff/history, and the [published author packet](https://github.com/kebag-logic/milan-fpga/tree/adeb1331026950e5c13c31debb44a225caa62ad1/review-evidence/linuxprof-r1).

The issue and ruling authorize a descriptor-only extension. They do not restore an FPGA operating-system product path forbidden by [#259](https://github.com/kebag-logic/milan-fpga/issues/259). The target has no gateware build, fabric-owner substitution, or software installation path. Its spelling `host` follows existing portable-host terminology; the unchanged bare-metal scope gate passes.

No private author material or other reviewer's report was read. [independent-verdict.md](independent-verdict.md) records the independent findings and ledger before prior-review retrieval. Subsequent retrieval found zero submitted reviews, zero inline review threads, and only the review-start conversation comment. There are no prior public findings to resolve or retain. [public-state.json](public-state.json) records the consulted public state.

## Findings

### R900-1-F1

[R900] MINOR Conformance / Robustness / Tests - `sw/builder/endstation_builder.py:4801`; `sw/builder/test_builder.py:30804` - Host dispatch bypasses the existing malformed-board refusal boundary.

**Authority/evidence:** Issue #983 requires unchanged FPGA profile validation. `load_config()` explicitly promises ConfigError on a violation at lines 4788-4789. Starting with the valid FPGA 1x1 config, replace only `board` with `[]`, `""`, or `["ax7101"]`. At the source base all three return `ConfigError: board: missing required key 'target'`. At the reviewed head all three raise AttributeError from the new unconditional `brd.get("target")`. The ADP generator CLI handles ConfigError but not AttributeError (`sw/firmware/ctrl/adp/adp_entity.py:106`). Gate 42 exercises keys inside a mapping, not this container boundary. See [regression-result.json](regression-result.json) and [regression.log](regression.log).

**Impact:** Malformed input escapes the documented validation interface and crashes callers that correctly catch ConfigError. This does not accept invalid configurations or change valid FPGA artifacts; severity is MINOR.

**Required outcome:** Host dispatch must preserve controlled ConfigError refusal for these malformed board values. Add a discriminating regression test, retaining valid FPGA/host controls and the missing-fabric-owner plants.

**Verification:** Re-run `regression_probe.py` and require ConfigError for all three inputs at the corrected head. Gates 41/42 must stay green, and the added regression must fail against `677d605f`.

### R900-1-F2

[R900] MINOR Docs - `docs/ENDSTATION_BUILDER.md:1248`; `sw/builder/endstation_builder.py:4815` - Host TSpec is documented as current-format-derived, but uses the widest advertised talker format.

**Authority/evidence:** The new section says, “SRP's TSpec takes the declared current format.” The adjacent source explanation also describes each talker's current format. Line 4818 instead calls `framer_declared_channels()`, whose lines 1184-1200 maximize channel width across every format of every talker. `_srp_rows()` applies that shared width at `clocking.sampling_rate_hz`. An accepted host variant with a two-channel current format and two/eight-channel supported formats produces MaxFrameSize **217**; its current-format geometry is **73**. The variant packs successfully into a 4,784-byte image. See [regression-result.json](regression-result.json).

**Impact:** The documented rule predicts a different reservation size and bandwidth than the generator computes. This is an incorrect protocol-field derivation claim, not cosmetic wording; it is MINOR rather than RESIDUE. No defect in the conservative calculation itself is established here.

**Required outcome:** Describe the actual shared maximum across advertised AAF talker formats, at the configured sampling rate, without claiming it is each stream's current-format geometry. Correct the section and source explanation. No calculation change is requested.

**Verification:** The current-two/supported-two-and-eight fixture retains its measured 217-byte result, and both explanations match `framer_declared_channels()` and `_srp_rows()`.

### R900-1-R1

[R900] RESIDUE Docs - [PR #986 body, Status](https://github.com/kebag-logic/milan-fpga/pull/986) - Publication wording predates the published PR.

**Authority/evidence:** The body says “Not pushed; no hosted run exists yet.” The PR exposes the reviewed head, and the hosted snapshot contains four queued runs. No successful or executed job is inferred.

**Impact:** Stale publication wording only; no measurement, generated artifact, test, conformance claim, or verdict changes. It does not leave an additional lens unclean.

**Exact fix:** Replace that sentence with: “Published head: `677d605f37c3a80654df1dd2cde053b57242845b`. The evidence below is local source-head evidence; hosted acceptance is tracked separately.”

**Verification:** Compare the sentence with the PR head. Preserve the existing incomplete-gate disclosures.

## Five-lens results

**Conformance:** The host branch rejoins existing entity, clocking, stream, format, SRP, platform, cluster and identity code. Its owner is exactly `host-phc`; fabric features and SoC declarations refuse. The unchanged domain-zero and clockAccuracy validators run. The Configuration descriptor exists. The 5,784-byte image contains AAF input 0, CRF input 1 and AAF output 0, no CRF output, and ENTITY/ADP counts 1/2. AAF format is `0x0205022002006000`; CRF is `0x041060010000BB80`. These match #983 and the board ruling's inventory. F1 leaves the validation-contract portion unclean.

The `entity.conf` acceptance path is real and board-owned. At public board commit `cce8c9a4143548c80800b2def821431ff45e3698`, `milan-linux/tools/gen-entity-conf.sh` calls this checkout's unchanged `adp_entity.py`. It generated correct values for the PR example and board YAML. The latter matches every published entity.conf value, including model ID `0x001BC50AC1000100`, counts 1/2 and capabilities `0xC588`, `0x4001`, `0x4801`. Only the exported-tree revision comment requires normalization because this clone lacks `.milan-fpga-rev`. [entity-conf-result.json](entity-conf-result.json) names exact public inputs and output hashes. This proves generation, not daemon or board behavior.

[R900] PASS RTL - `source.diff`; `sw/firmware/ctrl/loop/ctrl_loop.h:353`; [identity-result.json](identity-result.json); [shape-result.json](shape-result.json) - No RTL, firmware C implementation, hardware interface, or submodule gitlink changes. The authorized scheduler-header row is the sole firmware delta. Clock/reset/CDC and datapath contracts are untouched. All **245** independently captured FPGA builder/image/header artifacts match base/head across five configs at own, explicit split and explicit all-fabric placements. The comparison loads each exact builder blob against unchanged dependencies without replacing tracked files. Existing scheduler token/macro outputs and refusal outcomes match across twelve config/interface selections. The host loop translation unit compiles with strict warnings and its static assertions.

The `(1,1,2)` row requires `CTRL_HOST_PLATFORM`. Gate 41 proves refusal without it, unchanged listed FPGA rows with it, and no definition in this repository's build inputs. Its figures reuse 1x1/1if, justified as a stated profile with one fewer talker and unchanged sinks. The comment excludes measurement of descriptor-dependent costs and host preemption. This supports the stated conditional profile, not a measured host timing guarantee.

**Robustness:** Gate 42 passes 28 input plants, including five FPGA separation/owner cases. Independent probes cover all nine required gPTP declarations, integer extrema and wrong types, link rates, queue counts, interface widths and clockAccuracy values. Sixteen valid gPTP extrema survive into descriptor bytes. Existing packed-image L6/L10 cases were additionally applied to the host, including malformed offsets, empty/excess/partial arrays and required descriptor removal. Removing host-owner validation in memory makes the new refusal test fail. [boundary-result.json](boundary-result.json) records 119 observations. F1 remains open.

**Tests:** Gates 32/41/42 pass: 116 documented FPGA keys, 64 host keys, three agreeing generators, the macro guard and 28 refusals. Independent evidence adds FPGA identity, scheduler preprocessing, entity.conf generation, host-loop compilation and boundary/packer negative controls. The image probe accumulates index-map runs to locate the differently sized AAF/CRF descriptors. F1 needs a committed regression before Tests can be clean.

**Docs:** ENDSTATION_BUILDER section 6 describes the profile, key differences, no-build boundary, runtime MAC integration duty and unmeasured scheduling assumptions. No added source comment contains a prohibited bench lane label, review round, reviewer ID or issue-comment ID. `docs_check`, bare-metal check/self-test, document paths and the em-dash gate pass. F2 leaves Docs unclean despite these mechanical passes. R1 is publication residue.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1 | #983; board #29 ruling; builder host/common loaders; host YAML; boundary-result.json; entity-conf-result.json | R900-1 | 677d605f37c3a80654df1dd2cde053b57242845b |
| RTL | CLEAN | source.diff; ctrl_loop.h:353-425; identity-result.json; shape-result.json; integrity-result.json | R900-1 | 677d605f37c3a80654df1dd2cde053b57242845b |
| Robustness | UNCLEAN: F1 | builder host loaders; test_builder.py:30804; boundary-result.json; regression-result.json | R900-1 | 677d605f37c3a80654df1dd2cde053b57242845b |
| Tests | UNCLEAN: F1 | test_builder.py gates 32/41/42; focused-gates.json; independent probes; evidence-audit.json | R900-1 | 677d605f37c3a80654df1dd2cde053b57242845b |
| Docs | UNCLEAN: F2; R1 residue only | ENDSTATION_BUILDER section 6; builder:4812-4818; docs logs; regression-result.json; PR body | R900-1 | 677d605f37c3a80654df1dd2cde053b57242845b |

## Limits and pending manager duties

The author packet's 24 published file hashes verify; its 170-artifact manifests match. The four subset receipts report 114 passing function verdicts from the 115-function inventory, once each. Gate 1b (`test_baremetal_profile_contract`) did not complete. Calibration reports NOT RUN; its function-level pass is not calibration evidence. The firmware logs report 21, 18 and 8 passing arms, not four completed shards. [evidence-audit.json](evidence-audit.json) retains these distinctions. Subset JSON has no intrinsic head/tree binding; attribution comes from public REVIEW READY and the immutable packet. **No manager source bank exists at this head, and none is inferred.**

**Incomplete-bank judgment:** These omissions do not prevent this bounded technical review or add a separate code finding. They prevent claiming the full local bar is complete. The manager owes the complete builder/native banks and union evidence on the final current-dev candidate, including gate 1b and firmware shards/mutation campaigns, plus separate required source-head hosted/act acceptance. Focused probes or a later candidate pass must not be presented as completed source-head bank execution.

The hosted observation found `rtl-fast`, `docs`, `elaborate` and `rtl-full` queued. No executed job result or successful skipped context was credited. Hosted/act acceptance remains the manager's duty. No Docker, act, host orchestrator or its self-test ran here.

At assignment, live dev was identified as `e275d7950ef3385753e6a15d2e191ba855b171ed`, distinct from the source base. The manager must construct and validate the actual current-dev candidate at merge time and link receipts. This review makes no candidate claim. Findings require correction and re-review at the corrected head. Two independent positive reviews, no review in flight, explicit merge authorization and post-merge containment remain required.

Physical calibration was NOT RUN. Field skips and desk checks are not hardware proof. Media-clock operation, host scheduling bounds, board enumeration/installation, release soak and physical timing were not tested. The board's publicly disclosed CRF-clock limitation is not resolved by descriptor generation.

Full parent/processor/gPTP/Yosys/builder banks were not run. The scoped RTL simulator was not used. No source fixes, commits, pushes, GitHub writes, sub-agents, shared installs, hardware operations or edits to another checkout occurred. Commands were foreground processes; bounded independent checks ran concurrently with no heavy hardware build. Disposable files are confined to packet `scratch/`.

Initial probe failures are retained: em-dash first lacked the pinned renderer; a disposable environment installed the lock and the retry passed. Boundary-probe expectations were corrected to the existing clockAccuracy table, mixed-length index-run format and AAF channel-bit position. The initial standalone C compile lacked the shared wire include; the corrected command passes. These were review setup/expectation errors, not source findings or weakened production tests. Initial and final logs are distinguishable.

[integrity-result.json](integrity-result.json) verifies exact HEAD/tree, every tracked blob's raw bytes/mode, the complete stage-zero index, and raw bytes/index/pins for protocol-processor, gptp-processor, verilog-axis, tsn-c-stack and lwSRP. The unused external gitlink is unchanged and uninitialized. Status is clean; no assume-unchanged or skip-worktree flags exist. No restoration was needed: tracked source bytes were never mutated.

## Reproduction and packet

Review scripts accept `REPO PACKET`: `run_focused.py`, `identity_probe.py`, `boundary_probe.py`, `regression_probe.py`, `shape_probe.py`, `evidence_audit.py`, `integrity_probe.py`. `entity_conf_probe.py REPO PACKET --fetch` retrieves its exact public board inputs. The evidence audit requires the published packet commit locally. No script executes prohibited full banks.

For the em-dash retry, create a virtual environment under `PACKET/scratch`, install `tools/markdown/requirements.txt` with `--require-hashes`, and run `scripts/check_em_dash.py --base 854bd7236792ce1adbd10c43b13a6a5002ad3bb6` with that interpreter. Set `TMPDIR=PACKET/scratch` and `PYTHONDONTWRITEBYTECODE=1`.

`MANIFEST.sha256` lists publishable scripts, raw logs, statuses and JSON receipts using packet-relative paths. `scratch/` is excluded and must not be published. Verify with `sha256sum -c MANIFEST.sha256` from the packet directory.

R900-1 FINISHED
