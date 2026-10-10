[R582] NEGATIVE - exact head 25bbe4d956e79de979783d7e4706a5581c0742a7

# R582-1: internal independent review of PR #704 (issue #665, lane F-INT PR 1 of 2)

Head `25bbe4d956e79de979783d7e4706a5581c0742a7`, tree `d4cc09d512434ae646a3fca511876a44c195522b`,
base `7c1b52bee26b497080ee22b1c1986109f80a5ee7`. Scope: ruling
[#665 6088423771](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6088423771)
(decision 2 (a) and "PR 1"); comparator commits `780a199c` and `79efa393` read as
infrastructure for PR 2 under rulings 6087214078, 6087462816 and 6087654804.
I reconstructed the task from AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue
body and its rulings, ARCHITECTURE_HW_SW_SPLIT.md, MAILBOX_SPLIT.md, the diff and history,
the published evidence tree `e1dd23a1:review-evidence/665int-r1`, and my own runs.
There are no prior review findings on this PR to resolve: the only PR comments at this head are the
two review-start notices.

**Verdict: NEGATIVE.** The block, its RTL, its writers and its tests are sound,
and every gate I ran passes, including all 167, 492 and 186 plants. One MAJOR and two MINOR findings
remain open, all under Conformance and Docs. The block does not carry the listener
started level, which the ruling's "listener accept" needs. It does not carry the CRF
source's Talker-declaration level, which the datapath consumes. And `DA_GATE` is
documented as the processor's `acmp_declaring_o` but publishes a weaker predicate.
The publication block has no consumer before PR 2, so none of these changes the
shipped image. Each one is a gap or an incorrect statement in the contract that PR 2 is
supposed to build on.

## Findings

### R582-1-F1 - MAJOR - Conformance, Docs - the block omits each sink's started level, part of the listener accept the ruling names

- **Where:** `sw/mailbox/mailbox.yaml:376` (`BINDING`: `BOUND` and `SID_VALID` only);
  `docs/design/MAILBOX_SPLIT.md:807` and `:820`; `docs/ARCHITECTURE_HW_SW_SPLIT.md:88`.
- **Authority and evidence:**
  - Ruling 6088423771, decision 2 (a), says firmware writes every class-D value the split
    datapath consumes, including "listener accept and bound stream_id".
  - The datapath's listener accept is not `BOUND` alone. `hdl/milan/milan_datapath.sv:5375`
    defines `acmpl_stopped_v_w = acmpl_bound_v_w & ~pp_aecp_strm_started_w`. Then `:6270`
    sets `avtprx_accept_p = avtprx_accept_p_w && !avtprx_stopped_w`, and `:5886` drives
    `KL_crf_rx.stop_i` from the CRF sink's bit.
  - `hdl/milan/KL_pp_shadow.sv:612-620` calls that level LOAD-BEARING for the listener
    accept pulse. It also says the ACMP binding record owns it: "the AECP commands MOVE the
    bit, the record OWNS it".
  - In the split placement that owner is the firmware ACMP core. `sw/firmware/ctrl/acmp/acmp.h:278`
    holds `started` (Milan v1.2 5.3.8.7). `acmp.c:816` and `:832` set it from STREAMING_WAIT in
    the BIND_RX entry, whose response echoes the flag, and `acmp_set_started` (`acmp.h:450`)
    moves it.
  - Nothing in the block publishes it. The design page maps "listener bound" to `acmp_bound_o`
    only, and both pages describe the block as carrying the values the datapath consumes.
- **Impact:** PR 2's static selection has no published source for the started level. A
  sink bound with STREAMING_WAIT, or stopped later, would have its AVTPDUs accepted,
  which Milan v1.2 5.3.8.7 says must be discarded. Avoiding that needs another contract
  change after this one. The documents state a completeness the block does not have.
- **Required outcome:** One of these two:
  - The block carries each sink's started level, written by the ACMP owner before the
    BIND_RX response that promises it and before any later move is reported. It needs the
    same RTL checks, model twin, writer ordering test and moved, wrong-field and skipped
    plants as the other values.
  - Or the issue records a manager decision placing this value in another lane.

  Either way, the completeness statements must match what the block carries.
- **Verification:** A register field and its output in `KL_mbx`, P-checks with plants
  through both adapters, an ACMP ordering test with its three plants, and a regenerated
  contract (`gen_mailbox.py --check`). Alternatively, the decision comment and corrected text.

### R582-1-F2 - MINOR - Conformance, Docs - the CRF source's Talker-declaration level is consumed by the datapath and not published

- **Where:** `sw/mailbox/mailbox.yaml:315` (the block's register set);
  `docs/design/MAILBOX_SPLIT.md:807`.
- **Authority and evidence:**
  - The same ruling says "every class-D value the datapath consumes".
  - `hdl/milan/milan_datapath.sv:5677-5678` derives `crft_class_a_w` from the processor's
    `srp_tk_decl_state_o` for the CRF source. `:6225` feeds it to the CRF framer's `vlan_en_i`,
    the interlock that tags CRF frames only while their Talker declaration is on the wire
    (802.1Q 35.1.2, as the comment at `:5663-5670` explains).
  - That is an SRP-owned value, and in the split build F4 owns it. The block publishes
    `LICENCE`, `IDLE_SLOPE` and `SR_DOMAIN`, none of which is this level. `LICENCE` also
    needs a registered Listener, so it is a different predicate.
  - The executor's own enumeration in STOP 6088406545 (cited lines `:7265-7307`) did not
    include `:5677`, and the ruling copied that list.
- **Impact:** The split CRF talker would have no source for its tagging interlock. PR 2
  would have to choose a substitute or change the contract again.
- **Required outcome:** Publish the CRF source's declaration level (or a per-source
  declared level), written by the SRP owner before the declarations it describes. Or
  record a manager decision that names its split-build source. Then correct the
  completeness text.
- **Verification:** As for F1, or the decision comment.

### R582-1-F3 - MINOR - Conformance, Docs - `DA_GATE` is documented as `acmp_declaring_o` but publishes a weaker predicate

- **Where:** `sw/mailbox/mailbox.yaml:321-330` (generated into `KL_mbx_pkg.sv`,
  `mbx_contract.h` and `MAILBOX_CONTRACT.md`); `docs/design/MAILBOX_SPLIT.md:819`;
  `sw/firmware/ctrl/maap/maap_mbx.c:62`.
- **Authority and evidence:**
  - The contract text says `DA_GATE` bit s is "the processor's acmp_declaring_o".
  - The processor's level is `gstate == GS_DECLARING` (`protocol-processor/hdl/acmp/KL_acmp_talker.sv:359`).
    It is entered only when the DA is valid and not in conflict, and the source was probed
    within T-SRP-DAFRESH (15 s) or has a registered Listener (`:691`, `:740-750`, `fresh_f`
    at `:396`; processor `docs/architecture/05_acmp_engine.md:405`, citing Milan 4.3.3.1).
  - The firmware writes `(1 << count) - 1` while the MAAP range is valid. That is DA validity
    only, for every source.
  - The datapath's AAF gate with SRP gating off (`milan_datapath.sv:2008-2011`) is
    `acmp_talker_active` alone, which is this level. So the two placements gate egress
    differently.
  - The PR's "choices made public" record the stream_id and `LICENCE` differences, but
    not this one.
- **Impact:**
  - The contract's statement of equivalence is wrong.
  - PR 2's two-placement comparison will meet an unrecorded difference in the talker
    egress gate. Ruling 6087214078 treats an unrecorded difference as a STOP.
- **Required outcome:** One of these two:
  - The published level matches the processor's predicate.
  - Or the difference is recorded as a public choice with its consequence for the egress
    gate, and the contract text no longer claims equivalence.

  Either is fine, but the outcome needs to be accepted on the issue.
- **Verification:** The regenerated contract text and the design page's choices list, or
  a writer test that holds the gate closed without a probe or Listener and its plant.

No RESIDUE and no SUGGESTION items are recorded. A firmware that requires `ID.MINOR >= 2` before relying on
the block, and a core-only restart leaving stale publication state, were both considered and
dismissed. The firmware writes only where 2.1 has holes, and the SoC resets the mailbox with
the CPU (`milan_soc.py:2544`, `ResetSignal("sys")`).

## Evidence by focus item

**Publication block RTL** (`hdl/milan/mailbox/KL_mbx.sv:62-70` ports, `:157-174` decode,
`:260-313` storage, write and outputs, `:343-349` read-back inside `reg_read`):

- **Generation.** The register map change stays inside the mailbox window, and
  `KL_mbx.sv` changes only through the generator.
- **Generator gates.** `gen_mailbox.py --check` and `--crosscheck` report 0 findings, and
  `--selftest` reports 0 arms failed. The self-test includes the new overlap, stride and
  field arms. The storage at `:260` is declared before the read-back that reads it at `:343`.
- **Decode and reset.** Every register resets to 0 (synchronous active-low reset, as in
  the rest of the module). The interface index is bounded at full width before truncation,
  and the sink index is bounded before it is used. A hole, an entry's fourth word or an
  absent interface takes no write, reads 0 and is not counted. A partial strobe goes
  through the existing `refused_w` path into `BUS_ERR`.
- **Layout.** The block sits at 0x800 to 0xA00 (0xC00 at two interfaces), clear of the
  event ring (0x400 to 0x500) and the first channel ring (0x1000).
- **Clocking.** Same clock as the module, no clock-domain crossing introduced.
- **Bench and plants.** Pinned Verilator 5.050 (identity printed):
  - checks: 401 Wishbone, 446 AXI4-Lite, 32 co-simulation, then 403, 448 and 388 at two
    interfaces, all with 0 failures;
  - quick plants: 6 of 6;
  - `mutants.py --jobs 6`: 167 of 167 caught, including the 20 publication arms through
    both adapters (`receipts/mbx_make.log`, `receipts/mbx_mutants.log`).
- **Synthesis and lint.** `syn/yosys/run.sh` on `KL_mbx`, `KL_mbx_wb` and `KL_mbx_axil`
  (three tops, not the bank) passes, with `KL_mbx` at 406,331 cells, the author's figure
  (`receipts/yosys_mbx.log`). The lint ratchet is 90 <= 90.

**Writers before the promising response:**

- **ACMP.** `acmp.c:285`, at the top of `transmit` (`:282`), runs `publish()` before
  every sent or queued frame, and `finish` (`:485`) runs it first. In `bind` (`:808`) and
  `unbind` (`:843`) the state moves before the response, and `srp_stop` (`:683`) clears
  the stream first. So a re-bind out of SETTLED publishes `SID_VALID` clear before its
  response.
- **MAAP.** `maap_mbx.c:62` writes the gate before the allocation callback, and `:70`
  refuses more than 16 sources.
- **SRP.** `LICENCE` is published before every licence report in `poll` (`:759`), before
  the revocations of `reset_interface` (`:701`), and before those of
  `srp_mbx_destroy` (`:333`). `SR_DOMAIN` and `IDLE_SLOPE` are written in
  `create_participants` (`:226`), `change_domain` (`:614`) and `declare_sources` (`:144`),
  before `mrp_mad_join` and the declarations, which leave later from the poll's
  `mrp_transmit`.
- **ADP.** It has no writer. Its `available_index` reaches only the CSR
  (`milan_csr.sv:2309`), as the design page says.
- **Firmware gate.** `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` with the
  pinned RV32 SDK (installed into scratch from the pinned archive by
  `scripts/ci_rv32_sdk.py`, digest verified) gives rc 0 and `test_ctrl_firmware: PASS`:
  - 57 arm reports, 0 failures;
  - 492 of 492 `ctrl_mutants.py` plants caught;
  - all 186 `srp_mutants.py` plants caught, plus the one-interface subset and the lwSRP
    pin arms (`receipts/fw_gate.log`).
- **Publication plants on their own.** The F-INT plants run separately
  (`scripts/fint_plants.py`): 21 of 21 ctrl and 18 of 18 SRP. That covers the moved,
  wrong-field and skipped plant for every writer, each caught by its named test
  (`receipts/fint_ctrl.log`, `receipts/fint_srp.log`).
- **Coverage.** `fw_coverage.py --check` gives `firmware coverage: PASS (22 files)`, and
  every writer file is at 100 % of lines and branches (`receipts/fw_cov.log`).

**The test-only event-delivery hold:**

- **Placement.** `mbx_model_evt_pause` is in `sw/firmware/ctrl/host/mbx_model.c:286` and
  is called only by `srp_mbx.cpp:852` and `:860`. No image or RV32 build compiles the host
  model.
- **The test asserts the hold.** `srp_mbx.cpp:859` checks "the DOWN record stayed held".
- **The hold's own plant.** Ignoring the hold fails that assertion (`cancelled-link-record-posted`
  in the campaign, and my `hold-ignored` probe).
