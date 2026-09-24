[R304] POSITIVE - exact head 3face0914efd9d5e71f36da7e30108cfe09c837d

# R304-3 independent review: FPGA-gPTP issue #75 / PR #76, round 3

- Exact head `3face0914efd9d5e71f36da7e30108cfe09c837d`, tree `c1f98ddfb81a5e4d06dfa436cc5162023b590314`, source base `e5dcea6e351abff18a27a00f8e345f3251bdbd8f`. The clone is detached and was verified byte-exact after all probes.
- **Verdict: POSITIVE.** No MINOR, MAJOR or BLOCKER finding is open at this head, and all five lenses are CLEAN.
- The round-3 target is R304-2 F3, which is the same finding as R305-2 F1: while the level is low, asCapable loss and recovery was not pinned. It is **RESOLVED as specified**.
  - The unchanged round-2 reviewer mutant X01 is now caught by the shipped harness, on the new named check.
  - The shipped control `slew idle asCapable loss arms qualification` uses X01's exact pattern and replacement. It fails only inside the new block.
- The requested manager-guide area refresh, R304-2 S1 (= R305-2 S1), was **taken**. Every figure matches the published synthesis reports.
- I recorded my verdict and ledger (`receipts/verdict_before_prior_findings.md`, 19:50:59Z) before I read any prior public review finding. Reconciliation did not change that verdict.

## 1. Reconstructed scope and authorities

- **Repository governance:** the head has no `AGENTS.md` or `CONTRIBUTING.md`; both are absent from the tree. `README.md` and `docs/README.md` set the truth order: current RTL and generated microcode, then executable tests, then the role guides, then history.
- **Issue #75 frozen acceptance:**
  1. A registered, `clk_i`-synchronous `phc_slew_active_o` level.
  2. A timing contract covering reset, asCapable loss, missing Sync, replacement step, and return to grandmaster duty.
  3. Tests for the policy's own start and end, for steps and ordinary tracking not asserting the level, and for each defined edge. Tie-low and early-clear mutants must fail.
  4. `docs/INTEGRATION.md` documents the port and contract.
  5. The parent consumer check belongs to milan-fpga #545.
- **Manager scope decisions on the issue:**
  - A265 executor on base `e5dcea6`.
  - A272 round 2 (R304-1/R305-1 F1 and F2, plus suggestions).
  - A275 round 3 (issue comment 5819725333) requires three things:
    - an engine check where asCapable is lost and then recovered through wire inputs, the first consumed pairs after recovery are in-band, and the level stays low with no edge;
    - a named mutation control equivalent to X01;
    - a refresh of the `docs/MANAGER.md` area snapshot.
  - "Nothing else changes."
- **Interface authorities at head:**
  - `docs/INTEGRATION.md:279-355`: the slew-active contract. Row `:301` covers in-band tracking without an active correction ("Stay inactive"). Row `:325` covers asCapable loss.
  - `docs/HDL_DEVELOPER.md:115-137`: the RTL-owned lapse hook. `:135`: "While inactive, these writes must leave qualification unarmed."
  - `hdl/top/KL_gptp_engine.sv:872-879`: the hook itself, with the guard at `:876-877`. Bit 2 of `st_wdata_w` is asCapable and bit 3 is sync-ok (`tb/verilator/engine/sim_main.cpp:194-195`).
- **Round-3 delta** (`git diff 4a897e4..3face09`) touches three files only:
  - `docs/MANAGER.md` (+12/−2);
  - `tb/verilator/engine/mutants.py` (+6);
  - `tb/verilator/engine/sim_main.cpp` (+27).
- RTL, the generator, the four ROM images and `bench/` are byte-identical to the round-1 head `49d23b2`. Raw `git diff --quiet 49d23b2 HEAD -- hdl syn tb/tsngen tb/verilator/ucpu tb/verilator/engine/gptp_ucode.hex bench` returns 0.

## 2. Findings

No open MINOR, MAJOR or BLOCKER findings.

### Suggestions (do not affect the verdict)

- **S1 (Docs):** `docs/MANAGER.md:46` says "The baseline used 4,773 LUTs and 3,646 registers" but does not name the baseline commit. The published `author/base-source.txt` records only a temporary path.
  - Suggestion: name `e5dcea6` next time this snapshot is touched, so the +80/+6 comparison can be reproduced from the guide alone.
