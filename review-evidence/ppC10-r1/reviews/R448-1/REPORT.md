[R448] NEGATIVE - exact head 54f9411ab9a4b4aea58393f7fa1303ddcc96ee3c

# R448-1 independent internal review: PR #149 (lane C10, issues #25, #17, #37; #22 related)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head reviewed: `54f9411ab9a4b4aea58393f7fa1303ddcc96ee3c`, tree `419d056441b96802ec72c1671cc25abbd25ad4d5`
- Source base: `f4167536d358c996f4e1b70b875879c1651f85d3`. The diff is 15 files, +480/-105, ten commits including the `--no-ff` merge `5c20350` of PR #26's two commits.
- Reviewer role: internal independent reviewer, cleared context, own detached clone. The clone was verified byte-exact after the probes (`receipts/clone_integrity.txt`).

## Verdict in one paragraph

All four processor items do what the PR says, and the probes confirm it. The Yosys gate covers all 42 declared modules and refuses a missing or stale top. It parses `all.v` once and names each failing top while still giving every other top a verdict; this matches an independent per-top oracle on four planted faults. The allocator cannot mask a failure. The `MAX_PAYLOAD_P` guard refuses above 65527 and builds at 65527. The `protocol_processor_top` reorder is formally equivalent to the base, and a negative control proves the check can fail. The NSD arm kills the three PR mutants and two of mine, and the 40/40 campaign reproduces every published count. **The verdict is NEGATIVE for two reasons.** (F1, MAJOR) The published parent adoption patch `parent-adoption-c10-1269cdaf.patch` is incomplete. With c8, p2 and c10 applied at milan-fpga `1269cdaf` and this head pinned, the parent's own CI step `check_rtl_source_lists.py --selftest` fails 1 of 49. It passes 49/49 at the parent's current pin. The manager's 16-command consumer set never runs that self-test, so it does not cover the patch. (F2, MINOR) The ten-line shift in `KL_pp_nvm_port.sv` left three line citations stale, though the PR says it moved them all.

## 1. Reconstruction (in the required order)

1. **Contributor rules.** This repository has no `AGENTS.md` or `CONTRIBUTING.md` at the head. `docs/README.md` is the authors' convention page: single-source rules, ID registries, and `make check` enforcement. It was read.
2. **Frozen acceptance and scope decisions.** Issue bodies #25, #17, #22 and #37. The two maintainer corrections on #25 (5449611948 and 5449704965) establish that the tops array, not the read mode, gives elaboration coverage. The lane assignment comment 5967291597 says: items in order, each issue's own acceptance list is the bar, no logic may be added, item 3's OOC cost must be equal, and STOP on any port, parameter-meaning or behaviour change. Its gates are every processor suite, the Yosys gate with every top, and the parent consumer set (16) at `1269cdaf` with the c8 then p2 patches.
3. **Authorities.** Milan v1.2 5.4.2.15 and IEEE 1722.1-2021 7.4.23.1, as cited by #37 and in the code. 06 §6.4 sets lock precedence. The 07 §5.2 record header (8 bytes) and the `dev_len_o[15:0]` port (`KL_pp_nvm_port.sv:162`) bound the payload.
4. **Diff and history.** `git diff f4167536..54f9411` was read in full. `hdl/` changes only in `KL_pp_nvm_port.sv` (the guard plus two doc-comment lines) and `protocol_processor_top.sv` (commit `34b5246` alone). The microcode generator is unchanged, and the ROM image is byte-identical to base.
5. **Public evidence.** `kebag-logic/milan-fpga@2a54253e/review-evidence/ppC10-r1` holds author material only: HANDOFF, PR-BODY and three adoption patches. All five SHA-256 values match the published manifest (`receipts/evidence_sha256_check.txt`), and PR-BODY.md equals the live PR body. The issue and PR carry no manager evidence comments beyond the two review-start notices. The manager's source-bank receipts named in the assignment are not in that directory; see Limits.

**Prior public review findings on PR #149:** there are none to resolve. The PR has 0 reviews, 0 inline comments, and only the two `INDEPENDENT REVIEW STARTED` comments, checked after this pass.

## 2. Item-by-item evidence

### Item 1 (#25): every module is a top, the census, parse-once, attribution, allocator, timing

