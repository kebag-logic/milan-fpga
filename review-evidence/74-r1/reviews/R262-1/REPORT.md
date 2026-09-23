[R262] NEGATIVE - exact head 6d1572d6caeb94cd3dd871b9df90e4c5298998b6

Round R262-1: internal cleared-context review of issue #74 ledger item 2
(junction-counter raced-lock chatter), PR #528.

- Head `6d1572d6caeb94cd3dd871b9df90e4c5298998b6`, tree
  `5c66dc66bfae09bdd50143afcb318f91c2351ec9`, one commit on base
  `ede8d48ecd7c7f589a14b957951f040d92c99c70`.
- Items 1, 3 and 4 of #74 are out of scope and were not reviewed.

## Verdict in brief

The mechanism is sound. The executor chose a lock-phase keep-off in
`KL_media_grid_align` and repaired the coincidence branch in
`KL_chan_map_capture`. I reproduced every claim in the executor's evidence
with my own runs. I also probed well beyond the committed arms: 118 raced and
non-raced engagements, both rate directions, 100 MHz and 50 MHz, delivery
jitter from 0 to 16 edges, and step slips injected at each lock. None found a
defect in the RTL.

The verdict is NEGATIVE on the Docs lens alone:

- **F1 (BLOCKER).** The generated traceability matrix was not regenerated.
  The required hosted `docs-check` context fails at this exact head, and the
  failure reproduces locally.
- **F2 (MINOR).** The `SLIP_TDM` paragraph in `REGISTER_MAP.md` states two
  properties more strongly than the RTL banner and the PR's own evidence
  support.

Both fixes are text-only. Neither needs an RTL or harness change.

## Reconstruction (public state only)

- Contract: `AGENTS.md`, `CONTRIBUTING.md` (sections 2, 3 and 6.1), and
  `docs/README.md`, which puts requirements over interfaces, code, tests and
  summaries.
- `REQUIREMENTS.md` has no clause on the junction counters. Issue #74 cites
  Milan 5.3.11.1 and 7.2.2 for the media-clock work.
- Scope:
  - the #74 body;
  - ledger item 2 (issuecomment-5507453907);
  - the [A10] assignment (5794151797);
  - the [A197] TAKEN (5794228544), DECISION (5794560116) and REVIEW READY
    (5795282366) comments;
  - the origin finding, PR #323 [R1] finding 1 (issuecomment-5506033067);
  - the PR #528 body;
  - the [A10] review start (5795480660).
- Interface authorities:
  - `docs/design/TIME_SYNC.md`, Media boundary;
  - `docs/reference/REGISTER_MAP.md`, the 0x8D4 section (`SLIP_TDM`, 0x8D8);
  - `hdl/milan/milan_datapath.sv:1259-1274`, where the capture and counters
    are wired;
  - `milan_datapath.sv:5562-5573`, where the aligner is wired;
  - `milan_datapath.sv:5896-5960`, the settle band and recentre.
- Diff and history: `git diff ede8d48e..6d1572d6` (10 files, +357/-44, one
  commit whose message is one line with no trailer).
- Public evidence: `review-evidence/74-r1/author-a197/` at `9edfb9a1`
  (receipts README, handoff, decision). I read these only as claims to
  reproduce.

**Wiring fact that makes the unit harness representative.** The aligner and
the junction counters see the same two signals:

- the same frame marker, `aafcap_pv_w && aafcap_slot_w == 0`
  (`milan_datapath.sv:1259` and `:5569`);
- the same tick, `media_tick_p` (`:1274` and `:5570`).

So the aligner's capture phase is exactly the phase the counter races on. The
wrap `tb/verilator/media_grid_align/media_grid_align_wrap.sv:79-94` wires
both the same way.

## Scope decision on the coincidence-branch repair

I judge the repair to be inside item 2:

- **It was public before the edit.** The DECISION comment announced it.
- **It is necessary.** With the keep-off alone (`MGA_MUT_COIN`), the lock is
  clean, but three things stay wrong:
  - a free-running passage counts 11 dups for one slip;
  - a skip-direction slip is counted as 10 dups and 0 skips;
  - acquisition from below counts 331 dups against 46 skips.

  (Receipt: `receipts/head_MGA_MUT_COIN.log`.)
- **The old law hid slips.** It made the old caveat's "never a hidden slip"
  false. That is the same law that item 2's "false-alarm direction only"
  relied on.

## Findings

