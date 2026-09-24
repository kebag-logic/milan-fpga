[R279] POSITIVE - exact head f8d30ecf44e3c1bb50bdc3a452e40d43d663f7f3

# R279-2: external independent review of PR #109 (processor issues #92 and #93), correction round 1

| Item | Value |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #109, branch `92-93-boot-restore` |
| Exact head | `f8d30ecf44e3c1bb50bdc3a452e40d43d663f7f3`, tree `fe3d88165d1b9d215fb80e474a8a381b112004e3` (isolated detached clone; identity re-verified after all probes, `receipts/90-clone-integrity-after.txt`) |
| Source base | `fbc1f7156d711e5b7f511da8a16d9494256b017b`. The PR's own commits sit on main `09f9bf38` (PP #107's LeaveAll commits reach `fbc1f715..head` only through that merge). The correction round is six commits on `156c206c`: `d849257`, `6ac5504`, `e88f50b`, `7297a64`, `39625c9`, `f8d30ec` |
| Reviewer role | external independent reviewer, cleared context. Public review start: PR #109 comment 5808772169 |
| Simulator | CI-pinned 5.050 rev v5.050, wrapper sha256 `905795b9…e92f`, the same as the manager's banks (`receipts/00-identity.txt`) |
| Verdict | **POSITIVE.** No open BLOCKER, MAJOR or MINOR finding. All five lenses are CLEAN. Suggestions only |

## Verdict summary

The correction round closes every round-1 finding at this head. I checked each fix against its failing arm:

- **R278-1 F1 = R279-1 F3 (MAJOR): resolved.** The capture compare's unbound rule (`hdl/acmp/KL_acmp_nvm_shadow.sv:325-326`) stops a read-only write-back after a failed walk from being committed over saved records. I tested it three ways:
  - my round-1 probe, re-run unchanged: 358/358;
  - a new reviewer probe in which every earlier saved sink is stored before the failure, followed by 17 read-only GETs: 21/21;
  - the author's N8a-c and pp_top BW3.

  With the compare restored to its `156c206c` form, all three fail with completed-scenario assertions.
- **R278-1 F2 = R279-1 F2 (MINOR): resolved.** pp_top BW4 grades the top's `restore_done_o`/`restore_busy_o` pair in every cycle of every walk. My round-1 mutants R1 and R2 are now killed.
- **R279-1 F1 (MINOR): resolved.** The operator §6 table, the integrator tie-off cell and the §7 qualification now say the same three things, and N9a-c grade them. My round-1 unwired-face probe agrees (351/351).

**Decision 5.** The author asked reviewers to rule on one point: after a failed walk, an UNBIND of a sink the walk left unbound writes nothing, so that sink's saved binding comes back on the next healthy boot. I reproduced this (probe R279-FU) and accept it. The authority is the repository's normative listener matrix, F05.3 (`docs/architecture/05_acmp_engine.md:247`). Its `UNBIND_RX` row in state UNB runs `A1 A7` only. `A10` ("clear binding + NVM clear") runs only from a bound state. So an UNBIND of an UNBOUND sink has nothing to persist. #92 acceptance 3 ("a later BIND/UNBIND … persists") is still met:

- a BIND after a failed walk persists (probe R279-FB);
- an UNBIND of a sink bound live after the failed walk persists (R279-FB);
- an UNBIND after a healthy walk persists (R279-H1 and the existing L09u).

This behaviour was not in the round-1 findings, so it is recorded here, not carried forward. It is the author's recorded decision, and the docs state it (07 §5.3 `:419-431`, operator guide `:205-208`).

## Reconstruction order and sources (all public)

1. **Contributor rules.** The repository has no `AGENTS.md` or `CONTRIBUTING.md`. I used `README.md` (the gates `run_suites.sh`, `lint_hdl.sh`, `make check` and `gen_matrix --check`; Milan wins over IEEE 1722.1) and `docs/README.md` (single-source ID registries, one home per figure, citation rules). CI is `.github/workflows/hdl.yml`.
2. **Scope.** The issue #92 and #93 bodies (frozen acceptance, the S1/S3/S4 contract and the "does NOT do" list), plus every maintainer, manager and author comment:
   - the A10 assignments (including A235: "the saved binding must also survive a read-only GET_RX_STATE after a failed binding walk");
   - the A218, A225 and A235 notes.
