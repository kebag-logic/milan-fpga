[R583] NEGATIVE - exact head 0a8f700fcd67ffee5399b998c99eeeb5e4efbccc

# R583-5: external independent review of PR #704 (#665 F-INT PR 1)

- Head: `0a8f700fcd67ffee5399b998c99eeeb5e4efbccc`, tree `1ea11eb8c51b613469dd8bc86a91d8cc9233e31e` (verified in the detached clone).
- Base of the lane: `7c1b52bee26b497080ee22b1c1986109f80a5ee7`.
- Delta reviewed: `4274a205..0a8f700f`, ten commits:
  - round 5, `d8a24d08..4a99c1e9`: the text census's fail-closed cone, B13, the TALKER_DECL adoption and failed-creation tests;
  - round 6, `6172157f..0a8f700f`: the netlist census, its CI step, the documents, the `srpcmp` arm.
- The round-5 focus in this assignment names `census_netlist.py` and "89 occurrences". At this head round 6 has replaced both: the text reader is deleted and the census reads an elaborated netlist. So this round reviews the head as published and answers the round-5 focus items where they still apply (section 2).
- Sequence: reconstructed from the public state in order (AGENTS.md, CONTRIBUTING.md, docs/README, the issue body, rulings 6087047553, 6087214078, 6087462816, 6087654804 and 6088423771, the round-5 assignment 6095903333, the round-6 assignment 6097292237, the REVIEW READY 6098450429, then the diff and the executable evidence). Sections 1 to 5 were written before any prior review report was read; section 6 was added after.

## 1. Findings

### R583-5-F1 (MINOR): the census sees one parameter shape, so a class-D read in a generate branch that shape prunes passes

- Lenses: Conformance, Robustness, Tests, Docs.
- Where: `sw/mailbox/census_elab.py:366` elaborates `hierarchy -check -top milan_datapath` at the datapath's default parameters. That is `N_STREAMS=1`, `LOOPBACK_P=0`, every optional block present, with the arty_current header.
- Claims that do not hold for the shipping shapes:
  - `sw/mailbox/publication_census.py:12` says it "fails closed";
  - `publication_census.py:20-24` and `docs/design/MAILBOX_SPLIT.md:866` say the way a read is written "does not matter";
  - `MAILBOX_SPLIT.md:840` says "it fails closed";
  - `tb/verilator/mbx/README.md:28` makes the same claim.
- Authority:
  - Ruling 6088423771, decision 2: the block must carry "every class-D value the datapath consumes in the split build".
  - The shipping shapes select other generate branches. `sw/litex/milan_soc.py:922-1096` passes `N_STREAMS`, `LOOPBACK_P`, the audio front end and the optional-block prunes per build. `configs/generated/sweep_opts_arty.sh` builds `--num-streams 4`. `sweep_opts_ax7101.sh` builds `--loopback-lane`. `endstation_ax7101_8x8` has 8 streams.
  - The text census this replaced read every generate branch.
- Evidence, from `scripts/census_probes_r583_5.py` (receipt `receipts/census_probes_r583_5.log`). The census code is unmodified and each plant is an in-memory datapath copy:
  - **S1, accepted with 0 findings:** `pp_cd_srp_over_limit_w` routed onto `crf_tx.vlan_en_i` inside `if (N_STREAMS > 1)`.
  - **S2, accepted with 0 findings:** the same read inside a generate loop with no iteration at `N_STREAMS = 1`.
  - **S3, accepted with 0 findings:** the same read inside `if (LOOPBACK_P != 0)`.
  - **Controls, both refused** with `unmapped read: pp_cd_srp_over_limit_w -> probe_w reaches the wire`:
    - S1c, the same branch taken at the census's shape;
    - S4, the same read masked by the constant `(N_STREAMS > 1)` instead of a generate branch.
  - Every shipping shape can be elaborated, and nothing is misclassified today. `scripts/census_shapes.py` (receipt `receipts/census_shapes.log`) runs the unmodified census over a deferred read with `hierarchy -chparam` and the shape's header, and finds the same 39 reads with 0 findings in each shape:

    | Shape | Netlist cells |
    |---|---|
    | arty_4x4 | 134,974 |
    | ax7101_1x1_tdm8 | 66,810 |
    | 8 streams with the loopback lane | 306,644 |
    | every optional block pruned, gPTP plane off | 63,880 |

