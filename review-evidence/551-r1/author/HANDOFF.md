# [A257] Issue #551 handoff

Status: author implementation complete and locally committed. All assigned gates pass; ready for independent review.
Issue: https://github.com/kebag-logic/milan-fpga/issues/551
Assignment: https://github.com/kebag-logic/milan-fpga/issues/551#issuecomment-5814963437
Base: `59b816708852472da6ed4576386c30ebd5f8f839`
Branch: `551-licence-real-grant`
Head: `4eca4540d6a278aeb56687029d752bade6e714e3`
Commit subject: Require real SRP admission for talker licences

## Change list

| File:line | Change |
|---|---|
| `hdl/milan/milan_datapath.sv:6594` | Bitwise ACTIVE AND real per-source admission grant; shared by every AAF/CRF licence and diagnostic consumer. |
| `hdl/milan/milan_datapath.sv:5278` | CRF reservation contract now names both terms. |
| `hdl/milan/milan_datapath.sv:6569` | Opening, refusal, counter and status semantics rewritten. |
| `tb/verilator/milan_dp/sim_crf_licence.cpp:1048` | Pending service tuple staging and actual MAC Listener Ready timing calibration. |
| `tb/verilator/milan_dp/sim_crf_licence.cpp:1072` | Refused/admitted re-declarations for both sources and both admission phases; nonzero counter histories and measured latency. |
| `tb/verilator/milan_dp/sim_crf_licence.cpp:364` | Continuous ACTIVE/grant/licence sampling and decoded Listener event observation. |
| `tb/verilator/milan_dp/crflic_probes.vlt:1` | Simulation-only visibility for captured request registers and decoded event observation. |
| `tb/verilator/milan_dp/Makefile:259` | Licence recipe includes the visibility configuration; same recipe in default sweep and mutants. |
| `tb/verilator/milan_dp/crflic_mutants.py:53` | Retained ACTIVE-removal controls plus three real-grant-removal controls. |
| `tb/verilator/milan_dp/README.md:395` | Fixture boundaries, cases, mutation recipe and measured latency. |
| `docs/reference/FR_NFR.md:215` | FR-SRP-03 refusal has no optimistic licence exception. |
| `docs/reference/REGISTER_MAP.md:933` | CRF reservation field requires the real grant. |
| `docs/reference/REGISTER_MAP.md:1105` | Refused branch, raw ACTIVE versus licensed status, and indexed snapshot semantics. |
| `docs/reference/EGRESS_QUEUE_MAP.md:77` | Admission/refusal semantics and absent-shaper boundary. |
| `docs/traceability/ieee8021q.md:49` | Updated admission contract and Q-9/Q-10 executable evidence. |
| `CHANGELOG.md:29` | Changed licence and refused behavior; latency measurement. |

## Tests

| Command/case | Result | Evidence |
|---|---|---|
| `make -C tb/verilator/milan_dp crflic VERILATOR_JOBS=8` | rc 0; 253 checks, 0 failures | `crflic.log` |
| `[G]`: AAF source 0, CRF source 1, phases 0 and 1 | Real ceiling refuses throughout; optimistic ACTIVE rises then falls; Talker Failed follows. No licence, STREAM_START/STREAM_STOP pair, counter reset, or emitted PDU. | `crflic.log` |
| `[H]`: matching admitted cases | All stream and reset interval counters at the genuine STREAM_START. | `crflic.log` |
| Ordinary Listener Ready / withdrawal, Asking Failed / Ready Failed, LeaveAll, counter interval behavior | Original focused cases pass. | `crflic.log` |
| `make -C tb/verilator/milan_dp VERILATOR_JOBS=8` | rc 0; all 13 simulation legs and built-in render mutation campaign pass | `milan_dp-default.log` |

