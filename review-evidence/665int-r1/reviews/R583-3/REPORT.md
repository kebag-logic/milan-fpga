[R583] NEGATIVE - exact head 232d466312890c978cd6f74e38550a176650fe55

Round R583-3. This is the external, cleared-context independent review of PR #704, issue #665 lane F-INT PR 1 of 2. The PR adds the mailbox publication block.

- Head: `232d466312890c978cd6f74e38550a176650fe55`, tree `3e21bd325e634732436df43f2c08d1bc3eb74f3f`.
- Source base: `7c1b52bee26b497080ee22b1c1986109f80a5ee7`.
- Delta reviewed: `25bbe4d9..232d4663`. That is the ten round-3 commits through `b2aa3ccf`, plus the four round-4 commits (`cc4e54e0`, `e5af02e8`, `0bffed69`, `232d4663`). The whole PR diff against the base was also read.

Reconstruction order:

1. AGENTS.md and CONTRIBUTING.md, then docs/README.
2. Issue #665: the body, plus manager rulings 6087047553, 6087214078, 6087462816, 6087654804, 6088423771, 6092086337 and 6094461419.
3. The executor's public REVIEW READY posts.
4. The linked authorities: `docs/ARCHITECTURE_HW_SW_SPLIT.md`, `docs/design/MAILBOX_SPLIT.md`, `sw/mailbox/mailbox.yaml` and the `milan_datapath.sv` consumers.
5. The diffs and the history.
6. Public executable evidence.

Prior reviewers' reports and scripts were read only after the independent pass over the diff. No manager source bank is claimed or inferred at this head.

## Findings

### R583-3-F1 - MINOR - Conformance, Robustness, Tests, Docs - the census's cone is not fail-closed past the first hop, so a status or processor read can reach the wire and still pass

**Where:**
- `sw/mailbox/publication_census.py:50-55` and `:67-69`: the docstring claim.
- `:447-452`: a statement with no assignment is dropped unless it is an instance.
- `:464-465`: an instance port whose name ends in `_o` or starts with `o_` is never followed.
- `:482-485`: control reads are taken only from `if`/`case`/`for` parentheses.
- `:410`: an always block's event control is consumed and not read.
- `:515-528`: `cone()`.
- `docs/design/MAILBOX_SPLIT.md:886-887`.
- The PR body, "Completeness by construction", third bullet.

**Authority:**
- Ruling 6092086337 item 3: "every wire-affecting read of a processor class-D output ... must map to a block field or a named, ruled exclusion, and the check fails on an unmapped read".
- Ruling 6094461419 item 2: every occurrence must be "a read the census maps to a block field, CSR-status-only use or a ruled exclusion". It asks for a census that fails closed "by construction, not by covering parser forms one at a time".
- The census classifies a read as `status` or `processor` only from the terminals its cone reaches. The docstring says (`:54-55`): "Always blocks are followed as a whole, so the cone over-approximates: a path it cannot rule out counts as reaching the wire."
- MAILBOX_SPLIT.md:886-887 and the PR body say: "A read the census does not map fails the suite, and so does a status read that reaches the wire."

**Evidence:**
- `scripts/census_cone_probe.py`, receipt `receipts/census_cone_probe.txt`. The probe imports the head's census and plants text in memory only.
- Every plant leaves the class-D wire's own occurrence untouched: `assign lwsrp_res_active = |pp_cd_srp_active_w;` is a status row, LWSRP_STATUS. Each plant then adds one hop from that status consumer to another module's input port, which is the wire.
- Control, a plain `assign probe_q = lwsrp_res_active;`: REFUSED with "counted as status, but it reaches the wire at u_probe_sink.a_i".
- `case (1'b1) lwsrp_res_active: probe_q = 1'b1; ...` in an `always_comb`: ESCAPED, 0 findings.
- A function whose body is `return lwsrp_res_active;`, called into `probe_q`: ESCAPED.
- `always_ff @(posedge lwsrp_res_active) probe_q <= 1'b1;`: ESCAPED.
- An input port named `.a_o(lwsrp_res_active)` on a non-CSR instance: ESCAPED.
- The same forms on a population wire itself are refused at this head as unaccounted occurrences. The round-4 rule covers the first hop only, not the nodes of the cone.

