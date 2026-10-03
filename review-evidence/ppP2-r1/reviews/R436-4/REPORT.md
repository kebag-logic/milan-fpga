[R436] POSITIVE - exact head 3957814550f164d72bfaad5d28cd0e7cac0ecaaf

# R436-4: internal independent delta review of PR #145 (lane P2, NVM port robustness)

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan, issue #15, PR #145.
- **Exact head:** `3957814550f164d72bfaad5d28cd0e7cac0ecaaf`, tree `a09432d236078129056d8b198e581b6ba77fdc6a`.
- **Base:** `c74711d45a8bbc0d6b38cb49211b26a4a6413e88`.
- **Round-4 delta:** three commits on `527662d6`:
  - `f879a26`: T28g-k, the harness changes, FZ10, D28a/D28b, and the plant rows;
  - `a691e0e`: R437-1's residue R2-R4;
  - `3957814`: FZ10's message.
- **Scope of this review:** the round-4 assignment (#15 comment 5963997438). The author's packet is `review-evidence/ppP2-r1/author-r4` at milan-fpga `849311fe`. Its `PR-BODY.md` is byte-identical to the live PR body.
- **Toolchain:** the pinned simulator 5.050 wrapper, sha256 `905795b9…e92f`, is the same as in R436-3 (`receipts/verilator_identity.txt`).
- **Clone integrity:** the clone is unchanged after every probe. HEAD and tree are exact, with 0 status entries (ignored files included) and index blobs and modes equal to the HEAD tree (482 entries). No worktree byte differs. The repository has no submodule gitlinks (`receipts/clone_integrity.txt`). Every probe ran in a `git archive` extraction under `scratch/`.

## Verdict

**POSITIVE.**

- **R436-3 F1 is closed** at its original severity, MINOR.
  - All 13 of my round-3 drain plants, run unchanged, now fail a named check. These include the four that passed every check in round 3: Z1, Z3, Z8 and Z10b.
  - My own new width plants also fail named checks: the count at 9 to 15 bits.
  - The harness's 65,527-byte READ is what pins widths 11 to 15. The suite alone cannot, since it never owes more than 1,024.
- **No contract-legal device is refused:**
  - the seven legal models are 393/0 at 20, 21, 37, 100, 1,000 and 4,096;
  - the harness is 10/10 at ten legal bounds and at both payload bounds (1,024 and 65,527).
- **Residue:** R436-3 R1 and R437-1 R2-R5 are taken in the reviewers' exact text. R5 is docs-only, and it applies after C8's patch at milan-fpga dev `1269cdaf`.
- **One new RESIDUE (R1)**, wording only.

## Delta reviewed

**1. RTL.**
- `KL_pp_nvm_port.sv` is byte-identical to `527662d` (`git diff --quiet`).
- The only `hdl` edits are R4's two port comments. Both files are identical to round 3 with comments stripped (`receipts/r4_comment_only.txt`).
- The round-3 drain bound I traced in R436-3 is unchanged (`KL_pp_nvm_port.sv:290-327`):
  - `left_w` is `HDR_LEN_C - hidx_r` in `S_RHCOLL`, `plen_r - bcnt_r` in `S_RPPUMP`, and `dev_len_o` elsewhere. That is 0 in the wait states and the full length for a late grant.
  - The count is 16 bits wide. With `MAX_PAYLOAD_P` at most 65,527, `dev_len_o` never exceeds 65,535, so 16 bits is exactly enough.

**2. Tests** (`tb/nvm_port/sim_main.cpp:2446-2611`, `fuzz_main.cpp`, `Makefile`).
- T28g: a header READ abandoned in `S_RHCOLL` after 3 and after 7 bytes. 5 and 1 are drained, then DEADLINE `TMO` + 2 after the last owed byte.
- T28h: a READ abandoned in `S_RHWAIT` or `S_RPWAIT`, with every byte moved. None is drained.
- T28i: a header READ and a payload READ granted late. 8 and 40 are drained.
- T28k: a WRITE granted late. No read byte is taken, and the device's own err then ends it.
- T28j: a READ owing 590, then one owing 1,024, abandoned and granted late. Each is resumed at legal pace, and the waiting restore is served byte-exact.
- Every arm then has the device end the command and checks that the next operation is served.
- The harness:
  - is built at `MAX_PAYLOAD_P` = 65,527 and finds that bound by binary search on the port, not from the Makefile;
  - has babble abandon at header bytes, payload bytes and terminals;
  - draws half of its resume and babble records long;
  - in every seed, abandons a READ owing 65,527 bytes and serves the restore behind it;
  - has FZ10 require that every branch was reached.
- I read each new check's pass condition against the banner (`KL_pp_nvm_port.sv:84-107`) and 02 §8. Each grades the property it names.

**3. Gate.**
- `deadline_rows.py` splits D28 into D28a (header) and D28b (payload).
- It adds every round-3 plant of both reviews as a row, with the reviewer's own text, and Z1/Z3/Z8/Z10b again on the harness.
- My 13 Z texts are byte-identical to `plants_drain.py` (`receipts/rows_vs_plants.txt`).

**4. Docs.**
- 09 §8.6 rows, the README's T28/harness/plant sections and header, the Makefile comment, and the PR body's Round 4.
- No 02 §8 or banner change.

## Findings

### R1 - RESIDUE - Docs (wording only)

- **Where:** `docs/architecture/09_verification.md:342`, the coverage cell "the round-3 reviews' plants Z1-Z12, Z10b and B1-B13".
- **Problem:** the second review's plant labels skip B11 and add B6b. The README states this at the same claim (`tb/nvm_port/README.md:726`: "R437-3's B1-B13 (B6b beside B6, no B11)"), but the normative row does not.
- **Why it is only wording:**
  - the set of plants the gate grades is unchanged;
  - every row the label range denotes is measured (`receipts/figures.log`: B1-B10, B6b, B12, B13 all equal the README);
  - no figure, check or claim moves.
- **Exact fix:** in `docs/architecture/09_verification.md:342`, replace "Z1-Z12, Z10b and B1-B13" with "Z1-Z12, Z10b and B1-B13 (B6b beside B6, no B11)". Optionally make the same edit to the module docstring at `tb/nvm_port/deadline_rows.py:24`.

No BLOCKER, MAJOR or MINOR is open.

## Prior public findings at this head

| Finding (severity) | Status at this head | Evidence |
|---|---|---|
| R436-3 F1 (MINOR): drain bound pinned in one branch; width ungraded | **Closed** | See the plant table below. Z1 and Z8 fail T28g; Z3 fails T28h; Z10b fails T28j (3 of 393), and on the harness FZ7, FZ9 and FZ10. Every other Z plant is killed by name (Z10 by the width lint, as in round 3). The figures gate measured Z1-Z12, Z10b, Z1/fuzz, Z3/fuzz, Z8/fuzz and Z10b/fuzz equal to the README. R436g (`babble_probe.sh`) and R436h (`resume_long_probe.sh`), run unchanged apart from the head pin, are clean on the head. They fail Z1, Z2, Z3 and Z8 (FZ9) and Z10b (FZ7) at every bound. |
| R436-3 R1 (RESIDUE): PR body's Round 3 parent-visible item 3 | **Closed** | The live PR body carries the exact fix text ("changed this round only to bound the drain by what the READ still owes; the patch's "drains an owed read's bytes" still holds…"). |
| R437-3 F1 (MINOR): same defect, plants B1-B13 | **Closed on my evidence**; the second review owns its own re-run | Every B row is a gate row and is measured non-zero by my figures run: B6 and B6b fail 2 (T28g), B7 2 (T28i), B8 2 (T28h), B10 3 (T28j), B12 1 (T28k), and B1-B5, B9 and B13 1-22 each. I did not run that review's `spec_drain.py` or `spec_zdrain.py`. |
| R437-1 R2 (RESIDUE): README coincident-model sentences | **Closed** | `tb/nvm_port/README.md:1135-1136` ("it was the first model here to vary the handshake for a whole run") and `:1141-1142` ("the pristine model, which keeps every accepted byte"), in the exact text. |
| R437-1 R3 (RESIDUE): T15/T16 comments | **Closed** | `tb/nvm_port/sim_main.cpp:1164-1165` ("A device err inside the WRITE leaves …") and `:1250` ("commit torn while writing one"). |
| R437-1 R4 (RESIDUE): managers' cause comments | **Closed** | `hdl/acmp/KL_acmp_nvm_shadow.sv:208` and `hdl/aecp/KL_aecp_nvm_writer.sv:260` append ", 3 DEADLINE (read as DEVICE)". Comment only: identical with comments stripped. Lint is clean, and `tb/acmp_nvm` is 388/0. |
| R437-1 R5 (RESIDUE): parent saved-state page §15 citation | **Closed** | See the parent patch section below. |

### The parent patch (R5)

- **Hash:** `parent-adoption-p2-cdf49d1a.patch` is sha256 `590f791d…f539fa`, 11,888 bytes.
- **Diff against round 1's** (`3dda8509…d08b`): exactly one new hunk, `@@ -1909,7 +1927,7 @@`. It replaces one table cell's "processor issue 15's open recovery contract" with "section 15 item 4 (amended)".
- **Scope:** it touches only `docs/design/SAVED_STATE_MATERIALIZATION.md`.
- **At milan-fpga dev `1269cdafb4bb964c757baae0f0c5a932d43f540b`:**
  - `parent-adoption-c8-cdf49d1a.patch` (sha256 `aa5a88eb…`) applies with rc 0;
  - p2 then checks and applies with rc 0;
  - p2 also applies alone.
- **The c4c6 patch neither applies nor reverse-applies at dev 1269cdaf.** That fits the assignment's statement that dev carries an *adaptation* of c4c6, not the patch text. The manager's parent run is the authority here (`receipts/parent_patch_check.txt`).

## Plants and probes (exact head)

Edit texts are in `scripts/plants_drain.py` (R436-3's, unchanged) and `scripts/plants_r4.py` (new). Raw logs are in `receipts/`, and the summary is in `receipts/drain_plants.md`.

| Plant | Defect | Standing `make run` | Named by |
|---|---|---|---|
| head | none | **1,219 / 1,219 PASS** (393 × 3 + 10 × 4), 45 s | - |
| Z1 / Z8 | `S_RHCOLL` owes 8 / one over | 2 of 393 each | T28g |
| Z3 | a wait state owes 8 | 2 of 393 | T28h |
| Z10b | count 8 bits, lint-clean | 3 of 393 | T28j |
| Z2, Z4-Z7, Z9, Z11, Z12 | see `receipts/drain_plants.md` | 1-27 of 393 | T24, T28d-j, T30e, RW1 |
| Z10 | count 8 bits, lint-unclean | `elab_bounds.sh` width lint | lint |
| W9 / W10 (new) | count 9 / 10 bits | 3 / 2 of 393 | T28j |
| W11-W15 (new) | count 11-15 bits | suite 393/0 at 100, 37 and 20; harness at bound 1 fails 2 of 10 | FZ7, FZ10 ("a restore behind a READ owing 65527 bytes … cause 3") |
| Y1 (new) | an abandoned WRITE taken as a READ | 1 of 393 | T28k (48 read bytes taken) |

**Legal devices** (`receipts/models_at_bounds/SUMMARY.txt`; `receipts/fuzz_extra_*.log`):
- Pristine, half-page, page-buffered NOR, lazy erase, lazy erase + page-buffered, coincident and unsolicited are each **393 PASS, 0 FAIL** at 20, 21, 37, 100, 1,000 and 4,096.
- Short read (297/96) and silent (122/271) fail service checks only. Every RW check passes under all nine models at all six bounds.
- The standing harness is 10/10:
  - at 1, 2, 3 and 37 in `make run`;
  - at 4, 5, 8, 19, 64 and 100 at `MAX_PAYLOAD_P` 65,527;
  - at 1, 3, 37 and 100 at 1,024.
- No false DEADLINE in any of these runs.

**Figures gate** (`scripts/run_figures.sh`; `receipts/figures.log`):
- 160 builds. Every measured row and figure agrees with the README:
  - 12 arms;
  - 126 mutations and probes, including D28a = 2, D28b = 1, every Z and B row, and Z1/Z3/Z8 = 1 and Z10b = 3 on the harness;
  - 10 models;
  - the 5-build matrix;
  - `make run` at 1,219/0.
- The run exited 1 only because its git-history pin checks (`pre_fix_forms.git_verbatim`) cannot read history in a `git archive` extraction.
- I ran that function alone, read-only, in the clone, with no bytecode written. It reports **0 problems** (`receipts/figures_git_pins_in_clone.txt`). So the gate's verdict at the head is clean.

**Other gates at the head:**
- `lint_hdl.sh`: 41 modules, LINT OK, rc 0.
- `make check`: lint, wavedrom, links 1,060, matrix 115 REQ / 17 GAP, module matrix 94 rows with 0 untested, parameters 28 = 28 = 28, rc 0.
- `tb/acmp_nvm`: 388 / 388.

## Issue-by-issue acceptance at this head

| Issue | Status | Evidence |
|---|---|---|
| #15 items 1-4 and ruling (c), both branches | MET (no RTL change since round 3) | T24 twelve states; T28a-k; T29; T30; FZ5-FZ8 at ten bounds; the elaboration guard; the silent model at six bounds |
| #18, #19, #20, #21 | MET (unchanged by round 4) | T25; `tb/acmp_nvm` 388; the gate's M/S/latch rows; the seven legal models at six bounds |

## Lens results

### Conformance (CLEAN)

- The round-4 assignment is followed:
  - item 1 in full: every branch of the bound pinned, D28 split, the harness extended, every plant a row;
  - item 2: the residue in exact text;
  - item 3: main is still `c74711d4`, which is contained in the head, so there was no merge.
- No port, parameter or RTL logic changed, so there was no STOP condition.
- The drain bound conforms to the banner (`KL_pp_nvm_port.sv:84-99`) and 02 §8. No legal device is refused.
- The p2 patch is docs-only and applies after C8's at dev `1269cdaf`.
- R1 is wording only.

### RTL (CLEAN)

- The port's bytes are identical to round 3's, which I traced in full in R436-3.
- The two manager edits are comment-only (verified).
- Lint is clean over 41 modules, and the elaboration guard holds.
- The 16-bit count width is now shown to be necessary as well as sufficient: W9-W15 each fail.
- The out-of-context cost is unchanged, because the bytes are unchanged. R436-3 measured it.

### Robustness (CLEAN)

- No false DEADLINE against any legal device or manager:
  - nine models at six bounds;
  - the harness at ten bounds and two payload bounds.
- A babbling backend is answered DEADLINE in every branch: header, payload, wait state, late grant, and an owed WRITE.
- Long abandoned READs, up to 65,527 bytes, are drained whole and the waiting request is served.

### Tests (CLEAN)

- 1,219 checks at the head.
- Every non-equivalent drain plant of mine fails a named check: 13 Z plants plus 8 new ones, with Z10 caught by the lint.
- The gate's 160 builds agree.
- FZ10 guards the harness's own reach.

### Docs (CLEAN; R1 residue)

- These agree with the measurements and the RTL:
  - the README's header, T28/harness/plant sections and plant table (every count equal to my runs);
  - 09 §8.6's rows;
  - the Makefile comment;
  - the PR body's Round 4.
- The R2-R5 residue is in the exact text.
- R1 (09's "B1-B13") is residue.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #15 body; comments 5951891343, 5952386396, 5961238126, 5963684192, 5963997438 and 5964850117; PR #145 body (Round 4; byte-identical to author-r4 at `849311fe`); banner `:84-107`; 02 §8; the three parent patches (sha256), the p2 hunk diff, and application at milan-fpga dev `1269cdaf` | R436-4 | 3957814550f164d72bfaad5d28cd0e7cac0ecaaf |
| RTL | CLEAN | `KL_pp_nvm_port.sv` (byte-identical to `527662d`; drain bound `:290-327` re-read); R4 manager comments (comment-only proof); `lint_hdl.sh` (41 modules); `elab_bounds.sh` via `make run`; width plants W9-W15 | R436-4 | 3957814550f164d72bfaad5d28cd0e7cac0ecaaf |
| Robustness | CLEAN | nine device models × six bounds; standing harness at 1-5, 8, 19, 37, 64 and 100 (65,527) and 1, 3, 37 and 100 (1,024); R436g and R436h on the head; T28g-k behaviour | R436-4 | 3957814550f164d72bfaad5d28cd0e7cac0ecaaf |
| Tests | CLEAN | `sim_main.cpp` T28g-k; `fuzz_main.cpp` (round-4 diff); Makefile; `deadline_rows.py` (Z texts byte-compared); R436-3 plants Z1-Z12 and Z10b unchanged; new W9-W15 and Y1; figures gate (160 builds) plus git pins in the clone; `tb/acmp_nvm` 388 | R436-4 | 3957814550f164d72bfaad5d28cd0e7cac0ecaaf |
| Docs | CLEAN (R1 residue) | `tb/nvm_port/README.md` (header, T28, harness, plant table, R2 lines); 09 §8.6 `:326-346`; `measure_figures.py` docstring and waiver; `deadline_rows.py` docstring; PR body Round 4 and Round 3 item 3; `make check` | R436-4 | 3957814550f164d72bfaad5d28cd0e7cac0ecaaf |

## Real limits

- **Not run here:**
  - the full `run_suites.sh` bank;
  - the mutation campaigns;
  - `syn/yosys/run.sh` and any out-of-context synthesis. The port's bytes are unchanged, so round 3's measured cost carries.
  - the donor bank (9) and the parent consumer set (16).

  For those I rely on the PR body's Round 4 table and the manager's banks. I ran the suites round 4 touches (`nvm_port`, and `acmp_nvm` for the R4 comments), lint, the docs gates and the figures gate.
- **The second review's scripts (`probe.py`, `spec_drain.py`, `spec_zdrain.py`) were not run.** Its B plants are graded here only through the gate's B rows, which my figures run measured.
- **The figures gate ran in a history-less extraction.** Its git-pin step was therefore run separately, read-only, in the clone (0 problems). The run's rc was 1 for that reason alone.
- **Hosted CI.** At my snapshot (03:17Z), `docs-gates` and `portability` were success and `suites` was in progress (`receipts/hosted_checks_snapshot.txt`). The manager owns hosted and act acceptance.
- **The randomized harnesses are models.** They use fixed seeds and are not proofs. R436g, R436h and W9-W15/Y1 are reviewer probes and are not proposed as the PR's code.
- **The c4c6 patch does not apply at dev `1269cdaf`**, as expected for an adapted dev. Whether dev's adaptation is equivalent is the manager's parent run to show.
- **Hardware.** Physical calibration NOT RUN. No hardware. Field skips are not hardware proof.

## Pending manager duties

- Run the donor bank (9), and the parent consumer set (16) at dev `1269cdaf` with `parent-adoption-c8-cdf49d1a.patch`, then `parent-adoption-p2-cdf49d1a.patch` (sha256 `590f791d…f539fa`).
- Build the final current-dev candidate at the merge turn (source base `c74711d45a8bbc0d6b38cb49211b26a4a6413e88`, live dev `1269cdafb4bb964c757baae0f0c5a932d43f540b`).
- Hosted and act acceptance at the exact head (`suites` was still in progress at my snapshot), distinguishing executed jobs from skipped contexts.
- Carry R1 (09 §8.6 "B1-B13" qualifier) to the residue checklist.
- Merge still requires the second independent review to be POSITIVE at this head, and the full completion bar.

R436-4 FINISHED
