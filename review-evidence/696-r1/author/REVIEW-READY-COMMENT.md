[A570] REVIEW READY
Commit: `030eb98a12685a2ca41cf8d785bb0eb69dc32a98` (branch `696-maap-annexb`, local, not pushed; clean tree)

Ruling [6089712293](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6089712293) is applied (option b, no floor exception).

**Changed** since the [route-floor STOP](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6089695284):
- `0df48637`: merge of dev `8b61b709` (= `origin/dev`, the merge of #699) into `39571196`, as a merge commit. No conflict and pins unchanged. The lane's diff over dev equals its diff over `6aa25dec`.
- `e6f00121`: `syn/ooc/pp_resource_baseline.json` only. The three endpoints are written by `record --write` from the merge-result measurement. Identities, tolerances, floors and ceilings are unchanged; `check-baseline` exits 0.
- `030eb98a`: `docs/design/AREA_BUDGET.md` (record table, binding WNS limit, seventh re-baseline) and `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` (new section "Re-baseline of 2026-10-10, issue #696").

**Validation** at the merge result `0df48637` (M); the documentation set again at `030eb98a` (F). Every command rc 0, unpiped:

| Gate | Result |
|---|---|
| `run_all_suites.sh` (clean worktree, no flock) | 61/61 suites, 2,185,905 checks, 0 failures, 0 timeouts; 4 declared field-campaign skips |
| `tsn_fuzz` with the `rtl.yml`-pinned generator | AAF 164 and gPTP 677 pass, both freshness checks pass |
| `xvlog_gate.py --check` (exclusive lock) | 81 + 52 sources, 0 findings |
| `syn/yosys/run.sh` | 58/58 tops; tied-input and tap-purity gates pass |
| `lint_rtl.py --check --self-test` | 90 <= 90 |
| `behave --no-capture -f plain` | 404 scenarios, 1,968 steps |
| MAAP unit / real datapath | 171 / 3 checks, 0 failures |
| MAAP campaign | 51 rows: 49 planted defects caught at their named checks, 2 clean controls |
| MAAP coverage | 215/215 lines |
| Firmware differential `--self-test` | 12/12 cases, 17/17 defects |
| `test_ctrl_firmware.py --require-rv32 --self-test` | pass; general campaign 471/471 |
| Documentation set (94 commands from `docs.yml` plus fast-workflow self-tests) | rc 0 at M and at F; em-dash base `8b61b709` |

Endpoints measured at M through the recipe (`--single-thread-synthesis`, `--integrated-clock`) in one exclusive-lock job, with nothing heavy beside it:

| Endpoint | Measured | vs #645/#647 record | `check` |
|---|---|---|---|
| `route-1x1` | LUT 50,230; FF 54,308; slice 15,823 (27 free); RAMB36 74; RAMB18 27; DSP 14; WNS +0.114 ns; WHS +0.036 ns; 101,344/101,344 nets routed | -37 / -105 / +44; WNS -0.185 ns (limit binding at the old record: at least +0.049 ns) | exit 0 |
| `ooc-1x1` | LUT 23,179; FF 19,779 | every figure equal | exit 0 |
| `ooc-8x8` | LUT 30,135; FF 27,380 | every figure equal | exit 0 |

The measurement inputs were byte-identical to the lane (122 / 119 files, 6 / 6 images), and their digests were unchanged after the runs. There were zero `Synth 8-4445` diagnostics.
The worst setup path (+0.114 ns, 16 levels) runs from `milansoc_sdram_zqcs_timer_count1_reg[1]` to `milansoc_sdram_bankmachine1_level_reg[0]`, in the SDRAM controller.
Route WNS history: #686 +0.241, #645/#647 +0.299, lane head `39571196` +0.029 (not recorded), merge result +0.114 (recorded).

**MAAP resources at M against the ceiling** (`milan_datapath_ooc.tcl`, one thread, exclusive lock): `g_maap.maap_engine` 445 LUT / 340 FF.
That is +6 / +60 against the `6aa25dec` base of 439 / 280, so it is within the +60 / +60 ceiling with the FF allowance fully used.
Dev `8b61b709` alone measures 443 / 280, so the lane's share is +2 / +60, as before the merge.
In the routed image the engine uses 425 LUT / 339 FF. Its worst setup path in keeps +4.037 ns, its worst path out +6.719 ns, and its worst hold +0.135 ns.

**Acceptance criteria:** 1 met (M1-M8 conformed with checks and planted defects; the M6 capacity and M3 pool bias are justified by clause in `MAAP_FABRIC.md`; M8 counting was withdrawn by ruling). 2 met. 3 met: the area is within budget, and all three records were re-recorded through the recipe at the merge result. 4 (bench) belongs to the post-merge lane.

**Open risks/questions:**
- The MAAP FF allowance is fully used.
- The processor banks were not rerun: pins and processor sources are unchanged since their passing run at `963ad3b8e`.
- The field campaign rewrites only the timestamp line of its two generated result pages; that change was discarded.
- No hosted checks: there is no push or PR in this assignment.
- `HANDOFF.md`, `PR-BODY.md` (`Closes #696`) and `merge-receipts/` are in the assigned output directory. No job remains running.
