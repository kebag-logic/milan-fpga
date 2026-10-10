[R582] NEGATIVE - exact head b2aa3ccfe31652ad34d93e3ea446f31b58dc9c1c

# R582-2: internal independent review of PR #704 (issue #665, lane F-INT PR 1 of 2)

Round R582-2. Exact head `b2aa3ccfe31652ad34d93e3ea446f31b58dc9c1c`, tree `bbe108c257c71be2553d713e035a0648e8808aa3`,
base `7c1b52bee26b497080ee22b1c1986109f80a5ee7` (an ancestor of the head; 21 commits, 49 files). This is a
cleared-context review: I rebuilt the scope from public state only, then made my own pass over the diff before
reading the earlier public findings.

**Summary.** The publication block, its generator, its RTL, the host-model twin and the four writers are correct
at this head. The writers are ACMP (bound, started, stream_id), MAAP (DA gate) and SRP (licence, Talker
declarations, idle slope, Domain). Every gate I re-ran passes:

- 402 / 447 / 32 / 404 / 449 / 389 mailbox checks;
- 175 of 175 RTL plants;
- 505 of 505 firmware plants, 0 escaped;
- the coverage ratchet at 22 files;
- the census at 39 of 39 reads.

An independent grep of `milan_datapath.sv` confirms that at this head the census is complete.

All five earlier findings (R582-1-F1 to F3 and R583-1-F1 to F3, where R582-1-F2 = R583-1-F1) are resolved.

One MINOR finding remains. Ruling 6092086337 item 3 requires the census to be a standing check that fails on an
unmapped read, and it does not always do so. Two reviewer plants of real, unmapped class-D reads pass it:

- a processor class-D output wired under a name without the `pp_cd_` prefix and read on the wire;
- a class-D wire used as a `case` item label.

So the verdict is NEGATIVE. One RESIDUE (comment wording) and one SUGGESTION are also recorded.

## Scope reconstructed (public sources)

- **Assignment** 6087047553, narrowed by **ruling 6088423771**: F-INT is split into two PRs, and this is PR 1. It
  covers:
  - a publication block inside the mailbox window, with its map and docs;
  - the firmware writers in the F2 to F4 adapters, each placed before its promising response;
  - GoogleTest at the 100 % ratchet, with three plants per writer: moved, wrong field and skipped;
  - an RTL simulation of the block with plants;
  - an all-fabric image that stays byte-identical;
  - the firmware size against 224 KB;
  - the mailbox area as a measurement only.

  VERSION stays unchanged. The GET_STREAM_INFO face needs no publication.
- **Ruling 6092086337 (round 3)** sets six items:
  1. Publish the started level.
  2. Publish the Talker-declared level.
  3. Add a census as a standing check: every wire-affecting read of a processor class-D output in
     `milan_datapath.sv` maps to a field or a ruled exclusion, the check fails on an unmapped read, and a planted
     unmapped read is caught.
  4. `DA_GATE` stays DA validity, recorded as a choice with its egress consequence.
  5. Add a two-interface DA-gate test, and the plant `rv-maap-gate-on-interface-0`.
  6. Use `idle_slope_bps` in both harness views.
- **Rulings 6087214078, 6087462816 and 6087654804** set the comparison contract for PR 2. The comparator commits
  stay as infrastructure.
