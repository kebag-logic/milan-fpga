# R458-2 review scripts for milan-fpga #230 / processor PR #154

These scripts are reviewer-owned and disposable. Nothing here is proposed for the repository.

**Inputs.**
- Two `git archive` extractions of the processor: base `c4cb84ff` (`<base_tree>`) and head `9160f7d7` (`<head_tree>`).
- The pinned Verilator 5.050. `VERILATOR` names it, or a wrapper for it. The host's own `verilator` is a different version and must not be first on `PATH`.

| Script | What it does |
|---|---|
| `round1-unchanged/` | R458-1's `lockstep/` directory, byte for byte. Its sha256 equal R458-1's `MANIFEST.sha256`; the execute bits are as in round 1. To rerun: `round1-unchanged/probes.py <base_tree> <head_tree> <work> <verilator-jcap wrapper>`, with `VERILATOR_REAL` set to the pinned tool. |
| `probe_receipt.py <R458-1 probe_results.txt> <work>` | Compares this round's run of the unchanged probes with the round-1 receipt, cell by cell. It also names each probe's failing committed checks, by tag and `[sources/sinks]` shape. |
| `r2_probes.py <head_tree> <work>` | Round-2 probes: the `TM_SEL` encoding swapped in the RTL (behaviour-neutral); the wrap's force dropped; two full-specific selection defects; and the talker flop arm reading the 64-bit stream_id or the 12-bit VLAN at the idle gate face. Each probe runs the committed `make` targets named for it. |
| `slope_shapes.sh <head_tree> <work>` | Runs the four committed slope control patches in the admission suite one shape at a time (N = 1, 2, 3, 5, 8). |
| `check_r1_table.py <controls-final.log> <md>...` | Checks the round-1 lockstep control table, cell by cell and its "Caught at" column, against the author's published log. |
| `check_r2_table.py <campaign dir> <md>...` | Checks the round-2 control table (per-shape failing checks, named checks, "Caught at") against this reviewer's own srp_top campaign receipts. |
| `oor_read.sv`, `oor_main.cpp`, `oor_packed.sv`, `oor_packed_main.cpp` | Small modules that show what Verilator 5.050 returns for an out-of-range read of a one-element array, unpacked and packed, at 64, 48, 32 and 12 bits. |

Receipts are in `../receipts/`. Absolute paths in them are rewritten as `$PACKET`, `$TOOLS` and `$HOME`.
