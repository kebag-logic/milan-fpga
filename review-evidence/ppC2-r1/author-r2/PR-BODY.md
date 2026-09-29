[A439]

Closes #66
Closes #67
Closes #68

Lane C2 (MAAP) of the PP program. It drives the three MAAP behaviours the
compliance-matrix audit found untested (GAP-04: REQ-MAAP-001, -002 and -005), fixes
the one RTL defect a new test exposed, and adds a MAAP mutation campaign with a
ledger. Branch `c2-maap-coverage` from `main` `c951a9ff`, head `b03d36f`.

## 1. #66: the fit clamp (IEEE 1722-2016 B.1, B.3.6.1, Table B.9; REQ-MAAP-001)

- **Reject arm, deterministic** (`tb/maap` U17). The widest block (`cfg_count_i` =
  255) fits the pool only at offsets up to `0xFE00 - 255 = 0xFD01`. A kind-7 stub
  in `maap_wrap.sv` (harness only; kinds 5 and 6 pass through) hands the engine
  `0xFDFF`, then `0xFD02`, then `0xFD01`. The two overhanging draws are redrawn
  (three draws consumed), and the byte-exact PROBE names `91:E0:F0:00:FD:01`,
  count 255, whose block ends exactly at `91:E0:F0:00:FD:FF`.
- **Seed clamp** (U18). A seeded walk with `cfg_seed_offset_i = 0xFFFF` (above
  `0xFE00 - 8`) probes the clamped offset `0xFDF8` byte-exact without drawing an
  address (footnote a). It claims the block and grants its last source
  `91:E0:F0:00:FD:FF`.
- **RTL fix, found by U17b** (`hdl/maap/KL_pp_maap.sv:569-577`). An engage fall
  (Release! or link loss) while a kind-7 draw was in flight left the walker's
  draw mark set. The answer arrived in `W_OFF` unread, and the next walk's
  `W_IVAL` waited forever. From then on no PortOperational! reached
  ReserveAddress!, so there was no PROBE and no claim until reset (Table B.7,
  PortOperational! from INITIAL; B.3.5.9). U17b drops the link at four
  consecutive cycles of the redraw loop and requires every re-engage to probe.
  Before the fix it failed phases 1 to 3 and U18 behind the wedge (6 FAIL of 89).
  The `W_ADDR` exit now clears the mark.
- Mutants `fit-compare-forced-true` (the compare the issue cites at `:587`, now
  `:594`), `fit-compare-off-by-one`, `seed-clamp-removed` and
  `release-keeps-draw-mark` are all KILLED.

## 2. #67: maap_version 0 and 2 through the real RX validator (B.2.3.2, B.2.3.4, Tables B.1/B.10; REQ-MAAP-002)

- `tb/rx_validator` F28: PROBEs with maap_version 2, 0 and 31 (31 sets all five
  bits of the lane) are each accepted, committed, demuxed to `PP_PROTO_MAAP`, and
  deliver the received version in the status lane. The hdr beat is compared field
  by field.
- `tb/pp_top` MP7: a conflicting maap_version-2 PROBE, then a maap_version-0
  PROBE, against the DEFEND-state claim crosses the real validator and dispatch.
  Each is answered by a byte-exact unicast DEFEND carrying our version 1 and the
  B.3.6.6 overlap, and the claim is kept.
- Mutant `validator-maap-version-1-only` (a `maap_version == 1` acceptance rule
  added to the validator) turns both suites red: F28, 47 FAIL of 453; MP7, 4 FAIL
  of 33.
- No RTL change was needed.

## 3. #68: the Table B.7 conflict walk with a discriminating compare_MAC (B.3.5.5 to B.3.5.7, Table B.7, B.3.6.4; REQ-MAAP-005)

- Every tie-break scenario now uses a peer whose forward and octet-reversed orders
  against our MAC disagree, and checks that premise. `00:11:22:33:44:FF` is
  forward-lower but reversed-higher (we win). `F2:11:22:33:44:01` is
  forward-higher but reversed-lower (we lose).

  | Cell | We win | We lose |
  |---|---|---|
  | PROBE / rProbe! | U9: the walk continues | U19 (new): yield, fresh range |
  | DEFEND / rAnnounce! | U7: the claim stands | U8: yield, fresh 4-probe walk |
  | DEFEND / rDefend! | U20 (new): the claim stands, nothing sent | U21 (new): yield, fresh range |

- U22 (new): PROBE / rAnnounce! from a peer we beat in both orders still yields
  (no tie-break).
- `tb/pp_top` MP4's winner is now `F2:11:22:33:44:01`: reversed-lower, and
  forward-higher than the bench's `0A:0B:0C:0D:0E:0F`.
