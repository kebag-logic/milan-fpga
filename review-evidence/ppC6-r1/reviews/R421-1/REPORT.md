[R421] NEGATIVE - exact head 5e806296b73d04ccf095ad00e081cb790fbbaf8d

# R421-1: external review of processor PR #139 (lane C6, notifications and Identify)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #139 (closes #54, #58, #80, #86)
- Exact head: `5e806296b73d04ccf095ad00e081cb790fbbaf8d`, tree `ebe7b48fe653437d1bed59f510c15d5d62163144`
- Base: `0451d83d9d3f2ed5f4513c59ac5ac219ad9dd7ff` (five commits: 018ee6c, b5beed6, 4ce963e, 5cf99f7, 5e80629)
- Scope authorities: #80 assignment comment 5915639621, the design-gate STOP 5915752457 and the manager ruling 5915765717 (four conditions); the acceptance lists of #54, #58, #80 and #86; the PR body; public evidence at kebag-logic/milan-fpga `2c5328276c35d9bbc0214ac10f0c49532a0dfd01` `review-evidence/ppC6-r1` (every downloaded file matched its MANIFEST.json `published_sha256`).
- Not judged here, as instructed: the later merge with processor main `d5f73bac` (C2).

## Verdict

**NEGATIVE.** One open MINOR (F1). The lane otherwise meets its bar: I reproduced every
graded claim I could run (pp_top 8,078 checks, the three changed unit suites, lint at both
parameter settings, the doc gates, notify_mutants.py 30 of 30 KILLED, both EN=0
equivalence proofs), and found no defect in the identify frames, the pushes, the
SET_STREAM_INFO fix, the STORM/RND suites or the parent-visible list. F1 is a
behaviour-versus-claim gap: under contention or TX backpressure between frames 2 and 3,
the spacing the lane says is "never less" than T-IDENT-BURST (and "never bunches") is
less, and no test exercises that case.

## Findings

### F1 [MINOR] Frame 3 is scheduled from t0 rather than frame 2's departure, so a late frame 2 shortens the 2-to-3 gap below T-IDENT-BURST. The lane says this never happens, and no test covers it.

- **Lenses:** RTL, Robustness, Tests, Docs.
- **Where:**
  - `hdl/aecp/KL_aecp_notify.sv:155-159` (banner: "each is armed only once the frame before it has gone, so a held engine delays a burst but never bunches it").
  - `hdl/aecp/KL_aecp_notify.sv:779-790`: t0 is set once at frame 1. The comment at :781 says "every delay below is at least its T- value".
  - `hdl/aecp/KL_aecp_notify.sv:726-728`: frame 3's deadline is `t0 + 2 x T-IDENT-BURST`, whenever frame 2 actually went.
  - `docs/architecture/09_verification.md:224` ("three frames spaced `T-IDENT-BURST` (never less)").
  - `docs/architecture/08_timing.md` T-IDENT-BURST row.
  - `tb/pp_top/README.md:1210-1226` (ID5, and ID6: "a held engine delays a burst but never bunches it").
  - `tb/pp_top/notify_phases.hpp:199-211`: the check rule `gap >= BURST`, "never less".
  - `tb/pp_top/notify_phases.hpp:348-407`: ID5 contends only with frame 1, and ID6 holds only before frame 1.
  - The PR body, item 1: "a held engine delays a burst, never bunches it".
- **Authority:** IEEE 1722.1-2021 §7.5.1 / §7.5.1.2.1 (txIdentify sends the notification three times with a 150 ms delay between transmissions); #54 acceptance 2 ("spaced by T-IDENT-BURST"); the ruling's condition 4 (the burst graded on the wire).
- **Evidence:** a reviewer probe on the lane's own third build (`scripts/r421_ident_probe.hpp`, `receipts/probe-ident-contention.log`). It adds no RTL change. It uses 15 registered controllers and the suite's timebase (1 ms = 100 clocks, T-IDENT-BURST = 15,000 clocks).
  - **P1:** one ordinary SET_NAME fan-out, started just before frame 2's deadline. The frame 2→3 gap drops to between 13,996 and 14,568 clocks in 23 of 31 offsets. The minimum is 13,996, i.e. 1,004 clocks under T-IDENT-BURST. With no contention the gap is exactly 15,000. The frame 1→2 gap grows by the same amount, up to 16,250.
  - **P2:** MAC `tx_ready` held low for 200, 250 and 320 ms, starting 10 ms after frame 1. The 2→3 gaps are 9,111, 4,144 and **63** clocks: frames 2 and 3 leave back to back.
  - In silicon the P1 shortfall is the frame-2 queueing delay (microseconds at the default clock). The P2 bunching is real at any clock rate.
  - Every section-ID check still passes at this head. The case is simply never exercised: ID5 presses during a fan-out, so only frame 1 contends; ID6 holds the engine before the burst.
