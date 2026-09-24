[R278] NEGATIVE - exact head 156c206cbaedf721f7caef5c94faa21876a28c32

# R278-1 independent review: PR #109 (processor issues #92 and #93)

| Item | Value |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan |
| PR | #109, base `main`; review start comment 5807070947 |
| Exact head | `156c206cbaedf721f7caef5c94faa21876a28c32`, tree `a1c45f5e7949764ad008c04ff66ca3494db97a5e` (verified in the review clone) |
| Source base | `fbc1f7156d711e5b7f511da8a16d9494256b017b`. Author head `3691340c`, manager merge `69a6eac2` of main `09f9bf38` (PP #107), then five idiom commits |
| Simulator | the CI-pinned simulator 5.050, wrapper sha256 `905795b9…e92f` (`receipts/env.txt`) |
| Verdict | **NEGATIVE**: one open MAJOR (F1) and one open MINOR (F2) |

## 1. How the review was reconstructed

The review followed the brief's order:

1. **Guidance.** The processor has no AGENTS.md or CONTRIBUTING.md. I read README.md, which gives the gates (`run_suites.sh`, `lint_hdl.sh`, `make check`, `gen_matrix --check`) and the rule that Milan wins over IEEE 1722.1.
2. **Scope.** I read the issue bodies of #92 and #93, including #93's S1, S3 and S4 contract and its "does NOT do" list. I also read the maintainer and manager comments: the one-lane assignment, both author REVIEW READY tables, the A225 idiom assignment and its DONE note.
3. **Authorities.** I read the saved-state/fast-connect contract at `2d8fd62f`, and the parent consumer's `KL_pp_shadow.sv` at `26d855a9`, specifically its device-face contract: blank reads as 0xFF, and a refusal counts as a failure.
4. **The diff and history.** I read `git diff fbc1f715..156c206c`. The PR-owned part is `09f9bf38..156c206c`; the SRP LeaveAll commits arrived with the merge of main.
   - The merge `69a6eac2` equals `git merge-tree 3691340c 09f9bf38`, tree `80addf41…`, and the two sides touch no common file.
   - The five idiom commits touch only `tb/`.
5. **Public evidence.** Folder `review-evidence/pp92-r1` at milan-fpga `94ccff2d`:
   - `manager-r2`: donor-full and parent-consumer, both at exact head `156c206c`, every command exit 0. The parent `tb/verilator/pp_shadow` bench scores 371 checks and 0 failures, including "P3: a legitimate blank READ still completes".
   - `author` and `idiom-a225`: logs and the published mutant edits.
6. **Hosted CI at exact head.** The `hdl` workflow ran on both push and pull_request: `suites`, `docs-gates` and `portability` all succeeded. The only skipped step is "Build Verilator v5.050", which had a cache hit, so nothing was skipped in any executed job. The manager owns hosted and act acceptance.

**Prior public review findings.** None exist. PR #109 has no reviews and no review comments; its only comment is the review-start notice. The issues carry none either. There is nothing to resolve or retain.

## 2. Findings

### F1 — MAJOR — a read-only GET_RX_STATE after a failed binding walk erases saved bindings

- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.
- **Where:**
  - `hdl/acmp/KL_acmp_nvm_shadow.sv:314` (`c1_diff_w`).
  - `hdl/acmp/KL_acmp_nvm_shadow.sv:580-582`: the atomic reject clears `valid_r` only. The stored fields stay in the shadow RAM.
  - `hdl/acmp/KL_acmp_nvm_shadow.sv:516-523`: the new DEVICE and deadline routes into that reject.
  - Docs: `docs/architecture/07_memory_maps.md:391-392` and `docs/architecture/05_acmp_engine.md:165-169`.
  - Tests: `tb/acmp_nvm/sim_main.cpp:2016-2021` (N1) and `tb/pp_top/sim_main.cpp:9055-9082` (BW3).

**Authority.**
- #92 objective and acceptance 1: a read-only GET_RX_STATE anywhere in a sink's boot-restore window cannot erase or replace its saved binding.
- #92 acceptance 2: a subsequent reset restores the same binding.
- The saved-binding persistence that #92 derives from Milan v1.2 5.3.8.
- 07 §5.3 as landed: "A read-only command that arrives during the walk is answered from the restored image afterwards and changes nothing here."

**Evidence.**
- **Mechanism.** The walk stores a sink's NVM record in the shadow RAM (H_RS_STORE). A later record then fails the walk with cause 1, 2 or 3. The atomic reject clears only that sink's `valid_r`; its RAM image keeps the saved talker, controller and flags. The listener, released on defaults, serves the GET and writes back its unbound record. `c1_diff_w` compares that projection with the RAM image, sees a difference, captures a "live change", sets dirty, and flushes the unbound record over the saved one.
- **Unit probe P1** (`probes/run_p1.sh`, `receipts/p1-head.log`), real listener, gate, shadow, arbiter and port. Sinks 0, 3 and 7 are saved; the walk fails at sink 3; one read-only GET of sink 0 follows:
  - P1-0, the no-fault control: clean.
  - P1-1, device error (cause 2): 1 erase and 1 write; sink 0's record goes from valid-byte `03` to `00`; a healthy reset no longer restores sink 0.
  - P1-2, silent device ended 2,000 cycles late (cause 3): the same result.
  - P1-3, torn payload (cause 1): the same result.
- **Top-level probe P2** (`probes/run_p2.sh`, `receipts/p2-head.log`). This is pp_top BW3 exactly, except that NVM is allowed to settle before the case's own BIND: the held GET of sink 0 writes region 0x20 (1 erase and 1 write), and byte 8 goes from `03` to `00`.
- **Attribution** (`receipts/p1-counterfactual-B0{1,2}.log`):
  - With the pre-PR zero-byte-err handling restored (full B02), P1-1 keeps sink 0.
  - With no deadline (B01), P1-2 never ends and writes nothing.
  - So the device-error and deadline routes to the erasure are introduced by this PR. The torn route (P1-3) is the same mechanism and existed before it.
- **Mechanism check** (`receipts/p1-mechanism.log`; a disposable probe, not a proposed fix). Making `c1_diff_w` ignore field-only differences between two unbound records makes all 16 probe checks pass. The full acmp_nvm suite stays at 332/332, so no existing case depends on the behaviour.
- **Why the benches miss it:**
  - N1b and N1c send the GET to the stored sink 0 but never grade NVM or the dirty vector after it. `n_failed_walk` checks for writes only before the GET.
  - N3 sends its GET to sink 7, which was never stored.
  - pp_top BW3 follows the GET with a BIND to the same sink inside the same debounce window, so the GET's flush is coalesced into the BIND's write and hidden.

**Impact.** A transient device error, or a device that is silent for 20 ms while the binding walk reads a later record, fails the walk. The failure itself is correct under #93. But the first read-only GET_RX_STATE of any earlier stored sink then permanently replaces that sink's saved binding with an unbound record. That GET can be one held from the boot window, or any later controller poll. The next healthy boot restores nothing for that sink. This is the #92 defect class, reached through the failure paths this PR adds, and it contradicts 07 §5.3's "changes nothing here". It also reaches the parent: a backend refusal mid-walk after a stored record is exactly the case the parent's P3 now fails whole.

**Required outcome.**
1. After a failed walk of any cause, a listener write-back that only restates its default state must not be persisted over the saved records. For example, the reject could bring each rejected sink's RAM image into agreement with the listener's default, or the capture compare could stop treating field-only differences between unbound records as a change. The alternative is an explicit maintainer decision that a failed walk forfeits saved bindings on first touch, stated in 07 §5.3, 05 §5.1 and the operator guide. That would contradict #92's objective, so it needs the owner.
2. The torn route (cause 1) should be fixed by the same change, or split to its own issue with a recorded decision.
3. Add discriminating regressions for causes 1, 2 and 3 with a sink stored before the failing record:
   - `tb/acmp_nvm`: grade NVM bytes after a read-only GET of that sink, plus a healthy-reset round trip.
   - `tb/pp_top` BW3, or a sibling case: grade NVM before any BIND.
   - Each needs a failing arm.

**Verification.** At the fixed head:
- `probes/run_p1.sh <repo> <head> <out>` reports 16/16.
- P2 reports its PROBE check as PASS.
- The new regressions go red with the correction removed.
- acmp_nvm, pp_top and the manager's donor and parent banks stay green.

### F2 — MINOR — the top's `restore_done_o` and `restore_busy_o` composition has no failing arm

- **Lenses:** Tests.
- **Where:** `hdl/top/protocol_processor_top.sv:2498-2500`. The claim is made in 05 §5.1 ("The release is the binding walk's end" row) and in the integrator and operator guides.

**Authority.** #93 S4 says `released_o` is the binding walk's end, `restore_done_o` takes it, and "No enable can therefore precede the last preload's record write and discovery arm". 05 §5.1 adds that `restore_busy_o` covers the gap, so the pair never reads neither-busy-nor-done.

**Evidence** (`receipts/mutants-summary.txt`, `receipts/mutants/mutant-pp_top-X-top-*.log`):
- `X-top-done-no-release` (`restore_done_o = nvm_walk_done_w`) survives pp_top: 1407 checks, 0 failures.
- `X-top-busy-gap` (the gap term deleted) also survives: 1407 checks, 0 failures.
- The acmp_nvm wrap exposes the shadow's own `restore_done_o`, so the top's AND is graded nowhere. The gate's release itself is graded: LRdone is killed with 97 FAIL.

**Impact.** An integration or refactor that drops the release from `restore_done_o`, or the busy gap, would pass every bench. An entity enable gated on `restore_done_o` could then precede the last preload's record write and A4 arm by up to four cycles, or the status pair could read idle mid-walk.

**Required outcome.** Add a pp_top check that `restore_done_o` never rises before the listener's release, meaning after the last preload's record write and discovery arm. Add a second check that `restore_busy_o || restore_done_o` holds on every cycle from the walk's start.

**Verification.** Both mutants above are killed by completed-scenario assertions, and pp_top stays green.

### S1 — SUGGESTION — guard the read-deadline parameter

- **Lenses:** RTL, Robustness.
- **Where:** `hdl/acmp/KL_acmp_nvm_shadow.sv:119,499` and `hdl/top/protocol_processor_top.sv:129`.

`RS_TMO_CYC_P - 1` underflows at 0: a `CLK_HZ_P` below 50 makes the top default 0, which turns the deadline into about 2^32 cycles. An elaboration-time check (`RS_TMO_CYC_P >= 1`) would make that misconfiguration visible. This does not affect the verdict.

## 3. Independent executions at exact head

All runs used disposable archive copies of the exact head under `scratch/`; none ran in the clone.

| Run | Result | Receipt |
|---|---|---|
| `tb/acmp_nvm` run | 332 checks, 332 PASS | `receipts/acmp_nvm-head-run.log` |
| `tb/acmp_nvm` pinned (issue #92 criterion 4 control) | exit non-zero, 96 FAIL. The FAIL lines are byte-identical to the published after-log. L05a: `sink 0 holds 000000000000000000000000`, 1 erase and 1 write, an unbound reply, a reset that restores nothing. These are completed-scenario assertions, with no timeout or crash | `receipts/acmp_nvm-head-pinned.log` |
| `tb/lsn_admit` | 18/18 | `receipts/lsn_admit-head-run.log` |
| `tb/nvm_port` | 136/136, T23a-k present | `receipts/nvm_port-head-run.log` |
| `tb/pp_top`, first (all-section) build | 1407 checks, 0 failures | `receipts/mutants/mutant-pp_top-BASELINE.log` |
| Scoped lint (`-Wall`, whole tree visible) of `KL_pp_acmp_lsn_admit`, `KL_pp_nvm_mgr_arb`, `KL_pp_nvm_port`, `KL_acmp_nvm_shadow`, `protocol_processor_top` | all exit 0, no warnings | `receipts/lint-scoped.log` |
| Published failing arms (`probes/mutants.py`) | every one KILLED: LG01 96, LG02 55, LG03 40, LG02t 19, LG03t 7, LG04 5, LG05 12, LRdone 97, B01 16, BA1 13, BC1 9, B03 9, A01 1, B04 128 (325), B02 9 (both edits; first edit alone 4); pp_top LG01 5, B01 2, B03 2. These match the published counts | `receipts/mutants-summary.txt`, `receipts/mutants/` |
| Port cause arms C1-C4 | not re-run here. They are graded by `make -C tb/nvm_port figures` (measured 10/4/6/1, matching the README), which the manager ran at exact head, exit 0 | manager-r2 donor-full 08 |
| Reviewer mutants | Killed: X-drain-leak (2), X-drain-done-leak (2), X-tmo-off-by-one (2, N5b), X-no-req-stall (1, N4), and in lsn_admit each release term on its own (busy 2, pre 2, arm 2). Survived: X-top-done-no-release and X-top-busy-gap (F2). The busy, arm or both release terms also survive in acmp_nvm and pp_top; this is expected, because the shadow's terminal already trails the last preload's write and arm, the RTL comment says so, and tb/lsn_admit grades each term alone. Not a finding | same |
| Probes P1, P1m, P1c, P2 | see F1 | `receipts/p1-*.log`, `receipts/p2-head.log` |

## 4. Lens notes

- **Conformance.**
  - Met: #92 acceptance 1-5 for a walk that completes. The gate holds every work face; L05a-f and L05s are clean; the pinned control reproduces L05. #93 S1, S3 and S4 are as specified: port cause codes, cause-gated `rs_empty_w`, the no-progress deadline with abort and drain, and the admission rules.
  - Open: F1, which breaks saved-binding persistence on #93's new failure paths.
  - Open items handled correctly: #15 is not claimed (the PR says "Relates"; the docs and the arbiter banner state the quarantine). The D3-terminal case has no subject in the processor and is graded against the enable instead (BW1/BW3 with `entity_enable_i` low). #93's cost figures are estimates outside its acceptance and were not re-measured.
- **RTL.**
  - The gate masks valid and ready on the two acceptance faces, so a pop is exactly a take.
  - The scoreboard candidacy reads the masked ready, so a held listener head does not block AECP. A held listener head does block ACMP-talker heads behind it in the shared ACMP queue, which the contract accepts as producer policy for the bounded window.
  - The arbiter's busy covers manager 1's grant cycle. The drain starts only for an open READ and ends only on that operation's own done or err.
  - The port's `refuse_w` matches exactly the two UNFRAMED transitions to S_FIN.
  - Open: F1.
- **Robustness.** The walk always terminates (preload never stalls, read bounded). A silent device leaves the port quarantined, as documented. Open: F1, whose trigger is a transient device fault.
- **Tests.** The published arms and my additional ones are discriminating, with completed-scenario verdicts. Open: the F1 gap (no post-failure NVM grading) and F2.
- **Docs.** 05 §5.1, 07 §5.3, 02 §8/§8.2, 08 T-NVM-RS-DEADLINE, the integrator guide (walk mandatory, blank faces as 0xFF then done, err or early done fails the walk) and the operator guide all match the RTL, and the matrix lists both new modules. Open: F1 (07 §5.3:391-392 and 05 §5.1:165-169 claim a read-only command changes nothing).

## 5. Consumer impact

A blank or unbacked device face must now answer reads with 0xFF bytes and then `done`. An `err`, or a `done` before the 8 header bytes, fails the walk.

- The parent backend answers an unvalidated image as 0xFF reads.
- Its refusal test P3 already expects `restore_fail`, and passes at exact head (manager-r2 parent-consumer 07: 371/0).
- `restore_go_i` is now mandatory: without it the listener stays owned until reset. The parent's firmware owns that on every boot path (milan-fpga T4).
- F1 applies to the parent as well: a backend refusal after a stored record, followed by a controller poll.

## 6. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #92 and #93 bodies and comments; saved-state contract `2d8fd62f`; parent `KL_pp_shadow.sv` @`26d855a9`; P1/P2/P1c probes; pinned control | R278-1 | 156c206cbaedf721f7caef5c94faa21876a28c32 |
| RTL | UNCLEAN (F1) | `KL_pp_acmp_lsn_admit.sv`, `KL_pp_nvm_mgr_arb.sv`, `KL_pp_nvm_port.sv` diff, `KL_acmp_nvm_shadow.sv` diff, `protocol_processor_top.sv` diff; scoped lint; P1m | R278-1 | 156c206cbaedf721f7caef5c94faa21876a28c32 |
| Robustness | UNCLEAN (F1) | failure causes 1-3 × stored sinks (P1, P2); drain and quarantine (N3/N5c, reviewer drain mutants); release terms | R278-1 | 156c206cbaedf721f7caef5c94faa21876a28c32 |
| Tests | UNCLEAN (F1, F2) | acmp_nvm, lsn_admit, nvm_port, pp_top at head; 18 published arms re-run (15 acmp_nvm, 3 pp_top) plus C1-C4 via the manager's figures run; 14 reviewer mutants | R278-1 | 156c206cbaedf721f7caef5c94faa21876a28c32 |
| Docs | UNCLEAN (F1) | 01, 02, 05, 07, 08, integrator and operator guides, MODULE_MATRIX, tb READMEs vs measured counts | R278-1 | 156c206cbaedf721f7caef5c94faa21876a28c32 |

## 7. Real limits

- No hardware and no physical calibration. Field skips are not hardware proof.
- I did not run the full processor bank, `make check`, the synthesis run or the nvm_port `figures` target. I did not run any parent bank. For those I rely on the manager's exact-head public evidence (manager-r2, all exit 0) and on hosted CI at exact head.
- No Milan or IEEE PDF was consulted. Conformance is judged against the issues' frozen acceptance and the parent contract, which cite Milan v1.2 5.3.8.
- The pre-PR base bench was not run. The torn-route attribution (P1-3) comes from the code: the atomic reject and the compare are unchanged from base. The new-route attribution comes from head counterfactuals B01 and B02.
- The P1m compare change is a mechanism probe, not a validated fix.

## 8. Pending manager duties

- Route F1 and F2 to the author and re-review at the fixed head.
- Build the final current-dev candidate at the merge turn (source base `fbc1f715`, live dev `50e78097`) and re-run the parent consumer gates on it, including `pp_shadow` with a mid-walk refusal after a stored record, once F1 is fixed.
- Confirm that parent T4 pulses `restore_go_i` on every boot path.
- Own hosted and act acceptance.
- Keep #15 and #20 open, as the PR states.
- Obtain the second independent review.

## 9. Integrity after probes

- The review clone was never modified; every probe ran in an archive copy.
- `HEAD`: `156c206c…`.
- `write-tree` equals `HEAD^{tree}`: `a1c45f5e…`.
- `git status --porcelain --ignored`: empty.
- Every tracked blob's worktree hash matches. The ls-tree and ls-files mode/blob/path digests are equal (`6d4f8714…`).
- The repository has no submodule gitlinks (`receipts/clone-integrity.txt`).

R278-1 FINISHED
