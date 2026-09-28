# [A417] Issue #595 handoff

Status: Assigned local work complete; ready for independent review.

Head: `44d3ae3b15a0d058abb837c655ad24bd9b64c6e8`.
Base: `1fa2357fcb9b83ad7d6cbeab0c7cc0eb957cdd3a`.
Branch: `595-yaml-int-refusal`.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
Worktree: `$LANES/595-yaml-int-refusal`.
Processor pin: `16be6768f710e79450aace277abacd6c2c3336e5`; unchanged checkout and gitlink.
Roles: author [A417], internal reviewer [R388], external reviewer [R389].

Assignment: https://github.com/kebag-logic/milan-fpga/issues/595#issuecomment-5867362523
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/595#issuecomment-5867413642

The sole [A10] comment settles scope; the board showed Backlog.
No push, PR creation, merge, other checkout, or configuration edits.
No hardware, firmware, processor, RTL, or gitlink changes.
Stop after the REVIEW READY comment with this local head.

## Sources and decisions

Read #595 body and all [A10] comments, PR #585, and both linked reports:

- https://github.com/kebag-logic/milan-fpga/pull/585
- https://github.com/kebag-logic/milan-fpga/blob/c0c58c242333ce58c14b3048cf5686e46b42f2d6/review-evidence/573-r1/reviews/R340-3/REPORT.md
- https://github.com/kebag-logic/milan-fpga/blob/104102d6237e9b1a854cdbc81e53681a8d67b5e9/review-evidence/573-r1/reviews/R341-3/REPORT.md

Applied the assignment's exact quoted-string rule to both unsigned callers.
Declared null differs from an omitted optional field.
An empty formats list remains valid and retains its existing default.
Existing semantic controls now declare quoted values to reach their original guards.
Their width, I/G-bit, pin-consistency and capabilities oracles remain intact.

## Change list

| File:line | Change |
|---|---|
| `sw/builder/endstation_builder.py:1425` | Check declared formats list type before fallback or iteration. |
| `sw/builder/endstation_builder.py:3181` | Refuse non-strings before separator removal; correct the docstring. |
| `sw/builder/endstation_builder.py:3295` | Retain missing-MAC refusal; route explicit null to the quote rule. |
| `sw/builder/endstation_builder.py:3664` | Parse strings only, preserving range checks. |
| `sw/builder/endstation_builder.py:3677` | Default only when omitted; refuse explicit non-strings. |
| `sw/builder/endstation_builder.py:3694` | Verify quoted declarations; refuse explicit null. |
| `sw/builder/test_declarations.py:178` | Assert exact ConfigError messages rather than incidental errors. |
| `sw/builder/test_declarations.py:189` | Pin MAC spellings, scalar refusals and existing semantics. |
| `sw/builder/test_declarations.py:227` | Cover both unsigned callers and packed capabilities. |
| `sw/builder/test_declarations.py:275` | Cover all eight stream indices, list types, values and defaults. |
| `sw/builder/test_declarations.py:507` | Include the new controls in the declaration and full banks. |
| `sw/builder/test_builder.py:25539` | Quote hexadecimal declarations while retaining numeric expected values. |
| `sw/builder/test_builder.py:25724` | Keep semantic refusals reachable under the new type rule. |
| `sw/builder/test_builder.py:25776` | Quote the agreeing OUI and divergent capability fixtures. |
| `sw/builder/README-parameters.md:127` | Document list type and derived defaults. |
| `sw/builder/README-parameters.md:159` | Document every new string-only field and YAML hazards. |
| `docs/ENDSTATION_BUILDER.md:883` | Record the string and list rules in the builder contract. |

## Rule per field

| Field | Rule |
|---|---|
| `platform.mac_address` | Required hex string, optional prefix/underscores/colon/dash; nonzero, 48-bit, unicast. Explicit null gets the quote instruction; missing gets the required-field error. |
| `entity.vendor_oui` | Optional hex string, 24-bit, first-octet I/G bit clear. Omitted uses the existing default. Declared null refuses. Model-ID consistency still applies. |
| `entity.entity_capabilities` | Optional hex string, 32-bit, equal to the processor's ADP constant. Omitted derives the existing value. Declared null refuses. |
| `streams.talkers[i].formats` | A declared value must be a list. Missing or empty lists retain defaults. Every entry remains a quoted hex word under PR #585. |
| `streams.listeners[i].formats` | The same list/string rule; derived family completion remains unchanged. |

## Refusal and quoted-spelling cases

Measured by `focused_evidence.py` while running the committed declaration tests.
All 233 loader attempts completed with their expected result.
Capabilities resolve from the final packed ENTITY descriptor, not the legacy ROM.
MAC values below show canonical colon spelling; OUI values show the resolved model prefix.
An empty scalar is an explicit YAML null. No resolved value exists after refusal.

