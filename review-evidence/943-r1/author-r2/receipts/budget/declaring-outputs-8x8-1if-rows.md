# the arm's aecp-outputs rows and aecp-fanout's SET_STREAM_INFO row at 8x8/1if (table.md at a16899b1)
|---|---:|---|---:|---|---:|---:|---:|
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 2.780 (3.157) | fits | 0 aecp | 1 | 0 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice, completed, to every registration (#936, #943) | 0 | `aecp_outputs.declared.if0` (aecp-outputs) | 1.615 (1.867) | fits | 0 acmp | 1 | 0 |
| GET_STREAM_INFO_O0 of a declaring STREAM_OUTPUT | 0 | `aecp_outputs.get_stream_info.get_stream_info_o1.if0` (aecp-outputs) | 0.182 (0.645) | fits | 0 aecp | 9 | 0 |
| GET_STREAM_INFO of a declaring STREAM_OUTPUT behind a held egress | 0 | `aecp_outputs.held_get_stream_info.if0` (aecp-outputs) | 4.103 (4.482) | fits | 0 aecp | 1 | 0 |
| SET_STREAM_INFO of a declaring STREAM_OUTPUT, its notices past the AECP ring's room behind a held egress | 0 | `aecp_outputs.held_set_stream_info.if0` (aecp-outputs) | 9.138 (9.507) | fits | 0 aecp | 1 | 0 |
| SET_STREAM_INFO_STREAM_ID of a declaring STREAM_OUTPUT, refused NOT_SUPPORTED | 0 | `aecp_outputs.set_stream_info.set_stream_info_locked.if0` (aecp-outputs) | 0.194 (0.661) | fits | 0 aecp | 2 | 0 |
|---|---:|---:|---:|---:|---|---|
|---|---:|---:|---:|---|
|---|---:|---:|---:|
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 277,977 | 2.780 | 20 | 24 | fits | 60,881 | 77 | 0.614 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice, completed, to every registration (#936, #943) | `aecp_outputs.declared.if0` | 161,540 | 1.615 | 20 | 24 | fits | 44,982 | 60 | 0.509 |
| GET_STREAM_INFO_O0 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o0.if0` | 15,639 | 0.156 | 20 | 24 | fits | 38,408 | 18 | 0.815 |
| GET_STREAM_INFO_O1 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o1.if0` | 18,164 | 0.182 | 20 | 24 | fits | 37,824 | 18 | 0.808 |
| GET_STREAM_INFO_O2 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o2.if0` | 13,587 | 0.136 | 20 | 24 | fits | 36,573 | 18 | 0.778 |
| GET_STREAM_INFO_O3 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o3.if0` | 18,020 | 0.180 | 20 | 24 | fits | 37,647 | 18 | 0.811 |
| GET_STREAM_INFO_O4 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o4.if0` | 18,082 | 0.181 | 20 | 24 | fits | 37,391 | 18 | 0.803 |
| GET_STREAM_INFO_O5 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o5.if0` | 13,747 | 0.137 | 20 | 24 | fits | 36,773 | 18 | 0.783 |
| GET_STREAM_INFO_O6 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o6.if0` | 18,123 | 0.181 | 20 | 24 | fits | 37,814 | 18 | 0.807 |
| GET_STREAM_INFO_O7 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o7.if0` | 13,540 | 0.135 | 20 | 24 | fits | 36,596 | 18 | 0.783 |
| GET_STREAM_INFO_O8 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o8.if0` | 14,882 | 0.149 | 20 | 24 | fits | 37,715 | 18 | 0.807 |
| SET_STREAM_INFO_STREAM_ID of a declaring STREAM_OUTPUT, refused NOT_SUPPORTED | `aecp_outputs.set_stream_info.set_stream_info_stream_id.if0` | 18,271 | 0.183 | 20 | 24 | fits | 37,821 | 18 | 0.785 |
| SET_STREAM_INFO_LOCKED of a declaring STREAM_OUTPUT, refused ENTITY_LOCKED | `aecp_outputs.set_stream_info.set_stream_info_locked.if0` | 19,396 | 0.194 | 20 | 24 | fits | 38,109 | 18 | 0.794 |
| SET_STREAM_INFO of a declaring STREAM_OUTPUT, its notices past the AECP ring's room behind a held egress | `aecp_outputs.held_set_stream_info.if0` | 913,805 | 9.138 | 20 | 24 | fits | 29,445 | 20 | 0.625 |
| GET_STREAM_INFO of a declaring STREAM_OUTPUT behind a held egress | `aecp_outputs.held_get_stream_info.if0` | 410,346 | 4.103 | 20 | 24 | fits | 29,445 | 20 | 0.625 |
