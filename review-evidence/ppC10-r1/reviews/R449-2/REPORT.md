[R449] NEGATIVE - exact head cd08ca7b3d962ab040d8aaa023c57e7b0e010a6d

# R449-2: external independent review of PR #149 (issue #25, lane C10), round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #149, head
  `cd08ca7b3d962ab040d8aaa023c57e7b0e010a6d`, tree `e0b4807f1a6e2254a495f147f28e55e86d08f0bf`,
  base `f4167536d358c996f4e1b70b875879c1651f85d3`. Review start: PR #149 comment 5970584532.
- Delta reviewed: round 2, `54f9411a..cd08ca7b` (five commits: `1a5f555` census from all.v,
  `6ba4659` derived bound, `522d49a` severity grading, `137ac73` citations and wording,
  `cd08ca7` run.sh functions). It was judged against R448-1 (5969219155), R449-1
  (5969434371) and the round-2 assignment (5969440297).
- Reconstructed from: README.md and docs/README.md (the repository has no AGENTS.md or
  CONTRIBUTING.md), the issue #25 body and all its comments (the two author corrections, the
  lane assignment 5967291597 and the round-2 assignment 5969440297), the live PR body,
  `git diff f4167536..cd08ca7b` and the per-commit history. Public evidence was read at
  kebag-logic/milan-fpga `2a54253e:review-evidence/ppC10-r1` (round 1) and at that branch's
  later archive commit `2da8e8f0` (`author-r2/`: the amended c10 patch, PR-BODY.md and
  HANDOFF.md). Every evidence file's sha256 equals its MANIFEST.json entry, and the published
  `author-r2/PR-BODY.md` is byte-equal to the live PR body (`receipts/evidence-sha256.txt`).
- Order kept: I wrote my own pass over the round-2 diff before reading the prior findings.
  R449-1's findings were then read from my own round-1 packet. R448-1's findings are judged
  from the manager's round-2 assignment text. I did not read R448-1's report or any other
  reviewer's material.
- Every result below was re-executed by this reviewer in scratch copies, unless it is marked
  "read only". Raw receipts are under `receipts/` and scripts under `scripts/`.

## Verdict

NEGATIVE, on one open MINOR finding. Round 2 resolves every round-1 finding as filed. It
does not close the census's header-layout dependence, which R449-1 F2's required outcome
asked for.

What holds at this head:

- **Round-1 F1 (parent self-test).** Resolved. At milan-fpga `1269cdaf` + c8 + p2 + the amended c10,
  `check_rtl_source_lists.py` and `--selftest` are both rc 0 (50/50). Each of six
  refusal-disabling checker mutants turns the self-test red, including one the old
  self-test could not see: `verdict()` dropping `STALE RECORD`. The parent-visible list
  names the self-test change.
- **The derived bound.** It is computed from `$bits(dev_len_o)` and `HDR_LEN_C`, in both the
  condition and the message. `hdr10` refuses. The port's Yosys netlist is unchanged from
  `54f9411` at 1024 and at 65527.
- **elab_bounds.sh.** It grades the fatal class. The `$error`, `$warning` and `$info`
  mutants are killed, with and without sv2v and yosys on PATH.
- **Citations.** The whole moved set is correct.
- **The run.sh refactor.** My 21 round-1 fault cases reproduce row for row, except
  `newmod`, which goes from rc 0 to rc 1, named.

Still open:

- **R449-2 F1 (MINOR).** The census and the parse-failure naming
  in `syn/yosys/run.sh` only read headers whose line starts with `module`. sv2v writes a
  module's attribute instance on the header line: `(* keep_hierarchy = "yes" *) module X`.
  - Such a module escapes the census, and a fault inside it passes the gate with rc 0, 42 OK
    and XILINX OK.
  - Naming it in `tops` is refused as "no longer exist", so the module cannot be covered at
    all.
  - A parse failure in a `module automatic` module is reported "in module automatic".

  The PR body and the run.sh comment state the opposite. The escape was already present at
  `54f9411`, and R449-1 missed it.

## Findings

### F1 - MINOR - Robustness, Tests, Conformance, Docs - all.v headers with a leading attribute escape the census, and `parse_site` misnames lifetime-keyword headers