| Field | YAML token | Exact message | Resolved value |
|---|---|---|---|
| `platform.mac_address` | `"0x020000000002"` | `accepted` | `02:00:00:00:00:02` |
| `platform.mac_address` | `"020000000002"` | `accepted` | `02:00:00:00:00:02` |
| `platform.mac_address` | `"02:00:00:00:00:02"` | `accepted` | `02:00:00:00:00:02` |
| `platform.mac_address` | `"02-00-00-00-00-02"` | `accepted` | `02:00:00:00:00:02` |
| `platform.mac_address` | `"0x0200_0000_0002"` | `accepted` | `02:00:00:00:00:02` |
| `platform.mac_address` | `"123456789012"` | `accepted` | `12:34:56:78:90:12` |
| `platform.mac_address` | `"0x000000F42402"` | `accepted` | `00:00:00:f4:24:02` |
| `platform.mac_address` | `"10:20:30:40:50:02"` | `accepted` | `10:20:30:40:50:02` |
| `platform.mac_address` | `0x000000F42402` | `platform.mac_address: quote the hexadecimal value as a YAML string` | - |
| `platform.mac_address` | `0x020000000002` | `platform.mac_address: quote the hexadecimal value as a YAML string` | - |
| `platform.mac_address` | `020000000002` | `platform.mac_address: quote the hexadecimal value as a YAML string` | - |
| `platform.mac_address` | `123456789012` | `platform.mac_address: quote the hexadecimal value as a YAML string` | - |
| `platform.mac_address` | `10:20:30:40:50:02` | `platform.mac_address: quote the hexadecimal value as a YAML string` | - |
| `platform.mac_address` | `0` | `platform.mac_address: quote the hexadecimal value as a YAML string` | - |
| `platform.mac_address` | `true` | `platform.mac_address: quote the hexadecimal value as a YAML string` | - |
| `platform.mac_address` | `false` | `platform.mac_address: quote the hexadecimal value as a YAML string` | - |
| `platform.mac_address` | `null` | `platform.mac_address: quote the hexadecimal value as a YAML string` | - |
| `platform.mac_address` | `<empty scalar>` | `platform.mac_address: quote the hexadecimal value as a YAML string` | - |
| `platform.mac_address` | `1.5` | `platform.mac_address: quote the hexadecimal value as a YAML string` | - |
| `platform.mac_address` | `[]` | `platform.mac_address: quote the hexadecimal value as a YAML string` | - |
| `platform.mac_address` | `{}` | `platform.mac_address: quote the hexadecimal value as a YAML string` | - |
| `platform.mac_address` | `<omitted>` | `platform.mac_address is required` | - |
| `platform.mac_address` | `'0'` | `platform.mac_address: '0' out of MAC-48 range (or all-zero)` | - |
| `platform.mac_address` | `'1000000000000'` | `platform.mac_address: '1000000000000' out of MAC-48 range (or all-zero)` | - |
| `platform.mac_address` | `'010000000001'` | `platform.mac_address: '010000000001' has the I/G bit set - a station MAC must be UNICAST (it becomes the AVTP stream_id prefix and the ATDECC entity_id)` | - |
| `platform.mac_address` | `xyz` | `platform.mac_address: 'xyz' is not a MAC-48` | - |
| `entity.vendor_oui` | `"0x123456"` | `accepted` | `0x123456` |
| `entity.vendor_oui` | `"123456"` | `accepted` | `0x123456` |
| `entity.vendor_oui` | `"0x12_3456"` | `accepted` | `0x123456` |
| `entity.vendor_oui` | `0x123456` | `entity.vendor_oui: quote the hexadecimal value as a YAML string` | - |
| `entity.vendor_oui` | `1193046` | `entity.vendor_oui: quote the hexadecimal value as a YAML string` | - |
| `entity.vendor_oui` | `123456` | `entity.vendor_oui: quote the hexadecimal value as a YAML string` | - |
| `entity.vendor_oui` | `001234` | `entity.vendor_oui: quote the hexadecimal value as a YAML string` | - |
| `entity.vendor_oui` | `10:20:30` | `entity.vendor_oui: quote the hexadecimal value as a YAML string` | - |
| `entity.vendor_oui` | `0` | `entity.vendor_oui: quote the hexadecimal value as a YAML string` | - |
| `entity.vendor_oui` | `true` | `entity.vendor_oui: quote the hexadecimal value as a YAML string` | - |
| `entity.vendor_oui` | `false` | `entity.vendor_oui: quote the hexadecimal value as a YAML string` | - |
| `entity.vendor_oui` | `null` | `entity.vendor_oui: quote the hexadecimal value as a YAML string` | - |
| `entity.vendor_oui` | `<empty scalar>` | `entity.vendor_oui: quote the hexadecimal value as a YAML string` | - |
| `entity.vendor_oui` | `1.5` | `entity.vendor_oui: quote the hexadecimal value as a YAML string` | - |
| `entity.vendor_oui` | `[]` | `entity.vendor_oui: quote the hexadecimal value as a YAML string` | - |
| `entity.vendor_oui` | `{}` | `entity.vendor_oui: quote the hexadecimal value as a YAML string` | - |
| `entity.vendor_oui` | `'-1'` | `entity.vendor_oui: '-1' is outside 24 bits` | - |
| `entity.vendor_oui` | `'1000000'` | `entity.vendor_oui: '1000000' is outside 24 bits` | - |
| `entity.vendor_oui` | `<omitted>` | `accepted` | `0x001BC5` |
| `entity.entity_capabilities` | `"0x0000C588"` | `accepted` | `0x0000C588` |
| `entity.entity_capabilities` | `"0000C588"` | `accepted` | `0x0000C588` |
| `entity.entity_capabilities` | `"0x00_00C588"` | `accepted` | `0x0000C588` |
| `entity.entity_capabilities` | `0x0000C588` | `entity.entity_capabilities: quote the hexadecimal value as a YAML string` | - |
| `entity.entity_capabilities` | `50568` | `entity.entity_capabilities: quote the hexadecimal value as a YAML string` | - |
| `entity.entity_capabilities` | `123456` | `entity.entity_capabilities: quote the hexadecimal value as a YAML string` | - |
| `entity.entity_capabilities` | `001234` | `entity.entity_capabilities: quote the hexadecimal value as a YAML string` | - |
| `entity.entity_capabilities` | `10:20:30` | `entity.entity_capabilities: quote the hexadecimal value as a YAML string` | - |
| `entity.entity_capabilities` | `0` | `entity.entity_capabilities: quote the hexadecimal value as a YAML string` | - |
| `entity.entity_capabilities` | `true` | `entity.entity_capabilities: quote the hexadecimal value as a YAML string` | - |
| `entity.entity_capabilities` | `false` | `entity.entity_capabilities: quote the hexadecimal value as a YAML string` | - |
| `entity.entity_capabilities` | `null` | `entity.entity_capabilities: quote the hexadecimal value as a YAML string` | - |
| `entity.entity_capabilities` | `<empty scalar>` | `entity.entity_capabilities: quote the hexadecimal value as a YAML string` | - |
| `entity.entity_capabilities` | `1.5` | `entity.entity_capabilities: quote the hexadecimal value as a YAML string` | - |
| `entity.entity_capabilities` | `[]` | `entity.entity_capabilities: quote the hexadecimal value as a YAML string` | - |
| `entity.entity_capabilities` | `{}` | `entity.entity_capabilities: quote the hexadecimal value as a YAML string` | - |
| `entity.entity_capabilities` | `'-1'` | `entity.entity_capabilities: '-1' is outside 32 bits` | - |
| `entity.entity_capabilities` | `'100000000'` | `entity.entity_capabilities: '100000000' is outside 32 bits` | - |
| `entity.entity_capabilities` | `<omitted>` | `accepted` | `0x0000C588` |
| `entity.entity_capabilities` | `<omitted>` | `accepted` | `0x0000C588` |
| `streams.talkers[0].formats` | `"0205022000806000"` | `streams.talkers[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[0].formats` | `"0x0205022000806000"` | `streams.talkers[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[0].formats` | `0x0205022000806000` | `streams.talkers[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[0].formats` | `0205022000806000` | `streams.talkers[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[0].formats` | `123456` | `streams.talkers[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[0].formats` | `10:20:30` | `streams.talkers[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[0].formats` | `0` | `streams.talkers[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[0].formats` | `true` | `streams.talkers[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[0].formats` | `false` | `streams.talkers[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[0].formats` | `null` | `streams.talkers[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[0].formats` | `<empty scalar>` | `streams.talkers[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[0].formats` | `""` | `streams.talkers[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[0].formats` | `1.5` | `streams.talkers[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[0].formats` | `{}` | `streams.talkers[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[0].formats` | `{"0x0205022000806000": 1}` | `streams.talkers[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[0].formats` | `["0x0205022000806000"]` | `accepted` | `0x0205022000806000` |
| `streams.talkers[0].formats` | `["0205022000806000"]` | `accepted` | `0x0205022000806000` |
| `streams.talkers[0].formats` | `["0x0205_0220_0080_6000"]` | `accepted` | `0x0205022000806000` |
| `streams.talkers[0].formats` | `[0x0205022000806000]` | `streams.talkers[0].formats: quote the hexadecimal value as a YAML string` | - |
| `streams.talkers[0].formats` | `<omitted>` | `accepted` | `0x0205022001006000` |
| `streams.talkers[0].formats` | `[]` | `accepted` | `0x0205022001006000` |
| `streams.talkers[1].formats` | `"0205022000806000"` | `streams.talkers[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[1].formats` | `"0x0205022000806000"` | `streams.talkers[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[1].formats` | `0x0205022000806000` | `streams.talkers[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[1].formats` | `0205022000806000` | `streams.talkers[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[1].formats` | `123456` | `streams.talkers[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[1].formats` | `10:20:30` | `streams.talkers[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[1].formats` | `0` | `streams.talkers[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[1].formats` | `true` | `streams.talkers[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[1].formats` | `false` | `streams.talkers[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[1].formats` | `null` | `streams.talkers[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[1].formats` | `<empty scalar>` | `streams.talkers[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[1].formats` | `""` | `streams.talkers[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[1].formats` | `1.5` | `streams.talkers[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[1].formats` | `{}` | `streams.talkers[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[1].formats` | `{"0x0205022000806000": 1}` | `streams.talkers[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[1].formats` | `["0x0205022000806000"]` | `accepted` | `0x0205022000806000` |
| `streams.talkers[1].formats` | `["0205022000806000"]` | `accepted` | `0x0205022000806000` |
| `streams.talkers[1].formats` | `["0x0205_0220_0080_6000"]` | `accepted` | `0x0205022000806000` |
| `streams.talkers[1].formats` | `[0x0205022000806000]` | `streams.talkers[1].formats: quote the hexadecimal value as a YAML string` | - |
| `streams.talkers[1].formats` | `<omitted>` | `accepted` | `0x0205022001006000` |
| `streams.talkers[1].formats` | `[]` | `accepted` | `0x0205022001006000` |
| `streams.talkers[2].formats` | `"0205022000806000"` | `streams.talkers[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[2].formats` | `"0x0205022000806000"` | `streams.talkers[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[2].formats` | `0x0205022000806000` | `streams.talkers[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[2].formats` | `0205022000806000` | `streams.talkers[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[2].formats` | `123456` | `streams.talkers[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[2].formats` | `10:20:30` | `streams.talkers[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[2].formats` | `0` | `streams.talkers[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[2].formats` | `true` | `streams.talkers[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[2].formats` | `false` | `streams.talkers[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[2].formats` | `null` | `streams.talkers[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[2].formats` | `<empty scalar>` | `streams.talkers[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[2].formats` | `""` | `streams.talkers[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[2].formats` | `1.5` | `streams.talkers[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[2].formats` | `{}` | `streams.talkers[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[2].formats` | `{"0x0205022000806000": 1}` | `streams.talkers[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[2].formats` | `["0x0205022000806000"]` | `accepted` | `0x0205022000806000` |
| `streams.talkers[2].formats` | `["0205022000806000"]` | `accepted` | `0x0205022000806000` |
| `streams.talkers[2].formats` | `["0x0205_0220_0080_6000"]` | `accepted` | `0x0205022000806000` |
| `streams.talkers[2].formats` | `[0x0205022000806000]` | `streams.talkers[2].formats: quote the hexadecimal value as a YAML string` | - |
| `streams.talkers[2].formats` | `<omitted>` | `accepted` | `0x0205022001006000` |
| `streams.talkers[2].formats` | `[]` | `accepted` | `0x0205022001006000` |
| `streams.talkers[3].formats` | `"0205022000806000"` | `streams.talkers[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[3].formats` | `"0x0205022000806000"` | `streams.talkers[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[3].formats` | `0x0205022000806000` | `streams.talkers[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[3].formats` | `0205022000806000` | `streams.talkers[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[3].formats` | `123456` | `streams.talkers[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[3].formats` | `10:20:30` | `streams.talkers[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[3].formats` | `0` | `streams.talkers[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[3].formats` | `true` | `streams.talkers[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[3].formats` | `false` | `streams.talkers[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[3].formats` | `null` | `streams.talkers[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[3].formats` | `<empty scalar>` | `streams.talkers[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[3].formats` | `""` | `streams.talkers[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[3].formats` | `1.5` | `streams.talkers[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[3].formats` | `{}` | `streams.talkers[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[3].formats` | `{"0x0205022000806000": 1}` | `streams.talkers[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.talkers[3].formats` | `["0x0205022000806000"]` | `accepted` | `0x0205022000806000` |
| `streams.talkers[3].formats` | `["0205022000806000"]` | `accepted` | `0x0205022000806000` |
| `streams.talkers[3].formats` | `["0x0205_0220_0080_6000"]` | `accepted` | `0x0205022000806000` |
| `streams.talkers[3].formats` | `[0x0205022000806000]` | `streams.talkers[3].formats: quote the hexadecimal value as a YAML string` | - |
| `streams.talkers[3].formats` | `<omitted>` | `accepted` | `0x0205022001006000` |
| `streams.talkers[3].formats` | `[]` | `accepted` | `0x0205022001006000` |
| `streams.listeners[0].formats` | `"0205022000806000"` | `streams.listeners[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[0].formats` | `"0x0205022000806000"` | `streams.listeners[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[0].formats` | `0x0205022000806000` | `streams.listeners[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[0].formats` | `0205022000806000` | `streams.listeners[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[0].formats` | `123456` | `streams.listeners[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[0].formats` | `10:20:30` | `streams.listeners[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[0].formats` | `0` | `streams.listeners[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[0].formats` | `true` | `streams.listeners[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[0].formats` | `false` | `streams.listeners[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[0].formats` | `null` | `streams.listeners[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[0].formats` | `<empty scalar>` | `streams.listeners[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[0].formats` | `""` | `streams.listeners[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[0].formats` | `1.5` | `streams.listeners[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[0].formats` | `{}` | `streams.listeners[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[0].formats` | `{"0x0205022000806000": 1}` | `streams.listeners[0].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[0].formats` | `["0x0205022000806000"]` | `accepted` | `0x0205022000806000, 0x0215022002006000` |
| `streams.listeners[0].formats` | `["0205022000806000"]` | `accepted` | `0x0205022000806000, 0x0215022002006000` |
| `streams.listeners[0].formats` | `["0x0205_0220_0080_6000"]` | `accepted` | `0x0205022000806000, 0x0215022002006000` |
| `streams.listeners[0].formats` | `[0x0205022000806000]` | `streams.listeners[0].formats: quote the hexadecimal value as a YAML string` | - |
| `streams.listeners[0].formats` | `<omitted>` | `accepted` | `0x0205022001006000, 0x0215022002006000` |
| `streams.listeners[0].formats` | `[]` | `accepted` | `0x0205022001006000, 0x0215022002006000` |
| `streams.listeners[1].formats` | `"0205022000806000"` | `streams.listeners[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[1].formats` | `"0x0205022000806000"` | `streams.listeners[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[1].formats` | `0x0205022000806000` | `streams.listeners[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[1].formats` | `0205022000806000` | `streams.listeners[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[1].formats` | `123456` | `streams.listeners[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[1].formats` | `10:20:30` | `streams.listeners[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[1].formats` | `0` | `streams.listeners[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[1].formats` | `true` | `streams.listeners[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[1].formats` | `false` | `streams.listeners[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[1].formats` | `null` | `streams.listeners[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[1].formats` | `<empty scalar>` | `streams.listeners[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[1].formats` | `""` | `streams.listeners[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[1].formats` | `1.5` | `streams.listeners[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[1].formats` | `{}` | `streams.listeners[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[1].formats` | `{"0x0205022000806000": 1}` | `streams.listeners[1].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[1].formats` | `["0x0205022000806000"]` | `accepted` | `0x0205022000806000, 0x0215022002006000` |
| `streams.listeners[1].formats` | `["0205022000806000"]` | `accepted` | `0x0205022000806000, 0x0215022002006000` |
| `streams.listeners[1].formats` | `["0x0205_0220_0080_6000"]` | `accepted` | `0x0205022000806000, 0x0215022002006000` |
| `streams.listeners[1].formats` | `[0x0205022000806000]` | `streams.listeners[1].formats: quote the hexadecimal value as a YAML string` | - |
| `streams.listeners[1].formats` | `<omitted>` | `accepted` | `0x0205022001006000, 0x0215022002006000` |
| `streams.listeners[1].formats` | `[]` | `accepted` | `0x0205022001006000, 0x0215022002006000` |
| `streams.listeners[2].formats` | `"0205022000806000"` | `streams.listeners[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[2].formats` | `"0x0205022000806000"` | `streams.listeners[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[2].formats` | `0x0205022000806000` | `streams.listeners[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[2].formats` | `0205022000806000` | `streams.listeners[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[2].formats` | `123456` | `streams.listeners[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[2].formats` | `10:20:30` | `streams.listeners[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[2].formats` | `0` | `streams.listeners[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[2].formats` | `true` | `streams.listeners[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[2].formats` | `false` | `streams.listeners[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[2].formats` | `null` | `streams.listeners[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[2].formats` | `<empty scalar>` | `streams.listeners[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[2].formats` | `""` | `streams.listeners[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[2].formats` | `1.5` | `streams.listeners[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[2].formats` | `{}` | `streams.listeners[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[2].formats` | `{"0x0205022000806000": 1}` | `streams.listeners[2].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[2].formats` | `["0x0205022000806000"]` | `accepted` | `0x0205022000806000, 0x0215022002006000` |
| `streams.listeners[2].formats` | `["0205022000806000"]` | `accepted` | `0x0205022000806000, 0x0215022002006000` |
| `streams.listeners[2].formats` | `["0x0205_0220_0080_6000"]` | `accepted` | `0x0205022000806000, 0x0215022002006000` |
| `streams.listeners[2].formats` | `[0x0205022000806000]` | `streams.listeners[2].formats: quote the hexadecimal value as a YAML string` | - |
| `streams.listeners[2].formats` | `<omitted>` | `accepted` | `0x0205022001006000, 0x0215022002006000` |
| `streams.listeners[2].formats` | `[]` | `accepted` | `0x0205022001006000, 0x0215022002006000` |
| `streams.listeners[3].formats` | `"0205022000806000"` | `streams.listeners[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[3].formats` | `"0x0205022000806000"` | `streams.listeners[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[3].formats` | `0x0205022000806000` | `streams.listeners[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[3].formats` | `0205022000806000` | `streams.listeners[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[3].formats` | `123456` | `streams.listeners[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[3].formats` | `10:20:30` | `streams.listeners[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[3].formats` | `0` | `streams.listeners[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[3].formats` | `true` | `streams.listeners[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[3].formats` | `false` | `streams.listeners[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[3].formats` | `null` | `streams.listeners[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[3].formats` | `<empty scalar>` | `streams.listeners[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[3].formats` | `""` | `streams.listeners[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[3].formats` | `1.5` | `streams.listeners[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[3].formats` | `{}` | `streams.listeners[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[3].formats` | `{"0x0205022000806000": 1}` | `streams.listeners[3].formats: must be a list of quoted hexadecimal strings` | - |
| `streams.listeners[3].formats` | `["0x0205022000806000"]` | `accepted` | `0x0205022000806000, 0x0215022002006000` |
| `streams.listeners[3].formats` | `["0205022000806000"]` | `accepted` | `0x0205022000806000, 0x0215022002006000` |
| `streams.listeners[3].formats` | `["0x0205_0220_0080_6000"]` | `accepted` | `0x0205022000806000, 0x0215022002006000` |
| `streams.listeners[3].formats` | `[0x0205022000806000]` | `streams.listeners[3].formats: quote the hexadecimal value as a YAML string` | - |
| `streams.listeners[3].formats` | `<omitted>` | `accepted` | `0x0205022001006000, 0x0215022002006000` |
| `streams.listeners[3].formats` | `[]` | `accepted` | `0x0205022001006000, 0x0215022002006000` |