- Impact: a class-D read added under a shape-dependent generate branch passes `rtl-fast` with no finding. The split build of that shape would then lack the value, which the census exists to prevent. The limit is stated only in the REVIEW READY open risks, not in the docstrings, MAILBOX_SPLIT.md, the mbx README or the PR body, all of which state the guarantee without it.
- Required outcome, either of:
  - `--check` elaborates every tracked shape (each `configs/generated/endstation_*` header with the datapath parameters its build passes) and fails on a read any shape makes. A self-test plant of a shape-gated read (S1 or S3) is refused by its own words.
  - Or a maintainer decision, recorded on #665, limits the guarantee to one shape. The census docstrings, MAILBOX_SPLIT.md, the mbx README and the PR body then state the limit exactly: default parameters, and generate branches pruned there are not seen.
- Verification: re-run `scripts/census_probes_r583_5.py REPO`. S1, S2 and S3 are REFUSED, or the decision and the stated limit are linked.

### R583-5-F2 (MINOR): four of the census's stated rules have no plant; removing each leaves all 102 self-test arms green

- Lens: Tests.
- Rules that no plant reaches:
  - `sw/mailbox/publication_census.py:331` and `MAILBOX_SPLIT.md:920`: every datapath output is the wire;
  - `publication_census.py:514`: a status read reaching the wrapper fails;
  - `publication_census.py:506`: a field read reaching no wire fails;
  - `publication_census.py:451` and `MAILBOX_SPLIT.md:900`: no bit may have two drivers.
- Authority: AGENTS.md section 6, Tests ("each new test can fail for the defect it claims to detect"). `publication_census.py:78-81` lists these as failures the census raises, and the self-test is the census's only standing regression guard in `rtl-fast`.
- Evidence, from `scripts/census_mutations.py` (receipt `receipts/census_mutations.log`). Each self-test arm is elaborated once, and the self-test's own verdict logic re-runs on that netlist with one rule removed in memory. 11 mutations were run:
  - **6 killed:**
    - terminals by port name, not by cell;
    - any wrapper input counted as the answer face;
    - a memory write that does not lead to its reads;
    - a cell with no output ending the path silently;
    - a mux select or flop clock that leads nowhere (27 arms turn BAD);
    - the population second-driver check.
  - **5 survived** with 0 arms BAD:
    - "a datapath output is not the wire", and the same rule removed in `cone()`;
    - the status-to-wrapper check;
    - the field-reaches-no-wire check;
    - the any-bit two-driver check.
  - The unmodified census does enforce the two rules that matter most. In `receipts/census_probes_r583_5.log`:
    - R1, a status consumer driven to a new datapath output, is refused: `reaches the wire at the datapath output probe_o`;
    - R2, a status consumer ORed into `gsi_avb_chg_i`, is refused: `counted as status, but it reaches the processor wrapper`.
- Impact: a later edit that drops the datapath-output end leaves every gate green. Such an edit could be a change to `terminal()` or `flow()`, or a refactor of how ports are read. A status read that reaches a top-level output, the most direct path to the wire, would then pass. The other three are same-class gaps with lower impact.
- Required outcome: a self-test plant per stated rule, each refused by its own words, so that removing any of the four rules turns at least one arm BAD. At minimum this means the datapath-output rule and the status-to-wrapper rule.
- Verification: `scripts/census_mutations.py REPO` reports these mutations KILLED.

### R583-5-F3 (MINOR): the PR body's round-6 budget figure is contradicted by the exact-head hosted run

- Lenses: Docs, Conformance.
- Where: the PR #704 body, round-6 table, row "Item 4: budget": "at `--jobs 4` on its four cores the census adds about 5 to 6 minutes". The REVIEW READY 6098450429 estimates the job "near 20 of 30".
- Authority: round-6 assignment 6097292237 item 4: "The census must fit its hosted job with margin. Report its run time locally and confirm the job time."
- Evidence: hosted `yosys-elaboration` job 114234325390 at this exact head (receipts `receipts/yosys_elaboration_steps.txt` and `receipts/hosted_yosys_elaboration_census_step.log`):
  - the census step ran 10 min 08 s (14:25:45 to 14:35:53Z), about twice the stated figure;
  - the job ran 24 min 36 s (14:22:54 to 14:47:30Z) of its 30-minute limit, a margin of 5.4 min, not about 10;
  - the census reported `checks: 39 failures: 0` and `selftest: 0 of 102 arm(s) failed; 102 elaborations in 569 s at --jobs 4`.
