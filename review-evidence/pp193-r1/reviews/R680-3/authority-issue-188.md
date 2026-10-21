https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/188

Found by the in-house qualification run of 2026-10-18 on the AX7101 (dev e9cbb676, processor 2cbed0a9).

**Behaviour.**
- A bound sink can settle again before its Listener applicant has sent the pending Leave. Two cases trigger it: a rebind to another source, and the re-probe after the talker's registration ends.
- In that case the DUT never sends the Leave. The old Listener declaration stays registered at the bridge until a LeaveAll plus LeaveTime ages it out, which takes 5-20 s.
- On UNBIND, or when the re-probe comes later than the next transmit opportunity, the Leave does go out.

**Required.**
- IEEE 802.1Q-2018 10.7.7 and Table 10-3: Lv! takes the Applicant from AA/QA to LA, and LA sends the Leave at the next tx!. There is one Applicant instance per attribute value, so a new declaration for another value does not cancel the pending Leave of the old one.
- Milan v1.2 5.5.3.5 (the listener state machine's "clear the SRP parameters and stop SRP" actions).

**Source.** `hdl/srp/KL_srp_listener_fsm.sv:629` abandons the wind-down (`app_r[ctl_sink_i] <= A_VO_C`), and `:626` overwrites the stream ID. The banner at `:67-71` documents this as a deliberate trade-off.

**Done when:**
- the Leave for the old Listener declaration is sent at the next transmit opportunity even when the sink settles to a new source first;
- suite cases cover the rebind and the re-probe, each with a planted mutant;
- the processor's suites and the parent's consumer gates pass.

