[A635] Cut the notify-queue to event-router path

Refs #181. This PR does not close the issue, because acceptance item 1 is not met: the cut removes the
path, but the logic depth does not halve. The measurements are below.

Branch `181-notify-router-cut`, from main `22c139a4`, head `16c89c53`. Four commits: the RTL, the
architecture docs, the out-of-context record, and the record of the cone's two halves. Merges cleanly
into current main.

## The cone

On the parent's route-1x1 with milan-fpga #760's change, the worst setup path at base runs from
`u_notify/cmdq_count_r` to `u_event_router/sel_r`: 30 levels, +0.016 ns. It passes through:

- `u_notify`: the count's nonzero compare, merged with the emission pick into `amap_busy_o`;
- the AECP admission ready, the scoreboard's ACMP-versus-AECP pick and the ACMP listener's ready;
- `u_event_router`: the acknowledge entering the round-robin scan's base and pending set, then the
  priority scan, then `sel_r`.

## The change

- `hdl/aecp/KL_aecp_notify.sv`: a new flop, `cmdq_nempty_r`, holds the queue's occupancy. It is
  written beside every count update: cleared at reset, set by a push, and on a pop with no push it
  takes `cmdq_count_r != 1`. `amap_busy_o` and the emission pick read this flop instead of comparing
  the count. The push condition and every emission rule are unchanged.
- `hdl/packet_engine/KL_pp_event_router.sv`: the scan's base and its pending-minus-presented set are
  keyed on `valid_r` instead of `deliver_w`, so the next select comes from registers only. The
  acknowledge now only enables the select's existing load (`deliver_w || !valid_r`). A grant is only
  loaded on a delivery or from idle, and in both cases the new scan is exactly the old one.
- Docs: `03_packet_engine.md` §5 (the router's registered scan), the `cmdq_*` row in
  `06_aecp_engine.md`, and the measurement in `syn/ooc/README.md`.

There is no register-map, top-level port or parameter change, and nothing outside `u_notify` and
`u_event_router` changes. No command decode changes either, so the #176, #177 and #178 paths are
untouched. SET_STREAM_INFO is accepted and refused exactly as at base, and its success notification
is queued and emitted in the same cycle.

## Behaviour: no added cycle

Every port of both modules is cycle for cycle equal to base, so the documented service bounds stand
as they are.

- Router: a Yosys sequential equivalence check of base against head (`equiv_simple -seq 2`,
  `equiv_induct -seq 2`, `equiv_status -assert`) proves every equivalence cell at `N_SRC_P` 1, 5, 8,
  16 and 29 (91 / 205 / 286 / 505 / 859 cells, 0 unproven).
- Notify: temporal induction proves `cmdq_nempty_r == (cmdq_count_r != 0)` in every cycle after
  reset. It is proven at 1 in / 1 out and at the default shape, and at `N_IF_P=2,
  EN_IDENTIFY_NOTIF_P=1` with a deeper bound. Head differs from base only by the flop and its two
  readers, so given the invariant every output is unchanged.
- Planted mutants, run outside the tree, each fail these proofs:
  - notify: the pop keeps the queue occupied; the push is not seen; the pop is off by one. Each
    fails with `Induction step failed` and `proof did fail!`.
  - router: the base is always `ptr_r` (6 cells unproven); the presented event is not removed
    (2 unproven); the load ignores the acknowledge (8 unproven).
  - Both unmutated controls pass.

## Depth: out-of-context synthesis

This uses the unchanged complete-processor recipe at 10 ns. The full table is in `syn/ooc/README.md`.

| | 1x1 base | 1x1 head | 8x8 base | 8x8 head |
|---|---:|---:|---:|---:|
| `cmdq_count_r` to `sel_r` | 22 levels | no path | 32 levels | no path |
| `cmdq_count_r` to `cmdq_nempty_r` | - | 3 levels | - | 2 levels |
| `cmdq_nempty_r` to `sel_r` | - | 22 levels | - | 22 levels |
| WNS | -5.416 | -5.416 | -11.482 | -6.045 |

The depth does not halve. The half after the register keeps 22 levels at both shapes. Of those, 16 to
18 sit in the AECP admission ready, the scoreboard and the ACMP listener, between the two blocks, and
those modules are outside this change's scope. At 8x8 the cut removes about 10 levels, mostly the
router's scan. At 1x1 it removes none, because the count compare was already folded into the emission
pick.

## Routed: parent route-1x1

The scratch parent is milan-fpga dev `7d79ffb2` with the gitlink moved, never committed. The
route-1x1 recipe is unchanged, every run held the exclusive lock, and the route-1x1 resource gate was
run on each result.

| Route | WNS | gate | worst path | count to select | occupancy to select |
|---|---:|---|---|---|---|
| base, with #760 | +0.016 ns | fails (below the +0.03 floor) | the cone, 30 levels | 30 levels | - |
| head, without #760 | +0.181 ns | passes | `u_aecp/u_d3`, outside the cone | no path | 24 levels, +2.778 ns |
| head, with #760 | +0.144 ns | passes | Ethernet receive clock, outside the processor | no path | 24 levels, +3.196 ns |

With #760 the cone is no longer the worst path, and the route passes the gate's WNS floor. Routed,
the half after the register is still 24 of the cone's 30 levels.

## Gates

The rc tables are identical at base and head, and so are the records:

- processor gates, all rc 0: `scripts/run_suites.sh`, `scripts/lint_hdl.sh`, `make check`,
  `scripts/gen_matrix.py --check`, `syn/yosys/run.sh`, the req-tag execution check and the Yosys
  elaboration guards. The only differences are source and netlist line numbers in warnings and guard
  messages;
- every campaign that builds a changed file, all rc 0: the d3, notify, AECP dispatch, AECP, counter, GSI,
  name-write, ACMP, name-state and elaboration-guard mutant campaigns. Every graded
  record is identical, with source line numbers normalised for the elaboration guards;
- the scratch parent's consumer gates. Two of them return rc 1 at both base and head, and neither
  is this change's: the moved gitlink's documented pin, and the dev's existing test-evidence
  ratchet. The ROM digests are identical.