- Impact: the PR's own evidence for item 4 states a hosted cost and margin that the measured run contradicts. This changes a figure, so it is not wording residue.
- Required outcome: the PR body states the measured hosted figures (census step 10 min 08 s, job 24 min 36 s of 30, margin 5.4 min) in place of the estimate. If the manager judges an 18 % margin too thin, the job's split or limit is decided.
- Verification: a PR body diff, checked against job 114234325390.

### R583-5-R1 (RESIDUE): one stale historical row in the PR body

- Lens: Docs.
- Where: the PR body, round-3 table, row "Item 3: completeness" reads "the census above, run by the mailbox suite's `make`". Since `cac84af7` the census is not in the mailbox suite's default `make`; it runs in `rtl-fast`'s `yosys-elaboration` job and by `make census`.
- Exact fix: replace "run by the mailbox suite's `make`" with "then run by the mailbox suite's `make`; since round 6 by `rtl-fast`'s `yosys-elaboration` job and `make census`".

No BLOCKER or MAJOR was found.

## 2. What was examined, and the clean results

Commands ran in a scratch copy of the head (`scratch/tree`, a `cp -a` of the clone with `third_party/lwSRP` initialised at its gitlink `9197193e`).

Tools:
- sv2v `v0.0.12`: the pinned release, its zip's sha256 `ff8c9eea...5a00` checked as CI checks it;
- Yosys 0.66;
- the pinned Verilator 5.050 (`--version` "Verilator 5.050 2026-07-01 rev v5.050").

Each campaign below had rc 0 (`receipts/campaign_rcs.txt`).

| Campaign | Result | Receipt |
|---|---|---|
| `publication_census.py --check --list` | 25 class-D nets from the `pp_shadow` cell's ports, 4 unread (`acmp_bound_eid`, `srp_domain_change`, `srp_granted_slope_bps`, `srp_lstn_decl_state`); 39 reads of 21 nets: 10 field, 14 status, 15 answer face; PASS; 35 s, 1.18 GB RSS | `census_check_list.log` |
| `publication_census.py --check --selftest --jobs 4` | 39 checks, 0 failures; `selftest: 0 of 102 arm(s) failed` in 375 s; 1.21 GB peak per process | `census_selftest_jobs4.log` |
| `make -C tb/verilator/mbx` (pinned Verilator) | 402 / 447 / 32 / 404 / 449 / 389 checks, 0 failures, 0 `%Warning`; mbx plants 6 of 6 | `mbx_bench.log` |
| `test_ctrl_firmware.py --jobs 4` (arms, without `--require-rv32`) | 50 arms ok, `test_ctrl_firmware: PASS`; `srpcmp` "named controls and plants missing: none"; B13 and both new `Pub*` tests in the passing suites | `fw_gate_arms.log` |
| `scripts/fw_r5_plants.py` | positive control ok; the author's ACMP plant `pub-acmp-adapter-sid-valid-always` killed in `acmp` and `acmpif2` by B13's words; the author's five SRP round-5 plants killed at two and at one interface; six reviewer plants killed (below) | `fw_r5_plants.log` |
| `scripts/srpcmp_arm_probe.py` | the arm's verdict on nine altered comparator reports matches the stated rule (below) | `srpcmp_arm_probe.log` |
| `scripts/census_shapes.py`, `census_probes_r583_5.py`, `census_mutations.py` | see F1 and F2 | as named |

The six reviewer firmware plants:
- ACMP:
  - SID_VALID following `bound`;
  - SID_VALID following `started`;
  - SID_VALID set by `stream_id != 0u || started`.
- SRP:
  - a refused join publishing the sources already joined;
  - the adoption republishing one source short;
  - the adoption dropping source 0 while the Domain is owed.

The nine `srpcmp` cases:
- passing as they should: the real report, an extra plant, an extra control;
- failing as they should: 17 of 18 plants, only one plant, a renamed plant, a missing control, a failing control, no plants.

### Hosted evidence at this exact head

Read from `receipts/hosted_check_runs.json`; the manager owns hosted acceptance.