| Claim | Evidence (receipt) | Result |
|---|---|---|
| 42 declared modules = 42 tops; the census refuses missing and stale | `gate_probes/h-drop-srp_top.log` (rc 1, names `KL_srp_top`); `h-add-bogus.log` (rc 1, "no longer exist") | holds |
| parsed once, green | `timing/head-r1.log`: `YOSYS 42 tops, all.v parsed 1 time(s)`, 42 OK, `YOSYS XILINX OK` | holds |
| RAMB36 regression unchanged and passing | `syn/yosys/run.sh:274` byte-identical to base; `YOSYS XILINX OK KL_aecp_engine` in every green run and in both hosted portability jobs | holds |
| PR planted-fault table, replayed in base and head | `gate_probes/{b,h}-*.log`, `scripts/gate_cases.txt`. Base misses `KL_srp_top`, `protocol_processor_top`, `KL_acmp_nvm_shadow`, `KL_mrp_strip` and `KL_srp_admission` (rc 0) and catches `KL_pp_dispatch_fifo` through its parent; head goes red on each and names it | every rc and every named top matches the PR table |
| two faults; syntax fault in `all.v` | `h-two.log`: 4 tops named, `parsed 4 time(s)`. `h-allv-syntax.log`: `YOSYS FAIL all.v in module KL_srp_top`, 42 not elaborated | holds |
| **own faults, in modules the table does not list** | `h-own-prng.log` (unresolved instance in `KL_pp_prng`), `h-own-fatal-rx_slots.log` (elaboration `$fatal` in `KL_pp_rx_slots`), `h-own-badport-timer.log` (bad port in `KL_pp_timer_service`, refused earlier by sv2v, rc 1) | red, each top named, the other 40 tops still get OK |
| a red gate still gives every top a verdict | every red elaboration probe has OK + FAIL = 42 per-top lines | holds |
| attribution is correct | `gate_probes/oracle-*.txt`: the pre-PR one-yosys-per-top method over the same planted trees gives the same failing set for prng, srp_admission and two-fault. For the `$fatal` fault the pre-PR method fails all 42, because a plain read elaborates every module at read time. A per-top `-defer` oracle gives exactly the gate's two tops | gate = oracle |
| the allocator cannot mask a failure | the prng fault gives identical verdicts under default jemalloc, explicit jemalloc and `YOSYS_MALLOC=none`; an inherited `LD_PRELOAD` is unset when `none` (`h-inherited-preload-none.log`); a missing or non-ELF `YOSYS_MALLOC` gives rc 2 before any work; `--selftest-alloc` PASS. A fake `yosys` that exits 0 silently yields rc 1 with all 42 tops `not elaborated` (`h-fake-yosys-exit0.log`): verdicts need yosys's own `@@ok` markers | holds |
| wall time measured on one host | `timing/times.tsv`, two rounds each, alone: head 35.63/35.58 s, `none` 55.35/47.62 s, base 88.80/98.01 s. PR: 35.97 / 48.12 / 88.80 (median of 3) | reproduced in scale; the verdict lines are identical across allocators |
| hosted | `hosted_portability_{pr,push}_yosys_lines.txt`: Yosys 0.33 on the hosted runner, 42 OK, parsed once, XILINX OK | executed and green |

### Item 2 (#17): `MAX_PAYLOAD_P` guard

- `KL_pp_nvm_port.sv:197-200` is a module-scope `if (MAX_PAYLOAD_P > 65527) ... $fatal(1, "... is above 65527 ...")`. With the pinned Verilator 5.050 (identity in `receipts/verilator_identity.txt`), `elab_bounds.sh` gives rc 0: 1024 and 65527 build clean under `-Wall`; 65528, 65535 and 2^32-1 are refused by name and bound (`nvm_port/elab_bounds.log`). sv2v + Yosys also accept 65527 and refuse 65528 (`nvm_port/yosys_maxp.txt`).
- All five PR mutants turn the gate red: guard deleted, bound 65528, `>=`, message without the bound, `initial` placement (`nvm_port/elab_mutants.txt`).
- No logic was added: Yosys equivalence of `KL_pp_nvm_port`, base vs head, is proven at `MAX_PAYLOAD_P` = 1024 and 65527 (291/291 `$equiv`, `nvm_port/nvm_port_equiv.txt`).
- On "derived from the field width, not mirrored": the **value** is the field-width consequence. 65527 = 2^16 - 1 - `HDR_LEN_C`(8), the comment at `:112-113` and the message state the derivation, and both edges are graded. The **expression**, however, is a literal mirror, not computed from `$bits(dev_len_o)` and `HDR_LEN_C`. Issue #17's acceptance does not require derivation, and the codebase's guards use literal bounds (`KL_aecp_desc_store.sv:260`, `KL_pp_nvm_port.sv:188`). So this is recorded as suggestion S1, not as a defect.