**At this head:**
- No status or processor read reaches the wire.
- `scripts/census_textual_cone.py` (`receipts/census_textual_cone.txt`) is an independent, purely textual cone. It treats any occurrence of a cone node as an edge, and any unparsed occurrence as reaching the wire. It follows all 29 status and processor rows: 0 leave their class.
- Its self-test, `receipts/census_textual_cone_selftest.txt`, catches the case-label and function-return plants (2 of 2).
- The gap is in the standing guarantee.

**Impact:**
- PR 2 rewires this same file around the status and GET_STREAM_INFO consumers.
- A later edit that routes one of the 14 status or 15 answer-face consumers onto egress through one of these forms passes the mailbox suite.
- The value would then be read on the wire but not carried by the block: the round-1 defect class.
- The docstring and the design page tell the next author that this cannot happen.

**Required outcome:**
- The cone fails closed by construction, the same way the first hop now does. One way: every non-comment occurrence of every node a status or processor cone visits must be its declaration, its driver or a read edge the census parsed. Any other occurrence either fails or counts as reaching the wire.
- The self-test plants at least the case-label, function-body, event-control and `_o`-named input-port hops from a status consumer, and requires each one refused.
- The docstring, MAILBOX_SPLIT.md and the PR body state only what the check then guarantees.

**Verification:**
- `python3 -I scripts/census_cone_probe.py <tree>`: every plant REFUSED, control included.
- `publication_census.py --check --selftest` and `make -C tb/verilator/mbx`: still 39 checks, 0 failures on the tracked datapath.
- `scripts/census_textual_cone.py <tree>`: still 0.

### R583-3-S1 - SUGGESTION - Tests - `sw/firmware/ctrl/srp/srp_mbx.c:156-191`, `sw/firmware/ctrl/test/srp_mbx.cpp:157` - a partly failed `declare_sources` is not observed on TALKER_DECL

The comment at `srp_mbx.c:78-79` says: "A creation that fails declared nothing the block shows: declare_sources publishes only once every source joined."

The plant `rv-talker-decl-before-the-joins` publishes every source's bit before the joins. It escapes `PubTalkerDeclPrecedesTheDeclarationsAndIsWithdrawnFirst` (`receipts/reviewer_fw_plants_srp.txt`). Across the whole `srp_mbx`, `srp_app` and `srp_rx_retry` suites at one and two interfaces, it is caught only by `srp_app`'s access-count tests, because of the extra write (`receipts/reviewer_srp_wide.txt`). An equal-cost write on the failure path would pass.

The impact is low: such a source is not licensed, and the policing-off case is already a recorded choice. A named test that forces a mid-loop join refusal and asserts that TALKER_DECL stays clear would pin the comment. This item does not affect coverage.

RESIDUE: none.

## Prior public findings at this head

