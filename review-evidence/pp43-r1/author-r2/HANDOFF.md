# [A255] HANDOFF — PR #111 (issues #43/#49), round 2

Status: **REVIEW READY**. All assigned items are implemented and committed locally. Every CI gate, the suite bank, lint, portability, the retained mutant runner, both reviewers' probes and mutant sets, and the parent consumer check pass at the final head. Nothing was pushed, no PR was edited, no parent commit was made and no hardware was used.

- Lane: `$LANES/pp43-49-gsi-internal`, branch `43-49-gsi-internal` (local, not pushed)
- Start head: `5771578784c77e945980c78faa52f3e54bcf5e2d` (round 1)
- **Final head: `a14ef8b4787b5309dd9ab472e82ae2b4a3fdbb72`**, tree `71081cc12048a81b920dc48b9a508e3b120b96e3`
- Source base: `939c143333d11e2378a514f1c7b6abd4c3259bfd`
- Authority:
  - decision [43#issuecomment-5814505442](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/43#issuecomment-5814505442)
  - reviews [R294-1](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/111#issuecomment-5814496442) and [R295-1](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/111#issuecomment-5814334568)
  - evidence packet at kebag-logic/milan-fpga `pp43-review-evidence` (archives `6f71700a`, `41da432c`), read-only
- Tools (outside this directory):
  - pinned Verilator 5.050: `$VALIDATION_TOOLS/verilator-v5.050/bin`
  - Vivado 2026.1: `~/Xilinx/2026.1/Vivado/bin/vivado`
  - yosys 0.66 + sv2v and mmdc from the host PATH

Review notification: [43#issuecomment-5816221930](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/43#issuecomment-5816221930) (text in `REVIEW-READY.md`).

## Round-2 commits (one-line subjects, no body, no trailers)

| Commit | Subject | Content |
|---|---|---|
| `f28e90b2` | Notify re-bind started/stopped changes, keep FailureInformation changes off the Listener declaration and read input owners live | RTL, all tests, docs |
| `68ad935641` | Let the processor OOC recipe take a stream shape and record the input selector area | `syn/ooc` tcl shape args and README record only |
| `a14ef8b4` | Compare the ungated bridge with the latch it held before the swap | Test only (see "Why a14ef8b") |

## Items (assignment order)

### 1. R295-1 F1: re-bind notification

- **RTL** (`hdl/acmp/KL_pp_acmp_listener.sv`): removed `bind_act_r` and the `!bind_act_r` exclusion from `act_strt_chg_o`/`act_strt_cmd_chg_o`.
  - The exclusion existed because A4's discovery arm used to push upstream. Round 1 removed that term.
  - From PRB_W_RESP, a BIND_NEW to another talker (`A1 A11 A9 A2 A3 A4 A5`) leaves pbsta/acmpsta at ACTIVE/0, so nothing notified the STREAMING_WAIT flip.
  - **De-duplication argument:** the started/stopped pulse and the top's `lstn_gsi_changed_r` are both registered at the X_WB record write. A walk that moves both lands them in the same cycle, and the OR gives one event.
  - `bnd_was_r` is now load-bearing: it keeps a fresh bind (undefined to started) from pulsing. The comment says so.
- **Comments:**
  - listener port doc and the `bnd_was_r` / X_WB comments
  - top `stri_events` comment and the `ev_stri_in_i` comment at the engine instance
- **06 §7:** now holds the single STREAM_INPUT trigger rule. The §6.2 paragraph points to it.
- **06 F06.13:** the BOUND/STREAMING_WAIT row names the re-bind.
- **Response-level test, GI REBIND-SW** (`tb/pp_top/gsi_internal.hpp`, `rebind_from_probing`), after the second reset:
  - bind sink 0, which reaches ACTIVE
  - wait for the first PROBE_TX (the sink is now PRB_W_RESP)
  - BIND_RX to `talker+0x55` with STREAMING_WAIT set
  - expect exactly one unsolicited response within 150 ms, byte-exact with STREAMING_WAIT and ACTIVE/0; the solicited body must match
  - then the new talker's ACTIVE/7 and the unbind are checked
- **Harness integrator fold** (GI only, `H::gsi_fold_sw`): STREAMING_WAIT = `acmp_bound_o` && !`aecp_strm_started_o`. It follows F06.13's "folded by the integrator". The pp_top wrapper now exposes `acmp_bound_o`.
- **Unit test** (`tb/acmp_listener` RV8): RV8b and RV8d check exactly one pulse, one cycle after the record write, for that sink. RV8c checks that a re-bind keeping STREAMING_WAIT gives none.
- **Retained mutant** `rebind-started-trigger-removed` (adds `&& !apend_r[ACT_A2_C]`) is killed by `GI REBIND-SW: exactly one unsolicited response for sink 0, got 0`.
- **Unit mutant** (same edit): RV8b and RV8d fail.

### 2. R294-1 F1 = R295-1 F2: separate FailureInformation-change strobe

- **RTL, `KL_srp_listener_fsm`:**
  - `ind_reg_w` is restored to the base form (fresh registration or type swap).
  - New `ind_fchg_w` feeds a registered `evt_tk_fail_chg_o`.
  - The applicant (`decl_pend_r`/`AE_NEW_C`) and `evt_tk_registered_o` are untouched by it.
- **Wiring:** `KL_srp_top` exports the strobe; the top ORs it only into `stri_events`. It never reaches the event router or the ACMP listener (decision: preferably not, so not).
- **Wire-level test** (GI, around FAILED-REFRESH):
  - Control: after the fresh Failed registration on sink 0, at least one Listener New (MSRP frames parsed per vector value, 1 s window).
  - After the changed refresh: zero Listener New in 600 ms.
  - FAILED-REFRESH still notifies (existing pair).
  - The R294 P2 anchors (`a1`/`a2` blocks and the unique `void run() {`) are kept intact.
- **Module tests:**
  - `srp_stream_fsms` section L (19 checks): change and unchanged, bridge-only and code-only, a non-registering In, the LV case, swaps, a two-stream hit-sink compare and a shared-stream late settle.
  - `srp_top` section D (4 checks): strobe counts, latch values, no Listener New on the wire, unchanged refresh.
  - Mutation tables are added to both READMEs.
- **Retained mutants:** `failure-change-strobe-removed` and `failure-change-redeclares` are killed by the named FAILED-REFRESH checks.
- **Docs:**
  - 10 §6.4 paragraph and the F10.5 self-transition
  - 02 event-catalog row `TK_FAILURE_CHANGE{sink}` (direct, not routed)
  - F02.10 msrp_fail row
  - F06.13 row

### 3. Selector-0 sample-and-hold removed

- **RTL:** in `protocol_processor_top`, `gsi_sample` and its 81 registers are removed. `gsi_owner_read` reads the SRP code, the gated bridge and `lstn_gsi_status_r` live at the selector 4, 5 and 7 beats. The guard `32'(gsi_desc_index_o) < N_STREAM_IN_P` stays before narrowing.
- **06 F06.13** "Reads" paragraph with the coherence bound: one gather spans a few cycles, longer only while the integrator holds a beat (bounded by the watchdog). A change inside it can mix beats in that one response. The change is itself a trigger whose pending bit is set after the change (`KL_aecp_notify` sets `pe_sin_r` on intake and clears it at emission selection), so its own notification follows with coherent values.
- **Integrator guide §8** pointer updated.
- **Registers saved** (Vivado hierarchical report, the top's own registers, round 1 → round 2): **−81 at 8x8, −78 at 1x1**.
  - Total registers against round 1: −74 at 8x8 and −71 at 1x1. Besides the sample, the SRP listener gains the strobe registers (+8 at 8x8, +1 at 1x1). The remaining few are synthesis variance.
  - Caveat: the hierarchical reports leave some instances unlisted, and which ones varies by build; `g_rx_pool[0]` is listed only in some. The instance rows therefore do not sum exactly to the totals, and the totals are authoritative. Own plus listed children against total, 8x8: base 30,245/30,354, round 1 31,029/31,138, round 2 30,992/31,064. The top's own row is comparable across builds: base 4,615, round 1 4,768, round 2 4,687.

### 4. Area

- The SRP listener bridge output is ungated (`msrp_fail_bridge_o = fsysid_r`). The top gates it once after the index mux: `srp_tk_reg_state_w[gsi_sink_w] == 2'd2`.
- The FailureInformation compare is one 72-bit comparator on the lowest candidate hit sink. Candidates are sinks registered Failed on the same key; they share a latch, and the invariant is argued in the RTL comment. The `srp_stream_fsms` L8 and L9 checks and unit mutants back it.
- The failure **code** stays gated per sink, because it is a top-level port (`srp_snk_fail_code_o`) and its behaviour is kept.
- **OOC recipe** (`syn/ooc/protocol_processor_ooc.tcl`) takes optional args 2 and 3, `N_STREAM_IN_P` and `N_STREAM_OUT_P`. Runs used the candidate's recipe with `-tclargs <tree> [1 1]` on `git archive` extracts of base, round 1 and `f28e90b2`. `a14ef8b` has the same RTL.
- Reports: `area/<tree>-<shape>/`, summary `area/summary.txt` (from `area/area_table.py`).

| Shape | Resource | Base | Round 1 | Round 2 | Round 2 − base | Round 2 − round 1 |
|---|---|---:|---:|---:|---:|---:|
| 8x8 | LUTs | 28,092 | 28,732 | 28,326 | +234 | −406 |
| 8x8 | FF | 30,354 | 31,138 | 31,064 | +710 | −74 |
| 1x1 | LUTs | 20,978 | 21,163 | 21,245 | +267 | +82 |
| 1x1 | FF | 23,446 | 23,745 | 23,674 | +228 | −71 |

- Block RAM is unchanged (24 and 16.5 tiles).
- Base and round-1 8x8 totals reproduce the published round-1 reports exactly.
- Touched instances, round 2 − round 1:

| Shape | Instance | LUTs | FF |
|---|---|---:|---:|
| 8x8 | SRP u_listener | −353 | +8 |
| 8x8 | top own | +41 | −81 |
| 1x1 | SRP u_listener | −47 | +1 |
| 1x1 | top own | +32 | −78 |

- The 1x1 LUT delta against round 1 (+82) is dominated by untouched modules (u_talker +40, u_event_router +25, u_timer +25, u_originator −63, g_rx_pool[0] −58, ...). This is synthesis variance.
- **WNS (OOC, informational).** Base −9.524, round 1 −9.618, round 2 −10.089 ns at 8x8. At 1x1: base −5.564, round 2 −6.065 ns. The worst path is the pre-existing `u_notify` → `u_event_router`/`u_tx_arbiter` path in every build.
- **Targeted report** on the round-2 8x8 netlist (`area/cand-8x8-paths/`):
  - into `u_aecp/gxr_data_r`: slack +4.831 ns (met)
  - from `u_srp/u_listener/fsysid_r`: +5.968 ns (met)

### 5. Also taken

- **R295-1 S1 / R294-1 S2, index guard.** After the second reset, the GI image is `image(10)` (STREAM_INPUT 0..9).
  - `index_guard(1, 1)`: query 9 expects zero internal fields; query 1 (the alias) is PASSIVE, the control.
  - Solicited only. `ntfy_stri_in_w` is per hardware sink, so no unsolicited response can name index 9. This is stated in the test comment and the README.
  - Retained `index-guard-removed` is killed.
- **R295-1 S3, portable affinity.** `gsi_mutants.py` pins eight CPUs only when `os.sched_setaffinity`/`os.sched_getaffinity` exist. It also counts mutants from the list instead of printing "8".
- **R295-1 S4.** The `dbg_recwr_*` ports are documented in `KL_pp_acmp_listener` as the functional record write bus (NVM shadow capture and the GSI status view). They were not renamed, which avoids a five-file rename across suites.

## Gates at the final head `a14ef8b4` (receipts: `gates/<name>.log`, `gates.jsonl`; each run in the foreground, rc read directly, never piped)

The CI workflow `.github/workflows/hdl.yml` has three jobs: docs-gates, suites and portability.

| Gate | rc | Result |
|---|---|---|
| `verilator --version` | 0 | 5.050 2026-07-01 |
| `./scripts/lint_hdl.sh` | 0 | all modules OK |
| `./scripts/run_suites.sh` | 0 | **16,416 checks, 0 failing** (pp_top 1,948; srp_stream_fsms 1,087; srp_top 259; acmp_listener 2,544) |
| `python3 scripts/gen_matrix.py --check` | 0 | 92 rows, 0 untested |
| `git fetch --no-tags origin refs/pull/13/head`, then `make -C tb/nvm_port figures` | 0 / 0 | figures agree |
| `check-links.py` / `check-matrix.py` / `render-wavedrom.py --check` / `make stale` | 0 each | 846 links; 115 REQ rows; 18 blocks |
| `make check` | 0 | 41 mermaid + 18 wavedrom |
| `git diff --check 939c1433 HEAD` | 0 | |
| `./syn/yosys/run.sh` | 0 | 36 tops OK |
| `python3 tb/pp_top/gsi_mutants.py` (pinned) | 0 | 13/13 killed by named checks; golden and restored 488/0 (`mutants/`) |
| Scoped lint: top 1x1/8x8; SRP listener, SRP top and ACMP listener at N=1 | 0 | 0 findings (`scoped-lint.txt`) |

- Unit-suite mutants (scratch copies, `unit-mutants/`): all killed.
  - `srp_stream_fsms`: 4 mutants, 8, 6, 2 and 2 FAIL
  - `srp_top`: 1 mutant, 3 FAIL
  - `acmp_listener`: 1 mutant, 2 FAIL
- Earlier runs at `68ad935` are also in `gates.jsonl`. Two of them (make-check, yosys) first ran with a stripped PATH in my runner and returned rc 2 and 127 because the tools were missing. The runner was fixed to inherit PATH, and both were re-run rc 0. These are not gate failures of the tree. `mutants-dev/` is a pre-commit development run.

## Parent consumer check (`$LANES/pp94-parent-consumer`, exactly as before)

- The parent stays at HEAD `3eaee03f0c50522c4e4da8e12c771ec130a8c2f9`. Its index gitlink is unchanged (`2e1675d2…`) and nothing is staged. Only the processor submodule checkout moved: `git fetch <lane> a14ef8b4…` then `git checkout --detach a14ef8b4…`. `git status` shows only ` M protocol-processor`.
- `python3 scripts/check_rtl_source_lists.py`: rc 0, 106 files, 4/4 consumer lists.
- `make -C tb/verilator/pp_shadow -j8` (pinned 5.050): rc 0, **371 checks, 0 failures**.
- The gitlink-dependent parent gates are the manager's and were not run.

## Reviewer probes and mutants (published scripts, sha256 equal to their MANIFESTs)

- `verilator8` differs from its manifest hash. The published copy has a sanitized path placeholder; it only appends `-j 8` to `$PINNED_VERILATOR`, which was set to the same pinned 5.050.
- The scripts are mode 644 in the packet. They were copied to `/tmp` and made executable, with contents unchanged.
- Each run used a fresh `git archive` of `a14ef8b4`.

| Item | Receipt | Result |
|---|---|---|
| R294 P1 `probe_srp_redeclare.sh` | `reviewer-probes/p1-srp-redeclare-final.log` | `changed-failure: reg_strobes=0`, **`changed-failure next tick pushes=0`**, unchanged 0/0; probe-modified suite 1087/0 |
| R294 P2 `probe_top_redeclare.sh` | `reviewer-probes/p2-top-redeclare-final.log` | **changed-failure: 0 listener declarations** for sink 0 (round 1 had 2 New); unchanged window: periodic JoinMt only; probe-modified GI 488/0 |
| R295 `run_probe.sh` (R1, R2, R3) | `reviewer-probes/r295-probe-final.log` | **R1: rebind_notifications=1, started 1→0**; R1b 0; **R2: changed_refresh_new=0** (first_failed_new=2 control); R3: no leak; 8 checks, 0 failures |
| R294 `extra_mutants.py`, run unchanged | `reviewer-mutants/r294-unchanged/stdout.txt` | rc 1: `srp-failure-strobe-removed: expected 1 site(s), found 0`. The script aborts at its first mutant because that site was removed by design. |

- The same scripts were then driven by `reviewer-mutants/drive.py`. It imports the published module and calls its own `main()`. It keeps every entry whose exact site still exists byte for byte, reports gone sites, and adds `~translated` entries only where the mutated behaviour still exists on a new site.

| Reviewer mutant | Site at final head | Verdict |
|---|---|---|
| R294 `notify-every-write` | unchanged | KILLED |
| R294 `srp-failure-strobe-removed` | gone → `~translated` (strobe never raised) | KILLED (FAILED-REFRESH) |
| R294 `sel4-integrator-byte` | gone (`gsi_fail_code_r` is now `_w`) → `~translated` | KILLED (RESET/BIND-ACTIVE failure code) |
| R294 `live-unsampled-fields` | moot: sample removed | — |
| R294 `index-guard-removed` | gone (guard now before live reads) → `~translated` | KILLED (INDEX-GUARD) |
| R295 `golden-gi` / `golden-full` | unchanged | pass 488/0 and 1928/0 |
| R295 `sink-index-guard-removed` | unchanged | **KILLED** (survived in round 1) |
| R295 `status-compare-removed` | unchanged | KILLED |
| R295 `desc-type-ignored` (full) | unchanged | KILLED (G2) |
| R295 `srp-failure-change-strobe-removed` | gone → `~translated` | KILLED (FAILED-REFRESH) |
| R295 `sample-transparent`, `sample-transparent-full` | moot: sample removed | — |

Receipts: `reviewer-mutants/{r294,r295-gi,r295-full}/` (`sites.json`, `results.json`, per-variant logs).

## Why a14ef8b exists

- R294's P1 injects a changed Failed refresh right after the "AskingFailed rides New after the swap" anchor. My first version of the ungated-bridge check ("L failure gated off") pinned the literal `0xBBBB0000CCCC`, so the probe-modified suite showed 1 FAIL. That failure was unrelated to P1's criterion, which already printed `pushes=0` at `68ad935`.
- The check now compares with the latch value held just before the swap back, which is just as exact and robust to the probe. P1 at `a14ef8b` runs 1087/0.

## Notes for the manager

- **Not taken (outside the directive list):** R294-1 S3, the decoder's registered `evt_failure_system_id_o` copy (+128 FF at both shapes, pre-existing, now kept alive).
- **Pre-existing observation, not changed here:** the SRP listener re-latches `acc_latency` on every registering event (10 §6.4 "refresh re-latches"), but a refresh that changes only accumulated latency raises no event. GET_STREAM_INFO's msrp_accumulated_latency can therefore change without a notification.
  - The base behaves the same.
  - F06.13 lists its update event as "talker-attr change".
  - My docs describe only the observed trigger set and do not claim every field.
  - Worth a separate decision.
- **Output directory contents:** this output directory holds six empty Vivado `.Xil/` folders under `area/*/`. Deleting them was refused by the session's permission mode. They hold no tools.

## Pending manager duties

- Push `43-49-gsi-internal` at `a14ef8b4` and update the PR #111 body from `PR-BODY.md`.
- Hosted/act acceptance.
- Parent gitlink-dependent gates and the merge-turn candidate (source base `939c1433`).
- Independent re-review of round 2.
- Parent #508 adoption: the integrator gather for input selectors 5 and 7 becomes unused. The integrator must keep deriving MSRP_FAILURE_VALID and its other validity flags from `srp_tk_reg_state`, and must fold `acmp_bound_o`/`aecp_strm_started_o` into STREAMING_WAIT.

## Scratch cleanup

`/tmp/a255-scratch` held the read-only evidence fetch, the reviewer scripts, the `git archive` trees and the mutant work copies. It was deleted after every receipt above was copied here (`ls` confirms absence). The lane's working tree is clean at `a14ef8b4`; its build products are git-ignored.
