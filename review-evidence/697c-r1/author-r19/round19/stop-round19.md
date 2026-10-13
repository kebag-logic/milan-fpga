[A583] STOP

Commit: 95ca54cb9454d967b5534b4c3cc32c4c7e2e6a62 (Round 19, branch `697-consume`, local only)
Parents: 27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c and fetched dev d5858bbee328cf8d2c39a99ec14203f5d0ddd123.

The merge is committed. The sole conflicted file, `sw/firmware/ctrl/test/ctrl_srp_image.py`, retains both sides: M8a's split memory, firmware-owned reset entry, linker and layout option, and the lane's stack sources, legacy-source handling and pin check. Every other dev change is inherited unchanged. No additional implementation change was made. The working tree is clean; nothing was pushed or edited on PR #705.

STOP reason: the required boundary gate exits 2 at `ctrl_configs.held`, naming three unclassified programs introduced into its discovered population by M8a:
- `sw/litex/ctrl_memory.py`
- `sw/litex/milan_soc.py`
- `sw/litex/test_ctrl_memory.py`

Each is refused as neither a known builder nor classified in `PART_OF`, `OUTSIDE` or `SUITES`. This occurs before the boundary controls and final dependency judgement. The last program compiles the firmware reset entry (`test_ctrl_memory.py:540`), so classifying all three as compiling no firmware would be inaccurate. Resolving this needs registry/capture integration beyond the assignment's “No other change” scope. I have preserved the refusal instead of changing that scope. This is a validation/scope STOP; no image mismatch or pin change was found.

Validation completed:
- All 65 linked ELFs equal dev `d5858bbe` by SHA-256 and direct byte comparison: five standalone, 30 flat runtime and 30 split runtime variants, covering every shipped shape, both interface counts and each supported composition. Manifest SHA-256: `96f55deba3b69b224fb838b746f559b3c944b552c694cef3211470d8b11db584` on both sides.
- Image self-test: 33 checks PASS, rc 0.
- All four firmware builder captures: rc 0 (RV32 self-test, control build-only, store build-only, coverage build-only).
- Boundary over those captures: rc 2 in 34.71 s, the refusal above.
- Pin controls on CPython 3.12.3: 106, 0 misbehaved; census and figures clean; four figure controls caught. The stack pin remains `405dc68310a18f669049ffc10cc23eef7300dcff`; lwSRP is unchanged.
- M8a memory test: 0 failures, 44/44 mutants caught, rc 0. Simulation-runner self-test: rc 0.
- CI contract: 2169 items; self-test: 3064 arms; both rc 0.
- Round 18 documentation command list: 54/54 rc 0. The source-list self-test ran with `MAKEFLAGS` unset; the historical failure under `MAKEFLAGS=w` is not declared fixed.

Reproduce the boundary refusal after making the four captures with their own builder commands:

```sh
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$CAP/rv32" -- python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$CAP/control" -- python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --build-only --jobs 4
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$CAP/store" -- python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --build-only --jobs 4
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$CAP/coverage" -- python3 sw/firmware/gtest/fw_coverage.py --build-only --jobs 4
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator \
  --capture "$CAP/rv32" --capture "$CAP/control" --capture "$CAP/store" --capture "$CAP/coverage"
```

Round 19's HANDOFF and prepared PR body record the resolution, all before/after image hashes and sizes, pin-proof continuity, gate receipts, and coverage/mutation tables distinguishing completed checks from NOT RUN. R584-16-RES-1 and RES-2 are applied exactly to the prepared body. The packet is retained for publication.

The full Round 18 bar remains incomplete: coverage measurement, firmware execution/mutation campaigns, both complete boundary sides and the remaining entry-point/hook/configuration and disposable act campaigns were not completed after this refusal. No new coverage percentage, firmware kill count or approval is claimed. No hosted run or PR-head act replica was started because the new head was not pushed.
