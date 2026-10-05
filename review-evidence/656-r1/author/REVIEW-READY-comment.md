[A536] REVIEW READY
Commit: `d0e29f6dda6f04f3ace1dbb395f57379e58cacaf` on `656-dp-gptp-order` (two commits on dev `c0280fc0`; not pushed by this lane, per its rules)

**Verdict: bench timing defect, fixed in the bench. No RTL, port, register or parameter change.**

**1. Bisect (first-parent merges only).** One run takes about 55 min here (sim 3,220-3,321 s), over the 40-min limit. Pinned Verilator 5.050, `make -C tb/verilator/milan_dp_gptp`, one detached worktree per point, submodules at that point's gitlinks.

| Point | Physical leg | Sim |
|---|---|---|
| `1269cdaf` | GOOD 139 / 0 (accounting 40 / 0) | 3320.81 s |
| `bbf704ec` Merge PR #634 | BAD 139 / 3 | 3300.10 s |
| `54643724` Merge PR #644 (midpoint) | BAD 139 / 3 | 3285.35 s |
| `241f9184` | BAD 139 / 3 (nightly 37184411090) | 4639.98 s hosted |
| dev `c0280fc0` | BAD 139 / 3 | 3268.83 s |

- **First bad merge: `bbf704ec`.** `5fabb46e` was not run: it is not a bisect step, and its simulation inputs are identical.
- **First bad commit inside it, by mechanism: `d676ecfd4`.** It is the only commit in the PR that changes the aligner select, to `mga_sel_w = int_clk_selected_r | follow_sel_r` (A2-a, #629 D4; `milan_datapath.sv:5905`).
- **Confirmed by a pair on the same pins** (processor `b2db3a97`): parent `0b074298` GOOD 139 / 0 + 40 / 0, `d676ecfd` BAD 139 / 3.
- The 275-line transcript is byte-identical at dev, `bbf704ec`, `54643724` and the nightly artifact (sha256 `aef5c121e480eb0c...`).

**2. Mechanism.**
- This leg keeps INTERNAL and models plan A: audio is 782/1591 of the 50 MHz axis clock, so FSYNC is 47,999.49 Hz, 10.64 ppm under 48 kHz.
- Under A2-a the aligner holds the media NCO on that FSYNC, and the loopback queue (`KL_chan_map_capture`, 8 events per pair) drains on the NCO.
- The bench's peer talker was paced on the axis clock, at exactly 48 kHz. The queue therefore drops its oldest event (`lb_skip`, `SLIP_LB`) every 1.958 s.
- Print-only trace at dev:
```text
TRACE STATE t=2.00 lb_dup=0 lb_skip=0 tdm_dup=0 tdm_skip=0 mga_eng=1 mga_err=0 trim=-170 nco_en=1
TRACE ORDER t=4.513547 last=216645 index=216647 step=2 lb_skip=4 tdm_dup=0 mga_eng=1 trim=-170
TRACE ORDER t=6.471693 last=310635 index=310637 step=2 lb_skip=8
TRACE ORDER t=8.429839 last=404625 index=404627 step=2 lb_skip=12
TRACE ORDER t=10.387985 last=498615 index=498617 step=2 lb_skip=16
TRACE ORDER t=15.283986 last=216603 index=216605 step=2 lb_skip=4   (after the reset)
```
- Reading the trace: trim -170 is -10.6 ppm. Each error is a one-sample gap on the edge where `lb_skip` steps by 4 (once per pair). The windows score 2 (peer loss) + 2 (recovery) + 1 after the reset = 5. The gPTP transitions play no part.
- At `1269cdaf` the aligner is off at INTERNAL (`mga_eng=0`). The same beat shows as `tdm_dup` at t = 1.95 and 3.90 s, at the TDM junction, which this leg does not grade.
- So the checker grades correctly, and the DUT counts every slip. `REGISTER_MAP.md`'s slip table reads exactly this pattern ("climbing | static") as "the upstream talker's clock is not this media clock". `obj_aclk`'s ring phases already pace their talker on the physical grid (`sim_aclk.cpp:816-852`).

**3. Fix.**
- `sim_ax1x1gptp.cpp`: the peer sends one six-sample PDU per `6 * 512` modeled audio-clock edges, a peer following the DUT's INTERNAL media clock. Check code, windows, timers and counts are unchanged.
- `tb/verilator/milan_dp/README.md`: a model row and one paragraph.

**Planted controls** (scratch; the plant is the existing `tdm8render` mutant "A2-a removed", `wire mga_sel_w = follow_sel_r;`):

| RTL \ talker paced on | axis clock (old) | audio clock (fix) |
|---|---|---|
| A2-a (dev) | FAIL 139 / 3 | **PASS 139 / 0, 40 / 0** |
| A2-a removed | PASS 139 / 0, 40 / 0 | **FAIL 139 / 5** (8 ordering errors) |

**4. Gates.** Pinned 5.050, all rc 0:
- **Exact head, the hosted job's own two commands**: `env -u SUITE_TIMEOUT VERILATOR_JOBS=4 scripts/run_all_suites.sh <out> --physical-gptp` then `suite_tally.py <out> --quiet --expect-suite-root tb/verilator --physical-gptp` give `PASS milan_dp_gptp`, checks 179, failures 0 (physical 139 / 0, every `bad_order=0`; accounting 6 / 0, 20 / 0, 14 / 0; driver 3968.59 s of 5400 s).
- **Fix commit `c24722ac`**, `make -C tb/verilator/milan_dp_gptp`: 139 / 0 + 40 / 0.
- **Builder bank**, `sw/builder/test_builder.py` (it reads this harness in `test_sim_clock`): "ALL GATES PASS EXCEPT 1 NOT RUN". Gate 11 needs a Vivado build tree.
- **Other head gates:** `test_clock_contract.py`, `check_cpp_idiom.py`, `measure_naming.py --check`, `measure_test_evidence.py --check`, `check_hygiene.py --check` (each with `--selftest`), `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `check_feature_status.py`, and with the pinned markdown lock `check_em_dash.py --base c0280fc0` (0 findings) and `gen_toc.py --check` / `--verify-anchors`.

**Acceptance criteria:**
1. Met: first bad merge `bbf704ec`, first bad commit `d676ecfd4` (bisect plus mechanism, confirmed by the pair).
2. Met: the check was grading a wrong bench model. Corrected, with planted controls on both sides.
3. Met locally (139 / 0 at the exact head, pinned 5.050). **The hosted nightly is open:** it needs a push and a Physical gPTP dispatch, or the first nightly after merge. The PR body therefore says "Relates to #656".

**Open risks / questions:**
- **#645.** Same queue and counter, but a followed, locked case. This mechanism does not explain it. The queue's 2-event margin with no recentre fits #645's one-slip signature, but that is untested here. #647 does not overlap. No RTL is touched, so lane A531's files are not.
- **#396.** At INTERNAL the loopback path still slips about 0.51/s per 10 ppm against an unfollowed talker (A2-a's documented consequence). A zero-glitch run through it needs the clocks followed.
- **The 160-PDU pin.** `verify_abort.py`'s exact pin of 160 RX PDUs per 20 ms holds deterministically here (all eight windows). At the new period of 6,250.0665 cycles, about 0.17 % of window phases would count 159.
- **Stale counts (not touched).** `tb/verilator/milan_dp/README.md:297` and `tb/verilator/milan_dp_gptp/README.md:7,9` still say 137 / 177. The leg has counted 139 / 179 since before this lane.
