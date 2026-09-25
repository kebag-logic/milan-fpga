[A244] Section 2 of the integrator guide and diagram 21 now enumerate all 24 overridable parameters of `protocol_processor_top`. This adds the five parameters named in #99 plus `NVM_RS_TMO_CYC_P`, gives each parameter its documented owner, and replaces copied defaults with references to F01.5, F08.1, or the top declaration. RTL and defaults are unchanged.

Diagram 21's SVG master was edited and its PNG regenerated with the documented command and visually inspected. A new inventory check compares the guide table and diagram text with the top's parameter declarations, excludes derived localparams, rejects missing/extra/duplicate entries, and runs in the CI documentation job and `make check`.

Validation: all CI documentation/static gates returned 0, including links, compliance and module matrices, WaveDrom freshness, export staleness, HDL lint, µPC map consistency, NVM README figure verification, and portability/memory-mapping checks. `make check` and 11 inventory probes also pass. The pre-change guide returns 1 and reports exactly the six missing parameters; the current inventory reports `top 24, guide 24, diagram 24, OK`. The PNG matches a fresh export byte for byte.

Closes #99
