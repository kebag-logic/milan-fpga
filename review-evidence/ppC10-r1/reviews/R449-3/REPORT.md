[R449] POSITIVE - exact head 39298e03aa53d5f82c7485b8d12d2b69a47b0d55

# R449-3: external independent review of PR #149 (issue #25, lane C10), rounds 3 and 3b

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #149, head
  `39298e03aa53d5f82c7485b8d12d2b69a47b0d55`, tree `7f3b4639ee70ad34c567f4df4cc9fec4c8172780`,
  source base `f4167536d358c996f4e1b70b875879c1651f85d3`. Processor `main` is now `c4cb84ff`
  (PR #150, lane P1). Review start: PR #149 comment 5973160279.
- Delta reviewed:
  - Round 3, `cd08ca7b..b6f17f22`: one commit, the census from yosys's own module list, and
    `parse_site`.
  - Round 3b: the `--no-ff` merge `39298e03` of `main` `c4cb84ff`, with parents `b6f17f2`
    and `c4cb84f`.
  - Judged against R448-2 (5970948940), R449-2 (5970973855) and the assignments 5970977905
    (round 3) and 5972322274 (round 3b).
- Reconstructed from:
  - README.md and docs/README.md. The repository has no AGENTS.md or CONTRIBUTING.md.
  - The issue #25 body and all eleven comments: the two author corrections, the lane
    assignment 5967291597, and the round-2, round-3 and round-3b assignments.
  - The live PR body.
  - `git diff f4167536..39298e03`, `git diff c4cb84f..39298e03` (the PR's own diff against
    the moved `main`) and the commit graph.
- Public evidence:
  - kebag-logic/milan-fpga `2a54253e:review-evidence/ppC10-r1`.
  - The same branch's later archive `d2222115`: `author-r2/parent-adoption-c10-1269cdaf.patch`
    and `author-r3/PR-BODY.md`.
  - P1's `parent-adoption-p2-p1-1269cdaf.patch`, from the `ppP1-review-evidence` branch.
  - Every file used has the sha256 published in its MANIFEST.json, and `author-r3/PR-BODY.md`
    is byte-equal to the live PR body (`receipts/evidence_sha256.txt`).
- Order kept:
  - Before reading any round-2 finding, I made my own pass over the round-3 and round-3b
    diff and ran the round-2 probes and my own probes.
  - I then read the findings of the two round-2 reports on the PR, R448-2's and my own
    R449-2's.
  - I did not read any round-3 review by another reviewer.
- Every result below was re-executed by this reviewer at this head, in scratch copies,
  unless it is marked "read only". Scripts are under `scripts/` (see `scripts/README.md`).
  Raw receipts are under `receipts/`.

## Verdict

POSITIVE. There is no open BLOCKER, MAJOR or MINOR. One RESIDUE (a PR-body column label)
and the two retained round-2 SUGGESTIONS are recorded below. None of them affects the
verdict.

**Round 3: the census.**
- The declared set is now yosys's own `select -list =*` of the `read_verilog -defer` design
  that the gate elaborates. It is written at `syn/yosys/run.sh:237`, read by `census()` at
  `:169-188`, and the census is called at `:271`.
- Every header form that escaped the census or was misnamed at `cd08ca7` is now counted or
  named:
  - an attribute instance on the header line or on the line before;
  - two attribute instances;
  - comments;
  - `macromodule`;
  - split headers;
  - escaped identifiers;
  - black and white boxes.
- `module automatic` fails the parse, because yosys 0.66 rejects the lifetime keyword, and
  `parse_site` names the module.
- R448-2 F1 = R449-2 F1 is resolved.

**Round 3b: the merge.**
- Replaying the merge with `git merge-tree` gives one conflict, `tb/nvm_port/README.md:105-106`.
  The head equals the replay in every other file.
- The resolution keeps P1's writer citation (`KL_aecp_nvm_writer.sv:549-552`) and
  re-derives the shadow instance as `protocol_processor_top.sv:2731`.
- Both sides are whole:
  - The PR's diff against `c4cb84f` touches only its own two RTL files.
  - The merge's RTL diff against `b6f17f2` equals P1's RTL diff.
- Every ROM is identical at `f4167536`, `b6f17f2`, `c4cb84f` and `39298e03`.
- These reproduce the PR's figures:
  - every processor suite;
  - the Yosys gate, 42 tops (P1 added no module);
  - every `tb/pp_top` campaign;
  - the parent consumer set (17).

## Findings

### R1 - RESIDUE - Docs - the red-proof table's "this head" column quotes all.v line numbers from an earlier head

- **Artifact:** the PR body §1 red-proof table:
  - its header at body line 52: `| Fault planted in | main f4167536 | this head |`;
  - the row at body line 61, which quotes `all.v:20318`;
  - the row at body line 69, which quotes `all.v:20749`.
- **Evidence:** at `39298e03` the same probes cite other all.v lines, because P1's RTL
  lengthens all.v:
  - R448-2's unchanged `plant.py allv-syntax KL_srp_top` gives
    `YOSYS FAIL all.v in module KL_srp_top: all.v:20441: ...` (`receipts/allv_syntax_row.log`).
  - R448-2's unchanged `c-auto-split` gives
    `YOSYS FAIL all.v in module KL_r448_auto: all.v:20859: ...`
    (`receipts/r448_census_cases/c-auto-split.log`).
  - Each row's rc and named module are as the table states.
- **Impact:** a reader who reproduces either row sees a different all.v line from the one
  quoted. The verdict, rc and module of every row hold at this head. Only the label of the
  column that holds an earlier head's log excerpts is wrong. No measurement, test, code or
  conformance claim changes, so this is RESIDUE.
- **Exact fix:** in the table header at body line 52, replace `this head` with
  `this PR (log excerpts from b6f17f2; all.v line numbers move with each merge)`.
- **Verification:** read the PR body.

### S1 - SUGGESTION - retained from R449-2 S1: the parent's own census still reads `.sv` text

This is unchanged at this head and out of this PR's scope, as the round-3 assignment says.
The PR body lists it under "Not done here" and "Open suggestions".

### S2 - SUGGESTION - retained from R449-2 S2: the yosys leg of `elab_bounds.sh` never runs hosted

- The PR changes no workflow: `git diff --stat c4cb84f..39298e03` lists no file under
  `.github/`.
- Locally, the bench prints `YOSYS OK   MAX_PAYLOAD_P=65527 elaborates, MAX_PAYLOAD_P=65528
  stops at the guard's $finish` (`receipts/elab_bounds.log`).

## Prior public findings at this head

**R448-2 F1 = R449-2 F1 (MINOR): resolved.** The finding: an attributed header escapes the
census, and `parse_site` misnames `module automatic` and attributed headers.

- R448-2's `run_census_cases.sh`, unchanged, 16 rows:
  - `c-attr-same` and `c-attr-own`: rc 1, naming `KL_r448_attrs` and `KL_r448_attro`.
  - `c-attr-own-top-clean`: rc 0, with 43 OK, parsed 1 time and XILINX OK.
  - `c-attr-own-top`: rc 1, `YOSYS FAIL KL_r448_attro`.
  - `c-auto-split`: rc 1, named `KL_r448_auto` through the parse failure.
  - Every other head row is red and named.
  - `c-ifdef` gives rc 0. That is the census's stated scope (`run.sh:165-167` and PR body
    §1).
  - The four `r1-*` rows run on the round-1 tree (`54f9411`). They give its known results:
    `split` and `attr-same` rc 0; `attr-own` and `ifdef` rc 1.