- **S2 (Docs, Tests):** the engine-suite bullets in `docs/TEST_DEVELOPER.md:105-107` list idle timeouts, GM changes and returns from mastership. They do not list the round-3 inactive asCapable loss and recovery check or its control.
  - A275 explicitly scoped this round to the harness, the control and the manager guide, so this is not required here.
  - Suggestion: add one bullet with the next test-guide change.
- **S3 (Robustness), carried from R304-2 S2 / R304-1 S3:** field behaviour is not characterised.
  - The ±100 ns / two-pair completion and the held intervals come from simulation. This run traced 6,138,826 and 3,833,378 cycles at 2 MHz for the ±90 µs traces.
  - Parent #545 may want to count assertions and time spent high.

## 3. Resolution of prior public review findings at this head

I read these only after my verdict and ledger were written.

| Prior item | Status at 3face091 | Evidence |
|---|---|---|
| R304-2 F3 (MINOR; Tests, Conformance): inactive asCapable loss/recovery unpinned; X01 survives | **RESOLVED as specified** | `sim_main.cpp:4766-4791`: bad Pdelay (`PD_FAR`) drops asCapable while inactive, the harness holds it lost for 100 ms, and good exchanges restore it. It re-announces, then consumes two in-band pairs (0 ns with the link-up threshold, then +100 ns). It checks: level low throughout, no edge, no rate write during the lapse or recovery, exactly one PI rate write per pair (`slew_probe`), and matching PI arithmetic. The control is at `mutants.py:101-106`. Unchanged `probe_mutants_r2.py`: X01 **caught**, first failure `FAIL slew: in-band pair after asCapable recovery stays inactive got 1 exp 0`, 1614 checks / 3 FAIL, all three inside the new block (`receipts/reviewer_r2_head/reviewer_00.json`). The shipped arm catches the control on the same named check (`receipts/shipped_arm_slice_4_8.log`). |
| R305-2 F1 (MINOR; Tests, Conformance), the same finding | **RESOLVED as specified** | As above. R305-2 additionally required "each pair writes exactly one PI rate", which `slew_probe` enforces (`sim_main.cpp:4707`, `:4709`). R305-2's R21 is textually identical to X01 and to the shipped control. I did not run the external reviewer's driver; that reviewer owns it. |
| R304-2 S1 = R305-2 S1 (SUGGESTION): MANAGER area snapshot | **Taken** | `docs/MANAGER.md:35-52` matches the published reports exactly (§4 Docs; `receipts/evidence_crosscheck.txt`). |
| R304-2 S2 (SUGGESTION): field characterisation | Carried as S3 | — |
| R304-1 F1 / R305-1 F1 (MINOR): inactive idle-timeout, GM-change and return-from-GM directions | **Still resolved** | Round-1 driver, unchanged: R07 is caught at `slew: in-band return from GM stays inactive`; R14 at `slew: in-band pair after idle timeout stays inactive`. Shipped controls `slew idle lapse arms qualification` and `slew mastership keeps qualification` are caught on their named checks. |
| R304-1 F2 / R305-1 F2 (MINOR): stale SOURCE_EVIDENCE anchors; slew row | **Still resolved** | `check_source_evidence.py`: 20 exact, 0 findings; selftest PASS, 7 arms (`receipts/contract_docs_head.log`). |
| R304-1 S1/S2, R305-1 S1/S2 (SUGGESTION) | Still taken | `docs/MANAGER.md:56-80` ROM budget matches regeneration (1,008/1,024, `SERVO@0`, `FUTO@13`); `docs/HDL_DEVELOPER.md:115-137`; `mutants.py:38-44`. R02 still survives, as recorded there. |
| R304-1 S3 (SUGGESTION) | Carried as S3 | — |

## 4. Lens results (artifact-specific evidence)

### Conformance: CLEAN

- The inactive asCapable loss/recovery check pins the last unpinned direction of issue item 2's five named edges against issue item 3. It uses public wire stimuli only: Pdelay responses, Announce, Sync and Follow_Up.
- The check's expectations match `INTEGRATION.md:301` and `:325` and `HDL_DEVELOPER.md:135`.
- The first recovered pair is graded with the link-up threshold (`linkup=true`), which is consistent with #68 (an asCapable rise re-arms link-up). Offset 0 therefore reaches the slew leg instead of stepping, which is exactly the path X01 corrupts.
- Scope follows A275: only the harness, `mutants.py` and `MANAGER.md` changed.

