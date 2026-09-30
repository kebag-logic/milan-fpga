[R419] NEGATIVE - exact head f963fe9ac591b8a42547700468fc875db27ae5ab

# R419-1 external review: processor PR #140 (lane C5a, AECP deadlines and the scoreboard)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #140, issue #81 (relates), #57 (closes), #84 (relates).
- Exact head `f963fe9ac591b8a42547700468fc875db27ae5ab`, tree `032d052c6fc98564760fd0fc1b33872227ff22a1`, base `0451d83d9d3f2ed5f4513c59ac5ac219ad9dd7ff`, five commits (04c2f5c, 9a82661, fb0c13c, f1898da, f963fe9).
- Round R419-1, external reviewer, cleared context, own detached clone. All five lenses applied.

Verdict: NEGATIVE. There is one open MAJOR finding and three open MINOR findings. Conformance, Tests and Docs are UNCLEAN at this head. RTL and Robustness are CLEAN.

## 1. Reconstruction (what was read, in order)

1. Workflow rules: AGENTS.md and CONTRIBUTING.md from kebag-logic/milan-fpga at `c530a48e`. This repository has neither file. Also this repository's `README.md` and `docs/README.md`.
2. Issue bodies and comments:
   - #81: the frozen acceptance 1-4, and the assignment comment 5915626788 (design first; STOP only for a port, parameter or parent-visible change).
   - #57: acceptance 1-3.
   - #84: acceptance 1-4.
   - the PR #140 body and its two review-start comments.
3. Authorities:
   - `docs/architecture/08_timing.md` §4 (F08.3, T-AECP-RESP, T-BUDGET-*);
   - `docs/architecture/03_packet_engine.md` §6 (F03.7, rules (d) and (e));
   - `docs/architecture/06_aecp_engine.md` §6.9, §8 and §8.1;
   - `docs/00_MILAN_COMPLIANCE_REVIEW.md` REQ-MVU-005 (:400);
   - `hdl/packet_engine/KL_pp_scoreboard.sv` (the matrix).

   The IEEE 1722.1 §9.3.2.6 and Milan §5.4.3.3/§5.4.3.4 clauses were read through their in-tree quotations. The specification PDFs are not in the tree.
4. `git diff 0451d83d..f963fe9a`, which touches 49 files, and the history of all five commits.
5. Public evidence at kebag-logic/milan-fpga `c530a48e` `review-evidence/ppC5a-r1`:
   - `MANIFEST.json`;
   - `author/HANDOFF.md` (sha256 `b709e8b5…`, matches the manifest);
   - `author/PR-BODY.md`;
   - `author/parent-adaptation-132-c1.patch`.

   That tree contains no manager bank receipts, and the issue and PR carry no manager evidence comment yet. The manager's static/builder and native bank results were therefore not inspectable (section 7).
6. Prior public findings on PR #140. The PR has 0 reviews and 0 review comments. Its two issue comments are review-start notices. There is no prior finding to resolve or retain.

## 2. Executable evidence produced by this round

Everything below ran in the foreground, in a scratch export of the exact head under `scratch/`, with the pinned simulator 5.050 (`receipts/verilator-identity.txt`). Build parallelism was capped at 8, except for the two builds noted in section 7.

