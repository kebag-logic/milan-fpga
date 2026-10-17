[A631]

Closes #177

GET_AVB_INFO with any descriptor_type other than AVB_INTERFACE now answers NOT_IMPLEMENTED with the command echoed at its own length, the correctly sized response of IEEE 1722.1-2021 9.3.5.3.3 as 06 section 8.2 reads it. It previously answered NOT_SUPPORTED. AVB_INTERFACE still answers SUCCESS, and an AVB_INTERFACE index that does not exist still answers NO_SUCH_DESCRIPTOR. A command shorter than cdl 16 still answers BAD_ARGUMENTS. The order is length, then type, then existence, so a wrong type answers NOT_IMPLEMENTED whether that descriptor exists or not.

The change is confined to the GET_AVB_INFO arm of the engine's A_PLD-exit re-dispatch. An existing comment that bounded the NOT_IMPLEMENTED refusal sites at two now counts three. The command model's status set and entries follow (`NOT_IMPLEMENTED` and `NOTIMPL` replace `NOT_SUPPORTED` and `NSUPPE`), F06.14 is regenerated, and `tb/aecp_cmds/decode.json` is re-recorded. In the record only AEM 0x0027's wrong-type program moved: NOTIMPL, status 1, echo, at cdl 16-100. The microcode ROM is byte-identical.

The decision is recorded with the issue's clauses in the compliance review (section 8, item 12), with IEEE 7.4.40.1 and 7.4.40.3, Table 7-141 status 1 versus 11, 9.3.5.3.3 and Milan v1.2 5.4.2.23. It also appears in 06 sections 6.10 and 8.1.

Tests (`tb/pp_top` section V, run in the main build and by `make aecp-dispatch`):

- V5: 13 byte-exact NOT_IMPLEMENTED echo rows. They cover ENTITY, CONFIGURATION, AUDIO_UNIT, both STREAM types, the types either side of AVB_INTERFACE, CLOCK_DOMAIN, an absent CLOCK_DOMAIN index, 0x0109, 0x8009 and 0xFFFF at cdl 16, and a CLOCK_DOMAIN padded to cdl 20.
- V1b: an AVB_INTERFACE command padded to cdl 20 draws V1's SUCCESS response unchanged.
- V1, V3 and V4 are kept.
- M9 now sends 0x0027 with a real AVB_INTERFACE body. With the filler body the wrong-type refusal is byte-identical to M9's expected answer, and a guard-less `gavb_w` was measured to pass.

Planted mutants, each failing by name:

- Nine new dispatch-campaign arms: the message-type guard, the old NOT_SUPPORTED arm, a header-only NOT_IMPLEMENTED, the type gate dropped, a low-byte-only type gate, an inverted type gate, E_GAVB's locate miss ignored, padding refused, and the length floor moved to 14.
- One new standing control in `tb/aecp_cmds`: the old NOT_SUPPORTED arm.

Validation at processor main and this head:

- Every processor suite passes, 1,029,951 checks at main and 1,029,964 at this head. Every suite record is identical except tb/pp_top's default build, which gains the 13 new checks.
- Lint, `make check`, the matrix, the portability elaboration and the requirement-tag execution check pass at both ends. They differ only by the new link, the nine new patch files and +2 line offsets in the converted netlist.
- All 14 campaigns that build a changed file pass at both ends, and every existing record is identical: as sorted lines for the four completion-order drivers, with netlist line offsets masked for the two guard campaigns. The dispatch campaign grows from 44 to 53 checks and the decode controls from 16 to 17; every new arm is killed.
- A scratch parent at dev, with the processor gitlink at main and then at this head, passes all 17 consumer gates at both ends. Its evidence gate first refused three processor test readers that dev does not yet classify (two guard benches and the decode controls), at main as well as at this head. It passes with the two classifications earlier lanes supplied, applied uncommitted and attached as `parent-evidence-classification.patch`. The builder's external calibration-report arm stays not run. No parent commit is included.

Ports, parameters and register maps are unchanged.