- `rtl-fast` success, with `yosys-elaboration` success. The census step ran and passed: 39 checks, 0 failures, 102 arms, 0 failed.
- `firmware-unit`, `verilator-lint`, `elaborate`, `docs-check`, `docs-check-no-git`, `wire-accountability`, `bdd-conformance` and `changes`: success.
- Verilator shards 0 to 4/5 and the `verilator-suites` aggregate: success.
- Yosys shards 0 to 3/4 and `yosys-portability`: success.
- `full-ci-gate`: success.
- "Physical gPTP (nightly and manual)" was skipped, not executed. It is no hardware evidence.

### Earlier reviewers' census probes at this head

Scripts were downloaded from `665int-review-evidence@91f09725` (sha256 in `receipts/prior-probes/downloaded_probe_scripts.sha256`) and run unmodified. The in-process ones also ran through `scripts/run_prior_probes.py`, which only appends blackbox definitions of the `KL_probe_sink` and `KL_probe_buf` modules the scripts instantiate. As published, `hierarchy -check` refuses every arm for the undefined module (`R583-3_cone_asis.log`).

| Probe | Result at this head |
|---|---|
| R582-3 `census_cone_probe.py` part 1 | 0 escaping arms. Status `lwsrp_talker_declared` and answer-face `gsi_tkdcl_w`, by positional port, `.name`, case label and function return, are each refused by their read's row at `crf_tx.vlan_en_i` or the probe input; the plain-assign controls are refused |
| R582-3 `census_cone_probe.py` part 2 | Stops on `pc.netlist`, the deleted text reader. Its question, which cone nodes the census does not model, is answered for the netlist by `census_mutations.py` |
| R583-3 `census_cone_probe.py` | The control and 4 forms refused, each `counted as status, but it reaches the wire at u_probe_sink.a_i` or `.a_o` |
| R583-3 `census_textual_cone.py` | Stops on `pc.netlist`; there is no text census at this head to compare it with |
| R582-4 `census_block_probe.py` | 0 escaping arms, 0 controls not refused; `iff` and both `alias` forms refused by sv2v |
| R583-4 `r583_4_census_probes.py` | 13 probes, 0 escapes, 6 controls refused. The nested-parenthesis arm is refused by Yosys for the probe's own undeclared `axis_rst`; the self-test's `axis_resetn` version is refused by dataflow in the hosted log |
| R582-3 `census_extra_forms.py` | 4 of 6 refused. The accepted two build no data dependency: an empty generate `if` on a net, and a level sensitivity list driving a constant. I agree that neither carries a value to the wire in hardware |
| R582-2 `census_probes.py`, R583-2 `census_escape_probe.py` (subprocess, as published) | `unexpected: 0`; 5 of 5 refused, two of them by the undefined `KL_probe_buf` |

### Round-5 focus items that still apply at this head

- **The cone fails closed at every node.** In the netlist census, every cell leads from each input bit to all its output bits, a memory write leads to its reads, and every end is a cell input, a datapath output or a cell with no output. The two terminals are named by cell and port (`publication_census.py:326-338`). This is confirmed by the hosted and local self-test, the reviewer probes above and the six killed mutations. The exception is the shape limit (F1).
- **The parser moved; behaviour is unchanged apart from the cone rule.** At this head the text reader is deleted. The netlist census finds the same 25 nets and the same 39 reads with the same kinds as the text census at `4a99c1e9`; "89 occurrences" is a text-census figure with no netlist meaning.
- **New tests.** B13 kills four SID_VALID plants: the author's and my three. `PubTalkerDeclHoldsAcrossADomainAdoption` kills five adoption plants: three of the author's and two of mine. `PubTalkerDeclIsNotPublishedByACreationThatFails` refuses every allocation of a re-creation in turn and kills three failed-creation plants: two of the author's and one of mine. Each is killed by its named test and words.
- **Hosted rtl-fast and the Verilator shards are green at this head**, as listed above.

### Clean-lens results

```text
[R583] PASS RTL — hdl/ (git diff 4274a205..0a8f700f -- hdl is empty; no RTL file changed since 4a99c1e9), receipts/mbx_bench.log (pinned Verilator 5.050 at this head: 402/447/32/404/449/389 checks, 0 failures, 0 warnings, 6 of 6 RTL plants), hdl/common/csr/milan_csr.sv:2309-2395,2547,2876-2979 (every CSR_READBACK input the census ends a status cone at feeds only live_mux, strm_mux or the snapshot shadow, i.e. CPU read-back) — the census's RTL terminal assumptions checked against milan_csr; the PR's mailbox RTL re-run at the exact head
```