### Item 3 (#22): declaration reorder

- `34b5246` touches only `protocol_processor_top.sv`. The sorted multiset of non-blank lines differs from base by exactly one added comment line (`reorder/sorted_nonblank_lines.diff`).
- **Formal equivalence**, Yosys, `scripts/reorder_equiv.sh`. Base and head `protocol_processor_top` are elaborated from the sv2v output. All 33 submodule instances (27 parameterized and 6 plain; the top holds no memory cells) are cut out: 599 submodule-output nets become free inputs, and 390 submodule-input nets become compared outputs. Seven expression-valued connections are first given shared public names. Then `equiv_make; equiv_simple; equiv_induct`. **Result: 13,957 `$equiv`, all proven** (`reorder/pos5.result`).
- **Negative controls**, so the check is not vacuous. One constant changed in a top-level assign is caught (`neg5.result`, `hz_aem_cmd_w` unproven), and one constant changed inside a submodule-input expression is caught (`neg25.result`). A first black-box-only formulation was found unsound (undriven black-box outputs) and was discarded; the receipts are from the sound formulation. `reorder/reorder_equiv_repro.txt` re-ran it from scratch: proven, then caught, then caught.
- Per-type cell counts of the unflattened top match (`unflattened_top_stat.diff`: header lines only).
- Use-before-declaration, by a textual scan (`scripts/ubd_scan.py`, `reorder/ubd_{base,head}.txt`): 60 at base and 17 at head. Exactly 43 identifiers were resolved, matching the commit message, and none were introduced. The 17 left are all inside instance port-connection lists, which the published xvlog evidence shows Vivado accepts. xvlog itself could not be run here (Limits).
- The pinned-Verilator `lint_hdl.sh` gives rc 0, 41/41 (`lint/lint_hdl.log`).

### Item 4 (#37): SET_CLOCK_SOURCE NO_SUCH_DESCRIPTOR arm

