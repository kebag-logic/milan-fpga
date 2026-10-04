# [A528] HANDOFF: #81 / #84 closeout lane

- Processor branch `pp81-scoreboard-faces`, from `main` `83999eba`; head **`db2c4eb`**.
  Not pushed, no PR opened.
- Assignment: processor issue #81, comment 5977862493.
- Issue comments: TAKEN is #81 comment 5977869877; REVIEW READY is #81 comment
  5981951639 (2026-10-04 18:11), with head `db2c4eb`.
- PR body: `PR-BODY.md`, beside this file.

## Status

DONE. Every item is done. Every processor suite and campaign that builds a changed file
ran rc 0 at four commits: base `83999eba`, head `beb7c22`/`7b95590`, the moved main
`c050d971`, and the merge head `db2c4eb`. The parent consumer set (17) ran at the head
and at the merge head. The OOC 1x1 pair was measured twice.

Two points need the manager's eye:

1. **Item 1's premise is out of date** (section Items, 1). T-IDENT-BURST and T-IDENT-REARM
   have RTL and grading since issue #80. F08.1 now says "landed", not "not landed".
2. **Area, second pair.** `main` -> merge head measures +67 LUT and +110 FF, past the
   60/60 STOP line on its face. The base -> head pair measures −30 / −4. The +110 FF are
   all the timer-arm queue's face-0 entries 1-3, which Vivado trims in three builds and
   keeps in the fourth; the classifier has no path to them. The lane judged it not
   item 4's cost and did not STOP. See section OOC.

## Commits (one-line subjects, no body, no trailer)

