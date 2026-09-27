State the parent/processor descriptor ownership contract and record the clause-backed #122 disposition.

Closes #125
Closes #122

Parent shipping checks are authoritative for all generated model content, covering every L1–L10 semantic obligation and ADP stream-count maxima. Processor semantic checks, including coverage retained or added under #60, provide defence in depth. Generic packed-image checks remain authoritative for image acceptance, including L2 index density; parent checks own L2 multi-level ordering.

The contract distinguishes ownership from implemented enforcement, records descriptor body/directory agreement as enforced at `493e5e4b`, and retains #38, #39, #60, #89 and the parent follow-ups. It states the AUDIO_UNIT extent and the separate shipping, loader and conversion limits. Integrator §6 requires matching ENTITY/ADP identity, valid model IDs, stream-count maxima and the primary IDENTIFY index.

For #122, the STOP rule applies. Milan v1.2 §5.3.3.8, printed p. 27 (PDF p. 34), requires at least one AUDIO_CLUSTER on every Stream Port Input and Stream Port Output. IEEE 1722.1-2021 §7.2.13, Table 7-23 (pp. 81–82), defines `number_of_clusters` separately from `number_of_maps`. Dynamic mapping sets `number_of_maps` to zero; it does not relax the cluster count. F07.2 retains `1..*`. The [#122 clause disposition](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/122#issuecomment-5853884588) resolves the contract interpretation; the D8 zero-cluster correction remains with the parent under [milan-fpga#584](https://github.com/kebag-logic/milan-fpga/issues/584).

## Round 2

- Extend the explicit parent authority statement to every L1–L10 model obligation, including L1 partition/cardinalities and F07.2 minima, L2 multi-level ordering, L3, L4, L5, L7 and L8. Apply the defence-in-depth allocation to all processor semantic checks, including future #60 coverage.
- Replace the ambiguous reference after the rule table with “the generic packed-image checks listed in the §3.1 introduction.”
- Link the D8 correction owner and clarify that dynamic mapping does not relax the cluster count.
- Name `cfg_src_en_i`, `cfg_src_iface_i` and `cfg_stream_id_i` in the packed-vector sentence.
- Cite Milan v1.2 §5.3.3.1 for zero/all-ones model-ID invalidity in integrator §6 and L9's clause column.

## Validation

All repository documentation gates, link checks, generated-matrix checks and whitespace checks passed with return code 0: 917 links; 115 requirement rows and 17 gap findings; parameter inventories 24/24/24; 41 diagram blocks and 18 waveform blocks; generated matrix 92 rows with 0 untested. The unchanged public review probe passed **18/18**, preserving every current packing-enforcement claim.

Only `docs/architecture/07_memory_maps.md` and `docs/guides/integrator.md` changed. The parent ownership page was used read-only for the L1–L10 authority comparison. No code change or new semantic enforcement is claimed.
