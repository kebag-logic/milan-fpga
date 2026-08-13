# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@aecp @cmd:READ_DESCRIPTOR @class:getter
Feature: READ_DESCRIPTOR is answered again (IEEE 1722.1-2021 7.4.5)
  On 2026-08-12 this repository's AECP/AEM RTL was deleted and this tier went
  with it, on the premise "this device answers no AECP command at all". The
  protocol-processor submodule then landed its AECP uCPU and the premise
  expired: READ_DESCRIPTOR (0x0004) is the one AEM command this processor
  really answers, out of a static descriptor image, and it answers the two
  failure cases apart from each other.

  THREE ANSWERS, ONE COMMAND. Success is configuration_index, a reserved
  halfword and the descriptor itself, so the AECPDU is 28 + N. A locate that
  finds no such (configuration, type, index) is NO_SUCH_DESCRIPTOR. A
  configuration_index outside configurations_count is BAD_ARGUMENTS, because
  the microprogram range-checks the configuration BEFORE it locates - the two
  statuses come from two different checks and this feature keeps them apart.
  BOTH failures answer the IEEE 7.4.5 four-octet {descriptor_type,
  descriptor_index} stub, "in the same location as in the command frame", so
  a controller can tell which read failed without keeping its own book.

  WHAT IS DELIBERATELY NOT HERE. Everything the submodule still does not
  implement: SET/GET_CLOCK_SOURCE, SET/GET_MAX_TRANSIT_TIME, GET_COUNTERS and
  the Table 5.22 unsolicited push, the audio-map getters and setters, entity
  lock and acquire semantics beyond the generic echo, saved-state persistence
  and SET_CONFIGURATION / NAME / SAMPLING_RATE / STREAM_FORMAT / STREAM_INFO.
  Those features were deleted with the RTL and stay deleted: a scenario that
  asserts an answer nothing gives is a conformance claim with no device
  behind it.

  This is an OFFLINE model (tests/README.md T1) - a Python mirror of the
  shipped command path in tests/steps/aecp_engine_steps.py, which lists the
  submodule sources it was derived from. It proves the CONTRACT, not the
  Verilog; the submodule owns benches for the Verilog.

  Background:
    Given the protocol-processor AECP engine with the 8-descriptor Milan image

  # ------------------------------------------------------------- success ---
  @class:getter
  Scenario: reading ENTITY[0] answers SUCCESS with the whole response shape
    When the controller reads descriptor type 0 index 0 in configuration 0
    Then the AECP response status is 0
    And the AECP response message_type is 1
    And the AECP response echoes command_type 4 with u clear
    And the AECP response target_entity_id is our own
    And the AECP response echoes the sequence_id and the controller_entity_id
    And the AECP response is unicast back to the requester from our own MAC
    And the AECP response configuration_index is 0 and the reserved halfword is zero
    And the AECP response descriptor is 312 octets opening with type 0 index 0
    And the AECP response AECPDU is 340 octets
    And the AECP response control_data_length counts its own payload
    And the AECP response is well formed against its command
    And the AECP engine counted a command and a response

  @class:getter
  Scenario Outline: every descriptor the image directory serves answers SUCCESS
    When the controller reads descriptor type <type> index 0 in configuration 0
    Then the AECP response status is 0
    And the AECP response descriptor is <len> octets opening with type <type> index 0
    And the AECP response AECPDU is <aecpdu> octets
    And the AECP response is well formed against its command

    # The lengths are the submodule TEST VECTOR's (example_milan_8.json), not the
    # shipping entity model's: its streams use Milan v1.2 Annex C Table C.1 on
    # purpose, where shipping descriptors use IEEE 1722.1-2021 Table 7-8. See
    # DescriptorImage.MILAN_8 in steps/aecp_engine_steps.py before changing a row.
    Examples: the docs/architecture/07 section 3.1 tree, lengths from the submodule vector
      | type | len | aecpdu | descriptor    |
      | 0    | 312 | 340    | ENTITY        |
      | 1    | 98  | 126    | CONFIGURATION |
      | 2    | 152 | 180    | AUDIO_UNIT    |
      | 5    | 152 | 180    | STREAM_INPUT  |
      | 6    | 152 | 180    | STREAM_OUTPUT |
      | 9    | 102 | 130    | AVB_INTERFACE |
      | 10   | 86  | 114    | CLOCK_SOURCE  |
      | 36   | 78  | 106    | CLOCK_DOMAIN  |

  @class:getter
  Scenario: the read does not mutate the entity, so two reads agree
    When the controller reads descriptor type 5 index 0 in configuration 0
    Then the AECP response status is 0
    And the AECP response descriptor is 152 octets opening with type 5 index 0
    When the controller reads descriptor type 5 index 0 in configuration 0
    Then the AECP response status is 0
    And the AECP response descriptor is 152 octets opening with type 5 index 0

  # ------------------------------------------------ NO_SUCH_DESCRIPTOR ---
  @class:getter @negative
  Scenario: an unknown descriptor_type is a locate miss, not a bad argument
    When the controller reads descriptor type 255 index 0 in configuration 0
    Then the AECP response status is 2
    And the AECP response carries the 7.4.5 stub for type 255 index 0
    And the AECP response is well formed against its command

  @class:getter @negative
  Scenario Outline: an index past the directory count is a locate miss
    When the controller reads descriptor type <type> index <index> in configuration 0
    Then the AECP response status is 2
    And the AECP response carries the 7.4.5 stub for type <type> index <index>

    Examples: the shipped image is 1 in / 1 out, so index 1 does not exist
      | type | index |
      | 5    | 1     |
      | 6    | 1     |
      | 5    | 255   |
      | 1    | 1     |
      | 36   | 9     |

  # ---------------------------------------------------- BAD_ARGUMENTS ---
  @class:getter @negative
  Scenario: a configuration_index past configurations_count is BAD_ARGUMENTS
    When the controller reads descriptor type 0 index 0 in configuration 1
    Then the AECP response status is 7
    And the AECP response configuration_index is 1 and the reserved halfword is zero
    And the AECP response carries the 7.4.5 stub for type 0 index 0
    And the AECP response is well formed against its command

  @class:getter @negative
  Scenario: the configuration check runs first, so a bad configuration outranks a bad type
    When the controller reads descriptor type 255 index 7 in configuration 9
    Then the AECP response status is 7
    And the AECP response carries the 7.4.5 stub for type 255 index 7

  @class:getter @negative
  Scenario: a configuration that exists but holds nothing is a locate miss, not BAD_ARGUMENTS
    Given the AECP image declares 3 configurations
    When the controller reads descriptor type 0 index 0 in configuration 2
    Then the AECP response status is 2
    And the AECP response configuration_index is 2 and the reserved halfword is zero
    And the AECP response carries the 7.4.5 stub for type 0 index 0

  # ------------------------------------------------- the 7.4.5 stub ---
  @class:getter @negative
  Scenario Outline: both failure paths carry the four-octet 7.4.5 stub, not a success-sized body
    When the controller reads descriptor type <type> index <index> in configuration <cfg>
    Then the AECP response status is <status>
    And the AECP response carries the 7.4.5 stub for type <type> index <index>
    And the AECP response AECPDU is 32 octets
    And the AECP response control_data_length is 20
    And the AECP response control_data_length counts its own payload
    And the AECP response is well formed against its command

    Examples: the locate miss and the bad configuration answer the same shape
      | cfg | type | index | status | path                |
      | 0   | 255  | 0     | 2      | NO_SUCH_DESCRIPTOR  |
      | 0   | 5    | 3     | 2      | NO_SUCH_DESCRIPTOR  |
      | 1   | 0    | 0     | 7      | BAD_ARGUMENTS       |
      | 64  | 6    | 2     | 7      | BAD_ARGUMENTS       |

  # -------------------------------------------------- the short command ---
  @class:getter @negative
  Scenario Outline: a READ_DESCRIPTOR too short to carry its operands is BAD_ARGUMENTS
    When the controller sends a READ_DESCRIPTOR of control_data_length <cdl>
    Then the AECP response status is 7
    And the AECP response message_type is 1
    And the AECP response carries the command payload verbatim
    And the AECP response is well formed against its command

    Examples: 20 is the first length that carries configuration, reserved, type and index
      | cdl |
      | 12  |
      | 16  |
      | 19  |

  @class:getter
  Scenario: control_data_length 20 is long enough, and is served
    When the controller sends a READ_DESCRIPTOR of control_data_length 20
    Then the AECP response status is 0
    And the AECP response descriptor is 312 octets opening with type 0 index 0

  # --------------------------------------------------- the unloaded image ---
  # The store validates magic + layout version + checksum before it serves
  # anything, and until it agrees, region 0xD reads zero. The microprogram
  # meets that zero at its configuration range check, BEFORE any locate, so an
  # unloaded image answers BAD_ARGUMENTS - not the NO_SUCH_DESCRIPTOR the
  # store's own banner prose predicts for "software has not loaded the image
  # yet". Pinned here as the behaviour that ships, so the divergence between
  # the prose and the microprogram cannot drift unnoticed in either direction.
  @class:getter @negative
  Scenario: before software loads the image, every read is refused and none is silent
    Given the protocol-processor AECP engine before software loads the image
    When the controller reads descriptor type 0 index 0 in configuration 0
    Then the AECP response status is 7
    And the AECP response carries the 7.4.5 stub for type 0 index 0
    And the AECP response is well formed against its command
    And the AECP engine counted a command and a response
