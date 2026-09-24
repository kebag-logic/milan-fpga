[A290]

Authority checked independently: Milan Specification Consolidated v1.2,
Final Approved 2023-11-30. Source file basename:
`Milan_Specification_Consolidated_v1.2_Final_Approved 20231130.pdf`.
SHA-256: `6bb902be1c1de8c44f4c4c583a645b0b37e0b2dac27870486ce229e68ce3bba8`.

| Clause | Printed page | Finding |
|---|---|---|
| 5.4.4.2 | 58 | SET_SYSTEM_UNIQUE_ID support is introduced as a recommendation; Figure 5.5 command is 40 bytes |
| 5.4.4.3 | 59 | GET_SYSTEM_UNIQUE_ID has the same recommendation note; its command uses Figure 5.3, 32 bytes |
| 5.4.4.4 | 59–60 | SET_MEDIA_CLOCK_REFERENCE_INFO has the same recommendation note; Figure 5.6 command is 104 bytes |
| 5.4.4.5 | 61 | GET_MEDIA_CLOCK_REFERENCE_INFO has the same recommendation note; Figure 5.7 command is 32 bytes |
| 7.6 | 115 | Media Clock Management has the same recommendation note; 7.6.1–7.6.2 describe priorities and domain names |
| Table 5.19 | 55 | Status 1 means the command type is unsupported; status 0 reports successful execution |
| Table 5.20 | 58 | The only defined capability flags concern redundancy and changing talker mappings while running; neither waived command pair has a flag |

The command sections also contain implementation language after their recommendation
notes. The notes expressly qualify feature support in this version. The
[owner decision](https://github.com/kebag-logic/milan-fpga/issues/510#issuecomment-5789766089)
selects the October waiver and a P4 revisit if the conformance lab requires it.

The response lengths recorded by this change are the current engine's command
reflection behavior, verified from emitted frames. The standard's successful
GET response formats are longer; the waiver does not claim those formats or
their state semantics are implemented. The separate timing issue #57 remains open.