- R448-2's `parse_site_unit.sh` names `KL_first`, `KL_auto` and `KL_attr`. At `cd08ca7` it
  named `KL_first`, `automatic` and `automatic`.
- My R449-2 `census_probe.sh`, unchanged, 13 runs:
  - Every form gives rc 1 and is named.
  - `allvauto` names `KL_r449_allvauto`.
  - The `top` variants give `YOSYS FAIL KL_r449_<form>`.

**R449-2 S1 and S2 (SUGGESTION): retained.** They are S1 and S2 above.

**The round-1 findings resolved in round 2 stay resolved.** These are R448-1 F1, F2, S1 and
S2, and R449-1 F1-F4 and R1-R3:

- With the amended c10, parent gate 3 and its self-test are rc 0 (50 of 50).
- `KL_pp_nvm_port.sv:196-200` is unchanged.
- `elab_bounds.sh` still grades the fatal class.
- `run.sh:9-10` keeps R1's text.
- Every `KL_pp_nvm_port.sv` citation was re-derived (see Docs).
- The README's shadow citation is `:2731`, the `KL_acmp_nvm_shadow #(` line.
- R3's text is in the c10 patch, unchanged since round 2 (sha256 `55e62329...`).

## Evidence by lens

### Conformance

#25 acceptance, at this head:
- **Bullet 1 (every module is a top, and a check enforces it).** 42 modules are declared and
  42 are tops. The census refuses:
  - a module missing from `tops`: `drop-srp_top`, `newmod` and every census form;
  - a top that no module declares: `bogus` (`receipts/r449_faults/`).