| Commit | Item |
|---|---|
| `4ffd8f0` | 1: F08.1 rows and 09's TIM claim |
| `371505d` | 3: 02 §2 rule 5 |
| `bacad0e` | 2: section TD, the sixth pp_top build |
| `beb7c22` | 4: GET_DYNAMIC_INFO's class, HZ8 amended, HZ13 |
| `7b95590` | the AECP campaign record in `tb/pp_top/README.md` (no build or campaign reads it) |
| `db2c4eb` | `git merge --no-ff` of `main` `c050d971` (PR #153, the notification registry in LUTRAM); no conflict |

- `beb7c22` amends the first item-4 commit `35a2622` (never pushed).
- The first head campaign, at `35a2622`, ran HZ8's new check inside HZ8. That moved
  HZ9's name saves under three arms (`hz-name-as-ro`, `hz-name-key-none` x3,
  `hz-acmp-reads-as-steps`: their HZ11b failures became HZ11a's).
- The check now runs after HZ12, and every head chain was restarted.
- That earlier run is scratch only (`$VALIDATION_STORAGE/pp81-a528/old-head-35a2622`).

## Items

### 1. #81 acceptance 4: F08.1 rows (docs only)

- **Finding.** T-IDENT-BURST and T-IDENT-REARM are not "rows without RTL".
  - Issue #80 (lane C6, 2026-09-30) landed them in `KL_aecp_notify` behind
    P-EN-IDENTIFY-NOTIFICATION. At the merge head that is
    `hdl/aecp/KL_aecp_notify.sv:753-755` (694-696 before the merge).
  - They are graded by `tb/pp_top` ID and `tb/aecp_notify` FT, and mutation-proven by
    `notify_mutants.py` (`ident_burst_100ms`, `ident_no_rearm`, ...).
  - 00 GAP-06 says "Identify work remaining: none in this repository".
  - Writing "not landed" would be false. F08.1 records acceptance 4's
    "implemented and graded" branch instead.
- **Changes:**
  - `docs/architecture/08_timing.md:30-31`: landed, with the owner, the gate and the
    suites;
  - `:32`: T-CTR-OBSERVE is integrator-owned;
  - `docs/architecture/09_verification.md:53`: the TIM row no longer claims every
    F08.1 row.
- **Test:** docs only. `make check` rc 0, 1,122 links (base 1,120).

### 2. #81 acceptance 4: the defaults pinned

- **Changes:**
  - `tb/pp_top/pp_top_wrap.sv:549-557`: `ifndef PP_TOP_TIM_DEFAULTS` around the two
    400 ms overrides;
  - `tb/pp_top/Makefile:185-196`: `timer-defaults(-build)`. `run` makes six builds
    and expects six tallies (`:169-170`);
  - `tb/pp_top/sim_main.cpp:13804-13808`: the sixth build runs TD alone;
  - `tb/pp_top/notify_phases.hpp:1608-1717`: section TD.
- **Tests and arms:**

| Check | What | Killing arm (planted in `tb/pp_top/mutations/`) | Its failure |
|---|---|---|---|
| TD1 | auto-unlock push 60,000 to 60,020 ms after the LOCK_ENTITY (measured 60,003, both heads) | `td-lock-default-59s` (top default 59,000) | got 59,003 ms |
| TD2 | expiry DEREGISTER 300,000 to 300,020 ms after the REGISTER (measured 300,002; 6 monitor probes answered) | `td-tl-default-301s` (top default 301,000) | got -1 ms (none by 300,020) |

TD's third check is the existing `NotifyBench` restore premise. The sixth build simulates
30 million clocks in about 90 s.

### 3. #84 acceptance 4: 02 §2 rule 5

- `docs/architecture/02_interfaces.md:115-124`.
- Verified: no `negedge` in `hdl/`, and every `always_ff` is `@(posedge clk_i)`.
- No other asynchronous-reset wording in `docs/architecture`.

### 4. #84 R419-2 F5: GET_DYNAMIC_INFO

- **Change.** `hdl/top/protocol_processor_top.sv:1645-1646`: an AEM GET_DYNAMIC_INFO
  presents `MAP_CFG`, keeping the NONE key. The comment is at `:1542-1554`.
  - Only the scoreboard consumes the class. The top reads `hazard_class` in the
    admission mux only; the normalizer just copies it.
  - A key alone cannot do it: the classifier's operands end at @31, and a record's
    descriptor starts at @32.
- **Tests** (`tb/pp_top/sim_main.cpp`):
  - HZ1 row `:13167`;
  - HZ8 banner `:13519-13520`;
  - HZ8's batch check `:13703-13715`, run after HZ12;
  - HZ13 `:13717-13743`;
  - run order `:13756-13758`.

| Check | Killing arm(s) |
|---|---|
| HZ1 GET_DYNAMIC_INFO row (MAP_CFG, 0xFC00) | `hz-gdi-key-none` x3, `hz-gdi-as-barrier`, `hz-stub-restored` |
| HZ8 batch naming no stream: not admitted / admitted after | `hz-gdi-key-none-no-stream` (named), `hz-gdi-key-none`, `-held`, `hz-stub-restored`, `hz-barrier-no-priority` |
| HZ8 batch premise (UNBIND_RX held) | `hz-barrier-no-priority` |
| HZ13a not admitted / admitted after | `hz-gdi-key-none` (named), `-held`, `-no-stream`, `hz-stub-restored`, `hz-barrier-no-priority` |
| HZ13a premise | `hz-barrier-no-priority` |
| HZ13b admitted beside a GET_RX_STATE | `hz-gdi-as-barrier` (named), `hz-acmp-reads-as-steps`, `hz-barrier-no-priority` |
| HZ13b premise | `hz-barrier-no-priority` |
| HZ13c not admitted / admitted after | `hz-gdi-key-none-held` (named), `hz-gdi-key-none`, `-no-stream`, `hz-stub-restored`, `hz-barrier-no-priority` |
| HZ13c premise (GDI held), ACMP answered | `hz-barrier-no-priority` |

`hz-gdi-key-none`'s HZ13a failure reproduces R419-2's G1: key 0xFC00, refused 0 clocks.

## OOC 1x1 cost (#638's recipe)

**The recipe** (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md` in the scratch parent):

- the export (the `build.sh ax7101` preview, then `milan_soc.py` without `--build`);
- an RTL elaboration for the parameter block;
- the standalone synthesis with `--integrated-clock`.

**The tools:**

- Vivado 2026.1 under `flock /tmp/milan-vivado.lock`, one instance at a time, no heavy
  build beside it.
- Environment: the LiteX venv, the verified SDK and `LITEX_ENV_CC_TRIPLE=riscv32-linux`,
  as the #230 lane used.
- Scripts: `$VALIDATION_STORAGE/pp81-a528/bin/{meas.sh,head-vivado.sh,pair-vivado.sh}`.

**Inputs:**

- ROMs, XDC and `.init` images are sha256-equal across all four exports.
- `baseline_chparam.txt` is identical across all four.
- Each log has exactly one `Synth 8-4445` match, the echoed command.

| Commit | LUT (logic + memory) | FF | F7 | CARRY4 | RAMB36/18 | DSP | WNS/WHS est. | synth |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| base `83999eba` | 24,930 (23,644 + 1,286) | 25,465 | 639 | 1,643 | 21/3 | 8 | −2.059/+0.159 | 11:57-12:17 |
| head `7b95590` | 24,900 (23,614 + 1,286) | 25,461 | 623 | 1,644 | 21/3 | 8 | +0.479/+0.159 | 14:31-14:51 |
| main `c050d971` | 24,130 (21,980 + 2,150) | 23,418 | 621 | 1,494 | 21/3 | 8 | −4.327/+0.159 | 17:13-17:34 |
| merge `db2c4eb` | 24,197 (22,047 + 2,150) | 23,528 | 621 | 1,494 | 21/3 | 8 | −2.782/+0.159 | 17:35-17:56 |

The top's RTL is byte-identical between base and main, and between head and merge
(`git diff 83999eb c050d971 -- hdl/top` is empty). So both pairs apply exactly item 4.

- **base -> head: −30 LUT, −4 FF.**
- **main -> merge: +67 LUT, +110 FF.**
  - **The flip-flops.** The top's own FF row goes 3,169 -> 3,279. Every child's FF count
    is unchanged.
    - The census (`baseline_cells.tsv`): `armq_r` 1,152 -> 1,260 and `armq_cnt_r`
      22 -> 24. `link_q_r` -1 and `st_ls_r` +1 cancel.
    - The `armq_r` difference is face 0 (the ACMP listener) alone: 36 bits kept in base,
      head and main, 144 in merge (entries 1 to 3 untrimmed).
    - `arm_drain_pick` (`protocol_processor_top.sv:2990-3001`) pops face 0 whenever it is
      non-empty, so `armq_cnt_r[0]` never exceeds 1, and entries 1 to 3 are never
      written. Vivado proved that in three builds and not in the fourth.
    - Without those bits, merge FF = main FF = 23,418.
  - **The LUTs.** The rebuilt-hierarchy rows are not an attribution:
    - base -> head: the top row +155, children −185;
    - main -> merge: the top row +23, children +44. Unchanged RTL there moves:
      `u_listener` +95, `u_acmp_q` −56, `u_aecp_q` +49, `u_ca_builder` −35.
  - **Judgment:** item 4 costs about nothing (0 FF; LUT within synthesis noise). Not a
    STOP. Flagged for the manager in the PR body and in REVIEW READY.
- **The resource gate** (`pp_resource_gate.py check --endpoint ooc-1x1`):
  - base rc 1 (LUT +598) and head rc 1 (+568), against the recorded baseline, which
    predates the name stage's `u_d3`. #230 and #232 recorded the same.
  - main rc 0 (−202 / −1,927) and merge rc 0 (−135 / −1,817).

### Lock waits and incidents

- The head measurement first queued behind other lanes' routes and a held batch. It was
  withdrawn, the head parent gates ran meanwhile, and the measurement re-ran in one lock
  hold (elab, OOC, xvlog).
- The main/merge pair's first launch found real gitignored `configs/generated/*.hex`
  and `sw/builder/out/` left by the parent gates, so its links failed. It was stopped
  about 25 s into elaboration and its partial outputs were deleted. The parent's
  ignored products were cleaned, and it re-ran with a guard that refuses non-symlinks.
  - The base and head measurements were not affected. Their `baseline_images.json`
    shows the WORK ROMs through the links.

## Suites

Pinned Verilator 5.050. Every command ran unpiped through `runlog.sh` (log plus an rc
file). Base and main ran in the scratch parent's processor submodule; head and merge
ran in the lane checkout.

| Gate | base `83999eba` | head `beb7c22` | main `c050d971` | merge `db2c4eb` |
|---|---|---|---|---|
| `make -C tb/pp_top` | rc 0, 10,416 | rc 0, 10,431 | rc 0, 10,416 | rc 0, 10,431 |
| `./scripts/run_suites.sh` | rc 0, 33 suites, 1,021,469 | rc 0, 1,021,484 | rc 0, 1,021,485 (`aecp_notify` 30, #153) | rc 0, 1,021,500 |
| `./scripts/lint_hdl.sh` | rc 0, 41 modules | rc 0 | rc 0 | rc 0 |
| `make check` | rc 0, 1,120 links | rc 0, 1,122 (also at `7b95590`) | rc 0, 1,120 | rc 0, 1,122 |
| `gen_matrix.py --check` | rc 0, 94 rows, 0 untested | rc 0 | rc 0 | rc 0 |
| `./syn/yosys/run.sh` | rc 0, 42 tops + Xilinx map | identical OK lines | identical | identical |
| `git diff --check` | | rc 0 vs `83999eba` (at `7b95590`) | | rc 0 vs `c050d971` |

- Every `tb/pp_top` section line is identical, base to head and main to merge, except HZ
  (177 -> 189), the default build's total, and the sixth build (TD 3). TB's histogram is
  included.
- The µPC map and M9 gates pass in all four sweeps.

## Campaigns (every one that builds the top, the pp_top bench or `KL_aecp_notify`)

`--jobs 3` where the driver takes it. The logs were compared with `compare.py`, paths
normalized, base vs head and main vs merge.

| Campaign | base / main | head / merge | Record |
|---|---|---|---|
| `aecp_mutants.py` | rc 0, 5 controls + 55 arms | rc 0, 6 controls + 61 arms | changed (below). base and main logs are byte-identical, as are head and merge |
| `aecp_dispatch_mutants.py` | rc 0, 44 of 44 | same | identical |
| `acmp_mutants.py` | rc 0, 19 of 19 | same | identical as a set (completion order) |
| `ctr_mutants.py` | rc 0, 18 of 18 | same | identical |
| `d3_mutants.py` | rc 0, 110 of 110 | same | identical as a set |
| `gsi_mutants.py` | rc 0, 20 detected | same | identical |
| `name_wr_mutant.py` | rc 0, killed | same | identical |
| `notify_mutants.py` | rc 0, 40 of 40 / 47 of 47 (#153's arms) | same as each | identical as a set |
| `tb/maap/mutants.py` | rc 0, 32 of 32 | same | identical |
| `tb/adp_engine/mutants.py` | rc 0, 43 of 43 | same | identical |

Changed AECP records:

- `hz-stub-restored` 74 -> 81;
- `hz-acmp-reads-as-steps` 26 -> 27;
- `hz-barrier-no-priority` 127 -> 139;
- six new arms and the `timer-defaults` control.

Every added failure line is a new or changed check, and no base failure line disappeared.

## Parent consumer set (17)

**The scratch parent:** `$VALIDATION_STORAGE/pp81-a528/milan-fpga`, a clone at dev `241f9184`,
never committed or pushed.

- `gptp-processor` and `third_party/verilog-axis` are at their pins; `external` is not
  initialized.
- `protocol-processor` is a clone of this lane's repository; its gitlink is set in the
  index only.
- c8, p2-p1 and c10 applied cleanly in that order.
- After the merge, PR #153's own `parent-adoption-232-241f9184.patch` (sha256
  `88ee5e96...`, `pp232-a520` output dir) was applied fourth for gate 9 only.

**The runner:** `bin/pgates.sh`, with the pinned Verilator first and the host's GNU
Make 4.4.1.

| # | Gate | head `7b95590` | merge `db2c4eb` | Result at merge |
|---:|---|---:|---:|---|
| 1 | `check_cpp_idiom.py` | 0 | 0 | every count 0 <= 0 |
| 2 | `check_py_idiom.py` | 0 | 0 | ratchets held; 195,220 lines (base 195,163; +21 arms, +36 #153) |
| 3 / 3s | `check_rtl_source_lists.py` / `--selftest` | 0 / 0 | 0 / 0 | 42/42 tops / 50 of 50 |
| 4 | `pp_srcs.py --check --selftest` | 0 | 0 | 46 sources |
| 5 | `check_port_contracts.py` | 0 | 0 | 1,759 ports, 111 <= 111 |
| 6 | `measure_naming.py --check` | 0 | 0 | 95 recorded |
| 7 | `measure_test_evidence.py --check` | 0 | 0 | 72 <= 77, 10, 0, 3 |
| 8 | `docs_check.py` | 0 | 0 | 0 findings |
| 9 / 9s | `xvlog_gate.py --check` / `--selftest` (lock) | 0 / 0 (3 == ratchet) | 1 without #153's patch (BANK IT `pd_ix_w`); **0 / 0 with it** (2 == ratchet) | pinned at `db2c4eb8` |
| 10 | `sw/builder/test_builder.py` | 0 | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11: local board build tree) |
| 11 | `lint_rtl.py --check` | 0 | 0 | 90 <= 90 |
| 12 | `pp_shadow -j16` | 0 | 0 | 606, 606, 646, 311 |
| 13 / 14 | `nvm_cosim` lint / quick | 0 / 0 | 0 / 0 | lint runs complete / 315 of 315 |
| 15 | `milan_dp -j16 VERILATOR_JOBS=3` | 0 | 0 | 9 RESULT PASS |
| 16 | `milan_dp_render -j16` | 2 | 2 | 65 + 155, 2 failures: T30 INTERNAL LAW (227, 285), #643 |
| 16b | `tdm8_render_mutants.py --leg-defects` | 0 | 0 | 5 of 5 |
| 17 | `check_sh_idiom.py` | 0 | 0 | every count held |

- **Base `83999eba`:** gates 1-8, 3s, 11 and 17 rc 0, the same output as head apart
  from the py-idiom count.
- **Gate 16 base control:** the processor and gitlink at `83999eba`, render products
  removed, `tdm8render` rc 2 with the same two T30 failures and the same numbers. So
  they are #643's.
- **The merge round's light gates** also re-ran with the fourth patch: all rc 0.

## Receipts (scratch; nothing copied here)

| File under `$VALIDATION_STORAGE/pp81-a528/` | sha256 (first 16) | bytes |
|---|---|---:|
| `suites/base-run_suites.log` | fc0377753214ffd2 | 1,750 |
| `suites/head-run_suites.log` | d1d722c551334c7f | 1,750 |
| `suites/main-run_suites.log` | bcae02867e6572bd | 1,750 |
| `suites/merge-run_suites.log` | 76973b5d0978c3cd | 1,750 |
| `suites/base-pp_top.log` | 85dd1ab72a93e04e | 27,988 |
| `suites/head-pp_top.log` | 3188badd0571ef85 | 43,455 |
| `suites/main-pp_top.log` | e26631d9d9556376 | 160,743 |
| `suites/merge-pp_top.log` | 04b1c86892cc0943 | 187,105 |
| `camp/{base,main}-aecp.log` | 2da0dc4d3c9abb4d | 71,290 |
| `camp/{head,merge}-aecp.log` | 53d881784de32314 | 78,512 |
| `meas/base/ax7101-ooc/baseline.log` | 8d5131b7f3cd5161 | 237,391 |
| `meas/head/ax7101-ooc/baseline.log` | c5fbc011af24ec03 | 236,122 |
| `meas/main/ax7101-ooc/baseline.log` | 052cb6140fa327ec | 305,832 |
| `meas/merge/ax7101-ooc/baseline.log` | 372c05cc5c606677 | 305,444 |
| `meas/{base,head,main,merge}/ax7101-elab/elaborate.log` | 0847fbf3efcc730b, cb7facf00be89106, 4598267db349ae5c, 2febe9191d748990 | 213,960, 213,963, 209,702, 209,947 |
| `pgates-merge/16_milan_dp_render.log` | c427b394d2b6aab8 | 172,835 |
| `pgates-merge4/09_xvlog_gate.log` | 61c50f0159aaf6c5 | 1,025 |
| `pgates-merge/10_builder.log` | 7ad1814a028e828f | 99,939 |
| `pgates-merge/15_milan_dp.log` | ea9c367b458de546 | 2,097,617 |

## Left as is (cosmetic, after every gate had run)

- The classifier comment has one short line at `protocol_processor_top.sv:1547`.
- Two `tb/pp_top/README.md` lines run past the wrap width (the HZ1 and HZ8
  sentences).
- Changing them would move an RTL file, or the head, after every measurement.