- **Fidelity.** The RTL poster holds a LINK level while the ring is full and owes no
  record once the level returns (`KL_mbx_evt.sv:87`, `:112`, `:235`), which is what the
  model's hold reproduces.
- **Probes** (`scripts/probe_link_hold.py`; receipts `probe_head_if2`, `probe_parent_if1/2`,
  `probe_nohold_if1/2`):
  - At the parent `9b73a8c6`, at one and two interfaces, `cancelled-link-never-recovers`
    escapes. This confirms the author's report.
  - On a head export with the hold removed from the test, the correct firmware passes and
    the plant escapes.
  - With the hold removed and the publication writes compiled out of the driver, the plant
    is caught again. So the publication writes, through the model's on-access poster, are
    exactly what posted the record.
  - With the hold, the plant is caught.
- **Judgement:** the hold does not hide a firmware ordering issue. With records delivered,
  the correct firmware recovers and the test passes. The reset publish order (licence
  closed, then revocations, then participants re-created with `SR_DOMAIN` and
  `IDLE_SLOPE`) does not depend on event delivery. The hold restores the test's original
  intent, level recovery while the record is held, explicitly rather than by relying on the
  model's lazy poster.

**All-fabric default:**

- **Static check.** The only file outside the mailbox, firmware, tests and docs is
  `sw/litex/milan_soc.py`. All three of its hunks are inside `class CtrlMailbox`
  (`:2504-2572`), which is reached only through `add_ctrl_mailbox` under
  `if ctrl_mailbox:` (`:3343`). The mailbox sources are a curated list added only there
  (`:2486`) (`receipts/default_build_static.txt`).
