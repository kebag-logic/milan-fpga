https://github.com/Mister-M-alt/FPGA-gPTP/issues/82

Found by the in-house qualification run of 2026-10-18 on the AX7101 (dev e9cbb676, gptp-processor e4869fd0).

**Behaviour.** From boot until a gPTP peer has first appeared, the DUT, alone on its link, publishes grandmaster ID 0 and an AS path with 0 entries. GET_AVB_INFO and GET_AS_PATH both report this. Once a peer has come and gone, the DUT correctly reports itself.

**Required.** IEEE 802.1AS-2020 10.3.13.2.4:
- b) gmPriority is the best of the systemPriorityVector and the ports' vectors, so a PTP Instance with no port vector is its own grandmaster;
- i) pathTrace is then {thisClock}.

So before any peer, the grandmaster is thisClock, and the path is {thisClock}.

**Source.**
- `hdl/top/KL_gptp_engine.sv:783`: the published grandmaster resets to 0.
- `:870`: it is written only by the engine's publication.
- `:969-971`: the path count is forced to 0 while the grandmaster is 0.
- In milan-fpga, `hdl/milan/milan_datapath.sv:1515` consumes it.

**Done when:**
- the engine publishes thisClock as grandmaster and {thisClock} as the path from reset;
- a simulation case covers the boot state with no peer, with a planted mutant;
- the parent's consumer gates pass.

