[R449] NEGATIVE - exact head 54f9411ab9a4b4aea58393f7fa1303ddcc96ee3c

# R449-1: external independent review of PR #149 (issue #25, lane C10)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #149, head
  `54f9411ab9a4b4aea58393f7fa1303ddcc96ee3c`, tree `419d056441b96802ec72c1671cc25abbd25ad4d5`,
  base `f4167536d358c996f4e1b70b875879c1651f85d3`. Review start: PR #149 comment 5968846991.
- Reconstructed from: README.md, docs/README.md (the repository has no AGENTS.md or
  CONTRIBUTING.md), issue #25 body and its comments (including the lane assignment
  5967291597), issues #17, #22, #37 and PR #26, the PR body, `git diff f4167536..54f9411`
  and per-commit history, and the public evidence at kebag-logic/milan-fpga
  `2a54253e:review-evidence/ppC10-r1` (five files, every sha256 equal to its MANIFEST.json
  entry; the published PR-BODY.md equals the live PR body).
- Every result below was re-executed by this reviewer in scratch copies unless marked
  "read only". Raw receipts are under `receipts/`, scripts under `scripts/`, the two extra
  microcode arms under `receipts/item4/`.

## Verdict

NEGATIVE. The four items do what the PR says at the processor head: the Yosys gate covers
all 42 modules, parses once, names every failing top and still gives the rest a verdict;
the replayed fault table matches the PR row for row; the allocator cannot change a
verdict; the reorder is behaviour-neutral (my own Vivado OOC netlist is byte-identical to
base apart from its Date line, the same hash the PR gives); the NSD arm is
defect-sensitive and the dispatch campaign is 40/40 with the one moved count reproduced.
No logic is added. Hosted portability and docs-gates are green at the head.

Four findings stay open, and any one of them makes the verdict NEGATIVE:

- F1 (MAJOR): adopting the PR with `parent-adoption-c10-1269cdaf.patch` leaves the parent's
  `check_rtl_source_lists.py --selftest` red. The parent's docs workflow runs that
  self-test, and the consumer evidence did not include it.
- F2 (MINOR): the new census misses a module declared with `module` and its name on
  separate lines, so a fault inside that module passes the gate with rc 0.
- F3 (MINOR): the `MAX_PAYLOAD_P` refusal repeats 65527 as a literal. It is not derived
  from the field width.
- F4 (MINOR): `elab_bounds.sh` does not grade the `$fatal` choice. A `$error` or
  `$warning` mutant survives it, and with either one Yosys accepts 65528.

## Findings

### F1 - MAJOR - Tests, Robustness, Docs - the c10 adoption patch leaves a parent CI gate red

- Artifact: `review-evidence/ppC10-r1/author/parent-adoption-c10-1269cdaf.patch` (sha256
  `6870d2ed...e304b`). It touches only `scripts/processor_yosys_tops.budget` and
  `scripts/xvlog.budget`. Also the PR body, "Parent consumer set (16)" and
  "Parent-visible list" item 2.
- Evidence: I built a scratch parent at milan-fpga dev `1269cdaf` (984 index entries)
  with gptp-processor `5dce647a` and verilog-axis `48ff7a7e`, and the processor gitlink
  set to `54f9411`. The submodules were registered, `git submodule status` was clean, and
  c8, then p2, then c10 were applied, each after a clean `git apply --check`. Results are
  in `receipts/parent/summary.txt`:
  - At dev `1269cdaf` with its own pin `631eeb34`: `check_rtl_source_lists.py` rc 0 and
    `--selftest` rc 0 (49/49).
  - With c8 + p2: gate 3 rc 1 with six `STALE RECORD` lines, and gate 9 rc 1 with
    `BANK IT ... srp_class_a_prio_w`. Both are as the PR states.
  - With c8 + p2 + c10: gate 3 rc 0 (`protocol-processor 42/42 tops, 0 recorded`), gate 4
    rc 0, gate 5 rc 0 (1,756 ports, 111 <= 111), gate 9 rc 0
    (`PASS (3 finding(s) == ratchet)`), and the gate 5 and gate 9 self-tests rc 0. But
    **`check_rtl_source_lists.py --selftest` rc 1, 48/49**:
    `[FAIL] the record is non-empty at this pin, so the refusal arms grade a live population`.
    The arm is at parent `scripts/check_rtl_source_lists_selftest.py:378-379` and requires
    `bool(l_rec)`. The c10 patch empties the record, which is this PR's intended effect.
  - Parent `.github/workflows/docs.yml:263-264` runs both
    `check_rtl_source_lists.py` and `check_rtl_source_lists.py --selftest` in one step
    ("RTL source-list drift gate").
