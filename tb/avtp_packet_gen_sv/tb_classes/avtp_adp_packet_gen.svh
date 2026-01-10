/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

class avtp_adp_packet_gen extends avtp_control_subtype;

  // adp_entity_capabilities_t adp_entity_capabilities;
  // adp_talker_capabilities_t adp_talker_capabilities;
  // adp_listener_capabilities_t adp_listener_capabilities;
  // adp_controller_capabilities_t adp_controller_capabilities; // for now zero
  adp_message_type_t adp_message_type;

  logic [7:0] tmp[$];
  avtp_adp_t avtp_adp;

  function new();
    super.new();
    $display("[INFO][AVTP_ADP_PACKET_GEN] : The ADP Packet is being Generated");
  endfunction

  function subtype_t subtype_gen();
    super.subtype_gen();
  endfunction

  function avtp_common_hdr_t subtype_header_gen();
    // Assign ADP to the packet subtype and name
    subtype_cntrl = ADP;
    avtp_common_hdr.subtype = subtype_cntrl;
    avtp_common_hdr.h = '0;
    avtp_common_hdr.ver = '0;
    avtp_common_hdr.name = subtype_cntrl.name();
    count++;
    return avtp_common_hdr;
  endfunction

  function void avtp_packet_gen(ref logic [7:0] q[$]);
    super.avtp_packet_gen(q);
  endfunction

  function avtp_adp_t adp_packet_gen(ref logic [7:0] q[$]);
    avtp_adp.avtp_common_hdr = avtp_common_hdr;
    avtp_adp.adp_message_type = adp_message_type_t'($urandom_range(adp_message_type.first(),adp_message_type.last()));
    avtp_adp.valid_time = $urandom_range(0,31);
    avtp_adp.entity_id = {$urandom, $urandom};
    avtp_adp.entity_model_id = {$urandom, $urandom};

    q.push_back({avtp_common_hdr.h, avtp_common_hdr.ver, avtp_adp.adp_message_type});

    // -------------------- ERROR -----------------------
    // The streaming operation halts the VIVADO in GUI!!
    // tmp = {>>8{avtp_adp.valid_time,avtp_adp.control_data_length}};
    // foreach (tmp[i]) begin
    //   q.push_back(tmp[i]);
    // end
    // tmp = {>>8{avtp_adp.entity_id, avtp_adp.entity_model_id}};
    // foreach (tmp[i]) 
    //   q.push_back(tmp[i]);
    
    q.push_back({avtp_adp.valid_time, avtp_adp.control_data_length[10:8]});
    q.push_back(avtp_adp.control_data_length[7:0]);

    for (int i = 0; i < 8; i++) begin
      q.push_back(avtp_adp.entity_id[63-(8*i) -: 8]);
    end
    for (int i = 0; i < 8; i++) begin
      q.push_back(avtp_adp.entity_model_id[63-(8*i)-:8]);
    end
    // 48 octet left - The rest of the fields are randomized for now.
    for (int i = 0; i < 48; i++) begin
      q.push_back($urandom_range(0,255));
    end

    // Assign the randomly generated values to the
    // q[0],q[1] EthernetType
    // q[2] subtype
    // q[14:21] - entity_model_id
    // q[22:25] - entity_capabilities
    // q[26:27] - talker_stream_sources
    // q[28:29] - talker_capabilities
    // q[30:31] - listener_stream_sinks
    // q[32:33] - listener_capabilities
    // q[34:37] - controller_capabilities
    // q[38:41] - available_index
    // q[42:49] - gptp_grandmaster_id
    // q[50]    - gptp_domain_number
    // q[51]    - reserved0 - ignored for now
    // q[52:53] - current_configuration_index
    // q[54:55] - identify_control_index
    // q[56:57] - interface_index
    // q[58:65] - association_id
    // q[66:69] - reserved1 - ignored for now

    // TODO: find a way to make it better!!!
    avtp_adp.entity_capabilities  = {q[22],q[23],q[24],q[25]};
    avtp_adp.talker_stream_sources = {q[26],q[27]};
    avtp_adp.talker_capabilities = {q[28],q[29]};
    avtp_adp.listener_stream_sinks = {q[30],q[31]};
    avtp_adp.listener_capabilities = {q[32],q[33]};
    avtp_adp.controller_capabilities = {q[34],q[35],q[36],q[37]};
    avtp_adp.available_index = {q[38],q[39],q[40],q[41]};
    avtp_adp.gptp_grandmaster_id = {q[42],q[43],q[44],q[45],q[46],q[47],q[48],q[49]};
    avtp_adp.gptp_domain_number = q[50];
    // avtp_adp.reserved0 = q[51];
    avtp_adp.current_configuration_index = {q[52],q[53]};
    avtp_adp.identify_control_index = {q[54],q[55]};
    avtp_adp.interface_index = {q[56],q[57]};
    avtp_adp.association_id = {q[58],q[59],q[60],q[61],q[62],q[63],q[64],q[65]};
    // avtp_adp.reserved1 = {q[69],q[68],q[67],q[66]};

    return avtp_adp;
  endfunction


endclass