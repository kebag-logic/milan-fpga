https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/189

Found by the in-house qualification run of 2026-10-18 on the AX7101 (dev e9cbb676, processor 2cbed0a9).

**Behaviour.**
- The talker replaces its Talker Advertise by a Talker Failed in place: one declaration, with no Leave in between.
- After that, GET_STREAM_INFO reports REGISTERING and REGISTERING_FAILED, and the DUT declares Listener Asking Failed.
- But GET_RX_STATE keeps REGISTERING_FAILED at 0 (flags 0x0002).
- With a fresh Talker Failed registration, both commands report it correctly.

**Required.**
- Milan v1.2 5.5.3.5.44, Table 5.39: REGISTERING_FAILED is "1 if registering a Talker Failed attribute". See also Table 5.23.
- IEEE 802.1Q-2018 35.2.6: a declaration-type change is the new declaration alone.

**Source.**
- `hdl/acmp/KL_pp_acmp_listener.sv:1158-1161` latches the Talker-Failed bit only on an EVT_TK_REGISTERED that hits a valid, non-ignored cell. In SETTLED_RSV_OK that event is a don't-care (Milan v1.2 Table 5.30), so the in-place swap's strobe is dropped.
- `:652` and `:694` drive the GET_RX_STATE flag from that bit.

**Done when:**
- GET_RX_STATE's REGISTERING_FAILED follows the registered declaration type on every change, including the in-place swap in both directions, with no state transition added;
- a suite case and a planted mutant cover it;
- the processor's suites and the parent's consumer gates pass.