- **Author's export proof.** `DEFAULT-BUILD.json` shows dev against head with 3,856 of
  3,876 files identical. The rest are date and stamp files, archives with identical members,
  and the comment-only hierarchy-tree order. A dev-against-dev re-export shows the same
  classes of difference, so they belong to the generator run.
- **What it proves.** This shows identical Vivado inputs, not a byte-identical bitstream.
  None was built.

**Firmware size** (`ctrl_srp_image.py`, pinned SDK, runtime built in scratch from the shared
LiteX sources; its archive digests differ from the author's, but the sections are identical):

| Shape | Base span | Head span | Delta | Of 224 KB |
|---|---:|---:|---:|---:|
| 1x1, one interface | 80,368 B | 81,376 B | +1,008 B | 35.5 % |
| 8x8, two interfaces | 122,672 B | 123,856 B | +1,184 B | 54.0 % |

AECP is not linked (F5). Receipts: `receipts/size_*`.

**Mailbox area:** I did not run Vivado, so the out-of-context figure (+446 LUT, +1,136 FF,
WNS +0.329 ns) is the author's. The flip-flop count matches the storage exactly: 80
interface bits plus 16 x 66 sink bits. The design page's table follows the existing
convention. The question of whether this answers the ruling's "M0s recipe" item is the
author's open question for the manager.

**Naming:** `measure_naming.py --check` reports NAMING RATCHET: PASS. `pub_idle_slope_bps_o`
carries its unit. The other eight ports carry gates, levels, identifiers and Domain codes,
which have no unit.

**Docs gates:** `docs_check.py` reports 0 findings. With the pinned Markdown renderer,
`check_em_dash.py --base 7c1b52be` reports 0 findings and `gen_toc.py --check` reports OK.
`git diff --check` is clean.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 MAJOR, F2 MINOR, F3 MINOR) | ruling 6088423771 against `mailbox.yaml:315-388`; `milan_datapath.sv:2008-2011`, `:5335-5407`, `:5677`, `:6225`, `:6270`; `KL_pp_shadow.sv:612-620`; `KL_acmp_talker.sv:359`, `:691`, `:740-750`; writer order in `acmp.c`, `maap_mbx.c`, `srp_mbx.c` | R582-1 | 25bbe4d956e79de979783d7e4706a5581c0742a7 |
| RTL | CLEAN | `KL_mbx.sv:62-70`, `:157-174`, `:260-313`, `:343-349`; `KL_mbx_pkg.sv:300-360`; `mailbox_skeleton.py`; bench 401/446/32/403/448/388; 167 of 167 plants; Yosys on 3 tops; lint ratchet | R582-1 | 25bbe4d956e79de979783d7e4706a5581c0742a7 |
| Robustness | CLEAN | P4 and P5 (holes, absent interfaces, partial strobe, reset); driver refusals (`mbx.c` `mbx_pub_*`, D14); `maap_mbx.c:70` count bound; `_Static_assert`s in `acmp_mbx.c:15` and `srp_mbx.c:23`; port re-entry guard (A31); destroy before `index` (`srp_mbx.c:333`); the cancelled-LINK hold probes | R582-1 | 25bbe4d956e79de979783d7e4706a5581c0742a7 |
| Tests | CLEAN | `suite.hpp:1668-1936` and `mutants.py` F-INT arms; `test_acmp.cpp` A31, `test_acmp_mbx.cpp` B10 and B11, `test_maap_mbx.cpp`, `srp_mbx.cpp:51-150`, `:841-870`; 492 of 492, 186 of 186, F-INT 21 + 18; coverage 22 files; probe receipts | R582-1 | 25bbe4d956e79de979783d7e4706a5581c0742a7 |
| Docs | UNCLEAN (F1, F2, F3) | `MAILBOX_SPLIT.md:802-860`, `:1046-1071`; `ARCHITECTURE_HW_SW_SPLIT.md:88-92`, `:187`; the generated `MAILBOX_CONTRACT.md`; the ctrl, maap, srp and mbx READMEs; PR body; HANDOFF | R582-1 | 25bbe4d956e79de979783d7e4706a5581c0742a7 |

