/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

class avtp_control_subtype extends avtp_base_packet_gen;

  static int count = 0;
  subtype_control_t subtype_cntrl;

  function new();
    super.new();
    $display("[INFO][AVTP_CONTROL_SUBTYPE] : The Control Packet is being Generated");
  endfunction

  function subtype_t subtype_gen();
    subtype = CONTROL_HDR;
    return subtype;
  endfunction

  function avtp_common_hdr_t subtype_header_gen();
    // Generate random control type
    subtype_cntrl = subtype_control_t'($urandom_range(subtype_cntrl.first(), subtype_cntrl.last()));
    $display("[INFO][AVTP_CONTROL_SUBTYPE] : The Subtype of the Control header is %s", subtype_cntrl.name());

    avtp_common_hdr.subtype = subtype_cntrl;
    avtp_common_hdr.name = subtype_cntrl.name();
    count++;
    return avtp_common_hdr;
  endfunction

  function void avtp_packet_gen(ref logic [7:0] q[$]);
    q.push_back(ether_type[16:8]);
    q.push_back(ether_type[7:0]);
    q.push_back(avtp_common_hdr.subtype);
  endfunction

endclass