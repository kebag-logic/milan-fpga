[R395] NEGATIVE - exact head ddb0774779d10a9b0bd90a4822f4e5df9fdedb1b

Round R395-3 is an external independent review of PR #618 for issue #617.

| Item | Value |
|---|---|
| Exact head | `ddb0774779d10a9b0bd90a4822f4e5df9fdedb1b` |
| Tree | `8ed377b8eae84e92b00387b7ce377e6aaa763cd1` |
| Source base | `ce550952e47fbd92367f0d9b099345100f7f4215` |
| Round-3 range | `377d1ac3..ddb07747` (four commits) |
| Rulings applied | issue 617 comment 5879911799 |
| Lenses covered | Conformance, RTL, Robustness, Tests, Docs |

## Verdict in one paragraph

The round-3 RTL answer is correct.

- **NCO fix.** `KL_media_nco`'s monotone terminal compare keeps one tick per period whatever cycle a trim update lands on. The count never wraps. A steady trim is bit-for-bit unchanged.
  - My re-run of `media_nco` check 10: it passes at the head and fails 10 times with the `377d1ac3` NCO.
  - My fine crossing probe reports 0 failures at -50 and -60 ppm, and at +50 ppm. The committed `CRF-fine-50` reproduces: 768 engagements, last slip at column 57.
  - The `==` mutant is killed in both of its legs. The area figures reproduce exactly at the datapath's binding.
- **Keep-off binding.** The wrapper binds `milan_datapath`'s own keep-off declaration, and RM5 is killed.
- **Envelope.** I re-measured the envelope and the settled lock myself: 136 engagements across the whole frame at +/-80 and +/-100 ppm, 100,000 columns each. None has a tail slip, and each lock settles about 250 cycles off the crossing.
- **Grading change.** A lock tail may not start inside the engagement window. This is a sound rule and it hides no defect. The slips it admits at -60 ppm are single, net-zero repeat/skip pairs during acquisition, and the documents name them. A tail that can never start fails `[V]`, so the rule cannot pass a run vacuously.
- **Full local suite.** Every committed arm reproduces locally: junction 20,832/0, datapath 332/0, mutation arm 27/27, `chmap_capture` 371/0 + 20/0, `media_grid_align` 45/0 with its three negative controls red.

What does not hold is the suite on the hosted gate.

- At this exact head (merge ref `7abe4d52`), hosted `Verilator shard 1/5` fails `capture_coherence`. The mutation arm's `dp` and `dp-band` clean controls and both of their mutants "did not compile". The CI result is 23 PASS, 4 FAIL.
- The same four items failed the same way at `377d1ac3`.
- They pass locally, both on the source head and on the exact hosted merge tree. The arm discards build output, so the CI log cannot say why.
- The suite also used 1,442 s of its 1,800 s hosted guard with those four builds not completing. A working arm would very likely exceed the guard.

That is F1. It is a BLOCKER under Tests: the PR's own suite is red on a mandatory hosted context at the exact head.

## Findings

### F1 - BLOCKER - Tests - `capture_coherence`'s datapath mutation legs do not build on the hosted runner, so the suite fails the exhaustive gate at this exact head, and its duration leaves no room to fix that inside the 1,800 s guard

- **Where.**
  - `tb/verilator/capture_coherence/mutants.py`:
    - `LEGS["dp"]` and `LEGS["dp-band"]` (the `make -s -C . dp-build DP_SRC=<temp copy> DP_MDIR=<temp dir>` recipe);
    - `build()`, which captures the build's output and never prints it.
  - `tb/verilator/capture_coherence/Makefile`: `dp-build`, and the `all: run dp mutants` chain.
  - `scripts/run_all_suites.sh:247`: the 1,800 s default per-suite guard.
- **Authority.**
  - AGENTS.md section 7: an RTL-relevant PR head needs exact-head `verilator-suites` evidence after it is marked ready.
  - AGENTS.md section 6, Tests: "Existing regressions remain green", and each committed mutant must be able to fail.
  - The mutation arm's own rule: "a mutant that cannot build proves nothing about the harness".
  - The round-3 review scope, item 6: judge the hosted CI risk and whether the suite needs a quick/full split.
