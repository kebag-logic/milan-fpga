[A194] REVIEW READY
Commit: 4876423d4cf8e89b820c56f8339f230abefb4827 (tree b2fb9e0516aa4ed9a17cdedfb1ae25460270d408, parent 97aa1ec9). It is committed in the lane and not pushed, by instruction. The push is the manager's.

**Finding answered:** R227-3 MINOR Tests and R228-F6 MINOR Tests, the same finding. The low boundary `key[-1] + 3 >= start` of `_rv32_forget_overlap` had no failing control.

**Changed** (tests only: `sw/builder/test_builder.py`, +20/-7, in the existing literal resolver control set in `test_baremetal_profile_contract`):
- **The stale-probe arm.** A parked `0x80001000` must come back unplaced after:
  - "a byte store at a frame slot's last byte": `sw a5,-20(s0)`, `sb zero,-17(s0)`, `lw a4,-20(s0)`;
  - "a byte store at a static word's last byte": `sw a5,0(a3)`, `sb zero,3(a3)`, `lw a4,0(a3)`.
- **The kept-probe arm**, which pins the boundary from the other side. The parked word must survive:
  - "a byte store one past a frame slot's last byte": `sb zero,-16(s0)`;
  - "a byte store one past a static word's last byte": `sb zero,4(a3)`.
- **Comments and the printed note.** They name the new shape. The counts are computed: 15 stale probes and 5 kept probes.

There is no production, docs, workflow or ratchet change. `BAREMETAL_FIRMWARE.md:494-496` ("the rewrites above, each against a whole-word positive arm") already covers footprint-overlap rewrites. The commit subject is one line with no trailers.

**Validation** (at 4876423d, Python 3.14.7):

| Command | Exit | Result |
|---|---|---|
| `python3 -B -u sw/builder/test_firmware_compiler.py --sdk-destination <pinned SDK, mapped read-only> --audit <file>` | 0 (366 s) | GATE 1b PASS. 217/217, 17/17 and 4/4, 46/46. 0 NOT RUN, 235 compiles. 242 audited invocations with 0 argv tails changed. All 120 census assemblies are `rv32i2p1_m2p0_a2p1_f2p2_d2p2_zicsr2p0_zifencei2p0`. It prints "15 rewrites of a parked word ... while 5 stores ... left exactly theirs" |
| `python3 -B -u sw/builder/test_firmware_compiler.py --absent --audit <file>` | 0 (301 s) | GATE 1b PASS. 182/182, 17/17 and 4/4, 46/46. 1 NOT RUN (the compiled census), 0 compiles |
| `python3 -B -u sw/builder/test_firmware_compiler.py --selftest` | 0 | PASS |

The lane's `git status --short --ignored` is empty after the runs. The SDK tree's path, size, mtime and mode listing hashed the same before and after.

**Mutation evidence.** Each probe ran in a disposable copy of the committed tree. Edits are exact-string, each asserted to apply once. Verdicts are read from the gate's own assertion sentence, or from a stop marker planted right after the stale and kept loops.

| Probe | Edit | Result |
|---|---|---|
| M0 | none | stop marker reached: every literal control passes |
| M1 | `key[-1] + 3 >= start` -> `+ 3 > start` | **KILLED**: "after a byte store at a frame slot's last byte the RV32 resolver still placed the next store ([2147487744])", which is 0x80001000 |
| M1s | M1 with the new frame probe deleted | **KILLED** on "after a byte store at a static word's last byte ...", so each new probe kills alone |
| M1x | M1 with both new stale probes deleted | stop marker reached, which reproduces the reported gap |
| M2 | `+ 3 >= start` -> `+ 4 >= start` (over-forget) | **KILLED** on "after a byte store one past a frame slot's last byte ... [unplaced(None)]" |
| M2s | M2 with the new frame kept probe deleted | **KILLED** on the static kept-probe sentence |
| M1, complete gate 1b, SDK mapped | M1, no stop marker | exit 1, **KILLED** on the M1 sentence |
| M1, complete gate 1b, absent | M1, no stop marker | exit 1, **KILLED** on the M1 sentence |

**Acceptance criteria.** Items 1-5 are unchanged by this commit. It adds controls only, and the gate 1b counts match the previous head.

**Required outcome of R227-3 and R228-F6: met.**
- The `>=` to `>` revert is KILLED in the literal controls and through the complete gate 1b, in both modes.
- The head passes.
- The head's resolver code is unchanged, so its refusal of the reviewers' byte-3 compiled plants is unchanged. I did not re-run those plants, which are reviewer tooling.

**Open risks/questions**
- **Verilator version.** The 46 RTL variants elaborated with the system Verilator 5.052, not the pinned 5.050. No RTL path is touched.
- **Not run, by instruction.** The full banks, act and any hosted job. The commit is not pushed, so no hosted evidence exists for it yet.
- **Optional suggestions not taken.** These are the companion boundary `key[-1] <= start + width - 1` (R228-S8, R227-3-S1 M16) and R227-3-S1 M17. Both remain optional suggestions.
- **Next.** R227 and R228 re-review the head once it is pushed.
