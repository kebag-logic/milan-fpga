Scratch accounting of the #764 constant (addendum item 4).
RTL: KL_crf_tx.sv at dev e26f1816 (git show e26f1816:hdl/ieee1722/crf/KL_crf_tx.sv), KL_tdm_capture_master.sv and cdc_pulse.sv, cdc_pair_fifo.sv at the lane head (unchanged from e26f1816).
Build: verilator --cc --exe --build -j 2 -Wno-fatal -Wno-lint -Wno-style --top-module acct_wrap cdc_pulse.sv cdc_pair_fifo.sv KL_tdm_capture_master.sv KL_crf_tx_base.sv acct_wrap.sv acct.cpp -o Vacct
Clocks: audio 24.576 MHz x (1 - 10.64 ppm), datapath 50 MHz, one shared audio clock and reset, three reset-release phases.