Additional parser-level controls retain values before field semantics:

| Field widths | Quoted hex spelling | Result |
|---|---|---|
| 24 and 32 | `123456` | `0x123456` |
| 24 and 32 | `001234` | `0x001234` |
| 24 and 32 | `10_20` | `0x1020` |
| 24 and 32 | `0` | `0x0` |
| 24 | `FFFFFF` | `0xFFFFFF` |
| 32 | `FFFFFFFF` | `0xFFFFFFFF` |

These are parser controls; later OUI/capability semantics still apply.

## Mutant table

Only the three inspected functions are mutated in memory.
No source file or processor file is changed by the campaign.
Each restored control passes; source SHA256 is unchanged.

| Restored defect | Named control | Killing assertion | Result and diagnostic |
|---|---|---|---|
| `MAC integer decimal-text reread as hex` | `test_station_mac_string_contract` | `test_declarations.py:186 _yaml_refused` | `KILLED: accepted 0x000000F42402: expected platform.mac_address: quote the hexadecimal value as a YAML string` |
| `Declared uint accepts integers` | `test_declared_hex_string_contract` | `test_declarations.py:186 _yaml_refused` | `KILLED: accepted 0x123456: expected entity.vendor_oui: quote the hexadecimal value as a YAML string` |
| `Scalar formats iterates or defaults` | `test_formats_list_contract` | `test_declarations.py:184 _yaml_refused` | `KILLED: ('"0205022000806000"', 'streams.talkers[0].formats: must be a list of quoted hexadecimal strings', 'streams.talkers[0].formats: must contain only AAF formats (Milan v1.2 5.3.3.4; AAF/CRF families must not mix)')` |

