# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@aecp @matrix:AECP-3
Feature: the AECP answer contract - served commands, fallback, and two silent cases
  IEEE 1722.1-2021 9.3.5.3.3: "Any command that is received and not
  implemented shall be responded to with a correctly sized response and a
  status of NOT_IMPLEMENTED." NOT_IMPLEMENTED is an ANSWER, not silence, and
  a correctly sized one - so an unimplemented opcode has to produce a
  well-formed AECPDU, never a dropped frame and never a malformed one. The
  protocol-processor's AECP engine satisfies that fallback for unsupported
  opcodes and message types by copying the command payload into the response
  buffer before the microprogram runs and emitting the command's own length
  back. Served opcodes use their command-specific microprograms instead.

  ONE OPCODE IS NOT NOT_IMPLEMENTED. IEEE 7.4.39.2 is opcode-specific:
  "IDENTIFY_NOTIFICATION is only ever sent as an unsolicited response ... If
  an ATDECC Entity ever receives this as a command then it shall return a
  response with the status code BAD_ARGUMENTS." An opcode-specific rule
  governs over 9.3.5.3.3's fallback, so 0x0026 answers BAD_ARGUMENTS. This
  was settled once already against a reading that made it NOT_IMPLEMENTED;
  the scenario below is the standing oracle so it is not re-litigated.

  TWO THINGS GET SILENCE, AND ONLY TWO. A command whose target_entity_id is
  not ours is dropped on the F06.2 MATCHED arc. An AECP RESPONSE arriving as
  input is freed without a reply, because this entity originates no AECP
  command and answering a response is how a control plane builds a storm.
  Both are COUNTED, not lost, and the scenarios below assert that NO frame is
  produced - not that some status came back.

  NOTE ON THE DECODE. The dispatch arms read the 14-bit command_type field at
  AECPDU octets 22 and 23 without consulting the protocol, so a VENDOR_UNIQUE
  command whose protocol_id began 0x00 0x04 would land on the READ_DESCRIPTOR
  microprogram. Milan's protocol_id is 00-1B-C5-0A-C1-00 and does not, which
  is why this is a note and not a scenario.

  WHAT IS DELIBERATELY NOT HERE. This feature does not restore the D1 index
  coverage and D2 non-success size cases the file of this name carried before
  2026-08-12. Those measured GET_STREAM_INFO against READ_DESCRIPTOR and the
  per-command response-size table. GET_STREAM_INFO is served now, and those
  exact response cases are graded by the processor and milan_dp RTL suites.
  Nor does this feature cover ENTITY_AVAILABLE, CONTROLLER_AVAILABLE,
  LOCK_ENTITY or the unsolicited registry. It does not duplicate other
  served-command behavior, including GET_COUNTERS. Those paths are covered by
  their command-specific BDD features and RTL suites.

  This is an OFFLINE model (tests/README.md T1); tests/steps/aecp_engine_steps.py
  lists the submodule sources it mirrors.

  Background:
    Given the protocol-processor AECP engine with the 8-descriptor Milan image

  # ------------------------------------------- the NOT_IMPLEMENTED echo ---
  @class:negative
  Scenario Outline: an unimplemented AEM command is echoed, not dropped
    When the controller sends AEM opcode <opcode> to the AECP engine
    Then the AECP response status is 1
    And the AECP response message_type is the command type plus one
    And the AECP response message_type is 1
    And the AECP response echoes command_type <opcode> with u clear
    And the AECP response carries the command payload verbatim
    And the AECP response control_data_length is 20
    And the AECP response control_data_length counts its own payload
    And the AECP response is well formed against its command
    And the AECP engine counted a command and a response

    # Every row below is an OPEN Milan v1.2 compliance gap: the clause makes
    # the command a SHALL and this engine answers the NOT_IMPLEMENTED echo.
    # When one lands, DELETE its row and add it to the SERVED inventory in
    # tests/steps/aecp_engine_steps.py - never leave it here passing for the
    # wrong reason, which is how this table went stale the last time.
    Examples: Milan SHALL commands this processor has not implemented yet
      | opcode | command                           |
      | 16     | SET_NAME                          |
      | 17     | GET_NAME                          |

    Examples: opcodes with no command behind them at all
      | opcode | command                           |
      | 104    | the last of the 0x0000-0x0068 span|
      | 16383  | 0x3FFF, the reserved top          |

  @class:negative
  Scenario: an ADDRESS_ACCESS command is answered as an ADDRESS_ACCESS response
    When the controller sends an ADDRESS_ACCESS command to the AECP engine
    Then the AECP response message_type is 3
    And the AECP response message_type is the command type plus one
    And the AECP response status is 1
    And the AECP response carries the command payload verbatim
    And the AECP response control_data_length is 22
    And the AECP response is well formed against its command

  @class:negative
  Scenario: a Milan MVU command is answered as a VENDOR_UNIQUE response with its protocol_id intact
    When the controller sends the Milan MVU command to the AECP engine
    Then the AECP response message_type is 7
    And the AECP response message_type is the command type plus one
    And the AECP response status is 1
    And the Milan protocol_id survives the AECP echo whole
    And the AECP response carries the command payload verbatim
    And the AECP response control_data_length is 20
    And the AECP response is well formed against its command

  # An OUI head that collides with an AEM opcode (issue #83). The engine and
  # this model both read @22..@23 as `opcode`, and on a VENDOR_UNIQUE PDU those
  # bytes are the first half of a 48-bit protocol_id. Both dispatched 00-04 to
  # READ_DESCRIPTOR, so the suite and the gateware agreed on the wrong answer.
  # The list is the DISPATCH's opcodes, not a guess: 0x0026 is
  # IDENTIFY_NOTIFICATION, and an earlier attempt at this used 0x0024, which is
  # REGISTER_UNSOLICITED_NOTIFICATION - an opcode, but a guarded one, so it was
  # neither the arm that was broken nor "nothing".
  @class:negative
  Scenario Outline: a VENDOR_UNIQUE protocol_id that collides with an AEM opcode is still NOT_IMPLEMENTED
    When the controller sends a VENDOR_UNIQUE command whose protocol_id starts <oui> to the AECP engine
    Then the AECP response message_type is 7
    And the AECP response status is 1
    And the AECP response protocol_id is echoed whole
    And the AECP response carries the command payload verbatim
    And the AECP response is well formed against its command

    Examples: the AEM opcodes the dispatch names
      | oui    |
      | 0x0004 |
      | 0x0026 |
      | 0x0029 |
      | 0x002B |

    Examples: OUIs with bit 15 set, which the u-bit mask used to eat
      | oui    |
      | 0x8004 |
      | 0xFC1B |

  # VENDOR_UNIQUE is only one of the message types whose @22..@23 is not a
  # command_type. The model may be widened to re-expose AVC_COMMAND (4),
  # HDCP_APM_COMMAND (8), the reserved 10/12 and EXTENDED_COMMAND (14) and stay
  # green unless something sends them, so this outline sweeps the message type
  # as well as the word.
  @class:negative
  Scenario Outline: a NON-AEM message carrying an AEM opcode is NOT_IMPLEMENTED whatever its type
    When the controller sends a message_type <mt> command whose word at 22 is <oui> to the AECP engine
    Then the AECP response status is 1
    And the AECP response protocol_id is echoed whole
    And the AECP response is well formed against its command

    Examples: the residual bucket
      | mt | oui    |
      |  4 | 0x0004 |
      |  4 | 0x0014 |
      |  8 | 0x0004 |
      | 10 | 0x0006 |
      | 12 | 0x0016 |
      | 14 | 0x0018 |

  # --------------------------------------------- 7.4.39.2 beats 9.3.5.3.3 ---
  @class:negative @cmd:IDENTIFY_NOTIFICATION
  Scenario: IDENTIFY_NOTIFICATION arriving as a command is BAD_ARGUMENTS
    When the controller sends AEM opcode 38 to the AECP engine
    Then the AECP response status is 7
    And the AECP response message_type is 1
    And the AECP response echoes command_type 38 with u clear
    And the AECP response carries the command payload verbatim
    And the AECP response control_data_length counts its own payload
    And the AECP response is well formed against its command

  # ------------------------------- START/STOP_STREAMING, the wrong target ---
  # Milan 5.4.2.19/5.4.2.20 implement these per Stream INPUT and require
  # "NOT_SUPPORTED shall be returned" for a Stream Output. 5.3.7.3 says why:
  # the specification "excludes the possibility for a Stream Output to be
  # stopped". IEEE Figure 7-59 gives command and response ONE shape, four
  # bytes of {descriptor_type, descriptor_index}, so the refusal is cdl 16 -
  # the same length as the success - and only NOT_IMPLEMENTED may answer at
  # the command's own size.
  #
  # The SUCCESS path is not modelled here on purpose: it moves state in the
  # ACMP binding record, which this offline model does not carry. It is
  # graded on the real RTL in the protocol processor's pp_top (W21) and end
  # to end, over the wire, in tb/verilator/milan_dp.
  @class:negative @cmd:START_STREAMING
  Scenario Outline: START/STOP_STREAMING on a target that is not a Stream Input
    When the controller sends AEM opcode <opcode> naming descriptor type <dtype> to the AECP engine
    Then the AECP response status is 11
    And the AECP response message_type is 1
    And the AECP response echoes command_type <opcode> with u clear
    # IEEE Figure 7-59 gives command and response ONE shape - four bytes of
    # {descriptor_type, descriptor_index}. Pin the NUMBER, not just internal
    # consistency: a response that shortened its body and its cdl together
    # stays self-consistent and is still the wrong frame on the wire.
    And the AECP response control_data_length is 16
    And the AECP response control_data_length counts its own payload
    And the AECP response is well formed against its command

    Examples: Milan 5.4.2.19/5.4.2.20 - a Stream Output is refused by name
      | opcode | dtype | target        |
      | 34     | 6     | STREAM_OUTPUT |
      | 35     | 6     | STREAM_OUTPUT |

    # ...and so is every other type. That is what keeps a locate on
    # {ENTITY, 0} - a descriptor that EXISTS - out of the write path.
    Examples: every other descriptor type takes the same refusal
      | opcode | dtype | target        |
      | 34     | 0     | ENTITY        |
      | 35     | 0     | ENTITY        |
      | 34     | 26    | CONTROL       |
      | 35     | 26    | CONTROL       |

  # The other half of the partition. Without these rows the outline above
  # holds for a model that answers NOT_SUPPORTED to EVERY target - which is
  # what this model did until the type rule was written into it, and the
  # refusal rows all passed for the wrong reason.
  @class:positive @cmd:START_STREAMING
  Scenario Outline: START/STOP_STREAMING on a Stream Input is served
    When the controller sends AEM opcode <opcode> naming descriptor type 5 to the AECP engine
    Then the AECP response status is 0
    And the AECP response message_type is 1
    And the AECP response echoes command_type <opcode> with u clear
    And the AECP response control_data_length is 16
    And the AECP response control_data_length counts its own payload
    And the AECP response is well formed against its command

    Examples: Milan 5.4.2.19/5.4.2.20 - "for each Stream Input"
      | opcode | command         |
      | 34     | START_STREAMING |
      | 35     | STOP_STREAMING  |

  # ------------------------------------ never silence, never malformed ---
  @class:negative
  Scenario: the whole AEM opcode space answers, and the verdicts partition it
    # The served set is an INVENTORY, not a literal in this file: it lives in
    # tests/steps/aecp_engine_steps.py's SERVED table with a Milan clause per
    # row, and the last step below parses the engine's own opcode localparams
    # and fails if the two disagree. That gate is the point of the scenario.
    # Without it this suite spent three days green while asserting
    # NOT_IMPLEMENTED for twelve commands the RTL had started answering.
    When the controller sweeps AEM opcodes 0 to 104 plus 16383
    Then every swept opcode was answered and none was met with silence
    And every swept answer is well formed against its command
    And the swept opcodes partition into the served set and the NOT_IMPLEMENTED remainder
    And the served inventory matches the opcodes the engine RTL decodes
    And every swept answer carries the command payload verbatim except the served set

  # --------------------------------------------------- silent refusal ---
  @class:negative @silent
  Scenario: a command addressed to another entity gets no frame back
    When a command for entity 0x001B92FFFE00DEAD reaches the AECP engine
    Then the AECP engine emits no frame at all
    And the AECP engine counted a drop and no command

  @class:negative @silent
  Scenario: an entity_id one bit away from ours is still not ours
    When a command for entity 0x001B92FFFE001123 reaches the AECP engine
    Then the AECP engine emits no frame at all
    And the AECP engine counted a drop and no command

  @class:negative @silent
  Scenario Outline: an AECP response arriving as input is never answered
    When an AECP <kind> arrives at the AECP engine as input
    Then the AECP engine emits no frame at all
    And the AECP engine counted a drop and no command

    Examples: every odd message_type is a response, and answering one builds a storm
      | kind                    |
      | AEM response            |
      | ADDRESS_ACCESS response |
      | VENDOR_UNIQUE response  |

  # ----------------------------------------------------- profile refusal ---
  # Milan v1.2 Delta 7 requires ACQUIRE_ENTITY to never succeed and to answer
  # NOT_SUPPORTED (11) with owner_id zero over the 8 octets of the acquire
  # form. The processor selects that refusal for opcode 0x0000, and the root
  # wire harness independently grades its length, addressing, and zero owner.
  @cmd:ACQUIRE_ENTITY
  Scenario: Milan Delta 7 ACQUIRE_ENTITY returns NOT_SUPPORTED with no owner
    When the controller sends ACQUIRE_ENTITY to the AECP engine
    Then the AECP response status is 11
    And the AECP response owner_id is zero, not the acquiring controller
