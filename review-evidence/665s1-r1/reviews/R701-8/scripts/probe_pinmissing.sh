#!/bin/bash
# Does build.mailbox_pins_missing parse a real Verilator PINMISSING report? A LiteX-shaped top
# leaves one KL_mbx input and one KL_mbx_wb output unconnected and one non-mailbox pin too;
# the parser must name exactly the two mailbox pins, under the pinned 5.050 and the PATH Verilator.
. "$(dirname "$0")/env.sh"
W=$PACKET/scratch/pinmissing; rm -rf "$W"; mkdir -p "$W/gateware"; cd "$W/gateware"
cat > sim.v <<'V'
module KL_mbx(input wire clk_i, input wire fw_ack_p_i, output wire fw_send_o);
  assign fw_send_o = clk_i ^ fw_ack_p_i;
endmodule
module KL_mbx_wb(input wire clk_i, output wire ack_o);
  assign ack_o = clk_i;
endmodule
module other(input wire a, output wire b);
  assign b = a;
endmodule
module sim(input wire clk, output wire y, output wire z);
KL_mbx KL_mbx(
	.clk_i(clk),
	.fw_send_o(y)
);
KL_mbx_wb KL_mbx_wb(
	.clk_i(clk)
);
other other(
	.b(z)
);
endmodule
V
for V in $VALIDATION_TOOLS/pinned-verilator-5.050/verilator verilator; do
  echo "== $($V --version)"
  $V --lint-only -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-MULTITOP --top-module sim "$W/gateware/sim.v" > "$W/verilate.log" 2>&1
  grep -c PINMISSING "$W/verilate.log"
  python3 -B -c "
import sys; sys.path.insert(0, '$CHECKOUT/tb/verilator/ctrl_service_budget')
from pathlib import Path; import build
got = build.mailbox_pins_missing(Path('$W/verilate.log').read_text(), Path('$W/gateware'))
want = ['KL_mbx.fw_ack_p_i', 'KL_mbx_wb.ack_o']
print('parsed', got, 'OK' if got == want else 'BAD (want %s)' % want)
"
done