- Mutant `compare-mac-forward` (`cmp_mac_true_w = own_mac_i < rxm_sa_r`) turns
  `tb/maap` red (9 FAIL) and MP4 red (5 FAIL). One arm per new cell
  (`probe-rprobe-never-yields`, `defend-rdefend-ignored`,
  `defend-rdefend-no-tiebreak`, `probe-rannounce-tiebreak`) and
  `yield-reuses-range` are also KILLED.
- `tb/maap/README.md` now carries the mutation ledger, in the SRP suites' form.
- No RTL change was needed.

## Mutation campaign

`make -C tb/maap mutants` plants each reviewed patch in `tb/maap/mutations/` into a
scratch copy of `hdl/` with `git apply`. Controls run first. Each arm must finish
its simulation red with its own named check, and a build failure or a missing
tally never counts as a kill. The driver reads only simulation logs. pp_top arms
use the new `make -C tb/pp_top maap-internal` (the MP section alone). The HDL
workflow runs the campaign next to the SRP one. At the head: 3 controls PASS and
13 of 13 arm runs KILLED.

## Validation (processor, head `b03d36f`)

- `./scripts/run_suites.sh`: rc 0, 33 suites, 1,015,919 checks, 0 failing (base:
  1,015,815). maap 75 to 114, rx_validator 393 to 453, pp_top 7,751 to 7,756.
- `./scripts/lint_hdl.sh`, `make check`, `scripts/gen_matrix.py --check`,
  `git diff --check c951a9ff HEAD`: rc 0.
- `make -C tb/maap mutants`: rc 0, 16 of 16.
- `make -C tb/srp_top mutants`: 56 of 56 KILLED, assertion coverage 49/49, run
  in batches.
- `make -C tb/nvm_port figures`: rc 0.
- `syn/yosys/run.sh`: rc 0.
- pp_top `gsi-internal`, `name-writes` and `maap-internal`: rc 0.

The SRP campaign, the NVM figures, Yosys and the pp_top `gsi-internal` and
`name-writes` runs were at `3407c84`. `b03d36f` changes only one rx_validator test
file, which none of them reads. `maap-internal` ran at the head, inside the MAAP
campaign.

## Parent consumer gates

Run in a scratch parent at milan-fpga dev `13eda870`, with the gitlink at
`b03d36f`. It was the 15 identifiable consumer commands, plus both candidates for
the sixteenth (`protocol-processor/scripts/check-integrator-params.py`,
`scripts/lint_rtl.py --check`).

- All rc 0: the nine script gates (C++ and Python idiom, xvlog, RTL source lists,
  `pp_srcs`, port contracts, naming, test evidence, docs), `pp_shadow` (2,120
  checks), `nvm_cosim` lint and quick (315/315), `milan_dp_render` (152/152, 65/65,
  5/5), and both candidates.
- `test_builder --require-elaboration --require-rv32`: rc 0, with its one
  recorded NOT RUN arm (gate 11: the placement report is absent on the host).
- `milan_dp`: rc 0. Every leg passes (gptp, gptp-lat, gmstep, main, notify,
  crflic, nxn, nxndv, nxn8, nxn4c, nolpf, prune, ax1x1, aclk), and the render
  and gmstep mutation campaigns are 6/6 each.

The C++ rule-11 gate first counted one multi-declarator declaration in the new F28
test. `b03d36f` fixes it, and the gate is back at 0 <= 0.

## Parent-visible for pin adoption

1. No port, parameter or interface change.
2. The `KL_pp_maap` fix acts only with `cfg_maap_internal_i = 1`. The parent ties
   it to 0 (`hdl/milan/milan_datapath.sv:7695`), so the shipping fabric is
   unchanged.
3. Optional: `scripts/measure_test_evidence.py --check` passes with 74 <= 77
   unarmed suites (75 <= 77 at the base pin), because `tb/maap` is now armed by
   its `mutants` driver. The budget could be lowered to 74. No disposition row is
   needed: 0 unexplained readers, and no host time.
4. New entry points: `make -C tb/maap mutants`, `make -C tb/pp_top maap-internal`.

## What remains

- The manager's official consumer bank, hosted CI and the two reviews.
- Two corners of the Release! arc, reasoned from the source and not in this
  scope; each would need its own issue:
  - the `W_ADDR` engage-fall exit does not re-arm the footnote-a seed, which
    `docs/architecture/11_maap_engine.md` §6 says Release! does;
  - a frame already being drawn or built when the engage falls still leaves
    the wire, although footnote c says Release! sends no PDU.

## Round 2 ([A445]): R400-1 and R401-1

Head `053f979`, nine commits on `b03d36f`. Both round-1 reviews were NEGATIVE:
R400-1 had four MINORs, and R401-1 had one MINOR and three suggestions. This
round resolves them as below.