### RTL: CLEAN

- Unchanged since round 1 (raw `git diff --quiet` returns 0 over `hdl`, `syn`, the four images and `bench`).
- All four tracked ROM images regenerate byte-exact from the head generator (`receipts/static_checks_head.log`: 4× MATCH; 1,008/1,024 words).
- `make lint` (engine and bench) rc=0 with the pinned simulator (`receipts/lint_head.log`).
- `make contract` PASS.
- The hook (`KL_gptp_engine.sv:872-879`) gates both flag terms on `phc_slew_active_o`, as the guide states.

### Robustness: CLEAN

- The new block is load-bearing and specific. X01, and the shipped control built from the same text, fail only the three checks inside `:4766-4791`. Nothing else in the suite sees them.
- The neighbouring arms are still discriminating:
  - X02 (sync-ok arms while inactive) is caught at the idle-timeout check;
  - X04 (step arms qualification) is caught;
  - X05 (mastership arms qualification) is caught.
- X03 (an idle lapse arms a single pair) survives, and it is port-equivalent:
  - a remaining count of 1 on an in-band pair decrements to 0;
  - the slew leg then writes 0, so the level never rises;
  - an out-of-band pair reloads the count anyway.
- R02 (the active-direction asCapable term removed) survives, and is documented as defence in depth by a reachability argument (`mutants.py:38-44`). That argument is not an executed proof.
- All other round-1 reviewer mutants (21/22) are caught (`receipts/reviewer_r1_head.log`).

### Tests: CLEAN

- Shipped engine suite, pinned Verilator 5.050: **1,613/1,613 PASS on each of the three images** (default, request counter seeded above 16 bits, Sync counter seeded above 16 bits), rc=0 (`receipts/engine_suite_head.log`).
- **Shipped mutation arm** (`mutants.py`, its own `main()`, unmodified): **33/33 caught** and 0 non-PASS lines. It ran as four slices of its own `MUTATIONS` list, each with a passing positive control (`receipts/shipped_arm_slice_*.log`). All six `slew:` controls fail their named checks, including the new one.
- Unchanged round-1 driver, author set: 33/33 caught, all six slew controls `named=True`; control 1,613 PASS (`receipts/author_head.log`, `receipts/author_head/`).
- Unchanged `make_gap_tree_r2.py`, probe C: control 1,631/1,631 PASS. X01 fails `probeC: in-band pair after asCapable recovery stays inactive` and the shipped named check (1633 checks / 5 FAIL; `receipts/reviewer_r2_probeC*`, `receipts/probeC_tree.diff`).
- The script hashes equal the published R304-2 manifest (`receipts/script_and_tool_identity.txt`).

### Docs: CLEAN

- `docs/MANAGER.md:31-52` against the published reports on the `gptp75-review-evidence` branch. `4999d8d6` (linked from the guide) is an ancestor of `26975a0c`.
- Engine:
  - baseline: 4,773 LUTs / 3,646 registers / 466 memory LUTs / 1.5 BRAM / 4 DSP, WNS +2.249 ns;
  - candidate: 4,853 / 3,652 / 466 / 1.5 / 4, WNS +1.773 ns, "All user specified timing constraints are met";
  - the round-3 re-synthesis reproduces the candidate figures (dated 2026-09-24 20:53).
- MicroCPU: 1,643 / 733 / 1.5 / 4, WNS +1.941 ns (round-3 report).
- Tool: Vivado v.2026.1. Part `xc7a100tfgg484-2`, 10.000 ns clock (`syn/ooc/engine_ooc.tcl`).
- Deltas: +80 LUTs and +6 registers, as stated.
- No stale area figure remains in the current guides.
- `make docs` passes: docs check (11 current, 17 historical pages), selftest 10 arms, diagrams (9 pinned assets), selftest 10 arms, and source evidence 20 exact with 7 negative controls (`receipts/contract_docs_head.log`).