- **Authorities** read:
  - `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 1 (a value is written before the response that promises it);
  - `docs/design/MAILBOX_SPLIT.md`, "The publication block", Verification and Measured area;
  - `sw/mailbox/mailbox.yaml`;
  - `CONTRIBUTING.md` section 3;
  - `AGENTS.md` sections 6 and 7.

## Findings

### R582-2-F1 - MINOR - Conformance, Tests, Docs - `sw/mailbox/publication_census.py:80`, `:466`, `:400-403` - the standing census misses two forms of unmapped class-D read

- **Authority:** Ruling 6092086337 item 3 says: "Every wire-affecting read of a processor class-D output in
  `milan_datapath.sv` must map to a block field or a named, ruled exclusion, and the check fails on an unmapped
  read." The PR's documentation states the same property in three places:
  - `docs/design/MAILBOX_SPLIT.md:848`: "A read the census does not name fails the suite";
  - `docs/ARCHITECTURE_HW_SW_SPLIT.md:90`;
  - `tb/verilator/mbx/README.md:9`.
- **Evidence:** The reviewer probe `scripts/census_probes.py` (receipt `receipts/census_probes.log`) runs the census
  on scratch copies of the head's datapath. The control is clean, and three plants are refused as expected. Two
  plants are accepted with `RESULT: PASS`:
  1. **A processor class-D output wired under a non-`pp_cd_` name and read on the wire.** The plant changes
     `.srp_domain_change_o (pp_cd_srp_domain_change_w)` (`milan_datapath.sv:8273`) to `(probe_dom_chg_w)` and reads
     it into `crft_class_a_w`, the CRF talker's C-TAG enable. The census only counts names matching
     `POPULATION = re.compile(r"\bpp_cd_\w+_w\b")` (`:80`, applied at `:466`). It never checks that the wrapper's
     class-D ports (`milan_datapath.sv:8270-8293`) connect to names in that population. Its "stale row" rule cannot
     catch this either, because the output had no read before.
  2. **A class-D wire used as a `case` item label inside an always block.** An example is
     `case (1'b1) pp_cd_srp_over_limit_w: ...`. `netlist()` scans only the parentheses of `if`, `case` and `for` in
     a statement's leading part (`:400-403`). A label between the `case (...)` and the `:` is never read.

  By contrast, an alias wire, a `case` selector and a function body are all refused.
- **At this head:** no read is unmapped. My grep of every `pp_cd_*_w` and `pp_aecp_strm_started_w` occurrence finds
  the same 39 reads as the census (receipt `receipts/census_list.txt`), and all 21 wrapper class-D ports connect to
  `pp_cd_*` names. The gap is in the standing guarantee.
- **Impact:**
  - A later change can add a wire-affecting class-D read that the census passes. Likely sources are the PR 2
    rewiring around this same instance, or a processor pin that adds an output.
  - The block would then be incomplete again, which is the defect the ruling made this check to prevent. Ruling
    6092086337 notes that the first list missed two values.
  - The three documentation sentences above claim more than the check does.
- **Required outcome:**
  - The census derives or checks its population from the processor wrapper's instance. Every class-D output port
    of `KL_pp_shadow` either connects to a population name or is refused by name. Or an equivalent rule makes the
    population independent of a naming convention.
  - A `case` item label is counted as a read.
  - Each of these forms has a self-test plant that is refused.
  - The documentation claim stays true, or is narrowed to what the check proves.
- **Verification:** Re-run `scripts/census_probes.py <checkout> <scratch>`. The expected result is `unexpected: 0`.
  The census `--selftest` should show the two new arms refused, and `--check` should still show 39 of 39 at the
  candidate head.

### R582-2-R1 - RESIDUE - Docs - `sw/firmware/ctrl/host/mbx_model.h:163-164`, `sw/firmware/ctrl/host/mbx_model.c:27` - the model's comments say the ports carry the stream_id only while SID_VALID is set

- `KL_mbx` drives `pub_sid_o` unconditionally (`hdl/milan/mailbox/KL_mbx.sv:318`). Gating is the reader's rule, as
  the port comment at `KL_mbx.sv:72` and the bench's `Bench::pub` say ("the stream_id the datapath takes").
- `mbx_model.h:163` says the view is "as KL_mbx's pub_*_o ports carry it: ... each sink's stream_id only while its
  SID_VALID is set". `mbx_model.c:27` says "the stream_id driven only while SID_VALID".
- The model's view applies the datapath's take rule correctly. Only the wording is wrong: no code, test, figure or
  claim depends on it.
- **Exact fix:**
  - `mbx_model.h:163-164`: "What interface `interface`'s datapath takes from KL_mbx's pub_*_o ports: every field,
    and each sink's stream_id only while its SID_VALID is set."
  - `mbx_model.c:27`: "the stream_id taken only while SID_VALID".

### R582-2-S1 - SUGGESTION - Robustness - `sw/firmware/ctrl/maap/maap_mbx.c:62` with `sw/mailbox/mailbox_model.py:412`

- I carry R583-1's S2 forward unchanged. The contract accepts up to 32 publication sources, and
  `maap_mbx_init` accepts `count == MBX_N_PUB_SOURCES`. At 32, `(1u << count) - 1u` is undefined behaviour.
- At this contract's 16 sources it is well defined.
- A 64-bit mask, or a contract bound of 31, would remove the case. This item does not affect coverage.

## Prior public findings at this head

| Finding | Status at this head | Evidence |
|---|---|---|
| R582-1-F1 (MAJOR): the started level | **Resolved** | See note (a) |
| R582-1-F2 = R583-1-F1: the Talker declarations | **Resolved** | See note (b) |
| R582-1-F3: `DA_GATE` claimed `acmp_declaring_o` | **Resolved as ruled** (item 4) | See note (c) |
| R583-1-F2: the DA gate's interface | **Resolved** | See note (d) |
| R583-1-F3: the idle slope's unit | **Resolved** | See note (e) |
| R583-1 S1 to S3 (suggestions) | S2 retained as R582-2-S1; S1 and S3 do not affect coverage | See note (f) |

Notes:

- **(a) The started level.**
  - `BINDING.STARTED` (bit 2) is driven on `pub_started_o` (`KL_mbx.sv:317`).
  - The census row (`pp_aecp_strm_started_w`, `acmpl_stopped_v_w`) maps it.
  - The writer is `publish()` (`acmp.c:198`): before `p_send` in `transmit()`, and at the start of `finish()`.
  - `acmp_set_started` runs `finish()` before it returns.
  - Tests: `B12` and `A31`, plus RTL P2/P3. Plants caught in my run: `pub-acmp-started-after-the-response`,
    `-after-the-report`, `-from-bound`, `-move-skipped`, `top-pub-started-*` (both adapters), and
    `model-pub-started-not-stored`.
- **(b) The Talker declarations.**
  - `TALKER_DECL.DECLARED` is driven on `pub_talker_decl_o`.
  - The census maps the row (`pp_cd_srp_tk_decl_state_w`, `crft_class_a_w`).
  - `declare_sources` publishes once every source has joined. `withdraw_declared` runs before
    `msrp_app_destroy` at reset (`srp_mbx.c:743`) and at destroy (`:355`).
  - `PubTalkerDeclPrecedesTheDeclarationsAndIsWithdrawnFirst` covers it. All seven `pub-declared-*` plants were
    caught.
- **(c) `DA_GATE`.**
  - `mailbox.yaml` (generated text at `KL_mbx_pkg.sv:303`) now says "address validity only" and names the missing
    4.3.3.1 predicate.
  - `MAILBOX_SPLIT.md:882-893` names the egress consequence: with policing off, the split talkers stream once MAAP
    holds the address. It also names lane F3b.
  - The census row's reason cites the choice.
- **(d) The DA gate's interface.**
  - Tests: `DaGateOpensOnTheAcquiringInterfaceAloneBeforeItsReport` and
    `DaGateOfEveryInterfaceOpensBeforeItsOwnReport` (`test_maap_mbx.cpp:152`, `:168`).
  - `rv-maap-gate-on-interface-0` was caught in my run: `maap_if2`, 10 checks failed.
- **(e) The idle slope's unit.** The field is `idle_slope_bps` at `mbx_model.h:168` and `frames.hpp:31`, and the RTL
  port is `pub_idle_slope_bps_o`.
- **(f) R583-1's suggestions.**
  - S1 (a direct unbind-from-PRB_W_RESP case) would add a test, and the existing plants already kill that path.
  - S3 (a core-only restart): `KL_mbx` resets with `ResetSignal("sys")`, the CPU's domain
    (`milan_soc.py:2544`, `:2551`). It is recorded under Limits for PR 2.

## Lens coverage (artifact-specific, at the exact head)

Format: `[R582] <result> <lens> - <artifact> - <what was checked and against what>`.

[R582] MINOR Conformance - `publication_census.py:80`, `:400-403`, `:466` - R582-2-F1: the item-3 standing-check
property ("the check fails on an unmapped read") does not hold for two read forms. Everything else under this lens
was checked and is clean:

- `mailbox.yaml:307-413` against rulings 6088423771 (decision 2 (a), PR 1) and 6092086337 items 1, 2, 4, 5 and 6.
- The writer order against `ARCHITECTURE_HW_SW_SPLIT.md` section 1:
  - `acmp.c` `transmit` and `finish`, `bind` and `unbind` (where `srp_stop` clears the stream before the response);
  - `maap_mbx.c:62` before `m->allocation`;
  - `srp_mbx.c` `create_participants`, `declare_sources`, `change_domain`, `reset_interface` (`:736`, `:743`),
    `srp_mbx_destroy` (`:349`, `:355`), and both licence sites in `poll` (`:822`, `:831`).
- The census's 39 rows against my own grep of `milan_datapath.sv` (identical).
- The status cones `acmpl_vlan_w` and `lwsrp_*` reach CSR only (`milan_datapath.sv:2557-2625`).
- VERSION is unchanged, and no register outside the mailbox block changes.
- The parent `KL_maap`'s address reaches the datapath in the split build through the existing CSR route
  (`MAILBOX_SPLIT.md:436`). It is outside the processor class-D population as ruled.

[R582] PASS RTL - `hdl/milan/mailbox/KL_mbx.sv:150-176`, `:261-321`, `:351-358`, `KL_mbx_pkg.sv:296-370` - checked
against the contract's map and `CONTRIBUTING.md` section 1:

- Decode: power-of-two strides, the interface bound tested before truncation into `pub_if_w`, the entry bound
  `< 16`, the holes and the fourth word.
- Writes: `wr_w` requires `host_be_i == 4'hF`, every register has a synchronous reset, and the field masks match.
- Read-back: every read is guarded by `pub_at_w`.
- Outputs: per-interface and per-sink slices.
- Widths: SR_DOMAIN is a 25-bit register with 16 field bits. The measured +1,168 FF equals the field storage
  (105 - 9 + 16 x 67), and +483 LUT matches the table's totals (`MAILBOX_SPLIT.md:1106-1115`).
- `milan_soc.py:2559-2571` binds all eleven ports at contract widths.
- The lint ratchet passes (90 <= 90).

[R582] PASS Robustness - `KL_mbx.sv` decode and reset; `mbx.c:137-233` refusals; `maap_mbx.c:62`, `:70`;
`srp_mbx.c:61-83`, `:342-357`, `:726-746`, `:818-833`; `acmp.c:188-211`, `:513-530` - checked against the contract,
the RTL suite P4/P5 and my own probes:

- Partial strobes are refused and counted, holes and absent interfaces read 0, and a reset during activity clears
  the block (P5, at one and two interfaces).
- A sink or interface beyond the contract, and more than 16 sources, are refused.
- At a link loss, a reset or destroy, LICENCE closes before the revocations are reported.
- A re-entrant call from the publish port is refused (plant `pub-acmp-port-unguarded` caught).
- My two probes on the owed-stop licence site (skipped, and moved after the report) are both caught by
  `Srp.PubLicenceIsSetAndClearedBeforeEachChangeIsReported` (`receipts/srp_probe.log`). The control is 57/57.
- The 32-source shift is SUGGESTION S1 only.

[R582] MINOR Tests - `publication_census.py` self-test (`:515-578`) - R582-2-F1: the self-test has no arm for the
two read forms that escape. Everything else under this lens was checked and is clean:

- The mailbox suite gives 402 / 447 / 32 / 404 / 449 / 389 checks with 0 failures, and 6 of 6 quick plants.
- `mutants.py` catches 175 of 175, including all 28 `top-pub-*` arms, after four positive controls.
- `test_ctrl_firmware.py --require-rv32 --self-test` passes in both slices: 253 + 252 = 505 of 505 caught,
  0 escaped. That includes 23 `pub-*` SRP plants, each caught twice, and every `pub-acmp-*`, `pub-maap-*`,
  driver and model plant.
- `fw_coverage.py --check` passes at 22 files. `acmp.c`, `acmp_mbx.c`, `maap_mbx.c`, `mbx.c` and `srp_mbx.c` are
  at 100 % of lines and branches.
- Each writer test reads the block at the response's `TX_HEAD` commit, not at the end of the entry
  (`test_acmp_mbx.cpp` B10 and B12, `srp_mbx.cpp` `commit_trace`).

[R582] MINOR Docs - `docs/design/MAILBOX_SPLIT.md:848`, `docs/ARCHITECTURE_HW_SW_SPLIT.md:90`,
`tb/verilator/mbx/README.md:9` - R582-2-F1: these lines claim that any unmapped read fails the suite. Everything
else under this lens was checked and is clean:

- The publication section (`:802-914`) matches the code. That includes the bound figures 77, 50, 32, 14 and 49,
  `SRP_MBX_PUB_POLL_MAX` = 40, and the measured-area arithmetic.
- The generated `MAILBOX_CONTRACT.md` passes `gen_mailbox.py --check`, `--crosscheck` and `--selftest` (0
  findings).
- The ctrl, maap, srp and mbx READMEs agree with the code.
- The PR body's figures match my runs (census, mailbox, mutants, firmware plants, coverage).
- `docs_check.py`, `check_em_dash.py --base 7c1b52be`, `check_py_idiom.py`, `gen_module_matrix.py --check`,
  `measure_naming.py --check` and `git diff --check` all pass.
- R582-2-R1 is wording only.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R582-2-F1, MINOR) | rulings 6088423771 and 6092086337; `mailbox.yaml:307-413`; writer order in `acmp.c`, `maap_mbx.c`, `srp_mbx.c`; the census against `milan_datapath.sv` (independent grep) | R582-2 | b2aa3ccfe31652ad34d93e3ea446f31b58dc9c1c |
| RTL | CLEAN | `KL_mbx.sv:150-176`, `:261-321`, `:351-358`; `KL_mbx_pkg.sv:296-370`; `tb_mbx_top.sv`; `milan_soc.py:2534-2571`; lint ratchet; area arithmetic | R582-2 | b2aa3ccfe31652ad34d93e3ea446f31b58dc9c1c |
| Robustness | CLEAN | RTL P4/P5; driver refusals; MAAP init bound; SRP reset, destroy and owed-stop paths (reviewer probes caught); ACMP port guard | R582-2 | b2aa3ccfe31652ad34d93e3ea446f31b58dc9c1c |
| Tests | UNCLEAN (R582-2-F1, MINOR) | `suite.hpp` P0-P5; `mutants.py` 175/175; `ctrl_mutants.py` and `srp_pub_mutants.py` 505/505; coverage at 22 files; census self-test plus reviewer probes | R582-2 | b2aa3ccfe31652ad34d93e3ea446f31b58dc9c1c |
| Docs | UNCLEAN (R582-2-F1, MINOR; R582-2-R1 is RESIDUE) | `MAILBOX_SPLIT.md:802-1127`; `ARCHITECTURE_HW_SW_SPLIT.md:88-93`, `:188`; generated contract; four READMEs; PR body; docs gates | R582-2 | b2aa3ccfe31652ad34d93e3ea446f31b58dc9c1c |

