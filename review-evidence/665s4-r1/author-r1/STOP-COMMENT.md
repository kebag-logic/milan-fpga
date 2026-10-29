[A698] STOP

Head: `9c2f12a80494b9ee95441ca7f9c606ee6cfe617f` on `665-s4-f1-target` (local branch `s4-f1-target`), from `dev-soft-core` `f4c9ad4f`. Nothing is pushed. The PR body is ready.

**On the split CPU, the capture misses its 24.5 ms bound at both points. So the first acceptance item is not met, and a decision is needed.**

Measured on the S2 harness's test SoC: the shipping VexiiRiscv at 50 MHz, with the split's 4 KiB instruction cache. Every record of the shape is dirty, and each record is latched from its real owner.

| Point | Capture, CPU cycles | ms | Fixed cost per step, cycles | Cost per payload byte, cycles |
|---|---:|---:|---:|---:|
| 1x1 | 1,361,143 | 27.22 | 11,062 | 263.7 |
| 8x8 | 5,161,328 | 103.23 | 16,500 | 205.5 |

- F1 latches one record per service step (`ctrl_nvm/README.md`, "Write-back"). Every step first pays the flash port's 64-bit clock conversion: an idle step costs 9,389 to 9,486 cycles.
- At 8x8 the payload bytes alone cost 48.9 ms, twice the bound even with no fixed cost. The shipping writer's capture, the one the bound was set for, copies 13,210 B in 13.86 ms, about 52 cycles per byte.
- Every step is within T_svc = 10 ms at both points. The longest at 8x8 is 2.64 ms, a 576-byte map record. The capture's elapsed time is paced at one record per 10 ms tick: 0.53 s at 1x1 and 1.64 s at 8x8, from the first capture step to the last.

Everything else in the scope is done and passes at both points:

- The flash port compiles against the split SoC's own LiteSPI, `timer0` and flash window, generated from its `csr.csv` (`gen_flash_port.py`).
- The S2 harness places those devices where the split SoC does. It refuses any other placement.
- Boot works with valid, absent, torn and wrong-version slots. AECP and ACMP answer the restored name and binding from the real owners.
- D3's apply order is the container's. The two planted reorders are caught.
- The guard refuses every program or erase outside the journal on the target. With the guard planted away, the flash model catches the escaped write.

Gates, all rc 0:

- At the head, 99 gates: the docs workflow's, the idiom and evidence gates, `firmware-boundary` in both modes, behave (406 scenarios), and the generator, target and harness self-tests.
- At `19d79844`, which differs from the head only by two docstrings and four line wraps:
  - the builder bank;
  - the store gate: 435 tests, 109 of 109 defects;
  - the firmware campaigns: 1,006 plants caught, none escaped;
  - coverage at 100 %;
  - `nvm_cosim`: 39 of 39 mutants;
  - the census.
- The S2 harness at both points: 0 refusals.
- `nvm_capture_cpu` at 8x8: at most 13.863 ms, with both controls caught.

The full evidence is in the PR body.

Decision needed, for the owner and the manager:

- **(a)** Rule that F1's capture is not held to 24.5 ms. That bound is half the shipping writer's hold floor. F1 holds no owner during its capture, and a change behind its cursor opens its own window (DR2a). Each step stays held to T_svc, which the cases grade. The owner would also rule whether the capture's elapsed time needs a bound of its own.
- **(b)** Make the capture fit. A new lane would change F1's write path to latch several records per step, still within T_svc, with a word-wide compare and copy and a cheaper crc16. It would also take the 64-bit divide out of the port's clock, which S2b's branch already replaces. By the decomposition, the cost per byte must fall by more than half even if the fixed cost reaches zero.
- **(c)** Keep the bound for D5 on the shipping writer only, as `check_nvm_capture.py` holds it today, and apply (a) to F1.
- **Recommend (a)**, with the owner's ruling on the elapsed time. (b) changes F1's per-step contract, its asserted step bound and its host suite, to meet a bound whose reason, the hold, does not exist in the split.

Shared files: the S2 harness's `build.py`, `split_soc.py`, `selftest.py` and README, `ctrl_srp_image.py` and `ctrl_configs.py`. S2b also edits these. This lane alone edits the harness's `sim_main.cpp` and `grade.py`.
