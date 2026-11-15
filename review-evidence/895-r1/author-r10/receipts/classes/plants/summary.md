# Arm B aecp-fanout records by class (round 10, R836-4-F2)

## 1x1/1if: R8-B1

| Record start (bus cycles) | Command | Status | Class | CPU cycles | Rule us | Stated us | Held (command passed) | Held (round 8 survey call) |
|---:|---|---:|---|---:|---:|---:|---|---|
| 79898229 | 0x2d REMOVE_AUDIO_MAPPINGS, paced | 0 | paced | 22,183 | 235 | 300 | True | True |
| 80708503 | 0x2c ADD_AUDIO_MAPPINGS, paced | 0 | paced | 20,224 | 215 | 300 | True | True |
| 81612689 | 0x2d REMOVE_AUDIO_MAPPINGS, paced | 0 | paced | 23,877 | 255 | 300 | True | True |
| 82516495 | 0x2c ADD_AUDIO_MAPPINGS, paced | 0 | paced | 22,138 | 235 | 300 | True | True |
| 84037557 | 0x06 SET_CONFIGURATION, paced | 0 | paced | 28,288 | 300 | 300 | True | True |
| 84916859 | 0x0e command 0x000e | 0 | other | 20,363 | 215 | 235 | True | False |

## 8x8/2if: R8-B8

| Record start (bus cycles) | Command | Status | Class | CPU cycles | Rule us | Stated us | Held (command passed) | Held (round 8 survey call) |
|---:|---|---:|---|---:|---:|---:|---|---|
| 96100476 | 0x2d REMOVE_AUDIO_MAPPINGS, paced | 0 | paced | 28,627 | 305 | 595 | True | True |
| 97037257 | 0x2c ADD_AUDIO_MAPPINGS, paced | 0 | paced | 26,480 | 280 | 595 | True | True |
| 98604619 | 0x06 SET_CONFIGURATION, paced | 0 | paced | 55,365 | 585 | 595 | True | True |
| 99510230 | 0x0e command 0x000e | 0 | other | 17,511 | 185 | 265 | True | False |
| 104472378 | 0x2d REMOVE_AUDIO_MAPPINGS, paced | 0 | paced | 27,702 | 295 | 595 | True | True |
| 105318397 | 0x2c ADD_AUDIO_MAPPINGS, paced | 0 | paced | 26,157 | 275 | 595 | True | True |
| 106223347 | 0x0e command 0x000e | 0 | other | 17,300 | 185 | 265 | True | False |

## The planted controls on the real pass's evidence path

| Plant | Point | Raised record | Evidence path | rc | Its line |
|---|---|---|---|---:|---|
| control | 1x1/1if | none | record_classes.py (every leg, both points) | 0 | RESULT: PASS |
| control | 1x1/1if | none | corrected survey | 0 | UNDER 0 |
| control | 1x1/1if | none | round 8 survey | 0 | UNDER 0 |
| control | 8x8/2if | none | record_classes.py (every leg, both points) | 0 | RESULT: PASS |
| control | 8x8/2if | none | corrected survey | 0 | UNDER 0 |
| control | 8x8/2if | none | round 8 survey | 0 | UNDER 0 |
| paced-over | 1x1/1if | SET_CONFIGURATION accepted -> 40,000 cycles | record_classes.py (every leg, both points) | 1 | REFUSED 1x1/1if answering-ports aecp-fanout: a record of 40,000 CPU cycles, 420 us by the rule, over the paced record's 300 us (SET_CONFIGURATION, paced) |
| paced-over | 1x1/1if | SET_CONFIGURATION accepted -> 40,000 cycles | corrected survey | 1 | | edit_rows.EDIT_RECORD_US | record.aecp.edit | 300 | 40,000 | 420 | classes.paced: B/aecp-fanout (SET_CONFIGURATION, paced) | UNDER by 120 | |
| paced-over | 1x1/1if | SET_CONFIGURATION accepted -> 40,000 cycles | round 8 survey | 0 | UNDER 0 |
| stream-info-over | 1x1/1if | SET_STREAM_INFO -> 30,000 cycles | record_classes.py (every leg, both points) | 1 | REFUSED 1x1/1if answering-ports aecp-fanout: a record of 30,000 CPU cycles, 315 us by the rule, over the other record's 235 us (command 0x000e) |
| stream-info-over | 1x1/1if | SET_STREAM_INFO -> 30,000 cycles | corrected survey | 1 | | load_grade.STATED_US | record.aecp | 235 | 30,000 | 315 | classes.other: B/aecp-fanout (command 0x000e) | UNDER by 80 | |
| stream-info-over | 1x1/1if | SET_STREAM_INFO -> 30,000 cycles | round 8 survey | 0 | UNDER 0 |
| paced-over | 8x8/2if | SET_CONFIGURATION accepted -> 60,000 cycles | record_classes.py (every leg, both points) | 1 | REFUSED 8x8/2if answering-ports aecp-fanout: a record of 60,000 CPU cycles, 630 us by the rule, over the paced record's 595 us (SET_CONFIGURATION, paced) |
| paced-over | 8x8/2if | SET_CONFIGURATION accepted -> 60,000 cycles | corrected survey | 1 | | edit_rows.EDIT_RECORD_US | record.aecp.edit | 595 | 60,000 | 630 | classes.paced: B/aecp-fanout (SET_CONFIGURATION, paced) | UNDER by 35 | |
| paced-over | 8x8/2if | SET_CONFIGURATION accepted -> 60,000 cycles | round 8 survey | 0 | UNDER 0 |
| stream-info-over | 8x8/2if | SET_STREAM_INFO -> 30,000 cycles | record_classes.py (every leg, both points) | 1 | REFUSED 8x8/2if answering-ports aecp-fanout: a record of 30,000 CPU cycles, 315 us by the rule, over the other record's 265 us (command 0x000e) |
| stream-info-over | 8x8/2if | SET_STREAM_INFO -> 30,000 cycles | corrected survey | 1 | | load_grade.STATED_US | record.aecp | 265 | 30,000 | 315 | classes.other: B/aecp-fanout (command 0x000e) | UNDER by 50 | |
| stream-info-over | 8x8/2if | SET_STREAM_INFO -> 30,000 cycles | round 8 survey | 0 | UNDER 0 |
