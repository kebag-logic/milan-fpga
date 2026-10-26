# the search ignores the moving source's own IDs (may take the withdrawn ID back)
OLD = "      if ((cfg_stream_id_i[j*64+16 +: 48] == mv_sid_w[63:16])\n"
NEW = "      if ((j != 32'(ev_src_r)) && (cfg_stream_id_i[j*64+16 +: 48] == mv_sid_w[63:16])\n"