| Receipt | What | Result |
|---|---|---|
| `receipts/suite-pp_top.log` | `make -C tb/pp_top`, all three builds | 8,112 checks, 0 FAIL, rc 0 (default build 8,036, fixture 20, timebase 56) |
| `receipts/suite-ucpu.log` | `make -C tb/ucpu` | 415 checks, 0 FAIL, rc 0 |
| `receipts/head-deadline.log`, `receipts/head-hazards.log` | sections DL and HZ alone | DL 29/0, HZ 83/0 |
| `receipts/aecp-mutants.txt` (+ `aecp-mutants/` logs) | `tb/pp_top/aecp_mutants.py`, all arms | 5 controls PASS, 30 arms KILLED, rc 0. Every per-arm count matches the author's record |
| `receipts/d3-two-controls-head.txt`, `…-kill-tied-off.txt` (+ dirs) | `d3_mutants.py --only hold_released_at_go dispatch_not_held`, at head and with `dl-kill-tied-off` applied | head: 17 and 6 failing checks, each including one `D3O6`. Kill tied off: 16 and 5, no `D3O6`. The author's statement is reproduced |
| `receipts/reviewer-mutants.txt` (+ dir), `scripts/reviewer_mutants.py` | 6 reviewer-designed arms on the kill seam | 1 KILLED, 5 SURVIVED (see F2 and S1) |
| `receipts/probe-hz-reachability.log`, `scripts/probe_hz_reachability.py` | extra HZ arms: can NAME_WR, IDENTIFY and CLOCK_CFG conflict with an ACMP class at this top? | NAME_WR conflict reached with a legal command. IDENTIFY and CLOCK_CFG reached only through a stream descriptor_type (see F1) |
| `receipts/lint_hdl.log`, `receipts/make_check.log`, `receipts/gen_matrix_check.log` | lint, the documentation gates, matrix drift | all rc 0 |
| `receipts/mutation-patches-apply-check.txt` | `git apply --check` of every `tb/*/mutations/*.patch` at head | 130 applied, 0 refused |
| `receipts/hosted-exact-head-snapshot.txt` | exact-head hosted run 36789123922, read-only, 23:32 UTC | `docs-gates` success and `portability` success. In `suites`, the lint+suites step succeeded and the AECP campaign step was still pending |
| `receipts/tree-integrity.txt` | clone integrity after all probes | HEAD, tree and index tree are exact. Worktree is clean, the blob-hash and mode sweeps are clean, and there are no assume-unchanged or skip-worktree flags. This repository has no gitlinks (0 index records of mode 160000) |

## 3. Findings

### F1 - MAJOR - Conformance, Tests, Docs - NAME_WR has a reachable admission conflict at this top; the "four classes cannot conflict" statement is false for it

- **Where:**
  - `docs/architecture/03_packet_engine.md:233-238`: "With two single-issue clients the matrix admits no conflict between `CLOCK_CFG`, `NAME_WR`, `REGISTRY_OP` or `IDENTIFY` and any class ACMP presents".
  - The same claim is in the PR body's "What remains" and in HANDOFF §0.4, §3 and §6. There it is the stated reason #84 acceptance 2 "cannot be met at this top" for those four classes.
- **Authority and evidence:**
  - The scoreboard matrix makes RO_SNAPSHOT conflict with every write class on the same key: `hdl/packet_engine/KL_pp_scoreboard.sv:132-139`, rule 2, "vs any other class ... conflicts only on the same key".
  - `hz_classify` keys SET_NAME from the wire `{descriptor_type, descriptor_index}` (`hdl/top/protocol_processor_top.sv:1493`, `:1533-1535`).
  - It keys an ACMP GET_RX_STATE of sink k as RO_SNAPSHOT `{STREAM_INPUT, k}` (`:1505-1509`).
  - So a SET_NAME on STREAM_INPUT k, a legal IEEE 1722.1 §7.4.17 target, conflicts with an in-flight ACMP GET_RX_STATE of sink k, and the reverse holds too.
  - Probe `R419-P1` (`receipts/probe-hz-reachability.log`) holds a GET_RX_STATE of sink 1 behind the stalled MAC, using the suite's own `hold_acmp`. SET_NAME on STREAM_INPUT 1 is not admitted while the ACMP read keeps its key. It is admitted after the key frees and answers SUCCESS (status 0).
  - The control `R419-P0` (SET_NAME on STREAM_INPUT 0) is admitted beside it.
  - HZ8 (`tb/pp_top/sim_main.cpp:11678-11697`) only tries SET_NAME on CLOCK_DOMAIN 0 against a held STREAM_CFG step. That pair cannot conflict.
  - As a result, the NAME_WR arm `hz-name-as-ro` is killed only by HZ1's class label, never by a behavioural conflict.