| Finding | Status at `232d4663` | Evidence |
|---|---|---|
| R582-1-F1 (MAJOR): each sink's started level | Resolved | `BINDING.STARTED` on `pub_started_o` (`KL_mbx.sv:317`; stored by the BINDING write at `:300-301`). `acmp.c` `publish()` runs in `transmit()` (`:288`) before any frame, and first in `finish()` (`:490`). `acmp_set_started` publishes before it returns (`:1196-1207`). `port_publish` sends a started-only move as one `BINDING` write that keeps `SID_VALID` (`acmp_mbx.c:71-80`). RTL P2/P3 checks, model twin, `A31TheStartedLevelIsPublishedBeforeItIsPromised` (`test_acmp.cpp:1995`), `B12` (`test_acmp_mbx.cpp:688`). The executor's moved, wrong-field and skipped plants are caught, and so are the reviewer's 4 ACMP/driver plants and 1 RTL plant. Census row `pp_aecp_strm_started_w -> acmpl_stopped_v_w` = `BINDING.STARTED`. |
| R582-1-F2 = R583-1-F1: each source's Talker declarations | Resolved | `TALKER_DECL.DECLARED` on `pub_talker_decl_o` (`KL_mbx.sv:294`, `:355`). Set in `declare_sources` before the declarations are sent (`srp_mbx.c:189`). Withdrawn before reset or destroy removes the participants (`:743`, `:355`). `PubTalkerDeclPrecedesTheDeclarationsAndIsWithdrawnFirst` with 7 plants, all caught. The reviewer's interface-0 plants for set and withdraw are caught at two interfaces. The census maps the CRF interlock (`milan_datapath.sv:5677-5678`, consumer `crft_class_a_w`, which drives `crf_tx.vlan_en_i` at `:6225`) to `TALKER_DECL.DECLARED`. |
| R582-1-F3: `DA_GATE` claimed `acmp_declaring_o` | Resolved as ruled (6092086337 item 4) | `mailbox.yaml` says "address validity only" and names the missing 4.3.3.1 predicate. The MAILBOX_SPLIT choices list gives the egress consequence: with policing off, the split AAF talkers stream once MAAP holds the address. F3b lands the predicate before PR 2. No equivalence claim remains. |
| R583-1-F2: the DA gate's interface | Resolved | `DaGateOpensOnTheAcquiringInterfaceAloneBeforeItsReport` and `DaGateOfEveryInterfaceOpensBeforeItsOwnReport` (`test_maap_mbx.cpp:152`, `:168`) kill `rv-maap-gate-on-interface-0` in the head's `ctrl_mutants.py` (shard receipts). |
| R583-1-F3: idle slope unit | Resolved | `idle_slope_bps` in `mbx_model.h:168`, `bench.hpp`, `frames.hpp` and every user. |
| R582-2-F1 = R583-2-F1 (MINOR): census population and occurrences | Resolved for the first hop | The population comes from the wrapper instance's class-D connections and is checked against `KL_pp_shadow`'s class-D sections. Every occurrence is accounted for: 25 declarations, 25 connections, 39 reads. The prior scripts, unmodified (`receipts/prior_scripts_sha256.txt`), report: `census_probes.py` `probes: 6, unexpected: 0`; `census_escape_probe.py` all REFUSED; `census_textual_crosscheck.py` 25/25/39 with 0 unaccounted. A related gap one hop further out is new: R583-3-F1. |
| R582-2-R1 (RESIDUE) | Applied | `mbx_model.h:162-164` and `mbx_model.c:27` carry the exact wording. |
| R583-2-S2 (ruled required): comparator under a gate | Resolved | The `srpcmp` arm (`ctrl_arms.py`, `arm_srpcmp`) runs in every firmware gate run: 5 controls PASS, 18 plants caught. MAILBOX_SPLIT Verification and the ctrl README name it. |
| R582-2-S1 = R583-2-S1 (SUGGESTION): 32-source mask | Retained as optional, not taken | Unreachable at 16 sources. It does not affect coverage. |

R583-1's `consumer_census.py` was rerun at the head (`receipts/prior_consumer_census_head.txt`). It finds 29 read lines over 24 `pp_cd_*` wires. Every one of them is among the census's 39 reads. The census's extra 10 are 8 reads in `wire x = ...` initialisers, which the line script skips as declarations (`:1765`, `:4912`, `:4913`, `:4915`, `:4918`, `:4919`, `:4920`, `:7327`), and the 2 reads of `pp_aecp_strm_started_w`, a name outside the script's `pp_cd_` pattern.

## Focus items

- **BINDING.STARTED.** Covered in the first row above. A started-only change keeps `SID_VALID`:
  - RTL check P3 "STARTED moves on its own output; the stream_id and BOUND stay";
  - B12, which counts exactly one write to the entry, carrying `bound|valid|started`.

  On a re-bind to another talker, `srp_stop` clears the stream before the response, so the response's publication takes the old stream off (`acmp.c:825-838`). The reviewer's plant that moves `started` after the response on that path is caught by A31.