The round first stopped at `ea79d8b`: a frame whose TX slot was requested before
the fall still left after it, and recalling it would need a processor port
change. The manager ruled that such a frame may drain (option 2: no cancel path,
no port change), and set three points for R400-1 F1. The last three commits
close them. No RTL logic changed after the ruling.

### The Release! rule (IEEE 1722-2016 Table B.7, B.3.1 c) and e), B.3.2, B.3.5.2, B.3.5.9, footnotes a and c)

Table B.7's Release! row stops probe_timer (PROBE) or announce_timer (DEFEND)
and returns to INITIAL. No Release! cell carries sProbe, sAnnounce or sDefend,
and a stopped timer does not expire. B.3.2 executes each state table entry
sequentially. The walker executes an entry over many cycles, so a Release! that
lands mid-entry is ordered by that entry's TX slot request:

- **Before the request.** The Release! comes first and the entry is dropped whole:
  no timer, no frame, no state change. This holds in every walker state that runs
  before the request, and for a fall of a single cycle.
- **From the request on.** The frame belongs to the entry that requested it, and
  it drains as that entry's last act. It is the only frame that can: no slot
  request follows the fall. The top's pool-access arbiter holds the builder as
  owner until it commits, and `KL_pp_tx_slots` frees a committed slot only by
  sending it. The Release! does not wait for the frame:
  - the claim is withdrawn at the fall;
  - the entry's state change is dropped, so no claim is published after the fall;
  - the Release! is latched, so a rise that lands before the lane takes the frame
    still gives INITIAL and a fresh walk.
- **The drain window** runs from the slot request to the lane grant: 63 cycles
  when the pool and the lane grant at once, longer in the top, and unbounded
  while the egress stalls.
- **Begin!/PortOperational!** is the engage level as the released machine sees
  it, so a rise during the teardown or a drain is never lost.
- **Every Release! re-arms the footnote-a seed.** Within an engagement the seed
  is probed once and a conflict is never answered with it again.

`docs/architecture/11_maap_engine.md` §6 and the `KL_pp_maap.sv` banner state
this rule. They cite Table B.7, B.3.2 and B.3.5.2 for the ordering and say "no PDU
generated after the fall". REQ-MAAP-007 and `tb/maap/README.md` say the same.

### Per finding

| Finding | Commit | Change | Clause | Failing arm |
|---|---|---|---|---|
| R400-1 F1 (R401-1 F2 and F3 folded in) | `4de2c60` | `W_IVAL`, `W_RX` and `W_POST` honour a fall; the TX states withdraw the claim and latch the Release!; `W_OFF` starts on the engage level | Table B.7 Release!/PortOperational!, B.3.2, B.3.5.2, B.3.5.9 | U23 to U26 fail 13 checks against the start head's RTL. Arms `ival-sends-after-release`, `post-publishes-after-release`, `tx-path-absorbs-release`, `off-waits-for-an-edge`, `rx-release-returns-to-idle`: all KILLED |
| R400-1 F1, ruling point 1 | `d0acc9b` | U28: 17 falls, landed so the walker first sees each in a chosen state, cover all 12 walker states. For 33 s after each: no TX slot request, no timer started, no timer expiry, no claim, INITIAL; at most the one frame requested by then drains | Table B.7 Release!, B.3.1 c) and e), B.3.2 | New arms `idle-serves-a-latched-expiry-first` and `teardown-keeps-announce-timer`, both KILLED on U28. U28 fails 4 checks against the start head's RTL |
| R400-1 F1, ruling point 2 | `4f6affc` | U23's drained arm: exactly one slot request (the ANNOUNCE's), byte-exact, on the lane within 63 cycles of the fall at each of 75 offsets (measured maximum 63) | B.3.2, Table B.7 Release! | New arm `drain-waits-for-the-link` KILLED on U23 (drain and window) |
| R400-1 F1, ruling point 3 | `053f979` | `11` §6 and the banner cite Table B.7, B.3.2 and B.3.5.2, and say "no PDU generated after the fall" | Table B.7, B.3.2, B.3.5.2 | (docs) |
| R400-1 F2 + R401-1 F1 | `8ae76ee` | `W_OFF`, which every Release! reaches, re-arms the seed | Table B.7 footnote a | U27 fails the `W_ADDR` arc at the start head. Arm `seed-rearmed-on-idle-release-only` KILLED |
| R400-1 F3 | `fa21c58` | U18b: seed `0xFDF9` clamped to `0xFDF8`; `0xFDF8` and `0xFDF7` taken as given; byte-exact, no draw | B.1, Table B.9, footnote a | Arm `seed-clamp-off-by-one` KILLED; the reviewer's own patch is killed too |
| R400-1 F4 | `2c11d6f` | U17c: Release! during a draw that fits: nothing sent, the draw is never adopted, the next engage probes | Table B.7 Release!, B.3.5.9 | Arm `release-waits-for-draw` KILLED; the reviewer's own patch is killed too |
| R401-1 F4 (suggestion) | `8382cf6` | The comment and README name both stalled states: `W_ADDR` for an unseeded walk, `W_IVAL` for a seeded one | (docs) | none needed |

