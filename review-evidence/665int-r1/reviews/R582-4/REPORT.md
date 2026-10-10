[R582] NEGATIVE - exact head 4a99c1e92ba74c3cbab87a2d6c414113311e743b

# R582-4: internal independent review of PR #704 (issue #665, lane F-INT PR 1 of 2)

- Exact head `4a99c1e92ba74c3cbab87a2d6c414113311e743b`, tree `73e89cc4a550360d26f39b26b4d6ca8c5150ad65`. This is the published PR head (`gh pr view 704`: `headRefOid` equal).
- Source base `7c1b52bee26b497080ee22b1c1986109f80a5ee7`. Dev `554e61d2` is merged in at `26370439`. Live dev is `e8454e27`; its drift from `554e61d2` touches none of `hdl/`, `sw/mailbox/`, `tb/verilator/mbx/`, `sw/firmware/ctrl/` or `MAILBOX_SPLIT.md`.
- **Delta reviewed:** the first-parent commits `b2aa3ccf..4a99c1e9`. That is 13 commits plus the merge:
  - round 4: `cc4e54e0`, `e5af02e8`, `0bffed69`, `232d4663`;
  - round 4b: the merge `26370439`, then `0ca1e397`, `6cf5b8de`, `4274a205`;
  - round 5: `d8a24d08`, `7e41b593`, `9d05ed5f`, `457b4ce4`, `5aefe957`, `4a99c1e9`.
- **Why the delta runs past `232d4663`:** the round-4 assignment (6094461419) names `b2aa3ccf..232d4663`. The head under review also carries round 4b (6095125193) and round 5 (6095903333). Lens coverage is banked against this head, so every commit to it was reviewed.
- **How it was reconstructed:** in a cleared-context detached clone, from these sources:
  - AGENTS.md and CONTRIBUTING.md;
  - the issue body;
  - the round-4, 4b and 5 assignments and the author's REVIEW READY comments on #665;
  - the review-start comment 6096996787;
  - the diff, the history and the PR body.
- Prior public review findings were read only after my own pass and its probes had run (see "Prior public findings").
- No manager source bank runs at this head, and none is claimed or inferred. Physical calibration is NOT RUN. Skipped hosted contexts are not hardware proof.

## Verdict

**NEGATIVE: one MINOR finding (R582-4-F1). It leaves Conformance, Robustness, Tests and Docs unclean; RTL is clean.**

The round-4/4b/5 work does what the assignments asked of it:

- The census takes its population from the wrapper instance, and 25 wires and 89 occurrences are accounted at this head.
- Every escaping probe of R582-2, R583-2, R582-3 and R583-3 is refused by name. I re-ran them unmodified.
- The `srpcmp` arm gates the comparator.
- R582-2-R1's exact wording is applied.
- B13, the two `TALKER_DECL` tests and the composed START/STOP test each pass, and each kills its own plants.

Round 5 asked for more, though: a cone that fails closed at every node, where "any occurrence is an edge to every identifier the enclosing statement or block can drive". That is not achieved. A status or answer-face consumer routed to the wire through an ordinary procedural block passes the census with 0 findings, in either of two ways:

- the block has no `begin` straight after its event control;
- the block uses a compound assignment.

The reverse `alias` form passes the same way. 12 of 12 such arms escape; their controls are refused. At this head no classification is wrong: every procedural block in the datapath opens `begin` on its own line, and no compound assignment or `alias` exists. So this is a standing-guarantee gap of the same class as R582-3-F1, as were the prior census findings, and it is MINOR.

## Findings

### R582-4-F1 - MINOR - Conformance, Robustness, Tests, Docs - `sw/mailbox/census_netlist.py:287-310` (`always_blocks`), `:172-194` (`assignment`), `:207-224` (`lvalue_at`); `sw/mailbox/publication_census.py:52-77`, `:314`; `docs/design/MAILBOX_SPLIT.md:886-901`; `tb/verilator/mbx/README.md:14-18`; PR body "The cone fails closed at every node" - the cone does not reach every target of a procedural block, and it reads a compound assignment or an `alias` as a plain target, so a status or answer-face read routed to the wire through them passes

