[A224] Pin gPTP at donor main e5dcea6e, record the step policy and the media re-base, and add the gmstep leg (#387)

Relates to #387. The RTL half of acceptance 3 waits for #529. Acceptance 4 is the manager's bench step.

## Status

Acceptances 1, 2 and 5 are met. Acceptance 3 is not. The leg that grades it is in this PR, but three decided behaviours need `hdl/milan/milan_datapath.sv`, which #529 holds: the `mr` toggle, the MEDIA_RESET count and the single counted render event. The exact edit, verified on a scratch copy, is recorded on #387. Acceptance 4 is the booted-board handover on the #117 bench, the manager's step after merge.

Correction round 1 (author A224) answers R276-1 F1 to F5 and R277-1 findings 1 to 3, and takes the four suggestions.

## Description

- **Pin** (`6caee191`): `gptp-processor` moves from `c1b61743` to `e5dcea6e`.
  - That commit is donor main, the merge of FPGA-gPTP PR #74, and its tree is identical to the reviewed head `ba926810`.
  - The plane now steps at link-up above 20 us. Once locked, including after a GM change, it slews up to 100 us and steps above that. The whole trim stays inside 200 ppm.
  - `syn/yosys/rom_digests.tsv` gains the new pin's row through `./ooc.sh --record-rom-digests`.
  - The donor links, the pin table and both pin-bearing diagrams follow the gitlink through their generators.
  - No gPTP ROM is tracked here. Every consumer, and the builder for each configuration, regenerates it from the pinned generator.
- **Docs** (`6273e4be`, `44bf0891`, `021b2e07`):
  - `docs/design/TIME_SYNC.md` "Step policy" states the policy once. It now also says who holds the 200 ppm bound: the microcode clamps to it, and `KL_gptp_txret` refuses egress timestamps outside it.
  - `docs/design/GM_LOSS_RECOVERY.md` "Media re-base on a PHC step" sets the decided reaction beside what this tree does. It has the following rows:
    - The grid-aligner row quotes decision part (b) verbatim. Its This-tree column records that the aligner has no PHC or step input, and that under CRF selection a step reaches it only through the CRF-steered grid (#539). Whether the aligner needs its own re-centre is a question with the owner.
    - The packet NCO has its own row, because the decision does not name it.
    - A new row records ruling 5802264260 item 2: a step while an `mr` restart is pending merges into one restart and still counts its MEDIA_RESET. The tree state is "Not yet".
    - The CRF-servo row cites #539.
  - The section lists which rows the gmstep leg grades and which it does not, and where each ungraded row is covered or left open.
- **gmstep leg** (`f0ba7ba1`, `fdd613a1`): `tb/verilator/milan_dp/sim_gmstep.cpp`, run with `make -C tb/verilator/milan_dp gmstep`.
  - The leg drives a 1.5 s grandmaster step while the AAF listener is bound and locked under CRF selection.
  - The counted event must belong to the step:
    - The render re-base is counted within 500 cycles after the plane's step pulse.
    - The first PDU with the new `mr` level leaves within two talker intervals of that pulse.
    - MEDIA_RESET has not moved at a counter read taken between the commit and the step.
  - The render law is graded where `KL_render_setpoint` states it: the fill right after every PDU push equals TARGET_C, 14 events. The fill at accept moves with the start phase, so it is printed and not graded.
  - The licence checks count the silence from the last talker PDU to the end of the window. The leg also requires talker PDUs after `tu` clears.
  - The Stream Input GET_COUNTERS answers must be valid, and FRAMES_RX must advance by the PDUs the listener accepted.
  - An optional feed delay, `GMSTEP_FEED_DELAY`, moves the start phase.
  - The leg is not in the default sweep. At this revision it fails exactly four checks: two counted re-bases (one of them outside the step's window), no `mr` toggle, and no MEDIA_RESET. The pending datapath edit closes all four, giving 48/48 at every one of 42 start phases, with 10/10 negative controls caught at two phases.

## How to reproduce

```sh
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
make -C tb/verilator/milan_dp gmstep VERILATOR_JOBS=8
make -C tb/verilator/milan_dp gmstep GMSTEP_FEED_DELAY=12 VERILATOR_JOBS=8
make -C tb/verilator/gptp_shadow VERILATOR_JOBS=8
make -C tb/verilator/milan_dp gptp gptp-lat VERILATOR_JOBS=8
(cd syn/yosys && ./ooc.sh tcam)
python3 scripts/check_gptp_docs.py && python3 -B scripts/docs_check.py
```

## How to validate

The local gate results are in the #387 REVIEW READY comments of A214 and A224. At this head, `gmstep` reports 48 checks with 4 failures, which are the four named above. The negative-control runner and the edited datapath copy it runs on are in the A224 packet. They join the tree with the datapath edit.

## Definition of done for #387 (not reached by this PR)

- The `milan_datapath.sv` edit, including the failing arm for the pending-restart merge.
- `gmstep` and its negative-control runner wired into the sweep.
- The "Not yet" rows of `GM_LOSS_RECOVERY.md` turned.
- An owner ruling on the grid aligner's re-centre.
- The #117 bench measurement.