## 5. Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #75 body; A265, A272 and A275 scope comments; `INTEGRATION.md:279-355`; `HDL_DEVELOPER.md:115-137`; `sim_main.cpp:4730-4888` | R304-3 | 3face0914efd9d5e71f36da7e30108cfe09c837d |
| RTL | CLEAN | `KL_gptp_engine.sv` and `gen_gptp_ucode.py` (full-PR diff); byte identity since 49d23b2; four-image ROM regeneration; engine and bench lint; PHC contract | R304-3 | 3face0914efd9d5e71f36da7e30108cfe09c837d |
| Robustness | CLEAN | Reviewer sets R01-R22 and X01-X05 at head; probe C tree; failure localisation of X01 and the control; X03/R02 survivor analysis | R304-3 | 3face0914efd9d5e71f36da7e30108cfe09c837d |
| Tests | CLEAN | `sim_main.cpp` (+27), `mutants.py` (+6); engine suite on three images; shipped arm 33/33; round-1 driver 33/33 | R304-3 | 3face0914efd9d5e71f36da7e30108cfe09c837d |
| Docs | CLEAN (S1, S2 open as SUGGESTION) | `MANAGER.md` against 8 published utilization/timing reports and `area.json`; `TEST_DEVELOPER.md`; `SOURCE_EVIDENCE.md` via checker; docs, diagram and contract gates | R304-3 | 3face0914efd9d5e71f36da7e30108cfe09c837d |

## 6. Executed evidence (all listed in MANIFEST.sha256)

- `scripts/run_engine_suite.sh`: the shipped `make run`, with the Verilator build capped at `-j 8`.
- `scripts/run_shipped_arm_slice.py`: the shipped `mutants.main()`, unchanged, on slices [0:4], [4:8], [8:12] and [12:33].
- `scripts/round1/probe_mutants.py`, `scripts/probe_mutants_r2.py` and `scripts/make_gap_tree_r2.py`: unchanged from R304-2.
- `scripts/round1/static_checks.sh`: ROM regeneration.
- `scripts/clone_integrity.sh`, with results in `receipts/clone_integrity.txt`:
  - HEAD and tree match;
  - porcelain status is empty, including ignored files;
  - the index equals HEAD;
  - 104/104 tracked blobs and modes re-hash to HEAD;
  - `fsck` rc=0;
  - there are 0 gitlinks and no `.gitmodules`, so no submodule gitlink exists to verify in this repository.
- `receipts/hosted_status.txt`: the exact head has 0 check-runs and 0 status contexts. The repository tracks no workflows, so nothing ran on hosted CI and nothing was skipped there.
- All probe trees were exported with `git archive` into the reviewer scratch area. The reviewed clone was never written.

## 7. Real limits

- **Foreground-window deviation.** My first attempt to run the shipped arm serially exceeded the session's 10-minute per-command window, and the session moved it to background.
  - I misjudged that run as dead, because my process listing could not see it, and deleted its log and temp dir while it was still running. Its result is void and nothing in this report relies on it.
  - It overlapped my first slice pair for several minutes, so concurrent compile jobs may briefly have reached 12, above the 8-job cap.
  - The final slice pair also passed the window and was moved to background. I polled its logs in the foreground until both slices finished, and did not touch it.
- I did not run the full gPTP/parent/PP/Yosys/builder banks or the parser, µCPU, gasket, tsngen and bench-simulation suites. That was out of scope; RTL has been unchanged since round 1. The manager reports those banks passed at this head, but I found no separate manager-bank receipt under the public evidence path (`26975a0c` holds the author packets), so I rely on my own focused runs.
- No synthesis was run. The area and WNS figures were checked against the published reports, not re-measured.
- I did not execute the external reviewer's own driver (R21/R22). I only verified that R21's text equals X01.
- X03 and R02 survive. X03 is port-equivalent by analysis; R02 rests on the documented reachability argument, not an executed proof.
- **Physical calibration NOT RUN.** No hardware was used, and simulation is not field or hardware proof. The measured-completion durations are simulation-only.
- Raw logs contain local absolute paths; publication redaction is the manager's.

## 8. Pending manager duties

- Obtain the second independent review at this exact head (R305-3) before merge.
- Build and accept the final current-dev candidate at merge (source base `e5dcea6`, live dev `573f0052`). This is distinct from the source validation above.
- Hosted and act acceptance; this repository currently has no hosted jobs.
- Parent #545: connect `KL_gptp_shadow.u_engine` through to the CRF servo, validate the mastership retirement addend, and run the consumer gates.
- Settle acceptance of the ±100 ns / two-pair completion tolerance, and reconcile the measured held durations with the parent's 0.5 s premise.
- Physical calibration and hardware validation.
- Publish this packet: REPORT.md plus the MANIFEST-listed files, with path redaction as needed.

R304-3 FINISHED