- **Authority:**
  - Round-5 assignment 6095903333, item 1: "Treat every non-comment occurrence of any cone node ... as an edge to every identifier the enclosing statement or block can drive. An occurrence the census cannot classify counts as reaching the wire."
  - Ruling 6092086337 item 3's standing check, and 6094461419: fail closed "by construction, not by covering parser forms one at a time".
  - The census docstring (`publication_census.py:53-56`) and `MAILBOX_SPLIT.md:887-889` both state that a read leads to "every target of the procedural block (`always`, `initial`, `final`) it lies in". The mbx README (`:16-17`) and the PR body state the same.
  - `MAILBOX_SPLIT.md:896-901` adds that "any other occurrence counts as reaching the wire, whatever its form ... and any form not yet written".
- **Evidence (`receipts/census_block_probe.log`, script `scripts/census_block_probe.py`, in-memory copies of the datapath):**
  - **The setup.** Each arm routes `lwsrp_talker_declared` (CENSUS row "status") or `gsi_tkdcl_w` (row "processor") through a procedural block into another module's input port. The census defines that port as the wire (R583-3's `KL_probe_sink` form).
  - **The controls.** Each is the same block with `begin` right after the event control, a plain blocking assignment, or `alias probe_q = <consumer>`. All 6 are refused ("counted as status, but it reaches the wire at u_probe_sink.a_i").
  - **The escapes:** 12 of 12 report 0 findings, with RESULT PASS. Six forms escape at each of the two consumers:
    - **E1** `always_ff @(posedge axis_clk) if (c != '0) begin probe_a <= '1; probe_q <= '1; end`. There is no `begin` after the event control, so `always_blocks` (`:307-308`) takes the block as its first statement only. `probe_q`'s assignment lies outside it, and the condition's edge reaches `probe_a` alone.
    - **E2** `always_ff @(posedge axis_clk) if (c != '0) probe_a <= '1; else probe_q <= '1;`, for the same reason.
    - **E3** `always_comb case (c) '0: probe_a = '1; default: probe_q = '1; endcase`, for the same reason.
    - **E4** `always_ff @(posedge axis_clk iff (axis_resetn)) begin if (c != '0) begin ... end end`. The event regex `@\s*(\([^)]*\)|\*)` (`:296`) stops at the first `)`, so `begin` is not seen and the block shrinks to one statement.
    - **E5** `always_ff @(posedge axis_clk) begin probe_a <= '0; probe_q |= c; end`. `assignment()` takes `|=` as `=` with the left-hand side `probe_q |`, and `lvalue_at` finds no target. The read's edge goes only to the block's other targets, so `probe_q` is never reached.
    - **E6** `wire probe_q; alias <consumer> = probe_q;`. The consumer's occurrence is classified as "a place driving it" (`publication_census.py:314`), but `alias` is bidirectional, so the value reaches `probe_q` and the wire.
  - **The forms are legal.** All six forms elaborate under the pinned Verilator 5.050 with rc 0, warnings only (`scripts/census_block_forms.sv`, `receipts/census_block_forms_lint.log`).
  - **Why the first hop is not affected:** it accepts only declarations, the connection and recorded reads. For a population wire, E5 and E6 are therefore refused there as unaccounted occurrences. The gap is in the cone, past the first hop.
- **At this head:** no classification is wrong.
  - Every procedural block in `milan_datapath.sv` opens `begin` on its header line.
  - No compound assignment or `alias` occurs outside comments.
  - The census passes 39 of 39 checks, and R583-3's independent textual cone agrees: 0 of 29 reads leave their class.
