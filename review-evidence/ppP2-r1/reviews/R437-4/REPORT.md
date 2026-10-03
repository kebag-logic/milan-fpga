[R437] POSITIVE - exact head 3957814550f164d72bfaad5d28cd0e7cac0ecaaf

# R437-4: external delta review of PR #145 (lane P2, NVM port robustness)

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan. Issue #15, lane P2 (#15, #18, #19, #20 and #21; the PR closes all five).
- **Head:** `3957814550f164d72bfaad5d28cd0e7cac0ecaaf`, tree `a09432d236078129056d8b198e581b6ba77fdc6a`.
  - Three lane commits on round 3's `527662d6`:
    - `f879a26`: T28g-k, the randomized harness and the gate rows;
    - `a691e0e`: residue R2-R4;
    - `3957814`: FZ10's message.
  - There is no merge this round. Main is still `c74711d4` (re-checked during this review), and the head contains it.
- **Scope:** round 4 (assignment 5963997438), which answers R436-3 and R437-3. Both were NEGATIVE on the same MINOR: the drain bound was pinned in one branch, and its width was not graded.
- **Clone:** isolated and detached. At the end it was verified byte-exact at the head (`receipts/clone_integrity.txt`):
  - `write-tree` equals `a09432d2`, and the porcelain is empty, ignored files included;
  - the index's modes and blobs equal the HEAD tree;
  - there are no gitlinks and no `.gitmodules`, so no submodule pin is required.
- **Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open, and all five lenses are clean.
  - **My round-3 F1 is closed at its original severity (MINOR):**
    - every one of my 13 drain plants, run unchanged, fails a named suite check in all six cells (pristine and coincident completion, at 100, 37 and 20);
    - the five that survived round 3 now fail T28g (B6, B6b), T28h (B8), T28i (B7) and T28j (B10);
    - B12, which I had measured equivalent, fails T28k.
  - **R436-3's F1 is closed** under the same rule. Its Z1-Z12 and Z10b, byte-identical to its published `plants_drain.py`, each fail a named check in all six cells.
  - **The count's width is graded to its full 16 bits:**
    - my new 11-, 12- and 15-bit plants pass the suite but fail the harness's FZ7 and FZ10, because the harness is built at `MAX_PAYLOAD_P` = 65,527;
    - the 8-bit and 10-bit plants fail T28j as well.
  - **No contract-legal device is refused:**
    - the seven legal models pass 393/393 at bounds 20, 21, 37, 100, 1,000 and 4,096 (42 builds);
    - the harness passes 10/10 at bounds 1, 2, 3, 5, 19, 37 and 100.
  - The figures gate is rc 0: 160 builds, and every one of its 154 rows agrees.
  - One RESIDUE (R1, wording) and one SUGGESTION (S1) are recorded. Neither affects the verdict.

## 1. Reconstruction (order followed)

