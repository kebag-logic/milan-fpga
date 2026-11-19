# the arm's aecp-outputs rows and aecp-fanout's SET_STREAM_INFO row at 1x1/1if (table.md at a16899b1)
|---|---:|---|---:|---|---:|---:|---:|
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 3.297 (3.580) | fits | 0 aecp | 1 | 0 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice, completed, to every registration (#936, #943) | 0 | `aecp_outputs.declared.if0` (aecp-outputs) | 1.337 (1.386) | fits | 0 acmp | 1 | 0 |
| GET_STREAM_INFO_O0 of a declaring STREAM_OUTPUT | 0 | `aecp_outputs.get_stream_info.get_stream_info_o0.if0` (aecp-outputs) | 0.264 (0.611) | fits | 0 aecp | 2 | 0 |
| GET_STREAM_INFO of a declaring STREAM_OUTPUT behind a held egress | 0 | `aecp_outputs.held_get_stream_info.if0` (aecp-outputs) | 4.068 (4.392) | fits | 0 aecp | 1 | 0 |
| SET_STREAM_INFO of a declaring STREAM_OUTPUT, its notices past the AECP ring's room behind a held egress | 0 | `aecp_outputs.held_set_stream_info.if0` (aecp-outputs) | 9.104 (9.408) | fits | 0 aecp | 1 | 0 |
| SET_STREAM_INFO_STREAM_ID of a declaring STREAM_OUTPUT, refused NOT_SUPPORTED | 0 | `aecp_outputs.set_stream_info.set_stream_info_stream_id.if0` (aecp-outputs) | 0.268 (0.613) | fits | 0 aecp | 2 | 0 |
|---|---:|---:|---:|---:|---|---|
|---|---:|---:|---:|---|
|---|---:|---:|---:|
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 329,694 | 3.297 | 20 | 24 | fits | 58,492 | 78 | 0.612 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice, completed, to every registration (#936, #943) | `aecp_outputs.declared.if0` | 133,680 | 1.337 | 20 | 24 | fits | 41,217 | 60 | 0.524 |
| GET_STREAM_INFO_O0 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o0.if0` | 26,385 | 0.264 | 20 | 24 | fits | 35,023 | 18 | 0.809 |
| GET_STREAM_INFO_O1 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o1.if0` | 21,454 | 0.215 | 20 | 24 | fits | 32,050 | 18 | 0.765 |
| SET_STREAM_INFO_STREAM_ID of a declaring STREAM_OUTPUT, refused NOT_SUPPORTED | `aecp_outputs.set_stream_info.set_stream_info_stream_id.if0` | 26,816 | 0.268 | 20 | 24 | fits | 33,898 | 18 | 0.775 |
| SET_STREAM_INFO_LOCKED of a declaring STREAM_OUTPUT, refused ENTITY_LOCKED | `aecp_outputs.set_stream_info.set_stream_info_locked.if0` | 23,961 | 0.240 | 20 | 24 | fits | 33,962 | 18 | 0.788 |
| SET_STREAM_INFO of a declaring STREAM_OUTPUT, its notices past the AECP ring's room behind a held egress | `aecp_outputs.held_set_stream_info.if0` | 910,446 | 9.104 | 20 | 24 | fits | 23,327 | 20 | 0.647 |
| GET_STREAM_INFO of a declaring STREAM_OUTPUT behind a held egress | `aecp_outputs.held_get_stream_info.if0` | 406,815 | 4.068 | 20 | 24 | fits | 23,327 | 20 | 0.647 |