- **Impact:** PR 2 rewires this file. If a status or answer-face consumer is routed to egress through a header-only `always` (the most common Verilog style), an `iff` event, a compound assignment or an `alias`, the mailbox suite passes while the block lacks the value. That is the failure the census exists to stop. The docstring, the design page, the bench README and the PR body also state a block rule the reader does not implement.
- **Required outcome:**
  - Every procedural block's extent is its whole body, whatever its form. That includes a body that is one statement (an `if`/`else`, `case` or loop holding further statements) and an event control with nested parentheses.
  - Any assignment form the reader does not parse as plain `=` or `<=` is the wire, or drives all it can: compound operators, `alias` on either side, and any other.
  - The census refuses these arms by name in its standing self-test, at a status and at an answer-face consumer. Or else the docstring, MAILBOX_SPLIT.md, the bench README and the PR body state the limit explicitly, with a ruling accepting it.
- **Verification:**
  - `python3 -I -B scripts/census_block_probe.py <tree>` reports 0 escaping arms, with all controls refused.
  - `publication_census.py --check --selftest` passes at the new head with the new arms refused.
  - The prior probes stay refused.

### R582-4-S1 - SUGGESTION - Tests - `sw/firmware/ctrl/test/ctrl_arms.py:420-434` (`arm_srpcmp`) - the arm fails on no plant, but not on fewer plants

The arm fails on a non-zero exit, an unreadable report, a control other than PASS, or an empty plant list. `receipts/srpcmp_arm_probe.log` shows 6 of 6 cases as expected. A comparator whose plant table silently shrank from 18 to 1 would still pass. A floor on the plant count, or the named plant set, would pin it. This is optional and does not affect coverage.

RESIDUE: none.

## Lenses at this head (artifact-specific)

```text
[R582] MINOR Conformance - census_netlist.py:287-310, :172-194; publication_census.py:52-77 - R582-4-F1: round-5 item 1 (block-wide edges, unclassifiable = wire) not met for header-only blocks, nested event controls, compound assignment, alias
[R582] PASS RTL - hdl/milan/mailbox/KL_mbx.sv:59-72, :150-176, :261-321, :351-358; KL_mbx_pkg.sv; sw/litex/milan_soc.py:2504-2571 - PR's RTL patch vs dev byte-identical to its patch at b2aa3ccf (`diff` of the two patches: SAME); decode guard, sync reset, field masks, read mux, unread SoC ports re-read; bench at this head 402/447/32/404/449/389 checks 0 failures 0 warnings; mutants --quick 6/6
[R582] MINOR Robustness - census_netlist.py:296, :307-308; publication_census.py:314 - R582-4-F1: unusual but legal input forms make the gate under-approximate the cone
[R582] MINOR Tests - publication_census.py --selftest (census_plants.py) - R582-4-F1: no plant for these forms and the gate cannot fail for them; the round-4b/5 firmware tests otherwise verified (below)
[R582] MINOR Docs - publication_census.py:53-56; MAILBOX_SPLIT.md:886-901; tb/verilator/mbx/README.md:14-18; PR body - R582-4-F1: the stated block rule is not what the reader does
```

### Evidence per lens

**Conformance.** Each assignment item is checked against the code and a receipt:

