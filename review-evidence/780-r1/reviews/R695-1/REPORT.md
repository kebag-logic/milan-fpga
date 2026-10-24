[R695] POSITIVE - exact head 25f05752f7e50e3cf7e27008e434ffde930b4b6f

Round R695-1: internal, cleared-context, independent review of issue #780 / PR #783 (the fifth parent pin adoption, protocol-processor `ed211803`).
Tree: `5db8e8298734d18c8a50ba24cd8c46140292302b`. Source base and observed live dev: `a032c6d6e3775f145349d5a495c1e1ad12294936`.

The adoption is correct. The gitlink is exact, FPGA-gPTP is unmoved, and every pin-derived record regenerates. At the wrapper boundary, a wrong-type GET_AVB_INFO now answers NOT_SUPPORTED (11) at the command's own length; at the previous pin it answered NOT_IMPLEMENTED (1). My own pass found one MINOR (F1) and one RESIDUE (R1); `receipts/independent_verdict_before_prior_findings.txt` records them as NEGATIVE, written and hashed before I read any other reviewer's comment. The external round reported the same two items independently, and the manager published corrections to the PR body and the issue at 2026-10-24T21:35Z. The head did not change. I checked both corrections against my own probe output, and both are now resolved (see "Prior public findings"). No finding is left open under any lens, so the verdict is POSITIVE.

## Reconstruction

Read in order: AGENTS.md and CONTRIBUTING.md (roles, lenses, completion), docs/README.md, issue #780 body, the manager assignment `issuecomment-6386868969`, the executor's TAKEN / REVIEW READY, processor issue #200 and merged PR #201 (merge `ed2118035e4cec76fb1b59cfbf8a053aeacc8af8`, identical to public processor `main`), and the processor delta `93fb0b2d..ed211803`. Then I reviewed `git diff a032c6d6..25f05752` and its three commits (`e4bd7f5b`, `afdbd99b`, `25f05752`), and after that the published receipts at evidence commit `3e0d0e08`. I read no private author material, lane scratchpad or management checkout. I read other reviewers' comments only after my verdict and ledger were written and hashed.

Parent delta: 8 paths. The protocol-processor gitlink, `syn/yosys/rom_digests.tsv` (+2 rows), the boundary diagram master/SVG/PNG/manifest, `docs/reference/SUBMODULES.md` (pin row plus the adoption section), and `CHANGELOG.md`. No parent HDL, test, model, script or firmware file changes.

## Findings

### F1 - MINOR - Tests, Docs - RESOLVED during this round (public correction, head unchanged)

