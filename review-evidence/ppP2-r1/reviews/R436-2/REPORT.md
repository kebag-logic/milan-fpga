[R436] NEGATIVE - exact head c0715410418b47ffaccf5feed55b71617fcfaf82

# R436-2: internal independent delta review of PR #145 (lane P2, NVM port robustness)

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #145. It closes #15, #18, #19, #20 and #21.
- **Head:** exact head `c0715410418b47ffaccf5feed55b71617fcfaf82`, tree `4bbf1197895a9fadf4d14dea2ae9ad5f2d3336b0`. It is a `--no-ff` merge of main `631eeb342ca1e3fa80e734077a56a943aee76ff1` (#142) into round 2's `c26b14b3`.
- **Delta reviewed:**
  - round 2 (`70bf017d..c26b14b3`, six commits; assignment on #15, comment 5956438390);
  - round 2b (the merge; assignment 5959104191).
- **Clone:** round R436-2 ran in a cleared context, in its own detached clone. After every probe the clone was verified byte-exact at the head (`receipts/clone_integrity.txt`):
  - worktree, index, blob bytes, modes and `write-tree` all equal `4bbf1197`;
  - the porcelain is empty, ignored files included;
  - the repository has no gitlinks.

## Verdict

**NEGATIVE.** One MINOR finding is open (F1), so the Tests and Docs lenses are unclean.

**F1:** two defects I planted in round 2's pause logic pass all 343 checks under every model, and the figures gate passes too. Each one makes the port refuse a contract-legal device with DEADLINE:
- **Q1:** the `S_WEWAIT` member of the new latched-terminal term is dropped;
- **Q9:** a verdict is allowed on a paused cycle.

The RTL at the head is correct. My independent randomized harness finds no false trip and no starvation by any manager pattern at bounds 1, 2, 3, 37 and 100. Its silent-device verdict lands on exactly the (TMO + 1)-th owed cycle under random manager strobes.

**Every round-1 finding is closed at this head**, and each round-1 probe now fails a named check:
- R436-1: F1 (W15, W15b, W16) and F2 (T1 under lazy erase);
- R437-1: F1, and F2 (X12, X17, X18, X24).

**The merge is clean:**
- both sides are kept;
- every one-sided file equals its parent;
- no RTL changed;
- no cited line moved.

**Smaller items:**
- One SUGGESTION: an over-length owed drain holds a waiting request off (S1).
- Two wording RESIDUEs (R1, R2).
- R437-1's S2 and R2-R5 are retained; they were not assigned this round.

## How the review was reconstructed

1. **Contributor rules.** The tree has no AGENTS.md or CONTRIBUTING.md. I read `README.md` and `docs/README.md` (the single-source rules: timing only in F08.1, parameters only in F01.5).
2. **Scope.** Issue #15's body and its comments:
   - the scope and reachability corrections (5355168983, 5355231359);
   - the readiness assignment (5573417155);
   - the lane assignment (5951891343);
   - the design STOP (5952358239) and the ruling (5952386396);
   - the round-1 REVIEW READY (5955151206);
   - the round-2 assignment (5956438390) and its REVIEW READY (5959067531);
   - the round-2b assignment (5959104191) and its REVIEW READY (5960259376).

   Also the acceptance lists of #18, #19, #20 and #21.
3. **The PR body.** Its Round 2 and Round 2b sections. It is byte-identical to `review-evidence/ppP2-r1/author-r2b/PR-BODY.md` on milan-fpga's `ppP2-review-evidence` branch, except for a trailing newline.
4. **Authorities:**
   - the port banner (`KL_pp_nvm_port.sv:28-108`);
   - 02 §8 (`02_interfaces.md:530-546`) and F08.1's `T-NVM-PORT-DEADLINE` row (`08_timing.md:46`);
   - the integrator guide's `NVM_MEM_TMO_CYC_P` row and the top's parameter comment;
   - 09 §8.2 and §8.5;
   - the `tb/nvm_port` README's line between a contract freedom and a broken backend.
5. **The diffs:**
   - `git diff 631eeb34..c0715410` (20 files);
   - the round-2 delta `70bf017d..c26b14b3` (10 files, the RTL hunk read in full);
   - the merge, re-derived with `git merge-tree`.
6. **Public evidence:**
   - milan-fpga `d56e2227` `review-evidence/ppP2-r1` (the round-1 author packet);
   - the `ppP2-review-evidence` branch head `c86a5ff9`, for the author-r2b packet. Both parent patches match their stated sha256: p2 `3dda8509…d08b` (9,728 bytes) and c4c6 `67bcd698…7bd7c` (2,687 bytes).
7. **Prior public review findings on this PR.** I read R436-1 (5956427403) and R437-1 (5956174225), and their published probe definitions, only after my own pass over the diff. All are resolved or retained below.

I did not read any other reviewer's round-2 report, any lane scratchpad, or any private author material.

## Executed evidence (exact head; receipts listed in MANIFEST.sha256)

The simulator is the scoped Verilator 5.050 wrapper. `--version` prints `Verilator 5.050 2026-07-01 rev v5.050`; the wrapper's hash is in `receipts/verilator_identity.txt`. The system default (5.052) was never used.

| Run | rc | Result | Receipt |
|---|---:|---|---|
| `make -C tb/nvm_port run` (`elab_bounds.sh`, then builds at 100 and at 37) | 0 | 343 + 343 = 686 PASS | `receipts/nvm_port_make_run.log` |
| `elab_bounds.sh` | 0 | ELAB OK at 1 and 2^31-1; GUARD OK at 0, 2^31 and 2^32-1 | `receipts/elab_bounds.log` |
| `make -C tb/nvm_port figures` | 0 | 88 builds: baseline 343/343; `make run` 343 + 343; all 87 rows agree, the same figures as the PR body; one waiver (2) | `receipts/figures_gate.log` |
| every figures-gate model at 37 (`scripts/models_at_37.py`) | 0 | the seven legal models 343/0 each; short read 265/78; silent 115/228; RW checks pass under all nine | `receipts/models_at_37/` |
| `make -C tb/acmp_nvm run` | 0 | 372 + 16 = 388 PASS | `receipts/acmp_nvm_run.log` |
| `make -C tb/pp_top run` | 0 | 9,168 PASS (round 2's 9,151 plus main's 17 D3C checks) | `receipts/pp_top_run.log` |
| `scripts/lint_hdl.sh` | 0 | 41 modules LINT OK | `receipts/lint_hdl.log` |
| `make check` (disposable clone); `gen_matrix.py --check` | 0, 0 | 41 mermaid + 18 WaveDrom; links 1,045; REQ 115 rows, 17 GAP; module matrix 94 rows, 0 untested; parameters 28 = 28 = 28 | `receipts/make_check.log`, `receipts/gen_matrix.log` |
| round-1 probes, unchanged (`scripts/rerun_round1.py`) | – | see "Round-1 findings" | `receipts/rerun_round1/` |
| R437-1's X20, unchanged | – | 343 + 343 PASS (survives) | `receipts/rerun_x20/` |
| reviewer plants in the pause logic (`scripts/plant.py`): the suite under 4 models, plus a fuzz at 37 and 3 | – | 16 rows | `receipts/plants/plants.md`, `plants.json` |
| reviewer randomized harness on the head (`scripts/pause_fuzz.cpp`): legal, silent, resume and babble at 1, 2, 3, 37 and 100 | 0 | 0 false trips; every silent verdict at exactly TMO + 1 owed cycles; resume served iff r <= TMO; babble never answered | `receipts/fuzz_head/SUMMARY.txt` |
| directed checks R436d-f, injected into probe copies (`scripts/directed.py`) | – | head 347 + 347; Q1 fails R436d; Q9 fails R436e alone | `receipts/directed/SUMMARY.txt` |
| D23 invariant monitor (`scripts/d23_invariant.sh`) | – | 0 violations under 5 models and 6 fuzz runs; the owed state is reached tens of thousands of times | `receipts/d23_summary.txt`, `receipts/d23/` |
| out-of-context cost (`scripts/ooc_cost.sh`: sv2v, then Yosys `synth_xilinx -flatten`) | 0 | see the RTL lens | `receipts/ooc/` |
| merge re-derivation (`git merge-tree`, per-file blob comparison) | – | see the merge section | this report |
| hosted checks at the head (read-only snapshot) | – | `docs-gates` and `portability` succeeded on both runs; `suites` was in progress at the snapshot | `receipts/hosted_checks_snapshot.txt` |

## Round-1 findings, judged at this head under their original severity

Every round-1 probe was re-run with its edit copied verbatim from the published round-1 scripts. Each ran in a fresh export with `make run` (both bounds), under the pristine harness and under the coincident-completion model.

| Finding | Severity | Status | Evidence at c0715410 |
|---|---|---|---|
| R436-1 F1: owed-command ends and drains unpinned | MINOR | **RESOLVED** | W15 fails T28a, W15b fails T28b, and W16 fails T28d, under both models. Recorded as figures rows D18, D19 and D20, which agree. |
| R436-1 F2 = R437-1 F1: #21 item 4, T1 under lazy erase | MINOR | **RESOLVED** | Lazy erase and lazy erase + page-buffered both read 343/0, at 100 (figures gate) and at 37. T1 keeps its bus pins (`sim_main.cpp:916-922`) and conditions only the erased tail on the backend's erase semantics (`:929`), as assigned by outcome (a). |
| R437-1 F2: X12, X17, X18 and X24 unpinned | MINOR | **RESOLVED** | X12 fails T28c and RW3; X17 fails T28e; X18 fails T28d; X24 fails T28a; X24b fails T28a and T28b. Rows D18-D22 agree, and the README and 09 §8.5 counts are measured by the gate. |
| R436-1 R1 (sentence fragment) | RESIDUE | **RESOLVED** | `README.md:899-902` uses the exact text. |
| R437-1 R1 ("below") | RESIDUE | **RESOLVED** | `README.md:899` reads "above". |
| R436-1 S1 = R437-1 S1: the watchdog clears rather than pauses | SUGGESTION | **TAKEN** | See W6 below. |
| R436-1 S2: harness constants fixed at 100 | SUGGESTION | **TAKEN** | `make run` builds at 100 and at 37, both 343/0. All nine models at 37 are as the PR body states. |
| R437-1 S2: a late grant carrying err (X20) | SUGGESTION | **RETAINED** (not assigned) | X20 still passes 343 + 343. |
| R437-1 R2-R5 | RESIDUE | **RETAINED** (not assigned) | Still present: `README.md:906-913`, `sim_main.cpp:1125` and `:1211`, `KL_acmp_nvm_shadow.sv:208`, `KL_aecp_nvm_writer.sv:260`, and the parent page. |

**W6** was my round-1 plant "pause, not clear". Its anchor names the round-1 count, which the head replaced, so at the head it reports `ANCHOR occurs 0 times`.

Applied unchanged to the round-1 port source under the head's harness:
- **Pristine:** it passes 343 + 343.
- **Coincident model:** it fails 5: T24 S_RPREQ ×4 and RW4.

That is D26. The figures gate runs the coincident model on the head, requires 343/0, and records D26/coincident = 5, so a regression to W6 fails the gate. **W6 is closed.**

The round-1 count itself, under the head's harness, fails T29a, T29b and RW1 (D24).

## The delta, item by item

1. **T1 is model-neutral.** It now asserts the erased array only where the harness's `lazy_erase` switch says the backend has erase semantics. The bus-level ERASE pins stay. Both lazy rows read 343/0, and **#21 item 4 is met**: every model the port must tolerate is 343/0 at both bounds.
2. **T28a-e and rows D18-D23.** T28 drives the owed command's err, done and slow drain while a request waits in `S_RHREQ` or `S_WEREQ`, and a deadline in `S_WWAIT`. D18-D22 are each killed by a named check.

   **D23's equivalence claim holds.** A command becomes owed only on the edge out of a deadline cycle (into `S_FIN`), or in the `S_FIN` cycle that follows (the late grant). It is cleared only by the device's terminal. While it is owed, the first request state (`S_WEREQ` or `S_RHREQ`) blocks on it. So `owed_r` implies the state is `S_IDLE`, `S_FIN`, `S_WHDR`, `S_WEREQ` or `S_RHREQ`.

   A monitor of exactly that invariant (`scripts/d23_invariant.sh`) records 0 violations under the pristine, coincident, unsolicited, short and silent models and six fuzz runs. Owed-at-first-request cycles: 2,429 in the pristine suite and 28,796 in the resume fuzz at 37. The figure "measured equivalence" is honest. The two guards, and `dev_req_o`'s own `!owed_r`, are redundant by construction.
3. **The pause** (`KL_pp_nvm_port.sv:258-260`, `:278-282`). The count restarts only on progress, zeroes in `S_IDLE`, counts owed cycles, and holds otherwise. The second term exempts a wait state whose terminal is already latched.

   I traced every transition into a newly owed state. The count is always 0 there: from `S_IDLE`, from a progress cycle, or carried through a holding state (`S_WHDR`, `S_RHFWD`, a manager-stalled pump, a latched wait) whose last event was progress.

   - **The second term is needed for exactly two of its four members.**
     - The latched cycle of `S_RHWAIT` precedes `S_RHFWD` and then `S_RPREQ`.
     - The latched cycle of `S_WEWAIT` (an ERASE answered on its grant) precedes `S_WWREQ`.
     - `S_WWAIT` and `S_RPWAIT` exit to `S_FIN` and then `S_IDLE`, which zeroes the count, so their members are equivalent. Q3 and Q4 below are 0 everywhere, the fuzz included.
   - **No contract-legal device is falsely refused, and no manager pattern starves the verdict.** The reviewer harness's legal mode never trips at 1, 2, 3, 37 or 100, with devices biased to the exact bound. Those devices answer ERASEs on their grant and complete on the final byte's edge. Strays appear where nothing is owned, and the manager drops its strobe at random, periodically, or for up to 5·TMO.
   - **The silent verdict is exact.** In silent mode, at every bound, it lands on exactly the (TMO + 1)-th owed cycle counted by an oracle written from the banner, under random manager drops.
   - **What can still hold a waiting request off:**
     - a manager that never presents its strobe, which wedges itself, not a device;
     - an over-length owed drain (S1).
   - **T29 grades D24's failure exactly.** Its timing check `TMO + 2 + held` holds. But its drop phase never lands on the cycle after the count reaches its bound, so it cannot see Q9 (F1).
4. **Harness waits derived from TMO.** The second build at 37 is green, and so are all nine models at 37. The harness refuses to build below TMO = 20. That limit is documented.
5. **Out-of-context cost** (main `631eeb34`: 197 LUT, 118 FF, 14 CARRY4), reproduced exactly:

   | Setting | Cost |
   |---|---|
   | head at the default | +48 LUT, +30 FF, +7 CARRY4 (245 / 148 / 21) |
   | head at 1 | +51 LUT, +4 FF |
   | head at 2^31-1 | +69 LUT, +34 FF, +8 CARRY4 |
   | round-1 head at the default | +60 LUT, +30 FF |

   The pause adds no flip-flop.

### The merge (round 2b)

- **Re-derived.** `git merge-tree` of `c26b14b3` and `631eeb34` conflicts only in `09_verification.md`. Its automerge of `07_memory_maps.md` equals the head's blob.
- **Every one-sided file equals its parent.** Against the merge base `2ebd4fe8`, every file only the lane changed equals `c26b14b3`, and every file only main changed equals `631eeb34`.
- **09's one conflict, §8.2's closing paragraph, keeps both sides:**
  - main's D3C row, its 87-control count, and its `aecp_dispatch_mutants.py` `d3` sentence;
  - the lane's "the port's own deadline, resets and handshake models are §8.5's", which replaces the base's "#18, #19 and #21 are not closed by this evidence".
  - §8.5 keeps its number; main ends at §8.4.
- **No RTL change.** `git diff c26b14b3 c0715410 -- hdl` is main's `gen_ucode.py` comment alone.
- **No cited line moved.** Every `KL_pp_nvm_port.sv:NNN` citation in the tree still points at its text (`:33-34`, `:233-244`, `:319-323`, `:415-418`). `09_verification.md:56` is unchanged.
- **The suites that read merged files are green:** `pp_top` 9,168, `acmp_nvm` 388, `nvm_port` 686, the figures gate, and the docs gates.

## Reviewer plants in the pause logic

Each plant edits one copy of the port; every anchor occurs exactly once. Each runs:
- the PR's suite at 100 under the pristine, coincident, unsolicited and lazy-erase models;
- the reviewer fuzz, at 37 and at 3: legal, silent and resume modes, 3 seeds × 600 operations.

Cells are fails of 343. Fuzz cells are legal/silent/resume fails.

| Plant | Defect | Suite (4 models) | Fuzz 37 | Fuzz 3 |
|---|---|---|---|---|
| **Q1** | `S_WEWAIT`'s latched cycle still owes | **0, 0, 0, 0** | 456/420/105 | 567/557/136 |
| Q2 | `S_RHWAIT`'s latched cycle still owes | 0, **5** (RW4, T24), 0, 0 | 435/105/26 | 564/111/28 |
| Q3 | `S_WWAIT`'s latched cycle still owes | 0 everywhere | 0 | 0 (equivalent) |
| Q4 | `S_RPWAIT`'s latched cycle still owes | 0 everywhere | 0 | 0 (equivalent) |
| Q5 | the count runs on cycles that owe nothing | 14 (RW4, T24, T29a, T29b) | 3172/2085/252 | 4043/2861/360 |
| Q6 | a dropped `rready` clears the count | 2 (RW1, T29a) | 0/531/0 | 0/278/0 |
| Q7 | a dropped `wvalid` clears the count | 2 (RW1, T29b) | 0/586/0 | 0/303/0 |
| Q8 | `S_WHDR` and `S_RHFWD` clear the count | 0 everywhere | 0 | 0 (equivalent) |
| **Q9** | the verdict may land on a paused cycle | **0, 0, 0, 0** | 63/161/12 | 1002/270/83 |
| Q10 | zeroed in `S_FIN`, not `S_IDLE` | 0 everywhere | 0 | 0 (equivalent) |
| D24, D25, D26, D20, D21 (calibration) | the gate's own rows | 3; 7; 0 pristine and 5 coincident; 1; 1, as the gate records | all detected | all detected |
| pristine | none | 0 | 0 | 0 |

## Findings

### F1 - MINOR - Tests, Docs

**Two non-equivalent defects in round 2's pause logic pass all 343 checks under every model, and the figures gate.** Each one refuses a contract-legal device with DEADLINE.

- **Where:**
  - The RTL:
    - the latched-terminal term at `hdl/packet_engine/KL_pp_nvm_port.sv:258-260` (its `S_WEWAIT` member);
    - the verdict `assign dl_w = owe_w && !prog_w && tmo_hit_w;` at `:276`.
  - The checks that leave them unpinned:
    - T29 at `tb/nvm_port/sim_main.cpp:2105-2134` (drop phase `cycles % (TMO / 2)`);
    - T24's `S_WWREQ` arm at `:1845`, whose ERASE completes normally;
    - T21's ERASE answered on its grant, followed by a WRITE grant far inside the deadline (the README's own D26 note);
    - the D26 rows at `tb/nvm_port/measure_figures.py:412-417` and `README.md:594-603`.
  - The coverage claims: `docs/architecture/09_verification.md:307` maps "a clock in which the device owes nothing pauses the count … and a wait state consuming a latched done owes nothing" to T29, D24, D25 and D26 under the coincident model. Also `README.md:464-466` and `:526-534`.
- **Authority:**
  - The port banner, `KL_pp_nvm_port.sv:69-83`: a cycle that owes nothing "PAUSES the count", and the operation ends only "On the (MEM_TIMEOUT_CYC_P + 1)-th owed cycle without its event".
  - `:33-34`: "backends without erase semantics answer ERASE with done at once".
  - 02 §8, `02_interfaces.md:533-541` ("unless that terminal is already latched"; a clock owing nothing "pauses the count").
  - F08.1, `08_timing.md:46`.
  - The suite's own boundary convention: an event `TMO` silent cycles late is tolerated (T24, `sim_main.cpp:1857-1862`).
  - The round-2 assignment, item 4, and this review's focus: no contract-legal model or manager pattern may falsely trip the count.
  - The R436-1 F1 precedent: a planted defect the suite passes is a test gap of this severity.
- **Evidence:**
  - **Q1** (`S_WEWAIT` dropped from the exemption):
    - 0 of 343 under the pristine, coincident, unsolicited and lazy-erase models;
    - legal-mode fuzz: 456 false DEADLINEs at 37 and 567 at 3, against 0 at the head;
    - a trace shows the mechanism: an ERASE done on its own grant, then the WRITE's grant exactly TMO cycles after its request, refused because the latched `S_WEWAIT` cycle counted;
    - directed check R436d (that exact device): passes at the head (347 + 347) and fails under Q1.
  - **Q9** (`dl_w = !prog_w && tmo_hit_w && state is neither S_IDLE nor S_FIN`):
    - 0 of 343 under all four models;
    - legal-mode fuzz: 63 false DEADLINEs at 37 and 1,002 at 3;
    - directed check R436e: a withheld payload byte presented on the (TMO + 1)-th owed cycle, with the manager dropping `rready` on the one cycle the count sat at its bound. It passes at the head and fails under Q9 alone;
    - its control R436f, one owed cycle later, gives DEADLINE at the head, which shows R436e sits at the boundary.

  Receipts: `receipts/plants/`, `receipts/directed/SUMMARY.txt`; scripts `scripts/plant.py`, `scripts/directed.py`, `scripts/pause_fuzz.cpp`.
- **Impact:**
  - Today's RTL is right.
  - Either regression would ship green through `run_suites.sh` and through the figures gate.
  - On a board, the regressions refuse legal backends:
    - Q1 refuses a backend without erase semantics (the banner's own example) whose WRITE grant comes late;
    - Q9 refuses any device answering near its bound while the manager holds a strobe.
  - The managers turn either refusal into failed walks and write attempts, and then `nvm_alarm_o`.
  - 09 §8.5 lists both properties as graded.
- **Required outcome:**
  - Add standing checks that kill Q1 and Q9, each naming its property. Two examples:
    - an ERASE answered on its grant, then a WRITE grant exactly `TMO` cycles after the request, served (R436d);
    - a byte on the (`TMO` + 1)-th owed cycle with the manager holding on the cycle the count reaches its bound, served, plus its one-cycle-later DEADLINE control (R436e/f).

    The templates are in `scripts/directed.py`. Alternatively, phase-align a T29 drop to the bound cycle and add an ERASE-on-grant variant of T24's `S_WWREQ` boundary arm.
  - Record Q1 and Q9 as figures-gate mutation rows.
  - Keep the README and the 09 §8.5 counts in step.
- **Verification:**
  - Q1 and Q9 each fail a named check.
  - The head stays 343+n/0 under every contract-legal model at both bounds, with the RW checks passing under all nine.
  - `make -C tb/nvm_port figures` gives rc 0.
  - The re-review re-runs `scripts/plant.py --only Q1-wewait-latched-owes,Q9-verdict-on-paused-cycle` unchanged.

### S1 - SUGGESTION - Robustness

**An over-length owed drain holds a waiting request off for ever.**

- **Where:** `KL_pp_nvm_port.sv:589` (`dev_rready_o` includes `owed_r && owed_rd_r`) and `:271`, where every drained byte is progress.
- **Evidence:**
  - A backend keeps presenting bytes past an abandoned READ's length, one every `TMO` / 2 cycles, and never ends the command.
  - It restarts the count of the request waiting on it every time.
  - Reviewer fuzz, babble mode: none of 132-150 waiting requests per bound was answered within 400·`TMO` cycles, at 1, 2, 3, 37 and 100 (`receipts/fuzz_head/babble_*`).
- **Why only a suggestion:**
  - Such a backend is broken: a READ owes at most its length.
  - It is outside #15's silent-device scope.
  - In normal operations the port never takes more than the length it requested.
- **Suggested change:** either:
  - track the abandoned READ's remaining length, so that after its last byte only the terminal is progress (a 16-bit count); or
  - state the limit beside the banner's "takes and discards the bytes of an owed READ" and in 02 §8.

### R1 - RESIDUE - Docs (wording only)

`tb/nvm_port/README.md:470-471` reads "T24 T28 and T29 grade all of it", with the comma missing. The PR body's Round 2 item 3 says this sentence now reads "T24, T28 and T29".

**Exact fix:** "… as its end. T24, T28 and T29 grade all of it at `TMO` = 100, …".

### R2 - RESIDUE - Docs (wording only)

T29's withheld bytes are named by ordinal, one too low. The harness withholds index 10 and index 20 (`sim_main.cpp:2111`, `:2123`): ten payload bytes, and twenty WRITE bytes (`sent.size() == 20`), move first.

**Exact fix:**
- In `tb/nvm_port/README.md:529-530`, "never presents the payload READ's 10th byte" becomes "never presents the payload READ's 11th byte", and "never takes the WRITE's 20th" becomes "never takes the WRITE's 21st".
- Make the same two replacements in the PR body's Round 2 item 4 ("Graded by T29").

## Issue-by-issue acceptance at this head

| Issue | Item | Status | Evidence |
|---|---|---|---|
| #15 | 1. One `err` within a bounded time | MET | T24 in twelve states; T29 under manager drops; fuzz silent mode exact at 1-100 |
| #15 | 2. Busy low; next request served (ruling (c)) | MET | T24 served and DEADLINE branches; T28a-e; resume fuzz served iff r <= TMO |
| #15 | 3. Parameter named as class E | MET | `MEM_TIMEOUT_CYC_P`; `NVM_MEM_TMO_CYC_P = CLK_HZ_P`; elaboration guard |
| #15 | 4. Silent-device standing model | MET | silent 115/228 at 100 and at 37; RW checks pass |
| #18 | 1-3 | MET | unchanged since round 1 (T25; `tb/acmp_nvm` R; the README wording); `acmp_nvm` 388 |
| #19 | 1-3 | MET | M2-lo, M7, the latch rows, M8 and the model rows; figures gate agrees |
| #20 | 1-3 | MET | `acmp_nvm` 388 (N1a-d, N12a-e, A2/F4/G2 green) |
| #21 | 1-3 | MET | four handshake models; their mutation rows agree |
| #21 | 4. Existing checks green under every required model | **MET** (was NOT MET) | seven legal models 343/0 at 100 and at 37 |

F1 is a test-coverage gap in round 2's own logic. It does not unmeet any issue's acceptance item, but it leaves the PR's coverage claim for the pause short.

## Lens results

### Conformance (CLEAN)

- The ruling (5952386396) and the round-2 assignment are followed:
  - the pause, as assigned in item 4;
  - no port, and no parameter beyond the ruled two;
  - containment of the abandoned WRITE;
  - nothing released by time.
- #21 now closes legitimately.
- Both parent patches are unchanged (sha256 verified), and so is the banner sentence the p2 patch relies on.
- The merge follows 5959104191: it is `--no-ff`, keeps both sides, keeps §8.5's number, and changes no RTL.

### RTL (CLEAN)

- I read the whole round-2 hunk, and the count, pause, verdict and owed logic in full.
- The second term exempts one cycle at most: a latched wait state always leaves on that cycle.
- D23's guards are redundant by invariant.
- No new register; cost reproduced exactly.
- Lint is clean over 41 modules; the elaboration guard holds.

### Robustness (CLEAN; S1 advisory)

- No false trip of a contract-legal device and no manager-pattern starvation at five bounds.
- Strays and owed terminals behave as specified.
- The only hold-off left is a broken over-length drain (S1), or a manager that never presents its strobe.

### Tests (UNCLEAN: F1)

- 343 checks in each of two builds; 88 figures builds agree.
- Every round-1 probe is killed by a named check.
- Q1 and Q9 survive every model.

### Docs (UNCLEAN: F1's coverage claim at 09 §8.5:307; R1, R2 residue)

These read consistently with the RTL:
- the banner, 02 §8, F08.1, the integrator row and the top comment;
- the README's D18-D26 and "Two bounds" text;
- 09 §8.2's merged paragraph.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #15 body and comments 5355168983, 5355231359, 5573417155, 5951891343, 5952358239, 5952386396, 5955151206, 5956438390, 5959067531, 5959104191, 5960259376; acceptance of #18-#21; PR body (Rounds 2 and 2b); author-r2b packet and both parent patches (sha256); merge resolution | R436-2 | c0715410418b47ffaccf5feed55b71617fcfaf82 |
| RTL | CLEAN | `KL_pp_nvm_port.sv` (full, round-2 hunk traced), `protocol_processor_top.sv` comment, merge `hdl` diff (ucode comment only); lint 41; OOC at default, 1 and 2^31-1 and round-1 | R436-2 | c0715410418b47ffaccf5feed55b71617fcfaf82 |
| Robustness | CLEAN (S1 advisory) | pause, latched term, verdict, owed command, drain, late grant; 10 own plants plus 5 calibration rows; randomized harness at 1, 2, 3, 37 and 100 in 4 modes; D23 invariant | R436-2 | c0715410418b47ffaccf5feed55b71617fcfaf82 |
| Tests | UNCLEAN (F1) | `tb/nvm_port` (`sim_main.cpp` T1, T24, T28, T29 and the TMO derivation; Makefile; `measure_figures.py`; README); figures gate 88 builds; models at 37; round-1 probes W6, W15, W15b, W16, X12, X17, X18, X24, X24b and X20; directed R436d-f; `tb/acmp_nvm` 388; `tb/pp_top` 9,168 | R436-2 | c0715410418b47ffaccf5feed55b71617fcfaf82 |
| Docs | UNCLEAN (F1); R1, R2 residue | 02 §8, 08 F08.1, 09 §8.2 and §8.5, integrator guide, top comment, `tb/nvm_port` README, PR body; `make check`, `gen_matrix.py --check` | R436-2 | c0715410418b47ffaccf5feed55b71617fcfaf82 |

## Real limits

- **Not run here:**
  - the full `run_suites.sh` bank;
  - the five CI mutation campaigns;
  - `d3_mutants.py`, `aecp-dispatch-mutants` and the other round-2b campaigns, whose launch was not permitted in this session;
  - `syn/yosys/run.sh`;
  - the donor bank and the parent consumer set.

  For those I rely on the PR body's round-2b table and on the manager's public evidence. I ran only the suites the delta and the merge touch (`nvm_port`, `acmp_nvm`, `pp_top`), lint, the docs gates and the figures gate.
- **Hosted CI.** `suites` was still in progress at my snapshot. `docs-gates` and `portability` had succeeded. The manager owns hosted and act acceptance.
- **The randomized harness is a model.** It uses fixed seeds and covers what its device and manager generate; it is not a proof. D23's equivalence is shown by an invariant monitor and an inductive argument, not by a formal tool.
- **Cost instrument.** The out-of-context cost is sv2v plus Yosys `synth_xilinx`, not a Vivado report.
- **Redaction.** Home-directory prefixes in raw receipts are redacted to `$HOME`. The wrapper's sha256 in `verilator_identity.txt` was taken before that redaction.
- **Clone cleanup.** Two untracked artifacts that my own runs created in the clone (`abc.history` and `tb/nvm_port/__pycache__`) were removed before the final integrity check.
- **Hardware.** Physical calibration NOT RUN. No hardware. Field skips are not hardware proof.

## Pending manager duties

- Run the donor bank (9) and the parent consumer set (16) at dev `cdf49d1a`, with `parent-adoption-c4c6-ea3fb388.patch` and then `parent-adoption-p2-cdf49d1a.patch`, both unchanged.
- Build the final current-dev candidate at the merge turn (source base `631eeb342ca1e3fa80e734077a56a943aee76ff1`, live dev `cdf49d1a28527562888f0a903de51b6b15b1244f`).
- Hosted and act acceptance at the exact head, distinguishing executed jobs from skipped contexts.
- Own the evidence for the round-2b campaigns (`d3_mutants.py` 87 of 87, `aecp-dispatch-mutants` 37 of 37, and the rest of the PR body's table).
- Route F1 to the author. Re-review the fix head:
  - re-run `scripts/plant.py --only Q1-wewait-latched-owes,Q9-verdict-on-paused-cycle` and `scripts/directed.py` unchanged;
  - re-run the figures gate.
- Carry R1 and R2, and R437-1's retained R2-R5, to the residue checklist. Keep R437-1 S2 (X20) and S1 here as open suggestions.

R436-2 FINISHED