- **Round 4, item 1 (population from the instance).** `population()` (`publication_census.py:384-424`) reads the wrapper instance's named connections and refuses unnamed ones, expressions, omissions, duplicates and shared wires. `class_d_face()` (`:353-381`) checks `CLASS_D_PORTS` against the wrapper's class-D sections. `census_list.log` shows 25 ports, each to its wire.
- **Round 4, item 2 (every occurrence accounted).** `survey()` (`:451-492`) classifies every population occurrence. `census_check_selftest.log` gives 25 declarations, 25 connections and 39 reads. R583-2's independent cross-check gives the same 25 / 25 / 39 with 0 unaccounted.
- **Round 4, item 3 (the probes).** All prior probes are refused by name, run unmodified (table below).
- **Round 4, item 4 (the documents).** The first-hop rule is stated in the docstring (`:15-40`), `MAILBOX_SPLIT.md:841-874`, `ARCHITECTURE_HW_SW_SPLIT.md:90-91`, the mbx README and the PR body.
- **R583-2-S2 (the comparator gated).** `arm_srpcmp` runs in every non-coverage invocation of `test_ctrl_firmware.py` (`:189-193`), which hosted `rtl-fast`/`firmware-unit` runs (`rtl-fast.yml:284`). `MAILBOX_SPLIT.md` (Verification) and the ctrl README name it. `srp_wire_compare_selftest.log` shows 5 controls PASS and 18 plants.
- **R582-2-R1 (residue wording).** `mbx_model.h:162-164` and `mbx_model.c:27` carry the exact wording.
- **Round 4b.** The census reconciliation against F5 holds. Since `232d4663`, the merge changed no PR-owned RTL, generator or firmware source; only `sw/firmware/ctrl/README.md` was merged on both sides.
- **Round 5, items 2 to 4.** Met (see Tests).
- **Round 5, item 1.** Not met (R582-4-F1).

**RTL.** The PR's RTL (`KL_mbx.sv`, `KL_mbx_pkg.sv`, the SoC instance) is unchanged since `b2aa3ccf`. I re-read it at this head, checking six points:

- the decode guard on `rel >> log2(stride) < N_IF` and on `entry < N_SINKS` before any array index;
- the write gated by `wr_w && pub_at_w`;
- the field masks;
- the read mux behind `pub_at_w`;
- the sync reset of every publication register;
- `pub_sid_o` driven unconditionally, with the port comment saying the datapath takes it only while SID_VALID.

The checks came back clean:

- **Default build.** The SoC leaves every `pub_*_o` unread, so the default build's behaviour is unchanged.
- **Bench, run by me with the pinned Verilator 5.050 in a scratch mirror:**
  - `run-wb` 402, `run-axil` 447, `run-cosim` 32, `run-if2` 404/449/389;
  - 0 failures and 0 `%Warning` (`receipts/mbx_*.log`);
  - `mutants-quick` 6/6, `top-pub-sid-valid-held-high` among them.

**Robustness.** The census was fed unusual but legal forms (`census_block_probe.py`, plus every prior probe), and the first hop stayed closed. The `srpcmp` arm was fed every failure mode a comparator can report (`srpcmp_arm_probe.log`): 6 of 6 behave as required. The firmware paths the new tests cover are all refusal and failure paths:

- the stale stream after an unbind;
- a re-creation refused at each of its allocations;
- an adoption overwriting a foreign register value.

**Tests.** Each new test was run unplanted, then its plants were run through the checkout's own harness tables (`scripts/focused_plants.py`, builds under scratch):

- **Unplanted** (`focused_baseline.log`): `acmp` 95 tests and `acmpif2` 26 tests, B13 among them; `srp_mbx.cpp` 59 of 59 at one and two interfaces, both `PubTalkerDecl*` tests among them; F5's `app` arm with `App.StartAndStopPublishTheStartedLevelBeforeTheirResponse` at one and two interfaces. All pass.
- **Plants:**
  - `pub-acmp-adapter-sid-valid-always` is caught by B13 at both `acmp` and `acmpif2` (`focused_ctrl.log`, 1/1);
  - the five `srp_pub_mutants.ROUND5` plants are each caught by their named test with their own words, at two interfaces and at one (`focused_srp2.log`, `focused_srp1.log`, 5/5 each);
  - `app-start-skips-publication` and `app-start-response-before-publication` are caught (`focused_aecp.log`, 2/2).
- **The census self-test:** 0 of 64 arms failed. It is unclean only through R582-4-F1.

**Docs.**

