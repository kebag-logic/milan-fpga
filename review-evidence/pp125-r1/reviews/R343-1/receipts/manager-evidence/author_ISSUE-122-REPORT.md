[A348] STOP disposition: retain F07.2's STREAM_PORT_INPUT-to-AUDIO_CLUSTER_IN multiplicity `1..*`.

Milan Specification v1.2 §5.3.3.8, printed p. 27 (PDF p. 34), states: “Each Stream Port Input of a Configuration shall contain at least one AUDIO_CLUSTER descriptor.” The same clause imposes the corresponding output minimum.

Milan §5.3.3.7 requires the STREAM_PORT descriptor format from IEEE 1722.1 §7.2.13 and prohibits attached input AUDIO_MAP descriptors. IEEE Std 1722.1-2021 §7.2.13, pp. 81–82, Table 7-23, defines number_of_clusters at offset 12: “The number of clusters within the Port.” Dynamic mapping uses number_of_maps=0; it does not waive Milan's cluster minimum.

The zero-cluster 8x8 input pools recorded by parent D8 (docs/ENDSTATION_BUILDER.md) and docs/reference/PP_DESCRIPTOR_OWNERSHIP.md therefore conflict with Milan §5.3.3.8. Their correction is a parent decision. Successful packing is no waiver. No F07.2 multiplicity edit will be made in this lane; #125's separate documentation work continues.