- **TALKER_DECL.** Covered in the second row above. Write order is checked by tracing `TALKER_DECL` writes against the `SR_DOMAIN` write that starts the recreation, and against each MRPDU's commit.
- **Census.** It runs first in `make -C tb/verilator/mbx` (`Makefile:62-70`; the head of `receipts/mbx_make_all.log`). It reports 39 checks, 0 failures, 25 wires and 89 occurrences, and its self-test passes 0 of 35 arms failed (`receipts/census_head.txt`). It also runs in the hosted exhaustive sweep through `run_all_suites.sh`'s `make -C`. The second hop is open: R583-3-F1.
- **DA_GATE.** Documented as address validity, with no equivalence claim. The egress consequence is named. The datapath shows the gates agree with policing on: `lwsrp_stream_gate` is ACTIVE AND admitted (`milan_datapath.sv:7265-7266`).
- **Two-interface MAAP tests, `idle_slope_bps`.** Resolved; see the table.
- **All-fabric default.** Static inspection:
  - `milan_soc.py` changes only inside `CtrlMailbox` (hunks at `:2511`, `:2534`, `:2556`).
  - The mailbox sources are added only under `--ctrl-mailbox` (`:3343-3346`).
  - The curated default source list (`:1325`) does not name `hdl/milan/mailbox`.
  - `sw/builder` does not reference `sw/firmware/ctrl`.
  - Every other changed path lies under `docs/`, `sw/firmware/ctrl/`, `sw/mailbox/`, `tb/verilator/mbx/` or `hdl/milan/mailbox/`.

  The executor's export-level byte comparison was not re-run (limit).
- **Firmware size.** The gate's own `rv32` arm (pinned SDK, `receipts/rv32_sdk_install.txt`) measures the portable control set's text at 34,716 B at the base and 35,900 B at the head, +1,184 B (`receipts/rv32_arm_size.txt`). This agrees in size with the executor's linked +1,312 B (1x1, SRP adapter included). The linked 81,680 B / 124,176 B figures against 229,376 B were not reproduced: the fixture needs externally provisioned Picolibc and compiler-rt. Either way the image sits far inside the 224 KB limit.
- **Mailbox area.** This is a measurement only, and it was not re-run. The FF arithmetic checks out:
  - 3 × 16 + 32 + 16 + 16 × 67 = 1,168;
  - 4,114 − 2,946 = 1,168;
  - 3,585 − 3,102 = 483 LUT.

## Lens coverage (artifact-specific, exact head `232d4663`)