3. **Authorities.** 05 §5.1 and F05.3, 07 §5.3 (F07.8/F07.9), 02 §8, F01.5 `P-NVM-RS-TMO-CYC`, F08.1 `T-NVM-RS-DEADLINE`, the integrator and operator guides, and Milan v1.2 5.3.8 as the processor cites it. I did not consult any specification PDF.
4. **The diff and history.**
   - `git diff fbc1f715..f8d30ec` in full (48 files). The PR-owned part is `09f9bf38..f8d30ec`.
   - The correction round, `156c206c..f8d30ec` (11 files), which changes one RTL line pair plus an elaboration guard and comments, `receipts/01-history-and-scope.txt`.
   - `git diff --check 09f9bf38..HEAD` is clean.
5. **Public executable evidence.** milan-fpga @`e2dc1023` `review-evidence/pp92-r1`: `correction-a235`, `manager-r2`, and the manager's bank records for this head (`$VALIDATION_STORAGE/pp92-manager-r3`: donor-full and parent-consumer, both `complete.json` exit 0).
6. **Prior public review findings.** I read R278-1 (comment 5807355668) and R279-1 (comment 5807713906) only after my own pass over the diff, my probes and my mutants. I did not read the concurrent R278-2 report.

## Findings

None at MINOR or above.

### Suggestions (they do not affect the verdict)

- **S1 (RTL, Tests): the zero-deadline guard is non-fatal in this repository's own benches.**
  - The guard is `hdl/acmp/KL_acmp_nvm_shadow.sv:501-503`. It follows the repository's convention of an elaboration `$error` in a generate block.
  - The pinned simulator reports it as `%Warning-USERERROR`. Without `-Wno-fatal` the build exits 1. With `-Wno-fatal`, which every `tb/*/Makefile` passes, it exits 0 and builds (`receipts/21-zero-deadline-guard.log`).
  - So a bench, or a consumer that builds the same way, instantiated with `CLK_HZ_P < 50` would still get the wrapped deadline, with only a warning.
  - The listener's own guard uses `$fatal(1, …)` (`KL_pp_acmp_listener.sv:347`), which stops every flow. Using `$fatal` here, or adding a one-line bench check, would make the refusal unconditional.
- **S2 (Docs): cite F05.3 for decision 5.** 07 §5.3 and the PR body justify decision 5 by saying the listener "cannot tell it from a GET". The stronger normative reason is F05.3's UNB row (no A10). Citing it in 07 §5.3 would stop a later reader from taking the behaviour for a measurement artefact.
- **Round-1 suggestions not taken, retained as optional.** Their state at this head:
  - R279-1 S1: per-face top wiring. My re-run mutants R8, R9 and R10 still survive pp_top at 1434/1434 (`receipts/r1-rerun/R8.log`, `R9.log`, `R10.log`).
  - R279-1 S2: a device error in the same cycle as a refused header. R6 still survives nvm_port at 136/136.
  - R279-1 S3: the arbiter lets manager 1 starve manager 0 (`KL_pp_nvm_mgr_arb.sv:166`). Latent, because manager 1 is tied idle.
  - R279-1 S6: fail and blank levels read before done. RTL unchanged.
  - R278-1 S1: done. R279-1 S4: done; the PNG was re-rendered and now shows `KL_pp_acmp_lsn_admit` and `KL_pp_nvm_mgr_arb`. R279-1 S5: done; the port comment at `KL_acmp_nvm_shadow.sv:135` now reads "any cause".

## Prior public review findings: disposition at this head

| Finding | Severity | Disposition | Evidence at this head |
|---|---|---|---|
| R278-1 F1 = R279-1 F3: a read-only GET after a failed walk erased saved bindings | MAJOR | **Resolved** | My round-1 `probe_failed_walk.py`, re-run unchanged: 358/358. For every cause, 0 writes and 0 erases after the GET, byte 8 stays `03`, and a healthy reboot restores it (valid `0x81`) (`receipts/r1-rerun/probe-failed-walk.log`). New reviewer probes R279-FW1..3 (walk fails at the LAST sink, sinks 0-2 all stored, 17 GETs): PASS. With the compare restored to its `156c206c` form, 6 of 21 fail, e.g. "3 writes, 3 erases; sink 0 holds 000…" (`receipts/20-probes-fw.log`). Author arms reproduced: acmp_nvm N8a-c fail 9 of 349 with the old compare, and pp_top BW3 fails 2 of 1,414, "byte 8 03 -> 00" (`receipts/22-mutants.log`). The torn route (cause 1) is fixed by the same change. |
| R278-1 F2 = R279-1 F2: top done/busy composition had no failing arm | MINOR | **Resolved** | pp_top BW4. R1 (`restore_done_o = nvm_walk_done_w`) is KILLED with 2 FAIL. R2 (the gap term deleted) is KILLED with 1 FAIL. Re-run with my round-1 `mutate.py` (`receipts/r1-rerun/R1.*`, `R2.*`) and again with my own mutant runner (`receipts/22-mutants.log`). The S0 comment is corrected. |
| R279-1 F1: guides said an unwired face reads done without fail | MINOR | **Resolved** | Operator §6 table (`docs/guides/operator.md:213-222`), the integrator tie-off cell, and §7's "never wedges" now qualified for `restore_go_i`. All match 07 §5.3 and the RTL. Graded in acmp_nvm N9a-c. My round-1 `probe_unwired.py` re-run gives P1 done=1 fail=1 blank=1 cause=3, and P2 done=1 fail=1 blank=1 cause=2, at 351/351 (`receipts/r1-rerun/probe-unwired.log`). |
| R278-1 S1 | SUGGESTION | Taken | The guard is present. See S1 above on its fatality. |
| R279-1 S1-S6 | SUGGESTION | S4 and S5 taken; S1, S2, S3 and S6 retained as optional | See above. |