## Real limits

- **Not run by me:**
  - Vivado: the `xvlog` front end and the out-of-context area. They are the author's, at
    `9b73a8c6`, whose child changes only the host model and two test files.
  - The LiteX default-config export. I checked the default path statically and rely on
    the author's export evidence.
  - Any bitstream, and the full Yosys, builder, parent, processor or gPTP banks.
- **Toolchain substitutions.** The firmware size uses a runtime archive I built from the
  shared LiteX sources; its digests differ from the author's, and the sizes match. The
  naming and Markdown gates ran in a scratch clone whose submodules are local clones at
  the gitlinks.
- **Where things ran.** Every build and probe ran in the scratch clone. The review clone
  was verified at the end (`receipts/clone_integrity.txt`): the index tree equals the
  head tree, gitlinks are unchanged, and status is clean.
- **Hardware and calibration.** Physical calibration was NOT RUN. Hosted field skips (the
  physical gPTP job) are not hardware proof.
- **Hosted contexts.** The exact-head hosted contexts I read were all `success` except
  that skip (`receipts/hosted_checks_snapshot.txt`). That is an observation only.

## Pending manager duties

- Decide F1 to F3, either fixes in this PR or recorded rulings, then re-review the
  corrected head.
- Answer the author's open question on the M0s area item.
- Validate the current-dev merge candidate (live dev `8b61b709`) with the builder and
  native banks, and accept the hosted and act evidence.
- Get the external review (R583).

R582-1 FINISHED