## 3. Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F3) | rulings 6088423771, 6097292237 items 1 to 5, 6095903333 items 1 to 4; `census_elab.py`, `publication_census.py`; B13, `PubTalkerDecl*`; the `srpcmp` arm; hosted job 114234325390 | R583-5 | `0a8f700fcd67ffee5399b998c99eeeb5e4efbccc` |
| RTL | CLEAN | `hdl/` delta (empty), `receipts/mbx_bench.log`, `milan_csr.sv` read-back paths | R583-5 | `0a8f700fcd67ffee5399b998c99eeeb5e4efbccc` |
| Robustness | UNCLEAN (F1) | shape and parameter dependence (`census_shapes.log`, `census_probes_r583_5.log`); the failed-creation and adoption paths of `srp_mbx.c:156-190,630-655,735-745`; `acmp_mbx.c:55-80` | R583-5 | `0a8f700fcd67ffee5399b998c99eeeb5e4efbccc` |
| Tests | UNCLEAN (F1, F2) | `census_plants.py` (98 plants), `census_mutations.log`, `fw_r5_plants.log`, `ctrl_mutants.py:616-625`, `srp_pub_mutants.py:156-194`, `test_acmp_mbx.cpp:731-783`, `srp_mbx.cpp:208-279`, `ctrl_arms.py:415-449`, `srpcmp_arm_probe.log` | R583-5 | `0a8f700fcd67ffee5399b998c99eeeb5e4efbccc` |
| Docs | UNCLEAN (F1, F3; R1 residue) | `MAILBOX_SPLIT.md:833-960,1037-1052`, `ARCHITECTURE_HW_SW_SPLIT.md:88-95`, `CI_WORKFLOWS.md:142-149`, `tb/verilator/mbx/README.md:1-46`, `tb/verilator/mbx/Makefile`, `sw/firmware/ctrl/README.md:221`, `sw/firmware/ctrl/srp/README.md:338-344`, the PR #704 body at this head | R583-5 | `0a8f700fcd67ffee5399b998c99eeeb5e4efbccc` |

## 4. Real limits

- **Yosys build.** The local Yosys is a distribution build of 0.66, not CI's build from the `v0.66` tag. sv2v is the pinned release. Local census figures (39 reads, 102 arms) equal the hosted run's.
- **Firmware gate.** It ran without `--require-rv32`, so the ten RV32 SRP shape arms did not run; the author's 60 arms are these 50 plus those ten. The full firmware plant campaigns (`ctrl_mutants.py` 506, `aecp_mutants.py` 76, the SRP table) and the coverage ratchet were not re-run. Rounds 5 and 6 change no firmware source, and only the round-5 plants and my own were run.
- **Shape parameters.** The shape probe's parameters are reconstructed from `configs/generated/sweep_opts_*.sh` and `milan_soc.py`. The 8-stream case uses the `ax7101_8x8` header with approximated audio parameters, and `arty_8ch` was not run separately. The finding does not depend on these: S1 to S3 plant into the default shape.
- **Census mutations.** They are in-memory replacements of census functions over real elaborations; the census's files were never edited.
- **Clone integrity.** The review clone was never edited; every probe ran in `scratch/tree` or in memory. After the probes, the clone has HEAD `0a8f700f` and tree `1ea11eb8`. `git ls-files -s` hashes equal to `git ls-tree -r HEAD` (blob ids and modes), `git diff-index` is clean, and `git status --ignored` is empty: three `__pycache__` directories my first `--help` run created were removed. The submodule gitlinks are unchanged: `external efeb541a`, `gptp-processor 5dce647a`, `protocol-processor 2ad2f845`, `third_party/lwSRP 9197193e`, `third_party/verilog-axis 48ff7a7e`.
- **Receipt redaction.** In `receipts/mbx_bench.log` the pinned Verilator's image path prefix is replaced by `<pinned-verilator-root>`, as noted in its first line. No other receipt is edited.
- **Not run:** the docs workflow, the builder, the default-image export, the area and size measurements, any Vivado run, act. No manager source bank exists at this head, and none is claimed. Physical calibration was not run, and field skips are not hardware proof.

