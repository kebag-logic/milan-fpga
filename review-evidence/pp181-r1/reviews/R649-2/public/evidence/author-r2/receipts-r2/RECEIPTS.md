# #181 round-2 author receipts

Host-specific paths are redacted: `<home>`, `<data>`, `<host>`. Text files are at most 200 KB. A larger
or binary file is not copied: `LARGE.tsv` lists its sha256, its size, its place here and its scratch path,
and where it is text an `.excerpt.txt` sits beside it. `sums/RAW-<dir>.sha256` hold each copied file's sha256
before redaction, and `sums/MANIFEST-<dir>.sha256` the bytes as published (one pair per top-level
directory, so each list stays under 200 KB; `MANIFEST-top` covers this index and `LARGE.tsv`).

## Identities

- Processor head `c5afc0a42f200af01dd83e67b579dc3badc42601` (branch `181-notify-router-cut`, not pushed),
  on `42eb9aef` (PR #187): `2cacc920` merges main `08ae0013`, `a0a57895` (comments), `c5afc0a4` (checks).
- Processor base `08ae00130f096f241463172c4781885934400ee4` (main, #183).
- Scratch parent: milan-fpga dev `7d79ffb26308ac51eaeeab6ec43d798d057ae0cd`, its `protocol-processor`
  gitlink staged at the base or the head (never committed or pushed; `pgates/*/gitlink.txt`).
- milan-fpga #760: branch `760-pdelay-hysteresis` at `22840662207171f9148c4445c78e952fe19e4802`, applied
  as `git diff 7d79ffb2 22840662` (sha256 `003e49859d84a36189f0edb0ee629948dc9179cdeccda2d4549c91aeefeedf5b`,
  the round-1 patch) to the scratch parent's working tree for the route only, and reverted after it
  (`chain.txt`).
- Tools: Verilator 5.050 (`2026-07-01 rev v5.050`, the pinned build); sv2v v0.0.12 (sha256
  `b29952bc8f400ca90207507db0ff6763263e03d3eec711da80338430ed636b9b`); Yosys 0.33 (git sha1 `2584903a060`,
  the CI image's; sha256 `88c0a12bb814a1a8716b1ae10b482e35d3005ed558e1f5f626b3dc983ea3abd0`) for the processor
  gates and proofs; the scratch parent's own gates pick the host Yosys 0.66, the same at base and head;
  Python 3.14.8; Vivado 2026.1, every run under the exclusive lock; the parent's pinned RV32 SDK
  (`riscv32-ilp32d--glibc--stable-2025.08-1`, archive sha256 `d42680e9...`, installed into the lane's
  scratch by the parent's own `scripts/ci_rv32_sdk.py` and verified: `scripts/sdk-install.log`).

## Index (and the head each receipt ran at)

| Directory | What | Ran at | Command (driver in `scripts/`) |
|---|---|---|---|
| `logs/head`, `logs/base` | processor gates: `scripts/run_suites.sh` (with `REQ_TAG_LOG`), `check-req-tags.py --suites --evidence`, `lint_hdl.sh`, `make check`, `gen_matrix.py --check`, `syn/yosys/run.sh`, `tb/elab_guards/guards.py --frontend yosys`; `rc.txt` per gate | head in the lane; base in the scratch parent's submodule | `gates.sh <tree> <label>` |
| `camp/camp_compare*.out` | the base/head record comparison, raw and with source/netlist line numbers normalised | - | `camp_compare.py base head`, `camp_compare_lines.py base head` |
| `camp/head`, `camp/base` | every campaign that builds a changed file (`KL_aecp_notify.sv`, `KL_pp_event_router.sv`, `tb/aecp_notify/*`): d3, notify, AECP dispatch, AECP, counters, GSI, name write, ACMP, name state, elaboration guards; each campaign's console log, records and every mutant log (records only: build trees and source copies are not published) | head in the lane; base in a clean `git archive 08ae0013` export | `campaigns.sh <tree> <label>` |
| `pgates/head`, `pgates/base` | the scratch parent's consumer gates, one log and rc each, `summary.txt`, the gitlink, parent status before and after, the ROM digest record | the scratch parent with the gitlink at head / base | `parent_gates.sh <dir>` (each gate through `pgate.sh`) |
| `route-head760` | route-1x1, recipe unchanged: `route.out`, `route-1x1-check.log` (WNS, WHS, the resource gate), the dry run, argv and elaboration logs; Vivado's own log as an excerpt | head + #760 | `chain_parent.sh`, which calls `route.sh r2-head760` |
| `cone/head760` | the cone on the routed checkpoint: count to select, count to occupancy, occupancy to select, the worst paths into `sel_r`, the clock group's top ten | head + #760 | `route_cone.tcl <route.dcp>` (in `chain_parent.sh`) |
| `ooc/head-1x1`, `ooc/head-8x8`, `ooc/base-1x1`, `ooc/base-8x8` | the unchanged complete-processor OOC recipe (`syn/ooc/protocol_processor_ooc.tcl`, 10 ns) and the cone queries, with utilisation and timing reports | head in the lane; base in the export | `chain_ooc.sh`, which calls `ooc_run2.sh <tree> <out> <n_in> <n_out>` and `ooc_cone2.tcl` |
| `proofs` | router equivalence (5 shapes) and its 5 mutants; occupancy induction (3 shapes) and its 7 mutants; mutant diffs in `proofs/mutants/` | sources `git show c5afc0a4:` (head) and `08ae0013:` (the router's gold) | `run_proofs.sh` (`equiv.sh`, `inv.sh`, `make_mutants.py`) |
| `in-tree-checks/occ2` | the eleven new campaign arms' development run (all KILLED, goldens PASS) | the working tree just before `a0a57895` (the same bench and RTL logic as the head; the head campaign repeats them) | `notify_mutants.py --only occupancy_...` |
| `in-tree-checks/basecq` | sections CQ on the RTL before the flop, and with R648-1's B5 and B7 | the head's bench with main `08ae0013`'s `KL_aecp_notify.sv` | `RECIPE.txt` |
| `in-tree-checks/pre`, `first-run` | the first `make check` runs of the new suite, `make check` and `lint_hdl.sh` before the commits | the working tree before `a0a57895` | as named |
| `r648-inputs` | R648-1's published mutant diffs, index and matrix, read from milan-fpga `65f0ab37` | - | - |
| `scripts` | every driver above, exactly as run; `publish.py` produced this directory | - | - |