- **The other three classes:**
  - `R419-P3` and `R419-P4` show that SET_CONTROL and SET_SAMPLING_RATE are also serialized against the ACMP read when their wire descriptor_type names STREAM_INPUT. They answer NOT_SUPPORTED (11) afterwards. So IDENTIFY and CLOCK_CFG conflicts are reachable at admission, but only through a descriptor type those commands do not legally carry.
  - Only REGISTRY_OP is structurally unreachable: ACMP keys always carry type STREAM_INPUT or STREAM_OUTPUT, and the registry key has type 0x3F.
  - Probe `R419-P2` (the talker side, GET_TX_STATE vs SET_NAME on STREAM_OUTPUT) is inconclusive. The GET_TX_STATE hold premise could not be established with `hold_acmp`.
- **Impact:**
  - A normative architecture page now asserts an admission invariant the landed RTL does not have.
  - The PR uses that invariant to declare part of a frozen acceptance criterion (#84-2) unmeetable, which invites a waiver on a false premise.
  - The parent-visible behaviour list (PR body and HANDOFF §4, "Nothing that ran concurrently before now waits, except these conflicts") omits a real new serialization: SET_NAME on a stream descriptor against an ACMP state read of that stream.
- **Required outcome:**
  - 03 §6, and the PR's What-remains and parent-visible list, state the reachability that is actually true: NAME_WR reachable with legal commands; CLOCK_CFG and IDENTIFY reachable only through a stream descriptor type; REGISTRY_OP unreachable.
  - `tb/pp_top` section HZ grades the NAME_WR admission conflict (SET_NAME on a stream descriptor against a held ACMP read of the same stream, and against another stream's), with a failing mutation arm.
  - Whether CLOCK_CFG and IDENTIFY are graded through the stream-typed form, or recorded as reachable only through malformed commands, is a public decision, not an implicit one.
- **Verification:** the new HZ arm passes at the fixed head, and `hz-name-as-ro` or an equivalent arm fails it. The 03 §6 text matches `probe_hz_reachability.py`'s result.

### F2 - MINOR - Tests - two safety invariants of the kill seam survive mutation

- **Where:**
  - `hdl/aecp/KL_aecp_engine.sv:1699-1700`: `!regun_r && !lockc_r`, the never-preempt exemption for REGISTER/DEREGISTER_UNSOLICITED_NOTIFICATION and LOCK_ENTITY.
  - `hdl/top/protocol_processor_top.sv:3577`: `|| sb_kill_ack_w`, which ends the AECP owner when a kill is honoured.
- **Evidence:** `receipts/reviewer-mutants.txt`.
  - `r-registry-lock-preempted` removes the registry and lock exemption. It SURVIVED `tb/pp_top` deadline and `tb/ucpu` run.
  - The author's `dl-edit-preempted` removes all three exemptions but fails only DL6, the edit (tb/pp_top README table).
  - `r-kill-ack-keeps-owner` SURVIVED `tb/pp_top` deadline.
- **Why they matter:**
  - `E_REGUN`, `E_DEREG` and `E_LOCKEN` (`hdl/aecp/ucode/gen_ucode.py:911-938`, `:985-1005`) commit their change in their first op, a registry `GATHER_EXT`, which is not in the µCPU's effect set.
  - A preempt after that op, possible whenever the deadline passes inside the program, would answer ENTITY_MISBEHAVING for a registration or lock that took effect. That is exactly the partial commit rule (e) forbids, and 03 §6 and 06 §8.1 say it is prevented.
  - Without the owner clear, the killed command's RX-slot return re-releases its hold id, which the comment at `:3574-3576` says a new admission may already own.
  - The RTL is correct at this head. The property is unproven.
- **Required outcome:** a check that fails when the registry and lock exemption is removed. For example, a REGISTER or LOCK_ENTITY queued past its deadline behind a stall must answer its own SUCCESS with its effect visible. Also a check, or a recorded equivalence argument, for the owner clear on an honoured kill. Each needs a mutation record.
- **Verification:** `scripts/reviewer_mutants.py <tree> <out> r-registry-lock-preempted,r-kill-ack-keeps-owner` reports KILLED, or the equivalence argument is published for the second.

### F3 - MINOR - Conformance, Docs - a REQ-MVU-005 violation found by the lane is left untracked while the PR closes #57

- **Where:** `hdl/aecp/KL_aecp_engine.sv:3649-3653` and `:3672-3675`. On a response-memory failure (`rsp_fail_w`), every response, MVU included, is rebuilt with `ST_ENTITY_MISBEHAVING_C` (status 10).
- **Evidence:**
  - REQ-MVU-005 (`docs/00_MILAN_COMPLIANCE_REVIEW.md:400`) and 06 §6.9 (`:692`) allow MVU statuses SUCCESS and NOT_IMPLEMENTED only. The PR relies on the same reading for the deadline path (`:3609-3616`).
  - The PR body and HANDOFF §6 record this as "REQ-MVU-005 latent, found here and not acted on".
  - No public issue tracks it (open-issue search, this round), and no in-tree document records it.
  - The PR says `Closes #57`, the REQ-MVU-005 ticket.
  - Likewise, the notification-hold finding recorded in 08 §4 has no tracking issue.
- **Impact:** once #57 closes, the only public record of a known REQ-MVU-005 status violation is a merged PR description. AGENTS §4 requires newly discovered work to become an issue.
- **Required outcome:** before merge, either fix the fault path to answer MVU with NOT_IMPLEMENTED, or open public issues for both findings and record the MVU one in the tree (00 GAP-03 residue or 06 §6.9).
- **Verification:** an issue link or fix commit, and the in-tree record, at the new head.

### F4 - MINOR - Tests, Docs - ambiguous check IDs and a stale harness banner

- **Duplicate IDs:**
  - `tb/ucpu/sim_main.cpp` now has two `P19` sections: the pre-existing GET_AUDIO_MAP P19a-P19d (`:1060-1152`) and the new deadline P19a-P19h (`:1506-1610`).
  - The campaign's named check for `ucpu-preempt-repeats` is the prefix `"P19a completes"` (`tb/pp_top/aecp_mutants.py:46`). It matches both `P19a completes` (`:1087`, GET_AUDIO_MAP) and `P19a completes: one redirect` (`:1520`). A failure of the unrelated audio-map check would therefore count as this arm's kill.
  - `tb/ucpu/README.md:65-78`, 09 §8.3 and the PR cite "tb/ucpu P19" for the deadline.
- **Stale banner:** the HZ banner (`tb/pp_top/sim_main.cpp:11215-11217`) and the comment at `:11318` still say the ACMP hold is "a PROBE_TX the talker cannot answer yet". The harness actually fills the TX pool with GET_RX_STATE answers (`:11469-11495`), and HANDOFF §3 records that the PROBE_TX method was abandoned.
- **Impact:** the ambiguous IDs weaken the named-check discipline of the campaign, and the stale banner misdescribes the premise mechanism to the next reader.
- **Required outcome:**
  - The deadline checks carry an ID not used elsewhere in the suite.
  - The campaign's expected string names it unambiguously.
  - README, 09 §8.3 and the banner describe the harness as it is.
- **Verification:** the new ID occurs in exactly one section of `tb/ucpu/sim_main.cpp`; `aecp-mutants` still reports 30 KILLED.

### Suggestions (no effect on coverage)

- **S1:**
  - Three reviewer arms survived that are equivalent at this ROM and topology:
    - `r-effects-short`: in every non-exempt µprogram a WRITE_ST or NAME_WR precedes COMMIT, NVM_MARK and NOTIFY_ENQ, and the one program whose first effect is COMMIT (`E_AMADD`) is exempt;
    - `r-queued-counts-unsolicited`;
    - `r-kill-latched-unsolicited`.
  - These guards are defence in depth. Consider saying so where they are declared, so a later reviewer does not re-derive it.
- **S2:**
  - TB2's "full GET_DYNAMIC_INFO batch" is the thirteen getters once each (`tb/pp_top/sim_main.cpp:10981-10984`), not a batch that fills the 524-octet response.
  - At 0.1 % of T-AECP-RESP the difference is immaterial. Consider wording it as "all thirteen getters" in 08 §4 and 09 §8.3.
- **S3:** the resource figures come from an out-of-context open-source synthesis flow. Vivado, the instrument of record, is still owed (the PR says so).

## 4. Focus questions answered

- **Design (HANDOFF §0) against 08 §4, F03.7 and the response-time clauses: sound.**
  - One deadline register and one comparator suffice for the single-issue engine.
  - The rule (d) boot-hold re-arm is keyed on residency before the D3 done terminal.
  - The kill is honoured only with `kill_resp_queued_i`.
  - Preemption happens only at an instruction boundary and before the first effect.
  - Every op wait is bounded by a 4,096-clock watchdog, so the forced response follows the expiry by about 3 ms at most at P-CLK-HZ, well inside the 140 ms rule (e) keeps.
  - No top-level port or parameter changed. The top's diff hunks are all internal. The new ports are on `KL_aecp_engine` and `KL_aecp_ucpu`, which only the processor instantiates in this tree.
- **#81 (04c2f5c): confirmed in RTL and by the reproduced arms.**
  - Deadline read at admission (`protocol_processor_top.sv` deadline block), kill face driven, running command cut before its first effect and answered status 10.
  - MVU answered NOT_IMPLEMENTED with echo; DL3 is byte-exact, and the reviewer arm `r-mvu-no-echo` is KILLED.
  - Key released only at the forced response's hand-off (`dl-released-before-queued` KILLED).
  - The Table 5.19 reading agrees with the in-tree authority (REQ-MVU-005, 06 §6.9). The PDF itself was not available.
- **#57 (9a82661):** section TB reproduces the author's histogram exactly (`receipts/suite-pp_top.log`: worst case 24,681 clocks, 0.103 % of T-AECP-RESP). All three budget arms are KILLED, and ROM images are regenerated per arm (`forget_generated_roms`).
- **#84 (fb0c13c):**
  - All nine classes reach the scoreboard (HZ1).
  - The SET_CONFIGURATION admission-pick fix is correct: the barrier can only be the AECP head, and that head leaves its queue only on a grant. Its arm `hz-barrier-no-priority` fails 33 checks.
  - The four-class limit is not wholly true (F1).
- **aecp-mutants in CI:** the step was added to `.github/workflows/hdl.yml`. It was still pending in the exact-head hosted run at the snapshot.
- **The two D3 negative controls failing D3O6:** expected. With the hold defeated, the command runs during the slowed restore. It is not "held until the terminal", so rule (d)'s exemption no longer applies and the kill answers it (`D3O6: ... 0 of them answered` → forced answer). With the kill tied off, the counts return to 16 and 5.

## 5. Per-lens results at f963fe9ac591b8a42547700468fc875db27ae5ab

- `[R419] UNCLEAN Conformance`: F1 (the #84-2 reachability judgment) and F3 (REQ-MVU-005 status on the fault path, untracked).
  - Checked and correct:
    - #81-1 to #81-3;
    - #57-1 to #57-3;
    - #84-1 and #84-3;
    - the key-release and FAIL_SAFE semantics of 03 §6 rule (e);
    - the MVU reading against 00:400 and 06:692.
  - #81-4 and #84-4 are declared not done, consistent with "Relates".
- `[R419] PASS RTL` - `hdl/top/protocol_processor_top.sv` classifier (:1439-1556), pick (:3485-3495), owners (:3540-3582) and deadline block (:3584-3625); `hdl/aecp/KL_aecp_engine.sv:361-374,1670-1720,2996-3010,3606-3632`; `hdl/aecp/KL_aecp_ucpu.sv` preempt (:465-486, :712-727); `gen_ucode.py` E_DLKILL.
  - Checked against 03 §6 and the scoreboard contract:
    - reset of every new register;
    - the wrap-safe 32-bit compare;
    - no same-clock accept/kill-ack overlap;
    - no double release across kill_ack and the RX return;
    - the barrier head leaving its queue only on a grant;
    - the preempt never cutting a stalled op or following an effect;
    - no top-level port or parameter change;
    - lint clean.
- `[R419] PASS Robustness` - `receipts/probe-hz-reachability.log`, `receipts/aecp-mutants.txt`, `receipts/d3-two-controls-*.txt`, `receipts/reviewer-mutants.txt`.
  - Checked:
    - malformed descriptor types (serialized, then NOT_SUPPORTED);
    - frames owed no response (DL5);
    - the boot restore (D3O6 and the two controls);
    - a repeated preempt (P19h);
    - a slow-but-live face on every waiting op (DL1, DL2, DL4, DL6, TB4);
    - GET_DYNAMIC_INFO void;
    - the admission wedge (HZ3).
  - The survivors in F2 are test gaps on correct RTL and are filed under Tests.
- `[R419] UNCLEAN Tests`: F1 (no behavioural NAME_WR conflict arm), F2 (two surviving non-equivalent arms) and F4 (ambiguous named check). Suites and campaign reproduced green: 8,112 and 415 checks; 35/35.
- `[R419] UNCLEAN Docs`: F1 (03 §6:233-238, the PR's parent-visible list), F3 (untracked findings) and F4 (tb/ucpu README P19, the HZ banner). The 08 §4, 09 §8.3, integrator and operator additions were otherwise checked against the RTL and the measured numbers. `make check` is rc 0.

## 6. Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F3) | issues #81/#57/#84 acceptance; 08 §4, 03 §6, 06 §6.9/§8.1, 00:400; top classifier and kill face; DL, TB and HZ results | R419-1 | f963fe9ac591b8a42547700468fc875db27ae5ab |
| RTL | CLEAN | protocol_processor_top.sv, KL_aecp_engine.sv, KL_aecp_ucpu.sv, gen_ucode.py, KL_pp_scoreboard.sv (contract); lint_hdl | R419-1 | f963fe9ac591b8a42547700468fc875db27ae5ab |
| Robustness | CLEAN | probe P0-P4, DL1-DL7, D3O6 plus the two D3 controls, TB4, HZ3, reviewer arms | R419-1 | f963fe9ac591b8a42547700468fc875db27ae5ab |
| Tests | UNCLEAN (F1, F2, F4) | tb/pp_top sim_main.cpp DL/TB/HZ, tb/ucpu P19, aecp_mutants.py and 29 patches, the reproduced campaign, reviewer arms | R419-1 | f963fe9ac591b8a42547700468fc875db27ae5ab |
| Docs | UNCLEAN (F1, F3, F4) | docs diff (00, 03, 06, 08, 09, integrator, operator), tb/pp_top and tb/ucpu READMEs, PR body, HANDOFF | R419-1 | f963fe9ac591b8a42547700468fc875db27ae5ab |

## 7. Real limits

- **Simulator.** The instructed pinned-simulator path did not exist on this host. This round used the pinned wrapper of this head's manager tool directory instead. It identifies as version 5.050; the wrapper and binary sha256 values are in `receipts/verilator-identity.txt`.
- **Build parallelism.** Two builds used the Makefiles' default `-j 0` (all host threads) before the scratch copy was capped at `-j 8`: the first `gsi-build` of the head, and the probe build. Every later build and run respected the 8-job limit.
- **Not re-run.** This round did not re-run:
  - the full D3 campaign (only its two changed controls);
  - the SRP, ADP, GSI, name-write, retry, SRP-admission and descriptor-guard campaigns;
  - `run_suites.sh` over all 33 suites;
  - the yosys resource measurements;
  - any parent or builder gate.
- **Not inspected.** The parent consumer set was not inspected. The manager's bank receipts were not present in the named public evidence tree, so they could not be checked.
- **Specifications.** The specification PDFs are not available. Clause readings rely on their in-tree quotations.
- **Probe coverage.** Probe P2 (talker side) was inconclusive. The F1 conclusion rests on P1.

## 8. Pending manager duties

- The exact-head hosted `suites` job, including the new AECP campaign step (pending at the snapshot); hosted and act acceptance.
- The donor bank, and the parent consumer bank at dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b` (gitlink only, carrying the #132 + C1 adaptation), both to be posted.
- The final current-dev candidate build at the merge turn (source base `0451d83d`). This is distinct from the source validation above.
- Physical calibration: NOT RUN. Field skips are not hardware proof.
- A second independent positive review, and re-review of the fixes for F1-F4 at a new head.

R419-1 FINISHED