```text
[R583] UNCLEAN Conformance - sw/mailbox/publication_census.py:50-55,447-485,515-528 vs ruling 6092086337 item 3 / 6094461419 item 2 - R583-3-F1 open; all else applied clean: mailbox.yaml publication block (DA_GATE, LICENCE, IDLE_SLOPE, SR_DOMAIN, TALKER_DECL, BINDING.{BOUND,SID_VALID,STARTED}); acmp.c:198-212,288,490,804-866,1196-1207 vs Milan v1.2 5.3.8.7 and the ARCHITECTURE_HW_SW_SPLIT section 1 ordering rule; srp_mbx.c:64-83,156-191,309-360,718-743,815-833 vs 802.1Q 35.1.2 and the TALKER_DECL contract text; maap_mbx.c:57-63 DA_GATE vs ruling 6092086337 item 4
[R583] PASS RTL - hdl/milan/mailbox/KL_mbx.sv:61-72,150-176,261-322,351-358 (decode, sync-reset storage, field masks, pub_*_o, read mux) and sw/mailbox/mailbox_skeleton.py:56-69,196-200,360-368,585-594 - same reset style as host_write/answer; widths and per-interface/per-sink slicing; mbx make 402/447/32/404/449/389 checks 0 failures; mutants.py 175/175 after controls; reviewer RTL plants 3/3 (STARTED masked by SID_VALID, TALKER_DECL read-back dropped, TALKER_DECL on interface 0 at two interfaces); lint ratchet 90<=90; gen_mailbox --check/--crosscheck/--selftest 0 findings
[R583] UNCLEAN Robustness - sw/mailbox/publication_census.py cone (R583-3-F1); otherwise applied clean: failure/refusal paths of mbx_pub_* (interface/sink refusal, D14), MAAP count > 16 refused at init, static asserts acmp_mbx.c:15 and srp_mbx.c:23, SRP reset/destroy withdrawal order, sink_reset keeping the publish port's view (acmp.c:519-527), two-interface isolation (RTL P2, B10-B12, MAAP and SRP if2 arms)
[R583] UNCLEAN Tests - sw/mailbox/publication_census.py --selftest lacks second-hop plants (R583-3-F1); otherwise applied clean: firmware gate 42 arms incl. srpcmp and rv32 (the 10 RV32 SRP shape arms need --require-rv32, not run), ctrl_mutants 505/505 (shards 169+168+168), SRP plant runs 261/261 and both lwSRP pin arms, reviewer ctrl plants 4/4, reviewer SRP plants 2/3 with S1 noted, fw_coverage PASS 22 files, writer files 100 % lines and branches
[R583] UNCLEAN Docs - publication_census.py:54-55,67-69, docs/design/MAILBOX_SPLIT.md:886-887, PR body "Completeness by construction" overstate the cone (R583-3-F1); otherwise applied clean: docs_check, check_em_dash (0 findings over 494 added lines), gen_toc, measure_naming, check_py_idiom, gen_module_matrix, check_hygiene, git diff --check; DA_GATE/TALKER_DECL choices, area table arithmetic, access-bound figures (SRP 40 per interface = 5+3+32), contract reference
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R583-3-F1) | `mailbox.yaml`, `acmp.c`, `acmp_mbx.c`, `mbx.c`, `maap_mbx.c`, `srp_mbx.c`, `publication_census.py`, `milan_datapath.sv` consumers | R583-3 | `232d466312890c978cd6f74e38550a176650fe55` |
| RTL | CLEAN | `KL_mbx.sv`, `KL_mbx_pkg.sv`, `mailbox_skeleton.py`, `tb_mbx_top.sv`, `milan_soc.py` `CtrlMailbox` | R583-3 | `232d466312890c978cd6f74e38550a176650fe55` |
| Robustness | UNCLEAN (R583-3-F1) | census cone; firmware refusal and failure paths; two-interface isolation | R583-3 | `232d466312890c978cd6f74e38550a176650fe55` |
| Tests | UNCLEAN (R583-3-F1) | census self-test; `suite.hpp`; `mutants.py`; `ctrl_mutants.py`; `srp_pub_mutants.py`; `test_acmp*.cpp`, `test_maap_mbx.cpp`, `srp_mbx.cpp`, `srp_app.cpp`; coverage ratchet | R583-3 | `232d466312890c978cd6f74e38550a176650fe55` |
| Docs | UNCLEAN (R583-3-F1) | `MAILBOX_SPLIT.md`, `ARCHITECTURE_HW_SW_SPLIT.md`, `MAILBOX_CONTRACT.md`, mbx README/Makefile, ctrl/srp/maap READMEs, census docstring, PR body | R583-3 | `232d466312890c978cd6f74e38550a176650fe55` |

## Executed evidence (source head, reviewer clone and scratch tree)

All of the following ran at `232d4663`, in a scratch clone of the reviewer clone with submodules at their gitlinks. lwSRP is a fresh clone of the public repository at `9197193e`. The tool was the pinned Verilator 5.050 (`verilator --version` "5.050 2026-07-01 rev v5.050").

| Command | Result | Receipt |
|---|---|---|
| `publication_census.py --check --list --selftest` | rc 0; 39 checks, 0 failures; 25/25/39; selftest 0 of 35 failed | `receipts/census_head.txt` |
| `make -C tb/verilator/mbx` (census, wb, axil, cosim, if2, quick plants) | rc 0; 402 / 447 / 32 / 404 / 449 / 389, 0 failures; 6 of 6 | `receipts/mbx_make_all.log`, `.rc` |
| `mutants.py --jobs 4` | rc 0; 175 of 175 after controls | `receipts/mbx_mutants_full.log`, `.rc` |
| `test_ctrl_firmware.py --self-test --mutation-shard i 3 --jobs 4` | shard 0 rc 0, PASS: 42 arms incl. `srpcmp` and `rv32`, 169/169 ctrl plants, 261 SRP plant runs, lwSRP pin arms. Shards 1 and 2: 42 arms ok, 168/168 each, then stopped because their unsharded SRP campaign repeats shard 0's | `receipts/fw_selftest_shard{0,1,2}.log`, `shard0.rc`, `shard{1,2}.note` |
| `fw_coverage.py --check --jobs 4` | rc 0; PASS, 22 files | `receipts/gate_fw_coverage.txt` |
| `lint_rtl.py --check --self-test` | rc 0; 90 <= 90 | `receipts/gate_lint_rtl.txt` |
| `gen_mailbox.py --check/--crosscheck/--selftest` | rc 0 | `receipts/gen_mailbox.txt` |
| `srp_wire_compare.py --self-test` | rc 0; 5 controls PASS, 18 plants | `receipts/srp_wire_compare_selftest.txt` |
| docs gates (pinned Markdown environment for em-dash and TOC) | all rc 0 | `receipts/gate_*.txt` |
| reviewer probes: `census_cone_probe.py`, `census_textual_cone.py` (+ selftest) | control refused, 4 escapes; head 0 of 29 leave class; selftest 2/2 | `receipts/census_cone_probe.txt`, `census_textual_cone*.txt` |
| reviewer plants: `reviewer_rtl_plants.py`, `reviewer_fw_plants.py` (ctrl, srp), `reviewer_srp_wide.py` | RTL 3/3; ctrl 4/4; SRP 2/3 (S1) | `receipts/reviewer_*.txt` |
| prior reviewers' scripts, unmodified | consumer census superset holds; probes all refused; 0 unaccounted | `receipts/prior_*.txt` |
| gate `rv32` arm at base and head (`rv32_arm_size.py`) | 34,716 -> 35,900 B text | `receipts/rv32_arm_size.txt` |
| hosted checks at the exact head | 0 check runs, 0 workflow runs at 2026-10-10T07:58Z | `receipts/hosted_checks_snapshot.txt` |
| clone integrity after all work | HEAD/tree exact; index == HEAD tree; 0 worktree blob mismatches; gitlinks at pins | `receipts/clone_integrity.txt` |

All probes planted copies only: in-memory text, or copies under `scratch/`. The reviewer clone was never edited. One receipt (`mbx_make_all.log`) had a host-local include-path prefix redacted to `<pinned-verilator-root>`.

## Real limits

- **Not run here:**
  - Vivado front end (`xvlog_gate.py`), Yosys, builder, LiteX simulations, `fw_service_budget`, `test_ctrl_nvm.py`, `behave`, the 64-suite sweep and `act`, per assignment.
  - The executor's AX7101 export byte comparison and out-of-context area/WNS.
  - The linked `ctrl_srp_image.py` size, which needs externally provisioned Picolibc and compiler-rt. The object-level rv32 arm figure stands in for it.
  - The 10 RV32 SRP shape arms that `--require-rv32` adds: the executor's 52 arms are this run's 42 plus those 10.
- **Toolchain:** the host suites used the host's GoogleTest (1.18) and GCC 16.2.1, not the hosted job's toolchain.
- **Host load:** load averages of 40-80 came from other jobs, so wall times are not representative.
- **Hardware:** physical calibration NOT RUN. No hardware was used. Field skips are not hardware proof.
- **Census scope:** it covers the wrapper's class-D face and the started level, as ruled. Its population comes from section headings in `KL_pp_shadow.sv` (a stated limit). The wrapper's AECP faces are PR 2's to source.

## Pending manager duties

- Hosted evidence at `232d4663`: no check run or workflow run existed at 07:58Z. `rtl-fast`, and after the PR is marked ready the exhaustive Verilator and Yosys contexts, must run on this exact head, or on its successor once R583-3-F1 is answered.
- Current-dev merge candidate (live dev `554e61d299ef7ddb5aca6fb9ce0e6a6cd076d8cb`): builder and native banks, the all-fabric default byte-identity, and the `act` local replica.
- R583-3-F1 must be answered and re-reviewed at a head that includes the change. Conformance, Robustness, Tests and Docs are to be re-covered there.
- RTL is banked clean at `232d4663`. It stays banked only if nothing in its scope changes; a census-only fix does not touch it.

R583-3 FINISHED
