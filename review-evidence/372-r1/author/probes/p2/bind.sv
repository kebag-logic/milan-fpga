bind dut chk u_chk (.clk(clk), .rst_n(rst_n), .a(a), .b(b), .y(y),
                    .idle_i(state == IDLE), .one_i(state == S_ONE), .two_i(state == S_TWO));
