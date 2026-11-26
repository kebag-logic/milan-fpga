/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_usbnet_pkg.sv
  Description : The frame rules of the USB network path (#1011), named once
                and shared by the receive copy and the transmit check.
                A frame is read from its first 19 octets: the destination
                (0-5), the source (6-11), the EtherType (12-13), and either
                the AVTP subtype (14) of an untagged frame or the tag (14-15),
                inner EtherType (16-17) and AVTP subtype (18) of a frame with
                one IEEE 802.1Q tag.
                THE STREAM SUBTYPES. IEEE 1722-2016 Table 6 places every
                stream data format (61883/IIDC, MMA, AAF, CVF, CRF, TSCF, SVF,
                RVF, AEF continuous, vendor and experimental stream) at
                subtype 0x00 to 0x7F, and every control or alternative format
                (NTSCF, ESCF, EECF, AEF discrete, ADP, AECP, ACMP, MAAP,
                experimental control) at 0x80 to 0xFF. A stream frame is
                therefore an AVTP frame (EtherType 0x22F0) whose subtype has
                bit 7 clear. Reserved stream values fall on the same side.
                THE LINK-LOCAL BLOCK. IEEE 802.1Q-2018 8.6.3, Table 8-1: the
                destinations 01-80-C2-00-00-00 to -0F are not forwarded by a
                bridge (gPTP, MSRP and LLDP use them). MVRP and MMRP use the
                MRP application block 01-80-C2-00-00-20 to -2F instead
                (Table 10-1: -21 and -20). #1011 and usb-audio#5 name MVRP
                among the excluded protocols, so that block is excluded too.
  Spec refs   : IEEE 1722-2016 5.2 and Table 6; IEEE 802.1Q-2018 8.6.3, Table 10-1,
                9.6 (the tag) and 8.6.6 (priority); IEEE 802-2014 8.2 (group
                and local address bits)
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//
`default_nettype none

package KL_usbnet_pkg;

  localparam logic [15:0] ETH_AVTP_C  = 16'h22F0;
  localparam logic [15:0] ETH_CTAG_C  = 16'h8100;
  localparam logic [15:0] ETH_STAG_C  = 16'h88A8;
  //! the octets the rules read
  localparam int unsigned HDR_OCTETS_C = 19;

  //! the record types of the bus-side length header (docs/design/USB_NET_PATH.md)
  localparam logic [3:0] REC_FRAME_C  = 4'h0;  //! an Ethernet frame, either way
  localparam logic [3:0] REC_HOST_C   = 4'h1;  //! the computer's address and USB state
  localparam logic [3:0] REC_DETACH_C = 4'h2;  //! the computer left

  //! receive-copy verdicts, one per frame the device received
  typedef enum logic [2:0] {
    RXV_HOST      = 3'd0,  //! copied: unicast to the computer
    RXV_GROUP     = 3'd1,  //! copied: broadcast or multicast
    RXV_UNICAST   = 3'd2,  //! kept: unicast to anyone else (the device too)
    RXV_LINKLOCAL = 3'd3,  //! kept: 01-80-C2-00-00-0x or -2x
    RXV_STREAM    = 3'd4,  //! kept: an AVTP stream subtype
    RXV_SHAPE     = 3'd5,  //! kept: too short, or a tag the rules cannot read
    RXV_FULL      = 3'd6,  //! would be copied, but no room
    RXV_OFF       = 3'd7   //! no computer attached
  } rx_verdict_e;

  //! transmit-check verdicts, one per frame the computer sent
  typedef enum logic [2:0] {
    TXV_PASS      = 3'd0,  //! queued for injection
    TXV_SOURCE    = 3'd1,  //! dropped: the source is not the computer's address
    TXV_LINKLOCAL = 3'd2,  //! dropped: 01-80-C2-00-00-0x or -2x
    TXV_STREAM    = 3'd3,  //! dropped: an AVTP stream subtype
    TXV_PRIORITY  = 3'd4,  //! dropped: a tag whose priority is not best effort
    TXV_LENGTH    = 3'd5,  //! dropped: shorter than a header or longer than the limit
    TXV_SHAPE     = 3'd6   //! dropped: a tag the rules cannot read
  } tx_verdict_e;

  //! the header fields, MAC order (octet 0 in the top byte)
  typedef struct packed {
    logic [47:0] dst;
    logic [47:0] src;
    logic [15:0] etype;   //! octets 12-13
    logic [7:0]  o14;     //! untagged subtype, or the tag's first octet
    logic [7:0]  o15;
    logic [15:0] itype;   //! octets 16-17: the inner EtherType of a tagged frame
    logic [7:0]  o18;     //! the subtype of a tagged frame
  } hdr_t;

  function automatic logic is_group(input logic [47:0] a);
    return a[40];
  endfunction

  //! 01-80-C2-00-00-0x, and the MRP application block 01-80-C2-00-00-2x
  function automatic logic is_link_local(input logic [47:0] a);
    return (a[47:4] == 44'h0180C200000) || (a[47:4] == 44'h0180C200002);
  endfunction

  function automatic logic is_tagged(input hdr_t h);
    return (h.etype == ETH_CTAG_C) || (h.etype == ETH_STAG_C);
  endfunction

  //! a second tag behind the first: the subtype is not where the rules look
  function automatic logic is_unreadable_tag(input hdr_t h);
    return is_tagged(h) && ((h.itype == ETH_CTAG_C) || (h.itype == ETH_STAG_C));
  endfunction

  function automatic logic is_stream(input hdr_t h);
    if (is_tagged(h)) return (h.itype == ETH_AVTP_C) && !h.o18[7];
    return (h.etype == ETH_AVTP_C) && !h.o14[7];
  endfunction

  //! the octets a frame must carry before the rules can decide on it
  function automatic logic [4:0] need_octets(input hdr_t h);
    if (is_tagged(h)) return 5'd19;
    if (h.etype == ETH_AVTP_C) return 5'd15;
    return 5'd14;
  endfunction

  //! which frames the computer receives (#1011, receive filter)
  function automatic rx_verdict_e rx_rule(input hdr_t h, input logic [11:0] len,
                                          input logic [47:0] host,
                                          input logic host_ok);
    if (!host_ok)                                   return RXV_OFF;
    if (len < 12'(need_octets(h)) || is_unreadable_tag(h)) return RXV_SHAPE;
    if (is_stream(h))                               return RXV_STREAM;
    if (!is_group(h.dst))  return (h.dst == host) ? RXV_HOST : RXV_UNICAST;
    if (is_link_local(h.dst))                       return RXV_LINKLOCAL;
    return RXV_GROUP;
  endfunction

  //! which frames the computer may send (#1011, transmit inject)
  //! (the longest frame is refused at its record header, before buffering)
  function automatic tx_verdict_e tx_rule(input hdr_t h, input logic [11:0] len,
                                          input logic [47:0] host,
                                          input logic host_ok);
    if (len < 12'(need_octets(h)))                  return TXV_LENGTH;
    if (!host_ok || h.src != host)                  return TXV_SOURCE;
    if (is_link_local(h.dst))                       return TXV_LINKLOCAL;
    if (is_unreadable_tag(h))                       return TXV_SHAPE;
    if (is_stream(h))                               return TXV_STREAM;
    //! IEEE 802.1Q-2018 Table 8-5: priorities 0 and 1 are the best-effort and
    //! background classes; 2 and 3 are the SR class defaults (34.5), and any
    //! other priority would outrank best effort at the next bridge
    if (is_tagged(h) && h.o14[7:5] > 3'd1)          return TXV_PRIORITY;
    return TXV_PASS;
  endfunction

  //! a usable address for the computer: individual and locally administered
  //! (IEEE 802-2014 8.2.2; the owner's decision on #1011)
  function automatic logic host_mac_ok(input logic [47:0] a);
    return !a[40] && a[41];
  endfunction

endpackage

`default_nettype wire