- Impact: the PR says adopting this head needs the c10 patch "after c8 and p2", and that
  gates 1-9 and 11 re-ran rc 0 with it. An adoption done exactly that way turns the
  parent's hosted docs workflow red. The 16-gate consumer set ran gate 3 without its
  self-test, so it does not cover the patch.
- Required outcome: the adoption deliverable also amends the parent self-test arm. For
  example, replace the "record non-empty" arm with a synthetic recorded omission, or
  assert that an empty record means every declared module is a top. Then re-run
  `check_rtl_source_lists.py --selftest`, and every other self-test in the parent workflow
  that reads either budget, at `1269cdaf` + c8 + p2 + c10, and record it in the PR body's
  consumer table.
- Verification: in that scratch parent,
  `python3 scripts/check_rtl_source_lists.py && python3 scripts/check_rtl_source_lists.py --selftest`
  both rc 0.

### F2 - MINOR - Robustness, Tests, Conformance - the census misses a module whose name is on the next line

- Artifact: `syn/yosys/run.sh:157-158`
  (`grep -rhoE '^[[:space:]]*module[[:space:]]+[A-Za-z_][A-Za-z0-9_]*'`). The regex is
  matched one line at a time.
- Evidence: probe `own-newmod` (`receipts/faults/own-newmod.gate.log`,
  `scripts/yosys_fault.sh ... newmod KL_r449_newmod`). It adds `hdl/top/KL_r449_newmod.sv`,
  declared as `module` with `KL_r449_newmod (input wire clk_i);` on the next line, and
  containing an instance of an undeclared module. sv2v accepts the file and emits
  `module KL_r449_newmod (clk_i);` into all.v. The census does not see the module, and
  `read_verilog -defer` never elaborates it because it is no top. The gate prints
  **rc 0, 42 YOSYS OK, `parsed 1 time(s)`, `YOSYS XILINX OK`**. In the same tree,
  `scripts/gen_matrix.py` (a multi-line-aware `\s+` under `re.M`) does see the new module.
  At the head the census equals the module set of sv2v's all.v (42 = 42), so nothing
  escapes today.
- Authority: #25 acceptance bullet 1: "a check fails the gate if that ever stops being
  true". The run.sh comment at :140-141 says "a new module cannot be added without a top".
- Impact: a legal SystemVerilog declaration form removes a module from Yosys elaboration
  without any red, which is the gap #25 exists to close. With `-defer`, the tops array is
  the only elaboration coverage.
- Required outcome: derive `declared` in a way that does not depend on header layout. For
  example, read `^module NAME` from the sv2v output the gate already builds, before the
  first yosys, or match across newlines as gen_matrix does. Add a planted split-header
  module to the PR's red-proof table.
- Verification: `scripts/yosys_fault.sh <head-tree> <work> newmod KL_r449_newmod` gives
  rc 1, with the module named either by the census or by a `YOSYS FAIL` line.

### F3 - MINOR - RTL, Robustness - the `MAX_PAYLOAD_P` bound is a mirrored literal

- Artifact: `hdl/packet_engine/KL_pp_nvm_port.sv:197-198`:
  `if (MAX_PAYLOAD_P > 65527)` and the message text `"... is above 65527 ..."`. The values
  it stands for are `dev_len_o`'s 16 bits (`:162`) and `HDR_LEN_C = 16'd8` (`:182`).
- Evidence (`receipts/item2/`, `scripts/nvm_bound_probe.sh`):
  - Variant `derived` uses
    `localparam int unsigned MAXP_BOUND_C = (1 << $bits(dev_len_o)) - 1 - int'(HDR_LEN_C)`
    with the same `$fatal`, printing the bound by `%0d`. It gives `elab_bounds.sh` rc 0
    (65527 is printed, so the shipped grep still matches), sv2v rc 0, Yosys rc 0 at 65527
    and rc 1 at 65528. These are the same outcomes as pristine, and the bound is an
    elaboration constant, so no logic is added.
  - Variant `hdr10` changes `HDR_LEN_C` to 10 and keeps the shipped guard.
    `elab_bounds.sh` still passes, and 65527 still elaborates although 10 + 65527
    overflows 16 bits. The mirror does not follow the field.