Latency compares raw ACTIVE (the pre-#551 licence) with the new licence on the same run:

| Source | Admission phase 0 | Admission phase 1 |
|---|---|---|
| AAF uid 0 | 2 cycles | 1 cycle |
| CRF uid 1 | 0 cycles | 1 cycle |

The ordinary Listener Ready case adds 0 cycles. The focused leg's 100 MHz admission clock makes the measured 0--2 cycles 0--20 ns; at 50 MHz those cycles represent 0--40 ns. These measurements cover the two-source shape. The processor optimistic window is three rounds of N_SOURCES cycles.

## Fixture boundary

The test stages a captured pending DECLARE/WITHDRAW_TALKER request at the processor service boundary. The next clock executes the real declaration and admission machinery. It does not force admission results, optimistic state, ACTIVE, registrar state, or licences. Listener Ready comes through the real MAC decoder; measured decode latency is asserted again during each replay. Oversized TSpec = 20,000 bytes, one interval frame; admitted TSpec = 224 bytes. The admission pipeline is warmed, then withdrawal clears the real grant before the graded re-declaration. Nonzero MEDIA_RESET/TIMESTAMP_UNCERTAIN/FRAMES_TX histories (17/29/43) make an accidental reset observable. Previous frames and their observation interval finish before seeding. This is a staged integration corner, not an end-to-end controller timing claim. Media clocks remain running, and admitted counterparts must emit multiple PDUs.

## Mutants

Campaign command: `make -C tb/verilator/milan_dp crflic-mutants VERILATOR_JOBS=8`.

| Mutation | Required failing check | Result |
|---|---|---|
| All gates use raw grant, omitting ACTIVE | CRF licence never opened before Listener Ready | Caught by named harness assertion |
| CRF alone uses raw grant | CRF licence equals ACTIVE AND real grant | Caught by named harness assertion |
| AAF source 0 alone uses raw grant | AAF gate never opened before Listener Ready | Caught by named harness assertion |
| All gates omit real grant | Refused CRF licence never opened | Caught by named harness assertion |
| CRF alone omits real grant | Refused CRF licence never opened | Caught by named harness assertion |
| AAF source 0 alone omits real grant | Refused AAF gate never opened | Caught by named harness assertion |

Campaign rc 0: 7 checks, 7 PASS, 0 FAIL (clean control plus six caught mutants). Evidence: `crflic-mutants.log`. The driver requires a failing harness verdict and the named assertion; a build failure or crash does not count.

## Gates

Every listed command runs in the foreground, without a pipeline. Commands were invoked through the required `rtk proxy` prefix. Paths below are repository-relative. The Markdown renderer uses `/tmp/milan-551-docs-venv/bin/python3`, with `tools/markdown/requirements.txt` installed using its pinned hashes; no environment or toolchain is stored in this output directory.

| Command | Exit code | Log |
|---|---|---|
| `python3 scripts/docs_check.py` | 0 | `docs_check.log` |
| `env GIT_DIR=/tmp/milan-551-absent-git-dir python3 scripts/docs_check.py` | 0 | `docs_check-no-git.log` |
| `python3 scripts/check_em_dash.py --base 59b816708852472da6ed4576386c30ebd5f8f839` | 0 | `check_em_dash.log` |
| `python3 scripts/check_doc_style.py` | 0 | `check_doc_style.log` |
| `python3 scripts/gen_toc.py --check` | 0 | `gen_toc.log` |
| `python3 scripts/check_doc_paths.py` | 0 | `check_doc_paths.log` |
| `python3 scripts/xvlog_gate.py --check` | 0 | `xvlog_gate.log` |
| `python3 scripts/check_rtl_source_lists.py` | 0 | `check_rtl_source_lists.log` |
| `python3 scripts/check_cpp_idiom.py` | 0 | `check_cpp_idiom.log` |
| `python3 scripts/check_py_idiom.py` | 0 | `check_py_idiom.log` |
| `python3 scripts/check_sv_idiom.py` | 0 | `check_sv_idiom.log` |
| `python3 scripts/lint_rtl.py --check` | 0 | `lint_rtl.log` |
| `git diff --check` | 0 | `git-diff-check.log` (empty) |
| `git diff 59b816708852472da6ed4576386c30ebd5f8f839 HEAD --check` | 0 | `git-base-diff-check.log` (empty) |

No-git mode uses an absent GIT_DIR to exercise the same filesystem inventory fallback without removing worktree metadata or creating another checkout; its log explicitly reports `filesystem walk (no git)`. xvlog ran, with 0 first-party findings and 4 unchanged pinned-processor findings at the existing ratchet. RTL lint passed its existing ratchet.

## Remaining work

Author work and PR-BODY.md are complete. Public REVIEW READY posted: https://github.com/kebag-logic/milan-fpga/issues/551#issuecomment-5815540316. REVIEW-READY.md contains its exact body. Independent reviewer assignment and subsequent publication/review/merge gates remain for the manager. No push, PR creation/edit, merge, other checkout, sub-agent or hardware action was performed.

## Default sweep receipts

| Leg | Result |
|---|---|
| `./obj_gptp/Vmilan_dp_gptp` | 181 checks: 181 PASS, 0 FAIL |
| `./obj_gptplat/Vmilan_dp_gptplat` | 181 checks: 181 PASS, 0 FAIL |
| `./obj_dir/Vmilan_dp_sim` | milan_datapath: 230 checks, 0 failures |
| `./obj_notify/Vmilan_dp_notify` | checks: 146   failures: 0 |
| `./obj_crflic/Vmilan_dp_crflic` | checks: 253   failures: 0 |
| `./obj_nxn/Vmilan_dp_nxn` | checks: 1708   failures: 0 |
| `./obj_nxndv/Vmilan_dp_nxndv` | checks: 1710   failures: 0 |
| `./obj_nxn8/Vmilan_dp_nxn8` | checks: 3136   failures: 0 |
| `./obj_nxn4c/Vmilan_dp_nxn4c` | checks: 1708   failures: 0 |
| `./obj_nolpf/Vmilan_dp_nolpf` | milan_datapath: 230 checks, 0 failures |
| `./obj_prune/Vmilan_dp_prune` | checks: 33   failures: 0 |
| `./obj_ax1x1/Vmilan_dp_ax1x1` | milan_datapath: 227 checks, 0 failures |
| `./obj_aclk/Vmilan_dp_aclk` | media_aclk: 139 checks, 0 failures |
| Built-in render mutation campaign | 6 checks: 6 PASS, 0 FAIL |
