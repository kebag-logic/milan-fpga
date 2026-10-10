[R582] NEGATIVE - exact head 0a8f700fcd67ffee5399b998c99eeeb5e4efbccc

Round R582-5, internal independent review of issue #665 / PR #704 (F-INT PR 1, the publication block). Exact head `0a8f700fcd67ffee5399b998c99eeeb5e4efbccc`, tree `1ea11eb8c51b613469dd8bc86a91d8cc9233e31e`, source base `7c1b52be`, PR diff measured against dev `554e61d2` (merged at `26370439`). Lenses covered this round: Conformance, RTL, Robustness, Tests, Docs. Two open MINOR findings, one SUGGESTION, RESIDUE none.

## Scope reconstructed

- Public scope: assignment 6087047553; rulings 6087214078, 6088423771 (decision 2 (a), PR 1), 6092086337 (round 3), 6094461419 (round 4), 6095125193 (round 4b), 6095903333 (round 5) and 6097292237 (round 6). REVIEW READY comments 6096664445 (`4a99c1e9`) and 6098450429 (`0a8f700f`). PR body at this head.
- **Assignment versus head.** This round's assignment names the delta `4274a205..4a99c1e9` (round 5, six commits) and a text census in `sw/mailbox/census_netlist.py`. The published head is four commits later: round 6 (`6172157f`, `cac84af7`, `0058de84`, `0a8f700f`, answering ruling 6097292237) deletes `census_netlist.py` and moves the census onto a netlist elaborated by sv2v and Yosys (`sw/mailbox/census_elab.py`). I reviewed the whole delta `4274a205..0a8f700f` (10 commits, 18 files) at the exact head. Each round-5 focus item is answered below as it applies at this head.
- Delta content:
  - the census (`publication_census.py`, `census_elab.py`, `census_plants.py`);
  - new firmware tests: B13 (`test_acmp_mbx.cpp:736`), `PubTalkerDeclHoldsAcrossADomainAdoption` (`srp_mbx.cpp:213`) and `PubTalkerDeclIsNotPublishedByACreationThatFails` (`srp_mbx.cpp:244`);
  - plants (`ctrl_mutants.py:619-625`, `srp_pub_mutants.py:156-194`) and the `srpcmp` arm (`ctrl_arms.py:415-449`);
  - the census step in `rtl-fast` (`rtl-fast.yml:191-200`, `ci_events.py:2319-2324`);
  - docs.
- The delta changes no file under `hdl/`, `configs/` or `sw/litex/`, nor the mailbox contract, the generator or any firmware source. `git diff --stat 4274a205..HEAD` over those paths lists only `sw/firmware/ctrl/srp/README.md`. The PR's RTL patch against dev is byte-identical to its patch at `232d4663`: the diffs `7c1b52be..232d4663` and `554e61d2..HEAD` over `hdl/` are 248 lines each, equal apart from `index` lines.

## Findings

### R582-5-F1 - MINOR - Conformance, Robustness, Tests, Docs - `sw/mailbox/census_elab.py:10-14,99-107`; `sw/mailbox/publication_census.py:12,14-16,61-62`; `docs/design/MAILBOX_SPLIT.md:836-846`; `docs/ARCHITECTURE_HW_SW_SPLIT.md:91-92`; PR body "Completeness by construction" - the census elaborates one shape, so a read or a status cone in code that shape does not build passes, while the shipped shapes build it

