[R302] NEGATIVE - exact head 39a0171c8c39e68065b14b9178b30d708a9f7645

# R302-1 internal independent review: issue #546 / PR #554

- Round: R302-1, cleared-context internal reviewer.
- Exact head: `39a0171c8c39e68065b14b9178b30d708a9f7645`, tree `5399d73e1e581116e8cc8dd9f82ead83bbf3c666`.
- Source base: `57456af96b3127b9d309a995bbbd35a6113ce52d`, one commit (`39a0171c8`).
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs. All five were applied at this head.
- Verdict: NEGATIVE. One MAJOR is open under `Tests` and `Docs`. `Conformance`, `RTL` and `Robustness` are covered clean.

## Reconstruction

Read in this order: `AGENTS.md`, `CONTRIBUTING.md` (house style, verification bar), `docs/README.md`.
Then the issue #546 body (Observed, Authority, Acceptance 1-3), the executor assignment comment and the
`[A264] REVIEW READY` comment, and the PR #554 body. Then the diff `57456af96..39a0171c8` (21 files, +694/-23),
the #539 detector rationale at `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:297-305` and the Annex B.1.1 rows in
`docs/reference/MILAN_COMPLIANCE_MATRIX.md:228` and `docs/reference/REGISTER_MAP.md:750`. Then the public
evidence tree `review-evidence/546-r1` at `1461cd870f` (manifest, area logs, gate table, and the #539
150 us trace `author/539-talker-step-150000.log`), and the hosted check runs at the exact head.

Frozen acceptance used:

1. Discard the CRF rate sample spanning a talker discontinuity (tu toggle, or step-shaped jump), in simulation with a failing arm.
2. A GM-change scenario with steps at both ends keeps the servo locked, or gives exactly one counted re-lock.
3. Gates green.

Scope decisions (assignment comment): prefer the tu marker (IEEE 1722-2016 4.4.4.3/4.4.4.7); jump backstop with a
threshold derived from, not mirrored from, #539; change `KL_crf_rx` and the servo sample path, not the servo's own guard logic.

## Finding

### R302-1-F1 MAJOR, lenses `Tests` and `Docs`: the connected GM-change harness cannot fail for the #546 defect

- Location: `tb/verilator/crf_rx/sim_talker_step.cpp:31-32`, `:66`, `:117-140` (comments at `:32` "the timestamp backstop alone" and `:126` "talker changes first; local guard cannot hide it").
  Also the acceptance-2 evidence in the `[A264] REVIEW READY` issue comment and the PR #554 body. Also the harness row at `docs/design/GM_LOSS_RECOVERY.md:213`.
- Authority: `AGENTS.md` section 6, `Tests`: "Each new test can fail for the defect it claims to detect".
  `Docs`: "The PR and Issue contain enough evidence for another cold reviewer". Issue #546 acceptance 2 names this scenario.
- Evidence (receipts under `receipts/probes/`, campaign `probes/run_probes.py`):
  - Mutant `rx_no_detection` forces `rate_break_w` to 0. That is the pre-fix receiver: no tu, jump or gap detection.
    Under it the shipped `talker_step` fails only the two "receiver withholds crossing rate samples" checks.
    Every servo-level check still passes: LOCKED on every clock, integrator within 1 ppm, no held updates, recovered rate, one counted local step.
    The integrator ranges are 30.723..30.723 and 30.703..30.723 ppm, the same as the clean design (`rx_no_detection__talker.log`, `clean__talker.log`).
  - Mutants `jump_removed` and `lower_bound_removed` pass all 19 `talker_step` checks, although its second event is described as "the timestamp backstop alone" (`jump_removed__talker.log`, `lower_bound_removed__talker.log`).
  - The "withholds" check is satisfied by a sampling artifact. `observe()` reads the combinational `rate_valid_o` after the accepting edge while the harness still drives `frame_p_i` high.
    At that point `prev_ts_ns_r` already equals the current timestamp, so the zero spacing reads as a jump. The DUT never samples that view.
    Reviewer scenario `quiet` has no step and no tu edge; that sampling still reports invalid, while the registered view stays valid (`clean__loop_quiet.log`, 4/4).
  - Mechanism: the listener step lands 100 ms after the talker step. The #539 guard abandons the servo window, and the re-based window closes more than 512 ms after the talker step. By then the contaminated ring has aged out, and in both shipped events no servo boundary fell in the 100 ms exposure.
  - The design itself is correct when the scenario can discriminate. The reviewer scenarios `talker_only_neg` and `talker_only_pos` use the same wrapper and event model, with no listener step:
    the clean design holds the integrator at exactly 30.723 ppm and stays LOCKED.
    `rx_no_detection` drives it to +177.207 ppm and -115.762 ppm and drops LOCKED; the second figure is the issue's own -115.82 ppm observation.
    `jump_removed` and `lower_bound_removed` fail the unmarked case.
  - `lag_sweep` puts steps at both ends with the listener lag at 100 to 500 ms. The clean design passes 36/36. `rx_no_detection` fails 13 checks: 100 ms is hidden, 200 ms and above are exposed.
