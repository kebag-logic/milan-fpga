[A635] Cut the notify-queue to event-router path

Closes #181. Under the [A10] ruling on acceptance item 1 (issue comment 6249065327), item 1 is replaced by its purpose: the cone no longer limits the shipping timing gate. The depth target is not met (22 levels OOC, 24 routed); the measurements are below.

Round 1: branch `181-notify-router-cut`, from main `22c139a4`, head `16c89c53`. Four commits: the RTL, the
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

## Round 2

The round-2 head is `c5afc0a4`, three commits on `42eb9aef`:

- a merge of processor main `08ae0013`, which brings in #176's SET_STREAM_INFO 2013 body. It has no
  conflict, and its tree is the one `git merge-tree` gives;
- the requirement IDs in the two #181 comments, R649-1-F2's exact wording. This commit changes comments only;
- the in-tree checks of the duplicated occupancy state (R648-1-F-2).

There is no register-map, top-level port or parameter change. In this change's two RTL files, only
comments differ from round 1. No command decode changes either: SET_STREAM_INFO is accepted and
refused exactly as on main. That means the 2021 body (cdl 96) and, since #176, the 2013 body (cdl 60);
any other length is BAD_ARGUMENTS.

### The occupancy flop, checked in tree (R648-1-F-2)

`tb/aecp_notify` gains two sections. A Verilator configuration file, `occupancy.vlt`, makes the queue's
count and its occupancy flop readable by the bench. It changes no RTL.

- **OC1** ends every run of all three builds. It checks `cmdq_nempty_r == (cmdq_count_r != 0)` at every
  clock edge.
- **CQ1** pushes two commands back to back into an idle block. The second goes in the clock the emitter
  claims the first, and it is the last push. Each registered controller but the requester receives both
  entries, in order, at its next sequence_id.
- **CQ2** pushes `P-NOTIF-QUEUE-DEPTH` + 1 = 17 commands behind a held round, which fills the queue to
  16. Every entry reaches each registered controller but its requester, in order: 26 jobs.
- **CQ1b** and **CQ2b**: `amap_busy_o` is high in every clock from the first push to the last job, and
  low after it. That includes the clocks where only the queue holds it: right after the first push, and
  between two rounds.

The suite grows from 67 to 80 checks. The CQ checks pass unchanged on the RTL before the flop, so they
describe behaviour that did not change.

The reviewer's seven occupancy mutants are now arms of `tb/pp_top/notify_mutants.py`, with the
reviewer's own edits. Each is KILLED by its named checks (109 of 109 in the campaign at the head):

| Mutant | Fails |
|---|---|
| a pop beside a push clears the occupancy | CQ1 (the second entry is stranded: 2 jobs of 3) and OC1 |
| `amap_busy_o` drops the occupancy term | CQ1b (2 clocks low) and CQ2b (17 clocks low) |
| a pop clears the occupancy at once | CQ2 (3 jobs of 26) and OC1 |
| a pop keeps it set; a push does not set it; a pop clears it one entry late | OC1, CQ1 and CQ2 (and more) |
| the reset sets it (one arm per run) | OC1 in each of the five runs |

### Receipts (R649-1-F1, R648-1-F-1)

Every round-2 figure in this description has a receipt in the round-2 author receipts. They hold the
gate logs, the OOC and route reports with the exact commands, and the proof, control and mutant logs,
each with the head it ran at, plus an index. The author's round-1 receipts are on
milan-fpga's evidence branch at `d678eaa0`.

The out-of-tree proofs were re-run at `c5afc0a4`:

- **Router equivalence** against main proves every cell at `N_SRC_P` 1, 5, 8, 16 and 29 (91 / 205 / 286 /
  505 / 859). Five planted mutants each leave 2 to 8 cells unproven.
- **Occupancy induction** is proven at three shapes. Six writer mutants fail it. The reader mutant passes
  it, as it must, and the in-tree CQ1b/CQ2b kill it.

### Routed: parent route-1x1 with #760, at the round-2 head

The recipe is unchanged. The scratch parent is milan-fpga dev `7d79ffb2`, with the gitlink at `c5afc0a4`
and #760's change in the working tree only, never committed. Vivado ran under the exclusive lock, and the
route-1x1 resource gate was run on the result.

| Route | WNS | gate | worst path | count to select | occupancy to select |
|---|---:|---|---|---|---|
| base `22c139a4`, with #760 (round 1) | +0.016 ns | fails (below the +0.03 floor) | the cone, 30 levels | 30 levels | - |
| head `16c89c53`, with #760 (round 1) | +0.144 ns | passes | Ethernet receive clock | no path | 24 levels |
| **head `c5afc0a4`, with #760** | **+0.220 ns** | **passes** | inside `u_aecp` (micro-sequencer to `u_d3`), 34 levels | **no path** | 22 levels, +3.510 ns |

With #760 the route closes above the +0.030 ns floor. Its worst path is inside the AECP engine, not
through this cone.

### Out of context, at the round-2 head

| | 1x1 base `08ae0013` | 1x1 head | 8x8 base | 8x8 head |
|---|---:|---:|---:|---:|
| `cmdq_count_r` to `sel_r` | 22 levels | no path | 33 levels | no path |
| `cmdq_nempty_r` to `sel_r` | - | 19 levels | - | 21 levels |
| WNS | -4.819 | -4.819 | -10.720 | -5.844 |

The half after the register is 19 levels at 1x1 and 21 at 8x8 at this head, against 22 at round 1's head;
routed, it is 22. `syn/ooc/README.md` keeps round 1's dated record.

### Gates at the round-2 head

Base is main `08ae0013`, head is `c5afc0a4`. The processor gates and the campaigns returned rc 0 at both:

- processor gates: `scripts/run_suites.sh` (1030000 and 1030013 checks, 0 failing; the 13 are the new
  `tb/aecp_notify` checks), `scripts/lint_hdl.sh`, `make check`, `scripts/gen_matrix.py --check`,
  `syn/yosys/run.sh`, the req-tag execution check (226 and 227 evidence lines) and the Yosys elaboration
  guards. The logs are identical apart from those counts and source or netlist line numbers;
- every campaign that builds a changed file: d3, notify, AECP dispatch, AECP, counters, GSI, name write,
  ACMP, name state and elaboration guards. Every record is identical once line numbers are normalised,
  except the notify campaign's eleven new arms and its golden run's tally;
- the scratch parent's consumer gates. The rc table is identical at base and head. Three rows return rc 1
  at both, as in round 1, and none of them is this change's:
  - the moved gitlink's documented pin;
  - the parent's test-evidence ratchet and its self-test. Three existing processor mutation scripts have
    no disposition in the parent, at dev `7d79ffb2` or at the current dev.

  The ROM digests are identical.
