/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

class avtp_alter_subtype extends avtp_base_packet_gen;

  bit8 stream_rnd;
  static int count = 0;
  subtype_alter_t subtype_alter;

  function new();
    super.new();
    $display("[INFO][AVTP_ALTER_SUBTYPE] : The Alternative Packet is being Generated");
  endfunction

  function subtype_t subtype_gen();
    subtype = ALTER_HDR;
    return subtype;
  endfunction

  function avtp_common_hdr_t subtype_header_gen();
    subtype_alter = subtype_alter.first();
    stream_rnd = $urandom_range(subtype_alter.first(), subtype_alter.last());

    while(stream_rnd != subtype_alter) begin
      for (int i = 0; i < subtype_alter.num() - 1; i++) begin
        if (stream_rnd == subtype_alter) break;
        else subtype_alter = subtype_alter.next();
      end
      if (stream_rnd == subtype_alter) break;
      else stream_rnd = $urandom_range(subtype_alter.first(), subtype_alter.last());
    end
    $display("[INFO][AVTP_ALTER_SUBTYPE] : The subtype of the Alternative header is %s", subtype_alter.name());
    avtp_common_hdr.subtype = stream_rnd;
    avtp_common_hdr.name = subtype_alter.name();
    count++;
    return avtp_common_hdr;
  endfunction

  function void avtp_packet_gen(ref logic [7:0] q[$]);
    q.push_back(ether_type[16:8]);
    q.push_back(ether_type[7:0]);
    q.push_back(avtp_common_hdr.subtype);
  endfunction

endclass