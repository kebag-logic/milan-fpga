[A701b]

## Contents

- **[Status](#status)** -- REVIEW READY at the head below; `806-adopt-gptp-135afd04` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- The task, why it stays open until the bench run, and roles.
- **[Description](#description)** -- The gitlink, the companion, the review fixes, the records and the resource delta.
- **[Authoritative references](#authoritative-references)** -- The clauses, the donor PR and the gate rules.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout, submodules and tools.
- **[How to validate](#how-to-validate)** -- The gate commands and the expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- The gate's committed rule, the open risks and what this lane did not change.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

**REVIEW READY** at `0c45ebf28e2c11352aa4ad40d46780143b1a77ab`; `806-adopt-gptp-135afd04` -> `dev` (`1e80128f`).

Every gate #806 lists is rc 0, except the resource gate's committed rule on route-1x1. The last commit, `0c45ebf2`, changes three documents only; its docs gates are rc 0 at this head, and the results below were taken at `f99405af` and `cf3ef596`, whose other inputs are equal:

- The full parent sweep: 64 / 64 suites, 2,191,710 checks, 0 in-suite failures, 0 timed out. Among them `milan_dp` (its `gptp` and `gptp-lat` legs 210 / 210 each), `milan_dp_gm_steps` 202, `gptp_shadow` 325 and `tsn_fuzz` 897.
- `make -C tb/verilator/tsn_fuzz ptp`: 675 pass, its results file fresh.
- The physical gPTP leg (`milan_dp_gptp`): 205 checks, 0 failures, over 17.992742740 simulated seconds.
- The rtl-fast workflow, every job: success; behave 495 scenarios.
- Yosys: 60 / 60 tops. RTL lint within ratchet; xvlog 0 findings.
- The SystemVerilog, shell, C++ and Python idiom gates within every ratchet.
- The docs workflow under GNU Make 4.3, rerun at this head: 44 steps, 0 failed, 2 skipped by rule.
- Ten planted defects, each killed on every check it names.
- The resource gate: ooc-1x1 and ooc-8x8 pass; route-1x1 is refused on WNS alone.
- route-1x1 on the recipe's three placement directives: every corner of each meets the build floor; the best, AltSpreadLogic_high, has a worst-corner WNS of +0.235 ns.

Timing recovery is ruled under #814/#818; this change meets the build floor at every corner on its best directive.

## Linked Issue / roles

Relates to #806

#806 closes once the in-house qualification's link-toggle gPTP scenario passes on an image built from this change. That run belongs to the bench, after merge; this lane has no bench access.

FPGA-gPTP #94 (in the gPTP repository) is closed by its PR #95, merged as `135afd04`, the pin this adopts.

Executor: `[A701]` (round 1, to `f99405af`), `[A701b]` (round 2, `0c45ebf2`)
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

FPGA-gPTP main `135afd04` (PR #95, a merge of `409c3075` with an identical tree) gives the engine portEnabled, against IEEE 802.1AS-2011 with Cor1 and Cor2, the edition Milan v1.2 profiles:

| Behaviour the parent now sees | Clause |
|---|---|
| A link loss is portEnabled FALSE: asCapable clears at once, not at the fifth lost response, and the port starts no gPTP frame while disabled. A frame whose first byte is unaccepted is withdrawn; a started one completes | 802.1AS-2011 10.2.4.11; Figure 11-8 NOT_ENABLED |
| Each portEnabled edge after the first sample since reset ends the multiple-responder Pdelay_Req cease, one retained across a warm reset included; the rise sends one Pdelay_Req at once, and asCapable returns after two exchanges | Milan v1.2 4.2.6.2.5 and 4.2.6.2.4 |
| The 5-minute countdown exit is unchanged | Milan v1.2 4.2.6.2.5 |

The engine's one port change is the input `port_enabled_i`; no parameter changes, and the source set is unchanged. The parent drives it from `eff_link_w` (`hdl/milan/milan_datapath.sv:3194-3195`): the PHY link AND `LINK_CTRL[0]` (the firmware's link qualification) AND the link guard's receive-clock estimate (or the guard disabled), all `axis_clk` levels.

| Commit | Change |
|---|---|
| `f911adec` | `gptp-processor` gitlink `f97c1803` -> `135afd04` |
| `a20f458e` | PR #95's parent companion (sha256 `aeeab9c8...`, the version reviewed at `409c3075`), applied with `git apply --index` without its gitlink hunk (it names `409c3075`; commit 1 sets the merge, same tree). Every pre-image blob equals dev's and every post-image blob equals the patch's. `KL_gptp_shadow` gains `port_enabled_i`; `milan_datapath` drives it from `eff_link_w`; the three plane test wrappers tie it 1; the milan_dp `gptp` leg checks the link loss, the cease's toggle exit and the unchanged countdown |
| `e67ae2f1` | Review finish, tests: every companion check drove `i_link_up`, so a datapath wiring `port_enabled_i` to `i_link_up` alone passed them all. Adds `#94 asCapable falls when LINK_CTRL[0] withdraws the link`, `#94 asCapable falls when the guard loses the receive clock`, and a precondition before each loss so no fall passes vacuously |
| `f475329c` | Pin-derived records through their generators: the ROM ledger row (`gptp_ucode.hex` `99266fa9...`, equal to the donor's tracked images), the pin table, the boundary and time-sync diagrams, 19 donor links, and the port census header |
| `12a7948f` | Review finish, docs: the companion's port-enable section in `docs/design/GPTP_PLANE.md` failed the concise-style gate (7 findings); split to the limit, meaning unchanged |
| `67d8d192` | The loss page's detection table gains the link loss; the time-sync page says only an asCapable fall and rise re-arms link-up (the FPGA-gPTP #68 ruling's words), where it said nothing else does |
| `cf3ef596` | Review finish, tests, found by this lane's planted-defect campaign: with the donor's "the falling edge raises no event" planted, the `LINK_CTRL[0]` check passed on a stale TRUE and the rise's clear. Each link return's edge is now taken before the next phase reads asCapable; the campaign then kills that defect |
| `8eea9d3c` | The gPTP integrator guide names the port-enable seam |
| `f99405af` | The adoption record: pin page, changelog, and the area page's slice-headroom sentence with the gate's WNS refusal |
| `0c45ebf2` | R736-1-R1: the sentences on who resolves the WNS refusal now carry the #814/#818 ruling (the area page verbatim; the pin page and the changelog in two sentences, under the concise-style limit) |

### The new checks and the defects that kill them

All in the milan_dp `gptp` leg (`tb/verilator/milan_dp/sim_gptp.cpp:1717-1807`), which also runs as `gptp-lat`: 210 checks, 205 at the companion, 202 at dev. Each defect planted alone in a clean clone at `cf3ef596`, the leg rebuilt from scratch; three clean passes print no FAIL. Parent defects break the wiring; engine defects are the donor's own planted texts, by name from `gptp-processor/tb/verilator/engine/port_mutants.py`.

| Defect | Checks that print FAIL |
|---|---|
| The shadow ties portEnabled high | link loss, `LINK_CTRL[0]`, guard, toggle exit |
| The shadow ties it low | the three preconditions |
| The datapath drives it from the PHY link alone | `LINK_CTRL[0]`, guard |
| The datapath drops `LINK_CTRL[0]` | `LINK_CTRL[0]` |
| The datapath drops the guard's estimate | guard |
| Engine: a portEnabled edge keeps the cease | toggle exit |
| Engine: the falling edge raises no event | link loss, `LINK_CTRL[0]`, guard |
| Engine: slot 6 runs no NOT_ENABLED leg | link loss, `LINK_CTRL[0]`, guard, toggle exit |
| Engine: the countdown loads one beat less | countdown |
| Engine: the cease entry ends the cease at once | countdown |

10 of 10 killed, each on every check it names; every new check has a killer.

### Resources against the twelfth record

Vivado 2026.1, the recipe in `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, at `cf3ef596` (the later commits change documents only), one run at a time under the Vivado lock.

| Endpoint | Gate | LUT | FF | Other |
|---|---|---|---|---|
| route-1x1 | **refused** | 52,012 -> 51,837 (-175, tol. 500) | 53,707 -> 53,788 (+81, tol. 600) | slices 15,780 -> 15,823 (+43, tol. 80), 27 of 15,850 free; RAMB and DSP unchanged; **WNS +0.440 -> +0.032 ns (-0.408, tol. 0.25)**; WHS +0.036 -> +0.034 |
| ooc-1x1 | pass | 24,346, unchanged | 20,404, unchanged | RAMB and DSP unchanged |
| ooc-8x8 | pass | 34,156, unchanged | 29,782, unchanged | RAMB and DSP unchanged |

Against dev's own route (the #803 merge route, the same synthesis inputs as dev): +36 LUT, +28 FF, -11 slices, WNS -0.271 ns, on the shipping directive ExtraPostPlacementOpt. Every corner meets the build floor (WNS >= +0.03 ns, WHS >= 0): Slow WNS +0.032, WHS +0.052; Fast WNS +1.638, WHS +0.034. The worst setup path is the SoC path `docs/design/AREA_BUDGET.md` already names, the AXI-Lite-to-Wishbone bridge state to the SPI-flash PHY counter (18 logic levels), outside the wrapper and the datapath.

#### route-1x1 on the three placement directives

The #814 ruling judges WNS on the build floor at every corner, on the best of the recipe's three directives; the fall from the record becomes a warning (#818 changes the gate). The recipe's directive step reran implementation at `f99405af` from the same synthesis checkpoint, with only `place_design -directive` changed and the default seed.

| Directive | Slow 0C / 85C WNS, WHS | Fast 0C / 85C WNS, WHS | LUT | FF | Slices (free) | Worst setup path |
|---|---|---|---:|---:|---|---|
| ExtraPostPlacementOpt (shipping) | +0.032, +0.052 | +1.638, +0.034 | 51,837 | 53,788 | 15,823 (27) | SoC AXI-Lite-to-Wishbone bridge to the SPI-flash PHY counter, 18 levels |
| **AltSpreadLogic_high (best)** | **+0.235**, +0.037 | +1.633, +0.011 | 51,874 | 53,787 | 15,837 (13) | the sys-clock reset synchroniser's output (`macsys_rst`, fan-out 212) to the MAC RMON counters' reset, 0 levels, 8.757 ns of routing |
| ExtraTimingOpt | +0.218, +0.037 | +1.633, +0.011 | 51,849 | 53,787 | 15,837 (13) | the same bridge-to-flash path, 18 levels |

Both corners of each temperature pair read the same; TNS and THS are 0 everywhere; every run has 0 routing errors and the same RAMB and DSP counts. Against the record, the best directive's WNS fall is 0.205 ns (a warning under the ruling) and its slices are +57 (tolerance 80). The committed gate cannot read a directive run (it refuses it as holding no recipe script), so these figures come from its own parsers; #818 adds that comparison. Nothing is re-recorded here: the record follows #818's format, and the re-record comes from the merge route.

## Authoritative references

- IEEE 802.1AS-2011 with Cor1-2013 and Cor2-2015: 10.2.4.11 portEnabled (MAC_Operational and the administrative port state); 11.2.15 and Figure 11-8, NOT_ENABLED, left only through INITIAL_SEND_PDELAY_REQ with lostResponses 0 and asCapable FALSE.
- Milan v1.2 4.2.6.2.4 (asCapable after two exchanges) and 4.2.6.2.5 (the cease ends when the link state toggles, portEnabled toggles, pttPortEnabled toggles, or after 5 minutes).
- FPGA-gPTP #94 and PR #95; the engine's port-enable contract in its `docs/INTEGRATION.md` at `135afd04`.
- FPGA-gPTP #68's link-up ruling: only an asCapable fall and rise (or reset) re-arms the 20 us link-up step.
- `docs/design/GPTP_PLANE.md` (Port enable), `docs/design/AREA_BUDGET.md` (the resource gate), `docs/integration/BUILDING.md` section 5 (the build floor), `docs/testing/CI_WORKFLOWS.md` (worker projections).

## How to get into the same state

```sh
git fetch origin 806-adopt-gptp-135afd04
git switch --detach FETCH_HEAD
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
git -C gptp-processor rev-parse HEAD
git submodule status
```

`gptp-processor` reads `135afd043309369a87ddbc8d6550aff8ec52a157`. Tools: Verilator 5.050, sv2v v0.0.12, Yosys 0.66, GNU Make 4.3, CPython 3.12.3, tsn-gen at `deca300c` (the workflows' `TSN_GEN_REV`), Vivado 2026.1 for the resource gate.

## How to validate

```sh
make -C tb/verilator/milan_dp gptp
make -C tb/verilator/milan_dp gptp-lat
make -C tb/verilator/milan_dp_gm_steps
make -C tb/verilator/tsn_fuzz ptp
bash scripts/run_all_suites.sh logs --wait
python3 scripts/suite_tally.py logs --quiet --expect-suite-root tb/verilator
bash scripts/run_all_suites.sh logs-physical --wait --physical-gptp
python3 scripts/suite_tally.py logs-physical --quiet --expect-suite-root tb/verilator --physical-gptp
bash syn/yosys/run.sh
python3 scripts/lint_rtl.py --check
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/check_doc_style.py
python3 scripts/docs_check.py
python3 scripts/check_submodule_docs.py
python3 scripts/check_gptp_docs.py --with-submodule
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 docs/diagrams/timesync_chain.gen.py --check
bash syn/yosys/ooc.sh --record-rom-digests
git diff --exit-code syn/yosys/rom_digests.tsv
python3 scripts/check_port_contracts.py
python3 syn/ooc/pp_resource_gate.py check-baseline
```

The directive runs follow the recipe's "Repeat implementation with the repository's other two placement directives" step in `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, from the route's own synthesis checkpoint.

Expected result / pass criteria: the `gptp` and `gptp-lat` legs print `210 checks: 210 PASS, 0 FAIL`; the sweep tallies 64 suites with 0 in-suite failures; the physical suite 205 checks, 0 failures; `tsn_fuzz ptp` 675 pass with its results file fresh; Yosys 60 / 60 tops; every listed gate exits 0, and the ROM ledger is byte-identical after re-recording. The resource gate (`python3 syn/ooc/pp_resource_gate.py check <dir> --endpoint <e>` after the recipe's three runs) passes ooc-1x1 and ooc-8x8 and refuses route-1x1 on WNS, as recorded above. Each directive run meets WNS >= +0.03 ns and WHS >= 0 at every corner; AltSpreadLogic_high is the best, at +0.235 ns.

Measured here (receipts kept with the lane's evidence):

| Gate | Result |
|---|---|
| Sweep, four shards, then the tally | 64 / 64 suites, 2,191,710 checks, 0 in-suite failures |
| `gptp` and `gptp-lat` legs | 210 / 210 each |
| `tsn_fuzz ptp` | 675 pass, freshness PASS; the results file changes only its date stamp, so it stays as committed |
| Physical suite (its inputs at `cf3ef596` equal this head's) | 205 checks: physical 151, setup abort 6, no-TX 20, no-Pdelay 14, recentre 14; 5,653 s of its 6,900 s deadline |
| rtl-fast, every job | success; behave 14 features, 495 scenarios, 2,288 steps |
| Yosys | 60 / 60 tops; 0 unjustified ties; TAP-PURITY PASS |
| Lint, xvlog, idiom, port, naming, test-evidence, source-list and builder gates | rc 0; the builder's two NOT RUN arms are the ones #803 recorded |
| Docs workflow | 44 steps, 0 failed; the LiteX builder leg, the Markdown gates on CPython 3.12.3 and the no-git gates rc 0 |
| Planted defects (at `cf3ef596`, the leg's inputs equal) | 3 clean passes; 10 of 10 killed |
| Resource gate (at `cf3ef596`, synthesis inputs equal) | ooc-1x1 and ooc-8x8 pass, equal to the record; route-1x1 refused on WNS |
| route-1x1, AltSpreadLogic_high and ExtraTimingOpt (at `f99405af`, the same synthesis checkpoint) | both rc 0, 0 routing errors; worst-corner WNS +0.235 and +0.218 ns, WHS +0.011 ns |
| Docs gates at `0c45ebf2`: concise style, TOC (self-test, anchors, check), the resource record, submodule and gPTP docs, hygiene, TODO ownership, feature status, `docs_check.py`, and the docs workflow | rc 0; docs workflow 44 steps, 0 failed, 2 skipped by rule; the LiteX builder leg, the Markdown gates on CPython 3.12.3 and the no-git gates rc 0 |

## Known limitations / out of scope

- **The resource gate's committed rule refuses route-1x1.** On the shipping directive its WNS, +0.032 ns, is 0.408 ns under the record's +0.440 ns, beyond the 0.25 ns tolerance. Every other figure is within tolerance, the route fits with 27 slices free, and every corner meets the build floor. The slow path is in the SoC, which this change does not touch. Timing recovery is ruled under #814/#818; this change meets the build floor at every corner on its best directive. The best directive, AltSpreadLogic_high, leaves 13 slices free, not 27. This lane re-records nothing; the re-record follows #818 from the merge route.
- **The `milan_dp` gptp case's hosted window.** On this host the case's user time rises from 163.8 s (dev) to 335.4 s (the companion) and 351.1 s (this head). `gptp` sits in `milan_dp` leg 0, whose worker projects 1,551 s against the 1,620 s rule with 69 s of margin, so its hosted window will likely exceed the projection; the 45-minute timeout is not at risk. `PIECE_SECONDS` are hosted measurements, to be refreshed from this change's hosted run as `docs/testing/CI_WORKFLOWS.md` prescribes; this lane does not invent them.
- The bench scenario, as in Linked Issue.
- pttPortEnabled, the cease's third exit in Milan v1.2 4.2.6.2.5, has no parent control (always enabled), so nothing drives it.
- The guard check runs last in the leg: once armed, the guard starts its MAC recovery for a receive clock this leg does not model.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied: not yet (the area gate follows #818 and its re-record; the bench scenario after merge)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes: every gate rc 0 except the resource gate's committed route-1x1 rule, which #818 replaces
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