### F1: BLOCKER, Docs: generated traceability matrix not regenerated

**Where:**

- `docs/traceability/MODULE_MATRIX.md:71`, the `KL_chan_map_capture` row;
- `hdl/ieee1722/aaf/README-tests.md:20`, the same row.

**Authority:**

- `CONTRIBUTING.md` section 6.1: regeneration of a generator's committed
  Markdown is mandatory.
- `CONTRIBUTING.md` section 2.1: `docs-check` is one of the seven required
  contexts of the `dev` merge bar.
- `.github/workflows/docs.yml:122-123` runs
  `docs/traceability/gen_module_matrix.py --check`.

**Evidence:**

- **Hosted.** `docs-check` at this exact head (run 35864125964, job
  107191310168) failed at step 16, "Traceability matrix no-drift gate".
  Steps 17 to 45 were skipped. Receipt:
  `receipts/hosted_failed_steps_observed.txt`.
- **Local reproduction.** At head, `gen_module_matrix.py --check` prints
  `STALE` for both files with rc=1. At base it is up to date with rc=0.
  Receipt: `receipts/head_traceability_matrix_check.log`.
- **Cause.** The new wrap instantiates the real `KL_chan_map_capture`, so the
  regenerated row adds `media_grid_align` to that module's tests. After
  regeneration, `--check` returns rc=0. Receipt:
  `receipts/traceability_regen.diff`.
- **Coverage gap.** The REVIEW READY and PR-body gate lists do not include
  this gate. Their "docs gates exit 0" statement therefore does not cover it.

**Impact:**

- A required status context is red at the head, so the merge bar cannot be
  met.
- The committed trace understates the tests that cover
  `KL_chan_map_capture`.
- Product behaviour is unaffected.

**Required outcome:**

- Both generated files match the generator output at the new head.
- The hosted `docs-check` then runs past step 16 to completion.

**Verification:**

- `python3 docs/traceability/gen_module_matrix.py --check` exits 0 at the
  new head.
- The hosted `docs-check` succeeds at that exact head, with steps 17 to 45
  executed.

**Other lenses:**

- Not Tests: this is a documentation no-drift gate, and every touched suite
  and test ratchet is green.
- Not Conformance or RTL: no behaviour is involved.

### F2: MINOR, Docs: the `SLIP_TDM` paragraph overstates two properties

**Where:**

- `docs/reference/REGISTER_MAP.md:1816-1825`;
- the banner at `hdl/ieee1722/crf/KL_media_grid_align.sv:84-86`.

**Authority:**

- `AGENTS.md` section 6, Docs lens: changed contracts are reflected
  accurately in the authoritative docs.
- The RTL banner's own statement of the law,
  `hdl/ieee1722/aaf/KL_chan_map_capture.sv:509-512`.
- The PR's clearance floor, `tb/verilator/media_grid_align/sim_main.cpp:48-50`.

**(a) The passage law is stated without its condition.**

`REGISTER_MAP.md:1818-1819` says "a slow free-running passage counts once in
its own direction". The RTL paragraph limits that to a marker that "dithers
between two adjacent cycles" and says "a wider dither on the way through adds
balanced dup/skip pairs".

The PR models the root's frame marker with one edge of capture-FIFO delivery
jitter. That model is used in G7/G8 and in the DECISION's case that the
keep-off is required. Under it, the marker's dither is wider than two cycles.

My probe ran a G9-style passage against the same RTL (5 seeds, each
direction):

| Delivery jitter | Dups per passage | Skips per passage | Net |
|---|---|---|---|
| none | exactly 1 (slow) or 0 (fast) | 0 (slow) or exactly 1 (fast) | ±1 |
| 1 edge | 3 to 6 | 2 to 7 | exactly ±1 |
| 2 edges | 9 to 16 | 9 to 16 | exactly ±1 |

Receipt: `receipts/probe_passage.txt`.

The same page's ceiling row (`:1780`, "35.6 h") and reading row (`:1835`,
"dups climbing 0.51/s") hold only for the one-count case.

**(b) The clearance number is too high.**

`REGISTER_MAP.md:1823` says the loop "holds the marker at least 1/128 sample
off the tick". The banner (`KL_media_grid_align.sv:84-85`) says "under the
lock the marker stays the keep-off clear of every tick".

1/128 sample is 16.3 cycles at 100 MHz, and the target is 16 cycles. The
measured lock clearance is 14 to 15 cycles:

