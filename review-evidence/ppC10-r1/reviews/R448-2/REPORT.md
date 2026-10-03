[R448] NEGATIVE - exact head cd08ca7b3d962ab040d8aaa023c57e7b0e010a6d

# R448-2: independent internal review of PR #149 (lane C10; issues #25, #17, #37; #22 related), round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #149.
- Exact head: `cd08ca7b3d962ab040d8aaa023c57e7b0e010a6d`, tree `e0b4807f1a6e2254a495f147f28e55e86d08f0bf`.
- Source base: `f4167536d358c996f4e1b70b875879c1651f85d3`. The round-2 delta is `54f9411a..cd08ca7b`: five commits and seven files (`syn/yosys/run.sh`, `hdl/packet_engine/KL_pp_nvm_port.sv`, `tb/nvm_port/{elab_bounds.sh,README.md,Makefile,sim_main.cpp}`, `docs/architecture/09_verification.md`).
- Review start: PR #149 comment 5970571759. Round-2 assignment: issue #25 comment 5969440297.
- Role: internal independent reviewer, cleared context, own detached clone. After the probes the clone is byte-exact (`receipts/clone_integrity.txt`).

## Verdict

**NEGATIVE, for one open MINOR finding (F1).**

Round 2 resolves every round-1 finding as each was literally stated:

- The amended parent patch leaves gate 3 and its self-test green, and the self-test still kills both refusals.
- The `MAX_PAYLOAD_P` bound is derived and its class is graded.
- The citations are correct.
- R449-1's split-header probe now goes red.

However, the new census reads `^module` from sv2v's all.v, and sv2v keeps a module's attribute instance on the header line. So a module declared as `(* keep_hierarchy = "yes" *) module X`, with the attribute on the same line or on the line before, escapes the census. With a fault planted in it, the gate passes rc 0. The own-line form was caught by round 1's census, so it is a regression in this round.

If that module is listed in `tops`, the gate refuses it as "no longer exist under hdl/". The parent's gate 3, meanwhile, requires it as a top. No configuration passes both gates.

This is the class of R449-1 F2, whose required outcome was a census that "does not depend on header layout". That outcome is therefore retained in a narrower form.

## 1. Reconstruction

1. **Contributor rules.** The processor has no `AGENTS.md` or `CONTRIBUTING.md`. The parent's (milan-fpga `1269cdaf`) were read: AGENTS.md §6 (lenses, severities, the clean-lens format) and CONTRIBUTING.md's section map. The processor's `docs/README.md` was read for conventions.
2. **Frozen scope.** Issue #25's body and its acceptance, the two maintainer corrections (5449611948, 5449704965), the lane assignment (5967291597) and the round-2 assignment (5969440297). Issue #151, which owns the other module-scope `$error` guards, was also read.
3. **Authorities.**
   - #25 acceptance bullet 1: "Every module declared under `hdl/` is a top in `tops`, and a check fails the gate if that ever stops being true."
   - #25 acceptance bullet 3: "A failure names the module it failed on".
   - #17: refuse above the `dev_len_o` bound by name.
   - The parent `scripts/check_rtl_source_lists.py` (gate 3), its self-test, and `.github/workflows/docs.yml:263-264,367-368`.
4. **Diff and history.** `git diff f4167536..cd08ca7b` and `54f9411a..cd08ca7b` (raw), per commit.
5. **Public evidence.**
   - milan-fpga `2a54253e:review-evidence/ppC10-r1` is round 1's author packet.
   - The round-2 author packet (`author-r2/`, including the amended `parent-adoption-c10-1269cdaf.patch`, sha256 `55e62329...`) is in the same directory at the later public commit `2da8e8f0`. Every sha256 equals its MANIFEST.json entry, and `author-r2/PR-BODY.md` equals the live PR body (`receipts/evidence_sha256_check.txt`).
   - No manager bank receipts are in that directory. The manager's static/builder/native results are taken as stated in the assignment.

My own verdict and finding were written to `receipts/independent_pass_draft.md` (17:51 local) before I read R448-1 or R449-1.

## 2. Evidence by round-2 item

### Item 1: the parent adoption patch (R448-1 F1 = R449-1 F1)

Scratch parent: milan-fpga `1269cdaf` worktree, with the submodules initialized at gptp `5dce647a` and verilog-axis `48ff7a7e`. The protocol-processor gitlink is `cd08ca7b` (tree `e0b4807f`, clean). c8, then p2, then the amended c10 each passed `git apply --check`, then were applied (`receipts/parent/setup.txt`).