## Lens evidence

### Conformance: CLEAN

**Issue #92.**

- **Acceptance 1** (a read-only GET anywhere in the window) holds at this head:
  - L05a-f and L05s pass (acmp_nvm 349/349, `receipts/10-acmp_nvm-head.log`).
  - The pinned-wiring control reproduces the recorded L05 failure: 107 of 349 FAIL, including L05a "sink 0 holds 000000000000000000000000" (`receipts/22-mutants.log`).
  - The extended objective, that the saved binding survives a read-only GET after a failed walk for causes 1-3, is met (see the dispositions table).
- **Acceptance 2** (real listener and manager integration, reset round trip): the acmp_nvm wrap, and pp_top BW0-BW3.
- **Acceptance 3** (later BIND/UNBIND ordered and persisted):
  - L09 and L10, plus probes R279-FB, H1 and H2;
  - an UNBIND of an UNBOUND sink has nothing to persist under F05.3 (decision 5, accepted above).
- **Acceptance 4** (a discriminating regression without a timeout verdict): the pinned control, pp_top LG01, and the new N8/BW3 arms.
- **Acceptance 5** (contract recorded): 05 §5.1 and 07 §5.3.

**Issue #93.**

- S1, S3 and S4 are as specified. The RTL for S1, S3 and S4 is unchanged since `156c206c` apart from the compare and the guard, and the round-1 arms still bite: nvm_port 136/136 and lsn_admit 18/18.
- #15 and #20 are correctly left open.
- The D3 terminal has no subject in the processor. It is graded against the enable instead.

**Parent consumer.** The manager's parent-consumer bank at dev f86c34fe, with the gitlink committed locally at this head, exits 0: `pp_shadow` 371/0, the idiom ratchets, `xvlog_gate` and `test_builder`. One calibration arm did NOT RUN; see Real limits.

### RTL: CLEAN

Reviewed in full at this head:

- `KL_acmp_nvm_shadow.sv`: the capture pipeline, flag files, reject, restore, replay, flush and the new guard;
- `KL_pp_acmp_lsn_admit.sv`;
- `KL_pp_nvm_mgr_arb.sv`;
- the port's cause register;
- the top's gate, arbiter and done/busy wiring.

**The unbound rule is safe on every path I traced.**

- It changes no write between a bound record and any other record.
- A BIND after a failed walk compares valid 1 against 0 and is written.
- A bound-to-unbound transition is written.
- Stale RAM fields left by the reject never reach the media:
  - a later bound write overwrites them;
  - an unbound sink is only flushed after a bound-to-unbound write has refreshed its RAM image.
- Unbound records are never preloaded, so no restorable state is lost.
- The taint path (a capture in the middle of a flush) differs only for unbound-to-unbound pairs, which carry no restorable content.
- The full acmp_nvm bench is green with the rule in place (349/349, and 21/21 for my probes), and so is pp_top (1434/1434).

**Lint.** Scoped `-Wall` lint of the four changed modules exits 0 with no warnings (`receipts/23-lint-changed-modules.log`). The manager's full lint of 39 files exits 0.

### Robustness: CLEAN

- A transient device error, a torn read or a silent device during the walk now leaves every saved record on the media:
  - through read-only polls held from the boot window, or sent later (FW1-3, 17 GETs each);
  - until a controller binds that sink.
- Deadline, drain and quarantine behaviour is unchanged from round 1 and still graded:
  - N3, N5b, N5c and N9a;
  - BW3, including a device that ends the abandoned read late.