- Authority: the lane's review focus for item 2 ("derived from the field width, not
  mirrored"), and the module's own banner, which states the bound as
  `8 + payload_length` fitting 16 bits.
- Impact: the guard and its message encode the arithmetic by hand. A future change to the
  header or the length field silently leaves a wrong bound that the bench still calls
  correct.
- Required outcome: compute the bound from `$bits(dev_len_o)` and `HDR_LEN_C` (or an
  equivalent single source) in both the condition and the message, and keep 65527 only
  in the bench as the specification value it checks against.
- Verification: after the fix, the `pristine` row of `scripts/nvm_bound_probe.sh` equals
  today's `derived` row, and its `hdr10` row shows the bound following the field:
  `elab_bounds.sh` rc 1, `ELAB FAIL MAX_PAYLOAD_P=65527`.

### F4 - MINOR - Tests, Robustness - `elab_bounds.sh` cannot tell `$fatal` from `$error` or `$warning`

- Artifact: `tb/nvm_port/elab_bounds.sh:47-68`. `refused()` passes on any non-zero
  Verilator `--lint-only -Wall` exit whose output contains `MAX_PAYLOAD_P=<v> is above 65527`.
- Evidence (`receipts/item2/SUMMARY.txt`):
  - Mutant `err` (`$fatal(1,` changed to `$error(`) and mutant `warn` (`$warning(`):
    `elab_bounds.sh` **rc 0, all 6 GUARD OK**, while sv2v + Yosys `chparam` at 65528
    gives **rc 0**, so the refusal is gone in the portability front end.
  - Pristine gives Yosys rc 1 at 65528 (`System task $finish executed`).
  - Verilator 5.050 reports all three as warnings: `%Warning-USERFATAL`,
    `-USERERROR` and `-USERWARN`. With `-Wno-fatal` all three exit 0. The bench therefore
    grades the message and not the severity.
  - The PR's own table shows that module-scope `$error` is missed by Yosys, and every
    other module-scope guard in `hdl/` uses `$error` (for example
    `KL_pp_nvm_port.sv:188-190` beside it). Harmonising this guard to house style is a
    plausible edit, and the bench would not notice it.
- Authority: #17 acceptance ("fails elaboration"). The PR claims defect sensitivity
  ("Five mutants each turn it red") and states that the `$fatal` placement was measured
  across front ends.
- Required outcome: the bench pins the fatal class. Either require `%Warning-USERFATAL`
  (or `%Error`) in the refused output, or add an sv2v + Yosys leg that requires rc 1 at
  65528 when those tools are present. Record a `$error` mutant as killed.
- Verification: `scripts/nvm_bound_probe.sh`: the `err` and `warn` variants give
  `elab_bounds.sh` rc 1, and pristine gives rc 0.

### R1 - RESIDUE - Docs - a stale comment in run.sh

`syn/yosys/run.sh:9-10` says "the yosys verdicts are read from status files and AND-OR
lists". Since `b5e3b97` there are no status files: the verdicts come from the
`@@begin`/`@@ok` markers in `gate.log`. Exact fix: replace "read from status files and
AND-OR lists" with "read from the markers in gate.log and AND-OR lists". This is wording
only.

### R2 - RESIDUE - Docs - one line citation in a test comment was not moved

`tb/nvm_port/sim_main.cpp:1443` still cites `` (`dev_cmd_owned_w`, :234-245) ``. After the
guard's ten lines that range holds `tmo_r` and the header-view comment, and
`dev_cmd_owned_w` is at `:244-255`, as `tb/nvm_port/README.md:222` already says. Exact fix:
`:234-245` becomes `:244-255`. `54f9411` moved the other five citation sites, and
`measure_figures.py`'s ARMS table is correct (all twelve lines are `if (dev_err_i)` arms of
the named states). This is a comment only.

### R3 - RESIDUE - Docs - parent prose made stale by the c10 adoption patch