`ea79d8b` only reorders the scenarios, so U19 to U22 still end the suite, as the
reviewers' probe scripts expect. R400-1 S1 and S2 are retained: they are not in
the round-2 assignment.

**The reviewers' probes at `053f979`.** R400's P1, P1c, P3, P4 and P5 pass, and
P2's claim part passes (0 of 160 offsets). P2's PDU part counts 64 of 160
offsets. Classified in P2's own slot, each of the 64 is the ANNOUNCE whose slot
was requested by the first cycle the fall is seen: no offset has a slot request
after it, and the latest lane request comes 63 cycles after the fall. R401's P1
and P2 pass. Its P3 frame is the first PROBE, which was already being written
when the fall was seen, with no slot request after it. Both are the drain the
ruling accepts; the probes' literal checks still count them.

### Parent-visible for pin adoption (round 2)

1. No port, parameter or interface change. The Release! change acts only with
   `cfg_maap_internal_i = 1`, which the parent ties to 0.
2. The unit wrapper `tb/maap/maap_wrap.sv` reads the walker state through one
   hierarchical reference. The parent's port-contract inventory of test-only
   hierarchical observations goes from 133 to 134; it is not a ratchet, and the
   gate passes.
3. Tallies: `tb/maap` goes from 114 to 191 checks, and `run_suites.sh` from
   1,015,919 to 1,015,996. The MAAP campaign is now 3 controls plus 24 arms
   (27 checks).
4. REQ-MAAP-007's wording changed in `docs/00_MILAN_COMPLIANCE_REVIEW.md`; the
   parent's compliance matrix does not quote it.
5. Unchanged: the test-evidence ratchet can still be lowered to 74, and the entry
   points are the same.

### Validation (round 2, head `053f979`)

- **Processor:**
  - `./scripts/run_suites.sh` rc 0 (33 suites, 1,015,996 checks);
  - `./scripts/lint_hdl.sh`, `make check`, `scripts/gen_matrix.py --check` and
    `git diff --check` all rc 0;
  - `make -C tb/maap mutants`: 27/27;
  - `make -C tb/srp_top mutants`: 56/56 KILLED, coverage 49/49, in batches;
  - `make -C tb/nvm_port figures`, `syn/yosys/run.sh`, and pp_top
    `maap-internal`, `gsi-internal` and `name-writes`: all rc 0.
- **Reviewers' round-1 scripts** at the new head, on the reviewers' Verilator
  5.050: head suites green, the campaign 27/27, both of R401's own mutants
  KILLED, 4 of 5 of R400's mutants KILLED (S1's survives), and the probes as
  above.
- **Parent consumer gates** in a scratch parent at milan-fpga dev `9e3ccbfb`,
  gitlink at `053f979`: see the table below.

| Parent consumer command (scratch parent, dev `9e3ccbfb`, gitlink `053f979`) | rc | Result |
|---|---|---|
| `scripts/check_cpp_idiom.py`, `check_py_idiom.py`, `docs_check.py` | 0, 0, 0 | within budget; 0 findings |
| `scripts/xvlog_gate.py --check` | 0 | 4 findings == ratchet, as at round 1 |
| `scripts/check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | 0, 0 | OK |
| `scripts/check_port_contracts.py` | 0 | processor 111 <= 111 undocumented, no port added |
| `scripts/measure_naming.py --check` | 0 | 96 recorded |
| `scripts/measure_test_evidence.py --check` | 0 | 74 <= 77; can be lowered to 74 |
| `sw/builder/test_builder.py --require-elaboration --require-rv32` | 0 | all gates pass except gate 11 NOT RUN (placement report absent on the host, as at round 1) |
| `make -C tb/verilator/pp_shadow` | 0 | 2,120 checks, no PINMISSING |
| `make -C tb/verilator/nvm_cosim lint` / `quick` | 0 / 0 | 84 non-fatal warnings / 315/315 |
| `make -C tb/verilator/milan_dp` | 0 | every leg PASS (gptp 181 ... aclk 190); render and gmstep controls 6/6 each |
| `make -C tb/verilator/milan_dp_render` | 0 | 152/152, 65/65, 5/5 |
| `protocol-processor/scripts/check-integrator-params.py`, `scripts/lint_rtl.py --check` | 0, 0 | 24/24/24; 90 <= 90 |
