# HANDOFF: #814 SoC sys-domain timing cuts, round 3, executor [A703c]

Status: **REVIEW READY** at head `8b28ebaf035e786ccf5b8e50098dbc111f51831f`, unchanged: no gate needed a fix, so round 3 added no commit. The worktree is clean and every submodule is at its gitlink. Nothing pushed.

- **The #818 gate passes the round-2 route set** (PR #820 at `32f0d9b5`, in scratch, exit 0). It selects ExtraPostPlacementOpt at +0.128 ns, at or above the floor at every signoff corner; the 0.312 ns fall from the record is a WARNING.
- **Every gate the STOP skipped passes at the head**: the full sweep (64 of 64, four shards), rtl-fast (all 12 jobs), the docs workflow gates (42 steps) and the builder bank. Three shards' first start aborted in the sweep's own cancellation self-test during a host memory dip; they passed when rerun unchanged (section 2).
- No Vivado ran, and the record was not re-recorded (the record rule).

- Lane: `814-soc-timing-cut`, from dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141` (verified ancestor; live remote dev still `1e80128f`)
- origin: https://github.com/kebag-logic/milan-fpga.git (verified); no git command was run inside a submodule
- Assignment: the round-3 [A10] ruling, issuecomment-6527475726; the record rule, issuecomment-6525285974; #818 / PR #820 at `32f0d9b5`
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/814#issuecomment-6528077001
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/814#issuecomment-6530796025 (text in `REVIEW-READY.md`)
- PR body for the manager: `PR-BODY.md`
- Round 2 (routes, capture, service runs): `../814-a703b/HANDOFF.md`; round 1 (the cuts and their checks): `../814-a703/HANDOFF.md`

## 1. The #818 verdict on the round-2 route set

**Verdict: PASS (exit 0). ExtraPostPlacementOpt is selected, the shipping directive, at +0.128 ns worst-corner WNS. Every signoff corner meets the build floor. The 0.312 ns fall from the record prints as a WARNING.**

How it was run: PR #820's head `32f0d9b5425a8526ac9d39e5913c01944c36e4d0` (branch `818-wns-gate`, fetched from origin, SHA verified), checked out in a scratch clone and never committed here. Its `syn/ooc/pp_resource_gate.py` and its own `pp_resource_baseline.json` were used. #818 does not change that file, so it holds dev's twelfth record, the same one the lane's head carries. The inputs are round 2's three routed directories at `8b28ebaf`, read in place:

```sh
python3 syn/ooc/pp_resource_gate.py check <w-h1>/ax7101/gateware --endpoint route-1x1 \
  --comparison <w-h1>/ax7101-AltSpreadLogic_high --comparison <w-h1>/ax7101-ExtraTimingOpt
