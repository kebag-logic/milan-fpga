/*
 * SPDX-FileCopyrightText: 2025 Kebag Logic <info@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

class avtp_aecp_packet_gen extends avtp_control_subtype;

  static int count = 0;

  logic [7:0] tmp[$];

  function new();
    super.new();
    $display("[INFO][AVTP_AECP_PACKET_GEN] : The AECP Packet is being Generated");
  endfunction

  function subtype_t subtype_gen();
    super.subtype_gen();
  endfunction

  function avtp_common_hdr_t subtype_header_gen();
    // Assign AECP to the packet subtype and name
    subtype_cntrl = AECP;
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

  // Helper: push a 64-bit entity ID MSB first (8 bytes)
  function void push_eid(ref logic [7:0] q[$], input bit [63:0] eid);
    for (int i = 0; i < 8; i++) begin
      q.push_back(logic'(eid[63-(8*i) -: 8]));
    end
  endfunction

  // No-payload AECP command (e.g. GET_CONFIGURATION, REGISTER/DEREGISTER_UNSOLICITED)
  // control_data_length = 20 (common header only, no additional payload)
  function avtp_aecp_no_payload_t aecp_no_payload_gen(
    ref   logic [7:0]  q[$],
    input bit  [3:0]   msg_type,
    input bit  [14:0]  cmd_type,
    input bit  [15:0]  seq_id,
    input bit  [63:0]  tgt_eid,
    input bit  [63:0]  ctlr_eid
  );
    avtp_aecp_no_payload_t pkt;
    localparam bit [10:0] CDL = 11'd20;

    // Push EtherType (0x22F0) + subtype byte (0xFB)
    avtp_packet_gen(q);

    // Byte 3: {sv=1, h=0, ver=3'b0, msg_type[3:0]}
    q.push_back(logic'({1'b1, 1'b0, 3'b0, msg_type[3:0]}));
    // Byte 4: {status[4:0]=0, cdl[10:8]}
    q.push_back(logic'({5'b0, CDL[10:8]}));
    // Byte 5: cdl[7:0]
    q.push_back(logic'(CDL[7:0]));

    // Bytes 6-13: target_entity_id MSB first
    push_eid(q, tgt_eid);

    // Bytes 14-21: controller_entity_id MSB first
    push_eid(q, ctlr_eid);

    // Bytes 22-23: sequence_id MSB first
    q.push_back(logic'(seq_id[15:8]));
    q.push_back(logic'(seq_id[7:0]));

    // Byte 24: {u_flag=0, cmd_type[14:8]}
    q.push_back(logic'({1'b0, cmd_type[14:8]}));
    // Byte 25: cmd_type[7:0]
    q.push_back(logic'(cmd_type[7:0]));

    // Populate return struct
    pkt.common.message_type        = msg_type;
    pkt.common.status              = 5'b0;
    pkt.common.control_data_length = CDL;
    pkt.common.target_entity_id    = tgt_eid;
    pkt.common.controller_entity_id= ctlr_eid;
    pkt.common.sequence_id         = seq_id;
    pkt.common.u_flag              = 1'b0;
    pkt.common.command_type        = cmd_type;

    return pkt;
  endfunction

  // ACQUIRE_ENTITY command
  // control_data_length = 36 (20 common + 4 flags + 8 owner_id + 2 desc_type + 2 desc_idx)
  function avtp_aecp_acquire_t aecp_acquire_entity_gen(
    ref   logic [7:0]  q[$],
    input bit  [63:0]  tgt_eid,
    input bit  [63:0]  ctlr_eid,
    input bit  [15:0]  seq_id,
    input bit  [31:0]  flags,
    input bit  [63:0]  owner_id
  );
    avtp_aecp_acquire_t pkt;
    localparam bit [10:0] CDL = 11'd36;

    // Push EtherType (0x22F0) + subtype byte (0xFB)
    avtp_packet_gen(q);

    // Byte 3: {sv=1, h=0, ver=3'b0, AEM_COMMAND=4'h0}
    q.push_back(logic'({1'b1, 1'b0, 3'b0, 4'h0}));
    // Byte 4: {status[4:0]=0, cdl[10:8]}
    q.push_back(logic'({5'b0, CDL[10:8]}));
    // Byte 5: cdl[7:0]
    q.push_back(logic'(CDL[7:0]));

    // Bytes 6-13: target_entity_id MSB first
    push_eid(q, tgt_eid);

    // Bytes 14-21: controller_entity_id MSB first
    push_eid(q, ctlr_eid);

    // Bytes 22-23: sequence_id MSB first
    q.push_back(logic'(seq_id[15:8]));
    q.push_back(logic'(seq_id[7:0]));

    // Byte 24: {u_flag=0, AEM_CMD_ACQUIRE_ENTITY[14:8]=7'h00}
    q.push_back(logic'({1'b0, 7'h00}));
    // Byte 25: AEM_CMD_ACQUIRE_ENTITY[7:0]=8'h00
    q.push_back(logic'(8'h00));

    // Bytes 26-29: acquire_flags MSB first
    q.push_back(logic'(flags[31:24]));
    q.push_back(logic'(flags[23:16]));
    q.push_back(logic'(flags[15:8]));
    q.push_back(logic'(flags[7:0]));

    // Bytes 30-37: owner_id MSB first
    push_eid(q, owner_id);

    // Bytes 38-39: descriptor_type = 0
    q.push_back(logic'(8'h00));
    q.push_back(logic'(8'h00));

    // Bytes 40-41: descriptor_index = 0
    q.push_back(logic'(8'h00));
    q.push_back(logic'(8'h00));

    // Populate return struct
    pkt.common.message_type        = 4'h0;
    pkt.common.status              = 5'b0;
    pkt.common.control_data_length = CDL;
    pkt.common.target_entity_id    = tgt_eid;
    pkt.common.controller_entity_id= ctlr_eid;
    pkt.common.sequence_id         = seq_id;
    pkt.common.u_flag              = 1'b0;
    pkt.common.command_type        = 15'h0000;
    pkt.acquire_flags              = flags;
    pkt.owner_id                   = owner_id;
    pkt.descriptor_type            = 16'h0000;
    pkt.descriptor_index           = 16'h0000;

    return pkt;
  endfunction

  // LOCK_ENTITY command
  // control_data_length = 36 (20 common + 4 flags + 8 locked_id + 2 desc_type + 2 desc_idx)
  function avtp_aecp_lock_t aecp_lock_entity_gen(
    ref   logic [7:0]  q[$],
    input bit  [63:0]  tgt_eid,
    input bit  [63:0]  ctlr_eid,
    input bit  [15:0]  seq_id,
    input bit  [31:0]  flags,
    input bit  [63:0]  locked_id
  );
    avtp_aecp_lock_t pkt;
    localparam bit [10:0] CDL = 11'd36;

    // Push EtherType (0x22F0) + subtype byte (0xFB)
    avtp_packet_gen(q);

    // Byte 3: {sv=1, h=0, ver=3'b0, AEM_COMMAND=4'h0}
    q.push_back(logic'({1'b1, 1'b0, 3'b0, 4'h0}));
    // Byte 4: {status[4:0]=0, cdl[10:8]}
    q.push_back(logic'({5'b0, CDL[10:8]}));
    // Byte 5: cdl[7:0]
    q.push_back(logic'(CDL[7:0]));

    // Bytes 6-13: target_entity_id MSB first
    push_eid(q, tgt_eid);

    // Bytes 14-21: controller_entity_id MSB first
    push_eid(q, ctlr_eid);

    // Bytes 22-23: sequence_id MSB first
    q.push_back(logic'(seq_id[15:8]));
    q.push_back(logic'(seq_id[7:0]));

    // Byte 24: {u_flag=0, AEM_CMD_LOCK_ENTITY[14:8]=7'h00}
    q.push_back(logic'({1'b0, 7'h00}));
    // Byte 25: AEM_CMD_LOCK_ENTITY[7:0]=8'h01
    q.push_back(logic'(8'h01));

    // Bytes 26-29: lock_flags MSB first
    q.push_back(logic'(flags[31:24]));
    q.push_back(logic'(flags[23:16]));
    q.push_back(logic'(flags[15:8]));
    q.push_back(logic'(flags[7:0]));

    // Bytes 30-37: locked_id MSB first
    push_eid(q, locked_id);

    // Bytes 38-39: descriptor_type = 0
    q.push_back(logic'(8'h00));
    q.push_back(logic'(8'h00));

    // Bytes 40-41: descriptor_index = 0
    q.push_back(logic'(8'h00));
    q.push_back(logic'(8'h00));

    // Populate return struct
    pkt.common.message_type        = 4'h0;
    pkt.common.status              = 5'b0;
    pkt.common.control_data_length = CDL;
    pkt.common.target_entity_id    = tgt_eid;
    pkt.common.controller_entity_id= ctlr_eid;
    pkt.common.sequence_id         = seq_id;
    pkt.common.u_flag              = 1'b0;
    pkt.common.command_type        = 15'h0001;
    pkt.lock_flags                 = flags;
    pkt.locked_id                  = locked_id;
    pkt.descriptor_type            = 16'h0000;
    pkt.descriptor_index           = 16'h0000;

    return pkt;
  endfunction

  // READ_DESCRIPTOR command
  // control_data_length = 28 (20 common + 2 cfg_idx + 2 reserved + 2 desc_type + 2 desc_idx)
  function avtp_aecp_read_desc_t aecp_read_descriptor_gen(
    ref   logic [7:0]  q[$],
    input bit  [63:0]  tgt_eid,
    input bit  [63:0]  ctlr_eid,
    input bit  [15:0]  seq_id,
    input bit  [15:0]  cfg_idx,
    input bit  [15:0]  desc_type,
    input bit  [15:0]  desc_idx
  );
    avtp_aecp_read_desc_t pkt;
    localparam bit [10:0] CDL = 11'd28;

    // Push EtherType (0x22F0) + subtype byte (0xFB)
    avtp_packet_gen(q);

    // Byte 3: {sv=1, h=0, ver=3'b0, AEM_COMMAND=4'h0}
    q.push_back(logic'({1'b1, 1'b0, 3'b0, 4'h0}));
    // Byte 4: {status[4:0]=0, cdl[10:8]}
    q.push_back(logic'({5'b0, CDL[10:8]}));
    // Byte 5: cdl[7:0]
    q.push_back(logic'(CDL[7:0]));

    // Bytes 6-13: target_entity_id MSB first
    push_eid(q, tgt_eid);

    // Bytes 14-21: controller_entity_id MSB first
    push_eid(q, ctlr_eid);

    // Bytes 22-23: sequence_id MSB first
    q.push_back(logic'(seq_id[15:8]));
    q.push_back(logic'(seq_id[7:0]));

    // Byte 24: {u_flag=0, AEM_CMD_READ_DESCRIPTOR[14:8]=7'h00}
    q.push_back(logic'({1'b0, 7'h00}));
    // Byte 25: AEM_CMD_READ_DESCRIPTOR[7:0]=8'h04
    q.push_back(logic'(8'h04));

    // Bytes 26-27: configuration_index MSB first
    q.push_back(logic'(cfg_idx[15:8]));
    q.push_back(logic'(cfg_idx[7:0]));

    // Bytes 28-29: reserved = 0
    q.push_back(logic'(8'h00));
    q.push_back(logic'(8'h00));

    // Bytes 30-31: descriptor_type MSB first
    q.push_back(logic'(desc_type[15:8]));
    q.push_back(logic'(desc_type[7:0]));

    // Bytes 32-33: descriptor_index MSB first
    q.push_back(logic'(desc_idx[15:8]));
    q.push_back(logic'(desc_idx[7:0]));

    // Populate return struct
    pkt.common.message_type        = 4'h0;
    pkt.common.status              = 5'b0;
    pkt.common.control_data_length = CDL;
    pkt.common.target_entity_id    = tgt_eid;
    pkt.common.controller_entity_id= ctlr_eid;
    pkt.common.sequence_id         = seq_id;
    pkt.common.u_flag              = 1'b0;
    pkt.common.command_type        = 15'h0004;
    pkt.configuration_index        = cfg_idx;
    pkt.reserved                   = 16'h0000;
    pkt.descriptor_type            = desc_type;
    pkt.descriptor_index           = desc_idx;

    return pkt;
  endfunction

  // Check a received response queue for matching sequence_id and status.
  // Returns 1 if both match, 0 otherwise.
  // Response queue layout (byte offsets from start of AVTP payload after EtherType+subtype):
  //   q[3]      : {sv, h, ver, message_type}
  //   q[4]      : {status[4:0], cdl[10:8]}
  //   q[5]      : cdl[7:0]
  //   q[6..13]  : target_entity_id
  //   q[14..21] : controller_entity_id
  //   q[22..23] : sequence_id
  //   q[24..25] : {u_flag, command_type}
  function bit check_response(
    input logic [7:0]  resp_q[$],
    input bit  [15:0]  expected_seq_id,
    input bit  [4:0]   expected_status
  );
    bit [15:0] got_seq_id;
    bit [4:0]  got_status;

    if (resp_q.size() < 26) begin
      $display("[WARN][AVTP_AECP_PACKET_GEN] check_response: queue too short (%0d bytes)", resp_q.size());
      return 1'b0;
    end

    got_status  = resp_q[4][7:3];
    got_seq_id  = {resp_q[22], resp_q[23]};

    if (got_seq_id !== expected_seq_id) begin
      $display("[FAIL][AVTP_AECP_PACKET_GEN] check_response: sequence_id mismatch: got 0x%04h, expected 0x%04h",
               got_seq_id, expected_seq_id);
      return 1'b0;
    end

    if (got_status !== expected_status) begin
      $display("[FAIL][AVTP_AECP_PACKET_GEN] check_response: status mismatch: got 0x%02h, expected 0x%02h",
               got_status, expected_status);
      return 1'b0;
    end

    $display("[PASS][AVTP_AECP_PACKET_GEN] check_response: seq_id=0x%04h status=0x%02h OK",
             got_seq_id, got_status);
    return 1'b1;
  endfunction

endclass
