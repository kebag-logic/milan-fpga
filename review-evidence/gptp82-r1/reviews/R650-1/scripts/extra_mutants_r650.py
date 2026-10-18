# Reviewer probe mutants for the #82 boot commit (exec'd by
# run_engine_mutants_parallel.py --extra). Each is a disposable fault in a
# scratch copy of the head RTL; `breaks` names what the reviewer expects.
EXTRA = [
    ("R650 boot commit ignores a running handler", "top/KL_gptp_engine.sv",
     "      if (boot_pub_pend_r && local_clock_valid_r && !dbg_busy_o) begin",
     "      if (boot_pub_pend_r && local_clock_valid_r) begin",
     "(probe: is the idle guard graded?)"),
    ("R650 boot commit fires before thisClock is known", "top/KL_gptp_engine.sv",
     "      if (boot_pub_pend_r && local_clock_valid_r && !dbg_busy_o) begin",
     "      if (boot_pub_pend_r && !dbg_busy_o) begin",
     "#82 cold boot: first commit names thisClock"),
    ("R650 boot commit never retires", "top/KL_gptp_engine.sv",
     "        boot_pub_pend_r   <= 1'b0;\n        boot_pub_commit_r <= 1'b1;",
     "        boot_pub_commit_r <= 1'b1;",
     "(probe: is a repeated engine commit graded?)"),
    ("R650 a microcode commit does not cancel the boot commit", "top/KL_gptp_engine.sv",
     "      end else if (ucpu_commit_w) begin\n        boot_pub_pend_r <= 1'b0;\n      end",
     "      end",
     "(probe: is the cancel branch graded?)"),
    ("R650 self path count ignores clock validity", "top/KL_gptp_engine.sv",
     "  assign pub_path_count_o = pub_gm_self_w ? {3'd0, local_clock_valid_r}",
     "  assign pub_path_count_o = pub_gm_self_w ? 4'd1",
     "(probe: count 1 with GM 0 before the first beat)"),
    ("R650 self path keeps the raw tail", "top/KL_gptp_engine.sv",
     "  assign pub_path_o       = pub_gm_self_w ? '0 : pub_path_r;",
     "  assign pub_path_o       = pub_path_r;",
     "#82 warm reset: first commit path is {thisClock}"),
]
