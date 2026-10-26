# the published ID takes slot 0's upper 48 bits for every slot (an output not following its slot)
OLD = "        {cfg_stream_id_i[g*64+16 +: 48],\n"
NEW = "        {cfg_stream_id_i[16 +: 48],\n"