- **Bullet 2 (red on a broken new top).** `inst-srp_top`, `inst-pptop`, `inst-dfifo`,
  `inst-two`, `fatal-srp_top` and `port-shadow` all give rc 1.
- **Bullet 3 (a failure names its module).** Every red row names its module. That includes
  a killed yosys (`killonce-maap`: `YOSYS FAIL KL_pp_maap: yosys exited 137`) and a nonzero
  exit after clean tops (`rcone`).
- **Bullet 4 (the RAMB36E1 assertion).** `run.sh:304` is unchanged:
  `YOSYS XILINX OK  KL_aecp_engine`.
- **Bullet 5 (wall time and top count).** These are reported in the PR body, and #25 does not
  make them a pass criterion. My gate run took 38.89 s at a load average of 22-33. I make no
  timing claim.

#17 and #37 did not change in rounds 3 and 3b, and their gates pass at the merge (below).

Assignment 5972322274, item 1:
- one merge commit with both parents, no rebase;
- both sides kept;
- citations re-derived;
- ROMs identical.

### RTL

- `git diff c4cb84f 39298e03 -- hdl` touches only `KL_pp_nvm_port.sv` and
  `protocol_processor_top.sv`. `git diff b6f17f2 39298e03 -- hdl` equals
  `git diff f4167536 c4cb84f -- hdl` line for line: P1's four RTL files
  (`receipts/merge_checks.txt`).
- Compare the top's sorted multiset of non-blank lines at the merge with `c4cb84f`'s. They
  differ by one added comment line:
  `// u_notify's arm and PRNG faces, read by this mux and the PRNG mux below`.
  The same holds at round 3 against `f4167536`. The reorder adds no logic.
- `scripts/top_netlist_equiv.sh` builds the netlist at `c4cb84f` and at the merge with
  sv2v and yosys 0.66 (`hierarchy -check -top protocol_processor_top; proc; opt_clean;
  write_verilog -noattr`). The two netlists:
  - are 3,442,245 bytes each;
  - differ only in generated names that carry all.v line numbers and creation counters;
  - give equal sorted multisets of 110,759 lines once those two are normalised
    (`receipts/netlist_equiv.log`).
- `scripts/rom_identity.sh`: the sha256 of each of these is the same at all four
  revisions (`receipts/rom_identity.txt`):
  - `ucode.hex`;
  - `ltn_rom.hex`;
  - `example_milan_8.bin` and `.map`;
  - `milan_min.bin` and `.map`.
- `lint_hdl.sh`: 41 of 41 (pinned Verilator 5.050).

### Robustness

- `census()` reads only yosys's list (`sed -n 's/^\$abstract\\//p'`) and refuses an empty
  list (`run.sh:171`). It runs once, on the first parse, before any verdict line
  (`run.sh:271`).