## Five-configuration SHA256 before/after

Baseline was generated before source edits, at the recorded base.
The final run compares every generated file's raw bytes as well as hashes.
Five configuration files and 70 artifacts match, including all three Arty shapes.
Generation uses the normal derivation/writer and AEM image path.
The sweep fragment is emitted separately without transferring tracked ownership.
Artifacts stay in disposable scratch; only sizes and hashes are retained here.

| Configuration or artifact | Bytes before/after | SHA256 before | SHA256 after |
|---|---|---|---|
| `configs/endstation_arty_4x4.yaml` | 11390 / 11390 | `c9d907e6d56b6413c79383f0fc8bafb13a820af1969218a2625dd84167fbd865` | `c9d907e6d56b6413c79383f0fc8bafb13a820af1969218a2625dd84167fbd865` |
| `endstation_arty_4x4/adp_shape_defaults.svh` | 7603 / 7603 | `fbf4bf36ab9c972789aa4a774fea6a1e8f462eadebc919ea30384bc89b3d02fe` | `fbf4bf36ab9c972789aa4a774fea6a1e8f462eadebc919ea30384bc89b3d02fe` |
| `endstation_arty_4x4/aecp_aem_rom.svh` | 52444 / 52444 | `1cd6c92190c1b4f8c14783423a1618328e2fbefe286ab78edb00f96adb45f59d` | `1cd6c92190c1b4f8c14783423a1618328e2fbefe286ab78edb00f96adb45f59d` |
| `endstation_arty_4x4/aem_desc.bin` | 10112 / 10112 | `1b288e13ccbf03410c593a53bc22f4a68e3d289eef8a7f907e63bc98a51415ff` | `1b288e13ccbf03410c593a53bc22f4a68e3d289eef8a7f907e63bc98a51415ff` |
| `endstation_arty_4x4/aem_desc.json` | 225 / 225 | `6670576ec481a23477264ceae23ac67a491f0637427fa9f43aef3e26405e89cd` | `6670576ec481a23477264ceae23ac67a491f0637427fa9f43aef3e26405e89cd` |
| `endstation_arty_4x4/aem_desc.map` | 1311 / 1311 | `09cf3da5a39730c1acedae4f09474c2d98d1aa17d8fa36f0238adc210fdaa571` | `09cf3da5a39730c1acedae4f09474c2d98d1aa17d8fa36f0238adc210fdaa571` |
| `endstation_arty_4x4/aem_overlay.json` | 11920 / 11920 | `a9b9d900fb425e95e2b3728b47bc5c10b7d7f6b1027be1758f27b01b00b8f98c` | `a9b9d900fb425e95e2b3728b47bc5c10b7d7f6b1027be1758f27b01b00b8f98c` |
| `endstation_arty_4x4/build_plan.md` | 11000 / 11000 | `c040b872fa0102576fccf0f235cd9436722efd9f66cf885b220a5dfcd502d722` | `c040b872fa0102576fccf0f235cd9436722efd9f66cf885b220a5dfcd502d722` |
| `endstation_arty_4x4/gptp_ucode.hex` | 13312 / 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| `endstation_arty_4x4/lwsrp_csr_defaults.svh` | 2183 / 2183 | `90d4615e95883d5c1fdf5ce4eb8e716ac655114d8f0eb9e5579ec8e671bbfa88` | `90d4615e95883d5c1fdf5ce4eb8e716ac655114d8f0eb9e5579ec8e671bbfa88` |
| `endstation_arty_4x4/lwsrp_table.json` | 4084 / 4084 | `90e1aa992317980e97ec42768d524e9b8af65e2279a31e1696f5f68254f05221` | `90e1aa992317980e97ec42768d524e9b8af65e2279a31e1696f5f68254f05221` |
| `endstation_arty_4x4/lwsrp_table.svh` | 4288 / 4288 | `36331d96c16b57ba3660a3183af58752195d94f2681d03ccfcf50003f227b222` | `36331d96c16b57ba3660a3183af58752195d94f2681d03ccfcf50003f227b222` |
| `endstation_arty_4x4/platform_shape.json` | 246 / 246 | `bbd040ba298a66ff0bd856f8f0b4e75c04c1831ba635a5b3ad756625ab8b0a28` | `bbd040ba298a66ff0bd856f8f0b4e75c04c1831ba635a5b3ad756625ab8b0a28` |
| `endstation_arty_4x4/soc_params.json` | 589 / 589 | `fe552b1ec220f349b55cd499bc62680e9f7abf28397125cc457fd7cf63f61fb8` | `fe552b1ec220f349b55cd499bc62680e9f7abf28397125cc457fd7cf63f61fb8` |
| `endstation_arty_4x4/sweep_opts_arty.sh` | 1209 / 1209 | `f50e8a7f952d693de9c85e76caec5d77c252726cd6409eaee57e4a328efe8dcc` | `f50e8a7f952d693de9c85e76caec5d77c252726cd6409eaee57e4a328efe8dcc` |
| `configs/endstation_arty_8ch.yaml` | 12583 / 12583 | `3cdf5b053c9b71b7e1535115d7352e5b73dff6e203c251b5220e32c6396a915d` | `3cdf5b053c9b71b7e1535115d7352e5b73dff6e203c251b5220e32c6396a915d` |
| `endstation_arty_8ch/adp_shape_defaults.svh` | 7877 / 7877 | `48076cb36b171972c3e060087ad98755d957f13603b4793cb2784725eda0bf48` | `48076cb36b171972c3e060087ad98755d957f13603b4793cb2784725eda0bf48` |
| `endstation_arty_8ch/aecp_aem_rom.svh` | 71921 / 71921 | `19dd262b93e56aeab1641f3d3e534fc7af372f1c2f8c1801e5a7895d1982ae34` | `19dd262b93e56aeab1641f3d3e534fc7af372f1c2f8c1801e5a7895d1982ae34` |
| `endstation_arty_8ch/aem_desc.bin` | 15360 / 15360 | `2b5c008cf3a2ff1eca11ef5e24c5a2e391e97f25435854430e563758de516b9b` | `2b5c008cf3a2ff1eca11ef5e24c5a2e391e97f25435854430e563758de516b9b` |
| `endstation_arty_8ch/aem_desc.json` | 225 / 225 | `21b168d41ba1e6517eb8fd702070565826b795b45a98c91d218bae932d4d8259` | `21b168d41ba1e6517eb8fd702070565826b795b45a98c91d218bae932d4d8259` |
| `endstation_arty_8ch/aem_desc.map` | 1311 / 1311 | `163d5a414e34591ad639c3682747a35c43db64dcb3d46cb06c77d4c33edb634a` | `163d5a414e34591ad639c3682747a35c43db64dcb3d46cb06c77d4c33edb634a` |
| `endstation_arty_8ch/aem_overlay.json` | 16978 / 16978 | `87fc3c51e2fc5a49b91d67e05ea621449391619430ecfaef4cac5422b5b4b94e` | `87fc3c51e2fc5a49b91d67e05ea621449391619430ecfaef4cac5422b5b4b94e` |
| `endstation_arty_8ch/build_plan.md` | 11003 / 11003 | `1a93c95f35d176c5b52e03c1f0d5ccea7726c682a803948a5763029a509edf76` | `1a93c95f35d176c5b52e03c1f0d5ccea7726c682a803948a5763029a509edf76` |
| `endstation_arty_8ch/gptp_ucode.hex` | 13312 / 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| `endstation_arty_8ch/lwsrp_csr_defaults.svh` | 2183 / 2183 | `f2519804843397b4bde6393e3be67f348e3b3ef6e73e62fef22b3a71b4ecf87f` | `f2519804843397b4bde6393e3be67f348e3b3ef6e73e62fef22b3a71b4ecf87f` |
| `endstation_arty_8ch/lwsrp_table.json` | 4084 / 4084 | `0e151e2854b3799281d19d01e67c27b04a53ca470a672ad27bc48f93ea840987` | `0e151e2854b3799281d19d01e67c27b04a53ca470a672ad27bc48f93ea840987` |
| `endstation_arty_8ch/lwsrp_table.svh` | 4288 / 4288 | `c7189e2e3dcf79a7fcd6c204674fca581d89aea327c77b65ea7aa57f38aa3e19` | `c7189e2e3dcf79a7fcd6c204674fca581d89aea327c77b65ea7aa57f38aa3e19` |
| `endstation_arty_8ch/platform_shape.json` | 246 / 246 | `b818b72a035c5f73870925ffe208eda20292bedc629a399d5d31aa14160242ce` | `b818b72a035c5f73870925ffe208eda20292bedc629a399d5d31aa14160242ce` |
| `endstation_arty_8ch/soc_params.json` | 589 / 589 | `7a10be52746259e11e1c43402cb8097ca5234e9b358fd6160af5c5e42673faff` | `7a10be52746259e11e1c43402cb8097ca5234e9b358fd6160af5c5e42673faff` |
| `endstation_arty_8ch/sweep_opts_arty.sh` | 1209 / 1209 | `8ea30219313f53e66c302861aa6e8824d0ded1f7f6ddc159a113ff79326a75f3` | `8ea30219313f53e66c302861aa6e8824d0ded1f7f6ddc159a113ff79326a75f3` |
| `configs/endstation_arty_current.yaml` | 15156 / 15156 | `95304ca8726592dbaa3ba7298def5971ec2229b1ff936bfe6c44d21f9dfe1621` | `95304ca8726592dbaa3ba7298def5971ec2229b1ff936bfe6c44d21f9dfe1621` |
| `endstation_arty_current/adp_shape_defaults.svh` | 7130 / 7130 | `13540133426c56e849bfc7b5fbbac883c0f90bc0a0af4700247179e17372fe34` | `13540133426c56e849bfc7b5fbbac883c0f90bc0a0af4700247179e17372fe34` |
| `endstation_arty_current/aecp_aem_rom.svh` | 33428 / 33428 | `d8365928caecf01dc79b3d9a75a6c56573669ad121d8cc04b42f44820601c999` | `d8365928caecf01dc79b3d9a75a6c56573669ad121d8cc04b42f44820601c999` |
| `endstation_arty_current/aem_desc.bin` | 5792 / 5792 | `ac833c3ccde42a2d9a78b517d660b9f7da03c4b3d31227aa65dcaf9e8def6192` | `ac833c3ccde42a2d9a78b517d660b9f7da03c4b3d31227aa65dcaf9e8def6192` |
| `endstation_arty_current/aem_desc.json` | 228 / 228 | `f2b7d5df50d5f93440e8a87b0eef92825be04297de4f69ba4d49faa403187310` | `f2b7d5df50d5f93440e8a87b0eef92825be04297de4f69ba4d49faa403187310` |
| `endstation_arty_current/aem_desc.map` | 1310 / 1310 | `77dad531965096987d682f77e93f81e5b6f182eaae879fb43b084be8570bec4c` | `77dad531965096987d682f77e93f81e5b6f182eaae879fb43b084be8570bec4c` |
| `endstation_arty_current/aem_overlay.json` | 6238 / 6238 | `12f48ab98be36408d6090158d5fc27341ca72d53217fcf892e097fbadab4e70e` | `12f48ab98be36408d6090158d5fc27341ca72d53217fcf892e097fbadab4e70e` |
| `endstation_arty_current/build_plan.md` | 9105 / 9105 | `4eb5e433433f1c3af1311a4585c9a80101178766c8aa9f7573a75d3e034167bf` | `4eb5e433433f1c3af1311a4585c9a80101178766c8aa9f7573a75d3e034167bf` |
| `endstation_arty_current/gptp_ucode.hex` | 13312 / 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| `endstation_arty_current/lwsrp_csr_defaults.svh` | 2187 / 2187 | `d10ce5559b108f54800b8432b672a0d33379721bf2a4edf0058e185484f3881d` | `d10ce5559b108f54800b8432b672a0d33379721bf2a4edf0058e185484f3881d` |
| `endstation_arty_current/lwsrp_table.json` | 2274 / 2274 | `dc4a200fa4dae047598419a78713677aefeab85b957808b9ec7284f2411a668f` | `dc4a200fa4dae047598419a78713677aefeab85b957808b9ec7284f2411a668f` |
| `endstation_arty_current/lwsrp_table.svh` | 3826 / 3826 | `df3c4fa0289d23deea8f8e688573faa1adbb12f8485a7b5613bd30b8b288f8e4` | `df3c4fa0289d23deea8f8e688573faa1adbb12f8485a7b5613bd30b8b288f8e4` |
| `endstation_arty_current/platform_shape.json` | 250 / 250 | `03328f238565f45f775a8fb17921a20ac4172d864b218e3703c23e185e678c99` | `03328f238565f45f775a8fb17921a20ac4172d864b218e3703c23e185e678c99` |
| `endstation_arty_current/soc_params.json` | 498 / 498 | `696350eee365adb614b78e445d6522569e73d0eaa555b4de6603319d45da59cb` | `696350eee365adb614b78e445d6522569e73d0eaa555b4de6603319d45da59cb` |
| `endstation_arty_current/sweep_opts_arty.sh` | 1143 / 1143 | `969f765fe53c592a9fd4afcbb415733fd3ed1c2e367d788faf81e9f2e88ec6c7` | `969f765fe53c592a9fd4afcbb415733fd3ed1c2e367d788faf81e9f2e88ec6c7` |
| `configs/endstation_ax7101_1x1_tdm8.yaml` | 12363 / 12363 | `d2c757e2fcd24d3f494e8c3d2e9f798bf7eba9b7e201741e7125d4f27692c807` | `d2c757e2fcd24d3f494e8c3d2e9f798bf7eba9b7e201741e7125d4f27692c807` |
| `endstation_ax7101_1x1_tdm8/adp_shape_defaults.svh` | 7240 / 7240 | `c6c43feb9ae573103527e71b33be9bb6625b2dbca74d7bb2db1e01c6fd255d3e` | `c6c43feb9ae573103527e71b33be9bb6625b2dbca74d7bb2db1e01c6fd255d3e` |
| `endstation_ax7101_1x1_tdm8/aecp_aem_rom.svh` | 40979 / 40979 | `deea618d789b235c532edc47db08838afc7ffc2f74953f1a117d1fb2c7bd5d33` | `deea618d789b235c532edc47db08838afc7ffc2f74953f1a117d1fb2c7bd5d33` |
| `endstation_ax7101_1x1_tdm8/aem_desc.bin` | 7352 / 7352 | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |
| `endstation_ax7101_1x1_tdm8/aem_desc.json` | 231 / 231 | `bb7bc5f2e15596af864f18b699d44f699acf1d5b5b9ce80f4edd29d655498d5e` | `bb7bc5f2e15596af864f18b699d44f699acf1d5b5b9ce80f4edd29d655498d5e` |
| `endstation_ax7101_1x1_tdm8/aem_desc.map` | 1243 / 1243 | `07151f7c4b493da8e1d3fea32a7e9755951d8e97e021e040ef2a9f3899cb7ede` | `07151f7c4b493da8e1d3fea32a7e9755951d8e97e021e040ef2a9f3899cb7ede` |
| `endstation_ax7101_1x1_tdm8/aem_overlay.json` | 7196 / 7196 | `e148841ac36dbf3e6d6729c49c7c944ed5194adc75941ceb69e3af80b11e3621` | `e148841ac36dbf3e6d6729c49c7c944ed5194adc75941ceb69e3af80b11e3621` |
| `endstation_ax7101_1x1_tdm8/build_plan.md` | 10825 / 10825 | `203c4859f9557b4a250454fe9e0561706cc581708811988cd926edda9b942858` | `203c4859f9557b4a250454fe9e0561706cc581708811988cd926edda9b942858` |
| `endstation_ax7101_1x1_tdm8/gptp_ucode.hex` | 13312 / 13312 | `78c8418a00b35cdae75c459c5269ca3892355507c4dc8af9eb2c29d81b87673b` | `78c8418a00b35cdae75c459c5269ca3892355507c4dc8af9eb2c29d81b87673b` |
| `endstation_ax7101_1x1_tdm8/lwsrp_csr_defaults.svh` | 2190 / 2190 | `0e9df2d455d90782c87546dab4dd1fe7b5fb7f4bc81074e910ba71ddc7016d74` | `0e9df2d455d90782c87546dab4dd1fe7b5fb7f4bc81074e910ba71ddc7016d74` |
| `endstation_ax7101_1x1_tdm8/lwsrp_table.json` | 2289 / 2289 | `61b2e71d9a40c61bfb0eaf884af6257b1b030e441c5f507f99720d0c18dad47d` | `61b2e71d9a40c61bfb0eaf884af6257b1b030e441c5f507f99720d0c18dad47d` |
| `endstation_ax7101_1x1_tdm8/lwsrp_table.svh` | 3832 / 3832 | `8209fdee3cd744d24a066b76017f71f16d87f636c4470eb95e9f986dce550522` | `8209fdee3cd744d24a066b76017f71f16d87f636c4470eb95e9f986dce550522` |
| `endstation_ax7101_1x1_tdm8/platform_shape.json` | 253 / 253 | `0325a3cc988f7f97b34997ef3ac53c6624edfc62b0bd4b5ffb42dc72894ddae7` | `0325a3cc988f7f97b34997ef3ac53c6624edfc62b0bd4b5ffb42dc72894ddae7` |
| `endstation_ax7101_1x1_tdm8/soc_params.json` | 799 / 799 | `d5ec9866f86c339dc1c178c31c7800a359813660d9cbcc95e242e1e29b13c516` | `d5ec9866f86c339dc1c178c31c7800a359813660d9cbcc95e242e1e29b13c516` |
| `endstation_ax7101_1x1_tdm8/sweep_opts_ax7101.sh` | 1366 / 1366 | `515d8610aa1a58f3b2e6b004d63eada43e826886ab420370ac9c45b63697670f` | `515d8610aa1a58f3b2e6b004d63eada43e826886ab420370ac9c45b63697670f` |
| `configs/endstation_ax7101_8x8.yaml` | 19799 / 19799 | `ede309aa78d5eb566e9a3c93a0ef6c843cc181c1d3f2bbe32eda5db62961983e` | `ede309aa78d5eb566e9a3c93a0ef6c843cc181c1d3f2bbe32eda5db62961983e` |
| `endstation_ax7101_8x8/adp_shape_defaults.svh` | 8490 / 8490 | `85939da9c5718d5aacd63ba6be04279e93ad06db16e0f55f2d2f58b7d5926a00` | `85939da9c5718d5aacd63ba6be04279e93ad06db16e0f55f2d2f58b7d5926a00` |
| `endstation_ax7101_8x8/aecp_aem_rom.svh` | 86567 / 86567 | `9f6963190256809964376e8747ebc3465d4b4831df01ec3d91c7e8892e46d755` | `9f6963190256809964376e8747ebc3465d4b4831df01ec3d91c7e8892e46d755` |
| `endstation_ax7101_8x8/aem_desc.bin` | 18288 / 18288 | `193bf18736d23256c1b25d9af1bddb0721d95780fb36a14cf5f91476aff1a2d4` | `193bf18736d23256c1b25d9af1bddb0721d95780fb36a14cf5f91476aff1a2d4` |
| `endstation_ax7101_8x8/aem_desc.json` | 227 / 227 | `7adf2a07b069f4b2bb23f5e8383353f9467b85d4915d1b5069288c3f99203366` | `7adf2a07b069f4b2bb23f5e8383353f9467b85d4915d1b5069288c3f99203366` |
| `endstation_ax7101_8x8/aem_desc.map` | 1244 / 1244 | `14d38a422d09d4b729032b19cfeb515756b30156c22f65df842184956ffd989f` | `14d38a422d09d4b729032b19cfeb515756b30156c22f65df842184956ffd989f` |
| `endstation_ax7101_8x8/aem_overlay.json` | 20163 / 20163 | `baef8bb15a57606b047e657c8ba50460d7f806983a0e08bf24432fc32435fb0c` | `baef8bb15a57606b047e657c8ba50460d7f806983a0e08bf24432fc32435fb0c` |
| `endstation_ax7101_8x8/build_plan.md` | 15175 / 15175 | `2d303d06c5fc2f13648734ea1cb9660963bf745e73ee312476cc3a10c914a20e` | `2d303d06c5fc2f13648734ea1cb9660963bf745e73ee312476cc3a10c914a20e` |
| `endstation_ax7101_8x8/gptp_ucode.hex` | 13312 / 13312 | `78c8418a00b35cdae75c459c5269ca3892355507c4dc8af9eb2c29d81b87673b` | `78c8418a00b35cdae75c459c5269ca3892355507c4dc8af9eb2c29d81b87673b` |
| `endstation_ax7101_8x8/lwsrp_csr_defaults.svh` | 2185 / 2185 | `c9849c561b9aab3f682e2974ce1ba81443c2696a0c1a4e53d3975f2557c159c4` | `c9849c561b9aab3f682e2974ce1ba81443c2696a0c1a4e53d3975f2557c159c4` |
| `endstation_ax7101_8x8/lwsrp_table.json` | 6496 / 6496 | `b525824ef9b4a7c52bc99946b08807708f5c7a0ac9087d20a0cc62f3b5e95266` | `b525824ef9b4a7c52bc99946b08807708f5c7a0ac9087d20a0cc62f3b5e95266` |
| `endstation_ax7101_8x8/lwsrp_table.svh` | 4917 / 4917 | `eed72271ec9a0e3d68b8ca9f367d83251140c5464272a65ef0843a00ce95525e` | `eed72271ec9a0e3d68b8ca9f367d83251140c5464272a65ef0843a00ce95525e` |
| `endstation_ax7101_8x8/platform_shape.json` | 248 / 248 | `a08aef1e775ecd345a7f87157f4bf3eed28306250d49003d0c5231e714e6cf17` | `a08aef1e775ecd345a7f87157f4bf3eed28306250d49003d0c5231e714e6cf17` |
| `endstation_ax7101_8x8/soc_params.json` | 786 / 786 | `41763d46738df0e907116212b9bedb85beebba34f6a66057bee0d921321ef823` | `41763d46738df0e907116212b9bedb85beebba34f6a66057bee0d921321ef823` |
| `endstation_ax7101_8x8/sweep_opts_ax7101.sh` | 1358 / 1358 | `3261424191ebeaa7d5bff89627aa2e47f7d0614aa1d27951e91e228cb99d2ad5` | `3261424191ebeaa7d5bff89627aa2e47f7d0614aa1d27951e91e228cb99d2ad5` |

