[A333]


Separate processor change after this parent review; no donor file changed.
Replace the section 3.1 introduction beginning "Structural rules enforced"
with the following text, preserving the L1-L10 clause table:

> The consuming product owns its shipping model semantics. For the parent
> end-station, the allocation and measured enforcement are recorded in
> `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` of kebag-logic/milan-fpga.
> That contract distinguishes construction from discriminating refusal.
> The processor owns generic packed-image structure and validation:
> image extents, directory well-formedness, dense indices, name binding,
> line-buffer bounds and descriptor type/index consistency. An ownership
> assignment is not evidence that every check is implemented. At processor
> commit 990f96526bb89356c963a260ebbdcf2a77e6623a, the packer checks density,
> duplicate keys, names and line-buffer bounds but does not compare the
> descriptor body's type/index with its directory key.
>
> Parent shipping checks are authoritative for configuration-dependent
> semantics: model identity and evolution, AUDIO_UNIT rate-list offset,
> count and length, clock-source construction and list shape, and ADP
> stream-count maxima across supported configurations. Processor checks
> retained for the same semantic constraints are defence in depth.
> Neither construction nor byte-exact serving substitutes for a negative
> validation case. Open obligations remain under processor issues 38,
> 39, 60 and 89 and the parent matrix's linked follow-ups.

Add after L10:

> The AUDIO_UNIT descriptor extent must equal 144 + 4 times its rate count.
> The parent currently emits one configuration per image, with one or
> three rate words. Its loader permits at most eight distinct entries,
> but its image conversion currently supports only 48000, 96000 and
> 192000 Hz. These are separate limits. The processor packer at the pin
> above does not enforce the L10 semantic offset/count/length checks or
> the L6 identity clock-source list; issue 89 remains open.

Add to integrator guide section 6:

> Drive entity_model_id_i from the same identity used in ENTITY bytes.
> Zero and all ones are invalid. A static-model change requires a new
> model identity, subject to IEEE 1722.1 section 6.2.2.8's exclusions.
> Drive talker_sources_i and listener_sinks_i with the maximum respective
> STREAM_OUTPUT and STREAM_INPUT counts over every supported configuration.
> The ENTITY descriptor must carry those same values. Drive identify_index_i
> with the primary IDENTIFY CONTROL index present in every configuration.
> These are integrator obligations, not properties proved by ADP transport.

Further precise processor documentation dispositions:

- F07.2's STREAM_PORT_INPUT-to-cluster `1..*` edge conflicts with the
  parent's documented zero-cluster 8x8 input pools. Resolve against the
  actual governing clause under PP60; this audit makes no waiver.
- L3 must preserve the distinct Milan 6.3 talker and 6.4 listener
  obligations. The parent's rate-family gate does not establish a
  universal per-stream, per-configuration Base-format rule.
- Section 3.2/3.3 must credit the parent constructor for Table 7-8 bytes.
  The packer preserves bytes; it does not synthesize the redundancy tail.
  PP82's runtime overlays and response ceiling remain separate work.
- The generic metadata/body consistency gap stays processor-owned under
  F7, separately from PP60. Publishing allocation does not close it.
