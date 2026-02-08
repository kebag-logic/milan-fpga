/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

package adp_pkg;

  //! AVTP Ethernet Type
  localparam [15:0] AVTP_ETHERNET_TYPE_C = 16'h22F0;
  //! ADP subtype
  localparam [7:0]  ADP_SUBTYPE_C = 8'hFA;
  //! SV-Version-ADP Message Type
  localparam [7:0]  SV_VER_MSG_TYPE_DISCOVERY_C = 8'h02;
  localparam [7:0]  SV_VER_MSG_TYPE_AVAILABLE_C = 8'h00;
  localparam [7:0]  SV_VER_MSG_TYPE_DEPARTING_C = 8'h01;
  //! Total bytes in hex
  localparam [10:0]  CTRL_DATA_LENGTH_C = 11'h38;

  //! Typedef for adp_message_type
  typedef enum logic[3:0] {
    ENTITY_AVAILABLE,
    ENTITY_DEPARTING,
    ENTITY_DISCOVER,
    RESERVED
  } adp_message_type_t;

  //! ADP Advertise Related Events
  typedef struct {
    logic RCV_ADP_DISCOVER;
    logic TMR_ADVERTISE;
    logic TMR_DELAY;
    logic LINK_UP;
    logic LINK_DOWN;
    logic GM_CHANGE;
    logic SHUTDOWN;
  } adp_advertise_event_t;

  //! ADP Discovery Related Events
  typedef struct {
    logic RCV_ADP_AVAILABLE;
    logic RCV_ADP_DEPARING;
    logic TMR_NO_ADP;
  } adp_discovery_event_t;

  //! Struct for holding the parsed packet information.
  typedef struct packed {
    adp_message_type_t adp_message_type;
    logic [4:0] valid_time;
    logic [63:0] entity_id;
    logic [63:0] entity_model_id;
    logic [31:0] entity_capabilities;
    logic [15:0] talker_stream_sources;
    logic [15:0] talker_capabilities;
    logic [15:0] listener_stream_sinks;
    logic [15:0] listener_capabilities;
    logic [31:0] controller_capabilities;
    logic [31:0] available_index;
    logic [63:0] gptp_grandmaster_id;
    logic [7:0] gptp_domain_number;
    logic [15:0] current_configuration_index;
    logic [15:0] identify_control_index;
    logic [15:0] interface_index;
    logic [63:0] association_id;
    logic entity_info_valid;
  } entity_info_t;


endpackage