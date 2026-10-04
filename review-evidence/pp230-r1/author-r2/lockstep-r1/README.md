# [A523] round-1 lockstep bench and planted controls (milan-fpga #230)

The bench behind round 1's equivalence claim (HANDOFF sections 4.1 and 4.2), published for round 2 (assignment
5978448959, item 1, "Packet"). The files are the ones that ran, byte for byte; `MANIFEST.sha256` lists every file.
Round 1's HANDOFF section 10 gives the first 16 hex digits of the same files.

| File | Role |
|---|---|
| `make_ref.py` | rebuilds the reference RTL `ref/*.sv` from base `c4cb84ff`'s `hdl/srp` (`git archive c4cb84ff`): every module name renamed `<name>_ref`. Written for this packet; it reproduces round 1's `ref/` byte for byte |
| `gen_top.py` | writes `lockstep_top.sv`: `KL_srp_top_ref` and the `KL_srp_top` under test on the same inputs every cycle; all 51 outputs (`diff_o`) and 56 internal signals (`idiff_o`) compared every cycle after the first reset |
| `lockstep_main.cpp` | the environment: MRPDUs from shared value pools (plus noisy and truncated ones), the class-B port with every op, a timer-service model (with spurious expiries), a PRNG model, a TX-slot pool, mid-run resets |
| `build.sh` | one shape: `build.sh <hdl/srp under test> <out> <sources> <sinks> <SLOT_AW_P> <JOIN> <PERIODIC> <LEAVE>`; Verilator 5.050 with `--x-initial unique --x-assign unique` |
| `campaign.sh` | the round-1 campaign: shapes 2/2, 9/9, 1/1, 3/5, 8/8 with compressed cadences and 2/2 with the default ones, 8 runs each |
| `campaign-final.log`, `.rc` | its record at the RTL commit `25847d07`: 48 runs x 1,000,000 cycles, 0 mismatching cycles (top and internal) |
| `make_controls.py` | the sixteen planted controls, one exact edit each |
| `run_controls.sh` | each control at 2/2, 9/9, 3/5 and 1/1, 6 runs x 300,000 cycles |
| `controls-final.log`, `.rc` | its record: the mismatching cycles per control and shape (HANDOFF section 4.2) |

Paths. The scripts name the lane's scratch directory and the pinned simulator: `build.sh` reads the base tree from
`<scratch>/basetree/hdl` (for `pp_pkg.sv` and `srp_pkg.sv`) and the bench from `<scratch>/lockstep`, with `ref/` beside
it. To rerun elsewhere, set `L` (the bench) at the top of `build.sh`, `run_controls.sh` and `campaign.sh` and `B` (the
base tree's `hdl`) in `build.sh`, extract
`git archive c4cb84ff` as the base tree, run `make_ref.py <base>/hdl/srp <bench>/ref`, and point `build.sh`'s first
argument at the `hdl/srp` under test (`git archive 25847d07`, or any later processor commit; the RTL has not changed
since).

What replaced it in the repository. Round 2 commits the coverage instead of the bench (the assignment preferred
directed arms to a frozen copy of the base RTL): `tb/srp_stream_fsms` WK1-WK8 and `tb/srp_top` TF1-TF5 at
sources/sinks 1/1, 2/2, 3/5 and 9/9, and these sixteen controls, with both reviews' probes, as killed controls of
`tb/srp_top/mutants.py` (HANDOFF "Round 2").
