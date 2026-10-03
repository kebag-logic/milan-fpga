[R448] NEGATIVE - exact head 39298e03aa53d5f82c7485b8d12d2b69a47b0d55

# R448-3: independent internal review of PR #149 (lane C10; issues #25, #17, #37; #22 related), rounds 3 and 3b

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #149.
- Exact head: `39298e03aa53d5f82c7485b8d12d2b69a47b0d55`, tree `7f3b4639ee70ad34c567f4df4cc9fec4c8172780`. It is a `--no-ff` merge whose parents are `b6f17f2` (round 3) and `main` `c4cb84ff` (PR #150, lane P1).
- Source base: `f4167536d358c996f4e1b70b875879c1651f85d3`. This review covers the delta `cd08ca7b..39298e03`:
  - round 3, `b6f17f2`, which changes only `syn/yosys/run.sh`;
  - round 3b, the merge.
- Review start: PR #149 comment 5973159947. Assignments: issue #25 comments 5970977905 (round 3) and 5972322274 (round 3b).
- Role: internal independent reviewer, cleared context, own detached clone. After the probes the clone is byte-exact (`receipts/clone_integrity.txt`).

## Verdict

**NEGATIVE, on one open MINOR finding (F1, Docs).** The code, the tests and the merge are sound. Every acceptance item I re-ran holds at this head.

- **Round 3.** The census now uses yosys's own module list. It resolves R448-2 F1 and R449-2 F1 fully. Every round-2 probe I re-ran unchanged gives the outcome those findings required, and the unchanged rows match round 2 row for row.
- **Round 3b.** The merge keeps both sides whole. Its one conflict is resolved with re-derived citations, and the ROMs are byte-identical across base, both parents and the merge.
  - At the merge: the suite total equals the PR's figure, the Yosys gate is green with 42 tops, and every campaign I ran matches its record.
  - The parent consumer gates are rc 0 at `1269cdaf` + c8 + p2-p1 + c10.
- **F1.** The PR body's §1 red-proof table labels its result column "this head", but two of its quoted yosys error excerpts carry `all.v` line numbers from before the round-3b merge. At this head the same plants report the line 110 higher. That is a figure attributed to a revision that does not produce it. Under the owner rule it is not wording only, so it is MINOR. The fix is small: re-quote the two line numbers at the merge, or label the column with the revision they were measured at.

## 1. Reconstruction

1. **Contributor rules.** The processor has no `AGENTS.md` or `CONTRIBUTING.md`. I read the parent's (milan-fpga `1269cdaf`): AGENTS.md §2, §3 and §6 (reading order, lens tokens, severities). I read the processor's `docs/README.md` for conventions.
2. **Frozen scope.** I read issue #25's body and acceptance, the two maintainer corrections (5449611948, 5449704965), the lane assignment (5967291597), and the round-2, round-3 and round-3b assignments (5969440297, 5970977905, 5972322274). I read the acceptance of #17 and #37 for the conformance lens.
3. **Authorities.**
   - #25: bullet 1, every declared module is a top and a check fails otherwise; bullet 2, red on a broken new top; bullet 3, a failure names its module; bullet 4, the RAMB36E1 assertion is unchanged.
   - #17: refuse `MAX_PAYLOAD_P` above the bound, with a `$fatal` naming it.
   - #37: the NO_SUCH_DESCRIPTOR arm, killed by a one-word branch move.
   - Round 3b: keep both sides, re-derive every line citation at the merge, ROMs identical, re-measure at the merge.
4. **Diff and history.**
   - `git diff f4167536..39298e03` (33 files);
   - `cd08ca7..b6f17f2` (run.sh only);
   - the merge, re-run with `git merge-tree b6f17f2 c4cb84f` and compared against the committed tree.
5. **Public evidence.**
   - milan-fpga `2a54253e:review-evidence/ppC10-r1` (round 1).
   - The later archive `d2222115` on `ppC10-review-evidence` (`author-r2/`, `author-r3/`).
   - P1's `parent-adoption-p2-p1-1269cdaf.patch` from `ppP1-review-evidence` `c7675469`.
   - Every fetched file's sha256 equals its MANIFEST.json entry (`receipts/evidence_sha256_check.txt`). No manager bank receipts are published there, so the manager's static, builder and native passes are taken as stated in the review start.

I read the prior public findings (R448-2, R449-2) only after my own pass over the diff and the round-3 mechanism. Section 4 judges each of them.

## 2. Evidence

### Round 3: the census is yosys's own list (`syn/yosys/run.sh:157-188, 235-242, 249-260, 269-271`)

The mechanism, as read:

- The one elaboration run writes `tee -q -o declared.txt select -list =*` right after `read_verilog -defer all.v` (`:237`).
- `census()` takes the `$abstract\NAME` lines (`:171-172`). It runs once, on the first run's list, and only after that run's first `@@begin`, so only after a successful parse (`:271`).
- A failed parse is named by `parse_site()`, which reads past attribute instances and a lifetime keyword (`:253-259`).

My round-2 probes, re-run unchanged (scripts byte-identical to round 2; `receipts/probe_script_identity.txt`):

| Probe | Result at this head | Required (5970977905) |
|---|---|---|
| `run_census_cases.sh`, `c-attr-same` / `c-attr-own` | rc 1, the census names `KL_r448_attrs` / `KL_r448_attro` (round 2: rc 0) | rc 1, named |
| `c-attr-own-top-clean` | rc 0: 43 OK, `parsed 1 time(s)`, XILINX OK (round 2: rc 1, "no longer exist") | rc 0 |
| `c-attr-own-top` | rc 1, `YOSYS FAIL KL_r448_attro: ERROR: Module \r448_absent_module referenced ...` | rc 1, `YOSYS FAIL` |
| the other 12 rows (head and round-1 trees) | every rc equal to round 2. `c-auto-split` now names `KL_r448_auto` through the parse failure; `c-ifdef` is rc 0, the stated scope | unchanged |
| `parse_site_unit.sh` | `KL_first`, `KL_auto`, `KL_attr` (round 2: `automatic` twice). The same under `gawk --posix` | names `KL_auto`, `KL_attr` |
| R449-2 `census_probe.sh`, 12 forms (split, auto, cmtblock, cmtline, macro, attr, attrline; split, auto, attr and attrline in `tops`; allvauto) | every form rc 1 and named. `attr top` gives `YOSYS FAIL KL_r449_attr`; `allvauto` gives `YOSYS FAIL all.v in module KL_r449_allvauto` | every form passes |
| R449-2's 21 `yosys_fault.sh` cases (`jobs.txt` unchanged) | every rc and every verdict line equal to R449-2's receipts, modulo `all.v` line numbers | unchanged |
| my 24 round-2 gate cases (`run_gate_cases.sh`) | every rc equal. Verdict lines are equal except an `all.v` line number (+110, the merge) and a redacted path | reproduce |

My own probes of the new mechanism (`scripts/r3_probe.sh`, `receipts/r3_probes/`):

- `(* blackbox *)` and `(* whitebox *)` modules are named by the census (rc 1), and pass in `tops` (rc 0). A faulty blackbox is also named.
- `module static` with the name split is named through the parse failure.
- An escaped identifier (`module \KL_r448_esc+`) is named by the census.
- The first top failing elaboration, plus an uncovered module: the census still fires on run 1's list (rc 1, names `KL_r448_plain`).
- Mutants of the round-3 change are each killed by a probe above:
  - `select -list *`: the blackbox is missed (rc 0);
  - `ls`: rc 1, all stale;
  - the census call removed: the attributed fault passes (rc 0);
  - the list line removed: rc 1, "listed no module";
  - the sed pattern broken: rc 1;
  - the census run on a failed parse: the parse failure loses its module name.
- An unsupported list option fails safe: rc 1, reported as a parse failure (S2).
- The clean gate at this head (`receipts/runs/gate-head-jemalloc.log`) gives `yosys allocator: /usr/lib/libjemalloc.so.2`, 42 `YOSYS OK`, `YOSYS 42 tops, all.v parsed 1 time(s)` and `YOSYS XILINX OK  KL_aecp_engine` (the RAMB36E1 assertion is unchanged, at `run.sh:304`), in 38.3 s with a peak RSS of 0.8 GB. With `YOSYS_MALLOC=none`: identical verdict lines, 64.2 s on a loaded host. `--selftest-alloc`: PASS.
- Hosted, read only, at the exact head: both `portability` jobs succeeded on Ubuntu's yosys 0.33-5build2, with 42 OK, parsed once and XILINX OK (`receipts/hosted/`). This executes the `select -list =*` census on 0.33.

### Round 3b: the merge

- **Both sides kept** (`receipts/merge_sides.txt`). For each of the 33 changed files I compared the multiset of added and removed lines. The lane's delta (`f4167536..b6f17f2`) equals the merge's delta against `main`, and P1's delta (`f4167536..c4cb84f`) equals the merge's delta against `b6f17f2`. The one exception is `tb/nvm_port/README.md`.
- **The one conflict.** `git merge-tree` reproduces the merge with exactly one conflict, in `tb/nvm_port/README.md:102-108`. The committed tree differs from that auto-merge only there.
  - `KL_aecp_nvm_writer.sv:549-552` is `frame_ok_w`'s declaration and assign.
  - `protocol_processor_top.sv:2731` is `KL_acmp_nvm_shadow #(`.
  - Both were re-derived correctly.
- **Citations** (`scripts/cite_drift.py`, `receipts/cite_drift.txt`). Every `path:N` citation into a file changed on either side was checked against the text it named on the side it came from. Only `README.md:106` moved, and it is correct.
  - I also checked the bare citations by inspection: `README.md:102-104`, `:226`, `:407`, `:413`, `:1138`; `sim_main.cpp:1328`, `:1441`, `:1443`, `:1591`; `measure_figures.py:117`; and the PR body's `KL_pp_nvm_port.sv:196-200` and `KL_pp_acmp_listener.sv:344-347`. The three #22 sites (`KL_aecp_notify.sv:557`, `KL_pp_originator.sv:194`, `KL_pp_rx_validator.sv:383`) are also correct.
- **ROMs** (`scripts/rom_regen.sh`, `receipts/rom_regen.txt`). I regenerated `ucode.hex`, `ltn_rom.hex`, and both descriptor images with their maps, at `f4167536`, `b6f17f2`, `c4cb84ff` and the merge. All six are byte-identical at all four revisions.
- **Every processor suite at the merge** (pinned Verilator 5.050, from a `git archive` of the head; `receipts/suites/`): 33 suites, all rc 0, **1,021,449 checks** (`suite_tallies.txt`), equal to the PR's figure.
  - `tb/pp_top` has 10,416 checks.
  - The `run_suites.sh` preflights `check_upc_map.py` and `check_m9_opcodes.py` (with its self-test) are rc 0.
  - `lint_hdl.sh` is rc 0, `make check` is rc 0 (1,114 links, 94 rows, 0 untested), and `gen_matrix.py --check` is rc 0.
- **`elab_bounds.sh`** (in `make -C tb/nvm_port`): 4 ELAB OK and 6 GUARD OK (`MAX_PAYLOAD_P` 65528, 65535 and 2^32-1 are refused as `%Warning-USERFATAL`). The yosys leg reports "65527 elaborates, 65528 stops at the guard's $finish".
- **`tb/pp_top` campaigns at the merge** (`receipts/campaigns/`):
  - `aecp_dispatch_mutants.py`, full: 4 controls PASS and 40 of 40 KILLED. Every arm's failing-check count equals its README record (`readme_count_compare.txt`).
  - This lane's three NSD arms were also run alone. Their failing checks are exactly those in the PR table (NSD3+LK4, NSD1+NSD3, NSD1+LK5). The `aecp-dispatch` control still totals 928 checks.
  - `d3_mutants.py`, P1's added arms (D3N's 11, D3KR's 2, D3V's 3, the 7 unrestorable): 4 goldens PASS and 23 of 23 KILLED.
  - `name_wr_mutant.py`: golden and restored PASS, the mutant killed.
  - `notify_mutants.py`, full: goldens PASS and 40 of 40 KILLED.
