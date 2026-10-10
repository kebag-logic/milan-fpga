[R583] POSITIVE - exact head 67c1285b3b28b12a3af4f3f3aae6e92befd5febb

# R583-6: external independent review of PR #704 (#665 F-INT PR 1, the publication block)

Round R583-6, cleared context. Exact published head `67c1285b3b28b12a3af4f3f3aae6e92befd5febb`, tree
`dd07654c71dc292cd5055793bd038691f06fa1a0`. Source base `7c1b52bee26b497080ee22b1c1986109f80a5ee7`; the
lane's own delta was read against the merged dev `554e61d299ef7ddb5aca6fb9ce0e6a6cd076d8cb` (63 files, 44
first-parent commits); the rest of `7c1b52be..67c1285b` is F5 (#700) and #701/#699, merged by the round-4b
assignment. Public review start: #704 comment 6101391772.

No BLOCKER, MAJOR or MINOR finding is open at this head. Two SUGGESTIONs and two RESIDUE items are recorded
below; none leaves a lens unclean. Every earlier public finding on this PR is resolved at this head (section 4).

## 1. Scope reconstructed

From AGENTS.md, CONTRIBUTING.md (by reference), the #665 body and the manager's comments:

- Assignment 6087047553 and ruling 6088423771 split F-INT into two PRs. **PR 1 (this one):** a publication
  block in the mailbox window carrying every class-D value the split datapath reads (decision 2 (a)); the
  firmware writers, each before the response that promises the value; GoogleTest ordering tests with the
  three plants per writer (moved after the response, wrong field, skipped); an RTL simulation of the block
  with plants; the all-fabric image byte-identical to dev; the firmware size against 224 KB; the mailbox area
  as a measurement. VERSION unchanged. The build switch, the two-placement simulation and both images are PR 2.
- Round 3 (6092086337): add the started level and the Talker declarations; a standing census mapping every
  wire-affecting read of a class-D output to a block field or a ruled exclusion; DA_GATE stays address
  validity as a public choice (F3b adds the predicate); the two-interface DA-gate test; `idle_slope_bps`.
- Rounds 4, 4b, 5, 6 (6094461419, 6095125193, 6095903333, 6097292237): the census fails closed, from the
  wrapper cell's ports, through a cone that fails closed at every node, computed from the elaborated netlist;
  dev merged (F5); B13, the adoption and failed-creation `TALKER_DECL` tests; `srpcmp` under a gate.
- **Round 7 (6100024293), the frozen acceptance for this head:** (1) elaborate every shape the builder builds,
  parameters from the builder, failing on anything unmapped in any shape or differing between shapes, with
  R583-5 S1/S2/S3 and R582-5 arms B and E planted at a shape that builds them, and the documents naming the
  shapes and defines; (2) a plant for each stated rule and a standing rule-removal mutation check; (3) the
  census in its own `rtl-fast` job, required by the aggregate and pinned by `ci_events.py`, using at most 60 %
  of its timeout at the head, with a cold-cache estimate, the hosted figures being the manager's to report;
  (4) refuse unpinned sv2v or Yosys naming both versions; (5) apply R583-5-R1.

## 2. Findings

### R583-6-S1 (SUGGESTION): gate 23m holds a hand list of configurations; the census elaborates `configs/*.yaml`

- Lenses: Tests, Robustness.
- Where: `sw/builder/test_builder.py:347` (`CONFIGS`, five hand-listed configs) and `:23379` (gate 23m iterates
  `CONFIGS`) against `sw/mailbox/census_elab.py:170` (`shapes()` globs `configs/*.yaml`).
- Evidence: `receipts/probes/config_coupling.log`. A sixth config added to a disposable copy is elaborated by
  `shapes()` at `datapath_params()`'s values, while gate 23m's list does not contain it, so no gate holds that
  shape's parameters to the Instance `milan_soc.py` builds until someone also edits `CONFIGS`. At this head the
  two sets are equal (5 = 5), so nothing is wrong today and the round-7 requirement ("parameters from the builder
  itself, never from a list in the census") is met.
- Suggested outcome: gate 23m iterates the same `configs/*.yaml` glob, or a gate asserts that `CONFIGS` covers it.
- Verification: the coupling probe reports no config "elaborated by the census but not held by gate 23m".

### R583-6-S2 (SUGGESTION): PR 2 also needs the talker destination address of the parent `KL_maap`

- Lenses: Conformance, Docs.
- Where: `hdl/milan/milan_datapath.sv:1948-1949` (`eff_aaf_dmac` takes `maap_addr` while `maap_addr_valid`),
  `:2008` (`aaf_gate`'s MAAP term), `:7168-7187` (the parent `KL_maap` instance); ruling 6088423771 decision 1
  removes that parent `KL_maap` in the split placement.
- Evidence: the census population is the processor wrapper's class-D face by ruling, so `KL_maap`'s
  `addr_o`/`addr_valid_o` are outside it. The address is already in the mailbox (`MAAP_BASE_LO`/`HI`,
  `sw/mailbox/mailbox.yaml:158`, written by the MAAP adapter before the allocation is reported), but `KL_mbx`
  exports no port for it, and neither the PR body's known limitations nor the design page's open items name it.
  This is not PR 1's acceptance (decision 2 lists the class-D values), so it is a suggestion.
- Suggested outcome: name the parent `KL_maap`'s address and validity as a PR 2 item (export `MAAP_BASE` or
  equivalent) in the known limitations or `MAILBOX_SPLIT.md`'s open items.
- Verification: the text names it.

### R583-6-R1 (RESIDUE): the PR body's round-3 "Item 3: completeness" row predates round 7

- Lens: Docs. Wording in the PR body only.
- Where: PR body, Round 3 table, row "Item 3: completeness": "...; since round 6 by `rtl-fast`'s
  `yosys-elaboration` job and `make census`". Since `cb63ff0a` the census runs in its own `publication-census` job.
- Exact fix: replace "since round 6 by `rtl-fast`'s `yosys-elaboration` job and `make census`" with "since round 6
  by `rtl-fast`'s `yosys-elaboration` job, since round 7 by its own `publication-census` job, and by `make census`".

### R583-6-R2 (RESIDUE): a Makefile comment states the census's reach more broadly than the census

- Lens: Docs. A code comment only; no target, test or figure changes.
- Where: `tb/verilator/mbx/Makefile:64-65`: "the block must carry every value the split datapath consumes".
  The census covers the wrapper's class-D face and the started level (as `MAILBOX_SPLIT.md:1030-1037` and the PR
  body's limits say); the AECP faces and the parent `KL_maap` are outside it.
- Exact fix: "the block must carry every class-D value of the processor wrapper that the split datapath reads on
  the wire".

## 3. Lens results (each with the artifact examined at this head)

[R583] PASS Conformance - issue #665 body; rulings 6088423771, 6092086337, 6094461419, 6095125193, 6095903333, 6097292237, 6100024293 items 1-5; `hdl/milan/mailbox/KL_mbx.sv:159-176,271-321,351-358`; `sw/mailbox/mailbox.yaml:304-415`; `sw/mailbox/census_elab.py`, `publication_census.py`, `census_rules.py`, `census_selftest.py`; `sw/builder/endstation_builder.py` `datapath_params`; `.github/workflows/rtl-fast.yml` job `publication-census`; hosted job 114284711008 - each round-7 item checked against code and run: six shapes from the builder (`receipts/local/census_check_selftest.log`, hosted log), S1/S2/S3/B/E and the four rule plants refused by their words, 31 rules each proven by removal, pins refused naming both versions, the job 14 min 08 s of `timeout-minutes: 45` (31 %) at this head with all shapes and the self-test, required by the aggregate and pinned by `ci_events.py --check` (rc 0); the writers' order matches ruling 6088423771 and the placement contract (`acmp.c:198-212,288,490`, `maap_mbx.c:62`, `srp_mbx.c:61-83,157-190,258,339-355,650,729-743,819-832`). The public reading "a cone end that differs between shapes" compared as classes of end is accepted: per shape every status or answer-face read reaching any wire already fails, so a per-port comparison adds nothing to publication completeness and fails unchanged RTL (`i_tlk_lobs_v` from four streams up). S2 is a suggestion only.

[R583] PASS RTL - `hdl/milan/mailbox/KL_mbx.sv:90` (full-strobe write), `:159-176` (decode: offset, interface and sink fields, holes, absent interfaces), `:271-303` (reset and masked writes), `:305-321` (outputs), `:351-358` (read mux); `KL_mbx_pkg.sv:300-358`; `mailbox_model.py` `_check_publication` and `mailbox_skeleton.py:575-580` (power-of-two strides); `receipts/local/mbx_bench.log` (pinned Verilator 5.050: 402/447/32/404/449/389 checks, 0 failures, 6 of 6 quick RTL plants); `receipts/probes/csr_readback_cone.log` (the census's CSR terminal trust: each of the 8 `CSR_READBACK` inputs of `milan_csr`, elaborated and flattened, reaches only `s_axi_rdata`); hosted Yosys shards 0-3/4 and `verilator-lint` success at this head - single clock domain, synchronous active-low reset clears every register, widths and indexing bounded by `pub_at_w`, no new CDC in this PR (the `pub_*_o` consumer and its crossing are PR 2's, `MAILBOX_SPLIT.md:1331-1335`). No RTL, contract, generator, firmware or bench source changed since `0a8f700f`.

[R583] PASS Robustness - `tb/verilator/mbx/suite.hpp` P1-P5 (masks, isolation, SID_VALID, holes/absent interface/partial strobe, reset) passing in `receipts/local/mbx_bench.log`; `receipts/probes/census_probes_verdicts.txt` (four shape-gated reads not in the author's plants, under `TALKER_WIRE_CHANS_P > 4`, `AUDIO_IF_RENDER_SLOTS_P != 0`, `GPTP_INGRESS_LAT_NS_P != 0` and a status read on the wire only under `N_STREAMS > 7`, each refused in exactly the shapes that build it; the unbuilt-branch control accepted, the disclosed limit); failure and boundary writer paths (`receipts/plants/*`: an owed stop publishing a stale licence, destroy's licence after its reports, MAAP refusing the contract's 16 sources, each caught) - the census fails closed on shape-dependent code the builder builds, unpinned tools and refused forms; the writers hold on reset, destroy, failed creation and boundary counts.

[R583] PASS Tests - `receipts/local/census_check_selftest.log` (0 of 120 arms failed, 0 of 31 rules unproven; same as the hosted job); `receipts/plants/*.fails.txt` (five independent writer plants, none in `ctrl_mutants.py` or `srp_pub_mutants.py`, each caught by a named test: `B10`/`D14` for a stream_id move that skips the SID_VALID clear, `PubLicenceIsSetAndClearedBeforeEachChangeIsReported` twice, `A31LeavingSettlementTakesTheStreamOffTheDatapath`/`A31OnlyAMovedTripleIsPublished`, `DaGateIsPublishedBeforeEachAllocationIsReported`); `receipts/local/firmware_gate_positive.log` (60 arms, `srpcmp` ok, PASS); hosted `firmware-unit` job 114284710904 at this head (`mutants: 506 of 506 caught`, every `pub-declared-*` plant at both interface counts, `firmware coverage: PASS (30 files)`); gen_mailbox `--check`/`--crosscheck`/`--selftest` rc 0 - each new test can fail for its defect; S1 is a suggestion only.

[R583] PASS Docs - `docs/design/MAILBOX_SPLIT.md:802-1120`, `docs/ARCHITECTURE_HW_SW_SPLIT.md:88-98,192`, `docs/testing/CI_WORKFLOWS.md` (the `publication-census` paragraph and lists), `tb/verilator/mbx/README.md:1-46` and Makefile, census docstrings, generated `docs/reference/MAILBOX_CONTRACT.md` (gen `--check` clean), the PR body; `receipts/local/gate_*.log` (`docs_check` 0, `check_em_dash` 0 over 679 added lines, `git diff --check`, `check_baremetal_only`, `gen_module_matrix --check`, `measure_naming`, `check_py_idiom`, `lint_rtl`, `ci_events --check`, `guard_selftest` all rc 0) - shapes, define, rules, job and counts (6 shapes, 25 nets, 39 reads, 118 plants plus 2 controls, 31 rules) match the code and both runs; R1 and R2 are wording only.

## 4. Earlier public findings on this PR, resolved or retained at this head

| Finding | State | Evidence at this head |
|---|---|---|
| R582-1-F1 (MAJOR, started level) | Resolved | `BINDING.STARTED`, `pub_started_o`; bench P2/P3; hosted A31/B12 and plants; local positive gate |
| R582-1-F2 = R583-1-F1 (Talker declarations) | Resolved | `TALKER_DECL`; `PubTalkerDecl*` tests; hosted `pub-declared-*` plants |
| R582-1-F3 (DA_GATE meaning) | Resolved as ruled | contract and design page state address validity and the egress consequence; F3b named |
| R583-1-F2 (gate per interface) | Resolved | `DaGateOpensOnTheAcquiringInterfaceAlone...`; `rv-maap-gate-on-interface-0` in the hosted 506 |
| R583-1-F3 (`idle_slope_bps`) | Resolved | `pub_idle_slope_bps_o`, harness views |
| R582-2-F1 = R583-2-F1 (fail closed) | Resolved, superseded by the netlist census | population from `pp_shadow`'s ports; selftest arms |
| R582-2-R1 (RESIDUE, model comments) | Applied | `mbx_model.h:162-163` and `mbx_model.c:27` carry the exact text (R583-5's "retained" row read it wrongly) |
| R582-2-S1 = R583-2-S1 (32-source mask) | Optional, not taken | unchanged; defined at the contract's 16 sources |
| R583-2-S2 (comparator under a gate) | Resolved | `[ok] arm srpcmp` in the local positive gate |
| R582-3-F1 = R583-3-F1 (cone past the first hop) | Resolved | netlist cone through every cell; selftest arms |
| R582-3-F2, R582-3-F3, R583-3-S1 | Resolved | B13; adoption and failed-creation tests; plants in the hosted campaign |
| R582-4-F1 = R583-4-F1, R583-4-F2 | Resolved | refused by dataflow or by sv2v/Yosys; selftest arms, local and hosted |
| R582-4-S1 (`srpcmp` names) | Resolved | arm passes with its named controls and plants |
| R582-5-F1 = R583-5-F1 (one shape) | Resolved | six builder shapes; S1/S2/S3, arms B and E refused; this round's four further shape probes refused |
| R583-5-F2 (unplanted rules) | Resolved | 31 rules, `mutations: 0 of 31 rule(s) no arm proves`, local and hosted |
| R582-5-F2 = R583-5-F3 (budget) | Resolved | own job; hosted 14 min 08 s of 45 min (31 %) at this head; recording it in the PR body is the manager's (ruling item 3) |
| R582-5-S1 (pins) | Resolved | two pin arms refused naming both versions |
| R583-5-R1 (RESIDUE) | Applied with its exact text | round 7 moved the job again, see R583-6-R1 |

## 5. Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | rulings 6088423771 to 6100024293; block RTL and contract; census code; writers; hosted `publication-census` 114284711008 | R583-6 | `67c1285b3b28b12a3af4f3f3aae6e92befd5febb` |
| RTL | CLEAN | `KL_mbx.sv`, `KL_mbx_pkg.sv`, generator checks; mbx bench and 6 quick plants (pinned Verilator 5.050); `milan_csr` read-back cone; hosted Yosys shards and lint | R583-6 | `67c1285b3b28b12a3af4f3f3aae6e92befd5febb` |
| Robustness | CLEAN | bench P1-P5; four new shape probes and the limit control; failure and boundary writer plants | R583-6 | `67c1285b3b28b12a3af4f3f3aae6e92befd5febb` |
| Tests | CLEAN (S1 suggestion) | census self-test and rule mutations; five independent firmware plants; positive firmware gate; hosted `firmware-unit` 114284710904 | R583-6 | `67c1285b3b28b12a3af4f3f3aae6e92befd5febb` |
| Docs | CLEAN (R1, R2 residue) | `MAILBOX_SPLIT.md`, `ARCHITECTURE_HW_SW_SPLIT.md`, `CI_WORKFLOWS.md`, mbx README and Makefile, docstrings, PR body; docs gates | R583-6 | `67c1285b3b28b12a3af4f3f3aae6e92befd5febb` |

## 6. Executed evidence (this round, exact head, scratch copies only)

- Census `python3 -B sw/mailbox/publication_census.py --check --selftest --jobs 5`, pinned sv2v v0.0.12
  (release zip sha256 checked against `rtl-fast.yml`), Yosys 0.66: rc 0; `6 shape(s), checks: 234 failures: 0`;
  25 nets, 4 unread, 39 reads of 21 nets in each shape; `--check` 158 s; `selftest: 0 of 120 arm(s) failed`
  (563 s); `mutations: 0 of 31`; 12 min 03 s wall, 1.21 GB peak RSS per process; host load average 100 to 230.
- Census probes (`scripts/probe_r583_6.py`, through `--check --datapath`): 4 of 4 refused in the shapes that
  build them, the unbuilt control accepted.
- `scripts/csr_readback_cone.py`: 0 of 8 read-back inputs reach any `milan_csr` output but `s_axi_rdata`.
- `scripts/config_coupling_r583_6.py`: S1.
- `make -C tb/verilator/mbx -j4` (pinned Verilator 5.050): rc 0, 402/447/32/404/449/389, 0 failures, 6 of 6 plants.
- `test_ctrl_firmware.py --require-rv32 --jobs 2` (pinned RV32 SDK installed offline from its digest-checked
  archive, lwSRP at its pin): rc 0, 60 arms, `srpcmp` ok. `scripts/fw_plants_r583_6.py`: 5 of 5 caught.
- `gen_mailbox.py --check`, `--crosscheck`, `--selftest`, and the docs and lint gates in section 3: rc 0.
- Hosted at this head (inspected, not owned): `publication-census`, `firmware-unit`, `elaborate` (gate 23m:
  5 elaborations, 3/3 cuts), `yosys-elaboration`, Yosys shards 0-3, `verilator-lint`, `rtl-fast` success;
  Verilator shards 1/5 and 4/5 were still in progress when sampled; `Physical gPTP` skipped (not hardware proof).
- The review clone is byte-exact at the head (`receipts/clone_integrity.txt`): index tree `dd07654c`, worktree
  equal to HEAD, no untracked file, every gitlink unchanged. Nothing was written into it.

## 7. Real limits

- Local runs used the distribution build of Yosys 0.66 (`86f2ddebc-dirty`), not CI's from-tag build; the counts
  equal the hosted job's exactly.
- The firmware plant campaigns (506 + 76 + SRP) and the coverage ratchet were not rerun locally: the first local
  self-test attempt was refused by a pre-existing image arm that reads the `third_party/lwSRP` submodule path
  directly (empty in this clone); the hosted `firmware-unit` job at this head is the evidence. Host GoogleTest
  1.18 and GCC 16 were used for the local positive gate.
- Gate 23m (no LiteX interpreter here), the Vivado front end, the all-fabric export, the image sizes, the
  mailbox area and the full 175-plant `mutants.py` were not run; their inputs are unchanged since round 4b, and
  gate 23m ran hosted at this head.
- The CSR cone probe elaborates `milan_csr` at its default parameters only.
- No hardware, no calibration (NOT RUN), no field result; skipped hosted contexts are not hardware proof.
- No manager source bank ran at this head, and none is claimed or inferred.

## 8. Pending manager duties

- Record the hosted `publication-census` figures at this head in the PR body (ruling 6100024293 item 3): run
  38076540233, job 114284711008, 18:42:48 to 18:56:56Z, 14 min 08 s of 45 min (31 %), census step 13 min 54 s,
  warm Yosys cache (build step skipped), `--jobs 4`. Cold-cache estimate with the stated uncached build
  (12 min 28 s to 18 min 47 s): about 26 min 36 s to 32 min 55 s (59 % to 73 %), inside the timeout.
- Confirm the public reading of "cone end that differs between shapes" (classes of end); this reviewer accepts it.
- Accept the remaining hosted contexts (Verilator shards 1/5 and 4/5 were in progress) and the act replica.
- Validate the current-dev merge candidate at the merge turn (live dev `f88df731`), builder and native banks.
- Carry R583-6-R1 and R583-6-R2 to the residue checklist; decide whether to take S1 and S2.
- Obtain the internal review's verdict for this head.

R583-6 FINISHED
