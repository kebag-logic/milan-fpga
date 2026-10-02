[R437] NEGATIVE - exact head 70bf017d62d60b4401126c7b1bb087f4cb115c5a

# R437-1: external review of PR #145 (lane P2, NVM port robustness)

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan
- **Issues:** #15, #18, #19, #20 and #21. The PR body closes all five.
- **Head and base:** head `70bf017d62d60b4401126c7b1bb087f4cb115c5a`, tree `529d9a3779fe8503fd5c7c9798df16c2df11a689`. Base `main` `2ebd4fe8d31e88c44559e934bd624e1c50515ad5`.
- **Clone:** an isolated, detached clone. After every probe it was verified byte-exact at the head: worktree, index, modes and `write-tree` all equal `529d9a37`, and the repository has no gitlinks.
- **Verdict:** NEGATIVE.
  - Two MINOR findings are open (F1, F2), so three lenses are unclean: Conformance, Tests and Docs.
  - The RTL lens and the Robustness lens are clean. I found no RTL defect. Every planted defect that survived the suite was a gap in the tests, not in the port.

## 1. What I reconstructed, and in what order

1. **Repository rules.** The repo has no AGENTS.md or CONTRIBUTING.md. I used README.md, `docs/README.md` (the single-source rules: values only in F01.5 and F08.1) and the `hdl/README` rules where they are cited.
2. **Scope.** I read the five issue bodies and these scope comments:
   - on #15: 5355168983 (bound every device wait), 5355231359 (reachability), 5951891343 (the assignment), 5952358239 (the author's STOP), 5952386396 (the manager's ruling) and 5955151206 (review ready);
   - on #18: 5355176017 (narrowed to naming plus a reset phase; the crc16 belongs to the manager);
   - on #19: 5355175775 (#21 extracted).
3. **Authorities.**
   - In this repository: 02 §8 and §8.2 (`docs/architecture/02_interfaces.md:501-627`), 07 §5.3 (`:636-650`, `:698`), 08 §2 (`:43-46`, `:63-100`), F01.5 (`01_overview.md:176-179`), the integrator guide (`:96`, `:357`), 09 §8.5, the port banner (`KL_pp_nvm_port.sv:42-107`) and the line the `tb/nvm_port` README draws between a contract freedom and a broken backend (`README.md:582-608`, `:788-818`).
   - In the parent at dev `cdf49d1a`: `KL_nvm_backend.sv` (the 50 ms `T_HOLD_MS_P` hold at `:119-145`; the registered grant at `:851` and `:896`; `done_r` raised in `S_FIN` at `:1024`, one cycle after the final byte moves), `KL_pp_shadow.sv:997-1105`, and `docs/design/SAVED_STATE_MATERIALIZATION.md`.
4. **The change.** `git diff 2ebd4fe8..70bf017d`: 20 files, five commits.
5. **Public evidence.** milan-fpga `d56e2227` `review-evidence/ppP2-r1`:
   - MANIFEST.json, PR-BODY, STOP-COMMENT and both parent patches;
   - their hashes match the MANIFEST (`receipts/parent_patch_check.txt`);
   - the p2 patch is 9,728 bytes, sha256 `3dda8509…d08b`, as the author stated.
6. **Prior review findings on this PR.** None existed when this review started. The only PR comments were the two review-start notices (5955490074, 5955490954). There were no reviews and no review comments. Nothing therefore needs resolving or retaining.

## 2. Executed evidence

All of it ran at the exact head on scoped Verilator 5.050 (identity in `receipts/toolchain.txt`).