- The figures stated match the receipts:
  - 25 / 89 / 39;
  - 10 field, 14 status and 15 processor reads (`census_list.log`);
  - 62 plants plus 2 controls = 64 arms;
  - 5 controls and 18 comparator plants;
  - "seventeen arms and lwSRP's" in the ctrl README (17 rows plus `lwsrp`).
- Local doc gates: `docs_check.py` 0 findings, `check_baremetal_only.py --check` 0, `check_py_idiom.py` 0. The hosted `docs-check` at this head succeeded.
- Commits are one line with no trailers.
- Unclean only through R582-4-F1.

## Prior probes, re-run unmodified at this head

The scripts were taken from the review-evidence branch (`b7bcc102` for round 2, `798ec01a` for round 3). Hashes are sha256.

| Probe (sha256 prefix) | Result at `4a99c1e9` |
|---|---|
| R582-2 `census_probes.py` (`8646720a`) | `probes: 6, unexpected: 0`; the 5 escape arms, among them the off-prefix wire `probe_dom_chg_w`, are refused by name |
| R583-2 `census_escape_probe.py` (`8e58b694`) | the control and the 4 forms (case-item label, positional, implicit `.name`, function return) are all REFUSED as unaccounted occurrences |
| R583-2 `census_textual_crosscheck.py` (`7929711f`) | 25 declarations, 25 wrapper outputs, 39 census reads; 0 unaccounted |
| R582-3 `census_cone_probe.py` (`88fa7d64`) | part 1: 0 escaping (all 10 arms refused); part 2: 72 nodes, 0 unaccounted |
| R582-3 `census_extra_forms.py` (`ed309ec5`) | 6 of 6 refused |
| R583-3 `census_cone_probe.py` (`8d651fc3`) | 5 of 5 refused, plus the control |
| R583-3 `census_textual_cone.py` (`903887f3`) and its self-test (`219e8b3c`) | 0 of 29 leave their class; self-test 0 of 2 failed |

The census itself: `--check --selftest` rc 0, 39 checks, 0 failures, `selftest: 0 of 64 arm(s) failed`. The bench's `census` target gives the same.

## Prior public findings

These were read after my pass.

