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
