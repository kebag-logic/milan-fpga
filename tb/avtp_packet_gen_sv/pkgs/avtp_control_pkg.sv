/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

package avtp_control_pkg;

  import avtp_pkt_common_pkg::*;
    
  typedef enum bit8 {
    ADP = 8'hFA,
    AECP,
    ACMP,
    MAAP = 8'hFE,
    EF_CONTROL
  } subtype_control_t;

  // ------------------------ ADP ------------------------ //
  typedef enum bit [3:0] {
    ENTITY_AVAILABLE,
    ENTITY_DEPARTING,
    ENTITY_DISCOVER,
    RESERVED
  } adp_message_type_t;

  typedef enum bit32 {
    EFU_MODE  = 32'h0000_0001,
    ADDRESS_ACCESS_SUPPORTED = 32'h0000_0002,
    GATEWAY_ENTITY = 32'h0000_0004,
    AEM_SUPPORTED = 32'h0000_0008,
    LEGACY_AVC = 32'h0000_0010,
    ASSOC_ID_SUPPORTED = 32'h0000_0020,
    ASSOC_ID_VALID = 32'h0000_0040,
    VENDOR_UNIQUE_SUPPORTED  = 32'h0000_0080,
    CLASS_A_SUPPORTED = 32'h0000_0100,
    CLASS_B_SUPPORTED = 32'h0000_0200,
    GPTP_SUPPORTED = 32'h0000_0400,
    AEM_AUTH_SUPPORTED = 32'h0000_0800,
    AEM_AUTH_REQUIRED = 32'h0000_1000,
    AEM_PERSISTENT_ACQUIRE_SUPPORTED = 32'h0000_2000,
    AEM_IDENTIFY_CONTROL_INDEX_VALID = 32'h0000_4000,
    AEM_INTERFACE_INDEX_VALID = 32'h0000_8000,
    GENERAL_CONTROL_IGNORE = 32'h0001_0000,
    ENTITY_NOT_READY = 32'h0002_0000,
    ACMP_ACQUIRE_WITH_AEM = 32'h0004_0000,
    ACMP_AUTH_WITH_AEM = 32'h0008_0000,
    SUPPORTS_UDPV4_ATDECC = 32'h0010_0000,
    SUPPORTS_UDPV4_STREAMING = 32'h0020_0000,
    SUPPORTS_UDPV6_ATDECC = 32'h0040_0000,
    SUPPORTS_UDPV6_STREAMING = 32'h0080_0000,
    MULTIPLE_PTP_INSTANCES = 32'h0100_0000,
    AEM_CONFIGURATION_INDEX_VALID = 32'h0200_0000
  } adp_entity_capabilities_t; 

  typedef enum bit16 {
    TALKER_IMPLEMENTED = 16'h0001,
    TALKER_OTHER_SOURCE = 16'h0200,
    TALKER_CONTROL_SOURCE = 16'h0400,
    TALKER_MEDIA_CLOCK_SOURCE = 16'h0800,
    TALKER_SMPTE_SOURCE = 16'h1000,
    TALKER_MIDI_SOURCE = 16'h2000,
    TALKER_AUDIO_SOURCE = 16'h4000,
    TALKER_VIDEO_SOURCE = 16'h8000
  } adp_talker_capabilities_t;

  typedef enum bit16 {
    LISTENER_IMPLEMENTED = 16'h0001,
    LISTENER_OTHER_SOURCE = 16'h0200,
    LISTENER_CONTROL_SOURCE = 16'h0400,
    LISTENER_MEDIA_CLOCK_SOURCE = 16'h0800,
    LISTENER_SMPTE_SOURCE = 16'h1000,
    LISTENER_MIDI_SOURCE = 16'h2000,
    LISTENER_AUDIO_SOURCE = 16'h4000,
    LISTENER_VIDEO_SOURCE = 16'h8000
  } adp_listener_capabilities_t;

  typedef enum bit32 {
    CONTROL_IMPLEMENTED = 32'h0000_0001
  } adp_controller_capabilities_t;

  typedef struct {
    avtp_common_hdr_t avtp_common_hdr;
    adp_message_type_t adp_message_type;
    bit [4:0] valid_time;
    bit [10:0] control_data_length = 11'd56;
    bit64     entity_id;
    bit64     entity_model_id;
    bit32     entity_capabilities;
    bit16     talker_stream_sources;
    bit16     talker_capabilities;
    bit16     listener_stream_sinks;
    bit16     listener_capabilities;
    bit32     controller_capabilities;
    bit32     available_index;
    bit64     gptp_grandmaster_id;
    bit8      gptp_domain_number;
    bit8      reserved0 = 8'h0;
    bit16     current_configuration_index;
    bit16     identify_control_index;
    bit16     interface_index;
    bit64     association_id;
    bit32     reserved1 = 32'h0;
  } avtp_adp_t;

  
  // ------------------------ AECP ------------------------ //
  // ------------------------ ACMP ------------------------ //
  // ------------------------ MAAP ------------------------ //


endpackage