[R583] NEGATIVE - exact head 4a99c1e92ba74c3cbab87a2d6c414113311e743b

Round R583-4, external independent review of issue #665 lane F-INT, PR #704 (PR 1 of 2, the publication block).
Exact head `4a99c1e92ba74c3cbab87a2d6c414113311e743b`, tree `73e89cc4a550360d26f39b26b4d6ca8c5150ad65`.
Source base `7c1b52bee26b497080ee22b1c1986109f80a5ee7`; the head merges dev `554e61d2` (F5), so the PR's own
change is `git diff 554e61d2 HEAD` (56 files). Live dev at assignment: `e8454e2751d05b02ee8e5a571857589ab358ab86`.

The round-4 assignment ([#665 6094461419](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6094461419))
answered by `b2aa3ccf..232d4663` is the focus. The published head also carries round 4b (the dev merge,
`26370439`, `6cf5b8de`, `0ca1e397`, `4274a205`) and round 5 (`d8a24d08` to `4a99c1e9`, the cone rule of
[6095903333](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6095903333)). This review covers the
exact head, so it judges both rules as they stand there.

## Verdict in one paragraph

Every earlier finding is resolved or applied, except that the census's fail-closed rule still has gaps. All prior
reviewers' escaping probes are refused by name, run unmodified. The census gives 25 wires and 89 occurrences
(25 + 25 + 39), with 10 field, 14 status and 15 answer-face reads. The population really comes from the wrapper
instance and matches `KL_pp_shadow.sv`'s class-D sections, port for port. The `srpcmp` arm gates the comparator.
R582-2-R1 is applied word for word. The block's RTL, its writers and the round-5 tests hold. All PR plants were
re-run and every one is caught: ctrl 134/134; SRP 29/29 at two interfaces and 5/5 at one; AECP 2/2. The mbx RTL
table gives 175/175.

The census does not yet meet the rule its docstring, MAILBOX_SPLIT.md and the PR body state. 13 new probe forms,
each legal SystemVerilog that carries the class-D value in simulation, pass the census with zero findings:

- **R583-4-F1:** the procedural-block cone is wrong whenever the block has no outer `begin`.
- **R583-4-F2:** the first hop is fooled by escaped identifiers and by macros defined in an included file. A
  declaration initialiser also gets through as a second driver.

Both are MINOR. Nothing is misclassified in today's datapath: every one of its 62 procedural blocks opens
`begin` on its header line, and none of these forms occurs. The gap is in the standing guarantee the rulings
asked for, so Conformance, Robustness, Tests and Docs stay unclean.

## Findings

### R583-4-F1 - MINOR - Conformance, Robustness, Tests, Docs - the cone's procedural-block edges are lost when a block has no outer `begin`

- **Where:** `sw/mailbox/census_netlist.py:287-310` (`always_blocks`). With a body that is not `begin`, the block
  is taken as the first statement only, up to the first `;` (`:308`). Its event control is matched by
  `@\s*(\([^)]*\)|\*)` (`:296`), which stops at the first `)`. The rule this breaks is stated at
  `sw/mailbox/publication_census.py:52-57`, `docs/design/MAILBOX_SPLIT.md:886-889` and the PR body ("The cone fails
  closed at every node", "every target of the procedural block ... it lies in").
- **Authority:** ruling [6095903333](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6095903333)
  item 1 says to treat every occurrence of a cone node as an edge to every identifier the enclosing statement or
  block can drive. Ruling 6092086337 item 3 requires the census to fail on an unmapped wire-affecting read.
- **Evidence:** `scripts/r583_4_census_probes.py` gives `receipts/r583_4_census_probes.log`, 8 ESCAPE lines. From
  the status consumer `lwsrp_talker_declared` and from the answer-face consumer `gsi_tkdcl_w`, each of these forms
  drives a register that feeds another module's input port (the wire), and each passes with 0 findings:
  - `always_ff @(posedge axis_clk) if (X[0]) probe_a <= 1'b0; else probe_q <= 1'b1;`;
  - the same with `begin ... end` branches;
  - a begin-less `case (X[0]) ... default: probe_q <= ...; endcase`;
  - a `begin ... end` block whose event control nests parentheses (`@(posedge clk or posedge (rst))`).

  The same `if/else` inside an outer `begin ... end` is refused, and so is the gsi control (4 controls).
  `scripts/legality/legality_tb.sv` runs under the pinned Verilator 5.050 (`receipts/legality_run.log`, `LEGALITY
  PASS`). It shows that the begin-less else-branch register follows the condition: it holds while the condition
  is 1 and loads when it is 0.
- **Impact:** a status or answer-face read can reach the wire through an ordinary coding style, and the census
  still passes. That is the escape class R582-3-F1 = R583-3-F1 was raised for. Round 5 refuses the probes it was
  given, but not the rule's "enclosing block".
- **Required outcome:** a procedural block's extent, and so every target its reads can drive, covers its whole
  body whatever the form: a begin-less `if/else`, `case`, nested statements and parenthesised event controls. If
  the extent cannot be established, the census fails closed, either refusing the block or counting its reads as
  reaching the wire. The self-test refuses each begin-less form above by name, from a status consumer and from an
  answer-face consumer, beside a begin/end control.
- **Verification:** `python3 -I r583_4_census_probes.py <export>`, unmodified, reports no ESCAPE on the eight F1
  lines. `publication_census.py --check --selftest` passes with the new arms.

### R583-4-F2 - MINOR - Conformance, Robustness, Tests, Docs - first-hop escapes: escaped identifiers, macros defined in an included file, and a declaration initialiser as a second driver

- **Where:**
  - `sw/mailbox/census_netlist.py:61-85` (`strip_comments`) treats `//`, `/*` and `"` as comment or string
    openers even inside an escaped identifier. IEEE 1800-2017 5.6.1 says an escaped identifier runs from `\` to
    white space and may hold any printable character.
  - `sw/mailbox/publication_census.py:435-448` (`outright`) looks for a token paste and a hierarchical reference
    only in the datapath text. `:483-490` checks an included file only for a literal population-wire name.
  - `:468-482` counts a population wire's initialised declaration (`wire w = expr;`) as its declaration.
  - The rule is stated at `publication_census.py:25-40` and `docs/design/MAILBOX_SPLIT.md:862-874`: "Any other
    occurrence fails, whatever its syntactic form ... a second driver, and any form not yet written. A form the
    parser does not understand is therefore refused, never skipped", and a token paste and a hierarchical
    reference "each fail wherever it appears". The same wording is in the mbx README (`tb/verilator/mbx/README.md`,
    item 1) and in the PR body ("Every occurrence is accounted for"). The PR body's limits name only reads from
    outside the datapath and its includes.
- **Authority:** round-4 assignment [6094461419](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6094461419)
  item 2: any occurrence other than the three accounted kinds fails, whatever its syntactic form. Item 4: the
  documents state exactly this rule.
- **Evidence:** `receipts/r583_4_census_probes.log`, 5 ESCAPE lines, each with 0 findings:
  - an included file (`ethernet_events.svh`, which the datapath includes) defines
    ``` `define PROBE_CD(n) pp_cd_``n``_w ```. The datapath reads `pp_cd_srp_over_limit_w` through
    `` `PROBE_CD(srp_over_limit) `` onto the CRF talker's `vlan_en_i`;
  - an included file defines `` `define PROBE_H pp_shadow.srp_over_limit_o ``, a hierarchical read of the
    wrapper's class-D port, used the same way;
  - `wire \probe//w ; assign \probe//w = pp_cd_srp_over_limit_w;` is routed to `vlan_en_i`. The census blanks
    everything after `//` as a comment, the read included;
  - `wire \probe"a ;` ... `wire \probe"b ;` around `assign probe_w = pp_cd_srp_over_limit_w;`. The census blanks
    the whole span as a string;
  - `wire pp_cd_srp_over_limit_w = 1'b0;` as a second driver beside the wrapper's connection. It lints clean
    under Verilator 5.050 `-Wall` (`receipts/second_driver_lint.log`).

  The five same-intent controls in the datapath are refused, among them the paste and the hierarchical
  reference written in the datapath and the `assign` second driver. `legality_tb.sv` simulates the `//`-escaped
  and `"`-escaped identifiers and the include-defined paste macro. Each carries the class-D value (1, then 0).
- **Impact:** a read of a class-D value can sit inside the census's declared scope (the datapath and its
  includes) and the census still passes. The documents say such forms are refused. These forms are unusual,
  which is why the severity is MINOR, but the assignment asked for fail-closed "by construction, not by covering
  parser forms one at a time".
- **Required outcome:**
  - The lexer recognises escaped identifiers before it blanks comments and strings, or refuses any escaped
    identifier that holds `//`, `/*` or `"`.
  - A token paste or hierarchical reference in any included file copy is refused as it is in the datapath. So is
    a macro whose definition the census cannot see. Using any macro defined outside the datapath in an expression
    is one way to do it.
  - An initialised declaration of a population wire is refused as a second driver, or the documents stop
    claiming that form.
  - Each case gets a named self-test arm.
  - The docstring, MAILBOX_SPLIT.md, the mbx README and the PR body state the rule the code then enforces.
- **Verification:** `r583_4_census_probes.py`, unmodified, reports no ESCAPE on the five F2 lines. The census
  self-test refuses the new arms by their words.

RESIDUE: none. SUGGESTION: none new. R582-2-S1 = R583-2-S1 (the 32-source mask) stays optional.

## Prior public findings at this head

| Finding | Status at `4a99c1e9` | Evidence |
|---|---|---|
| R582-1-F1 (MAJOR) the started level | Resolved | `BINDING.STARTED` on `pub_started_o` (`KL_mbx.sv:71`, `:285-321`). P1/P2 plants `top-pub-started-*` caught (`receipts/mbx_mutants_full.log`). ACMP plants `pub-acmp-*` caught (`receipts/fw_gate_pr_plants.log`). The F5 path: `app-start-*` 2/2 (`receipts/srp_aecp_pr_plants.log`). |
| R582-1-F2 = R583-1-F1 the Talker declarations | Resolved | `TALKER_DECL.DECLARED` on `pub_talker_decl_o`. `pub-declared-*` plants all caught at two interfaces, and the round-5 ones at one interface too. |
| R582-1-F3 `DA_GATE` | Resolved as ruled | The contract says DA validity only. F3b is recorded. |
| R583-1-F2 the DA gate's interface | Resolved | `rv-maap-gate-on-interface-0` is caught by `DaGateOpensOnTheAcquiringInterfaceAloneBeforeItsReport` (`fw_gate_pr_plants.log`). |
| R583-1-F3 `idle_slope_bps` | Resolved | Harness views and users. |
| R582-2-F1 = R583-2-F1 the census fails closed | Population and accounting: resolved. "Whatever its syntax": retained in part as R583-4-F2 | My independent read of `KL_pp_shadow.sv:633-679` gives 17 SRP and 7 ACMP/ADP class-D outputs, equal to `CLASS_D_PORTS` (`publication_census.py:150-157`), connected 1:1 in the instance (`milan_datapath.sv:8040` onward). R582-2 `census_probes.py`: 6 probes, 0 unexpected. R583-2 `census_escape_probe.py`: 5/5 REFUSED. `census_textual_crosscheck.py`: 25/25/39, 0 unaccounted. |
| R582-2-R1 (RESIDUE) | Applied word for word | `mbx_model.h:161-162` and `mbx_model.c:27`. |
| R583-2-S2 (ruled required) | Resolved | `ctrl_arms.py:415-434`; `test_ctrl_firmware.py:193` runs it in every non-coverage invocation, the hosted `firmware-unit` (`rtl-fast.yml:284`) included. Arm rc 0, 5 controls PASS and 18 plants (`receipts/r583_4_srpcmp_arm.log`). 3/3 planted comparators fail the arm: exit 1, a control reported failed, no plants. `MAILBOX_SPLIT.md:1029` and the ctrl README name it. |
| R582-3-F1 = R583-3-F1 the cone | Every reviewer probe is refused. The rule is not met: retained as R583-4-F1 | R582-3 `census_cone_probe.py`: part 1 has 0 escaping, part 2 has 72 nodes and 0 unaccounted. `census_extra_forms.py`: 6/6. R583-3 `census_cone_probe.py`: 5/5. `census_textual_cone.py`: 0 leave their class. Its self-test: 0 of 2 failed. |
| R582-3-F2 `SID_VALID` with no stream | Resolved | `B13AMoveWithNoStreamLeavesSidValidClearOverAStaleStream` (`test_acmp_mbx.cpp:736`). `pub-acmp-adapter-sid-valid-always` is caught by B13 in `acmp` and `acmpif2`. |
| R582-3-F3 `TALKER_DECL` across a Domain adoption | Resolved | `Srp.PubTalkerDeclHoldsAcrossADomainAdoption` (`srp_mbx.cpp:213`). Its 3 plants are caught at two and at one interface. |
| R583-3-S1 a partly failed creation (ruled required) | Resolved | `Srp.PubTalkerDeclIsNotPublishedByACreationThatFails` (`srp_mbx.cpp:244`). Its 2 plants are caught at two and at one interface. |

## Lens results

```text
[R583] MINOR Conformance - sw/mailbox/census_netlist.py:287-310; publication_census.py:435-490 vs rulings 6094461419 item 2 and 6095903333 item 1 - R583-4-F1, R583-4-F2 open. Otherwise applied clean: the population from the instance (KL_pp_shadow.sv:633-679 = CLASS_D_PORTS, 24 + aecp_strm_started_o); 39 reads, 10 field / 14 status / 15 answer face, each row against milan_datapath.sv; the field rows against mailbox.yaml (gen_mailbox --check / --crosscheck 0 findings); writers ahead of their promising response (acmp.c publish() in transmit and finish, acmp_mbx.c:66-80, srp TALKER_DECL tests); R582-2-R1 wording; srpcmp under the gate
[R583] PASS RTL - hdl/milan/mailbox/KL_mbx.sv:59-72, :150-176, :261-321, :351-358 at 4a99c1e9 - decode guarded by pub_at_w (interface < MBX_N_IF_C, sink < 16, register match) before every array index; writes only on full strobes (wr_w, :90), partial strobes refused into BUS_ERR (:92, :247); field masks per register; reset clears every register; outputs combinational from storage; sid gating left to the reader as documented; milan_soc.py binds every pub_* port unread. Bench (pinned Verilator 5.050): 402 Wishbone, 447 AXI4-Lite, 32 co-simulation, 404 / 449 / 389 at two interfaces, 0 failures; mutants 175/175; lint_rtl --check --self-test 90 <= 90; gen_mailbox --selftest 0 failed arms
[R583] MINOR Robustness - census_netlist.py:61-85, :287-310; publication_census.py:435-490 - R583-4-F1, R583-4-F2 (unusual but legal input forms pass the census). Otherwise applied clean: refusal paths of mbx_pub_* (sink and interface past the block, pub-*-past-the-block plants caught), the static asserts acmp_mbx.c:15, a creation refused at each allocation (srp_mbx.cpp:244), SID_VALID with no stream (B13), two-interface isolation (if2 arms, rv-maap-gate-on-interface-0)
[R583] MINOR Tests - sw/mailbox/census_plants.py (64 arms) - R583-4-F1, R583-4-F2 (no arm for the 13 escaping forms). Otherwise applied clean: firmware gate 60/60 arms (srpcmp and F5's eight among them, --require-rv32); this PR's plants ctrl 134/134, SRP 29/29 at if2 + 5/5 round-5 at if1, AECP 2/2; mbx 175/175; census self-test 0 of 64 failed; each new test (B13, the two SRP TALKER_DECL tests, App.StartAndStopPublishTheStartedLevelBeforeTheirResponse) shown to fail for its plant
[R583] MINOR Docs - publication_census.py:25-40, :52-77; docs/design/MAILBOX_SPLIT.md:862-874, :886-905; tb/verilator/mbx/README.md item 1; PR body "Completeness by construction" and "The census reads text" - claim refusal of every form and an enclosing-block cone (R583-4-F1, F2). Otherwise applied clean: ARCHITECTURE_HW_SW_SPLIT.md:88-94, :189; the 25/89/39, 10/14/15, 62-plant and 64-arm figures match the run; MAILBOX_SPLIT.md:1029 and the ctrl README name srpcmp; docs_check, check_em_dash --base 554e61d2 (0 over 557 added lines), gen_toc --check, check_py_idiom, check_baremetal_only --check, git diff --check all rc 0
```

## Execution evidence (this round, exact head)

All receipts are under `receipts/` with rc files. Scripts are under `scripts/`. Disposable trees are under the
unpublished `scratch/`.

| Run | Result |
|---|---|
| `publication_census.py --check` / `--list` / `--selftest` (in the clone) | rc 0. 25 wires; 89 occurrences = 25 + 25 + 39; 39 reads of 21 wires; self-test 0 of 64 arms failed |
| Prior probes, unmodified, against an export of the head (provenance in `receipts/prior_probe_provenance.txt`) | All rc 0, every form refused (see the table above) |
| `scripts/r583_4_census_probes.py` | 13 probes, **13 ESCAPE**; 6 controls, all refused (R583-4-F1, F2) |
| `scripts/legality/legality_tb.sv` (Verilator 5.050 `--binary`) | `LEGALITY PASS`, rc 0 |
| `second_driver.sv` lint `-Wall` | rc 0, no warning |
| `tb/verilator/mbx` `make all` (export, pinned Verilator) | census PASS; 402 / 447 / 32 / 404 / 449 / 389 checks, 0 failures; quick plants 6/6; rc 0 |
| `tb/verilator/mbx/mutants.py --jobs 6` | 175 of 175 caught, rc 0 |
| `scripts/lint_rtl.py --check --self-test` | PASS, 90 <= 90, rc 0 |
| `gen_mailbox.py --check` / `--crosscheck` / `--selftest` | 0 findings / 0 findings / 0 arms failed |
| Firmware gate arms plus this PR's plants (`scripts/r583_4_fw_gate_pr_plants.py`, `--require-rv32 --self-test --jobs 4`) | 60/60 arms ok, including `srpcmp`. ctrl plants 134/134. The run then stops at the AECP campaign's table-drift control, which refuses a filtered table by design. Overall rc 1 comes from that stop alone. |
| SRP and AECP PR plants (`scripts/r583_4_srp_aecp_pr_plants.py`, AECP table-drift control bypassed, as stated in the script) | SRP 29/29 at two interfaces; the 5 round-5 plants at one interface 5/5; AECP 2/2; rc 0 |
| `srp_wire_compare.py --self-test`; `scripts/r583_4_srpcmp_arm.py` | rc 0; the arm passes, and 3/3 planted comparators fail it |
| Documentation gates | `docs_check`, `check_em_dash --base 554e61d2`, `gen_toc --check`, `check_py_idiom`, `check_baremetal_only --check`, `git diff --check 554e61d2 HEAD`: all rc 0 |
| Clone integrity after all runs (`receipts/clone_integrity.txt`) | HEAD and tree exact. Index records equal HEAD's tree (sha256 `b162a43d...`). 1,273 worktree blobs rehashed, 0 mismatches. Five gitlinks unchanged. No untracked or ignored files. lwSRP was deinitialised again. |

Two receipts had a local home path replaced by `$HOME`: `mbx_make_all.log` and `legality_build.log`.

Hosted contexts at the exact head, read only (`receipts/hosted_check_runs.txt`): 19 completed successfully,
`rtl-fast` and `firmware-unit` among them. `Verilator shard 1/5` was still in progress when read. `Physical gPTP`
was skipped, which is not hardware proof. The manager owns hosted and act acceptance.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R583-4-F1, F2) | rulings 6088423771, 6092086337, 6094461419, 6095903333; `mailbox.yaml`; `publication_census.py`, `census_netlist.py`, `census_plants.py`; `milan_datapath.sv` consumers; `KL_pp_shadow.sv` class-D face; writers in `acmp.c`, `acmp_mbx.c`, `maap_mbx.c`, `srp_mbx.c` | R583-4 | `4a99c1e92ba74c3cbab87a2d6c414113311e743b` |
| RTL | CLEAN | `KL_mbx.sv`, `KL_mbx_pkg.sv`, `tb_mbx_top.sv`, `suite.hpp` P0-P5, `mutants.py`, `milan_soc.py` instance; bench, 175 plants, lint ratchet, generator checks | R583-4 | `4a99c1e92ba74c3cbab87a2d6c414113311e743b` |
| Robustness | UNCLEAN (R583-4-F1, F2) | census input forms (13 probes); firmware refusal paths; failed creation; no-stream moves; two-interface isolation | R583-4 | `4a99c1e92ba74c3cbab87a2d6c414113311e743b` |
| Tests | UNCLEAN (R583-4-F1, F2) | census self-test (64 arms); firmware gate 60 arms; PR plants ctrl 134, SRP 29 + 5, AECP 2; mbx 175; `srpcmp` arm and its plants | R583-4 | `4a99c1e92ba74c3cbab87a2d6c414113311e743b` |
| Docs | UNCLEAN (R583-4-F1, F2) | census docstrings; `MAILBOX_SPLIT.md`; `ARCHITECTURE_HW_SW_SPLIT.md`; mbx, ctrl, SRP and AECP READMEs; `mbx_model.h` / `.c` comments; PR body; docs gates | R583-4 | `4a99c1e92ba74c3cbab87a2d6c414113311e743b` |

## Real limits

- No manager source bank ran at this head, and none is claimed or inferred. The all-fabric byte-identity, the
  firmware size against 224 KB and the mailbox area are not re-measured here. They are the author's published
  receipts, and the PR's own RTL and SoC inputs did not change after round 3. No builder, Yosys, Vivado, export,
  LiteX, gPTP, PP or full-suite bank was run, as assigned.
- `fw_coverage.py --check` (the 100 % ratchet) and `test_ctrl_nvm.py` were not run in this round.
- The firmware plants were limited to those whose names occur in no base test script: 134 ctrl, 29 SRP, 2 AECP.
  The full tables (506 ctrl, 76 AECP) were not re-run. Two stated driver changes made the filtered run possible:
  the unnamed-test check and the AECP table-drift check were bypassed.
- The 13 escape forms are legal SystemVerilog, shown by simulation, but none occurs in today's datapath. No
  present misclassification is claimed.
- Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Route R583-4-F1 and R583-4-F2 to the executor. Re-cover Conformance, Robustness, Tests and Docs at the
  corrected head. RTL is covered clean here at `4a99c1e9`; a later commit that touches mailbox RTL un-covers it.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, against live
  dev `e8454e27`, and publish those receipts.
- Hosted acceptance at the exact head, including the in-progress `Verilator shard 1/5`, and the act replica.
- Carry R582-2-S1 = R583-2-S1 as optional.

R583-4 FINISHED