- An erased-media face gives done, not failed, blank (N9c). An err face fails with cause 2 (N9b). A never-granting face fails with cause 3 and quarantines the port (N9a).
- A boot without `restore_go_i` leaves the listener owned. This is documented, and it is now also stated in the tie-off cell.

### Tests: CLEAN

Focused suites at the exact head, run with the pinned simulator in a disposable extract:

| Suite | Result | Receipt |
|---|---|---|
| acmp_nvm | 349/349 | `receipts/10-acmp_nvm-head.log` |
| nvm_port | 136/136 | `receipts/11-nvm_port-head.log` |
| lsn_admit | 18/18 | `receipts/12-lsn_admit-head.log` |
| pp_top (default 1,414 + fixture 20) | 1434/1434 | `receipts/13-pp_top-head.log` |

**Failing arms, all completed-scenario assertions** (`receipts/22-mutants.log`, `receipts/20-probes-fw.log`, `receipts/r1-rerun/`):

| Arm | Suite | Result |
|---|---|---|
| Compare without the unbound rule | acmp_nvm | 9 of 349 FAIL (N8a-c) |
| Compare without the unbound rule | pp_top default build | 2 of 1,414 FAIL (BW3) |
| Compare without the unbound rule | reviewer probes | 6 of 21 FAIL |
| Top done without the release | pp_top | 2 FAIL (BW4) |
| Top busy without the gap term | pp_top | 1 FAIL (BW4) |
| Pinned wiring | acmp_nvm | 107 of 349 FAIL, L05a included |

**Other checks.**

- The correction round deletes no pre-existing check: the only removed bench lines are the refactor of `nv_record_ok` and one comment (`receipts/01-history-and-scope.txt`).
- The published counts in `tb/acmp_nvm/README.md` and `tb/pp_top/README.md` (349, 107, 9, M35-M37) match my measurements.
- Coverage limits carried as suggestions: R6, R8, R9 and R10 survive (retained round-1 suggestions S1 and S2).

**Manager banks at this head** (exit 0): `run_suites.sh` with 15,797 checks and 0 failing, lint, `make check`, `gen_matrix --check`, yosys, nvm_port figures and `diff --check`.

### Docs: CLEAN

