# #181 author receipts (published 2026-10-18 for R649-1-F1)

Host-specific paths are redacted: `<home>`, `<data>`, `<slots>`, `<host>`.

**What these receipts cover.**
- Every receipt here was produced at the AUTHOR head `16c89c53` on processor main `22c139a4`, or at its RTL-equivalent predecessors as `HANDOFF.md` lists them.
- The composed source head `42eb9aef` (the manager's clean merge of main `77cf6fb4`) has no receipt here. The manager's donor bank and the next pin adoption's candidate bank and route measure it.

**Index:**
- `logs/`: processor gate logs at base and head (suites, lint, `make check`, the matrix, yosys).
- `prec/`: the precision-proof inputs and results.
- `equiv/`: the equivalence runs.
- `cone/`, `ooc/`: the out-of-context synthesis queries and reports. The recipe `syn/ooc/protocol_processor_ooc.tcl` is unchanged, with a 10 ns clock.
- `route-base760/`, `route-h0/`, `route-h760/`, `route-head/`, `route-head760/`: the routed 1x1 runs, each with `route.out`, `route-1x1-check.log` (WNS, WHS, the resource gate) and `work.tar.xz` (argv, dry run, elaboration).
  - `760` means the scratch parent carries milan-fpga #760's branch `760-pdelay-hysteresis` at `22840662`.
  - `base` is processor `22c139a4` and `head` is `16c89c53`.
- `rom/`: the ROM records.
- `camp/`: the campaign records, including every planted-mutant log and its failing words.
- The `*.sh`, `*.tcl` and `*.py` files at the top level: the exact drivers used.