- **Parent consumers** at milan-fpga `1269cdaf` + c8 (`aa5a88eb`) + p2-p1 (`d3034e89`) + c10 (`55e62329`), processor gitlink `39298e03` (`receipts/parent/`):
  - Setup: a `git archive` of dev, with 984 index entries and a tree equal to dev's. Submodules: gptp `5dce647a` and verilog-axis `48ff7a7e`. Each patch was applied after a clean `--check`.
  - Gates 1-8, 11 and 17, plus `check_sh_idiom`, `check_todo_ownership`, `check_hygiene` and `measure_fail_fast` with their self-tests, and `check_entity_shape --self-test`: all rc 0.
  - Gate 3: `protocol-processor 42/42 tops, 0 recorded`; its self-test 50/50.
  - Gate 5: 1,759 processor ports.
  - Control without c10: gate 3 is rc 1 (STALE RECORD) and its self-test 47/49.

## 3. Findings

### F1: MINOR. Docs. The red-proof table's "this head" column quotes pre-merge `all.v` line numbers

- **Where:** PR #149 body, §1 "Red on a broken new top, naming it", column "this head". Two rows:
  - "a syntax fault planted in `all.v` inside `KL_srp_top`" quotes `all.v:20318`;
  - "`module automatic` with the name on the next line" quotes `all.v:20749`.
  - The table is `author-r3/PR-BODY.md` lines 61 and 69 in the public archive.
