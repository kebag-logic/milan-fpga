[A567] STOP at `ed340b9b85258194247334b85e62cf9c23d4d051`.

The two preliminary checks reproduce defects. A successful PROBE_TX_RESPONSE with VLAN `0xA123` settles and returns GET_RX_STATE with `0x0123`, contrary to Milan v1.2 5.3.8.9 and Table 5.38. The settlement output is a 12-bit port (`hdl/acmp/KL_pp_acmp_listener.sv:187`), and its top-level consumer and storage are also 12 bits (`hdl/top/protocol_processor_top.sv:1898`, `:1918`, `:1021`). Correcting that full path crosses the assignment's port and source-scope STOP boundaries.

After a same-talker rebind changes the controller, the guard rejects the originally sent probe's controller, accepts the replacement controller, and changes the retry. This conflicts with Milan v1.2 5.5.3.5.17 step 2, 5.5.3.5.18 step 1, and 5.5.3.5.16 step 1.

The unchanged listener and talker suites pass 3111 and 1342 checks. A separate diagnostic builds successfully and exits 1 with five clause failures. Processor source and expectations remain unchanged; no commit was created. The scratch parent is at the requested base with both adoption patches and the processor gitlink staged at this head. Full acceptance gates, campaigns, parent consumer gates and OOC were not run after STOP. HANDOFF.md and PR-BODY.md are complete in the assigned output directory; acceptance remains unmet.