- Artifact: `tests/steps/aecp_engine_steps.py:246-247` (the GET_AVB_INFO SERVED row, verdict SUCCESS), `tests/steps/aecp_engine_steps.py:512-527` and `:761-779` (the sweep and its partition check), `tests/steps/aecp_engine_model.py:617-628` (`build_aem_command`: default operands are ENTITY[0], so the GET_AVB_INFO descriptor_type at @24 is 0x0000). Also the PR #783 body "The grep" line "The behave model grades only an existing target", and the REVIEW READY wording "milan_dp and the behave model only target AVB_INTERFACE".
- Evidence: `receipts/probe_behave_model_gavb.txt` runs the parent model itself. GET_AVB_INFO with the sweep's own shape (ENTITY at @24, cdl 20) returns status 0, and so do CLOCK_DOMAIN 0 and AVB_INTERFACE 0. The partition step expects 0 for opcode 0x0027. The wire probe (`receipts/probe_gavb_head.log`) shows that the adopted engine answers 11 to this shape, and `receipts/probe_gavb_old93fb.log` shows 1 at the previous pin. So the model does exercise a wrong-type GET_AVB_INFO. Its expected value is a constant that matches neither pin, and the published evidence described its scope wrongly.
- Impact: the evidence for acceptance item 2 gave the wrong reason why no parent expectation changed, and it overstated what the 406 behave scenarios establish about this case. The frozen criterion itself holds: no parent test, model or document expects status 1 here.
- Required outcome: correct the published claim so that it says the inventory model returns SUCCESS for its generic ENTITY[0] operands and does not grade the wrong-type wire response. The model limitation is pre-existing and also covers other target-gated served rows (for example GET_STREAM_INFO, whose wrong-type arm processor PR #201 describes as NOT_SUPPORTED). It is new work outside #780 (AGENTS.md section 4); see S3.
- Resolution verified: the current PR body (updated 2026-10-24T21:35:08Z, head still `25f05752`) and the manager correction on #780 (`issuecomment-6389770127`) now say: "The behave sweep uses generic ENTITY[0] operands and its GET_AVB_INFO inventory row returns SUCCESS; it does not grade the wrong-type wire response. It contains no status-1 expectation for this case. The processor V5 tests and the parent-boundary probe establish the adopted status." That text matches `receipts/probe_behave_model_gavb.txt` exactly (type 0, status 0) and the wire receipts. This finding is the same as the external round's R696-1-F1.

### R1 - RESIDUE - Docs - RESOLVED

- Artifact: PR #783 body, Authoritative references: "its compliance review entry (processor `docs/architecture`, section 8 item 12)".
- Evidence: at `ed211803` the decision is `protocol-processor/docs/00_MILAN_COMPLIANCE_REVIEW.md` section 8, row 14 (line 598). Row 12 is the SET_CONFIGURATION notification decision. The implementation text is in `docs/architecture/06_aecp_engine.md` section 6.10 (lines 974 and 997). This is a navigation pointer only. It changes no clause, status or measurement.
- Exact fix: "processor `docs/00_MILAN_COMPLIANCE_REVIEW.md`, section 8, row 14; implementation in `docs/architecture/06_aecp_engine.md` section 6.10". The current PR body carries this text. This is the same item as the external round's R696-1-R1.

### S1 - SUGGESTION - Tests - builder leg 1 intermittent

On the author's first docs pass, `docs-gates-2/gate_25_1` failed with rc 1 (973.6 s) in `sw/builder/test_builder.py:28826-28831` `test_nvm_firmware_shapes`, which runs `sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test`. The published tail does not include the child's failure output. I judge the retry acceptable for this delta. The diff touches only documentation and the processor gitlink. No file under `sw/firmware/nvm_hosttest/`, `sw/firmware/ctrl_nvm/` or `sw/firmware/common/` references the processor (searched at this head). The same leg then passed twice at the same head, once on CPython 3.12.3 (208.0 s) and once with the integration interpreter (304.2 s), and the self-test passed alone (166 s). Host load as the cause is **not proved**. Suggest a public issue that captures the failing child output if it recurs. I found no existing issue for it.

### S2 - SUGGESTION - Tests - parent wire row for the changed status

No committed parent test grades the wrong-type GET_AVB_INFO status. The processor's V5 rows do, and the PR discloses this as out of the issue's Required list. My disposable `pp_shadow` probe (`scripts/gavb_probe.py`) shows such a row is cheap and discriminating: it fails at the previous pin and passes at this head. A future lane could commit one.

### S3 - SUGGESTION - Tests - track the behave model's target-gate limitation

This is the pre-existing model limitation behind F1. The SERVED inventory gives one verdict per opcode for the sweep's ENTITY[0] operands, and only START/STOP_STREAMING key the verdict on the target type. Suggest a separate public issue so that the inventory's comment "records what each served opcode answers to exactly this shape" (`tests/steps/aecp_engine_model.py:621-624`) is either made true or reworded.

No RESIDUE comment-rule instance: the parent delta adds no source comments. The donor's new source comments (`KL_aecp_engine.sv:1298-1307` and `:3446-3453`) cite issue #200 and the clauses, and they name no bench lane, review round, reviewer ID or issue-comment ID.

## Independent execution at this head (disposable copies under `scratch/`, reviewed clone never edited)

| Check | Receipt | Result |
|---|---|---|
| Wrong-type GET_AVB_INFO through `milan_datapath` / `KL_pp_shadow` (probe, head) | `receipts/probe_gavb_head.log` | CLOCK_DOMAIN 0: status 11, cdl 16, descriptor_type echoed, all common fields and the 60-octet frame graded. ENTITY 0: status 11, cdl 16. Absent AVB_INTERFACE: NO_SUCH_DESCRIPTOR (2). cdl 14: BAD_ARGUMENTS (7). 628 checks, 1 failure, and that failure is the probe's own wrong expectation (see Limits) |
| Same probe, processor at `93fb0b2d` (negative control) | `receipts/probe_gavb_old93fb.log` | CLOCK_DOMAIN 0 and ENTITY 0 answer status 1 at cdl 16. The two status-11 checks fail as they should, so the probe discriminates the change. Absence and short cases are identical to head |
| `pp_shadow` base leg, unmodified, head | `receipts/pp_shadow_base_head.log` | 610 checks, 0 failures, RESULT PASS |
| `milan_dp`, head, `make -j6 SIM_JOBS=2 VERILATOR_JOBS=2` (pinned Verilator 5.050, identity printed) | `receipts/milan_dp_head.log`, `.summary.txt` | rc 0. RESULT PASS 15, RESULT FAIL 0. 11,630 `[ok]`, 1,127 `[PASS]`, 0 `[FAIL]`, the same figures as the author's receipt. Every GET_AVB_INFO send is AVB_INTERFACE 0 (`sim_nxn.cpp:1721,1770,10301`, `sim_gptp.cpp:1036`). A first attempt with SIM_JOBS=3 was refused by `sim_pool` before any simulation (my invocation error, `milan_dp_head_try1_simjobs3_refused.*`) |
| `cd tests && behave --no-capture -f plain` | `receipts/behave_head.log` | 14 features, 406 scenarios, 1,977 steps passed, 0 skipped |
| Behave model on GET_AVB_INFO | `receipts/probe_behave_model_gavb.txt` | Status 0 for every target (F1) |
| ROM ledger re-record (`ooc.sh --record-rom-digests` + `git diff --exit-code`) | `receipts/rom_record.log`, `.rc` | rc 0, byte-identical. `ed211803` rows equal the `93fb0b2d` rows (ucode `1f78804e…a80a8e`, ltn `23cc67ee…e7e956`) |
| Ledger consulted at this pin (`ooc.sh tcam`), then a planted wrong ucode row | `receipts/ooc_tcam_digest_verify.*`, `ooc_tcam_digest_mutant.*` | Verify rc 0. The mutant is refused, rc 2, with "content digest mismatch for ucode.hex at protocol-processor pin ed211803…". Ledger restored |
| Pin-record and ratchet checks (10 commands) | `receipts/pincheck_summary.tsv`, `pincheck_*.log` | All rc 0: baseline PASS 3 endpoints; boundary diagram OK (6 exact gitlinks, decoded PNG); time-sync diagram OK; submodule docs OK; gPTP docs OK; port contracts OK; naming 95 = 95; test-evidence PASS; integrator params 29/29/29; lint PASS 89 <= 89. With the ROM re-record these are the 11 pin-record checks |
| Final clone state | `receipts/clone_state_final.txt` | HEAD/tree exact, write-tree equals tree, worktree == index == HEAD, 0 status entries (ignored files included), `ls-files -s` digest equals `ls-tree -r` digest (blob ids and modes), gitlinks `ed2118035e4c…` / `55680bff3b28…` checked out and clean |

Grep (acceptance item 2), re-run independently over the parent with submodules excluded: `GET_AVB_INFO|0x0027|avb_info` gave 204 hits and `NOT_IMPLEMENTED` variants gave 338 hits, triaged by file. Findings:
- Firmware AECP `sw/firmware/ctrl/aecp/aecp_commands.c:388-397` already answers NOT_SUPPORTED to a non-9 type, after the length check and before the existence check.
- milan_dp and `tb/tools/hive_compliance.py:450` target AVB_INTERFACE only.
- `docs/reference/MILAN_COMPLIANCE_MATRIX.md:129`, `docs/testing/TESTING.md`, `FR_NFR.md` and the register map name no status for this case.
- The behave model expects SUCCESS, not 1 (F1).
- The remaining hits are history: the fourth adoption's `CHANGELOG.md:143` and `docs/reference/SUBMODULES.md:228`, both explicitly reversed by the new sections.

The claim "no parent test, model or document expected status 1" (`CHANGELOG.md:56`, `SUBMODULES.md:274`) holds.

## Published author evidence examined (source-head receipts, not a manager bank)

From `review-evidence/780-r1` at `3e0d0e08`:
- **Sweep:** four shard specs at this head and base, each exit 0; `suite-tally.out` shows 2,190,096 checks and 0 in-suite failures.
- **milan_dp summary:** matches my run exactly.
- **Firmware `table.txt`:** 8 commands, all rc 0.
- **rtl-fast `combined.txt`:** 11/11 needs jobs succeed, taking each job's latest run. The six firmware jobs are from run 2, after the SDK was installed from its pinned archive. Their first run stopped at SDK provenance verification, before any test ran.
- **Docs `all.out`:** 44 steps under Make 4.3, with one failure (leg 1, S1), leg-1 passes on both interpreters, and the no-git docs/status checks both rc 0. Two steps were skipped by rule: the local act-runner contract and the git-strip body, which the separate no-git receipts cover. Skipped steps are not counted as executed.
- **Vivado check logs** against the eleventh record, each RESULT PASS:
  - route-1x1: LUT 51,259 -> 51,182 (-77), FF 0, SLICE 15,835 -> 15,825 (-10), WNS 0.236 -> 0.165 (tolerance 0.25), WHS 0.028 -> 0.036, route complete
  - ooc-1x1: LUT +17, FF +2
  - ooc-8x8: LUT -17, FF -2
  - RAMB36/RAMB18/DSP unchanged everywhere
- **Lint and Yosys receipts:** rc 0.

I did not rebuild any Vivado endpoint (one heavy run at a time, and it is owned by the author/manager), so the resource figures rest on the published receipts.

## Reviewer-owned coverage ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #780 Required list and assignment; processor #200 and PR #201; `protocol-processor/hdl/aecp/KL_aecp_engine.sv:3446-3462` (wrong type -> `UPC_NSUPPE_C` with `echo_r` set, length checked before type); `CHANGELOG.md:47-59` and `docs/reference/SUBMODULES.md:260-274` against IEEE 1722.1-2021 Table 7-141 (1 = command type unsupported, 11 = implemented command, unsupported target) and 7.4.40; wire probe head/old (`receipts/probe_gavb_*.log`): 11 at cdl 16 with echo now, 1 before, absence and short cases unchanged; parent grep triage | R695-1 | 25f05752f7e50e3cf7e27008e434ffde930b4b6f |
| RTL | CLEAN | Processor delta `93fb0b2d..ed211803` under `hdl/`: only `KL_aecp_engine.sv` (one synthesised constant, comments) plus `aecp_commands.json` (status set); no port, parameter, width, reset or FSM change; parent `hdl/milan/KL_pp_shadow.sv` and `milan_datapath.sv` unchanged and do no status post-processing; ROM digests equal across pins; `check_port_contracts`, `check-integrator-params` and lint at this head; published Vivado route/ooc PASS | R695-1 | 25f05752f7e50e3cf7e27008e434ffde930b4b6f |
| Robustness | CLEAN | Ordering length -> type -> existence observed at the wire: cdl 14 BAD_ARGUMENTS; a wrong type answers 11 whether the descriptor exists (ENTITY 0) or not (CLOCK_DOMAIN 0 in this image); absent AVB_INTERFACE 0x7777 NO_SUCH_DESCRIPTOR at both pins; the plane keeps serving after the refusals (the rest of the `pp_shadow` base leg passes after the probe rows); donor V1/V1b/V3/V4/V5 rows, inspected rather than run; ledger refusal mutant | R695-1 | 25f05752f7e50e3cf7e27008e434ffde930b4b6f |
| Tests | CLEAN | `pp_shadow` base 610/0; probe and negative control (`receipts/probe_gavb_*.log`); `milan_dp` 15 PASS / 0 FAIL; behave 406/406; model probe; `tests/steps/aecp_engine_steps.py:246,512,761`, `aecp_engine_model.py:617`; published sweep/firmware/rtl-fast receipts. F1 resolved by the verified public correction; S1-S3 optional | R695-1 | 25f05752f7e50e3cf7e27008e434ffde930b4b6f |
| Docs | CLEAN | `CHANGELOG.md:11,47-59`; `docs/reference/SUBMODULES.md:25,260-274`; `docs/diagrams/submodule_boundaries.{drawio,svg,png}` and `PNG_MANIFEST.json` (generator `--check` OK); `syn/yosys/rom_digests.tsv:72-73` (re-record identical); line ranges cited in the PR verified; corrected PR body and `issuecomment-6389770127`. F1 and R1 resolved | R695-1 | 25f05752f7e50e3cf7e27008e434ffde930b4b6f |

## Prior public findings on this PR

Read only after `receipts/independent_verdict_before_prior_findings.txt` was written (sha256 `d7ed773d291e44be125cb4c01b55c92e0d7fde0c07e921e31d5242c2b6e8ece4`).
- **R696-1-F1** (MINOR, Tests and Docs, behave model scope claim) is the same as my F1. It is RESOLVED at this head by the PR body and `issuecomment-6389770127`, checked against `receipts/probe_behave_model_gavb.txt`.
- **R696-1-R1** (RESIDUE, Docs, compliance pointer) is the same as my R1. It is RESOLVED in the PR body, and I verified it at `ed211803` (`00_MILAN_COMPLIANCE_REVIEW.md:598`, `06_aecp_engine.md:974,997`).
- No other public findings, formal reviews or inline threads exist on PR #783.

## Real limits

- My probe's AVB_INTERFACE 0 row expected SUCCESS and got NO_SUCH_DESCRIPTOR at both pins. This is a probe expectation error, not a defect: `pp_shadow`'s synthetic descriptor image (`tb/verilator/pp_shadow/sim_main.cpp:1009-1062`) carries no AVB_INTERFACE. The SUCCESS path is covered by `milan_dp` B2 and OWNERLESS rows.
- Not rerun by me: the full sweep, Yosys 60 tops, the firmware gate set, the docs gates, rtl-fast, and all three Vivado endpoints. These rest on the author's published source-head receipts. Donor suites were inspected, not run.
- Processor PR #201 records an existing interoperability caveat: the reference controller stack may size a non-NOT_IMPLEMENTED answer against the GET_AVB_INFO response form, cdl 32 + 4N. The issue explicitly requires the echo at command length, so this adoption follows that ruling and does not resolve the question.
- S1's failing child output is not published, so its cause is unknown.
- Physical calibration is NOT RUN. Field skips, simulation, synthesis and timing are not hardware or certification proof.
- Hosted contexts (`receipts/hosted_snapshot.txt`, a read-only observation at 2026-10-24T22:03Z): 45 completed success, 1 skipped (Physical gPTP), and 5 in progress, including Verilator shards 8/16 and 9/16. I make no hosted acceptance claim.

## Pending manager duties

- No manager source bank exists at this exact head, and I claim none. The manager must build and validate the current-dev merge candidate (builder and native banks), and publish its receipts on the PR.
- The manager owns hosted/act acceptance, including telling executed jobs from skipped contexts, and must wait for the in-progress hosted contexts.
- Carry R1 to the residue checklist (already applied to the PR body), and decide whether to open issues for S1 and S3.
- Complete the two-positive review bar and confirm no round is in flight.
- Obtain explicit merge authorization, check post-merge containment, and close/move #780 only when the completion bar is met.

No source fixes, commits, pushes, GitHub writes, author contact, sub-agents, containers, act, hardware or merge. Publishable content is this file plus the files listed in `MANIFEST.sha256`; `scratch/` is excluded.

R695-1 FINISHED
