[R871] POSITIVE - exact head a16899b1fb2a0c731ebf18476d1a38627254ea4e

# R871-2: internal cleared-context delta review of PR #953 (#943, relates to #665), round 2

- **Head:** `a16899b1fb2a0c731ebf18476d1a38627254ea4e`, tree `4a56ad08834166f69a5ef066b727978485ac0188`.
- **Delta reviewed:** `502b041c..a16899b1`, two commits:
  - `106c7203`: the AppOutputs test and its plant rows.
  - `a16899b1`: the `declaring-outputs` harness arm.
- **Full PR diff:** `0839453f..a16899b1` was read for context. Code the delta does not touch keeps its round-1 lens verdict.
  - No firmware source changed since `502b041c`. `git diff 502b041c..a16899b1 -- sw/firmware` touches only `test/test_aecp.cpp` and `test/aecp_output_mutants.py`.
  - The PR diff touches no RTL and no submodule.
- **Order of work:**
  - I reconstructed the task from AGENTS.md and CONTRIBUTING.md, #943's body and its four public comments, the PR body and the delta. The four comments are the classification, TAKEN and both REVIEW READY comments.
  - I read the prior public findings (R872-1, R871-1) only after my own pass over the diff.
- **Verdict:** POSITIVE.
  - No BLOCKER, MAJOR or MINOR is open.
  - Two SUGGESTIONs and one RESIDUE are recorded.
  - The margin risk is judged acceptable for this PR and carried to the manager's final-image measurement (section 4).

## 1. Evidence base

**Author packet.** Archive `f9f1e85d91749fbba4506b54236e63f3eeba7ca6`, `review-evidence/943-r1/author-r2`.
- All 49 files listed for `author-r2/` in `MANIFEST.json` match their published sha256, and no file is unlisted (`receipts/author-packet-verification.txt`).
- Its console receipts name a clean clone of `a16899b1` (`HEAD a16899b1 DIRTY 0`).
- **Not exact-head runs:** the three plant receipts (`budget/plant-*.txt`) ran on `502b041c` with round 2's change applied (`DIRTY 7`). That is every delta file except the design-doc paragraph. I re-ran one plant on the exact head (below).

**My own probes.** All ran at the exact head. Scripts are in `scripts/` (`reproduce.sh` reruns them all); raw receipts are in `receipts/`.