## Gate table

Every recorded gate below ran from the physical worktree at `44d3ae3b15a0d058abb837c655ad24bd9b64c6e8`.
Commands run in the foreground, without pipelines, with 7200-second per-gate limits.
Markdown uses `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python`.
`gates.jsonl` records command arguments, environment, status, duration, log size and SHA256.
Logs over 200 KB stay outside this output directory.

| Gate | Exact command | rc | Seconds | Log |
|---|---|---|---|---|
| declarations | `python3 sw/builder/test_declarations.py` | 0 | 4.47 | `declarations.log` |
| builder-full | `python3 sw/builder/test_builder.py --require-rv32 --require-elaboration` | 0 | 779.95 | `builder-full.log` |
| compiler-controls | `python3 sw/builder/test_firmware_compiler.py --selftest` | 0 | 1.37 | `compiler-controls.log` |
| compiler-absent | `python3 sw/builder/test_firmware_compiler.py --absent --audit $VALIDATION_STORAGE/595-a417-artifacts-pd_q3_j0/compiler-absent-audit.jsonl` | 0 | 443.96 | `compiler-absent.log` |
| focused-mutants | `python3 $MANAGEMENT/2026-09-23/595-a417/focused_evidence.py` | 0 | 3.77 | `focused-mutants.log` |
| artifact-identity | `python3 $MANAGEMENT/2026-09-23/595-a417/artifact_inventory.py after $VALIDATION_STORAGE/595-a417-artifacts-pd_q3_j0` | 0 | 0.57 | `artifact-identity.log` |
| docs-check | `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/docs_check.py` | 0 | 4.52 | `docs-check.log` |
| docs-check-no-git | `GIT_DIR=/dev/null $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/docs_check.py` | 0 | 4.42 | `docs-check-no-git.log` |
| em-dash | `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/check_em_dash.py --base 1fa2357fcb9b83ad7d6cbeab0c7cc0eb957cdd3a` | 0 | 3.17 | `em-dash.log` |
| doc-style | `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/check_doc_style.py` | 0 | 0.06 | `doc-style.log` |
| doc-style-selftest | `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/check_doc_style.py --selftest` | 0 | 0.06 | `doc-style-selftest.log` |
| toc-selftest | `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/gen_toc.py --selftest` | 0 | 0.82 | `toc-selftest.log` |
| anchors | `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/gen_toc.py --verify-anchors` | 0 | 1.67 | `anchors.log` |
| toc | `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/gen_toc.py --check` | 0 | 2.87 | `toc.log` |
| doc-paths | `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/check_doc_paths.py` | 0 | 0.11 | `doc-paths.log` |
| python-idiom | `python3 scripts/check_py_idiom.py` | 0 | 3.42 | `python-idiom.log` |
| naming | `python3 scripts/measure_naming.py --check` | 0 | 0.46 | `naming.log` |
| diff-worktree | `git diff --check` | 0 | 0.06 | `diff-worktree.log` |
| diff-branch | `git diff --check 1fa2357fcb9b83ad7d6cbeab0c7cc0eb957cdd3a HEAD` | 0 | 0.06 | `diff-branch.log` |

