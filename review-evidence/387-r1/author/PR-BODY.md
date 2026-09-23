[A214] Pin gPTP at donor main e5dcea6e, record the step policy and the media re-base, and add the gmstep leg (#387)

Part of #387.

## Status

Acceptances 1, 2 and 5 are met. Acceptance 3 is not: the leg that grades it is here, but the decided `mr` and MEDIA_RESET reaction and the single counted render event need `hdl/milan/milan_datapath.sv`, which #529 holds. The exact edit, verified on a scratch copy, is recorded on #387. Acceptance 4 (the booted-board handover on the #117 bench) is the manager's step after merge.

## Description

- **Pin** (`6caee191`): `gptp-processor` `c1b61743` -> `e5dcea6e` (donor main, the merge of FPGA-gPTP PR #74; tree identical to the reviewed head `ba926810`). The plane now steps at link-up above 20 us and, once locked (including after a GM change), slews up to 100 us and steps above it, with the whole trim inside 200 ppm. `syn/yosys/rom_digests.tsv` gains the new pin's row through `./ooc.sh --record-rom-digests`; donor links, the pin table and both pin-bearing diagrams follow the gitlink through their generators. No gPTP ROM is tracked in this repository: every consumer, and the builder per configuration, regenerates it from the pinned generator.
- **Docs** (`6273e4be`, `44bf0891`): `docs/design/TIME_SYNC.md` "Step policy" states the policy once; `docs/design/GM_LOSS_RECOVERY.md` "Media re-base on a PHC step" states the decided reaction beside what this tree does, as measured.
- **gmstep leg** (`f0ba7ba1`): `tb/verilator/milan_dp/sim_gmstep.cpp`, `make -C tb/verilator/milan_dp gmstep`. A 1.5 s grandmaster step while the AAF listener is bound and locked under CRF selection. It is not in the default sweep: at this revision it fails exactly three checks (two counted re-bases instead of one, no `mr` toggle, no MEDIA_RESET), which the pending datapath edit closes (40/40 with it, 7/7 negative controls caught).

## How to reproduce

```sh
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
make -C tb/verilator/milan_dp gmstep VERILATOR_JOBS=8
make -C tb/verilator/gptp_shadow VERILATOR_JOBS=8
make -C tb/verilator/milan_dp gptp gptp-lat VERILATOR_JOBS=8
(cd syn/yosys && ./ooc.sh tcam)
python3 scripts/check_gptp_docs.py && python3 -B scripts/docs_check.py
```

## How to validate

The local gate results are in the #387 REVIEW READY comment. `gmstep` reports 37/40 at this head, and the three failures are the ones named above.

## Definition of done for #387 (not reached by this PR)

The `milan_datapath.sv` edit, `gmstep` and its negative-control runner wired into the sweep, the "Not yet" rows of `GM_LOSS_RECOVERY.md` turned, and the #117 bench measurement.
