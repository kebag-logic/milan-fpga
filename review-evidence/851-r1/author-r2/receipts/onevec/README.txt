Scratch clone of the lane at e44a4d20 with the [ONEVEC] check (the committed bb9f0a06 content, idiom-fixed), pinned Verilator 5.050.
planted-never-merges: a copy of the processor hdl/ tree with KL_srp_encoder.sv line `assign sr_hit_w    = sr_cont_w && (q_key_w == sr_key_r);` replaced by `assign sr_hit_w    = 1'b0;`, built with make crflic-build PP_DIR=<copy>.
probe-encoder-92100657: the same, with KL_srp_encoder.sv taken from processor 92100657 (git show), not a committed arm.
campaign-arm-run_pp_mutant: crflic_mutants.run_pp_mutant over PP_MUTATIONS, the committed campaign's own code path.
