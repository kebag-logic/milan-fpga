# R458-2 draft verdict and ledger, written before re-reading prior public review comments

Exact head 9160f7d7f005050887cab942710940b91e34fc65, tree bd926d188f3205a819e9248ed1a07dae14098e7f.
Written after my own independent pass (diff, history, merges, evidence, unchanged round-1 probes,
campaign at the head, own round-2 probes). At this point I had read neither R459-1's report again
(comment 5978360032) nor the manager's response (5978368336), nor any round-2 review. The slope
per-shape re-measure was still running.

Draft verdict: NEGATIVE, on one open MINOR (draft F1 below). No RTL defect; HDL unchanged since 25847d07.

## Round-1 findings, own
- R458-1 F1 (MINOR): RESOLVED. 17/17 round-1 probes are caught by a committed suite when run
  unchanged; the eight survivors are caught by srp_stream_fsms WK1-WK8; tf-full-guard-31 by srp_top TF4.
  Both arms are elaborated at 1/1, 2/2, 3/5, 9/9. The campaign gives 126/126 with coverage 78/78, and its
  33 new controls are killed.
- R458-1 F3 (MINOR): RESOLVED as raised. The PR body and HANDOFF state the counts row by row, and both
  tables match the logs: the round-1 table 16/16 rows against controls-final.log, the round-2 table
  29/29 rows against my campaign.
- R458-1 F2: already resolved in round 1.
- S1 (FIFO full boundary): taken up by the held arm (TF4/TF5).
- O1: outside the diff; still the manager's to file.

## New, draft
- draft F1 MINOR (Tests, Docs). tb/srp_top/README.md:621-622 says "Every control is caught at every
  shape where its arm is elaborated and the edit is not equivalent by construction". This is
  contradicted by its own table: `wsid-flops-of-control-sink` at 1/1 is "0 (equivalent in
  simulation)", and the arm is elaborated there.
  - The same edit's round-1 zero at 1/1 is explained as "(one sink: same index)" (PR body line 211,
    HANDOFF 4.2 row and the bullet "equivalent by construction (one source or one sink)").
  - In fact the latched index reaches the out-of-range value at one context. The round-1 bench drove
    out-of-range indices: the DA edit at one source mismatched 47,564 cycles.
  - The zero is the Verilator 5.050 aliasing of a one-element 64-bit packed array. I reproduced it
    with a small module, and it persists with --x-assign unique. The same blind spot hides a talker
    stream_id read at the gate face at 1/1 (my probe), which is caught at 2/2.
- draft R1 RESIDUE: PR body line 9 "Head `1199255`." (the head is 9160f7d7; line 280 records the merge).
- draft R2 RESIDUE: docs/guides/hdl-engineer.md:88-92 attributes `slope_q_r` to "those SRP arrays'
  walks"; it is the admission walk's.
- Suggestions:
  - randomise unreset memory in the store build too;
  - note the 1/1 stream_id aliasing in tb/srp_stream_fsms/README.

## Judgements asked for
- **The forced state cannot mask a real defect on the paths it judges.**
  - Dropping the force fails TF4/TF5 at every shape, so the forced arm is non-vacuous.
  - Two full-specific selection defects (each FIFO skipped while it holds 32 words) are caught by
    TF4/TF5 at every shape, because the drain from full runs unforced.
  - Its only blind case, a push at full in the same cycle as a pop, is unreachable from the ports and
    pre-existing guard semantics.
- **The TM_SEL encoding workaround fails loudly, never silently.** The encoding swapped in the RTL is
  behaviour-neutral (the srp_top suite passes 2,200/2,200), and it makes the held arm fail at every
  shape.
- **The 1/1 flop-arm coverage claim holds in substance, with one documented simulator limit.**
  - WK1-WK8 check every published value at 1/1.
  - Index faults on DA and VLAN are caught at 1/1.
  - Index faults on the 64-bit stream_id through an out-of-range idle face are invisible to Verilator
    at 1/1 and caught at 2/2, the same elaboration arm.
  - The README's summary sentence overstates this (draft F1).

## Draft ledger
| Lens | State |
|---|---|
| Conformance | CLEAN |
| RTL | CLEAN |
| Robustness | CLEAN |
| Tests | UNCLEAN (draft F1) |
| Docs | UNCLEAN (draft F1) |
