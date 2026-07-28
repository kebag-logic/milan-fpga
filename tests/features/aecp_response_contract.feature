# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@item10 @cmd:STREAM_INFO @matrix:CMD-7 @matrix:AECP-2 @matrix:AECP-3 @silicon:0x0016
Feature: AECP response contract - index coverage (D1) and non-success size (D2)
  Two defects measured on silicon 2026-07-27 against gateware 0x0001_0016, both invisible
  to every desk gate that was green at the time (57/57 Verilator suites, yosys 48/48,
  behave 113/113, lint at ratchet) because our own tools read the AEM STATUS BYTE and moved
  on. Hive also validates the RESPONSE FRAME, and called the entity "not fully Milan
  compliant" fifteen times.

  D1 INDEX COVERAGE. READ_DESCRIPTOR served STREAM_OUTPUT.0-8 and STREAM_INPUT.0-8
  byte-exact while GET_STREAM_INFO answered NO_SUCH_DESCRIPTOR on 1-8 (Hive: 8x
  STREAM_OUTPUT + 7x STREAM_INPUT). IEEE 1722.1-2021 7.4.16.2 defines one
  GET_STREAM_INFO_RESPONSE per {descriptor_type, descriptor_index}, and 7.4.5 makes the
  descriptor directory the statement of which of those pairs exist, so the two commands
  must consult the same oracle. This is only visible in a MULTI-STREAM shape - at 1 in /
  1 out there is no index 1 to get wrong, which is why the shipped testbench missed it.

  D2 NON-SUCCESS RESPONSE SIZE. A non-success AEM response still carries the full response
  payload for its command; only NOT_IMPLEMENTED reflects the COMMAND. The rule is taken
  from the controller stack that raises the log line (L-Acoustics avdecc
  src/protocol/protocolAemPayloads.cpp checkResponsePayload) and from that library's
  per-command size constants, each tagged with the IEEE clause it came from - the IEEE and
  Milan texts themselves are paywalled and are NOT in this repo, so no sentence of them is
  quoted here. Calibrated against the Milan-validated reference device 3CC0C60102030000,
  which answers a non-existent descriptor with the SUCCESS-sized 68-byte response
  (2026-07-28); an earlier version of our compliance tool asserted "a non-success response
  echoes the COMMAND" and that device refuted it.

  Background:
    Given a fresh Milan AECP model

  # ------------------------------------------------------------------ D1 ---
  @class:getter @matrix:CMD-7
  Scenario Outline: every STREAM_OUTPUT the directory serves answers GET_STREAM_INFO
    Given the entity model has 9 STREAM_INPUT and 9 STREAM_OUTPUT descriptors
    Then READ_DESCRIPTOR and GET_STREAM_INFO agree for 6 index <index>
    And the model responds status 0

    Examples: the 8x8 ship shape - 8 AAF sources plus the CRF source
      | index |
      | 0 |
      | 1 |
      | 2 |
      | 3 |
      | 4 |
      | 5 |
      | 6 |
      | 7 |
      | 8 |

  @class:getter @matrix:CMD-7
  Scenario Outline: every STREAM_INPUT the directory serves answers GET_STREAM_INFO
    Given the entity model has 9 STREAM_INPUT and 9 STREAM_OUTPUT descriptors
    Then READ_DESCRIPTOR and GET_STREAM_INFO agree for 5 index <index>
    And the model responds status 0

    Examples: the 8x8 ship shape - 8 AAF sinks plus the CRF sink
      | index |
      | 0 |
      | 1 |
      | 2 |
      | 3 |
      | 4 |
      | 5 |
      | 6 |
      | 7 |
      | 8 |

  @class:getter @negative
  Scenario Outline: an index past the directory is refused by BOTH commands
    Given the entity model has 9 STREAM_INPUT and 9 STREAM_OUTPUT descriptors
    Then READ_DESCRIPTOR and GET_STREAM_INFO agree for <type> index <index>
    And the model responds status 2

    Examples: out of range - the refusal must also be consistent
      | type | index |
      | 6 | 9 |
      | 6 | 10 |
      | 6 | 255 |
      | 5 | 9 |
      | 5 | 64 |

  @class:getter @negative
  Scenario: the deployed 1x1 shape keeps refusing index 1 on both commands
    Then READ_DESCRIPTOR and GET_STREAM_INFO agree for 6 index 1
    And the model responds status 2

  # ------------------------------------------------------------------ D2 ---
  @class:getter @matrix:AECP-3
  Scenario Outline: the clause fixes the response size, and the status does not change it
    Then the modelled response control_data_length for command <cmd> is <cdl>

    Examples: clause response sizes (control_data_length = payload + 12)
      | cmd | cdl | clause                                       |
      | 15  | 68  | 7.4.16.2 / Milan 7.3.10 GET_STREAM_INFO 56 B |
      | 9   | 24  | 7.4.10.2 GET_STREAM_FORMAT 12 B              |
      | 17  | 84  | 7.4.18.2 GET_NAME 72 B                       |
      | 16  | 84  | 7.4.17.1 SET_NAME 72 B                       |
      | 21  | 20  | 7.4.22.2 GET_SAMPLING_RATE 8 B               |
      | 23  | 20  | 7.4.24.2 GET_CLOCK_SOURCE 8 B                |
      | 41  | 148 | 7.4.42.2 GET_COUNTERS 136 B                  |
      | 39  | 32  | 7.4.40.2 GET_AVB_INFO 20 B minimum           |
      | 40  | 16  | 7.4.41.2 GET_AS_PATH 4 B minimum             |
      | 43  | 24  | 7.4.44.2 GET_AUDIO_MAP 12 B minimum          |

  @class:getter @negative @matrix:AECP-3
  Scenario: a refused GET_STREAM_INFO is the same size as an accepted one
    Given the entity model has 9 STREAM_INPUT and 9 STREAM_OUTPUT descriptors
    Then READ_DESCRIPTOR and GET_STREAM_INFO agree for 6 index 90
    And the model responds status 2
    And the modelled response control_data_length for command 15 is 68
