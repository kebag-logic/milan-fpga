Pin tsn-c-stack <merge commit>: an ENTITY_DISCOVER longer than 56 octets is read by its first 56

Moves `third_party/tsn-c-stack` from `715589c1` to the merge of the ADP length change. Between `715589c1` and that change's base, the stack's `main` moved only in tests and documents.

## What changes

The ADP core reads an ENTITY_DISCOVER whose control_data_length is above 56 by its first 56 octets after entity_id. Below 56 it is discarded and counted, as before. Transmit is unchanged at 56.

Authority: IEEE 1722.1-2021 6.2.2.6 (a transmit rule) and 6.2.7.1.3 (rcvdDiscover has no length condition); Milan v1.2 5.6.3.1 and Table 5.50 (the only discard reason is the entity_id); IEEE 1722-2016 4.4.5.4 (a payload length). Milan v1.2 5.5.2.2 and IEEE 1722.1-2021 7.4.37.1 are the existing tolerance pattern.

## What does not change

- The mailbox filter reads the destination, EtherType, subtype, message type and the entity_id at octet 18; the split tap reads the destination, EtherType and subtype. Neither reads control_data_length, and neither is edited.
- The `adp` channel's `max_frame_bytes` stays 128, so a discover of up to 102 octets of control data in a complete frame reaches the firmware. A longer frame is dropped and counted in RX_DROP, as now.

## Tests (parent side, `parent-consumer.patch`)

- `AdpAdapter.PinRejectsWrongDiscoveryControlLength` expected 57 and 2047 to be refused, so it fails on the new core. It becomes `PinRejectsShortDiscoveryControlLength` (0 and 55, valid_time 0 and 31) and `PinAcceptsLongDiscoveryThroughMailbox`: 57, 84 and 102 with the surplus present and absent, 256 and 2047 with it absent.
- `ctrl_mutants.py`: five plants on the new comparison, each with its named test: the check removed, valid_time counted as length, the mask narrowed to 0x00FF, the previous exact comparison, and 56 refused.

## To do at the bump

- Set the gitlink to the stack's merge commit; add the row to `docs/reference/SUBMODULES.md` and the change log entry, regenerating what they feed.
- Run the complete firmware gate and the stack boundary gate at the final pin.
