https://github.com/Mister-M-alt/FPGA-gPTP/issues/84

Found by the in-house qualification run of 2026-10-18 on the AX7101 (dev e9cbb676).

**Behaviour.** While the DUT is the gPTP grandmaster, every talker AVTPDU it sends carries tu = 1. This was seen on all 5,673 frames of its CRF stream in one window. With another station as grandmaster, the same stream carries tu = 0.

**Required.**
- Milan v1.2 4.3.5.2: a Talker sets tu as IEEE 1722-2016 4.4.4.7 describes.
- IEEE 1722-2016 4.4.4.7 and 10.4: tu marks a timing discontinuity and returns to 0 once gPTP time is normal again.
- A grandmaster's own time is the domain's time, so it is stable.

**Source.**
- `hdl/ucode/gen_gptp_ucode.py:1671` (`prog_become`): taking the grandmaster role clears the sync-ok flag.
- In milan-fpga, `hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:211` derives tu from it, through `hdl/milan/milan_datapath.sv:2040`.

**Done when:**
- the grandmaster role counts as synchronised, and tu is 0 while the instance is grandmaster;
- the 0.25 s holdover on a grandmaster change stays (Milan v1.2 Annex B.1.1);
- a simulation case and a planted mutant cover it;
- the parent's consumer gates pass.