- Impact: the only receiver-to-servo evidence for acceptance 2 passes identically with the receiver fix removed.
  The public acceptance evidence says the integrator "is unchanged for the marked positive step" and the unmarked step "varies only 0.020 ppm". Both statements are equally true of the unfixed receiver, so they do not evidence the fix.
  A later regression in detection, in validity wiring, or in the window phase would stay green in this harness. Only the isolated `discontinuity` harness and `make mutants` would catch it, and that target is not in the sweep.
- Required outcome: the connected GM-change harness must fail when receiver detection is removed, and its unmarked event must fail when the jump backstop is removed.
  A servo boundary must be guaranteed inside the contaminated interval (for example a talker-only event, or a listener lag of at least one window). The validity observation must use the value the servo samples.
  The harness comments and the published acceptance-2 evidence must describe what the scenario actually proves.
- Verification: re-run `probes/run_probes.py` with the shipped harness. `rx_no_detection`, `jump_removed` and `lower_bound_removed` must be `FAIL` on `talker`, `clean` must be `PASS`, and the `quiet`-style artifact must no longer satisfy the withhold check.

## Suggestions (non-blocking; they do not affect coverage)

- S1 `Docs`, `hdl/ieee1722/crf/KL_crf_rx.sv:275`, `docs/design/TIME_SYNC.md:191`: the 100 ppm term is credited to "Annex B.1.1's 100 ppm media clock".
  The repository reads B.1.1 as the LocalClock bound (`MILAN_COMPLIANCE_MATRIX.md:228`). Say that the media bound is inherited from the LocalClock. The value itself is sound.
- S2 `Tests`, `tb/verilator/crf_rx/Makefile:53,78`: `mutants` is outside `all`, so the sweep never proves the failing arms. `tcam`, `render_setpoint`, `gptp_txts` and `gptp_shadow` gate theirs in `all`.
  The servo-validity mutant exists only as a one-off receipt (`author/servo-valid-mutant.py`).
