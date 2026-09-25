[A289] Round 2 production-firmware conflict

The unchanged production firmware also names `id` in the diagnostic `printf` between its read and guard, at `sw/firmware/milan_baremetal/milan_baremetal.c:1440-1441`. A strict implementation already refuses the unchanged firmware itself on the assigned rule. This is in addition to the accepted discard-mask fixture reported above.

The narrowest proposed exceptions are the two existing complete expression shapes: that diagnostic call and `(void)(id & 1u);`. Hostile near-miss fixtures would keep wrappers, output operands, other calls and assignments refused. No exception has been added. The decision must authorize those shapes or amend the requirement to preserve the firmware and corpus unchanged.
