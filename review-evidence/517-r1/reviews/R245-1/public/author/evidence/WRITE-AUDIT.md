# A178 final-source write audit

Source: `7ab1c8d0ad073fbc1977c455dea89b7b318d4e52`.
Public settled decision: https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5780545051
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5780571502

The command/harness inventory below is retained from A176's factual audit.
A178 independently checked the four selected harnesses, common harness header,
expanded 109-source HDL list, builder write redirection and both image-generator
commands. No additional mutable simulation dependency was found.
The HDL file operations are ACMP, AECP and gPTP ROM reads.
Only sim_nxn performs external writes or invokes generators among the selected
C++ harnesses. The generator flags and existing writes are unchanged.

The public decision is implemented by marking all five sim_nxn commands
exclusive. Their full lifetimes are serialized in legacy relative order;
audited independent commands can fill the second slot. The frame-output
variable overrides this for the whole ordinary set, even when empty.

The inaccurate sim_nxn comment is corrected. `scope-equivalence.json` records
47,519 unchanged C++ executable tokens. The only Makefile changes outside
the ordinary tail are the explicit SIM_JOBS variable and its comment.
Build/gPTP/render recipes, other model harnesses and processor pins are fixed.
Each measured run keeps the actual three tracked-header byte copies and
compares them with the commit before and after running.

| Legacy position | Executable | Harness | Mutable external outputs |
|---|---|---|---|
| 1 | `./obj_dir/Vmilan_dp_sim` | `sim_main.cpp` | stdout/stderr only |
| 2 | `./obj_notify/Vmilan_dp_notify` | `sim_nxn.cpp`, timed | private image directory; shared 1x1 TDM8 generated header |
| 3 | `./obj_nxn/Vmilan_dp_nxn` | `sim_nxn.cpp`, N=4 | private image directory; shared Arty 4x4 generated header; optional counter frame |
| 4 | `./obj_nxndv/Vmilan_dp_nxndv` | `sim_nxn.cpp`, divergent N=4 | private image directory; same shared Arty 4x4 generated header; optional counter frame |
| 5 | `./obj_nxn8/Vmilan_dp_nxn8` | `sim_nxn.cpp`, N=8 | private image directory; shared AX7101 8x8 generated header; optional counter frame |
| 6 | `./obj_nxn4c/Vmilan_dp_nxn4c` | `sim_nxn.cpp`, N=4, four channels | private image directory; same shared Arty 4x4 generated header; optional counter frame |
| 7 | `./obj_nolpf/Vmilan_dp_nolpf` | `sim_main.cpp` | stdout/stderr only |
| 8 | `./obj_prune/Vmilan_dp_prune` | `sim_prune.cpp` | stdout/stderr only |
| 9 | `./obj_ax1x1/Vmilan_dp_ax1x1` | `sim_main.cpp` | stdout/stderr only |
| 10 | `./obj_aclk/Vmilan_dp_aclk` | `sim_aclk.cpp` | stdout/stderr only |

All ten calls take no arguments and run from `tb/verilator/milan_dp`.
The Makefile retains their elaboration parameters and source lists.

The four harnesses' file APIs and their common harness header were searched.
Only sim_nxn writes files or invokes subprocesses. Its private `mkdtemp`
directory contains the builder outputs, image.bin, image.json and generator.log
(`sim_nxn.cpp:353-441`). Success removes that directory; failure retains it.
The frame output path is read through getenv and opened `wb`
(`sim_nxn.cpp:2837-2841`). Presence, including empty, requires serial execution
of the entire ordinary set and preserves the legacy final writer/failure.
The timed notification leg exits after image enumeration, before counter dumps.

The expanded `make -s -C tb/verilator/milan_dp print-srcs` list has 109 HDL
sources. Inspection for `$fopen`, `$fwrite`, `$fdisplay`, `$writemem*`,
`$readmem*` and `$dump*` found only ROM reads in the ACMP listener, AECP uCPU
and gPTP uCPU sources. ROM files are built before the ordinary phase.