| Run | rc | Result |
|---|---:|---|
| `tb/nvm_port` `make` (the elab guard, then the suite) | 0 | 326/326. The guard refuses 0, 2^31 and 2^32-1 by name and builds 1 and 2^31-1 clean |
| `tb/acmp_nvm` `make` (two builds) | 0 | 372 + 16 = 388/388 |
| `make -C tb/nvm_port figures` | 0 | 76 builds: 1 + 12 arms + 49 mutations + 9 models + 5 matrix. Every figure agrees (`receipts/figures.log`) |
| `make check` (disposable local clone) | 0 | 41 mermaid + 18 WaveDrom blocks; 1,045 links; matrices; parameters 28 = 28 = 28 |
| Lint (`lint_hdl.sh` flags) of `KL_pp_nvm_port`, `KL_pp_nvm_mgr_arb` and `protocol_processor_top` | 0 | Clean. The top is clean at `NVM_MEM_TMO_CYC_P` = 1, 64 and 2^31-1, and refuses 0 by name |
| Out-of-context synthesis (sv2v, then `synth_xilinx` xc7) | 0 | Base: 197 LUT, 118 FF, 14 CARRY4. See the cost lines below the table |
| Probe set 1: 29 planted defects and behaviour probes | – | `receipts/probes1/SUMMARY.txt` |
| Probe set 2: directed proofs for the survivors | – | `receipts/probes2/` |
| Probe set 3: #19's and #21's mutations, the models, and the acmp_nvm planted defects | – | `receipts/probes3/SUMMARY.txt` |
| Parent patch apply check at dev `cdf49d1a` | 0 | See section 4.6 |

The out-of-context cost of `KL_pp_nvm_port`, against the base's 197 LUT and 118 FF:

- **At the default:** +60 LUT, +30 FF, +7 CARRY4.
- **At 1, the smallest legal value:** +52 LUT, +4 FF.
- **At 2^31-1, the largest:** +47 LUT, +34 FF.

The default and the smallest value reproduce the author's figures exactly.

Hosted CI at the exact head, snapshot at 15:37Z (`receipts/hosted_checks_snapshot.txt`):

- `docs-gates` and `portability` succeeded on both the push run and the PR run.
- `suites` was still in progress on both.

The manager owns hosted acceptance.

## 3. Findings

### F1 - MINOR - Conformance, Tests: #21's criterion 4 is not met, but the PR closes #21

- **Where:**
  - `tb/nvm_port/sim_main.cpp:888`: `CHECK(h.store[3][f1.size()] == 0xFF, "T1 erase visible past the record")`;
  - `tb/nvm_port/README.md:822-831` and `:883-884`;
  - the PR body: "Closes #21" and "Lazy erase's single FAIL is the pre-existing T1".
- **Authority:**
  - #21 acceptance item 4: "The existing 83 checks stay green under every model the port is contractually required to tolerate."
  - Lazy erase is such a model. The port's own banner grants it (`KL_pp_nvm_port.sv:33-34`: "backends without erase semantics answer ERASE with done at once"). The README classifies it as a freedom, not a broken backend (`README.md:811-818`).
  - The assignment (5951891343): "The PR closes each issue whose acceptance it meets in full, and relates to the rest."
- **Evidence:**
  - Under the lazy-erase model with the RTL untouched, the suite gives 325/326, and the only failure is `T1 erase visible past the record` (`receipts/probes3/MOD-lazy.log`). The figures gate reproduces both lazy rows.
  - T1 is one of the original checks.
  - The check reads the device model's array after a device `done`. That is a backend side effect, as the README itself says.
  - The port behaviour T1 is there to pin is already pinned on the bus by `T1 op0 = ERASE region 3 len 0` and `T1 erase pulsed region 3 once`.
- **On the author's call:** naming T1 as "the one known exception" records the gap. It does not meet the criterion.
- **Impact:** #21 is closed with one acceptance item unmet, and a check that tests the harness, not the port, stays red under a model the port must tolerate.
- **Required outcome:** one of these two.
  - (a) Make the T1 array check model-independent: drop it, condition it on a model with erase semantics, or restate it on the bus. Then both lazy rows read 326 PASS, 0 FAIL, and the README and the figures gate follow.
  - (b) Change "Closes #21" to "Relates to #21", with a public ruling that amends item 4.
- **Verification:** `make -C tb/nvm_port figures` gives rc 0 with the lazy and lazy + page-buffered rows at 0 FAIL, or the PR body and the ruling are published.

### F2 - MINOR - Tests, Docs: four owed-command and watchdog properties are not pinned

The PR claims these properties are graded, but no check covers them.

- **Where:**
  - `tb/nvm_port/sim_main.cpp:1793-2051` (T24);
  - the claim at `tb/nvm_port/README.md:452-458` ("Every grant, byte and terminal restarts the count … takes the device's next done or err as its end. T24 grades all of it");
  - `docs/architecture/09_verification.md` §8.5 ("the abandoned command stays owed … | T24 …; D9-D17").
