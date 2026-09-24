[R278] POSITIVE - exact head f8d30ecf44e3c1bb50bdc3a452e40d43d663f7f3

# R278-2 independent review: PR #109 (processor issues #92 and #93), correction round 1

| Item | Value |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan |
| PR | #109, base `main`; review start comment 5808677208 |
| Exact head | `f8d30ecf44e3c1bb50bdc3a452e40d43d663f7f3`, tree `fe3d88165d1b9d215fb80e474a8a381b112004e3` (verified in the review clone, `receipts/clone-integrity.txt`) |
| Round-1 head | `156c206cbaedf721f7caef5c94faa21876a28c32`. The correction is six commits on it: `d849257`, `6ac5504`, `e88f50b`, `7297a64`, `39625c9`, `f8d30ec` |
| Source base | `fbc1f7156d711e5b7f511da8a16d9494256b017b`. The PR-owned diff is `09f9bf38..f8d30ec`; the SRP LeaveAll commits came in with the merge of main (`69a6eac2`, PP #107) |
| Simulator | the CI-pinned simulator 5.050. Wrapper sha256 `905795b9…e92f`, binary `fb2cc573…defcdf` (`receipts/env.txt`) |
| Verdict | **POSITIVE**. No open BLOCKER, MAJOR or MINOR. Every round-1 finding from both reviews is resolved. Three new SUGGESTIONs do not affect the verdict |

## 1. How the review was reconstructed

1. **Guidance.** The processor has no AGENTS.md or CONTRIBUTING.md. I read README.md (the gates and "Milan wins"), docs/README.md (single-source and figure rules, editing workflow) and hdl/README.md (rules 1-5: a testbench with every RTL commit, `$error` guards, Verilator and Yosys portability).
2. **Scope.** I read the #92 and #93 bodies, which hold the frozen acceptance, #93's S1/S3/S4 contract and its "does NOT do" list. I also read every maintainer and manager comment on both issues:
   - the one-lane assignment;
   - the A225 idiom assignment;
   - the A235 correction assignment. Its scope decision is: "The saved binding must also survive a read-only GET_RX_STATE after a failed binding walk, not only in the restore window. Every fix gets a failing arm."
   - the author's REVIEW READY notes, and the PR body with its five decisions.
3. **Authorities.** 05 §5.1 and the F05.3 listener matrix, 07 §5.3 (F07.9, "How a binding walk ends", "A failed walk keeps the saved records"), 08 `T-NVM-RS-DEADLINE`, and the integrator and operator guides. I also read the listener RTL where the unbound rule depends on it: the A10 clear, and START/STOP applying only to a bound sink.
4. **Diff and history.** I read `git diff fbc1f715..f8d30ec`, and closely the correction round, `git diff 156c206..f8d30ec`: `KL_acmp_nvm_shadow.sv`, `tb/acmp_nvm`, `tb/pp_top` (sim, wrap, README), 05, 07, the two guides and the PNG.
5. **Public evidence.** Folder `review-evidence/pp92-r1` at milan-fpga `e2dc1023`. It holds `manager-r2` (the round-1 head), `correction-a235` (author logs and tools) and both round-1 review packets. I read the manager's exact-head banks for this head in the review-provided output directory: donor-full at `f8d30ec` and parent-consumer at parent `692ff116` (live dev `f86c34fe` plus a local gitlink commit). Each command in both exited 0 (§7).
6. **Prior public findings** (R278-1, R279-1) were read only after my own pass over the correction diff. They are resolved in §4.

## 2. What the correction does, and whether it is right

**The unbound rule** is at `hdl/acmp/KL_acmp_nvm_shadow.sv:318-327`:

```
c1_diff_w = (c1_vld_r != valid_r[sink]) || (c1_vld_r && (proj != cmp_data))
```

Two unbound records now compare equal, whatever their other fields hold. I checked that this is safe against the rest of the design:

- **Unbound fields carry nothing.** The listener's A10 (UNBIND of a bound sink) zeroes every persisted field (`KL_pp_acmp_listener.sv:1225-1240`). START/STOP changes `f_started` only for a bound sink (`:1051`), matching Milan 5.3.8.7, which leaves started/stopped undefined while unbound. So no Milan-visible state lives in the fields of an unbound record, and no walk preloads one (`H_RP_RD` skips `!valid_r`).
- **Every transition that matters still writes.** Bound to unbound, unbound to bound, and bound to bound with any field changed all write. Probe P3 and mutants Y-* confirm this (§3).
- **Decision 5 matches the architecture.** After a failed walk, an UNBIND of a sink the walk left unbound writes nothing. This is not a new policy: F05.3 (`docs/architecture/05_acmp_engine.md:247`) runs only A1 A7 for `UNBIND_RX` in UNBOUND, with no A10 "NVM clear". The saved binding therefore returns on the next healthy boot. A controller that wants it gone has a working route, BIND then UNBIND (P3-2). I accept the decision; S1 below suggests documenting that route.
- **Refusal (c) in the header can no longer fire for an unbound capture.** "A capture during restore WINS" no longer applies to an unbound capture of a sink whose `valid_r` is 0. Such a capture is no longer a change, so it does not touch the sink. In the top this is unreachable, because the gate owns the listener for the whole restore span. At `156c206` an all-zero unbound record compared equal to the zero-swept RAM anyway. Not a defect; see S2.

**The elaboration guard** is at `:501-503`, `$error` when `RS_TMO_CYC_P < 1`. Under default flags and under `lint_hdl.sh` it is fatal at 0, and it passes at 3000. With the guard deleted, 0 elaborates silently: the failing arm. Under `-Wno-fatal`, which every suite Makefile uses, it is demoted to a warning. `$fatal` is demoted the same way in this simulator. The guard uses the same idiom as the tree's other seven elaboration guards, so this is a property of the idiom, not of this change (`receipts/rs-tmo-guard.log`).

**BW4** (`tb/pp_top/sim_main.cpp:1179`, `:9186`) samples every cycle of every walk in the run. It checks three things:
- `busy || done` from each walk's start;
- `done` never while the gate owns the listener;
- no X_PRELOAD cycle or A4 arm at or after `done`.

The taps are `dbg_lsn_released_o`, `dbg_lsn_preload_o` and `dbg_lsn_arm_o` in `pp_top_wrap.sv`. BW4's own walk ends on sink 7's saved binding, so the shadow's terminal rises while that preload's arm is still up. That is the shape that makes the done-without-release mutant observable.

**The docs** now agree with the RTL. I checked 05 §5.1, 07 §5.3:397-398 and :419-430, the integrator tie-off cell and §7, integrator step 3, and the operator §6 table against the probes and against N9a-c.

## 3. Independent executions at exact head

Every run used a disposable archive copy under `scratch/`, never the clone. Builds were capped at `-j 2`, with at most 4 at once.

| Run | Result | Receipt |
|---|---|---|
| `tb/acmp_nvm` run | 349/349 | `receipts/base-head-acmp_nvm.txt` |
| `tb/acmp_nvm` pinned (the #92 criterion-4 control) | exit non-zero, 107 of 349 fail. L05a: `sink 0 holds 000000000000000000000000`, 1 write and 1 erase, an unbound reply, a reset that restores nothing. All completed-scenario assertions | `receipts/base-head-acmp_nvm-pinned.txt` |
| `tb/pp_top` (both builds) | 1434/1434 (1414 default + 20 VID) | `receipts/base-head-pp_top.txt` |
| `tb/lsn_admit` | 18/18 | `receipts/base-head-lsn_admit.txt` |
| `tb/nvm_port` | 136/136 | `receipts/base-head-nvm_port.txt` |
| Scoped lint (`-Wall`, whole tree) of the shadow, gate, arbiter, port and top | all exit 0, no warnings | `receipts/lint-scoped.log` |
| **P1**, my round-1 probe, unchanged: sinks 0/3/7 saved, the walk fails at sink 3 with cause 2, 3 or 1, then one read-only GET of sink 0 | **head 16/16**: no write, sink 0 byte-exact, a healthy reset restores all three. At `156c206`: 9 FAIL, the same failure as round 1 (byte 8 `03`→`00`) | `receipts/probe-P1-head.log`, `probe-P1-r1.log` |
| **P2**, my round-1 top probe, re-anchored only (same logic; one file runs against both heads) | **head: no FAIL line**, region 0x20 has 0 writes and 0 erases, byte 8 `03`→`03`. At `156c206`: FAIL, 1 write and 1 erase, `03`→`00`. The verdict is the FAIL line; the probe exits 0 by design | `receipts/probe-P2-*.log`, `scripts/p2_pp_top_bw3_get.py` |
| **P3**, new: the edges of the unbound rule | **head 30/30**. P3-1: a BIND after a failed walk persists and is restored. P3-2: BIND then UNBIND after a failed walk leaves sink 0 unbound on the media. P3-3: decision 5, an UNBIND alone writes nothing and the binding returns. P3-4: an UNBIND of a restored sink persists. P3-5: a re-BIND to another talker persists. P3-6: UNBIND then two GETs gives one unbound record. At `156c206` only P3-3 differs (3 FAIL), which is the intended behaviour change | `receipts/probe-P3-*.log`, `scripts/p3_unbound_rule_edges.py` |
| Correction arms | **F1-compare** (the compare back to its `156c206` form): acmp_nvm 9 FAIL (N8a-c), pp_top 2 (BW3, `03 -> 00`). **X-top-done-no-release**: pp_top 2 (BW4, 8 owned cycles with done). **X-top-busy-gap**: pp_top 1 (BW4, 8 cycles with neither level). All match the published counts | `receipts/mutants-summary.txt`, `receipts/mutants/` |
| Reviewer mutants of the rule | Killed: **Y-vld-only** 22 (B6), **Y-no-unbound-write** 7 (D1), **Y-no-write-when-invalid** 35 in acmp_nvm and 12 in pp_top, **Y-reject-keeps-valid** 14 (G4). Survived: **Y-no-bypass** (see S3; the bypass dates from 2026-08-12 and this PR does not touch it) | same |
| Published #93 and #92 arms, re-run on the changed shadow | All KILLED, at exactly the published counts. acmp_nvm: LG01 107, LG02 71, LG03 45, LG02t 19, LG03t 7, LG04 5, LG05 12, LRdone 108, B01 20, BA1 15, BC1 13, B03 10, A01 1, B04 120 (of 342), and B02 with both edits 12 (N1a-d, N8b, N9b, `mutant-acmp_nvm-B02both.log`). pp_top: LG01 8, B01 2, B03 2. My round-1 extra mutants are KILLED as well: drain leaks 2 and 2, tmo off-by-one 2, no REQ stall 1, and each lsn_admit release term alone 2 | same |
| Expected survivors | X-rel-busy-top and X-rel-both-top pass pp_top, as in round 1. The gate's flop already trails the shadow's terminal past the one-cycle arm, and tb/lsn_admit grades each term on its own. Not a finding | same |
| Deadline guard | fatal at 0 under default flags and `-Wall`, passes at 3000, silent at 0 with the guard deleted. Demoted under `-Wno-fatal`, and `$fatal` is demoted too | `receipts/rs-tmo-guard.log` |

## 4. Prior public review findings at this head

| Finding | Status at `f8d30ec` | Evidence |
|---|---|---|
| R278-1 F1 = R279-1 F3 (MAJOR): a read-only GET after a failed walk erased saved bindings | **RESOLVED**, for all three causes, the torn route included | P1 16/16, P2 clean, P3 30/30. N8a-c and BW3 are the regressions; F1-compare kills 9 and 2. 07 §5.3:397-398 and :419-430, 05 §5.1 and the operator guide state it |
| R278-1 F2 = R279-1 F2 (MINOR): the top's done/busy composition had no failing arm | **RESOLVED** | BW4 kills both mutants (2 and 1). The S0/R comment is corrected (`tb/pp_top/sim_main.cpp`, section R) |
| R278-1 S1: guard `RS_TMO_CYC_P` | **RESOLVED**, with its failing arm | `receipts/rs-tmo-guard.log` |
| R279-1 F1 (MINOR): the guides described an unwired face as done without fail | **RESOLVED** | Operator §6 has the three-row table. The integrator tie-off cell states the same three outcomes, and §7 is qualified for `restore_go_i`, one of the two options the finding allowed. Figure 21's tie-off rule still holds for the face itself, since a silent face ends at the deadline. N9a-c grade the pins |
| R279-1 S4 (PNG) and S5 (port comment) | **RESOLVED** | the re-rendered `20-rtl-dataflow.png` shows `KL_pp_acmp_lsn_admit` and `KL_acmp_nvm_shadow → KL_pp_nvm_mgr_arb → KL_pp_nvm_port`. `KL_acmp_nvm_shadow.sv:135` now reads "any cause" |
| R279-1 S1, S2, S3, S6 | **RETAINED as SUGGESTIONs** (not taken, optional). They do not affect either verdict | unchanged code paths, per the PR body |

## 5. Findings

No BLOCKER, MAJOR or MINOR finding is open. SUGGESTIONs only:

### S1 — SUGGESTION — Docs, Conformance: cite F05.3 for decision 5 and name the route to clear a saved binding

- **Where:** `docs/architecture/07_memory_maps.md:419-430`; `docs/guides/operator.md:205-208`.
- **Evidence:** P3-3, where an UNBIND alone after a failed walk writes nothing and the binding returns, and P3-2, where BIND then UNBIND clears it.
- **Impact:** an operator who meant to drop a binding the failed walk could not read sees it return on the next healthy boot, and the guide does not say what to do instead.
- **Outcome:** in 07 §5.3, say that this follows F05.3 (`UNBIND_RX` in UNBOUND runs no A10). In the operator guide, name BIND then UNBIND as the way to clear such a binding.
- **Verification:** re-read both files.

### S2 — SUGGESTION — RTL, Docs: qualify refusal (c) in the shadow banner

- **Where:** `hdl/acmp/KL_acmp_nvm_shadow.sv:71-75`.
- **Evidence:** with the unbound rule, an unbound capture of a sink whose `valid_r` is 0 is not a change, so it neither touches the sink nor wins over a record stored later in the walk.
- **Impact:** in the top the admission gate makes this unreachable. A future second integration without the gate would read the banner as a stronger promise than the RTL keeps.
- **Outcome:** add half a sentence to (c) saying that it holds for captures that differ from the stored projection, and that the top's gate keeps live captures out of the restore span.
- **Verification:** re-read the banner.

### S3 — SUGGESTION — Tests: the capture compare's one-cycle write bypass has no failing arm (predates this PR)

- **Where:** `KL_acmp_nvm_shadow.sv:316-317` (`cmp_data_w`).
- **Evidence:** mutant Y-no-bypass passes acmp_nvm 349/349. The bypass dates from 2026-08-12, and this PR does not change it.
- **Impact:** a later edit could drop the forwarding unnoticed. With the unbound rule the compare only reads it for bound-to-bound captures.
- **Outcome:** a follow-up issue, not this PR: add an acmp_nvm case with two bound record writes to one sink in consecutive cycles.
- **Verification:** Y-no-bypass reddens that case.

**Observation, not a finding:** at the legal value `RS_TMO_CYC_P = 1`, `-Wall` lint flags `rs_wd_r >= 0` as a constant comparison (UNSIGNED, `:517`). `lint_hdl.sh` lints the default parameters, so no gate sees it.

## 6. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #92 and #93 acceptance and the A235 scope decision; F05.3; 05 §5.1; 07 §5.3; listener A10 and START/STOP; the pinned control (107/349, L05a); P1, P2 and P3 at both heads | R278-2 | f8d30ecf44e3c1bb50bdc3a452e40d43d663f7f3 |
| RTL | CLEAN | `KL_acmp_nvm_shadow.sv` (compare, reject, guard, banner), the top's done/busy composition, gate, arbiter and port (unchanged since round 1); scoped lint; deadline guard arms | R278-2 | f8d30ecf44e3c1bb50bdc3a452e40d43d663f7f3 |
| Robustness | CLEAN | failure causes 1-3 × stored sinks (P1, P2, N8); the rule's edges (P3); unwired faces (N9); drain and deadline mutants; release terms | R278-2 | f8d30ecf44e3c1bb50bdc3a452e40d43d663f7f3 |
| Tests | CLEAN (S3 predates this PR) | acmp_nvm, pinned, pp_top, lsn_admit and nvm_port at head; 3 correction arms (4 runs), 18 published arms plus B02 with both edits, 10 round-1 reviewer mutants, 6 new rule mutant runs | R278-2 | f8d30ecf44e3c1bb50bdc3a452e40d43d663f7f3 |
| Docs | CLEAN (S1, S2) | 05, 07, integrator and operator guides, figures 20 (SVG and PNG) and 21, the acmp_nvm and pp_top READMEs (count claims 349, 107, M35-M37 and B02 12, all re-measured), MODULE_MATRIX | R278-2 | f8d30ecf44e3c1bb50bdc3a452e40d43d663f7f3 |

## 7. Manager evidence read, and hosted CI

- **Donor-full at `f8d30ec`** (base `09f9bf38`), every command exit 0:
  - `lint_hdl.sh`;
  - `run_suites.sh`, 15,797 checks, 0 failing;
  - `make check`;
  - `gen_matrix --check`;
  - the synthesis run;
  - nvm_port `figures`;
  - `git diff --check`.
- **Parent-consumer at `692ff116`** (live dev `f86c34fe` plus a local gitlink commit to `f8d30ec`), every command exit 0:
  - `check_cpp_idiom`;
  - `check_py_idiom` (long module 10 <= 10, long function 9 <= 9);
  - `xvlog_gate --check`;
  - `check_rtl_source_lists`;
  - `pp_srcs --check --selftest`;
  - `test_builder`;
  - `tb/verilator/pp_shadow`, 371 checks, 0 failures.
- **Hosted CI at exact head.** The `hdl` workflow ran for `push` and for `pull_request`, head `f8d30ecf`. `suites`, `docs-gates` and `portability` succeeded in both runs. The only skipped step is "Build Verilator v5.050", a cached toolchain build, so no gate step was skipped in an executed job. The manager owns hosted and act acceptance.

## 8. Real limits

- No hardware and no physical calibration. Field skips are not hardware proof.
- I did not run the full processor bank (`run_suites.sh`, `make check`, synthesis, `figures`) or any parent bank. For those I rely on the manager's exact-head results in §7 and on hosted CI.
- The parent's `pp_shadow` bench passed, but I did not inspect whether it has a mid-walk refusal after a stored record followed by a poll.
- No Milan or IEEE PDF was consulted. Conformance is judged against the frozen acceptance, the manager's scope decision and the in-repo architecture, which cites Milan v1.2 5.3.8.
- P3 is a reviewer probe, not a suite case.
- The Y-* mutants were run on acmp_nvm; only Y-no-write-when-invalid was also run on pp_top.
- The simulator demotes elaboration `$error` and `$fatal` under `-Wno-fatal`. The guard's refusal therefore depends on the consumer's flags, as it does for every guard in the tree.

## 9. Pending manager duties

- Build the final current-dev candidate at the merge turn (source base `fbc1f715`, live dev `f86c34fe`) and re-run the donor and parent consumer gates on it.
- Confirm that parent T4 pulses `restore_go_i` on every boot path, and that the parent's device model answers blank media as 0xFF then `done` (PR decision 3).
- Own hosted and act acceptance.
- Keep #15 and #20 open, as the PR states.
- Obtain the second independent review.
- Route S1-S3 (and R279-1 S1, S2, S3, S6) as optional follow-ups at the owner's discretion.

## 10. Integrity after probes

- The review clone was never modified; every probe ran in an archive copy under `scratch/`.
- `HEAD` is `f8d30ecf…`, and `write-tree` equals `HEAD^{tree}` (`fe3d8816…`).
- `git status --porcelain --ignored` is empty, and the diff and index are clean.
- Every tracked blob's worktree hash matches. The ls-tree and ls-files mode/blob/path digests are equal (`e4ac5a16…`).
- The repository has no submodule gitlinks and no `.gitmodules` (`receipts/clone-integrity.txt`).

R278-2 FINISHED