```

- The gate read the same reports round 2 cited: each directory's `route_status.rpt` and `utilization_place.rpt` are byte-identical to round 2's receipts. `gate-inputs.sha256` records the 30 files the gate reads.
- Nothing in the inputs changed: the listing of every non-checkpoint file (name, size, mtime) hashes the same before and after (`snap-before.txt`, `snap-after.txt`).
- Each comparison's script passed #818's own check: it is the snippet's script written from the shipping route's script.

| Directive | Worst-corner WNS / WHS ns | Selected |
|---|---|---|
| ExtraPostPlacementOpt | +0.128 / +0.030 | **yes**, the best worst-corner WNS |
| AltSpreadLogic_high | +0.039 / +0.029 | no |
| ExtraTimingOpt | +0.010 / +0.029 | no |

The selected route against the record and the floors (`receipts/gate818/check-set.log`):

| Figure | Record | Route | Delta | Verdict |
|---|---:|---:|---:|---|
| LUT | 52,012 | 51,827 | -185 | ok, below the record |
| FF | 53,707 | 54,022 | +315 | ok |
| Slices | 15,780 | 15,764 | -16 | ok, below the record |
| RAMB36 / RAMB18 / DSP | 74 / 27 / 13 | 74 / 27 / 13 | 0 | ok |
| WNS ns | +0.440 | +0.128 | -0.312 | **WARNING**: fell by more than 0.25 from the record. Printed, not gated (#818) |
| WHS ns | +0.036 | +0.030 | -0.006 | ok |
| Slow 0C / Slow 85C | | WNS +0.128, WHS +0.059 | | floor met |
| Fast 0C / Fast 85C | | WNS +1.311, WHS +0.030 | | floor met |
| Route status | | complete, no unrouted net, no routing error | | ok |

- **ExtraTimingOpt at +0.010 ns** misses the floor at both slow corners. Under #818 that does not fail the set, because a directive that is not selected is not judged on its timing. It is the same route that round 2's STOP item 3 named. The shipping image is built from the selected directive, and that directive meets the floor at every corner.
- **Round 2's STOP items 1 and 2 under the round-3 ruling.** The 0.312 ns fall is now the WARNING above. The ruling's only STOP is a failing gate, so the families outside F1 to F4 within 0.3 ns no longer stop the lane. Its reason: the integration image without #814 misses the floor (+0.003 ns at ExtraPostPlacementOpt, -0.220 ns at AltSpreadLogic_high) on #814's own LiteDRAM families, while the morning integration that included #814 routed at +0.236 ns. The families round 2 listed are reported again in the PR body as known limitations, unchanged and not cut.

Controls on the same inputs, so that a PASS is not the only answer the gate can give:

| Run | rc | Output |
|---|---:|---|
| the shipping route alone, `--shipping-selection` | 0 | the same verdict and the same WARNING (`check-shipping-alone.log`) |
| the shipping route with neither `--comparison` nor `--shipping-selection` | 2 | `NOT COMPARABLE: judge a route on the recipe's three placement directives, ...` (`control-no-set.log`) |
| the ExtraTimingOpt directory alone, `--shipping-selection` | 2 | `NOT COMPARABLE: ... holds 0 recipe scripts, not one`: a comparison directory is not a shipping route (`control-eto-alone.log`) |

#818's own planted arms, run at `32f0d9b5` in the same scratch clone (`selftests.txt`), each rc 0:
- `pp_resource_gate.py --selftest`;
- `pp_resource_gate_selftest.py`: 304 arms and 500 fuzz cases, `PASS`. These include `pp_resource_gate_set_selftest.py`'s route-set arms, imported as a module; run alone, that file prints nothing and exits 0. Among those arms: "a set whose best directive misses the floor at one corner fails: exit 1", "a set whose shipping directive misses the floor and whose best meets it passes, naming the best: exit 0", "a large fall passes with a WARNING: exit 0" and "a resource over its tolerance still fails: exit 1";
- `pp_resource_gate_mutants.py`: `control passes, all 230 mutants fail`.

**No record was re-recorded.** The record rule (issuecomment-6525285974) re-records it once on dev, after the last release merge. `syn/ooc/pp_resource_baseline.json` and `docs/design/AREA_BUDGET.md` are unchanged at the head. No Vivado ran this round.

## 2. Gates at the head