- S3 `Docs`, `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv` banner: it lists every window-skip policy (step guard, #539 PHC step guard, win_skip), but not the new `crf_rate_valid_i` skip. Only the port and inline comments describe it.
- S4 `Robustness`/observability: receiver discards from unmarked jumps are counted nowhere (a public decision, "No additional CSR bit or discard tally").
  A stream that breaks the ring more often than every 512 ms keeps the servo frozen while it reports LOCKED. Consider a tally when a future Issue touches telemetry.
- S5 `Docs`, `docs/design/GM_LOSS_RECOVERY.md:152`: "(#539); The receiver" has a capital letter after a semicolon.

## Lens results (clean lenses in the finding format)

```text
[R302] PASS Conformance - hdl/ieee1722/crf/KL_crf_rx.sv:382-395,514-599; hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:567-568; receipts/probes/clean__loop_*.log - AC1: tu edges (either sign), unmarked jumps and gaps restart the ring; the event PDU seeds 256 new intervals; failing arms reproduced (author mutants 9/32/17/2 failures; reviewer mutants 12 more). AC2: steps at both ends, talker-only, step inside a held tu, 20 us, listener-first and five repeated events all keep LOCKED with the integrator within 0.02 ppm and no receiver unlock. AC3: hosted contexts at the head succeed. The tu reading (10.4.5 bit, 4.4.4.7 semantics, held level permits recovery) is consistent with the cited clauses. The servo's own guard logic is untouched (only the pp_run_r term changed).
[R302] PASS RTL - hdl/ieee1722/crf/KL_crf_rx.sv:282-286,386-395,440-445,511-599,611-615; hdl/milan/milan_datapath.sv:1725,5448,5488,5532,5547 - one clock domain (axis_clk, both instances), no new CDC. 64-bit full-width spacing, unsigned compare both bounds, 2^32 aliases caught. Threshold arithmetic verified: ceil(600e6/999900)=601, 601+768=1369, 1<<$clog2(1369)=2048; below the plane's 20 us smallest step; not the #539 4096. Pend/break ordering, bind-rise override, timeout split on stop_i, and every new register reset. Lint -Wall adds no warning versus base. Mapped area 355->433 LUT, 509->544 FF, 125->147 CARRY4 matches the +80/+35/+22 claim (FF +35 because synthesis shares prev_ts_ns_r[31:0] with ts_new_r).
[R302] PASS Robustness - receipts/probes/clean__jitter.log (31/31), clean__disc.log (1658/1658), clean__loop_repeated.log, clean__loop_tu_only.log - per-timestamp jitter up to +/-640 ns with +/-601 ns/interval drift, tu held high, 12 000 PDUs per case: never invalid, rate exact. A legitimate tu-only edge withholds exactly 256 PDUs, four times. Malformed or foreign markers, back-to-back accepts, lost or duplicate PDU, STOP, silence, rebind, reset, 64-bit rollover and five overlapping GM changes all behave. Thresholds halved or doubled, 32-bit spacing, a removed lower bound, silence/bind/break validity leaks, refill off by one, and an uncancelled pending update are each killed.
```

## Reviewer ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #546 AC1-3 and scope comment; `KL_crf_rx.sv` rate path; servo `pp_run_r` term; reviewer loop scenarios; hosted check runs | R302-1 | `39a0171c8c39e68065b14b9178b30d708a9f7645` |
| RTL | CLEAN | `KL_crf_rx.sv` (full), `KL_mmcm_drp_servo.sv:246-305,480-640`, `milan_datapath.sv` instances; -Wall lint vs base; area logs | R302-1 | `39a0171c8c39e68065b14b9178b30d708a9f7645` |
| Robustness | CLEAN | Jitter/drift/tu-held probe, lifecycle checks, 15 reviewer mutants, overlapping-event loop scenario | R302-1 | `39a0171c8c39e68065b14b9178b30d708a9f7645` |
| Tests | UNCLEAN (F1) | `sim_talker_step.cpp`, `crf_talker_wrap.sv`, `sim_discontinuity.cpp`, `sim_main.cpp` replica, `mutants.py`, servo `sim_main.cpp` U13; all re-run | R302-1 | `39a0171c8c39e68065b14b9178b30d708a9f7645` |
| Docs | UNCLEAN (F1) | `TIME_SYNC.md`, `GM_LOSS_RECOVERY.md`, `REGISTER_MAP.md`, `TESTING.md`, `MODULE_MATRIX.md`, README-tests, RTL banners/ports; PR body and REVIEW READY evidence | R302-1 | `39a0171c8c39e68065b14b9178b30d708a9f7645` |

## Executed evidence at this head (reviewer-run)

Tool: pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`), wrapper sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`.
All builds ran from a `git archive` of the exact head into a disposable scratch tree. The clone was never edited.
Local paths in receipts are replaced by placeholders, and compiler build logs are not published.

| Run | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/crf_rx` (unit, discontinuity, talker_step) | rc 0; 13 836/0, 1 658/0, 19/0 | `receipts/crf_rx_make.log` |
| `python3 mutants.py` (author campaign) | rc 0; clean passes; tu 9, jump 32, refill 17, accept-edge 2 failures | `receipts/crf_rx_mutants.log` |
| `make -C tb/verilator/mmcm_servo` | rc 0; 82/0 unit incl. U13, 8/0 rails, 113/0 PHC step | `receipts/mmcm_servo_make.log` |
| `make -C tb/verilator/mmcm_servo_autorepair` | rc 0; 47/0 | `receipts/mmcm_servo_autorepair_make.log` |
| Reviewer campaign (`probes/run_probes.py`, 43 rows) | campaign PASS: every expectation met, including F1's non-kills | `receipts/probes/SUMMARY.txt` and per-row logs |
| Clone integrity after probes | HEAD/tree exact; worktree and index clean; index equals tree; no skip/assume flags; 4 gitlinks equal the head tree; every tracked blob re-hashes equal | `receipts/clone_integrity.txt` |
| Hosted check runs at the head (read only) | 21 completed success; `Physical gPTP (nightly and manual)` skipped | `receipts/hosted_check_runs.tsv` |

Informative row: `clean loop:subthreshold`. An unmarked 2 000 ns talker step is below the 2 048 ns backstop by construction and reaches the servo.
The integrator moved 30.723 to 28.770 ppm and the servo left LOCKED for ACQUIRE, with no receiver unlock. That band sits below the plane's smallest (20 us) step; it is recorded as a limit, not a finding.

## Prior public findings

At round start the PR carried only the two review-start comments, and the issue carried the assignment and REVIEW READY.
No earlier review finding existed to resolve or retain. The concurrent R303 round was not read.

## Real limits

- Simulation only. Physical calibration was not run, and no hardware, bench or field result backs this review. Skipped hosted contexts are not hardware proof.
- Timing: `rate_valid_o` and `rate_break_w` put a 64-bit subtract and two 64-bit compares combinationally from the parser registers into `pp_run_r` and the receiver controls at 100 MHz (`milan_datapath.sv:67`). Area was re-read from evidence. No timing closure was run or seen for this head.
- The false-positive probe models bounded uniform timestamp jitter. No foreign talker's actual CRF timestamp statistics were measured.
- Full parent, processor, gPTP, Yosys and builder banks and the xvlog gate were not run by this reviewer. The manager's source-bank evidence and hosted results were read, not reproduced.

## Pending manager duties

- Publish this report and the manifest-listed receipts.
- Route F1 to the executor, then re-review at the new head: `Tests` and `Docs` must be covered again there. `Conformance`, `RTL` and `Robustness` stay banked at `39a0171c8` only while their scope is untouched.
- Build and validate the final candidate against live `dev` at the merge turn; own act and hosted acceptance for the new head.
- Keep the physical-calibration limit visible in any completion ledger.

R302-1 FINISHED