| Probe | Result | Receipt |
|---|---|---|
| `declaring-outputs` arm, 1x1/1if, groups `aecp-fanout,aecp-outputs` | rc 0. 0 refusals, 0 budget misses (0 of 21), 0 of 509 passes over the share. `DECLARING aecp-outputs: 6 completion(s) in 6 record(s), 1 in rounds of THE RETRY, 19 GET_STREAM_INFO(s)` | `receipts/budget-1x1-declaring.log` |
| `record_classes.py` over that leg alone | Held other dearest **23,330** cycles, 245 us by the rule, stated 245 (the completed SET_STREAM_INFO). Reported paced 30,226 (320 us) and 29,535 (315 us). The three declaring paths are present. The refusals are only for the absent formal legs (arm A, arm B), as expected for a lone leg. | `receipts/record-classes-own-1x1-declaring-leg.txt` |
| Answers and records decoded from that run | 16 notices and 3 responses each carry flags `f2000000` and the allocated MAAP address (`91e0f0001f7b` + n). REGISTERING is set only on output 0's responses after the Listener Ready. Six STREAM_INFO records each ran exactly 1 completion (GET x3, SET NOT_SUPPORTED, SET ENTITY_LOCKED, SET SUCCESS). One completion ran in a round. | `receipts/own-1x1-declaring-answers.txt` |
| Plant `completion-unexecuted`, 8x8/1if, exact head | `CONTROL completion-unexecuted caught: 14 finding(s)`, 0 refusals, rc 0 | `receipts/budget-8x8-unexecuted.log` |
| Every `aecp_output_mutants.ROWS` row planted alone, 1x1, two interfaces (the campaign's arm) | Unplanted rc 0. **17 planted, 0 escaped**, each failing on its named words | `receipts/fw-plants-1x1-if2.log`, `receipts/fw-plants-1x1-if2-results.json` |
| The four interface and flag rows, 8x8, two interfaces | Unplanted rc 0. 4 planted, 0 escaped | `receipts/fw-plants-8x8-if2.log`, `receipts/fw-plants-8x8-if2-results.json` |
| `record_classes.checks()`, which includes `declaring_outputs.checks()` | 41 checks, 0 failures | `receipts/record-classes-checks.txt` |
| Clone integrity after the probes | HEAD and tree unchanged; index tree `4a56ad08`; worktree equals HEAD; 0 porcelain lines; gitlinks unchanged | `receipts/clone-integrity.txt` |

- **Determinism:** my 1x1/1if figures equal the author's receipts exactly. That covers 23,330, 30,226 and 29,535 cycles, the 6 + 1 completions and the 19 answers.
- **Tools:** Verilator is the scoped pinned 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`).
- **Redaction:** in two console logs, host home paths are replaced by `<home>`.

**Hosted state at this head** (`receipts/hosted-checks-a16899b1.txt`, a read-only snapshot):
- Passed: `wire-accountability`, `bdd-conformance`, `verilator-lint`, `Prepare pinned Yosys`.
- Pending or queued: the Verilator shards, the firmware jobs, docs, elaborate and Yosys.
- Skipped: `Physical gPTP`, which is not hardware proof.
- The manager owns hosted and act acceptance.

## 2. Prior findings, resolved or retained at this head

| Finding | Status | Evidence |
|---|---|---|
| **R872-1-F1** MAJOR (Conformance, RTL, Robustness, Tests): no maintained arm executes the declaring-output completion | **Resolved** | The breakdown follows the table. |
| **R872-1-F2** MINOR (Tests, Docs): the exploratory fixture cleared `brief`, which affects its figures and causal claim | **Resolved** | The breakdown follows the table. |
| **R872-1-R1** RESIDUE (Docs): PR body destination, step and roles | **Resolved** | The PR body reads `943-out-status -> flip-train-1117` and "joins the flip train as step 13". Roles are `[R871]` and `[R872]`. The future `dev-soft-core` base is stated as conditional. |
| **R871-F1** MINOR (Tests): AppOutputs could not fail for MSRP_FAILURE_VALID beside REGISTERING_FAILED, or for another interface's Listener | **Resolved** | The breakdown follows the table. |
| **R871-S1** SUGGESTION: a formal declaring-face arm, and an owner ruling on margin | **Addressed.** The arm is built, with a Listener registered. The margin half is carried to the owner and manager (section 4). | |
| **R871-S2** SUGGESTION: stale per-shape plant receipts | **Addressed.** Round 2 publishes the 17-row receipts and labels round 1's as superseded. My 17-of-17 run agrees. | |

**R872-1-F1, how it is resolved:**
- **The fixture matches the real face.** `declaring_outputs.py:69-88` answers flags `0xf2000000` for type 6, in both brief and whole observations, and keeps the caller's `brief`. The real face does the same: `aecp_face.c:169` reads only word 0 when brief and never writes `brief`.
- **Only whole observations are completed.** The completion is entered at `ctrl_app_aecp.c:85` only for whole observations with STREAM_DEST_MAC_VALID. Each source-port entry is counted through `completion_source`.
- **The run fails on every gap the finding named.** `findings()` (`:261-291`) is wired into `run.py:987`. It fails the run when:
  - a whole STREAM_INFO record of an output does not run exactly one completion;
  - any other record runs one;
  - no round runs one;
  - an answered GET, an accepted SET, an ENTITY_LOCKED or a NOT_SUPPORTED never ran it;
  - a GET answer lacks the completion's values.
- **The rows account for the work.** They cover the declared Talker's notice fanned out in THE RETRY, and a SET and a GET behind a held egress past the ring's room. Each fits within its 20 ms at both points (author rows; my 1x1/1if run shows 0 misses).
- **record_classes holds the completed records.** It holds every completion-running record at its class's statement (`record_classes.py:192-197`). It refuses a pass at 1x1/1if or 8x8/1if unless it has an answered GET, an accepted SET and a refused SET, each completed (`:106`, `:261-268`). The author's real-leg receipts `record-classes-*-without-declaring.txt` show `RESULT: FAIL` with all three named.
- **The three negative controls are caught at both points:**
  - `completion-unexecuted`: 7 records at 1x1/1if and 14 at 8x8/1if. I reproduced the 8x8/1if one at the exact head.
  - `brief-completed`: 3 findings at each point.
  - `completion-dearer`: 7 and 14 held records over `record.aecp`.
- **Nothing it rests on moved.** No bound, stated cost or firmware source changed.

**R872-1-F2, how it is resolved:**
- `declaring_outputs.fixture_findings` (`:294-309`) refuses a fixture that clears `brief`. The self-test plants exactly that (`:322-323`), and it passes in my checks run.
- The author's `brief-probe.txt` shows a brief read gives brief=1 with 0 source calls. A whole read gives 1 call, with `91e0f0000100`.
- On the arm's image the map edits' and largest-command records ran 0 completions. Otherwise `record_findings` would have failed my run.
- The round-1 figures are withdrawn in the PR body and in round 2's REVIEW READY, and no excess is apportioned.

**R871-F1, how it is resolved:**
- `test_aecp.cpp:896-912` pins the whole flags word (`0xf2000040` or `0xf2000000`) under Ready, Ready Failed and Asking Failed.
- At two interfaces it first registers the stream's Listener, Asking Failed, on the other interface. It keeps that Listener registered and expects neither flag.
- The new rows are `output-registering-failed-msrp-failure-valid` and `output-listener-any-interface`. My plants at 1x1/2if and 8x8/2if catch both on their named words ("never MSRP_FAILURE_VALID", "another interface's Listener is not its own").
- At one interface the two interface rows are the fix's own code, as stated. The campaign's arm runs two interfaces.

## 3. Findings at this head

### R871-2-S1 SUGGESTION - Tests - `tb/verilator/ctrl_service_budget/declaring_outputs.py:209-213` - the arm's value check accepts any base per interface
- **Evidence:** `answer_findings` requires a MAAP-pool address and one base per interface (`dest - n` constant). It does not require the base to be the range MAAP allocated. So a completion that read source n+1's address for every output would pass the arm's value check.
- **Impact:** small. The conformance check is `AppOutputs`, which pins `BASE+n` exactly (`test_aecp.cpp:894`, `:912`). The arm's job is cost and execution.
- **Possible change:** take the base from the PROBE_TX_RESPONSE's destination, or from the testbench's MAAP log, and require `base + n`.

### R871-2-S2 SUGGESTION - Tests - `tb/verilator/ctrl_service_budget/declaring_outputs.py:188-199` - SET_STREAM_INFO answers are timed and counted, not value-checked
- **Evidence:** `stream_infos` collects only GET_STREAM_INFO (0x000F) frames. The completed SET_STREAM_INFO response and its notices (`notify:...:000e`) are graded by row and by record, but their `stream_dest_mac` and flags are not read.
- **Impact:** small. #943's acceptance names GET_STREAM_INFO, and both commands use the same completion function.
- **Possible change:** extend `stream_infos` to 0x000E responses of a STREAM_OUTPUT.

### R871-2-R1 RESIDUE - Docs - `tb/verilator/ctrl_service_budget/declaring_outputs.py:296`, `:323` - a review-finding ID in source
- **Evidence:**
  - The docstring at `:296` reads "(a brief observation that leaves it cleared is completed, R872-1-F2)".
  - The self-test check label at `:323` reads "(R872-1-F2's)".
  - This breaks the comment rule: no review rounds or reviewer IDs in source. It is a new instance in the delta. A grep of the delta's added lines for lane, round and reviewer labels finds no other.
- **Why it is RESIDUE:** it is wording only. It changes no behaviour, check or figure; the label string only names a check.
- **Exact fix:**
  - At `:296`, replace "R872-1-F2" with "#943".
  - At `:323`, change the label to `"the declaring arm refuses a fixture that clears brief"`.

## 4. The margin risk (task item 4): judgment

**The measured margins.** The rule is a record's cycles at the CPU clock, plus 5 %, rounded up to 5 us (`record_classes.py:133`).

| Record | Leg | Measured cycles | Limit (statement) | Margin |
|---|---|---:|---:|---:|
| Completed SET_STREAM_INFO, 1x1/1if | declaring arm, held | 23,330 | 23,333 (245 us) | **3 cycles**, reproduced exactly |
| Paced edit, 1x1/1if | arm B, formal, held | 29,422 | 29,523 (310 us) | 101 cycles |
| Largest legal command, 8x8/1if | arm B, formal, held | 163,520 | 163,809 (1,720 us) | 289 cycles |

**On the declaring arm's own image:**
- The records that run no completion measure 30,226 cycles (320 us) and 167,522 cycles (1,760 us). They are reported, not held.
- My decode confirms those records ran 0 completions. So their excess comes from placement, not from this PR's work.
- The fixture's `bridge_source` wrapper adds one call to every completion. Its completed records are therefore, if anything, dearer than the product's.

**Judgment: acceptable for this PR. No defect of this PR is owed.**
- **Every held bound is met.** Every record that a formal or declaring leg holds is within its statement at this head.
- **The fragility predates this PR.** It is the train's sensitivity to code placement. Round 1 measured 29,331 to 31,749 cycles for the same paced work across this branch's images. Round 2 changes no firmware source, so the formal image's figures are round 1's.
- **A bad merge cannot pass silently.** `record_classes.py` now refuses any final pass at 1x1/1if or 8x8/1if that lacks the declaring leg. So if a merged image's placement pushes the completed SET_STREAM_INFO past 245 us, the candidate measurement refuses it.
- **Restating is not open to this PR.** Restating the paced edit would put 1x1/1if's last-queued-notice row over its 140 ms bound; the author's 325 us trial gave 141.54 ms.
- **The remaining question is the owner's.** How far the AECP class statements must stand from placement is an owner ruling (R871-S1's second half), not a correctness defect of this lane.

**Carried as a pending manager duty.** At the merge turn, the current-dev candidate's final-image measurement must include:
- the `declaring-outputs` leg at 1x1/1if and at 8x8/1if;
- arm A and arm B, graded together with it by `record_classes.py`;
- `flip_grade.py --check`.

If any held record refuses there, the owner rules before merge: either restate against the 140 ms bound, or control placement. Dropping the declaring leg is not a remedy.

## 5. Lens coverage at this head

### Conformance: PASS
- **Artifacts:** `sw/firmware/ctrl/app/ctrl_app_aecp.c:54-90` (unchanged since `502b041c`), `test_aecp.cpp:866-912`, `receipts/own-1x1-declaring-answers.txt`.
- **Checked against #943's acceptance and Milan v1.2 5.4.2.10.2, Tables 5.8 and 5.11:**
  - `stream_dest_mac` is the Talker's MAAP address.
  - REGISTERING is set for a matching Listener on the output's own interface.
  - REGISTERING_FAILED is set for Asking Failed alone, and MSRP_FAILURE_VALID never.
- **Checked against IEEE 1722.1-2021:** the flag bits (`0xF2000000`) and the status codes in `WHOLE_STATUSES`.
- **Executed:** answers from the arm's run carry the allocated address and the correct REGISTERING.

### RTL: PASS
- **Artifacts:** `record_classes.py:133` and `:192-197`, the budget receipts, and `git diff --stat 0839453f..a16899b1 -- hdl protocol-processor gptp-processor third_party external tb/verilator/ctrl_service_budget/sim_main.cpp`, which is empty.
- **No RTL change:** no RTL, testbench or contract changed.
- **The new path's CPU service envelope is now measured and held at both points.** This was the resource and timing side of R872-1-F1.
  - 1x1/1if: 245 of 245 us.
  - 8x8/1if: 220 of 265 us.
  - Rows: 1.3 to 9.1 ms, each of 20 ms.
- **Margin:** judged in section 4.

### Robustness: PASS
- **Artifacts:** `declaring_outputs.py:118-185` and `:245-291`, `test_aecp.cpp:893-899`.
- **Refused and backpressured paths:** NOT_SUPPORTED, ENTITY_LOCKED under another controller's lock, and a held egress past the ring's room are each completed and timed.
- **Ordering:** notices before the Listener, responses after it.
- **Persistence:** the other interface's Listener stays registered across the steps and after the output's own Listener sends its Leave (Lv).
- **Partial runs:** a run of only some groups cannot bank coverage, because record_classes requires all three declaring paths.

### Tests: PASS (S1 and S2 optional)
- **Artifacts:** `declaring_outputs.py:294-379`, `record_classes.py:356-416`, `aecp_output_mutants.py:39-66`, and my probes.
- **Self-checks:** all 41 pass.
- **Plants:**
  - `completion-unexecuted` is caught at the exact head at 8x8/1if.
  - The other plants are caught in the author's receipts at both points.
  - All 17 firmware rows are caught at 1x1/2if, and 4 of 4 at 8x8/2if.
- **Independence from the implementation:** the test pins the face's whole flags word and the exact `BASE+n`, rather than restating the code.

### Docs: PASS (RESIDUE R871-2-R1)
- **Artifacts:** `tb/verilator/ctrl_service_budget/README.md:261` and `:345-363`, `docs/design/SPLIT_CONTROL_MEMORY.md:3000`, `build.py:134-137`, `run.py:612-616`, the PR #953 body.
- **Figures:** they match my reproduction and the author's receipts. That covers 23,330 cycles at 245 us, 20,707 at 220 of 265 us, 30,226 at 320 us and 167,522 at 1,760 us.
- **Behaviour:** the arm, its findings and its plants are described as implemented.
- **PR body:** the withdrawn figures and the destination are corrected.
- **Docs gate:** its steps return rc 0 at `a16899b1` (author receipt). The exception is the RV32 SDK provenance check, which fails at base too.

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `ctrl_app_aecp.c:54-90`, `test_aecp.cpp:866-912`, `receipts/own-1x1-declaring-answers.txt` | R871-2 | `a16899b1fb2a0c731ebf18476d1a38627254ea4e` |
| RTL | CLEAN | Empty RTL and testbench diff; `record_classes.py:133,192-197`; `receipts/record-classes-own-1x1-declaring-leg.txt`; author `budget/record-classes-*.txt` | R871-2 | `a16899b1fb2a0c731ebf18476d1a38627254ea4e` |
| Robustness | CLEAN | `declaring_outputs.py:118-291`, `test_aecp.cpp:893-899` | R871-2 | `a16899b1fb2a0c731ebf18476d1a38627254ea4e` |
| Tests | CLEAN | `declaring_outputs.py:294-379`, `record_classes.py:356-416`, `aecp_output_mutants.py`, `receipts/fw-plants-*`, `receipts/budget-8x8-unexecuted.log`, `receipts/record-classes-checks.txt` | R871-2 | `a16899b1fb2a0c731ebf18476d1a38627254ea4e` |
| Docs | CLEAN (RESIDUE R871-2-R1 carried) | `README.md:261,345-363`, `SPLIT_CONTROL_MEMORY.md:3000`, PR #953 body | R871-2 | `a16899b1fb2a0c731ebf18476d1a38627254ea4e` |

## 7. Real limits

- **Not run by me:** the full firmware gate, docs gate, twin, ledger and release image. For those I relied on:
  - the author's exact-head receipts: firmware gate PASS on all 4 shards (1,806 invocations), fw_coverage PASS, and the docs steps;
  - round 1's carried receipts, for the firmware that has not changed.
- **Not reproduced by me:**
  - the unplanted 8x8/1if declaring run and its record_classes figures;
  - the `brief-completed` and `completion-dearer` plants;
  - the formal arm A and arm B legs.
- **Plant receipts not on the exact head:** the author's three plant receipts ran on `502b041c` plus round 2's files. The only difference is one Markdown paragraph, which is not built.
- **Inherited firmware-boundary refusal:** the hosted `firmware-boundary` job is expected to refuse `sink_mutants.py` and `talker_notice.py`.
  - The author's receipt shows the same text at base `0839453f`, so this is inherited, not caused by this delta.
  - `declaring_outputs.py` is not refused: it does not name `sw/firmware/ctrl` (see `ctrl_configs.BUILDER_NAMES`).
- **Hosted contexts:** mostly pending when I read them.
- **Hardware:** physical calibration was NOT RUN, and field skips are not hardware proof.
- **Source bank:** no manager source bank ran at this head, and none is claimed.

## 8. Pending manager duties

1. **Final-image measurement at the merge turn.** On the current-dev candidate (source base `0839453f`, live dev `e275d795`):
   - run the declaring-outputs leg at 1x1/1if and 8x8/1if, with arm A and arm B, through `record_classes.py`;
   - run `flip_grade.py --check` (section 4);
   - link the receipts on the PR.
2. **Hosted and act acceptance of the exact head.** The Verilator shards, firmware jobs, docs, elaborate and Yosys were pending at my snapshot. The inherited `firmware-boundary` refusal needs classifying.
3. **Residue checklist.** Carry R871-2-R1.
4. **Owner routing.**
   - The AECP class statements' margin against placement (R871-S1's second half) goes to the owner.
   - The author also reported that the split's GET_TX_STATE never sets REGISTERING_FAILED. That was seen beside this PR and is out of its scope; it goes to a new issue.

R871-2 FINISHED
