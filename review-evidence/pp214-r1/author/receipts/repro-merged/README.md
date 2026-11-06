The merged testbench (tb/ byte-identical to the head) against the RTL before the fix: the head's tree with main
92100657's hdl/srp/KL_srp_encoder.sv, the only file under hdl/ that differs. tb/srp_top reads 8683 checks: 8675 PASS,
8 FAIL (OV0 to OV7; OV0: 69 of 17650 frames carry a value twice). tb/srp_encoder reads 692 checks: 644 PASS, 48 FAIL.
