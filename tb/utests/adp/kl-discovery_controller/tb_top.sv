module tb_top();

  parameter TDATA_WIDTH_P = 64;
  parameter T = 10;
  parameter MAX_BOUNDED_TALKER_CNT_C = 16;
  bit clk;
  bit rst_n;

  // Inputs
  logic [63:0] talker_entity_id;
  logic talker_entity_id_valid;
  logic talker_departed;
  logic rcv_adp_available;
  logic rcv_adp_departing;
  logic [63:0] rcv_entity_id;
  logic [31:0] rcv_available_index;
  logic [15:0] rcv_interface_index;
  logic [63:0] rcv_gptp_grandmaster_id;
  logic [7:0] rcv_gptp_domain_number;
  logic [4:0] rcv_valid_time;

  // Outputs 
  wire [31:0] available_index;
  wire [15:0] interface_index;
  wire [63:0] gptp_grandmaster_id;
  wire [7:0] gptp_domain_number;
  wire [4:0] valid_time;
  wire [MAX_BOUNDED_TALKER_CNT_C-1:0] active_talker_o;

  adp_discovery_event_t discovery_events;

  // Save the given/deleted talker entity ids to compare with DUT
  logic [MAX_BOUNDED_TALKER_CNT_C-1:0][63:0] bounded_talker_db;
  logic [MAX_BOUNDED_TALKER_CNT_C-1:0] active_talker;
  int number_of_talker;
  int status = 1;
  int random_number;

  KL_discovery_controller DUT
  (
    .clk_i(clk),
    .rst_n(rst_n),
    .talker_entity_id_i(talker_entity_id),
    .talker_entity_id_valid_i(talker_entity_id_valid),
    .talker_departed_i(talker_departed),
    .rcv_adp_available_i(rcv_adp_available),
    .rcv_adp_departing_i(rcv_adp_departing),
    .rcv_entity_id_i(rcv_entity_id),
    .rcv_available_index_i(rcv_available_index),
    .rcv_interface_index_i(rcv_interface_index),
    .rcv_gptp_grandmaster_id_i(rcv_gptp_grandmaster_id),
    .rcv_gptp_domain_number_i(rcv_gptp_domain_number),
    .rcv_valid_time_i(rcv_valid_time),
    .rcv_available_index_o(available_index),
    .rcv_interface_index_o(interface_index),
    .rcv_valid_time_o(valid_time),
    .rcv_gptp_grandmaster_id_o(gptp_grandmaster_id),
    .rcv_gptp_domain_number_o(gptp_domain_number),
    .active_talker_o(active_talker_o),
    .discovery_events(discovery_events)
  );

  always #(T/2) clk = ~clk;

  task reset_dut;
    #100;
    $display("[INFO][TOP] : Reseting the DUT");
    talker_entity_id = '0;
    talker_entity_id_valid = '0;
    talker_departed = '0;
    rcv_adp_available = '0;
    rcv_adp_departing = '0;
    rcv_entity_id = '0;
    rcv_available_index = '0;
    rcv_interface_index = '0;
    rcv_gptp_grandmaster_id = '0;
    rcv_gptp_domain_number = '0;
    rcv_valid_time = '0;
    bounded_talker_db = '0;
    active_talker = '0;
    rst_n = 1'd1;
  endtask

  // Give bounded talker id to be saved 
  task automatic give_talker;
    ref logic [63:0] talker_entity_id;
    ref logic talker_entity_id_valid;
    begin
      talker_entity_id = {$urandom, $urandom};
      @(posedge clk);
      talker_entity_id_valid = 1'd1;
      @(posedge clk);
      talker_entity_id_valid = 1'd0;
    end
  endtask
  
  // Delete a random-active bounded talker from database
  task automatic delete_talker;
    ref logic [63:0] talker_entity_id;
    ref logic talker_departed;
    ref logic [MAX_BOUNDED_TALKER_CNT_C-1:0] active_talker;
    ref logic [MAX_BOUNDED_TALKER_CNT_C-1:0][63:0] bounded_talker_db;
    begin
      int random_number;
      random_number = $urandom_range(0,MAX_BOUNDED_TALKER_CNT_C-1);

      while(!active_talker[random_number]) begin
        random_number = $urandom_range(0,MAX_BOUNDED_TALKER_CNT_C-1);
      end
      $display("[INFO][TOP][DELETE_TALKER] : The %dth talker will be deleted", random_number);
      // We found the random-active place
      talker_entity_id = bounded_talker_db[random_number];
      active_talker[random_number] = 1'd0;
      @(posedge clk);
      talker_departed = 1'd1;
      @(posedge clk);
      talker_departed = 1'd0;
    end
  endtask

  // Provide rcv_adp_available or rcv_adp_departing input with POSITIVE | NEGATIVE case
  // POSITIVE Case - Where the rcv_entity_id is one of the bounded_talker_id
  // NEGATIVE Case - Where the rcv_entity_id is not valid within bounded_talker_id
  task automatic give_adp_pkt;
    ref logic [63:0] rcv_entity_id;
    ref logic rcv_adp_available;
    ref logic rcv_adp_departing;
    ref logic [31:0] rcv_available_index;
    ref logic [15:0] rcv_interface_index;
    ref logic [63:0] rcv_gptp_grandmaster_id;
    ref logic [7:0] rcv_gptp_domain_number;    
    ref logic [4:0] rcv_valid_time;
    ref logic [MAX_BOUNDED_TALKER_CNT_C-1:0] active_talker;
    ref logic [MAX_BOUNDED_TALKER_CNT_C-1:0][63:0] bounded_talker_db;
    input string s;
    input string p;
    ref int random_number;
    begin
      #50;
      rcv_gptp_grandmaster_id = {$urandom, $urandom};
      rcv_gptp_domain_number = $urandom_range(0,255);
      rcv_available_index = $urandom;
      rcv_interface_index = $urandom_range(0,65535);
      rcv_valid_time = $urandom_range(0,31);

      $display("[INFO][TOP][GIVE_RCV_AVAILABLE] : %s TEST",s);
      if (s == "POSITIVE") begin
        random_number = $urandom_range(0,MAX_BOUNDED_TALKER_CNT_C-1);

        while(!active_talker[random_number]) begin
          random_number = $urandom_range(0,MAX_BOUNDED_TALKER_CNT_C-1);
        end
        rcv_entity_id = bounded_talker_db[random_number];
        $display("[INFO][TOP][GIVE_RCV_AVAILABLE] : Giving a entity_id equal to the bounded talker id %dth", random_number);
      end

      if (s == "NEGATIVE") begin
        rcv_entity_id = {$urandom, $urandom};
        for (int i = 0; i < MAX_BOUNDED_TALKER_CNT_C; i++) begin
          if (bounded_talker_db[i] == rcv_entity_id) begin
            rcv_entity_id = {$urandom, $urandom};
            i = 0;
          end
        end
      end
      if (p == "ADP_AVAILABLE") begin
        @(posedge clk);
        rcv_adp_available = 1'd1;
        @(posedge clk);
        rcv_adp_available = 1'd0;
      end
      else if (p == "ADP_DEPARTING") begin
        @(posedge clk);
        rcv_adp_departing = 1'd1;
        @(posedge clk);
        rcv_adp_departing = 1'd0;
      end
      else $fatal(1,"[FATAL][TOP][GIVE_RCV_AVAILABLE] : Wrong Packet Arguments Passed %s", p);
    end
  endtask;

  initial begin
    reset_dut();
    #100ns;


    // --------------------------------------------------------------------------- //
    $display("---------------------------------------------");
    $display("[INFO][TOP] : ------ TP.UT.DISCOVERY_CONTROLLER_0000 --------- ");
    $display("[INFO][TOP] : Randomly giving bounded talkers to the DUT");
    for (int i = 0; i < $urandom_range(3,15); i++) begin
      give_talker(talker_entity_id, talker_entity_id_valid);
      bounded_talker_db[i] = talker_entity_id;
      active_talker[i] = 1;
      #100ns;
    end
    $display("[INFO][TOP] : Deleting Two bounded talkers from Database");
    for (int i = 0; i < 2; i++) begin
      delete_talker(talker_entity_id, talker_departed, active_talker, bounded_talker_db);
      #100;
    end

    $display("[INFO][TOP] : Comparing database in TB vs Database in DUT");
    for (int i = 0; i < MAX_BOUNDED_TALKER_CNT_C; i++) begin
      if (active_talker[i]) begin
        if (bounded_talker_db[i] != DUT.bounded_talker_db_r[i])
          $fatal(1,"[FATAL][TOP] : TP.UT.DISCOVERY_CONTROLLER_0000 Failed");
      end
    end
    $display("[INFO][TOP] : TP.UT.DISCOVERY_CONTROLLER_0000 Succesfull");


    // --------------------------------------------------------------------------- //
    $display("---------------------------------------------");
    $display("[INFO][TOP] : ------ TP.UT.DISCOVERY_CONTROLLER_0001 --------- ");
    $display("[INFO][TOP] : Giving RCV_ADP_AVAILABLE input with CORRECT entity_id within Database");
    give_adp_pkt(rcv_entity_id, rcv_adp_available, rcv_adp_departing, rcv_available_index, rcv_interface_index,rcv_gptp_grandmaster_id,rcv_gptp_domain_number,rcv_valid_time, active_talker, bounded_talker_db, "POSITIVE", "ADP_AVAILABLE", random_number);
    @(posedge discovery_events.RCV_ADP_AVAILABLE[random_number]);
    $display("[INFO][TOP] : Comparing the output");
    status &= (rcv_available_index == available_index);
    status &= (rcv_interface_index == interface_index);
    status &= (rcv_gptp_grandmaster_id == gptp_grandmaster_id);
    status &= (rcv_gptp_domain_number == gptp_domain_number);
    status &= (rcv_valid_time == valid_time);
    if (!status)
      $fatal(1,"[FATAL][TOP] : TP.UT.DISCOVERY_CONTROLLER_0001 Failed");
    $display("[INFO][TOP] : TP.UT.DISCOVERY_CONTROLLER_0001 Succesfull");


    // --------------------------------------------------------------------------- //
    $display("---------------------------------------------");
    $display("[INFO][TOP] : ------ TP.UT.DISCOVERY_CONTROLLER_0002 --------- ");
    $display("[INFO][TOP] : Giving RCV_ADP_DEPARTING input with CORRECT entity_id within Database");
    give_adp_pkt(rcv_entity_id, rcv_adp_available, rcv_adp_departing, rcv_available_index, rcv_interface_index,rcv_gptp_grandmaster_id,rcv_gptp_domain_number,rcv_valid_time, active_talker, bounded_talker_db, "POSITIVE", "ADP_DEPARTING", random_number);
    $display("[INFO][TOP] : Comparing the output");
    @(posedge discovery_events.RCV_ADP_DEPARTING[random_number]);    
    status &= (rcv_available_index == available_index);
    status &= (rcv_interface_index == interface_index);
    status &= (rcv_gptp_grandmaster_id == gptp_grandmaster_id);
    status &= (rcv_gptp_domain_number == gptp_domain_number);
    status &= (rcv_valid_time == valid_time);
    if (!status)
      $fatal(1,"[FATAL][TOP] : TP.UT.DISCOVERY_CONTROLLER_0002 Failed");
    $display("[INFO][TOP] : TP.UT.DISCOVERY_CONTROLLER_0002 Succesfull");
    
    // --------------------------------------------------------------------------- //
    $display("---------------------------------------------");
    $display("[INFO][TOP] : ------ TP.UT.DISCOVERY_CONTROLLER_0003 --------- ");
    $display("[INFO][TOP] : Giving RCV_ADP_AVAILABLE input with WRONG entity_id within Database");
    give_adp_pkt(rcv_entity_id, rcv_adp_available, rcv_adp_departing, rcv_available_index, rcv_interface_index,rcv_gptp_grandmaster_id,rcv_gptp_domain_number,rcv_valid_time, active_talker, bounded_talker_db, "NEGATIVE", "ADP_AVAILABLE", random_number);

    fork
      begin
        // event must not occured, since entity id is not matched
        @(posedge discovery_events.RCV_ADP_AVAILABLE[random_number]);
        status = 0;
      end
      begin
        #1000ns;
        status = 1;
      end
    join_any

    if (!status) 
      $fatal(1,"[FATAL][TOP] : TP.UT.DISCOVERY_CONTROLLER_0003 Failed");
    $display("[INFO][TOP] : TP.UT.DISCOVERY_CONTROLLER_0003 Succesfull");

    // --------------------------------------------------------------------------- //
    $display("---------------------------------------------");
    $display("[INFO][TOP] : ------ TP.UT.DISCOVERY_CONTROLLER_0004 --------- ");
    $display("[INFO][TOP] : Giving RCV_ADP_DEPARTING input with WRONG entity_id within Database");
    give_adp_pkt(rcv_entity_id, rcv_adp_available, rcv_adp_departing, rcv_available_index, rcv_interface_index,rcv_gptp_grandmaster_id,rcv_gptp_domain_number,rcv_valid_time, active_talker, bounded_talker_db, "NEGATIVE", "ADP_DEPARTING",random_number);

    fork
      begin
        // event must not occured, since entity id is not matched
        @(posedge discovery_events.RCV_ADP_DEPARTING[random_number]);
        status = 0;
      end
      begin
        #1000ns;
        status = 1;
      end
    join_any

    if (!status) 
      $fatal(1,"[FATAL][TOP] : TP.UT.DISCOVERY_CONTROLLER_0004 Failed");
    $display("[INFO][TOP] : TP.UT.DISCOVERY_CONTROLLER_0004 Succesfull");
    $finish;
  end


  
endmodule