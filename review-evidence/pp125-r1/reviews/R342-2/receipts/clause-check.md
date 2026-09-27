# Clause checks for the round-2 delta (short citations only)

Sources (local copies, extracted page by page with `pdftotext -layout -f N -l N` into the unpublished scratch directory):

- Milan Specification Consolidated v1.2 (Final Approved 20231130), file sha256 `6bb902be1c1de8c44f4c4c583a645b0b37e0b2dac27870486ce229e68ce3bba8`.
- IEEE Std 1722.1-2021, file sha256 `ad7b822008c1b78bce8af1470f1ace177a22344aa48c0da939066d6db9a65b9c`.

| Delta statement | Location at e04234e1 | Extracted page | Clause text (short) | Result |
|---|---|---|---|---|
| Zero and all-ones `entity_model_id` are invalid, Milan v1.2 §5.3.3.1, printed p. 25 | `docs/guides/integrator.md:242` | Milan PDF p. 32; footer "5.3. Entity model 25" (printed = PDF − 7) | §5.3.3.1 ENTITY: "The entity_model_id field shall be a valid EUI-64 (neither all zeros nor all ones)." | correct clause and page |
| L9 clause column "Milan v1.2 §5.3.1, §5.3.3.1" | `docs/architecture/07_memory_maps.md:132` | Milan PDF pp. 31-32 (printed 24-25) | §5.3.1 Introduction: static properties changed offline → "reports a different Entity Model ID"; §5.3.3.1 as above | both halves of L9 (evolution, validity) now cited |
| Maxima across configurations, Milan §5.3.3.1 (unchanged, re-read) | `docs/guides/integrator.md:246-248` | Milan PDF p. 32 | talker_stream_sources / listener_stream_sinks "maximum … among all possible Configurations" | correct |
| "dynamic mapping sets `number_of_maps` to zero; it does not relax the cluster count" | `docs/architecture/07_memory_maps.md:80-81` | IEEE PDF p. 82 (printed 82), §7.2.13 / Table 7-23 | dynamic-mapping entities "set the number_of_maps field to zero (0)"; `number_of_clusters` (offset 12) is a separate field | correct; nothing in the clause touches `number_of_clusters` |
| Cluster minimum, Milan §5.3.3.8 printed p. 27 (unchanged text) | `docs/architecture/07_memory_maps.md:78-79` | verified in round 1 (PDF p. 34) | — | unchanged |

External link targets added by the delta: kebag-logic/milan-fpga#584 (OPEN, "8x8 stream input ports own no AUDIO_CLUSTER, against Milan 5.3.3.8"; acceptance 2 updates D8 and the parent ownership page) — the correct owner of the D8 correction. See `external-links.txt`.