## Acceptance criteria

| Criterion | Evidence | Result |
|---|---|---|
| 1. MAC and declared unsigned string rule | Exact field/quote refusals, quoted-value checks, both callers, explicit nulls | Met |
| 2. Formats list type | Exact list-type refusals at all eight tested stream indices | Met |
| 3. Declaration controls and mutants | 233 loader cases, parser boundaries, three named mutant kills and restored controls | Met |
| 4. Five configurations unchanged | Five input hashes and 70 generated-artifact hashes/sizes agree; raw bytes compared | Met |
| 5. Documentation | Updated MAC docstring, parameter guide and builder contract | Met |

Final integrity: clean worktree at the stated head, one-line commit,
and unchanged processor pin. See `final-integrity.json`.
The local commit tree is `47a89d188ea29c1b02da4919a448423c04acb2eb`.
The final public action is the prepared `REVIEW-READY.md` issue comment.

## Limits and remaining work

The full builder bank reports exactly one unrun arm: gate 11 utilization calibration.
The calibration report is absent from disk. Compiler-absent controls intentionally stand down RV32 instruments.
These are reported stand-downs, not hardware validation.
Before committing, a new capabilities test initially read the orphan legacy ROM.
It failed and was corrected to inspect the final packed descriptor.
All gate claims above concern only the recorded committed head.
Independent reviews, publication, merge-train conflict handling and merge remain with the maintainer.
Issue #577 / PR #612 overlaps this builder; no integration checkout was created.
No review verdict or lens ledger is asserted by the author.