- **Authority:**
  - 02 §8 (`02_interfaces.md:536-546`): every grant, byte and terminal restarts the count; the owed command's terminal is "credited to no operation"; a deadline in any accepted command leaves it owed.
  - The port banner, `KL_pp_nvm_port.sv:75-99`.
- **Evidence:** I planted defects in the watchdog and owed-command logic (`scripts/probes_set1.py`). Four leave all 326 checks green: X12, X17, X18 and X24.
  - Each one is a real change of behaviour, not an equivalent mutant.
  - For each, a directed probe (`scripts/probes_set2.py`) passes on the head RTL and fails on the mutant (`receipts/probes2/`).

  | Defect | Mutation | Directed probe: head / mutant |
  |---|---|---|
  | **X18** | Drained bytes of an owed READ are not progress (`prog_w` read term `&& !owed_r`, `:271`) | A restore blocked on an owed READ that drains one byte every 60 cycles. Head: served byte-exact. Mutant: err DEADLINE while the device is moving (`Q18-*`) |
  | **X17** | The owed command's `done` is not progress (`:268`, `|| owed_r` removed) | An owed ERASE's done arrives about 60 cycles into a waiting restore, then a legal 60-cycle grant. Head: served. Mutant: DEADLINE (`Q17-*`, round 2) |
  | **X24** | `S_RHREQ`'s `if (!owed_r)` guard removed (`:426`; all four guards removed is also green) | An owed ERASE ends in err while a restore waits. Head: the err is credited to no operation and the restore is served. Mutant: the restore ends err DEVICE, the owed command's err misattributed (`Q24-*`, round 2) |
  | **X12** | A deadline in `S_WWAIT` leaves nothing owed (`:300`) | A WRITE whose done comes three deadlines late, then a commit. Head: no request over it. Mutant: 101 request cycles into a busy device, so RW3 fails (`Q12-*`) |

  - A fifth survivor, **X20**, is minor: a late grant that carries `err` is made owed. No harness backend presents a grant and an err in the same cycle. See S2.
  - For contrast, these planted defects are killed: X01, X02, X03, X05, X10, X11, X14 (by `elab_bounds`), X15 (by `elab_bounds` at 1), X16, X21, X26, X27 and X28.
  - These are equivalent, as expected: X22 (count not reset), X23 (late-grant flag not reset) and X25 (no saturation).
- **Impact:** the RTL is correct today. Probes against the head RTL show the right behaviour in all four cases. But the drain-as-progress, owed-terminal-as-progress, attribution and owed-after-`S_WWAIT` properties can regress with the suite and its figures gate green. The README and 09 §8.5 claim T24 grades them. The assignment names "drained READ bytes" explicitly.
- **Required outcome:**
  - Add checks that kill X12, X17, X18 and X24, each with a message naming the property. The four directed probes are ready templates.
  - Add the four as figures-gate mutation rows.
  - Correct the README and 09 §8.5 counts.
- **Verification:**
  - Each of the four mutants reddens a named check.
  - The pristine RTL stays 326+n/0 under every contract-legal model, and the RW checks pass under all nine.
  - `make -C tb/nvm_port figures` gives rc 0.

### S1 - SUGGESTION - RTL, Robustness: a manager that toggles its strobe defeats the bound

- **Where:** `KL_pp_nvm_port.sv:262-263` and `:278-282`. The count clears on any cycle that owes nothing (`!owe_w`).
- **Evidence:** a reviewer phase (`P1-manager-toggle`, `receipts/probes1/P1-manager-toggle.log`):
  - The device withholds a payload READ byte for ever while the manager drops `rready` for one cycle in every 50. The port never answers: `run_op` gives up after 100,000 cycles (rc -1).
  - The same happens on the commit side when `wvalid` drops one cycle in 50.
- **Why only a suggestion:**
  - No in-tree driver of the manager face does this. Its strobes are state-level and steady through each data phase:
    - `KL_acmp_nvm_shadow.sv:963`, `:966`;
    - `KL_aecp_nvm_writer.sv:1092`, `:1094`;
    - `KL_pp_nvm_mgr_arb.sv:178-182`, where the drain holds `rready`.
  - The STOP said "the counter clears on any cycle the port is not waiting on the device", and the ruling accepted the design. 02 §8 says "in a row".
