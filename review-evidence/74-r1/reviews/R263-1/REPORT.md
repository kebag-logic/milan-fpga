[R263] NEGATIVE - exact head 553edeb86b9144f7b15721255fbe5ad11ef1fe36

Round R263-1, external independent review of issue #74 item 2 / PR #528.
Head `553edeb86b9144f7b15721255fbe5ad11ef1fe36`, tree `d78849a3b5b3c9f5eb48b4ce4df5785233ab6245`,
base `ede8d48ecd7c7f589a14b957951f040d92c99c70`.

## Verdict in one paragraph

Item 2's RTL does what the frozen scope asks. It is verified independently at
this head, and every negative control fails as it should. A raced lock no longer
chatters. A real held or surplus frame at the lock counts exactly once. A
non-raced engagement is cycle-identical to the base. The new coincidence law
is net-exact. The root `aclk` leg is byte-identical to the base. The verdict is
NEGATIVE for one MINOR Docs finding (F1): the rewritten `SLIP_TDM` paragraph in
`docs/reference/REGISTER_MAP.md` states two properties more strongly than the
RTL law and the PR's own evidence model support. Conformance, RTL, Robustness
and Tests are covered CLEAN at this head. Two defects I found in code this diff
does not change (O1, O2) are reported below as new work for new Issues. They
are not attributed to this change, and the evidence says so.

## Reconstruction (public state only)

Read in order: `AGENTS.md`, `CONTRIBUTING.md` (lane, verification bar, docs
rules), `docs/README.md`; issue #74 body, the reopening ledger
(issuecomment-5507453907, item 2), the item-2 assignment (5794151797), the
executor's TAKEN (5794228544), DECISION (5794560116) and REVIEW READY
(5795282366); the origin finding (PR #323 [R1] finding 1,
issuecomment-5506033067); PR #528 body; the manager comments on PR #528
(5795480660, 5795493487, 5796238119). Then the diff
`ede8d48e..553edeb8` (12 files; RTL: `KL_media_grid_align.sv`,
`KL_chan_map_capture.sv`) and its two commits: `6d1572d6` is the change, and
`553edeb8` is the manager's regeneration of `MODULE_MATRIX.md` and
`hdl/ieee1722/aaf/README-tests.md`. Last came the root wiring in
`hdl/milan/milan_datapath.sv` (aligner at 5562-5574, capture at 1207-1281,
settle logic at 5910-5957) and the NCO `hdl/ieee1722/crf/KL_media_nco.sv`,
which the diff does not change. The published author packet
`review-evidence/74-r1/author-a197/` (receipts README, G0-G6 comparison
files) was used for cross-checks only. Its `scratch/` tree was not read. No
other reviewer's material was read before this verdict and ledger were written.

Frozen item-2 scope used as the acceptance, from the assignment and the TAKEN
interpretation, with no public objection:

- (A1) At a slip-free lock where the frame marker races onto the tick,
  `tdm_dup_cnt_o` counts no phantom dups.
- (A2) A real dup or skip still counts exactly once.
- (A3) The fix is graded in simulation with a negative control.
- (A4) No counter or CSR word is added, removed or re-mapped, and `mr`
  triggers, CLOCK behaviour, shipping shape, pins and test populations are
  kept. `milan_datapath.sv` and `milan_csr.sv` stay untouched. The
  coincidence-law change is not an exception to this: it is the declared
  second half of the public DECISION, made before the edit.

## Findings

### F1 - MINOR - Docs - the `SLIP_TDM` paragraph overstates passage exactness and lock clearance