- [G7] measures 15 and [G8] measures 14 (`receipts/head_media_grid_align.log`);
- my 118-engagement sweep gives 14 to 15;
- the harness's own floor is 12, "the keep-off ... less the lock's own dither
  and the delivery jitter".

**Impact:** `REGISTER_MAP.md` is the reader-facing contract for the word that
#74's bench acceptance will read. Two consequences:

- A bench reader at INTERNAL with a jittered marker would see skips climbing
  beside dups. No row of the reading table matches that.
- The stated clearance is 1 to 2 cycles more than the design delivers.

**Required outcome:**

- The paragraph states the passage law with its condition, as the RTL banner
  already does.
- It says that, under a wider delivery dither, dups minus skips is the slip
  count.
- The clearance is stated as the keep-off target less the lock's dither and
  jitter, in `REGISTER_MAP.md` and in the aligner banner.

**Verification:**

- Text check against `KL_chan_map_capture.sv:502-515` and the
  `kLockClearMin` comment.
- The docs gates pass.

**Other lenses:** the RTL, the tests and the acceptance behaviour are correct
as they stand; only the prose overclaims.

### Suggestions (optional, do not affect coverage)

- **S1, Docs, `REGISTER_MAP.md` `SLIP_TDM` paragraph.** Say that acquisition
  can leave balanced pairs in the absolute counts.
  - An engagement within the loop's transient reach of a tick crosses it
    during acquisition. At the plan's -10.64 ppm that reach is about 40
    cycles, on the rate-offset side.
  - It leaves balanced pairs: 84/84 in [G8], and 65 to 110 in my one-edge
    sweep (`receipts/probe_sweep_jit1.txt`).
  - So only differences at lock are a verdict. The PR body and the bench
    README already say this; the authoritative page does not.
- **S2, Docs, `CHANGELOG.md`.** Add an Unreleased entry for the `SLIP_TDM`
  counting-law change. The house pattern is at `CHANGELOG.md:44`: "VERSION is
  unchanged; the release step owns the bump". The executor's handoff asks for
  a release note, but today it lives only in the PR body.
- **S3, Tests, `tb/verilator/media_grid_align` [G9].** Add a jittered passage
  that asserts net exactness, `dups - skips == +/-1`. That pins the property
  F2 asks the docs to state.
  - The shipped law passes it (`receipts/probe_passage.txt`).
  - The old law fails it: it hides the skip.

## Evidence (all at the exact head unless stated)

**Toolchain:**

