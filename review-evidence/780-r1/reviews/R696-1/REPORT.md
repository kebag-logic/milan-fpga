[R696] NEGATIVE - exact head 25f05752f7e50e3cf7e27008e434ffde930b4b6f

Round R696-1, external independent review of issue #780 / PR #783.
Tree: `5db8e8298734d18c8a50ba24cd8c46140292302b`.
Source base: `a032c6d6e3775f145349d5a495c1e1ad12294936`.

The adoption itself passes the focused checks. One MINOR finding remains in the public description of test coverage; it prevents clean Tests and Docs coverage. No RTL correction is requested. One separate navigation correction is RESIDUE.

## Findings

### R696-1-F1: MINOR; Tests, Docs

Artifact: [issue #780 REVIEW READY, Grep item 2](https://github.com/kebag-logic/milan-fpga/issues/780#issuecomment-6389598798); related PR #783 Description / The grep. Source: `tests/steps/aecp_engine_steps.py:246`, `:511`, `:761`; `tests/steps/aecp_engine_model.py:417`, `:617`.

Authority/evidence: the handoff says “milan_dp and the behave model only target AVB_INTERFACE”. The model sweep actually calls `build_aem_command(0x0027)` with its default eight zero payload octets. Those octets name descriptor type 0, ENTITY, not AVB_INTERFACE (9). The served inventory supplies SUCCESS (0), and the model returns that constant without applying the GET_AVB_INFO target gate. `model_probe.py` reads the actual inventory expression and reproduces type 0 / status 0; `model-probe.log` retains the result. The scope explanation in the PR should distinguish this inventory model from a valid-target wire test. AGENTS.md section 6 requires accurate, artifact-specific Tests and Docs evidence.

Impact: the published evidence gives reviewers the wrong reason why no parent expectation changed and obscures the scope of the 406-scenario result. The narrow frozen acceptance claim remains true: there is no wrong-type GET_AVB_INFO expectation of NOT_IMPLEMENTED/status 1 to update. The model does not establish the changed status or valid-target-only coverage. This finding concerns the newly published evidence, not a request to broaden #780 into a model rewrite. Correcting a test-coverage claim is outside the owner's purely-wording RESIDUE exception.

Required outcome: correct the handoff's target claim and clarify the PR's model description. Exact replacement: “The behave sweep uses generic ENTITY[0] operands and its GET_AVB_INFO inventory row returns SUCCESS; it does not grade the wrong-type wire response. It contains no status-1 expectation for this case. The processor V5 tests and the parent-boundary probe establish the adopted status.” The existing model limitation may be tracked separately; this review requires no model/code change for #780.

Verification: run `python3 model_probe.py` from the exact-head checkout using the packet script; compare the corrected public evidence with the emitted type 0 / status 0 and the wire-probe results. Re-review the corrected evidence before clearing Tests and Docs.

### R696-1-R1: RESIDUE; Docs

Artifact: PR #783, Authoritative references, processor compliance-review entry.

Authority/evidence: the PR locates the ruling at “processor docs/architecture, section 8 item 12”. At the adopted pin the compliance decision is `protocol-processor/docs/00_MILAN_COMPLIANCE_REVIEW.md`, section 8, row 14. Row 12 concerns SET_CONFIGURATION notifications. The implementation detail is in `protocol-processor/docs/architecture/06_aecp_engine.md`, section 6.10.

Impact: an imprecise navigation pointer. The cited IEEE Table 7-141, status interpretation, implementation, tests and measurements remain unchanged.

Required outcome / exact fix: replace the parenthetical with “processor docs/00_MILAN_COMPLIANCE_REVIEW.md, section 8 row 14; docs/architecture/06_aecp_engine.md, section 6.10”.

Verification: open those entries at `ed2118035e4cec76fb1b59cfbf8a053aeacc8af8`. This navigation-only correction does not independently make a lens unclean.

## Reconstruction and independent checks

Read the repository operating contract and contribution rules, documentation index, issue body and assignment `issuecomment-6386868969`, the product requirements and architecture/boundary authorities, and processor #200 / merged PR #201. Then reviewed parent `a032c6d6..25f05752` and donor `93fb0b2d..ed211803`, including histories, before reading public executable receipts. No private author material, management source bank, or other reviewer's report informed this verdict or ledger.

- Parent delta: eight paths, three commits. Gitlink, ROM ledger, boundary master/render/manifest, pin/adoption page and CHANGELOG only. Parent HDL and tests are unchanged.
- Required gitlink is exactly `ed2118035e4cec76fb1b59cfbf8a053aeacc8af8`. gPTP remains `55680bff3b287b9a7b0c759f51471fa617c17335`.
- `rtl-delta.log`: stripping comments leaves exactly one changed synthesized token, `UPC_NOTIMPL_C` to `UPC_NSUPPE_C`. Donor top interfaces are unchanged. The existing echo flag remains set; the shared program sets status 11 and sends the command-sized response without gathers. Clock, reset, CDC, state, widths and arbitration structures are unchanged.
- `grep-expectations.log`: parent-wide symbolic/opcode search, supplemented by decimal firmware opcode 39. `sw/firmware/ctrl/aecp/aecp_commands.c:389` rejects a short body first, a non-9 type with NOT_SUPPORTED next, and an absent AVB_INTERFACE index with NO_SUCH_DESCRIPTOR. `sw/firmware/ctrl/test/test_aecp.cpp:836` already expects 7, 11 and 2. The compliance matrix and testing guide contain no conflicting status expectation. Previous adoption rows are explicitly historical, followed by the reversing adoption.
- `rom-regeneration.log`: both native generators reproduce the head and old-pin ledger digests. `ucode.hex` is `1f78804e448c385d633ed4355b7d84100ec13b12c77305c3bc11986653a80a8e`; `ltn_rom.hex` is `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956`.
- Boundary generator check, submodule-doc check, port-contract check, integrator-parameter check, resource-baseline policy check and command-model check all return 0. The boundary check validates six exact gitlinks and the decoded PNG. The PNG was also visually inspected. `CHANGELOG.md:47` and `docs/reference/SUBMODULES.md:260` state status 11, Table 7-141, command echo, unchanged absence/short cases and unchanged interfaces.
- New source-comment lines in the adopted donor delta explain behavior and the issue/specification basis. No new prohibited bench lane, reviewer identity or issue-comment identifier was found in source comments. Existing contextual wording was not treated as a new instance.

## Focused execution and sensitivity

`run_focused.py`, `probe.cpp.inc` and `parent-probe.patch` reproduce the disposable parent integration probe. The explicitly supplied simulator reported version 5.050 before use. Independent light checks ran concurrently with the foreground build; the build used `make -j16`, with eight simulator compilation jobs. No full parent/donor/builder/Yosys bank, hardware, privileged operation or container runner was executed.

`parent-probe.log`, rc 0: **160 checks, 0 failures**, including setup checks and 19 GET_AVB_INFO transactions through `milan_datapath` / `KL_pp_shadow` to the MAC boundary. Fifteen unsupported-target transactions cover ENTITY, CONFIGURATION, AUDIO_UNIT, STREAM_INPUT/OUTPUT, adjacent types, CLOCK_DOMAIN, absent index, 0x0109, 0x8009, 0xffff, cdl 16/20/76 and a repeat after other failures. Their status and complete frame bytes are checked, including Ethernet minimum padding. Three commands at cdl 12/13/15 return BAD_ARGUMENTS. An absent AVB_INTERFACE index returns NO_SUCH_DESCRIPTOR.

`mutation_probe.py`: reverting only the changed donor dispatch constant in the disposable tree yields **30 failures**, exactly fifteen wrong-status checks and fifteen byte-exact echo checks. All fifteen unsupported-target responses become status 1. `parent-mutant.rc` is 2 from make, and `mutation-verdict.log` confirms the expected rejection and byte-exact source restoration. This is a successful negative control, not a source-head gate failure.

Probe development limits: the initial comparison omitted Ethernet padding; it was corrected to compare the full padded frame. An attempted abbreviated setup produced no responses and was replaced with the existing harness's complete pre-AECP setup. Those were disposable probe defects. The final golden and mutant receipts use the same corrected setup and expectations. The original candidate checkout was never edited.

Donor `tb/pp_top/sim_main.cpp:5608` and `:5739` were examined for V1/V1b/V3/V4/V5: real interface success, padded success, absence, truncation and thirteen byte-exact wrong-type rows. Its dispatch controls include old status, wrong fixed length, header-only, dropped/inverted type gate, high-byte alias and wrong length floor. These donor tests were inspected, not rerun as a full bank.

## Published consumer evidence

Source: [public evidence at 3e0d0e08](https://github.com/kebag-logic/milan-fpga/tree/3e0d0e08ac6adcb2aa0f43316d800073f2492e6a/review-evidence/780-r1). `audit_evidence.py` verifies all **109 executable receipt files** against their published manifest hashes. It independently recomputes unique suite membership, summed check counts, latest fast-job outcomes and docs-step outcomes. These are the author's source-head execution receipts, not a manager source bank.

| Consumer | Examined evidence and result |
|---|---|
| Full sweep | Four exact-head shard specs/results/completion logs: 15 + 16 + 17 + 16 unique suites = 64/64; 2,190,096 checks; zero in-suite failures/timeouts |
| milan_dp | `receipts/milan_dp/summary.txt`: 15 PASS, zero FAIL, 11,630 `[ok]` and 1,127 `[PASS]` lines; omitted full log identified by hash/size |
| Firmware | `receipts/firmware/table.txt` and logs: eight commands rc 0; saved-state 109/109 planted defects caught; coverage passes on 30 files; boundary passes |
| Fast gate | Both JSON runs and combined receipt: latest executions give 11/11 successful jobs at the same head with no tracked changes. First six firmware jobs stopped before tests at SDK provenance verification; after verified archive installation those jobs executed successfully. This step-body replica is not hosted/act acceptance |
| behave | `receipts/bdd/behave-head.log`: 14 features, 406 scenarios, 1,977 steps passed; no skipped scenarios. Its model scope is limited as F1 states |
| Yosys / lint | `receipts/yosys/run.log` and rc: 60/60 tops, no unjustified ties; lint log: 89 violations at ratchet 89, PASS |
| Docs | Original step receipts plus successful leg-1 retries and Markdown-interpreter receipts: latest executed steps rc 0 under Make 4.3; two explicitly skipped workflow bodies are not counted as execution. Separate no-git docs/status receipts return 0 |
| Pin records | `receipts/pinchecks/table.txt`: all eleven commands rc 0, including native ROM re-record and byte-identical ledger check |
| Resources | Three comparison logs, route reports, signoff summaries and sequential bank timestamps; unchanged eleventh baseline accepted by independent `check-baseline` |

Builder retry judgment: the original leg-1 tail shows a nonzero saved-state writer self-test subprocess, not a diagnosed load-related root cause. The isolated self-test later passes; the same leg/script hash passes at the same source head both without and with the integration interpreter. The writer and its harness are unchanged in this adoption. I accept the disclosed successful source-head reruns as the required consumer evidence; I do **not** claim that load causation was proved or that the first run was green. The complete first failing child output is not published in this packet, so its cause remains a real limit. The manager's independent current-dev candidate bank remains required.

| Endpoint | Baseline to head | Assessment |
|---|---|---|
| route-1x1 | LUT 51,259 -> 51,182 (-77); FF 53,208 unchanged; slices 15,835 -> 15,825 (-10) | PASS; WNS 0.236 -> 0.165 ns, WHS 0.028 -> 0.036 ns; complete routing, zero errors |
| ooc-1x1 | LUT 23,828 -> 23,845 (+17); FF 20,000 -> 20,002 (+2) | PASS |
| ooc-8x8 | LUT 32,467 -> 32,450 (-17); FF 28,220 -> 28,218 (-2) | PASS |

RAMB36/RAMB18/DSP are unchanged at every endpoint. Route timing retains positive setup/hold, zero TNS/THS and the documented floor. Standalone timing is not a gated claim. No re-baseline or tolerance relaxation was needed. Full synthesis checkpoints and several large logs are represented by public hashes/summaries, not independently rebuilt here.

## Reviewer-owned coverage ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #780 body/assignment; processor #200/#201; `REQUIREMENTS.md:23`; donor engine `:3443`; command model; `grep-expectations.log`; `parent-probe.log`; consumer receipts | R696-1 | 25f05752f7e50e3cf7e27008e434ffde930b4b6f |
| RTL | CLEAN | Donor engine `:3454`, shared E_NSUPPE program; unchanged donor top and `hdl/milan/KL_pp_shadow.sv`; `rtl-delta.log`; port-contract and resource checks | R696-1 | 25f05752f7e50e3cf7e27008e434ffde930b4b6f |
| Robustness | CLEAN | Length/type/existence ordering; donor V1/V1b/V3/V4/V5; 19 parent transactions; repeated refusal and high-byte aliases; `parent-mutant.log` | R696-1 | 25f05752f7e50e3cf7e27008e434ffde930b4b6f |
| Tests | UNCLEAN | `tests/steps/aecp_engine_steps.py:246,511,761`; model `:417,617`; firmware test `:836`; golden/mutant and public receipts. F1 open | R696-1 (applied; no clean coverage banked) | 25f05752f7e50e3cf7e27008e434ffde930b4b6f |
| Docs | UNCLEAN | `CHANGELOG.md:47`; `docs/reference/SUBMODULES.md:260`; diagram/manifest and ROM ledger; issue handoff and PR evidence. F1 open; R1 residue | R696-1 (applied; no clean coverage banked) | 25f05752f7e50e3cf7e27008e434ffde930b4b6f |

All five lenses were applied independently. No clean lens is claimed for the open MINOR. After this independent verdict and ledger were written, PR comments, formal reviews and inline review threads were inspected: only two manager review-start comments were present, with no formal reviews or inline threads. There were no prior public findings to resolve or retain, and no other reviewer report was read. `prior-findings.json` records this reconciliation.

## Limits and pending manager duties

- `checkout-integrity.log` proves actual tracked blob bytes, executable/symlink modes and complete stage-0 index equality for the parent and all five initialized submodules. Both required gitlinks match. The unused historical `external` checkout is absent; its recorded gitlink is verified.
- The independent probe covers this status/echo adoption, not exhaustive reset, backpressure or maximum-frame campaigns. Those paths are unchanged and rely on the reviewed architecture and published consumer regressions. The donor PR documents an existing controller response-sizing interoperability caveat; this adoption follows the explicit command-length echo ruling rather than resolving that separate question.
- Physical calibration is **NOT RUN**. Field-analysis skips, simulation, synthesis and timing reports are not hardware or certification proof.
- `hosted-snapshot.json` is a read-only observation: fast/full were queued, docs/elaboration in progress. No successful hosted context or executed long job is inferred. The manager owns hosted/act acceptance, including distinguishing executed jobs from skipped contexts.
- No manager source bank exists at this exact head, and none is claimed. Before merge, the manager must validate the current-dev merge candidate with builder/native banks and publish its receipts. Source evidence at base `a032c6d6` is distinct from that candidate validation.
- Correct and re-review F1; carry R1 to the residue checklist. Complete both independent reviews, update the reviewer-accepted ledger, wait for all rounds to finish, satisfy required hosted/local evidence, obtain merge authorization, validate containment, and close/move the issue only after the repository completion bar is met.
- No source fixes, commits, pushes, GitHub writes, author contact or merge were performed. Disposable copies remain under `scratch/` and are excluded from publication. Portable scripts and receipts are selected by `MANIFEST.sha256`; build-log paths are redacted without changing verdicts or measurements.

R696-1 FINISHED
