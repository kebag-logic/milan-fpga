[A313] Make SRP and boot declarations describe the implemented behavior.

Closes #400
Closes #403

Every SRP declaration now identifies its live consumer, fixed-profile validation or legacy scratch role. Unsupported timer, VID and TSpec values refuse with a reason. The generated startup VID reaches the processor through the parent wrapper, while documented runtime diagnostics and Domain adoption remain available.

Every declared Stream Output, including CRF, receives the required 2 ms factory presentation offset. Legal runtime offsets affect only their addressed output and reach both readback and transmitted timestamps. The configuration explicitly names the existing promiscuous receive posture. AAF and MAAP reset disabled; generated firmware policy supplies their active values and allocates exactly the declared outputs.

The bundle incorporates dev 864b36f5, retains its processor revision 990f9652 and ROM digests, and regenerates the submodule diagrams. Validation also corrected two stale test fixtures and documented the existing listener-offset refusal, with additional negative cases. Actual saved-state restoration remains assigned to #70 under the 2026-09-23 owner decision.

Validation passed: both complete builder modes with all-config elaboration, 26 declaration refusals and binding/header mutations, the 20-case CSR reset matrix, protocol-wrapper VID/adoption/RX/allocation checks, every entry in the default datapath sweep, 344 behavior scenarios, and the requested documentation and source gates. The historical placed-utilization calibration report was unavailable. Area comparisons for all three changed RTL modules show zero delta at the measured default shape.
