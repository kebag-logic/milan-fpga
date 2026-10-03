# R449-3 scripts

Every script derives the packet directory from its own location (or `PACKET_DIR`), and
works on scratch copies under `<packet>/scratch/`; none writes to the review clone.

Setup used for this round (all under `<packet>/scratch/`):

- `bin/verilator`: a two-line shim that execs the pinned Verilator 5.050; `bg.sh` puts
  `scratch/bin` first on PATH, so every suite, campaign and parent gate used it.
- `head-tree`, `gate-tree`, `suites-tree`, `camp-tree`, `pristine`: `git archive` of
  `39298e03`. `r1-tree`: `git archive` of `54f9411` (R448-2's `r1` rows). `trees/head`,
  `trees/r1`: symlinks for `run_census_cases.sh`.
- `r449pk/`: staging for R449-2's scripts, which expect `$PACKET/scripts/` and a real
  `$PACKET/scratch/head-tree`: `scripts` links to `round2/r449-2`, `scratch/head-tree` is a
  copy of the head export.
- `parent/`: milan-fpga `1269cdaf`, submodules at their pins (protocol-processor at
  `39298e03`, gitlink recorded), then c8, p2-p1 and c10 applied (`git apply --check` first).

| Script | Purpose |
|---|---|
| `bg.sh`, `waitfor.sh` | start a job detached with its own log/rc/time files; wait on rc files |
| `round2/r448-2/*`, `round2/r449-2/*` | the round-2 probes, byte-identical to their published copies (`receipts/round2_probe_copies.sha256`) |
| `run_r449_census.sh`, `run_r449_faults.sh` | run R449-2's `census_probe.sh` / `yosys_fault.sh` cases, 4 at a time |
| `census_extra.sh`, `run_census_extra.sh` | new census probes: boxes, escaped name, two attributes, first-top failure, two mutants |
| `parse_site_edges.sh` | 12 edge lines through the head's `parse_site`, under gawk and `gawk --posix` |
| `allv_syntax_row.sh` | the PR body's all.v syntax-fault row at this head |
| `top_netlist_equiv.sh` | sv2v + yosys netlist of `protocol_processor_top`, two revisions, raw and normalised |
| `rom_identity.sh` | every ROM regenerated at f4167536, b6f17f2, c4cb84f, 39298e03 |
| `merge_checks.sh` | merge replay, RTL sides, the top's line multiset, cited lines |
| `lane_b.sh`, `lane_c.sh`, `lane_d.sh`, plus the d3 driver | the processor campaigns |
| `readme_counts.py` | each arm's failing-check count vs its `tb/pp_top/README.md` record |
| `parent_light.sh`, `parent_heavy_a.sh`, `parent_heavy_b.sh` | the parent consumer set (17) and the self-tests |
| `integrity.sh` | the review clone's head, tree, status, index and every blob/mode |