- **Authority/evidence.** Round 4 (6094461419) requires a census that fails closed by construction. The census's own rule is "a path the census cannot rule out reaches the wire" (`publication_census.py:61-62`). Ruling 6092086337 item 3 covers every wire-affecting read. The census elaborates `milan_datapath` once: CI's recipe, `configs/generated/endstation_arty_current` as the shape header, define `SYNTHESIS`, and the module's default parameters (`N_STREAMS = 1`). The builder ships other shapes: `endstation_builder.emit_design_opts` gives `--num-streams 8 --audio-interface tdm32 ...` for AX7101 8x8 and `--num-streams 4` for Arty 4x4. Code those shapes build and the census shape does not is never elaborated, so the census never sees it.
  - `receipts/census_generate_probe.log` uses the census's own `findings()` and an in-memory planted copy, the same routing its `routed` plants use:
    - arm A, a plain unmapped wire read of `pp_cd_srp_over_limit_w`: refused;
    - arm B, the same read inside `if (N_STREAMS > 1) begin ... end`: **ACCEPTED, 0 findings, 39 reads**;
    - arm C, the same copy at the Arty 4x4 shape: refused as `unmapped read: pp_cd_srp_over_limit_w -> probe_w reaches the wire`.
  - `receipts/census_generate_cone_probe.log` makes a one-term edit to an **existing** loop: `& ~lwsrp_talker_declared` in `g_aaf_stream_en` (`milan_datapath.sv:2116-2122`). That loop builds the AAF stream gate of streams 1..N-1 and has no iteration at `N_STREAMS = 1`.
    - Default shape: **ACCEPTED, 0 findings**.
    - Arty 4x4: refused, `pp_cd_srp_tk_decl_state_w -> lwsrp_talker_declared: counted as status, but it reaches the wire at aaf_packetizer.stream_en_i; ...`.
    - Control (stream 0's gate, outside the loop): refused.
  - Today nothing escapes. `receipts/shape_*.log` runs the census at AX7101 8x8, AX7101 1x1 TDM8 and Arty 4x4, each with its own generated header and the builder's parameters. Each gives the same 39 (wire, consumer) reads and classes as the CI shape, PASS.
  - The PR body's limits section states the one-shape limit ("It elaborates one shape, the CI gate's ..."). The census docstrings, `MAILBOX_SPLIT.md:836-846` and `ARCHITECTURE_HW_SW_SPLIT.md:91-92` state "fails closed" without it. The self-test has no plant of this class.
- **Impact.** The standing guarantee is weakest exactly where PR 2 works: the shipped multi-stream shapes and their parameter-dependent generate code. Both kinds of edit pass the `rtl-fast` census while the AX7101 8x8 image (`N_STREAMS = 8`) builds them: a new class-D read on the wire, and a status or answer-face consumer moved onto the wire. The split placement would then lack a value it needs, or the census would count a wire-affecting read as status. The text census it replaced saw every branch.
- **Required outcome.** Either:
  - (a) the census classifies the reads of every shape the builder builds (at least each `configs/*.yaml`, with its generated header and builder parameters), and fails on a read, row or cone end that is unmapped or differs in any shape; or
  - (b) a public ruling accepts the single-shape elaboration as the guarantee.

  Either way, the census docstrings, `MAILBOX_SPLIT.md` and `ARCHITECTURE_HW_SW_SPLIT.md` must state exactly which shapes and defines the guarantee covers, consistent with the PR body. Under (a), a self-test plant equivalent to arm B or arm E must be refused by name.
- **Verification.** Re-run `scripts/census_generate_probe.py` and `scripts/census_generate_cone_probe.py`: arms B and E refused under (a). Under (b), the ruling is linked and the three documents carry the limit. Under (a), also check the hosted `yosys-elaboration` time (see F2).

### R582-5-F2 - MINOR - Conformance, Docs - PR body, Round 6 table, row "Item 4: budget"; REVIEW READY 6098450429 - the census's hosted cost is stated as a pre-push estimate that the hosted run at this head contradicts

- **Authority/evidence.** Ruling 6097292237 item 4: "The census must fit its hosted job with margin. Report its run time locally and confirm the job time." The PR body says that at `--jobs 4` the census "adds about 5 to 6 minutes". REVIEW READY says "the job lands near 20 of 30". Hosted `rtl-fast` run 38059340686 at this head (pull_request merge ref `0e50c0e4`), job `yosys-elaboration` 114234325390:
  - the census step ran 14:25:45 to 14:35:53, **10 min 08 s** (`selftest: 0 of 102 arm(s) failed; 102 elaborations in 569 s at --jobs 4`);
  - the job ran **24 min 36 s** of its `timeout-minutes: 30` (`receipts/hosted_census_step_excerpt.txt`, `receipts/hosted_jobs_38059340686.tsv`).
  - The job had a warm Yosys cache (`Cache hit for: yosys-v0.66-Linux`). No cache miss appears in the last 80 `rtl-fast` runs, so the cold-cache time is not measured.
- **Impact.** The figure the ruling asked to be confirmed is about twice the one recorded, and the margin is 5 min 24 s (18 %), not about 10 minutes. A cold Yosys build in the same job, or slower runners, would eat into that. This changes a measured figure, so it is not RESIDUE.
- **Required outcome.** The PR body records the hosted figures at the head it is merged from (census step and job time against 30 min). Whether that margin satisfies item 4 is decided publicly (the manager owns hosted acceptance): the budget as measured, or a change such as a split job, a raised limit or fewer elaborations. If F1 is fixed by elaborating more shapes, the budget is re-measured with that change.
- **Verification.** The PR body figures match the hosted `yosys-elaboration` log at the merge head, and the decision is linked.

### R582-5-S1 - SUGGESTION - Robustness - `sw/mailbox/census_elab.py:132-136`

The census prints the sv2v and Yosys versions but does not check them against the pins (`syn/yosys/README.md:62-75`). With an unpinned sv2v v0.0.13 it fails closed, but on an unrelated error (`receipts/census_check_sv2v_0013.log`: `Identifier '$time' is implicitly declared`). Refusing a version other than the pinned ones with its own message would make a local refusal self-explaining. Optional; no effect on coverage.

RESIDUE: none.

## Focus items of the assignment, at this head

- **The cone fails closed at every node; terminals by instance and port.** Superseded at this head by the netlist rule of round 6. `terminal()` (`publication_census.py:326-338`) stops a cone only at cell `csr` (kind `milan_csr`) on a `CSR_READBACK` input, or at cell `pp_shadow` (kind `KL_pp_shadow`) on a `PROCESSOR_FACE` input. Every other cell input, every datapath output and every output-less cell is the wire. There is no `_o` naming rule.
  - Yosys cells lead from each input bit to every output bit (`flow`/`step`, `:280-317`), and a memory write leads to its reads.
  - The CSR terminals are trusted as read-back only. I traced each `CSR_READBACK` port inside `milan_csr.sv`: only `live_mux` (`:2309`, `:2369-2377`, `:2395`), the stream-window mux (`:2547`) and the snapshot shadow (`:2876`, `:2906-2979`) read them.
  - At the CI shape, Yosys resizes no port connection (`receipts/census_yosys_warnings.log`: 6 warnings, all memory-to-register, 0 resize or width). So no connection bit of a blackboxed cell is dropped. The single-shape limit is F1.
- **Parser moved to `census_netlist.py`; 25 / 89 / 39.** `census_netlist.py` no longer exists at this head; round 6 deleted it. The netlist census gives 25 class-D nets from the wrapper cell's ports, 39 reads of 21 nets and 4 unread nets: 10 field, 14 status, 15 answer face, PASS (`receipts/census_check_list.log`). `CENSUS`, `CLASS_D_PORTS`, `CSR_READBACK`, `PROCESSOR_FACE`, `STARTED` and `STARTED_PORT` are AST-identical to those at `4a99c1e9` and at `4274a205`. Run on the head's text, R583-2's textual tally still counts 25 declarations, 25 wrapper connections and 39 other occurrences (89). Its 39 equals the netlist read count, but it cannot map them, because the netlist listing has no source lines (`receipts/reviewer_probes/R583-2_census_textual_crosscheck.log`).
- **Both reviewers' `census_cone_probe.py` parts 1 and 2; plain-assign controls; R583-3's `census_textual_cone.py`.** These are the published scripts, unmodified (sha256 in `receipts/reviewer_probe_scripts.sha256`, matching the digests earlier rounds cite).
  - R582-3 part 1, run as published: the plain-assign control is refused by its dataflow. The positional-port arm instantiates the undefined `KL_probe_buf`, which `hierarchy -check` refuses, and the script stops there.
  - With the probe modules defined (`scripts/run_reviewer_probe.py --define-modules`), all 10 arms are refused by dataflow, both consumers' controls included. Each names its row and the port it reaches (`u_probe_pos.a`, `u_probe_dot.lwsrp_talker_declared`, `crf_tx.vlan_en_i`, ...).
  - R582-3 part 2 and R583-3's `census_textual_cone.py` call the deleted text reader (`pc.netlist(text)`) and stop. They do not apply to a netlist census.
  - R583-3 `census_cone_probe.py`: 5 of 5 refused as published (undefined module), and 5 of 5 refused by dataflow with the modules defined, the `_o`-named input included (`u_probe_sink.a_o`).
  - R582-4 `census_block_probe.py` with modules defined: E1, E2, E3 and E5 and the controls are refused by dataflow. E4 (`iff`) and both `alias` forms are refused by sv2v.
  - R583-4 probes: 13 probes and 6 controls refused. The nested-parenthesis arm names `axis_rst`, which the datapath does not declare. The census's own plant of that form uses `axis_resetn` and is refused by dataflow (`receipts/census_selftest.log`, lines 77 and 82).
  - R582-2 `census_probes.py`: 6 probes, 0 unexpected. R583-2 `census_escape_probe.py`: 5 of 5 refused.
  - R582-3 `census_extra_forms.py`: 4 of 6 refused. The 2 accepted forms build no hardware dependency: an empty generate `if` on a non-constant condition, and a level-only sensitivity list driving a constant. Accepting them is correct.
- **The census's own self-test.** `--check --selftest --jobs 6` at this head with the pinned sv2v v0.0.12 and Yosys 0.66: 39 checks, 0 failures; `selftest: 0 of 102 arm(s) failed`. Both controls are clean, and every arm is refused by its own words (`receipts/census_selftest.log`, 420 s, peak 1.2 GB per elaboration).
- **New tests and plants** (`scripts/fw_focus_probe.py`, the gate's own arms and campaigns):
  - B13 passes in `acmp` and `acmpif2`.
  - `pub-acmp-adapter-sid-valid-always` is killed by B13 at both arms; the first failure is B13's own words.
  - `Srp.PubTalkerDecl*` (3 tests) pass at two and at one interface.
  - The five round-5 SRP plants are each killed by their named test and words at two interfaces and again at one: `pub-declared-dropped-at-adoption`, `-withdrawn-after-the-adoption`, `-skipped-at-adoption`, `-before-the-joins` and `-as-each-source-joins` (`receipts/fw_*.log`).
  - Reading the tests:
    - B13 asserts that the unbind leaves the old stream_id in `SID_LO`/`SID_HI`, then that every write of the rebind and of both started moves is `BINDING` alone with `SID_VALID` clear.
    - The adoption test pre-writes a value the firmware did not write, so a skipped publication shows, and reads `TALKER_DECL` at each Talker MRPDU's commit under the adopted VID.
    - The failed-creation test refuses each allocation of a link restart's re-creation in turn, so a refusal lands between the two sources' joins.
- **`srpcmp` arm (R582-4-S1).** `scripts/srpcmp_arm_probe.py` sends doctored copies of the comparator's real report through the arm, 8 of 8 as expected:
  - the tracked report and an added plant pass;
  - a dropped, renamed or nearly emptied plant list, a dropped control, a failed control and an empty list each fail.
  - The comparator exits non-zero on an escaped plant (`srp_wire_compare.py:250`), so "present" also means "caught".
- **Hosted `rtl-fast` and Verilator shards at this head.** Run 38059340686 (`rtl-fast`): `changes`, `bdd-conformance`, `verilator-lint`, `yosys-elaboration` (census step included) and `firmware-unit` succeeded, and so did the `rtl-fast` aggregate. Run 38059340673 (`rtl-full`): `full-ci-gate`, Verilator shards 0-4, Yosys shards 0-3, `verilator-suites` and `yosys-portability` succeeded; `Physical gPTP (nightly and manual)` was **skipped** (not run). `elaborate` (38059340693) and `docs` (38059340684: `docs-check`, `docs-check-no-git`, `wire-accountability`) succeeded.
  - The pull_request runs built merge ref `0e50c0e4`, which is this head merged into live dev `e8454e27`, not the bare head.
  - `mbx` passed in Verilator shard 2/5. `firmware-unit` ran the B13 plant, the round-5 SRP plants at both interface counts and `srpcmp` ("named controls and plants missing: none").
  - Excerpts: `receipts/hosted_*`. Hosted acceptance remains the manager's.

## Prior public findings at this head

| Finding | Status at `0a8f700f` | Evidence |
|---|---|---|
| R582-1-F1 (MAJOR), R582-1-F2 = R583-1-F1, R582-1-F3, R583-1-F2, R583-1-F3 | Resolved, unchanged since (no RTL, contract, generator or writer source in this delta) | PR RTL patch identical to `232d4663`'s; exact-head mbx bench below |
| R582-2-F1 = R583-2-F1 (census population, fail closed) | Resolved | Population from the wrapper cell's ports (`population()`, `publication_census.py:414-448`); R582-2 and R583-2 probes refused |
| R582-2-R1 (RESIDUE) | Applied (unchanged in this delta) | `mbx_model.h`, `mbx_model.c` not touched since `232d4663` |
| R583-2-S2 (ruled required) | Resolved | the `srpcmp` arm, run hosted |
| R582-3-F1 = R583-3-F1 (cone past the first hop) | Resolved for every published form, by the netlist rule | All probes refused (above); the census's 102-arm self-test. The single-shape limit is new and recorded as R582-5-F1 |
| R582-3-F2 (`SID_VALID` on a stream-less move) | Resolved | B13 and its plant |
| R582-3-F3 (`TALKER_DECL` across an adoption) | Resolved | adoption test and three plants at both interface counts |
| R583-3-S1 (partly failed creation, ruled required) | Resolved | failed-creation test and two plants at both interface counts |
| R582-4-F1 = R583-4-F1 (begin-less blocks, `iff`, compound assignment, `alias`) | Resolved | refused by dataflow, or by sv2v for `iff`/`alias` (`census_selftest.log` lines 56-93; R582-4 and R583-4 probes) |
| R583-4-F2 (escaped names, included macros, initialiser as second driver) | Resolved | `guard()` refuses an escaped name holding `//` or `/*`; included macro and `"`-escaped name refused as unmapped reads; initialiser refused as a second driver (R583-4 probes) |
| R582-4-S1 (required by ruling 6097292237) | Resolved | `srpcmp_arm_probe.log` 8 of 8 |
| R582-2-S1 = R583-2-S1, R583-1-S1/S3 | Optional, not taken | No effect on coverage |

## Lens results

```text
[R582] UNCLEAN Conformance - sw/mailbox/publication_census.py:12,61-62; census_elab.py:10-14; PR body Round 6 "Item 4: budget"; hosted job 114234325390 - R582-5-F1 (fail-closed guarantee covers one shape) and R582-5-F2 (job time not confirmed; hosted 24 min 36 s of 30) open. Applied clean otherwise: ruling 6097292237 items 1-3 and 5 (CI recipe, hierarchy kept, proc passes, population and cone from the netlist, table byte-identical, 102 arms), 6095903333 items 2-4 (B13, adoption, failed creation, each with plants), R582-4-S1.
[R582] PASS RTL - hdl/ unchanged in 4274a205..0a8f700f; PR RTL patch vs dev identical to 232d4663's (248-line diff); milan_csr.sv:2309-2395,2547,2876-2979 (CSR_READBACK terminals are read-back only); KL_pp_shadow class-D face = CLASS_D_PORTS (census population check, 25 nets); Yosys elaboration of milan_datapath at 4 shapes, 0 resize warnings at the CI shape; exact-head tb/verilator/mbx with Verilator 5.050: 402 / 447 / 32 / 404 / 449 / 389 checks, 0 failures, 0 warnings, quick plants 6 of 6.
[R582] UNCLEAN Robustness - milan_datapath.sv:2116-2122 (g_aaf_stream_en) via scripts/census_generate_cone_probe.py - R582-5-F1 open (configuration-dependent code not elaborated). Applied clean otherwise: unpinned sv2v fails closed; escaped-name guard; second driver and multiple-driver checks; tool refusal paths; the failed-creation test at every allocation; B13 over a stale stream.
[R582] UNCLEAN Tests - sw/mailbox/census_plants.py (no configuration-dependent plant) - R582-5-F1 open. Applied clean otherwise: census self-test 0 of 102 failed; every reviewer probe refused (modules defined); B13 kills its plant; 5 round-5 SRP plants killed at 1 and 2 interfaces; srpcmp arm 8 of 8 doctored reports as expected.
[R582] UNCLEAN Docs - docs/design/MAILBOX_SPLIT.md:836-846, docs/ARCHITECTURE_HW_SW_SPLIT.md:91-92, publication_census.py:12 (fails closed, no shape limit) vs PR body limits; PR body budget row - R582-5-F1, R582-5-F2 open. Applied clean otherwise: docs_check 0 findings (202 md); check_em_dash --base 554e61d2 0 over 593 added lines; gen_toc --check OK; check_baremetal_only --check 0; check_py_idiom OK; ci_events --check OK (1757 items); CI_WORKFLOWS.md, mbx README/Makefile and srp/ctrl READMEs match the code; no stale census_netlist reference.
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R582-5-F1, R582-5-F2) | rulings 6094461419, 6095903333, 6097292237; census code; PR body; hosted job 114234325390 | R582-5 | `0a8f700fcd67ffee5399b998c99eeeb5e4efbccc` |
| RTL | CLEAN | PR RTL patch; `milan_csr.sv` read-back paths; netlist at 4 shapes; exact-head mbx bench | R582-5 | `0a8f700fcd67ffee5399b998c99eeeb5e4efbccc` |
| Robustness | UNCLEAN (R582-5-F1) | census elaboration, guards, driver checks; shape and generate probes; failure-path tests | R582-5 | `0a8f700fcd67ffee5399b998c99eeeb5e4efbccc` |
| Tests | UNCLEAN (R582-5-F1) | census self-test; reviewer probes; B13, adoption and failed-creation tests and their plants; `srpcmp` arm | R582-5 | `0a8f700fcd67ffee5399b998c99eeeb5e4efbccc` |
| Docs | UNCLEAN (R582-5-F1, R582-5-F2) | `MAILBOX_SPLIT.md`, `ARCHITECTURE_HW_SW_SPLIT.md`, `CI_WORKFLOWS.md`, mbx README/Makefile, ctrl and srp READMEs, docstrings, PR body; docs gates | R582-5 | `0a8f700fcd67ffee5399b998c99eeeb5e4efbccc` |

The verdict and this ledger were fixed before I read any earlier round's findings text (unpublished scratch draft, 2026-10-10T18:54:27+02:00). The earlier findings were then checked against them (table above), and neither changed.

## Executed evidence (exact head, reviewer clone and scratch)

Tools: sv2v v0.0.12 (release zip sha256 `ff8c9eea...5a00`, as `rtl-fast.yml:176` pins), Yosys 0.66 (git sha1 `86f2ddebc`, the same as the hosted job's), Verilator 5.050 (scoped binary, `--version` checked). All commands ran in the foreground or were waited on; every rc is in `receipts/`.

| Command (scripts relative to this packet) | Result | Receipt |
|---|---|---|
| `publication_census.py --check --list` | 25 nets, 39 reads, 4 unread, PASS, 40 s, 1.18 GB | `census_check_list.log` |
| `publication_census.py --check --selftest --jobs 6` | 0 of 102 arms failed, rc 0, 7 min 56 s | `census_selftest.log` |
| `scripts/census_shape_probe.py` at the default shape, AX7101 8x8, AX7101 1x1 TDM8 and Arty 4x4 | 39 identical reads, PASS at each | `shape_*.log` |
| `scripts/census_generate_probe.py` | A refused, **B accepted**, C refused | `census_generate_probe.log` |
| `scripts/census_generate_cone_probe.py` | D refused, **E accepted**, F refused | `census_generate_cone_probe.log` |
| `scripts/census_yosys_log.py` | 6 memory warnings, 0 resize | `census_yosys_warnings.log` |
| `publication_census.py --check` with sv2v v0.0.13 | rc 2 (refused) | `census_check_sv2v_0013.log` |
| `scripts/run_reviewer_probe.py` and the published probes | as listed in the focus items | `reviewer_probes/` |
| `scripts/fw_focus_probe.py` (5 parts) | all rc 0, 1 + 5 + 5 plants caught | `fw_*.log` |
| `scripts/srpcmp_arm_probe.py` | 8 of 8 | `srpcmp_arm_probe.log` |
| `make -C tb/verilator/mbx -j16` (exported head) | 402/447/32/404/449/389, 0 failures, 6/6 plants | `mbx_make.log` |
| docs and CI gates (`docs_check`, `check_em_dash --base 554e61d2`, `gen_toc --check`, `check_baremetal_only --check`, `check_py_idiom`, `ci_events --check`) | all rc 0 | `gate_*.log` |
| clone integrity after probes | HEAD, tree and index `1ea11eb8`; worktree and index equal HEAD; gitlinks at pins; no untracked or ignored files left | `clone_integrity.txt` |

## Real limits

- The shape probes use my mapping from the builder's design options to datapath parameters. I took the AX7101 8x8 TDM32 master clock as 98.304 MHz, because the elaboration guard refuses the default; Arty 4x4 has `AUDIO_IF_I2S_PAIR_P = 1`. A shape's other SoC-side parameters (descriptor bases, ROM paths) do not affect class-D reads.
- The cold-cache hosted time of `yosys-elaboration` is not measured.
- I did not run the full firmware gate (`test_ctrl_firmware.py --require-rv32 --self-test`), the full RTL plant table, Yosys over every top, the builder, export, size or area banks, LiteX simulations or `act`. This delta changes none of their inputs. For source-head execution, the author's published receipts and the hosted runs (merge ref) are the evidence.
- No manager source bank was run at this exact head, and none is claimed or inferred.
- Physical calibration NOT RUN. The hosted `Physical gPTP` job was skipped. Field skips are not hardware proof.

## Pending manager duties

- Rule on R582-5-F1: elaborate every shipped shape, or accept the single-shape guarantee with the limit documented consistently.
- Decide whether the hosted margin of `yosys-elaboration` (24 min 36 s of 30 at this head) meets ruling 6097292237 item 4 (R582-5-F2).
- Validate the current-dev merge candidate (source base `7c1b52be`, live dev `e8454e27`) with the builder and native banks at the merge turn, and own hosted and act acceptance.
- Carry R582-5-S1 as optional.

R582-5 FINISHED
