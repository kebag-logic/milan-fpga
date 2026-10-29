# The final head against the measured legs

- `59038a1d` (the final head) renames the record mover's first register from RING to CFG in the glue and the firmware header; nothing else in the firmware, RTL or harness changed after `39aba024`, the measured legs' head.
- The split image at the final head is byte-identical to the measured legs' at both points: 1x1/1if `f3d8ffed...` (as `M100-A1`), 8x8/2if `8a65058c...` (as `M100-A8`).
- The harness's `backlog` group at 1x1/1if arm A, at the final head with the same profiling variant and `CSB_CPU_HZ=100000000` (`F100-A1`): every probe's ms and the summary are identical to `M100-A1`'s, and the group log is byte-identical but for its command lines (scratch paths).