- **Authority and evidence:**
  - Round-3b assignment 5972322274 item 2: re-measure at the merge commit. AGENTS.md §6 Docs lens: "The PR and Issue contain enough evidence for another cold reviewer".
  - `receipts/line_shift/`: R448-2's unchanged `c-auto-split` case gives `YOSYS FAIL all.v in module KL_r448_auto: all.v:20749` on a `b6f17f2` tree, and `all.v:20859` at this head.
  - The `all.v` syntax plant moves the same way: `receipts/gate_probes/h-allv-syntax` is `all.v:20441` at this head against `all.v:20331` at `cd08ca7`. The reason is that P1's `hdl/aecp` lines precede both modules in `all.v`.
  - The Round 3b section re-measures the gates but not this table, and nothing in §1 says the excerpts predate the merge. The Validation table, by contrast, does say "at `b6f17f2`".
- **Impact:** a reader re-running the red proof at the stated head gets different numbers in two quoted results and cannot tell a stale excerpt from a changed outcome. The rc values and the named modules do reproduce.
- **Why MINOR, not RESIDUE:** the defect is a measured figure attributed to a revision that does not produce it. The owner rule excludes figures from RESIDUE, and a doubtful case is MINOR.
- **Required outcome:** either quote the merge's line numbers for those rows (`all.v:20859` for the `module automatic` row; the syntax row as re-measured with the author's own plant), or state against those rows, or in the column header, the revision the excerpts were measured at (`b6f17f2`), noting that `all.v` line numbers move with the merge.
- **Verification:** re-run `scripts/r448-2/run_census_cases.sh` (row `c-auto-split`) at the new head, and compare its `all.v:N` with the body.

