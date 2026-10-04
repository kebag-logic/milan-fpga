[A528]
Closes #81
Closes #84
Relates to #71

The #81 (GAP-07) and #84 (GAP-10) closeout lane, as assigned on #81
(comment 5977862493). Branch `pp81-scoreboard-faces` from `main` `83999eba`.
The lane's six commits (one per item, one README record, and the merge of `main` `c050d971`) end at `db2c4eb`. The manager's round-1b commit `1d6c78f` and the merge of `main` `07b1469d` (PR #154) follow, and the head is `f9b8f0e`.

| Commit | Item |
|---|---|
| `4ffd8f0` | 1: the F08.1 rows without RTL in this repository |
| `371505d` | 3: 02 §2 rule 5, the synchronous reset |
| `bacad0e` | 2: T-NOTIF-TIMELIMITED and T-LOCK-UNLOCK pinned at their defaults |
| `beb7c22` | 4: GET_DYNAMIC_INFO serialized against listener steps (R419-2 F5) |
| `7b95590` | the AECP campaign record in `tb/pp_top/README.md` |
| `db2c4eb` | `git merge --no-ff` of `main` `c050d971` (PR #153); no conflict |

No register-map, port or parameter change. The top's port and parameter header is
byte-identical to the base and to `main` `c050d971`. This lane's one RTL change is
one case arm in the top's F03.7 classifier and its comment.

## Rulings

- **REGISTRY_OP (#84 acceptance 2).** REGISTRY_OP is met by HZ1 (its class and key)
  and HZ8 (it never over-serializes). It has no reachable admission conflict at this
  top: its key, the registry's, is one no ACMP transaction presents, and the
  single-issue AECP engine never holds two transactions at once. So no conflict arm
  can exist for it.
- **ACMP's stamped deadline** keeps its design budget, graded by TB5, with no kill
  consumer, as PR #140 recorded. 08 §4 states it (`docs/architecture/08_timing.md:170-171`).
- **F03.3's kill count and trace** stay out: a status word is a register-map change.

## Acceptance, item by item

| Issue | Acceptance | Where it is met |
|---|---|---|
| #81 | 1: the deadline is read and drives the kill face and a forced FAIL_SAFE response | PR #140 (`tb/pp_top` DL) |
| #81 | 2: a compressed-timer arm stalls a command past its budget, with a mutation record | PR #140 (DL1 to DL11, the `dl-*` arms) |
| #81 | 3: AECP <= 240 ms and ACMP <= 50 ms under the 08 §4 worst-case stimuli | PR #140 (`tb/pp_top` TB1 to TB5) |
| #81 | 4: the F08.1 rows without RTL; the 300 s / 60 s defaults pinned | items 1 and 2 below |
| #84 | 1: every F06.14 state-changing opcode takes its F03.7 class and key | PR #140 (HZ1) |
| #84 | 2: one admission conflict graded per newly reachable class | PR #140 (HZ2 to HZ12); REGISTRY_OP by the ruling above (HZ1 and HZ8) |
| #84 | 3: 03 §6's classifier paragraph and 06 §8's Dispatch decision note | PR #140; 03 §6 updated again for GET_DYNAMIC_INFO (item 4) |
| #84 | 4: 02 §2 rule 5 states the synchronous active-low reset | item 3 below |
| #84 | PR #140's remainder: R419-2 F5, GET_DYNAMIC_INFO against listener steps | item 4 below |

## 1. #81 acceptance 4: the F08.1 rows (docs only)

Finding: two of the three rows are no longer "rows without RTL". Issue #80
(lane C6, merged 2026-09-30) landed T-IDENT-BURST and T-IDENT-REARM in
`KL_aecp_notify`, built when P-EN-IDENTIFY-NOTIFICATION = 1. They are graded by
`tb/pp_top` section ID (the third build), `tb/aecp_notify` FT and
`tb/pp_top/notify_mutants.py`, and 00 GAP-06 records "Identify work remaining:
none in this repository". Marking them "not landed" would make F08.1 false. So
F08.1 now states #81 acceptance 4's other branch, "implemented and graded":

- `docs/architecture/08_timing.md:30-31`: T-IDENT-BURST and T-IDENT-REARM are
  **landed**. The owner is `KL_aecp_notify`, built only with
  P-EN-IDENTIFY-NOTIFICATION = 1 (not at its default 0). The row names the suites
  that grade them.
- `docs/architecture/08_timing.md:32`: T-CTR-OBSERVE is **integrator-owned**: the
  integrator's counter banks behind the `ctr_*` face. There is no RTL here, so no
  suite here grades it.
- `docs/architecture/09_verification.md:53`: F09.3's TIM row claimed compressed-timer
  runs "over every F08.1 row" and "every F08.1 row exercised". Both are now limited
  to the rows with RTL here; T-CTR-OBSERVE is named integrator-owned. No other file
  claims these rows are graded.

## 2. #81 acceptance 4: the 300 s / 60 s defaults

Clauses: IEEE 1722.1-2021 §7.4.37.2 (a TIME_LIMITED registration times out after
300 s) and §7.4.2, Milan v1.2 §5.4.2.2 (the lock times out after 60 s, with a
notification); F08.1 T-NOTIF-TIMELIMITED and T-LOCK-UNLOCK.

The preferred route, prescaler compression:

- `tb/pp_top/pp_top_wrap.sv:549-557`: the wrap's two 400 ms overrides
  (`REG_TL_TIMEOUT_MS_P`, `LOCK_TIMEOUT_MS_P`) now stand only when
  `PP_TOP_TIM_DEFAULTS` is not defined.
- `tb/pp_top/Makefile:185-196`: a sixth build, `make timer-defaults`, defines it. It
  keeps the first build's prescaler (1 ms = 100 clocks), so the top's own 60,000 and
  300,000 ms counts elapse on the timebase: 30 million clocks. `make` runs all six
  builds and its tally expects six (`:169-170`).
- `tb/pp_top/notify_phases.hpp:1608-1717`, section TD: a controller registers
  TIME_LIMITED and another locks the entity. The registered one answers every
  CONTROLLER_AVAILABLE the monitor sends it (Milan §5.4.5.3), so only the timer
  under test can end its registration.
  - **TD1**: the auto-unlock notification (LOCK_ENTITY, u = 1, locked_id 0) reaches
    the registered controller no sooner than 60,000 ms after the LOCK_ENTITY was
    fed and at most 20 ms later. Measured: 60,003 ms.
  - **TD2**: the expiry DEREGISTER (u = 1) reaches it no sooner than 300,000 ms after
    the REGISTER and at most 20 ms later. Measured: 300,002 ms, with 6 monitor
    probes answered.
  - The lower bound is exact: the timer is armed in the ms its program runs, which
    is after the command was fed. The 20 ms covers the run to the arm, the sweep,
    and the notification's build and serialization.
- Arms in `tb/pp_top/aecp_mutants.py:61-67`, one per check and one per side of the
  window. Each changes the top's parameter default:
  - `td-lock-default-59s` (`LOCK_TIMEOUT_MS_P` 59,000): fails TD1 (59,003 ms);
  - `td-tl-default-301s` (`REG_TL_TIMEOUT_MS_P` 301,000): fails TD2 (no DEREGISTER
    by 300,020 ms).
- Docs: 09 §8.3 (`docs/architecture/09_verification.md:254`, `:270-272`) and the
  `tb/pp_top` README (section TD, both build tables).

## 3. #84 acceptance 4: 02 §2 rule 5

`docs/architecture/02_interfaces.md:115-124` now states the reset the RTL
implements. There is one input, `rst_n`, synchronous and active low. It is
sampled only at the core clock's rising edge, so it takes effect only while that
clock runs, and no flop has an asynchronous reset. Every `always_ff` in `hdl/` is
`@(posedge clk_i)`, and none names `rst_n` in its sensitivity list. The
boot-sequencer order follows its release, kept by holds rather than staged resets.

The rule used to read "asynchronous assert, synchronous release, released in the
boot-sequencer order". No other asynchronous-reset wording is in
`docs/architecture`. The "async" entries there are the MAC-boundary FIFOs and the
management domain, which are clock-domain wording, not reset wording.

## 4. #84, R419-2 F5: GET_DYNAMIC_INFO against the listener steps

Clauses: 03 §6 F03.7 (RO_SNAPSHOT is "blocked only vs in-flight write on the same
key"); IEEE 1722.1-2021 §7.4.76.1 (each record is handled "as if it were an
independent command"); Milan v1.2 §5.4.2.10 (GET_STREAM_INFO's probing and ACMP
status).

- **Why a key alone cannot do it.** The classifier sees the operands @24 to @31.
  A GET_DYNAMIC_INFO record's descriptor lies past them: the first record's
  header fills @24 to @31, and its descriptor_type is at @32. The scoreboard
  compares keys for equality, so no key can stand for "any sink".
- **The change** (`hdl/top/protocol_processor_top.sv:1645-1646`): an AEM
  GET_DYNAMIC_INFO for this entity presents `MAP_CFG`, keeping the NONE key.
  - `MAP_CFG`'s class-wide cross-lock (the scoreboard's rule 5) holds the batch
    against every in-flight `STREAM_CFG` step, the listener's included.
  - Its NONE key is one no ACMP transaction presents, so it still runs beside every
    ACMP read.
  - The single-issue AECP engine never holds a second `MAP_CFG` beside it.
  - Nothing else reads the class: the scoreboard alone consumes it.
  - The classifier comment (`:1542-1554`) is updated; READ_DESCRIPTOR's reasoning
    is unchanged.
- **The over-serialization, accepted.** A batch that names no stream, or only a
  STREAM_OUTPUT, also waits for any stream step, and an ACMP stream step waits
  for the batch.
- **Tests** (`tb/pp_top/sim_main.cpp`):
  - HZ1 (`:13167`): the batch's row now wants `MAP_CFG`, NONE key.
  - HZ8, amended for exactly this case (`:13519-13520`, `:13703-13715`): a
    GET_DYNAMIC_INFO naming no stream (one GET_CONFIGURATION record) waits for a
    held UNBIND_RX. It runs after HZ12, so every earlier arm keeps its clock: an
    earlier placement moved HZ9's name saves under three arms, which changed their
    counts.
  - HZ13 (`:13717-13743`), R419-2's G0 graded on the batch: a GET_DYNAMIC_INFO
    carrying a GET_STREAM_INFO record of STREAM_INPUT 1 waits for a held UNBIND_RX
    of sink 1 (HZ13a). Held itself, it holds back an UNBIND_RX of sink 1 (HZ13c). It
    runs beside a held GET_RX_STATE of sink 1, two reads (HZ13b).
- **Arms** (`tb/pp_top/aecp_mutants.py:176-189`):
  - `hz-gdi-key-none` reverts to the NONE key, the base classification. It is named
    three times (HZ13a, HZ13c, HZ8) and fails 7 checks. Its HZ13a failure is
    R419-2's G1 reproduced: the batch is admitted beside the held UNBIND_RX, key
    0xFC00, refused 0 clocks.
  - `hz-gdi-as-barrier` over-serializes against reads too. It fails HZ1 and HZ13b.
- **Docs:**
  - 03 §6's classifier paragraph (`docs/architecture/03_packet_engine.md:265-279`);
  - 08 §4's list of holds an ACMP step can meet (`docs/architecture/08_timing.md:197-200`);
  - 09 §8.3's HZ1, HZ8 and HZ13 rows;
  - the `tb/pp_top` README.

## Records that changed

Two rounds compare the same records:

- the lane: base `83999eba` against the pre-merge head (`beb7c22`, then
  `7b95590`);
- the merge: `main` `c050d971` against the merge head `db2c4eb`.

The differences are the same in both rounds, line for line. Every other suite
and campaign record is identical.

| Record | Base / main | Head / merge head | Why |
|---|---:|---:|---|
| `tb/pp_top` HZ | 177 | 189 | HZ8's batch (3 with its premise), HZ13a (3), HZ13b (2), HZ13c (4) |
| `tb/pp_top` sixth build, TD | none | 3 | TD1, TD2 and the bench's restore premise |
| `tb/pp_top` total | 10,416 | 10,431 | the two rows above |
| `run_suites.sh` sweep | 1,021,469 / 1,021,485 | 1,021,484 / 1,021,500 | `tb/pp_top`, +15 in both rounds |
| `make check` links | 1,120 | 1,122 | the two links items 1 and 3 add |
| AECP campaign | 5 controls, 55 arms | 6 controls, 61 arms | the `timer-defaults` control and the six arms above |
| `hz-stub-restored` | 74 | 81 | HZ1's batch row now wants `MAP_CFG`; HZ8's batch x2, HZ13a x2, HZ13c x2 |
| `hz-acmp-reads-as-steps` | 26 | 27 | HZ13b |
| `hz-barrier-no-priority` | 127 | 139 | the twelve new HZ checks behind the wedge |

`main` `c050d971` itself differs from `83999eba` only by PR #153's own records:
`tb/aecp_notify` 14 -> 30 checks, and `notify_mutants.py` 40 -> 47 arms.

## Area: out-of-context 1x1

**Read this first.**

- Item 4 is the lane's only RTL change. It measured −30 LUT and −4 FF against the lane's
  base.
- Against the moved `main`, the same change measured +67 LUT and +110 FF. On its face that
  is past the assignment's 60 LUT / 60 FF STOP line.
- By attribution it is not item 4's cost; the analysis follows the table.
- The lane did not STOP on it. That is a judgment the manager may overrule.

**The recipe.** #638's recipe, `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` in the
scratch parent at dev `241f9184`:

- the shipping export (the `build.sh ax7101` preview, then `milan_soc.py` without
  `--build`);
- an RTL elaboration for the wrapper's parameter block. The recipe allows it: "At 1x1
  its 21 wrapper parameters equal the full synthesis log's";
- then the standalone synthesis with `--integrated-clock` (20 ns).

**The conditions.**

- Vivado 2026.1, `xc7a100t-fgg484-2`, `AreaOptimized_high`.
- Every run held `flock /tmp/milan-vivado.lock`, one instance at a time, with no heavy
  build of this lane beside it.
- The four exports' ROMs (`ltn_rom.hex`, `ucode.hex`), XDC and `.init` images hash
  equal, and the four `baseline_chparam.txt` files are identical.
- Each run's log has exactly one `Synth 8-4445` match: the echoed `set_msg_config`
  command.

| Commit | LUT (logic + memory) | FF | F7 | CARRY4 | RAMB36 / RAMB18 | DSP | WNS / WHS estimate, ns |
|---|---:|---:|---:|---:|---:|---:|---:|
| base `83999eba` | 24,930 (23,644 + 1,286) | 25,465 | 639 | 1,643 | 21 / 3 | 8 | −2.059 / +0.159 |
| head `7b95590` | 24,900 (23,614 + 1,286) | 25,461 | 623 | 1,644 | 21 / 3 | 8 | +0.479 / +0.159 |
| `main` `c050d971` | 24,130 (21,980 + 2,150) | 23,418 | 621 | 1,494 | 21 / 3 | 8 | −4.327 / +0.159 |
| merge head `db2c4eb` | 24,197 (22,047 + 2,150) | 23,528 | 621 | 1,494 | 21 / 3 | 8 | −2.782 / +0.159 |

The top's RTL (`protocol_processor_top.sv`) is byte-identical between base and `main`,
and between head and merge head. So both pairs apply exactly item 4: one opcode term
feeding the four class bits, and no register.

- **base -> head: −30 LUT, −4 FF.**
- **`main` -> merge head: +67 LUT, +110 FF.**
  - **The flip-flops.** All 110 are the untrimmed entries of the top's timer-arm queue
    for face 0, the ACMP listener (`armq_r` and `armq_cnt_r`,
    `hdl/top/protocol_processor_top.sv:2962-3044`): entries 1 to 3 (108 bits) and two
    count bits. `arm_drain_pick` pops face 0 whenever it is not empty, because it is
    first in the loop. So its count never exceeds 1, and entries 1 to 3 are never
    written.
    - Vivado proves that and trims them in the base, head and `main` builds, which keep
      36 bits of face 0. It does not in the merge build, which keeps 144.
    - The arm mux is identical in all four, and the classifier has no path to it.
    - Without those 110 bits, the merge head's FF count equals `main`'s exactly:
      23,418. Its other top-level register changes cancel: `link_q_r` -1, `st_ls_r` +1.
  - **The LUTs.** The rebuilt-hierarchy rows move both ways and are not an attribution:
    - base -> head: the top's own row +155, its children −185;
    - `main` -> merge head: the top's own row +23 (which also holds the untrimmed
      queue's write and shift logic), its children +44. The children include modules
      whose RTL is identical: `u_listener` +95, `u_acmp_q` −56, `u_aecp_q` +49,
      `u_ca_builder` −35.
- **The parent's resource gate** (`syn/ooc/pp_resource_gate.py check --endpoint
  ooc-1x1`, against `pp_resource_baseline.json`):
  - `main` and the merge head: rc 0 (merge head: LUT −135, FF −1,817 against the
    recorded baseline).
  - base and head: rc 1 (+598 and +568 LUT). The recorded baseline predates the name
    stage's `u_d3` growth, as the #230 and #232 lanes recorded.
- **Synthesis time:** about 20 minutes each.

## Validation

Verilator 5.050 (the CI pin). Every command ran unpiped, with its own log and rc
file.

- Base and `main` ran in the scratch parent's processor submodule, each at its
  commit.
- The two heads ran in this branch's checkout.
- `7b95590` changes only `tb/pp_top/README.md`, which no build or campaign reads.
  The docs gates and `git diff --check` ran again there.

### Processor suites

| Gate | Base `83999eba` | Head `beb7c22` | `main` `c050d971` | Merge head `db2c4eb` |
|---|---|---|---|---|
| `./scripts/run_suites.sh` | rc 0: 33 suites, 1,021,469 | rc 0, 1,021,484 | rc 0, 1,021,485 | rc 0, 1,021,500 |
| `make -C tb/pp_top` | rc 0, 10,416 (5 builds) | rc 0, 10,431 (6 builds) | rc 0, 10,416 | rc 0, 10,431 |
| `./scripts/lint_hdl.sh` | rc 0, 41 modules | rc 0 | rc 0 | rc 0 |
| `make check` | rc 0, 1,120 links | rc 0, 1,122 (also at `7b95590`) | rc 0, 1,120 | rc 0, 1,122 |
| `python3 scripts/gen_matrix.py --check` | rc 0, 94 rows, 0 untested | rc 0 | rc 0 | rc 0 |
| `./syn/yosys/run.sh` | rc 0, 42 tops and the Xilinx map | rc 0, the same | rc 0, the same | rc 0, the same |

- The µPC map and M9 gates pass in every run.
- `git diff --check 83999eba` is rc 0 at `7b95590`; `git diff --check c050d971` is rc
  0 at `db2c4eb`.
- Every per-section line of `tb/pp_top` is identical, base to head and main to merge
  head, except HZ, the default build's total and the new sixth build. TB's whole
  latency histogram is included.
- TD measures the same at both heads: the auto-unlock at 60,003 ms, the expiry at
  300,002 ms, 6 monitor probes answered.

### Campaigns

These are the campaigns that build a changed file: `protocol_processor_top.sv`, the
`tb/pp_top` bench, or main's `KL_aecp_notify.sv`. Each ran with `--jobs 3` where its
driver takes it. Logs were compared line by line, with paths normalized, base
against head and main against merge head.

| Campaign | Base / main | Head / merge head | Record |
|---|---|---|---|
| `tb/pp_top/aecp_mutants.py` | rc 0: 5 controls PASS, 55 of 55 KILLED | rc 0: 6 controls PASS, 61 of 61 KILLED | changed as listed above; main's equals base's and the merge head's equals the head's, line for line |
| `tb/pp_top/aecp_dispatch_mutants.py` | rc 0, 44 of 44 | the same | identical |
| `tb/pp_top/acmp_mutants.py` | rc 0: 19 of 19, goldens PASS | the same | identical (print order differs) |
| `tb/pp_top/ctr_mutants.py` | rc 0, 18 of 18 | the same | identical |
| `tb/pp_top/d3_mutants.py` | rc 0: 110 of 110, goldens PASS | the same | identical (print order differs) |
| `tb/pp_top/gsi_mutants.py` | rc 0: 20 detected, golden and restored PASS | the same | identical |
| `tb/pp_top/name_wr_mutant.py` | rc 0: killed, golden and restored PASS | the same | identical |
| `tb/pp_top/notify_mutants.py` | rc 0: 40 of 40 (base), 47 of 47 (main) | the same as each | identical (print order differs) |
| `tb/maap/mutants.py` | rc 0, 32 of 32 | the same | identical |
| `tb/adp_engine/mutants.py` | rc 0, 43 of 43 | the same | identical |

The campaigns that build no changed file were not re-run: `tb/srp_top`,
`tb/srp_admission`, `tb/acmp_talker` retry, `tb/desc_mem_guard`, `tb/desc_store` lint
and the `tb/nvm_port` figures.

### Parent consumer set

- milan-fpga dev `241f9184`, in a scratch clone that was never committed.
- `parent-adoption-c8-bbf704ec.patch`, then `parent-adoption-p2-p1-1269cdaf.patch`,
  then `parent-adoption-c10-1269cdaf.patch`, each applied cleanly with `git apply`.
- `gptp-processor` and `third_party/verilog-axis` are at their pins. `external` is
  recorded and not initialized.
- `protocol-processor` is a clone of this branch, with the gitlink set to the commit
  measured.
- The gates ran at the merge head `db2c4eb`. They also ran at `7b95590`, with the
  same verdicts.

| # | Command | rc | Result at the merge head `db2c4eb` |
|---:|---|---:|---|
| 1 | `scripts/check_cpp_idiom.py` | 0 | every count 0 <= 0 |
| 2 | `scripts/check_py_idiom.py` | 0 | every ratchet held. 307 modules, 195,220 lines: base 195,163, +21 for the arms added to `aecp_mutants.py`, +36 for main's `notify_mutants.py` |
| 3 | `scripts/check_rtl_source_lists.py` | 0 | 108 files in the `milan_datapath` closure, 4 of 4 lists; protocol-processor 42/42 tops, 0 recorded |
| 3s | `scripts/check_rtl_source_lists.py --selftest` | 0 | 50 of 50 |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0 | 46 tracked sources derived, self-test passed |
| 5 | `scripts/check_port_contracts.py` | 0 | protocol-processor 1,759 ports, 111 <= 111 undocumented |
| 6 | `scripts/measure_naming.py --check` | 0 | 95 candidates, all recorded |
| 7 | `scripts/measure_test_evidence.py --check` | 0 | 72 <= 77, 10 <= 10, 0 <= 0, 3 <= 3 |
| 8 | `scripts/docs_check.py` | 0 | 0 findings across 187 md + 975 files |
| 9 | `scripts/xvlog_gate.py --check`, then `--selftest` (alone, under the Vivado lock) | 1, then **0** | Without PR #153's parent patch: `BANK IT ... KL_aecp_notify.sv\|VRFC 10-3380\|pd_ix_w no longer occurs`. This is #153's fix (#22), which the pin bump banks; see below. With `parent-adoption-232-241f9184.patch` applied fourth: `PASS (2 finding(s) == ratchet; 0 hdl/, 2 pinned processors)`, pinned at `protocol-processor@db2c4eb8`; self-test PASS. At `7b95590`, before the merge, with the three patches: `PASS (3 finding(s) == ratchet)` |
| 10 | `sw/builder/test_builder.py` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN: gate 11 needs a local board build tree, as in earlier records |
| 11 | `scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j16` | 0 | 606, 606, 646 and 311 checks, 0 failures |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | both lint runs complete (its recipe makes warnings non-fatal) |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 of 315, `RESULT: PASS` |
| 15 | `make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=3` | 0 | 9 `RESULT: PASS`, 0 FAIL |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | **2** | two-stream leg: 65 checks, 0 failures. Shipping leg: 155 checks, **2 failures, both T30 INTERNAL LAW** (`got=227 exp=292` and `got=285 exp=292`; first-event delay 18396..18821 cycles). These belong to milan-fpga #643 / PR #648; see the base control below |
| 16b | `python3 tdm8_render_mutants.py --leg-defects`, in `tb/verilator/milan_dp_render` (the step of gate 16's recipe that make skipped) | 0 | 5 of 5 leg defects caught |
| 17 | `scripts/check_sh_idiom.py` | 0 | every count held |

- **Base control for gate 16.** The same parent was run with the processor and
  gitlink at `83999eba` and the render build products removed. `make -C
  tb/verilator/milan_dp_render tdm8render -j16` gave rc 2: 155 checks, the same two
  T30 INTERNAL LAW failures with the same numbers (got=227, got=285,
  18396..18821 cycles; T30 CRF LAW 17051..17055 in both). The failure is #643's at
  this dev revision, not this lane's.
- Gates 1 to 8, 3s, 11 and 17 also ran at base `83999eba`. Every one is rc 0 with the
  same output, except py-idiom's line count.
- **PR #153's parent patch.** After the merge, gate 9 needs
  `parent-adoption-232-241f9184.patch`, recorded in PR #153's body: sha256
  `88ee5e96...`, the same file in that lane's evidence. It drops the vanished `pd_ix_w`
  line from the parent's `scripts/xvlog.budget`.
  - The pin bump owes it, not this lane, as PR #140 treated #137's line.
  - It was applied fourth in the scratch copy. With it, gates 1 to 8, 3s, 11 and 17
    re-ran: all rc 0.
  - The other gates read no budget.

## Parent-visible list

- No port, parameter or register-map change. The top's header is byte-identical to
  the base.
- Behaviour: a GET_DYNAMIC_INFO now waits for an in-flight ACMP stream step, and an
  ACMP stream step waits for an in-flight GET_DYNAMIC_INFO. ACMP reads and every
  other command are unchanged.
- `tb/pp_top` builds six times. The new entry point is `make -C tb/pp_top
  timer-defaults`, and the AECP campaign gains its control and six arms. The CI
  step is unchanged.
- No parent adaptation is needed for this lane's changes. The merged `main` brings PR
  #153, whose own parent patch (`parent-adoption-232-241f9184.patch`, the xvlog ratchet)
  the pin bump owes.
- The parent's resource gate passes at the merge head (`ooc-1x1`, rc 0).

**Manager commit (round 1b).** `1d6c78f1` applies R468-1 F1 as its required outcome gives it: F06.14's GET_DYNAMIC_INFO class cell, F03.7's RO_SNAPSHOT and MAP_CFG rows, and the 03 §6 classifier list now name the landed MAP_CFG admission class. Docs only; `make check` passes. Item 3 also meets #71 acceptance 2 (R468-1 S3), hence "Relates to #71".

**Manager merge.** Processor `main` `07b1469d` (PR #154: SRP files only, none in common with this PR) merged at `f9b8f0ee` with no conflicts; donor and parent consumer re-run at that head.
