# #98 parser mutants: named checks and every FAIL line

## a TLV ahead of the information TLV refuses the Follow_Up (#98)

rc 1; 482 checks: 467 PASS, 15 FAIL; named 6, missed 0

Named: `#98 unknown TLV first: event`; `#98 three unknown TLVs first: event`; `#98 unknown TLV first, padded: event`; `#98 second information TLV: event`; `#98 identifiers at octet 6: event`; `#98 unknown TLV first: no drop`

```
FAIL #98 unknown TLV first: event got 0000000000000000 exp 0000000000000002
FAIL #98 unknown TLV first: w11 as the plain case got ffffffffffffffff exp fffff00000070000
FAIL #98 unknown TLV first: no drop got 0000000000000011 exp 0000000000000010
FAIL #98 three unknown TLVs first: event got 0000000000000000 exp 0000000000000002
FAIL #98 three unknown TLVs first: w11 as the plain case got ffffffffffffffff exp fffff00000070000
FAIL #98 three unknown TLVs first: no drop got 0000000000000012 exp 0000000000000011
FAIL #98 unknown TLV first, padded: event got 0000000000000000 exp 0000000000000002
FAIL #98 unknown TLV first, padded: w11 as the plain case got ffffffffffffffff exp fffff00000070000
FAIL #98 unknown TLV first, padded: no drop got 0000000000000013 exp 0000000000000012
FAIL #98 second information TLV: event got 0000000000000000 exp 0000000000000002
FAIL #98 second information TLV: w11 as the plain case got ffffffffffffffff exp fffff00000070000
FAIL #98 second information TLV: no drop got 0000000000000014 exp 0000000000000013
FAIL #98 identifiers at octet 6: event got 0000000000000000 exp 0000000000000002
FAIL #98 identifiers at octet 6: w11 as the plain case got ffffffffffffffff exp fffff00000070000
FAIL #98 identifiers at octet 6: no drop got 0000000000000015 exp 0000000000000014
```

## word 11 read at the fixed octets 68..73 (#98)

rc 1; 482 checks: 473 PASS, 9 FAIL; named 2, missed 0

Named: `#98 unknown TLV first: w11 as the plain case`; `#98 three unknown TLVs first: w11 as the plain case`

```
FAIL #98 unknown TLV first: w11 as the plain case got ffffffffffffffff exp fffff00000070000
FAIL #98 three unknown TLVs first: w11 as the plain case got 3333333333330000 exp fffff00000070000
FAIL #98 unknown TLV first, padded: w11 as the plain case got ffffffffffffffff exp fffff00000070000
FAIL #98 second information TLV: w11 as the plain case got ffffffffffffffff exp fffff00000070000
FAIL #98 identifiers at octet 6: w11 as the plain case got 0001111111110000 exp fffff00000070000
FAIL #98 information TLV with lengthField 30: no w11 write got 0000000000000001 exp 0000000000000000
FAIL fu tlvType 0x0008 drop: no w11 write got 0000000000000001 exp 0000000000000000
FAIL fu orgId 00-1B-19 drop: no w11 write got 0000000000000001 exp 0000000000000000
FAIL fu orgSubType 2 drop: no w11 write got 0000000000000001 exp 0000000000000000
```

## word 11 read two octets late (#98)

rc 1; 482 checks: 470 PASS, 12 FAIL; named 3, missed 0

Named: `#98 plain fu: w11 as the plain case`; `fu w11`; `#98 unknown TLV first: w11 as the plain case`

```
FAIL fu w11                   got f000000700000000 exp fffff00000070000
FAIL #98 plain fu: w11 as the plain case got f000000700000000 exp fffff00000070000
FAIL #98 unknown TLV first: w11 as the plain case got f000000700000000 exp fffff00000070000
FAIL #98 three unknown TLVs first: w11 as the plain case got f000000700000000 exp fffff00000070000
FAIL #98 unknown TLV first, padded: w11 as the plain case got f000000700000000 exp fffff00000070000
FAIL #98 second information TLV: w11 as the plain case got f000000700000000 exp fffff00000070000
FAIL #98 unknown TLVs after: w11 as the plain case got f000000700000000 exp fffff00000070000
FAIL #98 identifiers at octet 6: w11 as the plain case got f000000700000000 exp fffff00000070000
FAIL complete fu after the arms: w11 got f000000700000000 exp fffff00000070000
FAIL fu with a trailing TLV: w11 got f000000700000000 exp fffff00000070000
FAIL fu after a refused fu: every word is this frame's got 0000000000000006 exp 0000000000000007
FAIL fu after a refused pdresp: every word is this frame's got 0000000000000006 exp 0000000000000007
```