- **Impact:** the lane's evidence for #54 acceptance 2 claims a hard invariant that the RTL does not have. A reader of 08/09 or the integrator material would expect that a busy notification lane or a stalled MAC can only delay a burst. In fact it compresses the second gap, down to back-to-back frames. The suite's own grading rule would fail on this case, and nothing covers it.
- **Required outcome, either of:**
  - (a) Schedule each later frame at no less than T-IDENT-BURST after the previous frame actually left, e.g. `max(t0 + k x T-IDENT-BURST, departure(k-1) + T-IDENT-BURST)`. Departure can be taken as retirement if the TX-queue part is stated. Add a section-ID arm that contends and stalls frame 2 (P1/P2 shapes), with a recorded mutant.
  - (b) Keep the t0 chaining. Correct the claims in the RTL banner and :781, 08 F08.1, 09 §8.3, tb/pp_top/README ID5/ID6 and the PR body to the true bound: the gap from frame k to k+1 is T-IDENT-BURST less frame k's delay, and a TX stall of at least T-IDENT-BURST can bunch frames. Add a test arm that records that bound (a P1/P2-style contention of frame 2), so the invariant the suite grades is the one the RTL has.
- **Verification:** `scripts/run_r421_probes.sh <clone> <work> probe`, then the probe log. (a) needs every P1/P2 gap ≥ 15,000 clocks, or ≥ the stated departure bound. (b) needs the docs and the new arm to agree with the observed gaps, and ID1..ID6 unchanged.

### Suggestions (non-blocking)

- **S1 [SUGGESTION] (Conformance, Docs).**
  - What happens: a release followed by a press inside a burst starts the next burst as soon as the running one ends (`KL_aecp_notify.sv:162-163`, :776/:803/:812; ID3f: 106 clocks after frame 3). The second burst therefore comes about 300 ms after the first.
  - Why it matters: a strictly sampled Figure 7-142 evaluates `identifyButtonPressed` only after txIdentify completes. It would stay in IDENTIFY until the 1 s timeout if the button is held again by then.
  - Status: the behaviour is documented (integrator guide §6, 06 §7) and outside #54 acceptance 3, which covers a *held* trigger.
  - Proposal: state it in 06 §7 / F06.16 as a deliberate reading (an edge latched during the atomic txIdentify), or sample the level at the burst's end.
- **S2 [SUGGESTION] (RTL, Docs).**
  - What happens: `identify_button_i` is the first CDC inside the core. The integrator guide (`docs/guides/integrator.md:32-40`) says it "may come straight from a pin". The 2FF (`KL_aecp_notify.sv:754-755`) carries no synchroniser marking, and the guide gives no timing-exception guidance for the pin-to-`btn_q1_r` path.
  - Proposal: name the synchroniser flops and the false path / input-delay duty in the integrator guide, or keep the 2FF and say the integrator constrains it.
- **S3 [SUGGESTION] (RTL).**
  - What happens: `KL_aecp_engine.sv:2760-2761` still sets `gstri_r` for `PP_UNS_SINFO_C`. The new `E_SINFOUNS` program gathers nothing, so the flag only steers an unused gather route and the `tix_w` capture.
  - Status: harmless. It sits inside the proven-equivalent engine logic.
  - Proposal: drop it or say why it stays.
- **S4 [SUGGESTION] (Docs, evidence).**
  - What happens: the LUT figures of this yosys `synth_xilinx` flow are dominated by mapper variance.
    - My module-level out-of-context run of `KL_aecp_notify` maps 6,598 LUT at main and 8,002 at head EN=0. That is +1,404 for a netlist proven equivalent, whose generic netlist differs by a single `$ne_3` cell (`receipts/ooc/gen_notify_*-stat.txt`).
    - It maps 8,009 at EN=1, only +7 LUT over EN=0, while FF goes 1,721 → 1,785 and CARRY4 249 → 271.
  - Why it matters: the PR's whole-top "+569 LUT at 1" therefore does not measure the sequencer. The FF/CARRY deltas are the reliable cost figures.
  - Proposal: say so next to the table. The PR already names a Vivado out-of-context run at the parent as the authoritative figure.

### Prior public findings on this PR

