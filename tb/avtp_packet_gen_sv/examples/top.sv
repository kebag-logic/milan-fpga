module top;

  `include "avtp_packet_gen_pkg.svh"
  avtp_control_subtype avtp_control_pkt;
  avtp_stream_subtype avtp_stream_pkt;
  avtp_alter_subtype avtp_alter_pkt;
  avtp_random_subtype avtp_random_pkt;
  avtp_adp_packet_gen avtp_adp_pkt_gen;

  avtp_common_hdr_t avtp_common_hdr;
  subtype_t subtype;
  avtp_adp_t avtp_adp_pkt;

  logic [7:0] pkt[$];

  initial begin

    // $display("[TOP] : ---------------------TEST CASE-I-------------------------------");
    // $display("[TOP] : Generating Control Packet");
    // avtp_control_pkt = new();
    // subtype = avtp_control_pkt.subtype_gen();
    // avtp_common_hdr = avtp_control_pkt.subtype_header_gen();

    // $display("[TOP] : AVTP common header name is %s, the value is 0x%x", avtp_common_hdr.name, avtp_common_hdr.subtype);
    // avtp_control_pkt.avtp_packet_gen(pkt);
    // $display("[TOP] : The first octet of the avtp packet is 0x%X", pkt[0]);

    // $display("[TOP] : ---------------------TEST CASE-II------------------------------");
    // $display("[TOP] : Generating the Stream Packet");
    // avtp_stream_pkt = new();
    // subtype = avtp_stream_pkt.subtype_gen();
    // avtp_common_hdr = avtp_stream_pkt.subtype_header_gen();

    // $display("[TOP] : AVTP common header name is %s, the value is 0x%x", avtp_common_hdr.name, avtp_common_hdr.subtype);
    // avtp_stream_pkt.avtp_packet_gen(pkt);

    // $display("[TOP] : ---------------------TEST CASE-III------------------------------");
    // $display("[TOP] : Generating the Alternative Packet");
    // avtp_alter_pkt = new();
    // subtype = avtp_alter_pkt.subtype_gen();
    // avtp_common_hdr = avtp_alter_pkt.subtype_header_gen();

    // $display("[TOP] : AVTP common header name is %s, the value is 0x%x", avtp_common_hdr.name, avtp_common_hdr.subtype);
    // avtp_alter_pkt.avtp_packet_gen(pkt);


    // $display("[TOP] : ---------------------TEST CASE-IV------------------------------");
    // $display("[TOP] : Generating Random AVTP Packet");
    // avtp_random_pkt = new();
    
    // for (int i = 0; i < 100; i++) begin
    //   avtp_common_hdr = avtp_random_pkt.subtype_header_gen();
    //   avtp_random_pkt.avtp_packet_gen(pkt);
    // end

    $display("[TOP] : ---------------------TEST CASE-V------------------------------");
    $display("[TOP] : Generating ADP Packet");
    avtp_adp_pkt_gen = new();
    subtype = avtp_adp_pkt_gen.subtype_gen();
    avtp_common_hdr = avtp_adp_pkt_gen.subtype_header_gen();

    $display("[TOP] : AVTP common header name is %s, the value is 0x%x", avtp_common_hdr.name, avtp_common_hdr.subtype);
    avtp_adp_pkt = avtp_adp_pkt_gen.adp_packet_gen(pkt);
  
    for (int i = 0; i < pkt.size(); i++) begin
      $display("THE %dth value of the pkt is 0x%X", i, pkt[i]);
    end
    
  end
endmodule