## a Follow_Up is accepted without its information TLV (#98)

rc 1; 482 checks: 471 PASS, 11 FAIL; named 5, missed 0

Named: `#98 no information TLV: no event`; `#98 no information TLV: one drop`; `fu tlvType 0x0008 drop: no event`; `fu orgId 00-1B-19 drop: no event`; `fu orgSubType 2 drop: no event`

```
FAIL #98 no information TLV: no event got 0000000000000001 exp 0000000000000000
FAIL #98 no information TLV: one drop got 0000000000000010 exp 0000000000000011
FAIL #98 information TLV with lengthField 30: no event got 0000000000000001 exp 0000000000000000
FAIL #98 information TLV with lengthField 30: one drop got 000000000000001c exp 000000000000001d
FAIL fu tlvType 0x0008 drop: no event got 0000000000000001 exp 0000000000000000
FAIL fu tlvType 0x0008 drop: one drop got 0000000000000029 exp 000000000000002a
FAIL fu orgId 00-1B-19 drop: no event got 0000000000000001 exp 0000000000000000
FAIL fu orgId 00-1B-19 drop: one drop got 000000000000002a exp 000000000000002b
FAIL fu orgSubType 2 drop: no event got 0000000000000001 exp 0000000000000000
FAIL fu orgSubType 2 drop: one drop got 000000000000002a exp 000000000000002b
FAIL drop count advanced      got 0000000000000045 exp 0000000000000048
```

## a TLV value past messageLength is walked (#98)

rc 1; 482 checks: 477 PASS, 5 FAIL; named 5, missed 0

Named: `#98 information TLV past messageLength: no event`; `#98 information TLV past messageLength: one drop`; `#98 information TLV past messageLength: no w11 write`; `#98 trailing TLV past messageLength: no event`; `#98 trailing TLV past messageLength: one drop`

```
FAIL #98 information TLV past messageLength: no event got 0000000000000001 exp 0000000000000000
FAIL #98 information TLV past messageLength: one drop got 0000000000000011 exp 0000000000000012
FAIL #98 information TLV past messageLength: no w11 write got 0000000000000001 exp 0000000000000000
FAIL #98 trailing TLV past messageLength: no event got 0000000000000001 exp 0000000000000000
FAIL #98 trailing TLV past messageLength: one drop got 0000000000000012 exp 0000000000000013
```

## a malformed TLV header does not latch the refusal (#98)

rc 1; 482 checks: 476 PASS, 6 FAIL; named 6, missed 0

Named: `#98 TLV past messageLength ahead of the information TLV: no event`; `#98 TLV past messageLength ahead of the information TLV: one drop`; `#98 TLV past messageLength ahead of the information TLV: no w11 write`; `#98 odd lengthField ahead of the information TLV: no event`; `#98 odd lengthField ahead of the information TLV: one drop`; `#98 odd lengthField ahead of the information TLV: no w11 write`

```
FAIL #98 TLV past messageLength ahead of the information TLV: no event got 0000000000000001 exp 0000000000000000
FAIL #98 TLV past messageLength ahead of the information TLV: one drop got 000000000000001b exp 000000000000001c
FAIL #98 TLV past messageLength ahead of the information TLV: no w11 write got 0000000000000001 exp 0000000000000000
FAIL #98 odd lengthField ahead of the information TLV: no event got 0000000000000001 exp 0000000000000000
FAIL #98 odd lengthField ahead of the information TLV: one drop got 000000000000001b exp 000000000000001c
FAIL #98 odd lengthField ahead of the information TLV: no w11 write got 0000000000000001 exp 0000000000000000
```

## an EOF header's own overrun is not refused (#98)

rc 1; 482 checks: 480 PASS, 2 FAIL; named 2, missed 0

Named: `#98 header ends messageLength, value to come: no event`; `#98 header ends messageLength, value to come: one drop`