Parent `docs/development/CODE_QUALITY.md:612-616` still says "The six are recorded there as
**drift at the pin** ... the pin bump that brings it in deletes the lines". After the c10
patch the record is empty. Exact fix: "The six recorded there from pin 3770ae02 were
**drift at the pin**, not helper exceptions; the processor's lane C10 (its issue #25)
named all six as tops, and the pin bump that brought it in deleted their lines, since a
recorded name that has become a top is refused as stale and an omission that is not
recorded is refused outright. The record can therefore only shrink." This is wording
only. The published lane handoff already notes it.

### S1 - SUGGESTION - module-scope `$error` guards are invisible to the Yosys front end

Outside this PR, `KL_pp_nvm_port.sv:188` (`g_tmo_check`), `KL_pp_originator.sv:148`,
`KL_pp_release_merge.sv:37`, `KL_srp_encoder.sv:147`, `KL_acmp_nvm_shadow.sv:537,544` and
`protocol_processor_top.sv:842-873` use module-scope `$error`. Per the PR's measurement and
my `err` variant, sv2v + Yosys elaborate through them. A follow-up issue could decide
whether those guards should be `$fatal` as well.

## Evidence by item

### Item 1 (#25): census, parse once, red proofs, allocator, wall time

- Census: all 42 declared modules are in `tops`. The census equals the module set sv2v
  writes to all.v at the head (42 = 42). `drop KL_srp_top` gives rc 1, "modules declared
  under hdl/ with no entry in the tops array: KL_srp_top". `bogus KL_r449_gone` gives
  rc 1, "tops array names modules that no longer exist under hdl/: KL_r449_gone". Both
  match the PR. The split-header gap is F2.
- Parse once (`run.sh:222-267`): one yosys runs `read_verilog -defer all.v; design -save`,
  then for each top `design -load; hierarchy -check -top T; proc; opt_clean`. That is
  base's per-top program, with `-defer` added. The XILINX/RAMB36 command line is
  byte-identical to base and passes in every green run (`YOSYS XILINX OK  KL_aecp_engine`).
- Replay of the PR's planted-fault table at the head (`receipts/faults/SUMMARY.md`): every
  row matches.
  - `KL_srp_top` gives FAIL `KL_srp_top`, then `protocol_processor_top`, with 40 OK and
    2 parses.
  - `protocol_processor_top` gives 41 OK and 1 parse.
  - `KL_acmp_nvm_shadow`, `KL_mrp_strip` and `KL_srp_admission` are each named, then
    their parents.
  - `KL_pp_dispatch_fifo` gives `KL_pp_dispatch`, `KL_pp_dispatch_fifo`, then
    `protocol_processor_top`.
  - Two faults give four FAIL lines and `parsed 4 time(s)`.
  - A syntax fault in all.v gives `YOSYS FAIL all.v in module KL_srp_top: all.v:19241 ...`,
    then 42 "not elaborated". My line number differs from the PR's 20318 only because I
    planted the fault at a different place.
  - At base `f4167536`, the faults in `KL_srp_top` and `protocol_processor_top` give
    rc 0 (missed), as stated.
- My own faults, in modules the table does not list:
  - `KL_pp_nvm_mgr_arb`, undeclared instance: rc 1, FAIL `KL_pp_nvm_mgr_arb`, then
    `protocol_processor_top`, 40 OK. The system allocator run gives identical lines.
  - `KL_pp_acmp_lsn_admit`, an always-firing module-scope `$fatal`: rc 1, named, then
    `protocol_processor_top`, 40 OK.
  - `KL_aecp_desc_mem_guard`, an instance with a non-existent port, and
    `KL_pp_acmp_lsn_admit`, an instance with a non-existent parameter: rc 1, refused by
    sv2v, which names the instance and the target module.
  - yosys SIGKILLed once during `KL_pp_maap`: rc 1,
    `YOSYS FAIL KL_pp_maap: yosys exited 137 with no ERROR line`, and the other 41 still OK.
  - yosys exiting 1 after a clean run: rc 1, "every top passed, but yosys exited 1".
  - Every red run still prints a verdict for all 42 tops.
- Allocator: the head's verdict lines are identical under jemalloc and under
  `YOSYS_MALLOC=none`, both pristine and with a fault. An explicit missing library gives
  rc 2, and an explicit unloadable file gives rc 2 with the loader's complaint.
  `--selftest-alloc` PASS. The hosted portability job ran with the system allocator on
  yosys 0.33 and printed 42 OK, `parsed 1 time(s)`, `YOSYS XILINX OK`. A verdict comes only
  from an `@@ok` marker that yosys prints after the top's commands succeed, together with
  the yosys exit code, so a preload cannot turn a failure into a pass.
