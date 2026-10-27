[A685] REVIEW READY
Commit: `2a7b0df53951cf00695b177b26c660ebe49a0f1a` (branch `665-s2c-icache`, five commits on S2's round 3 `f8876638`, PR #792; base `dev-soft-core` `e76a755a`; not pushed). The lane started on S2's round 2 `cd3525c3` and was re-based onto round 3 when it landed, as the brief directs.

Changed:
- `sw/litex/milan_soc.py`: the split CPU (`--ctrl-mailbox` only) gains the pinned VexiiRiscv's own fetch L1, `--fetch-l1 --fetch-l1-sets=64 --fetch-l1-ways=1` (`CTRL_FETCH_L1`, `ctrl_cpu_args`). 4 KiB, direct-mapped, 64-byte lines, one refill at a time, no prefetch, **no data cache**: with the DMA port an LSU L1 makes the generator build its coherent interconnect and hub instead of patch 0005's non-coherent fabric, and the measured data-side cost is mostly byte-loop stores, which S2b removes first.
- `sw/builder/test_soc_options.py`: the all-fabric CPU must keep exactly its arguments and the split CPU add exactly the cache; three planted defects killed.
- S2's harness: `--fetch-l1 split|none|SETSxWAYS`, the fetch observers on the cache's refill bus (line read off the netlist), reuse bound to the cache and arm, and a labelled hybrid-XIP arm (`--xip`). Five self-test checks and five mutants. README section "The instruction cache".
- `docs/design/SPLIT_CONTROL_MEMORY.md` section 7 (parameters, reasons, decode, block RAM, the requirement conflict) and the `MARK_II_AREA_PLAN.md` ledger (+1.5 tiles).

**Measured** (S2's harness at round 3, arm A; 1x1 one interface / 8x8 two):

| | none (S2) | 2 KiB | **4 KiB (split)** | 8 KiB | 8 KiB 2-way | 16 KiB |
|---|---:|---:|---:|---:|---:|---:|
| Tiles, out of context | 4.5 | 5.5 | **6.0** | 7.0 | 7.5 | 9.0 |
| Composed maximum, ms | 14.81 / 27.84 | 8.99 / 14.58 | **8.60 / 14.03** | 8.40 / 13.76 | 8.19 / 13.63 | 8.17 / 13.53 |
| Paths missing T_svc | 22 of 81 / 60 of 129 | 16 / 37 | **13 / 34** | 13 / 31 | 12 / 29 | 12 / 29 |

- With 4 KiB: CPI 9.5 -> 5.8 / 5.7; worst pass 31.32 -> 19.32 ms / 59.79 -> 37.89 ms; backlog rows shorter by a quarter to two thirds (only the 1x1 event row fits); fan-out at registration capacity fits at 1x1 (SET_NAME 11.33 -> 6.45 ms), misses at 8x8 (10.0 to 13.6 ms). Arms B and SHUTDOWN, and the three controls (caught), are in the README.
- Cost on the product split CPU, out of context: +1 RAMB36 +1 RAMB18 (1.5 tiles), -9 LUT, +173 FF; routed at 20 / 10 ns, WNS +0.607 ns, WHS +0.003 ns. Outside the 56-tile firmware allocation; the ledger goes 114 -> 115.5 tiles (117.5 at 56 firmware tiles) of 121.5.
- **The cache alone does not close T_svc** at either point. The residual is the data side's: `memset`/`memcpy` 40 to 42 % of the composed maximum, the mailbox driver 12 to 21 %, AECP/ACMP/`mrp_mad` 15 to 21 %, software arithmetic 7 %; loads and stores wait 39 to 40 % of the cycles. For S2b: word-wide copies, zeroing only what is sent, the retry backoff, the per-pass cap. For the owner: the M extension, a data cache, the clock.
- **Hybrid XIP:** code in flash costs 2,100 to 2,160 cycles a refill. Behind 4 KiB, 71 of 78 / 111 of 125 paths miss; behind 32 KiB (13 tiles), 19 of 81 / 50 of 129, composed maxima 23.42 / 30.99 ms. No path inside T_svc holds from flash; moving the code would free 20.5 / 21 tiles, planned. F1's flash driver must stay in block RAM: in flash it stalled behind the command master's chip select and trapped (cause 2).
- **#791:** the decode is identical with and without the cache (as-built, harness cover and product split export); the `as-built` control faults at the same call with the cache. Unchanged, stays #791's.

Validation (all at the head unless named; receipts and the gate table are with the manager's handoff):
- `run.py --self-test`: rc 0, 86 checks, 57 of 57 mutants. `test_soc_options.py`: rc 0, `RESULT: PASS`.
- `test_builder.py --require-rv32` (`7e1124be`, nothing it reads changed after): rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11, the local Arty build report).
- `cd tests && behave`: rc 0, 406 scenarios.
- Docs gates, the workflow's 69 commands: 68 rc 0; `check_baremetal_only.py --check` rc 1 on S2's `scenario.py:805` (below).
- Python and C++ idiom with self-tests, hygiene, TODO ownership, SoC and RTL source lists, `git diff --check`: rc 0.
- All-fabric export, five shipped configs, base `e76a755a` against `f3c71e42`: normalised digest identical per config; the all-fabric CPU netlist is `VexiiRiscvLitex_f5f08b17` at both. The split export differs only in the CPU netlist name.
- Four-shard Verilator sweep (`f3c71e42`; only the harness README changed after): rc 0 per shard, 64 of 64 suites, 2,190,531 checks, 0 failures; `tsn_fuzz` declares its field campaigns skipped (tsn-gen absent). Shard 2 ran in the lane's unit with the hosted runners' `MAKEFLAGS=-j1 VERILATOR_JOBS=4` after its shard unit was OOM-killed at 10 GB building `capture_coherence`.
- The cacheless arms reproduce S2's round-2 and round-3 A1/A8 tables byte for byte. Every arm was regraded at the head: every table byte-identical.
- Vivado out of context (under the host lock) on 11 CPU netlists, Yosys on the same 11: rc 0 each.

Acceptance criteria: items 1, 2, 3 and 5 met; item 4 met as a residual: the cache does not close T_svc. The PR body says "Relates to #665".

Open risks/questions:
- **Requirement conflict, for the owner:** `FR_NFR.md` NFR-SCOUT-01 requires "one cacheless RV32I control hart" (repeated in `ARCHITECTURE_HW_SW_SPLIT.md`). The owner's decision gives the split hart an instruction cache. The text is not edited here; it needs the owner's amendment.
- **Inherited:** `check_baremetal_only.py --check` fails on S2's `scenario.py:805` comment ("the TX ring filled"), added at `cd3525c3`, present at `f8876638`; S2's file, left for its next round.
- In arm A's ACMP groups the AECP retry makes some one-phase samples longer with the cache (seven 8x8 inputs span two shorter passes); their pass bounds and arm B show the cache's effect.
- No integrated route, hardware or bench evidence.