| Probe (`scripts/parent_f1_probes.sh`, `receipts/parent/f1_probes.txt`) | rc | Result |
|---|---:|---|
| `check_rtl_source_lists.py` | 0 | `protocol-processor 42/42 tops, 0 recorded` (`gate3_c8_p2_c10.log`) |
| `check_rtl_source_lists.py --selftest` | 0 | `50 checks: 50 PASS` (`gate3_selftest_c8_p2_c10.log`) |
| live: a stale record planted (`KL_srp_top` added to the budget) | 1 | `STALE RECORD ... 'KL_srp_top'` |
| live: an unrecorded omission planted (`KL_srp_top` dropped from `tops`) | 1 | `TOPS DRIFT ... 'KL_srp_top'` |
| live: the same omission, recorded | 0 | debt, as designed |
| self-test with `verdict()` dropping STALE RECORD | 1 | 49/50; only the new arm "its record left behind ... STALE RECORD" fails |
| self-test with `verdict()` dropping TOPS DRIFT | 1 | 48/50 (the new synthetic arm and the commented-out-top arm) |
| self-test with stale or drift findings not counted | 1, 1 | the new arms fail |
| self-test with `compare_tops()` returning no stale / no unrecorded | 1, 1 | 48/50 and 44/50 |
| amended self-test with six records, processor at the old pin `631eeb34` | 0 | 50/50; gate 3 rc 0 with `36/42 tops, 6 recorded` (`selftest_amended_pin631eeb34_six_records.log`) |

Other parent checks with c10 are all rc 0 (`receipts/parent/other/`):

- `check_sh_idiom.py` and its self-test (48/48). The control run with round 1's `run.sh` is rc 1: `unquoted expansion 5 > 3`, `top-heavy long script 1 > 0`. So the gate scans `run.sh`, and round 2's function refactor is what makes it pass.
- `pp_srcs.py --check --selftest`, `check_entity_shape.py --self-test`, `check_todo_ownership.py --selftest` (45/45), `check_port_contracts.py`, `measure_naming.py --check`, `check_baremetal_only.py --check/--selftest`.
- `xvlog_gate.py --selftest` (PASS).

R449-1 R3's exact text is present in the patched `CODE_QUALITY.md`, and the old sentence is gone (`receipts/parent/r3_exact_text_check.txt`). The PR body's parent-visible list item 2 names the self-test change.

### Item 2: the census read from all.v (R449-1 F2)

All planted with a fault (an undeclared instance) in a new `hdl/top/` file (`scripts/census_probe.sh`, `census_cases.txt`, `receipts/census/`):

