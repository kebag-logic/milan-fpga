[R583] NEGATIVE - exact head b2aa3ccfe31652ad34d93e3ea446f31b58dc9c1c

Round R583-2, external independent review of issue #665 / PR #704 (F-INT PR 1, the publication block), tree `bbe108c257c71be2553d713e035a0648e8808aa3`, source base `7c1b52bee26b497080ee22b1c1986109f80a5ee7`. Cleared context. I reconstructed the scope from these sources, then read the diff (21 commits, 49 files) and the executable evidence:

- AGENTS.md and CONTRIBUTING.md;
- the issue body and the assignment 6087047553;
- rulings 6087214078, 6087462816, 6087654804, 6088423771 and 6092086337.

I read prior public findings only after the independent pass.

**Verdict: NEGATIVE on one MINOR finding.** These hold at this head:

- the block, its RTL and its generator;
- every firmware writer and its ordering;
- every round-3 answer.

Every gate I ran reproduces the author's tallies.

The one open defect is in the standing completeness check that ruling 6092086337 item 3 asks for. The census accepts an unmapped, wire-affecting read of a class-D wire when that read uses any of four legal SystemVerilog forms, and its documentation says it covers those forms. At this head the census is complete: an independent textual cross-check accounts for every occurrence. The defect is the guarantee the check gives PR 2, which rewrites the datapath it reads.

## Findings

### R583-2-F1 - MINOR - Conformance, Tests, Robustness, Docs - `sw/mailbox/publication_census.py:20-26`, `:179`, `:380`, `:401`; `docs/design/MAILBOX_SPLIT.md:836-839`; PR body "Completeness by construction" - the standing census silently accepts unmapped wire-affecting reads in four legal forms

- **Authority.** Ruling 6092086337 item 3 asks for a standing check. Every wire-affecting read of a processor class-D output in `milan_datapath.sv` must map to a block field or to a named, ruled exclusion, and the check must fail on an unmapped read.
- **What the census claims to cover.** Its docstring (`:20-26`), MAILBOX_SPLIT.md `:836-839` and the PR body all say it finds every read in these places:
  - a right-hand side;
  - an index;
  - a declaration's initialiser;
  - an `if`, `case` or `for` condition;
  - a port connection.
- **Evidence.** `scripts/census_escape_probe.py` plants a read of `pp_cd_srp_over_limit_w` into copies of the datapath. It routes each read to the CRF talker's `vlan_en_i`, which is on the wire. `receipts/census_escape_probe.log` shows:
  - **Control, a plain `assign`:** REFUSED (rc 1, "unmapped read ... reaches the wire").
  - **Positional port connection** (`KL_probe_buf u (pp_cd_..., probe_w);`): ACCEPTED (rc 0).
  - **Implicit `.name` port connection:** ACCEPTED (rc 0).
  - **`case` item label inside an `always_comb`:** ACCEPTED (rc 0).
  - **`function` body that returns the wire:** ACCEPTED (rc 0).
- **Cause.** Three parser gaps:
  - Instance ports are read only through `\.\s*(\w+)\s*\(` (`:380`).
  - Control reads are taken only inside the parentheses of `if`/`case`/`for` (`:179`, `:401`), so a case-item label is never read.
  - A `return` statement is dropped as a keyword statement.
- **Impact.** No value is missing at this head. `scripts/census_textual_crosscheck.py` finds every non-comment occurrence of the population in the datapath: 25 are declarations, 25 are the wrapper's own output connections, 39 lie on lines the census reports, and none is unaccounted (`receipts/census_textual_crosscheck.log`).
  - The ruling makes this a standing guard, and PR 2 adds the build-time selection to this same file.
  - A read PR 2 adds in one of these forms would pass the mailbox suite. That is the failure the census exists to stop: a consumed value missing from the block, as in round 1.
  - The documentation also tells the next author and reviewer that these forms are covered.
- **Required outcome.**
  - The census fails closed: it reports any non-comment occurrence of a population wire that is not one of these three:
    - a declaration;
    - a processor-wrapper output connection;
    - a read it has classified.
  - This includes reads through positional, implicit-name or wildcard port connections, case-item labels and function bodies.
  - Its self-test plants each of the four forms and requires each to be refused.
  - The docstring, MAILBOX_SPLIT.md and the PR body describe the coverage the check actually has.