- **Artifacts:**
  - `syn/yosys/run.sh:168-169`, the census:
    `grep -oE '^module[[:space:]]+((automatic|static)[[:space:]]+)?[A-Za-z_][A-Za-z0-9_]*' "$work/all.v" | awk '{print $NF}'`.
  - `syn/yosys/run.sh:245-246`, `parse_site`: `/^module[ \t]/ { m = $2 }`.
  - The comment at `syn/yosys/run.sh:163-165`: "sv2v writes each module as `module NAME`
    at the start of a line however its source lays the header out".
  - The PR body, §1: "sv2v writes each header as `module NAME` at the start of a line
    however the source lays it out, so a header split across lines still counts", and "A
    parse failure names the module of all.v that holds the cited line".
- **Evidence** (`scripts/census_probe.sh`, `receipts/census/`, `receipts/sv2v-forms/`).
  Each case adds one file under `hdl/top/` that holds an instance of an undeclared module,
  then runs the tree's own `syn/yosys/run.sh`:

  | Header form | Gate result |
  |---|---|
  | split; `module automatic` split; `/* */` between keyword and name; `//` comment then the name on the next line; `macromodule` | rc 1 each, named by the census |
  | split header added to `tops` | rc 1, `YOSYS FAIL KL_r449_split` |
  | **`(* keep_hierarchy = "yes" *) module KL_r449_attr (...)`** | **rc 0, 42 YOSYS OK, `parsed 1 time(s)`, `YOSYS XILINX OK`** |
  | **the attribute on its own line, `module` on the next** | **rc 0**. sv2v joins them, so all.v reads `(* keep_hierarchy = "yes" *) module KL_r449_attrline (clk_i);` |
  | the attributed module also added to `tops` | rc 1, `tops array names modules that no longer exist under hdl/: KL_r449_attr`. The census refuses the only remedy it prints |
  | `module automatic KL_r449_allvauto` in `tops` | rc 1, `YOSYS FAIL all.v in module automatic: all.v:20749: ERROR: syntax error, unexpected TOK_AUTOMATIC ...`. The module is misnamed. yosys 0.66 cannot parse the lifetime keyword at all, so red is the outcome; only the name is wrong |
  | the attributed module, on a tree at `54f9411` (`r1-c-attr`) | rc 0. Present since round 1, and missed by R449-1 |

  - `receipts/sv2v-forms/a.v`: sv2v 0.0.13 writes `(* blackbox *) module KL_t_attr2 (clk_i);`
    and `module \KL_t_esc+  (clk_i);`. The census regex matches neither (an escaped
    identifier is a second, rarer escape).
  - At this head nothing escapes. Every `module` keyword in all.v starts its line, and the
    census holds 42, equal to the `$abstract` modules in yosys's own `ls`.
  - The codebase already uses Xilinx attributes on declarations (`(* ram_style ... *)`,
    `(* ASYNC_REG ... *)`). A module-level `keep_hierarchy` or `DONT_TOUCH` is the same
    idiom, and it is legal SystemVerilog: `{ attribute_instance } module_keyword ...`.
- **Authority:**
  - #25 acceptance bullet 1: "a check fails the gate if that ever stops being true".
  - #25 acceptance bullet 3: "A failure names the module it failed on".
  - Round-2 assignment item 2, "A layout-independent census".
  - R449-1 F2's required outcome: "derive `declared` in a way that does not depend on header
    layout".
- **Impact:** a legal declaration form removes a module from Yosys elaboration while the
  gate stays green. That is the gap #25 exists to close: with `-defer`, the tops array is
  the only elaboration coverage. For such a module the census then forbids the fix it
  prints. The PR body and the run.sh comment assert a layout guarantee that does not hold.
- **Required outcome:**
  - Derive the declared names so that a leading attribute instance does not hide a module.
    For example, strip a leading `(* ... *)` before the match. Another option is to list
    the modules from yosys's own `read_verilog -defer all.v; ls`. `receipts/sv2v-forms/c-yosys-ls.txt`
    shows it lists the attributed module as `$abstract\KL_t_attr2`, though a `(* blackbox *)`
    module is omitted from it.
  - Use the same extraction in `parse_site`, so that `module automatic NAME` and an
    attributed header are named NAME.
  - Correct the run.sh comment and the PR body sentence, and add the attributed-header rows
    to the red-proof table.