- Verilator 5.050: the pinned wrapper
  `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`.
  - It prints `Verilator 5.050 2026-07-01 rev v5.050`.
  - Wrapper sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`.
  - `verilator_bin` sha256 `44898b22af4178b45214a0820a04eeac8632ae721ff005e69ef1cf69121bbfdd`.
  - The system `verilator` is 5.052 and was not used.
- `scripts/vwrap.sh` caps every Verilator build at 8 jobs; no step exceeded
  8 parallel jobs.
- The netlist leg and one lowering probe used Yosys 0.66 and sv2v v0.0.13.

**Isolation:** builds ran in disposable trees under `scratch/`:

- `git archive` extractions;
- a local clone with its submodules at the recorded gitlinks, for the legs
  that derive processor sources through git.

| ID | What | Result | Receipt |
|---|---|---|---|
| E1 | `make -C tb/verilator/media_grid_align` | 45/45. `MGA_MUT_U_SIGN` fails [G2] (11040). `MGA_MUT_NO_KEEPOFF` fails [G7] (5203 dups). `MGA_MUT_COIN` fails [G9] (11 dups) | `receipts/head_media_grid_align.log`, `receipts/head_MGA_MUT_*.log` |
| E2 | Head harness on base RTL (the two base files by blob id) | 13/45 fail, all in G7-G9. G7 windows are {0,0,771,2351,2431,1980,1694,1701} dups. At the base lock, a held frame counts 73/36 and a surplus 13 skips/21 dups; G8 counts 2278/356. G9: slow passage 10 dups; fast passage 0 skips and 9 dups | `receipts/headtb_basertl_media_grid_align.log` |
| E3 | Unchanged arms | Under the head harness, G0-G6 output is byte-identical for head RTL and base RTL. The base harness is 25/25 on both RTLs, with identical output | `receipts/base_media_grid_align.log`, `receipts/basetb_headrtl_media_grid_align.log` |
| E4 | `make -C tb/verilator/chmap_capture` | 204/204, netlist 20/20. Head harness on base RTL: 3/204 fail, exactly the new [T0] checks. Base harness on head RTL: 201/201, netlist 20/20 | `receipts/head_chmap_capture.log`, `receipts/headtb_basertl_chmap_capture.log`, `receipts/basetb_headrtl_chmap_capture.log` |
| E5 | `make -C tb/verilator/milan_dp aclk` | 139/139 at head. Rebuilt with the two base RTL files: 139/139, and the simulator output is byte-identical (sha256 `49c891b8...dbbf`). So this leg never reaches the changed paths | `receipts/head_milan_dp_aclk.log`, `receipts/*aclk.sim.out`, `receipts/baseRTL_milan_dp_aclk.log` |
| E6 | Static and docs gates | `lint_rtl --check` PASS 90 <= 90. `check_sv_idiom`, `measure_naming --check`, `check_port_contracts`, `check_cpp_idiom`, `measure_test_evidence --check`, `check_hygiene --check`: rc 0. `docs_check`, `gen_toc --check`, `check_doc_style`, `check_em_dash --base ede8d48e` (0 findings, 35 added lines), `git diff --check`: rc 0. Also rc 0: the nine docs-workflow steps the hosted failure skipped that this diff could touch | `receipts/head_lint_rtl_check.log`, `receipts/head_static_gates.log`, `receipts/head_docs_gates.log`, `receipts/head_docs_workflow_unexecuted_steps.log` |
| E7 | Traceability no-drift gate | STALE at head (rc 1), up to date at base (rc 0). See F1 | `receipts/head_traceability_matrix_check.log`, `receipts/traceability_regen.diff` |
| E8 | Reviewer mutants, each applied only on an exact single match (`scripts/apply_mutants.py`) | All 6 are killed by the committed arms. Details below | `receipts/mutants_summary.txt`, `receipts/mut_*.log` |
| E9 | Engagement-phase sweep: 59 phases, slow and fast, one edge of jitter, 1.5 s settle plus 5 x 0.2 s (`scripts/probe_main.cpp`) | 118/118 locks count 0/0. Clearance is 14 to 15 when the capture is clamped. The one exception, slow 2081, was still converging at 1.5 s: clearance 10 with zero counts. Acquisition leaves balanced pairs, net within 1, and only on the rate-offset side of a tick | `receipts/probe_sweep_jit1.txt` |
| E10 | Step slips at lock: 14 locks (raced from either side, both directions, plus mid-period) | A held frame is 1/0 every time. A surplus frame is 0/1, and so is an early step. The loop stays engaged | `receipts/probe_inject_jit1.txt` |
| E11 | Jitter margin at the raced locks | 0/0 at lock up to 6 edges with a 1.5 s settle. At 8 and 16 edges the slow-side lock is still acquiring at 1.5 s, and its counts are balanced. With a 4 s settle it is 0/0 with clearance at least 8 | `receipts/probe_jitter_margin.txt`, `receipts/probe_jitter_long_settle.txt` |
| E12 | 50 MHz shape (default keep-off 8 cycles; 18 engagements) | Lock 0/0, clearance at least 7. Held, surplus and early steps each count once | `receipts/probe50_jit1.txt` |
| E13 | Keep-off guard | Verilator reports the new `$error` at `LOCK_KEEPOFF_CYC_P` = 1042 and is silent at 1041. Severity matches the existing guards: USERERROR, fatal without `-Wno-fatal`. sv2v and Yosys lower the aligner at 100 and 50 MHz with rc 0 | `receipts/head_align_guard_probe.log`, `receipts/head_align_sv2v_yosys.log` |
| E14 | Free-running passage with delivery jitter | See F2(a) | `receipts/probe_passage.txt` |
| E15 | Hosted checks at head (observed, not accepted) | Listed below | `receipts/hosted_checks_observed.txt`, `receipts/hosted_failed_steps_observed.txt` |

E8 detail, which committed arm kills each reviewer mutant:

| Mutant | Change | Killed by |
|---|---|---|
| MA1 | no high-side clamp | [G8]: 636/637 at lock, clearance 0 |
| MA2 | no low-side clamp | [G7]: 5203/5203, clearance 0; held 60/59 |
| MA3 | keep-off of 4 cycles | the [G7] and [G8] clearance checks only (3 and 1 cycles); counters stay 0. So the clearance check is load-bearing |
| MC1 | coincidence always pends | [G9] and 3 [T0] checks |
| MC2 | consistent tick-first order | [G9] and [T0] "coincidence counts nothing (dup)" |
| MC3 | consistent marker-first order | [G9] and 3 [T0] checks |

E15 detail, hosted checks observed at this head:

- `docs-check`: failure (F1).
- `rtl-fast`: success.
- `elaborate`: success.
- `docs-check-no-git`: success.
- `wire-accountability`: success.
- `yosys-portability`: success.
- `verilator-suites`: failure, but not a test result. The `rtl-full` run
  concluded `cancelled`: Verilator shards 1/5 and 4/5 were cancelled inside
  step 14, and the aggregate then failed closed. I draw no inference from it.

**Receipt sanitisation:** the pinned tool's include root appeared in build
logs. Its home-directory prefix is replaced by `$HOME` in every receipt;
nothing else was altered.

## RTL review notes (basis for the clean lenses)

**`KL_media_grid_align.sv`:**

- **Where the new code is.** `LOCK_KEEPOFF_CYC_P` defaults to
  `DIV_C/128`: 16 cycles at 100 MHz, 8 at 50 MHz (`:114`). The guard
  `2*K >= DIV_C` is at `:144-145`. The unsigned 13-bit clamp `ref_keep_w`
  is at `:179-183`.
- **The one line that uses it.** The clamp feeds only `ref_r` in the single
  engage/re-engage branch (`:264`).
  - That branch is shared by fresh selection and watchdog re-engagement, so
    both paths are steered.
  - A capture in [16, 2067] is used unchanged, so a non-raced engagement is
    bit-identical (E3, E5).
- **Widths.** `KEEP_LO_C` and `KEEP_HI_C` cannot truncate under the guard.
- **Interface.** No port changed, and the new parameter is defaulted. The
  initial error of a raced engagement is at most the keep-off, which is
  inside the root's `SRC_SETTLE_ERR_C` band of `DIV/64`
  (`milan_datapath.sv:5910`).

**`KL_chan_map_capture.sv:541-546`:**

- **The new law.** At a coincidence, pend is kept. With nothing pending, the
  tick takes the coincident marker. With one pending, the tick takes it and
  the coincident marker pends.
- **Net accounting is exact.** From the first frame on (the unfed gate) and
  below saturation, the law preserves
  `ticks - markers == dups - skips + (initial pend - pend)` in every state,
  so dups minus skips tracks the true slip within one. The old branch broke
  this identity by one dup-direction count per coincidence over a pending
  marker.
- **No new state.** Reset and the unfed gate are unchanged.

## Out-of-scope observations (pre-existing, not findings of this round)

- The `U_LIM_PPM16_P` guard at `KL_media_grid_align.sv:142` is computed in
  `int unsigned`. It stays silent when `2*DIV_C << KP_LOG2_P` exceeds 32767;
  `KP_LOG2_P=6` lints clean. This diff does not touch it.
- G0-G6's C++ copy of the junction law pairs a marker with the tick produced
  on the same edge, while the RTL samples that tick one edge later. The new
  arms G7-G9 read the real counters instead.
- sv2v lowers the elaboration `$error` guards to `initial $display`, so Yosys
  does not refuse a bad parameter. This holds for every guard in the module.

## Reviewer-owned ledger (round R262-1)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #74 ledger item 2 and the [A197] TAKEN/DECISION interpretation against the diff. Raced lock: 0/0 from either side, both directions, both clocks (E1, E9, E12). Real step slips count exactly once (E1 [G7], E10). Non-raced engagement bit-identical (E3, E5). No shape, pin, CSR, `mr` or settle change: the diff touches no `milan_datapath.sv` or `milan_csr.sv`. Negative controls fail at base (E2, E4). Coincidence repair judged in scope (section above) | R262-1 | `6d1572d6caeb94cd3dd871b9df90e4c5298998b6` |
| RTL | CLEAN | `KL_media_grid_align.sv:112-114,144-145,177-183,264`; `KL_chan_map_capture.sv:529-548`; the wiring at `milan_datapath.sv:1259-1274,5562-5573,5896-5960`; widths, guard and portability (E13); lint (E6) | R262-1 | `6d1572d6caeb94cd3dd871b9df90e4c5298998b6` |
| Robustness | CLEAN | Phase boundaries at 15/16/17 and 2066/2067/2068 (E9). Held, surplus and early steps at lock (E10). Jitter 0 to 16 edges (E11). 50 MHz (E12). Watchdog and reselect share the clamped branch (`:250-265`). No new reset state. Unfed gate and saturation unchanged (`KL_chan_map_capture.sv:521-548`) | R262-1 | `6d1572d6caeb94cd3dd871b9df90e4c5298998b6` |
| Tests | CLEAN | [G7]-[G9] and the 3 new [T0] checks fail at base (E2, E4). The two committed mutants fail on their own arms (E1). All 6 reviewer mutants are killed (E8). Existing arms unchanged (E3). Integration leg green (E5). The `MGA_MUT_COIN` recipe refuses a no-op substitution (`Makefile`). S3 is optional | R262-1 | `6d1572d6caeb94cd3dd871b9df90e4c5298998b6` |
| Docs | UNCLEAN | F1 (BLOCKER): `docs/traceability/MODULE_MATRIX.md:71` and `hdl/ieee1722/aaf/README-tests.md:20` are stale (E7, E15). F2 (MINOR): `REGISTER_MAP.md:1816-1825` and `KL_media_grid_align.sv:84-86`. Checked without finding: the `TIME_SYNC.md:114` row, the `TESTING.md:428` row, `tb/verilator/media_grid_align/README.md`, and the `KL_chan_map_capture.sv:502-515` banner. No stale caveat wording remains in current docs. Docs gates in E6 | R262-1 | `6d1572d6caeb94cd3dd871b9df90e4c5298998b6` |

## Prior public review findings on PR #528

I read the PR thread only after the verdict and ledger above were written
(observed 2026-09-23T14:07Z).

- **Prior review findings: none.** The PR has no review, no review comment,
  and no `[R<n>]` comment before this round. Nothing needs resolving or
  retaining. PR #323 [R1] finding 1, the origin of item 2, is addressed by
  this change at this head (Conformance row above).
- **Another round has started, R263-1** (started 14:01:35Z, on a newer
  head). It has posted no report, and I read none.
- **Manager evidence, not a review.** The [A10] "SOURCE VALIDATION r1"
  comment (issuecomment-5795493487) independently reports F1's two stale
  files at `6d1572d6`. It states that regenerated output was committed as
  `553edeb86b9144f7b15721255fbe5ad11ef1fe36`, which is now the PR head.
- **What I checked of `553edeb8`: GitHub metadata only.**
  - Its parent is `6d1572d6`.
  - It modifies only `docs/traceability/MODULE_MATRIX.md` and
    `hdl/ieee1722/aaf/README-tests.md`, +1/-1 each.
  - I did not review it.
- **Consequences for the ledger:**
  - F1 is **retained at `6d1572d6`**. Its closure must be verified at
    `553edeb8` by a round that applies Docs there.
  - F2 is untouched by `553edeb8`, so it remains open at that head too.
  - `553edeb8` changes only Docs-scope files. Under AGENTS.md section 7, the
    four lenses banked CLEAN here at `6d1572d6` still cover that descendant,
    unless a later commit touches their scope.

## Real limits of this round

- **Not run** (out of bounds or not available):
  - the full parent, protocol-processor, gPTP, Yosys and builder banks;
  - act or the host `act_ci` runner;
  - hosted re-runs;
  - `xvlog_gate` (no Vivado front end on this host);
  - candidate-merge validation;
  - physical calibration and the bench. These are NOT RUN, and nothing here
    is hardware proof.
- **Jitter model.** The root's marker-delivery jitter is modelled here as a
  uniform 0 to J edges, as the executor modelled it (0 or 1). Its silicon
  width is unmeasured.
- **Integration coverage.** The root-level true-ratio leg is byte-identical
  with base RTL (E5), so no integration test drives a raced engagement
  through the real capture-FIFO crossing. The unit wrap uses the real modules
  of all three stages, wired as the datapath wires them.
- **50 MHz.** That shape is covered only by my probe, not by a committed arm.

## Pending manager duties

- Re-run the hosted `docs-check` after the F1 fix, at the PR head that
  carries it (`553edeb8` as observed). Its steps 17 to 45 have not executed
  at `6d1572d6`. F2 still needs a text change at a later head.
- Re-run the hosted `verilator-suites`: two shards were cancelled at this
  head, and no pass exists.
- Own the full source static/builder and native banks for this head. They
  are still running, and I make no claim about them.
- Own act and hosted acceptance, and the current-dev candidate at the merge
  turn.
- Items 1 (bench probe), 3 and 4 of #74 remain open.
- Any later commit un-covers every lens whose scope it touches.

R262-1 FINISHED