- **Verification.**
  - `python3 -I scripts/census_escape_probe.py <repo> <scratch>` from this packet: every plant REFUSED.
  - `publication_census.py --check --selftest` and `make -C tb/verilator/mbx`: still pass on the tracked datapath.

### R583-2-S1 - SUGGESTION - Robustness - `sw/firmware/ctrl/maap/maap_mbx.c:62`, `sw/mailbox/mailbox_model.py:412` - the DA gate mask is undefined for 32 sources, which the contract accepts

- The contract check accepts `publication.sources` up to 32, and the skeleton then makes `DA_GATE.OPEN` 32 bits wide.
- `maap_mbx_init` admits `count <= MBX_N_PUB_SOURCES`. With 32 sources and `ACMP_MAX_SOURCES` overridden to 32, `(1u << count) - 1u` is evaluated with `count == 32`, which is undefined behaviour in C11.
- This cannot happen at the shipped 16 sources.
- Fix: compute the mask with a guard (`count >= 32u ? 0xFFFFFFFFu : ...`), or cap the contract's sources at 31.

### R583-2-S2 - SUGGESTION - Tests, Docs - `sw/firmware/ctrl/test/srp_wire_compare.py` - the ruled comparator infrastructure is run by no gate and named by no document

- Ruling 6088423771 keeps the comparator as infrastructure for PR 2.
- Its `--self-test` passes (`receipts/srp_wire_compare_selftest.log`, rc 0).
- No Makefile, gate driver, workflow or document references it.
- Fix: run its self-test from `test_ctrl_firmware.py --self-test`, or name it in MAILBOX_SPLIT.md as PR 2's comparator, so it does not rot before PR 2 needs it.

RESIDUE: none.

## Prior public findings at this head

| Finding | Status at b2aa3ccf | Evidence |
|---|---|---|
| R582-1-F1 (MAJOR): the started level | Resolved | `BINDING.STARTED` (`mailbox.yaml`; `KL_mbx.sv:305-321`, `pub_started_o`). ACMP writes it before the BIND_RX response and before the notifier (`acmp.c:198`, `:285`, `:488`). Caught: RTL P2/P3 checks and plants (175/175), model twin `model-pub-started-not-stored`, A31S/B12 plants (moved, after report, from bound, skipped, adapter rewrite, SID_VALID dropped). Census row: `pp_aecp_strm_started_w -> acmpl_stopped_v_w` = `BINDING.STARTED` |
| R582-1-F2 = R583-1-F1: Talker declarations | Resolved | `TALKER_DECL.DECLARED`. Set before the declarations are sent (`srp_mbx.c:188-189`); withdrawn before destroy (`:80`). Seven `pub-declared-*` plants caught. Census row: `pp_cd_srp_tk_decl_state_w -> crft_class_a_w` = `TALKER_DECL.DECLARED` |
| R582-1-F3: `DA_GATE` documented as `acmp_declaring_o` | Resolved as ruled (item 4) | The contract text says "address validity only" and names the missing 4.3.3.1 predicate. The MAILBOX_SPLIT choices list names the egress consequence with policing off. F3b is recorded |
| R583-1-F2: DA gate interface routing | Resolved | `rv-maap-gate-on-interface-0` is caught at two interfaces by `DaGateOpensOnTheAcquiringInterfaceAloneBeforeItsReport` and `DaGateOfEveryInterfaceOpensBeforeItsOwnReport` (`receipts/ctrl_firmware_selftest.log`) |
| R583-1-F3: idle-slope unit in harness views | Resolved | `frames.hpp:31` and `mbx_model.h:168` use `idle_slope_bps` |

## Independent pass, by lens

### Conformance

- **PR 1 scope (ruling 6088423771) is met.**
  - The block sits in the mailbox window only.
  - Writers are in ACMP, MAAP and SRP. ADP has none, and the census justifies that: `pp_cd_adp_avail_index_w` reaches only `i_adp_available_index`, which is CSR status.
  - VERSION is unchanged; the contract minor moves from 2.1 to 2.2.
  - The default build is untouched: `ctrl_mailbox=False` at `milan_soc.py:2639` and `:3345`.