| Finding | Status at this head | Evidence |
|---|---|---|
| R582-1-F1 (MAJOR), R582-1-F2 = R583-1-F1, R582-1-F3, R583-1-F2, R583-1-F3 | Resolved, as R582-2 and R583-2 confirmed at `b2aa3ccf`. Nothing since reopens them | the contract, RTL, generator and writer sources are unchanged since `b2aa3ccf` (only README merges) |
| R582-2-F1 = R583-2-F1 (population fail-closed) | Resolved | round-4 items 1-3 above; all round-2 probes refused |
| R583-2-S2 (comparator ungated), required by the round-4 assignment | Resolved | the `srpcmp` arm; documents name it; `srpcmp_arm_probe.log` |
| R582-2-R1 (RESIDUE) | Applied | `mbx_model.h:162-164`, `mbx_model.c:27` carry the exact wording |
| R582-3-F1 = R583-3-F1 (cone one hop past the population) | Its named forms are resolved: every probe of both reviews is refused, and plants stand for each. Its required outcome ("anything else fails") is not fully met | carried forward as **R582-4-F1** |
| R582-3-F2 (SID_VALID on a stream-less move) | Resolved | B13 and its plant, 1/1 at `acmp` and `acmpif2` |
| R582-3-F3 (TALKER_DECL across an adoption) | Resolved | the adoption test and three plants, 3/3 at one and two interfaces |
| R583-3-S1 (partly failed creation), required by the round-5 assignment | Resolved | the failed-creation test and two plants, 2/2 at one and two interfaces |
| R582-2-S1 = R583-2-S1 (32-source mask), R583-1-S1/S3 | Optional, not taken | No effect on coverage |

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R582-4-F1) | the round-4/4b/5 assignment items against `publication_census.py`, `census_netlist.py`, `census_plants.py`, `ctrl_arms.py`, `test_ctrl_firmware.py`, `mbx_model.{h,c}`; `census_check_selftest.log`, `census_list.log`, prior probes, `census_block_probe.log` | R582-4 | `4a99c1e92ba74c3cbab87a2d6c414113311e743b` |
| RTL | CLEAN | `KL_mbx.sv:59-72,150-176,261-321,351-358`, `KL_mbx_pkg.sv`, `milan_soc.py:2504-2571`; RTL patch identity since `b2aa3ccf`; `mbx_run-{wb,axil,cosim,if2}.log`, `mbx_mutants-quick.log` | R582-4 | `4a99c1e92ba74c3cbab87a2d6c414113311e743b` |
| Robustness | UNCLEAN (R582-4-F1) | census reader on legal unusual forms (`census_block_probe.log`, `census_block_forms_lint.log`); `srpcmp_arm_probe.log`; the refusal and failure paths of B13 and both `TALKER_DECL` tests | R582-4 | `4a99c1e92ba74c3cbab87a2d6c414113311e743b` |
| Tests | UNCLEAN (R582-4-F1) | `focused_baseline.log`, `focused_ctrl.log`, `focused_srp1.log`, `focused_srp2.log`, `focused_aecp.log`; census self-test 64 arms; `srp_wire_compare_selftest.log` | R582-4 | `4a99c1e92ba74c3cbab87a2d6c414113311e743b` |
| Docs | UNCLEAN (R582-4-F1) | census docstring, `MAILBOX_SPLIT.md:569-1031`, `ARCHITECTURE_HW_SW_SPLIT.md:88-93`, the mbx README and Makefile, the ctrl, srp and aecp READMEs, the PR body; `docs_*.log`; commit form | R582-4 | `4a99c1e92ba74c3cbab87a2d6c414113311e743b` |

## Real limits

- **The full firmware campaign was not re-run** (`test_ctrl_firmware.py --require-rv32 --self-test`, about 40 minutes): no RV32 SDK is on this host. Only the round-4b/5 tests and their 10 plants were run, through the checkout's own harness and tables:
  - the `aecp` subset bypassed only its table-drift control, which refuses any subset by design;
  - the driver's `aecp`-filter and baseline-field fixes were made after the `ctrl` and `srp` modes ran, and those modes' code is unchanged.
  - For the full gate I rely on the author's published receipts and the hosted `firmware-unit` success at this head.
- **Not run:** the full mbx RTL plant table (175), Yosys, the export, size and area banks, and LiteX. No input of theirs changed since `b2aa3ccf`.
- **Two docs gates were not runnable locally:** `gen_toc.py --check` and `check_em_dash.py` need a Markdown renderer that is not installed, and installing it would be a shared install. The hosted `docs-check` at this head succeeded.
- **The census's assumptions:** the census is textual. It stops the cone at any `milan_csr` instance's listed ports, which assumes that block's outputs are read-back only. Files other than the datapath and its includes are outside it, as the author states.
- **The probe itself:** `census_block_probe.py` uses in-memory copies only. Its arms are representative forms, not an exhaustive grammar.
- **State left behind:** the clone was restored after the probes, and `receipts/restore_verify.txt` records the result:
  - the index tree equals the head tree;
  - status is empty, with no ignored files;
  - all five gitlinks are unchanged;
  - lwSRP was initialised at its pin for the SRP runs, then deinitialised.

## Pending manager duties

- Validate the current-dev merge candidate (source base `7c1b52be`, live dev `e8454e27`) with the builder and native banks at the merge turn, and link the receipts.
- Hosted and act acceptance. At inspection, every executed context at this head had succeeded except `Verilator shard 1/5`, which was still in progress. `Physical gPTP` is skipped, which is not hardware proof.
- Obtain the second, external review at the head that answers R582-4-F1.
- No residue to carry.

R582-4 FINISHED