- **Verification:** use `scripts/census_probe.sh <head-tree> <work> <form> [top]`:
  - `attr` and `attrline` give rc 1, naming `KL_r449_attr` / `KL_r449_attrline`.
  - `attr top` gives `YOSYS FAIL KL_r449_attr: ...`.
  - `allvauto` names `KL_r449_allvauto`, not `automatic`.
  - The 21 cases of `scripts/yosys_fault.sh` stay as in `receipts/faults/SUMMARY.md`.

### S1 - SUGGESTION - the parent's own census still reads `.sv` text

Parent `scripts/check_rtl_source_lists.py` `declared_modules()` still matches
`^\s*module\s+NAME` per line of each `.sv`. It now disagrees with the processor's all.v
census on split, `automatic` and attributed headers. This is outside this PR. A parent
follow-up could read the same source of truth.

### S2 - SUGGESTION - the yosys leg of `elab_bounds.sh` never runs hosted

`.github/workflows/hdl.yml` installs yosys and sv2v only in `portability`, which does not
run `tb/nvm_port`. The `suites` job therefore always prints `YOSYS SKIP`. The class check
alone still kills `$error` and `$warning`, as the `-noyosys` rows below show, so this
weakens nothing that is graded today. Running `elab_bounds.sh` in `portability` would
exercise the Yosys claim on the hosted yosys 0.33.

## Prior public findings at this head