- **Round-3 items 1 to 6 are present.** Item 3 is subject to F1.
- **"Before the response that promises it" holds for every writer.**
  - **ACMP.** `publish()` runs inside `transmit()` before every send and first in `finish()`. So the BIND_RX, UNBIND_RX and GET_RX_STATE responses, the store and the notifier all follow it. Every send path goes through `transmit()` except the owed-frame poll, whose state was published when the frame was queued.
  - **MAAP.** `DA_GATE` is written before `m->allocation`.
  - **SRP, `LICENCE`.** Written before every licence report, including the stop-owed path. A reviewer plant that moves it after the report is caught by `PubLicenceIsSetAndClearedBeforeEachChangeIsReported` at one and at two interfaces (`receipts/fw_probe_stop_owed_licence.log`).
  - **SRP, the other registers.** `SR_DOMAIN`, `IDLE_SLOPE` and `TALKER_DECL` are written before the joins are transmitted. The declarations are withdrawn before destroy.
- **The author's recorded semantic choices agree with the code I read:** the published stream_id window, LICENCE, DA validity, and the firmware's own declarations.

### RTL

- **Decode (`KL_mbx.sv:159-176`).**
  - The decode uses power-of-two bit fields.
  - The `rel >> log2(stride) < N_IF` check runs at full width, so an absent interface cannot alias.
  - The indices are guarded, so the arrays stay in range.
- **Storage (`:271-303`).** Field-masked, with a synchronous reset to 0. Writes come only through `wr_w`, which requires all four strobes.
- **Outputs (`:305-321`) and read-back (`:351-358`).** `pub_sid_o` is gated by `pub_sid_valid_o` at the consumer, as documented.
- **Generation.** `mailbox_skeleton.py` generates the block and refuses a contract the skeleton cannot wire.
- **No CDC.** Everything runs on the single `clk_i`. The consumer's crossing belongs to PR 2.
- **SoC binding.** All 37 of KL_mbx's ports are bound, with the right directions (`receipts/soc_port_bind_probe.log`).
- **Lint ratchet.** 90 <= 90 under the pinned 5.050.
- **Reviewer RTL plants outside the author's table: 3 of 3 caught** (`receipts/rtl_pub_probe.log`):
  - TALKER_DECL driven from LICENCE;
  - STARTED gated by BOUND;
  - IDLE_SLOPE written from a sink offset.

### Robustness

- **P4/P5 coverage.** Holes, the fourth word of an entry, absent interfaces up to index 3, partial strobes and reset are all covered, through both adapters and at two interfaces.
- **Driver refusals.** Out-of-range interfaces and sinks are refused, with D14 plants. `_Static_assert`s tie the ACMP and SRP sizes to the block.
- **Reset and destroy.** Every licence closes before the revocation is reported, and declarations are withdrawn before participants are destroyed.
- **Stream_id integrity.** A stream_id is never half written: SID_VALID clear, then both words, then SID_VALID set. A start or stop of a settled stream keeps SID_VALID.
- **Open.** F1 is the open robustness defect: unexpected input forms reach the standing check. S1 is latent.

### Tests

- **RTL suite.**
  - Checks: 402 / 447 / 32 / 404 / 449 / 389, 0 failures.
  - Plants: 6/6 quick; 175/175 full, after 4 positive controls.
- **Firmware.** 51 arms. 505/505 control plants and 261 SRP plant runs, none escaped.
- **Coverage ratchet.** 22 files, with every writer file at 100 % of lines and branches. Examples: `acmp.c` 767/767 lines and 362/362 branches; `srp_mbx.c` 540/540 and 486/486; `acmp_mbx.c`, `maap_mbx.c` and `mbx.c` also full.
- **The ruling's plants.** Every writer has moved, wrong-field and skipped plants, each killed by its named test.
- **Open.** F1 is the open tests defect: the census self-test plants three forms and does not cover the four that escape.

### Docs

- **Examined:**
  - `docs/ARCHITECTURE_HW_SW_SPLIT.md` (+8 lines);
  - `docs/design/MAILBOX_SPLIT.md`: the block, its writers, four choices, the bounds tables and the area;
  - the generated `docs/reference/MAILBOX_CONTRACT.md` (`gen_mailbox.py --check` clean);
  - the ctrl, maap, srp and mbx READMEs.
