================ hunk 1
--- OURS (5 lines)
  - **SRP.** Every source is configured on every interface with its generated TSpec and class, and declares nothing until its destination is valid: MAAP's range held and a probe of the last 15 s or a registered Listener, the MAAP adapter's DA gate, which the composition passes to SRP (#895; Milan v1.2 4.3.3.1). It then declares Talker Advertise at base + n on its own interface, and withdraws when the gate closes ([SRP](../srp/README.md)). The licences reach the fabric through the publication block (`srp_mbx.c`), and the platform records each.
  - **AECP.** `random` is the loop's millisecond clock. Every observation is the face's ([`aecp_face.c`](../aecp/aecp_face.c)), the platform's only `random`.
    GET_AS_PATH reads its AVB interface's GSI window, kind 2: the count, then each ClockIdentity of the path sequence by its ordinal, at most `AECP_PATH_ITEMS`, so it answers SUCCESS with the sequence the datapath serves (IEEE 1722.1-2021 7.4.41; Milan v1.2 5.4.2.24; #897).
    A window that does not answer, or a count past `AECP_PATH_ITEMS`, fails that port, and the core answers as for GET_AVB_INFO's.
    AS_PATH_CHANGED leads to the unsolicited GET_AS_PATH response, which reads the window again (Milan v1.2 Table 5.22).
--- BASE (2 lines)
  - **SRP.** Every interface declares every source, with its generated TSpec and class, unallocated at boot. The licences reach the fabric through the publication block (`srp_mbx.c`), and the platform records each.
  - **AECP.** `random` is the loop's millisecond clock. GET_AS_PATH has no split source at this base and answers unavailable.
--- THEIRS (11 lines)
  - **SRP.** Every interface declares every source, with its generated TSpec and class, unallocated at boot. The licences reach the fabric through the publication block (`srp_mbx.c`), and the platform records each.
  - **AECP.** `random` is the loop's millisecond clock. GET_AS_PATH has no split source at this base and answers unavailable.
  - **The REBOOT's reset port** (#871). `env.reboot` is the split SoC's `ctrl_reboot_req` CSR (`milan_soc.CtrlReboot`), which reaches `KL_reboot_ctrl` through a `MultiReg` ([REBOOT_RESET.md](../../../../docs/design/REBOOT_RESET.md#8-the-split-placement)). With it AECP answers a REBOOT of the ENTITY (IEEE 1722.1-2021 7.4.43); with 0 it answers NOT_IMPLEMENTED.
    The window from the SUCCESS to the port behaves as the processor's (REQ-FWX-001; the processor's `06_aecp_engine.md` section 6.11):
    - From the SUCCESS no received frame of any channel is taken. Every channel's take is behind a gate on `aecp_reboot_accepted`, set at boot with the channel's own binding behind it, so a frame stays in its ring and the mailbox drops whole one that finds no room.
    - Once the SUCCESS and its notifications have left the mailbox (`aecp_reboot_due`), `ctrl_plat_step` no longer services the loop, so no channel starts another transmission.
    - Once every other channel's ring has drained, ADP shuts down, so each advertising interface sends ENTITY_DEPARTING (Milan v1.2 5.6.3.3) and no other frame follows it.
    - Once ADP's ring has drained too, the platform writes 1 to the port.
  
    From the loop's last pass the platform services the saved-state store on its own centisecond and its F_NVM, and, once every other ring has drained, ADP's poll until the port fires. So a journal write in progress completes and the drain sees it, and no frame is taken that could start another write during the PHY hold.
    The sequence has no deadline: a ring the datapath never drains holds the port back, as the processor's MAC holds its request.
--- RESOLVED (14 lines, res lines 80-93)
  - **SRP.** Every source is configured on every interface with its generated TSpec and class, and declares nothing until its destination is valid: MAAP's range held and a probe of the last 15 s or a registered Listener, the MAAP adapter's DA gate, which the composition passes to SRP (#895; Milan v1.2 4.3.3.1). It then declares Talker Advertise at base + n on its own interface, and withdraws when the gate closes ([SRP](../srp/README.md)). The licences reach the fabric through the publication block (`srp_mbx.c`), and the platform records each.
  - **AECP.** `random` is the loop's millisecond clock. Every observation is the face's ([`aecp_face.c`](../aecp/aecp_face.c)), the platform's only `random`.
    GET_AS_PATH reads its AVB interface's GSI window, kind 2: the count, then each ClockIdentity of the path sequence by its ordinal, at most `AECP_PATH_ITEMS`, so it answers SUCCESS with the sequence the datapath serves (IEEE 1722.1-2021 7.4.41; Milan v1.2 5.4.2.24; #897).
    A window that does not answer, or a count past `AECP_PATH_ITEMS`, fails that port, and the core answers as for GET_AVB_INFO's.
    AS_PATH_CHANGED leads to the unsolicited GET_AS_PATH response, which reads the window again (Milan v1.2 Table 5.22).
  - **The REBOOT's reset port** (#871). `env.reboot` is the split SoC's `ctrl_reboot_req` CSR (`milan_soc.CtrlReboot`), which reaches `KL_reboot_ctrl` through a `MultiReg` ([REBOOT_RESET.md](../../../../docs/design/REBOOT_RESET.md#8-the-split-placement)). With it AECP answers a REBOOT of the ENTITY (IEEE 1722.1-2021 7.4.43); with 0 it answers NOT_IMPLEMENTED.
    The window from the SUCCESS to the port behaves as the processor's (REQ-FWX-001; the processor's `06_aecp_engine.md` section 6.11):
    - From the SUCCESS no received frame of any channel is taken. Every channel's take is behind a gate on `aecp_reboot_accepted`, set at boot with the channel's own binding behind it, so a frame stays in its ring and the mailbox drops whole one that finds no room.
    - Once the SUCCESS and its notifications have left the mailbox (`aecp_reboot_due`), `ctrl_plat_step` no longer services the loop, so no channel starts another transmission.
    - Once every other channel's ring has drained, ADP shuts down, so each advertising interface sends ENTITY_DEPARTING (Milan v1.2 5.6.3.3) and no other frame follows it.
    - Once ADP's ring has drained too, the platform writes 1 to the port.
  
    From the loop's last pass the platform services the saved-state store on its own centisecond and its F_NVM, and, once every other ring has drained, ADP's poll until the port fires. So a journal write in progress completes and the drain sees it, and no frame is taken that could start another write during the PHY hold.
    The sequence has no deadline: a ring the datapath never drains holds the port back, as the processor's MAC holds its request.
================ hunk 2
--- OURS (1 lines)
  - `platboot`: the boot and composition at one and two interfaces on the mailbox model, F1's flash model and the host bus (`test_plat_boot.cpp`), every bus access in one order, the flash's among them; a controller's bind after ready, written back to the flash by the store's service on the loop's tick; and GET_AS_PATH answered SUCCESS with the sequence the datapath serves (B11, #897);
--- BASE (1 lines)
  - `platboot`: the boot and composition at one and two interfaces on the mailbox model, F1's flash model and the host bus (`test_plat_boot.cpp`), every bus access in one order, the flash's among them; and a controller's bind after ready, written back to the flash by the store's service on the loop's tick;
--- THEIRS (1 lines)
  - `platboot`: the boot and composition at one and two interfaces on the mailbox model, F1's flash model and the host bus (`test_plat_boot.cpp`), every bus access in one order, the flash's among them; a controller's bind after ready, written back to the flash by the store's service on the loop's tick; and the REBOOT (B11 to B23): its order with rings held or full, each refusal, no port, the reset and the boot after it, a REBOOT during a journal write, nothing taken or sent after the port, a frame on each of the five channels left in its ring from the SUCCESS and while its SUCCESS cannot be handed over, and the MAAP, SRP and AECP frames queued with the REBOOT left in the pass that takes it, no ACMP, AECP, MAAP or SRP transmission after ENTITY_DEPARTING, and the DEPARTING held while the ACMP, MAAP or SRP ring holds a frame. AECP's check after the DEPARTING has no defect of its own, because AECP starts no frame after its SUCCESS; its three layers each carry one: the loop's stop (`plat-reboot-transmits-after-the-departing`), the receive gate (`plat-reboot-takes-aecp-frames-after-the-success`) and AECP's own silence (`reboot-serves-after-its-success`, `reboot-probes-after-its-success`, `reboot-retries-after-its-success`);
--- RESOLVED (1 lines, res lines 131-131)
  - `platboot`: the boot and composition at one and two interfaces on the mailbox model, F1's flash model and the host bus (`test_plat_boot.cpp`), every bus access in one order, the flash's among them; a controller's bind after ready, written back to the flash by the store's service on the loop's tick; GET_AS_PATH answered SUCCESS with the sequence the datapath serves (B24, #897); and the REBOOT (B11 to B23): its order with rings held or full, each refusal, no port, the reset and the boot after it, a REBOOT during a journal write, nothing taken or sent after the port, a frame on each of the five channels left in its ring from the SUCCESS and while its SUCCESS cannot be handed over, and the MAAP, SRP and AECP frames queued with the REBOOT left in the pass that takes it, no ACMP, AECP, MAAP or SRP transmission after ENTITY_DEPARTING, and the DEPARTING held while the ACMP, MAAP or SRP ring holds a frame. AECP's check after the DEPARTING has no defect of its own, because AECP starts no frame after its SUCCESS; its three layers each carry one: the loop's stop (`plat-reboot-transmits-after-the-departing`), the receive gate (`plat-reboot-takes-aecp-frames-after-the-success`) and AECP's own silence (`reboot-serves-after-its-success`, `reboot-probes-after-its-success`, `reboot-retries-after-its-success`);
================ hunk 3
--- OURS (1 lines)
  The control campaign plants [`plat_mutants.py`](../test/plat_mutants.py)'s 42 defects, each caught by a named test on its own words.
--- BASE (1 lines)
  The control campaign plants [`plat_mutants.py`](../test/plat_mutants.py)'s 40 defects, each caught by a named test on its own words.
--- THEIRS (1 lines)
  The control campaign plants [`plat_mutants.py`](../test/plat_mutants.py)'s 62 defects, each caught by a named test on its own words.
--- RESOLVED (1 lines, res lines 135-135)
  The control campaign plants [`plat_mutants.py`](../test/plat_mutants.py)'s 64 defects, each caught by a named test on its own words.
