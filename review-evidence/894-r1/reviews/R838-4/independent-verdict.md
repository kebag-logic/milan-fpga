[R838] NEGATIVE - exact head 5b264bf26416108add32d7fe5abca5252ffde2cb

Independent delta pass recorded before reading prior reviewers' reports or findings. Final reconciliation and receipt checks remain to be completed in REPORT.md.

Two documentation findings identified independently:

- Section 13's current built-design table (SPLIT_CONTROL_MEMORY.md:2345) still gives 12.82/72.71/68.62/14.50/125.84 ms. The changed AMAP_LIVE_WRITE input makes the actual values 12.85/72.91/68.80/14.51/126.46. Its current summary at line 2481 also retains R4 12.82. The later progression table is correct. MINOR, Docs; figures cannot use the wording-only exception.
- PR #902's exact documented core command selects eight tests, not the claimed thirteen. The published thirteen-test receipt used a wider selection including static maps, output ownership/partition, boot faults and restored ownership. The reproducible command needs that selection (or an accurate eight-test claim). MINOR, Docs; the executed tests themselves pass.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #894 rulings 6870437042 / 6867990126; aecp_maps.c:139-161,201-225,367-431; aecp_shape.py:19-59; flip-1x1.log | R838-4 independent pass | 5b264bf26416108add32d7fe5abca5252ffde2cb |
| RTL | CLEAN | delta has no RTL; aecp_maps.c direct-index layout and guard; aecp_mbx.h:42-54; generated descriptor shape and unchanged loop | R838-4 independent pass | 5b264bf26416108add32d7fe5abca5252ffde2cb |
| Robustness | CLEAN | aecp_maps.c legality/status ordering and out-of-domain lookup; test_aecp.cpp:2513,2632,2673,2701; map-core.log | R838-4 independent pass | 5b264bf26416108add32d7fe5abca5252ffde2cb |
| Tests | CLEAN | test_aecp.cpp changed enumeration and counting tests; aecp_map_mutants.py six new plants; published item2 receipts; flip-selftest.log | R838-4 independent pass | 5b264bf26416108add32d7fe5abca5252ffde2cb |
| Docs | UNCLEAN | SPLIT_CONTROL_MEMORY.md:2345,2481; PR #902 validation command and expected count; map-core.log | R838-4 independent pass | 5b264bf26416108add32d7fe5abca5252ffde2cb |

The 256-slot floor is an explicitly disclosed layout choice with no growth in the already-256-slot supported images. The reported 8x8 cost increase is restated. It is not a general cache-placement guarantee; #909 and merge-candidate remeasurement remain relevant.
