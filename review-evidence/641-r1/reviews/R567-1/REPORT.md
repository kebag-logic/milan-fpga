[R567] NEGATIVE - exact head 759d1d248fad095ab07bfcc480a0828117501f39

External independent review, round R567-1, of [issue #641](https://github.com/kebag-logic/milan-fpga/issues/641), [issue #651](https://github.com/kebag-logic/milan-fpga/issues/651), and [PR #699](https://github.com/kebag-logic/milan-fpga/pull/699).

Reviewed base: `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
Reviewed head: `759d1d248fad095ab07bfcc480a0828117501f39`.
Reviewed tree: `f43a876d37d15c921a5457698d1101b93274430f`.

Scope was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, both issue bodies and [the frozen assignment](https://github.com/kebag-logic/milan-fpga/issues/641#issuecomment-6081334020), then REQ-VER-02/03/04, architecture, descriptor ownership, the synthesis/measurement contracts, the three commits and their diff. The [published source evidence](https://github.com/kebag-logic/milan-fpga/tree/2f7a3d63d4cae0617e03ad4dd928a309fc3b1ec6/review-evidence/641-r1) was examined after the independent source pass. No private author material or other reviewer's report informed that pass.

## Acceptance and focused execution

| Requirement | Result and concrete evidence |
| --- | --- |
| #641.1: stopped Make parse is unreadable | `make-probes-43.log` and `make-probes-441.log`: errors before and after a rule still emit `# Files`, return 2 and are rejected. A complete database with missing generated products remains readable. Missing includes also refuse. |
| #641.2: both nested derivations are guarded | `tb/verilator/milan_dp_render/Makefile:86,92` and `tb/verilator/pp_shadow/Makefile:107` clear MAKEFLAGS. Direct probes under both versions find the correct nonempty frozen prerequisites and zero consumer findings. |
| #641.3: sizes derive from built images | `run.py:429` builds descriptor bytes and derives journal media. `oracle.json` contains no mirrored byte-count fields. `fixture-receipts.log` independently regenerates 1x1 and 8x8 media, compares all three public raw traces and grading, and rejects a one-byte journal-size error. Sizes are 3336/13256 journal bytes and 7512/19520 descriptor bytes. |
| #651.1: both flows fail active guards | `enforce_elaboration.py:14`, `run.sh:551`, `ooc.sh:564`: converted error/fatal tasks become fatal before parameter binding; run.sh normalizes before cache lookup. `refusal-results.json` records rc 1 for all three assigned configurations in each real flow. |
| #651.2: planted refusals | `guard-selftest.log`: 36 controls pass, covering valid 1/128 and refused 0/129/235, converted Error/Fatal, native error, OOC override, fast mode, enforcement deletion and a seeded false cache pass. |
| #651.3: CI inherits enforcement | `.github/workflows/rtl.yml:557` invokes the changed run.sh in every worker, including cache use. Hosted worker execution and aggregate state are recorded separately below. |

Both serial `check_entity_shape.py --self-test` runs pass 226 checks. OOC's 75 controls, cache controls, hermetic-list check, the fixture's 55 oracle/14 flash checks, diff check and changed-prose check also pass. Commands, actual exits and output are retained under `receipts/`; `scripts/` contains portable focused probes.

The first two broad shape self-tests overlapped their shared mutation target. Their failing receipts are retained but excluded from evidence. The target was restored from HEAD, both versions were rerun serially, and direct final byte/index checks pass. This was review orchestration interference, not a source finding.

The assigned stream replay first proves the builder's existing capacity refusal, then bypasses that earlier check only in memory to generate disposable downstream inputs. It does not widen the product's accepted configuration set.

## Shipping configuration regression

All five shipping datapath shapes pass both complete synthesis flows. This is a focused `milan_datapath` matrix, not a full inventory bank or SoC build. Each shape uses its freshly derived descriptor header and configured stream/audio/pruning parameters; stock synthesis descriptor/response memory-base defaults are retained. Only scratch source defaults and conversion arguments are substituted, following the OOC recipe for interface-bearing tops. Two heavy jobs ran concurrently. `scripts/shipping_flows.py` and `receipts/shipping-flows-results.json` retain the exact parameters and exits.

| Shipping shape | run.sh | ooc.sh |
| --- | --- | --- |
| arty_current | rc 0 | rc 0 |
| arty_4x4 | rc 0 | rc 0 |
| arty_8ch | rc 0 | rc 0 |
| ax7101_8x8 | rc 0 | rc 0 |
| ax7101_1x1_tdm8 | rc 0 | rc 0 |

## Findings

[R567] MINOR Docs - `docs/development/CODE_QUALITY.md:1258`, `docs/findings/README.md:26`, `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:25`, `hdl/ieee8021q/filtering/rx_mac_filter.sv:144` - R567-1-F1: current authorities still claim synthesis accepts active elaboration guards (retains public R566-1 F1).

Authority/evidence: AGENTS.md sections 5–7 require current contract documentation. CODE_QUALITY.md says the two synthesis flows do not enforce the guards and that `OOC_CHPARAM="TDATA_WIDTH=52" syn/yosys/ooc.sh rx_mac_filter` reports PASS. The current findings index and #649 summary repeat the unenforced-guard claim; the source comment does too. This review ran that exact example: `receipts/docs-example-52.log` and `.json` show rc 1 with the restored `$error` task. The legal `TDATA_WIDTH=64` control returns 0 (`docs-example-64.*`). Those checks use converter 0.0.13. The public prior review separately records the same refusal under 0.0.12. The updated #649 method note at lines 101–103 does not correct its summary or these other current authorities.

Impact: a current development guide states the opposite verdict for a runnable command, and the current findings index misstates what the gate enforces. This changes a gate/conformance claim and is not eligible for RESIDUE.

Required outcome: correct all named current claims. Both flows now reject active guards; the pinned 0.0.12 path preserves native errors, and converted diagnostics are normalized by the new helper. Mark the #649 limitation as belonging to the measured revision. The example with width 52 must be described as refused. Resolve the scope of the source-comment correction publicly if the lane's no-RTL-change rule needs clarification; moving an unresolved claim to another issue does not clean this lens.

Verification: re-read those artifacts at the corrected head, run the required documentation checks, and retain the illegal/legal example receipts under both supported converter forms. Docs remains UNCLEAN until correction and re-review. No functional acceptance item failed.


[R567] RESIDUE Docs - `tb/verilator/fw_service_budget/README.md:84` - R567-1-R1: split the new WIP-bound sentence.

Authority/evidence: `docs/README.md:140` asks for sentences under eleven words; this new sentence has fifteen. Impact: prose-style debt only. The 14.56-second calculation and 30-second comparison are correct and remain unchanged.

Exact fix: replace that sentence with: "Two full 64 KiB slots bound WIP at 14.56 seconds. This remains below the 30-second guard."

Required outcome: carry this wording correction to the manager's residue checklist. Verification: the replacement sentences have ten and six words, with identical quantities and meaning. This changes no code, test, measurement, generated artifact, verdict, conformance claim or privacy property. This residue does not independently make Docs unclean; F1 does.

One MINOR remains open. No BLOCKER or MAJOR was identified.

## Five independent lenses

[R567] PASS Conformance - `scripts/shape_consumer_inventory.py:184`, `tb/verilator/milan_dp_render/Makefile:86`, `tb/verilator/pp_shadow/Makefile:107`, `syn/yosys/run.sh:551`, `syn/yosys/ooc.sh:564`, `tb/verilator/fw_service_budget/run.py:429` - all six frozen issue acceptance items were traced into production call sites and tested against their named failure modes. No requirement, shipping configuration or product-image change appears in the diff.

[R567] PASS RTL - `receipts/source-identity.json`, `hdl/milan/KL_nvm_backend.sv:279`, `sw/litex/milan_soc.py:921`, `tb/verilator/nvm_capture_cpu/soc.py:73,161`, `tb/verilator/fw_service_budget/build.py:70` - the source delta contains no RTL, firmware, configuration or gitlink change. Guard conditions and parameter binding remain in the source; only disposable conversion output changes. The measurement callback now returns its inherited census unchanged to the existing unpacking caller. Clock/reset/CDC and shipping interface contracts are unchanged.

[R567] PASS Robustness - `make-probes-43.log`, `make-probes-441.log`, `guard-selftest.log`, `refusal-results.json`, `fixture-receipts.log` - stopped parses, missing includes/products, minimum/maximum and out-of-range parameters, inactive guards, overrides, both modes, stale cached success and incorrect fixture size were exercised. Existing timeout and cleanup behavior was inspected in the touched flows; the OOC controls remain green.

[R567] PASS Tests - `scripts/entity_shape_selftest.py:401`, `syn/yosys/guard_selftest.py:61`, `tb/verilator/fw_service_budget/run.py:440`, `tb/verilator/fw_service_budget/gen_oracle.py:16`, `receipts/public-custody.json` - negative controls require their own failure causes; deleting enforcement revives false success and restoring it defeats that cache entry. All three trace fixtures match independent regeneration and the published raw measurements. All 17 publication digests and 161 available source hashes per measurement match. Measurement binaries were not rebuilt by this review.

[R567] MINOR Docs - R567-1-F1 and the four artifacts named above - this lens was applied but is UNCLEAN. The changed synthesis README and #649 method note describe enforcement correctly, but other current authorities contradict it. The fixture regeneration instructions, public HANDOFF.md, assignment and REVIEW READY comment 6083295073 otherwise match the implementation and receipts. The two-slot wait bound is conservative; runtime limits were not relaxed. Measurement and calibration limits remain explicit.

## Reviewer-owned coverage ledger

Four lenses are CLEAN. Docs was applied and remains UNCLEAN because R567-1-F1 is open. Wording residues and optional suggestions do not independently prevent coverage.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Both issue bodies and assignment; shape_consumer_inventory.py:184; both Makefiles; run.sh:551; ooc.sh:564; run.py:429; six refusal receipts | R567-1 | 759d1d248fad095ab07bfcc480a0828117501f39 |
| RTL | CLEAN | source-identity.json; KL_nvm_backend.sv:279; milan_soc.py:921; capture soc.py:73,161; service build.py:70; ten shipping-flow receipts | R567-1 | 759d1d248fad095ab07bfcc480a0828117501f39 |
| Robustness | CLEAN | Both Make probe logs; guard-selftest.log; ooc-selftest.log; cache-selftest.log; refusal-results.json; fixture-receipts.log | R567-1 | 759d1d248fad095ab07bfcc480a0828117501f39 |
| Tests | CLEAN | entity_shape_selftest.py:401; guard_selftest.py:61; service run.py:440; gen_oracle.py:16; public-custody.json; all focused receipts | R567-1 | 759d1d248fad095ab07bfcc480a0828117501f39 |
| Docs | UNCLEAN | CODE_QUALITY.md:1258; findings/README.md:26; #649:25,101; rx_mac_filter.sv:144; synthesis/service READMEs; public evidence; docs-example-52/64 receipts; F1 | R567-1 (applied; no clean covering round) | 759d1d248fad095ab07bfcc480a0828117501f39 |

## Public findings reconciliation

The independent source pass, initial verdict and five-lens ledger were written before any other review report was read. `receipts/independence.json` records that boundary. Only then was [the public R566-1 report](https://github.com/kebag-logic/milan-fpga/pull/699#issuecomment-6084094858) read. Its F1 was independently confirmed against the named source and the two focused example runs above, changing the final verdict to NEGATIVE. All prior findings are retained or disposed below; none is silently cleared.

| Prior ID | Disposition | Evidence, impact, required outcome and verification |
| --- | --- | --- |
| R566-1 F1 | Retained: MINOR, Docs; R567-1-F1 | All four current claims remain at this exact head. Independent illegal/legal probe confirms their verdict contradiction. Correction and re-review are required as specified above. |
| R566-1 R1 | Retained: RESIDUE, Docs | `syn/yosys/README.md:44` and `enforce_elaboration.py:4,19` call the restored tasks “fatal”, while the literal task is `$error`. Effect is correctly fatal today; literal-name clarity is wording only. Exact README fix: “The helper restores converted error/fatal displays to `$error` tasks. Yosys refuses these when their generate branch is active.” Exact docstring fix: “Restore converted elaboration errors as `$error` tasks.” Manager residue checklist; verify task spelling and unchanged behavior. |
| R566-1 S1 | Retained: SUGGESTION, Tests | `.github/workflows/rtl-fast.yml:223,230` schedules sibling checks, but no workflow schedules `guard_selftest.py`. CI's pinned converter uses native errors; the new normalization self-test would improve future regression detection. Optional outcome: schedule it with the corresponding event coverage and consider actual-conversion fixtures. Verify a deleted/narrowed helper fails that job. Neither issue requires this scheduling. |
| R566-1 S2 | Retained: SUGGESTION, Robustness | `enforce_elaboration.py:14,19` and `docs-example-52.log`: the restored procedural `$error` is refused as an unsupported task, losing its specific message. The prior review's procedural-error variant is not a current RTL guard. Current acceptance requires nonzero refusal and is met. Optional outcome: preserve guard diagnostics and document version dependence; verify active/inactive guards across supported converters and synthesis versions. |
| R566-1 S3 | Retained: SUGGESTION, Robustness and Tests | `tb/verilator/pp_shadow/Makefile:107` lacks a nested-command status assertion. Its current guarded derivation passes both direct Make-version probes. This pre-existing failure-handling gap is outside the frozen change. Optional outcome: fail explicitly on nested derivation failure; verify a planted nested failure is refused under both Make versions. |

The public prior report remains evidence of its own runs; this review does not relabel them as independent executions here.

## Hosted execution provenance

The four hosted Yosys workers executed successfully, rather than taking a skipped-job path. Their retained artifacts contain exactly the 58 expected tops, each PASS, plus passing structural records. `receipts/hosted-tree-proof.json` ties all four workers to synthetic merge commit `e7e5a2c31dfa158a0722385525a45a616ef37370`, with parents `5603c353137e90c1fa95429f6d00ef7a2298d9ee` and `759d1d248fad095ab07bfcc480a0828117501f39`. Its tree is exactly `f43a876d37d15c921a5457698d1101b93274430f`. This establishes source-tree equivalence; it is not a manager source bank or final live-dev candidate receipt. Workers may use the repository's validated result cache. The physical gPTP job was skipped and provides no physical evidence.

The final read-only status snapshot (`receipts/hosted-checks-final.json`, `pr-state-final.json`) still names the reviewed head: rtl-fast and all four Yosys workers passed; two Verilator workers remained in progress. A successful `full-ci-gate` check is not treated as completion of those pending workers. No separate completed portability aggregate is inferred. The manager retains hosted acceptance.

## Limits and manager duties

The source-head broad gate evidence is the author's published receipts: 58/58 portability tops, 18/18 OOC tops, builder rc 0 with one calibration arm NOT RUN, and 38 documentation/script commands. This review did not run full parent, processor, gPTP, builder or Yosys banks. There is no manager source-head bank execution claimed or inferred.

The omitted builder arm is `test_resource_calibration` at `sw/builder/test_builder.py:19270`: it compares estimates with an archived placed utilization report and explicitly skips when that report is absent. That is acceptable as a declared limitation for this scripts/Makefiles/fixture change, which changes neither estimator nor RTL, configuration or shipping image. It supplies no physical calibration, area, route or hardware proof.

The refreshed 8x8 measurement retains two existing `milan_nvm` duty budget findings. A former maximum-heartbeat-gap finding belongs to the replaced trace; the new raw trace regrades without it under the unchanged threshold. The clean Tests result covers fixture custody and sizing; it does not establish product service-budget compliance. Field skips, simulations and the skipped physical hosted job provide no hardware proof.

Local synthesis uses the recorded 0.66 package build with external ABC and converter 0.0.13, exercising converted diagnostics. The author's full local synthesis receipts separately identify pinned converter 0.0.12. Local package identity is not claimed equal to the hosted bundled build. The scoped simulation executable's 5.050 identity was verified; no hardware or new full CPU simulation was run.

F1 requires correction and a new Docs review before completion. The manager owns hosted and local workflow-replica acceptance, independent-review reconciliation, the final live-dev merge candidate, its builder (48) and native (5) banks and required gates, merge authorization, post-merge containment, and issue/project closure. The supplied live-dev and source base were both `5603c353137e90c1fa95429f6d00ef7a2298d9ee`; no candidate validation is inferred from that equality. A later source change requires affected lenses to be reviewed again.

The review unit's recorded peak memory was 10,241,785,856 bytes within its 12,884,901,888-byte cap, with no OOM event (`receipts/resources.json`).

Final tracked-byte, mode and index verification covers the parent and all three required submodules. HEAD/tree and gitlinks remain exact; no source edits are delivered. `receipts/exact-tree.*` records the direct object comparison. Publish only REPORT.md and the files listed in MANIFEST.sha256; scratch is excluded.

R567-1 FINISHED
