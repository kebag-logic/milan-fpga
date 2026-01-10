/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

class avtp_random_subtype extends avtp_base_packet_gen;

  static int total_count = 0;
  static int control_count = 0;
  static int stream_count = 0;
  static int alter_count = 0;

  subtype_control_t subtype_cntrl;
  subtype_stream_t subtype_stream;
  subtype_alter_t subtype_alter;

  function new();
    super.new();
    $display("[INFO][AVTP_RANDOM_SUBTYPE] : The random subtype is being generated");
  endfunction

  function subtype_t subtype_gen();
  endfunction

  function avtp_common_hdr_t subtype_header_gen();
    avtp_common_hdr.subtype = $urandom_range(0,255);

    subtype_cntrl = subtype_cntrl.first();
    subtype_stream = subtype_stream.first();
    subtype_alter = subtype_alter.first();

    // Search for Control
    for (int i = 0; i < subtype_cntrl.num(); i++) begin
      if (avtp_common_hdr.subtype == subtype_cntrl) begin
        $display("[INFO][AVTP_RANDOM_SUBTYPE] : The generated subtype is Control %s, 0x%X", subtype_cntrl.name(), avtp_common_hdr.subtype);
        control_count++;
        break;
      end
      else subtype_cntrl = subtype_cntrl.next();
    end

    // Search for Stream
    for (int i = 0; i < subtype_stream.num(); i++) begin
      if (avtp_common_hdr.subtype == subtype_stream) begin
        $display("[INFO][AVTP_RANDOM_SUBTYPE] : The generated subtype is Stream %s, 0x%X", subtype_stream.name(), avtp_common_hdr.subtype);
        stream_count++;
        break;
      end
      else subtype_stream = subtype_stream.next();
    end

    // Search for Alternative
    for (int i = 0; i < subtype_alter.num(); i++) begin
      if (avtp_common_hdr.subtype == subtype_alter) begin
        $display("[INFO][AVTP_RANDOM_SUBTYPE] : The generated subtype is Alternative %s, 0x%X", subtype_alter.name(), avtp_common_hdr.subtype);
        alter_count++;
        break;
      end
      else subtype_alter = subtype_alter.next();
    end

    $display("[INFO][AVTP_RANDOM_SUBTYPE] : The generated subtype is 0x%X", avtp_common_hdr.subtype);
    total_count++;
    return avtp_common_hdr;
  endfunction

  function void avtp_packet_gen(ref logic [7:0] q[$]);
    q.push_back(ether_type[16:8]);
    q.push_back(ether_type[7:0]);
    q.push_back(avtp_common_hdr.subtype);
  endfunction

endclass