### S1: SUGGESTION. Robustness, Docs. The stale-entry message predates the scope change (`syn/yosys/run.sh:184`)

"tops array names modules that no longer exist under hdl/" now also fires for a module that exists under `hdl/` but sits in an inactive `` `ifdef `` (sv2v drops it, so yosys never lists it). The comment at `:166-167` and the PR body state that scope. The message could say "names modules that yosys did not parse from all.v (removed, or in an inactive `ifdef`)".

### S2: SUGGESTION. Robustness. A yosys that rejects the list command is reported as a parse failure (`run.sh:281-285`)

With the list option replaced by an unknown one (`receipts/r3_probes/m-list-cmd-unsupported.log`), the gate is red, which is safe. But it prints `YOSYS FAIL all.v: ERROR: Unknown option ...` and "not elaborated, the parse failed" for every top. Both yosys versions in use support `select -list =*` (local 0.66, hosted 0.33), so this matters only on a future or older yosys.

## 4. Prior public findings at this head

| Finding | Severity | Status at `39298e03` | Evidence |
|---|---|---|---|
| R448-2 F1: an attributed header escapes the census; `parse_site` misnames `automatic` and attributed headers | MINOR | **RESOLVED** | all five required outcomes hold. `c-attr-same`/`-own` rc 1, named; `c-attr-own-top-clean` rc 0; `c-attr-own-top` `YOSYS FAIL KL_r448_attro`; `parse_site_unit` names `KL_auto`, `KL_attr`; the attributed rows are in the red-proof table; the scope, including `` `ifdef ``, is stated at `run.sh:161-168` and in the PR body. Every other row is unchanged |
| R449-2 F1: the same class (attributed headers; `allvauto` misnamed) | MINOR | **RESOLVED** | every `census_probe.sh` form rc 1, named (`attr top` gives `YOSYS FAIL KL_r449_attr`; `allvauto` names `KL_r449_allvauto`); the 21 `yosys_fault.sh` cases equal R449-2's receipts; the run.sh comment and the PR body are corrected |
| R449-2 S1: the parent's own census reads `.sv` text | SUGGESTION | open, out of scope (parent follow-up); listed in "Not done here" | |
| R449-2 S2: the `elab_bounds.sh` yosys leg never runs hosted | SUGGESTION | open; listed; the workflow is unchanged | `elab_bounds.sh` still grades the class without yosys |
| Round-1 findings (R448-1 F1, F2, S1, S2; R449-1 F1-F4, R1-R3, S1), resolved at round 2 | | still **RESOLVED** at the merge | parent gate 3 and its self-test 50/50 with p2-p1; the `KL_pp_nvm_port.sv` citations and `:2731` re-derived; the derived bound and its class grading; R449-1 S1 stays with issue #151 |