- **Suggested change:** either hold the count on a non-owed cycle instead of clearing it, or state the manager-face obligation (`rready` and `wvalid`, once raised in a data phase, are not dropped without a handshake) beside 02 §8's deadline paragraph.

### S2 - SUGGESTION - Tests: a late grant that carries `err` is untested

- **Where:** the `!dev_err_i` term of the late-grant path, `KL_pp_nvm_port.sv:302`.
- **Evidence:** X20 survives (`receipts/probes1/X20-late-gnt-err-owed.log`).
- **Suggested change:** arm a harness backend that presents grant and err in the same cycle after a request-state deadline, if the contract allows it. Otherwise state that it does not.

### RESIDUE (wording only)

None of these changes a figure, a check or the code.

- **R1.** `tb/nvm_port/README.md:794`: "and \"The handshake models\" below has the other three". That section is above, at `:582`, so replace "below" with "above".
- **R2.** `tb/nvm_port/README.md:801-802` and `:807-808`.
  - Replace "it is the only model here that varies the handshake for EVERY phase rather than at one armed moment" with "it was the first model here to vary the handshake for a whole run". Unsolicited, short read and silent are now whole-run models too.
  - Replace "The four array-flavoured models: this one, which keeps every accepted byte" with "The four array-flavoured models: the pristine model, which keeps every accepted byte".
- **R3.** `tb/nvm_port/sim_main.cpp:1082` ("Cut the power inside the WRITE") and `:1169` ("a power cut while writing one"). Both sit in the device-err phases T15 and T16. Use "A device err inside the WRITE leaves …" and "a commit torn while writing one …", in line with #18's naming and the `:1081` header.
- **R4.** `hdl/acmp/KL_acmp_nvm_shadow.sv:208` and `hdl/aecp/KL_aecp_nvm_writer.sv:260` port comments read "1 DEVICE, 2 UNFRAMED". Append ", 3 DEADLINE (read as DEVICE)". Cause 3 is now produced (02 §8).
- **R5.** Parent `docs/design/SAVED_STATE_MATERIALIZATION.md:1930` (line number after both patches) still cites "processor issue 15's open recovery contract", while the patched §15 item 4 now reads AMENDED. Replace it with "section 15 item 4 (amended)", ideally in `parent-adoption-p2-cdf49d1a.patch`.

## 4. Judgement by assignment item

### 4.1 The watchdog

**Can a contractually valid slow device trip it?** No.

- Every grant, byte (the owed drain included) and terminal clears the count (`:267-271`, `:280`).
- T24's slow device, with every event `TMO` late over more than 40·`TMO` cycles, is served.
- At the default, the parent backend's longest legal stall is 50 ms. The bound is 1,000 ms (`KL_nvm_backend.sv:119-145`; `T_HOLD_MS_P` = 50 is the default and `KL_pp_shadow.sv:997-1007` does not override it). The derivation is stated in F01.5, F08.1 and the integrator guide, as ruled.
- The parent backend raises `done` one cycle after the final byte (`S_FIN`), so refusal (d) never refuses it.

**Can a stalled manager trip it?** No.

- `owe_w` excludes `S_WHDR`, `S_RHFWD` and a manager stall in either pump (`:258-263`).
- T24 stalls the manager three deadlines on every byte and is never charged. D5 and D6 are killed.

**Can an owed event be missed so the port wedges?**

- I found no path with the in-tree managers. The verdict needs `!prog_w`, so a grant, byte or terminal in the deadline cycle always wins.
- The owed state is cleared by the device's own terminal in any state (`:298-299`), or by reset.
- A request blocked on an owed command keeps counting (`owe_w` includes `req_st_w`; X16 is killed). So no request waits for ever.
- The one wedge I found needs a manager that toggles its strobe (S1).

**The late registered grant.** `lg_r` (`:296`, `:302`) matches the parent's registered `gnt_r`. T24's four request arms see `late_gnts == 1`, and D10 and D11 are killed.

**Drained READ bytes.**

