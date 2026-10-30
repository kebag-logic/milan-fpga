Confirmation of the [A10] cause (issuecomment-6518083444) by test.
Clone of 787-reboot-reset at 0d4be94ca859dbb596b0ffa78dca376c925392d4 (unfixed RTL), with the new tb/verilator/pp_shadow/sim_main.cpp
from the fix commit, minus its two references to RTL the unfixed head lacks (harness-applied.diff):
  - dut->i_ethtxend_tgl (the new datapath input) not driven
  - KL_reboot_ctrl stop_r read as false
and reboot_probes.vlt gaining the maap_tx_tvalid probe.
Commands (in the clone, tb/verilator/pp_shadow):
  make --no-print-directory build-base BUILD_DIR=<scratch>/obj-confirm   (rc 0)
  <scratch>/obj-confirm/Vpp_shadow_sim --reboot-only                     (rc 1: 69 checks, 10 failures)
rb-at-0d4be94c-committed-harness.log: the committed [RB] at 0d4be94c (38 checks, PASS: it grades the datapath port only).
