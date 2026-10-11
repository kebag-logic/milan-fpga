[R609] POSITIVE - exact head 15981b511370a8cfb58ec023fae27f8a800c058c

External independent delta review of issue #73 / PR #174, round R609-3. Tree `e4dacda27467378e175562d5001b8dbadea9d4bd`; source base `2cbed0a987c1e68402658d69459ab7e5aa571adc`; preceding reviewed head `9975764846e7e63bccf0b68a5188d5cc7f23f890`. All five lenses are CLEAN. No BLOCKER, MAJOR or MINOR remains. One wording RESIDUE and two previously published SUGGESTIONs are retained below; none changes the verdict.

The round-three requirements are met: an exhaustive field registry and checked generated references; exact command/echo mapping steps; named generator refusals; explicit semantic GDI export fields; declared status/oversize exemptions. The original behavior-preservation constraint also holds in the independent checks.

**Reconstruction and authority**

The review began from the [public start](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/174#issuecomment-6112176523) and the assigned detached clone. No repository or ancestor AGENTS.md or CONTRIBUTING.md was present. The supplied command-wrapper instruction, repository/HDL README and `docs/README.md` were read first.

Next came the [issue acceptance](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/73), [Mark II scope decision](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/73#issuecomment-6009640063), [frozen lane scope](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/73#issuecomment-6100509798), round-two decision and Python-rule addendum, and the [round-three assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/73#issuecomment-6107323038). Linked parent re-scope/F5 material confirms the firmware consumer; the lane explicitly defers its implementation and parent gate.

The authorities examined were REQ-VER-002/GAP-11, architecture 01 scope, 02 external/transaction/read-face contracts, 03 F03.7 hazards, 06 F06.14 and realized inventory, 09 verification/CI/field contract, and the concrete engine, micro-CPU, classifier, scoreboard, notification and status consumers. The status authority is the project's transcription of IEEE 1722.1-2021 Table 7-141. Copyrighted specification PDFs were not independently re-audited. Public parent [Rule 12](https://github.com/kebag-logic/milan-fpga/blob/7ee91b258d93fa77052faa621e9b84cdf46665a8/docs/development/CODE_QUALITY.md#rule-12-prefer-idiomatic-python) was also examined.

The base-to-head diff covers 31 files and 20 commits; the round-three delta is four commits. The independent pass covered the registries, generator, gate modules, observer/wrapper, mutation driver, Makefiles, workflow and changed documents before prior public findings were opened (`receipts/independent-pass.txt`). Then the immutable [public evidence packet](https://github.com/kebag-logic/milan-fpga/tree/7ee91b258d93fa77052faa621e9b84cdf46665a8/review-evidence/pp73-r1), published PR body, manager scope/evidence comments and prior public findings were reconciled. No private author material, management checkout, or separate review REPORT.md file was read. No other round-three verdict was consulted.

**Round-three resolution**

| Requirement / prior ID | Disposition and exact-head evidence |
|---|---|
| Exhaustive registry and references | RESOLVED. `aecp_fields.json` has 62 field paths: 29 held within their stated scope, 33 held to nothing. `fields.py:16,36` inventories nested paths in both directions and requires a consumer/check/probe for held entries. `field_docs.py` renders the docstring, 09 §8.10 and REQ-VER-002 Arch; the actual published PR field block passes `--pr-body`. The self-test executes all 29 held-field mutations after regenerating F06.14. Unknown nested and nonexistent registry fields also fail by path in independent probes. |
| R608-2-F1 — echo `per` | RESOLVED. `record.py:280` compares the accepted-offset gcd exactly; `table.py:115` ties echo response cdl/per to command cdl/per. Both 8→4 rows and the ADD-only 8→2 probe fail by name. Independent step probes cover both mapping rows and both command/response sides. |
| Half-record and multiple-record engine drifts | RESOLVED. `sim_main.cpp:299` tries count one at cdl 24/28 and count two at 28/36. The clean first entries accept cdls 20,28,36, gcd 8, with no cdl 24 dispatch to those entries. Both compiled 4-byte and 16-byte mutations fail for ADD and REMOVE before and after re-recording. The former observes gcd 4; the latter observes no positive offset and fails with gcd 0. Empty positive evidence is not accepted as proof. |
| Zero/null/negative steps | RESOLVED. `table.py:58` refuses a present `per` unless its exact type is integer and it is positive with a unit. Independent probes also reject booleans and fractional values on both sides of both echo rows; all 30 independent registry/step probes pass. |
| R608-2-F2 — status/oversize fields | RESOLVED by the assignment's explicit declaration option. `common_status`, `commands[].engine_status`, and `commands[].oversize` are declared held to nothing in the registry and generated references. The four prior probes still pass after F06.14 regeneration, as expected for these declared gaps. Status-path guarantees are explicitly conditional on the trusted exemptions. No independent status reachability or oversize derivation is claimed. |
| R609-2-F1 — `documented[]` semantics | RESOLVED. The six GDI rows' opcode, optional rtl and optional gdi are semantic inputs; name is identity/diagnostic and section/cells render. The blanket prose-only reference is gone. Re-running the unchanged export probe gives semantic failures for all three fields after F06.14 regeneration. |
| R608-2-F3 — generator diagnostics | RESOLVED. `gen_ucode.py:51` validates identities/entries before assembly; `:181` validates the MVU opcode before conversion. All eight prior generator probes refuse with named lines both normally and under optimization, including missing entries, missing name identified by AEM opcode/constant, and non-hex MVU opcode. |
| R608-2-R1 / R609-2-R1 | Their requested historical correction sentences are present, but equivalent unpublished-head wording survives for round three. Retained as the single residue R609-3-R1 below. |

**Earlier public findings**

Read after the independent pass: [R608-1](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/174#issuecomment-6104874774), [R609-1](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/174#issuecomment-6104929075), [R608-2](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/174#issuecomment-6107318258), [R609-2](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/174#issuecomment-6107310880). No prior adverse finding is silently waived.

| Prior ID | Disposition at this head |
|---|---|
| R608-1-F1 — decode/dispatch | RESOLVED. Fresh golden/restored observations pass; q1 redirect and q2 wrong-opcode decode fail by command name. All 16 standing compiled controls pass their detection criteria. Engine decode is observed, not parsed from source text. |
| R609-1-F1 — response/command sizes | RESOLVED within disclosed scope. Unchanged single-column sweep: 31/31 drifts fail on each side. The stronger coupled-echo sweep: 29/31 fail on each side; ACQUIRE_ENTITY and REGISTER_UNSOLICITED_NOTIFICATION remain the explicitly disclosed cdl-to-echo-only exceptions. GET_AUDIO_MAP 20/28 fail, 24 passes. Every reachable prior ROM-field mutation fails; no passing reachable mutation remains. |
| R608-1-F2 — real-file generator inputs | RESOLVED. File-copy and generator-alone plants execute; message/entries/status/MVU refusals are named. |
| R608-1-F4 / R609-1-F2 — ROM prerequisites | RESOLVED. Independent table-only edits invalidate and regenerate `ucode.hex` in pp_top, ucpu and aecp_cmds; all three change the ROM digest as expected. No full pp_top bank was run. |
| R608-1-F3 / R609-1-F3 — doubled plurals | RESOLVED. Stored plural units render unchanged; generated-document gate and full documentation check pass. |
| R609-1-S1 — status code authority | RESOLVED. STREAM_IS_RUNNING 12→13 fails against Table 7-141. |
| R609-1-S2 — documented missing name | RESOLVED. The size/probe sweep obtains the named schema refusal. |
| R608-1-S2 / R609-1-S3 — optimized assertions | RESOLVED. Explicit refusal survives optimized execution. |
| R608-1-S1 / R609-1-S4 — export reference | RESOLVED, including the semantic GDI correction of R609-2-F1. |
| R608-2-S2 — undigested inputs | RESOLVED. `inputs.py:40` includes model_lint.py, model_rules.py and verilator_harness.hpp in raw sweep digests. |
| R608-2-S1 / R608-2-S3 | RETAINED as verdict-neutral suggestions below. |
| Manager Python-rule addendum | RESOLVED for this source review. Focused inspection finds no structure/signature/docstring violations in 15 new gate/campaign modules, 146 functions. Published author consumer gate/listing and 54-check self-test pass with unchanged budgets and both evidence-reader patches. This is not a manager source bank. |

**Reviewer execution and receipts**

All mutations/build copies were confined to `scratch/`. Foreground orchestration waited for every child; independent campaigns/checks ran concurrently. The standing campaign used `--jobs 4`, prior engine campaign `--jobs 3`, and site/size campaigns `--jobs 4`. Make used `-j16`; each compilation was bounded to two workers. The scoped compiler reported version 5.050 before use. No full processor/parent/gPTP/synthesis/builder bank, hardware run, container CI run or shared install was performed.

| Check | Result | Receipt |
|---|---|---|
| Full documentation gate | `make -j16 check` rc 0; 41 Mermaid/18 WaveDrom blocks, links, IDs, figures, matrices, parameters and command gate pass | `receipts/make-check.log`, `.rc` |
| Command gate/self-test | 31 commands, 84 entries, 41 generated rows; 220/220 plants caught; all 29 held field classes exercised | `receipts/selftest.log`, `make-check.log` |
| Published PR reference | Exact generated field block matches registry; rc 0 | `receipts/pr-reference.log` |
| Micro-CPU suite | 437 PASS, 0 FAIL | `receipts/ucpu.log` |
| Standing compiled campaign | 16/16 detected; golden/restored each 585760 trials, zero timeouts, 176/176 checks | `receipts/command-controls/`, `command-controls.log` |
| Round-two table/generator/export probes | 23 table probes; required semantic failures and declared passes; eight generator plants × two modes; three GDI semantic fields | `receipts/table-probes/`, `generator-lines.txt`, `export-fields.log` |
| Round-two engine probes | Both mapping drifts fail at all three verdict steps; unswept MVU-byte limit reproduced | `receipts/engine-probes/summary.json` and raw logs |
| Round-two size/ROM probes | 62 single-column drifts rejected; coupled-echo results and permitted exceptions above; all reachable ROM probes detected | `receipts/prior-size-sweep.log`, `echo-size-lines.txt`, `prior-rom-size.log` |
| Round-two site mutation probe | 119 selected sites; 107 fail self-test when disabled; 12 survivors are record JSON emission lines, not diagnostic/refusal sites | `receipts/gate-mutation/` |
| Independent delta/prerequisite probes | 30/30 registry/step controls; three table-only rebuilds | `receipts/registry-probes.log`, `prerequisites.log` |
| Identity | 610 tracked blobs/modes and index agree; detached, clean, zero gitlinks; all 46 production SV files and both ROMs unchanged from base | `receipts/integrity.json`, `tracked-blobs.json`, `production-identity.json` |

The prior probes were preserved under `public/reviews/.../scripts/`. Four working copies needed only `tb/common` added to their input-copy inventory because the new gate digests that harness; the exact adaptation is retained in `receipts/prior-probe-adaptations.diff`. Their assertions/plant semantics were unchanged. The initial archive-only focused-doc run could not enumerate Git-tracked files for figures/IDs; it is retained as rc 2, and the full check was rerun successfully in the actual clone. This was an execution setup issue, not a source defect. The updated portable runner accepts a repository path for those gates.

ROM SHA256 at both base and head:

- `ucode.hex`, 26624 bytes: `518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8`.
- `ltn_rom.hex`, 6138 bytes: `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956`.

**Retained observations**

R609-3-R1 — RESIDUE — Docs. Artifact: published PR body, Round 2 closing paragraph and Validation closing paragraph (`receipts/pr-body.md`). Authority/evidence: the exact head is published, while these two sentences still state otherwise. Impact: publication-status prose only; no measurement, figure, test, code, generated artifact, verdict or conformance claim changes. Exact required fixes: replace “The round-3 measurements below are local; its new commits have not been pushed.” with “The round-3 measurements below were run locally at the stated commits.” Delete the separate final sentence “The new commits have not been pushed.” Verification: manager checks both replacements in the residue checklist. The earlier R608-2-R1/R609-2-R1 defect class is retained here, not counted twice.

R608-2-S1 — SUGGESTION — Tests, Robustness. Artifacts: `tb/aecp_cmds/sim_main.cpp:392` MVU sweep and `receipts/engine-probes/mvu-pid-first-byte-unchecked-3-gate.log`. Authority/evidence: the declared bounded sweep skips wrong protocol-ID bytes @22 and @24; the unchanged prior probe again passes after re-recording. Impact: no behavioral guarantee for those unswept bytes; the input digest alone detects the original edit. Required outcome if adopted: flip each protocol-ID byte independently and retain a named compiled control. Verification: that control fails semantically even after re-recording. This remains a disclosed, verdict-neutral coverage extension.

R608-2-S3 — SUGGESTION — Tests, Docs. Artifacts: wrapper `:164,256`, `sim_main.cpp` templates, and 09 §8.10's unswept-outcomes limit. Authority/evidence: lock-held and deadline-kill inputs are tied low; stimuli omit a bound-only running split and nonzero descriptor index. Impact: these outcomes are outside this observer's guarantees. Required outcome if adopted: name these examples in the stated limitation, or add independent stimuli/controls. Verification: documentation matches the actual stimulus or new controls prove each added case. No new coverage is inferred here.

**Public execution evidence and limits**

The selected author round-three receipts report the five source gates passing, suite totals 1,029,620→1,029,796 with every original suite record unchanged, nine existing campaign pairs unchanged under declared normalization, and 16 final observer controls plus golden/restored records identical on original-base production and head. The published elaboration receipt records byte-identical converted production source and engine netlist; this reviewer did not run a synthesis bank. Author consumer receipts identify parent `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5` with the exact processor head and the parent-name-evidence / parent-aecp-cmds-evidence patches. These are author source/consumer receipts, distinct from manager merge-candidate validation.

All 80 selected immutable packet artifacts match immutable Git blob identities; the 79 files other than the outer manifest itself match its published SHA256 values. Twelve examined original-file manifest differences have declared path redactions and match the outer published hashes. Receipts: `public-fetch.json`, `public-manifest-check.json`, and selected raw material under `public/author-r3/`.

Hosted snapshot at 2026-10-11 18:29:05 UTC: exact-head [push run 38162911571](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/38162911571) has executed, successful docs-gates and portability jobs; suites remains in progress. Its compiler-build step is skipped after cache use. Pending campaign steps and the whole run are not reported as passed. No exact-head pull_request merge execution was established in this snapshot; the older pull_request run is not evidence for this source head. The source does not contain processor main `6d536868` (#173/#151), confirmed by ancestry check. A hosted pull_request run tests a processor merge context, distinct from this detached source.

The observer covers its stated opcode/length/template population. Limits include opcodes above 0x007F, unswept outcomes, GDI's 524 ceilings, common/engine status exemptions, oversize, echo cdl pairs with declared floors, shared echo exceptions, and shared-entry descriptions. ROM walking checks sizes/statuses/lock/notification rather than field values/order. Golden models, stimulus generation, ACMP transition/timing-table generation and parent firmware consumption remain outside this lane's accepted delivery. Physical calibration NOT RUN; field skips are not hardware proof.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen acceptance and round-3 scope; REQ-VER-002/GAP-11; command/field registries; F03.7/F06.14; explicit export limits | R609-3 | 15981b511370a8cfb58ec023fae27f8a800c058c |
| RTL | CLEAN | 46 unchanged production SV blobs; both generated ROMs; dispatch handshake; 437-check micro-CPU run; golden/restored and compiled controls | R609-3 | 15981b511370a8cfb58ec023fae27f8a800c058c |
| Robustness | CLEAN | Named generator refusals normally and optimized; zero/null/negative/boolean/fractional per; exhaustive registry failures; post-rerecord probes; incremental ROM prerequisites | R609-3 | 15981b511370a8cfb58ec023fae27f8a800c058c |
| Tests | CLEAN | 220 plants and 29 held-field mutations; 16 compiled controls; public round-two table, generator, engine, size, ROM, export and site probes; CI wiring | R609-3 | 15981b511370a8cfb58ec023fae27f8a800c058c |
| Docs | CLEAN | docs/README; 06 generated and realization tables; 09 sections 7/8.10; compliance cells; generated docstring and published PR reference; suite README; model/export reference | R609-3 | 15981b511370a8cfb58ec023fae27f8a800c058c |

**Pending manager duties and packet integrity**

No manager source bank runs at this exact head, and none is claimed. Source validation is distinct from the final current-dev candidate: source base `2cbed0a987c1e68402658d69459ab7e5aa571adc`, live parent dev `6bfeeb132fa0b1ad8a5b957446c66a498e633af7`. At the merge turn the manager builds that candidate, runs builder/native banks with the applicable parent evidence patches, verifies candidate gitlinks, and links receipts on the PR. The manager owns hosted/act acceptance, final current-dev integration, residue closure, the independent-review completion bar, and publication. This standalone processor clone contains no submodule gitlinks; it cannot substitute for the parent's gitlink check.

The clone was never mutated by a probe. Final byte/mode/index checks preserve the exact assigned head/tree. No source fix, commit, push, GitHub write, merge, author contact, sub-agent, shared install or hardware access occurred. Portable scripts and raw receipts are enumerated by packet-relative SHA256 in `MANIFEST.sha256`; `scratch/` is disposable and excluded. Only the manifest-listed files and this report are publication material.

R609-3 FINISHED