| Header layout | at this head | at round 1 `54f9411` |
|---|---|---|
| `module` / name on the next line (also R449-1's `yosys_fault.sh newmod`, unchanged: `receipts/r449_probes/newmod-*`) | rc 1, census names it | rc 0, missed |
| the same, added to `tops` | rc 1, `YOSYS FAIL KL_r448_split: ... \r448_absent_module ...` | |
| `module automatic` / name on the next line; `module /* c */ X`; `module // c` / X; `macromodule X` | rc 1 each, census names it | |
| **`(* keep_hierarchy = "yes" *) module X`** (same line) | **rc 0, missed**: `YOSYS 42 tops`, XILINX OK | rc 0, missed |
| **`(* keep_hierarchy = "yes" *)` / `module X`** (own line) | **rc 0, missed** | rc 1, census names it |
| the own-line form, clean, added to `tops` | **rc 1**: `tops array names modules that no longer exist under hdl/: KL_r448_attro` | |
| a module inside an undefined `` `ifdef `` | rc 0, not counted | rc 1, census names it |

- all.v is exactly what yosys reads. The census greps `$work/all.v` (`run.sh:168-169`). The gate's `read_verilog -defer all.v` and the XILINX regression run in `$work` on the same file, and nothing writes all.v between them.
- `parse_site()` (`run.sh:241-247`), driven verbatim (`receipts/census_unit/parse_site_unit.txt`), names a parse error inside `module automatic KL_auto` as module `automatic`. Inside an attributed module, it names the previous module.
- The unchanged round-1 probes reproduce exactly: 24 cases from `scripts/gate_cases.txt`, plus the fatal-class fault, the fake exit-0 yosys and the two per-top oracles. Every rc and every named verdict line is identical to round 1 (`receipts/gate_probes/`).
- The clean head gate is rc 0: 42 OK, `parsed 1 time(s)`, XILINX OK (`receipts/head_gates/yosys_run.log`).

### Items 3-4: the derived bound and the graded class (R448-1 S1, R449-1 F3, F4)

- `KL_pp_nvm_port.sv:196-200`: `MAXP_BOUND_C = (1 << $bits(dev_len_o)) - 1 - int'(HDR_LEN_C)` is used in the condition and printed with `HDR_LEN_C` in the message. 65527 appears only in the bench.
- The round-2 hunks replace eleven lines with eleven, so later lines keep their numbers.
- No logic is added. sv2v + yosys `proc; opt -full; clean` netlists of the port are identical between round 1 and head, and between base and head, at 1024 and at 65527 (`receipts/nvm_equiv/`).
- `elab_bounds.sh` at the head is rc 0. The refusals are `%Warning-USERFATAL`, and the yosys leg reports `65528 stops at the guard's $finish` (yosys: `ERROR: System task $finish executed`, `receipts/nvm_yosys/`).
- Mutant campaign (`scripts/nvm_mutants.py`, `nvm_mutant_run.sh`, `receipts/nvm_mutants/`), pinned Verilator. **12 of 12 killed:**
  - guard deleted, bound + 1, `>=`, message without the bound, `initial` placement;
  - `$error`, and `$error` with sv2v and yosys off PATH (`YOSYS SKIP`, still red on the class);
  - `$warning`, `$info`;
  - `HDR_LEN_C` = 10 (refuses 65527: "is above 65525: 10 + it ...");
  - `dev_len_o` widened to 17 bits.
- Three expected equivalents survive at the shipped values: a literal condition, a literal message, and `$fatal(0, ...)`.
- R449-1's `nvm_bound_probe.sh`, unchanged (`receipts/r449_probes/`):
  - `pristine`: rc 0, with yosys refusing 65528.
  - `err` and `warn`: rc 1.
  - `hdr10`: rc 1, and yosys now refuses 65527 as well.
  - `derived`: its patch no longer applies, because the literal is gone, so the row is the pristine source. Its row equals pristine, as the PR says.
- The suite at the head: `make -C tb/nvm_port` rc 0, 1,219 checks, 0 FAIL (`receipts/nvm_suite/make_run.log`).
- `scripts/lint_hdl.sh` rc 0, 41/41 (`receipts/lint/`).

### Item 5: citations

Each moved citation was checked against base content (`scripts/cite_check.py`, `receipts/cite_check.txt`, and by inspection):

- `tb/nvm_port/README.md:226` and `sim_main.cpp:1443` → `:244-255` (`dev_cmd_owned_w`'s comment and assign).
- `README.md:1135`, `sim_main.cpp:1441` and `measure_figures.py:117` → `:350-354` (the sticky set).
- `sim_main.cpp:1328` → `:446-449` (`S_WWAIT` arm).
- `README.md:407` → `:376` (`state_r <= S_WEREQ;`).
- `README.md:413` → `:390` (`state_r <= S_WEWAIT;`).
- The ARMS table: all twelve lines are `if (dev_err_i) begin`.
- `README.md:106` → `protocol_processor_top.sv:2726` (`KL_acmp_nvm_shadow #(`).

No other citation into `KL_pp_nvm_port.sv` exists in the tree. The PR body's moved-citation table is complete and correct. `sim_main.cpp:1591`'s `:33-34` lies above the shift and is unchanged.

### Hosted CI at the exact head (read only; the manager owns acceptance)

Workflow `hdl`, push run 37132410209 and pull_request run 37132412884 (`receipts/hosted_checks_cd08ca7.txt`, `hosted_portability_*.txt`, `hosted_suites_steps_cd08ca7.txt`):

- `docs-gates`: success in both runs.
- `portability`: success in both runs. These were executed: 42 OK, `parsed 1 time(s)`, XILINX OK, system allocator.
- `suites`: still **in progress** in both runs at 16:12 UTC. "Lint (zero tolerance) + every suite" and the SRP and MAAP campaigns had succeeded. The ADP campaign was running; the AECP campaigns, the matrix and "nvm_port README figures agree with the tree" were pending.

## 3. Findings

### F1: MINOR. Conformance, Robustness, Tests, Docs. An attributed module header escapes the census

- **Where:**
  - `syn/yosys/run.sh:168-169` (census regex `^module[[:space:]]+((automatic|static)[[:space:]]+)?NAME` over all.v);
  - `run.sh:245` (`parse_site`'s `/^module[ \t]/ { m = $2 }`);
  - `run.sh:161-165`, the comment "sv2v writes each module as `module NAME` at the start of a line however its source lays the header out";
  - the PR body §1 "The census" bullet, which says the same, and its red-proof table.
- **Authority and evidence:**
  - #25 acceptance bullet 1, a check fails the gate when a declared module is not a top; bullet 3, a failure names its module. The round-2 assignment item 2 asks for "a layout-independent census", and R449-1 F2's required outcome was a census that "does not depend on header layout".
  - sv2v 0.0.13 writes `(* keep_hierarchy = "yes" *) module KL_attr2 (a);` on one line, whether the source has the attribute on the same line or the line before.
  - Receipts `census/c-attr-same` and `c-attr-own` are rc 0, with a planted unresolved instance never elaborated. `c-attr-own-top-clean` is rc 1, "no longer exist". `r1-attr-own` is rc 1 (round 1's `.sv` census counted it).
  - The parent's gate 3 (`check_rtl_source_lists.py:477-481`, `^\s*module\s+NAME` over the `.sv` text) counts the own-line form. Left out of `tops`, it gives `TOPS DRIFT ... 'KL_r448_attro'`, rc 1; listed in `tops`, it gives OK (`receipts/parent/attr_crosscheck/`). The processor gate refuses exactly that listing.
  - This codebase already uses attributes, including on their own line before a declaration (`KL_pp_dispatch.sv:302`, `KL_srp_encoder.sv:254`; parent `KL_crf_rx.sv:330`). No house rule forbids a module-level attribute.
  - Secondary effects of the same change: a module behind an undefined `` `ifdef `` is no longer counted (`c-ifdef` rc 0, `r1-ifdef` rc 1), and `parse_site` misnames `module automatic` and attributed modules (`census_unit/parse_site_unit.txt`).
- **Impact:**
  - A legal and plausible declaration form (`keep_hierarchy`, `DONT_TOUCH` on a module) removes a module from Yosys elaboration with the gate green. That is the gap #25 closes.
  - The same module cannot be made a top: the processor census rejects the listing, while parent gate 3 demands it. An author following both gates cannot pass.
  - The run.sh comment and the PR body assert a layout independence that is false for this form.
- **Required outcome:**
  - The census counts a module whose header carries one or more attribute instances, in either source layout. A clean attributed module listed in `tops` passes, and a faulty or omitted one is red and named.
  - `parse_site` names the module for `module automatic` and attributed headers.
  - The PR's red-proof table gains the attributed-header rows.
  - The run.sh comment and the PR body state the census's actual scope, including whether a module under an undefined `` `ifdef `` is meant to be counted (round 1 counted it). If it is not, say so.
- **Verification:**
  - With `scripts/run_census_cases.sh` (`census_cases.txt`, unchanged) at the new head: `c-attr-same` and `c-attr-own` rc 1, naming the module; `c-attr-own-top-clean` rc 0; `c-attr-own-top` rc 1 with `YOSYS FAIL KL_r448_attro`; every other row unchanged.
  - `scripts/parse_site_unit.sh` names `KL_auto` and `KL_attr`.
  - The unchanged gate probes (`scripts/run_gate_cases.sh`) reproduce.

No RESIDUE or SUGGESTION of my own at this head.

## 4. Prior public findings at this head

| Finding | Severity | Status at `cd08ca7` | Evidence |
|---|---|---|---|
| R448-1 F1: c10 leaves parent gate-3 self-test red | MAJOR | **RESOLVED** | gate 3 rc 0, self-test rc 0 (50/50); planted stale and unrecorded both red; drop-STALE `verdict()` mutant now killed by the new arm; six-record pin 50/50; parent-visible list names it (§2 item 1) |
| R448-1 F2: three stale nvm_port citations | MINOR | **RESOLVED** | `:244-255`, `:376`, `:390` verified; full set checked (§2 item 5) |
| R448-1 S1: compute the bound | SUGGESTION | **RESOLVED** | `KL_pp_nvm_port.sv:196-200`; netlists unchanged |
| R448-1 S2: `protocol_processor_top.sv:2714` | SUGGESTION | **RESOLVED** | `README.md:106` → `:2726`, the shadow instance |
| R449-1 F1: same as R448-1 F1 | MAJOR | **RESOLVED** | as above; the other budget readers are rc 0 |
| R449-1 F2: split header escapes the census | MINOR | split header **resolved** (`newmod` rc 1, named); required outcome "does not depend on header layout" **RETAINED** in narrower form as F1 (attributed headers escape; the own-line form worsened against round 1) | §2 item 2 |
| R449-1 F3: bound is a mirrored literal | MINOR | **RESOLVED** | derived in condition and message; `hdr10` refuses |
| R449-1 F4: `$error`/`$warning` pass the bench | MINOR | **RESOLVED** | `%Warning-USERFATAL\|%Error` required, plus the yosys leg; `err`, `warn`, `info` and `$error` off PATH all killed |
| R449-1 R1: run.sh "status files" | RESIDUE | **RESOLVED** | `run.sh:9-10` carries the exact text |
| R449-1 R2: `sim_main.cpp:1443` | RESIDUE | **RESOLVED** | `:244-255` |
| R449-1 R3: `CODE_QUALITY.md` prose | RESIDUE | **RESOLVED** | exact text in the amended c10 (`r3_exact_text_check.txt`) |
| R449-1 S1: other module-scope `$error` guards | SUGGESTION | out of scope; owned by issue #151 (open), whose acceptance covers it | issue #151 |

## 5. Lenses

- **Conformance: UNCLEAN (F1).** #25 acceptance bullet 1 is not met for attributed headers, against `run.sh:166-185`. #17 is met: `KL_pp_nvm_port.sv:196-200` refuses above the derived bound by name. The parent adoption contract is met: gate 3 and its self-test, and every other budget reader, are rc 0 at `1269cdaf` + c8 + p2 + c10.
- **RTL: CLEAN.**
  - Artifact: `hdl/packet_engine/KL_pp_nvm_port.sv:111-113,192-200`.
  - The bound arithmetic is exact at width 16 (65527); `len17` and `hdr10` follow the field.
  - The netlists of round 1 and head, and of base and head, are identical at 1024 and 65527.
  - Lint is 41/41.
  - The guard is `%Warning-USERFATAL` in Verilator 5.050 and stops yosys at `$finish`. The guard is elaboration-only, and no port changed.
- **Robustness: UNCLEAN (F1).** `syn/yosys/run.sh` census and `parse_site`: twelve header layouts at the head, four at round 1. The parse-once loop's refactor into `elaborate_tops()` was read and replayed (28 unchanged probes identical). The bench's class grading was checked off PATH.
- **Tests: UNCLEAN (F1).** The red-proof table lacks the attributed-header case that escapes. Otherwise:
  - `elab_bounds.sh` kills 12 of 12 mutants.
  - The amended parent self-test kills six `verdict()`/`compare_tops()` mutants.
  - The nvm_port suite is 1,219/1,219.
  - R449-1's probes reproduce the PR's stated rows.
- **Docs: UNCLEAN (F1).** `run.sh:161-165` and the PR body §1 claim layout independence. That changes what a reader believes the gate catches, so it is not wording only.
  - Otherwise correct: `tb/nvm_port/README.md:20-26,106,226,407,413`, `Makefile:63-66`, `elab_bounds.sh:19-29`, `09_verification.md:348`, and the PR body's moved-citation table and Round 2 table.

## 6. Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #25 acceptance vs `run.sh:166-185` census (16 layout cases); #17 vs `KL_pp_nvm_port.sv:196-200`; parent gate 3 + self-test + six other budget readers at `1269cdaf` + c8 + p2 + amended c10 (`55e62329`); issue #151 scope | R448-2 | cd08ca7b3d962ab040d8aaa023c57e7b0e010a6d |
| RTL | CLEAN | `KL_pp_nvm_port.sv:111-113,192-200`; port netlist identity r1/base vs head at 1024 and 65527; `lint_hdl.sh` 41/41; Verilator USERFATAL and yosys `$finish` at 65528 | R448-2 | cd08ca7b3d962ab040d8aaa023c57e7b0e010a6d |
| Robustness | UNCLEAN (F1) | `run.sh` census, `parse_site`, `elaborate_tops` (28 unchanged probes + 16 census cases + parse_site unit); `elab_bounds.sh` class grading with and without sv2v/yosys | R448-2 | cd08ca7b3d962ab040d8aaa023c57e7b0e010a6d |
| Tests | UNCLEAN (F1) | 12+3 `elab_bounds.sh` mutants; 10 parent F1 probes; `make -C tb/nvm_port` 1,219/1,219; R449-1 `yosys_fault.sh newmod` and `nvm_bound_probe.sh` unchanged; PR red-proof table | R448-2 | cd08ca7b3d962ab040d8aaa023c57e7b0e010a6d |
| Docs | UNCLEAN (F1) | `run.sh:1-11,157-165`; `tb/nvm_port/README.md`, `Makefile`, `elab_bounds.sh` header; `09_verification.md:348`; every citation into `KL_pp_nvm_port.sv` (`cite_check.txt`); PR body and Round 2 table; amended `CODE_QUALITY.md` text | R448-2 | cd08ca7b3d962ab040d8aaa023c57e7b0e010a6d |

## 7. Real limits

- **`make -C tb/nvm_port figures` was not completed here.** It needs git history and runs longer than this session's 10-minute foreground limit. It was killed at 590 s in a full-history scratch clone (`receipts/nvm_suite/figures_foreground_timeout.log`). Two detached attempts were terminated by the host, and so was a history-less attempt that had printed every measured row `[ok]` before failing only its git-history pins. That attempt's log was overwritten and is not published.
  - Round 2 touches the figures only through comment and README text. The ARMS table and every citation were verified by inspection.
  - The hosted step "nvm_port README figures agree with the tree" is pending at the exact head.
- Not run, as the brief forbids full banks: `scripts/run_suites.sh`, the five campaign drivers, `make check`, and the full parent, PP, gPTP, Yosys and builder banks. Parent gates 1, 2, 6-8 and 10-16 rest on the author's report and the manager's banks.
- R449-1's other 17 `yosys_fault.sh` cases were not rerun. My own 28 round-1 probes cover the same paths and reproduce.
- No Vivado or xvlog on this host. The OOC equality and the xvlog/Synth 8-6901 counts were not reproduced in this round. Round 2 changes no hdl logic: the port netlist is identical.
- The parent's `external` submodule (private) was not checked out. None of the commands run reads it.
- Hosted `suites` was in progress at both exact-head runs when read.
- Physical calibration NOT RUN. Field skips are not hardware proof. No hardware claim is made.

## 8. Pending manager duties

1. Route F1 to the author for a new round. The fix touches `run.sh`'s census and `parse_site`, the red-proof table, and the comment and PR-body claim. Rerun `scripts/run_census_cases.sh` and the unchanged probes.
2. Confirm that both hosted `suites` jobs finish green at the exact head, including the nvm_port figures step. The manager owns hosted/act acceptance.
3. At adoption, carry the amended c10 (`55e62329`) after c8 and p2, and keep `check_rtl_source_lists.py --selftest` in the consumer set.
4. Build the final current-dev candidate at the merge turn (source base `f4167536`, live dev `bbf704ec`). This source-head review does not cover it.
5. Close PR #26 at merge; issue #151 carries R449-1 S1.

## 9. Scripts and receipts

Every published file is listed in `MANIFEST.sha256`. Absolute paths in receipts are rewritten to `<packet>`, `<scratch>`, `<clone>` and `~`.

- `scripts/`: `gate_probe.sh`, `gate_cases.txt`, `plant.py`, `oracle.sh` (unchanged from round 1), `run_gate_cases.sh`, `plant_census.py`, `census_probe.sh`, `census_cases.txt`, `run_census_cases.sh`, `parse_site_unit.sh`, `cite_check.py`, `nvm_mutants.py`, `nvm_mutant_run.sh`, `nvm_port_equiv.sh`, `parent_f1_probes.sh`.
- R449-1's scripts were run unchanged from milan-fpga `2da8e8f0:review-evidence/ppC10-r1/reviews/R449-1/scripts/` (`yosys_fault.sh` sha256 `b7eca443...`, `nvm_bound_probe.sh` `31fac658...`).
- `receipts/`:
  - `gate_probes/`, `census/`, `census_unit/`, `head_gates/`;
  - `nvm_mutants/`, `nvm_equiv/`, `nvm_yosys/`, `nvm_suite/`;
  - `r449_probes/`, `parent/`, `lint/`;
  - `cite_check.txt`, `clone_integrity.txt`, `tool_identity.txt`, `evidence_sha256_check.txt`, `hosted_*.txt`, `independent_pass_draft.md`.

R448-2 FINISHED