## Executed evidence (source head, reviewer clone and scratch mirror)

The receipts are listed in `MANIFEST.sha256`, and tool identities are in `receipts/environment.txt`:

- Verilator 5.050.
- The pinned RV32 SDK: the archive's sha256 equals the pin in `scripts/ci_rv32_sdk.py`, and I extracted it into
  scratch.
- GoogleTest 1.18.0.

| Command | Result |
|---|---|
| `gen_mailbox.py --check`, `--crosscheck`, `--selftest` | rc 0, 0 findings, 0 arms failed |
| `publication_census.py --check --selftest` | rc 0; 39 checks, 0 failures; selftest 0 of 10 arms failed |
| `scripts/census_probes.py` (reviewer) | 6 probes, 2 unexpected acceptances (R582-2-F1) |
| `make -C tb/verilator/mbx census run-wb run-axil run-cosim run-if2 mutants-quick` | rc 0; 402, 447, 32, 404, 449, 389, each with 0 failures; 6 of 6 |
| `tb/verilator/mbx/mutants.py --jobs 6` | rc 0; 4 controls; 175 of 175 caught |
| `test_ctrl_firmware.py --require-rv32 --self-test --jobs 2 --slice 1/2` and `2/2` | rc 0 for both; PASS; 253 + 252 of 505 caught; 0 ESCAPED |
| `fw_coverage.py --check --jobs 3 --lwsrp third_party/lwSRP` | rc 0; PASS (22 files) |
| `scripts/srp_probe.py` (reviewer) | control 57/57; both planted owed-stop defects caught by the named test |
| `docs_check.py`, `check_em_dash.py --base`, `check_py_idiom.py`, `gen_module_matrix.py --check`, `measure_naming.py --check`, `lint_rtl.py --check --self-test`, `git diff --check` | all rc 0 |