- **Evidence.**
  - Hosted `rtl-full` run 36502597828 validates merge ref `7abe4d5261a91ee17aaa5dbffd6933bbd68ad64f` (dev `eaa88a32` plus this head). Its job `Verilator shard 1/5` concluded `failure` at 01:23:37Z with `failing suites: capture_coherence` and 4 in-suite failures (`receipts/hosted-ddb07747-shard1.txt`).
  - The suite's artifact log shows junction 20,832/0 and datapath 332/0. The mutation arm then reports:
    - `[FAIL] the unmutated source does NOT pass the dp harness (did not compile)`;
    - the same for the `dp-band` harness;
    - both `dp`/`dp-band` mutants "did not compile";
    - `27 checks: 23 PASS, 4 FAIL`.
  - The previous head failed identically: run 36487875476 at `377d1ac3`, `19 checks: 15 PASS, 4 FAIL` (`receipts/hosted-377d1ac3-shard1.txt`). Nothing in round 3 touches this path, and no public comment records it.
  - Locally the same four items pass:
    - on the source head (`receipts/mutants-dp.log`, `receipts/mutants-dp-band.log`);
    - on a scratch checkout of the exact hosted merge commit `7abe4d52`, whose submodule gitlinks match the head's (`receipts/merge7abe4d52-mutants-dp-control.log`).

    So the failure is not a merge interaction with live dev. It depends on the hosted environment, and `build()` suppresses the compiler output that would show which step fails.
  - **Duration.**
    - `capture_coherence` ran 1,442 s on the hosted shard (00:23:11 to 00:47:13). That is 80% of its 1,800 s guard, up from 1,042 s at `377d1ac3`.
    - This figure excludes whatever the four `dp` builds and runs would have cost had they compiled. Locally those four items cost about 300 s of the arm (`receipts/mutants-dp*.log`): each is a whole-`milan_datapath` Verilator build plus a `--quick` or `--band` run.
    - The committed chain takes 1,236 s locally (the author's figure) and ran 1,442 s hosted. A working arm is therefore likely to cross 1,800 s on the hosted runner. `run_all_suites.sh` reports that as TIMEOUT, which is not a pass.
- **Impact.**
  - The mandatory exhaustive context is red on this PR's own suite, so the PR cannot meet the completion bar.
  - In CI, the `dp` and `dp-band` legs never test their two mutants: the one-pair TDM frame length that `milan_datapath` hands over, and `milan_datapath`'s round-1 aligner binding. Only local runs exercise those two legs.
  - The fix route is constrained by the guard. Making the builds work in CI without also changing where the suite's time goes is likely to turn FAIL into TIMEOUT.
- **Required outcome.**
  - `capture_coherence` passes on the hosted exhaustive gate at the exact head, inside the runner's per-suite guard. The `dp` and `dp-band` controls and mutants build, and each mutant is caught by its named check.
  - The design choice is the author's and the manager's. Options include:
    - a quick/full split (for example the mutation arm, or its `dp` legs, as a separately scheduled or separately guarded target);
    - a suite-specific guard, as `milan_dp` has;
    - building the `dp` mutants where the hosted runner can.
  - A failing mutant build prints enough of its compiler and make output to diagnose it from the CI log.
  - The PR's evidence states the hosted duration against the guard it runs under.
- **Verification.**
  - Hosted `Verilator shard 1/5` at the new exact head passes `capture_coherence`. Its artifact log shows the `dp` and `dp-band` clean controls passing and both mutants caught.
  - The suite's hosted wall time is below its guard, with the margin stated.
  - A planted build break in a `dp` mutant shows its compiler error in the log.

### Suggestions (non-blocking)

- **S1 (Docs, Robustness): the negative-side on-crossing limit is understated, and its stated evidence does not reproduce.**
  - These all say "about 63 ppm below nominal, 67 above", with the evidence "net zero at -62 and +66, carried across at -63 and +68":
    - `docs/design/TIME_SYNC.md` "The guarded crossing";
    - `docs/reference/REGISTER_MAP.md` `SLIP_TDM`;
    - the `KL_chan_map_capture.sv` banner and the `milan_datapath.sv` binding comment;
    - `coherence_bench.hpp` `engage_columns()`;
    - the PR body.
  - My probes, with engagements on and just before the crossing:
    - **-63 ppm**, every quarter cycle x 64 sub-step phases, 768 engagements at 12,000 columns: no engagement is carried across. The close's excursion past its engagement point is at most one cycle. Every slip is one net-zero pair, by column 426 (`receipts/probe-fine-m63-long.log`, `receipts/probe-fine-m63-pre-long.log`).
    - **Further out**, the last slip moves out smoothly: column 615 at -64, 907 at -65, 1,323 at -66, 1,692 at -67 and 2,918 at -70. The excursion reaches only +6 cycles at -70 (`scripts/probe_crossing/excursion.sh` over those receipts).
    - **Positive side**: the break is sharp, as stated. +66 clears by column 8, and +67 dwells until column 1,143.
  - The stated negative limit is conservative, which is the safe direction. Every regime still yields one counted, net-zero pair, and nothing in the RTL or the committed grading depends on the figure. So I do not hold a lens on it.
  - A future edit could either describe the negative side as a gradual stretch with no sharp limit near 63 ppm, or cite the probe that shows a carried-across engagement there.
- **S2 (Docs): the NCO area figures depend on `TRIMW_P`.**
  - The PR's figures ("LUT 101 -> 106" at 50 MHz, "103 -> 104" at 100 MHz) reproduce exactly with `TRIMW_P = 18`, as `milan_datapath` binds it (`receipts/ooc-nco.txt`).
  - At the module default of 16 they read 106 -> 106 and 101 -> 103.
  - Either way, CARRY4 goes 35 -> 37 and the FF count is unchanged.
  - Naming the elaboration would let a reader reproduce the figures.
- **S3 (Tests): the new `make run` target of `media_nco` does not accept an absolute `MDIR`.** It runs `./$(MDIR)/Vmedia_nco_sim`, which fails with rc 2 for an absolute path (`receipts/nco377d1ac3-media_nco.log`). The mutation arm uses `build`, so nothing committed is affected.
- **S4 (Tests): `CRF-settle` grades a lock that is still converging.**
  - At 30,000 columns the tail spread is 109 to 159 cycles, against the quarter-frame `[V]` bound of about 260.
  - At 100,000 columns it settles to 8 to 14 cycles, about 250 cycles off the crossing (`receipts/probe-settle*.log`).
  - The committed claim holds, but its committed margin is thin. A longer run, or a tighter `[V]` bound for the settle scenarios, would make "settled" literal.

## Lens results with evidence

All results are at `ddb07747`.

### Conformance: CLEAN

Checked against ruling 1:

- Check 10 reproduces: 410/0 at the head (`receipts/head-media_nco.log`), and 400/10 with the `377d1ac3` NCO, all 10 in check 10 (`receipts/nco377d1ac3-media_nco-run.log`).
- `CRF-fine-50`: 768 runs, 141 slipping, every one net zero, last slip at column 57 (`receipts/head-capture_coherence-junction.log`).
- The `==` mutant is caught in the `nco` and `fine` legs (`receipts/mutants-r3a.log`, `receipts/mutants-r3b.log`).
- My `run_fine` probe reports 0 failures at -50 (20,544 checks), -60 (20,544) and +50 ppm (25,664) (`receipts/probe-fine-m50.log`, `receipts/probe-fine-m60.log`, `receipts/probe-fine-p50.log`).
- The area reproduces exactly (S2).

Against ruling 2: `mga_keepoff.py` copies the declarations, and RM5 is caught in `band50`.

Against ruling 3:

- The settled lock is guarded at +/-80 and +/-100 ppm. That holds in the committed `CRF-settle` and in my 136-engagement whole-frame probe at 100,000 columns: 0 tail slips, 0 failures.
- The limits reproduce:
  - unpulled transients of 238 cycles at 80 ppm and 298-299 at 100;
  - no crossing at +/-86;
  - crossings at -88 and +90 (`receipts/probe-transient*.log`).
- The `kEngageColumns` derivation holds: (64 - 50) ppm x 1041.7 cycles per frame is 0.0146 cycles per frame, so 68 frames, less about 4, gives 64 columns. It is measured at 57.

Against rulings 4 and 5: see RTL and Tests. Ruling 6: see Docs.

#617 acceptance 1-3 holds in simulation.

### RTL: CLEAN

I read `KL_media_nco.sv:241` (`>=`) with `:199-252`.

- `end_w` is always DIV-2, DIV-1 or DIV, and both sides of the compare are unsigned 32-bit. The count increments from 0, so it terminates by DIV at the latest and never wraps. `CNTW_C` holds DIV+1.
- At a steady trim the count meets the end exactly, so the compare behaves exactly like `==`.
- An update that lands on the old end and lowers the end closes the period at its old length, booked with the new trim. That is a one-cycle phase step.
- The step is two cycles only for a trim change of more than `DEN_C` LSB. At 50 MHz the clamp (+/-16,000) makes that unreachable. At 100 MHz it lies beyond the servo's +/-200 ppm authority.
- The CRF select and deselect switch the trim on any cycle, and the same compare covers them.

The NCO's consumers in `milan_datapath.sv` all count ticks or advance once per tick, and none measures the period's length. A one-cycle step with no lost or extra tick leaves each of them exact:

- the lrclk tap (`:759`);
- the media tone pilot (`:787`);
- the capture crossbar walk (`:1288`);
- the #386 recentre tick counter (`:6104`);
- the render feed (`:6282`);
- the aligner's delayed tick (`:5719-5722`).

`KL_crf_tx` and `KL_mmcm_drp_servo` run on `clk_audio` and do not consume `media_tick_p`. In the datapath the NCO's only trim source is the aligner's `u` (`:5735`).

The round-3 edits to `KL_media_grid_align.sv`, `KL_chan_map_capture.sv` and `milan_datapath.sv` are comment-only. Area: `receipts/ooc-nco.txt`.

### Robustness: CLEAN (S1 and S4 are suggestions)

Probes of the envelope beyond the committed band:

- **±55 to ±80 ppm**, placements every 8 cycles across ±264 of the crossing, 20,000 columns each (`receipts/probe-raced*.log`):
  - at ±55, ±60, -62 and +66, no placement slips;
  - at ±80, only raced engagements within about 60 cycles of the crossing slip, each with one net-zero pair by column 6,300.
- **On the crossing at ±70 and ±75 ppm**: net-zero single pairs by columns 2,918 and 4,737, with no tail slip (`receipts/probe-oncross*.log`).
- **Settled lock at ±80 and ±100 ppm**: no tail slip, and the lock sits about 250 cycles off the crossing (`receipts/probe-settle*.log`).
- **Tallies**: across all the probe receipts, 4,697 engagements tally 0/0 and 739 tally 1/1. None has any other count.
- **INTERNAL**: the trim is held at 0, so the grid is bit-for-bit what it was.
- **Reset**: unchanged.

### Tests: UNCLEAN (F1)

Locally, every committed arm reproduces:

| Arm | Result | Receipt |
|---|---|---|
| Junction | 20,832/0 | `receipts/head-capture_coherence-junction.log` |
| Datapath | 332/0 | `receipts/head-capture_coherence-dp.log` |
| Mutation arm | 27/27: 8 controls and 19 mutants, each mutant caught by its named check | `receipts/mutants-*.log` |
| `chmap_capture` | 371/0 plus netlist 20/0; the `[Q]` arm's 53 checks pass | `receipts/head-chmap_capture.log` |
| `media_grid_align` | 45/0, with its 3 negative controls red | `receipts/head-media_grid_align.log` |
| `media_nco` | 410/0 | `receipts/head-media_nco.log` |

The new mutants are caught by these checks:

| Mutant | Caught by |
|---|---|
| RM7 | `Q: col 2 pair 0 L is frame 4` |
| RM8 | `Q: col 1 pair 2 L is frame 2` |
| RM5 | `[C] slips while the CRF lock held` |

The grading change is sound:

- `tail_start()` changes nothing for committed scenarios within ±50 ppm, where the 64-column window is under half the run.
- The settle scenarios run with an unbounded window, so their tail is the second half.
- `lock_seen` is set only in the tail, so a tail that never starts fails `[V]`.

The open problem is on the hosted gate (F1).

### Docs: CLEAN (S1 and S2 are suggestions)

Checked:

- `TIME_SYNC.md`:
  - the loop-table NCO row;
  - the latency table's scope and its "Other shapes" row;
  - "The guarded crossing" and both of its tables;
  - the sweep table.
- `REGISTER_MAP.md`: `SLIP_TDM` and the verdict table.
- The RTL comments:
  - the `KL_chan_map_capture.sv` banner;
  - the `KL_media_grid_align.sv` banner (the settle-band sentence is scoped to the module default, and a pointer names the binding);
  - the `milan_datapath.sv` binding comment.
- `CHANGELOG.md` and `TESTING.md` (nineteen mutants).
- The `media_nco` README: row 10 and its mutant row.
- The PR body.

I cross-checked the documented figures against my own run:

| Figure | My run |
|---|---|
| True-plan band | one pair, by column 12 |
| `CRF-fine-50` | 141 slipping, last by column 57 |
| `CRF-settle` | last slip at column 13,065 |
| Unpulled transients | 238 and 299 cycles |

All are accurate, apart from the conservative negative-side limit (S1).

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #617 rulings 5879911799 items 1-6; `media_nco` check 10 at the head and with the `377d1ac3` NCO; `CRF-fine-50`; fine probes at -50/-60/+50; settle, limit and transient probes; OOC NCO area | R395-3 | ddb0774779d10a9b0bd90a4822f4e5df9fdedb1b |
| RTL | CLEAN | `KL_media_nco.sv:178-252`; NCO consumers in `milan_datapath.sv:736-787,1288,5700-5739,6104,6282`; comment-only diffs in `KL_media_grid_align.sv`, `KL_chan_map_capture.sv`, `milan_datapath.sv`; `receipts/ooc-nco.txt` | R395-3 | ddb0774779d10a9b0bd90a4822f4e5df9fdedb1b |
| Robustness | CLEAN | Raced, on-crossing, limit, transient and settle probes from 55 to 100 ppm; INTERNAL, reset and select/deselect trim paths | R395-3 | ddb0774779d10a9b0bd90a4822f4e5df9fdedb1b |
| Tests | UNCLEAN (F1) | `tb/verilator/capture_coherence/*` (Makefile, `mga_keepoff.py`, wrapper, bench, `sim_main.cpp`, `sim_dp.cpp`, `mutants.py`); `tb/verilator/chmap_capture` `[Q]`; `tb/verilator/media_nco` check 10; the full mutation arm re-run locally; hosted runs 36502597828 and 36487875476 | R395-3 | ddb0774779d10a9b0bd90a4822f4e5df9fdedb1b |
| Docs | CLEAN | `TIME_SYNC.md`, `REGISTER_MAP.md` `SLIP_TDM`, the three RTL banners and comments, `CHANGELOG.md`, `TESTING.md`, the `media_nco` README, the PR body | R395-3 | ddb0774779d10a9b0bd90a4822f4e5df9fdedb1b |

## Prior public findings on this PR, resolved or retained at ddb07747

I read these only after the verdict and ledger above were written.

### Round 2: my own findings (R395-2)

| Prior finding | Status at this head | Evidence |
|---|---|---|
| R395-2 F1 (MAJOR): the NCO terminal race lost two media ticks at -50 ppm | **RESOLVED** | See Conformance and RTL. In my `run_fine.sh -50 -1 2` probe, the placements that failed at `377d1ac3` (phases 34-36) now pass, with 0 failures in 20,544 checks. |
| R395-2 F2 (MINOR): the keep-off constant was unprotected | **RESOLVED** | The wrapper binds the datapath declaration through `mga_keepoff.py`. RM5 is committed and caught in `band50` (`receipts/mutants-r3a.log`). The full junction run also binds that declaration, so the ±50 ppm bands see a mutated datapath value. |
| R395-2 F3 (MINOR): the envelope and the `kEngageColumns` derivation | **RESOLVED** | The envelope is stated as relative rate, with limits, the regimes beyond them and the settled lock, and it reproduces (S1 is a conservative residue only). The derivation holds at ±50 ppm, and the ±50 ppm scope is stated. |
| R395-2 S1 (the aligner banner pointer) | **TAKEN** | `KL_media_grid_align.sv` banner, comment only. |
| R395-2 S2 (hosted duration of `capture_coherence`) | **Superseded by F1** | The suite now fails on the hosted gate, at 1,442 s of 1,800 s. |

My round-2 correction also stands, as the author noted: the -60 ppm failures in my `377d1ac3` receipts were the 64-column window, not the NCO race. None of those runs netted non-zero.

### Round 2: the internal reviewer's findings (R394-2)

| Prior finding | Status at this head | Evidence |
|---|---|---|
| R394-2 F1 (MINOR, Docs): the aligner banner claimed raced engagements start inside the settle band | **RESOLVED** | The banner is now scoped to the module default (1/128 sample). It adds that `milan_datapath` binds 256 cycles and a late tick, so raced engagements start outside the band and the #386 recentre waits up to its 32,768-tick ceiling. That agrees with `milan_datapath.sv` `MGA_KEEPOFF_CYC_C` and TIME_SYNC.md. |
| R394-2 F2 (MINOR, Docs): "about ±75 ppm" was falsified | **RESOLVED** | The PR body and the docs now state the measured regimes. My probes at +70 and ±75 ppm show on-crossing slips past 64 columns: single, net zero, with no tail slip. That is exactly the documented regime beyond the on-crossing limit (`receipts/probe-oncross*.log`). |
| R394-2 S1 (Tests): the queued-tick path had no failing check | **TAKEN** | `chmap_capture` `[Q]`; RM7 and RM8 are committed and caught. |
| R394-2 S2 (Tests): no ±50 ppm band in the arm | **TAKEN** | `band50` leg. |
| R394-2 S3 (Docs): state the pulled-engagement margin, and scope the latency table | **TAKEN** | TIME_SYNC.md envelope table ("256 - 4 x the rate"), plus the latency scope and "Other shapes" row. I re-derived the 104 x t cycle term: slot 4t + p injects 26 x 4t cycles after slot p. |

### Round 1

Every round-1 finding was resolved at `377d1ac3`, and nothing in round 3 reopens one.

## Real limits

- **Simulator.** The simulation used Verilator 5.050 (the CI pin) from `$VALIDATION_TOOLS/verilator-v5.050-src` (`receipts/tool-identity.txt`), because the assigned pinned-tool path does not exist on this host. Builds were capped at 4 jobs per stream, and at most 8 jobs ran at once.
- **Area.** The OOC used sv2v v0.0.13 (CI pins v0.0.12) and Yosys 0.66, following the per-top recipe of `ooc.sh` by hand, because `KL_media_nco` is not in its top list. It is an estimate.
- **Timing.** I did not measure timing closure of the NCO's new magnitude compare (CARRY4 35 -> 37) at 100 MHz. The shipping AX7101 shape runs the axis clock at 50 MHz.
- **F1's cause.** It is not identified. The hosted log does not contain the build output, and I did not use the hosted runner's environment (no act or Docker, per the review rules).
- **Envelope limits.** S1's negative-side measurements are probe runs, not committed checks. The settle probe covers ±80 and ±100 ppm only.
- **Not run by this reviewer** (the manager's banks):
  - `milan_dp`, `milan_dp_render`, `tdm`, `pair_fill`, `pp_shadow`, `crf_rx`, `crf_tx`, `mmcm_servo` and `mmcm_servo_autorepair`;
  - the builder bank, lint, the Yosys `run.sh`, the xvlog gate and the Markdown gates.
- **R394 probe scripts.** I did not run them. I covered the same ground (±70 and ±75 ppm placements, RM5, RM7, RM8) with my own probes and the committed arm.
- **Hardware.** Physical calibration: NOT RUN. Bench acceptance 4 is out of scope. Field skips are not hardware proof.
- **Other hosted contexts** at `ddb07747` (`receipts/hosted-checks-ddb07747.txt`):
  - Verilator shards 0, 2, 3 and 4 of 5: pass.
  - Yosys shards 0-3, `rtl-fast`, `elaborate`, `yosys-elaboration`, `verilator-lint`, `docs-check`, `full-ci-gate`: pass.
  - Physical gPTP: skipped. That is a skipped context, not an executed one.

## Pending manager duties

- **Route F1.** Decide the fix route: a quick/full split, a suite-specific guard, or making the `dp` mutant builds work on the hosted runner. Require the build output to be visible, and accept hosted `Verilator shard 1/5` at the new exact head.
- **Merge candidate.** Build the candidate merge on live `dev` (`eaa88a32` at the time of writing), and run the native banks at the new head.
- **Re-review scope.** After a new head, re-cover `Tests`. Re-cover any other lens whose files the fix touches: a `Makefile`, `mutants.py` or workflow change stays within `Tests`, unless the docs that describe the suite change as well.

## Restoration

The review clone is at exact head bytes (`receipts/restore-verification.txt`):

- HEAD `ddb07747`, tree `8ed377b8`;
- the index hash is identical before and after;
- all 953 tracked non-gitlink files hash to their index blobs, with their modes intact;
- the four gitlinks are unchanged;
- `git status --porcelain --ignored` is empty.

All probing, builds and the merge-tree checkout ran in `scratch/`, and nothing was written into the clone.

R395-3 FINISHED
