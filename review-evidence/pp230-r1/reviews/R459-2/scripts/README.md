# R459-2 scripts (portable; every path relative to the packet or given by env)

Setup, once: `P=<packet dir>`, `S=$P/scratch`, `CLONE=<clone at 9160f7d7>`;
`ln -s <Verilator 5.050 wrapper> $S/bin/verilator` (checked: `verilator --version`
= "Verilator 5.050 2026-07-01 rev v5.050", wrapper SHA-256 `905795b9...`);
`git -C $CLONE archive 9160f7d7 | tar -x -C $S/head` (pristine head tree; only
read); copy the round-1 packet's `scripts/` (R459-1) to `$S/r1/scripts/`, unchanged.

| Script | What it runs | Receipts |
|---|---|---|
| `bg.sh`, `waitrc.sh` | run a command detached with `.log`/`.rc`; wait on `.rc` files | - |
| (inline) `make -C $S/head/tb/<suite>` | positive SRP suites at the head, default `make` | `receipts/positive/` |
| `run_mutants.sh 7` | committed `tb/srp_top/mutants.py --jobs 7` in a fresh archive | `receipts/mutants/` |
| `summarize_r2.py` | per-shape failing checks of the 29 TF/WK controls vs the PR body | `receipts/mutants/per_shape_vs_body.md` |
| `slope_shapes.sh 3` | the four slope patches, admission suite one shape at a time | `receipts/slope/` |
| `r1_controls_vs_committed.sh 5` | round-1 `make_controls.py` UNCHANGED + the stall probe's defect edit, against the committed suites | `receipts/r1controls/` |
| `summarize_r1controls.py` | tabulates the above | `receipts/r1controls/SUMMARY.md` |
| `tmsel_probes.sh` | the wrap's named TM_SEL encoding against an RTL re-encoding and a hierarchical enum reference | `receipts/tmsel/` |
| `oor/oor.sv`, `oor/oor_main.cpp` | out-of-range read of a one-element packed array (64- and 48-bit) | `receipts/oor_check.txt` |
| `probe_patch_identity.py` | R458-1's published probe edits vs the committed patches | `receipts/r458-1_probe_patch_identity.txt` |
| (inline) `make -C <archive of 9160f7d7 / 1199255>/tb/aecp_notify` | the notify suite's last tally at the exact head and at the lane's head | `receipts/notify/` |

Every `.log` was redacted after the run: `<PACKET>`, `<CLONE>`, `<HOME>`, `<USER>`,
`<HOST>`, `<VERILATOR_IMAGE>`, `<VERILATOR_WRAPPER_DIR>`, `<TMP>`. The scripts' path
defaults were made portable after the run (`P` from the script's location, `CLONE`
required), and `run_mutants.sh` now creates its head archive when missing (done by hand in the run); no other line changed.