After the probes the clone was verified at the exact head:

- `HEAD` and tree match the head under review.
- The index matches `HEAD`, and the worktree matches the index.
- All 1,236 tracked blobs rehash to their index ids, and the modes are unchanged.
- No flag other than `H` is set in `git ls-files -v`.
- There are no untracked or ignored files. I removed a `__pycache__` I had created.
- All five gitlinks are at their recorded commits. I initialised `third_party/lwSRP` at its gitlink for the
  firmware gates.

The hosted check snapshot at this head is `receipts/hosted_checks.txt`, taken while the runs were in progress:

- 10 completed successfully, among them the four Yosys shards and verilator-lint.
- 9 were still in progress: the Verilator shards, firmware-unit, elaborate, docs-check and yosys-elaboration.
- 1 was skipped: physical gPTP, nightly and manual only.

The manager owns the hosted and act acceptance.

## Real limits

- **Not run:**
  - `xvlog_gate.py`: no Vivado front-end beside this review.
  - The full Yosys, builder, parent, PP and gPTP banks: not allowed.
  - `test_ctrl_nvm.py`: `ctrl_nvm` is unchanged by this diff.
  - The LiteX shipping-config export.
  - `act` and `act_ci`.
  - The out-of-context Vivado area.
- **All-fabric default.** I accepted it by inspection only:
  - `milan_datapath.sv` and the processor are untouched by the diff.
  - The change to `milan_soc.py` sits inside `CtrlMailbox`, which is built only under `--ctrl-mailbox`
    (`milan_soc.py:3345-3346`).
  - The author's export-level comparison is not reproduced here.
- **Area and size figures.** I checked these against their own tables, not re-measured.
- **The census.** It reads the datapath as text. My probes cover six forms, not every SystemVerilog construct.
- **Core-only restart.** The firmware publishes only moved values, so it assumes the block holds its reset values
  when the firmware starts. That holds while the mailbox resets with the CPU (`milan_soc.py:2544`, `:2551`). PR 2
  should keep it true or write the block at open.
- **Hardware.** Physical calibration was NOT RUN. Field and hardware behaviour is not proven, and skipped field
  contexts are not hardware proof.
- **Markdown renderer.** The em-dash gate ran with pycparser 3.1, where the pin is 3.0. The other renderer packages
  match the pin.

## Pending manager duties

- Route R582-2-F1 to the executor, then re-review the corrected head under Conformance, Tests and Docs.
- Carry R582-2-R1 to the residue checklist.
- At the merge turn:
  - validate the current-dev merge candidate (builder and native banks; live dev `554e61d2`);
  - accept the hosted exact-head contexts, which were still running when sampled;
  - obtain the external review's verdict.
- No manager source bank ran at this head, and none is claimed or inferred here.

R582-2 FINISHED