- **Conformance.** A SET_CLOCK_SOURCE naming a CLOCK_DOMAIN the entity lacks must answer NO_SUCH_DESCRIPTOR (status 2) with the response form (cdl 20), and must store, mark and notify nothing (IEEE 1722.1-2021 7.4.23.1; Milan v1.2 5.4.2.15). Under a foreign lock, ENTITY_LOCKED outranks the locate miss (06 §6.4, unchanged since #53). NSD1 to NSD3 (`tb/pp_top/sim_main.cpp:11538-11562`) grade exactly that, byte-exact, at the effect strobes and at a second registered controller. NSD0 deliberately leaves r6 = 2, so a dropped preload is visible. The arm adds 13 checks; AX is 231 in both the default and line builds (`dispatch/out/control-aecp-*.log`).
- **Campaign**, pinned Verilator, `--jobs 4`: 4 controls PASS and **40/40 KILLED** (`dispatch/campaign.log`, `results.json`, rc 0). All 40 failure counts equal the README table (`dispatch/readme_count_compare.txt`). The one moved count, `lk-sclks-miss-lock-nop` 1 to 2, is justified: removing E_SCLKSRF's CHECK_LOCK lets both LK4 and the new NSD3 answer NO_SUCH_DESCRIPTOR.
- **Own mutants** (`dispatch_own/`). The miss branch aimed at E_SCLKSRF − 1 survives with 928/928 checks, confirming the PR's "measured equivalent". The refusal tail carrying r12 (the requested index) in place of r6 is KILLED, failing NSD1 and NSD3 among 6 checks. The r6 preload changed to 1 is KILLED (NSD1, NSD3, LK4, LK5).

### Parent adoption (c10 patch)

- c8, then p2, then c10 each pass `git apply --check` and apply cleanly at `1269cdaf`. c10 changes only `scripts/processor_yosys_tops.budget` (deletes the six drift lines and rewords the header) and `scripts/xvlog.budget` (drops the `protocol_processor_top.sv` finding and refreshes three line annotations, which match the head sources).
- Gate 3 (`check_rtl_source_lists.py`) with this head pinned: rc 1 with c8+p2 (six STALE RECORDs, as the PR says) and rc 0 with c10 (`42/42 tops, 0 recorded`).
- **Its `--selftest`, run by the parent's CI right after it (`.github/workflows/docs.yml:263-264`), fails 1 of 49 with c10.** The failing check is "the record is non-empty at this pin" (`scripts/check_rtl_source_lists_selftest.py:378`). At pristine `1269cdaf` with its own pin `631eeb34`, both pass (49/49). See F1.
- Gate 9 (`xvlog_gate.py`) needs Vivado and was not run (Limits).

## 3. Findings

### F1: MAJOR. The parent adoption patch empties the tops budget, and the parent's CI self-test then fails

- **Lenses:** Conformance, Tests, Docs
- **Where:** `review-evidence/ppC10-r1/author/parent-adoption-c10-1269cdaf.patch` (sha256 `6870d2ed…`); the PR body's "Parent consumer set" table (row 3) and "Parent-visible list" item 2. In milan-fpga: `scripts/check_rtl_source_lists_selftest.py:376-379`, run by `.github/workflows/docs.yml:264`.
- **Authority/evidence:** the lane gate is the parent consumer set at `1269cdaf` with c8 then p2. The parent's own CI runs `check_rtl_source_lists.py --selftest` in the same step as gate 3. Receipts: `receipts/parent/gate3_selftest_c8_p2_c10.log` shows `49 checks: 48 PASS, 1 FAIL` with `[FAIL] the record is non-empty at this pin...`. `receipts/parent/gate3_selftest_baseline_1269cdaf_pin631eeb34.log` shows `49 checks: 49 PASS`. Summary: `receipts/parent/apply_and_gate3_summary.txt`.
- **Impact:** adopting this head with the stated patches turns the parent's "RTL source-list drift gate" CI step red. The PR says c10 is what adoption needs and reports gate 3 rc 0, but the 16-command consumer set never runs that self-test, so it does not cover the file the patch changes.
- **Required outcome:** the adoption bookkeeping must leave the parent's gate-3 self-test green with c8, p2 and c10 at `1269cdaf`. For example, the patch also retires or rewrites the "record is non-empty" arm now that the debt is paid, grading the stale and unrecorded arms on a synthetic population instead. The PR's parent-visible list then names that change, and the manager adds `check_rtl_source_lists.py --selftest` to the consumer set for this adoption.
- **Verification:** at `1269cdaf` with c8, p2 and the amended c10, and the processor at the head, `python3 scripts/check_rtl_source_lists.py` and `python3 scripts/check_rtl_source_lists.py --selftest` both give rc 0.

### F2: MINOR. Three line citations into `KL_pp_nvm_port.sv` went stale in the ten-line shift

- **Lenses:** Docs, Tests
- **Where:**
  - `tb/nvm_port/sim_main.cpp:1443` cites `:234-245` for `dev_cmd_owned_w`, now at `:244-255`. That range now lands on the header-validation view.
  - `tb/nvm_port/README.md:403` cites `` `:366` `` for the transition into `S_WEREQ`, now at `:376`.
  - `tb/nvm_port/README.md:409` cites `` `:380` `` for what `S_WEREQ` transitions to, now at `:390`.
- **Authority/evidence:** each citation was correct at base. At base, lines 234-245, 366 and 380 hold exactly the cited code, and the head equivalents are 244-255, 376 and 390. Commit `54f9411` and the PR body say the shift's line citations were moved ("the three line ranges cited in comments"). Four were moved; these three were missed. The `sim_main.cpp` one sits two lines below a citation the commit did update.
- **Impact:** a reader following the citations lands on the wrong code, and the PR's statement that the citations were moved is incomplete. These cross-references point at code rather than being pure wording, so under the owner rule they are MINOR.
- **Required outcome:** `:234-245` becomes `:244-255`, `` `:366` `` becomes `` `:376` ``, and `` `:380` `` becomes `` `:390` ``. The PR body's sentence about moved citations states the full set.
- **Verification:** `sed -n '244,255p;376p;390p' hdl/packet_engine/KL_pp_nvm_port.sv` shows `dev_cmd_owned_w`'s window, `state_r <= S_WEREQ;` and `state_r <= S_WEWAIT;`. `grep -n ':234-245\|`:366`\|`:380`' tb/nvm_port/` finds nothing.

### S1: SUGGESTION. Compute the payload bound instead of mirroring it

- **Lenses:** RTL, Robustness
- **Where:** `hdl/packet_engine/KL_pp_nvm_port.sv:197-198`
- **Rationale:** `65527` appears in the guard and in the message as a literal. A `localparam int unsigned MAXP_MAX_C = (1 << $bits(dev_len_o)) - 1 - HDR_LEN_C;`, used in the condition and printed with `%0d`, would keep `elab_bounds.sh`'s text and stay correct if the header or port width ever changed. Both are frozen today, so this is not a defect.
- **Verification:** `elab_bounds.sh` still rc 0, and the guard equivalence still holds.

### S2: SUGGESTION. A pre-existing stale citation in a file this PR edits

- **Lenses:** Docs
- **Where:** `tb/nvm_port/README.md:102` cites `protocol_processor_top.sv:2714` for the shadow instance.
- **Rationale:** the instance is at 2725 at base and 2726 at head. This was already wrong before the PR, so it is not counted against the PR. Fix it alongside F2.

## 4. Lenses: artifact-specific evidence

- **Conformance (UNCLEAN, F1).** Checked: #37 against IEEE 1722.1-2021 7.4.23.1, Milan v1.2 5.4.2.15 and 06 §6.4 (status 2, cdl 20, zero body, the lock first); #17 acceptance (refusal above 65527 naming the bound, `$fatal(1, …)`); #25 acceptance (all five items); the lane rules (no port, parameter-meaning or behaviour change: equivalence proven; ROM image unchanged). Failed: the parent adoption contract (F1).
- **RTL (CLEAN).** `KL_pp_nvm_port.sv` adds only a generate-if `$fatal`, and the netlist is equivalent at 1024 and 65527. `protocol_processor_top.sv` is a pure move, formally equivalent with negative controls. No ports changed (equivalence matched every port and exposed connection by name), and the per-type cell counts are equal. S1 is advisory only.
- **Robustness (CLEAN).** `syn/yosys/run.sh`: census in both directions; parse failure, elaboration failure, multi-fault, silent fake yosys, non-zero exit after all OK (code path read), allocator refusals and inherited `LD_PRELOAD` all probed; `set -euo pipefail` interplay read. `elab_bounds.sh`: legal and illegal edges plus five mutants.
- **Tests (UNCLEAN, F1, F2).** The NSD arm is defect-sensitive (3 PR mutants and 2 own mutants killed; one equivalent mutant confirmed). The campaign is 40/40 with counts matching the README. The gate fault table was replayed and extended. The consumer-set coverage gap (F1) and a stale citation in test source (F2) leave the lens unclean.
- **Docs (UNCLEAN, F1, F2).** Read: the 09 §8.1 clock_source row and the new §8.6 row; `tb/pp_top/README.md` NSD prose and table; `tb/nvm_port/README.md` and Makefile comments; `run.sh` comments (wall-time figures reproduced); the PR body against measurements. Defects: the PR's parent-visible claim (F1) and stale citations (F2).

## 5. Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | issues #25/#17/#22/#37 acceptance and scope comments; `gen_ucode.py` E_SCLKS/E_SCLKSRF; `sim_main.cpp` AX NSD; c8/p2/c10 patches at milan-fpga `1269cdaf`; parent gate 3 and its self-test | R448-1 | 54f9411ab9a4b4aea58393f7fa1303ddcc96ee3c |
| RTL | CLEAN | `KL_pp_nvm_port.sv` guard and nvm_port equivalence (1024, 65527); `protocol_processor_top.sv` reorder, formal equivalence with negative controls, cell stats; ROM image unchanged; pinned-Verilator lint 41/41 | R448-1 | 54f9411ab9a4b4aea58393f7fa1303ddcc96ee3c |
| Robustness | CLEAN | `syn/yosys/run.sh` census, attribution, re-parse loop and allocator (24 probes + fake yosys + selftest); `elab_bounds.sh` edges and 5 mutants | R448-1 | 54f9411ab9a4b4aea58393f7fa1303ddcc96ee3c |
| Tests | UNCLEAN (F1, F2) | dispatch campaign 44/44 (40 KILLED); own 3 arms; README count comparison; gate fault table plus per-top oracle; consumer-set coverage; `tb/nvm_port/sim_main.cpp` citations | R448-1 | 54f9411ab9a4b4aea58393f7fa1303ddcc96ee3c |
| Docs | UNCLEAN (F1, F2) | 09 §8.1/§8.6; `tb/pp_top/README.md`; `tb/nvm_port/README.md`, Makefile, `measure_figures.py` ARMS (12/12 lines verified); `run.sh` comments; PR body vs measurements | R448-1 | 54f9411ab9a4b4aea58393f7fa1303ddcc96ee3c |

## 6. Real limits

- **No Vivado or xvlog on this host.** The PR's xvlog result (37 to 38 of 41), `Synth 8-6901` 51 to 7, the byte-identical OOC netlist and the utilization table, and parent gate 9 (`xvlog_gate.py`) were not reproduced. They are corroborated only by the Yosys formal equivalence and the textual forward-use scan.
- **Not run (the brief forbids full banks):** the full `scripts/run_suites.sh` and parent banks. The 1,020,253-check total and `tb/pp_top`'s 9,222 rest on the author's report, partly corroborated: the AX tally is 231 in both builds, and the 13-check arithmetic was confirmed from source.
- The `make -C tb/nvm_port figures` (160 builds) and `make check` gates were not run locally. The ARMS line table and the moved citations were verified by inspection, and the hosted `docs-gates` job ran and passed at the head.
- Parent gates other than gate 3 and its self-test were not run. Gates 1, 2 and 4 to 16 rest on the author's report.
- The manager source-bank receipts named in the assignment were not present in `review-evidence/ppC10-r1` (author material only). They were not independently inspected.
- Hosted CI at the head: `docs-gates` and `portability` completed **success** in both the push run (37120641243) and the PR run (37120643855). Both `suites` jobs were still **in progress** at 12:29 UTC (`receipts/hosted_checks_54f9411.txt`). Hosted CI is therefore not yet shown green.
- Physical calibration was not run, and field skips are not hardware proof. This review makes no hardware claim.

## 7. Pending manager duties

1. F1: carry the parent-side fix (amended c10 or an equivalent parent change), add `check_rtl_source_lists.py --selftest` to the consumer set for this adoption, and re-run it.
2. F2: route the three citation fixes, plus S2 if accepted, to the author.
3. Confirm both hosted `suites` jobs finish green at the exact head before acceptance. The manager owns hosted and act acceptance.
4. Vivado-side confirmation (xvlog over every module, `KL_pp_shadow` `Synth 8-6901` count, OOC equality) and parent gate 9 at the merge turn.
5. Build the final current-dev candidate at the merge turn (source base `f4167536`, live dev `bbf704ec`). This source-head review does not cover it.
6. Close PR #26 at merge, as the lane assignment states.

## 8. Receipts and scripts (paths relative to this packet; all listed in MANIFEST.sha256)

- `scripts/`: `time_gate.sh`, `plant.py`, `gate_probe.sh`, `gate_cases.txt`, `oracle.sh`, `reorder_equiv.sh`, `ubd_scan.py`
- `receipts/timing/`: gate timings and logs
- `receipts/gate_probes/`: fault probes, oracle outputs, fake-yosys probe
- `receipts/dispatch/`: the 40-arm campaign, logs, `results.json`, README count comparison
- `receipts/dispatch_own/`: three reviewer arms, their patches and logs
- `receipts/nvm_port/`: `elab_bounds`, guard mutants, Yosys bound probe, nvm_port equivalence
- `receipts/reorder/`: line multiset, formal-equivalence scripts and results, negative-control diffs, forward-use scans, a reproduction run
- `receipts/lint/`, `receipts/selftest_alloc.log`, `receipts/verilator_identity.txt`
- `receipts/parent/`: gate 3 and self-test logs (baseline, c8+p2, c8+p2+c10), the c10 patch, summary
- `receipts/hosted_checks_54f9411.txt`, `receipts/hosted_portability_*_yosys_lines.txt`, `receipts/evidence_sha256_check.txt`, `receipts/clone_integrity.txt`

R448-1 FINISHED
