/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

class avtp_stream_subtype extends avtp_base_packet_gen;

  bit8 stream_rnd;
  static int count = 0;
  subtype_stream_t subtype_stream;

  function new();
    super.new();
    $display("[INFO][AVTP_STREAM_SUBTYPE] : The Stream Packet is being Generated");
  endfunction

  function subtype_t subtype_gen();
    subtype = STREAM_HDR;
    return subtype;
  endfunction

  function avtp_common_hdr_t subtype_header_gen();
    // Generate random number
    // Check whether generated random number is match with any value in struct
    // Re-generate the random if necessary
    subtype_stream = subtype_stream.first();
    stream_rnd = $urandom_range(subtype_stream.first(), subtype_stream.last());

    while(stream_rnd != subtype_stream) begin
      for (int i = 0; i < subtype_stream.num() - 1; i++) begin
        if (stream_rnd == subtype_stream) break;
        else subtype_stream = subtype_stream.next();
      end
      if (stream_rnd == subtype_stream) break;
      else stream_rnd = $urandom_range(subtype_stream.first(), subtype_stream.last());
    end
    
    $display("[INFO][AVTP_STREAM_SUBTYPE] : The subtype of the Stream header is %s", subtype_stream.name());
    avtp_common_hdr.subtype = subtype_stream;
    avtp_common_hdr.name = subtype_stream.name();
    count++;
    return avtp_common_hdr;
  endfunction

  function void avtp_packet_gen(ref logic [7:0] q[$]);
    q.push_back(ether_type[16:8]);
    q.push_back(ether_type[7:0]);
    q.push_back(avtp_common_hdr.subtype);
  endfunction

endclass