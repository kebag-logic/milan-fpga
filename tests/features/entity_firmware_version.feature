# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# The ENTITY descriptor's firmware_version, read the way a controller reads it.
#
# IEEE 1722.1-2021 7.2.1 Table 7-2 places firmware_version at ENTITY offset 116
# for 64 octets: "64-octet UTF-8 string containing the firmware version of the
# ATDECC Entity". 7.2 fixes the padding: "The 64-octet strings do not include
# the NULL terminator when they are 64-octets long. If the string is shorter
# than 64-octets then the remainder of the field shall be zero (0) padded."
# The Milan end-station Validation Test plan v1.9 test macro 3 (Enumerate a
# Milan Entity) reads firmware_version into the enumeration model on the first
# READ_DESCRIPTOR, so it is the first string any validation tool - and Hive -
# shows about this device.
#
# WHY THIS FILE EXISTS. Neither document can state the one requirement that
# matters: the string has to be TRUE. Until 2026-07-28 all three
# configs/endstation_*.yaml hardcoded firmware_version "0.1.0" while the
# gateware's own VERSION parameter said 0x0001_0016, and nothing compared them,
# so every board we ship told every controller on the segment that it ran
# firmware 0.1.0. Roadmap item 00 exactly: a declaration checked only against
# another declaration. These scenarios read the shipped descriptor bytes and
# the RTL parameter, and the last one is the negative control - it re-creates
# the 0.1.0 descriptor and requires the comparison to reject it, so the
# positive scenario is not passing by construction.

@item00 @aem @cmd:READ_DESCRIPTOR @matrix:AEM-1 @clause:1722.1-7.2.1
Feature: ENTITY descriptor firmware_version is the version the fabric runs

  Scenario: a controller reads a firmware_version that names this gateware
    Given the entity definition this gateware serves
    When a controller READ_DESCRIPTORs the ENTITY descriptor
    Then the firmware_version field is 64 octets at offset 116
    And the firmware_version is a NUL-terminated UTF-8 string, zero padded
    And the firmware_version names the gateware VERSION register

  Scenario: the TB golden image carries the same ENTITY descriptor
    Given the entity definition this gateware serves
    When a controller READ_DESCRIPTORs the ENTITY descriptor
    Then the TB golden image serves the same ENTITY descriptor

  @negative
  Scenario: the 2026-07-27 descriptor is rejected against the same fabric
    Given the entity definition still declares firmware_version "0.1.0"
    When a controller READ_DESCRIPTORs the ENTITY descriptor
    Then the firmware_version field is 64 octets at offset 116
    And the firmware_version is a NUL-terminated UTF-8 string, zero padded
    And the firmware_version contradicts the gateware VERSION register
