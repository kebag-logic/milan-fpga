| Tool | Role | SHA-256 |
|---|---|---|
| `b2_action.py` | acquisition: one locked capture and controller action | `b38b34cd816ea3b54bdcbe517e95137aec4b942323f2aacaee1bf7e740278a0b` |
| `run_action.sh` | bench-lock wrapper for one action | `77ca9d6448bf9a400594c775e1788b7642933765dc803cdc3daf5cfac27488bb` |
| `series.sh` | cycle series, one lock window per cycle | `d314a982b566e132545c30551342d919128d3b1971f5c050a6a0d49f6d718cbd` |
| `identity_locked.sh` | identity readback and UART grader under the lock | `0facac30157c813ad21f5a869dc9f31d9a0313f53346ef9d2cacf67539d03090` |
| `b2_analyze.py` | offline replay of one capture | `22a010930831c5bdb0a27240dd09e3decb3cef96dc1991390caa2ad3cadbee14` |
| `b2_summary.py` | distributions, growth and stop classes | `c7c753aaa156b7a2ef1552dbbcdec32f5ea24e1efb99377fb1d98e322cde725c` |
| `b2_pages.py` | page tables from the summary | `1e3412ff9ab6a4ba5d6f25c4c1865e1a92811d7bffafec9cf70bdfbe84bb8382` |
| `b2_assemble.py` | page assembly from the tables | `876016dfe28f7017d1a074092f6bb1136ee18265d66f8a86d0c0c63a60737067` |
| `aecp_identity.py` | ENTITY and CONFIGURATION byte comparison | `5e9ddcc669c1ab846413fff18d622f1fd2c87b51f99b4a5c0a0249438a0ef2f2` |
| `b2_reconnect.py` | controller transactions for the one pair | `3c86cf246fea8fd1736f42904dfff342d367eea98bcf302f328b75ca6b8d4b4c` |
| `b2_controller.py` | controller reads; PR #604 copy, import renamed | `29a3d493ba3c82b6618aef9dfd1a940057857230a7315d63a6cbf1c11a2beb51` |
| `avdecc_ro.py` | raw AVDECC reader, unchanged from PR #604 | `172836966609645d6e12adf19a8341a145a4dadc51edb81c6d29a23aae1fd75a` |
| `capture.py` | bounded tap capture, unchanged from PR #604 | `2601b03e16c0caa7c13f170a7316d7262a9f9bc4cc265dcba881165364a1fb61` |
| `console_read.py` | read-only console reader, unchanged from PR #604 | `652d6f839b1dff74c5ddbdfc4fc9fd42c250f0cd2b7e2eeeb5b7cc838a74ee63` |
| `wire_summary.py` | tap decoder, unchanged from PR #604 | `7a8af475fa5f8bfbb90636b92bf9d07a86140c54a9be10c12f9b76235bccd922` |
| `expected_crc.py` | reference CRC table, unchanged from PR #604 | `04d128bb0a9ffe8ad5898f4ece380899a096a1595aadda3ece1048c313bf19d7` |
| `census_compare.py` | census comparison, unchanged from PR #620 | `f014c6f2bd80e4622960c76dba3c908299357f8c9fcc03097441750d40d8db79` |
| [UART grader](../../scripts/baremetal_uart_smoke.py) at `13eda870` | identity and restore | `bc41ab03e64198b10a517124f960b9b59b77d7143661f728fe5666314e433886` |
