# PROBE_TX answers SUCCESS before the grant (DA validity ignored)
OLD = "  assign da_ok_w      = rec_w.da_valid && !pe_conflict_r[tsrc_w];\n"
NEW = "  assign da_ok_w      = !pe_conflict_r[tsrc_w];\n"