- My additional probes (`scripts/census_extra.sh`, `receipts/census_extra/`):

  | Case | rc | Result |
  |---|---:|---|
  | `(* blackbox *) module KL_r4493_bbox`, not in `tops` | 1 | the census names it |
  | the same, added to `tops` | 0 | 43 OK, parsed 1 time, XILINX OK |
  | a `(* whitebox *)` module holding a fault | 1 | the census names it |
  | an escaped identifier, `module \KL_r4493_esc$q` | 1 | the census names `KL_r4493_esc$q` |
  | two attribute instances on the line before `module` | 1 | the census names it |
  | a fault in the first top, plus a module not in `tops` | 1 | the census still runs and names the unlisted module |
  | mutant: `select -list *` (no `=`), with the blackbox module | 0 | the mutant survives: the `=` is what counts boxes |
  | mutant: the census call removed, with an attributed module | 0 | the mutant survives: the census is what catches the module |

- `scripts/parse_site_edges.sh` runs the head's `parse_site`, extracted verbatim, over 12
  cited lines. They cover:
  - headers, bodies and `endmodule` lines;
  - a stray line between modules (no name expected);
  - `module automatic`;
  - `module static` with a string attribute that holds `*`;
  - two attribute instances;
  - an escaped identifier;
  - `macromodule NAME(` with no space.

  All 12 give the expected name under gawk and under `gawk --posix`
  (`receipts/parse_site_edges.txt`).
- R449-2's `yosys_fault.sh`, unchanged, on 12 of its cases (`receipts/r449_faults/SUMMARY.md`).
  Every row matches the PR's red-proof table:
  - `inst-dfifo` names `KL_pp_dispatch`, `KL_pp_dispatch_fifo` and
    `protocol_processor_top`, and parses 3 times.
  - `inst-two` names four tops and parses 4 times.
- With `YOSYS_MALLOC=none` the gate is rc 0, and its verdict lines are identical to the
  jemalloc run's. `--selftest-alloc`: PASS.

### Tests

All at `39298e03`, with the pinned Verilator 5.050 first on PATH:

| Command | rc | Result | Against the PR body |
|---|---:|---|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, **1,021,449** checks, 0 failing; `tb/pp_top` 10,416 | equal |
| `./syn/yosys/run.sh` | 0 | 42 `YOSYS OK`, `all.v parsed 1 time(s)`, `YOSYS XILINX OK` | equal |
| `tb/nvm_port/elab_bounds.sh` | 0 | 4 ELAB OK, 6 GUARD OK (class printed), YOSYS OK | equal |
| `aecp_dispatch_mutants.py --jobs 3` | 0 | 4 controls PASS, 40 of 40 KILLED (NSD arms below) | equal |
| `aecp_mutants.py --jobs 3` | 0 | 5 controls PASS, 55 of 55 KILLED | equal |
| `ctr_mutants.py --jobs 3` | 0 | control PASS, 17 of 17 KILLED | equal |
| `d3_mutants.py --jobs 4` | 0 | 6 goldens PASS, 110 of 110 KILLED | equal |
| `notify_mutants.py --jobs 3` | 0 | 5 goldens PASS, 40 of 40 KILLED | equal |
| `acmp_mutants.py --jobs 3` | 0 | 3 goldens PASS, 19 of 19 KILLED | equal |
| `gsi_mutants.py --jobs 3` | 0 | golden and restored PASS, 20 detected | equal |
| `name_wr_mutant.py` | 0 | golden and restored PASS, the decode mutant killed | equal |
| `tb/adp_engine` `mutants.py --jobs 3` | 0 | 2 controls PASS, 30 of 30 KILLED | equal |
| `tb/maap` `mutants.py --jobs 3` | 0 | 3 controls PASS, 29 of 29 runs KILLED | equal |
| `tb/srp_top` `mutants.py --jobs 3` | 0 | 11 controls PASS, 78 KILLED | equal |

- The dispatch campaign's NSD-related arms fail these checks:

  | Arm | Failing checks |
  |---|---|
  | `sclks-miss-target-next-word` | LK4, NSD3 |
  | `sclks-miss-preload-dropped` | NSD1, NSD3 |
  | `sclks-miss-branch-dropped` | LK5, NSD1 |
  | `lk-sclks-miss-lock-nop` | LK4, NSD3 |