```
FAIL #98 header ends messageLength, value to come: no event got 0000000000000001 exp 0000000000000000
FAIL #98 header ends messageLength, value to come: one drop got 0000000000000012 exp 0000000000000013
```

## an odd lengthField is walked (#98)

rc 1; 482 checks: 479 PASS, 3 FAIL; named 3, missed 0

Named: `#98 odd lengthField: no event`; `#98 odd lengthField: one drop`; `#98 odd lengthField: no w11 write`

```
FAIL #98 odd lengthField: no event got 0000000000000001 exp 0000000000000000
FAIL #98 odd lengthField: one drop got 000000000000001a exp 000000000000001b
FAIL #98 odd lengthField: no w11 write got 0000000000000001 exp 0000000000000000
```

## a TLV header cut by messageLength is accepted (#98)

rc 1; 482 checks: 470 PASS, 12 FAIL; named 6, missed 0

Named: `#98 header cut after 1 octet(s): no event`; `#98 header cut after 1 octet(s), padded: no event`; `#98 header cut after 2 octet(s): no event`; `#98 header cut after 2 octet(s), padded: no event`; `#98 header cut after 3 octet(s): no event`; `#98 header cut after 3 octet(s), padded: no event`

```
FAIL #98 header cut after 1 octet(s): no event got 0000000000000001 exp 0000000000000000
FAIL #98 header cut after 1 octet(s): one drop got 0000000000000014 exp 0000000000000015
FAIL #98 header cut after 1 octet(s), padded: no event got 0000000000000001 exp 0000000000000000
FAIL #98 header cut after 1 octet(s), padded: one drop got 0000000000000014 exp 0000000000000015
FAIL #98 header cut after 2 octet(s): no event got 0000000000000001 exp 0000000000000000
FAIL #98 header cut after 2 octet(s): one drop got 0000000000000014 exp 0000000000000015
FAIL #98 header cut after 2 octet(s), padded: no event got 0000000000000001 exp 0000000000000000
FAIL #98 header cut after 2 octet(s), padded: one drop got 0000000000000014 exp 0000000000000015
FAIL #98 header cut after 3 octet(s): no event got 0000000000000001 exp 0000000000000000
FAIL #98 header cut after 3 octet(s): one drop got 0000000000000014 exp 0000000000000015
FAIL #98 header cut after 3 octet(s), padded: no event got 0000000000000001 exp 0000000000000000
FAIL #98 header cut after 3 octet(s), padded: one drop got 0000000000000014 exp 0000000000000015
```

## the walk reads padding past messageLength as a header (#98)

rc 1; 482 checks: 480 PASS, 2 FAIL; named 2, missed 0

Named: `#98 unknown TLV first, padded: event`; `#98 unknown TLV first, padded: no drop`

```
FAIL #98 unknown TLV first, padded: event got 0000000000000000 exp 0000000000000002
FAIL #98 unknown TLV first, padded: no drop got 0000000000000011 exp 0000000000000010
```

## a later information TLV is read again (#98)

rc 1; 482 checks: 481 PASS, 1 FAIL; named 1, missed 0

Named: `#98 second information TLV: w11 as the plain case`

```
FAIL #98 second information TLV: w11 as the plain case got 00000fff00090000 exp fffff00000070000
```

## a zero-length TLV ends the walk (#98)

rc 1; 482 checks: 479 PASS, 3 FAIL; named 2, missed 0

Named: `#98 three unknown TLVs first: event`; `#98 three unknown TLVs first: no drop`

```
FAIL #98 three unknown TLVs first: event got 0000000000000000 exp 0000000000000002
FAIL #98 three unknown TLVs first: w11 as the plain case got ffffffffffffffff exp fffff00000070000
FAIL #98 three unknown TLVs first: no drop got 0000000000000011 exp 0000000000000010
```

## the information TLV is named without its organizationId and subtype (#98)

rc 1; 482 checks: 471 PASS, 11 FAIL; named 4, missed 0

Named: `#98 three unknown TLVs first: w11 as the plain case`; `#98 no information TLV: no event`; `fu orgId 00-1B-19 drop: no event`; `fu orgSubType 2 drop: no event`

