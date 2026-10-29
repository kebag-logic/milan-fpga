### S4. The F1 flash and saved-state ports on the target

- **Scope.**
  - `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` on the split SoC's LiteSPI addresses, generated from its `csr.csv` and never hand-written.
  - The state port bound to the real owners: ACMP's binding owner, and AECP's formats, maps and names through `aecp_nvm.c`.
  - A flash region guard: no erase or program outside the journal region that `check_nvm_record_space.py` names. The bitstream and the AEM share the flash.
- **Acceptance.**
  - In the S2 or S3 CPU simulation, on the split CPU and memory, as the owner's decision of 2026-10-29 19:05 on #665 (option (c), issuecomment-6504551000) restates this item:
    - the split writer F1 is not held to D5's 24.5 ms capture bound: F1 holds no owner while it captures, and a change behind its cursor opens its own window (DR2a), so the hold the bound protects does not exist in the split;
    - each F1 step stays bounded by T_svc, under FR_NFR 3.4.1 as amended (20 ms, graded per family);
    - the total capture time has no bound of its own: it is measured and recorded at both points (CPU time and elapsed time). A power loss inside it loses at most the unsaved change, because the previous slot stays valid (the torn-slot boot cases);
    - D5 on the current flash writer is unchanged: the 24.5 ms bound covers the current flash writer's capture only. `check_nvm_capture.py` keeps it, and its 8x8 maximum of 13.863 ms stays gated.
  - Boot with valid, absent, torn and wrong-version slots on the target port.
  - `nvm_cosim` and `nvm_capture_cpu` pass.
  - D3's apply order holds: bindings, then formats, maps, settle and names (`ARCHITECTURE_HW_SW_SPLIT.md:138-143`).
- **Mutants and controls:** an erase outside the region is refused; a reordered apply is caught; a step over T_svc is caught; removing the 24.5 ms check from the current flash writer is caught.
- **Measurements:** the capture's CPU time in cycles and ms and its elapsed time, recorded with no bound; each step's CPU time against T_svc; the stage size against the 224 KB ledger.
- **Depends on:** the S2 harness for the target timing; S3 for the composed boot (the lane can start against S3's branch head).
- **Runs now:** yes, from the day S2's harness exists. Only `sw/firmware/ctrl_nvm/**` and `tb/verilator/`.
