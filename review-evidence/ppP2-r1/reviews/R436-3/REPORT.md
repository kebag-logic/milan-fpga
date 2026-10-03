[R436] NEGATIVE - exact head 527662d659b4ead97675744d12a43af1ea92b9b3

# R436-3: internal independent delta review of PR #145 (lane P2, NVM port robustness)

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #145 (closes #15, #18, #19, #20, #21).
- **Exact head:** `527662d659b4ead97675744d12a43af1ea92b9b3`, tree `c283d84beb26019fa3a1e3ffc520c9ab32610a42`.
- **Delta reviewed:**
  - round 3, the five commits on round 2b's `c0715410` (`593f291`, `ae1cb85`, `355e7d3`, `6fb74ad`, `f4519fe`; assignment #15 comment 5961238126);
  - the `--no-ff` merges `46796bf` (main `88969246`, PR #144, C8) and `527662d` (main `c74711d4`, PR #146).
- **Clone:** a cleared-context detached clone. Every build and probe ran in a `git archive` export or a disposable local clone under the packet's `scratch/`. At the end the clone is byte-exact at the head (`receipts/clone_integrity.txt`): index `write-tree` = HEAD tree = `c283d84b`; no file differs in bytes or exec bit; the porcelain is empty with ignored files included; no gitlinks and no `.gitmodules`. One ignored `tb/nvm_port/__pycache__` that my own import created was removed before that check.

## Verdict

**NEGATIVE.** One MINOR finding is open (F1), so the Tests and Docs lenses are unclean.

**F1:** round 3's new drain bound is pinned in only one of its three branches.
- Four non-equivalent defects I planted in it pass all 1,104 standing checks and the figures gate. The suite runs at 100, 37 and 20; the standing randomized harness at 1, 2, 3 and 37.
  - Z1 and Z8: a header READ abandoned in `S_RHCOLL` is counted as owing more bytes than it still owes.
  - Z3: a READ abandoned in its wait state is counted as owing bytes.
  - Z10b: the 16-bit count is cut to 8 bits. That one makes the port **refuse a contract-legal device** when the device resumes a READ that still owes 256 bytes or more.
- The RTL at the head is correct. My directed probes R436g and R436h pass on the head and kill all four plants.

Everything else assigned for round 3 holds at this head:
- **Every round-2 finding is resolved under its original severity.** R436-2 F1 and R437-2 F1-F3 are resolved, R436-2 R1 and R2 are taken, and both round-2 S1s and R437-2 S2 are taken.
- **My round-2 plants and probes, re-run unchanged, behave as required.** Every non-equivalent plant fails a named check under all four models. The equivalent ones (Q3, Q4, Q8, Q10) stay 0 everywhere, including in the fuzz.
- **The merges keep both sides**, and §8.6 is cited correctly.
- **The cost figure reproduces exactly:** +51 LUT, +16 FF, +9 CARRY4.
- One RESIDUE: a PR-body sentence (R1).

## How the review was reconstructed

1. **Contributor rules.** The tree has no AGENTS.md or CONTRIBUTING.md. I read `README.md` and `docs/README.md`, including the single-source rules: timing values only in F08.1, parameter values only in F01.5.
2. **Scope.** Issue #15's body and its corrections (5355168983, 5355231359), the lane assignment (5951891343), the ruling (5952386396), the round-3 assignment (5961238126) and the round-3 REVIEW READY (5963684192). I also read the review-start comment on the PR (5963697733).
3. **The PR body.** The live PR body is byte-identical to `review-evidence/ppP2-r1/author-r3/PR-BODY.md` on milan-fpga `ppP2-review-evidence` at `e291df44`. I read its Round 3 section in full. Both parent patches in author-r3 match the stated sha256: p2 `3dda8509…d08b` (9,728 bytes) and c4c6 `67bcd698…7bd7c` (2,687 bytes).
4. **Authorities:**
   - the port banner, `hdl/packet_engine/KL_pp_nvm_port.sv:69-107`;
   - 02 §8 `sec-02-nvm-deadline`, `docs/architecture/02_interfaces.md:530-555`;
   - 09 §8.2 and §8.6, `docs/architecture/09_verification.md:215` and `:323-350`;
   - the `tb/nvm_port` README, deadline section `:464-569`, mutations `:571-692` and "Three bounds" `:694-`.
5. **The diffs:**
   - `git diff c74711d4..527662d6` (22 files);
   - the round-3 delta `c0715410..f4519fe` (9 files), with the RTL hunk and the whole port read in full;
   - both merges, re-derived per file and with `git merge-tree`.
6. **Public evidence:**
   - milan-fpga `d56e2227` `review-evidence/ppP2-r1` (the round-1 author packet);
   - `ppP2-review-evidence` `e291df44` (author-r3, and my R436-2 packet). My R436-2 scripts were fetched from there and checked against R436-2's MANIFEST.sha256: `plant.py`, `directed.py`, `rerun_round1.py`, `pause_fuzz.cpp`, `build_fuzz.sh` and `ooc_cost.sh`, all OK.
   - No separate manager evidence comment exists on #15 or #145 after the REVIEW READY. For the manager's banks I rely on the assignment's statement.
7. **Prior public review findings.** I read R436-2 (PR comment 5961230273) and R437-2's findings section (5960887168) only after my own pass over the diff. I did not read the concurrent round-3 review, any lane scratchpad, or any private author material.

## Executed evidence (exact head; receipts listed in MANIFEST.sha256)

The simulator is the scoped 5.050 wrapper. Its `--version` and sha256 are in `receipts/verilator_identity.txt`. The system default (5.052) was not used.

| Run | rc | Result | Receipt |
|---|---:|---|---|
| `make -C tb/nvm_port run` | 0 | elab guard OK (1 and 2^31-1 build; 0, 2^31 and 2^32-1 refused by name); 356 PASS at each of 100, 37 and 20; 9 PASS at each of fuzz 1, 2, 3 and 37; **1,104 PASS** | `receipts/nvm_port_run_head.log` |
| `make -C tb/nvm_port figures` | 0 | 129 builds; baseline 356/356; `make run` 356 x 3 + 9 x 4; **all measured figures agree** (Q1 2, Q9 4, D27 3, D28 1, D29 3, D30 3, D27/fuzz 1, D31 2, coincident/4096 0, T6-timed/coincident/4096 16); 15 min | `receipts/figures_head.log` |
| `make -C tb/acmp_nvm` | 0 | 372 + 16 = 388 PASS | `receipts/acmp_nvm_run_head.log` |
| `scripts/lint_hdl.sh` (pinned) | 0 | 41 modules LINT OK | `receipts/lint_hdl_head.log` |
| `make check`; `gen_matrix.py --check` (disposable clone) | 0 | 41 mermaid + 18 WaveDrom; links 1,060; REQ 115 rows, 17 GAP; module matrix 94 rows, 0 untested; parameters 28 = 28 = 28 | `receipts/make_check_head.log` |
| R436-2 `plant.py`, unchanged (16 plants x 4 models + its fuzz at 37 and 3) | 0 | see "Round-2 findings" | `receipts/r436-2-plants/plants.md`, `plants.json` |
| R436-2 `directed.py`, unchanged (R436d-f) | 0 | head 360 x 3 + 9 x 4 = 1,116 PASS, plain and coincident; Q1, Q2, Q9 and D26 each fail named checks | `receipts/r436-2-directed/SUMMARY.txt` |
| R436-2 `pause_fuzz.cpp`, unchanged, on the head: legal, silent, resume and babble x 3 seeds at 1, 2, 3, 37 and 100 | 0 | 0 FAIL in every run; 0 false DEADLINEs; silent 600/600 per seed; resume served iff r <= TMO; **babble answered 196-225 per seed** (round 2 answered none) | `receipts/r436-2-fuzz-head-*.log` |
| Gate Q-rows against R436-2 `plant.py` | - | Q1-Q10 byte-identical | `receipts/q_rows_vs_r436_2.txt` |
| R436-3 drain plants Z1-Z12 and Z10b (`scripts/plants_drain.py`, `scripts/run_plant.sh`) | - | 9 killed by named checks, Z10 by lint; **Z1, Z3, Z8 and Z10b pass all 1,104** | `receipts/drain_plants.md`, `receipts/plant_*.log` |
| R436g babble at every byte and terminal (`scripts/babble_probe.sh`), at 3, 37 and 100 | - | head 0 fails; Z1, Z3, Z8 and Z2 fail FZ9 | `receipts/babble_*.log` |
| R436h resume with payloads to 600 B (`scripts/resume_long_probe.sh`), at 3 and 37 | - | head 0 fails, both FZ7 branches taken; Z10b fails FZ7 63 and 53 | `receipts/resumelong_*.log` |
| Nine models at 20, 21, 1,000 and 4,096 (`scripts/models_at.py`, adapted from R436-2's `models_at_37.py`) | 0 | the seven legal models 356/0 at every bound; short read 273/83; silent 115/241; RW checks pass under all nine | `receipts/models_at_bounds/SUMMARY.txt` |
| The standing harness at every bound from 4 to 19 (`make fuzz FUZZ_TMOS="4 ... 19"`) | 0 | 9/9 at each of the 16 bounds | `receipts/fuzz_gap_4_19.log` |
| The suite at 19 | 2 | refused at compile by `static_assert(TMO >= 20)`, as documented | `receipts/floor19.txt` |
| Out-of-context cost (`scripts/ooc_cost_r3.sh`: sv2v, then Yosys `synth_xilinx -flatten`) | 0 | see the RTL lens | `receipts/ooc/` |
| Merge re-derivation (`scripts/merge_check.sh`) | - | see the merge section | `receipts/merge_check.txt` |
| Hosted checks at the head (read-only snapshot) | - | `docs-gates` and `portability` succeeded, two runs each; `suites` in progress at the snapshot | `receipts/hosted_checks_snapshot.txt` |

## Round-2 findings, judged at this head under their original severity

| Finding | Severity | Status | Evidence at 527662d6 |
|---|---|---|---|
| R436-2 F1: Q1 and Q9 pass every check | MINOR | **RESOLVED** | `plant.py` unchanged: Q1 fails T30a and RW4 under the pristine, coincident, unsolicited and lazy-erase models; Q9 fails T30c, T30d, T30e and RW4 under all four. Fuzz at 37 and 3: Q1 456/420/105 and 567/557/136, Q9 63/161/12 and 1002/270/83. `directed.py` unchanged: the head passes R436d-f in all three suite builds; Q1 and Q9 fail them. The gate's Q1-Q10 rows are my edit text byte for byte, and the figures gate measures them as the README states. Q2, Q5, Q6 and Q7 fail named checks; Q3, Q4, Q8 and Q10 stay 0 in all four models and in the fuzz (equivalent, as argued in the README `:669-676`) |
| R436-2 S1: over-length owed drain | SUGGESTION | **TAKEN** | `owed_left_r` and `drain_w` (`KL_pp_nvm_port.sv:222`, `:290-296`, `:323-327`, `:608-610`). My unchanged babble mode now answers every waiting request at 1, 2, 3, 37 and 100; T28f; FZ9 (but see F1) |
| R436-2 R1: the comma | RESIDUE | **RESOLVED** | `tb/nvm_port/README.md:479` reads "T24, T28 and T29 grade all of it" |
| R436-2 R2: the ordinals | RESIDUE | **RESOLVED** | README `:545-546` reads "11th byte" and "21st"; PR body Round 2 item 4 (`:263-264`) likewise |
| R437-2 F1: a paused cycle at the bound | MINOR | **RESOLVED** | T30c-e (`sim_main.cpp:2187-2272`). Gate rows Y11 and Y16 fail 4 each (T30c-e, RW4) in my figures run; Q9, the same defect, is killed as above |
| R437-2 F2: `S_WEWAIT`'s latched term | MINOR | **RESOLVED** | T30a; gate row Y1 = Q1 fails 2 (T30a, RW4) |
| R437-2 F3: T6's poke at large bounds | MINOR | **RESOLVED** | T6 now waits for the backend to have taken the ERASE (`sim_main.cpp:1035-1037`). All nine models at 1,000 and 4,096 behave as stated, coincident 356/0. Gate row T6-timed/coincident/4096 = 16 shows that round 2's T6 would fail there |
| R437-2 S1 (= R436-2 S1) | SUGGESTION | **TAKEN** | as R436-2 S1 |
| R437-2 S2 (X20, a late grant carrying err) | SUGGESTION | **TAKEN** | T24 `late_grants_that_leave_nothing_owed` (`sim_main.cpp:1936-1972`); gate row D31 = X20 fails 2 |
| R437-1 R2-R5 | RESIDUE | **RETAINED** (not assigned) | carried by the manager; not re-derived in this round |

Round-1 findings (R436-1 F1/F2, R437-1 F1/F2) were resolved in R436-2. Their rows D18-D22 are re-measured by the figures gate at this head and agree, so nothing reopens them.

## The delta, item by item

1. **T30 and the standing harness** (`sim_main.cpp:2187-2272`; `tb/nvm_port/fuzz_main.cpp`).
   - **T30's arms:**
     - (a) puts the WRITE grant at the bound after an ERASE answered on its own grant;
     - (b) does the same for a payload READ after a header READ answered on its eighth byte;
     - (c) and (d) put a byte `TMO` cycles late on the one cycle the manager drops its strobe;
     - (e) is the one-cycle-later DEADLINE control.
   - The `S_WWAIT` and `S_RPWAIT` members are equivalent. I traced it: entering either wait state follows a final-byte progress cycle, so the count is 0, and a latched done leaves at once for `S_FIN` and then `S_IDLE`.
   - **The harness** is built by `make` at 1, 2, 3 and 37, one named check per property (FZ1-FZ9).
     - A false DEADLINE against a legal device fails FZ2, and through it `make run` and `run_suites.sh`. Q1 and Q9 under it at bound 3 fail FZ2 (gate rows).
     - At this head it is clean at every bound from 1 to 19 and at 37.
   - **The floor claim holds.** The suite is built at 100, 37 and 20, and 20 is the harness floor (`sim_main.cpp:57-58`: 19 is refused at compile). Every model behaves as stated at 20, 21, 1,000 and 4,096.
   - **"The smallest legal bound".** The assignment asked for a build there. The PR body reads it as the suite's floor, with 1-3 covered by the randomized harness. That reading is stated openly (PR body `:560-563`), and it is the only one the fixed 1-9 cycle protocol delays allow. The port's own bound 1 is elaborated by `elab_bounds.sh` and graded by FZ1-FZ9 at 1.
2. **The drain bound** (`KL_pp_nvm_port.sv:285-327`, `:608-610`).
   - **The RTL is correct.**
     - `owed_left_r` loads only on `dl_w && !owed_r`.
     - On a verdict cycle no byte moves: a byte is progress, so `dl_w` is false. That makes `8 - hidx_r` (`S_RHCOLL`) and `plen_r - bcnt_r` (`S_RPPUMP`) exact.
     - `dev_len_o` gives 8 or `plen_r` in a request state (the late grant), and 0 in a wait state, where every byte has moved.
     - It decrements exactly on the drain handshake.
     - While anything is owed the FSM cannot leave its first request state, so the drain never overlaps a data phase.
     - A legal device (at most its length, then a terminal) still ends the owed state with its terminal. The terminal is progress, so it is never refused.
   - **It conforms to the contract.** The bound is 02 §8's "takes and discards the bytes an owed READ still owes (its length less those that moved before the deadline) and no more" (`02_interfaces.md:542-548`), and the banner's `:86-93`.
   - **What is graded.** Only the `S_RPPUMP` branch is pinned (T28f, FZ9), not the `S_RHCOLL` branch, the wait-state branch or the count's width (F1).
3. **The late grant carrying err.** T24 grades it, both the DEADLINE pulse and the next commit served (gate row D31 = X20, 2 fails).
4. **The merges.**
   - **`527662d` (#146):** `git merge-tree` of its parents equals its tree exactly (`c283d84b`), so #146's driver changes are intact.
   - **`46796bf` (#144, C8):** one conflict, 09's appended section. The other three files the merge base shows changed on both sides (01, 07, the integrator guide) equal `git merge-tree`'s automerge byte for byte.
     - 09's resolution is C8's §8.5 verbatim, then this lane's section renamed §8.6, then the shared tail.
     - The only other edit is §8.2's pointer, now "§8.6's" (`09_verification.md:215`).
     - Every "09 §8.5" left in the tree is C8's descriptor lint: 00, 07 `:107` and `:171`, and the `tb/desc_store` README.
     - Every `KL_pp_nvm_port.sv:NNN` citation in the tree points at its text (`:33-34`, `:234-245`, `:340-344`, `:436-439`), as do the PR body's round-3 citations.
5. **Out-of-context cost:** reproduced exactly with my R436-2 recipe (`receipts/ooc/ooc_summary.txt`).

   | Setting | Round 2 `c0715410` (LUT / FF / CARRY4) | Head | Delta |
   |---|---|---|---|
   | the default | 245 / 148 / 21 | 296 / 164 / 30 | **+51 / +16 / +9** |
   | at 1 | 248 / 122 / 14 | 287 / 138 / 23 | +39 / +16 / +9 |
   | at 2^31-1 | 266 / 152 / 22 | 301 / 168 / 31 | +35 / +16 / +9 |
   | at 125,000,000 | 261 / 148 / 21 | 309 / 164 / 30 | +48 / +16 / +9 |

   Main `631eeb34` is 197 / 118 / 14.

## Findings

### F1 - MINOR - Tests, Docs

**The drain bound is pinned in one of its three branches. Four non-equivalent plants pass all 1,104 standing checks and the figures gate, and one of them refuses a contract-legal device.**

- **Where:**
  - The RTL: the `S_RHCOLL` branch of `left_w` (`hdl/packet_engine/KL_pp_nvm_port.sv:293`); its wait-state branch, which takes `dev_len_o`, 0 there (`:295`); and the width of `owed_left_r` (`:222`).
  - The checks that leave them unpinned:
    - T28f (`tb/nvm_port/sim_main.cpp:2402-2438`) abandons only a payload READ, before its 11th byte, owing 30;
    - FZ9's babble mode (`tb/nvm_port/fuzz_main.cpp:487`) abandons only at payload bytes;
    - no check resumes an abandoned READ that still owes 256 bytes or more (FZ7's payloads are 0-24 bytes, `fuzz_main.cpp:422`, `:446`);
    - gate row D28 edits the `S_RHCOLL` and `S_RPPUMP` branches together and is killed by the `S_RPPUMP` half alone (README `:650-652`).
  - The coverage claims: 09 §8.6 (`docs/architecture/09_verification.md:341`) maps "an owed READ drained of the bytes it still owes and no more" to T28f, D27-D31 and FZ9. Also README `:534-541`, and the PR body's Round 3 item 2.
- **Authority:**
  - The banner, `KL_pp_nvm_port.sv:86-93`: "drains the bytes an owed READ still owes and no more".
  - 02 §8 (`02_interfaces.md:542-548`): "its length less those that moved before the deadline".
  - The round-3 assignment (5961238126) item 2, and this review's focus: every non-equivalent plant in the drain bound must fail a named check, and no legal device may be refused.
  - The precedent of R436-1 F1, R436-2 F1 and R437-2 F1-F3: a planted defect the suite passes is a test gap of this severity.
- **Evidence** (`receipts/drain_plants.md`; edit text in `scripts/plants_drain.py`):
  - **Z1**: `left_w` in `S_RHCOLL` is `HDR_LEN_C`. **Z8**: it is `HDR_LEN_C - hidx_r + 1`. **Z3**: a READ abandoned in `S_RHWAIT` or `S_RPWAIT` owes 8. **Z10b**: `owed_left_r` is 8 bits wide, spelled lint-clean. Each is **1,104/1,104 PASS**: suite at 100, 37 and 20, harness at 1, 2, 3 and 37.
  - Each is non-equivalent:
    - **R436g** (`scripts/babble_probe.sh`) is the head's own babble mode, with the abandoned obligation drawn from every byte and terminal of a restore. The head is 0 fails at 3, 37 and 100. Z1 fails FZ9 229/249/241 times, Z8 316/299/285 and Z3 70/81/54 ("a READ owing 0 bytes … 8 taken").
    - **R436h** (`scripts/resume_long_probe.sh`) is the head's own resume mode with payloads up to 600 bytes; 664 abandoned frames of 264 bytes or more were exercised. The head is 0 fails, with both branches taken. Z10b fails FZ7 63 times at 3 and 53 at 37: "the abandoned command ended 26 cycles into a commit's wait: 0 done, 1 err, cause 3".
  - The other nine drain plants are killed by named checks: Z2, Z4-Z7, Z9, Z11, Z12, and Z10 by `elab_bounds.sh`'s width lint only.
- **Impact:**
  - Today's RTL is right; the head passes R436g and R436h.
  - **Z1, Z3 and Z8** would ship green. Against a backend presenting bytes past a READ's length, the port would take up to 8 bytes the READ does not owe, as progress. That delays the waiting request's DEADLINE by up to 8 byte intervals. It is exactly the "no more" this round adds, and 09 §8.6 lists it as graded.
  - **Z10b** would ship green and refuse a contract-legal device. A READ abandoned with 256 or more bytes still owed would be drained modulo 256. A backend that then delivers the rest at legal pace stalls on a byte the port no longer accepts, and never ends the READ. Every later request ends DEADLINE until reset.
    - The port takes payloads up to `MAX_PAYLOAD_P` = 1,024 at the top (`protocol_processor_top.sv:2885-2887` keeps the default).
    - The managers would turn the refusals into failed walks and write attempts, and then `nvm_alarm_o`.
- **Required outcome:**
  - Add standing checks that kill Z1, Z3, Z8 and Z10b, each naming its property. Two examples:
    - FZ9's abandonment drawn from every byte and terminal of a restore (R436g's two-line edit at `fuzz_main.cpp:487`), or directed T28f arms abandoned in `S_RHCOLL` after k header bytes and in `S_RHWAIT`/`S_RPWAIT`;
    - an abandoned READ owing at least 256 bytes, then resumed at legal pace and served: R436h's payload range, or a T28 arm with a payload above 300 bytes.
  - Record the four as figures-gate rows with the edit text of `scripts/plants_drain.py`.
  - Keep the README, 09 §8.6 and the PR body's counts in step.
- **Verification:**
  - Z1, Z3, Z8 and Z10b each fail a named check.
  - The head stays green in every build.
  - `make -C tb/nvm_port figures` gives rc 0.
  - The re-review re-runs `scripts/run_plant.sh {Z1,Z3,Z8,Z10b} scripts/plants_drain.py` unchanged.

### R1 - RESIDUE - Docs (wording only, PR body)

The PR body's "Round 3 parent-visible list", item 3, reads "The banner sentence the p2 patch paraphrases is unchanged". That sentence did change this round: `KL_pp_nvm_port.sv:86-93` and `02_interfaces.md:542-548`, as `git diff c0715410..f4519fe` shows. The patch's paraphrase still holds, and so does the decision to leave the patch unchanged, so no measurement, figure, verdict or artifact moves.

**Exact fix:** replace "The banner sentence the p2 patch paraphrases is unchanged. Its "drains an owed read's bytes" still holds, since bytes past a READ's length are not the READ's." with "The banner sentence the p2 patch paraphrases changed this round only to bound the drain by what the READ still owes; the patch's "drains an owed read's bytes" still holds, since bytes past a READ's length are not the READ's."

## Issue-by-issue acceptance at this head

| Issue | Status | Evidence |
|---|---|---|
| #15 items 1-4 | MET | T24 twelve states; T28; T29; T30; FZ5/FZ6 exact at 1-19 and 37; elab guard; silent model 115/241 at 20-4,096 |
| #15 ruling (c), both branches | MET | T24 served and DEADLINE branches; FZ7/FZ8; R436h on the head |
| #18, #19, #20, #21 | MET (unchanged by round 3) | T25; `tb/acmp_nvm` 388; gate rows M*, S*, latch rows; seven legal models 356/0 at 20, 21, 37, 100, 1,000 and 4,096 |

F1 does not unmeet an acceptance item: the head refuses no legal device. It leaves round 3's coverage claim for the drain bound short.

## Lens results

### Conformance (CLEAN)

- The round-3 assignment is followed item by item:
  - no port changed, and no parameter beyond the ruled two;
  - one internal count, as item 2 authorizes;
  - item 3 taken;
  - R436-2 R1 and R2 in the exact text;
  - both merges `--no-ff`, with C8 keeping §8.5 and this lane at §8.6.
- The drain bound conforms to 02 §8 and the banner. A READ owes at most its length, and no legal device is refused (R436h, the legal fuzz at 1-19 and 37, and all seven legal models at six bounds).
- Both parent patches are unchanged (sha256 verified). The PR body states that a parent adopting this head also needs C8's patch. That is the manager's to run.

### RTL (CLEAN)

- I read `KL_pp_nvm_port.sv` in full and the round-3 hunk line by line. The drain bound is exact in every branch (see the delta, item 2).
- Lint is clean over 41 modules, and the elaboration guard holds.
- The cost reproduces exactly: +51 LUT, +16 FF, +9 CARRY4 at the default.
- The merges change no RTL of this lane. #144's `KL_aecp_desc_store.sv` is main's own and is covered by the manager's banks.

### Robustness (CLEAN)

- No false DEADLINE:
  - my unchanged harness at 1, 2, 3, 37 and 100;
  - the standing harness at every bound from 1 to 19 and at 37;
  - all seven legal models at 20, 21, 37, 100, 1,000 and 4,096.
- The silent verdict lands exactly on the (TMO + 1)-th owed cycle.
- A babbling backend is now answered DEADLINE at every bound, and long resumed READs are served on the head.

### Tests (UNCLEAN: F1)

- 1,104 checks; 129 figures builds agree.
- Every round-2 plant is killed by a named check, apart from the equivalent ones.
- In the drain bound, Z1, Z3, Z8 and Z10b survive every standing check.

### Docs (UNCLEAN: F1; R1 residue)

- F1's coverage claim at 09 §8.6 `:341` and README `:534-541` is short.
- These read consistently with the RTL: 02 §8, the banner, 09 §8.2 and §8.6, the README's T30/T28f/D27-D31/Q/Y text, and the PR body's Round 3 (but see R1).

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #15 body and comments 5355168983, 5355231359, 5951891343, 5952386396, 5961238126, 5963684192; PR #145 body (Round 3; byte-identical to author-r3 at `e291df44`); both parent patches (sha256); 02 §8, banner; merge resolutions `46796bf` and `527662d` | R436-3 | 527662d659b4ead97675744d12a43af1ea92b9b3 |
| RTL | CLEAN | `KL_pp_nvm_port.sv` (full; round-3 hunk traced); merges' `hdl` diff; lint over 41 modules; elab guard; OOC cost at the default, 1, 2^31-1 and 125M against round 2 and main | R436-3 | 527662d659b4ead97675744d12a43af1ea92b9b3 |
| Robustness | CLEAN | the drain bound, the late grant with err, the pause and verdict; R436-2's harness in 4 modes at 5 bounds; the standing harness at 1-19 and 37; 9 models at 20, 21, 1,000 and 4,096; R436g and R436h on the head | R436-3 | 527662d659b4ead97675744d12a43af1ea92b9b3 |
| Tests | UNCLEAN (F1) | `tb/nvm_port` (`sim_main.cpp` T6, T24, T28f, T30; `fuzz_main.cpp`; Makefile; `measure_figures.py`; `deadline_rows.py`; README); `make run` 1,104; figures gate 129; R436-2 `plant.py` and `directed.py` unchanged; 13 drain plants; `tb/acmp_nvm` 388 | R436-3 | 527662d659b4ead97675744d12a43af1ea92b9b3 |
| Docs | UNCLEAN (F1); R1 residue | 02 §8, 09 §8.2 and §8.6, banner, `tb/nvm_port` README, PR body Round 3; `make check`, `gen_matrix.py --check`; citation and anchor sweep | R436-3 | 527662d659b4ead97675744d12a43af1ea92b9b3 |

## Real limits

- **Not run here:**
  - the full `run_suites.sh` bank;
  - the mutation campaigns (`d3_mutants.py`, aecp, dispatch, maap, adp, srp_top, acmp, notify, gsi, name_wr, srp_admission, retry);
  - `syn/yosys/run.sh`;
  - the donor bank and the parent consumer set;
  - `tb/pp_top` and `tb/desc_store`, which #144's merge touches but this lane does not.

  For those I rely on the PR body's Round 3 tables and the manager's banks. I ran the suites the round-3 delta touches (`nvm_port`, `acmp_nvm`), lint, the docs gates and the figures gate.
- **R437-2's own scripts were not run.** Its plant text is graded through the gate's Y1-Y16 rows, which my figures run measured, and through my own bound sweep.
- **Hosted CI.** `suites` was in progress at my snapshot. The manager owns hosted and act acceptance.
- **The randomized harnesses are models.** They use fixed seeds; they are not proofs. My R436g and R436h are probe edits of the head's own harness and are not proposed as the PR's code.
- **Cost instrument.** The cost is sv2v plus Yosys `synth_xilinx`, not a Vivado report.
- **Hardware.** Physical calibration NOT RUN. No hardware. Field skips are not hardware proof.

## Pending manager duties

- Run the donor bank (9), and the parent consumer set (16) at dev `cdf49d1a` with `parent-adoption-c4c6-ea3fb388.patch`, then C8's `parent-adoption-c8-cdf49d1a.patch`, then `parent-adoption-p2-cdf49d1a.patch`. Main carries C8.
- Build the final current-dev candidate at the merge turn (source base `c74711d45a8bbc0d6b38cb49211b26a4a6413e88`, live dev `cdf49d1a28527562888f0a903de51b6b15b1244f`).
- Hosted and act acceptance at the exact head, distinguishing executed jobs from skipped contexts.
- Own the evidence for the PR body's campaign table.
- Route F1 to the author. Re-review the fix head:
  - re-run `scripts/run_plant.sh` for Z1, Z3, Z8 and Z10b;
  - re-run R436g and R436h unchanged;
  - re-run the figures gate.
- Carry R1, and R437-1's retained R2-R5, to the residue checklist.

R436-3 FINISHED