```
FAIL #98 three unknown TLVs first: w11 as the plain case got 1111111122220000 exp fffff00000070000
FAIL #98 no information TLV: no event got 0000000000000001 exp 0000000000000000
FAIL #98 no information TLV: one drop got 0000000000000010 exp 0000000000000011
FAIL #98 no information TLV: no w11 write got 0000000000000001 exp 0000000000000000
FAIL fu orgId 00-1B-19 drop: no event got 0000000000000001 exp 0000000000000000
FAIL fu orgId 00-1B-19 drop: no w11 write got 0000000000000001 exp 0000000000000000
FAIL fu orgId 00-1B-19 drop: one drop got 000000000000002c exp 000000000000002d
FAIL fu orgSubType 2 drop: no event got 0000000000000001 exp 0000000000000000
FAIL fu orgSubType 2 drop: no w11 write got 0000000000000001 exp 0000000000000000
FAIL fu orgSubType 2 drop: one drop got 000000000000002c exp 000000000000002d
FAIL drop count advanced      got 0000000000000047 exp 0000000000000049
```

## the information TLV is named without its tlvType (#98)

rc 1; 482 checks: 478 PASS, 4 FAIL; named 3, missed 0

Named: `fu tlvType 0x0008 drop: no event`; `fu tlvType 0x0008 drop: one drop`; `fu tlvType 0x0008 drop: no w11 write`

```
FAIL fu tlvType 0x0008 drop: no event got 0000000000000001 exp 0000000000000000
FAIL fu tlvType 0x0008 drop: no w11 write got 0000000000000001 exp 0000000000000000
FAIL fu tlvType 0x0008 drop: one drop got 000000000000002b exp 000000000000002c
FAIL drop count advanced      got 0000000000000049 exp 000000000000004a
```

## the information TLV is named without its lengthField (#98)

rc 1; 482 checks: 481 PASS, 1 FAIL; named 1, missed 0

Named: `#98 identifiers at octet 6: w11 as the plain case`

```
FAIL #98 identifiers at octet 6: w11 as the plain case got 1111111122220000 exp fffff00000070000
```

## the information TLV is named by any lengthField of 28 or more (#98)

rc 1; 482 checks: 479 PASS, 3 FAIL; named 3, missed 0

Named: `#98 information TLV with lengthField 30: no event`; `#98 information TLV with lengthField 30: one drop`; `#98 information TLV with lengthField 30: no w11 write`

```
FAIL #98 information TLV with lengthField 30: no event got 0000000000000001 exp 0000000000000000
FAIL #98 information TLV with lengthField 30: one drop got 000000000000001d exp 000000000000001e
FAIL #98 information TLV with lengthField 30: no w11 write got 0000000000000001 exp 0000000000000000
```

## a complete header ending on the last declared octet is read as cut (#98)

rc 1; 482 checks: 480 PASS, 2 FAIL; named 2, missed 0

Named: `#98 unknown TLVs after: event`; `#98 unknown TLVs after: no drop`

```
FAIL #98 unknown TLVs after: event got 0000000000000000 exp 0000000000000002
FAIL #98 unknown TLVs after: no drop got 0000000000000011 exp 0000000000000010
```

## a zero-length TLV after the information TLV refuses the Follow_Up (#98)

rc 1; 482 checks: 480 PASS, 2 FAIL; named 2, missed 0

Named: `#98 unknown TLVs after: event`; `#98 unknown TLVs after: no drop`

```
FAIL #98 unknown TLVs after: event got 0000000000000000 exp 0000000000000002
FAIL #98 unknown TLVs after: no drop got 0000000000000011 exp 0000000000000010
```

## the last declared octet is not walked as a header byte (#98)

rc 1; 482 checks: 476 PASS, 6 FAIL; named 2, missed 0

Named: `#98 unknown TLVs after: event`; `#98 unknown TLVs after: no drop`

```
FAIL #98 unknown TLVs after: event got 0000000000000000 exp 0000000000000002
FAIL #98 unknown TLVs after: no drop got 0000000000000011 exp 0000000000000010
FAIL #98 header cut after 1 octet(s): no event got 0000000000000001 exp 0000000000000000
FAIL #98 header cut after 1 octet(s): one drop got 0000000000000015 exp 0000000000000016
FAIL #98 header cut after 1 octet(s), padded: no event got 0000000000000001 exp 0000000000000000
FAIL #98 header cut after 1 octet(s), padded: one drop got 0000000000000015 exp 0000000000000016
```

