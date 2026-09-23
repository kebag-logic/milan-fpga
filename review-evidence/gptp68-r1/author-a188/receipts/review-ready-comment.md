[A188] REVIEW READY

Author lane for #68. The branch is committed locally and has not been pushed, and no PR is open.

| Item | Value |
|---|---|
| Branch | `68-step-policy` (lane checkout `$LANES/gptp68-step-policy`) |
| Base (main) | `c1b617435824929a790739ea8585c3fe1a328cc0` |
| Head | `77c34e904eba2446755d13e1bf4763d1652c3ca7`, one commit on base: "Step the PHC only on a first synchronization over one second (#68)" |
| Head tree | `10154fc3f95ccc542a6f5dcd8a58105d302fd1af` |
| Working tree | clean (`git status --porcelain` empty) before and after the gate at the head |
| Lane record | `$REVIEWS/gptp68-a188-packet`: `HANDOFF.md`, `PR-BODY.md` (proposed PR text), `receipts/`, `scripts/` |

**Scope** is as recorded in the DECISION above (https://github.com/Mister-M-alt/FPGA-gPTP/issues/68#issuecomment-5790066720):
- The generator changes only in the SERVO leg: the first-synchronization gate, the one-second threshold (exactly 1 s slews), and the PI input saturated at +-20 us.
- `docs/INTEGRATION.md` records the policy and the pulse semantics, and describes `phc_addend_o` as signed.
- The engine harness adds the four required tests (900 ms slews with no step pulse, 1.1 s steps once, a GM change with a small offset does not step, and the first sync after asCapable) plus the +-1 s boundary, with nine new mutants.

**Gate.** The root gate (`make`: contract, tb, lint, docs) with Verilator 5.050 exited 0 on the working tree before the commit, and 0 again at the head.
- A single invocation in this lane is time-limited, so the gate ran as the Makefile's recipes in order, one invocation each. The engine mutation arm ran as four disjoint slices of its own mutant list.
- Results: ucpu 768/768; parser 268/268; engine 1137/1137 x3 with 23/23 mutants caught; gaskets 81/81 with 4/4 mutants; tsngen 288/288 with 3/3 mutants; bench, lint and docs passed.

**Evidence.**
- Each required test fails when its rule is removed; the per-test matrix is in `PR-BODY.md`.
- The base harness on the new ROM fails exactly the 15 checks that encoded the retired rule.
- A ROM-level differential shows the servo is bit-identical to the base inside +-20 us.

**Changed ROM images.** Only words 651..702 (the SERVO leg) change; real words go from 989 to 993.

| Tracked image | SHA-256 before | SHA-256 after |
|---|---|---|
| `tb/verilator/engine/gptp_ucode.hex` | `dee031848c5410d4f0d819eb3d5b124a8d2d0c95b83ffd465dfbff6b15f5c5d9` | `1e52fb26135da78254b96ab5349e2cf590c334d928a17cdee4cceb159a7ba823` |
| `tb/tsngen/gptp_ucode.hex` | `a5d3f91884943afab62c99fe9bbf0111cde8cffe4b318f0cfe9ba1fab9aeba7d` | `7e64371861e6f54ac824c4adb429ff8308919f371b8ad92336cdbad77a902d5d` |
| `tb/verilator/ucpu/gptp_ucode.hex` | `83f14a7d020d6b3d95d5e0e8e9cb878ac78d0a6aed7812ffac9b2dc39981a939` | `f3d73858d62b484145653ce55df239620fede86be7d1f22a093d234b054f2762` |
| `syn/ooc/work/gptp_ucode.hex` | `83f14a7d020d6b3d95d5e0e8e9cb878ac78d0a6aed7812ffac9b2dc39981a939` | `f3d73858d62b484145653ce55df239620fede86be7d1f22a093d234b054f2762` |

**Not done here, for the reviewers:**
- The parent adoption (kebag-logic/milan-fpga#387), its regenerated ROM digests and its suites were not run.
- A pre-existing neighbour-rate-ratio effect after a forward step is described in `PR-BODY.md` as analysis only, with a follow-up suggested.

Ready for the two independent reviewers.