- **Recomputed figures match:**
  - FF: 1,168 = 96 + 16 x 67;
  - LUT: 3,585 - 3,102 = 483;
  - census: 39 = 10 + 14 + 15.
- **Open.** F1 is the open docs defect: the coverage claim.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | issue body; assignment 6087047553; rulings 6087214078, 6087462816, 6087654804, 6088423771, 6092086337; `mailbox.yaml:317-412`; `milan_datapath.sv` class-D reads (39, independently cross-checked); `acmp.c:198-213,285-290,488-490,804-862,1196-1206`; `maap_mbx.c:36-75`; `srp_mbx.c:64-82,156-191,259,309-358,651,718-760,810-836`; `milan_soc.py:2504-2583,2639,3345` | R583-2 | b2aa3ccfe31652ad34d93e3ea446f31b58dc9c1c |
| RTL | CLEAN | `hdl/milan/mailbox/KL_mbx.sv:56-72,159-176,271-321,351-358`; `KL_mbx_pkg.sv`; `sw/mailbox/mailbox_skeleton.py` (`_pub_*`, `_check_wiring`); `tb_mbx_top.sv`; receipts `mbx_make_all.log`, `mbx_mutants_full.log` (175/175), `rtl_pub_probe.log` (3/3), `lint_rtl.log` (pinned 5.050), `soc_port_bind_probe.log` (37/37) | R583-2 | b2aa3ccfe31652ad34d93e3ea446f31b58dc9c1c |
| Robustness | UNCLEAN (F1) | `suite.hpp:1668-1966` (P0-P5); `mbx.c:147-233` refusals; `acmp_mbx.c:174-183`; `srp_mbx.c` reset, destroy and stop-owed paths; `host/mbx_model.c` publication twin; `publication_census.py` parser (`receipts/census_escape_probe.log`) | R583-2 | b2aa3ccfe31652ad34d93e3ea446f31b58dc9c1c |
| Tests | UNCLEAN (F1) | `suite.hpp`, `mutants.py`; `test_unit_driver.cpp` D14; `test_acmp.cpp:1924-2100` (A31); `test_acmp_mbx.cpp:610-740` (B10-B12); `test_maap_mbx.cpp`; `srp_mbx.cpp:92-200`; `srp_app.cpp`; `ctrl_mutants.py`, `srp_mutants.py`, `srp_pub_mutants.py`; `publication_census.py` self-test; receipts `ctrl_firmware_selftest.log` (51 arms, 505/505, 261 SRP runs), `fw_coverage_check.log`, `fw_probe_stop_owed_licence.log`, `srp_wire_compare_selftest.log` | R583-2 | b2aa3ccfe31652ad34d93e3ea446f31b58dc9c1c |
| Docs | UNCLEAN (F1) | `docs/ARCHITECTURE_HW_SW_SPLIT.md`; `docs/design/MAILBOX_SPLIT.md:802-1060`; `docs/reference/MAILBOX_CONTRACT.md` (generated); `sw/firmware/ctrl/README.md`, `maap/README.md`, `srp/README.md`; `tb/verilator/mbx/README.md`, `Makefile`; PR body; REVIEW READY 6094106295; receipts `docs_check.log`, `em_dash.log`, `gen_check.log`, `gen_crosscheck.log`, `gen_selftest.log`, `module_matrix.log`, `measure_naming.log`, `py_idiom.log`, `diff_check.log` | R583-2 | b2aa3ccfe31652ad34d93e3ea446f31b58dc9c1c |

## Executed evidence

All at this exact head; rc 0 unless stated.

- **Generator.** `gen_mailbox.py` `--check`, `--crosscheck`, `--selftest`: 0 findings, 0 arms failed.
- **Census.** `publication_census.py --check --selftest`: 39 checks, 0 failures, 0 of 10 arms failed. The `--list` output is in `receipts/census_list.log`.
- **Mailbox suite.** `make -C tb/verilator/mbx`, pinned Verilator 5.050:
  - the census;
  - 402 checks through Wishbone, 447 through AXI4-Lite, 32 in the co-simulation;
  - 404 / 449 / 389 at two interfaces;
  - 6 of 6 quick plants.
