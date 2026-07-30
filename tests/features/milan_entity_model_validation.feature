# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Milan v1.2 §5.3.3 (Descriptors), §5.3.8 (Stream Input/Output), §7.2 (Media Clock)
# Offline model: tests/steps/milan_conformance_steps.py
# The model reads the AEM overlay JSON from sw/builder/out/ to validate the
# entity model tree against Milan v1.2 structural constraints.

@milan_conformance @entity_model
Feature: Milan static entity model structural validation

  Milan v1.2 §5.3 defines the mandatory descriptor set and the structural
  constraints between them. The endstation builder (endstation_builder.py)
  emits an AEM overlay JSON that must satisfy these constraints for every
  shipping configuration.

  Background:
    Given the endstation builder is importable
    And the endstation config "endstation_arty_4x4"

  # --- Mandatory descriptors (Milan §5.3.3) ---

  Scenario: the ENTITY descriptor is present and has a valid entity_id
    Then the model has an ENTITY descriptor at index 0
    And the ENTITY descriptor entity_id is non-zero
    And the ENTITY descriptor configurations_count is at least 1

  Scenario: the AUDIO_UNIT descriptor exists and references a CLOCK_DOMAIN
    Then the model has an AUDIO_UNIT descriptor
    And the AUDIO_UNIT descriptor references a valid CLOCK_DOMAIN

  Scenario: each STREAM_INPUT and STREAM_OUTPUT has a valid format
    Then every STREAM_INPUT has a non-zero stream_format
    And every STREAM_OUTPUT has a non-zero stream_format

  # --- Milan §7.2.2: CRF Media Clock Input mandatory at N>=2 AAF listeners ---

  Scenario: a 4x4 config with 2+ AAF listeners has a CRF Media Clock Input
    Then the model has at least 4 STREAM_INPUT descriptors
    And at least 2 STREAM_INPUTs support a Milan Base Audio format
    And the model has a STREAM_INPUT supporting the Milan Media Clock format

  # --- Milan §7.2.3: CRF Media Clock Output mandatory at N>=2 AAF listeners ---

  Scenario: a 4x4 config with 2+ AAF listeners has a CRF Media Clock Output
    Then the model has a STREAM_OUTPUT supporting the Milan Media Clock format

  # --- Milan §5.3.3.9: STREAM_PORT_INPUT has no AUDIO_MAP (dynamic mapping) ---

  Scenario: every STREAM_PORT_INPUT uses dynamic audio mapping
    Then every STREAM_PORT_INPUT has map_mode dynamic
    And no STREAM_PORT_INPUT carries a static AUDIO_MAP descriptor

  # --- Milan §5.3.3.7: each STREAM_PORT has clusters ---

  Scenario: each STREAM_PORT_INPUT has at least one AUDIO_CLUSTER
    Then every STREAM_PORT_INPUT references at least one AUDIO_CLUSTER

  Scenario: each STREAM_PORT_OUTPUT has at least one AUDIO_CLUSTER
    Then every STREAM_PORT_OUTPUT references at least one AUDIO_CLUSTER

  # --- Milan §5.3.3.5: AVB_INTERFACE ---

  Scenario: the model has at least one AVB_INTERFACE descriptor
    Then the model has an AVB_INTERFACE descriptor

  # --- Milan §5.3.3.6: CLOCK_SOURCE ---

  Scenario: the model has at least one CLOCK_SOURCE descriptor
    Then the model has a CLOCK_SOURCE descriptor
    And the CLOCK_SOURCE references a valid CLOCK_DOMAIN

  # --- Channel count consistency ---

  Scenario: the 4x4 config advertises 4 channels per AAF stream
    Then every AAF STREAM_OUTPUT format declares 4 channels
    And every AAF STREAM_INPUT format declares 4 channels

  # --- Same config, different configuration index ---

  Scenario: the 8x8 config advertises 8 channels per AAF stream
    Given the endstation config "endstation_ax7101_8x8"
    Then every AAF STREAM_OUTPUT format declares 8 channels
    And every AAF STREAM_INPUT format declares 8 channels

  Scenario: the 1x1 config advertises 2 channels per AAF stream
    Given the endstation config "endstation_arty_current"
    Then every AAF STREAM_OUTPUT format declares 2 channels

  # --- Firmware version consistency (Milan §5.3.3.1) ---

  Scenario: the firmware version matches the gateware VERSION register
    Then the ENTITY descriptor firmware_version is non-empty
    And the firmware_version is a valid UTF-8 string
    And the firmware_version matches the CSR VERSION register

  # --- ADP shape consistency ---

  Scenario: the ADP advertised stream counts match the AEM model
    Then the ADP talker_stream_sources equals the STREAM_OUTPUT count
    And the ADP listener_stream_sinks equals the STREAM_INPUT count