- `scripts/readme_counts.py` compares each arm's measured failing-check count with the count
  `tb/pp_top/README.md` records for it. Every count is equal: dispatch 40 arms, AECP 55,
  counters 17 (`receipts/readme_counts_lane_b.txt`).
- The D3, notify, ACMP, GSI and name-write drivers grade named checks. Each reports
  `"missing": []` for every arm.
- After the campaigns, the campaign copy of the tree was unchanged except for a Python
  bytecode cache.

### Docs

- Every explicit line citation into a file both sides changed, and every
  `KL_pp_nvm_port.sv` citation, was read at the merge against the text it names
  (`receipts/merge_checks.txt`). All hold:

  | Citation | Text at the merge |
  |---|---|
  | `KL_aecp_nvm_writer.sv:549-552` | `frame_ok_w` |
  | `protocol_processor_top.sv:2731` | `KL_acmp_nvm_shadow #(` |
  | `KL_pp_nvm_port.sv:244-255` | `dev_cmd_owned_w` |
  | `KL_pp_nvm_port.sv:350-354` | the sticky done set |
  | `KL_pp_nvm_port.sv:446-449` | `S_WWAIT` / `if (dev_err_i)` |
  | `KL_pp_nvm_port.sv:376` | `state_r <= S_WEREQ` |
  | `KL_pp_nvm_port.sv:390` | `state_r <= S_WEWAIT` |
  | `KL_pp_nvm_port.sv:33-34` | unchanged |
  | `KL_pp_nvm_port.sv:196-200` | the guard |
  | `KL_pp_acmp_listener.sv:344-347` (PR body) | the `$fatal` precedent |
  | `KL_aecp_notify.sv:557`, `KL_pp_originator.sv:194`, `KL_pp_rx_validator.sv:383` (PR body) | the three #22 sites |

- The `run.sh` comments at `:7-10`, `:140-141`, `:157-168`, `:219-234`, `:244-248` and
  `:269-270` describe what the code does.
- These are intact at the merge:
  - the PR's 09 §8.1 and §8.6 rows;
  - `tb/nvm_port/README.md`;
  - `tb/pp_top/README.md`, including the NSD arms and section.
- `make check` is rc 0: 41 mermaid and 18 wavedrom blocks, 1,114 links, 115 REQ rows,
  17 GAP findings, 94 module rows with 0 untested, 28 parameters.
- `gen_matrix.py --check` is rc 0.
- The PR body's round-3 and round-3b claims reproduce, except R1's column label.

### Parent consumer set (17) at milan-fpga `1269cdaf` + c8 + p2-p1 + c10

The scratch parent:
- a fresh clone of dev at `1269cdaf` (984 tracked files);
- gptp-processor `5dce647a` and verilog-axis `48ff7a7e` at their pins;
- protocol-processor at `39298e03`, with its gitlink recorded;
- the three submodules registered, and `external` (private) not initialised.

`parent-adoption-c8-cdf49d1a.patch` (`aa5a88eb...`), then
`parent-adoption-p2-p1-1269cdaf.patch` (`d3034e89...`), then the amended
`parent-adoption-c10-1269cdaf.patch` (`55e62329...`) were each applied after a clean
`git apply --check`. Receipts: `receipts/parent_light.log`, `parent_heavy_a.log` and
`parent_heavy_b.log`.