No finding is worsened. F1 is new, and comes from the round-3b merge.

## 5. Lenses

- **Conformance: CLEAN.**
  - #25 bullet 1 holds against `run.sh:169-188, 237, 271`: 42/42 locally and hosted, and 12 + 16 header-form probes are counted or named.
  - #25 bullet 2: the five newly covered tops and planted new modules each go red.
  - #25 bullet 3: every red case names its module, including the parse failures and the escaped identifier.
  - #25 bullet 4: `run.sh:304` is unchanged and passes.
  - #17: the guard is unchanged by rounds 3 and 3b, and `elab_bounds.sh` is rc 0 at the merge.
  - #37: the NSD arms are killed, and the one-word move is graded.
- **RTL: CLEAN.**
  - Round 3 changes no `hdl/`. Against `main`, the merge changes only this lane's two RTL files (`KL_pp_nvm_port.sv`, `protocol_processor_top.sv`). Against `b6f17f2` it changes only P1's four (`KL_aecp_desc_store.sv`, `KL_aecp_engine.sv`, `KL_aecp_nvm_writer.sv`, and the top's port comments).
  - Lint is 41/41, and the ROMs are identical at four revisions.
  - At the merge, the gate elaborates all 42 tops under both allocators and passes XILINX.
- **Robustness: CLEAN** (S1 and S2 are optional).
  - The census covers attribute instances, boxes, comments, `macromodule`, split headers, escaped identifiers, a red first top and a failed parse.
  - The six mutants of the change are killed.
  - The unchanged fault cases and the allocator cases reproduce.
- **Tests: CLEAN.**
  - 33 suites are rc 0 with 1,021,449 checks.
  - The dispatch campaign is 40/40 with records equal; P1's D3 arms are 23/23; notify is 40/40; the name-write mutant is killed.
  - Every round-2 probe gives its required outcome.
- **Docs: UNCLEAN (F1).**
  - The red-proof table's "this head" excerpts predate the merge.
  - Otherwise correct: the run.sh comments at `:4-10`, `:157-168`, `:212-234` and `:244-248`; the `tb/nvm_port/README.md` conflict lines; every citation checked; and the PR body's Round 3 and Round 3b tables, against my receipts.

## 6. Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #25 bullets 1-4 against `run.sh:157-306` (local 0.66 and hosted 0.33); #17 `elab_bounds.sh` at the merge; #37 NSD arms; round-3 and round-3b assignment items | R448-3 | 39298e03aa53d5f82c7485b8d12d2b69a47b0d55 |
| RTL | CLEAN | merge sides per file (33); `hdl/` delta vs `main` and vs `b6f17f2`; ROM regeneration at 4 revisions; `lint_hdl.sh` 41/41; Yosys elaboration of 42 tops and XILINX | R448-3 | 39298e03aa53d5f82c7485b8d12d2b69a47b0d55 |
| Robustness | CLEAN | census and `parse_site` over 16 + 12 + 8 header/fault forms, 6 killed mutants and the unsupported-option probe; 24 + 21 unchanged fault cases; allocator cases | R448-3 | 39298e03aa53d5f82c7485b8d12d2b69a47b0d55 |
| Tests | CLEAN | 33 suites (1,021,449 checks); dispatch campaign 44/44 with README counts; D3 P1 arms 27/27 incl. goldens; notify 45/45; name-write; parent gates 1-8, 11, 17 and 9 more parent checks, with a no-c10 control | R448-3 | 39298e03aa53d5f82c7485b8d12d2b69a47b0d55 |
| Docs | UNCLEAN (F1) | PR body (all sections) against receipts; `run.sh` comments; `tb/nvm_port/README.md:102-108`; every `path:N` citation into changed files plus the bare ones listed in §2; `make check` | R448-3 | 39298e03aa53d5f82c7485b8d12d2b69a47b0d55 |

## 7. Real limits

- **Campaigns not run here.** The other 87 D3 arms, `ctr_mutants.py`, `acmp_mutants.py`, `gsi_mutants.py`, `aecp_mutants.py`, and the `tb/adp_engine`, `tb/maap` and `tb/srp_top` mutants were not run here. Their merge counts rest on the author's Round 3b table and on the hosted `suites` job: its SRP, MAAP and ADP campaigns had succeeded at the exact head, and its AECP hazard campaign succeeded in one of the two runs, when last read. I ran the campaigns that exercise this lane's arms and P1's new arms.
- `make -C tb/nvm_port figures` was not run. Its hosted step was pending when read.
- No Vivado or xvlog on this host. The out-of-context equality at the merge, the `Synth 8-6901` counts and parent gate 9 (`xvlog_gate.py`) were not reproduced.
- Parent gates 10 (`test_builder.py`) and 12-16 (`pp_shadow`, `nvm_cosim`, `milan_dp`, `milan_dp_render`) were not run. They rest on the author's report and the manager's banks. The parent's private `external` submodule was not checked out.
- yosys 0.33 was not run locally. The hosted `portability` jobs at the exact head executed it.
- Detached job launches were refused in this session, so every run was in the foreground. Two campaigns outlasted the 10-minute window and were polled to completion; their rc files and logs are in the receipts.
- The host was shared and heavily loaded (load 50-85 on 16 CPUs), so the wall times quoted here are not comparable to the PR's.
- Physical calibration NOT RUN. Field skips are not hardware proof. No hardware claim is made.

## 8. Pending manager duties

1. Route F1 to the author. It is a body-only fix: re-quote or label the two excerpts. No source change and no re-run beyond `c-auto-split` is needed.
2. Confirm that both hosted `suites` jobs finish green at the exact head, including the AECP dispatch campaign, the matrix and the nvm_port figures steps. They were in progress when read (`receipts/hosted_suites_steps_*.txt`). The manager owns hosted/act acceptance.
3. Build the final current-dev candidate at the merge turn (source base `f4167536`, live dev `5fabb46e`). This source-head review does not cover it.
4. At adoption, carry c8, then p2-p1 (`d3034e89`) in place of p2, then c10 (`55e62329`), and keep `check_rtl_source_lists.py --selftest` in the consumer set.
5. Close PR #26 at merge. Issue #151 keeps R449-1 S1, and R449-2 S1 needs a parent follow-up.
6. Residue checklist: no RESIDUE from this review.

## 9. Scripts and receipts

Every published file is listed in `MANIFEST.sha256`. Absolute local paths in receipts are rewritten to `<packet>`, `<scratch>`, `<clone>`, `<round-1 packet>`, `<round-2 packet>`, `<R449-2 packet>` and `<home path>`.

- `scripts/`:
  - `r448-2/` and `r449-2/`: the round-2 probes, run unchanged. `receipts/probe_script_identity.txt` gives the sha256 of the copies as run; one published file has a path redacted.
  - `r3_probe.sh`: the round-3 mechanism probes and mutants.
  - `cite_drift.py`: merge citation drift.
  - `rom_regen.sh`.
- `receipts/`:
  - `census/`, `census449/`, `census_unit/`, `gate_probes/` (+ `gate_probes_vs_r2.txt`), `r449_faults/` (+ `compare_vs_r449-2.txt`), `r3_probes/`, `line_shift/`;
  - `runs/` (the head gate), `suites/` (33 suites, lint, `make check`, the matrix, preflights, the gate under the system allocator, the allocator self-test);
  - `campaigns/`, `parent/` (with `setup.txt`), `hosted/`;
  - `merge_sides.txt`, `cite_drift.txt`, `rom_regen.txt`, `clone_integrity.txt`, `tool_identity.txt`, `evidence_sha256_check.txt`, `hosted_checks_39298e03.txt`.

R448-3 FINISHED
