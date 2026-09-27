[A348] State the parent/processor descriptor ownership contract and record the clause-backed #122 disposition.

Closes #125
Closes #122

The memory-map contract now assigns configuration-dependent shipping semantics to the parent and generic packed-image validation to the processor. It distinguishes ownership from implemented checks, records body/directory agreement as enforced at `493e5e4b`, and retains #38, #39, #60, #89 and the parent follow-ups. The AUDIO_UNIT extent and separate shipping, loader and conversion limits are explicit. Integrator §6 requires matching ENTITY/ADP identity, valid model IDs, stream-count maxima and the primary IDENTIFY index.

For #122, the STOP rule applies. Milan v1.2 §5.3.3.8, printed p. 27 (PDF p. 34): “Each Stream Port Input of a Configuration shall contain at least one AUDIO_CLUSTER descriptor.” IEEE 1722.1-2021 §7.2.13, pp. 81–82, Table 7-23 defines number_of_clusters: “The number of clusters within the Port.” Dynamic mapping sets number_of_maps to zero; it does not waive Milan's cluster minimum. F07.2 retains `1..*`. The parent D8 zero-cluster inputs require a parent decision, as [reported on #122](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/122#issuecomment-5853884588). This closes the contract interpretation, not the parent conformance discrepancy.

Validation: all repository documentation gates, link checks, generated-matrix checks and whitespace checks passed (rc 0). Existing body/key checks passed in both input forms. Eight targeted packing observations confirm the remaining L6/L10 semantic gaps. Only two documentation files changed.