1. **Repository rules.** There is no AGENTS.md or CONTRIBUTING.md. I used `README.md` and `docs/README.md` (the single-source rules, and `make check` before any commit).
2. **Scope.**
   - Issue #15's body and its four acceptance items, and these manager comments:
     - the lane charter 5951891343;
     - the STOP ruling 5952386396 (the default, containment, ruling (c)'s reading of "serves the next request", and the parent's amended saved-state contract);
     - the round-4 assignment 5963997438 (item 1's six sub-items, residue item 2, main item 3, the gates, and the STOP rule);
     - REVIEW READY 5964850117.
   - On #145, the review start 5964859052.
3. **Authorities.**
   - The port banner's deadline section (`hdl/packet_engine/KL_pp_nvm_port.sv:69-107`) and the drain bound (`:286-327`). Neither changed this round: the blob is `a62788bb…` at both `527662d` and the head (`receipts/rtl_delta.txt`).
   - 02 §8, unchanged.
   - 09 §8.6's rows (`docs/architecture/09_verification.md:339` and `:342`).
   - The `tb/nvm_port` README: T28's bullet (`:543-567`), the D27-D30 rows (`:676-687`), the plant table (`:735-762`) and "The randomized harness" (`:802-860`).
   - `deadline_rows.py` (`DRAIN_PLANTS` at `:115-147`, `DRAIN_ON_FUZZ` at `:149`, D28a and D28b at `:211-212`).
   - `fuzz_main.cpp`: `largest_legal_length` `:385`, `one_babble` `:529`, `one_widest` `:578` and FZ10 `:671`.
   - `sim_main.cpp` T28g-k (`:2446-2611`).
   - The Makefile: `MAXP` and `FUZZ_MAXP` (`:21-22`), and `fuzz_at` (`:38`).
4. **The diff.**
   - `git diff c74711d4..3957814` (24 files), for context.
   - The round-4 delta, `git diff 527662d..3957814` (9 files), read in full. The only `hdl` change is R4's two port comments, word-diffed in `receipts/rtl_delta.txt`.
5. **Public evidence.**
   - milan-fpga `review-evidence/ppP2-r1/author-r4`, at archive commit `849311fe`. The tree linked in the assignment, `d56e2227`, is an ancestor of that archive, 10 commits behind it, and holds only round 1's `author/` directory.
   - All five `author-r4` files match `MANIFEST.json`'s `published_sha256` (`receipts/evidence_check.txt`).
   - The live PR body equals `author-r4/PR-BODY.md`, apart from one trailing blank line.
   - I did not read the lane's HANDOFF.
6. **Prior public findings.** I read them only after my verdict and ledger were drafted (`scratch`, not published): R436-3 (5963891560) and my own R437-3 (5963994045). Their resolution is in section 4.

## 2. Executed evidence (exact head; scoped Verilator 5.050, identity in `receipts/toolchain.txt`)

| Run | rc | Result |
|---|---:|---|
| `make -C tb/nvm_port` on a `git archive` export | 0 | The guard refuses 0, 2^31 and 2^32-1 by name, and builds 1 and 2^31-1. 393 + 393 + 393 at 100, 37 and 20, plus 10 at each of 1, 2, 3 and 37: **1,219/1,219**. Each harness build prints "the largest payload the port accepts, asked of it: 65527 bytes" (`receipts/nvm_port_make.log`) |
| `make -C tb/acmp_nvm` (export) | 0 | 372 + 16 = **388/388** |
| `make -C tb/nvm_port figures`, in a disposable local clone at the head | 0 | **160 builds.** Baseline 393/393. `make run` gives [(393,393,0)×3, (10,10,0)×4]. 154 rows `[ok ]`, 0 disagree, "all measured figures agree with the tree". Rows include D28a 2, D28b 1, B12 1, Z1/fuzz 1, Z10b/fuzz 3, Q9/fuzz 5, coincident/4096 0, T6-timed 16, short read 297/96 and silent 122/271 (`receipts/figures_gate.log`) |
| `make check`, in a disposable local clone | 0 | 41 mermaid + 18 WaveDrom; links 1,060; REQ 115 rows / 17 GAP; 94 module rows, 0 untested; parameters 28 = 28 = 28 |
| Lint with `lint_hdl.sh`'s flags over every `hdl` file | 0 | Clean on the port at the default, 1, 2, 3, 37, 2^31-1 and `MAX_PAYLOAD_P` 65527, with 2^31 refused by name. Clean on the arbiter, the top, and R4's two modules, `KL_acmp_nvm_shadow` and `KL_aecp_nvm_writer` (`receipts/lint_changed.txt`) |
| My round-3 plants B1-B13, `spec_drain.py` unchanged | 0 | The suite in six cells, and the harness at 1, 3 and 37: 126 jobs (`receipts/spec_drain/`). The harness again at 2: 14 jobs (`receipts/spec_r4c/`) |
| My round-3 directed checks ZD1-ZD4, `spec_zdrain.py` unchanged | 0 | The head and the six round-3 survivors, in six cells: 42 jobs (`receipts/spec_zdrain/`) |
| R436-3's Z1-Z12 and Z10b, read from the head's `DRAIN_PLANTS` and byte-identical to R436-3's published `plants_drain.py` (`receipts/plant_text_identity.txt`), through my own driver | 0 | The suite in six cells, and the harness at 1, 2, 3 and 37: 130 jobs (`receipts/spec_z/`) |
| New probes (`spec_r4.py`) | 0 | 85 jobs (`receipts/spec_r4/`): <br>• W10, W11, W12 and W15, the count narrowed to 10, 11, 12 and 15 bits; <br>• B14, a READ granted late not recorded as a READ; <br>• B15, the drain unbounded; <br>• the seven legal models at 20, 21, 37, 100, 1,000 and 4,096; <br>• the head's harness at 1, 2, 3, 5, 19, 37 and 100 |
| New probes of the harness itself (`spec_r4b.py`) | 0 | 12 jobs (`receipts/spec_r4b/`): <br>• H1, babble abandons at payload bytes only; <br>• H2, no READ of the widest payload; <br>• H3, no long records; <br>each against the head's port. Also the short-read and silent models at 20, 100 and 4,096 |
| Parent patches on milan-fpga dev `1269cdaf` (a depth-1 fetch into scratch) | 0 | c8 then p2 apply, and p2 also applies alone. p2 touches only `docs/design/SAVED_STATE_MATERIALIZATION.md`. c4c6 applies neither forward nor in reverse there, as expected: that dev carries its adaptation (`receipts/parent_patch_apply.txt`) |

**Hosted CI at the exact head** (snapshot 03:06Z, `receipts/hosted_checks_snapshot.txt`):

- `docs-gates` and `portability` succeeded on both runs.
- `suites` was still in progress on both.
- The manager owns hosted and act acceptance.

### 2.1 The drain plants at this head

Every suite count is identical in all six cells: pristine and coincident completion, at 100, 37 and 20. W and B14/B15 ran under pristine only.

| Plant | Suite (fails of 393) | Named by | Harness at 1, 2, 3 and 37 (fails of 10) |
|---|---:|---|---|
| B1 payload arm one short | 20 | T24, T28d-f, T28j, T30e | 3: FZ7, FZ9, FZ10 |
| B2 header arm one short | 19 | T24, T28g | 2: FZ7, FZ9 |
| B3 request arm one short | 22 | T24, T28i, T28j | 0 (late-grant branch) |
| B4 request arm zero | 22 | T24, T28i, T28j | 0 (late-grant branch) |
| B5 payload arm one over | 1 | T28f | 1: FZ9 |
| **B6** header arm one over | **2** | **T28g** | 1: FZ9 |
| **B6b** header arm, the whole 8 | **2** | **T28g** | 1: FZ9 |
| **B7** request arm one over | **2** | **T28i** | 0 (late-grant branch) |
| **B8** wait states owe 8 | **2** | **T28h** | 1: FZ9 |
| B9 decrement unguarded | 15 | T28f-i, RW1 | 1: FZ9 |
| **B10** count 8 bits | **3** | **T28j** | 3: FZ7, FZ9, FZ10 |
| **B12** drain for any owed command | **1** | **T28k** | 0 |
| B13 count loaded only for an owned command | 22 | T24, T28i, T28j | 0 (late-grant branch) |
| W10 count 10 bits (new) | 2 | T28j | 2: FZ7, FZ10 (at 1, 3 and 37) |
| **W11, W12 and W15**, count 11, 12 and 15 bits (new) | 0 | none (the suite's READs owe at most 1,024) | **2: FZ7, FZ10** (at 1, 3 and 37) |
| B14 a late-granted READ not recorded as a READ (new) | 22 | T24, T28i, T28j | 0 (late-grant branch) |
| B15 drain unbounded (new; D27's defect) | 15 | T28f-i, RW1 | 1: FZ9 |
| Z1 / Z2 / Z3 / Z4 / Z5 / Z6 / Z7 | 2 / 1 / 2 / 22 / 1 / 20 / 19 | T28g / T28f / T28h / T24, T28i-j / T28f / T24, T28d-f, T28j, T30e / T24, T28g | 1 / 1 / 1 / 0 / 1 / 3 / 2 |
| Z8 / Z9 / Z10 / Z11 / Z10b / Z12 | 2 / 15 / 3 / 15 / 3 / 27 | T28g / T28f-i, RW1 / T28j / T28f-i, RW1 / T28j / T24, T28h-j, RW1 | 1 / 1 / 3 / 1 / 3 / 1 |

- **The head:** 0/393 in every cell, and 10/10 at every harness bound.
- **ZD1-ZD4:** they still pass on the head (409/409 in six cells). Each round-3 survivor now fails a T28 check beside my ZD check:
  - B6 and B6b fail T28g and ZD1;
  - B7 fails T28i and ZD3;
  - B8 fails T28h and ZD2;
  - B10 fails T28j and ZD4;
  - B12 fails T28k.
- **Agreement with the tree:** every suite and harness figure for B1-B13 and Z1-Z12/Z10b equals the README's plant table (`:735-762`) and its harness paragraph (`:852-860`).
- **Harness failures:** in every failing harness run, the failure is FZ7, FZ9 or FZ10, never FZ1-FZ4. No plant here makes a legal device refused.
- **FZ10 checks reach:** H1, H2 and H3 each fail FZ10 alone, at 3 and 37. So FZ10 fails if babble never abandons at a header byte or terminal, if no READ of the widest payload is abandoned, or if no long record is drawn.
- **The broken models:** short read gives 297/96 and silent 122/271 at 20, 100 and 4,096, with no RW check failing.

## 3. Findings

No BLOCKER, MAJOR or MINOR finding is open.

### R1 - RESIDUE - Docs: one sentence over-states which round-3 plants now fail the harness

- **Where:** `tb/nvm_port/README.md:852-853`: "The round-3 plants that passed the harness fail it now at every bound it is built at;".
- **Evidence:**
  - B7 and B12 passed round 3's harness, and both still pass it at 1, 2, 3 and 37 (`receipts/spec_drain/`, `receipts/spec_r4c/`).
  - The paragraph's last sentence (`:857-860`) states it correctly: "The plants in the late grant's branch (Z4, B3, B4, B7 and B13) and B12 pass it".
- **Why it is residue:**
  - No figure, gate row, check, code or claim of coverage moves.
  - The gate rows `Z1/fuzz`, `Z3/fuzz`, `Z8/fuzz` and `Z10b/fuzz` measure as stated.
  - The suite fails both plants (T28i and T28k).
- **Exact fix:** replace "The round-3 plants that passed the harness fail it now at every bound it is built at;" with "The round-3 plants that passed the harness, but for those named in the last sentence, fail it now at every bound it is built at;".

### S1 - SUGGESTION - Tests: pin the harness's half of the width as a gate row

- **What:** the suite's T28j grades the count's width only up to the suite's `MAX_PAYLOAD_P` of 1,024, because 11 bits hold it. The 11- to 16-bit range is graded only by the harness's `one_widest` (FZ7, FZ10), as the README's T28j bullet says.
- **Suggestion:** add a figures-gate row for a lint-clean width plant past 11 bits on the harness, for example W15 (`scripts/spec_r4.py`), as `Z10b/fuzz` does for 8 bits. That would fix the expected count against a later edit of `one_widest`.
- **Why it is optional:** today that edit is caught by FZ10's reach check (H2). Not required.

## 4. Prior public findings at this head

| Finding (severity) | Evidence at this head | Status |
|---|---|---|
| **R437-3 F1 (MINOR):** drain bound graded in one arm; width ungraded | My `spec_drain.py` and `spec_zdrain.py`, unchanged; only `probe.py`'s head pin and the harness's payload bound (the Makefile's `FUZZ_MAXP`) changed. All 13 B plants fail named checks in six cells (section 2.1). The required ZD1-ZD4 properties are now standing: ZD1 is T28g, ZD2 is T28h, ZD3 is T28i, and ZD4 is T28j with 590 owed. Each is a gate row with my exact edit text (byte-identical, `receipts/plant_text_identity.txt`). 09 §8.6 `:342` and the README name them. Gate rc 0 in a clone | **Closed** (MINOR) |
| **R436-3 F1 (MINOR):** Z1, Z3, Z8 and Z10b pass every check | Its exact plant text: Z1 fails T28g, Z3 T28h, Z8 T28g and Z10b T28j, in six cells. On the harness at 1, 2, 3 and 37, Z1, Z3 and Z8 fail FZ9, and Z10b fails FZ7, FZ9 and FZ10. Its two example probes are now standing: FZ9 abandons at any header byte, payload byte or terminal (`fuzz_main.cpp:542-546`), and FZ7 draws long records and the widest one. D28 is split (D28a 2, D28b 1) | **Closed** (MINOR) |
| **R436-3 R1 (RESIDUE):** the PR body's Round 3 parent-visible item 3 | The live body `:764-766` carries the exact fix text | **Closed** |
| **R437-1 R2-R5 (RESIDUE)**, carried by R437-3 and R436-3 | R2: README `:1135` and `:1142`. R3: `sim_main.cpp:1164-1165` and `:1250`. R4: `KL_acmp_nvm_shadow.sv:208` and `KL_aecp_nvm_writer.sv:260`, comment only. R5: `parent-adoption-p2-cdf49d1a.patch` `590f791d…`, which adds exactly one hunk (the row at `SAVED_STATE_MATERIALIZATION.md:1930`, now "section 8.8; section 15 item 4 (amended)"); it is docs only and applies after c8 on dev `1269cdaf`. Each is my round-1 text | **Closed** |
| R436-2 F1, R437-2 F1-F3, R437-1 and R436-1 findings, and their suggestions | Closed or taken at round 3. The port RTL is byte-identical since then. Their gate rows all measure as the README states in my gate run: Q1-Q10, Y1-Y16, Q1/fuzz, Q9/fuzz, D18-D31 (X20 = D31), T6-timed/coincident/4096 and coincident/4096 | **Remain closed** |

## 5. Judgement on the delta items

1. **Item 1: every branch of the drain bound.**
   - **Contract.** The bound is unchanged and correct, as round 3 found:
     - a READ owes its length less the bytes that moved;
     - a request state owes the whole length (the late grant), and a wait state owes 0;
     - a WRITE owes no read byte.

     T28k's device, which presents read bytes for an owed WRITE, is a broken backend. Refusing it follows the banner's "drains the bytes an owed READ still owes and no more", so B12 is no longer untestable. It is killed by a broken-device check, not by any legal device.
   - **Each sub-item is met:**
     - `S_RHCOLL`: T28g, after 3 bytes and after 7.
     - The wait states: T28h, both `S_RHWAIT` and `S_RPWAIT`.
     - The width: T28j, with 590 owed, and 1,024 both abandoned and late-granted. The harness serves a READ owing 65,527 in every seed, which my W11-W15 show is what grades the upper bits.
     - D28 is split.
     - The harness is extended: H1-H3 show that FZ10 enforces the extension's reach.
     - Every plant of both packets is a gate row in the reviewer's own text.
     - No legal device is refused.
   - **The late-grant branch** is graded by the suite alone (T28i, T28j's third arm), because the harness's device grants only while a request is up. The README states this (`:857-860`), and B3, B4, B7, B13 and B14 all fail the suite.
   - **T28j's pacing** (a byte every `TMO`/2 until the restore is issued) keeps a late-granted READ owing almost all of its length at every bound. I checked it at 4,096 under all seven legal models (0 FAIL).
2. **Item 2: residue.**
   - R436-3 R1 and R437-1 R2-R5 are each in the reviewer's exact text.
   - The two RTL hunks are comments; lint is clean on both modules.
   - The p2 patch's new hunk is one documentation table row.
3. **Item 3: main.**
   - Main is `c74711d4`, and the head contains it.
   - The STOP rule held: no port, parameter or RTL logic changed. The out-of-context cost therefore stands at round 3's measurement (296 LUT, 164 FF, 30 CARRY4 at the default) on identical bytes.
4. **Commit `3957814`** changes only FZ10's message text, so that it names no other check ID. FZ10 passes at every bound I built.
5. **Line citations.** The PR body's Round 4 citations resolve at this head: `KL_pp_nvm_port.sv:222` and `:293-295` (the assignment's), and `sim_main` T28g-k.
6. **The issues against their own acceptance lists:** #15 is met (ruling (c), both branches). #18, #19, #20 and #21 are met, as in rounds 1-3. Nothing this round changes an acceptance verdict.

## 6. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Acceptance of #15 and #18-#21; ruling 5952386396; the round-4 assignment (items 1-3, the gates, the STOP rule, respected); the banner `:69-107` and 02 §8 against the bound's four branches and its width; the seven legal models at 20 to 4,096; the harness at 1 to 100; the p2 patch (R5, docs only, applies after c8 on dev `1269cdaf`) | R437-4 | 3957814550f164d72bfaad5d28cd0e7cac0ecaaf |
| RTL | CLEAN | The `KL_pp_nvm_port.sv` blob, identical to round 3 (`a62788bb`); R4's two comment-only hunks; lint of the port at 7 settings (2^31 refused), the arbiter, the top and R4's two modules; round 3's cost stands on identical bytes | R437-4 | 3957814550f164d72bfaad5d28cd0e7cac0ecaaf |
| Robustness | CLEAN | A babbling backend in every branch (T28g-k; ZD1-ZD3; FZ9 at header bytes, payload bytes and terminals); a large abandoned READ ended at a legal pace (T28j, ZD4, `one_widest` at 65,527); the late grant (T28i, B14); short read and silent at 20, 100 and 4,096 with every RW check passing | R437-4 | 3957814550f164d72bfaad5d28cd0e7cac0ecaaf |
| Tests | CLEAN | `tb/nvm_port` (1,219); `tb/acmp_nvm` (388); the figures gate in a clone (160 builds, rc 0); T28g-k; `fuzz_main.cpp` (`one_babble`, `one_widest`, `largest_legal_length`, FZ10); `deadline_rows.py`; B1-B13 and ZD1-ZD4 unchanged; Z1-Z12 and Z10b in R436-3's exact text; W10-W15, B14 and B15; H1-H3 against FZ10 (409 probe builds in all) | R437-4 | 3957814550f164d72bfaad5d28cd0e7cac0ecaaf |
| Docs | CLEAN (R1 is residue) | The `tb/nvm_port` README (T28 bullet, D rows, plant table, harness section, header prose); the Makefile's comments; 09 §8.6 `:326-342`; the PR body's Round 4 section and its parent-visible list; R2-R5 at their locations; `make check` | R437-4 | 3957814550f164d72bfaad5d28cd0e7cac0ecaaf |

## 7. Real limits

- **Not run by me, by scope:**
  - `run_suites.sh`; `lint_hdl.sh` as a whole (I ran its flags on the changed and dependent tops);
  - `syn/yosys/run.sh`; the CI mutation campaigns that build `tb/pp_top`;
  - the donor bank and the parent consumer set;
  - act or hosted reproduction; Vivado; the out-of-context re-measurement (the bytes are identical to round 3's, which I measured).

  I rely on the manager's public evidence for these.
- **Hosted `suites`** was still in progress at my snapshot.
- **Device models are models.** No real backend or flash was run. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **The harness is seeded** (its three fixed seeds). Its results are reproducible, not exhaustive. Its late-grant branch is not reachable by its own device. The suite covers that branch.
- **R436-3's own drivers were not run.** Those are `run_plant.sh` and its R436g and R436h scripts. Its plant text was run instead, byte for byte, through my driver and through the gate. R436g's and R436h's properties are now standing harness behaviour, which H1 and H3 show FZ10 enforces.
- **The evidence link.** The tree linked in the assignment (`d56e2227`) predates the round-4 archive. I used the archive commit `849311fe`, which the assignment also names.
- **Process hygiene:**
  - My first figures-gate run was still running when I mistakenly started a second into the same scratch directory. I stopped both (my own processes only) and ran the gate once, cleanly, from a fresh clone. The rc 0 recorded is that clean run's.
  - After the runs, two script edits were made for portability. `spec_z.py` now takes the repository from `probe.py`'s `--repo`, where it had been hard-coded; `probe.py` passes it. No semantics changed.
  - The disposable gate clone left an ignored `__pycache__` there. The review clone has none.

## 8. Pending manager duties

- **The donor bank (9) and the parent consumer set (16)** at dev `1269cdaf`, with `parent-adoption-c8-cdf49d1a.patch` then `parent-adoption-p2-cdf49d1a.patch` (`590f791d…`). c4c6 does not apply on that dev, because the dev already carries it. The PR body's Round 4 parent-visible item 2 names the chain at `cdf49d1a` (c4c6, then C8, then p2).
- **Hosted and act acceptance** at the exact head. `suites` was still running at my snapshot.
- **The final current-dev candidate** at the merge turn (source base `c74711d4`, live dev `1269cdaf`).
- **Carry R1 to the residue checklist.**

## Receipts

Every published receipt is listed in `MANIFEST.sha256`.

- `scripts/probe.py` is the driver. Each job takes a `git archive` copy of the head and applies exact-once edits. It builds with the Makefile's flags: the suite at `MAX_PAYLOAD_P` 1,024, and the harness (probes named `FZ:`) at 65,527, with `-GMEM_TIMEOUT_CYC_P` and `-DNVM_PORT_TMO`. The model edits are imported from the head's `measure_figures.py`.
- The probe definitions:
  - `spec_drain.py` and `spec_zdrain.py` are round 3's, unchanged;
  - `spec_z.py` holds the gate's Z rows;
  - `spec_r4.py`, `spec_r4b.py` and `spec_r4c.py` are this round's.
- `scripts/summarize.py` writes each `SUMMARY.txt`. `scripts/baseline.sh` runs the suites, the gate and `make check`. `scripts/run_queue.sh` sequences the specs, and `scripts/lint_changed.sh` runs the lint.
- Home-directory prefixes in build logs are redacted as `<home>/`.

R437-4 FINISHED
