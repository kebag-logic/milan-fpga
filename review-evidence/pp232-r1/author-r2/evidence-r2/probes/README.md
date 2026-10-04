# #232 area lane: the reviewers' probes at the round-2 head (item 1)

"Every reviewer probe, run unchanged, must be caught by a committed test." Each R452-1 and
R453-1 control was planted on head `2ea3dee`'s `hdl/aecp/KL_aecp_notify.sv` (`head-file.sha256`) by the
reviewer's own script, and run through the committed suites by the reviewer's own probe
script. The scripts come from the parent's `pp232-review-evidence` branch at `4e438b23`,
unchanged:

- R452-1: `scripts/lockstep/plant.py` (10 controls), then `scripts/clear_cycle_probe.sh
  $LANE 2ea3dee... $PROBES/r452-controls $PROBES/r452-work <control>`. It runs
  `tb/aecp_notify` and `tb/pp_top` (`make`, every build and section) on a `git archive`
  of the commit.
- R453-1: `scripts/lockstep/make_controls.py` (12 controls), then `scripts/probe_committed.sh
  <archive tree> <control>.sv $PROBES/r453-work/<control> aecp_notify pp_top`.

Both planting scripts found each of their snippets exactly once at this head. Seven of
R453-1's planted files are byte-equal to R452-1's (`own_vs_new_row` equals
`own_compare_new_row`). All 22 were run, three at a time (`one.sh`), with the pinned
Verilator 5.050.

**Result: 22 of 22 controls fail a named committed check** (`table.md`). Each one fails
`tb/aecp_notify`. `tb/pp_top` also fails for the four that break every match after a
REGISTER (`no_set`, `register_not_reindexed`, `index_wrong_row`, `key_swapped`: U10a and
others). The three review faults: `override_set_only` fails IX6 and IX6b,
`own_compare_new_row` / `own_vs_new_row` fails IX5, and `stamp_without_valid` /
`stamp_read_without_valid` fails TS3.

The reviewer scripts read only the canonical tally line. `tb/aecp_notify`'s Makefile
prints that line after both of its builds, and make stops at the first build that exits
non-zero. So their printed lines (`printed/`) say "rc=2 no tally" for a failing control.
`aecp_notify/` holds each run's whole log, with its FAIL lines and the build's
`[build default] 26 checks, N failures`. `pp_top/` holds each `tb/pp_top` log's FAIL and
tally lines, and `controls/` each planted edit as a diff against the head file.
`sources.sha256` gives the full sha256 of every raw log. In the published copies,
`$HOME`, `$SCRATCH`, `$LANE`, `$PROBES` and `$PINNED_VERILATOR` stand for local
directories.
