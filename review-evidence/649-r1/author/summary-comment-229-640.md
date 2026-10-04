Draft only. Issue #649 asks for "a short summary comment on #229 and #640"; this lane may post only TAKEN, REVIEW READY
or STOP on #649, so the text below is for the maintainer to post (or not) after review. Same text for both issues.

---

[A527] #649 summary (side project, measurement only; findings page `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md` in the #649 PR, not yet reviewed)

- The shipping 1x1 route at dev `241f9184` (50,767 LUT) splits into the protocol processor 23,904 (47.1 %), the rest of
  `milan_datapath` 18,296 (36.0 %) and the SoC side 8,567 (16.9 %); all 175 blocks are tied to the `route-1x1` record.
  Outside the processor the large blocks are the gPTP plane (5,004) and the CSR block (3,073).
- Each stream per direction costs 3,828 LUT, 2,911 FF and 1.5 BRAM tiles out of context (Vivado, 1x1 to 4x4), two
  thirds of the LUTs in the processor. No shape above 1x1 fits the device.
- Channels per stream and the TDM capture width cost nothing; the TDM render lane is 499 routed LUT.
- The low-function-cost prunes (RX address filter, latency taps, loopback lane, probes) total about 1,200 routed LUT, a
  tenth of the 12,727-LUT NFR-RES-01 gap: the gap is redesign territory, the processor first, then the gPTP plane and
  the CSR block.
- Yosys LUT counts are 2.2 to 2.8 times Vivado's and Yosys does not enforce the RTL's elaboration guards (sv2v turns
  `$error` into `initial $display`); the out-of-context Vivado anchor is within 3.3 % of the route.
- The builder accepts an 8x8 TDM8 configuration (235 writable names) that the saved-state backend refuses (128).