- **Where:** `docs/reference/REGISTER_MAP.md:1816-1825`, the new sentences.
  1. "the tick takes a marker that was already pending first, so a slow
     free-running passage counts once in its own direction" (1817-1819).
  2. "the align loop now also holds the marker at least 1/128 sample off the
     tick" (1822-1824).

  The INTERNAL row of the reading table directly below (1835, "dups climbing
  0.51/s") inherits the first.

  The same clearance wording appears in the RTL banner
  `hdl/ieee1722/crf/KL_media_grid_align.sv:84-86`: "under the lock the marker
  stays the keep-off clear of every tick".
- **Authority/evidence:**
  - The shipped law's own banner states the exactness condition that the
    register reference drops.
    `hdl/ieee1722/aaf/KL_chan_map_capture.sv:509-512`: "a passage whose marker
    dithers between two adjacent cycles counts once ... a wider dither on the
    way through adds balanced dup/skip pairs". The PR body says the same under
    "Passage exactness has a limit".
  - The PR's own model of the root, used by [G7]/[G8], is one edge of marker
    delivery jitter ("the root's capture FIFO pop",
    `tb/verilator/media_grid_align/README.md:37`). Under that model a
    free-running passage at this head counts 3-5 dups AND 3-6 skips. The net
    is exactly +1 or -1 in every run. It counts once only at zero jitter, which
    is all [G9] grades (`receipts/passage_head.txt`, 24 runs, 4 seeds, jitter
    0/1/2, both directions).
  - Clearance: the lock TARGET is `DIV_C/128` = 16 cycles, which is under
    1/128 sample (16.28 cycles). The measured marker clearance at lock is 15
    ([G7]) and 14 ([G8]) cycles. My 1-edge sweep minimum is 14, and the graded
    floor is 12 (`kLockClearMin`). "At least 1/128 sample" is therefore not
    what is shipped or measured
    (`receipts/lockprobe_sweep_head_settle2s.summary.txt`).
- **Impact:** `REGISTER_MAP.md` is the reference a bench reader uses to
  interpret the live `SLIP_TDM` word, and the #74 bench lines (items 1/4,
  #448) read these counters. At INTERNAL, on silicon with the modelled
  capture-FIFO jitter, the word would show skips climbing beside dups. That
  matches no row of the reading table. This is the same class of misreading
  that item 2 exists to remove.
- **Required outcome:** The authoritative text states the law the RTL
  implements:
  - the NET (dup - skip) counts one per free-running passage, in its
    direction;
  - each half is exact only while the marker dithers over two adjacent
    cycles, and a wider dither (such as the modelled 1-edge delivery jitter)
    adds balanced dup/skip pairs;
  - the INTERNAL row is consistent with that;
  - the lock clearance is stated as the keep-off target (16 cycles at
    100 MHz) with the marker dithering around it (graded floor 12 cycles),
    not "at least 1/128 sample".

  No RTL change is needed.
- **Verification:** Re-read the paragraph, the INTERNAL row and the aligner
  banner against `KL_chan_map_capture.sv:502-515` and
  `receipts/passage_head.txt`. Then run `scripts/docs_check.py`,
  `scripts/gen_toc.py --check`, `scripts/check_doc_style.py` and
  `scripts/check_em_dash.py --base ede8d48e` green on the corrected head.

## Suggestions (optional; they do not affect coverage)

- **S1 (Tests).** [G9] grades the passage only with zero delivery jitter. A
  jittered passage that grades net = +/-1 (and prints the raw halves) would
  bind the passage claim to the same root model [G7]/[G8] use.
- **S2 (Tests).** The suite does not grade the two headline properties of the
  keep-off. One is "a non-raced engagement is bit-identical"; the other is "a
  raced one is pulled at most the keep-off". My `keep_cross` mutant, which
  clamps a low capture to the HIGH bound, is caught only through its side
  effects on [G7]/[G8] clearance. `probes/equiv` shows one way to grade both
  directly.
- **S3 (Tests).** [G8]'s 1 s settle has little margin. At the same geometry
  (engage 2082 edges after a tick, 1-edge jitter, plan rate), some other
  jitter draws still cross the tick in the 1.0-1.2 s window, because the
  acquisition hit the pre-existing NCO tick drop (O1)
  (`receipts/lockprobe_head_selected.txt` lead 2082 seed 0x74A197: 91/92 in
  that window; `receipts/lockprobe_sweep_head_settle1s.summary.txt`: 7 of 208
  runs). [G8] is deterministic, so it is not flaky in CI. A harness change
  upstream of it could still turn it red for a reason outside its arm.
- **S4 (Docs).** The PR body asks for a release note because `SLIP_TDM`
  semantics changed: a free-running slip used to count about a dozen dups and
  now counts once, net. No rule requires one, but an `Unreleased` entry in
  `CHANGELOG.md` would keep that note from depending on memory.

## New work found outside this diff (recommend new public Issues; not attributed to PR #528)

### O1 - `KL_media_nco` can drop two packet-grid ticks when its trim changes on the terminal cycle

- **Where:** `hdl/ieee1722/crf/KL_media_nco.sv:206-216`, unchanged by this PR.
- **Mechanism:**
  - `cnt_r == end_w` is an equality against a combinational `end_w` that
    depends on `trim_r`.
  - A trim decrease that lands on the cycle where `cnt_r` = `DIV_C` (the last
    cycle of a lent-cycle period) flips `ov_w` to 0. The compare then misses,
    and `cnt_r` (12 bits) wraps through 4096.
  - The next tick arrives about 6179 cycles later: two ticks are missing.
  - The banner's premise at `KL_media_nco.sv:187-191` ("servo_trim_i moves at
    most once per servo tick ... about 1 ms") no longer holds. Since #74 the
    aligner rewrites the trim on every frame, at the frame marker's phase.
- **Evidence:**
  - `receipts/ftrace_nco_tick_drop_lead2082.txt`: a marker arrives 4164 edges
    after the last tick, inside a 6179-cycle tick interval. The next frame
    reads err -1997 with u at the +3200 clamp.
  - `receipts/trace_2082_j1_s74A197_head.txt`: a ~1 s excursion.
  - Head: 22 of 260 runs in `receipts/lockprobe_sweep_head_settle2s.txt`
    drop NCO ticks, every one during an acquisition that crosses the tick. No
    run drops a tick at lock.
  - Base: the same drop recurs AT a raced-from-below lock
    (`receipts/lockprobe_base_selected.txt` lead 2080: `nco_gaps lock=2`,
    err -830/-529 inside the lock windows).
- **Classification:** Pre-existing, and not worsened.
  - Non-raced engagements: cycle-identical to the base, so the exposure is
    identical.
  - Raced engagements: the keep-off replaces the base's permanent exposure at
    the lock with a bounded exposure during acquisition. At lock the u update
    now lands well clear of the NCO's terminal count.
- **Impact when it fires:** Under CRF selection, a real two-sample hole in the
  packet grid and a whole-sample loop excursion at the +/-200 ppm rail for
  hundreds of ms. It also leaves an unbalanced junction count, which is a
  real slip counted honestly. It also makes the PR body's "acquisition counts
  balanced pairs" statement incomplete.
- **Possible directions (for that Issue, not this lane):** For example, a
  terminal compare that cannot be stepped over, or a period end latched once
  per period. The fractional accounting must still hold.

### O2 - The unwrapper's +/-DIV_C/2 fold boundary under a surplus marker

- **Where:** `KL_media_grid_align.sv:221-227`, unchanged by this PR.
- **Mechanism:** A surplus (non-frame) marker that lands about half a sample
  from the lock phase sits exactly on the fold boundary. The next true frame
  then mis-folds (err -2082), and the loop slews a whole sample at the clamp.
  The counters honestly count the resulting real slip.
- **Evidence:** `receipts/ftrace_unwrapper_fold_lead1041.txt`: surplus
  coincident with the tick at a 1041 lock gives err -1041, then -2082. In the
  sweep, 3 of 327 boundary-offset injections counted extra pairs.
- **Classification:** Pre-existing and reachable only by a marker-law
  violation. It is recorded here because it bounds the "a surplus frame is
  exactly one skip" statement to offsets away from the half-sample point.

## Lens results (each with the artifact examined at this head)

- [R263] PASS Conformance - `KL_media_grid_align.sv:72-86,112-114,144-145,177-183,264`; `KL_chan_map_capture.sv:502-546`; `milan_datapath.sv:1207-1281,2577,5562-5574,5910-5957`; `receipts/*` - A1-A4 checked against the ledger item 2, the assignment and TAKEN.
  - A1: a lock raced on the tick counts 0/0 over 8 x 0.2 s ([G7]; base 10928/3163). Every engagement phase (26 phases x jitter 0/1/2/4 x both rates) counts 0 at lock after 2 s. The exceptions are only the jitter-8 plan cases whose acquisition was still running.
  - A2: a held frame at lock is 1/0 and a surplus is 0/1 at 12 offsets in all 260 runs, away from the O2 boundary.
  - A3: base RTL fails 13/45 and 3/204, exactly the new checks. The author's three mutants plus my eight mutants are all killed.
  - A4: the diff touches neither `milan_datapath.sv` nor `milan_csr.sv`. The new parameter is defaulted and not overridden at the root. The root consumers of the aligner and counters are only `SLIP_TDM` and the #386 settle, and a raced start's |err| <= 16 is inside its 32-cycle band. Test populations only grow (25 -> 45, 201 -> 204). No Milan wire behaviour changes; the lock phase moves at most 16 cycles, and only for raced engagements.
- [R263] PASS RTL - `KL_media_grid_align.sv:114,144-145,165-183,229-265`; `KL_chan_map_capture.sv:517-550` - checked against CONTRIBUTING section 1/3 and the module contracts.
  - No new state. The clamp uses 13-bit unsigned `TSTW_C` compares on `tst_next_w`, which is at most 2083 with ticks present and saturates at 4165.
  - The elaboration guard refuses `2*K >= DIV_C`, so the `DIV_C - K` localparam cannot underflow.
  - Declarations come before use, with no declaration-with-initialiser split.
  - The `unique case` in the capture keeps all four arms. `2'b11` is a hold of `pend` plus `fed`.
  - The added logic is two comparators and a 2:1 mux on the engage-only `ref_r` path.
  - The port lists are unchanged.
  - Lint output is byte-identical for base and head RTL (90 <= 90; crf 4 <= 4, aaf 17 <= 17: `receipts/lint_rtl_*.txt`).
  - `check_sv_idiom`, `measure_naming --check`, `check_port_contracts` and `check_cpp_idiom` pass (`receipts/static_gates_focused.txt`).
  - Lockstep base-vs-head (`receipts/equiv_lockstep*.txt`): all 2084 engagement phases, both rates, jitter 0 and 1. The loops diverge ONLY for captures in 0..15 and 2068..2083, and the first-frame error delta is at most 16 cycles. Every other phase is cycle-identical in tick, u, err and engaged, including 1 s runs at the band edges 16/17/2066/2067.
- [R263] PASS Robustness - `receipts/lockprobe_sweep_head_settle{1s,2s}*.txt`, `receipts/law_random.txt`, `receipts/equiv_lockstep*.txt`, `receipts/passage_head.txt` - checked malformed input, jitter margin, every engagement phase, repeated and re-engagement, and coincidence storms.
  - Malformed input: held and surplus markers at 12 offsets per lock, including one coincident with the tick.
  - Jitter: 0..8 edges.
    - At <= 4 edges the lock clearance is >= 13. The one exception is a plan-rate run engaged from below (lead 2075, jitter 2). It was still settling after two O1 NCO tick drops: clearance 1, with 0 counts.
    - At 8 edges the clearance is 11. Lock counts are 0, except two plan-rate runs still acquiring after 2 s (132 and 84 balanced counts).
    - Source: `receipts/lockprobe_sweep_head_settle2s.summary.txt`.
  - Engagement: every phase 0..2083 in lockstep, plus the watchdog re-engage and deselect paths ([G4]/[G5] unchanged).
  - Coincidence storms: 16M random cycles with 1.47M coincidences. Head equals an independent reference model on every cycle, with 0 violations of dup - skip = ticks - markers + pend; base violates it.
  - INTERNAL: free-run is untouched ([G1]/[G5], and lockstep while deselected).
  - The pre-existing O1/O2 are reported as new work. The diff does not introduce them and the keep-off reduces O1's exposure.
- [R263] PASS Tests - `tb/verilator/media_grid_align/{sim_main.cpp:271-378,Makefile,media_grid_align_wrap.sv:75-94}`; `tb/verilator/chmap_capture/sim_main.cpp:351-406` - checked each new check against its claimed defect.
  - Head: 45/45, all three Makefile negative controls RED; chmap 204/204 plus netlist 20/20; root `aclk` 139/139 (`receipts/media_grid_align_head_run.log`, `receipts/chmap_capture_head_make.log`, `receipts/aclk_head_rtl.*`).
  - Base RTL under the head harnesses: 13/45 and 3/204, and the G7 windows reproduce the PR's {0,0,771,2351,2431,1980,1694,1701} (`receipts/base_rtl_head_harness.txt`).
  - My mutants, run with fresh builds (`receipts/mutants/`), are all killed:
    - coincidence variants `coin_old`, `coin_set`, `coin_tickfirst` fail [G9] and one to three chmap [T0] checks;
    - keep-off variants `keep_no_hi` (fails [G8]), `keep_no_lo` (fails [G7]), `keep_small`/4 cycles (caught by the clearance checks alone), `keep_cross` and `keep_raw` all fail.
  - Real wiring: the wrap feeds the real capture the same `pv && slot==0` marker and NCO tick that `milan_datapath.sv:1259,1274,5569-5570` do.
  - G0-G6 output is byte-identical for base and head RTL (`receipts/g0g6_*`, sha matches the author's).
  - The C++ copy of the law follows the new RTL law. No existing check was removed or weakened.
  - S1-S3 are optional.
- [R263] MINOR Docs - `docs/reference/REGISTER_MAP.md:1816-1825,1835`; `hdl/ieee1722/crf/KL_media_grid_align.sv:84-86` - F1.
  - Everything else examined in the lens is accurate against the RTL and my measurements:
    - `KL_chan_map_capture.sv:502-515`;
    - `KL_media_grid_align.sv:72-86` apart from the clearance wording;
    - `docs/design/TIME_SYNC.md:113`;
    - `docs/testing/TESTING.md:428`;
    - `tb/verilator/media_grid_align/README.md` (G7-G9 rows, negative controls);
    - the regenerated `MODULE_MATRIX.md:71` and `hdl/ieee1722/aaf/README-tests.md:20`.
  - The docs gates pass: `docs_check`, `gen_toc --check`, `check_doc_style`, `check_em_dash --base ede8d48e` (0 findings over 37 added lines), `gen_module_matrix --check`, `git diff --check`.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ledger item 2 + assignment + TAKEN (A1-A4); `KL_media_grid_align.sv`, `KL_chan_map_capture.sv`; `milan_datapath.sv` consumers; lockprobe sweeps; base-RTL harness run; root `aclk` base-vs-head | R263-1 | 553edeb86b9144f7b15721255fbe5ad11ef1fe36 |
| RTL | CLEAN | both RTL diffs line by line; lockstep equivalence (2084 phases); lint base-vs-head; idiom/naming/port gates | R263-1 | 553edeb86b9144f7b15721255fbe5ad11ef1fe36 |
| Robustness | CLEAN | jitter 0..8, all engagement phases, held/surplus at 12 offsets, random coincidence storms vs reference model, passage probe, NCO/unwrapper traces (O1/O2 out of diff scope) | R263-1 | 553edeb86b9144f7b15721255fbe5ad11ef1fe36 |
| Tests | CLEAN | `media_grid_align` 45/45 + 3 controls; `chmap_capture` 204/204 + NC 20/20; base RTL 13/45, 3/204; 8 reviewer mutants all killed; `aclk` 139/139 byte-identical to base | R263-1 | 553edeb86b9144f7b15721255fbe5ad11ef1fe36 |
| Docs | UNCLEAN (F1 MINOR open) | `REGISTER_MAP.md` SLIP_TDM paragraph + reading table; RTL banners; `TIME_SYNC.md`; `TESTING.md`; bench README; regenerated matrix pages; docs gates | R263-1 | 553edeb86b9144f7b15721255fbe5ad11ef1fe36 |

Coverage is banked against `553edeb8`. A later commit that touches a lens's
scope un-covers it. F1 can be fixed with a docs-only change. A docs-only
correction touches no artifact in the Conformance, RTL, Robustness or Tests
scope as recorded above, so those four stay covered at any descendant whose
diff from `553edeb8` is docs-only. Docs must be re-covered at that head.

## Prior public review findings on this PR

I read the PR thread and the issue comments after the verdict and ledger
above were written. The only prior review is the [R262] round R262-1,
NEGATIVE at `6d1572d6` (issuecomment-5796351579). No review objects or inline
review comments exist on the PR.

| Prior finding | State at `553edeb8` | Basis |
|---|---|---|
| R262 F1 (BLOCKER, Docs): `MODULE_MATRIX.md:71` and `hdl/ieee1722/aaf/README-tests.md:20` stale | **RESOLVED** | `553edeb8` changes only those two rows, adding `media_grid_align` to `KL_chan_map_capture`. `docs/traceability/gen_module_matrix.py --check` at this head prints "traceability matrix up to date", rc 0 (`receipts/static_gates_focused.txt`). Observed only, not accepted: hosted `docs-check` job 107196343021 at this head succeeded with all 47 steps executed, 0 skipped, and step 16 "Traceability matrix no-drift gate" successful (`receipts/hosted_docs_check_steps_553edeb8.txt`) |
| R262 F2 (MINOR, Docs): `SLIP_TDM` paragraph overstates passage exactness and lock clearance | **RETAINED** as this round's F1 | `553edeb8` does not touch `REGISTER_MAP.md` or the aligner banner. I reached the same defect independently before reading R262. My passage probe is consistent with its numbers: 1-edge jitter gives 3-5 dups and 3-6 skips with net ±1, against R262's 3-6 and 2-7 (`receipts/passage_head.txt`) |
| R262 S1 (Docs, optional): say that acquisition can leave balanced pairs | Still optional; one addition | O1 shows that an acquisition crossing can also leave an UNBALANCED count, from a real NCO tick drop. If that note is written, it should not promise balance |
| R262 S2 (CHANGELOG) and S3 (jittered [G9] net check) | Still optional | Same as this round's S4 and S1 |
| R262 observation: hosted `verilator-suites` failed at `6d1572d6` because shards were cancelled | Superseded at this head | Observed only: `verilator-suites` and Verilator shards 0-4 succeeded at `553edeb8` |

The origin finding, PR #323 [R1] finding 1 (phantom dups at a raced lock), is
addressed at this head. The evidence is the Conformance line (A1) and
`receipts/lockprobe_*`.

R262 reports a slow-side lock "still converging at 1.5 s" and a slow-side
lock "still acquiring" at 8-16 edges of jitter. Both are consistent with O1,
where a dropped NCO tick during the crossing forces a whole-sample recovery.
I did not rerun R262's cases, so this is a candidate mechanism, not an
attribution.

## Evidence commands (portable; `$V` = the pinned Verilator 5.050, `$H`/`$B` = head/base trees)

- Suites: `make -C tb/verilator/media_grid_align` and `make -C tb/verilator/chmap_capture` (head; netlist leg included).
- Base RTL under head harnesses: `probes/base_rtl_head_harness.sh $H $B <scratch> receipts/base_rtl_head_harness.txt`.
- Reviewer mutants: `probes/mutants/run_mutants.sh $H <scratch> receipts/mutants`.
- Raced-lock sweep: `probes/lockprobe/build.sh $H $H <out>`, then `SETTLE=200000000 probes/lockprobe/sweep.sh <out>/lockprobe <file> "0 1 2 4 8"` (and `SETTLE=100000000 ... "0 1 2 4"`). Summaries: `probes/lockprobe/summarise.py`.
- Passage probe: `LP_PASS=1` through `probes/lockprobe/passweep.sh`.
- Traces: `LP_TRACE=1` or `LP_FTRACE=lo,hi` on `lockprobe`.
- Lockstep: `probes/equiv/build.sh $H $B <out>`, then `equiv <plan|fast> <frames> <jitter> [lo hi]`.
- Counter law: `probes/law/build.sh $H $B <out>`, then `law <cycles> <seed> <pm> <pt> <pc>`.
- Root: `probes/aclk_pair.sh <head_root> <base_root> <out>` (two full trees with pinned submodules; the base tree differs only in the two RTL files).
- Static: `scripts/{docs_check,gen_toc --check,check_doc_style,check_em_dash --base ede8d48e,lint_rtl --check,check_sv_idiom,measure_naming --check,check_port_contracts,check_cpp_idiom}.py`, `docs/traceability/gen_module_matrix.py --check`, `git diff --check` (`receipts/static_gates_focused.txt`). The first three code-quality gates in that receipt REFUSED on a scratch clone with no submodules, which is their designed behaviour. They were rerun, and passed, after the pinned submodules were initialised from the local checkouts (the second block of the receipt).
- Hosted, read only: 21 executed contexts succeeded at this head, including `rtl-fast`, `verilator-suites`, `yosys-portability`, Verilator shards 0-4 and Yosys shards 0-3. `Physical gPTP (nightly and manual)` was SKIPPED and is not evidence (`receipts/hosted_checkruns_553edeb8.txt`).

## Real limits

- `scripts/xvlog_gate.py` was not run (no Vivado on this host), and neither was `xelab`.
- The full parent, protocol-processor, gPTP, Yosys and builder banks, `act`, and every other `milan_dp`/`milan_dp_render` leg were not run. `aclk` is the only root leg reproduced here.
- Every counter result is simulation. The root's marker delivery jitter is modelled (0..W edges), not measured.
- Physical calibration was NOT RUN. Field skips are not hardware proof. The bench items 1 and 4 of the #74 ledger remain.
- The mutation set is a sample of eight hand-chosen mutants, not an exhaustive campaign.
- O1/O2 were characterised in the unit loop only. Their root-level rate was not measured.

## Clone integrity

All builds and probes ran in disposable trees under the packet's `scratch/`:
`git archive` extractions, and one local clone whose submodules came from
the pinned local checkouts. None of this touched the review clone's objects.

One mis-scoped command left an untracked 72-byte `run.log` at the review
clone's root. It came from a failed `cd` inside a subshell, and it contained
only a shell error line. I identified it as my own and removed it.

The final state is verified in `receipts/clone_integrity.txt`:

- HEAD `553edeb8` (detached) and tree `d78849a3`.
- The index is byte-identical to the baseline I recorded at the start
  (sha256 `daf51ccd...`), and it matches HEAD.
- All 864 regular files were rehashed against their blob ids and modes, with
  0 mismatches.
- There are no assume-unchanged or skip-worktree flags, and no untracked or
  ignored entries.
- The four gitlinks are unchanged (`external` is still uninitialised, as at
  the start).
- The three initialised submodule worktrees are clean at their gitlinks.

## Pending manager duties

- Publish the source static/builder and native bank results for this head. This round does not claim or infer them.
- Own hosted and `act` acceptance.
- Build and validate the final current-dev candidate at the merge turn.
- Route F1 back to the executor.
- Decide on and file new Issues for O1 and O2.
- Obtain the internal review verdict and a re-review of the F1 fix at its exact head (Docs lens; the other four stay covered only if the fix is docs-only, as stated above).
- Keep #74 open for items 1, 3 and 4.

R263-1 FINISHED