## 5. Pending manager duties

- Decide F1: elaborate every shape, or rule a one-shape guarantee and have it stated.
- Accept the hosted figures for item 4 (F3).
- Carry R1 to the residue checklist.
- Validate the current-dev merge candidate (source base `7c1b52be`, live dev `e8454e27`) with the builder and native banks at the merge turn, and own hosted and act acceptance.

## 6. Prior public findings on this PR, resolved or retained at this head

(added after the verdict and ledger above were written)

The prior reports were read from the PR #704 comments:
- R583-1 6091895255 and R582-1 6092077028;
- R582-2 6094407605 and R583-2 6094456352;
- R583-3 6095481972 and R582-3 6095579677;
- R582-4 6097151483 and R583-4 6097287404.

No review of this head was published when they were read.

| Prior finding | State at this head | Evidence |
|---|---|---|
| R582-1-F1 (MAJOR), R582-1-F2 = R583-1-F1, R582-1-F3, R583-1-F2, R583-1-F3 | Resolved, as rounds 2 to 4 confirmed | Nothing in `4274a205..0a8f700f` touches the contract, RTL, generator or writer sources; the mbx bench and firmware arms pass at this head (`mbx_bench.log`, `fw_gate_arms.log`) |
| R582-2-F1 = R583-2-F1 (MINOR), the census's standing guarantee | Resolved for the population and the first hop; superseded by the netlist census | Population from the `pp_shadow` cell's class-D ports, checked against the wrapper's class-D sections. R582-2's probes give `unexpected: 0` and R583-2's 5 of 5 are refused (`prior-probes/`). The netlist census's own remaining gap is new: F1 |
| R582-2-R1 (RESIDUE), `mbx_model.h:163` / `mbx_model.c:27` wording | Retained as RESIDUE; unchanged at this head | `sw/firmware/ctrl/host/mbx_model.h:163` still reads "each sink's stream_id only while its SID_VALID is set" |
| R582-2-S1 = R583-2-S1 (SUGGESTION), the 32-source DA gate mask | Retained as optional, not taken | `maap_mbx.c:62` unchanged; well defined at the shipped 16 sources |
| R583-2-S2 (SUGGESTION, required by round 4), the comparator under no gate | Resolved | The `srpcmp` arm runs in every gate run (`fw_gate_arms.log`) |
| R582-3-F1 = R583-3-F1 (MINOR), the cone past the first hop | Resolved at this head | The netlist cone runs through every cell. Both reviewers' `census_cone_probe.py` part 1 arms are refused by dataflow, with the probe modules defined (`prior-probes/R582-3_cone_define.log`, `R583-3_cone_define.log`), and so are the self-test's plants of them (hosted log) |
| R582-3-F2 (MINOR), SID_VALID on a move with no stream | Resolved | B13 plus `pub-acmp-adapter-sid-valid-always`, killed at one and two interfaces; three more reviewer plants killed by B13 (`fw_r5_plants.log`) |
| R582-3-F3 (MINOR), TALKER_DECL across a Domain adoption | Resolved | `PubTalkerDeclHoldsAcrossADomainAdoption`; three author plants killed at one and two interfaces, two reviewer plants killed |
| R583-3-S1 (SUGGESTION, required by round 5), a partly failed `declare_sources` | Resolved | `PubTalkerDeclIsNotPublishedByACreationThatFails`; two author plants and one reviewer plant killed |
| R582-4-F1 (MINOR), block forms the text census missed | Resolved | R582-4's `census_block_probe.py`: 0 escapes, controls refused; its forms are self-test plants refused in the hosted run |
| R582-4-S1 (SUGGESTION, required by round 6), `srpcmp` fails only on no plant | Resolved | `srpcmp_arm_probe.log`: 9 of 9 cases as stated |
| R583-4-F1 (MINOR), begin-less blocks and nested event parentheses | Resolved | `r583_4_census_probes.py`: 0 escapes. The nested-parenthesis arm names an undeclared `axis_rst`; the self-test's `axis_resetn` version is refused by dataflow |
| R583-4-F2 (MINOR), escaped names, included macros, an initialiser | Resolved | The same probe; the self-test's escaped-name, included-macro and second-driver plants are refused (hosted log) |

None of the prior findings changes the verdict. F1, F2 and F3 are new at this head.

R583-5 FINISHED