- Wall time, measured: one round each, alone on this host (load average 9-14 from other
  tenants), end to end (`receipts/timing/`):

  | Revision | Tops | This review | PR median |
  |---|---:|---:|---:|
  | head, jemalloc | 42 | 33.16 s | 35.97 s |
  | head, system allocator | 42 | 49.89 s | 48.12 s |
  | base `f4167536` | 36 | 91.28 s | 88.80 s |
  | merge `5c20350` (PR #26's pool) | 42 | 30.46 s | 30.00 s |

  These are consistent with the PR within host noise, peak RSS about 0.8 GB in each. The
  pool is faster than parse-once, and the PR reports that openly. Parse-once is the
  issue's conservative option B.

### Item 2 (#17)

- The guard is at module scope with `$fatal(1, ...)`. `elab_bounds.sh` at the head gives
  rc 0: 4 ELAB OK (1024 and 65527 among them) and 6 GUARD OK. 65527 elaborates in
  Verilator 5.050 lint and in sv2v + Yosys. 65528 is refused by both, by name and bound.
  Open: F3 (the bound is mirrored) and F4 (the severity is not graded).
- No logic: the default build is unchanged, because the OOC netlist is identical (item 3).
  The nvm_port suite at the head gives rc 0, 1,219 checks.

### Item 3 (#22)

- `34b5246` touches only `hdl/top/protocol_processor_top.sv`. The sorted multiset of its
  non-blank lines differs by one added comment line
  (`receipts/item3/ppt-sorted-multiset.diff`). `git diff 34b5246 54f9411 -- hdl` is empty.
- xvlog 2026.1, packages first, one module file per invocation
  (`receipts/item3/xvlog-*.txt`): base 37/41 and head 38/41. `protocol_processor_top.sv`
  goes from `VRFC 10-3380 srp_class_a_prio_w` (:935) to clean. The three remaining
  failures are `KL_aecp_notify.sv:557`, `KL_pp_originator.sv:194` and
  `KL_pp_rx_validator.sv:383`, as the PR says.
- Vivado 2026.1 OOC (`syn/ooc/protocol_processor_ooc.tcl` through
  `scripts/ooc_netlist.tcl`, run alone, base then head, 171 s and 173 s): the netlist is
  19,508,014 bytes for both, and its sha256 without the Date line is
  `4baf5a8ceff9979470e908d87527cddc87b1eb125b0282f3839b0f0411a4e200` for both, the PR's
  hash. The util.rpt bodies are identical except the Date line, and util_hier is identical
  too: LUTs 30,658, registers 31,944, LUTRAM 1,222, F7/F8 1,482/57, RAMB36/RAMB18/DSP
  23/2/4. `Synth 8-6901` goes from 51 to 7, and from 44 to 0 in
  `protocol_processor_top.sv`. The reorder is behaviour-neutral, and #22 correctly stays
  "Relates to".

### Item 4 (#37): conformance and defect sensitivity

- The AX NSD arm (`tb/pp_top/sim_main.cpp:11538-11562`) has 13 checks: holder_set 2,
  refused 4, GET 1, foreign 5 and unlock 1. It runs in the default and line builds, so it
  adds 26. `make run` at the head gives **9,222 checks, 0 FAIL** (AX 231 in the line
  build).
- Conformance: the arm checks that SET_CLOCK_SOURCE on an absent CLOCK_DOMAIN is answered
  NO_SUCH_DESCRIPTOR at cdl 20, byte-exact, with descriptor type and index echoed and
  `clock_source_index` 0, and that nothing is stored, marked, notified or sent unsolicited.
  This matches the frozen scope of #37 and `docs/architecture/06_aecp_engine.md:469`
  (lock, then locate, with no such CLOCK_DOMAIN giving NO_SUCH_DESCRIPTOR) and `:318`
  (a miss carries a zero-valued body). It cites IEEE 1722.1-2021 7.4.23.1 / Table 7-141
  and Milan v1.2 5.4.2.15. NSD3 checks that the lock outranks the miss, as 06 documents.
  The normative PDFs are not in this workspace (see Limits), so the clause wording was
  checked only against the repository's own citations.
- Dispatch campaign at the head (`aecp_dispatch_mutants.py --jobs 3`, pinned Verilator,
  379 s): **4 controls PASS, 40/40 KILLED**, `44 checks: 44 PASS, 0 FAIL`. Every arm's
  failure count equals the README table. The one moved count, `lk-sclks-miss-lock-nop`
  from 1 to 2, is LK4 plus NSD3, as the README now records. The three new arms fail
  NSD3 + LK4 (next-word), NSD1 + NSD3 (preload dropped, with LK4/LK5 passing) and
  NSD1 + LK5 (branch dropped), exactly as documented.
- My own arms (`receipts/item4/`):
  - `r449-sclks-miss-target-main-lock` (the miss branch aimed at the main-path
    CHECK_LOCK, E_SCLKS + 9): KILLED by NSD1 and LK5, which get BAD_ARGUMENTS where
    NO_SUCH_DESCRIPTOR is due.
  - `r449-sclks-miss-target-prev-word` (E_SCLKSRF - 1): 928/928 pass. This reproduces the
    PR's documented equivalence: word 1143 is NOP fill, which runs on into E_SCLKSRF's
    CHECK_LOCK.

### Parent adoption patch (c10)

`parent-adoption-c10-1269cdaf.patch` changes only two files of milan-fpga:

- It deletes the six `scripts/processor_yosys_tops.budget` lines (`KL_acmp_nvm_shadow`,
  `KL_mrp_strip`, `KL_pp_dispatch_fifo`, `KL_srp_admission`, `KL_srp_top`,
  `protocol_processor_top`) and puts that file's header sentence in the past tense.
- It regenerates `scripts/xvlog.budget`. The
  `protocol_processor_top.sv|VRFC 10-3380|srp_class_a_prio_w` key is removed, and the
  other three keys stay, with line notes 557 and 383 matching my xvlog run at the head.

It applies cleanly after c8 (builder and AEM files) and p2 (one design document). Neither
of those touches the two budgets. Gates 3, 4, 5 and 9 and the self-tests of 5 and 9 are
rc 0 with it. Coverage gap: the consumer set did not run `check_rtl_source_lists.py --selftest`,
which fails (F1). Prose left stale by the patch is R3. `receipts/evidence-sha256.txt`
records the five published evidence files, all equal to the evidence MANIFEST.json.

### Head gates (focused, pinned Verilator 5.050)

| Command | rc | Result |
|---|---:|---|
| `make -C tb/pp_top run` | 0 | 9,222 checks, 0 FAIL |
| `make -C tb/nvm_port` (elab + suite) | 0 | 4 ELAB OK, 6 GUARD OK; 1,219 checks, 0 FAIL |
| `tb/nvm_port/measure_figures.py --check` (in a scratch git clone at the head) | 0 | "all measured figures agree with the tree", 160 builds, 904 s. A first attempt in a history-less archive copy reported only `git-form pin: cannot read dc354be~1 / 62d96d6~1` (the gate needs history), with every measured row `[ok]` |
| `scripts/lint_hdl.sh` | 0 | 41/41 LINT OK |
| `make check` | 0 | 41 mermaid + 18 wavedrom, 1,105 links, 115 REQ / 17 GAP, 94 rows 0 untested, 28 parameters |
| `scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `syn/yosys/run.sh` (jemalloc / system) | 0 / 0 | 42 OK, parsed once, XILINX OK |

### Hosted CI at the exact head (read only)

Read at 2026-10-03 13:02 UTC (`receipts/ci/`). Workflow `hdl`, run 37120641243 (push)
and run 37120643855 (pull_request), both at `54f9411`:

- `docs-gates`: success in both runs.
- `portability`: success in both runs. This job executed `syn/yosys/run.sh` on yosys
  0.33 with the system allocator and printed 42 OK, `parsed 1 time(s)`, `YOSYS XILINX OK`.
- `suites`: **still in progress in both runs**. In the PR run the lint and every-suite step
  and the SRP, MAAP, ADP and AECP-mutant campaigns had succeeded and the dispatch campaign
  was running; the matrix and figures steps were pending. The cached Verilator build step
  was skipped by design. Hosted green at the head is therefore NOT yet established. It is
  listed under pending manager duties, and the open findings make this verdict NEGATIVE
  independently of it.

### Prior public findings

When the review started, PR #149 carried no review findings: its only comments were the
two review-start notices, and it had no review objects. PR #26, which this PR supersedes,
carried author comments only. There is nothing to resolve or retain.

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | #25/#17/#22/#37 acceptance; 06 §6.4 rows :318/:469; NSD arm vs IEEE 1722.1-2021 7.4.23.1 / Table 7-141 and Milan 5.4.2.15 as cited; census against #25 bullet 1 | R449-1 | 54f9411ab9a4b4aea58393f7fa1303ddcc96ee3c |
| RTL | UNCLEAN (F3) | `KL_pp_nvm_port.sv:110-200` guard; `protocol_processor_top.sv` reorder (multiset, xvlog, OOC netlist hash, util); no logic added | R449-1 | 54f9411ab9a4b4aea58393f7fa1303ddcc96ee3c |
| Robustness | UNCLEAN (F1, F2, F3, F4) | `syn/yosys/run.sh` census, parse-once loop, resume, kill/rc paths, allocator selection; 21 fault cases (18 at the head, one of them fatal-class; 3 at base); guard severity across front ends; parent adoption at 1269cdaf + c8 + p2 + c10 | R449-1 | 54f9411ab9a4b4aea58393f7fa1303ddcc96ee3c |
| Tests | UNCLEAN (F1, F2, F4) | dispatch campaign 44/44; 2 own E_SCLKS arms; pp_top 9,222; nvm_port suite, elab_bounds and 4 own guard variants; lint 41/41; parent gates 3, 3-selftest, 4, 5, 5-selftest, 9, 9-selftest | R449-1 | 54f9411ab9a4b4aea58393f7fa1303ddcc96ee3c |
| Docs | UNCLEAN (F1; R1-R3 are residue) | PR body (all tables) against receipts; tb/pp_top README AX/NSD and campaign table; tb/nvm_port README/Makefile; 09 §8.1/§8.6 rows; run.sh comments; line citations; `make check` | R449-1 | 54f9411ab9a4b4aea58393f7fa1303ddcc96ee3c |

## Limits

- The IEEE 1722.1-2021 and Milan v1.2 PDFs are not distributed with the repository and
  were not consulted. Clause conformance for NSD was checked against the repository's
  cited clauses, 06 §6.4 and #37's frozen scope.
- Wall time is one round per revision on a shared host (load average 9-14), not a median
  of three.
- Of the parent consumer set, I ran only gates 3, 4, 5 and 9 and the self-tests of 3, 5
  and 9, in a shallow scratch parent. I did not run gates 1, 2, 6-8 or 10-16, or the full
  parent, PP, gPTP, Yosys or builder banks. That is within the allowed scope; the
  manager's published bank results stand for those.
- I did not run `./scripts/run_suites.sh` or the other four campaigns (aecp, srp, maap,
  adp). They build none of the files this PR changes beyond those covered above.
- Physical calibration NOT RUN. Field skips are not hardware proof. No hardware was used.
- Vivado was used for xvlog analysis and two OOC syntheses, each run alone.

## Pending manager duties

- F1-F4 need author rework and a new review round. R1-R3 go to the residue checklist with
  the exact fixes above.
- Confirm that the hosted `suites` jobs (push and pull_request) finish green at the exact
  head. See the CI section for their state when this report was written.
- Build the final current-dev candidate at the merge turn (source base `f4167536`, live
  dev `bbf704ec`). Source validation here does not cover it.
- Close PR #26 at merge, as the PR states. Carry #22's three remaining files forward, and
  #25's note on pinning yosys and sv2v in the `portability` workflow, which is not done
  and not in its acceptance.

## Integrity

After every probe, the isolated review clone is detached at
`54f9411ab9a4b4aea58393f7fa1303ddcc96ee3c`, tree `419d056441b96802ec72c1671cc25abbd25ad4d5`,
with `git status --porcelain --ignored` empty. Index and worktree equal HEAD. All 504
tracked files were re-hashed with `git hash-object --no-filters`, and every blob and
executable mode matches the index, which matches `git ls-tree -r HEAD`. The repository
has no gitlinks (0 index entries of mode 160000), so no submodule pin applies. All probes,
the parent tree and the clones ran under the packet's `scratch/`, and no other checkout
was edited.

## Receipts

Every published file is listed in `MANIFEST.sha256`. Absolute paths in receipts are
rewritten to `<packet>`, `<scratch>` and `~`.

R449-1 FINISHED
