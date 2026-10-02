[R437] NEGATIVE - exact head c0715410418b47ffaccf5feed55b71617fcfaf82

# R437-2: external delta review of PR #145 (lane P2, NVM port robustness)

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan. Issue #15, lane P2 (#15, #18, #19, #20, #21; the PR closes all five).
- **Head:** `c0715410418b47ffaccf5feed55b71617fcfaf82`, tree `4bbf1197895a9fadf4d14dea2ae9ad5f2d3336b0`. It is a `--no-ff` merge of round 2 (`c26b14b3`) with `main` `631eeb34` (PR #142).
- **Scope:** round 2 (assignment 5956438390, answering R436-1 and R437-1) and round 2b (assignment 5959104191, the merge).
- **Clone:** isolated and detached. After every probe it was verified byte-exact at the head (`receipts/clone_integrity.txt`):
  - `write-tree` equals `4bbf1197`, and the porcelain is empty, ignored files included;
  - the index's modes and blobs equal the HEAD tree;
  - there are no gitlinks and no `.gitmodules`, so no submodule pin is required.
- **Verdict: NEGATIVE.** Three MINOR findings are open (F1, F2, F3), so two lenses are unclean: Tests and Docs.
  - Conformance, RTL and Robustness are clean.
  - I found no RTL defect at this head, and every round-1 finding is closed.
  - The open findings are gaps in the tests:
    - two of my planted defects in the new pause logic survive every model at both bounds, and each falsely refuses a contract-legal device;
    - the TMO-derived harness is not green at every legal bound, as its README claims.

## 1. Reconstruction (order followed)

1. **Repository rules.** There is no AGENTS.md or CONTRIBUTING.md. I used `docs/README.md` (single-source rules, editing workflow, `make check`).
2. **Scope.** The bodies of issues #15, #18, #19, #20 and #21, and these comments on #15:
   - 5355168983 (bound every device wait) and 5355231359;
   - 5951891343 (lane assignment), 5952358239 (the STOP), 5952386396 (the ruling: `MEM_TIMEOUT_CYC_P`, DEADLINE cause 3, containment, ruling (c));
   - 5956438390 (round 2) and 5959067531 (round 2 REVIEW READY);
   - 5959104191 (round 2b) and 5960259376 (round 2b REVIEW READY).
3. **Authorities.**
   - The port banner (`hdl/packet_engine/KL_pp_nvm_port.sv:42-107`).
   - 02 §8, the deadline paragraph (`docs/architecture/02_interfaces.md:530-552`).
   - F08.1 `T-NVM-PORT-DEADLINE`, F01.5 `P-NVM-MEM-TMO-CYC`, and the integrator guide's `NVM_MEM_TMO_CYC_P` row.
   - 09 §8.2's closing paragraph and §8.5 (`09_verification.md:208-215`, `:295-319`).
   - The `tb/nvm_port` README: the model table, the mutation record and "Two bounds" (`:600-635`).
4. **The diff.** `git diff 631eeb34..c0715410` (20 files) and the round-2 commits `e42870e`, `6b6f309`, `ff2cce1`, `06db35e`, `36abf30` and `c26b14b`, plus the merge.
5. **Public evidence.** milan-fpga `review-evidence/ppP2-r1`: the round-1 packet at `d56e2227`, and `author-r2` and `author-r2b` on branch `ppP2-review-evidence` at `c86a5ff9`.
   - All 8 round-2 files match `MANIFEST.json` `published_sha256`.
   - The live PR body equals `author-r2b/PR-BODY.md`.
   - Both parent patches are byte-identical to round 1's (`receipts/parent_patch_check.txt`).
6. **Prior public findings, read only after my own independent pass:** R437-1 (5956174225) and R436-1 (5956427403). Their resolution is in section 4.

## 2. Executed evidence (exact head; scoped Verilator 5.050, identity in `receipts/toolchain.txt`)

| Run | rc | Result |
|---|---:|---|
| `make -C tb/nvm_port` on a `git archive` export: the elaboration guard, then builds at 100 and 37 | 0 | The guard refuses 0, 2^31 and 2^32-1 by name. 343 + 343 = 686/686 |
| `make -C tb/acmp_nvm` (export) | 0 | 372 + 16 = 388/388 |
| `make -C tb/nvm_port figures` | 0 | 88 builds. Baseline 343/343; `make run` [(343,343,0),(343,343,0),(686,686,0)]; all 87 rows agree, D18-D26 included (D23 0, D26 0, D26/coincident 5); short read 265/78 and silent 115/228 (`receipts/figures_gate.log`) |
| `make check`, in a disposable local clone at the head | 0 | 41 mermaid + 18 WaveDrom; links 1,045; REQ 115 rows / 17 GAP; 94 module rows, 0 untested; parameters 28 = 28 = 28 |
| `lint_hdl.sh` flags on `KL_pp_nvm_port`, `KL_pp_nvm_mgr_arb` and `protocol_processor_top` | 0 | Clean at the default and at `NVM_MEM_TMO_CYC_P` = 1, 37 and 2^31-1. Refused by name at 0 (top) and 2^31 (port) (`receipts/lint_changed.txt`) |
| Out-of-context cost (sv2v, then Yosys `synth_xilinx -family xc7 -flatten`), main `631eeb34` against the head | 0 | main 197 LUT, 118 FF, 14 CARRY4. At the default: **+48 LUT, +30 FF, +7 CARRY4**. At 1: +51 LUT, +4 FF. At 2^31-1: +69 LUT, +34 FF, +8 CARRY4. At 125 M: +64 LUT, +30 FF, +7 CARRY4. All equal the PR body (`receipts/ooc_cost.txt`) |
| D23 invariant, Yosys SAT temporal induction from reset, all inputs free | - | **Proven** at `MEM_TIMEOUT_CYC_P` = 3 and 100: `owed_r` is set only in `S_IDLE`, `S_FIN`, `S_WHDR`, `S_WEREQ` or `S_RHREQ`. The negative control (the invariant without `S_RHREQ`) finds a counterexample (`receipts/formal/`) |
| Planted pause-logic defects Y1-Y16 | - | `receipts/y_pause/`, `receipts/z2_directed/` (section 3) |
| Round-1 probes re-run unchanged | - | `receipts/r1_reprobe/` (section 4) |
| The head's suite at further legal bounds: 20, 21, 64, 200-800, 1000, 1001, 4096, 100000 | - | `receipts/bounds/`, `receipts/bounds2/`, `receipts/t6_restaged/` (F3) |
| Both parent patches at dev `cdf49d1a`, files fetched read-only | 0 | c4c6 then p2: `git apply --check` clean, each applied; the result blob is `6021944`, as in round 1 |

**Merge verification (round 2b).** The two sides share only `07_memory_maps.md` and `09_verification.md`.

- Every other file equals its own side: main's files equal `631eeb34`, the lane's equal `c26b14b3`.
- 07 carries this lane's hunks exactly beside main's L6 row.
- 09 §8.2's closing paragraph keeps both sides: main's D3C row, its count of 87 and its `aecp_dispatch_mutants.py` `d3` sentence, beside the lane's pointer to §8.5.
- §8.5 keeps its number; main ends at §8.4.
- The only `hdl` change is main's `gen_ucode.py`, and it touches comments only. The port, arbiter and top sources are byte-identical to round 2's.

**Hosted CI at the exact head** (snapshot 20:17Z, `receipts/hosted_checks_snapshot.txt`):

- `docs-gates` and `portability` succeeded on both runs.
- `suites` was still in progress on both.
- The manager owns hosted and act acceptance.

## 3. Findings

### F1 - MINOR - Tests, Docs: a paused cycle at the bound is not pinned as "never a verdict"

- **Where:**
  - `hdl/packet_engine/KL_pp_nvm_port.sv:276`: `assign dl_w = owe_w && !prog_w && tmo_hit_w;`. Its `owe_w` term is what keeps a cycle that owes nothing from being a verdict once the count sits at its bound.
  - The claims: T29 (`tb/nvm_port/sim_main.cpp:2095-2134`; README `:526-534`, "a dropped cycle owes nothing and neither counts nor restarts") and 09 §8.5 (`09_verification.md:307`, "a clock in which the device owes nothing pauses the count … | T29; D24, D25, D26").
- **Authority:**
  - The banner `:76-82` and 02 §8 (`02_interfaces.md:538-541`): a cycle that owes nothing PAUSES the count, and the verdict comes on the (`MEM_TIMEOUT_CYC_P` + 1)-th **owed** clock.
  - T24's tolerated arm: an event after exactly `TMO` silent owed cycles is legal.
  - T29: a manager dropping `rready` or `wvalid` is "a pattern a manager is free to present" (`sim_main.cpp:298-300`).
- **Evidence:** two planted defects survive.
  - **Y11** lets the verdict fire on a paused pump cycle (`(owe_w || S_WDPUMP || S_RPPUMP)`). It leaves all 343 checks green at 100 and at 37.
  - **Y16** is the natural simplification, a verdict on any busy cycle (`(state_r != S_IDLE) && (state_r != S_FIN)` in place of `owe_w`). It leaves all 343 green in 13 of 14 cells: seven legal models at two bounds. The one exception is T29b, coincident at 37.
  - My directed checks Z1a and Z1b drop the manager's strobe on the cycle after exactly `TMO` silent owed cycles, on which the device presents its byte. Z1a drops `rready` on payload byte 10; Z1b drops `wvalid` on WRITE byte 20.
  - The head passes both under all seven contract-legal models at both bounds (349/349).
  - Y11 and Y16 each fail Z1a, Z1b and RW4: an err DEADLINE against a device that was not silent (`receipts/z2_directed/`).
- **Impact:** a regression to a verdict on a paused cycle ships green.
  - It falsely refuses a legal device, the one T24 tolerates, whenever a legal manager pattern, the one T29 presents, drops its strobe on the bound cycle.
  - That is the pause property this round added, and both the README and 09 §8.5 present T29 as grading it.
- **Required outcome:**
  - Add a named check that kills Y11 or an equivalent: a strobe dropped exactly on the bound cycle against an event `TMO` owed cycles late, tolerated, done and byte-exact, in both pumps.
  - Record the defect as a figures-gate mutation row.
  - Correct the README and 09 §8.5 counts.
- **Verification:**
  - The new row fails its named check.
  - The head stays green under all seven legal models at 100 and 37, and the RW checks hold under all nine.
  - `make -C tb/nvm_port figures` gives rc 0.

### F2 - MINOR - Tests, Docs: the latched-done term is unpinned in `S_WEWAIT`

- **Where:**
  - `KL_pp_nvm_port.sv:259-260`, the round's second RTL term: a wait state whose terminal is already latched owes nothing.
  - The claims: 09 §8.5 `:307` ("a wait state consuming a latched done owes nothing | … D26 under the coincident model") and README `:594-601`.
- **Authority:**
  - The banner `:73-74` ("a terminal not yet latched") and 02 §8 `:535` ("unless that terminal is already latched").
  - The banner `:33-34`: backends without erase semantics answer ERASE with done at once. T21 grades the case where that done rides the grant.
  - T24's tolerated `S_WWREQ` arm: a WRITE grant `TMO` cycles late is legal.
- **Evidence:** I dropped the term one wait state at a time, each probe run under all seven legal models at 100 and 37 (`receipts/y_pause/`).
  - **Y2** (`S_RHWAIT`) fails 5 under coincident. That is the instance D26/coincident pins.
  - **Y3** (`S_WWAIT`) and **Y4** (`S_RPWAIT`) are 0 everywhere, and are equivalent: a latched done takes those wait states straight to `S_FIN`, and the count is zeroed in `S_IDLE`.
  - **Y1** (`S_WEWAIT`) is **0 in all 14 cells**. It is not equivalent. When ERASE's done rides its grant, the cycle in `S_WEWAIT` that consumes the latched done is charged, and the pause carries that charge into `S_WWREQ`.
  - My directed check Z2 combines T21's freedom with a WRITE grant `TMO` cycles late. The head passes it under all seven legal models at both bounds. Y1 fails Z2 (err DEADLINE) and RW4 (`receipts/z2_directed/`).
  - The README's own D26 text says the pristine model's only such sequence is "followed by a WRITE grant far inside the deadline".
- **Impact:**
  - Half of the term that this round found necessary can regress with the suite green.
  - The regression falsely refuses a backend without erase semantics that grants the next WRITE late but inside the deadline. That backend is a freedom the banner itself names.
  - 09 §8.5 presents the property as covered by D26/coincident, which covers only `S_RHWAIT`.
- **Required outcome:**
  - Add a named check that kills Y1, for example T24's `S_WWREQ` tolerated arm repeated with the ERASE answered on its grant, or Z2.
  - Record it as a figures-gate row.
  - Make 09 §8.5 and the README say which wait states are pinned, and that `S_WWAIT` and `S_RPWAIT` are equivalent.
- **Verification:**
  - Y1 fails a named check.
  - The head stays green as in F1.
  - `make -C tb/nvm_port figures` gives rc 0.

### F3 - MINOR - Tests, Docs: the TMO-derived harness is not evidence at every legal bound, because T6's poke outruns the commit under the coincident model

- **Where:**
  - `tb/nvm_port/sim_main.cpp:995-1003`. T6 stages its stray request `kStageCycles` = 2·`TMO`/5 after the accept, with `op_delay` = 3·`TMO`/10.
  - The claim: README `:606-609`, "Every wait in the harness that meets the deadline is a function of `TMO`, so the suite is evidence at any bound it is built at", followed by the statement that it used to fail at 1,000.
- **Authority:**
  - Round-2 assignment item 5: derive the harness constants from `TMO`.
  - #21 item 4 and the README model table: coincident completion is a contract freedom that must leave every check green.
- **Evidence:** the head, with no defect, under the coincident model (`receipts/bounds/`, `receipts/bounds2/`):
  - green at 20, 21, 37, 64, 100, 200, 300, 400 and 450;
  - **15 or 16 FAIL** at 500, 550, 600, 800, 1000, 1001, 4096 and 100000, with T6, then T7-T9 as collateral, and RW1 "3 wedged".
  - Pristine, lazy erase and unsolicited are green at 1000. The coincident model ends the WRITE on its last byte, which removes one `op_delay`, so the commit is over before the poke. The stray restore is then accepted by an idle port while the manager model is in commit mode, and the next operations wedge behind it.
  - **Attribution:** with only T6's poke re-staged to `TMO`/10, pristine, coincident and unsolicited are 343/0 at 37, 100, 500, 1000 and 100000 (`receipts/t6_restaged/`). The port is not at fault.
- **Impact:**
  - The suite's claim to be evidence at any bound is false for a required model at large bounds.
  - Built near a realistic deadline, a contract-legal model reports 16 failures and 3 wedges.
  - Only 100 and 37 are gated, so nothing catches it.
- **Required outcome:**
  - Stage T6's poke inside the operation at every bound. For example, name it on the bus as T25's `run_to_stage` does, or derive it so that it always falls before the ERASE completes.
  - Alternatively, bound the README's claim to the bounds and models it holds for, and gate it.
- **Verification:**
  - The coincident model is 343/0 at 1000 and at a large bound such as 4096.
  - Every model's figures are unchanged at 100.
  - `make -C tb/nvm_port figures` gives rc 0.

### S1 - SUGGESTION - RTL, Robustness: the owed READ's drain is not bounded by its length

- **Where:** `KL_pp_nvm_port.sv:271` and `:589`. Every byte drained from an owed READ is progress, whether or not the READ has bytes left.
- **Evidence:** a broken backend keeps streaming a READ, abandoned at a deadline, past its commanded length, one byte every `TMO`/2. A restore waiting in `S_RHREQ` is never answered: the harness guard trips after 1,961 drained bytes (`receipts/babble/`).
- **Why only a suggestion:** this is outside the contract and outside the four modelled backends. A READ never delivers more than its length.
- **Suggested change:** either stop counting the drain as progress once the owed READ's commanded length has moved (the port issued that length), or state in the banner that a device streaming past an owed READ holds the waiting request off.

### S2 - SUGGESTION - Tests (retained from R437-1 S2): a late grant that carries `err`

- **Evidence:** X20 still leaves the suite green under all seven legal models at both bounds (`receipts/r1_reprobe/`).
- **Status:** not assigned in round 2; the PR body lists it under "what remains".

### RESIDUE (wording only, retained from R437-1; not assigned, carried by the manager)

| ID | Location | Status at this head |
|---|---|---|
| R2 | `tb/nvm_port/README.md:906` and `:913` | still present; R437-1's exact fix stands |
| R3 | `tb/nvm_port/sim_main.cpp:1125` and `:1211` | still present (moved from `:1082`/`:1169`) |
| R4 | `hdl/acmp/KL_acmp_nvm_shadow.sv:208` and `hdl/aecp/KL_aecp_nvm_writer.sv:260` | still present |
| R5 | parent `SAVED_STATE_MATERIALIZATION.md:1930`, after both patches | still present; the patch is unchanged |

R437-1's R1 is resolved at `README.md:899`.

## 4. Prior public findings at this head

Each probe was re-run unchanged at the head under pristine and coincident, at 100 and 37 (`receipts/r1_reprobe/`).

| Finding | Probe | Result at the head | Status |
|---|---|---|---|
| R437-1 F1 (T1 under lazy erase; #21 item 4) | the lazy-erase models | 343/0 for both lazy rows, at 100 and 37 and at 20-1001; T1 keeps its bus pins (`sim_main.cpp:917-922`) | **Closed** |
| R437-1 F2 | X12 | 2 FAIL: T28c, RW3 | **Closed** |
| R437-1 F2 | X17 | 1 FAIL: T28e | **Closed** |
| R437-1 F2 | X18 | 1 FAIL: T28d (3 at 37, with T24's served branch) | **Closed** |
| R437-1 F2 | X24 | 1 FAIL: T28a | **Closed** |
| R437-1 F2 | X24b | 2 FAIL: T28a, T28b | **Closed** |
| R437-1 S1 (strobe toggle) | P1, round 1's phase on the harness's own drop mechanism | answered DEADLINE (347/347); T29 grades it | **Taken** |
| R437-1 S2 | X20 | 0 FAIL | Retained (S2 above) |
| R437-1 R1 | - | fixed | **Closed** |
| R437-1 R2-R5 | - | present | Retained as residue |
| R436-1 F1 | W15 | 1 FAIL: T28a | **Closed** |
| R436-1 F1 | W15b | 1 FAIL: T28b | **Closed** |
| R436-1 F1 | W16 | 1 FAIL: T28d | **Closed** |
| R436-1 F2 (= R437-1 F1) | - | as above | **Closed** |
| R436-1 R1 | - | the exact text is at `README.md:899-902` | **Closed** |
| R436-1 S1 (pause) | W6: its anchor is gone because the pause is now the design; its semantics at the head are the pause without the latched term | 0 under pristine; **5 under coincident** (T24 `S_RPREQ` ×3, slow restore, RW4), which is D26/coincident | **Taken**; the term it needed is partly unpinned (F2) |
| R436-1 S2 (TMO-derived harness) | - | the second build at 37 is green | **Taken**; a residual staging flaw at large bounds (F3) |

## 5. Judgement on the delta items

1. **T1 is model-neutral.** It keeps its bus checks: ERASE, then WRITE, then region 3 erased once. It asserts the erased tail only when `lazy_erase` is off, and the model and the check read the same switch. Both lazy rows are 343/0. **#21 item 4 is met:** every model the port must tolerate leaves all 343 checks green at 100 and 37.
2. **T28a-e and D18-D23.** Each row reproduces in the figures gate, and each round-1 probe fails its named T28 check.
   - **D23** (the `S_WWREQ` and `S_RPREQ` guards dropped) is a true equivalence. The invariant it rests on is proven by induction for all inputs at two bounds, with a negative control (`receipts/formal/`).
   - The same invariant also held in simulation, as an RTL monitor, under all nine models at both bounds.
3. **The pause.**
   - **Starvation:** none found. A silent device is answered under every manager pattern I planted. The count holds on a paused cycle and is zero only in `S_IDLE` or on a device event (`:278-282`). D24, Y13 and Y14 (a pause that clears in either pump) are killed, and so are Y8 (a request waiting on an owed command that pauses), Y9 and Y10 (a pump that owes only once the device is ready) and Y15 (a one-bit-short counter).
   - **False trips:** none at the head. A paused cycle charged as owed (Y5, Y6, Y7) is killed. A wait state with a latched done always leaves on that cycle, so the `!done_seen_r` term cannot starve.
   - The two surviving planted defects that do falsely trip are F1 and F2.
   - Y3, Y4 and Y12 (a manager handshake counted as progress) are equivalent.
   - The out-of-context cost reproduces, at +48 LUT and +30 FF at the default.
4. **Harness waits derived from TMO, and a second build at 37:** green at 37. F3 covers large bounds.
5. **The merge** is verified as above. No RTL change, and both sides are kept in 09 §8.2.

The issues against their own acceptance lists:

| Issue | Status |
|---|---|
| #15 | Met (ruling (c), both branches) |
| #18, #19, #20 | Met as in round 1 |
| #21 | Met (item 4 above) |

F1-F3 are test-coverage and harness defects. None changes an issue's acceptance verdict.

## 6. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Acceptance lists for #15, #18, #19, #20 and #21; the ruling 5952386396; the round-2 and 2b assignments; banner `:42-107`; 02 §8 `:530-552`; F08.1; F01.5; the integrator row; both parent patches at `cdf49d1a` | R437-2 | c0715410418b47ffaccf5feed55b71617fcfaf82 |
| RTL | CLEAN | `KL_pp_nvm_port.sv` (full read), the arbiter and top diffs, the merge's `hdl` delta (comment only); lint at 1, 37, the default and 2^31-1 plus the refusals; OOC cost at four settings; D23 induction proof | R437-2 | c0715410418b47ffaccf5feed55b71617fcfaf82 |
| Robustness | CLEAN (S1 advisory) | Pause, owed state, drain, late grant and reset: 16 planted pause defects plus 3 directed checks across 7 legal models × 2 bounds; a babbling-backend probe; bounds 20 to 100000 | R437-2 | c0715410418b47ffaccf5feed55b71617fcfaf82 |
| Tests | UNCLEAN (F1, F2, F3) | `tb/nvm_port` (686), `tb/acmp_nvm` (388), the figures gate (88 builds), the round-1 probes re-run, Y/Z probes, the bound sweep | R437-2 | c0715410418b47ffaccf5feed55b71617fcfaf82 |
| Docs | UNCLEAN (F1, F2, F3 coverage claims); R2-R5 are residue | The `tb/nvm_port` README, 09 §8.2 and §8.5, 02 §8, F08.1, the integrator guide, 07 (merge), the PR body's Round 2 and 2b sections, `make check` | R437-2 | c0715410418b47ffaccf5feed55b71617fcfaf82 |

## 7. Real limits

- **Not run by me, by scope:** `run_suites.sh`; `lint_hdl.sh` over all 41 modules; `syn/yosys/run.sh`; the CI mutation campaigns and `d3_mutants.py`; the donor bank; the parent consumer set; act or hosted reproduction; Vivado. I rely on the manager's public evidence for these.
- **Hosted `suites`** was still in progress at my snapshot.
- **Device models are models.** No real backend or flash was run. Physical calibration was NOT RUN, and field skips are not hardware proof. The default deadline is a derivation, not a measurement.
- **The formal proof covers only D23's invariant.** Everything else is simulation against the harness's models.
- **An observation, not a finding:** the port passes a manager's dropped `wvalid` straight to the device face (`:584-585`), and 02 §8 states no valid-hold rule for that face. A device whose `wready` waits on a held valid could therefore be slowed by a strobe-dropping manager. No in-tree device or manager does this.

## 8. Pending manager duties

- Run the donor bank (9) and the parent consumer set (16) at dev `cdf49d1a`, with `parent-adoption-c4c6-ea3fb388.patch` then `parent-adoption-p2-cdf49d1a.patch` (unchanged).
- Hosted and act acceptance at the exact head; the `suites` job was still running at my snapshot.
- The final current-dev candidate at the merge turn (source base `631eeb34`, live dev `cdf49d1a`).
- Route F1-F3 to the author, then re-review. Re-run Y1, Y11, Y16, the T6 bound sweep and the figures gate (`scripts/probe.py` with `scripts/spec_y_pause.py`, `spec_z2_directed.py`, `spec_bounds*.py` and `spec_t6stage.py`).
- Carry R2-R5 to the residue checklist.
- Renumber 09 §8.5 against lane C8 (PR #144), whichever merges second.

## Receipts

Every published receipt is listed in `MANIFEST.sha256`.

- `scripts/probe.py` is the driver. Each job takes a `git archive` copy of the head, applies exact-once edits, and builds with the Makefile's flags at `-GMEM_TIMEOUT_CYC_P`/`-DNVM_PORT_TMO`. The model edits are imported from the head's `measure_figures.py`.
- `scripts/spec_*.py` are the probe definitions.
- `scripts/ooc_cost.sh` measures the out-of-context cost; `scripts/formal_d23.sh` runs the D23 proof.

R437-2 FINISHED
