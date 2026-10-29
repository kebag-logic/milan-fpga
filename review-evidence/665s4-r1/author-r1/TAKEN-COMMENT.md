[A698] TAKEN

Branch: `665-s4-f1-target` (local worktree branch `s4-f1-target`), from `dev-soft-core` `f4c9ad4f`. The PR will target `dev-soft-core`.

Authoritative references: [A10] issuecomment-6493622258 (S4); the plan's section S4; `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 2 (steps 6-8 and the D3 apply order); `sw/firmware/ctrl_nvm/README.md` ("The flash port", "Boot", "Write-back"); `docs/design/SPLIT_CONTROL_MEMORY.md` sections 4 and 5; `sw/litex/milan_soc.py` `FLASHBOOT_RESERVED`; `scripts/check_nvm_record_space.py` check 5; `tb/verilator/nvm_capture_cpu/README.md` (the 24.5 ms bound); the S2 harness `tb/verilator/ctrl_service_budget/`.

Interpreted scope:
- The LiteSPI command master, `timer0` and the flash window that `nvm_flash_litespi.c` compiles against are generated from the split SoC's own `csr.csv` (`milan_soc.py --ctrl-mailbox --ctrl-firmware`), never hand-written. `csr.csv` carries no field offsets, so those come from the same export's LiteX `csr.h`, and every address is cross-checked between the two.
- The S2 harness places the flash and `timer0` at those addresses, with the split SoC's LiteSPI bank layout. It refuses a build whose own `csr.csv` differs on any register the port uses. The mailbox address stays the fixture's; that is S3's.
- The state port stays bound to the owners the image already composes: `acmp_nvm` for bindings, over `aecp_nvm` for formats, maps and names. On the target CPU, boot is proven with valid, absent, torn and wrong-version slots, graded by the restored values in AECP and ACMP answers. D3's order (bindings, then formats, maps, settle and names) is checked from the owners' entry order.
- The guard: program and erase stay inside the journal. Its bounds are `FLASHBOOT_RESERVED`'s journal, which the SoC publishes in `csr.csv`; they are checked against `check_nvm_record_space.py`'s slot geometry (one 64 KiB erase block per slot) and against every image slot.
- Assumption, for review: "the capture" is the store's capture phase for a full 8x8 work set, every record dirty. Its CPU time is summed over the capture's service calls and graded against 24.5 ms. Each step's CPU time is graded against T_svc = 10 ms. The elapsed time, paced at one record per tick, is reported but not graded.

Validation plan:
- the generator's self-test, with planted `csr.csv` defects;
- `test_ctrl_nvm.py --require-rv32 --self-test`, `test_ctrl_firmware.py --require-rv32 --self-test`, `fw_coverage.py --check` and every firmware mutant driver;
- the S2 harness's self-test and both points;
- the target cases at 1x1 and 8x8, each with planted controls: an erase outside the region, a reordered apply, and a capture slower by one page past its bound;
- `nvm_cosim`, `nvm_capture_cpu`, `test_builder.py --require-rv32`, the docs gates and `cd tests && behave`.

Shared files, to be listed at hand-off: the S2 harness (`build.py`, `split_soc.py`, `sim_main.cpp`, README), which S2b also edits, and `ctrl_srp_image.py`.

Blockers: none.
