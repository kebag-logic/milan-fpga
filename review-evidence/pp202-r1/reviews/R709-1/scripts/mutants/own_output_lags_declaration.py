# the published ID follows a move only once the moved ID is declared
OLD = "         sid_ovr_v_r[g] ? sid_ovr_r[g] : cfg_stream_id_i[g*64 +: 16]};\n"
NEW = "         (sid_ovr_v_r[g] && sid_used_r[g]) ? sid_ovr_r[g] : cfg_stream_id_i[g*64 +: 16]};\n"