- **05 §5.1** (a failed walk's image is the defaults, and a read-only command leaves the saved records alone) matches the RTL and the probes.
- **07 §5.3:**
  - "A failed walk keeps the saved records" matches the RTL and probes;
  - the table of how a walk ends matches `restore_cause_o`;
  - "It rejects the image, not the media" matches the RTL.
- **Operator §6.** The three-row table matches N9a-c and my round-1 unwired probe. The unbind sentence matches probe R279-FU.
- **Integrator guide.** The tie-off cell and step 3 ("only a later BIND replaces one") are accurate.
- **Shadow banner and port comments** now say "any cause".
- **Diagram.** The dataflow PNG was re-rendered and agrees with the SVG: both name the gate and the arbiter (inspected).
- **Suite READMEs** carry the new arms with the counts measured here.

The one docs improvement I propose is S2, a suggestion.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #92/#93 bodies, frozen acceptance and all maintainer, manager and author comments; F05.3 UNBIND_RX row; 07 §5.3; Milan v1.2 5.3.8 as cited; pinned control (107/349, L05a); probes FW1-3, FB, FU, H1, H2; decision 5; manager parent-consumer bank at this head | R279-2 | f8d30ecf44e3c1bb50bdc3a452e40d43d663f7f3 |
| RTL | CLEAN | `KL_acmp_nvm_shadow.sv` (full: compare `:325`, reject, flush and taint, guard `:501`), `KL_pp_acmp_lsn_admit.sv`, `KL_pp_nvm_mgr_arb.sv`, `KL_pp_nvm_port.sv` cause, `protocol_processor_top.sv` gate, arbiter and done/busy; scoped lint of 4 modules; guard behaviour (S1) | R279-2 | f8d30ecf44e3c1bb50bdc3a452e40d43d663f7f3 |
| Robustness | CLEAN | failed-walk causes 1-3 with 3 stored sinks and 17 polls; post-failure BIND/UNBIND; unwired-face probes P1/P2 and N9a-c; drain and quarantine cases; zero-deadline elaboration | R279-2 | f8d30ecf44e3c1bb50bdc3a452e40d43d663f7f3 |
| Tests | CLEAN | acmp_nvm, nvm_port, lsn_admit and pp_top at head; pinned control; 3 author arms plus 2 round-1 reviewer mutants killed; round-1 FW and unwired probes re-run; 4 retained survivors (R6, R8-R10, suggestions); README counts; the correction round removes no check | R279-2 | f8d30ecf44e3c1bb50bdc3a452e40d43d663f7f3 |
| Docs | CLEAN | 05 §5.1, 07 §5.3, operator §6 table, integrator tie-off cell, step 3 and §7, shadow and top port comments, 20-rtl-dataflow.png/.svg, tb/acmp_nvm and tb/pp_top READMEs | R279-2 | f8d30ecf44e3c1bb50bdc3a452e40d43d663f7f3 |

## Real limits

- **Not run here** (manager-owned, or outside the permitted scope): the full `run_suites.sh`, the full `lint_hdl.sh`, `make check`, yosys, nvm_port `figures`, and the parent consumer bank. I rely on the manager's exact-head records (`$VALIDATION_STORAGE/pp92-manager-r3`: donor-full `complete.json` exit 0, `run_suites` 15,797/0; parent-consumer `complete.json` exit 0, parent head `692ff116` = dev `f86c34fe` + one local commit setting the processor gitlink to this head).
- **Parent gitlink.** I did not inspect the parent gitlink directly. That checkout is a lane directory outside my read set, so the gitlink value is the manager's record. The processor itself has no submodule gitlinks (0 entries of mode 160000).
- **Hosted CI at the exact head.** Two `hdl` runs (push `35962744485`, pull_request `35962749215`), each with `docs-gates`, `suites` and `portability` executed and succeeded. The only skipped step is "Build Verilator v5.050", a cached tool build. The legacy combined-status API reports `pending` with zero contexts, which carries no result (`receipts/30-hosted-checks.tsv`). The manager owns hosted and act acceptance.
- **Final candidate.** Source validation at this head is distinct from the final current-dev candidate. The manager builds that at the merge turn (source base `fbc1f715`, live dev `f86c34fe`).
- **Specifications.** No Milan or IEEE PDF was consulted. Conformance rests on the frozen acceptance and the repository's normative F05.3 and 07 §5.3.
- **Cost figures.** Issue #93's cost figures were not re-measured, by the author or here.
- **Physical calibration NOT RUN.** The parent bank's calibration gate 11 did not run (its build tree is absent). Field skips are not hardware proof, and no hardware was used.
- **Other reviewers' material.** R278-1's probes (P1/P2) were not re-executed, because their scripts are another reviewer's material. Their scenarios are covered by my own FW probes and my re-run round-1 probe.

## Pending manager duties

- Obtain the second independent review (R278-2) and apply the two-positive merge bar.
- Build and gate the final current-dev candidate at the merge turn: the full donor and parent banks, including `pp_shadow`, the idiom ratchets and `xvlog_gate`, and hosted/act acceptance.
- Record the consumer impact at the parent:
  - blank or unbacked device faces must answer as 0xFF bytes and then `done`;
  - an err or an early done now fails the walk;
  - `restore_go_i` must pulse on every boot (parent T4).
- Keep #15 and #20 open. Carry S1, S2 and the retained round-1 suggestions as optional.

## Receipts (listed in MANIFEST.sha256)

- `receipts/00-identity.txt`: clone head and tree, simulator wrapper and binary hashes, compiler and Python.
- `receipts/01-history-and-scope.txt`: PR commits, the correction-round diff, `diff --check`, and the F05.3 row.
- `receipts/10-…13-*.log`: focused suites at the head.
- `receipts/20-probes-fw.log`: reviewer probes at the head and with the old compare.
- `receipts/21-zero-deadline-guard.log`: guard behaviour with and without `-Wno-fatal`.
- `receipts/22-mutants.log`: pp_top arms and the pinned control.
- `receipts/23-lint-changed-modules.log`: scoped lint.
- `receipts/30-hosted-checks.tsv`: hosted runs and jobs.
- `receipts/90-clone-integrity-after.txt`: HEAD, write-tree, empty status including ignored files, ls-tree/ls-files digests equal, 0 blob mismatches, 0 gitlinks.
- `receipts/r1-rerun/*`: round-1 probes and mutants re-run.
- `scripts/`: `r279_probe_cases.cpp`, `apply_probes.py`, `run_probes.sh`, `run_mutants.sh`. The `scripts/r1/` directory holds this reviewer's round-1 scripts, copied verbatim from the public evidence; they need `PIN_VERILATOR`. Every script runs only on disposable extracts under `scratch/`.

R279-2 FINISHED