| Finding | Severity | State at `cd08ca7` | Evidence |
|---|---|---|---|
| R449-1 F1 = R448-1 F1: c10 leaves the parent `check_rtl_source_lists.py --selftest` red | MAJOR | **Resolved** | the parent tests and mutants below |
| R449-1 F2: a split header escapes the census | MINOR | **Resolved as filed**; the required outcome ("does not depend on header layout") is **not fully met**, and the remainder is retained as R449-2 F1 | `own-newmod` is rc 1 and named (was rc 0); `c-attr` and `c-attrline` are rc 0 |
| R449-1 F3 = R448-1 S1: the bound is a mirrored literal | MINOR / SUGGESTION | **Resolved** | `KL_pp_nvm_port.sv:196-200`. My unchanged `nvm_bound_probe.sh`: `pristine` equals round 1's `derived` row (elab rc 0, yosys 65527 rc 0 / 65528 rc 1), and `hdr10` gives elab rc 1 `ELAB FAIL MAX_PAYLOAD_P=65527` |
| R449-1 F4: `$error`/`$warning` pass the bench | MINOR | **Resolved** | the probe's `err` and `warn` give elab rc 1 (were 0). Mutants are below |
| R448-1 F2 + R449-1 R2: stale `KL_pp_nvm_port.sv` citations | MINOR / RESIDUE | **Resolved** | the citation audit below |
| R448-1 S2: `protocol_processor_top.sv:2714` | SUGGESTION | **Resolved** | `tb/nvm_port/README.md:106` cites `:2726`, which is `KL_acmp_nvm_shadow #(` |
| R449-1 R1: run.sh "status files" | RESIDUE | **Resolved** | `run.sh:9-10` carries the exact text |
| R449-1 R3: parent `CODE_QUALITY.md:612-616` | RESIDUE | **Resolved in the adoption deliverable** | the amended c10 patch carries the exact text. It lands at adoption |
| R449-1 S1: other module-scope `$error` guards | SUGGESTION | **Out of scope** (scope decision 5969440297: issue #151) | unchanged; not graded here |

## Evidence

### Parent adoption (F1 of round 1)

Scratch parent: milan-fpga dev `1269cdaf` from a fresh clone (984 index entries), with
gptp-processor `5dce647a` and verilog-axis `48ff7a7e` at their pins, and protocol-processor
at `cd08ca7` with its gitlink recorded. c8, then p2, then the amended c10
(`author-r2/parent-adoption-c10-1269cdaf.patch`, sha256 `55e62329...`) were each applied
after a clean `git apply --check`. The patch changes four files, as the parent-visible list
says. Its self-test bullet names the change.

| Command | c8 + p2 | + c10 |
|---|---:|---:|
| `check_rtl_source_lists.py` | 1 (six `STALE RECORD`) | **0** (`protocol-processor 42/42 tops, 0 recorded`) |
| `check_rtl_source_lists.py --selftest` | 1 (47/49) | **0 (50/50)** |
| `pp_srcs.py --check --selftest` | 0 | 0 |
| `check_entity_shape.py --self-test` | 0 | 0 (219 checks) |
| `check_todo_ownership.py --selftest` | 0 | 0 (45/45) |
| `check_port_contracts.py` | 0 | 0 (processor 1,756 ports, 111 <= 111) |
| `check_sh_idiom.py` | 0 | 0. With the processor at `54f9411` (gitlink set): rc 1, `run.sh` unquoted expansion = 2 and top-heavy = 1. `cd08ca7` fixes it, as stated |

The self-test was graded on the synthetic population with
`scripts/parent_gate3_mutants.sh` (`receipts/parent/gate3-mutants/`). Each case below is a
scratch copy of the c10 parent:

| Case | gate 3 | self-test | Arm that catches it |
|---|---:|---:|---|
| pristine | 0 | 0 (50/50) | |
| `verdict()` drops `STALE RECORD` lines | 0 | **1** | only the new arm "its record left behind ... reaches the verdict as STALE RECORD" |
| `STALE RECORD` not counted as a finding | 0 | **1** | the same new arm |
| `compare_tops` stale = [] | 0 | **1** | the old arm 43 and the new arm 49 |
| `verdict()` drops `TOPS DRIFT` lines | 0 | **1** | arm 37 and the new arm 48 |
| `TOPS DRIFT` not counted | 0 | **1** | arms 37 and 48 |
| `compare_tops` unrecorded = [] | 0 | **1** | six arms, including 48 |
| planted stale record (`KL_srp_top` recorded while a top) | **1** `STALE RECORD` | 1 | |
| planted unrecorded omission (`KL_srp_top` dropped from `tops`) | **1** `TOPS DRIFT` | 1 | |
| that omission recorded | 0 (debt, as designed) | 0 | |

### Census (round-2 item 2)

- all.v is exactly what yosys reads. `census()` reads `$work/all.v`, the single sv2v output
  that the elaboration (`read_verilog -defer all.v`) and the XILINX regression
  (`read_verilog all.v`) both read. sv2v is given every `*.sv` under `hdl/`: packages first,
  then the rest. A module in a non-`.sv` file, or in an inactive `` `ifdef ``, reaches
  neither the census nor yosys.
- Split headers, `module automatic`, comments between the keyword and the name, and
  `macromodule` are all counted (`receipts/census/SUMMARY.md`). A leading attribute is not
  counted (F1).

### Unchanged round-1 probes (`receipts/faults/`)

`scripts/yosys_fault.sh` and `fault_batch_one.sh` are byte-identical to R449-1's. All 21
jobs of `jobs.txt` were run (18 on the head tree, 3 on base). Normalised for all.v line
numbers and `$paramod` hashes, every row's rc, OK count, parse count and first FAIL lines
equal R449-1's table, except `own-newmod`:

- at R449-1: rc 0, 42 OK;
- now: rc 1, `modules declared under hdl/ with no entry in the tops array: KL_r449_newmod`.

`own-killonce` and `own-rcone` still give a verdict for every top. `h-allv` still names
`KL_srp_top`.

### `MAX_PAYLOAD_P` (round-2 items 3 and 4)

- **The guard** (`KL_pp_nvm_port.sv:196-200`):
  - `localparam int unsigned MAXP_BOUND_C = (1 << $bits(dev_len_o)) - 1 - int'(HDR_LEN_C)`.
  - It is used in the condition, and printed by `%0d` in the message together with
    `HDR_LEN_C`.
  - 65527 now appears only in the bench and in prose.
  - The round-2 hunks keep the line count (+11 -11), so no line below them moved.
- **No logic.** `scripts/port_netlist.sh` produces the sv2v + yosys netlist
  (`proc; opt; opt_clean -purge; rename -enumerate`) of `KL_pp_nvm_port` at `54f9411` and
  at `cd08ca7`. It is byte-identical at `MAX_PAYLOAD_P` = 1024 and at 65527
  (`receipts/netlist/summary.txt`).
- **Mutants against `tb/nvm_port/elab_bounds.sh`** (`scripts/elab_mutants.sh`, pinned
  Verilator 5.050, `receipts/elab/`):

  | Mutant | rc | First failing line |
  |---|---:|---|
  | pristine; pristine without sv2v or yosys on PATH | 0; 0 | (`YOSYS OK`; `YOSYS SKIP`) |
  | guard deleted; bound + 1; `> BOUND + 8`; `initial` placement | 1 each | `GUARD FAIL MAX_PAYLOAD_P=65528 elaborated` |
  | `>=` | 1 | `ELAB FAIL MAX_PAYLOAD_P=65527` |
  | message without the bound | 1 | `failed without naming the parameter and its bound` |
  | `$error` (with yosys / without) | 1 / 1 | `refused as %Warning-USERERROR, not as %(Warning-USERFATAL\|Error)` |
  | `$warning` (with / without) | 1 / 1 | `refused as %Warning-USERWARN ...` |
  | `$info` (with / without) | 1 / 1 | `GUARD FAIL ... elaborated` |
  | `HDR_LEN_C` = 10 | 1 | `ELAB FAIL MAX_PAYLOAD_P=65527` |
  | `$fatal(0, ...)` | 0 | equivalent: still a fatal |

  The PR's nine mutants are all among these, and all are killed. In this run, the
  unchanged `nvm_bound_probe.sh`'s `derived` variant could not apply its round-1 edit,
  because its assertion targets the old literal text. That row is therefore a second
  pristine row, as expected.

### Citations (round-2 item 5)

Every citation into `KL_pp_nvm_port.sv` in the repository at base and at head was listed
(`git grep`), along with every bare `` `:N` `` in `tb/nvm_port`. For each one, the cited
base line was compared with the cited head line:

- `:234-245`→`:244-255` (README:226, sim_main.cpp:1443);
- `:340-344`→`:350-354` (README:1135, sim_main.cpp:1441, measure_figures.py:117);
- `:436-439`→`:446-449` (sim_main.cpp:1328);
- `:366`→`:376` (README:407);
- `:380`→`:390` (README:413);
- all twelve ARMS (each `if (dev_err_i) begin`).

All of these are content-identical. `:33-34` lies above every hunk and is unchanged.
`README.md:97-99`'s citations are into `KL_acmp_nvm_shadow.sv`, which did not change. No
citation lands in `:114-190`, the range that moved by one. The PR body's site table is
correct and complete.

### Head gates (focused, pinned Verilator 5.050, sv2v 0.0.13, yosys 0.66)

| Command | rc | Result |
|---|---:|---|
| `syn/yosys/run.sh` | 0 | 42 YOSYS OK, `parsed 1 time(s)`, `YOSYS XILINX OK` (jemalloc) |
| `syn/yosys/run.sh --selftest-alloc` | 0 | PASS |
| `make -C tb/nvm_port` (elab + suite) | 0 | 4 ELAB OK, 6 GUARD OK (class printed), YOSYS OK; 1,219/1,219 |
| `measure_figures.py --check` (scratch git clone at the head) | 0 | "all measured figures agree with the tree", 160 builds (393-check baseline), 969 s, run alone |
| `scripts/lint_hdl.sh` | 0 | 41 LINT OK |
| `make check` | 0 | 41 mermaid + 18 wavedrom, 1,105 links, 115 REQ / 17 GAP, 94 rows 0 untested, 28 parameters |
| `scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |

### Hosted CI at the exact head (read only)

Read at about 15:40 UTC (`receipts/ci/`). Workflow `hdl` ran twice at `cd08ca7`: run
37132412884 (pull_request) and run 37132410209 (push).

- `docs-gates`: success in both runs.
- `portability`: success in both runs. The PR run's log shows yosys 0.33, the system
  allocator, 42 OK, `parsed 1 time(s)` and `YOSYS XILINX OK`.
- `suites`: **in progress in both runs**. In the PR run, lint plus every suite had succeeded
  and the SRP campaign was running. Hosted green is not yet established.

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #25 acceptance bullets 1 and 3 against the all.v census and the parse-site naming; #17 ("fails elaboration", bound named); round-2 assignment items 1-5; scope decisions (#151 owns the other `$error` guards, #22 relates) | R449-2 | cd08ca7b3d962ab040d8aaa023c57e7b0e010a6d |
| RTL | CLEAN | `KL_pp_nvm_port.sv:109-114, 189-200` (derived bound, message, placement); netlist identity `54f9411` vs head at 1024 and 65527; no port, parameter-meaning or logic change in round 2 | R449-2 | cd08ca7b3d962ab040d8aaa023c57e7b0e010a6d |
| Robustness | UNCLEAN (F1) | `syn/yosys/run.sh` census and `parse_site` over 11 header forms; 21 unchanged fault cases; parse-once loop and resume after the function refactor; parent adoption at 1269cdaf + c8 + p2 + c10 with 10 checker/data cases | R449-2 | cd08ca7b3d962ab040d8aaa023c57e7b0e010a6d |
| Tests | UNCLEAN (F1) | the PR's red-proof table (no attributed-header row); `elab_bounds.sh` against 16 mutant runs; the parent self-test against 6 code mutants and 3 data plants; `make -C tb/nvm_port`; figures gate; lint; matrix | R449-2 | cd08ca7b3d962ab040d8aaa023c57e7b0e010a6d |
| Docs | UNCLEAN (F1) | the PR body (§1-§4, round-2 table, parent-visible list) against receipts; the run.sh comments; `tb/nvm_port/README.md` and Makefile; the 09 §8.6 row; the full moved-citation set; the c10 patch's CODE_QUALITY.md text; `make check` | R449-2 | cd08ca7b3d962ab040d8aaa023c57e7b0e010a6d |

## Limits

- **Parent consumer set.** In a scratch parent I ran gates 3 (with its self-test), 4
  (`pp_srcs.py --check --selftest`) and 5, the `check_entity_shape` and
  `check_todo_ownership` self-tests, and `check_sh_idiom.py`. I did not run gates 1, 2,
  6-16, or `xvlog_gate.py` and its self-test (xvlog is not on this host's PATH). I also did
  not run the full parent, PP, gPTP, Yosys or builder banks. This is within the allowed
  scope. The manager's published bank results stand for those.
- **Suites and campaigns.** I did not run `./scripts/run_suites.sh` or the mutation
  campaigns. Round 2 changes no file that they build beyond `KL_pp_nvm_port.sv`, which
  `make -C tb/nvm_port` and the figures gate cover.
- **Earlier items.** Items 3 and 4 (#22 reorder, #37 NSD) did not change in round 2. They
  rest on R449-1's evidence at `54f9411`.
- **Clause conformance.** The IEEE 1722.1-2021 and Milan v1.2 PDFs were not consulted.
- **Hardware.** Physical calibration NOT RUN. Field skips are not hardware proof. No
  hardware was used.
- **Host load.** The host was shared, with a load average of 13-20. No timing claim is made.

## Pending manager duties

- F1 needs author rework and a new review round. S1 and S2 are optional.
- Tell R448-2 that its figures-gate process was terminated by this reviewer at about
  15:56 UTC (see Integrity), so that step can be rerun.
- Confirm that the hosted `suites` jobs (push 37132410209 and pull_request 37132412884)
  finish green at the exact head.
- Build the final current-dev candidate at the merge turn (source base `f4167536`, live dev
  `bbf704ec`). Source validation here does not cover it.
- Carry the amended c10 patch, including R449-1 R3's text, into the parent adoption after
  c8 and p2. Close PR #26 at merge. Carry #22's three remaining files, and #25's
  yosys/sv2v pinning note, forward.

## Integrity

After every probe (last checked 2026-10-03T16:14Z), the isolated review clone
(`receipts/integrity.txt`):

- is detached at `cd08ca7b3d962ab040d8aaa023c57e7b0e010a6d`, tree
  `e0b4807f1a6e2254a495f147f28e55e86d08f0bf`;
- has `git status --porcelain --ignored` empty;
- has an index equal to `git ls-tree -r HEAD`;
- has all 504 tracked files re-hashed with `git hash-object --no-filters`, with every blob
  and mode equal to the index.

The repository has no gitlinks, so no submodule pin applies. The clone was only read:
`git archive`, `git show` and local clones into `scratch/`. Every probe, the scratch parent
and its submodule checkouts lived under the packet's `scratch/`, and I edited no other
checkout.

**Incident on the shared host.** During cleanup of my own figures run, I used a
command-line pattern to stop it. The pattern also terminated a concurrent reviewer's
figures-gate process: R448-2's `measure_figures.py --check` under that reviewer's own
packet scratch directory. I wrote nothing into that packet. That reviewer's figures
receipt for this round may be missing or truncated and may need a rerun. My own figures
result above comes from a separate, later run that ran alone in a fresh clone; an earlier
overlapping pair of my own runs was discarded.

## Receipts

Every published file is listed in `MANIFEST.sha256`. Absolute paths in receipts are
rewritten to `<packet>`, `<scratch>`, `<review-clone>`,
`<pinned-verilator-5.050>` and `~`.

R449-2 FINISHED
