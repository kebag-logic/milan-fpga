Vivado out-of-context synthesis, xc7a100tfgg484-2, AreaOptimized_high, one block per report.
servo: CLK_FREQ_HZ_P=50000000. mtt_round: N_P=2, BASE_HZ_P=48000. crf_tx_applied: ROUND_MTT_P=0.
The third run of the 44508dd8 batch (crf_tx with its default ROUND_MTT_P) inherited the previous
run's generic inside the same Vivado session, so it is not kept; crf_tx_round1_converter is the
module with its converter, as every round-1 build had it.
Slice LUTs / Slice Registers / DSPs:
  servo   f1fda3f1 1233 / 1006 / 0    b23e9e31 (dx form) 1384 / 1026 / 0    f1643214 1342 / 1026 / 0
  mtt_round multiplier form 122 / 155 / 1    44508dd8 182 / 190 / 0
  crf_tx with converter 404 / 298 / 1        ROUND_MTT_P=0 246 / 169 / 0
