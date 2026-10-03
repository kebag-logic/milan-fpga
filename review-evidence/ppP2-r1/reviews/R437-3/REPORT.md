[R437] NEGATIVE - exact head 527662d659b4ead97675744d12a43af1ea92b9b3

# R437-3: external delta review of PR #145 (lane P2, NVM port robustness)

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan. Issue #15, lane P2 (#15, #18, #19, #20, #21; the PR closes all five).
- **Head:** `527662d659b4ead97675744d12a43af1ea92b9b3`, tree `c283d84beb26019fa3a1e3ffc520c9ab32610a42`.
  - Five lane commits on round 2b's `c0715410`: `593f291`, `ae1cb85`, `355e7d3`, `6fb74ad` and `f4519fe`.
  - Then two `--no-ff` merges of main: `46796bf` (main `88969246`, PR #144, C8) and `527662d` (main `c74711d4`, PR #146).
- **Scope:** round 3 (assignment 5961238126), which answers R436-2 (1 MINOR) and R437-2 (3 MINOR).
- **Clone:** isolated and detached. At the end it was verified byte-exact at the head (`receipts/clone_integrity.txt`):
  - `write-tree` equals `c283d84b`, and the porcelain is empty, ignored files included;
  - the index's modes and blobs equal the HEAD tree;
  - there are no gitlinks and no `.gitmodules`, so no submodule pin is required.
- **Verdict: NEGATIVE.** One MINOR finding is open (F1), so two lenses are unclean: Tests and Docs.
  - Conformance, RTL and Robustness are clean.
  - All of my round-2 findings are closed at their original severity. Both round-2 suggestions are taken, and R436-2's F1 is closed.
  - The new drain bound is correct in all four of its arms (my directed checks ZD1-ZD4 pass at three bounds under two models).
  - **The gap:** the suite grades only one of those four arms in the direction that matters, and it does not grade the new count's width at all. Five of my non-equivalent plants in the bound pass all 356 checks and all 9 randomized checks. One of them (B10) wedges the port against a device that ends a large abandoned READ at a legal pace.

## 1. Reconstruction (order followed)

1. **Repository rules.** There is no AGENTS.md or CONTRIBUTING.md. I used `docs/README.md` (single-source rules, `make check`).
2. **Scope.** The issue bodies, as in rounds 1 and 2, and these comments on #15:
   - the ruling 5952386396;
   - the round-3 assignment 5961238126 (items 1-5, the gates and the STOP rule: no port, no parameter beyond the ruled two);
   - REVIEW READY 5963684192.

   On #145, the review start 5963698097.
3. **Authorities.**
   - The port banner's deadline section (`hdl/packet_engine/KL_pp_nvm_port.sv:69-107`).
   - 02 §8, the deadline paragraph (`docs/architecture/02_interfaces.md:530-555`).
   - 09 §8.6 (`09_verification.md:323-349`) and the §8.2 pointer (`:215`).
   - The `tb/nvm_port` README: T24, T28f, T29, T30, the D and plant tables, "Three bounds" and "The randomized harness" (`:470-770`).
   - `deadline_rows.py`, `fuzz_main.cpp` and `measure_figures.py`.
4. **The diff.**
   - `git diff c74711d4..527662d6` (22 files).
   - The lane's own delta, `git diff c0715410..f4519fe`: 9 files, with the RTL change confined to `KL_pp_nvm_port.sv`.
   - Both merges, checked file by file against their parents (section 5).
5. **Public evidence.**
   - milan-fpga `review-evidence/ppP2-r1`, `author-r3` (archive commit `e291df44`). Its four files match `MANIFEST.json`'s `published_sha256`.
   - The live PR body equals `author-r3/PR-BODY.md`, modulo the final newline.
   - Both parent patches are byte-identical to rounds 1 and 2 (c4c6 `67bcd698…`, p2 `3dda8509…`; `receipts/evidence_check.txt`).
6. **Prior public findings**, read only after my own pass over the diff and my drain plants: R436-2 (5961230273) and my own R437-2 (5960887168). Their resolution is in section 4.

## 2. Executed evidence (exact head; scoped Verilator 5.050, identity in `receipts/toolchain.txt`)

| Run | rc | Result |
|---|---:|---|
| `make -C tb/nvm_port` on a `git archive` export | 0 | The guard refuses 0, 2^31 and 2^32-1 by name and builds 1 and 2^31-1. 356 + 356 + 356 at 100, 37 and 20, plus 9 at each of 1, 2, 3 and 37: **1,104/1,104** |
| `make -C tb/acmp_nvm` (export) | 0 | 372 + 16 = **388/388** |
| `make -C tb/nvm_port figures`, in a disposable local clone at the head | 0 | 129 builds. Baseline 356/356. `make run` gives [(356,356,0)×3, (9,9,0)×4, (1104,1104,0)]. 123 rows `[ok ]`, 0 disagree, including Q1 2, Q9 4, Y1 2, Y11 4, Y16 4, Q1/fuzz 4, Q9/fuzz 4, coincident/4096 0, T6-timed 16, D27-D31 3/1/3/3/2 and D27/fuzz 1 (`receipts/figures_gate.log`) |
| The same gate on a `git archive` export | 2 | Every figure row is `[ok ]` (123). The only failures are the pre-fix matrix's git-history pins, which an export cannot read (`receipts/figures_gate_export_nogit.log`). This is why the gate must run in a clone, as the author did |
| `make check`, in a disposable local clone | 0 | 41 mermaid + 18 WaveDrom; links 1,060; REQ 115 rows / 17 GAP; 94 module rows, 0 untested; parameters 28 = 28 = 28 |
| `lint_hdl.sh` flags on the port (default, 1, 2, 3, 37, 2^31-1, `MAX_PAYLOAD_P` 65527), the arbiter and the top | 0 | Clean everywhere; 2^31 refused by name (`receipts/lint_changed.txt`) |
| Out-of-context cost (sv2v, then Yosys `synth_xilinx -family xc7 -flatten`), round 2 `c0715410` against the head | 0 | At the default: 245/148/21 → 296/164/30, **+51 LUT, +16 FF, +9 CARRY4**. At 1: +39/+16/+9. At 2^31-1: +35/+16/+9. At 125 M: +48/+16/+9. All equal the PR body (`receipts/ooc_cost.txt`) |
| Drain-bound plants B1-B13, each in the suite (pristine and coincident, at 100, 37 and 20) and the randomized harness (1, 3 and 37) | - | `receipts/drain/` (section 3, F1) |
| Directed drain checks ZD1-ZD4 at the head and against the surviving plants | - | `receipts/spec_zdrain/` (F1) |
| My round-2 probes and plants, re-run unchanged: Y1-Y16, Z1a/Z1b/Z2, the round-1 probes, the bound sweeps, BABBLE | - | `receipts/spec_y_pause/`, `spec_z2_directed/`, `spec_r3_rerun/` (Y1, Y11 and Y16 at 20 under the seven legal models, Y11 at 100 and 37 under all seven), `spec_r1_reprobe/`, `spec_bounds/`, `spec_bounds2/`, `spec_babble/` (section 4) |
| The randomized harness against false-DEADLINE plants at 1, 2, 3 and 37; the head's harness at 1-19, 37, 100 and 1,000 | - | `receipts/spec_fuzz/` (section 5) |
| The suite with only its `TMO >= 20` assert removed, at 19, 15, 10 and 5 | - | `receipts/spec_floor/` (section 5) |

**Hosted CI at the exact head** (snapshot 01:10Z, `receipts/hosted_checks_snapshot.txt`):

- `docs-gates` and `portability` succeeded on both runs (push and pull_request).
- `suites` was still in progress on both.
- The manager owns hosted and act acceptance.

## 3. Findings

### F1 - MINOR - Tests, Docs: the drain bound is graded in one of its four arms, and its count's width is not graded at all

- **Where:**
  - The bound, added this round:
    - `hdl/packet_engine/KL_pp_nvm_port.sv:222`, the 16-bit `owed_left_r`;
    - `:293-295`, `left_w`. Its four arms are header collection (`S_RHCOLL`), payload pump (`S_RPPUMP`), and `dev_len_o` for the rest: the length of a READ the backend granted late in a request state, and 0 in a wait state;
    - `:296`, `drain_w`;
    - `:323-327`, the count.
  - The checks that grade it:
    - T28f (`tb/nvm_port/sim_main.cpp:2402-2438`) and FZ9 (`fuzz_main.cpp` `one_babble`), each a payload READ abandoned in `S_RPPUMP`;
    - T24's twelve arms, a 40-byte record;
    - rows D27-D30 (`deadline_rows.py:96-109`). D28 edits two arms at once and is killed through the `S_RPPUMP` arm alone.
  - The coverage claims:
    - 09 §8.6 `:341` ("an owed READ drained of the bytes it still owes and no more … | T24 …; T28c, T28f; D9-D17, D22, D27-D31; … FZ9");
    - the README's T28f bullet (`:534-541`) and its D27-D30 paragraph (`:647-656`);
    - the PR body's Round 3 item 2 ("The drain `drain_w` … takes those bytes and no more").
- **Authority:**
  - The banner `:84-99` ("drains the bytes an owed READ still owes and no more … served once the device has ended the abandoned command").
  - 02 §8 `:543-548` ("its length less those that moved before the deadline … DEADLINE while it stays silent or presents bytes past the READ's length, which the port does not take").
  - Round-3 assignment item 2.
  - The review rule this lane has been held to in every round (R436-1 F1, R437-1 F2, R436-2 F1, R437-2 F1/F2): a non-equivalent planted defect that passes the suite is a test gap of this severity.
- **Evidence** (`receipts/drain/`, `receipts/spec_zdrain/`). All plant texts are in `scripts/spec_drain.py`.
  - **Killed (each falsely refuses a legal device that ends the abandoned READ late):**
    - B1, the payload arm one short: 18 of 356, T24, T28d-f and T30e; FZ7 and FZ9.
    - B2, the header arm one short: 17 of 356, T24.
    - B3 and B4, the request arm one short and zero: 19 of 356 each, T24.
    - B13, the count not loaded at a request-state deadline: 19 of 356, T24.
  - **Killed (over-drain):** B5, the payload arm one over, fails T28f and FZ9. B9, the count decremented unguarded so that it wraps, fails T28f, RW1 and FZ9.
  - **Pass everything:** 0 of 356 under pristine and coincident at 100, 37 and 20, and 0 of 9 in the randomized harness at 1, 3 and 37. Each is non-equivalent:
    - **B6**/**B6b**, the header arm one over / the whole 8. The head passes my ZD1, in which a header READ is abandoned before its 4th byte and its device then presents bytes past the length: exactly 5 drained, then DEADLINE. **B6 and B6b fail ZD1.**
    - **B7**, the request arm one over. The head passes ZD3: a header READ granted on the edge its deadline withdrew it, then bytes past the length: exactly 8 drained. **B7 fails ZD3.**
    - **B8**, a wait state owing 8. The head passes ZD2: a header READ abandoned in `S_RHWAIT`, then more bytes: none drained. **B8 fails ZD2 (8 drained).**
    - **B10**, `owed_left_r` 8 bits wide. The head passes ZD4: a 600-byte payload READ is abandoned before its 11th byte, its device then ends it at a legal pace, and the waiting restore is served byte-exact with 590 bytes drained. **B10 fails ZD4.** The port takes 590 mod 256 = 78 bytes and stops. The device cannot move its next byte, so it never ends the READ, and the waiting restore ends DEADLINE. Every later request does too, until reset.
  - The head passes ZD1-ZD4: 372/372 under pristine and coincident at 100, 37 and 20.
  - **B12** (the drain not limited to a READ) passes ZD1-ZD4 too. It is equivalent under the contract: no device presents read bytes for a WRITE or an ERASE.
- **Impact:**
  - The bound's RTL is right today, but a regression in three of its four arms, or in its width, ships green.
  - **B10** breaks #15 criterion 2's served branch, "served once the device has ended the abandoned command", for any READ that owes more than 255 bytes. The top keeps the default `MAX_PAYLOAD_P` of 1,024, and a restore's payload length is whatever the stored header says, up to that bound. The suite's own geometry is also 1,024.
  - **B6-B8** let a babbling backend hold a waiting request off with up to 8 bytes the READ never owed. That falsifies the "and no more" that 02 §8, the banner and 09 §8.6 state and attribute to these checks.
  - Of this round's item 2, only the payload-pump arm is graded in the over-drain direction.
- **Required outcome:**
  - Add named checks that kill B6 (or B6b), B7, B8 and B10, for example ZD1-ZD4 (`scripts/spec_zdrain.py` holds them verbatim as an edit of T28f's function):
    - a header READ abandoned mid-collection, then babbling: exactly what it owes is drained;
    - a READ abandoned in a wait state, then babbling: nothing is drained;
    - a READ granted late, then babbling: exactly its length is drained;
    - a READ owing more than 255 bytes, ended late at a legal pace: the waiting request is served.
  - Record each as a figures-gate row with this review's edit text.
  - Keep the 09 §8.6 row and the README counts in step.
- **Verification:**
  - B6, B6b, B7, B8 and B10 each fail a named check.
  - The head stays green under the seven legal models at 100, 37 and 20, and the RW checks hold under all nine.
  - `make -C tb/nvm_port figures` gives rc 0.
  - The re-review re-runs `scripts/spec_drain.py` and `scripts/spec_zdrain.py` unchanged.

### RESIDUE (wording only; retained from R437-1, not assigned; carried by the manager)

| ID | Location at this head | Status |
|---|---|---|
| R2 | `tb/nvm_port/README.md:1039` and `:1046` | still present; R437-1's exact fix stands |
| R3 | `tb/nvm_port/sim_main.cpp:1158` and `:1244` | still present; R437-1's exact fix stands |
| R4 | `hdl/acmp/KL_acmp_nvm_shadow.sv:208` and `hdl/aecp/KL_aecp_nvm_writer.sv:260` | still present ("1 DEVICE, 2 UNFRAMED"; append ", 3 DEADLINE (read as DEVICE)") |
| R5 | parent `SAVED_STATE_MATERIALIZATION.md:1930`, after both patches | still present; the patch is unchanged |

## 4. Prior public findings at this head

Each probe and plant was re-run unchanged at the head. Only `probe.py`'s `HEAD =` pin was updated. Two additions: a fuzz-harness target, and, after the runs, a switch that leaves no bytecode cache in the clone.

| Finding (severity) | Probe at the head | Result | Status |
|---|---|---|---|
| R437-2 F1 (MINOR): a paused cycle at the bound | Y11, Y16 | Each fails **T30c, T30d, T30e** and RW4 under all seven legal models at 100, 37 and 20 (some cells add T29a or T29b). Under the randomized harness each fails FZ2, FZ3, FZ6 and FZ7 at 1, 2, 3 and 37. Z1a and Z1b: 0 at the head under the seven legal models, and they fail on Y11 and Y16 | **Closed** |
| R437-2 F2 (MINOR): `S_WEWAIT`'s latched term | Y1 | Fails **T30a** and RW4 under all seven legal models at 100, 37 and 20, and FZ2/FZ3/FZ6/FZ7 at 1-37. Z2 fails on Y1 and passes at the head | **Closed** |
| R437-2 F3 (MINOR): the harness at every bound | bound sweeps | Coincident is 0 FAIL at 200, 300, 400, 450, 500, 550, 600, 800, 4,096 and 100,000. Pristine, coincident, unsolicited and lazy erase are 0 at 20, 21, 64, 1,000 and 1,001. Short read and silent fail service only, and every RW check holds. The README now bounds its claim "from its smallest, 20, up", gated by the coincident/4096 row and round 2's T6 as its control (16). My `spec_t6stage.py` cannot apply, because T6's old staging line is gone; the gate's T6-timed row is its replacement | **Closed** |
| R437-2 S1 (SUGGESTION): drain bound | BABBLE | 358/0: the restore behind a babbling READ is answered | **Taken** (gaps: F1) |
| R437-2 S2 / R437-1 S2 (SUGGESTION): a late grant carrying err | X20 | Fails T24 (2) under six of the seven legal models at 100 and 37; row D31 = 2. Under the unsolicited model the model's own stray done ends the wrongly owed command first, so X20 is 0 there. Mutation rows are graded under pristine | **Taken** |
| R436-2 F1 (MINOR): Q1 and Q9 | the gate's rows, with R436-2's exact text; Y1 and Y16 as the same defects | Q1 2 (T30a, RW4), Q9 4 (T30c-e, RW4), Q1/fuzz 4, Q9/fuzz 4 | **Closed** |
| R436-2 S1 (SUGGESTION) | as R437-2 S1 | | **Taken** |
| R436-2 R1, R2 (RESIDUE) | - | README `:479` reads "T24, T28 and T29 grade all of it". T29 names the 11th and 21st bytes (`:545-546`), and so does the PR body's Round 2 item 4 | **Closed** |
| R437-1 R2-R5 (RESIDUE) | - | present | Retained (section 3) |
| Round-1 probes (W15, W15b, W16, X12, X17, X18, X24, X24b, P1, W6) | `spec_r1_reprobe.py` | W15 T28a; W15b T28b; W16 and X18 T28d, T28f (and T24 at 37); X12 T28c, RW3; X17 T28e; X24 T28a; X24b T28a, T28b; P1's head 0; W6 T24, T30a, T30b, RW4 | Remain closed |

My other round-2 plants all fail named checks at 100 and 37: Y2, Y5-Y10 and Y13-Y15. Y3, Y4 and Y12 are 0, and are equivalent as argued in round 2 and in the README's table.

## 5. Judgement on the delta items

1. **T30 and the randomized harness.**
   - T30a-e are bus-staged: no silence is armed in (a)-(d), so RW4 grades them. They hit exactly the bound cycle (`mgr_drop_gap` = `TMO` + 1; `gap_drops` is required to be 1), and they pin the exemption and the verdict as the README says.
   - `fuzz_main.cpp` is independent of the suite: it has its own device, its own manager, and its own owed-cycle oracle from the banner. Its legal device is contract-legal, with every owed event at most `TMO` cycles after the previous one, biased to exactly `TMO`.
   - **A false DEADLINE against a legal device fails the suite.** Every false-DEADLINE plant I ran fails FZ2 at 1, 2, 3 and 37, and `make run` then fails: Y1, Y2, Y5, Y6, Y7, Y11, Y16, and a verdict one cycle early. FZ1-FZ9 are one check each, so the tally is stable.
   - The head's harness is 9/9 at every bound from 1 to 19, and at 37, 100 and 1,000.
2. **The 20 floor.**
   - With only the assert removed, the suite is green at 19 and fails at 15 and 10 (2 each, harness fixed delays: T4, T6, T19, T20) and at 5 (24-25).
   - So 20 is a conservative floor of the harness, not of the port. The port at 4-19 is shown by my harness runs; the standing gate builds 1, 2, 3 and 37.
   - The claim "builds at 100, 37 and 20, 1-3 covered by the randomized harness" holds as stated.
3. **T6.** The poke now waits for the ERASE to be accepted and not done (`sim_main.cpp:1035-1037`), inside the commit at every bound and model; see F3's closure above.
4. **The drain bound (item 2).**
   - **Contract.** A READ owes at most `dev_len_o`, which the port itself issued. `left_w` takes it less the bytes that moved: `hidx_r` and `bcnt_r` are exact at the deadline, because `dl_w` implies `!prog_w`, so no byte moves in that cycle. A request state's full length covers the late-grant path. A wait state owes 0 (`dev_len_o` is 0 there).
   - The count is taken only while nothing is owed, and decremented only on a drained handshake. Bytes past it are not taken (`dev_rready_o` falls), so they are not progress, and a waiting request ends DEADLINE.
   - **No legal device is refused:** ZD1-ZD4, the legal models at 20 to 100,000, and FZ1-FZ4 at 1 to 1,000.
   - The 16 bits suffice: `MAX_PAYLOAD_P` ≤ 65527.
   - The cost reproduces: +51 LUT, +16 FF and +9 CARRY4 at the default. No port and no parameter was added (the STOP rule is respected).
   - The test gap is F1.
5. **The late grant carrying err.** `:317`, `lg_r && dev_gnt_i && !dev_done_i && !dev_err_i`. T24's new arm checks DEADLINE, one late grant and one grant+err pair, then the next commit served with two ops. D31 = 2.
6. **The merges.** The merge base is `631eeb34`.
   - The two sides share only 01, 07, 09 and the integrator guide. In each of those, the lane's hunks against `c74711d4` are byte-identical to its hunks against the base. Every file only one side changed equals that side.
   - The eight #146 drivers, `tb/common/mutant_pool.py` and their READMEs equal main. `git diff c74711d4 HEAD -- tb/pp_top tb/acmp_talker tb/adp_engine tb/maap tb/srp_admission tb/srp_top tb/common tb/desc_store hdl/aecp` is empty.
   - 09 §8.5 is C8's "The descriptor model lint". This lane's section is §8.6 (`:323`). §8.2 keeps main's D3C text and points to "§8.6's" (`:215`).
   - Every `09 §8.5` citation in the tree (00, 07, `tb/desc_store`) names C8's section. No file cites this lane's section by its old number. The links gate passes (1,060).
7. **Line citations.** Every `KL_pp_nvm_port.sv:` citation in the tree and the PR body's Round 3 citations resolve to the cited text at this head.

**The issues against their own acceptance lists:**

| Issue | Status |
|---|---|
| #15 | Met (ruling (c), both branches) |
| #18, #19, #20 | Met as in rounds 1 and 2 |
| #21 | Met |

F1 is a test-coverage gap in a refusal that no acceptance item depends on, so it changes no issue's acceptance verdict.

## 6. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #15/#18-#21 acceptance; ruling 5952386396; round-3 assignment (items, gates, STOP rule); banner `:69-107`; 02 §8 `:530-555`; F08.1/F01.5 rows unchanged; parent patches unchanged (sha256 equal to rounds 1 and 2); the drain bound against "a READ owes at most its length" (ZD1-ZD4, FZ1-FZ4, seven legal models at 20 to 100,000) | R437-3 | 527662d659b4ead97675744d12a43af1ea92b9b3 |
| RTL | CLEAN | `KL_pp_nvm_port.sv` delta (`owed_left_r`, `left_w`, `drain_w`, late-grant err term) read in full context; lint at default, 1, 2, 3, 37, 2^31-1 and `MAX_PAYLOAD_P` 65527, 2^31 refused; arbiter and top lint; OOC cost at four settings against round 2 | R437-3 | 527662d659b4ead97675744d12a43af1ea92b9b3 |
| Robustness | CLEAN | Babbling backend (BABBLE, ZD1-ZD3, FZ9); late-ending large READ (ZD4); late grant with err; 13 drain plants × 6 suite cells + 3 harness bounds; harness at 1-19, 37, 100 and 1,000 | R437-3 | 527662d659b4ead97675744d12a43af1ea92b9b3 |
| Tests | UNCLEAN (F1) | `tb/nvm_port` (1,104), `tb/acmp_nvm` (388), figures gate (129 builds, rc 0 in a clone), T30, T28f, T24's late-grant err arm, `fuzz_main.cpp`, `deadline_rows.py`; my round-2 Y/Z probes, the round-1 probes, the bound sweeps and the floor probe; drain plants B1-B13 and ZD1-ZD4 | R437-3 | 527662d659b4ead97675744d12a43af1ea92b9b3 |
| Docs | UNCLEAN (F1's coverage claim at 09 §8.6 `:341`); R2-R5 residue | The `tb/nvm_port` README (T24, T28f, T29, T30, the D and plant tables, "Three bounds", "The randomized harness"), 02 §8, the banner, 09 §8.2/§8.5/§8.6 after the merge, the PR body's Round 3 section and its line citations, `make check` | R437-3 | 527662d659b4ead97675744d12a43af1ea92b9b3 |

## 7. Real limits

- **Not run by me, by scope:**
  - `run_suites.sh`; `lint_hdl.sh` over all 41 modules; `syn/yosys/run.sh`;
  - the CI mutation campaigns (including #146's eight drivers, whose files I verified equal main);
  - the donor bank and the parent consumer set;
  - act or hosted reproduction; Vivado.

  I rely on the manager's public evidence for these.
- **Hosted `suites`** was still in progress at my snapshot.
- **Device models are models.** No real backend or flash was run. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Formal coverage.** No formal proof was run this round. D23's invariant (round 2) is unaffected: the delta does not change where `owed_r` is set.
- **The randomized harness is seeded** (seeds 11-13). Its results are reproducible, not exhaustive.
- **The figures gate needs a git clone.** Its pre-fix matrix reads history, so on an export it fails on those pins alone. I ran it in a clone; the author ran it in the lane tree.
- **Probe hygiene.** The gate run in a clone, and my probe driver's import of the gate module, leave an ignored `tb/nvm_port/__pycache__/`. The one in the review clone was removed before the final integrity check.
- **`spec_fuzz.rc`** was written by hand (0) after its driver completed: the queue that ran it was stopped and its remaining specs were split into two queues. The JSON and per-job logs are complete.

## 8. Pending manager duties

- Run the donor bank (9) and the parent consumer set (16) at dev `cdf49d1a` with `parent-adoption-c4c6-ea3fb388.patch`, then C8's `parent-adoption-c8-cdf49d1a.patch`, then `parent-adoption-p2-cdf49d1a.patch`. Main carries C8, and the PR body reports that gates 10 and 15 fail without C8's patch.
- Hosted and act acceptance at the exact head; `suites` was still running at my snapshot.
- The final current-dev candidate at the merge turn (source base `c74711d4`, live dev `cdf49d1a`).
- Route F1 to the author, then re-review. Re-run `scripts/spec_drain.py` and `scripts/spec_zdrain.py` through `scripts/probe.py`, and `make -C tb/nvm_port figures` in a clone.
- Carry R2-R5 to the residue checklist.

## Receipts

Every published receipt is listed in `MANIFEST.sha256`. Home-directory prefixes in build logs are redacted as `<home>/`.

- `scripts/probe.py` is the driver. Each job takes a `git archive` copy of the head, applies exact-once edits, and builds with the Makefile's flags at `-GMEM_TIMEOUT_CYC_P`/`-DNVM_PORT_TMO`. A probe named `FZ:` builds `fuzz_main.cpp`. The model edits are imported from the head's `measure_figures.py`.
- The probe definitions:
  - `scripts/spec_drain.py` (B plants), `spec_zdrain.py` (ZD checks), `spec_fuzz.py`, `spec_floor.py` and `spec_r3_rerun.py`;
  - `scripts/r2/` holds my round-2 specs, unchanged.
- `scripts/summarize.py` tabulates results, and `scripts/anchor_check.py` checks that each anchor occurs exactly once.
- `scripts/baseline.sh` runs the suites, the gate and `make check`; `scripts/run_queue.sh` sequences specs.
- `scripts/ooc_cost.sh` measures the out-of-context cost, and `scripts/lint_changed.sh` runs the lint.

R437-3 FINISHED