- `dev_rready_o` includes `owed_r && owed_rd_r` (`:589`), and drained bytes are progress.
- The drain is correct on the head RTL (Q18 on the head passes), but it is unpinned (F2).
- D15 and D16 (drain off, kind overwritten) are killed.

**Reset.** Every new register resets. X21 (owed survives reset) is killed. X22 and X23 are equivalent.

**Elaboration refusal.**

- The port refuses 0, 2^31 and 2^32-1 by name and builds 1 and 2^31-1 (`elab_bounds.sh`). The top refuses 0 by name.
- A guard off-by-one (X14) and a counter one bit narrow (X15) are both killed by the guard script.

### 4.2 Short commands

Refusal (d) holds in all four data phases (`:387-390`, `:404-408`, `:446-451`, `:496-500`):

- T27 covers a to f, and T23c the header;
- S1 to S4 and M8 are killed.

A completion on the final byte's own edge stays legal: T22 passes, and so does the coincident model, 326/326.

### 4.3 The four handshake models

**Each model is justified against the contract:**

| Model | Class | Grounds |
|---|---|---|
| Unsolicited completion | freedom | refusal (c), `:52-62` |
| Coincident completion | freedom | the latch, `:319-323` |
| Short read | broken backend | refusal (d), `:63-67` |
| Silent | broken backend | the deadline, `:69-107` |

**#21's four mutations, each under its model:**

| Mutation | Model | Fails of 326 | A failing check that names the mechanism |
|---|---|---:|---|
| M6 | unsolicited | 222 | "T19a … the stray done was not consumed as the ERASE's" |
| The latch deleted | coincident | 200 | "T21/T22a-c the sticky done_seen_r latch" |
| M8 | short | 146 | "T23 c the short-read defence"; RW6 |
| D1 | silent | 267 | RW1 "every operation … was answered" (189 wedged); RW7 |

**#19's four, on the pristine model:**

| Mutation | Fails of 326 | Named by |
|---|---:|---|
| The low magic byte | 5 | T26a/b "the LOW magic byte" |
| The payload bound weakened to `<` | 4 | T26c/d "the payload bound's legal edge" |
| The latch deleted, both ways | 21 | T21/T22 |
| The short-read defence off | 22 | T23c |

**The original checks under every contract-legal model:**

- Green under pristine, half-page, page-buffered, coincident and unsolicited: 326/0.
- Not green under lazy erase or lazy + page-buffered: T1 (F1).

### 4.4 #18's resets