| # | Command | rc | Result |
|---:|---|---:|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | 0, 0 | ratchets held |
| 3 | `check_rtl_source_lists.py`; `--selftest` | 0; 0 | `protocol-processor 42/42 tops, 0 recorded`; 50 of 50 |
| 4 | `pp_srcs.py --check --selftest` | 0 | |
| 5 | `check_port_contracts.py` | 0 | protocol-processor 1,759 ports, 111 <= 111 undocumented |
| 6, 7 | `measure_naming.py --check`, `measure_test_evidence.py --check` | 0, 0 | 96 recorded; 72 <= 77, 0 <= 0 unexplained DUT readers |
| 8 | `docs_check.py` | 0 | 0 findings |
| 9 | `xvlog_gate.py --check`; `--selftest` | 0; 0 | `PASS (3 finding(s) == ratchet)`: the three #22 sites |
| 10 | `sw/builder/test_builder.py` | 0 | `ALL GATES PASS EXCEPT 1 NOT RUN`: its gate 11 needs a local build tree, as the PR says |
| 11 | `lint_rtl.py --check` | 0 | 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | four runs: 606, 606, 646 and 311 checks, 0 failures |
| 13, 14 | `make -C tb/verilator/nvm_cosim lint`, `quick` | 0, 0 | pass; 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | 9 `RESULT: PASS` |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | 0 failures; 5 of 5 leg-defect arms caught |
| 17 | `check_sh_idiom.py` | 0 | unquoted expansion 3 <= 3, top-heavy long script 0 <= 0 |
| | `check_sh_idiom.py --selftest`, `check_hygiene.py --check` and `--selftest`, `check_todo_ownership.py` and `--selftest`, `measure_fail_fast.py --check` and `--selftest`, `check_entity_shape.py --self-test` | all 0 | |

### Hosted CI at the exact head (read only; the manager owns acceptance)

Workflow `hdl` ran twice at `39298e03`: run 37151399092 (push) and run 37151403162
(pull_request). Read at 22:03 UTC (`receipts/hosted_status.txt`).

- **Push run: completed, success, every job executed.**
  - `suites` (job 111285877225) skipped only its Verilator build step, on a cache hit. It
    executed lint, every suite and the five campaigns, and its log shows
    `suites: 1021449 checks total, 0 failing`, `PASS pp_top (10416 checks ...)` and
    `all measured figures agree with the tree`
    (`receipts/hosted_suites_push_111285877225.log`).
  - `portability` (job 111285877086) shows yosys 0.33, `yosys allocator: system`,
    42 `YOSYS OK`, `all.v parsed 1 time(s)` and `YOSYS XILINX OK`
    (`receipts/hosted_portability_push_111285877086.log`). So the `select -list =*` census
    works on the hosted yosys.
- **Pull-request run:** `portability` and `docs-gates` succeeded; `suites` was still in
  progress.

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #25 acceptance bullets 1-5 against `run.sh` (census `:169-188`, list `:237`, call `:271`, verdicts `:262-295`, XILINX `:304`); the round-3 and round-3b assignments, item by item; #17 and #37 unchanged and green at the merge; scope decisions (#151; #22 relates; the parent census is out of scope) | R449-3 | 39298e03aa53d5f82c7485b8d12d2b69a47b0d55 |
| RTL | CLEAN | merge replay against the head; `hdl` diffs against both parents; the top's line multiset; sv2v + yosys netlist of `protocol_processor_top` at `c4cb84f` and at the merge; ROM identity at four revisions; lint 41 of 41 | R449-3 | 39298e03aa53d5f82c7485b8d12d2b69a47b0d55 |
| Robustness | CLEAN | `census()`, `gate_script()`, `parse_site()` and `elaborate_tops()` over 16 + 13 unchanged round-2 census runs; 8 new census runs (boxes, escaped name, two attributes, first-top failure, two mutants); 12 unchanged fault cases (kill, nonzero exit, parse failure, resume); 12 `parse_site` edge lines under two awk modes; the system allocator | R449-3 | 39298e03aa53d5f82c7485b8d12d2b69a47b0d55 |
| Tests | CLEAN | suites, 1,021,449 checks and 0 failing; 11 campaign drivers (controls, goldens, kills) and 112 README count records; `elab_bounds.sh`; the PR's red-proof rows; the parent consumer set (17) and its self-tests | R449-3 | 39298e03aa53d5f82c7485b8d12d2b69a47b0d55 |
| Docs | CLEAN (R1 RESIDUE carried) | `run.sh` comments; PR body §1-§4, Round 3, Round 3b, the Validation and parent tables; `tb/nvm_port/README.md` (the conflict lines); `tb/pp_top/README.md`; 09 §8.1 and §8.6; every citation into a file both sides changed; `make check`; `gen_matrix.py --check` | R449-3 | 39298e03aa53d5f82c7485b8d12d2b69a47b0d55 |

