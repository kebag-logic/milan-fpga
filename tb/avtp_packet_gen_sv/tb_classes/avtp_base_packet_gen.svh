/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

virtual class avtp_base_packet_gen;

  avtp_common_hdr_t avtp_common_hdr;
  subtype_t subtype;
  static int ether_type = 16'h22F0;
  
  function new ();
    $display("[INFO][AVTP_BASE_PACKET_GEN] : AVTP Base Packet Gen Class is Generated");
  endfunction

  pure virtual function subtype_t subtype_gen();
  pure virtual function avtp_common_hdr_t subtype_header_gen();
  pure virtual function void avtp_packet_gen(ref logic [7:0] q[$]);

endclass