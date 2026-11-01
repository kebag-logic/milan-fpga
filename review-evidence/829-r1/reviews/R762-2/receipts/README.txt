R762-2 receipts. Absolute home paths in gptp_txts-all.log are replaced by <home> and <pinned LiteX>; nothing else was edited.
gptp_txts-all.log    make -C tb/verilator/gptp_txts on a clean copy of the head, pinned Verilator 5.050, pinned LiteX
gate_1h_cuts.log     scripts/gate_1h_cuts.py on a disposable copy of the head, committed gate unmodified
gate_1h_cuts_with_comment_strip.log   the same cuts, with a one-line comment strip added to the gate's reader in that disposable copy only
lint_commented_binding.*   lint_rtl.py --check with the tick binding line-commented, disposable copy
comment_only.log     scripts/comment_only.sh: changed RTL preprocessed and converted, parsed milan_soc.py
ax_export_ready_lines.txt  the ready flop, the two resets and the observer connection, from the head export
ax_export_compare.txt  AX7101 1x1 export at both heads: comments, blanks and each tree's own root removed; tcl differs only by the output path of read_verilog
spot_mutants.txt, spot/  scripts/spot_mutants.sh: independent planted defects on the closed-loop suite
hosted_*.txt         exact-head hosted job states as read during this review
final_clone_integrity.txt  the review clone after all probes