## Limits

- **Vivado.**
  - I did not run the out-of-context synthesis. The PR's claim that the Vivado netlist and
    utilisation are equal at the merge is the author's measurement.
  - My netlist check uses sv2v + yosys 0.66 elaboration, compared after normalising
    line-derived generated names. That is weaker than byte equality.
  - The parent's xvlog gate ran the installed xvlog analysis front end (no synthesis) while
    campaign builds were running.
- **yosys 0.33.** It is not installed here. The hosted portability job shows the clean head
  passing on 0.33. I did not reproduce:
  - the PR's statement that 0.33's `ls =*` drops boxes;
  - its 0.33 fault rows.
- **Figures gate.** I did not run `make -C tb/nvm_port figures` locally. Neither round 3 nor
  the merge changes `KL_pp_nvm_port.sv` or a measured figure, and the hosted push `suites`
  job ran it at this head: `all measured figures agree with the tree`.
- **Fault cases.** I reran 12 of R449-1's 21 fault cases, not all 21. I did not rerun
  R448-2's `run_gate_cases.sh`.
- **Parent.**
  - The `external` submodule was not initialised, because it is private; the PR's own run
    also left it out.
  - Gate 10's internal gate 11 did not run, because it needs a local build tree.
  - I ran no full parent, PP, gPTP, Yosys or builder bank.
- **Clause conformance.** I did not consult the IEEE 1722.1-2021 or Milan v1.2 PDFs. Rounds
  3 and 3b make no clause claim.
- **Hardware.** Physical calibration NOT RUN. Field skips are not hardware proof. No
  hardware was used.
- **Host load.** The load average was 20-85 on 16 CPUs, from concurrent work. I make no
  timing claim.

## Pending manager duties

- Confirm that the pull-request run's `suites` job (run 37151403162, job 111285888063)
  finishes green at the exact head. The push run's `suites` is already green.
- Build the final current-dev candidate at the merge turn (source base `f4167536`, live dev
  `5fabb46e`). The source validation here does not cover it.
- Carry R1 to the residue checklist.
- Adoption order: c8, then p2-p1 (P1's patch, in place of p2), then the amended c10
  (`55e62329...`), as the parent-visible list states.
- Close PR #26 at merge.
- Carry #22's three remaining files and #25's yosys/sv2v pinning note forward. S1 and S2 are
  optional.

## Integrity

**The review clone was only read.** I used `git archive`, `git show`, `git merge-tree
--write-tree` (which writes objects only) and local clones into `scratch/`.

**One file was created and removed.** Running a descriptor generator's `--help` in the clone
once created an ignored `hdl/aecp/desc/__pycache__/`: two `.pyc` files, timestamped at that
command. I removed them.

**After every probe** (`receipts/integrity.txt`):
- the clone is detached at `39298e03aa53d5f82c7485b8d12d2b69a47b0d55`, tree
  `7f3b4639ee70ad34c567f4df4cc9fec4c8172780`;
- `git status --porcelain --ignored` is empty;
- the index equals `git ls-tree -r HEAD`;
- all 504 tracked files, re-hashed with `git hash-object --no-filters`, equal their blobs,
  and every mode is equal.

The repository has no gitlinks, so no submodule pin applies.

**Isolation.**
- Every probe, every campaign and the scratch parent ran under the packet's `scratch/`.
- I edited no other checkout.
- I stopped one duplicate start of my own parent light-gate script, by its PIDs only. No
  other process was touched.
- At most 16 jobs ran at once. The unit's 12 GB memory cap was not reached.

## Receipts

Every published file is listed in `MANIFEST.sha256`. In receipts, absolute paths are
rewritten to `<packet>`, `<review-clone>`, `<pinned-verilator-5.050>` and `~`.

R449-3 FINISHED