Each ran in its own clean clone at `8b28ebaf`, whose `dev` and `origin/dev` are the live remote dev tip `1e80128f` (`scripts/make_clone.sh`, submodules from the lane's checkouts at their gitlinks). Each clone's tracked tree was clean afterwards. All were run unpiped, and each rc is the command's own.

| Gate | Command | rc | Result | Receipts |
|---|---|---:|---|---|
| #818 gate on the round-2 route set | section 1 | 0 | `RESULT: PASS`, ExtraPostPlacementOpt selected at +0.128 ns, the fall a WARNING | `receipts/gate818/` |
| #818's own self-tests at `32f0d9b5` | section 1 | 0 x3 | 304 arms + 500 fuzz PASS; 230 of 230 mutants fail | `receipts/gate818/` |
| The full sweep, 4 shard units (`native-shards.py`, MemoryMax 10G, -j4) | `bash scripts/run_all_suites.sh <logs> --wait --shard k/4` | 0 x4 | **64 of 64 suites PASS**: 14 + 17 + 17 + 16, none failed or timed out; each preflight's cancellation self-test PASS | `receipts/sweep-8b28ebaf/` |
| rtl-fast, the workflow's step bodies replayed natively (`scripts/rtl_fast_steps.py`) | every job in `rtl-fast`'s `needs:` | 0 | **`rtl-fast: success`**, failed jobs none: all 12 needed jobs `success` (the change classifier gave `rtl=true`, so none was skipped), 56 run steps rc 0, 6,229 s; base read from the live dev `1e80128f`. Not run, by rule: `uses:` steps, the package-resolve and tool-build steps for tools already built here (Verilator 5.050, Yosys 0.66, sv2v v0.0.12), and the runtime-evidence record step | `receipts/rtlfast-8b28ebaf/` |
| The docs workflow's gate steps (`scripts/docs_run.sh`) | 44 selected steps; builder leg 1 again on the LiteX interpreter; the 5 markdown gates on CPython 3.12.3; the no-git step's 2 gates on an archive export | 0, 0, 0, 0 | **42 steps rc 0, 0 failed**; 1 of 1 and 5 of 5; `docs_check` rc 0, `feature_status` rc 0. Two steps are not run, by rule: `gate_42` executes the candidate's `act_ci.py` on the host, which AGENTS.md section 5 forbids; `docs-check-no-git/ci_step_3` deletes `.git`, so its two gates ran on the archive export | `receipts/docs-8b28ebaf/` |
| The builder bank | `python3 sw/builder/test_builder.py` | 0 | `ALL GATES PASS EXCEPT 2 NOT RUN` (1820 s). The same two arms dev's bank does not run on this host: gate 1b's `MAKEFLAGS += -e` mutation is inert under GNU Make 4.3, and gate 11 needs the absent mf48 calibration build | `receipts/builder-8b28ebaf/` |
| Vivado: route, ooc, xvlog | - | - | **not run, by the assignment** (no Vivado this round). The sweep's preflight `xvlog_gate.log` is the gate's offline self-test, `PASS` | - |
| The re-record | - | - | **not run, by the record rule** | - |

Round 2 at the same head (`../814-a703b/HANDOFF.md`, unchanged here): the three route-1x1 directives, ooc-1x1 and ooc-8x8 (gate `RESULT: PASS`, every figure equal to the record), the capture's six arms and three controls (all rc 0, worst 13.85922 ms against 24.5 ms), and the service-budget runs, 1x1 and 8x8 (`PASS`, no service finding). Round 1 at the same head (`../814-a703/HANDOFF.md`): `sw/litex/test_soc_timing_cuts.py` 15 arms PASS; `scripts/run_litex_sims.sh` 8 of 8 and its self-test 10 of 10; `check_nvm_capture.py` PASS; the idiom and doc-style gates within every ratchet.

### The sweep's first attempt

The first start of the four shards (16:39 UTC) **aborted in three of them**, 0, 2 and 3, all in the same second (16:40:28) and about 48 s in. Each failed in the sweep's preflight, in `scripts/test_suite_cancellation.py`'s hard-stop control (`hard_stop`, line 305). The process-containment cleanup it wraps (`scripts/owned_process.py:201`, 2 s grace plus 2 s reap) found an owned descendant still alive: `RuntimeError: CLEANUP FAILED: owned descendants remain: {...}`, then `ABORTING: sweep cancellation controls failed.` No suite started. Shard 1 passed the same control and ran to 17 of 17.

- **Cause, as far as the evidence goes: the host, not the head.** The lane changes no sweep script (`git diff --stat 1e80128f 8b28ebaf` touches only `sw/litex/`, `scripts/run_litex_sims.sh`, `ci/image/exec-audit.json` and two docs). The three aborts fell in one second, which points to a shared stall rather than three independent faults. At the time MemAvailable was dipping from 30.4 to 19.2 GB, with about 8.9 GB of swap in use and the release integration's synthesis holding 23 GB.
- **The rerun** used `scripts/rerun_shard.sh`, which does exactly what `native-shards.py` does for one shard: the same clone, spec, unit name, MemoryMax and CPU range. It kept each first attempt's logs under `attempt-1/`. It ran once MemAvailable was back at 35 GB, and the three shards were started 75 s apart so their cancellation controls did not overlap. All three passed the cancellation self-test (`suite cancellation: PASS`) and their suites. The first attempt's logs are in `receipts/sweep-8b28ebaf/shard-{0,2,3}/attempt-1/`.
- The same control can abort the hosted sweep under load. That is outside this lane; it is recorded here as an open risk.

## 3. The change at the head (rounds 1 and 2; no change this round)

Round 3 adds no commit, because no gate needed a fix. The lines below were re-read at `8b28ebaf` and are unchanged from round 1.

| File:line | Change | Reason |
|---|---|---|
| `sw/litex/milan_soc.py:2328-2391` | `cross_cpu_memory_ports` builds a second sys-side AXI port and puts `AXIReadyStage` between the crossing and the port LiteDRAM gets (`:2391`) | F2: LiteDRAM's ready was the crossing FIFOs' read enable |
| `sw/litex/milan_soc.py:2397` | `AXIReadyStage`: `PipeReady` on aw and ar; w, b and r pass through | F2's boundary, with no added cycle; w was measured outside the family |
| `sw/litex/milan_soc.py:2430` | `RegisteredRefresher`: LiteDRAM's `Refresher` with `cmd.valid` and `cmd.last` registered | F3: the ZQCS timer reached every bank machine through `refresh_req` |
| `sw/litex/milan_soc.py:2454`, `:3152` | `add_staged_sdram`: `add_sdram` with `ControllerSettings(refresh_cls=RegisteredRefresher)`; `MilanSoC` calls it | F3 through LiteDRAM's own hook; the other controller settings keep their defaults |
| `sw/litex/milan_soc.py:2465` | `SPIPHYStage`: a `stream.Buffer` each way (valid, payload and ready registered) and a chip-select flip-flop | F1's boundary, between the mmap FSM and the PHY |
| `sw/litex/milan_soc.py:2496` | `stage_spi_phy`: the stage takes over `phy.sink`, `phy.source` and `phy.cs`, and is the PHY's submodule | LiteSPI reads only those; the PHY's CSR names are unchanged |
| `sw/litex/milan_soc.py:3670-3690` | `MilanSoC.add_spi_flash`: LiteX's, with the PHY staged | every SoC built from this class carries the stage, the capture and service-budget harnesses included |
| `sw/litex/test_soc_timing_cuts.py` (new) | 15 arms (below) | the simulation check, with a planted unregistered path for each family |
| `scripts/run_litex_sims.sh:107` | `test_soc_timing_cuts` in the pinned inventory | the aggregate refuses an unlisted `test_*.py` |
| `ci/image/exec-audit.json:1206-1212` | the generated stand-in the aggregate's self-test writes for the new member | the image audit's reviewed list names every such stand-in |
| `docs/testing/TESTING.md:722-741`, `docs/litex/CLOCK_DOMAINS.md:276-281` | the new member; the CPU DDR crossing's stage | the authoritative test and clock-domain pages |

Not changed: the recipe, the directives, the floors, any constraint or pblock, `syn/ooc/pp_resource_baseline.json`, `docs/design/AREA_BUDGET.md`.

### The checks, planted mutants and failing words (round 1, at this head)

`sw/litex/test_soc_timing_cuts.py`. Each mutant substitutes one class in `milan_soc` for the build and must fail the named arms.

| Arm | Checks | Planted mutant and the failing words |
|---|---|---|
| F0, F1, F2 | only stage flip-flops drive the PHY's faces; no bridge or LiteSPI core flip-flop reaches a PHY flip-flop through logic alone | `WirePHYStage`: 89 forward and 21 back paths, F2 requires `fsm_state -> litespiclkgen_cnt` (the routed bridge-state-into-PHY-counter path) |
| F3, F4, F5 | twelve reads return the image; added cycles exactly `[8, 2, 2, 2, 8, 2, 8, 8, 2, 2, 8, 8]`; every command inside its chip select, in order | - |
| D0, D1, D2 | the stage feeds the aw and ar crossing FIFOs' read address; no LiteDRAM flip-flop reaches it through logic alone | `WirePassThrough`: 76 paths, D2 requires `axiburst2beat_beat_count -> memory_adr` |
| D3, D4 | the native port sees the same commands, words and masks, in the same cycles with and without the stage | - |
| Z0, Z1, Z2 | the refresh request is the stage's own flip-flops; no refresher flip-flop reaches a bank machine through it | LiteDRAM's own `Refresher`: 715 paths, Z2 requires `refreshtimer_count -> syncfifo_level` |
| Z3 | precharge-all and refresh on the DFI, each exactly one cycle later at the same spacing | - |

No new check this round. The new evidence is the #818 gate's verdict and its controls (section 1).

## 4. Resources and route timing (round 2's routes; no route this round)

| Directive | WNS / WHS ns, dev -> head | LUT, dev -> head | FF | Slices | #818 |
|---|---|---|---|---|---|
| ExtraPostPlacementOpt | +0.303 / +0.028 -> **+0.128 / +0.030** | 51,801 -> 51,827 | 53,760 -> 54,022 | 15,834 -> 15,764 | **selected**, floor met at every corner |
| AltSpreadLogic_high | +0.230 / +0.014 -> +0.039 / +0.029 | 51,846 -> 51,895 | 53,759 -> 54,024 | 15,795 -> 15,839 | not selected; floor met |
| ExtraTimingOpt | +0.106 / +0.054 -> +0.010 / +0.029 | 51,829 -> 51,882 | 53,758 -> 54,029 | 15,794 -> 15,839 | not selected; misses the floor at the slow corners |

Against the record (dev's twelfth, +0.440 ns): LUT -185, FF +315, slices -16, RAMB36 / RAMB18 / DSP 74 / 27 / 13 unchanged. ooc-1x1 and ooc-8x8 equal the record: 24,346 / 20,404 and 34,156 / 29,782 LUT / FF. F1 to F3 were +0.106 to +0.816 ns at dev; at the head each sits more than 1 ns from the worst path at every directive. The families that set the WNS now are in round 2's handoff, section 1, and in the PR body's known limitations.

## Progress log (UTC)

- 16:38 TAKEN posted; live remote dev `1e80128f`.
- 16:39 the four sweep shards started (CPUs 0-7, 8-15, 16-23, 24-31; MemAvailable 30.4 GB). 16:40 shards 0, 2 and 3 aborted in the cancellation self-test (section 2).
- 16:43-16:47 the #818 gate on the round-2 set, rc 0 `RESULT: PASS`; its controls; #818's self-tests.
- 16:53 the builder bank started detached (a first start at 16:42 inside a foreground shell, which could not outlive the bank's 30 minutes, was stopped at 16:52 before any verdict, and its clone discarded). 16:53 the docs gates. 16:54-16:56 shards 0, 2 and 3 started again, 75 s apart (MemAvailable 35 GB). 16:57 rtl-fast.
- 17:23 builder bank rc 0. 17:39 shard 1 rc 0 (17 of 17). 17:44 docs gates, all rc 0. 17:52 shards 0 and 3 rc 0 (14 of 14, 16 of 16). 17:58 shard 2 rc 0 (17 of 17). 18:40 rtl-fast rc 0, `success`. 18:5x REVIEW READY posted.

## Open risks

- **The sweep's cancellation self-test can abort under host load.** Its hard-stop control allows 4 s for an orphaned descendant to be reaped. Here it failed in three shards in the same second while MemAvailable fell to about 19 GB. The hosted sweep runs the same preflight. The lane does not touch it.
- **The flash stage has never been on hardware.** The pre-run image the manager flashed carried `77f979ce`, the Wishbone stage. The capture and service harnesses run the real LiteSPI core and the stage, but with a model PHY or a device boundary in place of the real PHY.
- **The WNS is set by families this lane does not change**: F4, the memory bridges into the CPU DMA port, the milan reset crossing into the MMCM servo, the AECP micro-CPU, LiteEth TX and the LiteDRAM bank machines. At one seed per directive, the head's three routes give +0.128, +0.039 and +0.010 ns.
- **The release integration that includes #814 is being rebuilt** (the ruling). That run decides the image, not this PR.

## How the runs were made

- The sweep: `native-shards.py 814-a703c <spec> <out> 4 0-7 8-15 16-23 24-31`. The spec comes from `scripts/make_sweep_spec.py`: pinned Verilator 5.050, sv2v v0.0.12, tsn-gen at the CI pin. CPU ranges are four 8-CPU quarters of the two free 16-CPU blocks `cpu_ranges.py` reported, because only two were free. Units `milan-814-a703c-shard{0..3}`, MemoryMax 10G, -j4, one clone each. The rerun was `scripts/rerun_shard.sh`.
- rtl-fast: `scripts/rtlfast_run.sh` with `scripts/rtl_fast_steps.py`, the workflow's `run:` bodies written out unchanged and run with `bash -e`, one job at a time, as a pull_request event against `dev`. The head is not pushed, so the act runner, which rechecks the remote head, cannot run it.
- The docs gates: `scripts/docs_run.sh` with `docs_steps.py` and `docs_steps_md312.py` (GNU Make 4.3, CPython 3.12.3 with the workflow's pinned requirements).
- The builder bank: `scripts/bg.sh` in a clean clone, with the lane environment (`scripts/env.sh`).
- The #818 gate: a scratch clone with PR #820's head fetched from origin (`32f0d9b5`, verified) and checked out detached. It read round 2's routed directories in place and wrote nothing (section 1).
- The lane's unit stayed under 4 GB (`memory.current`, sampled). Sweeps started only above 30 GB MemAvailable, and the gates beside them ran above 20 GB. No Vivado, no lock.
- Scratch outside the tree. Receipts redact host paths (`<scratch>`, `<scratch-r2>`, `<lanes>`, `<tools>`, `<home>`). Files over 200 KB are recorded by SHA-256 and size in each directory's `large.sha256`.

## Receipts

`INDEX.md` lists every file present (`scripts/gen_index.py`).

| Directory | Holds |
|---|---|
| `receipts/gate818/` | the #818 check on the set, its three controls, #818's self-tests, the inputs' digests and the before/after listing hashes, the gate clone's head and status |
| `receipts/sweep-8b28ebaf/` | per shard: the spec, the runner log, results, completion, the preflight logs and every suite log (or its digest); the first attempt of shards 0, 2 and 3 |
| `receipts/rtlfast-8b28ebaf/` | the run transcript, `receipts.json` (every job and step: rc, seconds, log digest, body digest), the base, every step log |
| `receipts/docs-8b28ebaf/` | the three passes' transcripts, rc and `receipts.json`, the no-git gates, the dev ref and the tsn-c-stack origin |
| `receipts/builder-8b28ebaf/` | the builder bank's log and rc |

`scripts/` holds the drivers used: `make_clone.sh`, `env.sh`, `fw_env.sh`, `bg.sh`, `make_sweep_spec.py`, `rerun_shard.sh`, `rtlfast_run.sh`, `rtl_fast_steps.py`, `docs_run.sh`, `docs_steps.py`, `docs_steps_md312.py`, `copy_receipts.py`, `gen_index.py`, and the wait helpers. `static_bank.sh` is carried from round 2 and was not run (its xvlog step needs Vivado).

## Not done (by the assignment's rules)

No push, no PR, no merge or rebase, no edit to any issue or PR comment, no sub-agents, no hardware or bench access, no flashing, no Vivado run, no re-record. On #814 the only posts are TAKEN and REVIEW READY.