Checked only after the verdict and ledger above were written: none exist (see the section near the end).

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | IDENTIFY_NOTIFICATION frame (DA 91-E0-F0-01-00-01, controller 90-E0-F0-FF-FE-01-00-01, u = 1, cmd 0x0026, CONTROL/`identify_index_i`, cdl 16, sequence from 0 and +1 per burst, 1 s timeout from the first frame) in `KL_aecp_notify.sv:693-839`, `gen_ucode.py` E_IDNOTIF, `notify_phases.hpp` ident(); A6/ID4 BAD_ARGUMENTS; SET_CONTROL does not start it (Milan §5.4.5.4); #58 pushes: requester excluded, per-entry seq, body from current state, 7 classes in NP plus 6/7/8/LOCK graded pre-lane; SET_STREAM_INFO unsolicited body = Figure 7-40 84 bytes (cdl 96), MSRP_ACC_LAT_VALID 0x20000000 with the offset at @48, layout checked against the pre-existing E_SIBAD 84-byte layout and the solicited echo; MGMT "not supported" statement against #58 acceptance 3 arm 2 (03 §5 item 4, 06 §7 class 2, REQ-NOT-002); the 03 §4/§5 landed-shape disposition against #86 acceptance 1/4; S1 | R421-1 | 5e806296 |
| RTL | UNCLEAN (F1) | the sequencer FSM, 2FF sync, generation-tagged REARM, face hand-off only outside N_EMIT_WAIT and `core_done_w` masking, the withdrawal path, arm arbitration against every notify-core arm site (N_IDLE lock, N_APPLY only: `core_arm_w` covers both), `amap_busy_o` hold, generate-gated zero-flop default; engine kind-15 mapping gated by the parameter; top wiring, owner-tag overlap guard (0xB1..0xB3 < 0xC0), singleton slots +1/+2; timer service fires past deadlines on the next sweep (so a late frame 2 makes frame 3 due at once: F1); lint 41 modules at 0 and the three changed modules at EN=1 (0 warnings); yosys EN=0 equivalence reproduced: notify vs main 6,365/0 unproven with a non-vacuity control at EN=1 (169 unproven), engine vs main plus the SINFO fix alone 21,481/0 unproven (five unchanged submodules as matched cut points); the ROM differs from main only in E_IDNOTIF (unreachable at 0) and E_SINFOUNS; out-of-context FF 1,721 = 1,721 at 0; S2, S3, S4 | R421-1 | 5e806296 |
| Robustness | UNCLEAN (F1) | probe P1/P2 (frame-2 contention and TX stall); ST (16 rows, 10 Hz counter churn on five descriptors, solicited AECP worst 70,958 / ACMP 249 clocks against 100,001 / 50,001); RN (720 seeded steps, 20 controllers, 0 divergence, 24 NO_RESOURCES, 117 denials, 7 auto-unlocks); originator R (4,000 steps, 3,757 events, 0 divergence, peak 8 live); release/press, press-before-restore (ID6), fan-out-during-press (ID5), bounce behaviour (documented integrator debounce duty) | R421-1 | 5e806296 |
| Tests | UNCLEAN (F1) | `make -C tb/pp_top run` rc 0, 8,078 = 7,996 + 20 + 62 (matches the PR and the author receipt); originator 107, ucpu 396, aecp_notify 10, ca_originator 16, dispatch 211, timer_service 48, all rc 0; `notify_mutants.py` rerun from an isolated copy: goldens PASS, 30 of 30 KILLED on their named checks, rc 0 (`receipts/mutants/`); the NP3 failing-before arm reproduced as mutant `stream_info_get_body` (engine mapping back to UPC_GSTRI_C, NP3 byte-exact FAIL) and matching the author's `np3-failing-arm-before-fix.log`; driver semantics (exact single-occurrence edits, completed tally, every named check failing, non-zero rc); independence of the RN and R models (expectations built from the clauses, sequence modelled from the wire); ID5/ID6 coverage gap (F1) | R421-1 | 5e806296 |
| Docs | UNCLEAN (F1) | 00 GAP-06/GAP-17/REQ-AEM-026/REQ-NOT-001/-002, 01 F01.5 (default 0), 02 F02.1/§2/§6, 03 §4/§5, 06 §2/§7/F06.16/command table, 08 F08.1/F08.4, 09 §8.3, integrator guide §1/§2/§6, operator and hdl-engineer guides, diagram 21 (SVG and PNG, stale gate green), tb/pp_top, tb/originator and tb/ucpu READMEs with mutation records; `make check` rc 0 (links 997, parameters 27 = 27 = 27, matrices), `gen_matrix.py --check` rc 0; the parent-visible list (the manager's rebased `parent-adoption-c6-e4b771f9.patch`: the `KL_pp_shadow` tie-offs `.EN_IDENTIFY_NOTIF_P (1'b0)` and `.identify_button_i (1'b0)`, each with a `//!` rationale, and the `DUT_READER_DISPOSITIONS` entry for `notify_mutants.py`, which reads HDL text only to plant edits and so does need the disposition, like `d3_mutants.py`); F1 claims in 08/09/README/PR; S1, S2, S4 | R421-1 | 5e806296 |

### The ruling's four conditions and each issue's acceptance, as I judge them

- **Condition 1** (default 0, zero area, cost at 0 and 1):
  - Default 0 in the top, notify and engine, and 01 F01.5 now reads 0.
  - EN=0 is equivalence-proven, with FF, CARRY and RAM equal to main.
  - The LUT figure is mapper variance (S4).
  - Met.
- **Condition 2** (synchronized/debounced or stated duty): 2FF in the core, and the debounce duty is stated in the port comment and the integrator guide. The button is not read at 0 (`gen_no_ident`). Met (S2 is advisory).
- **Condition 3** (parent-visible list): both parent edits are present in the manager's rebased patch at dev e4b771f9. The integrator guide and diagram 21 gain the parameter. The port-contract and naming checks pass per the author's parent receipts, which I did not rerun. Met, pending the manager's parent bank.
- **Condition 4** (grade both settings):
  - At 1: graded on the wire, with 11 identify mutants killed. The 2→3 spacing claim is overstated (F1).
  - At 0: ID0, plus the proofs.
  - Met except F1.
- **#54:**
  - 1 met; 3 met; 4 met.
  - 2 met in isolation. F1 shows the spacing is not guaranteed under contention.
- **#58:** 1 met; 2 met; 3 met (arm 2).
- **#80:** 1 met (F1 as above); 2 met; 3 met; 4 met.
- **#86:** 1 met; 2 met; 3 met (at tb/originator, as the issue permits); 4 met.

## Real limits

- The IEEE 1722.1-2021 and Milan v1.2 PDFs are not available to this reviewer. I judged conformance from the clause text and figure layouts quoted in the issues, the PR and the repository, and checked Figure 7-40's layout against the repository's pre-existing 84-byte E_SIBAD layout. I did not check it against the standard itself.
- The instructed Verilator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. I used `$VALIDATION_TOOLS/verilator-v5.050/bin/verilator`, which reports `Verilator 5.050 2026-07-01 rev v5.050`. The scratch copies set Verilator's `--build -j` to 8 (4 per copy for the two-way mutation campaign). The clone itself was never built in.
- As instructed, I did not run the full processor bank (`run_suites.sh`), the whole-top yosys run, or any parent bank. The 1,017,309-check total is the author's receipt only. My out-of-context figures are module-level (`KL_aecp_notify`).
- The author's `HANDOFF.md` inside the public evidence was not read (author material). The design was taken from the public STOP comment.
- Hosted checks at the exact head, read-only: docs-gates success, portability success, suites **in progress**. The manager owns hosted acceptance.
- No hardware. Physical calibration was NOT RUN, and skipped field contexts are not hardware proof.
- After the probes, the clone at `$REVIEWS/r421-1-ppC6` was verified at the exact head, see `receipts/clone-verification.txt`:
  - worktree and index blobs and modes equal the head tree;
  - no untracked or ignored files;
  - no gitlinks (this repository has no submodules).

## Pending manager duties

- Hosted CI acceptance at the head (the suites job was still running when checked).
- The parent consumer set with the combined adaptation and `parent-adoption-c6-e4b771f9.patch` at the merge turn, including the port-contract, naming and evidence ratchets.
- The later merge-delta round against processor main `d5f73bac` (C2), which conflicts with this branch.
- A Vivado out-of-context figure at the parent if an authoritative LUT cost is wanted (S4).
- Resolution of F1 by the executor, then a re-review of the new head.

## Prior public findings on this PR (checked after the verdict and ledger)

None to resolve or retain.

- PR #139 at head `5e806296` has 0 reviews and 0 review comments.
- Its only two issue comments are the manager's review-start notices for R420-1 and R421-1.
- Issue #80 carries the assignment, TAKEN, the STOP, the ruling and REVIEW READY, and nothing else.
- Issues #54, #58 and #86 have no comments.
- The author's PR-body observation (IEEE §7.5.2 lists DEREGISTER_UNSOLICITED_NOTIFICATION, and a solicited DEREGISTER does not push) is outside this lane's acceptance. It is not a review finding, and I neither adopt nor dispute it.

## Receipts

Every file listed in `MANIFEST.sha256` is publishable. The reproducer is
`scripts/run_r421_probes.sh`, and the probe source is `scripts/r421_ident_probe.hpp`.

R421-1 FINISHED