- T25 resets port and device together at six stages named on the bus (a to f). After the release it pins the port idle and silent: no pulse, no request, no byte.
- It then checks that the neighbour restores byte-exact, that the next commit is byte-exact, and that the torn record is refused at its header or forwarded whole and refused by the crc16.
- Two more resets hit the port alone (T25g/h).
- The crc16's ownership on the real binding manager is shown: with `rrec_ok_w`'s crc term forced true, R2 fails, along with F5, F10, F14 and F15 (`ACMP-A4`, which reproduces the README's claim).

### 4.5 #20

- Main's proof holds: the reintroduced #20 defect (`ACMP-A5`) fails N1a-d and 12 checks in all.
- N12 holds as the README claims:
  - a zero-byte DEADLINE read as blank fails N12a and N12d (`A1`);
  - the port's deadline removed fails N12a-d (`A2`);
  - a deadline that leaves nothing owed fails N12c (`A3`);
  - the first build stays green under all three.
- The blank first boot is unchanged (N12e). A2, F4 and G2 are green.

### 4.6 The parent patch

- `parent-adoption-p2-cdf49d1a.patch` changes one file only, `docs/design/SAVED_STATE_MATERIALIZATION.md` (+44 -19).
- At dev `cdf49d1a` the file's blob is `21dc772`, matching the patch's index line. The patch applies cleanly after `parent-adoption-c4c6-ea3fb388.patch` and gives blob `6021944`.
- It amends W13, §8.8 and §15 item 4 as ruled: three failed attempts, `nvm_alarm`, `nvm_backed` revoked, the pending bit dropped, and quarantine never released by time alone. It also amends §6.4 and the stage release notes for consistency.
- It contains no gate change and no RTL change. One stale label remains (R5).

### 4.7 Each issue against its own acceptance list

| Issue | Met? | Notes |
|---|---|---|
| #15 | Met | One bounded err, DEADLINE. Busy is low at the pulse, and both branches of "serves the next request" are graded as ruled. `MEM_TIMEOUT_CYC_P`, class E's name and idiom. The silent model is a standing variant. Caveat S1 |
| #18 | Met | All three items |
| #19 | Met | All three items |
| #20 | Met | All three items |
| #21 | Not met | Items 1 to 3 are met. Item 4 is not, because of F1 |

## 5. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | The five issues' acceptance lists; the assignment, STOP and ruling; 02 §8/§8.2, 07 §5.3, 08 §2, F01.5, F08.1; the parent backend, shadow and saved-state page; both patches | R437-1 | 70bf017d62d60b4401126c7b1bb087f4cb115c5a |
| RTL | CLEAN | `KL_pp_nvm_port.sv` (full read), `KL_pp_nvm_mgr_arb.sv`, `protocol_processor_top.sv` diff; the managers' cause handling (`KL_acmp_nvm_shadow.sv:575-609`, `KL_aecp_nvm_writer.sv:470-480`); lint; out-of-context synthesis at 1, the default and 2^31-1 | R437-1 | 70bf017d62d60b4401126c7b1bb087f4cb115c5a |
| Robustness | CLEAN (S1 is a suggestion) | Watchdog, owed, drain, late grant, reset and elab guard, each probed (29 planted defects or behaviour probes, 8 directed); slow and stalled cases; port-only resets | R437-1 | 70bf017d62d60b4401126c7b1bb087f4cb115c5a |
| Tests | UNCLEAN (F1, F2) | `tb/nvm_port` (326), `tb/acmp_nvm` (388), the figures gate (76 builds), every model, #19's and #21's mutations, the acmp planted defects, `elab_bounds.sh` | R437-1 | 70bf017d62d60b4401126c7b1bb087f4cb115c5a |
| Docs | UNCLEAN (F2's coverage claim); R1-R5 are residue | `tb/nvm_port/README.md`, `tb/acmp_nvm/README.md`, 01, 02, 07, 08 and 09 diffs, the integrator guide, diagram 21 (parameter gate), the PR body, `make check` | R437-1 | 70bf017d62d60b4401126c7b1bb087f4cb115c5a |

## 6. Real limits

- **Not run here, by scope:**
  - `run_suites.sh` (the full processor bank, including `pp_top`);
  - `lint_hdl.sh` over all 41 modules (only the three changed tops were linted);
  - `syn/yosys/run.sh`;
  - the five CI mutation campaigns and `d3_mutants.py`;
  - the donor bank, the parent consumer set, the act/hosted reproduction, and Vivado.

  I rely on the manager's public evidence for those.
- **Hosted CI:** `suites` was still running at my snapshot. `docs-gates` and `portability` had passed.
- **Device models are models.** No real flash or backend hardware was run. The default deadline is a derivation, not a measurement. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **The suite's harness geometry is tuned to `TMO` = 100.** It is also green at 64. At 37 it fails four checks, because of its own fixed 40-cycle delays (T25h, RW4) and one timing assumption in T24. That is a harness parameter limit, not a port defect (`P3-tmo37-pristine`).
- **Probe set 2, round 1** restored a region that the abandoned ERASE had itself erased, so Q17 and Q24 read UNFRAMED on the head RTL. Round 2 restores an untouched region, and only those results are cited. Both rounds are kept as receipts.

## 7. Pending manager duties

- The donor bank (9) and the parent consumer set (16) at dev `cdf49d1a`, with `parent-adoption-c4c6-ea3fb388.patch` and then `parent-adoption-p2-cdf49d1a.patch`.
- Hosted and act acceptance at the exact head.
- The final current-dev candidate build at the merge turn.
- Carry R1-R5 to the residue checklist.

## Receipts

Every receipt and script is listed in `MANIFEST.sha256`.

- `scripts/probe.py` is the probe driver: a copy of the tree per probe, exact-once edits, 8 parallel jobs.
- `scripts/probes_set{1,2,3}.py` are the probe definitions, including the directed phases' C++.
- `scripts/ooc_cost.sh` is the out-of-context cost run.

R437-1 FINISHED