- **RTL plants.** `tb/verilator/mbx/mutants.py --jobs 2`: 175 of 175, after 4 positive controls.
- **Firmware.** `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4`:
  - 51 arms;
  - 505 of 505 control plants;
  - 261 SRP plant runs, none escaped;
  - the lwSRP pin refusals;
  - `test_ctrl_firmware: PASS`.

  The RV32 compiler is the pinned SDK, archive sha256 `d42680e9...b78f`, verified by `ci_rv32_sdk.py`.
- **Coverage.** `fw_coverage.py --check --jobs 3`: PASS, 22 files.
- **Lint.** `lint_rtl.py --check --self-test`: 90 <= 90 under the pinned 5.050. A run under the host's Verilator 5.052 is kept separately; it gives the same result.
- **Docs and hygiene.**
  - `check_py_idiom.py`, `gen_module_matrix.py --check`, `measure_naming.py --check`, `docs_check.py`: all pass.
  - `check_em_dash.py --base 7c1b52be`: pass, 0 findings over 438 added lines, run in the pinned Markdown renderer environment.
  - `git diff --check`: clean.
- **Reviewer probes.**
  - `census_escape_probe.py`: 4 escapes, and the control refused (F1).
  - `census_textual_crosscheck.py`: 0 unaccounted occurrences.
  - `rtl_pub_probe.py`: 3 of 3 caught.
  - `soc_port_bind_probe.py`: 37 of 37 ports bound.
  - Stop-owed licence plant: caught at one and two interfaces.
  - `srp_wire_compare.py --self-test`: pass.
- **Tree after every probe** (`receipts/tree_verification.txt`):
  - HEAD and tree as above;
  - no tracked, staged or mode difference;
  - every blob hashes to its index entry;
  - gitlinks: `gptp-processor 5dce647a`, `protocol-processor 2ad2f845`, `third_party/lwSRP 9197193e` (initialised in this clone for the firmware gate), `third_party/verilog-axis 48ff7a7e`;
  - submodule work trees clean.

## Real limits

- **Not run here:**
  - Yosys;
  - `xvlog_gate.py`, which needs Vivado;
  - behave;
  - the builder and LiteX export;
  - `test_ctrl_nvm.py`, whose sources this PR does not change;
  - the full 64-suite sweep;
  - the firmware size relink and the out-of-context area run. The size and area figures are the author's.
- **All-fabric byte identity.**
  - The public evidence tree `e1dd23a1/review-evidence/665int-r1` holds the round-2 export at `9b73a8c6`. It does not hold the round-3 export at `bafd6a36` that the REVIEW READY comment cites.
  - My acceptance rests on the round-2 receipt plus a static argument. Between `9b73a8c6` and this head, the changes touch only these:
    - mailbox RTL, which the round-2 receipt shows the default TCL never reads;
    - firmware that is not built into the default images;
    - tests, docs and generators;
    - two keyword arguments inside `CtrlMailbox`, which is built only with `--ctrl-mailbox` (`milan_soc.py:3345`).
  - No bitstream was built.
- **Hosted runs.** A snapshot at review time (`receipts/hosted_check_runs.tsv`) showed 10 successful, 1 skipped and 9 in progress: the Verilator shards, yosys-elaboration, firmware-unit, docs-check and elaborate. I inspected them; I accept none of them.
- **No manager source bank** exists at this head, and I infer none.
- **Physical calibration NOT RUN.** Field skips are not hardware proof.
- **Host GoogleTest is 1.18.0.** The repository's gates accepted it.

## Pending manager duties

- Carry F1 to the author, then re-review it at a new head.
  - Conformance, Tests, Robustness and Docs must be covered again there.
  - RTL is clean at this head. It stays banked only if nothing in its scope changes.
- Validate the current-dev merge candidate with the builder and native banks: base `7c1b52be`, live dev `554e61d2`. Decide hosted and local-replica acceptance.
- Decide the open questions the author published:
  - the M0s area question, open since round 2;
  - whether F3b also takes the `TALKER_DECL` timing difference along with the `DA_GATE` predicate.
- Either publish round-3 receipts (the export at `bafd6a36`, the size and the area) or accept the static argument above.
- Ensure F3b lands before PR 2, as ruling 6092086337 item 4 requires.

R583-2 FINISHED
